# ERP2.0-M0-A3-T1 Consolidated Technical Standards Package

- Authorization: `ERP2.0-M0-A3-T1`
- Execution date: `2026-10-05`
- Entry: M0-A2 Foundation Architecture complete
- Purpose: freeze-candidate preparation only
- Final status: `ERP2.0-M0-A3-T1 TECHNICAL FOUNDATION STANDARDS = COMPLETE / READY FOR CIO FOUNDATION FREEZE REVIEW`

## 1. Freeze-candidate posture

This package consolidates eight technical standard families into reviewable candidates. `FREEZE-READY` means the rule is sufficiently technical and independent of unresolved Business/Security/Operations truth for CIO freeze review; it is not implementation authorization. Rules dependent on an unresolved owner, legal scope, retention period, data classification, or operating policy remain explicitly labelled.

Preserved principles:

`BUSINESS MEANING BEFORE PHYSICAL SCHEMA`  
`TARGET MODEL BEFORE MIGRATION EXECUTION`  
`ENTERPRISE DATABASE STANDARD BEFORE DOMAIN-SCALE IMPLEMENTATION`  
`DOMAIN PHYSICAL SCHEMA MAY EVOLVE INCREMENTALLY`  
`DURABLE KNOWLEDGE BEFORE HUMAN / AI SCALE-OUT`  
`TECHNICAL STANDARD != IMPLEMENTATION AUTHORIZATION`

No schema, migration, route, Authority, Message Bus, Production, or Functional implementation was executed.

## 2. Proposed standard identities

| ID | Candidate name | State |
|---|---|---|
| `ERP2-STD-DB-001` | Enterprise Database Architecture & Schema Standard | freeze candidate |
| `ERP2-STD-DEV-001` | Development / Integration Architecture Standard | freeze candidate |
| `ERP2-STD-ADR-001` | Architecture Decision Record Standard | freeze candidate |
| `ERP2-STD-MDP-001` | Module Development Pack Standard | freeze candidate |
| `ERP2-STD-CTX-001` | ERP2.0 Engineering Context Manifest Standard | freeze candidate |
| `ERP2-STD-MIG-001` | Track B Migration Process Standard | freeze candidate |
| `ERP2-STD-EVR-001` | Engineering Evidence & Release Baseline Standard | freeze candidate |
| `ERP2-STD-KRO-001` | Technical Versioning, Supersession & KRO Custody Standard | freeze candidate |

Final acceptance and KRO publication remain separate CIO actions.

## 3. `ERP2-STD-DB-001` — Enterprise Database Architecture & Schema Standard

### 3.1 Platform, ownership, and naming

| Rule | Classification |
|---|---|
| MariaDB `11.4.10` is the current approved non-Production platform baseline; Production activation is separately authorized | `FREEZE-READY` |
| One governed Alembic lineage; every revision has a unique ID, parent, owner, evidence, and upgrade/downgrade result | `FREEZE-READY` |
| Non-Production and Production targets, credentials, runtime activation, and evidence are separate | `FREEZE-READY` |
| Track C owns knowledge tables and knowledge semantics | `FREEZE-READY` |
| Track F Core owns organization, Work, and Communication/Continuity truth; Runtime Orchestration owns its bounded tables | `FREEZE-READY` |
| ERP Functional Domains own their physical tables only after a milestone target model is accepted | `FREEZE-READY` |
| Shared/reference data is owned by an accountable platform/domain owner; no generic ownerless shared table | `FREEZE-READY` |
| Migration/evidence artifacts are not domain business tables and are kept in their custody boundary | `FREEZE-READY` |
| Physical names use lowercase `snake_case`; columns, PK/FK, indexes, unique constraints, junctions, event/history, and migration identifiers follow one documented convention | `FREEZE-READY` |
| Namespace/company/site naming scope and legal entity dimensions | `BUSINESS DECISION DEPENDENT` |

### 3.2 Identity and relationships

