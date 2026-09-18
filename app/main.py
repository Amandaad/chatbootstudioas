from fastapi import FastAPI
from app.services.chatbot import responder, menu

app = FastAPI(
    title="Studio AS - Instagram Chatbot",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "projeto": "Studio AS Instagram Bot",
        "status": "online"
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
