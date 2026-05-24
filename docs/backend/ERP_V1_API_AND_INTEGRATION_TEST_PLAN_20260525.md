# ERP V1 API And Integration Test Plan

Date: 2026-05-25
Purpose: Define how to validate backend API implementation, frontend integration and system-level readiness for ERP V1.

## Test Scope

This plan covers:

- API contract tests for V1 aggregation endpoints.
- Frontend integration tests after each API is implemented.
- Cross-module functional checks for ODM food processing workflows.
- System-level smoke, performance and regression checks.

This plan does not replace backend unit tests owned by the engineer, but it defines the acceptance criteria needed before the frontend switches from mock fallback to real API data.

## Test Levels

| Level | Owner | Purpose | Tool / evidence |
| --- | --- | --- | --- |
| Unit test | Backend engineer / Codex review | Validate service functions, serializers and calculations. | Backend test output or engineer report. |
| API contract test | Engineer runs, Codex reviews | Confirm endpoint, status code, JSON and required top-level datasets. | `scripts/verify_v1_api_contracts.py` report. |
| Functional test | Codex + user review | Confirm each page supports the agreed business concerns. | Acceptance checklist and screenshots if needed. |
| Integration test | Codex + engineer | Confirm frontend consumes real API data without schema mismatch. | Frontend page run, browser check, console/network review. |
| System smoke test | Codex + engineer | Confirm critical pages build and load together. | `npm.cmd run lint`, `npm.cmd run build`, page smoke results. |
| Performance/stress test | Engineer + Codex review | Confirm acceptable response time and stability under expected load. | Backend performance report. |

## Core API Contract Targets

| Priority | Module | Endpoint | Required top-level datasets |
| --- | --- | --- | --- |
| 1 | Warehouse | `GET /api/v1/warehouse/dashboard` | `kpis`, `categorySummaries`, `capacities`, `records`, `risks`, `tasks` |
| 2 | Orders | `GET /api/v1/orders/dashboard` | `summary`, `orders` |
| 3 | Production | `GET /api/v1/production/dashboard` | `summary`, `orders`, `weekSchedule`, `alerts` |
| 4 | Quality | `GET /api/v1/quality/dashboard` | `summary`, `inspections` |
| 5 | Planning / APS | `GET /api/v1/planning/dashboard` | `summary`, `cases` |
| 6 | Purchasing | `GET /api/v1/purchasing/dashboard` | `summary`, `items` |
| 7 | Logistics | `GET /api/v1/logistics/dashboard` | `summary`, `shipments` |
| 8 | Finance | `GET /api/v1/finance/dashboard` | `summary`, `cases` |
| 9 | Traceability | `GET /api/v1/traceability/dashboard` | `summary`, `records` |
| 10 | R&D / Costing | `GET /api/v1/rd/dashboard` | `summary`, `projects` |
| 11 | Workforce | `GET /api/v1/workforce/dashboard` | `summary`, `cases` |
| 12 | Settings / Master Data | `GET /api/v1/settings/dashboard` | `summary`, `items` |
| 13 | Manager Dashboard | `GET /api/v1/dashboard/manager` | `managerSnapshot`, `managerFocusItems`, `managerDecisionItems`, `departmentBlockers`, `todayTasks`, `preOrderPipeline`, `productionLines`, `alertItems`, `productionTrendData`, `oeeTrendData`, `qualityTrendData`, `alertDistributionData`, `moduleShortcuts` |

## API Contract Verification Procedure

For each implemented module:

1. Start `restserver`.
2. Run the verification script for the module.
3. Save markdown output under `docs/backend/runtime-verification/`.
4. Confirm the report contains no credentials, customer secrets or supplier secrets.
5. Share or commit the report for Codex review.
6. Review the result with `docs/backend/API_RUNTIME_RESULT_REVIEW_TEMPLATE_20260525.md`.

Example:

```powershell
python scripts/verify_v1_api_contracts.py --base-url http://127.0.0.1:5000 --module warehouse --output docs/backend/runtime-verification/WAREHOUSE_API_CONTRACT_20260525.md
```

Expected result:

- HTTP status is 2xx.
- Response is valid JSON.
- Required top-level datasets match the current frontend service-layer contract.
- Dataset field names match the frontend API spec or documented mapping.

## Frontend Integration Procedure

After an API contract passes:

1. Confirm frontend service endpoint path matches backend route.
2. Run frontend lint and build:

```powershell
npm.cmd run lint
npm.cmd run build
```

3. Start frontend app and open the relevant page.
4. Confirm data source switches from mock fallback to API where supported.
5. Check browser console for schema, hydration or rendering errors.
6. Verify page-specific acceptance criteria from `docs/frontend/ERP_V1_FRONTEND_ACCEPTANCE_CHECKLIST_20260525.md`.
7. Record the page decision with `docs/frontend/ERP_V1_FRONTEND_PAGE_REVIEW_TEMPLATE_20260525.md`.

## Functional Test Cases

### Warehouse

| Case | Expected behavior |
| --- | --- |
| Inventory value by category exists | Page shows category totals for raw material, supplies, film/roll, WIP and finished goods. |
| Capacity data exists | Page shows used and available pallet positions by warehouse/storage area. |
| Long-turnover item exists | Risk alert identifies turnover over one month. |
| Shelf-life risk exists | Risk alert identifies less than one-third shelf life remaining, excluding supplies and film/roll. |
| Safety-stock shortage exists | Risk alert identifies item below safety level. |
| Pending inbound/outbound exists | Today's unprocessed inbound/outbound tasks are shown. |

