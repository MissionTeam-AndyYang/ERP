# coding=utf8
import sys
from pathlib import Path


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.restserver.app import create_app


URL = "/api/v2/quality-trace-delivery-evidence/overview?lotNo=CAND-C-LOT-001&deliveryReference=CAND-C-DELIVERY-001"
HEADERS = {"x-auth-token": "test-only", "x-timezone": "Asia/Taipei"}


def response(client):
    return client.get(URL, headers=HEADERS)


def test_six_states_explicit_link_and_no_winner(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    with create_app().test_client() as client:
        payload = response(client).get_json()["payload"]
    assert {item["state"] for item in payload["evidence"]} == {"PRESENT", "ABSENT", "INCOMPLETE", "PARTIAL", "CONFLICTING", "UNAVAILABLE"}
    assert payload["lotToDelivery"]["evidenceIds"] == ["D-LINKED-001"]
    assert payload["unlinkedDeliveryEvidence"][0]["evidenceId"] == "D-UNLINKED-001"
    assert payload["authoritative_winner"] is None


def test_deterministic_order_replay_and_truth_boundaries(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    with create_app().test_client() as client:
        first = response(client).get_json()["payload"]
        second = response(client).get_json()["payload"]
    assert first == second
    assert [item["evidenceId"] for item in first["evidence"]] == sorted(item["evidenceId"] for item in first["evidence"])
    assert first["truthLabels"]["business_truth"] is False
    assert first["capabilityBoundary"]["readOnly"] is True


def test_invalid_unknown_and_write_methods_are_denied(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    with create_app().test_client() as client:
        missing = client.get("/api/v2/quality-trace-delivery-evidence/overview", headers=HEADERS)
        unknown = client.get("/api/v2/quality-trace-delivery-evidence/overview?lotNo=OTHER&deliveryReference=CAND-C-DELIVERY-001", headers=HEADERS)
        post = client.post("/api/v2/quality-trace-delivery-evidence/overview", headers=HEADERS)
    assert missing.status_code == 400
    assert unknown.status_code == 404
    assert post.status_code == 405
