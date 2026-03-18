from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized settings with secure defaults for internal deployment."""

    app_name: str = "Subject Intel API"
    environment: str = "dev"
    database_url: str = "postgresql+psycopg://subject:subject@localhost:5432/subjectdb"
    jwt_secret: str = "change-me-in-prod"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 30
    refresh_token_minutes: int = 1440
    object_storage_endpoint: str = "https://object-storage.internal"
    object_storage_bucket: str = "subject-photos"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="SUBJECT_")


settings = Settings()
