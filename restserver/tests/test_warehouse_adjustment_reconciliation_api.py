import sys
from pathlib import Path

from flask import Flask


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.restserver.api.v2.warehouse_fixture import CWarehouseFixtureP3, CWarehouseFixtureP4, CWarehouseFixtureP5
from package.restserver.api.v2.warehouse_uri import warehouse_v2


VALID_ADJUSTMENT = {
    "fixtureId": "ERP2-WH-P5-ADJUSTMENT-RECONCILIATION-FIXTURE-001",
    "itemNo": "ERP2-P5-MAT-001",
    "itemCategory": "MATERIAL",
    "warehouseCode": "WH-P5-001",
    "locationCode": "LOC-P5-A",
    "referenceTransactionId": "fixture-transaction-p5-reference-001",
    "idempotencyKey": "P5-ADJUSTMENT-IDEMPOTENCY-001",
    "signedAdjustmentDelta": -5,
    "uom": "EA",
    "operationType": "ADJUSTMENT",
    "reason": "CONTROLLED_RECONCILIATION_ADJUSTMENT",
    "effectivity": "2026-09-13T09:00:00+08:00",
}


def build_app(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    obj_app = Flask(__name__)
    obj_app.register_blueprint(warehouse_v2)
    return obj_app


def request_headers():
    return {"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"}


def read_state_bytes():
    return CWarehouseFixtureP5.STATE_PATH.read_bytes()


def test_p5_adjustment_proves_signed_delta_reconciliation_and_get_readback(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            obj_before = obj_client.get("/api/v2/warehouse/fixture/p5", headers=request_headers())
            obj_post = obj_client.post(
                "/api/v2/warehouse/fixture/p5/adjustment",
                json=VALID_ADJUSTMENT,
                headers=request_headers(),
            )
            obj_after = obj_client.get("/api/v2/warehouse/fixture/p5", headers=request_headers())

        dict_before = obj_before.get_json()["payload"]
        dict_post = obj_post.get_json()["payload"]
        dict_after = obj_after.get_json()["payload"]
        assert obj_before.status_code == 200
        assert obj_post.status_code == 201
        assert obj_after.status_code == 200
        assert dict_before["fixture"]["fixtureId"] == "ERP2-WH-P5-ADJUSTMENT-RECONCILIATION-FIXTURE-001"
        assert dict_before["balance"] == {
            "balanceId": "fixture-balance-p5-001",
            "itemId": "fixture-item-p5-001",
            "warehouseId": "fixture-warehouse-p5-001",
            "locationId": "fixture-location-p5-001",
            "uom": "EA",
            "baselineBalance": 100,
            "signedAdjustmentDelta": 0,
            "afterBalance": 100,
            "invariant": "BASELINE BALANCE + SIGNED ADJUSTMENT DELTA = AFTER BALANCE",
            "invariantValid": True,
        }
        assert dict_post["operation"]["mutationApplied"] is True
        assert dict_post["adjustmentTransaction"]["transactionId"] == "fixture-transaction-p5-adjustment-001"
        assert dict_post["adjustmentMovement"]["movementId"] == "fixture-movement-p5-adjustment-001"
        assert dict_post["adjustmentMovement"]["referenceTransactionId"] == "fixture-transaction-p5-reference-001"
        assert dict_post["adjustmentMovement"]["signedAdjustmentDelta"] == -5
        assert dict_post["adjustmentMovement"]["movementQuantity"] == -5
        assert dict_post["adjustmentMovement"]["uom"] == "EA"
        assert dict_post["adjustmentMovement"]["beforeBalance"] == 100
        assert dict_post["adjustmentMovement"]["afterBalance"] == 95
        assert dict_post["adjustmentMovement"]["invariantValid"] is True
        assert dict_post["balance"]["invariantValid"] is True
        assert dict_post["reconciliation"] == {
            "referenceAfterBalance": 94,
            "computedAfterBalance": 95,
            "difference": 1,
            "status": "CONFLICTING",
            "automaticResolution": False,
        }
        assert dict_post["crosswalk"]["adjustmentEvidenceLinkId"] == "fixture-evidence-p5-adjustment-001"
        assert dict_post["fixture"]["classification"] == "NON-PRODUCTION / CONTROLLED VALIDATION DATA"
        assert dict_post["fixture"]["sourceClass"] == "SYNTHETIC_FIXTURE"
        assert dict_post["fixture"]["freshness"] == "NOT_MEASURED"
        assert dict_post["fixture"]["confidence"] == "CONTROLLED_FIXTURE_ONLY"
        assert dict_post["capabilityBoundary"]["correctionReplacement"] is False
        assert dict_post["capabilityBoundary"]["arbitraryMovementQuantity"] is False
        assert dict_after["adjustmentMovement"] == dict_post["adjustmentMovement"]
        assert dict_after["reconciliation"] == dict_post["reconciliation"]
    finally:
        CWarehouseFixtureP5.STATE_PATH.write_bytes(byt_initial)


def test_p5_replay_conflict_and_second_reference_reject_without_mutation(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            obj_first = obj_client.post(
                "/api/v2/warehouse/fixture/p5/adjustment",
                json=VALID_ADJUSTMENT,
                headers=request_headers(),
            )
            byt_after_first = read_state_bytes()
            obj_replay = obj_client.post(
                "/api/v2/warehouse/fixture/p5/adjustment",
                json=VALID_ADJUSTMENT,
                headers=request_headers(),
            )
            obj_conflict = obj_client.post(
                "/api/v2/warehouse/fixture/p5/adjustment",
                json=dict(VALID_ADJUSTMENT, signedAdjustmentDelta=-4),
                headers=request_headers(),
            )
            obj_duplicate = obj_client.post(
                "/api/v2/warehouse/fixture/p5/adjustment",
                json=dict(VALID_ADJUSTMENT, idempotencyKey="P5-ADJUSTMENT-IDEMPOTENCY-002"),
                headers=request_headers(),
            )

        dict_first = obj_first.get_json()["payload"]
        dict_replay = obj_replay.get_json()["payload"]
        assert obj_first.status_code == 201
        assert obj_replay.status_code == 200
        assert dict_replay["operation"]["replay"] is True
        assert dict_replay["operation"]["mutationApplied"] is False
        assert dict_replay["operation"]["conflictStatus"] == "REPLAY"
        assert dict_replay["operation"]["stateSha256Before"] == dict_first["operation"]["stateSha256After"]
        assert read_state_bytes() == byt_after_first
        assert obj_conflict.status_code == 409
        assert obj_conflict.get_json()["payload"]["status"] == "IDEMPOTENCY_CONFLICT"
        assert obj_conflict.get_json()["payload"]["mutationApplied"] is False
        assert obj_duplicate.status_code == 409
        assert obj_duplicate.get_json()["payload"]["status"] == "DUPLICATE_REFERENCE_ADJUSTMENT"
        assert obj_duplicate.get_json()["payload"]["mutationApplied"] is False
        assert read_state_bytes() == byt_after_first
    finally:
        CWarehouseFixtureP5.STATE_PATH.write_bytes(byt_initial)


def test_p5_invalid_inputs_reject_without_state_mutation(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        dict_invalid_cases = [
            ("missing_field", {str_key: str_value for str_key, str_value in VALID_ADJUSTMENT.items() if str_key != "reason"}),
            ("wrong_fixture", dict(VALID_ADJUSTMENT, fixtureId="WRONG-FIXTURE")),
            ("wrong_item", dict(VALID_ADJUSTMENT, itemNo="WRONG-ITEM")),
            ("wrong_category", dict(VALID_ADJUSTMENT, itemCategory="PRODUCT")),
            ("wrong_warehouse", dict(VALID_ADJUSTMENT, warehouseCode="WRONG-WH")),
            ("wrong_location", dict(VALID_ADJUSTMENT, locationCode="WRONG-LOC")),
            ("wrong_reference", dict(VALID_ADJUSTMENT, referenceTransactionId="WRONG-REFERENCE")),
            ("zero_delta", dict(VALID_ADJUSTMENT, signedAdjustmentDelta=0)),
            ("overflow_delta", dict(VALID_ADJUSTMENT, signedAdjustmentDelta=11)),
            ("unsupported_delta", dict(VALID_ADJUSTMENT, signedAdjustmentDelta=5)),
            ("unsupported_reason", dict(VALID_ADJUSTMENT, reason="CORRECTION")),
            ("invalid_effectivity", dict(VALID_ADJUSTMENT, effectivity="not-deterministic")),
            ("arbitrary_quantity", dict(VALID_ADJUSTMENT, quantity=5)),
        ]
        with obj_app.test_client() as obj_client:
            for str_case, dict_body in dict_invalid_cases:
                obj_response = obj_client.post(
                    "/api/v2/warehouse/fixture/p5/adjustment",
                    json=dict_body,
                    headers=request_headers(),
                )
                assert obj_response.status_code == 400, str_case
                assert obj_response.get_json()["payload"]["mutationApplied"] is False, str_case
                assert read_state_bytes() == byt_initial, str_case

            obj_malformed = obj_client.post(
                "/api/v2/warehouse/fixture/p5/adjustment",
                data="not-json",
                content_type="application/json",
                headers=request_headers(),
            )
        assert obj_malformed.status_code == 400
        assert read_state_bytes() == byt_initial
    finally:
        CWarehouseFixtureP5.STATE_PATH.write_bytes(byt_initial)


def test_p5_reset_replay_is_byte_stable_and_prior_fixtures_unchanged(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()
    obj_p3_path = CWarehouseFixtureP3.STATE_PATH
    obj_p4_path = CWarehouseFixtureP4.STATE_PATH
    byt_p3_initial = obj_p3_path.read_bytes()
    byt_p4_initial = obj_p4_path.read_bytes()

    try:
        with obj_app.test_client() as obj_client:
            dict_first = obj_client.post(
                "/api/v2/warehouse/fixture/p5/adjustment",
                json=VALID_ADJUSTMENT,
                headers=request_headers(),
            ).get_json()
        byt_after_first = read_state_bytes()
        assert byt_after_first != byt_initial
        CWarehouseFixtureP5.STATE_PATH.write_bytes(byt_initial)
        assert read_state_bytes() == byt_initial
        assert obj_p3_path.read_bytes() == byt_p3_initial
        assert obj_p4_path.read_bytes() == byt_p4_initial

        with obj_app.test_client() as obj_client:
            dict_second = obj_client.post(
                "/api/v2/warehouse/fixture/p5/adjustment",
                json=VALID_ADJUSTMENT,
                headers=request_headers(),
            ).get_json()

        assert dict_second == dict_first
        assert obj_p3_path.read_bytes() == byt_p3_initial
        assert obj_p4_path.read_bytes() == byt_p4_initial
    finally:
        CWarehouseFixtureP5.STATE_PATH.write_bytes(byt_initial)
        obj_p3_path.write_bytes(byt_p3_initial)
        obj_p4_path.write_bytes(byt_p4_initial)


def test_p5_denies_put_patch_delete_and_keeps_state_unchanged(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            for str_method in ("put", "patch", "delete"):
                obj_response = getattr(obj_client, str_method)(
                    "/api/v2/warehouse/fixture/p5/adjustment",
                    json=VALID_ADJUSTMENT,
                    headers=request_headers(),
                )
                assert obj_response.status_code == 405
                assert read_state_bytes() == byt_initial
    finally:
        CWarehouseFixtureP5.STATE_PATH.write_bytes(byt_initial)
