# Frontend API Endpoint Inventory And Backend Gap

Date: 2026-05-24
Purpose: Provide a single engineering checklist that connects V1 frontend service-layer endpoints to existing `restserver` backend candidates, missing aggregation APIs and implementation priorities.

## Source Baseline

- Database baseline: `docs/database/EWDB_20260526.sql`
- Workflow baseline: `docs/database/EWDB_20260522_WORKFLOW.md`
- Frontend API specs: `docs/frontend/api/`
- Field mapping: `docs/frontend/ERP_FRONTEND_API_FIELD_MAPPING_20260524.md`
- API tracker: `docs/backend/API_IMPLEMENTATION_TRACKER_20260524.md`
- Verification script: `scripts/verify_v1_api_contracts.py`
- Backend app registration: `restserver/package/restserver/app.py`

## Gap Classification

| Class | Meaning |
| --- | --- |
| A | Exact frontend aggregation endpoint already exists in backend |
| B | Existing backend resource APIs appear usable for backend-side aggregation |
| C | Dedicated route, data model or domain mapping is likely required |
| D | Documentation/frontend alignment issue already corrected |

Current result: no exact V1 dashboard aggregation endpoint was observed in `restserver`. Most core pages are Class B, while Quality, R&D, Workforce, Settings and AI require additional confirmation or new backend work.

## Frontend Endpoint Inventory

