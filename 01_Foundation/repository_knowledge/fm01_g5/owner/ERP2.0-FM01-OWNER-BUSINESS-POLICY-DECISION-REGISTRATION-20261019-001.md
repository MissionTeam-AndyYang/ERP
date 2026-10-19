# ERP2.0 FM-01 V1 Owner Business Policy Decision Registration

INTER-OFFICE RELAY COMMUNICATION STANDARD 003

## Registration Identity

- **Record:** `ERP2.0-FM01-OWNER-BUSINESS-POLICY-DECISION-REGISTRATION-20261019-001`
- **Decision ID:** `ERP2.0-FM01-OWNER-BUSINESS-POLICY-20261019-001`
- **Decision source:** CIO Office Governance V3 / Owner, `ERP2.0 — FM-01 V1 Owner Business Policy Decision Registration`
- **Decision date:** `2026-10-19`
- **Module:** FM-01 Organization / Location V1
- **Scope:** BP-01 through BP-18 business policy registration
- **Registering channel:** Business Owner Review Channel
- **Register owner:** Program Office policy-register record
- **Return target:** CIO Office Governance V3; CTO Office V2; Repository Office; PM Office

## Terminal Registration Fields

`DECISION_ID=ERP2.0-FM01-OWNER-BUSINESS-POLICY-20261019-001`

`OWNER_BP01_BP18=APPROVED`

`BO_BOARD_REGISTRATION=PASS`

`FM01_POLICY_REGISTER_UPDATE=PASS`

`DECISION_READBACK=REQUIRED`

`FM02_REFRESH=DEFERRED`

`CODING_AUTHORIZATION=NOT_GRANTED`

`TEST_AUTHORIZATION=NOT_GRANTED`

`PRODUCTION_AUTHORIZATION=NOT_GRANTED`

This is an additive registration of the CIO Owner Decision. It preserves prior decision history and does not itself authorize coding, database work, test execution, migration, runtime operation, or production change.

## Approved Business Policy Baseline

The following BP-01 through BP-18 items are registered as the approved FM-01 V1 business-policy baseline. Conditions stated in an item are binding limits on interpretation; they are not permission to infer missing execution bindings.

| ID | Registered business policy | Registration treatment |
|---|---|---|
| `BP-01` | FM-01 is the authoritative minimum maintenance service for the six entities: Legal Entity, Company, Site, Plant, Warehouse, and Location. Proposed stewardship is Corporate Administration for Legal Entity / Company, Production Operations for Site / Plant, and Warehouse Operations for Warehouse / Location. | **APPROVED**; actual appointments remain separately controlled. |
| `BP-02` | Separate `Reader`, `Maintainer`, `Approver`, `Audit Reader`, and `Technical Operator` roles are required. | **APPROVED**. |
| `BP-03` | An authorized Maintainer may directly update only allowlisted non-structural fields, initially limited to display name and applicable approved description / remark fields. | **APPROVED**; exact DB/API field catalogue remains an execution binding. |
| `BP-04` | Technical ID, stable reference, entity type, parent relationship, approval state, and audit fields cannot be directly edited through ordinary maintenance. | **APPROVED**. |
| `BP-05` | Create requires independent Approver approval before final business effect. | **APPROVED**. |
| `BP-06` | V1 lifecycle states are Active and Inactive. Pending Approval is a separate workflow state, not an additional lifecycle state. | **APPROVED**. |
| `BP-07` | Deactivation is prohibited while unresolved active dependent records or material downstream conflicts exist. | **APPROVED**. |
| `BP-08` | Reactivation requires parent validity, reference uniqueness, and relationship checks plus independent approval. | **APPROVED**. |
| `BP-09` | Preserve the Legal Entity -> Company -> Site -> Plant hierarchy. Warehouse is Site-scoped, with Plant association only as admitted by the business/schema contract. Location is Warehouse-scoped. Existing schema must not be silently changed. | **APPROVED WITH EXISTING-SCHEMA CONDITION**. |
| `BP-10` | Nested Location hierarchy is not activated in V1; future extension capability is retained. | **APPROVED**. |
| `BP-11` | A requester cannot approve the requester's own operation; approval must respect domain and scope authority. | **APPROVED**. |
| `BP-12` | Approver delegation is permitted only with explicit scope, duration, authorization, and segregation-of-duties enforcement. | **APPROVED**. |
| `BP-13` | Audit captures actor, timestamp, operation, entity, before / after values, reason, approver where applicable, and correlation evidence. | **APPROVED**. |
| `BP-14` | Seven-year retention is the proposed V1 default, subject to legal / corporate records-policy confirmation before enforcement or deletion. No automatic purge is permitted until confirmed. | **APPROVED WITH RETENTION-CONFIRMATION CONDITION**. |
| `BP-15` | Audit read access is restricted to authorized Audit Reader / governance roles. Maintainers cannot alter audit evidence. | **APPROVED**. |
| `BP-16` | FM-01 is the authoritative business maintenance interface for the six masters. Other modules consume approved APIs and cannot independently mutate them. This does not alter physical database or repository authority. | **APPROVED WITH AUTHORITY-BOUNDARY CONDITION**. |
| `BP-17` | Missing authorization, approval, parent-integrity, or transaction-state evidence fails closed. | **APPROVED**. |
| `BP-18` | Hard Delete, unrestricted Reparenting, large-scale organizational restructuring, bulk structural relocation, and advanced approval workflows outside V1 remain excluded. | **APPROVED / V1 EXCLUSIONS**. |

