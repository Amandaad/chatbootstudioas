SERVICOS = {
    "1": ("Selagem", "P R$180 | M R$220 | G R$250"),
    "2": ("Mechas", "Preço sob consulta com a equipe"),
    "3": ("Corte + Escova", "R$50"),
    "4": ("Escova", "P R$30 | M R$35 | G R$40"),
    "5": ("Cílios", "Preço sob consulta com a equipe"),
    "6": ("Micropigmentação", "Preço sob consulta com a equipe"),
    "7": (
        "Depilação",
        "Preço sob consulta com a equipe"
    ),
}


def menu():
    return """💖 Bem-vinda ao Studio AS!

Como posso ajudar?

1️⃣ Selagem
2️⃣ Mechas
3️⃣ Corte + Escova
4️⃣ Escova
5️⃣ Cílios
6️⃣ Micropigmentação
7️⃣ Depilação
8️⃣ Falar com atendente"""


def responder(mensagem: str):
    mensagem = mensagem.strip().lower()

    if mensagem in ("oi", "olá", "ola", "menu", "inicio", "início"):
        return menu()

    if mensagem in SERVICOS:
        nome, preco = SERVICOS[mensagem]
        return f"""✨ {nome}

Valores: {preco}

Qual dia você gostaria de agendar? 📅"""

    if mensagem in ("8", "atendente", "humano"):
        return "💕 Claro! Vou encaminhar você para uma atendente do Studio AS."

    return "Não entendi. 😊\n\n" + menu()
