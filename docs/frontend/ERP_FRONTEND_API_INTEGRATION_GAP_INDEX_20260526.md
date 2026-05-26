# ERP Frontend API Integration Gap Index

Date: 2026-05-26
Scope: Frontend-owned integration gap index after first-round low-risk UX refinement.

## Purpose

This document consolidates the page-level API readiness notes into one integration queue for Backend API Integration.

The goal is to keep the frontend session focused on:

1. Which API contracts need confirmation first.
2. Which pages should be integrated first.
3. Which frontend guardrails must remain consistent while backend endpoints are being implemented.

## Recommended Integration Order

| Priority | Workspace | Route | Endpoint | Why this order |
| --- | --- | --- | --- | --- |
| 1 | Warehouse | `/warehouse` | `GET /api/v1/warehouse/dashboard` | Inventory, location, expiry and task readiness are foundational for Planning, Quality, Logistics and Finance. |
| 2 | Orders | `/orders` | `GET /api/v1/orders/dashboard` | Sales order promise, fulfillment risk and customer/order context drive downstream planning and shipment views. |
| 3 | Production | `/production` | `GET /api/v1/production/dashboard` | Work-order schedule, MES status and loss/efficiency signals are core operational status inputs. |
| 4 | Quality | `/quality` | `GET /api/v1/quality/dashboard` | Release/blocking status controls warehouse movement, shipment readiness and traceability confidence. |
| 5 | Planning | `/planning` | `GET /api/v1/planning/dashboard` | Depends on orders, BOM/material availability, capacity and quality blockers; should follow initial source confirmation. |
| 6 | Purchasing | `/purchasing` | `GET /api/v1/purchasing/dashboard` | Material sourcing and receiving risk should be integrated after Planning gap fields are confirmed. |
| 7 | Logistics | `/logistics` | `GET /api/v1/logistics/dashboard` | Needs warehouse outbound, quality release, dispatch, documents, POD and cold-chain sources. |
| 8 | Finance | `/finance` | `GET /api/v1/finance/dashboard` | Depends on order amount, cost, shipment/POD, billing readiness and AR/AP source decisions. |
| 9 | Traceability | `/traceability` | `GET /api/v1/traceability/dashboard` | Needs stable batch relationship joins across purchase, inventory, production, quality and shipment. |
| 10 | Settings | `/settings` | `GET /api/v1/settings/dashboard` | Supports governance visibility; integration can proceed once permission/localization source decisions are made. |
| 11 | R&D / Costing | `/rd` | `GET /api/v1/rd/dashboard` | Requires confirmation of development-project source, development BOM semantics and costing linkage. |
| 12 | Workforce | `/workforce` | `GET /api/v1/workforce/dashboard` | Requires employee/skill/certification source confirmation; useful after Planning/Production shape stabilizes. |
| 13 | AI V1.1 | `/ai` | `GET /api/v1/ai/dashboard` | Today work status and delayed-item visibility can integrate after core module sources are stable enough to aggregate. |
| 14 | Batches | `/batches` | `GET /api/v1/batches/dashboard` | Item-centered batch operations can integrate after inventory, QA and warehouse/location source fields are stable. |

## Cross-Page API Gap Summary

| Workspace | Current frontend contract | Highest-priority backend confirmations | Integration readiness |
| --- | --- | --- | --- |
| Warehouse | `kpis`, `categorySummaries`, `capacities`, `records`, `risks`, `tasks` | Confirm inventory/location/expiry fields; clarify task and blocker source; distinguish real empty data from unavailable API. | Ready with notes |
| Orders | `summary`, `orders` | Confirm order status vocabulary, promised date, quote/contract/sample linkage and fulfillment risk source. | Ready with notes |
| Production | `summary`, `orders`, `weekSchedule`, `alerts` | Confirm work-order schedule, MES state, production actuals, loss and OEE source fields. | Ready with notes |
| Quality | `summary`, `inspections` | Confirm inspection lifecycle, release-blocking status, batch linkage and quality document source. | Ready with notes |
| Planning | `summary`, `cases` | Confirm order demand source, BOM explosion source, capacity/staff source and purchase/work-order suggestion fields. | Ready with notes |
| Purchasing | `summary`, `items` | Confirm supplier quote versus customer quote split, supplier contract split, receiving status and price variance source. | Ready with notes |
| Logistics | `summary`, `shipments` | Confirm POD source, dispatch/vehicle source, cold-chain telemetry source and shipment blocker rules. | Ready with notes |
| Finance | `summary`, `cases` | Confirm AR/AP source of truth, actual-cost availability, billing-ready rule and cost components. | Ready with notes |
| Traceability | `summary`, `records` | Confirm upstream/downstream batch relationship depth, document source and recall-scope calculation. | Ready with notes |
| Settings | `summary`, `items` | Confirm role/permission storage, login permission payload, localization source and mandatory master-data domains. | Ready with notes |
| R&D / Costing | `summary`, `projects` | Confirm development-project source, development versus production BOM, nutrition/sample status and supplier quote linkage. | Ready with notes |
| Workforce | `summary`, `cases` | Confirm employee/skill/certification tables, planned staff by line/date and staff-gap calculation rules. | Ready with notes |
| AI V1.1 | `kpis`, `todayWorkItems` | Confirm whether AI dashboard aggregates from module endpoints or dedicated AI signals; confirm progress state, module names and source record ids. | Ready with notes |
| Batches | `kpis`, `itemSummaries` | Confirm item-level aggregation, batch-location rows, quantity availability, QA hold/release, quarantine and expiry source rules. | Ready with notes |

