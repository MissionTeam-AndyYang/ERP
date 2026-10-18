# ERP2.0 Engineering Foundation V1.2 Approval Candidate

**Document ID:** `CIO-GOV-ERP2-ENG-FOUNDATION-V12-20261018-001`  
**Status:** `READY_FOR_CIO_APPROVAL / NOT_EFFECTIVE`  
**Owner:** CTO Office V2  
**Final approval authority:** CIO Office Governance V3  
**Review date:** 2026-10-18 (Asia/Taipei)

## 1. Authority and relationship

This is a controlled V1.2 approval candidate. It does not become effective until CIO approval and the required Repository/PM registration are recorded. Foundation V1.1 remains the current approved Functional Mainline baseline. The earlier V1.2 candidate collection remains preserved as historical input; this document is a reviewed candidate, not a silent replacement.

Proposed canonical path after approval:

`01_Foundation/standards/ERP2.0-ENGINEERING-FOUNDATION-V1.2-APPROVAL-CANDIDATE-20261018-001.md`

Current working path:

`20_Engineering_Workspace/Pre_FM01_Foundation_Finalization_20261018_001/ERP2.0-ENGINEERING-FOUNDATION-V1.2-APPROVAL-CANDIDATE-20261018-001.md`

## 2. Source baseline

| Source | Role | Status |
|---|---|---|
| `ERP2.0-FUNCTIONAL-DELIVERY-STANDARD-V1-FINAL-20261012-002.md` | Functional Mainline V1 authority | Existing baseline |
| `ERP2.0-FUNCTIONAL-DELIVERY-STANDARD-V1.1-CIO-ADDENDUM-20261013-001.md` | Detailed evidence and delivery supplement | Approved for FM-02 pilot and later FM-01 application |
| `ERP2.0-FUNCTIONAL-DELIVERY-STANDARD-V1.2-CIO-CANDIDATE-20261013-001.md` | Historical candidate input | Candidate only |
| `FM02-FOUNDATION-DELTA-AND-PROPOSED-CROSS-MODULE-STANDARD-20261018.md` | FM-02 delta and reusable delivery controls | CIO-approved bounded standard reference |
| `ERP2.0-PMO-LIFECYCLE-AND-REPORTING-STANDARD-FM02-20261018-001.md` | PM lifecycle/reporting control | Effective v1 within approved bounded scope |
| `Remote-Test-Execution-Standard.md` | Remote test execution boundary | Ready for CTO review; preparation-only |

The candidate uses these sources by reference. It does not duplicate or override their text.

## 3. Normative scope

V1.2 consolidates the minimum cross-module operating controls needed to transfer the FM-02 evidence model to FM-01 and later modules:

1. Design and architecture review gates must identify entry predicate, decision authority, evidence and safe-stop condition.
2. Protected implementation requires a fresh Engineering task, accepted capability/executor, authorized workspace, ReturnTarget and attributable source commit. Dispatch is not acceptance.
3. Database/schema/migration, backend/API and frontend/UI/CSS work are separate bounded layers with separate implementation, review and test evidence.
4. Approved coding conventions are applied by reference to the verified shared convention source; missing or proposed conventions remain `NOT_VERIFIED` or `PROPOSED` until approved.
5. Source integration, Independent TEST, remote test handoff, PM closure and Repository custody are distinct gates. Custody, readiness and mock/static evidence cannot be promoted to live execution or module acceptance.
6. Every delivered artifact carries stable identity, version/status, owner, approval evidence, exact Git path/commit/tree/hash, related tests, Knowledge reference, known gaps and non-authorizations.
7. PM reporting follows the complete chain `Module → Milestone → Sprint → WorkItem → Engineering Assignment → Artifact → Review → Test → Defect/Retest → Acceptance → Closure/Deferred Obligation`.
8. Deferred obligations are explicit, especially DB-dependent tests, restricted cases, unbound executors, protected-main merge, release and Production.

## 4. Layer and evidence rules

The V1.2 candidate retains the V1.1 layer model: requirements/ownership, database, backend business logic, REST API, integration, TEST, source/as-built, Repository/handover and UI. Each layer records design, source, runtime, test, custody and acceptance separately.

For HTTP services, a human-readable contract and machine-readable OpenAPI record are required where the service exists. Source existence does not prove route registration or live deployment. For migrations, applied history is not rewritten; target identity, revision, backup/recovery and protected mutation authority remain separate prerequisites.

Independent TEST must have attributable reviewer/task evidence and must be tied to Case/Run IDs, exact source, target, command, fixture, cleanup and limitations. Engineering self-test does not replace Independent TEST.

## 5. Version, supersession and approval

This candidate proposes a controlled successor relationship to V1.1 only. It does not supersede V1.1, assign an automatic successor version, or make Foundation V1.2 effective. CIO must approve the exact candidate and its effective date. Repository Office may register it as effective only after that approval and successful remote/Knowledge readback.

Future material changes follow the established version-change process and may require V1.3; no automatic promotion is implied.

## 6. Explicit non-authorizations

This candidate does not authorize database credentials, SQL, migration execution, Restore/Restart, Product-main merge, Production, release, unrestricted shell/host capability, live test execution, or new Product/SKU scope. FM-02 remains `DEV DELIVERY ACCEPTED WITH CONDITIONS`; full module acceptance remains not approved.

## 7. Proposed acceptance record

`FOUNDATION_V1.2 = READY_FOR_CIO_APPROVAL / NOT_EFFECTIVE`  
`FOUNDATION_V1.1 = EXISTING_BASELINE`  
`FOUNDATION_STANDARD_CONFLICTS = 0`  
`CIO_V1.2_FINAL_APPROVAL = PENDING`

The zero-conflict result means no contradictory normative rule was found in the bounded comparison. The candidate addresses identified omissions around assignment acceptance, evidence-state separation, remote handoff and deferred-obligation recording without changing approved business scope or execution authority.

