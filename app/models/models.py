from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from app.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    instagram_id = Column(String(120), unique=True, nullable=True)
    telefone = Column(String(30), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)


class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    descricao = Column(String(500), nullable=True)
    preco = Column(Float, nullable=False)


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, nullable=False)
    servico_id = Column(Integer, nullable=False)
    data_hora = Column(DateTime, nullable=False)
    status = Column(String(30), default="pendente")
