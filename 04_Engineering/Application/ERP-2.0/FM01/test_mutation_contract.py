from __future__ import annotations

import pytest

from .mutation_contract import (
    FM01ApprovalService,
    FM01ApprovalAuditAdapter,
    FM01ContractError,
    FM01MutationGateway,
    FM01InMemoryIdempotencyStore,
    FM01MutationCoordinator,
    MutationActor,
    MutationRequest,
)


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


def test_missing_atomic_persistence_binding_fails_closed():
    class Pending:
        def submit(self, request, fingerprint):
            return {"status": "pending_approval"}

        def replay(self, idempotency_key, fingerprint):
            return None

    class Audit:
        def append(self, request, before, after):
            return None

    gateway = FM01MutationGateway(
        pending_store=Pending(),
        audit_store=Audit(),
        runtime_authorizer=lambda request: True,
    )
    with pytest.raises(FM01ContractError) as error:
        gateway.submit_create(_request(operation="create", payload={"display_name": "New"}))
    assert error.value.code == "MUTATION_NOT_BOUND"


def test_fingerprint_is_stable_for_mapping_order():
    first = _request(payload={"display_name": "Updated", "nested": {"b": 2, "a": 1}})
    second = _request(payload={"nested": {"a": 1, "b": 2}, "display_name": "Updated"})
    assert FM01MutationGateway.fingerprint(first) == FM01MutationGateway.fingerprint(second)


def test_approval_service_submits_and_replays_without_final_effect():
    class Store:
        def __init__(self):
            self.rows = {}

        def find_idempotent(self, scope, key, fingerprint):
            row = self.rows.get((scope, key))
            if row is None:
                return None
            if row["fingerprint"] != fingerprint:
                raise FM01ContractError("IDEMPOTENCY_CONFLICT", "idempotency request conflicts", 409)
            return row

        def create_pending(self, request, fingerprint):
            row = {"approval_state": "PENDING_APPROVAL", "fingerprint": fingerprint}
            self.rows[("fm01", request.idempotency_key)] = row
            return row

        def decide(self, request_id, approver_id, approved, note):
            return {"approval_state": "APPROVED" if approved else "REJECTED"}

    service = FM01ApprovalService(Store())
    request = _request(operation="create", payload={"display_name": "New"})
    first = service.submit(request, "fm01")
    second = service.submit(request, "fm01")
    assert first == second
    assert first["approval_state"] == "PENDING_APPROVAL"


def test_approval_service_rejects_self_approval_and_missing_note():
    class Store:
        def decide(self, request_id, approver_id, approved, note):
            return {}

    service = FM01ApprovalService(Store())
    with pytest.raises(FM01ContractError) as error:
        service.decide(1, "same", "same", True, "approve")
    assert error.value.code == "SELF_APPROVAL_FORBIDDEN"
    with pytest.raises(FM01ContractError) as error:
        service.decide(1, "requester", "approver", True, "")
    assert error.value.code == "DECISION_NOTE_REQUIRED"


def test_persistence_adapter_rolls_back_when_audit_write_fails():
    class Session:
        def __init__(self):
            self.committed = False
            self.rolled_back = False
            self.values = []

        def begin(self):
            return self

        def add(self, value):
            self.values.append(value)
            if value.get("event_type") == "REQUEST_SUBMITTED":
                raise RuntimeError("synthetic audit failure")

        def flush(self):
            self.values[0]["approval_request_id"] = 1

        def commit(self):
            self.committed = True

        def rollback(self):
            self.rolled_back = True

    session = Session()
    adapter = FM01ApprovalAuditAdapter(lambda: session)
    with pytest.raises(FM01ContractError) as error:
        adapter.create_pending(_request(operation="create", payload={"display_name": "New"}), "f" * 64)
    assert error.value.code == "PERSISTENCE_FAILED"
    assert session.rolled_back is True
    assert session.committed is False


def test_approval_adapter_decision_uses_requester_and_approver_contract():
    class Session:
        def __init__(self):
            self.values = []
            self.committed = False

        def add(self, value):
            self.values.append(value)

        def flush(self):
            return None

        def commit(self):
            self.committed = True

        def rollback(self):
            raise AssertionError("rollback was not expected")

    session = Session()
    adapter = FM01ApprovalAuditAdapter(lambda: session)
    result = adapter.decide(7, "requester-1", "approver-1", True, "approved by independent reviewer")
    assert result["approval_state"] == "APPROVED"
    assert result["approver_id"] == "approver-1"
    assert session.values[1]["actor_id"] == "approver-1"
    assert session.committed is True


def test_row_version_is_carried_to_pending_request_shape():
    class Session:
        def add(self, value):
            self.value = value

        def flush(self):
            self.value["approval_request_id"] = 1

        def commit(self):
            return None

        def rollback(self):
            return None

    session = Session()
    adapter = FM01ApprovalAuditAdapter(lambda: session)
    row = adapter.create_pending(_request(operation="create", payload={"display_name": "New"}), "f" * 64)
    assert row["row_version"] == 1


def test_coordinator_replays_same_request_and_rejects_conflicting_fingerprint():
    class Entity:
        def __init__(self):
            self.applied = 0

        def read_row_version(self, resource, entity_id):
            return 1 if self.applied == 0 else 2

        def validate_parent_and_lifecycle(self, request):
            return None

        def apply_business_effect(self, request):
            self.applied += 1
            return {"approval_state": "PENDING_APPROVAL", "applied": self.applied}

    entity = Entity()
    coordinator = FM01MutationCoordinator(FM01InMemoryIdempotencyStore(), entity)
    request = _request(operation="create", payload={"display_name": "New"})
    first = coordinator.submit(request, "fm01")
    replay = coordinator.submit(request, "fm01")
    assert first["replayed"] is False
    entity.applied = 1
    assert replay["replayed"] is True
    assert entity.applied == 1
    with pytest.raises(FM01ContractError) as error:
        coordinator.submit(_request(operation="create", payload={"display_name": "Other"}), "fm01")
    assert error.value.code == "IDEMPOTENCY_CONFLICT"


def test_coordinator_rejects_stale_row_version_before_business_effect():
    class Entity:
        def read_row_version(self, resource, entity_id):
            return 2

        def validate_parent_and_lifecycle(self, request):
            raise AssertionError("validation must not run for stale input")

        def apply_business_effect(self, request):
            raise AssertionError("business effect must not run for stale input")

    coordinator = FM01MutationCoordinator(FM01InMemoryIdempotencyStore(), Entity())
    with pytest.raises(FM01ContractError) as error:
        coordinator.submit(_request(expected_row_version=1), "fm01")
    assert error.value.code == "STALE_VERSION"


def test_coordinator_preserves_parent_lifecycle_failure_and_does_not_store():
    class Entity:
        def read_row_version(self, resource, entity_id):
            return 1

        def validate_parent_and_lifecycle(self, request):
            raise FM01ContractError("PARENT_NOT_VALID", "parent or lifecycle is not valid", 409)

        def apply_business_effect(self, request):
            raise AssertionError("business effect must not run")

    store = FM01InMemoryIdempotencyStore()
    coordinator = FM01MutationCoordinator(store, Entity())
    with pytest.raises(FM01ContractError) as error:
        coordinator.submit(_request(), "fm01")
    assert error.value.code == "PARENT_NOT_VALID"
    assert store.get("fm01", "idem-1") is None
