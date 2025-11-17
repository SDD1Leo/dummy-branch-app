import os
import logging
import json

class Config:
    # Environment
    ENV: str = os.getenv("ENV", "development")

    # Logging level (CRITICAL FIX)
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

    # Application port
    PORT: int = int(os.getenv("PORT", "8000"))

    # Database URL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@db:5432/branchdb"
    )


class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "level": record.levelname,
            "message": record.getMessage(),
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
        })


def configure_logging(log_level: str):
    handler = logging.StreamHandler()
    if log_level.lower() == "json":
        handler.setFormatter(JSONFormatter())

    logging.basicConfig(level=log_level.upper(), handlers=[handler])
