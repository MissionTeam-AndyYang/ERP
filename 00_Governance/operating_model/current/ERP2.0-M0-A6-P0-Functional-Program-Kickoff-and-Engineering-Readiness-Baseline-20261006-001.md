# ERP2.0 M0-A6-P0 Functional Program Kickoff & Engineering Readiness Baseline

## Control

- Authorization: `ERP2.0-M0-A6-P0`
- Request: `ERP2.0-M0-A6-P0 — Functional Program Kickoff & Engineering Readiness Baseline`
- Owner: Program Management Office
- Required collaborators: CTO Office, Knowledge Repository / KRO, Repository Office
- Effective date: 2026-10-06, Asia/Taipei
- Input foundation: `ERP2.0-M0-A4 Enterprise Foundation Baseline v1`
- Input roadmap: `ERP2.0-M0-A5-R1 Functional Mainline Roadmap Baseline v1`
- Scope: operating model and readiness baseline only
- Exclusions: functional implementation, physical functional schema execution, B2/B3/B4 migration, Production, Cutover, Go-Live, irreversible repository restructuring, Message Bus activation, authority or route creation

## Completion

`ERP2.0-M0-A6-P0 PROGRAM KICKOFF & ENGINEERING READINESS = COMPLETE / READY FOR CIO FREEZE REVIEW`

This result means the operating/readiness package is prepared for CIO freeze review. It does not authorize FM-01 implementation, physical schema work, migration, release, or operational use.

## 1. Authoritative Inputs

| Input | Custody / status |
|---|---|
| Enterprise Foundation | `03_Track_C_Knowledge_Repository/Enterprise_Foundation_Baseline/ERP2.0-M0-A4-C1-Enterprise-Foundation-Baseline-Custody-Publication-20261005-001.md`; SHA-256 `561C0D57246878A18A14660E2A7D47D36AD92567E158A8A4C95ED969BBE4457B` |
| Foundation freeze package | `ERP2.0-M0-A4 Enterprise Foundation Baseline Freeze Package`; SHA-256 `26974F0DEE8C2705FDE881D61ADE25DEB800C6DBBB46B75B70E71FAB33F8A787` |
| Functional Roadmap | `03_Track_C_Knowledge_Repository/Functional_Mainline_Roadmap_Baseline/ERP2.0-M0-A5-C1-Functional-Mainline-Roadmap-Baseline-Custody-Publication-20261005-001.md`; roadmap report SHA-256 `CE63B5F70ABFE5CC334E05FDBB491B34FE30A68988077F6FBE5F86FBD5FAA23C` |
| MDP standard | `03_Track_C_Knowledge_Repository/Technical_Foundation_Standards/ERP2-STD-MDP-001-Module-Development-Pack-Standard-20261005-001.md` |
| KRO custody standard | `03_Track_C_Knowledge_Repository/Technical_Foundation_Standards/ERP2-STD-KRO-001-Technical-Versioning-Supersession-and-KRO-Custody-Standard-20261005-001.md` |

The source artifacts remain authoritative in their existing custody. This package is an operating overlay and does not create competing Foundation or Roadmap identities.

## 2. Functional Program Kickoff Standard

### 2.1 One-time kickoff

Program Kickoff establishes the operating identity and shared control model for the ERP2.0 Functional Mainline Program. It occurs once for this Program identity. A new kickoff is required only if CIO creates a materially new Program identity.

Kickoff establishes:

- authoritative Foundation and Roadmap references;
- Program identity and current phase;
- milestone, sprint, backlog, WorkItem and dependency models;
- decision and blocker/risk registers;
- PMO trigger model and reporting cadence;
- CTO decomposition and technical confirmation model;
- independent TEST validation model;
- KRO custody and Repository Office publication model;
- CIO re-entry conditions.

### 2.2 Distinct initiation events

| Event | Meaning | Authority |
|---|---|---|
| Program Kickoff | creates the operating frame for the whole Functional Mainline Program | CIO freeze / Program creation |
| Milestone Initiation | opens one roadmap milestone under the frozen frame | PMO after applicable entry decision |
| Sprint Initiation | opens a bounded Sprint under an initiated milestone | PMO/CTO within milestone authority |

No milestone or Sprint is implicitly activated by this package.

### 2.3 Control objects

