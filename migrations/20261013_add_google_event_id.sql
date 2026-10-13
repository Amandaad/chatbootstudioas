-- Execute uma vez no banco existente antes de publicar esta versão.
ALTER TABLE agendamentos
ADD COLUMN IF NOT EXISTS google_event_id VARCHAR(255);
