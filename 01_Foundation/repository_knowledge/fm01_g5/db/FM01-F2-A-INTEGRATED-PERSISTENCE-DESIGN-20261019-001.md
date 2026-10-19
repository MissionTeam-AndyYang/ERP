# FM-01 F2-A Integrated Local Persistence Design

Assignment: `CTO-FM01-F2-A-20261019-001`
Baseline: `65b87fc2ef36aa9c05e0900d639dad4f7fcc5f6f`
Design scope: FM01-local persistence only

## Design decision

The accepted FM-01 source has no local storage binding for pending approval,
idempotency, replay/conflict, or audit/evidence. The minimum additive design is
two FM01-local tables introduced after migration `fm01_org_location_0003_mutation_contract`:

1. `fm01_approval_request` is the durable request control record.
2. `fm01_audit_event` is the append-only audit/evidence record for request transitions.

No shared Workflow, IAM, Audit, retention, or production infrastructure is
created or activated by this design.

## Approval request record

`fm01_approval_request` stores:

- request identity: generated `approval_request_id`, `request_ref`, `correlation_id`, `transaction_id`;
- target: `resource_type`, `entity_id`, `operation`;
- actors: `requester_id`, optional `approver_id`, and role snapshots;
- state: `approval_state`, decision code/note, requested/decided timestamps;
- concurrency: non-null `row_version` with default 1;
- effectivity: `effective_from`, optional `effective_to`;
- payload and evidence: request payload JSON, `evidence_ref`, `audit_event_id`;
- replay control: `idempotency_scope`, `idempotency_key`, canonical fingerprint, replay/conflict result fields.

The composite uniqueness rule `(idempotency_scope, idempotency_key)` makes the
idempotency namespace explicit. The fingerprint is a canonical SHA-256 value
produced by the existing FM01 contract. A replay returns the existing request
when the key and fingerprint agree; a conflicting fingerprint is a fail-closed
runtime decision. The migration stores the facts but does not implement the
runtime decision.

## Audit and evidence record

`fm01_audit_event` stores an immutable event identity, request reference, event
type, actor identity/role, transaction and correlation identity, before/after
JSON snapshots, evidence reference, event timestamp, and an optional rollback
event reference. A foreign key ties each event to its approval request.

The runtime persistence adapter must insert the request transition and its audit
event in one database transaction, rolling back both on failure. The schema
provides the transaction identity and referential boundary; it does not activate
transaction management, IAM, read permissions, or retention policy.

## Lifecycle, parent integrity, and GET compatibility

The existing `0002` lifecycle/effectivity fields and parent foreign keys remain
unchanged. `0003` row-version columns remain unchanged. The new tables use a
polymorphic `resource_type` plus `entity_id` rather than introducing cross-table
foreign keys, so the six existing entities and GET-only API remain compatible.
Lifecycle overlap, successor rules, authorization, and restricted readback are
runtime policy bindings, not silently invented schema semantics.

## Classification and residual conditions

`PENDING_APPROVAL_STORAGE=APPROVED_SOURCE_IMPLEMENTATION`

`IDEMPOTENCY_REPLAY_CONFLICT_STORAGE=APPROVED_SOURCE_IMPLEMENTATION`

`AUDIT_EVIDENCE_STORAGE=APPROVED_SOURCE_IMPLEMENTATION`

`TRANSACTION_ATOMICITY=RUNTIME_BINDING_ONLY`

`IAM_ACTOR_AUTHORITY=RUNTIME_BINDING_ONLY`

`RETENTION_AND_RESTRICTED_READBACK=RUNTIME_BINDING_ONLY`

The migration is a bounded local source amendment. It is not production
database readiness, runtime activation, migration qualification, or business
authority approval.
