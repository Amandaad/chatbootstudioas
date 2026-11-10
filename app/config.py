from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Studio AS Meta Bot"
    app_env: str = "development"

    database_url: str
    meta_verify_token: str = ""
    meta_access_token: str = ""
    meta_app_secret: str = ""
    meta_page_id: str = ""
    meta_instagram_id: str = ""

    # Claude (Anthropic)
    claude_api_key: str = ""
    claude_model: str = "claude-haiku-5-5"

    # Twilio WhatsApp
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_whatsapp_from: str = "whatsapp:+14155238886"
    twilio_webhook_url: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
