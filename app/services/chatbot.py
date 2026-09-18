SERVICOS = {
    "1": ("Selagem", "P R$150 | M R$200 | G R$250"),
    "2": ("Mechas", "P R$150 | M R$200 | G R$250"),
    "3": ("Corte + Escova", "R$50"),
    "4": ("Escova", "P R$25 | M R$30 | G R$35"),
    "5": ("Cílios", "R$70"),
    "6": ("Micropigmentação", "R$250"),
    "7": (
        "Depilação",
        "Axila R$20 | Meia perna R$20 | "
        "Perna completa R$40 | Buço R$10 | Face R$50"
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
