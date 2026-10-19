# FM-01 Conditional Maintenance API Contract

Status: DESIGN INPUT ONLY / CONDITIONAL / NOT IMPLEMENTATION AUTHORIZATION

Return target: CTO Office V2  
Scope: `legal_entity`, `company`, `site`, `plant`, `warehouse`, `location` only

This document is a bounded API design review. It does not approve a write API,
change the existing GET-only implementation, alter the database, or establish a
business source of truth. Any item marked `POLICY` remains subject to CIO / Product
Owner confirmation.

## 1. Verified Baseline

| Evidence | Result |
|---|---|
| Source/API implementation commit | `f6e1b57e2bacee4b508bb847e62c8b7db7dd4f5a` |
| Recorded API HEAD candidate | `672734f635fd38ad8ded025cd6a5de1871e7ae12` |
| Existing routes | `GET /api/v1/fm01/<resource>`, lookup by `id` or `ref`, and `GET /api/v1/fm01/hierarchy` |
| Current write behavior | Write methods return HTTP 405; no mutation route is implemented |
| Current repository boundary | Allowlisted read columns; parameter-free SELECT; no mutation |
| Current standards | Foundation V1.2, Cross-Module Delivery Standard v1, and PM Lifecycle/Reporting Standard v1 are treated as effective |
| Migration reference | `NOT VERIFIED` in this review; no migration claim is made |

The current public GET representation is retained: `data` contains public rows and
`meta` contains resource, offset, limit, count, and total. Existing errors use the
`error.code` / `error.message` envelope.

## 2. Entity and Uniqueness Matrix

| Entity | Existing parent relationship | Existing reference uniqueness in verified fixture | Maintenance impact |
|---|---|---|---|
| `legal_entity` | none | `legal_entity_ref` | Reference is immutable by default |
| `company` | `legal_entity_id` | `(legal_entity_id, company_ref)` | Parent is required and must exist |
| `site` | `company_id` | `(company_id, site_ref)` | Parent is required and must exist |
| `plant` | `site_id` | `(site_id, plant_ref)` | Parent is required and must exist |
| `warehouse` | `site_id`, optional `plant_id` | `(site_id, warehouse_ref)` | Exact site/plant consistency rule is `POLICY` |
| `location` | `warehouse_id`, optional `parent_location_id` | `(warehouse_id, location_ref)` | Parent-cycle and reparenting rules are `POLICY` |

The unique constraints above are schema-fixture observations, not permission to
change schema or to infer operational ownership rules.

## 3. Route Contract Matrix

| Operation | Route | Current status | Conditional design |
|---|---|---|---|
| List / lookup | `GET /api/v1/fm01/<resource>` | IMPLEMENTED | Preserve. Supports `id`, `ref`, `limit`, `offset`; do not change envelope. |
| Detail | `GET /api/v1/fm01/<resource>/{id}` | NOT PRESENT in verified source | Optional compatibility alias only; requires API-owner approval. Existing lookup remains the contract. |
| Hierarchy | `GET /api/v1/fm01/hierarchy` | IMPLEMENTED | Preserve and keep read-only. |
| Basic create | `POST /api/v1/fm01/<resource>` | NOT IMPLEMENTED | Conditional design below; no implementation authorization. |
| Controlled update | `PATCH /api/v1/fm01/<resource>/{id}` | NOT IMPLEMENTED | Conditional design below; partial update is a design choice pending approval. |
| Deactivate | `POST /api/v1/fm01/<resource>/{id}/deactivate` | NOT IMPLEMENTED | Conditional design below. |
| Reactivate | `POST /api/v1/fm01/<resource>/{id}/reactivate` | NOT IMPLEMENTED | Conditional design below. |

No hard-delete route is proposed. Cross-module references must not be silently
recoded, deleted, or reused.

### Endpoint control record

Each endpoint below has an explicit policy dependency, state effect, transaction
boundary, fail-closed rule, and test-case placeholder. `TBD` means the design is
intentionally not approved for implementation.

