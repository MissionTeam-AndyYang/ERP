# Restserver API Development Guide

Date: 2026-05-27
Audience: backend engineer
Baseline: `EWDB_20260526.sql`, `package.restserver.app.create_app()`

## Code Review Status

The baseline restserver code review and runtime verification are accepted for the current scope:

```txt
Scope: restserver application factory, route registration, ORM table alignment, DB schema connectivity, heartbeat smoke.
Decision: passed.
Next scope: V1 read-only aggregation APIs, starting with Warehouse.
```

Reference:

- `docs/backend/API_RUNTIME_RESULT_REVIEW_RESTSERVER_EWDB_20260526_20260527.md`
- `docs/backend/RESTSERVER_DB_RECHECK_20260527.md`
- `docs/engineering/ENGINEER_CONFIRMATION_REQUESTS_20260527.md`

## Current Backend Architecture

| Concern | Current file / pattern |
| --- | --- |
| Flask app factory | `restserver/package/restserver/app.py` |
| Local dev entrypoint | `restserver/package/restserver/run.py` |
| WSGI entrypoint | `restserver/package/restserver/wsgi.py` |
| API prefix | `/api/v1` from `restserver/package/restserver/api/common.py` |
| Shared API runner | `restserver/package/restserver/api/apibase.py` |
| ORM models | `restserver/package/dbwrapper/table.py` |
| DB manager | `package.dbwrapper.dbmgr.CDBMgr` |
| DB connection | `package.dbwrapper.maria.CMaria` |
| V1 contract verifier | `scripts/verify_v1_api_contracts.py` |

## Existing Route Inventory

The current app factory registers 26 blueprints and 70 routes.

Important route groups for V1 dashboard aggregation:

| Domain | Existing route candidates |
| --- | --- |
| Warehouse / Inventory | `/api/v1/inventory`, `/api/v1/inventory/price`, `/api/v1/inventory/statistics`, `/api/v1/inventory/items`, `/api/v1/inventory/months`, `/api/v1/shipwarehouse`, `/api/v1/shipwarehouse/warehouserec` |
| Orders | `/api/v1/sale/productorder`, `/api/v1/sale/shippingorder`, `/api/v1/sale/statistics`, `/api/v1/sale/payment`, `/api/v1/sale/contract`, `/api/v1/sale/arap`, `/api/v1/quotation`, `/api/v1/contract` |
| Production | `/api/v1/workorder`, `/api/v1/workorder/productdata`, `/api/v1/workorder/expecteddata`, `/api/v1/workorder/statistics`, `/api/v1/work/process`, `/api/v1/work/progress`, `/api/v1/plstatistics/*` |
| Quality / Traceability | `/api/v1/batchnumber`, `/api/v1/batchtrace`, `/api/v1/batchtrace/record`, `/api/v1/inventory/record` |
| Planning / APS | `/api/v1/aps/quantity`, `/api/v1/bom/aps`, `/api/v1/bom/tree` |
| Purchasing | `/api/v1/purchase/purchaseorder`, `/api/v1/purchase/goodsreceiptnote`, `/api/v1/purchase/statistics`, `/api/v1/purchase/payment`, `/api/v1/purchase/contract`, `/api/v1/purchase/arap` |
| Finance | `/api/v1/sale/arap`, `/api/v1/sale/payment`, `/api/v1/purchase/arap`, `/api/v1/purchase/payment`, `/api/v1/plstatistics/itemcost` |

## API Implementation Pattern

For a new V1 aggregation API, prefer the existing restserver pattern:

1. Add or extend a blueprint URI file under `restserver/package/restserver/api/*_uri.py`.
2. Add an executor class in the paired domain file under `restserver/package/restserver/api/*.py`.
3. Route handler instantiates a `CAPIBase` subclass and calls `.run()`.
4. Executor returns:

```python
return n_status_code, n_code, str_message, dict_extra_data
```

5. `CAPIBase` wraps the response as:

```json
{
  "code": 0,
  "message": "success",
  "payload": {}
}
```

