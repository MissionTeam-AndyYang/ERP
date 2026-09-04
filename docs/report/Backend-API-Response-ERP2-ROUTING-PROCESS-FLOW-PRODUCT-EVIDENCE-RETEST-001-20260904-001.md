# Backend API Response - ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-001

## 1. Response Identity

| Field | Value |
| --- | --- |
| Work item | ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-001 |
| Response date | 2026-09-04 |
| Repository baseline | main |
| Repository HEAD at retest | 0dd51db |
| Related implementation commit | cdc6a61 Implement routing process flow read-only API |
| Classification | SAFE STOP - SHARED DEV ROUTING DATA SURFACE NOT READY |

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
| Read-only credential wrapper execution | PASS | Wrapper executed successfully when invoked with the Phase1 workspace root; raw secret exposure remained 0 |
| Direct Routing / Process / Flow table surface | NOT READY | Shared DEV contains `product`, `inproduct`, `product_spec`, and `product_bom_spec`, but does not contain `product_process`, `process_flow`, `process`, or `process_capacity` |

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

Engineering B's current Shared DEV coordination evidence lists the active fixture tables and explicitly states that no direct table name matching `routing`, `process`, `flow`, or `process_master` is present. Backend/API also verified the accepted Routing source tables directly through the governed read-only wrapper:

| Table | Shared DEV status |
| --- | --- |
| `product` | PRESENT |
| `inproduct` | PRESENT |
| `product_spec` | PRESENT |
| `product_bom_spec` | PRESENT |
| `product_process` | MISSING |
| `process_flow` | MISSING |
| `process` | MISSING |
| `process_capacity` | MISSING |

The present tables can support adjacent Product / WIP / BOM context. They cannot responsibly demonstrate the accepted Routing Product contract because they do not provide Routing Version identity, ordered step identity, reusable Process Master identity, or governed standard-performance evidence.

Therefore, the current Shared DEV data surface cannot complete a true DB-backed acceptance smoke for the four Routing APIs without an additional accepted Routing / Process Flow fixture, schema surface, or officially approved mapping source.

## 6. No Silent Mock Fallback

Backend/API did not use frontend mock data for this retest. The retest relied on local backend pytest fixtures for implementation verification and attempted to use the Engineering B Shared DEV wrapper for real DB validation.

Because the Routing source tables are not present in the coordinated Shared DEV fixture evidence, the real DB-backed no-silent-mock-fallback smoke remains pending. This is classified as a Shared DEV data-surface readiness blocker, not a confirmed backend Routing API logic defect.

## 7. Disposition

| Item | Status | Note |
| --- | --- | --- |
| Backend implementation | PASS | Existing read-only implementation remains valid under automated tests |
| API / code contract | PASS | `docs/spec/api/routing.md` matches implemented read-only endpoints |
| DB-backed acceptance retest | BLOCKED | Shared DEV Routing source data surface is not ready |
| Bounded remediation | NOT EXECUTED | Creating or applying missing Routing / Process Flow source tables would require explicit authorized fixture/schema action |

## 8. Required Next Action

Engineering A / Engineering B should provide one of the following before Backend/API reruns the DB-backed acceptance retest:

1. Provide an accepted non-production Routing / Process Flow fixture containing the required source tables and representative Product / WIP rows.
2. If the current Shared DEV model should not use direct `product_process`, `process_flow`, `process`, and `process_capacity` tables, provide the accepted mapping/adapter source-of-evidence so Backend/API can adjust the read-only data access without inventing schema.

Until one of these is complete, the correct status is Safe Stop before real DB-backed Routing acceptance completion.

## 9. Backend/API Disposition For CTO-To-CIO Consolidation

Backend/API cannot responsibly demonstrate the accepted Routing Product contract using only the current Shared DEV physical structures plus non-material mapping/adapter/config/test-support treatment.

Reason:

| Accepted contract area | Required evidence | Current Shared DEV support |
| --- | --- | --- |
| Routing Version identity | `product_process.no`, `item_no`, `version`, `date` | Missing |
| Ordered Routing Step identity | `process_flow.no`, `product_process_no`, `order` | Missing |
| Process / stage identity | `process.oneProcess`, `process.secProcess`, `process.comment` | Missing |
| Governed standard performance | `process_capacity.hourlyOutput`, `laborCount`, `unit`, `date` | Missing |
| Product / WIP item context | `product`, `inproduct` | Present |
| Recipe / packaging context | `product_spec`, `product_bom_spec` | Present |

The present Product / WIP / BOM tables are adjacent context only. Mapping them into Routing Version and ordered Process Flow would invent process sequence and Process Master evidence that is not physically available in the current Shared DEV fixture. That would materially change the source-of-evidence model and would exceed the bounded retest authority.

Proposed schema/data-surface change:

- Add or restore the accepted non-production Routing / Process Flow source surface: `product_process`, `process_flow`, `process`, `process_capacity`.
- Seed representative Product and WIP routing rows, including at least one effective version, one future or historical version, ordered process steps, process master labels/codes, and standard performance evidence.
- Preserve read-only Backend/API participant access after fixture application.

Affected domains:

- Routing / Process Flow read-only API.
- Product / WIP manufacturing definition context.
- Process Master read-only evidence.
- Capacity / standard performance read-only evidence.

Compatibility impact:

- No breaking change is required for the already implemented API contract.
- The current code and API document already target the accepted source tables.
- The change is a Shared DEV fixture/schema-surface readiness action, not an API shape change.

Recommendation:

- CTO/CIO should route the data-surface gap to the authorized Engineering A / Engineering B fixture or schema path.
- Backend/API should rerun the real DB-backed acceptance test only after the required Routing / Process Flow data surface is present under governed non-production read-only access.

## 10. Boundary Confirmation

Backend/API did not create or modify Shared DEV tables, did not use Production credentials, did not use Production data, did not perform Product write, Routing write, Process Master write, Production data/action, migration, Engineering Pull, Source-of-Truth transition, Cutover, or Go-Live activity.