| Endpoint | Policy dependency | Allowed state effect | Transaction boundary | Fail-closed rule | Test Case placeholder |
|---|---|---|---|---|---|
| Existing GET list/lookup | None for read representation; authorization boundary remains external | None | One read-only repository operation | Unsupported resource, invalid parameters, repository failure, or incomplete hierarchy data returns an error; never partial mutation | `FM01-GET-LIST-001` through `FM01-GET-LIST-006`, invalid parameter, not-found, 405 regression |
| Existing GET hierarchy | Hierarchy completeness policy only if partial parents are allowed | None | One read-only snapshot boundary | Any required collection failure returns an error; do not return a deceptively complete hierarchy | `FM01-GET-HIERARCHY-001`, empty collection, repository failure |
| Optional GET detail alias | API-owner decision on route compatibility | None | One read-only lookup | Alias must delegate to the same lookup rules; if identity is ambiguous, return `NOT_FOUND`/conflict rather than guess | `FM01-GET-DETAIL-001` (deferred until approved) |
| POST create | Initial state/DRAFT policy, approval policy, ref scope, idempotency retention | None to one new record in approved initial state | One transaction: validate, lock uniqueness scope, write record and audit/outbox atomically | Missing policy binding, parent uncertainty, audit failure, or idempotency-store failure aborts the whole operation | `FM01-CREATE-001` through `FM01-CREATE-006` |
| PATCH update | Editable-field, revision, parent-change and version persistence policy | Same record revision or approved new revision | One transaction: lock/version-check, validate, write, audit atomically | Missing version, stale version, audit failure, or downstream-check uncertainty aborts with no write | `FM01-UPDATE-001` through `FM01-UPDATE-007` |
| POST deactivate | Transition matrix, downstream-use exception, approval/evidence policy | Active to approved inactive/blocked state | One transaction: lock, recheck references, transition, audit atomically | Unknown state, missing approval/evidence, downstream uncertainty, or audit failure leaves state unchanged | `FM01-DEACTIVATE-001` through `FM01-DEACTIVATE-005` |
| POST reactivate | Reactivation review, approver, evidence and state policy | Inactive/blocked to approved active state | One transaction: lock, validate review, transition, audit atomically | Any review, evidence, authorization, or audit uncertainty rejects without state change | `FM01-REACTIVATE-001` through `FM01-REACTIVATE-005` |

## 4. Common Request Metadata

The following is a conditional contract for mutation requests:

| Header / field | Requirement | Classification |
|---|---|---|
| `Idempotency-Key` | Required for create and lifecycle actions; same key plus same canonical request replays the original result; same key plus different request returns conflict | CTO-approved implementation pattern; key format and retention are `POLICY` |
| `X-Correlation-ID` | Accepted and returned for traceability | CTO-approved implementation pattern; propagation and retention are `POLICY` |
| `expected_row_version` | Required for update and lifecycle actions to prevent stale writes | CTO-approved concurrency pattern; persistence column/migration is `POLICY` / `NOT VERIFIED` |
| actor identity | Derived from authenticated request context, never trusted from a free-form body field | CTO-approved boundary |
| approver/evidence | Required where the final policy classifies the action as approval-controlled | Required boundary; role appointment and evidence format are `POLICY` |

## 5. Basic Create

### Request

`POST /api/v1/fm01/<resource>`

The body is resource-specific and uses the existing schema names:

```json
{
  "<resource>_ref": "CLIENT-DEFINED-REFERENCE",
  "display_name": "Display name",
  "parent_id": 123,
  "effective_from": "2026-01-01T00:00:00Z",
  "effective_to": null,
  "source_reference": "external-record-reference",
  "provenance_note": "reason and provenance"
}
```

`parent_id` is a placeholder for the applicable relation key: for example,
`legal_entity_id`, `company_id`, `site_id`, `plant_id`, or `warehouse_id`.
`warehouse` may also carry `plant_id`; the consistency rule is unresolved.

Client input must not supply primary keys, audit timestamps, actor assignment IDs,
correlation IDs, status flags, or a server version value.

### Server-generated and response fields

The server would generate the primary key, created/updated timestamps, actor
provenance, correlation ID, initial lifecycle state, and version token. The response
would use the existing public representation in `data` and return mutation metadata:

```json
{
  "data": {
    "<resource>_id": 123,
    "<resource>_ref": "CLIENT-DEFINED-REFERENCE",
    "display_name": "Display name",
    "active_flag": false,
    "effective_from": "2026-01-01T00:00:00Z",
    "effective_to": null
  },
  "meta": {
    "correlation_id": "corr-123",
    "idempotent_replay": false,
    "row_version": 1
  }
}
```

Create should produce `DRAFT` only if Product Owner confirms that lifecycle policy.
The current fixture default `active_flag = 1` is not sufficient to establish a
create policy; the state model and persistence representation require confirmation.

