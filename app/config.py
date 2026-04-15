from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "SSR Group Backend"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me-in-production"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./ssr_group.db"

    # CORS
    CORS_ORIGINS: str = "https://ssrgroupcivil.in,http://localhost:3000,http://localhost:8000"

    # SMTP Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "SSR Group"
    SMTP_FROM_EMAIL: str = "info@ssrgroupcivil.in"

    # Admin
    ADMIN_EMAIL: str = "info@ssrgroupcivil.in"

    # WhatsApp
    WHATSAPP_PHONE: str = "918796138550"

    # HubSpot CRM
    HUBSPOT_ACCESS_TOKEN: str = ""
    HUBSPOT_BASE_URL: str = "https://api.hubapi.com"
    HUBSPOT_LIFECYCLE_STAGE: str = "lead"
    HUBSPOT_LEAD_STATUS: str = "NEW"
    HUBSPOT_FORM_TYPE_PROPERTY: str = ""
    HUBSPOT_DETAILS_PROPERTY: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
