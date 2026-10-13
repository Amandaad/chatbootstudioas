from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Studio AS Meta Bot"
    app_env: str = "development"

    database_url: str
    meta_verify_token: str
    meta_access_token: str = ""
    meta_app_secret: str = ""
    meta_page_id: str = ""
    meta_instagram_id: str = ""

    google_calendar_credentials_file: str = ""
    google_calendar_id: str = ""
    app_timezone: str = "America/Fortaleza"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