Duplicate handling: a uniqueness conflict returns HTTP 409 with
`DUPLICATE_REFERENCE`; it must not return the existing record as if creation
succeeded. A repeated idempotent request may return the original result only when
the canonical request fingerprint matches.

Create transaction and test obligations:

- Validate required fields and parent references before opening the write boundary.
- Within one transaction, re-check the uniqueness scope under the database's
  isolation/locking rules, persist the record, persist audit provenance, and persist
  the idempotency result.
- If any one of those operations fails, roll back all writes and return a generic
  fail-closed error; never report success without audit provenance.
- Test cases: valid create, missing required field, invalid parent, duplicate
  reference, repeated same-key replay, same-key different-payload conflict, audit
  failure rollback, unauthorized actor, and initial-state policy rejection.

## 6. Controlled Update / Save

`PATCH /api/v1/fm01/<resource>/{id}`

Editable candidates are `display_name`, approved parent relationship fields, and
effective dates. The reference code is immutable by default because FM-02 and other
modules consume these references. Any reference correction needs an explicit policy
and a controlled alias/migration design; no silent recoding is allowed.

The request includes `expected_row_version`. If the stored version differs, return
HTTP 409 `STALE_VERSION` and make no change. Successful updates increment the version
and record actor, correlation, reason, before/after values, timestamp, and supporting
provenance.

Update transaction and test obligations:

- Accept only an allowlisted patch field set; reject unknown or immutable reference
  fields before mutation.
- Lock or atomically compare the target row and `expected_row_version`; do not use a
  preliminary read as the concurrency guarantee.
- Revalidate parent, uniqueness, effective period, and downstream-reference rules in
  the same transaction that writes the update and audit record.
- If the version check, validation, audit write, or idempotency write fails, roll back
  and return `STALE_VERSION`, a validation error, or a generic fail-closed error as
  appropriate.
- Test cases: editable display name, immutable ref rejection, stale version, missing
  version, duplicate after parent change, overlapping effective period, downstream
  reference block, audit rollback, and concurrent same-row update.

Revision behavior for effective dates and specification-like historical records is
not inferred from the current FM-01 GET-only source. Whether a save creates a new
revision, closes the prior effective period, or edits a draft in place is a `POLICY`
decision.

## 7. Lifecycle Actions

The following are conditional action contracts. Each request carries a reason,
`expected_row_version`, idempotency key, and correlation context. Approval and
evidence are mandatory when the action policy requires them.

| Action | Proposed transition | Required guard |
|---|---|---|
| Activate | Draft/inactive to active | authorized actor; approval/evidence if policy requires |
| Deactivate | active to inactive | no blocking downstream reference, or explicit approved exception |
| Reactivate | inactive/blocked to active | authorized review, approver, reason, timestamp, and evidence |
| Block | active/inactive to blocked | authorized actor, reason, approver/evidence |
| Supersede | current record to superseded with successor reference | successor traceability and approval |
| Retire | terminal retirement | approval, evidence, and downstream impact review |

The verified FM-01 source exposes `active_flag`, but it does not implement these
transitions. The exact state values, transition matrix, successor field, and whether
all six entities support every action remain `POLICY` items.

Lifecycle transaction and test obligations:

- Lock the target state, verify the transition and approval evidence, re-check
  downstream references where required, write the new state and audit record, and
  commit them together.
- Idempotent retries with the same key and request fingerprint may replay the original
  result; a different fingerprint must fail with `IDEMPOTENCY_CONFLICT`.
- Any unknown state, missing authorization, missing evidence, downstream uncertainty,
  audit failure, or idempotency-store failure must leave the state unchanged.
- Test cases: every approved transition, invalid transition, missing reason, missing
  approver, missing evidence, downstream block, stale version, same-key replay,
  conflicting key, and rollback on audit failure.

## 8. Validation and Error Contract

The mutation contract should preserve the existing error envelope:

```json
{
  "error": {
    "code": "STALE_VERSION",
    "message": "The record was changed by another request.",
    "details": {
      "correlation_id": "corr-123"
    }
  }
}
```

