from __future__ import annotations

import pytest

from .mutation_contract import FM01ContractError, FM01MutationGateway, MutationActor, MutationRequest


def _request(**overrides):
    values = {
        "resource": "companies",
        "entity_id": 10,
        "operation": "update",
        "payload": {"display_name": "Updated"},
        "expected_row_version": 1,
        "idempotency_key": "idem-1",
        "correlation_id": "corr-1",
        "actor": MutationActor("maintainer-1", "Master Data Maintainer"),
    }
    values.update(overrides)
    return MutationRequest(**values)


def test_update_rejects_non_allowlisted_fields():
    gateway = FM01MutationGateway()
    with pytest.raises(FM01ContractError) as error:
        gateway.submit_update(_request(payload={"company_ref": "NEW"}))
    assert error.value.code == "IMMUTABLE_FIELD"


def test_self_approval_is_rejected_before_binding_check():
    gateway = FM01MutationGateway()
    with pytest.raises(FM01ContractError) as error:
        gateway.submit_update(_request(approver_id="maintainer-1"))
    assert error.value.code == "SELF_APPROVAL_FORBIDDEN"


def test_missing_runtime_binding_fails_closed():
    gateway = FM01MutationGateway()
    with pytest.raises(FM01ContractError) as error:
        gateway.submit_update(_request())
    assert error.value.code == "MUTATION_NOT_BOUND"
    assert error.value.status == 503


def test_fingerprint_is_stable_for_mapping_order():
    first = _request(payload={"display_name": "Updated", "nested": {"b": 2, "a": 1}})
    second = _request(payload={"nested": {"a": 1, "b": 2}, "display_name": "Updated"})
    assert FM01MutationGateway.fingerprint(first) == FM01MutationGateway.fingerprint(second)
