# Google Agenda — Studio AS

## 1. Criar credenciais
1. No Google Cloud Console, crie/selecione um projeto.
2. Ative a **Google Calendar API**.
3. Crie uma conta de serviço e baixe o JSON da chave.
4. Compartilhe a agenda do Studio AS com o e-mail da conta de serviço, dando permissão para **fazer alterações nos eventos**.
5. Guarde o JSON fora do Git. Nunca o envie para o repositório.

## 2. Variáveis de ambiente
Adicione ao arquivo local `.env` (não versionar):
```env
GOOGLE_CALENDAR_CREDENTIALS_FILE=/caminho/seguro/google-service-account.json
GOOGLE_CALENDAR_ID=seu_email_ou_id_da_agenda
APP_TIMEZONE=America/Fortaleza
```
No Docker, monte o arquivo de credenciais como um secret/volume somente leitura e configure o caminho visto pelo contêiner.

## 3. Atualizar o banco existente
Faça backup antes. Execute uma vez:
```bash
psql "$DATABASE_URL" -f migrations/20261013_add_google_event_id.sql
```
O comando adiciona o identificador do evento Google aos agendamentos existentes. Não execute migrações de produção sem backup.

## 4. Instalar dependências e iniciar
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 5. Testar
Consulte `/docs` no servidor local. Use uma data futura, durante o horário de atendimento (segunda a sábado, 08h–18h, horário de Fortaleza). O endpoint de disponibilidade não cria eventos. O endpoint de criação só confirma após criar o evento Google e persistir a reserva no banco.

- `POST /agendamentos/disponibilidade`
- `POST /agendamentos`

Exemplo de corpo:
```json
{
  "cliente_nome": "Cliente de teste",
  "cliente_instagram_id": "ID_REAL_OU_DE_TESTE",
  "servico_id": 1,
  "inicio": "2026-10-15T10:00:00-03:00"
}
```

A duração inicial é inferida pelo nome do serviço no código e usa 60 minutos como padrão. Ajuste `DURACOES_MINUTOS` em `app/routers/agendamentos.py` aos tempos reais do salão. A verificação externa do Google Calendar e a checagem no banco ajudam a evitar conflitos; para operação concorrente em escala, implemente uma restrição transacional de sobreposição no PostgreSQL e idempotência de reservas.

## Observações
- A API do Google Agenda fica protegida por credenciais de conta de serviço.
- A integração não envia mensagens ao Instagram por si só; o webhook da Meta deve chamar este fluxo e enviar a resposta através da Messaging API.
- Nunca confirme ao cliente antes do sucesso da gravação no Google Agenda e no PostgreSQL.
