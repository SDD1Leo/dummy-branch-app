import os
import logging
import json
from datetime import datetime
from flask import request, g   # <-- FIXED: added g

class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    PORT = int(os.getenv("PORT", "8000"))
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@db:5432/branchdb"
    )
    LOG_LEVEL = os.getenv("LOG_LEVEL", "info")


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # Safe request context logging
        try:
            log.update({
                "request_id": getattr(g, "request_id", None),
                "method": request.method,
                "path": request.path,
                "remote_addr": request.remote_addr,
            })
        except RuntimeError:
            pass

        return json.dumps(log)


def configure_logging(level: str):
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    root = logging.getLogger()
    root.setLevel(level.upper())
    root.handlers = [handler]
