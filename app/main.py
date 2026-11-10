from fastapi import FastAPI

from app.database import Base, engine
from app.models.models import Cliente, Servico, Agendamento
from app.services.chatbot import responder, menu
from app.routers.webhook_meta import router as webhook_meta_router
from app.routers.webhook_twilio import router as webhook_twilio_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Studio AS - Atendimento Inteligente",
    version="1.1.0"
)

app.include_router(webhook_meta_router)
app.include_router(webhook_twilio_router)


@app.get("/")
def home():
    return {
        "projeto": "Studio AS - ASIA",
        "status": "online",
        "canais": ["Instagram", "WhatsApp Twilio"]
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/menu")
def get_menu():
    return {"menu": menu()}


@app.post("/chat")
def chat(data: dict):
    mensagem = data.get("mensagem", "")
    return {
        "mensagem": mensagem,
        "resposta": responder(mensagem)
    }