## Backend Confirmation Packet

Use these as the first engineering alignment questions before implementing endpoint payloads.

| Area | Questions |
| --- | --- |
| Empty datasets | Can endpoints intentionally return empty arrays, and should empty arrays be treated as valid data? Frontend now treats arrays, including empty arrays, as valid API data. |
| Response envelope | Will backend return raw payloads or `{ data: ... }`? Frontend `apiGet` accepts both. |
| Date/time | Which fields are ISO timestamps versus display-ready strings? Frontend can display either but API contract should be stable. |
| Status vocabulary | Which status values are canonical per module, and do they map to `success`, `warning`, `danger`, `info`, `neutral` tones? |
| Owner fields | Which owner/team/user fields should be displayed for action follow-up? |
| Detail endpoints | Which V1 pages are dashboard-only first, and which require detail endpoint integration during the first API pass? |
| Search/filter | Frontend supports local search now. Server-side filters should wait until field names are stable unless backend already has common query patterns. |

## Frontend Integration Rules

| Rule | Current state |
| --- | --- |
| API unavailable | Service hook returns mock data, `source: "mock"` and an error message. |
| API available with valid arrays | Frontend uses API arrays, including empty arrays. |
| API missing an array field | Frontend falls back only that field to mock data. |
| API returns non-array for an array field | Frontend falls back only that field to mock data. |
| Page-level empty state | First-round UX pages now show controlled empty states for filtered empty results. |
| Mutations | Header CTAs are view navigation only in V1 unless a real mutation contract is explicitly added later. |

## Page-Level Source Documents

| Workspace | Readiness document |
| --- | --- |
| Warehouse | `docs/frontend/ERP_WAREHOUSE_API_FIELD_READINESS_20260525.md` |
| Orders | `docs/frontend/ERP_ORDERS_API_FIELD_READINESS_20260525.md` |
| Production | `docs/frontend/ERP_PRODUCTION_API_FIELD_READINESS_20260525.md` |
| Quality | `docs/frontend/ERP_QUALITY_API_FIELD_READINESS_20260525.md` |
| Planning | `docs/frontend/ERP_PLANNING_API_FIELD_READINESS_20260525.md` |
| Purchasing | `docs/frontend/ERP_PURCHASING_API_FIELD_READINESS_20260525.md` |
| Logistics | `docs/frontend/ERP_LOGISTICS_API_FIELD_READINESS_20260525.md` |
| Finance | `docs/frontend/ERP_FINANCE_API_FIELD_READINESS_20260525.md` |
| Traceability | `docs/frontend/ERP_TRACEABILITY_API_FIELD_READINESS_20260525.md` |
| Settings | `docs/frontend/ERP_SETTINGS_API_FIELD_READINESS_20260525.md` |
| R&D / Costing | `docs/frontend/ERP_RD_API_FIELD_READINESS_20260525.md` |
| Workforce | `docs/frontend/ERP_WORKFORCE_API_FIELD_READINESS_20260525.md` |
| AI V1.1 | `docs/frontend/ERP_AI_V1_1_API_FIELD_READINESS_20260526.md` |
| Batches | `docs/frontend/ERP_BATCHES_API_FIELD_READINESS_20260526.md` |

## Recommended Next Engineering Sequence

1. Backend engineer confirms Warehouse and Orders field names/status values.
2. Frontend maps Warehouse and Orders real payloads behind existing service hooks.
3. Backend engineer confirms Production and Quality blockers/release statuses.
4. Frontend validates cross-page blocker wording and empty-array behavior.
5. Proceed through Planning, Purchasing, Logistics and Finance using the priority table above.
6. Integrate Traceability after batch relationship joins are proven.
7. Integrate Settings, R&D and Workforce once their source-table questions are answered.
