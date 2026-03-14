"""Application settings — loaded from environment variables.

Updated for MemoriaOS (Gemini + GCP).
"""

from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings and configuration.

    Loads and validates configuration from environment variables and .env file.
    All attributes are automatically populated from matching env vars.
    """

    # All application configuration, loaded from .env or environment.

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Required ──────────────────────────────────────────────────────────
    google_api_key: SecretStr = Field(description="Google AI API Key for Gemini")

    # ── Cloud Run / GCP (Core Data) ─────────────────────────────────────────
    gcp_project_id: str = Field(default="my-tele-pa", description="Google Cloud Project ID")
    bq_dataset_id: str = Field(default="memoria_os_prod", description="BigQuery Dataset ID")
    gcs_bucket_name: str | None = Field(default=None, description="Bucket for media storage")

    # ── Optional: Notion ──────────────────────────────────────────────────
    enable_notion: bool = Field(default=False)
    notion_api_key: SecretStr | None = Field(default=None)
    
    # Per-domain page IDs (G1 gap fix)
    notion_wellness_page_id: str | None = Field(default=None)
    notion_finance_page_id: str | None = Field(default=None)
    notion_fitness_page_id: str | None = Field(default=None)
    notion_recipes_page_id: str | None = Field(default=None)
    notion_tasks_page_id: str | None = Field(default=None)

    # ── LLM ────────────────────────────────────────────────────────────────
    gemini_model: str = Field(default="gemini-2.5-flash")
    gemini_temperature: float = Field(default=0.1, ge=0.0, le=2.0)

    # ── App ────────────────────────────────────────────────────────────────
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="console")  # 'console' | 'json'
    timezone: str = Field(default="Europe/London")

    # ── Integrations ───────────────────────────────────────────────────────
    google_photos_client_id: str | None = Field(default=None)
    google_photos_client_secret: SecretStr | None = Field(default=None)


settings = Settings()  # type: ignore