| Priority | Module / Page | Frontend endpoint | Service / Hook | Required top-level datasets | Existing spec / verifier | Backend candidate routes | Gap | Recommended next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Warehouse | `GET /api/v1/warehouse/dashboard` | `src/services/warehouse-api.ts`, `src/hooks/use-warehouse-dashboard.ts` | `kpis`, `categorySummaries`, `capacities`, `records`, `risks`, `tasks` | Spec yes / verifier yes | `inventory`, `inventory/price`, `inventory/statistics`, `inventory/items`, `inventory/record`, `inventory/months`, `shipwarehouse/warehouserec`, `material`, `product`, `goods`, `batchnumber`, `batchtrace` | B | Confirm location/pallet-capacity fields, stock status, safety stock and value calculation. Implement first read-only aggregate. |
| 2 | Orders | `GET /api/v1/orders/dashboard` | `src/services/orders-api.ts`, `src/hooks/use-orders-dashboard.ts` | `summary`, `orders` | Spec yes / verifier yes | `sale/productorder`, `sale/shippingorder`, `sale/statistics`, `sale/payment`, `sale/contract`, `sale/arap`, `quotation`, `contract` | B | Compose fulfillment risk, delivery commitment, quotation/contract and collection status. |
| 3 | Production | `GET /api/v1/production/dashboard` | `src/services/production-api.ts`, `src/hooks/use-production-dashboard.ts` | `summary`, `orders`, `weekSchedule`, `alerts` | Spec yes / verifier yes | `workorder`, `workorder/productdata`, `workorder/expecteddata`, `workorder/statistics`, `work/assignment`, `work/process`, `work/productdata`, `work/progress`, `plstatistics/mancapacity`, `plstatistics/itemcapacity`, `plstatistics/itemloss`, `plstatistics/itemcost`, `productline` | B | Confirm MES source, quality signal source and week schedule derivation. |
| 4 | Quality | `GET /api/v1/quality/dashboard` | `src/services/quality-api.ts`, `src/hooks/use-quality-dashboard.ts` | `summary`, `inspections` | Spec yes / verifier yes | No dedicated quality blueprint observed; possible supporting data from `batchtrace`, `batchnumber`, `inventory/record`, `workorder`, `goods`, `material` | C | Engineer should confirm inspection/release/hold source. Dedicated quality endpoint is likely needed. |
| 5 | Planning / APS | `GET /api/v1/planning/dashboard` | `src/services/planning-api.ts`, `src/hooks/use-planning-dashboard.ts` | `summary`, `cases` | Spec yes / verifier yes | `aps/quantitydata`, `aps/labor`, `aps/quantityitem`, `aps/quantity`, `bom/aps`, `bom/tree`, `workorder`, `inventory/items` | B | Compose order feasibility, material shortage, labor and capacity checks. |
| 6 | Purchasing | `GET /api/v1/purchasing/dashboard` | `src/services/purchasing-api.ts`, `src/hooks/use-purchasing-dashboard.ts` | `summary`, `items` | Spec yes / verifier yes | `purchase/purchaseorder`, `purchase/goodsreceiptnote`, `purchase/statistics`, `purchase/payment`, `purchase/contract`, `purchase/arap`, `material/itemprice`, `quotation`, `contract` | B | Separate development-stage supplier quote/contract from mass-production purchasing. |
| 7 | Logistics | `GET /api/v1/logistics/dashboard` | `src/services/logistics-api.ts`, `src/hooks/use-logistics-dashboard.ts` | `summary`, `shipments` | Spec yes / verifier yes | `sale/shippingorder`, `shipwarehouse`, `shipwarehouse/shiprec`, `shipwarehouse/shippayment`, `shipwarehouse/shiparap`, `inventory`, `batchtrace` | B | Confirm dispatch, proof-of-delivery, temperature/cold-chain and billing-readiness data. |
| 8 | Finance | `GET /api/v1/finance/dashboard` | `src/services/finance-api.ts`, `src/hooks/use-finance-dashboard.ts` | `summary`, `cases` | Spec yes / verifier yes | `sale/arap`, `sale/payment`, `purchase/arap`, `purchase/payment`, `shipwarehouse/shiparap`, `shipwarehouse/warehousearap`, `plstatistics/itemcost` | B | Confirm AR/AP source of truth, estimated/actual margin and cost variance calculations. |
| 9 | Traceability | `GET /api/v1/traceability/dashboard` | `src/services/traceability-api.ts`, `src/hooks/use-traceability-dashboard.ts` | `summary`, `records` | Spec yes / verifier yes | `batchtrace`, `batchtrace/record`, `batchnumber`, `inventory/record`, `workorder`, `sale/shippingorder` | B | Compose upstream/downstream batch chain and recall scope. |
| 10 | R&D / Costing | `GET /api/v1/rd/dashboard` | `src/services/rd-api.ts`, `src/hooks/use-rd-dashboard.ts` | `summary`, `projects` | Spec yes / verifier yes | `bom`, `bom/tree`, `bom/process`, `bom/aps`, `quotation`, `material/itemprice`, `plstatistics/itemcost` | C | Product development project, sample status, nutrition label and version approval likely need explicit domain mapping. |
| 11 | Workforce | `GET /api/v1/workforce/dashboard` | `src/services/workforce-api.ts`, `src/hooks/use-workforce-dashboard.ts` | `summary`, `cases` | Spec yes / verifier yes | `aps/labor`, `work/assignment`, `productline`, `work/process` | C | Employee, shift, skill and certification data source must be confirmed. |
| 12 | Settings / Master Data | `GET /api/v1/settings/dashboard` | `src/services/settings-api.ts`, `src/hooks/use-settings-dashboard.ts` | `summary`, `items` | Spec yes / verifier yes | `user/login`, `auth`, `company`, `enterprise`, `product`, `bom`, `material`, `productline`, `shipwarehouse` | C | Confirm role/permission, localization, audit and master-data health endpoints. |
| 13 | Manager Dashboard | `GET /api/v1/dashboard/manager` | `src/services/dashboard-api.ts`, `src/hooks/use-dashboard.ts` | `managerSnapshot`, `managerFocusItems`, `managerDecisionItems`, `departmentBlockers`, `todayTasks`, `preOrderPipeline`, `productionLines`, `alertItems`, `productionTrendData`, `oeeTrendData`, `qualityTrendData`, `alertDistributionData`, `moduleShortcuts` | Spec yes / verifier yes | Aggregate from Warehouse, Orders, Production, Quality, Planning, Purchasing, Logistics, Finance and Traceability | B / D | Implement after stable module APIs. Frontend endpoint has been aligned to `/api/v1/dashboard/manager`. |
| 14 | Items / Item Master | `GET /api/v1/items/dashboard` | `src/app/items/page.tsx` service fetch | `kpis`, `itemCards`, `masterTasks`, `categories` | Support spec pending / verifier no | `product`, `goods`, `material`, `transitems`, `transitems/item`, `inventory/items` | B | Keep support-page aggregate after core operations unless item master becomes a blocker. |
| 15 | BOM / Formula | `GET /api/v1/bom/dashboard` | `src/app/bom/page.tsx` service fetch | `kpis`, `bomCards`, `changeTasks`, `lifecycle` | Support spec pending / verifier no | `bom`, `bom/tree`, `bom/process`, `bom/aps` | B | Can likely compose from current BOM routes; confirm versioning and approval fields. |
| 16 | Batches | `GET /api/v1/batches/dashboard` | `src/app/batches/page.tsx` service fetch | `kpis`, `batchCards`, `batchTasks`, `lifecycle` | Support spec pending / verifier no | `batchnumber`, `batchtrace`, `batchtrace/record`, `inventory/record` | B | Confirm expiry, hold/release and full chain status fields. |
| 17 | AI Center | `GET /api/v1/ai/dashboard` | `src/app/ai/page.tsx` service fetch | `kpis`, `insights`, `assistantTasks`, `flow` | Support spec pending / verifier no | No AI route observed | C | Treat as later-phase assistant/insight surface. Keep mock fallback until backend decision. |

