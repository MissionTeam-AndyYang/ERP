"""FM-02 Sprint-02 bounded Item Master integrity API.

This module preserves the Sprint-01 Item POST/GET/List response contract while
adding controlled categories, specification lineages, and an atomic,
business-approval-gated lifecycle transition.  It has no Product/SKU,
supplier/customer qualification, operational transaction, callback, or UI
behavior.
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Callable

import pymysql
from flask import Flask, jsonify, request
from pymysql.err import IntegrityError, OperationalError


ALLOWED_CATEGORIES = {"RAW", "MATERIAL", "FILM", "WIP", "FG"}
CATEGORY_IDS = {
    "RAW": "00000000-0000-0000-0000-000000000001",
    "MATERIAL": "00000000-0000-0000-0000-000000000002",
    "FILM": "00000000-0000-0000-0000-000000000003",
    "WIP": "00000000-0000-0000-0000-000000000004",
    "FG": "00000000-0000-0000-0000-000000000005",
}
ALLOWED_LIFECYCLE = {"DRAFT", "ACTIVE", "INACTIVE", "RETIRED"}
TRANSITIONS = {
    "DRAFT": {"ACTIVE", "INACTIVE"},
    "ACTIVE": {"INACTIVE", "RETIRED"},
    "INACTIVE": {"ACTIVE", "RETIRED"},
}
REQUIRED_ITEM_FIELDS = ("primary_category", "display_name", "ownership_context", "base_uom_code")


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def request_fingerprint(payload: dict[str, Any]) -> str:
    """Create a deterministic fingerprint for idempotent lifecycle requests."""
    canonical = {
        key: payload.get(key)
        for key in (
            "to_status",
            "reason",
            "business_actor_type",
            "business_actor_ref",
            "accountable_approval_role",
            "delegated_authorization_ref",
            "decision_evidence_ref",
            "effective_at",
            "request_id",
            "expected_row_version",
            "technical_work_item_id",
            "technical_executor_assignment_id",
            "technical_executor_ref",
        )
    }
    return hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest().upper()


class ItemIntegrityService:
    def __init__(self, connection_factory: Callable[[], Any], failure_hook: Callable[[str], None] | None = None):
        self.connection_factory = connection_factory
        self.failure_hook = failure_hook

    @staticmethod
    def _error(status: int, field: str, message: str) -> dict[str, Any]:
        return {"ok": False, "status": status, "errors": [{"field": field, "message": message}]}

    def _validate_item(self, payload: dict[str, Any]) -> list[dict[str, str]]:
        errors: list[dict[str, str]] = []
        for field in REQUIRED_ITEM_FIELDS:
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
        for field in ("item_id", "item_code", "item_category_id"):
            if payload.get(field):
                errors.append({"field": field, "message": "system generated and not client-selectable"})
        aliases = payload.get("legacy_references", [])
        if aliases is not None and not isinstance(aliases, list):
            errors.append({"field": "legacy_references", "message": "must be a list"})
        return errors

    def create_item(self, payload: dict[str, Any], correlation_id: str | None = None) -> dict[str, Any]:
        errors = self._validate_item(payload)
        if errors:
            return {"ok": False, "status": 400, "errors": errors}
        category = str(payload["primary_category"]).strip().upper()
        uom = str(payload["base_uom_code"]).strip().upper()
        connection = self.connection_factory()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT uom_code FROM uom WHERE uom_code=%s AND lifecycle_status='ACTIVE'", (uom,))
                if cursor.fetchone() is None:
                    connection.rollback()
                    return self._error(400, "base_uom_code", "unknown or inactive UOM")
                item_id = str(uuid.uuid4())
                item_code = self._new_item_code(cursor)
                now = utc_now()
                cursor.execute(
                    """INSERT INTO item
                    (item_id,item_code,item_category_id,primary_category,display_name,description,ownership_context,
                     base_uom_code,lifecycle_status,specification_summary,specification_reference,identity_fingerprint,
                     created_at,updated_at,row_version,correlation_id,provenance_note)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'DRAFT',%s,%s,%s,%s,%s,0,%s,%s)""",
                    (
                        item_id,
                        item_code,
                        CATEGORY_IDS[category],
                        category,
                        str(payload["display_name"]).strip(),
                        str(payload.get("description", "")).strip(),
                        str(payload["ownership_context"]).strip(),
                        uom,
                        str(payload.get("specification_summary", "")).strip(),
                        str(payload.get("specification_reference", "")).strip(),
                        self._item_fingerprint(payload, category, uom),
                        now,
                        now,
                        correlation_id,
                        "FM-02 SPRINT-02 DEV / bounded integrity foundation",
                    ),
                )
                for alias in payload.get("legacy_references", []) or []:
                    if not isinstance(alias, dict) or not all(str(alias.get(key, "")).strip() for key in ("legacy_system", "legacy_entity", "legacy_code")):
                        connection.rollback()
                        return self._error(400, "legacy_references", "each alias needs system, entity and code")
                    cursor.execute(
                        """INSERT INTO item_legacy_identifier
                        (legacy_reference_id,item_id,legacy_system,legacy_entity,legacy_code,alias_role,provenance_ref,created_at)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (
                            str(uuid.uuid4()), item_id, str(alias["legacy_system"]).strip(),
                            str(alias["legacy_entity"]).strip(), str(alias["legacy_code"]).strip(),
                            str(alias.get("alias_role", "LEGACY_REFERENCE")).strip(),
                            "FM-02 SPRINT-02 DEV alias / non-authoritative", now,
                        ),
                    )
            connection.commit()
            return self.get_item(item_id, connection=connection) | {"status": 201}
        except IntegrityError:
            connection.rollback()
            return self._error(409, "database", "duplicate or conflicting bounded identity")
        finally:
            connection.close()

    @staticmethod
    def _item_fingerprint(payload: dict[str, Any], category: str, uom: str) -> str:
        canonical = {
            "primary_category": category,
            "display_name": str(payload["display_name"]).strip(),
            "ownership_context": str(payload["ownership_context"]).strip(),
            "base_uom_code": uom,
            "specification_summary": str(payload.get("specification_summary", "")).strip(),
            "specification_reference": str(payload.get("specification_reference", "")).strip(),
        }
        return hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest().upper()

    @staticmethod
    def _new_item_code(cursor: Any) -> str:
        # The API contract permits any generated 12-character code; UUID hex is
        # collision-resistant and makes tests deterministic enough to inspect.
        for _ in range(8):
            candidate = uuid.uuid4().hex[:12].upper()
            cursor.execute("SELECT 1 FROM item WHERE item_code=%s", (candidate,))
            if cursor.fetchone() is None:
                return candidate
        raise RuntimeError("safe item code generation retries exhausted")

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
                    return self._error(400, "item_id/item_code", "lookup required")
                row = cursor.fetchone()
                if row is None:
                    return self._error(404, "lookup", "item not found")
                item = self._row(cursor, row)
                item["controlled_category"] = {"category_code": item.get("primary_category"), "category_name": None}
                try:
                    cursor.execute("SELECT category_code,category_name FROM item_category WHERE category_id=%s", (item.get("item_category_id"),))
                    category_row = cursor.fetchone()
                    if category_row is not None:
                        item["controlled_category"] = dict(category_row)
                except OperationalError:
                    # Sprint-01's target-limited app role remains compatible;
                    # the new integrity tables are read by the engineering lane.
                    connection.rollback()
                cursor.execute(
                    "SELECT legacy_system,legacy_entity,legacy_code,alias_role,provenance_ref FROM item_legacy_identifier WHERE item_id=%s ORDER BY legacy_code",
                    (item["item_id"],),
                )
                item["legacy_references"] = [self._row(cursor, alias) for alias in cursor.fetchall()]
                try:
                    cursor.execute(
                        """SELECT specification_id,specification_lineage_id,revision_no,specification_code,
                        specification_name,specification_hash,revision_status,effective_from,effective_to
                        FROM item_specification WHERE item_id=%s ORDER BY specification_lineage_id,revision_no""",
                        (item["item_id"],),
                    )
                    item["specifications"] = [self._row(cursor, spec) for spec in cursor.fetchall()]
                except OperationalError:
                    connection.rollback()
                    item["specifications"] = []
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
                clauses.append("i.primary_category=%s")
                params.append(category.upper())
            if lifecycle_status:
                clauses.append("i.lifecycle_status=%s")
                params.append(lifecycle_status.upper())
            query = "SELECT * FROM item i"
            if clauses:
                query += " WHERE " + " AND ".join(clauses)
            query += " ORDER BY i.created_at,i.item_id"
            with connection.cursor() as cursor:
                cursor.execute(query, tuple(params))
                items = []
                for row in cursor.fetchall():
                    item = self._row(cursor, row)
                    item["controlled_category"] = {"category_code": item.get("primary_category"), "category_name": None}
                    items.append(item)
                return {"ok": True, "status": 200, "items": items}
        finally:
            connection.close()

    def add_specification(self, item_id: str, payload: dict[str, Any], correlation_id: str | None = None) -> dict[str, Any]:
        required = ("specification_lineage_id", "revision_no", "specification_code", "specification_name", "specification_hash", "specification_summary", "effective_from")
        missing = [field for field in required if payload.get(field) in (None, "")]
        if missing:
            return {"ok": False, "status": 400, "errors": [{"field": field, "message": "required"} for field in missing]}
        if int(payload["revision_no"]) < 1 or len(str(payload["specification_hash"])) != 64:
            return self._error(400, "revision", "positive revision and 64-character specification hash required")
        status = str(payload.get("revision_status", "DRAFT")).upper()
        if status not in {"DRAFT", "ACTIVE"}:
            return self._error(400, "revision_status", "only DRAFT or ACTIVE is accepted")
        connection = self.connection_factory()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT item_id FROM item WHERE item_id=%s FOR UPDATE", (item_id,))
                if cursor.fetchone() is None:
                    connection.rollback()
                    return self._error(404, "item_id", "item not found")
                if status == "ACTIVE" and not payload.get("approved_by_assignment_id"):
                    connection.rollback()
                    return self._error(400, "approved_by_assignment_id", "ACTIVE revision requires approval reference")
                cursor.execute(
                    """SELECT specification_id FROM item_specification
                    WHERE item_id=%s AND specification_lineage_id=%s AND revision_status='ACTIVE'
                    AND effective_from < COALESCE(%s,'9999-12-31 23:59:59.999999')
                    AND COALESCE(effective_to,'9999-12-31 23:59:59.999999') > %s
                    FOR UPDATE""",
                    (item_id, payload["specification_lineage_id"], payload.get("effective_to"), payload["effective_from"]),
                )
                if cursor.fetchone() is not None and status == "ACTIVE":
                    connection.rollback()
                    return self._error(409, "effective_period", "active specification periods overlap within a lineage")
                now = utc_now()
                specification_id = str(uuid.uuid4())
                cursor.execute(
                    """INSERT INTO item_specification
                    (specification_id,item_id,specification_lineage_id,revision_no,specification_code,specification_name,
                     specification_hash,specification_summary,specification_reference,revision_status,effective_from,effective_to,
                     approved_by_assignment_id,correlation_id,source_reference,provenance_note,created_at,updated_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (
                        specification_id, item_id, payload["specification_lineage_id"], int(payload["revision_no"]),
                        payload["specification_code"], payload["specification_name"], payload["specification_hash"].upper(),
                        payload["specification_summary"], payload.get("specification_reference"), status,
                        payload["effective_from"], payload.get("effective_to"), payload.get("approved_by_assignment_id"),
                        correlation_id, "FM02-S02-API", "Bounded DEV specification lineage", now, now,
                    ),
                )
            connection.commit()
            return {"ok": True, "status": 201, "specification_id": specification_id}
        except IntegrityError:
            connection.rollback()
            return self._error(409, "specification", "duplicate lineage revision or integrity conflict")
        finally:
            connection.close()

    def change_lifecycle(self, item_id: str, payload: dict[str, Any], correlation_id: str | None = None) -> dict[str, Any]:
        required = ("to_status", "reason", "business_actor_type", "business_actor_ref", "accountable_approval_role", "decision_evidence_ref", "request_id", "idempotency_key")
        missing = [field for field in required if not str(payload.get(field, "")).strip()]
        if missing:
            return {"ok": False, "status": 400, "errors": [{"field": field, "message": "required"} for field in missing]}
        target = str(payload["to_status"]).upper()
        if target not in ALLOWED_LIFECYCLE:
            return self._error(400, "to_status", "unsupported lifecycle status")
        if str(payload.get("business_actor_type", "")).upper() in {"ENGINEERING", "TECHNICAL", "SYSTEM"}:
            return self._error(403, "business_actor_type", "technical executor cannot satisfy business approval")
        if target == "ACTIVE" and not str(payload.get("delegated_authorization_ref", "")).strip():
            return self._error(400, "delegated_authorization_ref", "activation requires delegated business authorization")
        fingerprint = request_fingerprint(payload)
        connection = self.connection_factory()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM item WHERE item_id=%s FOR UPDATE", (item_id,))
                item = cursor.fetchone()
                if item is None:
                    connection.rollback()
                    return self._error(404, "item_id", "item not found")
                cursor.execute("SELECT * FROM item_approval WHERE item_id=%s AND idempotency_key=%s", (item_id, payload["idempotency_key"]))
                existing = cursor.fetchone()
                if existing is not None:
                    if existing["request_fingerprint"] != fingerprint:
                        connection.rollback()
                        return self._error(409, "idempotency_key", "same key was used with a different request fingerprint")
                    connection.rollback()
                    return {"ok": True, "status": 200, "idempotent_replay": True, "approval_id": existing["approval_id"], "item": self.get_item(item_id, connection=connection)["item"]}
                expected = payload.get("expected_row_version")
                if expected is not None and int(expected) != int(item["row_version"]):
                    connection.rollback()
                    return self._error(409, "row_version", "optimistic concurrency conflict")
                current = str(item["lifecycle_status"])
                if target not in TRANSITIONS.get(current, set()):
                    connection.rollback()
                    return self._error(409, "to_status", f"transition {current}->{target} is not permitted")
                now = utc_now()
                approval_id = str(uuid.uuid4())
                cursor.execute(
                    """INSERT INTO item_approval
                    (approval_id,item_id,approval_type,decision,business_actor_type,business_actor_ref,accountable_approval_role,
                     delegated_authorization_ref,decision_evidence_ref,effective_at,request_id,idempotency_key,request_fingerprint,
                     technical_work_item_id,technical_executor_assignment_id,technical_executor_ref,correlation_id,created_at)
                    VALUES (%s,%s,'LIFECYCLE','APPROVED',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (
                        approval_id, item_id, payload["business_actor_type"], payload["business_actor_ref"],
                        payload["accountable_approval_role"], payload.get("delegated_authorization_ref"),
                        payload["decision_evidence_ref"], payload.get("effective_at") or now, payload["request_id"],
                        payload["idempotency_key"], fingerprint, payload.get("technical_work_item_id"),
                        payload.get("technical_executor_assignment_id"), payload.get("technical_executor_ref"),
                        correlation_id or payload.get("correlation_id") or payload["request_id"], now,
                    ),
                )
                if self.failure_hook:
                    self.failure_hook("after_approval")
                event_id = str(uuid.uuid4())
                cursor.execute(
                    """INSERT INTO item_lifecycle_event
                    (event_id,item_id,approval_id,from_status,to_status,reason,effective_at,business_actor_ref,accountable_approval_role,
                     decision_evidence_ref,technical_work_item_id,technical_executor_assignment_id,technical_executor_ref,
                     correlation_id,source_reference,provenance_note,created_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (
                        event_id, item_id, approval_id, current, target, payload["reason"], payload.get("effective_at") or now,
                        payload["business_actor_ref"], payload["accountable_approval_role"], payload["decision_evidence_ref"],
                        payload.get("technical_work_item_id"), payload.get("technical_executor_assignment_id"),
                        payload.get("technical_executor_ref"), correlation_id or payload.get("correlation_id") or payload["request_id"],
                        "FM02-S02-API", "Atomic bounded lifecycle transition", now,
                    ),
                )
                cursor.execute(
                    "UPDATE item SET lifecycle_status=%s,updated_at=%s,updated_by_assignment_id=%s,row_version=row_version+1 WHERE item_id=%s AND row_version=%s",
                    (target, now, payload.get("technical_executor_assignment_id"), item_id, item["row_version"]),
                )
                if cursor.rowcount != 1:
                    raise RuntimeError("row_version update did not affect exactly one item")
            connection.commit()
            return {"ok": True, "status": 200, "idempotent_replay": False, "approval_id": approval_id, "event_id": event_id, "item": self.get_item(item_id, connection=connection)["item"]}
        except IntegrityError:
            connection.rollback()
            return self._error(409, "lifecycle", "integrity conflict; transaction rolled back")
        except Exception as exc:
            connection.rollback()
            if self.failure_hook:
                return self._error(500, "lifecycle", "transition rolled back")
            raise exc
        finally:
            connection.close()

    @staticmethod
    def _row(cursor: Any, row: Any) -> dict[str, Any]:
        if isinstance(row, dict):
            return {key: value.isoformat(sep=" ") if isinstance(value, datetime) else value for key, value in row.items()}
        return {description[0]: value.isoformat(sep=" ") if isinstance(value, datetime) else value for description, value in zip(cursor.description, row)}


def build_app(service: ItemIntegrityService | None = None) -> Flask:
    app = Flask(__name__)
    if service is None:
        service = ItemIntegrityService(lambda: pymysql.connect(
            host=os.environ.get("FM02_DB_HOST", "127.0.0.1"),
            port=int(os.environ.get("FM02_DB_PORT", "3344")),
            user=os.environ["FM02_DB_USER"],
            password=os.environ["FM02_DB_PASSWORD"],
            database=os.environ.get("FM02_DB_NAME", "erp2_functional_dev_001"),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
        ))

    @app.post("/api/v1/items")
    def create_item() -> Any:
        result = service.create_item(request.get_json(silent=True) or {}, request.headers.get("X-Correlation-ID"))
        return jsonify(result), result["status"]

    @app.get("/api/v1/items/<item_id>")
    def get_item(item_id: str) -> Any:
        result = service.get_item(item_id=item_id)
        return jsonify(result), result["status"]

    @app.get("/api/v1/items")
    def list_items() -> Any:
        result = service.list_items(request.args.get("primary_category"), request.args.get("lifecycle_status"))
        return jsonify(result), result["status"]

    @app.post("/api/v1/items/<item_id>/specifications")
    def add_specification(item_id: str) -> Any:
        result = service.add_specification(item_id, request.get_json(silent=True) or {}, request.headers.get("X-Correlation-ID"))
        return jsonify(result), result["status"]

    @app.post("/api/v1/items/<item_id>/lifecycle")
    def change_lifecycle(item_id: str) -> Any:
        result = service.change_lifecycle(item_id, request.get_json(silent=True) or {}, request.headers.get("X-Correlation-ID"))
        return jsonify(result), result["status"]

    return app


if __name__ == "__main__":
    build_app().run(host="127.0.0.1", port=int(os.environ.get("FM02_API_PORT", "8088")), debug=False)
