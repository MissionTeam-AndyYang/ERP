from __future__ import annotations

import sys
from pathlib import Path

import pytest


PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "package"
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from fm02_c2.service import (  # noqa: E402
    CUSTOMER_SCOPE_SENTINEL,
    C2Service,
    CONVERSION_STATUSES,
    QUALIFICATION_STATUSES,
    build_app,
    normalize_customer_qualification,
    resolve_item_specific_conversion,
    validate_conversion_rule,
)


def customer_payload(**overrides):
    payload = {
        "customer_ref": "CUSTOMER-A",
        "approval_scope": "ANY_GENERAL_QUALIFIED_SUPPLIER",
        "supply_method": "DIRECT",
        "effective_from": "2026-10-13 00:00:00",
        "source_reference": "C2-TEST",
    }
    payload.update(overrides)
    return payload


def conversion_payload(**overrides):
    payload = {
        "from_item_uom_id": "UOM-1",
        "to_item_uom_id": "UOM-2",
        "conversion_type": "FIXED",
        "conversion_factor": "2.500000000000000000",
        "effective_from": "2026-10-13 00:00:00",
        "source_reference": "C2-TEST",
    }
    payload.update(overrides)
    return payload


def test_status_vocabulary_matches_frozen_migration_0005_contract():
    expected = {"DRAFT", "ACTIVE", "INACTIVE", "REJECTED", "SUPERSEDED"}
    assert QUALIFICATION_STATUSES == expected
    assert CONVERSION_STATUSES == expected

    for status in ("PENDING", "APPROVED", "EXPIRED", "REVOKED"):
        _, customer_errors = normalize_customer_qualification(
            customer_payload(qualification_status=status), "ITEM-1"
        )
        _, conversion_errors = validate_conversion_rule(
            conversion_payload(lifecycle_status=status), "ITEM-1"
        )
        assert any(error["field"] == "qualification_status" for error in customer_errors)
        assert any(error["field"] == "lifecycle_status" for error in conversion_errors)


def test_customer_scope_normalizes_null_supplier_to_reserved_non_null_key():
    normalized, errors = normalize_customer_qualification(customer_payload(), "ITEM-1")
    assert errors == []
    assert normalized["supplier_qualification_id"] is None
    assert normalized["supplier_qualification_scope_key"] == CUSTOMER_SCOPE_SENTINEL


def test_customer_scope_rejects_mismatched_supplier_scope_and_reserved_id():
    _, general_errors = normalize_customer_qualification(
        customer_payload(supplier_qualification_id="SUP-1"), "ITEM-1"
    )
    _, sentinel_errors = normalize_customer_qualification(
        customer_payload(supplier_qualification_id=CUSTOMER_SCOPE_SENTINEL), "ITEM-1"
    )
    assert any(error["field"] == "supplier_qualification_id" for error in general_errors)
    assert any("reserved" in error["message"] for error in sentinel_errors)


def test_active_customer_and_conversion_fail_closed_without_business_approval():
    _, customer_errors = normalize_customer_qualification(
        customer_payload(qualification_status="ACTIVE"), "ITEM-1"
    )
    _, conversion_errors = validate_conversion_rule(
        conversion_payload(lifecycle_status="ACTIVE"), "ITEM-1"
    )
    assert {error["field"] for error in customer_errors} >= {
        "approved_by_role", "approved_by_business_ref", "approval_evidence_ref"
    }
    assert {error["field"] for error in conversion_errors} >= {
        "approved_by_role", "approved_by_business_ref", "approval_evidence_ref"
    }


def test_fixed_and_catch_weight_rules_do_not_receive_implicit_parameters():
    _, fixed_errors = validate_conversion_rule(
        conversion_payload(conversion_factor=None), "ITEM-1"
    )
    _, catch_errors = validate_conversion_rule(
        conversion_payload(conversion_type="CATCH_WEIGHT", conversion_factor="1"), "ITEM-1"
    )
    assert any(error["field"] == "conversion_factor" for error in fixed_errors)
    assert any(error["field"] == "conversion_factor" for error in catch_errors)


