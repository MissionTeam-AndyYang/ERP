# ERP V1 API Implementation Tracker

Date: 2026-05-24
Purpose: Track backend implementation, runtime verification and frontend integration status for V1 APIs.

## Status Legend

| Status | Meaning |
| --- | --- |
| `spec_ready` | API development spec exists |
| `frontend_service_ready` | Frontend service/hook exists and can call the proposed API with mock fallback |
| `engineer_confirming` | Engineer is checking DB fields, existing endpoints and gaps |
| `confirmed` | Engineer confirmed implementation path |
| `backend_implemented` | Backend endpoint implemented |
| `runtime_verified` | API contract/runtime verification passed |
| `frontend_integrated` | Frontend uses real API data |
| `blocked` | Waiting for DB/schema/workflow decision |

## Implementation Priority

| Priority | Module | Reason |
| --- | --- | --- |
| 1 | Warehouse | Connects inventory value, availability, capacity, inbound/outbound and quality hold |
| 2 | Orders | Drives delivery commitment, fulfillment risk, margin and payment signals |
| 3 | Production | Validates work-order schedule, MES and efficiency data |
| 4 | Quality | Controls release/hold blockers for inventory, production and shipment |
| 5 | Planning / APS | Connects order demand to material, capacity and work-order suggestions |
| 6 | Purchasing | Supplies quote, contract, purchase and arrival risk |
| 7 | Logistics | Connects shipment readiness, dispatch, POD and billing readiness |
| 8 | Finance | Connects margin, cost variance, AR/AP and billing readiness |
| 9 | Traceability | Connects batch, order, work-order and recall chains |
| 10 | R&D / Costing | Connects pre-order development, BOM, costing and nutrition label |
| 11 | Workforce | Connects staff readiness and skill/certification constraints |
| 12 | Settings / Master Data | Provides governance, permissions and integration status |
| 13 | Manager Dashboard | Aggregates the stable module APIs into management cockpit |
| 14 | Support Pages | Items, BOM, Batches and AI Center are connected to service-layer fallback and can be formalized after core APIs |

## Module Tracker

