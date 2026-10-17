# FM-02 Sprint 1 — Full Option A Requirement Traceability Matrix

Status: source-reconciled; no live database, production or Sprint 2 claim
Date: 2026-10-17

| Requirement | Domain / rule | Database / migration | API / service | UI | Test / evidence | Classification | Status / decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-01 Item identity | Meaning, specification, lifecycle, intended use and downstream impact govern identity | `item` foundation; 0003 integrity | Foundation create/read/list | Item center reference | Business clarification; deterministic source review | APPROVED_AND_SPECIFIED | Source bounded; final enterprise policy open |
| FR-02 Code assignment | Controlled assignment after identity evidence; retired codes are not silently reused | Unique item code; legacy mapping 0006 | Foundation code generation | Code display only | Source review; live numbering policy not run | APPROVED_AND_SPECIFIED | Numbering policy DECISION_REQUIRED |
| FR-03 Category/lifecycle separation | Category describes item; lifecycle describes usability | 0003 category/lifecycle structures | Foundation lifecycle rules | Status states | 11 deterministic service cases | IMPLEMENTED / BOUNDED | Source-level PASS; formal owner open |
| FR-04 Draft creation/read/search/maintenance | Create is DRAFT-only; read/list are bounded | 0001/0002/0003 | Foundation API/service | `/items` prototype | Prior Sprint evidence | IMPLEMENTED / BOUNDED | Full live API/UI validation not run |
| FR-05 UOM reference | Controlled UOM and item-scoped UOM relationship | 0001 UOM; 0004/0005 item UOM | C2 service | Mock UOM panel | C2 deterministic cases | IMPLEMENTED / BOUNDED | Global UOM policy open |
| FR-06 Specification lineage | Revision, hash, status and effective window are traceable | 0003 specification table | Foundation validation | UI contract only | Source/migration review | IMPLEMENTED / BOUNDED | Enterprise effectivity policy open |
| FR-07 Supplier qualification | Supplier-specific requirement is a relationship, not automatic item identity | 0004 qualification | C2 qualification service | Mock/reference state | Synthetic qualification cases | IMPLEMENTED / BOUNDED | Supplier master ownership open |
| FR-08 Package/customer qualification | Package/customer meaning is explicit and item-bound | 0005 package/customer tables | C2 service | Mock panel | Synthetic scope/fingerprint cases | IMPLEMENTED / BOUNDED | Product/customer variant policy open |
| FR-09 Item-specific conversion | Distinct endpoints, positive factor, effective period, no global fallback | 0005 conversion | Resolve conversion route | Mock conversion state | Positive/negative/overlap cases | IMPLEMENTED / BOUNDED | Precision/rounding/defaults open |
| FR-10 Approval/lifecycle | Active/effective transitions require evidence and actor separation | 0003 approval/events | Foundation lifecycle service | Future workflow states | Approval/idempotency cases | IMPLEMENTED / BOUNDED | Final approver matrix open |
| FR-11 Legacy identifiers | Preserve source dataset/snapshot/locator and zero-row migration gate | 0006 mapping | No live migration endpoint | Unavailable state | Migration contract cases | IMPLEMENTED / BOUNDED | Live mapping acceptance not authorized |
| FR-12 Audit/idempotency/versioning | Durable replay, conflict rejection and optimistic version checks | Unique keys/version fields | C2 service transaction | Not a UI claim | Replay/conflict cases | IMPLEMENTED / BOUNDED | Live target evidence separate |
| FR-13 Product/SKU relationship | Product family, WIP, FG and customer variants remain relationships until policy decides | No new Product/SKU schema authorized | No Product/SKU API authorized | No Product/SKU UI authorized | Business clarification only | APPROVED_AND_SPECIFIED AS DEPENDENCY | DECISION_REQUIRED before implementation |
| FR-14 Cross-module references | BOM, Inventory, Purchasing, Planning, Production, Warehouse, Sales, Costing consume Item state | Dependency references only | No cross-module runtime | No cross-module UI | Roadmap/source references | APPROVED_AND_SPECIFIED AS DEPENDENCY | Other modules excluded from Sprint 1 |
| FR-15 API contract | Stable routes, structured errors, injected connection boundary | Uses existing schema contract | Three C2 routes plus bounded foundation source | No live wiring claim | Static review; dependencies unavailable for full collection | IMPLEMENTED / BOUNDED | Runtime validation HOLD |
| FR-16 UI contract | Loading, empty, error, unavailable and validation states | No UI DB authority | Mock/service boundary explicit | `/items` and C2 panel | Source review; build/browser not run | PROPOSED_NOT_APPROVED | Product/Frontend acceptance required |
| FR-17 Authorization | Separate Engineering, Product, TEST, CTO/CIO and Repository responsibilities | No privilege expansion | No credential loading | No authorization UI claim | Governance/source review | APPROVED_AND_SPECIFIED | Formal appointments not exposed |
| FR-18 Documentation/evidence | Status vocabulary and custody distinguish source, synthetic and live | Migration evidence retained | Evidence boundary documented | UI status labels | Offline plan and review records | APPROVED_AND_SPECIFIED | Post-correction Repository readback pending |
| FR-19 Test coverage | Unit, deterministic, API, UI, migration, negative and live procedures are named | Contract tests for migrations | API test plan | UI/component test plan | C2 offline evidence; dependency gaps visible | APPROVED_AND_SPECIFIED | `SCRIPT_READY`/`HOLD` retained where applicable |
| FR-20 Delivery | Local branch/commit custody; remote push only if authorized | Source paths recorded | N/A | N/A | Git readback; no remote configured | APPROVED_AND_SPECIFIED | `GITHUB_PUSH=BLOCKED_REMOTE_NOT_VERIFIED` |

## Classification rules

- `APPROVED_AND_SPECIFIED` means the requirement or boundary is supported by authoritative business/governance evidence, not that code is complete.
- `IMPLEMENTED` means source exists and was reviewed; it does not mean live runtime acceptance.
- `PROPOSED_NOT_APPROVED` means a design or prototype exists without the required Product/authority decision.
- `EXCLUDED` means outside Sprint 1 and not to be implemented under this record.
- `DECISION_REQUIRED` means a named business or architecture decision must precede expansion.
- `SCRIPT_READY`, `SYNTHETIC_PASS`, `LIVE_PASS`, `HOLD` and `NOT_RUN` remain distinct evidence states.