| Rule | Classification |
|---|---|
| System identity is separate from Business Reference | `FREEZE-READY` |
| Use immutable surrogate identity; never reuse IDs | `FREEZE-READY` |
| Business keys are explicit, constrained, and scoped only where approved | `FREEZE-READY` |
| External references and aliases are modeled explicitly; they are not hidden in PKs | `FREEZE-READY` |
| Every entity has explicit PK/FK relationships and orphan prevention | `FREEZE-READY` |
| N:N relationships use semantically appropriate junction keys; no unnecessary surrogate identity | `FREEZE-READY` |
| Cross-domain typed references preserve source type, source ID, resolver, and provenance | `FREEZE-READY` |
| Relationship lifecycle and effective dating are explicit where time changes meaning | `FREEZE-READY` |
| Global versus company/site/legal-entity business-key uniqueness | `BUSINESS DECISION DEPENDENT` |

### 3.3 Reference data, lifecycle, audit, and time

| Rule | Classification |
|---|---|
| Reference data has identity, owner, controlled values, lifecycle, version/effectivity, deprecation, and documentation | `FREEZE-READY` |
| Unapproved business-owned value lists are not frozen by the technical standard | `BUSINESS DECISION DEPENDENT` |
| Material lifecycle facts use append-only event/history where appropriate; current state may be derived | `FREEZE-READY` |
| A mutable status column may be used only as a projection/cache when its derivation and reconciliation are defined | `FREEZE-READY` |
| Lifecycle authority and transition evidence are explicit | `FREEZE-READY` |
| Applicable audit minimum: created_at, created_by Participant/Assignment, change/effective evidence, correlation, source reference, AuthorityOrigin, reason/change reference, version/revision | `FREEZE-READY` |
| Audit fields are applied by applicability profile; irrelevant governance fields are not added mechanically to every table | `FREEZE-READY` |
| Use half-open intervals, explicit timezone, overlap prevention, future-effective and historical-read rules | `FREEZE-READY` |
| Retention periods, legal hold, privacy deletion, and archive duration | `SECURITY DECISION DEPENDENT` + `BUSINESS DECISION DEPENDENT` |

### 3.4 Transactions, concurrency, indexes, and data types

| Rule | Classification |
|---|---|
| Application Service owns the transaction boundary; repositories do not silently commit independent business transactions | `FREEZE-READY` |
| Cross-domain distributed commits are not assumed; side effects and compensation are documented | `FREEZE-READY` |
| Database constraints are the first duplicate/integrity guard; explicit locks are added only for proven races | `FREEZE-READY` |
| Race-sensitive operations require concurrency tests, stale-read handling, idempotency, and no blind retry of uncertain effects | `FREEZE-READY` |
| PK/FK/unique indexes are mandatory; secondary indexes require query-plan evidence | `FREEZE-READY` |
| JSON is limited to opaque external payloads, bounded extensions, or non-canonical evidence metadata; canonical searchable meaning uses typed fields/entities | `FREEZE-READY` |
| Use governed lookup/reference tables, constrained vocabularies, application enums, or external mappings according to ownership and change frequency | `FREEZE-READY` |
| No uncontrolled magic strings | `FREEZE-READY` |
| Outbox/event pattern is not mandatory for every service; use only where a durable external side effect requires it and approve per architecture review | `FUTURE DECISION` |

### 3.5 Test target and environment

| Rule | Classification |
|---|---|
| Isolated non-Production target with identity, version, schema revision, and datadir/port evidence | `FREEZE-READY` |
| Deterministic reset/reseed, synthetic fixture ownership, cleanup, listener/process shutdown, and no Production-data leakage | `FREEZE-READY` |
| Evidence manifest records commands, hashes, environment, result, residual state, and custody path | `FREEZE-READY` |

## 4. `ERP2-STD-DEV-001` — Development / Integration Architecture Standard

### Repository and ownership

Application code, domain modules, shared platform, architecture documents, migration source, test assets, evidence, and Track C custody are separate recognizable areas. A domain owns its rules and contracts; shared platform owns cross-cutting validators, not domain decisions. Existing dirty worktrees are preserved unless a separate authorization permits change.

### Backend and frontend

`API / Controller → Application Service → Domain Policy / Rules → Repository / Persistence`

Transport adapters perform admission, invocation, result, and return mechanics only; they do not own business policy or create Authority. Frontends use feature/domain pages, shared components, typed API clients, explicit state boundaries, and no direct database access.

### API and integration contract

APIs use explicit versioning, resource/action semantics, stable error envelopes, correlation, idempotency for repeatable commands, pagination/search contracts where applicable, compatibility rules, and supersession. Integration contracts preserve source/target identity, AuthorityOrigin where organizational Work applies, executor attribution, ReturnTarget, retry/failure class, and no silent attribution rewrite.

