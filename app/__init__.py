from flask import Flask, g
from .config import Config, configure_logging
import uuid


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    configure_logging(app.config["LOG_LEVEL"])

    @app.before_request
    def attach_request_id():
        g.request_id = str(uuid.uuid4())

    from .routes.health import bp as health_bp
    from .routes.loans import bp as loans_bp
    from .routes.stats import bp as stats_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(loans_bp, url_prefix="/api")
    app.register_blueprint(stats_bp, url_prefix="/api")

    return app
