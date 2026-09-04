# Backend API Response - ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-002

## 1. Response Identity

| Field | Value |
| --- | --- |
| Authorization ID | ERP2-CIO-ROUTING-PROCESS-FLOW-SHARED-DEV-DATA-SURFACE-001 |
| Work items | ERP2-ROUTING-PROCESS-FLOW-SHARED-DEV-DATA-SURFACE-001; ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-002 |
| Response date | 2026-09-04 |
| Repository baseline | main |
| Classification | PASS - REAL SHARED DEV DB-BACKED ROUTING API RETEST COMPLETED THROUGH BOUNDED TEST-SUPPORT READONLY SURFACE |

## 2. Assignment Boundary

CTO/CIO authorized bounded non-production Shared DEV Routing / Process Flow acceptance test-support data surface and Backend/API retest.

Backend/API did not apply DDL in this follow-up. Engineering B applied the operational-owner controlled `test_support_...` surface and instructed Backend/API to consume it through the read-only wrapper only.

Backend/API did not create write routes, perform Product write, Routing write, Process Master write, Production credential/data/endpoint access, migration, Source-of-Truth transition, Engineering Pull, Cutover, or Go-Live.

## 3. Engineering B Support Surface Consumed

Engineering B return artifact:

`C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\Checkpoint_Exchange\To_CTO\Engineering-Office-B-Response-ERP2-ROUTING-PROCESS-FLOW-SHARED-DEV-DATA-SURFACE-001-Runtime-and-DB-Support-20260904-001.md`

Applied non-production test-support objects:

| Object | Backend/API use |
| --- | --- |
| `test_support_routing_process_flow_fixture` | Engineering B-owned fixture table; Backend/API does not write to it |
| `test_support_routing_process_step_fixture` | Engineering B-owned step fixture table; Backend/API does not write to it |
| `v_test_support_routing_process_flow_readonly` | Read-only fallback source for Routing Version and ordered step evidence |
| `v_test_support_routing_source_lineage_warnings` | Read-only fallback source for source-lineage / warning evidence |

Engineering B validation evidence:

| Check | Result |
| --- | --- |
| Test-support route count | 1 |
| Test-support step count | 2 |
| Read-only routing/process-flow view rows | 2 |
| Source-lineage / warning view rows | 1 |
| Read-only INSERT negative control | PASS - INSERT denied |
| Existing Product / BOM / spec / inventory counts preserved | PASS |

## 4. Backend/API Bounded Adaptation

Backend/API preserved the accepted public API contract and added a bounded read-only fallback:

1. If formal `product_process` exists, the Routing API uses the existing formal-table ORM path.
2. If formal `product_process` is absent and `v_test_support_routing_process_flow_readonly` exists, the Routing API reads the Engineering B `test_support_...` readonly surface.
3. Fallback responses keep the same response shape and explicitly identify boundary through:
   - `sourceCode = test_support`
   - `warningCode = test_support_only`
   - `processIdentitySourceCode = not_recorded`
   - `standardPerformanceSourceCode = not_recorded`

Updated files:

| File | Change |
| --- | --- |
| `restserver/package/restserver/api/v2/routing.py` | Added read-only test-support fallback query/mapping logic |
| `restserver/package/common/common.py` | Added `ERoutingSourceCode.TEST_SUPPORT` and `ERoutingWarningCode.TEST_SUPPORT_ONLY` |
| `restserver/tests/test_routing_process_flow_api.py` | Added fallback unit test |
| `docs/spec/api/routing.md` | Documented Shared DEV test-support fallback behavior |

## 5. Real Shared DEV DB-Backed Route Evidence

Backend/API used the governed read-only wrapper:

| Item | Value |
| --- | --- |
| Endpoint | `172.20.10.3:3307` |
| Database | `erp2_shared_dev_item_transitem_np` |
| Credential class | `ERP2_SHARED_DEV_ITEM_TRANSITEM_NP_READONLY` |
| Raw secret exposure | 0 |
| Backend DB env mapping | Wrapper-injected values mapped to `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` inside child process only |

Route retest:

