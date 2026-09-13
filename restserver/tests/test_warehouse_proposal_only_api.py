import json
import sys
from pathlib import Path

from flask import Flask


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.restserver.api.v2.warehouse_fixture import CWarehouseFixtureP6
from package.restserver.api.v2.warehouse_uri import warehouse_v2


VALID_PROPOSAL = {
    "proposalId": "fixture-proposal-p6-001",
    "originalTransactionId": "fixture-transaction-p6-original-001",
    "originalSource": "P6_CONTROLLED_ORIGINAL_EVIDENCE",
    "originalSourceRecordId": "fixture-source-record-p6-original-001",
    "originalTransactionType": "RECEIPT",
    "originalItemId": "fixture-item-p6-001",
    "originalItemCategory": "MATERIAL",
    "warehouseCode": "WH-P6-001",
    "locationCode": "LOC-P6-A",
    "proposalType": "CORRECTION_PROPOSAL",
    "proposedQuantity": 95,
    "reasonCode": "CONTROLLED_RECONCILIATION_PROPOSAL",
    "reasonText": "Preview-only controlled reconciliation proposal",
    "proposerId": "engineering-b-v2",
    "proposerRole": "CTO-owned Engineering B V2",
    "createdAt": "2026-09-13T10:00:00+08:00",
    "proposedEffectiveDate": "2026-09-14",
    "idempotencyKey": "P6-PROPOSAL-IDEMPOTENCY-001",
    "reviewNote": "REVIEW_REQUIRED: preview only",
    "policyReference": "P6-CONTROLLED-PREVIEW-001",
}


