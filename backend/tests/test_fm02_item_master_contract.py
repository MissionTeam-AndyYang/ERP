from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FOUNDATION = ROOT / "04_Engineering" / "Application" / "ERP-2.0" / "restserver" / "package" / "fm02_foundation" / "foundation.py"


def test_item_master_contract_routes_and_lifecycle_are_present():
    source = FOUNDATION.read_text(encoding="utf-8")
    assert '@app.post("/api/v1/items")' in source
    assert '@app.patch("/api/v1/items/<item_id>")' in source
    assert '@app.post("/api/v1/items/<item_id>/lifecycle")' in source
    for status in ("DRAFT", "ACTIVE", "BLOCKED", "INACTIVE", "SUPERSEDED", "RETIRED"):
        assert f'"{status}"' in source
    assert 'successor_relationship_id' in source
    assert 'item_successor_relationship' in source
    assert 'reentry_review_evidence_ref' in source
    assert 'required for name correction audit' in source


def test_item_master_backend_points_to_approved_schema_contract():
    source = FOUNDATION.read_text(encoding="utf-8")
    assert "item_code_allocation" in source
    assert "reservation_reason" in source
    assert "item_name_change_audit" in source
    assert "approval_evidence_ref" in source
    assert "item_successor_relationship" not in source or "successor_relationship_id" in source


def test_item_master_implementation_does_not_execute_database_or_runtime_operations():
    source = FOUNDATION.read_text(encoding="utf-8")
    assert "subprocess" not in source
    assert "CREATE DATABASE" not in source.upper()
    assert "DROP DATABASE" not in source.upper()
