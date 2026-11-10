import logging

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from app.config import settings
from app.services.chatbot import responder

router = APIRouter(prefix="/webhook", tags=["Twilio WhatsApp"])
logger = logging.getLogger(__name__)


@router.post("/twilio")
async def receber_mensagem_whatsapp(request: Request):
    """
    Recebe mensagens do WhatsApp encaminhadas pela Twilio e responde
    com TwiML. A assinatura X-Twilio-Signature é validada antes do
    processamento para impedir chamadas falsas ao webhook.
    """
    if not settings.twilio_auth_token:
        raise HTTPException(
            status_code=503,
            detail="Integração Twilio não configurada no servidor."
        )

    form = await request.form()
    signature = request.headers.get("X-Twilio-Signature", "")
    webhook_url = settings.twilio_webhook_url or str(request.url)

    validator = RequestValidator(settings.twilio_auth_token)
    if not validator.validate(webhook_url, form, signature):
        raise HTTPException(status_code=403, detail="Assinatura Twilio inválida.")

    mensagem = str(form.get("Body", "")).strip()
    remetente = str(form.get("From", "")).strip()

    if not mensagem or not remetente.startswith("whatsapp:"):
        raise HTTPException(status_code=400, detail="Mensagem WhatsApp inválida.")

    # Não registrar conteúdo nem telefone do cliente nos logs.
    resposta_texto = responder(mensagem)

    twiml = MessagingResponse()
    twiml.message(resposta_texto)

    return Response(
        content=str(twiml),
        media_type="application/xml",
        status_code=200
    )
