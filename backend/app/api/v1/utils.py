from typing import Any

from flask import current_app, g, jsonify, request
from pydantic import BaseModel, ValidationError

from app.core.exceptions import ApiError
from app.db.session import SessionLocal


def get_db():
    test_session = current_app.config.get("TEST_DB_SESSION")
    if test_session is not None:
        return test_session

    if "db_session" not in g:
        g.db_session = SessionLocal()
    return g.db_session


def close_db(error: BaseException | None = None) -> None:
    db = g.pop("db_session", None)
    if db is not None:
        db.close()


def parse_pagination() -> tuple[int, int]:
    skip = max(int(request.args.get("skip", 0)), 0)
    limit = min(max(int(request.args.get("limit", 50)), 1), 200)
    return skip, limit


def parse_body(schema: type[BaseModel]) -> BaseModel:
    return schema.model_validate(request.get_json(silent=True) or {})


def to_jsonable(data: Any) -> Any:
    if isinstance(data, BaseModel):
        return data.model_dump(mode="json")
    if isinstance(data, list):
        return [to_jsonable(item) for item in data]
    if isinstance(data, dict):
        return {key: to_jsonable(value) for key, value in data.items()}
    return data


def json_response(data: Any, status_code: int = 200):
    if status_code == 204:
        return "", 204
    return jsonify(to_jsonable(data)), status_code


def register_error_handlers(app) -> None:
    @app.errorhandler(ApiError)
    def handle_api_error(error: ApiError):
        return jsonify({"detail": error.detail}), error.status_code

    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        return jsonify({"detail": error.errors()}), 422
