# ERP 2.0 Engineer Confirmation Requests

Date: 2026-05-27
Purpose: Consolidate scattered engineer-facing confirmation items into one communication document.

## Current Accepted Baseline

| Area | Status | Reference |
| --- | --- | --- |
| Git branch | Use GitHub `main` as shared source of truth |  |
| Database baseline | `EWDB_20260526.sql` | `docs/database/EWDB_20260526.sql` |
| Workflow baseline | `EWDB_20260522_WORKFLOW.md` until replaced | `docs/database/EWDB_20260522_WORKFLOW.md` |
| Backend runtime baseline | Passed | `docs/backend/API_RUNTIME_RESULT_REVIEW_RESTSERVER_EWDB_20260526_20260527.md` |
| Restserver architecture | Flask `create_app()` + `run.py` + `wsgi.py` | `restserver/package/restserver/app.py` |
| Frontend service layer | Ready with mock fallback | `src/services/*`, `src/hooks/*` |
| First backend API target | Warehouse read-only aggregation API | `GET /api/v1/warehouse/dashboard` |

## Confirmed Runtime Result

Engineer DB/runtime verification has passed:

| Check | Result |
| --- | --- |
| `restserver.ok` | `true` |
| ORM table count | 79 |
| Missing required ORM tables | none |
| Blueprint count | 26 |
| Route count | 70 |
| `/heartbeat` | HTTP 200 |
| `database.ok` | `true` |
| DB table count | 79 |
| DB foreign key count | 118 |
| DB unique key count | 73 |
| Missing required DB tables | none |

Decision: baseline restserver + EWDB 20260526 runtime verification is accepted.

## Immediate Engineer Action

Please start with the first V1 read-only aggregation API:

```txt
GET /api/v1/warehouse/dashboard
```

Required frontend runtime datasets:

```txt
kpis
categorySummaries
capacities
records
risks
tasks
```

Verification command after implementation:

```powershell
python scripts/verify_v1_api_contracts.py --base-url http://127.0.0.1:5000 --module warehouse --output docs/backend/runtime-verification/WAREHOUSE_API_CONTRACT_YYYYMMDD.md
```

## Open Confirmation Items

### A. Baseline And Runtime

| ID | Confirmation needed | Suggested response |
| --- | --- | --- |
| A1 | Confirm `EWDB_20260526.sql` is the active DB baseline for subsequent API work. | yes / no / replacement file |
| A2 | Confirm `EWDB_20260522_WORKFLOW.md` remains the active workflow baseline until a newer workflow file is provided. | yes / no / replacement file |
| A3 | Confirm runtime verification should continue using `package.restserver.app.create_app()` / `wsgi.py`, not the removed `restserver.py`. | yes / no |
| A4 | Confirm whether passwordless DB connection strings must be supported. Current credentialed `.env` path works; passwordless config may produce incomplete URL in `CMaria.gen_connection_str()`. | credentialed only / support passwordless |

### B. Warehouse API

| ID | Confirmation needed | Why it matters |
| --- | --- | --- |
| W1 | Which existing backend endpoints/tables should source inventory quantity, reserved quantity and available quantity? | Required for `records`, `kpis`, `categorySummaries`. |
| W2 | Where are warehouse/storage location and pallet capacity stored? | Required for `capacities`. |
| W3 | Does inventory distinguish on-hand, reserved, quality-hold and available quantity? | Required for value/space/risk accuracy. |
| W4 | Where is safety stock stored? | Required for low-safety-stock risk. |
| W5 | What cost method should be used for inventory value? | Required for category inventory value and margin analysis. |
| W6 | Where is material/product inspection release or hold status stored? | Required for quality-hold risk and shipment/inventory blockers. |
| W7 | Can batch expiry and shelf-life be returned from existing tables/endpoints? | Required for shelf-life warning. |
| W8 | Should aggregation be backend-side, frontend-side, or temporary hybrid? | Recommended: backend-side for stable dashboard contracts. |

### C. Module API Mapping

