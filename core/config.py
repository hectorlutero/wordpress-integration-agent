import os
import logging
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """
    Agent Settings configuration using Pydantic Settings.
    Reads from .env file or environment variables.
    """
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # WordPress Settings
    WP_URL: str
    WP_USERNAME: str
    WP_APP_PASSWORD: str
    
    # GA4 Settings
    GA4_PROPERTY_ID: Optional[str] = None
    GA4_CREDENTIALS_PATH: Optional[str] = None
    
    # Agent Logic
    LOG_LEVEL: str = "INFO"
    REPORT_OUTPUT_DIR: str = "data"

    @property
    def reports_path(self) -> Path:
        path = BASE_DIR / self.REPORT_OUTPUT_DIR
        path.mkdir(parents=True, exist_ok=True)
        return path

# Instantiate settings
try:
    settings = Settings()
except Exception as e:
    # If .env is missing or invalid, we handle it gracefully for local dev
    print(f"Warning: Could not load settings from .env: {e}")
    # In a real environment, you might want to exit if mandatory vars are missing
    settings = None

def setup_logging():
    """Configures the agent logging."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper() if settings else "INFO")
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
