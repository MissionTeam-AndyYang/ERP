from __future__ import annotations

import os
import threading
import uuid
from datetime import datetime

import pymysql
from pymysql.cursors import DictCursor

from fm02_foundation.foundation import ItemIntegrityService, build_app


def connection_factory():
    return pymysql.connect(
        host=os.environ.get("FM02_DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("FM02_DB_PORT", "3344")),
        user=os.environ["FM02_DB_USER"],
        password=os.environ["FM02_DB_PASSWORD"],
        database=os.environ.get("FM02_DB_NAME", "erp2_functional_dev_001"),
        cursorclass=DictCursor,
        autocommit=False,
    )


def payload(**overrides):
    value = {
        "primary_category": "MATERIAL",
        "display_name": "FM02 Sprint02 synthetic item",
        "ownership_context": "FM02-IM-FOUNDATION-INTEGRITY-01",
        "base_uom_code": "EA",
        "description": "bounded test row",
    }
    value.update(overrides)
    return value


def lifecycle_payload(key: str, **overrides):
    value = {
        "to_status": "ACTIVE",
        "reason": "bounded integration test approval",
        "business_actor_type": "BUSINESS_OWNER",
        "business_actor_ref": "TEST-BUSINESS-OWNER",
        "accountable_approval_role": "Item Master Business Owner",
        "delegated_authorization_ref": "CIO-GOV-ERP2-FM02-SPRINT02-EXECUTION-RESUME-20261012-001",
        "decision_evidence_ref": "FM02-S02-TEST-EVIDENCE",
        "request_id": f"request-{key}",
        "idempotency_key": f"idempotency-{key}",
        "technical_work_item_id": "FM02-IM-FOUNDATION-INTEGRITY-01",
        "technical_executor_assignment_id": 9002,
        "technical_executor_ref": "engineering-executor",
        "correlation_id": f"correlation-{key}",
    }
    value.update(overrides)
    return value


def create(service: ItemIntegrityService, **overrides) -> str:
    result = service.create_item(payload(**overrides), correlation_id="FM02-S02-TEST")
    assert result["status"] == 201, result
    return result["item"]["item_id"]


def delete_item(item_id: str) -> None:
    connection = connection_factory()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM item_lifecycle_event WHERE item_id=%s", (item_id,))
            cursor.execute("DELETE FROM item_approval WHERE item_id=%s", (item_id,))
            cursor.execute("DELETE FROM item_specification WHERE item_id=%s", (item_id,))
            cursor.execute("DELETE FROM item_legacy_identifier WHERE item_id=%s", (item_id,))
            cursor.execute("DELETE FROM item WHERE item_id=%s", (item_id,))
        connection.commit()
    finally:
        connection.close()


def test_post_get_compatibility_and_category_readback():
    service = ItemIntegrityService(connection_factory)
    item_id = create(service, legacy_references=[{"legacy_system": "TEST", "legacy_entity": "ITEM", "legacy_code": "FM02-001"}])
    try:
        item = service.get_item(item_id=item_id)
        assert item["status"] == 200
        assert item["item"]["primary_category"] == "MATERIAL"
        assert item["item"]["controlled_category"]["category_code"] == "MATERIAL"
        assert item["item"]["lifecycle_status"] == "DRAFT"
        assert item["item"]["row_version"] == 0
        assert len(item["item"]["legacy_references"]) == 1
        app = build_app(service)
        client = app.test_client()
        listed = client.get("/api/v1/items?primary_category=MATERIAL")
        assert listed.status_code == 200
        assert any(row["item_id"] == item_id for row in listed.get_json()["items"])
    finally:
        delete_item(item_id)


def test_negative_category_and_uom_are_rejected_without_rows():
    service = ItemIntegrityService(connection_factory)
    bad_category = service.create_item(payload(primary_category="NOT_APPROVED"))
    bad_uom = service.create_item(payload(base_uom_code="BAD"))
    assert bad_category["status"] == 400
    assert bad_uom["status"] == 400
    with connection_factory() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS n FROM item WHERE ownership_context=%s", ("FM02-IM-FOUNDATION-INTEGRITY-01",))
            assert cursor.fetchone()["n"] == 0


def test_independent_specification_lineages_and_overlap_rejection():
    service = ItemIntegrityService(connection_factory)
    item_id = create(service)
    lineage_a = str(uuid.uuid4())
    lineage_b = str(uuid.uuid4())
    base = {
        "specification_code": "SPEC-A",
        "specification_name": "Customer A bounded spec",
        "specification_hash": "A" * 64,
        "specification_summary": "bounded specification",
        "effective_from": "2026-10-12 00:00:00.000000",
    }
    try:
        first = service.add_specification(item_id, {**base, "specification_lineage_id": lineage_a, "revision_no": 1})
        second = service.add_specification(item_id, {**base, "specification_code": "SPEC-B", "specification_name": "Regulatory B bounded spec", "specification_hash": "B" * 64, "specification_lineage_id": lineage_b, "revision_no": 1})
        assert first["status"] == 201
        assert second["status"] == 201
        active = service.add_specification(item_id, {**base, "specification_lineage_id": lineage_a, "revision_no": 2, "revision_status": "ACTIVE", "approved_by_assignment_id": 9002, "effective_to": "2026-12-31 00:00:00.000000"})
        overlap = service.add_specification(item_id, {**base, "specification_lineage_id": lineage_a, "revision_no": 3, "revision_status": "ACTIVE", "approved_by_assignment_id": 9002, "effective_from": "2026-11-01 00:00:00.000000", "effective_to": "2027-01-01 00:00:00.000000"})
        assert active["status"] == 201
        assert overlap["status"] == 409
        readback = service.get_item(item_id=item_id)
        assert {row["specification_lineage_id"] for row in readback["item"]["specifications"]} == {lineage_a, lineage_b}
    finally:
        delete_item(item_id)


def test_atomic_approval_lifecycle_idempotency_and_concurrency():
    service = ItemIntegrityService(connection_factory)
    item_id = create(service)
    try:
        first_payload = lifecycle_payload("atomic")
        activated = service.change_lifecycle(item_id, first_payload)
        replay = service.change_lifecycle(item_id, first_payload)
        conflict = service.change_lifecycle(item_id, {**first_payload, "reason": "different fingerprint"})
        assert activated["status"] == 200
        assert activated["item"]["lifecycle_status"] == "ACTIVE"
        assert activated["item"]["row_version"] == 1
        assert replay["status"] == 200 and replay["idempotent_replay"] is True
        assert conflict["status"] == 409
        with connection_factory() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS n FROM item_approval WHERE item_id=%s", (item_id,))
                assert cursor.fetchone()["n"] == 1
                cursor.execute("SELECT COUNT(*) AS n FROM item_lifecycle_event WHERE item_id=%s", (item_id,))
                assert cursor.fetchone()["n"] == 1
        second_id = create(service, display_name="FM02 concurrent synthetic item")
        results = []

        def worker(key: str):
            results.append(service.change_lifecycle(second_id, lifecycle_payload(key, expected_row_version=0)))

        threads = [threading.Thread(target=worker, args=(f"concurrent-{n}",)) for n in (1, 2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        assert sorted(result["status"] for result in results) == [200, 409]
        delete_item(second_id)
    finally:
        delete_item(item_id)


def test_rollback_removes_approval_and_event_and_preserves_item():
    item_service = ItemIntegrityService(connection_factory)
    item_id = create(item_service, display_name="FM02 rollback synthetic item")

    def fail(stage: str):
        if stage == "after_approval":
            raise RuntimeError("synthetic failure after approval insert")

    failing_service = ItemIntegrityService(connection_factory, failure_hook=fail)
    try:
        result = failing_service.change_lifecycle(item_id, lifecycle_payload("rollback"))
        assert result["status"] == 500
        with connection_factory() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT lifecycle_status,row_version FROM item WHERE item_id=%s", (item_id,))
                row = cursor.fetchone()
                assert row == {"lifecycle_status": "DRAFT", "row_version": 0}
                cursor.execute("SELECT COUNT(*) AS n FROM item_approval WHERE item_id=%s", (item_id,))
                assert cursor.fetchone()["n"] == 0
                cursor.execute("SELECT COUNT(*) AS n FROM item_lifecycle_event WHERE item_id=%s", (item_id,))
                assert cursor.fetchone()["n"] == 0
    finally:
        delete_item(item_id)


def test_activation_rejects_technical_actor_and_missing_business_authority():
    service = ItemIntegrityService(connection_factory)
    item_id = create(service, display_name="FM02 approval negative synthetic item")
    try:
        technical = service.change_lifecycle(item_id, lifecycle_payload("technical", business_actor_type="ENGINEERING"))
        missing_authority = service.change_lifecycle(item_id, lifecycle_payload("authority", delegated_authorization_ref=""))
        assert technical["status"] == 403
        assert missing_authority["status"] == 400
        readback = service.get_item(item_id=item_id)
        assert readback["item"]["lifecycle_status"] == "DRAFT"
        assert readback["item"]["row_version"] == 0
    finally:
        delete_item(item_id)
