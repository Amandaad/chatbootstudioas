from urllib.parse import parse_qs
import logging
import xml.etree.ElementTree as ET

from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.request_validator import RequestValidator

from app.config import settings
from app.services.claude_service import responder_com_claude
from app.services.chatbot import responder as responder_local

router = APIRouter(prefix="/webhook/twilio", tags=["WhatsApp Twilio"])
logger = logging.getLogger(__name__)


def _twiml(texto: str) -> Response:
    root = ET.Element("Response")
    message = ET.SubElement(root, "Message")
    message.text = texto
    xml = ET.tostring(root, encoding="unicode")
    return Response(content='<?xml version="1.0" encoding="UTF-8"?>' + xml,
                    media_type="application/xml")


async def _validar_assinatura(request: Request, form_data: dict) -> bool:
    # Em produção, configure TWILIO_AUTH_TOKEN e TWILIO_WEBHOOK_URL.
    if not settings.twilio_auth_token:
        return settings.app_env.lower() != "production"

    url = settings.twilio_webhook_url
    if not url:
        logger.error("TWILIO_WEBHOOK_URL ausente; não é possível validar assinatura.")
        return False

    validator = RequestValidator(settings.twilio_auth_token)
    signature = request.headers.get("X-Twilio-Signature", "")
    return validator.validate(url, form_data, signature)


@router.get("/health")
async def whatsapp_health():
    return {
        "channel": "whatsapp",
        "provider": "twilio",
        "status": "ready",
        "claude_configured": bool(settings.claude_api_key),
    }


@router.post("/incoming")
async def whatsapp_incoming(request: Request):
    raw_body = (await request.body()).decode("utf-8", errors="replace")
    parsed = parse_qs(raw_body, keep_blank_values=True)
    form_data = {key: values[0] for key, values in parsed.items()}

    if not await _validar_assinatura(request, form_data):
        return Response(status_code=403, content="Assinatura Twilio inválida")

    mensagem = form_data.get("Body", "").strip()
    if not mensagem:
        return _twiml("Olá! 💖 Sou a ASIA, assistente virtual do Studio AS. Como posso ajudar?")

    try:
        if settings.claude_api_key:
            resposta = await responder_com_claude(mensagem)
        else:
            resposta = responder_local(mensagem)
    except Exception:
        logger.exception("Falha ao processar mensagem recebida pelo WhatsApp.")
        resposta = (
            "Oi! 💖 Tive uma instabilidade momentânea. "
            "Pode repetir sua mensagem ou pedir para falar com nossa equipe?"
        )

    return _twiml(resposta[:1500])
