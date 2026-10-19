# FM-01 Independent Test Cases

**Revision:** `ERP2.0-FM01-TEST-CASES-20261019-002`  
**Execution contract:** See `Execution-Contract-Matrix.md`; one mapping exists for each of the 53 Case IDs below.

**Status:** PREPARED FOR FUTURE AUTHORIZED EXECUTION / NO EXECUTION CLAIMED  
**Scope:** `legal_entity`, `company`, `site`, `plant`, `warehouse`, `location`

## GET-only regression

| ID | Case | Classification | Expected |
|---|---|---|---|
| FM01-GET-01 | Six-resource allowlist collection reads | CONTRACT / DB_DEPENDENT | Only six approved resources are served; deterministic pagination and envelope preserved. |
| FM01-GET-02 | ID and reference lookup | CONTRACT / DB_DEPENDENT | Stable ID/ref lookup returns correct row or safe 404. |
| FM01-GET-03 | Hierarchy traversal | CONTRACT / DB_DEPENDENT | Legal entity to location hierarchy is consistent and parent links are reported, not repaired. |
| FM01-GET-04 | Pagination lower/default/maximum bounds | UNIT / CONTRACT | Default 50, maximum 100; invalid bounds fail safely. |
| FM01-GET-05 | Invalid resource/filter/parameter | CONTRACT / MOCK | 422/400 envelope with no SQL, credential or stack-trace disclosure. |
| FM01-GET-06 | Missing row and inconsistent relationship | CONTRACT / DB_DEPENDENT | 404 or 409 according to contract; no mutation or repair. |
| FM01-GET-07 | Write-method denial on GET-only baseline | CONTRACT / DB_DEPENDENT | POST/PUT/PATCH/DELETE remains denied until separately admitted. |
| FM01-GET-08 | DDL and privilege negative control | STATIC / DB_DEPENDENT | DDL and write privileges are absent or denied; no schema change. |
| FM01-GET-09 | Sensitive-field exclusion | CONTRACT / DB_DEPENDENT | Only approved public fields returned; provenance/audit internals stay bounded. |
| FM01-GET-10 | Restart/readback and zero mutation | NON_DB / DB_DEPENDENT | Read behavior survives restart; row and schema counts remain unchanged. |

## Create

| ID | Case | Classification | Expected |
|---|---|---|---|
| FM01-CRE-01 | Create root legal entity with valid identity | UNIT / MOCK / DB_DEPENDENT | One atomic row plus audit/idempotency result; immutable reference established. |
| FM01-CRE-02 | Create child with eligible active parent | UNIT / CONTRACT / DB_DEPENDENT | Child accepted only under correct parent and scope. |
| FM01-CRE-03 | Duplicate global/scoped reference | UNIT / DB_DEPENDENT | Rejected as duplicate; no second business effect. |
| FM01-CRE-04 | Missing parent or inactive parent | UNIT / DB_DEPENDENT | Fail closed with parent-not-found/ineligible result; no row. |
| FM01-CRE-05 | Warehouse plant/site inconsistency | UNIT / DB_DEPENDENT | Rejected; no partial warehouse or plant association. |
| FM01-CRE-06 | Location wrong-warehouse parent | UNIT / DB_DEPENDENT | Rejected; parent remains warehouse-local. |
| FM01-CRE-07 | Missing actor, assignment, correlation or idempotency | CONTRACT / MOCK | Rejected before business write. |
| FM01-CRE-08 | Create same key/same intent replay | UNIT / DB_DEPENDENT | Preserved original result returned; no duplicate row/audit effect. |
| FM01-CRE-09 | Create same key/changed intent | UNIT / DB_DEPENDENT | Idempotency conflict and safe stop; no second effect. |

## Controlled update

| ID | Case | Classification | Expected |
|---|---|---|---|
| FM01-UPD-01 | Allowlisted display/provenance field update | CONTRACT / DB_DEPENDENT | Before/after audit, actor, reason and version are persisted atomically. |
| FM01-UPD-02 | Immutable ref, surrogate ID or parent update | UNIT / DB_DEPENDENT | Rejected; hierarchy and identity unchanged. |
| FM01-UPD-03 | Missing or stale expected row version | UNIT / DB_DEPENDENT | Stale-version rejection; no update/audit mutation. |
| FM01-UPD-04 | Update approval/role separation | MOCK / DB_DEPENDENT | Maintainer cannot self-approve an approval-controlled operation. |
| FM01-UPD-05 | Update failure after validation | DB_DEPENDENT | Entire transaction rolls back, including audit/idempotency side effects. |

## Lifecycle