def build_app(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    obj_app = Flask(__name__)
    obj_app.register_blueprint(warehouse_v2)
    return obj_app


def request_headers():
    return {"x-auth-token": "test-token", "x-timezone": "Asia/Taipei"}


def read_state_bytes():
    return CWarehouseFixtureP6.STATE_PATH.read_bytes()


def test_p6_proposal_preserves_original_and_exposes_preview_only_impact(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()
    dict_initial_state = json.loads(byt_initial.decode("utf-8"))

    try:
        with obj_app.test_client() as obj_client:
            obj_before = obj_client.get("/api/v2/warehouse/fixture/p6", headers=request_headers())
            obj_post = obj_client.post(
                "/api/v2/warehouse/fixture/p6/proposal",
                json=VALID_PROPOSAL,
                headers=request_headers(),
            )
            obj_after = obj_client.get("/api/v2/warehouse/fixture/p6", headers=request_headers())

        dict_before = obj_before.get_json()["payload"]
        dict_post = obj_post.get_json()["payload"]
        dict_after = obj_after.get_json()["payload"]
        assert obj_before.status_code == 200
        assert obj_post.status_code == 201
        assert obj_after.status_code == 200
        assert dict_before["original"]["immutable"] is True
        assert dict_before["original"]["transactionId"] == "fixture-transaction-p6-original-001"
        assert dict_before["original"]["evidenceSha256"]
        assert dict_before["proposal"] is None
        assert dict_before["allowedStatuses"] == ["DRAFT", "PROPOSED", "REVIEW_REQUIRED", "REJECTED", "CANCELLED"]
        assert dict_post["operation"]["mutationApplied"] is True
        assert dict_post["operation"]["authoritativeStateChanged"] is False
        assert dict_post["proposal"]["proposalId"] == "fixture-proposal-p6-001"
        assert dict_post["proposal"]["status"] == "REVIEW_REQUIRED"
        assert dict_post["proposal"]["effective"] is False
        assert dict_post["proposal"]["proposedDelta"] == -5
        assert dict_post["proposal"]["before"]["label"] == "PREVIEW ONLY / NOT OFFICIAL BALANCE"
        assert dict_post["proposal"]["after"]["label"] == "PREVIEW ONLY / NOT OFFICIAL BALANCE"
        assert dict_post["preview"]["label"] == "PREVIEW ONLY / NOT OFFICIAL BALANCE"
        assert dict_post["preview"]["currentBalance"] == 100
        assert dict_post["preview"]["proposedDelta"] == -5
        assert dict_post["preview"]["projectedBalance"] == 95
        assert dict_post["preview"]["currentBalanceLabel"] == "PREVIEW ONLY / NOT OFFICIAL BALANCE"
        assert dict_post["preview"]["proposedDeltaLabel"] == "PREVIEW ONLY / NOT OFFICIAL BALANCE"
        assert dict_post["preview"]["projectedBalanceLabel"] == "PREVIEW ONLY / NOT OFFICIAL BALANCE"
        assert dict_post["preview"]["status"] == "REVIEW / BLOCKED PREVIEW CONDITION"
        assert dict_post["preview"]["reconciliationStatus"] == "CONFLICTING"
        assert dict_post["preview"]["reconciliationReference"] == 96
        assert dict_post["preview"]["reconciliationComputed"] == 95
        assert dict_post["preview"]["automaticResolution"] is False
        assert dict_post["lineage"]["relation"] == "proposes_correction_for"
        assert dict_post["lineage"]["originalEvidenceSha256"] == dict_before["original"]["evidenceSha256"]
        assert dict_post["proposal"]["proposalEvidenceSha256"]
        assert dict_post["capabilityBoundary"]["proposalOnly"] is True
        assert dict_post["capabilityBoundary"]["officialBalanceEffect"] is False
        assert dict_post["capabilityBoundary"]["officialCorrection"] is False
        assert dict_post["capabilityBoundary"]["automaticResolution"] is False
        assert dict_after["original"] == dict_post["original"]
        assert dict_after["proposal"] == dict_post["proposal"]
        dict_after_state = json.loads(read_state_bytes().decode("utf-8"))
        assert dict_after_state["original_evidence"] == dict_initial_state["original_evidence"]
        assert dict_after_state["balance"]["current_balance"] == 100
    finally:
        CWarehouseFixtureP6.STATE_PATH.write_bytes(byt_initial)


def test_p6_idempotency_replay_conflict_and_duplicate_are_non_effective(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            obj_first = obj_client.post(
                "/api/v2/warehouse/fixture/p6/proposal",
                json=VALID_PROPOSAL,
                headers=request_headers(),
            )
            byt_after_first = read_state_bytes()
            obj_replay = obj_client.post(
                "/api/v2/warehouse/fixture/p6/proposal",
                json=VALID_PROPOSAL,
                headers=request_headers(),
            )
            obj_conflict = obj_client.post(
                "/api/v2/warehouse/fixture/p6/proposal",
                json=dict(VALID_PROPOSAL, reasonText="different proposal content"),
                headers=request_headers(),
            )
            obj_duplicate = obj_client.post(
                "/api/v2/warehouse/fixture/p6/proposal",
                json=dict(VALID_PROPOSAL, idempotencyKey="P6-PROPOSAL-IDEMPOTENCY-002"),
                headers=request_headers(),
            )

        dict_first = obj_first.get_json()["payload"]
        dict_replay = obj_replay.get_json()["payload"]
        assert obj_first.status_code == 201
        assert obj_replay.status_code == 200
        assert dict_replay["operation"]["replay"] is True
        assert dict_replay["operation"]["mutationApplied"] is False
        assert dict_replay["operation"]["authoritativeStateChanged"] is False
        assert dict_replay["proposal"]["proposalId"] == dict_first["proposal"]["proposalId"]
        assert dict_replay["operation"]["stateSha256Before"] == dict_first["operation"]["stateSha256After"]
        assert read_state_bytes() == byt_after_first
        assert obj_conflict.status_code == 409
        assert obj_conflict.get_json()["payload"]["status"] == "IDEMPOTENCY_CONFLICT"
        assert obj_conflict.get_json()["payload"]["previewStatus"] == "REVIEW / BLOCKED PREVIEW CONDITION"
        assert obj_conflict.get_json()["payload"]["mutationApplied"] is False
        assert obj_duplicate.status_code == 409
        assert obj_duplicate.get_json()["payload"]["status"] == "DUPLICATE_PROPOSAL_REFERENCE"
        assert obj_duplicate.get_json()["payload"]["mutationApplied"] is False
        assert read_state_bytes() == byt_after_first
    finally:
        CWarehouseFixtureP6.STATE_PATH.write_bytes(byt_initial)


def test_p6_blocked_conditions_and_malformed_inputs_do_not_mutate(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        dict_invalid_cases = [
            ("missing_field", {str_key: str_value for str_key, str_value in VALID_PROPOSAL.items() if str_key != "reasonText"}, "MALFORMED_INPUT"),
            ("missing_lineage", dict(VALID_PROPOSAL, originalTransactionId=""), "MISSING_LINEAGE"),
            ("invalid_lineage", dict(VALID_PROPOSAL, originalTransactionId="wrong-original"), "INVALID_LINEAGE"),
            ("invalid_reason", dict(VALID_PROPOSAL, reasonCode="INVALID_REASON"), "INVALID_REASON"),
            ("negative_stock", dict(VALID_PROPOSAL, proposedQuantity=-1), "NEGATIVE_STOCK_RISK"),
            ("zero_value", dict(VALID_PROPOSAL, proposedQuantity=0), "NEGATIVE_STOCK_RISK"),
            ("downstream", dict(VALID_PROPOSAL, reviewNote="DOWNSTREAM_DEPENDENCY"), "DOWNSTREAM_DEPENDENCY"),
            ("closed_period", dict(VALID_PROPOSAL, proposedEffectiveDate="2026-08-31"), "CLOSED_PERIOD"),
            ("replacement_order", dict(VALID_PROPOSAL, proposalType="REPLACEMENT_DETAIL_PROPOSAL"), "REPLACEMENT_ORDER_DEPENDENCY"),
            ("unknown_field", dict(VALID_PROPOSAL, unexpectedField=True), "MALFORMED_INPUT"),
        ]
        with obj_app.test_client() as obj_client:
            for str_case, dict_body, str_code in dict_invalid_cases:
                obj_response = obj_client.post(
                    "/api/v2/warehouse/fixture/p6/proposal",
                    json=dict_body,
                    headers=request_headers(),
                )
                assert obj_response.status_code in (400, 409), str_case
                dict_payload = obj_response.get_json()["payload"]
                assert dict_payload["status"] == str_code, str_case
                assert dict_payload["previewStatus"] == "REVIEW / BLOCKED PREVIEW CONDITION", str_case
                assert dict_payload["mutationApplied"] is False, str_case
                assert dict_payload["authoritativeStateChanged"] is False, str_case
                assert read_state_bytes() == byt_initial, str_case
    finally:
        CWarehouseFixtureP6.STATE_PATH.write_bytes(byt_initial)


def test_p6_reset_replay_is_byte_stable_and_prior_fixtures_are_unchanged(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()
    obj_p3_path = Path(r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Warehouse_Operations\ERP2-WH-P3-RECEIPT-MOVEMENT-FIXTURE-001\state.json")
    obj_p4_path = Path(r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Warehouse_Operations\ERP2-WH-P4-REVERSAL-IDEMPOTENCY-FIXTURE-001\state.json")
    obj_p5_path = Path(r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Warehouse_Operations\ERP2-WH-P5-ADJUSTMENT-RECONCILIATION-FIXTURE-001\state.json")
    byt_p3_initial = obj_p3_path.read_bytes()
    byt_p4_initial = obj_p4_path.read_bytes()
    byt_p5_initial = obj_p5_path.read_bytes()

    try:
        with obj_app.test_client() as obj_client:
            dict_first = obj_client.post(
                "/api/v2/warehouse/fixture/p6/proposal",
                json=VALID_PROPOSAL,
                headers=request_headers(),
            ).get_json()
        byt_after_first = read_state_bytes()
        assert byt_after_first != byt_initial
        CWarehouseFixtureP6.STATE_PATH.write_bytes(byt_initial)
        assert read_state_bytes() == byt_initial
        assert obj_p3_path.read_bytes() == byt_p3_initial
        assert obj_p4_path.read_bytes() == byt_p4_initial
        assert obj_p5_path.read_bytes() == byt_p5_initial

        with obj_app.test_client() as obj_client:
            dict_second = obj_client.post(
                "/api/v2/warehouse/fixture/p6/proposal",
                json=VALID_PROPOSAL,
                headers=request_headers(),
            ).get_json()

        assert dict_second == dict_first
        assert obj_p3_path.read_bytes() == byt_p3_initial
        assert obj_p4_path.read_bytes() == byt_p4_initial
        assert obj_p5_path.read_bytes() == byt_p5_initial
    finally:
        CWarehouseFixtureP6.STATE_PATH.write_bytes(byt_initial)
        obj_p3_path.write_bytes(byt_p3_initial)
        obj_p4_path.write_bytes(byt_p4_initial)
        obj_p5_path.write_bytes(byt_p5_initial)


def test_p6_denies_put_patch_delete_and_keeps_state_unchanged(monkeypatch):
    obj_app = build_app(monkeypatch)
    byt_initial = read_state_bytes()

    try:
        with obj_app.test_client() as obj_client:
            for str_method in ("put", "patch", "delete"):
                obj_response = getattr(obj_client, str_method)(
                    "/api/v2/warehouse/fixture/p6/proposal",
                    json=VALID_PROPOSAL,
                    headers=request_headers(),
                )
                assert obj_response.status_code == 405
                assert read_state_bytes() == byt_initial
    finally:
        CWarehouseFixtureP6.STATE_PATH.write_bytes(byt_initial)