`Domain Service != Track F Orchestrator` and no duplicate retry/replay/orchestration engine is introduced.

### Configuration, errors, observability, security

Configuration is typed, environment-separated, validated at startup, and secrets are externalized. Error families include admission, validation, transport, execution, custody, return, business rejection, and Unverified. Minimum structured observability includes correlation, actor/assignment, endpoint/route where applicable, duration, outcome, evidence locator, and lifecycle event. Security consumes approved least privilege, IAM, endpoint ownership, secret, classification, masking, export, and retention policies.

### Testing, deployment, and release

`unit → service/integration → contract → database/migration → concurrency → independent validation`

Promotion requires environment identity, source/schema/API manifest, rollback evidence, and explicit operational authorization. Release identity is immutable; deployed does not mean Go-Live.

All rules in this section are `FREEZE-READY` except security policy values, which are `SECURITY DECISION DEPENDENT`.

## 5. `ERP2-STD-ADR-001` — ADR Standard

### Required template

`ADR ID, Title, Status, Context, Decision, Alternatives, Rationale, Consequences, Dependencies, Scope/Boundary, Owner, Approval Authority, Effective Version, Evidence, Supersedes, Superseded By, Review Date`.

Allowed lifecycle: `PROPOSED`, `ACCEPTED`, `REJECTED`, `DEFERRED`, `SUPERSEDED`, `RETIRED`.

### Operating rules

- Anyone may draft within assigned Work; the draft must state uncertainty and boundary.
- CTO/technical owner performs technical review.
- CIO or the named Business/Security/Operations authority accepts decisions within their authority ceiling.
- An ADR becomes effective only after acceptance and evidence custody.
- Supersession creates a new version/ADR and retains the historical predecessor; it does not overwrite history.
- KRO custody requires owner, version, representation, storage locator, provenance, hash, lifecycle event, and supersession link.
- The ADR does not itself create Authority or implementation authorization.

Classification: template and lifecycle are `FREEZE-READY`; acceptance authority for a particular business/security decision is `BUSINESS/SECURITY DECISION DEPENDENT`.

Historical decisions recommended for later ADR conversion, without bulk creation here:

1. Track F A/B/C boundaries and shared references.
2. Track C identity/version/representation/storage separation.
3. Single governed Alembic lineage and historical-root reconciliation.
4. Dedicated Participant Runtime Adapter versus raw Session endpoint.
5. P0 runtime spine and dependency-triggered route activation.
6. No authoritative target model, no migration execution.
7. Item Master identity/reference admission.
8. Governance approval versus execution authorization.

## 6. `ERP2-STD-MDP-001` — Module Development Pack Standard

Every Functional Domain/Module must maintain:

1. Module Overview
2. Scope / Out-of-Scope
3. Functional Requirements
4. Business Rules
5. Ownership / Source-of-Truth
6. Domain Model
7. Logical Schema
8. Physical Schema
9. API Contract
10. UI Contract
11. Authority / Role Rules
12. Integration Contract
13. Event / Trigger Contract
14. Test Contract
15. Migration Contract
16. Security / Data Classification
17. Observability
18. Known Decisions
19. Known Gaps
20. Deferred Items
21. Release Evidence
22. Version / Custody Manifest
23. Rollback / Reconciliation
24. Dependencies / Prerequisites

### Completion gates

| Gate | Minimum condition |
|---|---|
| Design Ready | scope, business meaning, owner candidates, logical model, dependencies, unresolved questions |
| Implementation Ready | accepted technical design, physical impact, API/integration contract, authority ceiling, test contract, bounded Work authorization |
| Validation Ready | implementation identity, environment, fixtures, acceptance/negative/concurrency/migration tests, cleanup plan |
| Migration Ready | authoritative target model, approved mapping, pilot/reconciliation plan, rollback, KRO custody, explicit migration authorization |
| Release Ready | validation PASS, residual risk accepted, release manifest, rollback evidence, operational/security/business approvals as applicable |

Gate labels are `FREEZE-READY`; the actual approval remains milestone-specific.

## 7. `ERP2-STD-CTX-001` — ERP2.0 Engineering Context Manifest

The manifest is mandatory for Internal Engineer, Remote Engineer, Contractor, Codex, Claude Code, and future automated workers.

