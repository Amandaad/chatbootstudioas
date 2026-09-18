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
