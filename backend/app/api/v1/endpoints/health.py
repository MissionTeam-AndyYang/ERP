from flask import Blueprint, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.db.session import engine

router = Blueprint("health", __name__)


@router.get("")
def health_check():
    return jsonify(
        {
            "status": "ok",
            "service": settings.app_name,
            "environment": settings.app_env,
        }
    )


@router.get("/db")
def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        return jsonify(
            {
                "status": "error",
                "database": "unreachable",
                "detail": exc.__class__.__name__,
            }
        )

    return jsonify(
        {
            "status": "ok",
            "database": "reachable",
        }
    )