| Route | Result | Evidence |
| --- | --- | --- |
| GET `/api/v2/routing/dashboard?effectiveDate=1700000000` | PASS | HTTP 200, `routingVersionCount=1`, `routingVersionIds=["TS-ROUTE-SD-001"]` |
| GET `/api/v2/routing/products/PRD-SD-001/versions?effectiveDate=1700000000` | PASS | HTTP 200, `versions=["TS-ROUTE-SD-001"]` |
| GET `/api/v2/routing/versions/TS-ROUTE-SD-001/steps?effectiveDate=1700000000` | PASS | HTTP 200, `steps=["TS-STEP-SD-001","TS-STEP-SD-002"]` |
| GET `/api/v2/routing/products/PRD-SD-001/current?effectiveDate=1700000000` | PASS | HTTP 200, `steps=["TS-STEP-SD-001","TS-STEP-SD-002"]` |

## 6. Source-Lineage And Warning Behavior

Real DB-backed steps response returned:

| Field | Value |
| --- | --- |
| `sourceLineage.routingVersionSourceCode` | `test_support` |
| `sourceLineage.stepSourceCode` | `test_support` |
| `sourceLineage.processIdentitySourceCode` | `not_recorded` |
| `sourceLineage.recipeReferenceSourceCode` | `product_spec` |
| `sourceLineage.packagingContextSourceCode` | `product_bom_spec` |
| `sourceLineage.resourceEligibilitySourceCode` | `not_recorded` |
| `sourceLineage.routingVersionId` | `TS-ROUTE-SD-001` |

Warning codes returned:

- `test_support_only`
- `resource_eligibility_not_governed`
- `missing_process_master`
- `missing_standard_performance`

This correctly preserves the non-production support-surface boundary and does not imply target Production schema, governed Process Master, governed standard performance, or resource eligibility authority.

## 7. Product / WIP Coverage

| Coverage | Result |
| --- | --- |
| Product | PASS; support surface provides Product route for `PRD-SD-001` |
| WIP | NOT PRESENT IN ENGINEERING B SUPPORT SURFACE; no Backend/API failure |

Engineering B's applied support surface contains one route whose product context is `PRD-SD-001` and two ordered steps: `MAT-SD-001 -> INP-SD-001`, then `INP-SD-001 -> PRD-SD-001`. This provides WIP visibility as an intermediate step reference, but not a standalone WIP Routing Version route.

## 8. No Silent Mock Fallback

No frontend mock data was used.

Evidence:

1. Backend/API route probe was executed inside the read-only Shared DEV wrapper child process.
2. The route output changed from the earlier missing `product_process` DB error to successful responses only after Engineering B applied `test_support_...` DB objects.
3. Returned identifiers match real Shared DEV support-surface rows:
   - `TS-ROUTE-SD-001`
   - `TS-STEP-SD-001`
   - `TS-STEP-SD-002`

## 9. Read-Only Negative Controls

| Control | Result |
| --- | --- |
| POST `/api/v2/routing/dashboard` | PASS, HTTP 405 |
| Engineering B read-only INSERT negative control | PASS, INSERT denied |

No Routing write, Product write, or Process Master write route was introduced.

## 10. Automated Test Evidence

| Test suite | Result |
| --- | --- |
| `restserver/tests/test_routing_process_flow_api.py` | PASS, 7 tests |
| `restserver/tests` | PASS, 93 tests |

The new Routing fallback test verifies the accepted response contract when formal Routing tables are absent and the Shared DEV `test_support_...` readonly views are present.

## 11. Disposition

ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-002 is complete from Backend/API side.

Result:

`PASS - REAL SHARED DEV DB-BACKED ROUTING API RETEST COMPLETED THROUGH BOUNDED NON-PRODUCTION TEST-SUPPORT READONLY SURFACE`

Residual note:

The current Shared DEV support surface is sufficient for bounded Product route acceptance evidence only. Standalone WIP Routing Version coverage remains absent because Engineering B did not include a WIP route row in the support surface. This does not block the Product Evidence retest, but should be added if CTO/CIO later requires explicit WIP route acceptance evidence.

## 12. Boundary Confirmation

Backend/API did not apply DDL in this follow-up, did not create or modify Shared DEV tables, did not expose raw secrets, did not use Production credentials, did not use Production data, did not perform Product write, Routing write, Process Master write, migration, Engineering Pull, Source-of-Truth transition, Cutover, or Go-Live activity.