Each active object carries a stable identity, owner, parent identity, scope, dependency set, authority ceiling, status, evidence locator, hash, and next decision point.

Minimum objects: Program, Milestone, Sprint, Backlog Item, WorkItem, Dependency, Decision, Blocker/Risk, Validation Result, Knowledge Promotion Record.

## 3. Functional Development Lifecycle

The standard lifecycle is:

`Business Meaning`
→ `Domain Architecture`
→ `Canonical / Logical Data Model`
→ `Physical Schema`
→ `API / Integration Contract`
→ `Implementation Readiness`
→ `Backend / Domain Logic`
→ `Frontend / UI where applicable`
→ `Automated Test`
→ `Independent Validation where applicable`
→ `Migration / Reconciliation where applicable`
→ `Operational Readiness`
→ `Documentation / Module Pack`
→ `KRO Custody`
→ `Module / Milestone Closure`

Each stage must state one of: `NOT STARTED`, `IN PROGRESS`, `READY`, `PASS`, `PASS WITH CONDITIONS`, `BLOCKED`, `NOT APPLICABLE`, or `CLOSED`.

Readiness meanings are separate:

- Design Ready: meaning, boundaries, owners, model and dependencies are sufficiently defined.
- Implementation Ready: bounded work authorization, contracts, authority ceiling and test contract exist.
- Validation Ready: implementation identity, environment, fixtures, acceptance and negative controls exist.
- Release Ready: validation result, residual risk, release manifest and rollback are accepted.
- Operational Ready: support, monitoring, recovery and operating ownership are accepted.
- Complete: all applicable gates are accepted and custody/closure evidence is recorded.

`IMPLEMENTED != COMPLETE`; `TEST PASS != BUSINESS ACCEPTANCE`; `RELEASE READY != GO-LIVE`.

## 4. Module Definition of Done

A module can be `COMPLETE` only when every applicable row is explicitly `PASS`, `PASS WITH CONDITIONS` with accepted residual conditions, or `NOT APPLICABLE` with rationale.

| Area | Required evidence |
|---|---|
| Business | scope, rules, owner, Source-of-Truth decision where required, deferred questions |
| Data | domain/logical/physical model, identity, lifecycle, constraints |
| Backend | domain logic, transaction boundary, errors, idempotency, concurrency |
| API/Integration | versioned contract, positive/negative cases, integration behavior |
| UI | implemented/tested where applicable, otherwise explicit N/A |
| Security | classification, access/IAM requirements, deferred security decisions |
| Test | unit, integration, contract, negative, migration/database/concurrency/regression as applicable, independent TEST where required |
| Migration | Track B stage, mapping, reconciliation, pilot, rollback and explicit authorization where applicable |
| Operations | deployment, health, support, monitoring, rollback/recovery |
| Documentation | Module Development Pack, Context Manifest, ADRs, schema/API docs, decision/gap records |
| Custody | accepted evidence in KRO, provenance, representation, storage, version and hash |

Completion state vocabulary: `DESIGN_READY`, `IMPLEMENTATION_READY`, `VALIDATION_READY`, `RELEASE_READY`, `OPERATIONAL_READY`, `COMPLETE_WITH_CONDITIONS`, `COMPLETE`, `BLOCKED`.

## 5. Schema Review & Baseline Protocol

| Stage | Inputs / owner | Exit evidence |
|---|---|---|
| SR-0 Business / Entity Semantics | business meaning, domain owner; PM facilitates | terms, boundaries, unresolved owner/SoT decisions |
| SR-1 Canonical / Domain Model | domain architect + CTO | entities, relationships, lifecycle, identity |
| SR-2 Logical Schema | data/domain engineering | logical tables/fields, constraints, indexes, lineage |
| SR-3 Physical Schema | CTO + Engineering | engine-specific DDL, migration impact, rollback plan |
| SR-4 Constraint / Transaction / Concurrency | CTO + Engineering + TEST when released | transaction, locking, idempotency, negative/concurrency evidence |
| SR-5 Migration / Reconciliation | PM + data/migration owner | mapping, pilot, reconciliation, rollback, B-stage authority |
| SR-6 Cross-Domain Integration | CTO + affected domain owners | contract, identity/reference, integration evidence |
| SR-F Final Schema Baseline | PM/KRO with CTO recommendation | accepted baseline identity, hash, provenance, KRO custody |

