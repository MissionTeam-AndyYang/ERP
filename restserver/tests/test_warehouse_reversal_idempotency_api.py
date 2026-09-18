import sys
from pathlib import Path

from flask import Flask


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.restserver.api.v2.warehouse_fixture import CWarehouseFixtureP3, CWarehouseFixtureP4
from package.restserver.api.v2.warehouse_uri import warehouse_v2


VALID_REVERSAL = {
    "fixtureId": "ERP2-WH-P4-REVERSAL-IDEMPOTENCY-FIXTURE-001",
    "originalTransactionId": "fixture-transaction-p4-original-001",
    "originalReceiptId": "fixture-receipt-p4-original-001",
    "itemCategory": "MATERIAL",
    "idempotencyKey": "P4-REVERSAL-IDEMPOTENCY-001",
    "reason": "RECEIPT_REVERSAL",
    "effectivity": "2026-09-13T08:30:00+08:00",
}


def build_app(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    obj_app = Flask(__name__)
    obj_app.register_blueprint(warehouse_v2)
    return obj_app


def request_headers():
    return {"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"}


def read_state_bytes():
    return CWarehouseFixtureP4.STATE_PATH.read_bytes()


def test_p4_valid_reversal_restores_balance_and_get_readback_is_attributable(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            obj_before = obj_client.get("/api/v2/warehouse/fixture/p4", headers=request_headers())
            obj_post = obj_client.post(
                "/api/v2/warehouse/fixture/p4/reversal",
                json=VALID_REVERSAL,
                headers=request_headers(),
            )
            obj_after = obj_client.get("/api/v2/warehouse/fixture/p4", headers=request_headers())

        dict_before = obj_before.get_json()["payload"]
        dict_post = obj_post.get_json()["payload"]
        dict_after = obj_after.get_json()["payload"]
        assert obj_before.status_code == 200
        assert obj_post.status_code == 201
        assert obj_after.status_code == 200
        assert dict_before["fixture"]["fixtureId"] == "ERP2-WH-P4-REVERSAL-IDEMPOTENCY-FIXTURE-001"
        assert dict_before["balance"]["afterBalance"] == 125
        assert dict_before["originalTransaction"]["transactionId"] == "fixture-transaction-p4-original-001"
        assert dict_post["operation"]["mutationApplied"] is True
        assert dict_post["operation"]["replay"] is False
        assert dict_post["reversalTransaction"]["transactionId"] == "fixture-transaction-p4-reversal-001"
        assert dict_post["reversalMovement"]["movementId"] == "fixture-movement-p4-reversal-001"
        assert dict_post["reversalMovement"]["originalTransactionId"] == "fixture-transaction-p4-original-001"
        assert dict_post["reversalMovement"]["originalReceiptId"] == "fixture-receipt-p4-original-001"
        assert dict_post["reversalMovement"]["quantity"] == 25
        assert dict_post["reversalMovement"]["movementQuantity"] == -25
        assert dict_post["reversalMovement"]["uom"] == "EA"
        assert dict_post["reversalMovement"]["beforeBalance"] == 125
        assert dict_post["reversalMovement"]["afterBalance"] == 100
        assert dict_post["reversalMovement"]["invariantValid"] is True
        assert dict_post["balance"]["invariantValid"] is True
        assert dict_post["balance"]["afterBalance"] == 100
        assert dict_post["lineage"]["relation"] == "REVERSAL_OF"
        assert dict_post["lineage"]["evidenceLinkId"] == "fixture-evidence-p4-reversal-001"
        assert dict_post["fixture"]["classification"] == "NON-PRODUCTION / CONTROLLED VALIDATION DATA"
        assert dict_post["fixture"]["sourceClass"] == "SYNTHETIC_FIXTURE"
        assert dict_post["fixture"]["freshness"] == "NOT_MEASURED"
        assert dict_post["fixture"]["confidence"] == "CONTROLLED_FIXTURE_ONLY"
        assert dict_after["reversalMovement"] == dict_post["reversalMovement"]
        assert dict_after["reversalTransaction"] == dict_post["reversalTransaction"]
        assert dict_after["balance"]["afterBalance"] == 100
    finally:
        CWarehouseFixtureP4.STATE_PATH.write_bytes(byt_initial)


def test_p4_identical_replay_is_explicit_and_conflicts_do_not_mutate(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            obj_first = obj_client.post(
                "/api/v2/warehouse/fixture/p4/reversal",
                json=VALID_REVERSAL,
                headers=request_headers(),
            )
            byt_after_first = read_state_bytes()
            obj_replay = obj_client.post(
                "/api/v2/warehouse/fixture/p4/reversal",
                json=VALID_REVERSAL,
                headers=request_headers(),
            )
            obj_conflict = obj_client.post(
                "/api/v2/warehouse/fixture/p4/reversal",
                json=dict(VALID_REVERSAL, reason="OTHER_REASON"),
                headers=request_headers(),
            )
            obj_duplicate = obj_client.post(
                "/api/v2/warehouse/fixture/p4/reversal",
                json=dict(VALID_REVERSAL, idempotencyKey="P4-REVERSAL-IDEMPOTENCY-002"),
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
        assert obj_duplicate.get_json()["payload"]["status"] == "DUPLICATE_REVERSAL"
        assert obj_duplicate.get_json()["payload"]["mutationApplied"] is False
        assert read_state_bytes() == byt_after_first
    finally:
        CWarehouseFixtureP4.STATE_PATH.write_bytes(byt_initial)


def test_p4_invalid_identity_category_reason_effectivity_and_fields_do_not_mutate(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        dict_invalid_cases = [
            ("missing_field", {str_key: str_value for str_key, str_value in VALID_REVERSAL.items() if str_key != "reason"}),
            ("wrong_fixture", dict(VALID_REVERSAL, fixtureId="WRONG-FIXTURE")),
            ("wrong_transaction", dict(VALID_REVERSAL, originalTransactionId="wrong-transaction")),
            ("wrong_receipt", dict(VALID_REVERSAL, originalReceiptId="wrong-receipt")),
            ("wrong_category", dict(VALID_REVERSAL, itemCategory="PRODUCT")),
            ("unsupported_reason", dict(VALID_REVERSAL, reason="ADJUSTMENT")),
            ("invalid_effectivity", dict(VALID_REVERSAL, effectivity="not-deterministic")),
            ("arbitrary_quantity", dict(VALID_REVERSAL, quantity=25)),
        ]
        with obj_app.test_client() as obj_client:
            for str_case, dict_body in dict_invalid_cases:
                obj_response = obj_client.post(
                    "/api/v2/warehouse/fixture/p4/reversal",
                    json=dict_body,
                    headers=request_headers(),
                )
                assert obj_response.status_code == 400, str_case
                assert obj_response.get_json()["payload"]["mutationApplied"] is False, str_case
                assert read_state_bytes() == byt_initial, str_case
    finally:
        CWarehouseFixtureP4.STATE_PATH.write_bytes(byt_initial)


def test_p4_reset_replay_is_byte_stable_and_p3_state_is_not_touched(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()
    obj_p3_path = CWarehouseFixtureP3.STATE_PATH
    byt_p3_initial = obj_p3_path.read_bytes()

    try:
        with obj_app.test_client() as obj_client:
            dict_first = obj_client.post(
                "/api/v2/warehouse/fixture/p4/reversal",
                json=VALID_REVERSAL,
                headers=request_headers(),
            ).get_json()

        byt_after_first = read_state_bytes()
        str_after_hash = dict_first["payload"]["operation"]["stateSha256After"]
        assert byt_after_first != byt_initial
        assert str_after_hash != dict_first["payload"]["operation"]["stateSha256Before"]
        CWarehouseFixtureP4.STATE_PATH.write_bytes(byt_initial)
        assert read_state_bytes() == byt_initial
        assert obj_p3_path.read_bytes() == byt_p3_initial

        with obj_app.test_client() as obj_client:
            dict_second = obj_client.post(
                "/api/v2/warehouse/fixture/p4/reversal",
                json=VALID_REVERSAL,
                headers=request_headers(),
            ).get_json()

        assert dict_second == dict_first
        assert obj_p3_path.read_bytes() == byt_p3_initial
    finally:
        CWarehouseFixtureP4.STATE_PATH.write_bytes(byt_initial)
        obj_p3_path.write_bytes(byt_p3_initial)


def test_p4_denies_put_patch_delete_and_keeps_state_unchanged(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            for str_method in ("put", "patch", "delete"):
                obj_response = getattr(obj_client, str_method)(
                    "/api/v2/warehouse/fixture/p4/reversal",
                    json=VALID_REVERSAL,
                    headers=request_headers(),
                )
                assert obj_response.status_code == 405
                assert read_state_bytes() == byt_initial
    finally:
        CWarehouseFixtureP4.STATE_PATH.write_bytes(byt_initial)