Frontend `apiGet` and `scripts/verify_v1_api_contracts.py` support direct objects, `{ data: ... }` and the restserver `{ payload: ... }` wrapper. For V1 dashboard endpoints, keep response shape stable inside the unwrapped dashboard object.

## Aggregation API Rules

| Rule | Guidance |
| --- | --- |
| Endpoint naming | Use `/api/v1/{module}/dashboard` for module dashboards. |
| Method | Use `GET` for V1 read-only dashboard APIs. |
| Mutations | Do not add POST/PUT/DELETE dashboard behavior in V1 unless explicitly planned. |
| Aggregation owner | Prefer backend-side aggregation for dashboard contracts. |
| Response stability | Required top-level datasets must remain stable after frontend integration. |
| Missing data | Return empty arrays or neutral/null values rather than failing the full dashboard when optional data is unavailable. |
| Security | Do not expose DB credentials, tokens, raw SQL errors, or confidential customer/supplier values in runtime reports. |
| Timezone | Continue passing `X_TIMEZONE` through `CAPIBase`; document local-date assumptions for dashboard calculations. |

## Required V1 Dashboard Endpoints

| Priority | Endpoint | Required top-level datasets |
| --- | --- | --- |
| 1 | `/api/v1/warehouse/dashboard` | `kpis`, `categorySummaries`, `capacities`, `records`, `risks`, `tasks` |
| 2 | `/api/v1/orders/dashboard` | `summary`, `orders` |
| 3 | `/api/v1/production/dashboard` | `summary`, `orders`, `weekSchedule`, `alerts` |
| 4 | `/api/v1/quality/dashboard` | `summary`, `inspections` |
| 5 | `/api/v1/planning/dashboard` | `summary`, `cases` |
| 6 | `/api/v1/purchasing/dashboard` | `summary`, `items` |
| 7 | `/api/v1/logistics/dashboard` | `summary`, `shipments` |
| 8 | `/api/v1/finance/dashboard` | `summary`, `cases` |
| 9 | `/api/v1/traceability/dashboard` | `summary`, `records` |
| 10 | `/api/v1/rd/dashboard` | `summary`, `projects` |
| 11 | `/api/v1/workforce/dashboard` | `summary`, `cases` |
| 12 | `/api/v1/settings/dashboard` | `summary`, `items` |
| 13 | `/api/v1/dashboard/manager` | `managerSnapshot`, `managerFocusItems`, `managerDecisionItems`, `departmentBlockers`, `todayTasks`, `preOrderPipeline`, `productionLines`, `alertItems`, `productionTrendData`, `oeeTrendData`, `qualityTrendData`, `alertDistributionData`, `moduleShortcuts` |

## Development Checklist

Before implementation:

- Confirm accepted endpoint path.
- Confirm source tables and existing route candidates.
- Confirm missing fields or business decisions.
- Confirm status mapping to frontend `StatusTone`: `success`, `warning`, `danger`, `info`, `neutral`.

During implementation:

- Keep API read-only for V1 dashboards.
- Use SQLAlchemy ORM/session via existing `CDBMgr` pattern.
- Keep helper functions small and module-local unless reused by another endpoint.
- Avoid logging sensitive payloads.
- Keep error handling compatible with `CAPIBase`.

After implementation:

```powershell
python scripts/verify_v1_api_contracts.py --base-url http://127.0.0.1:5000 --module warehouse --output docs/backend/runtime-verification/WAREHOUSE_API_CONTRACT_YYYYMMDD.md
```

Then provide:

- Code commit hash.
- Runtime verification output path.
- Known missing optional fields.
- Any frontend contract changes requested.

## Done Criteria For A V1 API

An API can be marked `backend_implemented` when:

- Endpoint is implemented on `main`.
- Required top-level datasets are present.
- Contract verifier passes for that module.
- Runtime report is stored under `docs/backend/runtime-verification/`.
- Report has no secrets.

It can be marked `frontend_integrated` only after:

- Frontend service consumes real API response.
- Page functional review passes.
- `npm.cmd run lint` and `npm.cmd run build` pass.