### Required fields

- product/version and environment;
- authoritative baselines and artifact hashes;
- repository layout and allowed paths;
- current DB/Alembic revision, schema, and API baseline;
- active Domain, Milestone, Sprint, WorkItem;
- Participant, Assignment, Context, Scope, Authority ceiling;
- allowed actions and prohibited action vocabulary;
- dependencies, open decisions, uncertainty, freshness;
- validation commands, expected evidence, cleanup/reset;
- KRO references, ReturnTarget, CorrelationID, escalation target;
- current owner and handoff history.

### Safety rules

`STALE / INCOMPLETE CONTEXT → SAFE_STOP`.

No worker silently resolves missing governance/business truth, assumes an endpoint/authority, promotes a document to Knowledge, or treats a task completion surface as proof of technical result. Every return states what was observed, what was not observed, exact blocker, owner, and minimum next action.

The field contract and safe-stop rules are `FREEZE-READY`; actual authority values are `BUSINESS/SECURITY/OPERATIONAL DECISION DEPENDENT`.

## 8. `ERP2-STD-MIG-001` — Track B Migration Process Standard

| Stage | Required owner | Entry | Exit | Evidence/KRO | Rollback/reconciliation | Stop |
|---|---|---|---|---|---|---|
| B0 Source Inventory | source/data owner + CTO | access/custody approved | complete inventory, owner, hashes | inventory/provenance custody | preserve source, no writes | source authority or access unclear |
| B1 Profiling/Qualification | data owner + Engineering | B0 accepted | quality, duplicates, nulls, code profile accepted | reproducible profile and exceptions | no target mutation | unsafe quality/identity |
| B2 Target Mapping | Business/Data owner + CTO | authoritative logical target | mapping, rules, exceptions accepted | mapping matrix, target refs, decisions | dry-run only until approved | `NO AUTHORITATIVE TARGET MODEL` |
| B3 Pilot/Reconciliation | CTO + Engineering + TEST | B2 accepted, isolated target | repeatable pilot, identity/count/balance/lineage reconciliation | pilot evidence, readback, KRO custody | deterministic rollback/reset | mismatch, loss, unresolved authority |
| B4 Production/Cutover | CIO/Business + CTO | B3 accepted and Production authorization | rehearsal, final reconciliation, rollback readiness | cutover, signoffs, audit | tested rollback and final reconciliation | any production/authority/rollback gap |

Mandatory invariants:

`NO AUTHORITATIVE TARGET MODEL → NO MIGRATION EXECUTION`  
`NO VALIDATED PHYSICAL TARGET → NO PILOT MIGRATION`  
`NO ACCEPTED PILOT / RECONCILIATION → NO PRODUCTION MIGRATION`

B4 is separately authorized. No migration occurred in this package.

## 9. `ERP2-STD-EVR-001` — Engineering Evidence & Release Baseline

Material work must return:

- request/authorization identity and boundary;
- participant/assignment/provenance;
- source/worktree/branch/commit identity where relevant;
- environment/database/runtime identity;
- frozen input and changed-file hashes;
- schema/Alembic revision;
- exact test commands and results;
- positive, negative, regression, concurrency, and migration roundtrip evidence where applicable;
- cleanup/shutdown and residual state;
- release manifest, approval state, risks, unresolved conditions, and return recipient.

Required semantic distinctions:

`TECHNICAL PASS != BUSINESS ACCEPTANCE`  
`RELEASE BUILT != RELEASE AUTHORIZED`  
`DEPLOYED != GO-LIVE`  
`INVOCATION != EXECUTION`  
`EXECUTION != VALIDATION != CUSTODY != WORK COMPLETION`

Evidence is immutable after validation; corrections create a new version/manifest. Hashes are computed over durable artifacts and never treated as authority by themselves.

Classification: evidence fields and lifecycle are `FREEZE-READY`; business acceptance and Production release authority are `BUSINESS DECISION DEPENDENT`.

## 10. `ERP2-STD-KRO-001` — Technical Versioning, Supersession & KRO Custody

Every technical standard/evidence artifact uses:

`KnowledgeItem identity → KnowledgeVersion → KnowledgeRepresentation → KnowledgeStorage`

Required metadata: owner assignment, source/provenance references, creation/review event, content hash where applicable, representation type, storage locator, effective/superseded state, and downstream freshness relationship.