| Condition | HTTP | Code |
|---|---:|---|
| malformed JSON, missing required field, invalid type or date | 400 | `INVALID_PARAMETER` / `VALIDATION_ERROR` |
| no authenticated identity | 401 | `AUTHENTICATION_REQUIRED` |
| authenticated actor lacks permission | 403 | `AUTHORIZATION_DENIED` |
| approval or evidence is required but absent | 403 | `APPROVAL_REQUIRED` / `EVIDENCE_REQUIRED` |
| resource or parent does not exist | 404 | `NOT_FOUND` / `PARENT_NOT_FOUND` |
| duplicate reference in its uniqueness scope | 409 | `DUPLICATE_REFERENCE` |
| stale version | 409 | `STALE_VERSION` |
| same idempotency key with different request | 409 | `IDEMPOTENCY_CONFLICT` |
| illegal lifecycle transition | 409 | `INVALID_STATE_TRANSITION` |
| effective periods overlap | 409 | `EFFECTIVE_PERIOD_OVERLAP` |
| downstream reference prevents change | 409 | `DOWNSTREAM_REFERENCE_CONFLICT` |
| unsupported FM-01 resource | 422 | `UNSUPPORTED_RESOURCE` |
| unexpected internal failure | 500 | `INTERNAL_ERROR` |

No error response may expose SQL text, credentials, internal stack traces, or
unapproved business data.

## 9. Audit, Authorization, and Correlation

Every successful mutation and rejected mutation that reaches authorization must be
traceable by correlation ID and request identity. The audit record should capture:

- entity and immutable primary key;
- operation and before/after state;
- actor, approver, and authorization decision;
- reason and supporting evidence reference;
- idempotency key and canonical request fingerprint;
- timestamp, row version, and source reference.

The executor and approver must be separable identities. Exact role names, delegated
authority, appointment records, audit retention period, evidence storage, and
correlation propagation across services remain `POLICY` items.

## 10. Classification and Open Policy Items

## 10A. UI-to-API Compatibility Review

Reviewed UI evidence:

- `16_Program_Office/ERP2.0-FM01-OWNER-UI-STYLE-DECISION-REGISTRATION-20261018-018.md`
- `20_Engineering_Workspace/FM01_Organization_Location_Module_Definition_20261008_001/ERP2.0-FM01-Integrated-Design-Spec-Candidate-20261018-001.md`
- `20_Engineering_Workspace/FM01_Organization_Location_Module_Definition_20261008_001/ERP2.0-FM01-Coding-UI-Style-Review-Matrix-20261018-001.md`

The UI decision registers the interaction patterns but explicitly keeps the
integrated design unfrozen and coding unauthorized. This review therefore checks
contract compatibility only; it does not treat the UI decision as mutation approval.

### Interaction mapping

| UI interaction | API compatibility result | Technical closure |
|---|---|---|
| Full-page Create | Compatible with conditional `POST /<resource>` | The form must submit only allowlisted business fields, show server-generated identity after success, preserve correlation, and treat a replay as a replay rather than a second record. DRAFT representation remains `POLICY`. |
| Right-side drawer simple Edit | Compatible with conditional `PATCH /<resource>/{id}` | The drawer must load the current version, send only changed allowlisted fields plus `expected_row_version`, and keep immutable reference fields read-only. |
| Full-page complex workflow | Compatible with lifecycle actions and future approval UI | The page must display pending/approved/rejected state and evidence requirements without assuming that a transition occurred before the API commits it. Exact workflow states remain `POLICY`. |
| Existing GET-only screens | Fully compatible | Existing list/lookup and hierarchy envelopes and 405 write behavior remain unchanged. |

### UI feedback rules

- `400` validation responses map field-level errors only when the server provides a
  safe field key; otherwise the UI shows a general validation message.
- `401` and `403` responses must return the user to an authorization or approval
  state without retrying automatically.
- `409 STALE_VERSION` must prompt a reload/compare flow; the client must not silently
  overwrite the newer server state.
- `409 IDEMPOTENCY_CONFLICT` must stop retry and require a new user action; the UI
  must not generate a new request behind the user's back.
- `409 DUPLICATE_REFERENCE`, `EFFECTIVE_PERIOD_OVERLAP`, and
  `DOWNSTREAM_REFERENCE_CONFLICT` are blocking business messages and must leave the
  form's unsaved values visible for correction or review.
- `500` and dependency failures show a safe generic message with correlation ID;
  internal details are not rendered.

### Authorization, approval, and audit presentation

The UI may display `authorization_required`, `approval_required`, evidence-needed,
or review-pending states only when returned by the API. It must not infer approval
from a successful validation response. On success, the UI should expose the server
correlation ID, resulting row version, and audit/provenance reference if the approved
contract makes those fields public. Evidence upload, appointment, and retention
semantics remain unresolved policy bindings.

