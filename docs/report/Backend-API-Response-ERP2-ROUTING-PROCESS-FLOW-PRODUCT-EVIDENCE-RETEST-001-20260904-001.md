# Backend API Response - ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-001

## 1. Response Identity

| Field | Value |
| --- | --- |
| Work item | ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-001 |
| Response date | 2026-09-04 |
| Repository baseline | main |
| Repository HEAD at retest | 0dd51db |
| Related implementation commit | cdc6a61 Implement routing process flow read-only API |
| Classification | SAFE STOP - SHARED DEV ROUTING DATA SURFACE / CREDENTIAL MATERIAL NOT READY |

## 2. Scope

This retest attempted to validate the implemented Routing / Process Flow read-only API against the bounded non-production Shared DEV database surface.

Target APIs:

| API | Method | Scope |
| --- | --- | --- |
| /api/v2/routing/dashboard | GET | Routing Version summary |
| /api/v2/routing/products/{item_no}/versions | GET | Product / WIP Routing Version list |
| /api/v2/routing/versions/{routing_version_id}/steps | GET | Ordered Routing steps |
| /api/v2/routing/products/{item_no}/current | GET | Current effective Routing |

## 3. Local Backend Verification

| Verification item | Result | Evidence |
| --- | --- | --- |
| Routing API pytest | PASS | `restserver/tests/test_routing_process_flow_api.py`: 6 passed |
| Full backend pytest suite | PASS | `restserver/tests`: 92 passed |
| Read-only negative control | PASS | POST to `/api/v2/routing/dashboard` is covered by pytest and returns 405 |
| API route registration | PASS | `routing_v2` is registered in `restserver/package/restserver/app.py` |

The local automated tests cover Product / WIP resolution, Routing Version state selection, step ordering, stable step identity, process reference mapping, recipe / packaging references, standard performance evidence, warning codes, source lineage, current version selection, missing step warning behavior, and write-route rejection.

## 4. Shared DEV Runtime Check

| Check | Result | Evidence |
| --- | --- | --- |
| Shared DEV endpoint TCP | PASS | `172.20.10.3:3307` accepted TCP connection |
| Engineering B runtime coordination | READY WITH DATA-SURFACE CONDITION | Engineering B evidence: `ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-001/shared_dev_runtime_retest_coordination_evidence_20260904.md` |
| Read-only credential wrapper execution | BLOCKED | Wrapper reported bounded non-production credential material not found for `ERP2_SHARED_DEV_ITEM_TRANSITEM_NP_READONLY` |
| Direct Routing / Process / Flow table surface | NOT READY | Engineering B evidence states no direct table name matching `routing`, `process`, `flow`, or `process_master` is present |

## 5. Data Surface Finding

The implemented Routing API reads the accepted Routing source model:

| Required source | Purpose |
| --- | --- |
| `product_process` | Routing Version evidence |
| `process_flow` | ordered Routing Step evidence |
| `process` | reusable process master evidence |
| `process_capacity` | standard performance / capacity evidence |
| `product` | finished goods item resolution |
| `inproduct` | WIP item resolution |
| `product_spec` | recipe reference evidence |
| `product_bom_spec` | packaging reference evidence |

Engineering B's current Shared DEV coordination evidence lists the active fixture tables and explicitly states that no direct table name matching `routing`, `process`, `flow`, or `process_master` is present. Therefore, the current Shared DEV data surface cannot complete a true DB-backed acceptance smoke for the four Routing APIs without an additional accepted Routing / Process Flow fixture or schema surface.

## 6. No Silent Mock Fallback

Backend/API did not use frontend mock data for this retest. The retest relied on local backend pytest fixtures for implementation verification and attempted to use the Engineering B Shared DEV wrapper for real DB validation.

Because the Shared DEV credential material is currently unavailable and the Routing source tables are not present in the coordinated Shared DEV fixture evidence, the real DB-backed no-silent-mock-fallback smoke remains pending. This is classified as a Shared DEV environment / fixture readiness blocker, not a confirmed backend Routing API logic defect.

## 7. Disposition

| Item | Status | Note |
| --- | --- | --- |
| Backend implementation | PASS | Existing read-only implementation remains valid under automated tests |
| API / code contract | PASS | `docs/spec/api/routing.md` matches implemented read-only endpoints |
| DB-backed acceptance retest | BLOCKED | Shared DEV Routing source data surface and current wrapper credential material are not ready |
| Bounded remediation | NOT EXECUTED | Creating or applying missing Routing / Process Flow source tables would require explicit authorized fixture/schema action |

## 8. Required Next Action

Engineering A / Engineering B should provide one of the following before Backend/API reruns the DB-backed acceptance retest:

1. Restore the bounded read-only credential material for `ERP2_SHARED_DEV_ITEM_TRANSITEM_NP_READONLY`.
2. Provide an accepted non-production Routing / Process Flow fixture containing the required source tables and representative Product / WIP rows.
3. If the current Shared DEV model should not use direct `product_process`, `process_flow`, `process`, and `process_capacity` tables, provide the accepted mapping/adapter source-of-evidence so Backend/API can adjust the read-only data access without inventing schema.

Until one of these is complete, the correct status is Safe Stop before real DB-backed Routing acceptance completion.

## 9. Boundary Confirmation

Backend/API did not create or modify Shared DEV tables, did not use Production credentials, did not use Production data, did not perform Product write, Routing write, Process Master write, Production data/action, migration, Engineering Pull, Source-of-Truth transition, Cutover, or Go-Live activity.
