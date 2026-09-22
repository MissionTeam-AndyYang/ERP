# coding=utf8
import sys
from pathlib import Path


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.restserver.app import create_app


URL = "/api/v2/legacy-path-b/demand-supply-evidence/overview?scenarioId=LPB-G0-SYN-SCENARIO-001"
HEADERS = {"x-auth-token": "test-only", "x-timezone": "Asia/Taipei"}


def response(client):
    return client.get(URL, headers=HEADERS)


def test_explicit_chain_and_all_six_states(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    with create_app().test_client() as client:
        payload = response(client).get_json()["payload"]
    assert {item["state"] for item in payload["evidence"]} == {"PRESENT", "ABSENT", "INCOMPLETE", "PARTIAL", "CONFLICTING", "UNAVAILABLE"}
    assert payload["chain"]["planningInterpretation"]["demandRef"] == "SYN-DEMAND-LPB-001"
    assert payload["chain"]["supplyReference"]["planningRef"] == "SYN-PLAN-INTERP-LPB-001"
    assert payload["chain"]["supplyReference"]["nonBinding"] is True
    assert payload["authoritative_winner"] is None


def test_replay_order_and_truth_boundaries(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    with create_app().test_client() as client:
        first = response(client).get_json()["payload"]
        second = response(client).get_json()["payload"]
    assert first == second
    assert [item["evidenceId"] for item in first["evidence"]] == sorted(item["evidenceId"] for item in first["evidence"])
    assert first["truthLabels"]["business_truth"] is False
    assert first["capabilityBoundary"]["readOnly"] is True
    assert first["capabilityBoundary"]["database"] is False


def test_invalid_unknown_and_write_methods_denied(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    path = "/api/v2/legacy-path-b/demand-supply-evidence/overview"
    with create_app().test_client() as client:
        missing = client.get(path, headers=HEADERS)
        unknown = client.get(path + "?scenarioId=OTHER", headers=HEADERS)
        writes = [getattr(client, method)(path, headers=HEADERS) for method in ("post", "put", "patch", "delete")]
    assert missing.status_code == 400
    assert unknown.status_code == 404
    assert [item.status_code for item in writes] == [405, 405, 405, 405]