## Closed Versus Unbound Matters

The following previously open policy principles are closed by this Owner Decision and must not be reopened as general discovery: role separation; Maintainer versus structural-field boundary; independent approval for Create, Deactivate, and Reactivate; requester self-approval prohibition; audit evidence requirement; Hard Delete exclusion; unrestricted Reparenting exclusion; Technical Operator versus Business Approver separation; V1 lifecycle state model; deactivation / reactivation guardrails; hierarchy boundary; and V1 exclusion of nested Location hierarchy.

The following remain execution bindings and are not inferred by this registration:

1. Actual departmental or named steward appointments and entitlement grants.
2. Exact DB/API field catalogue supported by the approved contract.
3. Specific approver and delegate appointments, authority scope, and duration.
4. Warehouse / Plant associations requiring existing-schema compatibility checks.
5. Exact statutory / company records-retention confirmation for BP-14.
6. Technical persistence and transaction contracts required to implement the approved policy.

These bindings do not reopen the approved policy principles. They must be resolved through the applicable authority and implementation-readiness controls before execution authorization.

## Historical Record Treatment

The following earlier artifacts are preserved as historical evidence. Any overlapping pending policy questions are superseded or closed only to the extent explicitly resolved by this Owner Decision; unresolved execution bindings remain open:

- `20_Engineering_Workspace/Checkpoint_Exchange/To_CTO/Business-Owner-Review-Response-FM01-B1-Business-Binding-Decision-20261019-001.md`
- `20_Engineering_Workspace/Checkpoint_Exchange/To_CTO/Business-Owner-Review-Response-FM01-Minimum-Master-Maintenance-Decision-20261018-001.md`
- `20_Engineering_Workspace/Checkpoint_Exchange/To_CTO/Business-Owner-Review-Response-FM01-Minimum-Master-Maintenance-Final-Policy-Closure-20261018-001.md`
- `20_Engineering_Workspace/Checkpoint_Exchange/To_CTO/Business-Owner-Review-Response-FM01-Prospective-Maintenance-Policy-Clarification-20261018-003.md`
- `20_Engineering_Workspace/Checkpoint_Exchange/To_CTO/Business-Owner-Review-Response-FM01-Policy-Binding-Registration-Readback-20261019-001.md`
- `16_Program_Office/ERP2.0-FM01-BUSINESS-OWNER-POLICY-BINDING-REGISTRATION-20261019-001.md`

No prior artifact is deleted, rewritten, or treated as evidence of execution authorization.

## Cross-Module Synchronization

`FM02_CROSS_MODULE_DECISION_REFRESH=PENDING_AFTER_FM01_DESIGN_FREEZE`

This FM-01 Owner Decision is authoritative for FM-01. It must not be applied automatically to FM-02 or used to rewrite an FM-02 baseline. Any FM-02 impact requires the separately governed refresh and review path.

## Boundary and Stop Conditions

- No coding, SQL, database operation, DML, schema implementation, migration, or production data change is authorized.
- No UI, API, runtime, Product-main, repository, Git, or dashboard modification is authorized.
- No test execution, TEST release, implementation assignment, or go-live action is authorized.
- Existing GET-only V1 behavior remains preserved until separate implementation authorization is issued.
- This record registers business policy only; it does not complete named-owner appointment, entitlement grant, technical contract, design freeze, or execution readiness.

## Registration Attribution

Prepared by: Business Owner Review Channel

Registered in: Program Office policy-register record path

Attribution basis: CIO Office Governance V3 / Owner decision supplied in the controlled Business Owner Review request on `2026-10-19`, Asia/Taipei.
