"""FM02 C2 routes registered in the main Flask application."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, current_app, jsonify, request

from app.api.v1.utils import get_db
from app.services.fm02_c2 import build_c2_service


router = Blueprint("fm02_c2", __name__)


def _service() -> Any:
    """Return an injected test service or the production session-bound service."""

    configured_service = current_app.config.get("FM02_C2_SERVICE")
    if configured_service is not None:
        return configured_service
    return build_c2_service(get_db())


@router.post("/items/<item_id>/customer-qualifications")
def create_customer_qualification(item_id: str):
    result = _service().create_customer_qualification(
        item_id,
        request.get_json(silent=True) or {},
        request.headers.get("X-Correlation-ID"),
    )
    return jsonify(result), result["status"]


@router.post("/items/<item_id>/uom-conversions")
def create_conversion_rule(item_id: str):
    result = _service().create_conversion_rule(
        item_id,
        request.get_json(silent=True) or {},
        request.headers.get("X-Correlation-ID"),
    )
    return jsonify(result), result["status"]


@router.get("/items/<item_id>/uom-conversions/<from_item_uom_id>/<to_item_uom_id>")
def resolve_conversion(item_id: str, from_item_uom_id: str, to_item_uom_id: str):
    result = _service().resolve_conversion(
        item_id,
        from_item_uom_id,
        to_item_uom_id,
        request.args.get("effective_at"),
    )
    return jsonify(result), result["status"]
