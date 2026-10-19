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
    ):
        self._pending_store = pending_store
        self._audit_store = audit_store
        self._runtime_authorizer = runtime_authorizer

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
        if not self._pending_store or not self._audit_store or not self._runtime_authorizer:
            raise FM01ContractError("MUTATION_NOT_BOUND", "FM-01 mutation bindings are unavailable", 503)

    def _submit_pending(self, request: MutationRequest) -> Mapping[str, Any]:
        if not self._runtime_authorizer(request):
            raise FM01ContractError("AUTHORIZATION_DENIED", "mutation authority is unavailable", 403)
        fingerprint = self.fingerprint(request)
        replay = self._pending_store.replay(request.idempotency_key or "", fingerprint)
        if replay is not None:
            return replay
        return self._pending_store.submit(request, fingerprint)

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
