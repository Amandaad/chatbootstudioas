from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse

from app.config import settings
from app.services.chatbot import responder

router = APIRouter(prefix="/webhook", tags=["Meta"])


@router.get("/meta")
async def verificar_webhook(
    hub_mode: str | None = None,
    hub_verify_token: str | None = None,
    hub_challenge: str | None = None
):
    if (
        hub_mode == "subscribe"
        and hub_verify_token == settings.meta_verify_token
    ):
        return PlainTextResponse(hub_challenge or "")

    return PlainTextResponse("Token inválido", status_code=403)


@router.post("/meta")
async def receber_webhook(request: Request):
    data = await request.json()

    print("WEBHOOK META:")
    print(data)

    return {
        "status": "received",
        "message": "Webhook recebido pelo Studio AS"
    }


@router.post("/teste-chat")
async def teste_chat(request: Request):
    data = await request.json()
    mensagem = data.get("mensagem", "")

    return {
        "mensagem": mensagem,
        "resposta": responder(mensagem)
    }