def test_resolver_is_item_specific_and_never_uses_global_rule():
    rows = [
        {
            "item_id": None,
            "from_item_uom_id": "UOM-1",
            "to_item_uom_id": "UOM-2",
            "lifecycle_status": "ACTIVE",
            "effective_from": "2026-01-01 00:00:00",
        },
        {
            "item_id": "OTHER-ITEM",
            "from_item_uom_id": "UOM-1",
            "to_item_uom_id": "UOM-2",
            "lifecycle_status": "ACTIVE",
            "effective_from": "2026-01-01 00:00:00",
        },
    ]
    result = resolve_item_specific_conversion("ITEM-1", "UOM-1", "UOM-2", rows, "2026-10-13 00:00:00")
    assert result["status"] == 404
    assert "Item-specific" in result["errors"][0]["message"]


def test_resolver_rejects_ambiguous_active_item_rules():
    row = {
        "item_id": "ITEM-1",
        "from_item_uom_id": "UOM-1",
        "to_item_uom_id": "UOM-2",
        "lifecycle_status": "ACTIVE",
        "effective_from": "2026-01-01 00:00:00",
    }
    result = resolve_item_specific_conversion("ITEM-1", "UOM-1", "UOM-2", [row, dict(row)], "2026-10-13 00:00:00")
    assert result["status"] == 409


class ScriptedCursor:
    def __init__(self, connection, responses):
        self.connection = connection
        self.responses = responses
        self.executed = []
        self.current = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def execute(self, sql, params=()):
        self.executed.append((sql, params))
        self.current = self.responses.pop(0) if self.responses else None

    def fetchone(self):
        if isinstance(self.current, list):
            return self.current.pop(0) if self.current else None
        value, self.current = self.current, None
        return value

    def fetchall(self):
        value, self.current = self.current or [], None
        return value if isinstance(value, list) else [value]


class ScriptedConnection:
    def __init__(self, responses):
        self.responses = list(responses)
        self.cursor_instance = ScriptedCursor(self, self.responses)
        self.commits = 0
        self.rollbacks = 0
        self.closed = False

    def cursor(self):
        return self.cursor_instance

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1

    def close(self):
        self.closed = True


def test_customer_write_locks_item_before_relationship_and_returns_idempotent_retry():
    first_connection = ScriptedConnection([{"item_id": "ITEM-1"}, None, None])
    service = C2Service(lambda: first_connection)
    result = service.create_customer_qualification("ITEM-1", customer_payload())
    assert result["status"] == 201
    assert first_connection.commits == 1
    assert "FOR UPDATE" in first_connection.cursor_instance.executed[0][0]
    assert first_connection.cursor_instance.executed[0][0].startswith("SELECT item_id FROM item")

    replay_connection = ScriptedConnection([{"item_id": "ITEM-1"}, {
        "customer_qualification_id": "CQ-1",
        "item_id": "ITEM-1",
        "customer_ref": "CUSTOMER-A",
        "supplier_qualification_id": None,
        "specification_id": None,
        "approval_scope": "ANY_GENERAL_QUALIFIED_SUPPLIER",
        "supply_method": "DIRECT",
        "qualification_status": "DRAFT",
        "effective_from": "2026-10-13 00:00:00",
        "effective_to": None,
        "source_reference": "C2-TEST",
    }])
    replay_service = C2Service(lambda: replay_connection)
    replay = replay_service.create_customer_qualification("ITEM-1", customer_payload())
    assert replay["status"] == 200
    assert replay["idempotent_replay"] is True
    assert replay_connection.rollbacks == 1


def test_customer_write_rejects_wrong_item_supplier_before_insert():
    connection = ScriptedConnection([{"item_id": "ITEM-1"}, None])
    service = C2Service(lambda: connection)
    result = service.create_customer_qualification(
        "ITEM-1",
        customer_payload(approval_scope="SPECIFIC_SUPPLIER", supplier_qualification_id="SUP-OTHER"),
    )
    assert result["status"] == 409
    assert connection.commits == 0
    assert connection.rollbacks == 1


def test_rest_surface_is_injected_and_conversion_endpoint_never_has_global_fallback():
    class StubService:
        def create_customer_qualification(self, *_):
            return {"ok": False, "status": 400, "errors": [{"field": "x", "message": "rejected"}]}

        def create_conversion_rule(self, *_):
            return {"ok": False, "status": 400, "errors": [{"field": "x", "message": "rejected"}]}

        def resolve_conversion(self, *_):
            return {"ok": False, "status": 404, "errors": [{"field": "conversion", "message": "no active Item-specific conversion rule exists"}]}

    client = build_app(StubService()).test_client()
    response = client.get("/api/v1/fm02/items/ITEM-1/uom-conversions/UOM-1/UOM-2")
    assert response.status_code == 404
    assert "Item-specific" in response.get_json()["errors"][0]["message"]
