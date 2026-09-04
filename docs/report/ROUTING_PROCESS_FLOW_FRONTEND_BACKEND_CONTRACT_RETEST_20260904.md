# Routing / Process Flow Frontend Backend Contract Retest

- Work item: ERP2-ROUTING-PROCESS-FLOW-RO-EXEC-001-UX-002
- Backend reference: ERP2-ROUTING-PROCESS-FLOW-RO-EXEC-001-BE-001
- Date: 2026-09-04
- Scope: Frontend contract alignment and non-production read-only retest

## Retest Purpose

Backend Routing / Process Flow read-only API has been implemented in `main`. This retest verifies that the `/routing` frontend no longer uses the earlier candidate route names and is aligned to the confirmed Backend API contract.

## Confirmed API Routes

Frontend now calls the confirmed read-only route family:

- `GET /api/v2/routing/dashboard`
- `GET /api/v2/routing/products/{item_no}/versions`
- `GET /api/v2/routing/versions/{routing_version_id}/steps`
- `GET /api/v2/routing/products/{item_no}/current`

The earlier candidate route family is no longer referenced by the Routing frontend, planned screen list, or frontend implementation report.

## Frontend Contract Alignment

Updated files:

- `src/services/routing-api.ts`
- `src/types/routing.ts`
- `src/mock/routing.ts`
- `docs/spec/api-proposal/planned_screen_list_naming.md`
- `docs/report/ROUTING_PROCESS_FLOW_FRONTEND_READONLY_IMPLEMENTATION_REPORT_20260904.md`

Frontend mapping now supports the confirmed Backend response shape:

- Dashboard list field: `routingVersions`
- Routing identity: `routingVersionId`
- Item category enum: `itemCategory`
- Detail payload root: `routingVersion`
- Ordered steps: `steps`
- Step order: `stepOrder`
- Recipe reference: `recipeReference`
- Packaging context: `packagingContext`
- Resource eligibility: `resourceEligibility`
- Standard performance: `standardPerformance`
- Structured source lineage: `sourceLineage`
- Controlled warnings: `missing_steps`, `missing_item_master`, `missing_process_master`, `packaging_context_not_governed`, `resource_eligibility_not_governed`

API mode continues to avoid silent mock fallback. Mock data is returned only when the user explicitly switches the Routing screen data source to `mock`.

## Validation

| Check | Result |
|---|---|
| `npm run lint` | PASS |
| `npm run build` | PASS |
| `/routing` generated in Next build | PASS |
| `python -m pytest restserver/tests/test_routing_process_flow_api.py -q` | PASS, 6 passed |
| `npm run test` | NOT AVAILABLE |
| Earlier candidate route reference check | PASS, no remaining implementation references |
| Routing write-control inspection | PASS, no create/edit/delete/approve/release/schedule/dispatch controls added |

The project still has no frontend `test` script in `package.json`; this remains `FRONTEND_TEST_SCRIPT_STANDARDIZATION_GAP`.

## Real Backend Data-Surface Status

Full Shared DEV DB-backed Routing smoke remains blocked by fixture/schema readiness, not by the frontend contract alignment.

Backend report indicates the Shared DEV database currently lacks Routing source tables such as `product_process` / routing source table fixtures. The Backend API code and targeted pytest coverage passed, but real DB-backed data validation depends on those source tables becoming available in the shared environment.

## Final Classification

**ROUTING_PROCESS_FLOW_FRONTEND_CONTRACT_ALIGNED_PASS_SHARED_DEV_FIXTURE_TABLE_PENDING**

The Routing / Process Flow frontend is aligned to the confirmed Backend route family and response fields, API/mock separation is preserved, no write controls were added, and lint/build/targeted Backend tests passed. Remaining validation is limited to Shared DEV routing source table fixture readiness.
