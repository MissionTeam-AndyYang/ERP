"""FM-01 local mutation contract boundaries.

This module deliberately contains orchestration interfaces and deterministic
validation only. It does not create tables, call a database, grant authority,
or apply a lifecycle change. Missing persistence, approval, evidence, or
runtime bindings fail closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Callable, Mapping, Protocol


class FM01ContractError(Exception):
    """Safe, structured contract failure without internal implementation data."""

    def __init__(self, code: str, message: str, status: int = 409):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status


@dataclass(frozen=True)
class IdempotencyReplay:
    """Durable replay result returned when key and fingerprint agree."""

    request: Mapping[str, Any]


class FM01IdempotencyStore(Protocol):
    """Storage contract for one atomic idempotency namespace."""

    def get(self, scope: str, key: str) -> Mapping[str, Any] | None: ...

    def put(self, scope: str, key: str, fingerprint: str, request: Mapping[str, Any]) -> Mapping[str, Any]: ...


class FM01EntityStateAdapter(Protocol):
    """Entity-specific CAS/lifecycle/parent checks supplied by the runtime."""

    def read_row_version(self, resource: str, entity_id: int) -> int | None: ...

    def validate_parent_and_lifecycle(self, request: "MutationRequest") -> None: ...

    def apply_business_effect(self, request: "MutationRequest") -> Mapping[str, Any]: ...


@dataclass(frozen=True)
class MutationActor:
    actor_id: str
    role: str


@dataclass(frozen=True)
class MutationRequest:
    resource: str
    entity_id: int
    operation: str
    payload: Mapping[str, Any]
    expected_row_version: int | None
    idempotency_key: str | None
    correlation_id: str | None
    actor: MutationActor | None
    approver_id: str | None = None
    evidence_ref: str | None = None


class PendingApprovalStore(Protocol):
    """Application-core adapter; no default persistence is supplied."""

    def submit(self, request: MutationRequest, fingerprint: str) -> Mapping[str, Any]: ...

    def replay(self, idempotency_key: str, fingerprint: str) -> Mapping[str, Any] | None: ...


class AuditEvidenceStore(Protocol):
    """Atomic audit/evidence adapter supplied only by an approved core binding."""

    def append(self, request: MutationRequest, before: Mapping[str, Any], after: Mapping[str, Any]) -> None: ...


class MutationPersistence(Protocol):
    """Optional FM01-local persistence adapter with explicit atomic semantics."""

    def submit_pending_with_audit(self, request: MutationRequest, fingerprint: str) -> Mapping[str, Any]: ...

    def replay_or_conflict(self, idempotency_key: str, fingerprint: str) -> Mapping[str, Any] | None: ...


class ApprovalRequestPersistence(Protocol):
    """Adapter for the approved FM01-local approval request table."""

    def find_idempotent(self, scope: str, key: str, fingerprint: str) -> Mapping[str, Any] | None: ...

    def create_pending(self, request: MutationRequest, fingerprint: str) -> Mapping[str, Any]: ...

    def decide(self, request_id: int, requester_id: str, approver_id: str, approved: bool, note: str | None) -> Mapping[str, Any]: ...


class FM01Session(Protocol):
    """Minimal session surface; concrete SQL/session ownership stays external."""

    def begin(self) -> Any: ...

    def add(self, value: Mapping[str, Any]) -> None: ...

    def flush(self) -> None: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...


class FM01ApprovalAuditAdapter:
    """Mapping adapter for the approved 0004 tables.

    It emits table-shaped records and delegates transaction execution to the
    injected session. The injected session factory owns the transaction boundary:
    the adapter calls commit only after all request/audit writes succeed and calls
    rollback on every failure. It does not open connections, execute SQL, or
    select runtime retention/authorization policy.
    """

    def __init__(self, session_factory: Callable[[], FM01Session]):
        self._session_factory = session_factory

    def create_pending(self, request: MutationRequest, fingerprint: str) -> Mapping[str, Any]:
        session = self._session_factory()
        try:
            request_row = self._pending_row(request, fingerprint)
            session.add(request_row)
            session.flush()
            session.add(self._audit_row(request, request_row, "REQUEST_SUBMITTED"))
            session.commit()
            return request_row
        except Exception as exc:
            session.rollback()
            raise FM01ContractError("PERSISTENCE_FAILED", "approval request was not persisted", 503) from exc

    def decide(self, request_id: int, requester_id: str, approver_id: str, approved: bool, note: str | None):
        if not approver_id or requester_id == approver_id:
            raise FM01ContractError("SELF_APPROVAL_FORBIDDEN", "requester cannot approve own request", 403)
        session = self._session_factory()
        try:
            decision = {
                "approval_request_id": request_id,
                "approver_id": approver_id,
                "approval_state": "APPROVED" if approved else "REJECTED",
                "decision_note": note,
            }
            session.add(decision)
            session.add({
                "approval_request_id": request_id,
                "event_type": "APPROVED" if approved else "REJECTED",
                "actor_id": approver_id,
            })
            session.commit()
            return decision
        except Exception as exc:
            session.rollback()
            raise FM01ContractError("PERSISTENCE_FAILED", "approval decision was not persisted", 503) from exc

    def find_idempotent(self, scope: str, key: str, fingerprint: str):
        raise FM01ContractError("PERSISTENCE_NOT_BOUND", "idempotency lookup adapter is not bound", 503)

    def _pending_row(self, request: MutationRequest, fingerprint: str) -> dict[str, Any]:
        return {
            "resource_type": request.resource,
            "entity_id": request.entity_id,
            "operation": request.operation,
            "requester_id": request.actor.actor_id if request.actor else "",
            "requester_role": request.actor.role if request.actor else None,
            "approval_state": "PENDING_APPROVAL",
            "row_version": request.expected_row_version,
            "payload_json": dict(request.payload),
            "idempotency_key": request.idempotency_key,
            "request_fingerprint": fingerprint,
            "correlation_id": request.correlation_id,
            "evidence_ref": request.evidence_ref,
        }

    def _audit_row(self, request: MutationRequest, request_row: Mapping[str, Any], event_type: str):
        return {
            "approval_request_id": request_row.get("approval_request_id"),
            "event_type": event_type,
            "actor_id": request.actor.actor_id if request.actor else "",
            "actor_role": request.actor.role if request.actor else None,
            "correlation_id": request.correlation_id,
            "evidence_ref": request.evidence_ref,
        }


class FM01ApprovalService:
    """Pending approval service; storage and final business effect stay injected."""

    def __init__(self, persistence: ApprovalRequestPersistence):
        self._persistence = persistence

    def submit(self, request: MutationRequest, scope: str) -> Mapping[str, Any]:
        if not scope:
            raise FM01ContractError("IDEMPOTENCY_SCOPE_REQUIRED", "idempotency scope is required", 400)
        fingerprint = FM01MutationGateway.fingerprint(request)
        existing = self._persistence.find_idempotent(scope, request.idempotency_key or "", fingerprint)
        if existing is not None:
            return existing
        return self._persistence.create_pending(request, fingerprint)

    def decide(self, request_id: int, requester_id: str, approver_id: str, approved: bool, note: str | None = None):
        if not approver_id or approver_id == requester_id:
            raise FM01ContractError("SELF_APPROVAL_FORBIDDEN", "requester cannot approve own request", 403)
        if not note or not note.strip():
            raise FM01ContractError("DECISION_NOTE_REQUIRED", "approval decision note is required", 400)
        return self._persistence.decide(request_id, approver_id, approved, note.strip())


class FM01MutationGateway:
    """Fail-closed FM-01-local mutation orchestration boundary.

    The gateway exposes contract decisions without choosing storage semantics or
    creating a shared authority. A concrete adapter must be injected before a
    mutation can be accepted.
    """

    _resources = {
        "legal-entities": ("legal_entity_id", "legal_entity_ref"),
        "companies": ("company_id", "company_ref"),
        "sites": ("site_id", "site_ref"),
        "plants": ("plant_id", "plant_ref"),
        "warehouses": ("warehouse_id", "warehouse_ref"),
        "locations": ("location_id", "location_ref"),
    }
    _allowlisted_update_fields = {"display_name"}

    def __init__(
        self,
        pending_store: PendingApprovalStore | None = None,
        audit_store: AuditEvidenceStore | None = None,
        runtime_authorizer: Callable[[MutationRequest], bool] | None = None,
        persistence: MutationPersistence | None = None,
    ):
        self._pending_store = pending_store
        self._audit_store = audit_store
        self._runtime_authorizer = runtime_authorizer
        self._persistence = persistence

    def submit_create(self, request: MutationRequest) -> Mapping[str, Any]:
        self._validate_common(request, "create")
        self._require_pending_bindings()
        return self._submit_pending(request)

    def submit_update(self, request: MutationRequest) -> Mapping[str, Any]:
        self._validate_common(request, "update")
        self._validate_update_payload(request.payload)
        self._require_pending_bindings()
        return self._submit_pending(request)

    def submit_lifecycle(self, request: MutationRequest) -> Mapping[str, Any]:
        if request.operation not in {"deactivate", "reactivate"}:
            raise FM01ContractError("INVALID_OPERATION", "unsupported lifecycle operation", 400)
        self._validate_common(request, request.operation)
        self._require_pending_bindings()
        return self._submit_pending(request)

    def _validate_common(self, request: MutationRequest, operation: str) -> None:
        if request.resource not in self._resources:
            raise FM01ContractError("UNSUPPORTED_RESOURCE", "resource is outside the FM-01 allowlist", 422)
        if request.operation != operation:
            raise FM01ContractError("INVALID_OPERATION", "operation does not match endpoint", 400)
        if request.entity_id < 1:
            raise FM01ContractError("INVALID_PARAMETER", "entity_id must be positive", 400)
        if request.expected_row_version is None or request.expected_row_version < 1:
            raise FM01ContractError("STALE_VERSION", "expected_row_version is required", 409)
        if not request.idempotency_key:
            raise FM01ContractError("IDEMPOTENCY_REQUIRED", "idempotency key is required", 409)
        if not request.correlation_id:
            raise FM01ContractError("CORRELATION_REQUIRED", "correlation id is required", 400)
        if request.actor is None or not request.actor.actor_id:
            raise FM01ContractError("AUTHENTICATION_REQUIRED", "authenticated actor is required", 401)
        if request.approver_id and request.approver_id == request.actor.actor_id:
            raise FM01ContractError("SELF_APPROVAL_FORBIDDEN", "requester cannot approve own request", 403)

    def _validate_update_payload(self, payload: Mapping[str, Any]) -> None:
        if not payload:
            raise FM01ContractError("VALIDATION_ERROR", "update payload is required", 400)
        if set(payload) - self._allowlisted_update_fields:
            raise FM01ContractError("IMMUTABLE_FIELD", "only display_name is updateable", 409)
        if not isinstance(payload.get("display_name"), str) or not payload["display_name"].strip():
            raise FM01ContractError("VALIDATION_ERROR", "display_name is required", 400)

    def _require_pending_bindings(self) -> None:
        if not self._pending_store or not self._audit_store or not self._runtime_authorizer or not self._persistence:
            raise FM01ContractError("MUTATION_NOT_BOUND", "FM-01 mutation bindings are unavailable", 503)

    def _submit_pending(self, request: MutationRequest) -> Mapping[str, Any]:
        if not self._runtime_authorizer(request):
            raise FM01ContractError("AUTHORIZATION_DENIED", "mutation authority is unavailable", 403)
        fingerprint = self.fingerprint(request)
        replay = self._persistence.replay_or_conflict(request.idempotency_key or "", fingerprint)
        if replay is not None:
            return replay
        return self._persistence.submit_pending_with_audit(request, fingerprint)

    @staticmethod
    def fingerprint(request: MutationRequest) -> str:
        canonical = {
            "resource": request.resource,
            "entity_id": request.entity_id,
            "operation": request.operation,
            "payload": request.payload,
            "expected_row_version": request.expected_row_version,
        }
        encoded = json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        return sha256(encoded).hexdigest()


class FM01InMemoryIdempotencyStore:
    """Deterministic source-level idempotency store for unit tests only."""

    def __init__(self):
        self._rows: dict[tuple[str, str], tuple[str, Mapping[str, Any]]] = {}

    def get(self, scope: str, key: str) -> Mapping[str, Any] | None:
        row = self._rows.get((scope, key))
        return None if row is None else row[1]

    def put(self, scope: str, key: str, fingerprint: str, request: Mapping[str, Any]) -> Mapping[str, Any]:
        existing = self._rows.get((scope, key))
        if existing is not None:
            if existing[0] != fingerprint:
                raise FM01ContractError("IDEMPOTENCY_CONFLICT", "idempotency request conflicts", 409)
            return existing[1]
        self._rows[(scope, key)] = (fingerprint, dict(request))
        return self._rows[(scope, key)][1]


class FM01MutationCoordinator:
    """Source-level orchestration for CAS, replay and approved business effect.

    Concrete SQLAlchemy/session work and runtime authority remain injected. The
    coordinator never treats an absent binding as success.
    """

    def __init__(
        self,
        idempotency_store: FM01IdempotencyStore,
        entity_adapter: FM01EntityStateAdapter,
    ):
        self._idempotency_store = idempotency_store
        self._entity_adapter = entity_adapter

    def submit(self, request: MutationRequest, scope: str) -> Mapping[str, Any]:
        if not scope or not request.idempotency_key:
            raise FM01ContractError("IDEMPOTENCY_REQUIRED", "idempotency scope and key are required", 409)
        fingerprint = FM01MutationGateway.fingerprint(request)
        existing = self._idempotency_store.get(scope, request.idempotency_key)
        if existing is not None:
            existing_fingerprint = existing.get("request_fingerprint")
            if existing_fingerprint != fingerprint:
                raise FM01ContractError("IDEMPOTENCY_CONFLICT", "idempotency request conflicts", 409)
            return {"replayed": True, "request": existing}
        if request.expected_row_version is None or request.expected_row_version < 1:
            raise FM01ContractError("STALE_VERSION", "expected_row_version is required", 409)
        current_version = self._entity_adapter.read_row_version(request.resource, request.entity_id)
        if current_version is None:
            raise FM01ContractError("NOT_FOUND", "entity was not found", 404)
        if current_version != request.expected_row_version:
            raise FM01ContractError("STALE_VERSION", "entity row_version is stale", 409)
        self._entity_adapter.validate_parent_and_lifecycle(request)
        result = self._entity_adapter.apply_business_effect(request)
        stored = self._idempotency_store.put(
            scope,
            request.idempotency_key,
            fingerprint,
            {"request_fingerprint": fingerprint, "result": result},
        )
        return {"replayed": False, "request": stored, "result": result}
