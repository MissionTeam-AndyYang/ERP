import json
import sys
from pathlib import Path

from flask import Flask


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.restserver.api.v2.warehouse_fixture import CWarehouseFixtureP3, CWarehouseFixtureP4, CWarehouseFixtureP5, CWarehouseFixtureP6, CWarehouseFixtureP7
from package.restserver.api.v2.warehouse_uri import warehouse_v2


VALID_OUTBOUND = {
    "fixtureId": "ERP2-WH-P7-OUTBOUND-PICK-INVENTORY-DECREMENT-FIXTURE-001",
    "itemNo": "ERP2-P7-MAT-001",
    "itemCategory": "MATERIAL",
    "warehouseCode": "WH-P7-001",
    "locationCode": "LOC-P7-A",
    "outboundRequestId": "P7-OUTBOUND-REQUEST-001",
    "idempotencyKey": "P7-OUTBOUND-IDEMPOTENCY-001",
    "quantity": 20,
    "uom": "EA",
    "operationType": "PICK_OUTBOUND",
    "effectivity": "2026-09-13T10:30:00+08:00",
    "requesterId": "engineering-b-v2",
    "requesterRole": "CTO-owned Engineering B V2",
}


def build_app(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    obj_app = Flask(__name__)
    obj_app.register_blueprint(warehouse_v2)
    return obj_app


def request_headers():
    return {"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"}


def read_state_bytes():
    return CWarehouseFixtureP7.STATE_PATH.read_bytes()


def test_p7_outbound_decrements_balance_and_get_readback_is_attributable(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            obj_before = obj_client.get("/api/v2/warehouse/fixture/p7", headers=request_headers())
            obj_post = obj_client.post(
                "/api/v2/warehouse/fixture/p7/outbound",
                json=VALID_OUTBOUND,
                headers=request_headers(),
            )
            obj_after = obj_client.get("/api/v2/warehouse/fixture/p7", headers=request_headers())

        dict_before = obj_before.get_json()["payload"]
        dict_post = obj_post.get_json()["payload"]
        dict_after = obj_after.get_json()["payload"]
        assert obj_before.status_code == 200
        assert obj_post.status_code == 201
        assert obj_after.status_code == 200
        assert dict_before["baselineTransaction"]["transactionId"] == "fixture-transaction-p7-baseline-001"
        assert dict_before["outboundTransaction"] is None
        assert dict_before["balance"]["afterBalance"] == 100
        assert dict_post["operation"]["mutationApplied"] is True
        assert dict_post["operation"]["authoritativeStateChanged"] is False
        assert dict_post["outboundTransaction"]["transactionId"] == "fixture-transaction-p7-outbound-001"
        assert dict_post["outboundTransaction"]["outboundRequestId"] == "P7-OUTBOUND-REQUEST-001"
        assert dict_post["outboundTransaction"]["operationType"] == "PICK_OUTBOUND"
        assert dict_post["movement"]["movementId"] == "fixture-movement-p7-outbound-001"
        assert dict_post["movement"]["quantity"] == 20
        assert dict_post["movement"]["movementQuantity"] == -20
        assert dict_post["movement"]["uom"] == "EA"
        assert dict_post["movement"]["beforeBalance"] == 100
        assert dict_post["movement"]["afterBalance"] == 80
        assert dict_post["movement"]["invariantValid"] is True
        assert dict_post["balance"]["invariantValid"] is True
        assert dict_post["balance"]["afterBalance"] == 80
        assert dict_post["balance"]["outboundQuantity"] == 20
        assert dict_post["crosswalk"]["outboundEvidenceLinkId"] == "fixture-evidence-p7-outbound-001"
        assert dict_post["fixture"]["classification"] == "NON-PRODUCTION / CONTROLLED VALIDATION DATA"
        assert dict_post["fixture"]["sourceClass"] == "SYNTHETIC_FIXTURE"
        assert dict_post["fixture"]["freshness"] == "NOT_MEASURED"
        assert dict_post["fixture"]["confidence"] == "CONTROLLED_FIXTURE_ONLY"
        assert dict_post["reconciliation"]["status"] == "NOT_EVALUATED"
        assert dict_after["movement"] == dict_post["movement"]
        assert dict_after["balance"]["afterBalance"] == 80
    finally:
        CWarehouseFixtureP7.STATE_PATH.write_bytes(byt_initial)


def test_p7_insufficient_and_invalid_inputs_reject_without_mutation(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        dict_invalid_cases = [
            ("insufficient", dict(VALID_OUTBOUND, quantity=101), "INSUFFICIENT_QUANTITY"),
            ("invalid_item", dict(VALID_OUTBOUND, itemNo="WRONG-ITEM"), "WRONG_ITEM_IDENTITY"),
            ("invalid_location", dict(VALID_OUTBOUND, locationCode="WRONG-LOC"), "WRONG_LOCATION_IDENTITY"),
            ("invalid_category", dict(VALID_OUTBOUND, itemCategory="PRODUCT"), "WRONG_ITEM_CATEGORY"),
            ("zero_quantity", dict(VALID_OUTBOUND, quantity=0), "INVALID_QUANTITY"),
            ("negative_quantity", dict(VALID_OUTBOUND, quantity=-1), "INVALID_QUANTITY"),
            ("overflow_quantity", dict(VALID_OUTBOUND, quantity=31), "QUANTITY_OVERFLOW"),
            ("wrong_uom", dict(VALID_OUTBOUND, uom="KG"), "UNSUPPORTED_UOM"),
            ("malformed", dict(VALID_OUTBOUND, unsupported=True), "MALFORMED_INPUT"),
            ("missing_identity", {str_key: str_value for str_key, str_value in VALID_OUTBOUND.items() if str_key != "outboundRequestId"}, "MISSING_FIELD"),
        ]
        with obj_app.test_client() as obj_client:
            for str_case, dict_body, str_code in dict_invalid_cases:
                obj_response = obj_client.post(
                    "/api/v2/warehouse/fixture/p7/outbound",
                    json=dict_body,
                    headers=request_headers(),
                )
                assert obj_response.status_code in (400, 409), str_case
                dict_payload = obj_response.get_json()["payload"]
                assert dict_payload["status"] == str_code, str_case
                assert dict_payload["mutationApplied"] is False, str_case
                assert dict_payload["authoritativeStateChanged"] is False, str_case
                assert read_state_bytes() == byt_initial, str_case
    finally:
        CWarehouseFixtureP7.STATE_PATH.write_bytes(byt_initial)


def test_p7_replay_conflict_and_duplicate_do_not_decrement_twice(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            obj_first = obj_client.post(
                "/api/v2/warehouse/fixture/p7/outbound",
                json=VALID_OUTBOUND,
                headers=request_headers(),
            )
            byt_after_first = read_state_bytes()
            obj_replay = obj_client.post(
                "/api/v2/warehouse/fixture/p7/outbound",
                json=VALID_OUTBOUND,
                headers=request_headers(),
            )
            obj_conflict = obj_client.post(
                "/api/v2/warehouse/fixture/p7/outbound",
                json=dict(VALID_OUTBOUND, quantity=19),
                headers=request_headers(),
            )
            obj_duplicate = obj_client.post(
                "/api/v2/warehouse/fixture/p7/outbound",
                json=dict(VALID_OUTBOUND, idempotencyKey="P7-OUTBOUND-IDEMPOTENCY-002"),
                headers=request_headers(),
            )

        dict_first = obj_first.get_json()["payload"]
        dict_replay = obj_replay.get_json()["payload"]
        assert obj_first.status_code == 201
        assert obj_replay.status_code == 200
        assert dict_replay["operation"]["replay"] is True
        assert dict_replay["operation"]["mutationApplied"] is False
        assert dict_replay["operation"]["stateSha256Before"] == dict_first["operation"]["stateSha256After"]
        assert dict_replay["balance"]["afterBalance"] == 80
        assert read_state_bytes() == byt_after_first
        assert obj_conflict.status_code == 409
        assert obj_conflict.get_json()["payload"]["status"] == "IDEMPOTENCY_CONFLICT"
        assert obj_conflict.get_json()["payload"]["mutationApplied"] is False
        assert obj_duplicate.status_code == 409
        assert obj_duplicate.get_json()["payload"]["status"] == "DUPLICATE_OUTBOUND_REQUEST"
        assert obj_duplicate.get_json()["payload"]["mutationApplied"] is False
        assert read_state_bytes() == byt_after_first
    finally:
        CWarehouseFixtureP7.STATE_PATH.write_bytes(byt_initial)


def test_p7_reset_replay_is_byte_stable_and_prior_fixtures_are_unchanged(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()
    obj_prior_paths = [
        CWarehouseFixtureP3.STATE_PATH,
        CWarehouseFixtureP4.STATE_PATH,
        CWarehouseFixtureP5.STATE_PATH,
        CWarehouseFixtureP6.STATE_PATH,
    ]
    dict_prior_bytes = {obj_path: obj_path.read_bytes() for obj_path in obj_prior_paths}

    try:
        with obj_app.test_client() as obj_client:
            dict_first = obj_client.post(
                "/api/v2/warehouse/fixture/p7/outbound",
                json=VALID_OUTBOUND,
                headers=request_headers(),
            ).get_json()
        byt_after_first = read_state_bytes()
        assert byt_after_first != byt_initial
        CWarehouseFixtureP7.STATE_PATH.write_bytes(byt_initial)
        assert read_state_bytes() == byt_initial
        assert all(obj_path.read_bytes() == byt_bytes for obj_path, byt_bytes in dict_prior_bytes.items())

        with obj_app.test_client() as obj_client:
            dict_second = obj_client.post(
                "/api/v2/warehouse/fixture/p7/outbound",
                json=VALID_OUTBOUND,
                headers=request_headers(),
            ).get_json()

        assert dict_second == dict_first
        assert all(obj_path.read_bytes() == byt_bytes for obj_path, byt_bytes in dict_prior_bytes.items())
    finally:
        CWarehouseFixtureP7.STATE_PATH.write_bytes(byt_initial)
        for obj_path, byt_bytes in dict_prior_bytes.items():
            obj_path.write_bytes(byt_bytes)


def test_p7_denies_put_patch_delete_and_keeps_state_unchanged(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            for str_method in ("put", "patch", "delete"):
                obj_response = getattr(obj_client, str_method)(
                    "/api/v2/warehouse/fixture/p7/outbound",
                    json=VALID_OUTBOUND,
                    headers=request_headers(),
                )
                assert obj_response.status_code == 405
                assert read_state_bytes() == byt_initial
    finally:
        CWarehouseFixtureP7.STATE_PATH.write_bytes(byt_initial)
