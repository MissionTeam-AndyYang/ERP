"""FM-02 C2 backend validation and REST service boundary.

This module is deliberately database-adapter based: callers inject a DB-API
connection factory, while unit tests can inject a scripted connection.  It
does not create a connection at import time and it does not provide a global
UOM conversion fallback.

The service covers only the bounded C2 contract:

* business approval evidence is mandatory before an ACTIVE record;
* customer qualification scope is deterministic even when the supplier
  qualification is NULL;
* customer writes lock the parent Item before relationship and interval
  checks, making idempotency and concurrency deterministic;
* conversion rules are Item-specific and both endpoints must belong to that
  Item; and
* CATCH_WEIGHT is metadata validation only, not a fixed-factor calculation.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Iterable

from flask import Flask, jsonify, request


CUSTOMER_SCOPE_SENTINEL = "00000000-0000-0000-0000-000000000000"
CUSTOMER_SCOPES = {"ANY_GENERAL_QUALIFIED_SUPPLIER", "SPECIFIC_SUPPLIER"}
QUALIFICATION_STATUSES = {"DRAFT", "ACTIVE", "INACTIVE", "REJECTED", "SUPERSEDED"}
CONVERSION_STATUSES = {"DRAFT", "ACTIVE", "INACTIVE", "SUPERSEDED"}
CONVERSION_TYPES = {"FIXED", "CATCH_WEIGHT"}
ACTIVE_STATUSES = {"ACTIVE"}
NON_CONFLICTING_STATUSES = {"REJECTED", "INACTIVE", "SUPERSEDED"}


def _error(status: int, field: str, message: str) -> dict[str, Any]:
    return {"ok": False, "status": status, "errors": [{"field": field, "message": message}]}


def _errors(errors: list[dict[str, str]], status: int = 400) -> dict[str, Any] | None:
    return {"ok": False, "status": status, "errors": errors} if errors else None


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _upper(value: Any) -> str:
    return _text(value).upper()


def _parse_time(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value.replace(tzinfo=None)
    if not _text(value):
        return None
    try:
        return datetime.fromisoformat(_text(value).replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def _intervals_overlap(left_from: Any, left_to: Any, right_from: Any, right_to: Any) -> bool:
    left_start = _parse_time(left_from)
    right_start = _parse_time(right_from)
    if left_start is None or right_start is None:
        return False
    left_end = _parse_time(left_to) or datetime.max
    right_end = _parse_time(right_to) or datetime.max
    return left_start < right_end and right_start < left_end


def _interval_contains(row: dict[str, Any], at: datetime) -> bool:
    start = _parse_time(row.get("effective_from"))
    end = _parse_time(row.get("effective_to")) or datetime.max
    return start is not None and start <= at < end


def _decimal(value: Any, field: str) -> tuple[Decimal | None, dict[str, str] | None]:
    if value is None or value == "":
        return None, None
    try:
        return Decimal(str(value)), None
    except (InvalidOperation, ValueError):
        return None, {"field": field, "message": "must be an exact decimal"}


def _fingerprint(value: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    ).hexdigest().upper()


def validate_approval_evidence(payload: dict[str, Any], status: str) -> list[dict[str, str]]:
    """Return approval errors; an ACTIVE record never receives implicit approval."""

    normalized_status = _upper(status)
    errors: list[dict[str, str]] = []
    if normalized_status == "ACTIVE":
        for field in ("approved_by_role", "approved_by_business_ref", "approval_evidence_ref"):
            if not _text(payload.get(field)):
                errors.append({"field": field, "message": "required before ACTIVE"})
        actor_type = _upper(payload.get("business_actor_type"))
        if actor_type in {"ENGINEERING", "TECHNICAL", "SYSTEM"}:
            errors.append({"field": "business_actor_type", "message": "technical executor cannot provide business approval"})
    return errors


def normalize_customer_qualification(payload: dict[str, Any], item_id: str | None = None) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    """Normalize and validate the customer scope key without applying defaults."""

    normalized = dict(payload)
    if item_id is not None:
        normalized["item_id"] = item_id
    normalized["item_id"] = _text(normalized.get("item_id"))
    normalized["customer_ref"] = _text(normalized.get("customer_ref"))
    normalized["approval_scope"] = _upper(normalized.get("approval_scope"))
    normalized["supply_method"] = _upper(normalized.get("supply_method"))
    normalized["qualification_status"] = _upper(normalized.get("qualification_status") or "DRAFT")
    normalized["supplier_qualification_id"] = _text(normalized.get("supplier_qualification_id")) or None
    normalized["specification_id"] = _text(normalized.get("specification_id")) or None
    normalized["effective_from"] = normalized.get("effective_from")
    normalized["effective_to"] = normalized.get("effective_to")
    normalized["source_reference"] = _text(normalized.get("source_reference"))
    errors: list[dict[str, str]] = []
    for field in ("item_id", "customer_ref", "approval_scope", "supply_method", "effective_from", "source_reference"):
        if not _text(normalized.get(field)):
            errors.append({"field": field, "message": "required"})
    if normalized["approval_scope"] not in CUSTOMER_SCOPES:
        errors.append({"field": "approval_scope", "message": "unsupported customer qualification scope"})
    if normalized["qualification_status"] not in QUALIFICATION_STATUSES:
        errors.append({"field": "qualification_status", "message": "unsupported qualification status"})
    start = _parse_time(normalized["effective_from"])
    end = _parse_time(normalized["effective_to"]) if normalized["effective_to"] else None
    if start is None and _text(normalized.get("effective_from")):
        errors.append({"field": "effective_from", "message": "must be an ISO timestamp"})
    if normalized["effective_to"] and end is None:
        errors.append({"field": "effective_to", "message": "must be an ISO timestamp"})
    if start is not None and end is not None and end <= start:
        errors.append({"field": "effective_to", "message": "must be after effective_from"})
    if normalized["supplier_qualification_id"] == CUSTOMER_SCOPE_SENTINEL:
        errors.append({"field": "supplier_qualification_id", "message": "reserved scope sentinel cannot be a real qualification"})
    if normalized["approval_scope"] == "ANY_GENERAL_QUALIFIED_SUPPLIER" and normalized["supplier_qualification_id"] is not None:
        errors.append({"field": "supplier_qualification_id", "message": "must be null for general supplier scope"})
    if normalized["approval_scope"] == "SPECIFIC_SUPPLIER" and normalized["supplier_qualification_id"] is None:
        errors.append({"field": "supplier_qualification_id", "message": "required for specific supplier scope"})
    errors.extend(validate_approval_evidence(normalized, normalized["qualification_status"]))
    if errors:
        return None, errors
    normalized["supplier_qualification_scope_key"] = normalized["supplier_qualification_id"] or CUSTOMER_SCOPE_SENTINEL
    return normalized, []


def validate_conversion_rule(payload: dict[str, Any], item_id: str | None = None) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    """Validate an Item-specific rule; no global/sentinel Item is accepted."""

    normalized = dict(payload)
    if item_id is not None:
        normalized["item_id"] = item_id
    normalized["item_id"] = _text(normalized.get("item_id"))
    normalized["from_item_uom_id"] = _text(normalized.get("from_item_uom_id"))
    normalized["to_item_uom_id"] = _text(normalized.get("to_item_uom_id"))
    normalized["conversion_type"] = _upper(normalized.get("conversion_type"))
    normalized["lifecycle_status"] = _upper(normalized.get("lifecycle_status") or "DRAFT")
    normalized["conversion_rule_version"] = normalized.get("conversion_rule_version", 1)
    normalized["source_reference"] = _text(normalized.get("source_reference"))
    errors: list[dict[str, str]] = []
    for field in ("item_id", "from_item_uom_id", "to_item_uom_id", "conversion_type", "effective_from", "source_reference"):
        if not _text(normalized.get(field)):
            errors.append({"field": field, "message": "required"})
    if normalized["item_id"] == CUSTOMER_SCOPE_SENTINEL:
        errors.append({"field": "item_id", "message": "global/sentinel conversion scope is not supported"})
    if normalized["from_item_uom_id"] == normalized["to_item_uom_id"] and normalized["from_item_uom_id"]:
        errors.append({"field": "to_item_uom_id", "message": "conversion endpoints must differ"})
    if normalized["conversion_type"] not in CONVERSION_TYPES:
        errors.append({"field": "conversion_type", "message": "must be FIXED or CATCH_WEIGHT"})
    if normalized["lifecycle_status"] not in CONVERSION_STATUSES:
        errors.append({"field": "lifecycle_status", "message": "unsupported conversion status"})
    try:
        if int(normalized["conversion_rule_version"]) < 1:
            raise ValueError
        normalized["conversion_rule_version"] = int(normalized["conversion_rule_version"])
    except (TypeError, ValueError):
        errors.append({"field": "conversion_rule_version", "message": "must be positive"})
    start = _parse_time(normalized.get("effective_from"))
    end = _parse_time(normalized.get("effective_to")) if normalized.get("effective_to") else None
    if start is None and _text(normalized.get("effective_from")):
        errors.append({"field": "effective_from", "message": "must be an ISO timestamp"})
    if normalized.get("effective_to") and end is None:
        errors.append({"field": "effective_to", "message": "must be an ISO timestamp"})
    if start is not None and end is not None and end <= start:
        errors.append({"field": "effective_to", "message": "must be after effective_from"})
    factor, factor_error = _decimal(normalized.get("conversion_factor"), "conversion_factor")
    tolerance, tolerance_error = _decimal(normalized.get("tolerance_value"), "tolerance_value")
    for error in (factor_error, tolerance_error):
        if error:
            errors.append(error)
    if normalized["conversion_type"] == "FIXED":
        if factor is None:
            errors.append({"field": "conversion_factor", "message": "required for FIXED conversion"})
        elif factor <= 0:
            errors.append({"field": "conversion_factor", "message": "must be positive for FIXED conversion"})
    if normalized["conversion_type"] == "CATCH_WEIGHT" and factor is not None:
        errors.append({"field": "conversion_factor", "message": "must be null for CATCH_WEIGHT conversion"})
    if normalized.get("rounding_scale") is not None:
        try:
            scale = int(normalized["rounding_scale"])
            if not 0 <= scale <= 18:
                raise ValueError
            normalized["rounding_scale"] = scale
        except (TypeError, ValueError):
            errors.append({"field": "rounding_scale", "message": "must be between 0 and 18"})
    errors.extend(validate_approval_evidence(normalized, normalized["lifecycle_status"]))
    if errors:
        return None, errors
    return normalized, []


def resolve_item_specific_conversion(
    item_id: str,
    from_item_uom_id: str,
    to_item_uom_id: str,
    candidates: Iterable[dict[str, Any]],
    effective_at: Any | None = None,
) -> dict[str, Any]:
    """Resolve exactly one active rule for one Item, never consulting globals."""

    if not _text(item_id) or not _text(from_item_uom_id) or not _text(to_item_uom_id):
        return _error(400, "conversion_scope", "item and both Item-scoped UOM endpoints are required")
    if from_item_uom_id == to_item_uom_id:
        return _error(400, "to_item_uom_id", "conversion endpoints must differ")
    at = _parse_time(effective_at) if effective_at is not None else datetime.now(timezone.utc).replace(tzinfo=None)
    if at is None:
        return _error(400, "effective_at", "must be an ISO timestamp")
    matches = []
    for row in candidates:
        if (
            _text(row.get("item_id")) == item_id
            and _text(row.get("item_id")) != CUSTOMER_SCOPE_SENTINEL
            and _text(row.get("from_item_uom_id")) == from_item_uom_id
            and _text(row.get("to_item_uom_id")) == to_item_uom_id
            and _upper(row.get("lifecycle_status")) == "ACTIVE"
            and _interval_contains(row, at)
        ):
            matches.append(row)
    if not matches:
        return _error(404, "conversion", "no active Item-specific conversion rule exists")
    if len(matches) != 1:
        return _error(409, "conversion", "active Item-specific conversion rules are ambiguous")
    return {"ok": True, "status": 200, "conversion_rule": dict(matches[0])}


class C2Service:
    """C2 write/read service with explicit transaction boundaries."""

    def __init__(self, connection_factory: Callable[[], Any]):
        self.connection_factory = connection_factory

    @staticmethod
    def _rollback(connection: Any) -> None:
        try:
            connection.rollback()
        except Exception:
            pass

    @staticmethod
    def _close(connection: Any) -> None:
        try:
            connection.close()
        except Exception:
            pass

    @staticmethod
    def _row(cursor: Any, row: Any) -> dict[str, Any]:
        if isinstance(row, dict):
            return dict(row)
        return {description[0]: value for description, value in zip(cursor.description, row)}

    @staticmethod
    def _customer_fingerprint(payload: dict[str, Any]) -> str:
        keys = (
            "item_id", "customer_ref", "supplier_qualification_id", "specification_id",
            "approval_scope", "supply_method", "effective_from", "effective_to",
            "source_reference", "qualification_status", "approved_by_role",
            "approved_by_business_ref", "approval_evidence_ref",
        )
        return _fingerprint({key: payload.get(key) for key in keys})

    @staticmethod
    def _conversion_fingerprint(payload: dict[str, Any]) -> str:
        keys = (
            "item_id", "from_item_uom_id", "to_item_uom_id", "conversion_type",
            "conversion_rule_version", "conversion_factor", "rounding_mode",
            "rounding_scale", "tolerance_value", "lifecycle_status", "effective_from",
            "effective_to", "source_reference", "approved_by_role",
            "approved_by_business_ref", "approval_evidence_ref",
        )
        return _fingerprint({key: payload.get(key) for key in keys})

    def create_customer_qualification(self, item_id: str, payload: dict[str, Any], correlation_id: str | None = None) -> dict[str, Any]:
        normalized, validation_errors = normalize_customer_qualification(payload, item_id)
        if validation_errors:
            return {"ok": False, "status": 400, "errors": validation_errors}
        assert normalized is not None
        connection = self.connection_factory()
        fingerprint = self._customer_fingerprint(normalized)
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT item_id FROM item WHERE item_id=%s FOR UPDATE", (item_id,))
                if cursor.fetchone() is None:
                    self._rollback(connection)
                    return _error(404, "item_id", "item not found")
                if normalized["supplier_qualification_id"]:
                    cursor.execute(
                        "SELECT * FROM item_supplier_qualification WHERE qualification_id=%s AND item_id=%s FOR UPDATE",
                        (normalized["supplier_qualification_id"], item_id),
                    )
                    supplier = cursor.fetchone()
                    if supplier is None:
                        self._rollback(connection)
                        return _error(409, "supplier_qualification_id", "supplier qualification is not Item-scoped")
                    supplier_row = self._row(cursor, supplier)
                    if normalized["qualification_status"] == "ACTIVE" and _upper(supplier_row.get("qualification_status")) != "ACTIVE":
                        self._rollback(connection)
                        return _error(409, "supplier_qualification_id", "ACTIVE customer permission requires ACTIVE supplier qualification")
                if normalized["specification_id"]:
                    cursor.execute(
                        "SELECT * FROM item_specification WHERE specification_id=%s AND item_id=%s FOR UPDATE",
                        (normalized["specification_id"], item_id),
                    )
                    specification = cursor.fetchone()
                    if specification is None:
                        self._rollback(connection)
                        return _error(409, "specification_id", "specification is not Item-scoped")
                    if normalized["qualification_status"] == "ACTIVE" and _upper(self._row(cursor, specification).get("revision_status")) != "ACTIVE":
                        self._rollback(connection)
                        return _error(409, "specification_id", "ACTIVE customer permission requires ACTIVE specification")
                cursor.execute(
                    """SELECT * FROM item_customer_qualification
                    WHERE customer_ref=%s AND item_id=%s AND approval_scope=%s
                      AND supplier_qualification_scope_key=%s AND effective_from=%s
                    FOR UPDATE""",
                    (normalized["customer_ref"], item_id, normalized["approval_scope"], normalized["supplier_qualification_scope_key"], normalized["effective_from"]),
                )
                existing = cursor.fetchone()
                if existing is not None:
                    existing_row = self._row(cursor, existing)
                    existing_fingerprint = existing_row.get("request_fingerprint") or self._customer_fingerprint(existing_row)
                    self._rollback(connection)
                    if existing_fingerprint == fingerprint:
                        return {"ok": True, "status": 200, "idempotent_replay": True, "customer_qualification": existing_row}
                    return _error(409, "qualification", "same customer scope/effective start has a different request fingerprint")
                cursor.execute(
                    """SELECT * FROM item_customer_qualification
                    WHERE customer_ref=%s AND item_id=%s AND approval_scope=%s
                      AND supplier_qualification_scope_key=%s
                      AND qualification_status NOT IN ('REJECTED','INACTIVE','SUPERSEDED')
                      AND effective_from < COALESCE(%s,'9999-12-31 23:59:59.999999')
                      AND COALESCE(effective_to,'9999-12-31 23:59:59.999999') > %s
                    FOR UPDATE""",
                    (normalized["customer_ref"], item_id, normalized["approval_scope"], normalized["supplier_qualification_scope_key"], normalized["effective_to"], normalized["effective_from"]),
                )
                if cursor.fetchone() is not None:
                    self._rollback(connection)
                    return _error(409, "effective_period", "customer qualification periods overlap")
                qualification_id = str(uuid.uuid4())
                cursor.execute(
                    """INSERT INTO item_customer_qualification
                    (customer_qualification_id,item_id,customer_ref,supplier_qualification_id,
                     supplier_qualification_scope_key,specification_id,approval_scope,supply_method,qualification_status,
                     effective_from,effective_to,approved_by_role,approved_by_business_ref,
                     approval_evidence_ref,source_reference,provenance_note,correlation_id,
                     created_by_assignment_id,updated_by_assignment_id,created_at,updated_at,row_version)
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0)""",
                    (
                        qualification_id, item_id, normalized["customer_ref"], normalized["supplier_qualification_id"],
                        normalized["supplier_qualification_scope_key"],
                        normalized["specification_id"], normalized["approval_scope"], normalized["supply_method"],
                        normalized["qualification_status"], normalized["effective_from"], normalized["effective_to"],
                        normalized.get("approved_by_role"), normalized.get("approved_by_business_ref"),
                        normalized.get("approval_evidence_ref"), normalized["source_reference"],
                        normalized.get("provenance_note"), correlation_id or normalized.get("correlation_id"),
                        normalized.get("created_by_assignment_id"), normalized.get("updated_by_assignment_id"),
                        datetime.now(timezone.utc).replace(tzinfo=None), datetime.now(timezone.utc).replace(tzinfo=None),
                    ),
                )
            connection.commit()
            normalized["customer_qualification_id"] = qualification_id
            normalized["idempotent_replay"] = False
            return {"ok": True, "status": 201, "customer_qualification": normalized}
        except Exception:
            self._rollback(connection)
            return _error(409, "qualification", "qualification write failed closed and was rolled back")
        finally:
            self._close(connection)

    def create_conversion_rule(self, item_id: str, payload: dict[str, Any], correlation_id: str | None = None) -> dict[str, Any]:
        normalized, validation_errors = validate_conversion_rule(payload, item_id)
        if validation_errors:
            return {"ok": False, "status": 400, "errors": validation_errors}
        assert normalized is not None
        connection = self.connection_factory()
        fingerprint = self._conversion_fingerprint(normalized)
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT item_id FROM item WHERE item_id=%s FOR UPDATE", (item_id,))
                if cursor.fetchone() is None:
                    self._rollback(connection)
                    return _error(404, "item_id", "item not found")
                endpoints: list[dict[str, Any]] = []
                for field in ("from_item_uom_id", "to_item_uom_id"):
                    cursor.execute("SELECT * FROM item_uom WHERE item_uom_id=%s AND item_id=%s FOR UPDATE", (normalized[field], item_id))
                    endpoint = cursor.fetchone()
                    if endpoint is None:
                        self._rollback(connection)
                        return _error(409, field, "UOM endpoint is not Item-scoped")
                    endpoints.append(self._row(cursor, endpoint))
                cursor.execute(
                    """SELECT * FROM uom_conversion
                    WHERE item_id=%s AND from_item_uom_id=%s AND to_item_uom_id=%s
                      AND conversion_type=%s AND conversion_rule_version=%s
                    FOR UPDATE""",
                    (item_id, normalized["from_item_uom_id"], normalized["to_item_uom_id"], normalized["conversion_type"], normalized["conversion_rule_version"]),
                )
                existing = cursor.fetchone()
                if existing is not None:
                    existing_row = self._row(cursor, existing)
                    existing_fingerprint = existing_row.get("request_fingerprint") or self._conversion_fingerprint(existing_row)
                    self._rollback(connection)
                    if existing_fingerprint == fingerprint:
                        return {"ok": True, "status": 200, "idempotent_replay": True, "conversion_rule": existing_row}
                    return _error(409, "conversion_rule", "same Item-specific rule identity has a different request fingerprint")
                cursor.execute(
                    """SELECT * FROM uom_conversion
                    WHERE item_id=%s AND from_item_uom_id=%s AND to_item_uom_id=%s
                      AND conversion_type=%s AND lifecycle_status NOT IN ('REJECTED','INACTIVE','SUPERSEDED')
                      AND effective_from < COALESCE(%s,'9999-12-31 23:59:59.999999')
                      AND COALESCE(effective_to,'9999-12-31 23:59:59.999999') > %s
                    FOR UPDATE""",
                    (item_id, normalized["from_item_uom_id"], normalized["to_item_uom_id"], normalized["conversion_type"], normalized["effective_to"], normalized["effective_from"]),
                )
                if cursor.fetchone() is not None:
                    self._rollback(connection)
                    return _error(409, "effective_period", "conversion rule periods overlap")
                rule_id = str(uuid.uuid4())
                cursor.execute(
                    """INSERT INTO uom_conversion
                    (conversion_rule_id,item_id,from_item_uom_id,to_item_uom_id,conversion_type,
                     conversion_rule_version,conversion_factor,rounding_mode,rounding_scale,
                     tolerance_value,lifecycle_status,effective_from,effective_to,approved_by_role,
                     approved_by_business_ref,approval_evidence_ref,source_reference,provenance_note,
                     correlation_id,created_by_assignment_id,updated_by_assignment_id,created_at,updated_at,row_version)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0)""",
                    (
                        rule_id, item_id, normalized["from_item_uom_id"], normalized["to_item_uom_id"], normalized["conversion_type"],
                        normalized["conversion_rule_version"], normalized.get("conversion_factor"), normalized.get("rounding_mode"),
                        normalized.get("rounding_scale"), normalized.get("tolerance_value"), normalized["lifecycle_status"],
                        normalized["effective_from"], normalized.get("effective_to"), normalized.get("approved_by_role"),
                        normalized.get("approved_by_business_ref"), normalized.get("approval_evidence_ref"), normalized["source_reference"],
                        normalized.get("provenance_note"), correlation_id or normalized.get("correlation_id"),
                        normalized.get("created_by_assignment_id"), normalized.get("updated_by_assignment_id"),
                        datetime.now(timezone.utc).replace(tzinfo=None), datetime.now(timezone.utc).replace(tzinfo=None),
                    ),
                )
            connection.commit()
            normalized["conversion_rule_id"] = rule_id
            normalized["idempotent_replay"] = False
            return {"ok": True, "status": 201, "conversion_rule": normalized}
        except Exception:
            self._rollback(connection)
            return _error(409, "conversion_rule", "conversion rule write failed closed and was rolled back")
        finally:
            self._close(connection)

    def resolve_conversion(self, item_id: str, from_item_uom_id: str, to_item_uom_id: str, effective_at: Any | None = None) -> dict[str, Any]:
        """Read only Item-specific rules; deliberately no second/global lookup exists."""

        connection = self.connection_factory()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT * FROM uom_conversion
                    WHERE item_id=%s AND from_item_uom_id=%s AND to_item_uom_id=%s
                      AND lifecycle_status='ACTIVE'
                    ORDER BY effective_from DESC""",
                    (item_id, from_item_uom_id, to_item_uom_id),
                )
                rows = [self._row(cursor, row) for row in cursor.fetchall()]
            return resolve_item_specific_conversion(item_id, from_item_uom_id, to_item_uom_id, rows, effective_at)
        finally:
            self._close(connection)


def build_app(service: C2Service) -> Flask:
    """Build an explicitly injected C2 REST app; no implicit DB credentials/runtime."""

    app = Flask(__name__)

    @app.post("/api/v1/fm02/items/<item_id>/customer-qualifications")
    def create_customer_qualification(item_id: str) -> Any:
        result = service.create_customer_qualification(item_id, request.get_json(silent=True) or {}, request.headers.get("X-Correlation-ID"))
        return jsonify(result), result["status"]

    @app.post("/api/v1/fm02/items/<item_id>/uom-conversions")
    def create_conversion_rule(item_id: str) -> Any:
        result = service.create_conversion_rule(item_id, request.get_json(silent=True) or {}, request.headers.get("X-Correlation-ID"))
        return jsonify(result), result["status"]

    @app.get("/api/v1/fm02/items/<item_id>/uom-conversions/<from_item_uom_id>/<to_item_uom_id>")
    def resolve_conversion(item_id: str, from_item_uom_id: str, to_item_uom_id: str) -> Any:
        result = service.resolve_conversion(item_id, from_item_uom_id, to_item_uom_id, request.args.get("effective_at"))
        return jsonify(result), result["status"]

    return app