Decision rights: PM controls sequencing and record integrity; CTO controls technical confirmation; domain/business authority accepts business meaning and Source-of-Truth decisions; TEST provides independent validation only when released; KRO records governed knowledge; CIO decides material scope, authority, unresolved cross-boundary conflicts and freeze.

Every stage records inputs, owner, reviewers, decision, evidence, validation, exit criteria, CIO re-entry trigger and KRO custody point.

Required pattern: `bounded review → issue finding → correction → validation → integration review → baseline`.

No Functional production schema is created or altered by P0.

## 6. Documentation Standard

Required categories: Foundation, Roadmap, Milestone, Sprint, Module, Architecture, Schema, API, Integration, Migration, Test, Release, ADR, Decision, Operation, Onboarding.

Every artifact records: identity, title, owner, status, parent object, source/provenance, created/reviewed time, content hash, representation, storage locator, dependencies, authority ceiling, supersession state and next action.

Document states:

- `WORKING`: editable engineering content;
- `REVIEW`: submitted for review;
- `ACCEPTED`: decision accepted but not necessarily KRO-published;
- `PUBLISHED`: KRO-custodied governed knowledge;
- `SUPERSEDED`: retained historical version replaced by a later accepted version;
- `HISTORICAL`: retained evidence, not current authority.

Historical chat is never the sole authoritative engineering context.

## 7. GitHub / Repository / KRO Knowledge Architecture

### 7.1 Responsibility boundaries

- GitHub: shared versioned engineering storage and collaboration surface.
- KRO/Track C: KnowledgeItem, KnowledgeVersion, provenance, lifecycle, canonical acceptance, representation, storage linkage, publication and freshness.
- Repository Office: repository structure, naming, path standards, hygiene, governed branching/release conventions and source/evidence separation.
- PMO: program control, package correlation and decision routing.
- CTO: technical custody/decomposition and engineering confirmation.

Preserve: `GitHub file != Knowledge authority`; `GitHub path != KnowledgeItem identity`; `Git commit != KnowledgeVersion automatically`; `Merge != Governance approval`; `GitHub release != Go-Live authorization`.

### 7.2 Target structure candidate

`Governance/`, `Foundation/`, `Programs/ERP2.0-Functional-Mainline/`, `Domains/<domain>/`, `Engineering/{backend,frontend,integration,migrations,tests}/`, `Evidence/`, `Operations/`, `Onboarding/`.

This is a `REPOSITORY TARGET STRUCTURE CANDIDATE` only. Existing files must be compared before any move. No irreversible move or repository rewrite is authorized by P0.

### 7.3 Promotion model

`Working → Review → Accepted → KRO KnowledgeVersion → Canonical Representation / Storage linkage → Published`

Publication requires an explicit governance/custody event. A source commit, file path or merge is not a substitute for KRO acceptance.

## 8. Working Content vs Governed Knowledge

Working content includes code, draft schema/API/ADR, Sprint work and test development. Governed published knowledge includes Foundation/Roadmap baselines, accepted standards, accepted ADRs, accepted schema baselines, accepted Module Packs, release baselines and milestone closure packages.

The same content may have a Git representation and a KRO representation, but each representation must retain its own identity, hash and lineage.

## 9. Engineering Context Consumption Model

Each Engineering Context Manifest references, where applicable: KnowledgeItem/KnowledgeVersion, Git repository/path/commit/tag/hash, schema revision, API version, Module Pack, Program/Milestone/Sprint/WorkItem, allowed paths, authority ceiling, validation commands and KRO canonical references.

Consumer sequence:

1. resolve current accepted context;
2. verify identity, hash and freshness;
3. verify scope and authority ceiling;
4. verify working baseline and allowed paths;
5. acknowledge dependencies and stop conditions;
6. execute only after entry criteria pass;
7. return attributable evidence and hash;
8. promote only through the governed promotion model.

`STALE / INCOMPLETE CONTEXT → SAFE_STOP`.

## 10. FM-01 / Sprint-01 Readiness Checklist

Target: `M0-FM-01 — Shared Enterprise / Master Data Foundation`.

