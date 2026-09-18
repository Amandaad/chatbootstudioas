from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Studio AS Meta Bot"
    app_env: str = "development"

    database_url: str

    meta_verify_token: str
    meta_access_token: str = ""
    meta_app_secret: str = ""
    meta_page_id: str = ""
    meta_instagram_id: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