Rules:

- stable KnowledgeItem identity is not a file path or database revision;
- version changes preserve prior versions;
- representation is not storage;
- source-system commit/release/Alembic ID is not automatically a KnowledgeVersion;
- publication requires explicit governance/custody event;
- supersession creates a new version and retains historical lineage;
- stale downstream context must be detected and safe-stopped;
- runtime Work/Message/Result does not become Knowledge without explicit promotion semantics.

KRO registration/publication is not authorized by M0-A3-T1. The standard is `FREEZE-READY`; publication owner/acceptance is `OPERATIONAL DECISION DEPENDENT` where custody operations are concerned.

## 11. Cross-Standard Consistency Matrix

| Boundary | DB | Development | ADR/Module | Context/Evidence | Migration/KRO | Result |
|---|---|---|---|---|---|---|
| Track C owns durable knowledge | typed source/storage and no hidden file truth | code/evidence separated from KRO | package/ADR have custody metadata | provenance/hash/locator required | publication/supersession explicit | `CONSISTENT` |
| Track F owns Work/Authority/runtime | actor/context/work refs explicit | services do not recreate orchestrator | module authority contract | correlation/ReturnTarget | migration references target facts | `CONSISTENT` |
| Domain owns business rules | typed physical model per milestone | domain policy layer | module rules required | evidence proves, not invents, business truth | target model before mapping | `CONSISTENT` |
| Migration does not define target truth | target schema precedes B3 | mapping is separate contract | ADR/decision evidence required | pilot reconciliation | B2 before B3/B4 | `CONSISTENT` |
| Adapter/transport owns no business policy | endpoint/route separate from Authority | transport adapter below domain service | module authority rules remain | attribution preserved | no route/authority invention | `CONSISTENT` |
| Documentation does not create Authority | no DB/schema mutation from docs | Work authorization required | ADR acceptance distinct from execution | evidence not approval | CIO/Business gate retained | `CONSISTENT` |

No material cross-standard contradiction was found.

## 12. Unresolved dependencies and classification

| Dependency | Classification | Handling |
|---|---|---|
| business-key scope and company/site/plant dimensions | `BUSINESS DECISION DEPENDENT` | do not freeze global uniqueness |
| entity ownership and Source-of-Truth | `BUSINESS DECISION DEPENDENT` | maintain owner-question register |
| archive/retention/legal deletion periods | `BUSINESS + SECURITY DECISION DEPENDENT` | technical hooks only |
| personal/financial/regulated data classes | `SECURITY DECISION DEPENDENT` | consume policy when approved |
| operational support/availability and TMS/HR boundaries | `OPERATIONAL DECISION DEPENDENT` | dependency-triggered design |
| outbox/event adoption by domain | `DEFERRED` | decide per integration need |
| final roadmap priority | `DEFERRED` | CIO review after standards freeze |
| KRO publication of these candidates | `DEFERRED` | separate custody/publication action |

These unresolved items do not block generic technical-standard preparation.

## 13. CIO freeze-review checklist

1. Accept or revise the eight proposed standard identities.
2. Confirm that `FREEZE-READY` rules are technical baselines, not implementation authority.
3. Assign owners for Business/Security/Operations-dependent rules.
4. Approve whether outbox is optional per domain or requires a common gate.
5. Approve the Context Manifest as mandatory for Human/AI/Remote Engineering work.
6. Approve evidence/release minimums and KRO custody/publication workflow.
7. Determine final KRO publication action; none was performed here.

## 14. Boundary and Stop/Re-entry assessment

- No new core Track is required.
- MariaDB remains compatible with the accepted architecture.
- Track C supports the versioning/provenance/custody model.
- Track F supports the work/authority/runtime/evidence model.
- Standards are mutually consistent.
- No irreversible implementation was required to define any standard.
- Business, Security, Privacy, and Operations unknowns are retained as labelled dependencies.
- No schema, migration, Functional module, Authority, route, Message Bus, Production, Cutover, or Go-Live action occurred.

The M0-A3-T1 Stop/CIO re-entry conditions were not triggered.

## 15. Final status

`ERP2.0-M0-A3-T1 TECHNICAL FOUNDATION STANDARDS = COMPLETE / READY FOR CIO FOUNDATION FREEZE REVIEW`
