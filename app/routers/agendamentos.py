from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.models import Agendamento, Cliente, Servico
from app.services.google_calendar import (
    create_event,
    delete_event,
    freebusy,
)

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

# Ajuste estes tempos conforme a duração real dos serviços no Studio AS.
DURACOES_MINUTOS = {
    "escova": 45,
    "corte + escova": 60,
    "selagem": 180,
    "mechas": 180,
    "cílios": 90,
    "micropigmentação": 120,
    "depilação": 30,
}


class AgendamentoInput(BaseModel):
    cliente_nome: str = Field(min_length=2, max_length=120)
    cliente_instagram_id: str | None = Field(default=None, max_length=120)
    servico_id: int = Field(gt=0)
    inicio: datetime


class DisponibilidadeInput(BaseModel):
    servico_id: int = Field(gt=0)
    inicio: datetime


def _intervalo(inicio: datetime, servico: Servico) -> tuple[datetime, datetime, datetime, datetime]:
    tz = ZoneInfo(settings.app_timezone)
    if inicio.tzinfo is None:
        inicio = inicio.replace(tzinfo=tz)
    else:
        inicio = inicio.astimezone(tz)

    duracao = DURACOES_MINUTOS.get(servico.nome.strip().lower(), 60)
    fim = inicio + timedelta(minutes=duracao)
    return inicio, fim, inicio.astimezone(ZoneInfo("UTC")), fim.astimezone(ZoneInfo("UTC"))


def _validar_horario(inicio: datetime, fim: datetime) -> None:
    tz = ZoneInfo(settings.app_timezone)
    local_inicio = inicio.astimezone(tz)
    local_fim = fim.astimezone(tz)

    if local_inicio <= datetime.now(tz):
        raise HTTPException(status_code=422, detail="Escolha uma data e horário futuros.")
    if local_inicio.weekday() == 6:
        raise HTTPException(status_code=422, detail="O Studio AS atende de segunda a sábado.")
    if local_inicio.date() != local_fim.date():
        raise HTTPException(status_code=422, detail="O serviço precisa terminar no mesmo dia.")
    if local_inicio.hour < 8 or local_fim.hour > 18 or (
        local_fim.hour == 18 and local_fim.minute > 0
    ):
        raise HTTPException(status_code=422, detail="Escolha um horário entre 08h e 18h.")


def _checar_disponibilidade(db: Session, inicio: datetime, fim: datetime,
                            inicio_utc: datetime, fim_utc: datetime) -> None:
    _validar_horario(inicio, fim)

    # Verifica a agenda do Google, incluindo eventos criados fora do sistema.
    ocupados = freebusy(inicio_utc.isoformat(), fim_utc.isoformat())
    if any(
        datetime.fromisoformat(item["start"].replace("Z", "+00:00")) < fim_utc
        and datetime.fromisoformat(item["end"].replace("Z", "+00:00")) > inicio_utc
        for item in ocupados
    ):
        raise HTTPException(status_code=409, detail="Esse horário já está ocupado. Escolha outro.")

    # Verifica também reservas ativas registradas no banco local.
    reservas = (
        db.query(Agendamento, Servico)
        .join(Servico, Servico.id == Agendamento.servico_id)
        .filter(Agendamento.status.in_(["pendente", "confirmado"]))
        .all()
    )
    for reserva, servico_existente in reservas:
        existente_inicio = reserva.data_hora
        if existente_inicio.tzinfo is None:
            existente_inicio = existente_inicio.replace(tzinfo=ZoneInfo(settings.app_timezone))
        existente_fim = existente_inicio + timedelta(
            minutes=DURACOES_MINUTOS.get(servico_existente.nome.strip().lower(), 60)
        )
        if existente_inicio.astimezone(ZoneInfo("UTC")) < fim_utc and existente_fim.astimezone(ZoneInfo("UTC")) > inicio_utc:
            raise HTTPException(status_code=409, detail="Já existe uma reserva nesse intervalo.")


@router.post("/disponibilidade")
def verificar_disponibilidade(payload: DisponibilidadeInput, db: Session = Depends(get_db)):
    servico = db.query(Servico).filter(Servico.id == payload.servico_id).first()
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")

    inicio, fim, inicio_utc, fim_utc = _intervalo(payload.inicio, servico)
    _checar_disponibilidade(db, inicio, fim, inicio_utc, fim_utc)
    return {
        "disponivel": True,
        "servico": servico.nome,
        "inicio": inicio.isoformat(),
        "fim": fim.isoformat(),
        "mensagem": "Horário disponível. A reserva ainda não foi criada.",
    }


@router.post("")
def criar_agendamento(payload: AgendamentoInput, db: Session = Depends(get_db)):
    servico = db.query(Servico).filter(Servico.id == payload.servico_id).first()
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")

    inicio, fim, inicio_utc, fim_utc = _intervalo(payload.inicio, servico)
    _checar_disponibilidade(db, inicio, fim, inicio_utc, fim_utc)

    cliente = None
    if payload.cliente_instagram_id:
        cliente = db.query(Cliente).filter(
            Cliente.instagram_id == payload.cliente_instagram_id
        ).first()
    if cliente:
        cliente.nome = payload.cliente_nome
    else:
        cliente = Cliente(
            nome=payload.cliente_nome,
            instagram_id=payload.cliente_instagram_id,
        )
        db.add(cliente)
        db.flush()

    event_id = None
    try:
        event_id = create_event(
            summary=f"Studio AS — {servico.nome} — {payload.cliente_nome}",
            description=(
                f"Cliente: {payload.cliente_nome}\n"
                f"Serviço: {servico.nome}\n"
                f"Origem: Instagram"
            ),
            start_iso=inicio.isoformat(),
            end_iso=fim.isoformat(),
        )
        reserva = Agendamento(
            cliente_id=cliente.id,
            servico_id=servico.id,
            data_hora=inicio.replace(tzinfo=None),
            status="confirmado",
            google_event_id=event_id,
        )
        db.add(reserva)
        db.commit()
        db.refresh(reserva)
    except Exception as exc:
        db.rollback()
        if event_id:
            try:
                delete_event(event_id)
            except Exception:
                pass
        if isinstance(exc, HTTPException):
            raise
        raise HTTPException(
            status_code=502,
            detail="Não foi possível concluir a reserva. Verifique a agenda e tente novamente.",
        ) from exc

    return {
        "id": reserva.id,
        "status": "confirmado",
        "servico": servico.nome,
        "inicio": inicio.isoformat(),
        "fim": fim.isoformat(),
        "google_event_id": event_id,
        "mensagem": "Agendamento confirmado no Studio AS.",
    }
