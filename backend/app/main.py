from flask import Flask

from app.api.v1.router import api_router
from app.core.config import settings
from app.api.v1.utils import close_db, register_error_handlers


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        APP_NAME=settings.app_name,
        APP_ENV=settings.app_env,
        DEBUG=settings.debug,
        VERSION="0.1.0",
    )

    from flask_cors import CORS

    CORS(app, origins=settings.cors_origins, supports_credentials=True)
    app.register_blueprint(api_router, url_prefix=settings.api_prefix)
    app.teardown_appcontext(close_db)
    register_error_handlers(app)

    @app.get("/")
    def root() -> dict[str, str]:
        return {
            "service": settings.app_name,
            "environment": settings.app_env,
            "status": "ok",
        }

    return app


app = create_app()
