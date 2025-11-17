from flask import Flask, request, g
from .config import Config, configure_logging
from .metrics import REQUEST_COUNT, REQUEST_LATENCY, ERROR_COUNT
import time
import uuid


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    configure_logging(app.config["LOG_LEVEL"])

    # Assign request ID
    @app.before_request
    def before():
        g.request_id = str(uuid.uuid4())
        g.start_time = time.time()

    @app.after_request
    def after(response):
        latency = time.time() - g.start_time

        endpoint = request.endpoint or "unknown"

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()

        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)

        if response.status_code >= 400:
            ERROR_COUNT.labels(
                endpoint=endpoint,
                status=response.status_code
            ).inc()

        return response

    # Import routes
    from .routes.health import bp as health_bp
    from .routes.loans import bp as loans_bp
    from .routes.stats import bp as stats_bp
    from .routes.metrics import bp as metrics_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(loans_bp, url_prefix="/api")
    app.register_blueprint(stats_bp, url_prefix="/api")
    app.register_blueprint(metrics_bp)

    return app
