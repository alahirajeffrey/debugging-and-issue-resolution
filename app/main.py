from flask import Flask, g
from app.logger import setup_logger
from app.utils.correlation import correlation_middleware
from app.routes.health import health_bp
from app.metrics import setup_metrics
from app.tracer import setup_tracing
from app.config import Config


def create_app():
    setup_logger()

    app = Flask(__name__)

    setup_tracing(app)
    setup_metrics(app)

    @app.before_request
    def before_request():
        correlation_middleware()

    @app.after_request
    def after_request(response):
        response.headers["X-Correlation-ID"] = g.correlation_id
        return response

    app.register_blueprint(health_bp)

    return app


if __name__ == "__main__":
    app = create_app()

    debug = Config.ENV == "development"

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=debug,
    )