| Priority | Module | Endpoint | Engineer confirmation needed |
| --- | --- | --- | --- |
| 1 | Warehouse | `/api/v1/warehouse/dashboard` | Source routes/tables, missing fields, aggregation owner. |
| 2 | Orders | `/api/v1/orders/dashboard` | Sale/order/quotation/contract mapping; delivery risk and collection status source. |
| 3 | Production | `/api/v1/production/dashboard` | Workorder/MES source, week schedule derivation, quality signal source. |
| 4 | Quality | `/api/v1/quality/dashboard` | Whether dedicated quality route/model is required; inspection/release/hold source. |
| 5 | Planning / APS | `/api/v1/planning/dashboard` | APS quantity, BOM expansion, material shortage and capacity calculation source. |
| 6 | Purchasing | `/api/v1/purchasing/dashboard` | Development-stage supplier quote/contract vs mass-production purchasing distinction. |
| 7 | Logistics | `/api/v1/logistics/dashboard` | Dispatch, POD, cold-chain and billing-readiness source. |
| 8 | Finance | `/api/v1/finance/dashboard` | AR/AP source of truth, estimated/actual margin and cost variance logic. |
| 9 | Traceability | `/api/v1/traceability/dashboard` | Batchtrace relationships, upstream/downstream chain and recall scope. |
| 10 | R&D / Costing | `/api/v1/rd/dashboard` | Product development project, sample status, BOM costing, nutrition label source. |
| 11 | Workforce | `/api/v1/workforce/dashboard` | Employee, shift, skill and certification source tables. |
| 12 | Settings / Master Data | `/api/v1/settings/dashboard` | Role/permission, localization, audit and master-data health source. |
| 13 | Manager Dashboard | `/api/v1/dashboard/manager` | Whether backend should aggregate module APIs after core modules are stable. |

### D. Support Pages

These are lower priority than core V1 APIs, but the frontend already has mock-fallback service endpoints.

| Support page | Endpoint | Confirmation needed |
| --- | --- | --- |
| Items / Item Master | `/api/v1/items/dashboard` | Whether product/material/goods/transitems/inventory can compose item master dashboard. |
| BOM / Formula | `/api/v1/bom/dashboard` | BOM versioning and approval fields. |
| Batches | `/api/v1/batches/dashboard` | Batch expiry, hold/release and lifecycle fields. |
| AI Center | `/api/v1/ai/dashboard` | Whether this remains placeholder/later phase. |

## Engineer Response Template

Please respond module by module:

```txt
Module:
Accepted endpoint:
Existing backend source endpoints:
Source tables:
Missing DB/table/field:
Aggregation owner: backend/frontend/temporary hybrid
Status mapping notes:
Security/permission notes:
Implementation blocker:
Expected implementation order:
Runtime verification output path:
```

For Warehouse specifically:

```txt
Warehouse endpoint accepted:
Inventory quantity source:
Reserved/available quantity source:
Warehouse capacity source:
Safety stock source:
Inventory value method:
Quality hold/release source:
Expiry/shelf-life source:
Backend aggregation plan:
Expected runtime verification file:
```

## Source Documents

| Document | Purpose |
| --- | --- |
| `docs/backend/API_IMPLEMENTATION_TRACKER_20260524.md` | Current API status and implementation priority. |
| `docs/backend/API_IMPLEMENTATION_HANDOFF_TO_ENGINEER_20260524.md` | Original backend API handoff. |
| `docs/backend/FRONTEND_API_ENDPOINT_INVENTORY_AND_BACKEND_GAP_20260524.md` | Endpoint inventory, backend candidates and gap classes. |
| `docs/backend/API_CONTRACT_VERIFICATION_GUIDE_20260524.md` | How to run contract verification. |
| `docs/backend/ERP_V1_API_AND_INTEGRATION_TEST_PLAN_20260525.md` | API/integration/system test plan. |
| `docs/backend/API_RUNTIME_RESULT_REVIEW_RESTSERVER_EWDB_20260526_20260527.md` | Accepted runtime verification review. |
| `docs/frontend/ERP_V1_FRONTEND_ACCEPTANCE_CHECKLIST_20260525.md` | Frontend acceptance criteria. |
| `docs/frontend/ERP_FRONTEND_API_FIELD_MAPPING_20260524.md` | Frontend/API field mapping. |
| `docs/engineering/RESTSERVER_API_DEVELOPMENT_GUIDE_20260527.md` | Restserver API development pattern and done criteria. |
| `docs/engineering/WAREHOUSE_DASHBOARD_API_IMPLEMENTATION_SPEC_20260527.md` | First Warehouse API implementation spec. |

## Current Decision

Baseline code review/runtime verification status:

```txt
Accepted for baseline restserver + DB readiness.
Next step is V1 Warehouse read-only aggregation API implementation.
```