## Backend Route Candidates Observed

Registered backend groups currently include:

```txt
auth, enterprise, company, sale, bom, purchase, mix, material, product,
transitems, contract, productline, bankaccount, work, workorder,
batchnumber, batchtrace, shipwarehouse, inventory, user, device, aps,
heartbeat, goods, quotation, plstatistics
```

Useful route-level candidates observed from backend `_uri.py` files:

```txt
aps/quantitydata, aps/labor, aps/quantityitem, aps/quantity
bankaccount
batchnumber
batchtrace, batchtrace/record
bom, bom/tree, bom/process, bom/aps
company, contract, enterprise, goods
inventory, inventory/price, inventory/statistics, inventory/items, inventory/record, inventory/months
material, material/itemprice
mix/item, mix/itemprice
plstatistics/mancapacity, plstatistics/itemcapacity, plstatistics/itemloss, plstatistics/itemcost
product, productline, productline/process, productline/station, productline/equipment, productline/factory
purchase/purchaseorder, purchase/goodsreceiptnote, purchase/statistics, purchase/payment, purchase/contract, purchase/arap
quotation
sale/productorder, sale/shippingorder, sale/statistics, sale/payment, sale/contract, sale/arap
shipwarehouse, shipwarehouse/contract, shipwarehouse/shiprec, shipwarehouse/shippayment, shipwarehouse/shiparap, shipwarehouse/warehouserec, shipwarehouse/warehousepayment, shipwarehouse/warehousearap
transitems, transitems/item
user/login
work/assignment, work/process, work/productdata, work/progress
workorder, workorder/productdata, workorder/expecteddata, workorder/statistics
```

## Recommended Backend Implementation Order

1. Warehouse: first read-only API and data mapping proof.
2. Orders: delivery commitment and fulfillment risk.
3. Production: schedule, MES, staff/material readiness and quality signals.
4. Quality: inspection/release/hold blocker model.
5. Planning / APS: order-to-material/capacity feasibility.
6. Purchasing: supplier quote/contract, mass-production PO and receiving risk.
7. Logistics: shipment readiness, dispatch and POD.
8. Finance: margin, AR/AP and cost variance.
9. Traceability: lot chain and recall scope.
10. R&D / Costing: product development, BOM costing and nutrition label.
11. Workforce: shift, skill and certification readiness.
12. Settings / Master Data: governance and system health.
13. Manager Dashboard: stable cross-module aggregate.
14. Support pages: Items, BOM, Batches and AI Center.

## Verification Notes

`scripts/verify_v1_api_contracts.py` currently covers the 13 core V1 aggregation endpoints:

```txt
warehouse, orders, planning, purchasing, quality, production, traceability,
logistics, finance, rd, workforce, dashboard, settings
```

It does not yet cover support-page endpoints:

```txt
items, bom, batches, ai
```

Add these module keys to the verification script after their API contracts are promoted from support-page fallback to formal backend implementation scope.

## Engineer Response Template

```txt
Module:
Accepted frontend endpoint:
Existing backend source endpoints:
Missing DB/table/field:
Aggregation owner: backend/frontend/temporary hybrid
Status mapping notes:
Security/permission notes:
Implementation blocker:
Runtime verification output path:
```
