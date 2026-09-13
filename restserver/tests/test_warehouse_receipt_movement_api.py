import sys
from pathlib import Path

from flask import Flask


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.restserver.api.v2.warehouse_fixture import CWarehouseFixtureP3
from package.restserver.api.v2.warehouse_uri import warehouse_v2


VALID_RECEIPT = {
    "fixtureId": "ERP2-WH-P3-RECEIPT-MOVEMENT-FIXTURE-001",
    "itemNo": "ERP2-P3-MAT-001",
    "itemCategory": "MATERIAL",
    "warehouseCode": "WH-P3-001",
    "locationCode": "LOC-P3-A",
    "receiptNo": "P3-RECEIPT-001",
    "quantity": 25,
    "uom": "EA",
    "transactionType": "RECEIPT",
    "effectivity": "2026-09-13T08:00:00+08:00",
}


def build_app(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    obj_app = Flask(__name__)
    obj_app.register_blueprint(warehouse_v2)
    return obj_app


def request_headers():
    return {"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"}


def read_state_bytes():
    return CWarehouseFixtureP3.STATE_PATH.read_bytes()


def test_p3_receipt_creates_attributable_movement_and_get_readback(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            obj_before = obj_client.get("/api/v2/warehouse/fixture/p3", headers=request_headers())
            obj_post = obj_client.post(
                "/api/v2/warehouse/fixture/p3/receipt",
                json=VALID_RECEIPT,
                headers=request_headers(),
            )
            obj_after = obj_client.get("/api/v2/warehouse/fixture/p3", headers=request_headers())

        dict_post = obj_post.get_json()["payload"]
        dict_after = obj_after.get_json()["payload"]
        assert obj_before.status_code == 200
        assert obj_post.status_code == 201
        assert obj_after.status_code == 200
        assert dict_post["operation"]["mutationApplied"] is True
        assert dict_post["receipt"]["receiptId"] == "fixture-receipt-p3-001"
        assert dict_post["receipt"]["receiptNo"] == "P3-RECEIPT-001"
        assert dict_post["movement"]["transactionId"] == "fixture-transaction-p3-001"
        assert dict_post["movement"]["movementId"] == "fixture-movement-p3-001"
        assert dict_post["movement"]["beforeBalance"] == 100
        assert dict_post["movement"]["movementQuantity"] == 25
        assert dict_post["movement"]["afterBalance"] == 125
        assert dict_post["movement"]["invariantValid"] is True
        assert dict_post["balance"]["invariantValid"] is True
        assert dict_post["crosswalk"]["evidenceLinkId"] == "fixture-evidence-p3-001"
        assert dict_post["fixture"]["classification"] == "NON-PRODUCTION / CONTROLLED VALIDATION DATA"
        assert dict_post["fixture"]["sourceClass"] == "SYNTHETIC_FIXTURE"
        assert dict_post["fixture"]["freshness"] == "NOT_MEASURED"
        assert dict_post["fixture"]["confidence"] == "CONTROLLED_FIXTURE_ONLY"
        assert dict_after["transactions"] == dict_post["transactions"]
        assert dict_after["movement"] == dict_post["movement"]
        assert dict_after["balance"]["afterBalance"] == 125
        assert dict_after["fixture"]["stateSha256"] == dict_post["operation"]["stateSha256After"]
    finally:
        CWarehouseFixtureP3.STATE_PATH.write_bytes(byt_initial)


def test_p3_invalid_and_duplicate_receipts_do_not_mutate_state(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        dict_invalid_cases = [
            ("missing_field", {str_key: str_value for str_key, str_value in VALID_RECEIPT.items() if str_key != "receiptNo"}),
            ("zero_quantity", dict(VALID_RECEIPT, quantity=0)),
            ("negative_quantity", dict(VALID_RECEIPT, quantity=-1)),
            ("wrong_fixture", dict(VALID_RECEIPT, fixtureId="WRONG-FIXTURE")),
            ("wrong_category", dict(VALID_RECEIPT, itemCategory="PRODUCT")),
            ("unsupported_transaction", dict(VALID_RECEIPT, transactionType="TRANSFER")),
        ]
        with obj_app.test_client() as obj_client:
            for str_case, dict_body in dict_invalid_cases:
                obj_response = obj_client.post(
                    "/api/v2/warehouse/fixture/p3/receipt",
                    json=dict_body,
                    headers=request_headers(),
                )
                assert obj_response.status_code == 400, str_case
                assert obj_response.get_json()["payload"]["mutationApplied"] is False
                assert read_state_bytes() == byt_initial, str_case

            obj_valid = obj_client.post(
                "/api/v2/warehouse/fixture/p3/receipt",
                json=VALID_RECEIPT,
                headers=request_headers(),
            )
            byt_after_valid = read_state_bytes()
            obj_duplicate = obj_client.post(
                "/api/v2/warehouse/fixture/p3/receipt",
                json=VALID_RECEIPT,
                headers=request_headers(),
            )

        assert obj_valid.status_code == 201
        assert obj_duplicate.status_code == 409
        assert obj_duplicate.get_json()["payload"]["status"] == "DUPLICATE_RECEIPT"
        assert obj_duplicate.get_json()["payload"]["mutationApplied"] is False
        assert read_state_bytes() == byt_after_valid
    finally:
        CWarehouseFixtureP3.STATE_PATH.write_bytes(byt_initial)


def test_p3_reset_replay_is_byte_stable_and_deterministic(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            dict_first = obj_client.post(
                "/api/v2/warehouse/fixture/p3/receipt",
                json=VALID_RECEIPT,
                headers=request_headers(),
            ).get_json()

        byt_after_first = read_state_bytes()
        str_first_hash = dict_first["payload"]["fixture"]["stateSha256"]
        assert byt_after_first != byt_initial
        CWarehouseFixtureP3.STATE_PATH.write_bytes(byt_initial)
        assert read_state_bytes() == byt_initial

        with obj_app.test_client() as obj_client:
            dict_second = obj_client.post(
                "/api/v2/warehouse/fixture/p3/receipt",
                json=VALID_RECEIPT,
                headers=request_headers(),
            ).get_json()

        assert dict_second == dict_first
        assert dict_second["payload"]["fixture"]["stateSha256"] == str_first_hash
    finally:
        CWarehouseFixtureP3.STATE_PATH.write_bytes(byt_initial)


def test_p3_denies_put_patch_delete_and_keeps_fixture_unchanged(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            for str_method in ("put", "patch", "delete"):
                obj_response = getattr(obj_client, str_method)(
                    "/api/v2/warehouse/fixture/p3/receipt",
                    json=VALID_RECEIPT,
                    headers=request_headers(),
                )
                assert obj_response.status_code == 405
                assert read_state_bytes() == byt_initial
    finally:
        CWarehouseFixtureP3.STATE_PATH.write_bytes(byt_initial)


def test_p3_payload_contains_capability_boundary_and_crosswalk(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            dict_payload = obj_client.get(
                "/api/v2/warehouse/fixture/p3", headers=request_headers()
            ).get_json()["payload"]

        assert dict_payload["fixture"]["fixtureId"] == "ERP2-WH-P3-RECEIPT-MOVEMENT-FIXTURE-001"
        assert dict_payload["item"]["itemNo"] == "ERP2-P3-MAT-001"
        assert dict_payload["warehouse"]["warehouseCode"] == "WH-P3-001"
        assert dict_payload["location"]["locationCode"] == "LOC-P3-A"
        assert dict_payload["receipt"] is None
        assert dict_payload["movement"] is None
        assert dict_payload["balance"]["beforeBalance"] == 100
        assert dict_payload["balance"]["movementQuantity"] == 0
        assert dict_payload["balance"]["afterBalance"] == 100
        assert dict_payload["balance"]["invariantValid"] is True
        assert dict_payload["capabilityBoundary"]["boundedReceiptOnly"] is True
        assert dict_payload["capabilityBoundary"]["arbitraryUpdateDelete"] is False
        assert dict_payload["capabilityBoundary"]["sql"] is False
        assert dict_payload["sourceLineage"]["noLiveSource"] is True
    finally:
        CWarehouseFixtureP3.STATE_PATH.write_bytes(byt_initial)