### Orders

| Case | Expected behavior |
| --- | --- |
| Order has delivery risk | Order card prioritizes fulfillment risk and due date. |
| Order has material shortage | Order exposes planning or purchasing blocker. |
| Order has quality/shipment hold | Order exposes downstream blocker. |
| Order has margin/payment data | Margin and collection status show as secondary management signals. |

### Production

| Case | Expected behavior |
| --- | --- |
| Weekly schedule exists | Page shows work orders by date and production line. |
| Material shortage exists | Work order shows material readiness warning. |
| Staff shortage exists | Work order shows staff readiness warning. |
| Quality inspection pending | Work order shows quality status and blocker if applicable. |
| Efficiency data exists | Page shows production efficiency, loss and labor cost indicators. |

### Quality

| Case | Expected behavior |
| --- | --- |
| Receiving inspection pending | Inspection queue shows material waiting for release. |
| Production inspection has defects | Quality item shows defect count/rate and decision status. |
| Shipment inspection blocks delivery | Page clearly marks shipment blocker. |
| Missing document exists | Document status highlights missing or incomplete evidence. |

### Planning / APS

| Case | Expected behavior |
| --- | --- |
| Order can be produced | Case decision shows executable status. |
| Material shortage blocks order | Case shows shortage item, required date and suggested action. |
| Capacity shortage blocks order | Case shows bottleneck process/line and required hours. |
| Suggested work orders exist | Page shows planned work-order suggestions. |

### Purchasing

| Case | Expected behavior |
| --- | --- |
| Supplier quote pending | Page shows quote/contract item requiring purchasing action. |
| Purchase order delayed | Page marks arrival risk. |
| Receiving completed | Page links receiving status to warehouse/quality flow. |
| Price variance exists | Page shows variance against contract or baseline price. |

### Logistics

| Case | Expected behavior |
| --- | --- |
| Shipment not ready | Page shows missing inventory, quality, document or dispatch blocker. |
| Shipment dispatched | Page shows carrier/dispatch status. |
| POD missing | Page shows proof-of-delivery as pending. |
| Billing blocked | Page links shipment completion to finance readiness. |

### Finance

| Case | Expected behavior |
| --- | --- |
| Margin below expectation | Page shows margin risk. |
| Cost variance exists | Page identifies material, production or logistics variance. |
| AR overdue | Page highlights collection risk. |
| AP due | Page highlights payment obligation. |

### R&D / Costing

| Case | Expected behavior |
| --- | --- |
| Development request exists | Page shows project stage and owner. |
| BOM version pending approval | Page shows version/control state. |
| Costing ready | Page shows cost result for quotation support. |
| Nutrition label pending | Page shows nutrition label readiness. |

### Workforce

| Case | Expected behavior |
| --- | --- |
| Staff shortage exists | Page identifies line/date shortage. |
| Skill gap exists | Page identifies missing skill or certification. |
| Shift assignment exists | Page connects staffing to production schedule. |

### Traceability

| Case | Expected behavior |
| --- | --- |
| Batch search result exists | Page can show batch record and status. |
| Upstream material exists | Page links material lots. |
| Downstream shipment exists | Page links customer/order/shipment. |
| Recall scope exists | Page can show affected scope. |

## System-Level Tests

| Test | Acceptance criteria |
| --- | --- |
| Frontend lint | `npm.cmd run lint` passes. |
| Frontend build | `npm.cmd run build` passes. |
| Core page smoke | `/`, `/warehouse`, `/orders`, `/production`, `/quality`, `/planning`, `/purchasing`, `/logistics`, `/finance`, `/rd`, `/workforce`, `/traceability`, `/settings` load without fatal error. |
| API fallback | If backend endpoint is unavailable, page remains usable with mock fallback. |
| API success | If backend endpoint is available, page consumes API response without schema errors. |
| Responsive smoke | Desktop and mobile viewports do not show overlapping text or broken layout. |

## Performance And Stress Targets

Initial targets for V1 read-only aggregation APIs:

| Metric | Target |
| --- | --- |
| Single dashboard response time | p95 under 1.5 seconds on staging-like data volume. |
| Manager dashboard response time | p95 under 2.5 seconds after module APIs are stable. |
| Error rate | Under 1 percent during normal smoke load. |
| Payload size | Keep response compact enough for dashboard use; avoid returning raw transaction dumps. |
| Concurrency smoke | 20 concurrent dashboard requests should not produce server errors. |

If the engineer uses a different performance tool, the report should still include endpoint, request count, concurrency, p50/p95 latency, error rate and environment notes.

## Evidence Handling

Runtime/test evidence should be stored under:

```txt
docs/backend/runtime-verification/
```

Review templates:

```txt
docs/backend/API_RUNTIME_RESULT_REVIEW_TEMPLATE_20260525.md
docs/frontend/ERP_V1_FRONTEND_PAGE_REVIEW_TEMPLATE_20260525.md
```

Before committing evidence:

1. Remove DB credentials.
2. Remove customer/supplier confidential values if unnecessary.
3. Keep endpoint, status, required dataset checks and error messages.
4. Prefer one report per module or per verification run.

## Exit Criteria For Backend-to-Frontend API Integration

A module can be marked `frontend_integrated` in the tracker when:

- API contract verification passes.
- Frontend service consumes real API response.
- Page functional test cases pass.
- Lint and build pass.
- No blocking schema mismatch remains.
- Any known business-data limitation is documented in the tracker.