| Check | Required state at entry |
|---|---|
| Program Kickoff | accepted/frozen by CIO |
| Foundation/Roadmap | authoritative custody and hash verified |
| Repository structure | current structure inventoried; target candidate understood |
| Documentation | standard active; Module Development Pack template initialized |
| Context Manifest | initialized with accepted references and authority ceiling |
| Schema review | SR-0 through SR-F protocol available; no physical schema execution in P0 |
| Source inventory | bounded source inventory and evidence boundary defined |
| Business backlog | clarification backlog with owner/dependency/status |
| Track B | B0/B1 boundaries explicit; B2/B3/B4 not implied |
| TEST | test plan and independent validation trigger identified |
| KRO | custody/promotion paths and metadata requirements defined |
| CIO re-entry | material scope, SoT, security, migration, production and authority triggers recorded |
| FM-01 decision | separate milestone entry decision received |

FM-01 implementation is `NOT STARTED / NOT AUTHORIZED` by this package.

## 11. Decision / Gap Register

| ID | Decision/gap | Owner | State | CIO re-entry |
|---|---|---|---|---|
| GAP-01 | FM-01 milestone entry and Sprint-01 authority | CIO/PMO | OPEN | required before implementation |
| GAP-02 | named domain owners and Source-of-Truth decisions | business/domain owners | OPEN | required where material |
| GAP-03 | security/privacy/access policy for each module | CIO/security owner | OPEN | required before security-sensitive work |
| GAP-04 | legal/site/operational scope | business/operations | OPEN | required where applicable |
| GAP-05 | KRO publication event for this package | CIO/KRO | PENDING | required for governed publication |
| GAP-06 | Repository Office review of target hierarchy | Repository Office | OPEN | required before movement/restructure |
| GAP-07 | Track B migration gate selection | PM/CTO/business | OPEN | required before B2/B3/B4 |
| GAP-08 | independent TEST release criteria per milestone | PM/CTO/TEST | DEFINED / NOT RELEASED | separate release decision |

## 12. Proposed Freeze Decision Matrix

| Subject | Proposed disposition | Authority |
|---|---|---|
| Program operating model | freeze after CIO review | CIO |
| Lifecycle / DoD / schema protocol | freeze as controlled standard | CIO with CTO recommendation |
| Documentation / context model | freeze as controlled standard | CIO/KRO |
| GitHub/KRO relationship | freeze as operating architecture, not SoT selection | CIO/KRO/Repository Office |
| Target repository hierarchy | candidate only | Repository Office review required |
| FM-01 implementation | not authorized by P0 | separate CIO decision |
| Physical functional schema | not authorized by P0 | separate technical/business decision |
| B2/B3/B4 migration | not authorized by P0 | separate Track B authority |
| Production/Cutover/Go-Live | not authorized | CIO |

## 13. Evidence Manifest

| Evidence | Identity | Status |
|---|---|---|
| This readiness package | `ERP2.0-M0-A6-P0-20261006-001` | PM prepared; CIO freeze review pending |
| M0-A4 Foundation custody/publication | `ERP2.0-M0-A4-C1` | existing accepted input |
| M0-A5 Roadmap custody/publication | `ERP2.0-M0-A5-C1` | existing accepted input |
| MDP standard | `ERP2-STD-MDP-001` | existing technical standard |
| KRO custody standard | `ERP2-STD-KRO-001` | existing technical standard |
| Repository target | `ERP2.0-REPOSITORY-TARGET-CANDIDATE-001` | candidate only |
| FM-01 checklist | `ERP2.0-M0-FM-01-SPRINT-01-READINESS-001` | prepared; implementation not authorized |

## 14. Explicit Non-Authorization

This package did not activate Functional implementation, create/alter Functional physical schema, execute B2/B3/B4 migration, restructure or move repository content, activate Message Bus, change authority/routes, enter Production, Cutover or Go-Live, or invent Business/Security/Operational truth.

## 15. Required CIO Disposition

CIO Governance shall select one:

1. `FREEZE / ACCEPT M0-A6-P0 OPERATING BASELINE`
2. `ACCEPT WITH SPECIFIC CONDITIONS`
3. `RETURN FOR SPECIFIC CORRECTION`
4. `PARTIAL / CIO DECISION REQUIRED`

Until disposition, the package is usable as a PM/CTO working readiness reference but is not a frozen governance standard.