| Module | Spec | Aggregation API | Detail APIs | Current status | Owner note |
| --- | --- | --- | --- | --- | --- |
| Warehouse | `docs/frontend/api/ERP_WAREHOUSE_API_DEVELOPMENT_SPEC_20260524.md` | `GET /api/v1/warehouse/dashboard` | inventory, locations, alerts, tasks, quality-holds | `spec_ready` + `frontend_service_ready` | First implementation candidate |
| Orders | `docs/frontend/api/ERP_ORDERS_API_DEVELOPMENT_SPEC_20260524.md` | `GET /api/v1/orders/dashboard` | orders, commitment, quotations, contracts, fulfillment | `spec_ready` + `frontend_service_ready` | Confirm sale/quotation/contract mapping |
| Planning / APS | `docs/frontend/api/ERP_PLANNING_APS_API_DEVELOPMENT_SPEC_20260524.md` | `GET /api/v1/planning/dashboard` | cases, materials, capacity, workorders | `spec_ready` + `frontend_service_ready` | Confirm APS quantity and BOM expansion |
| Purchasing | `docs/frontend/api/ERP_PURCHASING_API_DEVELOPMENT_SPEC_20260524.md` | `GET /api/v1/purchasing/dashboard` | supplier-quotes, supplier-contracts, purchase-orders, receipts, price-variance | `spec_ready` + `frontend_service_ready` | Confirm supplier/customer quote distinction |
| Quality | `docs/frontend/api/ERP_QUALITY_API_DEVELOPMENT_SPEC_20260524.md` | `GET /api/v1/quality/dashboard` | inspections, releases, blockers, documents | `spec_ready` + `frontend_service_ready` | Dedicated quality endpoint likely needed |
| Production | `docs/frontend/api/ERP_PRODUCTION_API_DEVELOPMENT_SPEC_20260524.md` | `GET /api/v1/production/dashboard` | workorders, schedule, mes, metrics | `spec_ready` + `frontend_service_ready` | Confirm MES source |
| Traceability | `docs/frontend/api/ERP_TRACEABILITY_API_DEVELOPMENT_SPEC_20260524.md` | `GET /api/v1/traceability/dashboard` | search, batch detail, upstream, downstream, recall-scope | `spec_ready` + `frontend_service_ready` | Confirm batchtrace relationships |
| Logistics | `docs/frontend/api/ERP_LOGISTICS_API_DEVELOPMENT_SPEC_20260524.md` | `GET /api/v1/logistics/dashboard` | shipments, dispatch, documents, POD | `spec_ready` + `frontend_service_ready` | Confirm POD and cold-chain data |
| Finance | `docs/frontend/api/ERP_FINANCE_API_DEVELOPMENT_SPEC_20260524.md` | `GET /api/v1/finance/dashboard` | orders, margins, cost-variance, billing-readiness, arap | `spec_ready` + `frontend_service_ready` | Confirm AR/AP source of truth |
| R&D / Costing | `docs/frontend/api/ERP_RD_COSTING_API_DEVELOPMENT_SPEC_20260524.md` | `GET /api/v1/rd/dashboard` | projects, samples, bom-versions, costing, nutrition | `spec_ready` + `frontend_service_ready` | Dedicated R&D endpoint likely needed |
| Workforce | `docs/frontend/api/ERP_WORKFORCE_API_DEVELOPMENT_SPEC_20260524.md` | `GET /api/v1/workforce/dashboard` | shifts, skills, certifications, line-readiness | `spec_ready` + `frontend_service_ready` | Confirm employee/skill tables |
| Manager Dashboard | `docs/frontend/api/ERP_MANAGER_DASHBOARD_API_DEVELOPMENT_SPEC_20260524.md` | `GET /api/v1/dashboard/manager` | summary, decisions, workqueue, blockers, preorder, operations | `spec_ready` + `frontend_service_ready` | Implement after core modules are stable |
| Settings / Master Data | `docs/frontend/api/ERP_SETTINGS_MASTER_DATA_API_DEVELOPMENT_SPEC_20260524.md` | `GET /api/v1/settings/dashboard` | master-data-health, permissions, integrations, localization, audit | `spec_ready` + `frontend_service_ready` | Confirm role/permission endpoint |
| Items / Item Master | Support-page spec pending | `GET /api/v1/items/dashboard` | kpis, itemCards, masterTasks, categories | `frontend_service_ready` | Compose from product/material/goods/transitems/inventory candidates |
| BOM / Formula | Support-page spec pending | `GET /api/v1/bom/dashboard` | kpis, bomCards, changeTasks, lifecycle | `frontend_service_ready` | Compose from bom, bom/tree, bom/process, bom/aps candidates |
| Batches | Support-page spec pending | `GET /api/v1/batches/dashboard` | kpis, batchCards, batchTasks, lifecycle | `frontend_service_ready` | Compose from batchnumber/batchtrace/inventory candidates |
| AI Center | Support-page spec pending | `GET /api/v1/ai/dashboard` | kpis, insights, assistantTasks, flow | `frontend_service_ready` | No backend AI route observed; keep later-phase placeholder |

## Engineer Confirmation Checklist

Ask the engineer to update or reply with:

1. Existing endpoint that can support each aggregation API.
2. Missing DB fields or tables.
3. Endpoint naming preference if different from the proposed spec.
4. Whether aggregation should be backend-side or frontend-side for each module.
5. Expected implementation order and blockers.
6. Runtime verification output after implementation.

## First Milestone

Milestone name: `Warehouse read-only API ready`

Completion criteria:

- Warehouse endpoint path confirmed.
- `GET /api/v1/warehouse/dashboard` or equivalent endpoint returns required datasets.
- Required fields for `summary`, `inventoryValueByCategory`, `capacityByWarehouse`, `riskAlerts`, `pendingInbound`, `pendingOutbound` are present.
- Verification script passes.
- Frontend service layer can map response into `src/types/warehouse.ts`.

## Second Milestone

Milestone name: `Core operations read-only APIs ready`

Completion criteria:

- Warehouse, Orders, Production and Quality dashboard APIs are implemented.
- Cross-module blockers can be derived from real data.
- Manager Dashboard can be implemented using module APIs or backend aggregation.

## Notes

- Do not treat this tracker as evidence that endpoints are already implemented.
- This tracker should be updated after engineer confirmation, implementation and runtime verification.
- Raw runtime output should be stored under `docs/backend/runtime-verification/` and reviewed before committing.
- Frontend endpoint inventory and backend gap details are tracked in `docs/backend/FRONTEND_API_ENDPOINT_INVENTORY_AND_BACKEND_GAP_20260524.md`.
