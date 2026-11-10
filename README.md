# 💇‍♀️ Studio AS — Instagram Chatbot

Chatbot desenvolvido em **Python + FastAPI** para atendimento automatizado do **Studio AS** através do Instagram, com preparação para integração com **Meta Ads**, agendamentos e banco de dados.

🔗 **GitHub:** https://github.com/Amandaad/chatbootstudioas

---

## 🎯 Objetivo

O projeto tem como objetivo automatizar o primeiro atendimento dos clientes do Studio AS através do Instagram.

O chatbot apresenta os serviços disponíveis, informa preços, identifica o interesse do cliente e prepara o fluxo para agendamento.

A aplicação foi desenvolvida com arquitetura preparada para integração com a **Instagram Messaging API da Meta**.

---

## 💬 Serviços

O chatbot possui atendimento para:

- ✨ Selagem
- 🎨 Mechas
- ✂️ Corte + Escova
- 💨 Escova
- 👁️ Cílios
- ✍️ Micropigmentação
- 🧴 Depilação

### Valores configurados

| Serviço | Valor |
|---|---:|
| Selagem P | R$ 150 |
| Selagem M | R$ 200 |
| Selagem G | R$ 250 |
| Mechas P | R$ 150 |
| Mechas M | R$ 200 |
| Mechas G | R$ 250 |
| Corte + Escova | R$ 50 |
| Escova P | R$ 25 |
| Escova M | R$ 30 |
| Escova G | R$ 35 |
| Cílios | R$ 70 |
| Micropigmentação | R$ 250 |
| Depilação Axila | R$ 20 |
| Depilação Meia Perna | R$ 20 |
| Depilação Perna Completa | R$ 40 |
| Depilação Buço | R$ 10 |
| Depilação Face | R$ 50 |

---

## 🧠 Fluxo do chatbot

```text
Cliente
   │
   ▼
Instagram
   │
   ▼
Meta Ads
   │
   ▼
Mensagem
   │
   ▼
Webhook
   │
   ▼
FastAPI
   │
   ▼
Chatbot Python
   │
   ├── Selagem
   ├── Mechas
   ├── Corte + Escova
   ├── Escova
   ├── Cílios
   ├── Micropigmentação
   └── Depilação
   │
   ▼
Agendamento


## 📲 WhatsApp com Twilio + ASIA (Claude)

O projeto agora possui um webhook de entrada para WhatsApp:

- Endpoint: `POST /webhook/twilio/incoming`
- Verificação: `GET /webhook/twilio/health`
- Resposta ao WhatsApp: TwiML XML
- IA: Anthropic Claude Haiku 5.5
- Fallback: atendimento local em Python se a chave Claude ainda não estiver configurada.

### Variáveis de ambiente

Copie `.env.example` para `.env` e preencha os valores reais. Nunca envie ou faça commit do arquivo `.env`.

```env
CLAUDE_API_KEY=sua_chave_anthropic
CLAUDE_MODEL=claude-haiku-5-5
TWILIO_AUTH_TOKEN=seu_auth_token
TWILIO_WEBHOOK_URL=https://SEU-TUNEL/webhook/twilio/incoming
APP_ENV=development
```

Mantenha também as variáveis já utilizadas pelo projeto, especialmente `DATABASE_URL`.
Em produção, configure obrigatoriamente `TWILIO_AUTH_TOKEN` e `TWILIO_WEBHOOK_URL` para validar a assinatura das chamadas da Twilio.

### Configuração inicial pelo WhatsApp Sandbox

1. No Console da Twilio, abra **Messaging > Try it out > Send a WhatsApp message** e ative o Sandbox.
2. No WhatsApp do celular, envie a mensagem de adesão (`join ...`) para o número do Sandbox indicado no Console.
3. Inicie a API no WSL/Docker e exponha a porta 8000 com um túnel HTTPS.
4. No campo **When a message comes in** do Sandbox, configure a URL pública terminando em `/webhook/twilio/incoming`, com método **POST**.
5. Envie uma mensagem de teste ao número do Sandbox.

O Sandbox é apenas para testes. Para atendimento público com o número comercial do Studio AS, será necessário concluir a ativação do remetente WhatsApp na Twilio e os requisitos da Meta.

### Observações

- O webhook responde diretamente com TwiML; não é necessário fazer uma chamada de saída separada para responder à mensagem recebida.
- A integração inicial não consulta nem grava horários no Google Agenda. A ASIA coleta a intenção de agendamento, mas não confirma reservas até a integração de disponibilidade ser concluída.
- A conversa ainda não mantém histórico entre mensagens. A persistência de contexto por cliente será uma próxima etapa.
