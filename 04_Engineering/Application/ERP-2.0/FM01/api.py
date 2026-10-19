"""Flask adapter for the FM-01 GET-only reference API."""

from __future__ import annotations

from typing import Any, Mapping

from flask import Blueprint, Flask, jsonify, request

from .repository import RESOURCE_TABLES, ReferenceRepository, synthetic_repository


_RESOURCE_KEYS = {
    "legal-entities": ("legal_entity_id", "legal_entity_ref"),
    "companies": ("company_id", "company_ref"),
    "sites": ("site_id", "site_ref"),
    "plants": ("plant_id", "plant_ref"),
    "warehouses": ("warehouse_id", "warehouse_ref"),
    "locations": ("location_id", "location_ref"),
}
_RELATION_KEYS = {
    "company": ("legal_entity_id",),
    "site": ("company_id",),
    "plant": ("site_id",),
    "warehouse": ("site_id", "plant_id"),
    "location": ("warehouse_id", "parent_location_id"),
}


def _error(code: str, message: str, status: int):
    return jsonify({"error": {"code": code, "message": message}}), status


def _parse_int(value: str | None, name: str) -> int | None:
    if value is None or value == "":
        return None
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if parsed < 1:
        raise ValueError(f"{name} must be positive")
    return parsed


def _public_row(table: str, row: Mapping[str, Any]) -> dict[str, Any]:
    id_key, ref_key = next(keys for path, keys in _RESOURCE_KEYS.items() if RESOURCE_TABLES[path] == table)
    result = {
        id_key: row.get(id_key),
        ref_key: row.get(ref_key),
        "display_name": row.get("display_name"),
    }
    for relation_key in _RELATION_KEYS.get(table, ()):
        result[relation_key] = row.get(relation_key)
    return result


def create_blueprint(repository: ReferenceRepository | None = None) -> Blueprint:
    """Create the FM-01 route surface for composition into an ERP app."""

    blueprint = Blueprint("fm01", __name__)
    repo = repository or synthetic_repository()

    @blueprint.get("/api/v1/fm01/<resource>")
    def collection(resource: str):
        if resource not in RESOURCE_TABLES:
            return _error("UNSUPPORTED_RESOURCE", "resource is outside the FM-01 allowlist", 422)
        try:
            row_id = _parse_int(request.args.get("id"), "id")
            row_ref = request.args.get("ref")
            if row_id is not None and row_ref:
                return _error("INVALID_PARAMETER", "id and ref cannot be combined", 400)
            limit = _parse_int(request.args.get("limit", "50"), "limit") or 50
            offset = _parse_int(request.args.get("offset", "1"), "offset") or 1
            if limit > 100:
                return _error("INVALID_PARAMETER", "limit must not exceed 100", 400)
            if offset < 1:
                return _error("INVALID_PARAMETER", "offset must be positive", 400)
        except ValueError as exc:
            return _error("INVALID_PARAMETER", str(exc), 400)

        table = RESOURCE_TABLES[resource]
        rows = list(repo.list_rows(table))
        id_key, ref_key = _RESOURCE_KEYS[resource]
        if row_id is not None:
            rows = [row for row in rows if row.get(id_key) == row_id]
        elif row_ref:
            rows = [row for row in rows if row.get(ref_key) == row_ref]
        rows = sorted(rows, key=lambda row: (row.get(id_key) is None, row.get(id_key)))
        if (row_id is not None or row_ref) and not rows:
            return _error("NOT_FOUND", "reference was not found", 404)
        page = rows[offset - 1:offset - 1 + limit]
        return jsonify({
            "data": [_public_row(table, row) for row in page],
            "meta": {"resource": resource, "offset": offset, "limit": limit, "count": len(page), "total": len(rows)},
        })

    @blueprint.get("/api/v1/fm01/hierarchy")
    def hierarchy():
        return jsonify({
            "data": {
                "legal_entities": [_public_row("legal_entity", row) for row in repo.list_rows("legal_entity")],
                "companies": [_public_row("company", row) for row in repo.list_rows("company")],
                "sites": [_public_row("site", row) for row in repo.list_rows("site")],
                "plants": [_public_row("plant", row) for row in repo.list_rows("plant")],
                "warehouses": [_public_row("warehouse", row) for row in repo.list_rows("warehouse")],
                "locations": [_public_row("location", row) for row in repo.list_rows("location")],
            }
        })

    return blueprint


def create_app(repository: ReferenceRepository | None = None) -> Flask:
    """Create an isolated app with the composed FM-01 route surface."""

    app = Flask(__name__)
    app.register_blueprint(create_blueprint(repository))
    return app