### UI retry and concurrency boundaries

- Create and lifecycle actions use the same idempotency key for a retry of the same
  user intent; a timeout does not justify generating a second key immediately.
- A successful idempotent replay should be rendered as the original result, with a
  replay indicator when exposed by the API.
- Update and lifecycle screens must retain the loaded row version and refuse to
  submit without it once concurrency is enabled.
- Refresh/reload is the only automatic recovery for a stale version; conflict
  resolution is user-mediated.

### UI contract test placeholders

- `FM01-UI-CREATE-001`: full-page create success and server identity display.
- `FM01-UI-CREATE-002`: validation and duplicate reference feedback.
- `FM01-UI-EDIT-001`: drawer sends allowlisted patch and version.
- `FM01-UI-EDIT-002`: stale version keeps unsaved changes and requests reload.
- `FM01-UI-LIFECYCLE-001`: approval/evidence-required state is shown without
  assuming transition success.
- `FM01-UI-RETRY-001`: idempotent retry does not create a duplicate.
- `FM01-UI-GET-001`: existing GET-only list/detail/hierarchy behavior remains intact.

### Compatibility result

`ENGINEERING_C_UI_API_COMPATIBILITY=PASS_WITH_POLICY_HOLD`

Technically, the requested UI patterns are compatible with the conditional contract
and do not require changes to the verified GET-only baseline. They cannot be released
as mutation screens until the policy bindings listed below are resolved. Engineering
D's attributable screen artifact was not found in the workspace search, so concrete
component-level assertions remain deferred.

### CTO-approved technical implementation details

- Preserve the existing GET/list/lookup and hierarchy routes and envelopes.
- Keep the six-entity allowlist and existing parent keys.
- Do not hard-delete or silently recode references.
- Use server-derived actor identity and structured errors.
- Use idempotency for create/actions and optimistic concurrency for updates/actions.
- Treat uniqueness, parent existence, stale versions, and effective-period overlap as
  explicit validation outcomes.
- Keep mutation implementation separate from the current read-only repository until
  the contract is approved.
- Treat every mutation as a single atomic business operation; do not expose a success
  response when audit or provenance persistence has failed.
- Keep existing GET behavior as a regression gate before any mutation route is enabled.

### Remaining CIO / Product Owner policy items

1. Whether every create starts as DRAFT and how DRAFT is represented alongside
   `active_flag`.
2. Exact lifecycle states and allowed transitions for each entity, including BLOCKED,
   SUPERSEDED, RETIRED, and reactivation.
3. Approval roles, evidence types, appointment records, and separation-of-duty rules.
4. Whether parent changes are allowed after downstream use; if allowed, whether they
   create revisions and effective periods.
5. Exact warehouse `site_id` / `plant_id` consistency rules and location reparenting
   or cycle rules.
6. Version persistence field and migration ownership; current migration reference is
   not verified.
7. Idempotency-key format, storage duration, replay window, and canonicalization.
8. Correlation-ID propagation and audit retention period.
9. Whether a separate `/{id}` detail route is required; current verified source uses
   query lookup instead.
10. Whether effective-period overlap is rejected for all six entities or only for
    selected revision-bearing records.

## 11. Review Result

`BACKEND_API_DESIGN_REVIEW=HOLD`

Reason: the existing GET-only baseline is verified and the conditional mutation
contract is internally consistent, but implementation cannot be approved until the
policy items above are resolved by the CIO / Product Owner and the migration/version
binding is verified. No source, database, runtime, or Product main changes were made.

Evidence paths inspected:

- `04_Engineering/Application/ERP-2.0/FM01/api.py`
- `04_Engineering/Application/ERP-2.0/FM01/http_service.py`
- `04_Engineering/Application/ERP-2.0/FM01/repository.py`
- `04_Engineering/Application/ERP-2.0/tests/test_fm01_application_composition.py`
- `04_Engineering/Application/ERP-2.0/tests/test_fm01_http_service.py`
- `04_Engineering/Application/ERP-2.0/tests/test_fm01_mariadb_repository.py`
- `04_Engineering/Application/ERP-2.0/tests/test_fm01_organization_location_api.py`
- `stage2_mariadb_fixture_20261011_001/schema_and_fixture.sql`

This artifact is a design input for CTO review, not an authorization to implement.
