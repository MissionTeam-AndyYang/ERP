"""Bounded FM-02 Sprint-01 Item Master DEV API.

This module intentionally contains no Product/SKU behavior, no lifecycle
transition endpoint, and no operational Source-of-Truth behavior.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import string
import uuid
from datetime import datetime, timezone
from typing import Any, Callable

import pymysql
from flask import Flask, jsonify, request
from pymysql.err import IntegrityError


ALLOWED_CATEGORIES = {"RAW", "MATERIAL", "FILM", "WIP", "FG"}
ALPHANUM = string.ascii_uppercase + string.digits
REQUIRED_FIELDS = ("primary_category", "display_name", "ownership_context", "base_uom_code")


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def stable_fingerprint(payload: dict[str, Any]) -> str:
    canonical = {
        "primary_category": str(payload["primary_category"]).strip().upper(),
        "display_name": str(payload["display_name"]).strip(),
        "ownership_context": str(payload["ownership_context"]).strip(),
        "base_uom_code": str(payload["base_uom_code"]).strip().upper(),
        "specification_summary": str(payload.get("specification_summary", "")).strip(),
        "specification_reference": str(payload.get("specification_reference", "")).strip(),
    }
    return hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest().upper()


class ItemService:
    def __init__(self, connection_factory: Callable[[], Any]):
        self.connection_factory = connection_factory

    def generate_item_code(self) -> str:
        return "".join(secrets.choice(ALPHANUM) for _ in range(12))

    def _validate(self, payload: dict[str, Any]) -> list[dict[str, str]]:
        errors: list[dict[str, str]] = []
        for field in REQUIRED_FIELDS:
            if not str(payload.get(field, "")).strip():
                errors.append({"field": field, "message": "required"})
        category = str(payload.get("primary_category", "")).strip().upper()
        if category and category not in ALLOWED_CATEGORIES:
            errors.append({"field": "primary_category", "message": "unsupported bounded category"})
        uom = str(payload.get("base_uom_code", "")).strip().upper()
        if uom and len(uom) > 3:
            errors.append({"field": "base_uom_code", "message": "must be a bounded UOM code"})
        if "lifecycle_status" in payload and str(payload["lifecycle_status"]).upper() != "DRAFT":
            errors.append({"field": "lifecycle_status", "message": "Create API permits DRAFT only"})
        for forbidden in ("item_id", "item_code"):
            if payload.get(forbidden):
                errors.append({"field": forbidden, "message": "system generated and not client-selectable"})
        aliases = payload.get("legacy_references", [])
        if aliases is not None and not isinstance(aliases, list):
            errors.append({"field": "legacy_references", "message": "must be a list"})
        return errors

    def create_item(self, payload: dict[str, Any], correlation_id: str | None = None) -> dict[str, Any]:
        errors = self._validate(payload)
        if errors:
            return {"ok": False, "status": 400, "errors": errors}

        normalized = dict(payload)
        normalized["primary_category"] = str(payload["primary_category"]).strip().upper()
        normalized["base_uom_code"] = str(payload["base_uom_code"]).strip().upper()
        for attempt in range(5):
            item_id = str(uuid.uuid4())
            item_code = self.generate_item_code()
            now = utc_now()
            connection = self.connection_factory()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT uom_code FROM uom WHERE uom_code=%s AND lifecycle_status='ACTIVE'", (normalized["base_uom_code"],))
                    if cursor.fetchone() is None:
                        connection.rollback()
                        return {"ok": False, "status": 400, "errors": [{"field": "base_uom_code", "message": "unknown or inactive UOM"}]}
                    cursor.execute(
                        """INSERT INTO item
                        (item_id,item_code,primary_category,display_name,description,ownership_context,
                         base_uom_code,lifecycle_status,specification_summary,specification_reference,
                         identity_fingerprint,created_at,updated_at,correlation_id,provenance_note)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,'DRAFT',%s,%s,%s,%s,%s,%s,%s)""",
                        (item_id, item_code, normalized["primary_category"], str(payload["display_name"]).strip(),
                         str(payload.get("description", "")).strip(), str(payload["ownership_context"]).strip(),
                         normalized["base_uom_code"], str(payload.get("specification_summary", "")).strip(),
                         str(payload.get("specification_reference", "")).strip(), stable_fingerprint(normalized),
                         now, now, correlation_id, "FM-02 SPRINT-01 DEV / non-operational synthetic implementation"),
                    )
                    for alias in payload.get("legacy_references", []) or []:
                        if not isinstance(alias, dict) or not all(str(alias.get(k, "")).strip() for k in ("legacy_system", "legacy_entity", "legacy_code")):
                            connection.rollback()
                            return {"ok": False, "status": 400, "errors": [{"field": "legacy_references", "message": "each alias needs system, entity and code"}]}
                        cursor.execute(
                            """INSERT INTO item_legacy_identifier
                            (legacy_reference_id,item_id,legacy_system,legacy_entity,legacy_code,alias_role,provenance_ref,created_at)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                            (str(uuid.uuid4()), item_id, str(alias["legacy_system"]).strip(), str(alias["legacy_entity"]).strip(),
                             str(alias["legacy_code"]).strip(), str(alias.get("alias_role", "LEGACY_REFERENCE")).strip(),
                             "FM-02 SPRINT-01 DEV alias / non-authoritative", now),
                        )
                connection.commit()
                return {"ok": True, "status": 201, "item": self.get_item(item_id, connection=connection)["item"]}
            except IntegrityError as exc:
                connection.rollback()
                if getattr(exc, "args", [None])[0] == 1062 and attempt < 4:
                    continue
                return {"ok": False, "status": 409, "errors": [{"field": "database", "message": "duplicate or conflicting bounded identity"}]}
            finally:
                connection.close()
        return {"ok": False, "status": 409, "errors": [{"field": "item_code", "message": "safe code generation retries exhausted"}]}

    def get_item(self, item_id: str | None = None, item_code: str | None = None, connection: Any | None = None) -> dict[str, Any]:
        own = connection is None
        connection = connection or self.connection_factory()
        try:
            with connection.cursor() as cursor:
                if item_id:
                    cursor.execute("SELECT * FROM item WHERE item_id=%s", (item_id,))
                elif item_code:
                    cursor.execute("SELECT * FROM item WHERE item_code=%s", (item_code,))
                else:
                    return {"ok": False, "status": 400, "errors": [{"field": "item_id/item_code", "message": "lookup required"}]}
                row = cursor.fetchone()
                if row is None:
                    return {"ok": False, "status": 404, "errors": [{"field": "lookup", "message": "item not found"}]}
                item = self._row(cursor, row)
                cursor.execute("SELECT legacy_system,legacy_entity,legacy_code,alias_role,provenance_ref FROM item_legacy_identifier WHERE item_id=%s ORDER BY legacy_code", (item["item_id"],))
                item["legacy_references"] = [self._row(cursor, alias) for alias in cursor.fetchall()]
                return {"ok": True, "status": 200, "item": item}
        finally:
            if own:
                connection.close()

    def list_items(self, category: str | None = None, lifecycle_status: str | None = None) -> dict[str, Any]:
        connection = self.connection_factory()
        try:
            clauses: list[str] = []
            params: list[str] = []
            if category:
                clauses.append("primary_category=%s")
                params.append(category.upper())
            if lifecycle_status:
                clauses.append("lifecycle_status=%s")
                params.append(lifecycle_status.upper())
            query = "SELECT * FROM item" + ((" WHERE " + " AND ".join(clauses)) if clauses else "") + " ORDER BY created_at,item_id"
            with connection.cursor() as cursor:
                cursor.execute(query, tuple(params))
                return {"ok": True, "status": 200, "items": [self._row(cursor, row) for row in cursor.fetchall()]}
        finally:
            connection.close()

    @staticmethod
    def _row(cursor: Any, row: Any) -> dict[str, Any]:
        if isinstance(row, dict):
            return {key: (value.isoformat(sep=" ") if isinstance(value, datetime) else value) for key, value in row.items()}
        return {description[0]: value.isoformat(sep=" ") if isinstance(value, datetime) else value for description, value in zip(cursor.description, row)}


def build_app(service: ItemService | None = None) -> Flask:
    app = Flask(__name__)
    if service is None:
        service = ItemService(lambda: pymysql.connect(
            host=os.environ.get("FM02_DB_HOST", "127.0.0.1"),
            port=int(os.environ.get("FM02_DB_PORT", "3344")),
            user=os.environ["FM02_DB_USER"],
            password=os.environ["FM02_DB_PASSWORD"],
            database=os.environ.get("FM02_DB_NAME", "erp2_functional_dev_001"),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
        ))
    @app.post("/api/v1/items")
    def create_item():
        result = service.create_item(request.get_json(silent=True) or {}, request.headers.get("X-Correlation-ID"))
        return jsonify(result), result["status"]

    @app.get("/api/v1/items/<item_id>")
    def get_item(item_id: str):
        result = service.get_item(item_id=item_id)
        return jsonify(result), result["status"]

    @app.get("/api/v1/items")
    def list_items():
        result = service.list_items(request.args.get("primary_category"), request.args.get("lifecycle_status"))
        return jsonify(result), result["status"]

    return app


if __name__ == "__main__":
    build_app().run(host="127.0.0.1", port=int(os.environ.get("FM02_API_PORT", "8088")), debug=False)
