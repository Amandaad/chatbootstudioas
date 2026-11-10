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


---

## 📲 Integração com WhatsApp via Twilio

O projeto também possui um endpoint para receber mensagens do WhatsApp pela Twilio.

### Endpoint

`POST /webhook/twilio`

Configure esse endereço como webhook de mensagens recebidas no Sandbox do WhatsApp ou no número WhatsApp habilitado na Twilio. O endpoint:

1. Valida o cabeçalho `X-Twilio-Signature` usando o Auth Token da conta.
2. Lê os campos `From` e `Body` enviados pela Twilio.
3. Encaminha o texto para o serviço existente `responder()`.
4. Devolve a resposta em TwiML para a Twilio enviar ao cliente.

### Variáveis de ambiente

Copie `.env.example` para `.env` e preencha os valores reais:

- `TWILIO_AUTH_TOKEN`: Auth Token da conta Twilio (mantenha em segredo).
- `TWILIO_WEBHOOK_URL`: URL pública exata cadastrada na Twilio, por exemplo `https://seu-dominio/webhook/twilio`.

Não envie o arquivo `.env` para o GitHub.

### Dependências adicionadas

- `twilio`: validação da assinatura e geração da resposta TwiML.
- `python-multipart`: leitura segura dos dados de formulário recebidos no webhook.

### Configuração no Console Twilio

1. Ative o WhatsApp Sandbox ou conecte um remetente WhatsApp aprovado.
2. Em **When a message comes in**, informe a URL pública `https://seu-dominio/webhook/twilio`.
3. Se estiver usando Cloudflare Tunnel, mantenha o túnel ativo e configure a mesma URL em `TWILIO_WEBHOOK_URL`.
4. Envie uma mensagem de teste para o número WhatsApp disponibilizado pela Twilio.

> O webhook está integrado ao fluxo de respostas atual do chatbot. A confirmação de horários e a criação de eventos no Google Agenda ainda precisam ser conectadas ao fluxo de agendamento antes de oferecer reservas reais pelo WhatsApp.