| ID | Case | Classification | Expected |
|---|---|---|---|
| FM01-LCY-01 | Deactivate eligible record | CONTRACT / DB_DEPENDENT | State transition preserves history and blocks new dependent creation. |
| FM01-LCY-02 | Deactivate with active dependents/downstream conflict | DB_DEPENDENT | Controlled rejection with no partial state change. |
| FM01-LCY-03 | Reactivate with valid parent/effectivity/successor | DB_DEPENDENT | Explicit revalidation required; successful transition fully audited. |
| FM01-LCY-04 | Reactivate with invalid parent/effectivity/authority | DB_DEPENDENT | Rejected; not an automatic inverse. |
| FM01-LCY-05 | Unknown or unsupported transition | UNIT / CONTRACT | Invalid-transition rejection; no write. |

## Identity, authorization, approval and audit

| ID | Case | Classification | Expected |
|---|---|---|---|
| FM01-AUD-01 | Reader attempts mutation | MOCK / DB_DEPENDENT | Authorization denied; no business or audit success record. |
| FM01-AUD-02 | Maintainer submits approval-controlled change | MOCK / DB_DEPENDENT | Pending/approval state only; no unauthorized final mutation. |
| FM01-AUD-03 | Same actor submits and approves | MOCK / DB_DEPENDENT | Separation-of-duty rejection. |
| FM01-AUD-04 | Technical operator presented as business approver | MOCK | Rejected; technical execution does not imply business approval. |
| FM01-AUD-05 | Accepted mutation audit readback | DB_DEPENDENT | Actor, assignment, operation, reason, evidence, before/after, correlation, idempotency and timestamp are retrievable within approved boundary. |
| FM01-AUD-06 | Rejected authorization-reaching request audit | DB_DEPENDENT | Rejection is attributable without exposing secrets or SQL. |

## Negative integrity, concurrency and security

| ID | Case | Classification | Expected |
|---|---|---|---|
| FM01-NEG-01 | Invalid FK/parent reference | UNIT / DB_DEPENDENT | Rejected with no orphan. |
| FM01-NEG-02 | Location self-parent or descendant cycle | UNIT / DB_DEPENDENT | Cycle rejected; no hierarchy corruption. |
| FM01-NEG-03 | Concurrent same-reference creates | DB_DEPENDENT | Exactly one winner; loser receives duplicate/conflict; no partial audit. |
| FM01-NEG-04 | Concurrent stale updates | DB_DEPENDENT | One version winner; stale writer rejected. |
| FM01-NEG-05 | Concurrent lifecycle transition | DB_DEPENDENT | Atomic transition prevents double effect. |
| FM01-NEG-06 | Replay after timeout/restart | DB_DEPENDENT | Same intent replays preserved result; changed intent halts. |
| FM01-NEG-07 | SQL/credential/stack-trace injection probe | STATIC / CONTRACT / MOCK | Inputs are parameterized/allowlisted; safe error only. |
| FM01-NEG-08 | Unauthorized cross-entity or cross-scope access | CONTRACT / DB_DEPENDENT | Denied without existence leakage beyond approved error contract. |

## UI component and interaction design cases

| ID | Case | Classification | Expected |
|---|---|---|---|
| FM01-UI-01 | Hierarchy/list/detail navigation | CONTRACT / E2E | Six-entity hierarchy is scannable, keyboard reachable and consistent with ERP2.0 shell. |
| FM01-UI-02 | Full-page Create flow | MOCK / E2E | Complex creation uses a full page; required fields, parent selection, duplicate and error states fail closed. |
| FM01-UI-03 | Right-side drawer simple Edit | MOCK / E2E | Simple allowlisted edits use a right-side drawer; immutable fields are protected and stale-version response preserves context. |
| FM01-UI-04 | Escalation to full-page complex operation | MOCK / E2E | Complex update/reparent/lifecycle operation leaves the drawer and opens a full-page flow with explicit review and confirmation. |
| FM01-UI-05 | Deactivate/reactivate confirmation | MOCK / E2E | Explicit transition, approval status and audit link are shown; no automatic inverse. |
| FM01-UI-06 | Unauthorized visibility and rejection | CONTRACT / E2E | Unauthorized actions are visible only according to policy and are rejected server-side; no mutation occurs. |
| FM01-UI-07 | Loading/empty/validation/failure states | CONTRACT / E2E | No ambiguous success; safe error envelope, validation feedback and retry boundary are shown. |
| FM01-UI-08 | Responsive/accessibility interaction | STATIC / E2E | Keyboard path, labels, focus, contrast, responsive layout and error association meet accepted style baseline. |
| FM01-UI-09 | Traditional Chinese / translation-ready structure | STATIC / MOCK / E2E | User-facing strings use Traditional Chinese and translation-ready keys/resources; no hard-coded mixed-language labels. |
| FM01-UI-10 | Audit/approval readback | MOCK / E2E | Safe provenance summary shown without credentials, SQL or unapproved internal fields. |

