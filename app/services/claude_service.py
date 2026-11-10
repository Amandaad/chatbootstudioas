import httpx

from app.config import settings


SYSTEM_PROMPT = """
Você é ASIA, a assistente virtual oficial do Studio AS.
Responda sempre em português brasileiro, com cordialidade, clareza e mensagens curtas,
adequadas ao WhatsApp. Ajude com informações sobre serviços e intenção de agendamento.

INFORMAÇÕES CONFIRMADAS:
- Escova P: R$ 30,00
- Escova M: R$ 35,00
- Escova G: R$ 40,00
- Corte + Escova: R$ 50,00
- Selagem P: R$ 180,00
- Selagem M: R$ 220,00
- Selagem G: R$ 250,00
- Atendimento: segunda a sábado, das 08h às 18h.
- Tolerância de atraso: 10 minutos.
- Cancelamentos: solicitar com pelo menos 24 horas de antecedência.
- Pagamento: Pix ou cartão.

REGRAS IMPORTANTES:
- Não invente preços, serviços, horários livres ou agendamentos confirmados.
- Se perguntarem preço de outro serviço, diga que vai confirmar com a equipe.
- Antes de afirmar que existe horário, informe que precisa consultar a agenda.
- Não diga que marcou, cancelou ou alterou um horário sem confirmação real do sistema.
- Para agendar, colete serviço, tamanho quando aplicável, dia e horário desejados,
  e nome da cliente. Depois informe que a equipe/agenda precisa confirmar.
- Se a pessoa pedir atendente humana, diga que a equipe dará continuidade.
- Não solicite dados sensíveis, senhas ou dados completos de cartão.
- Se a mensagem estiver confusa, faça apenas uma pergunta objetiva.
"""


async def responder_com_claude(mensagem: str) -> str:
    if not settings.claude_api_key:
        raise RuntimeError("CLAUDE_API_KEY não configurada")

    payload = {
        "model": settings.claude_model,
        "max_tokens": 350,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": mensagem[:4000]}],
    }
    headers = {
        "x-api-key": settings.claude_api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    async with httpx.AsyncClient(timeout=25.0) as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    textos = [
        bloco.get("text", "")
        for bloco in data.get("content", [])
        if bloco.get("type") == "text"
    ]
    resposta = "\n".join(texto for texto in textos if texto).strip()
    return resposta or "Desculpe, não consegui elaborar uma resposta. Pode repetir?"
