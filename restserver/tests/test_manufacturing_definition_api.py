# coding=utf8
import os
import sys
from pathlib import Path


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.common.common import EErrorCode
from package.restserver.app import create_app


def request(client, item_no, category):
    return client.get(
        "/api/v2/manufacturing-definition/overview?itemNo=%s&itemCategory=%s" % (item_no, category),
        headers={"x-auth-token": "test-only", "x-timezone": "Asia/Taipei"},
    )


def test_product_fixture_preserves_candidates_readiness_and_no_write_boundary(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    with create_app().test_client() as client:
        response = request(client, "ERP2-BMP-FG-001", 5)
    assert response.status_code == 200
    payload = response.get_json()["payload"]
    assert payload["resolutionStatus"] == "RESOLVED_WITH_WARNINGS"
    assert len(payload["definitionCandidate"]["recipeVersions"]) == 2
    assert payload["domainReferences"]["packaging"]["moduleReadiness"][0]["statusCode"] == "INCOMPLETE"
    assert payload["planningReadiness"]["calculationSupported"] is False
    assert payload["capabilityBoundary"]["readOnly"] is True
    assert payload["capabilityBoundary"]["manufacturingDefinitionWriteSupported"] is False


def test_partial_wip_preserves_missing_routing_without_winner_selection(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    with create_app().test_client() as client:
        response = request(client, "ERP2-BMP-WIP-001", 4)
    assert response.status_code == 200
    payload = response.get_json()["payload"]
    assert payload["resolutionStatus"] == "PARTIAL_CANDIDATE"
    assert payload["domainReferences"]["routing"]["moduleReadiness"][0]["statusCode"] == "UNAVAILABLE"
    assert "routing" in payload["planningReadiness"]["missingEvidence"]


def test_unknown_invalid_and_denied_write_are_non_mutating(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    with create_app().test_client() as client:
        unknown = request(client, "NOT-FOUND", 5)
        invalid = request(client, "ERP2-BMP-FG-001", 99)
        denied = client.post("/api/v2/manufacturing-definition/overview", json={}, headers={"x-auth-token": "test-only"})
    assert unknown.status_code == 404
    assert invalid.status_code == 400
    assert invalid.get_json()["code"] == EErrorCode.ERROR_INVAILD_PARAM
    assert denied.status_code == 405


def test_fixture_response_is_deterministic_for_same_subject(monkeypatch):
    monkeypatch.setenv("TOKEN_ENABLED", "1")
    with create_app().test_client() as client:
        first = request(client, "ERP2-BMP-FG-001", 5).get_json()["payload"]
        second = request(client, "ERP2-BMP-FG-001", 5).get_json()["payload"]
    first.pop("serverTimestamp")
    second.pop("serverTimestamp")
    assert first == second
