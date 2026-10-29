
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MediMind AI"
    app_environment: str = "development"
    api_prefix: str = "/api"

    knowledge_base_path: str = "data/knowledge_base.json"
    upload_directory: str = "uploads"
    max_upload_mb: int = 10

    aws_region: str = "ap-south-1"
    bedrock_model_id: str = ""
    use_bedrock: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
