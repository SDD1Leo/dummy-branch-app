from flask import Blueprint, jsonify
import logging
from sqlalchemy import text
from app.db import engine

bp = Blueprint("health", __name__)

@bp.route("/health", methods=["GET"])
def health():
    try:
        # SQLAlchemy 2.0 compatible health check
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        logging.info("Health check OK")
        return jsonify({"status": "ok"})

    except Exception as e:
        logging.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "error"}), 500
