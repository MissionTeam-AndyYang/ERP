# ERP Warehouse API Field Readiness

Date: 2026-05-25
Scope: Frontend readiness notes for `GET /api/v1/warehouse/dashboard` while backend integration is pending.

## Purpose

This document bridges the approved Warehouse V1 UI shape with the backend-facing Warehouse API spec. It is not a backend implementation design; it records what the frontend already expects, where normalization can happen and which fields require engineer confirmation.

## Current Frontend Contract

Current frontend service:

- `src/services/warehouse-api.ts`
- `src/hooks/use-warehouse-dashboard.ts`
- `src/types/warehouse.ts`

Current frontend endpoint:

```txt
GET /api/v1/warehouse/dashboard
```

Current frontend top-level shape:

```txt
kpis
categorySummaries
capacities
records
risks
tasks
```

Current backend API spec top-level shape:

```txt
summary
inventoryValueByCategory
capacityByWarehouse
riskAlerts
pendingInbound
pendingOutbound
qualityHoldItems
valueTrend
```

## Normalization Decision

Recommended V1 approach:

```txt
Backend may return the API spec shape.
Frontend service should normalize it into the existing WarehouseDashboardData shape.
The page component should remain unchanged unless a real user-facing information gap is discovered.
```

Reason:

- The current page layout already answers the approved Warehouse V1 management questions.
- Keeping normalization in `warehouse-api.ts` avoids scattering backend field names through UI components.
- Backend can preserve domain-oriented dataset names while frontend preserves stable component types.

## Field Readiness Matrix

| Frontend field | Backend spec candidate | Readiness | Notes |
| --- | --- | --- | --- |
| `kpis[].label/value/hint/tone` | `summary` | Needs frontend normalization | Derive KPI display values from total value, pallet usage, risk count and pending task counts. |
| `categorySummaries[].category` | `inventoryValueByCategory[].label` or category code mapping | Ready with mapping | Frontend currently uses Chinese category labels as typed values. Backend spec uses category codes plus labels. |
| `categorySummaries[].amount` | `inventoryValueByCategory[].inventoryValue` | Ready |
| `categorySummaries[].amountRatio` | Derived from category value / total value | Needs frontend or backend calculation | Prefer backend if totals are already computed, otherwise derive in service. |
| `categorySummaries[].reservedAmount` | `inventoryValueByCategory[].reservedValue` | Ready |
| `categorySummaries[].availableAmount` | `inventoryValueByCategory[].availableValue` | Ready |
| `categorySummaries[].palletCount` | `inventoryValueByCategory[].palletUsed` | Ready |
| `categorySummaries[].itemCount` | `inventoryValueByCategory[].itemCount` | Ready |
| `categorySummaries[].trend7Days` | `valueTrend` | Needs confirmation | Current UI expects one 7-day percentage per category. Backend spec lists trend as separate dataset. |
| `capacities[].id` | `capacityByWarehouse[].warehouseId` | Ready |
| `capacities[].warehouseName` | `capacityByWarehouse[].warehouseName` | Ready |
| `capacities[].warehouseType` | `capacityByWarehouse[].warehouseType` | Ready with label mapping | Backend may return code such as `frozen`; frontend can display mapped labels. |
| `capacities[].totalPallets` | `capacityByWarehouse[].totalPallets` | Ready |
| `capacities[].usedPallets` | `capacityByWarehouse[].usedPallets` | Ready |
| `capacities[].reservedPallets` | `capacityByWarehouse[].reservedPallets` | Ready |
| `capacities[].availablePallets` | `capacityByWarehouse[].availablePallets` | Ready |
| `capacities[].tone` | `capacityByWarehouse[].riskLevel` or `utilizationRate` | Needs mapping | Use warning when utilization is high, danger only if backend flags blocked/overcapacity. |
| `records[].id` | `inventory[].inventoryId` | Ready if detail included | Backend aggregate spec does not currently list top-level `inventory`; detail endpoint does. Dashboard needs either `records` or enough detail data. |
| `records[].itemNo/itemName` | `inventory[].itemNo/itemName` | Ready |
| `records[].category` | `inventory[].category` plus code mapping | Ready with mapping |
| `records[].warehouseNo` | `inventory[].warehouseId` or `locationCode` | Needs confirmation | Frontend displays a compact warehouse/location code. |
| `records[].warehouseName` | `inventory[].warehouseName` | Ready |
| `records[].batchNo` | `inventory[].batchNo` | Ready |
| `records[].sourceLabel/sourceNo` | `inventory[].sourceRefCategory/sourceNo` | Ready with mapping; API no longer returns `sourceType`, frontend display label must be derived from `sourceRefCategory`. |
| `records[].quantity` | `inventory[].onHandQty` | Ready |
| `records[].reservedQuantity` | `inventory[].reservedQty` | Needs business rule confirmation | Reservation may come from sales orders, production orders and pending warehouse tasks. |
| `records[].availableQuantity` | `inventory[].availableQty` | Ready if backend applies quality hold | Rule should be `onHand - reserved - qualityHold`. |
| `records[].amount` | `inventory[].inventoryValue` | Ready |
| `records[].reservedAmount` | Derived from reserved quantity and unit cost | Needs calculation |
| `records[].availableAmount` | Derived from available quantity and unit cost | Ready if backend returns or frontend derives |
| `records[].palletCount` | `inventory[].palletCount` | Needs source confirmation |
| `records[].safetyStock` | `inventory[].safetyStock` | Needs source confirmation |
| `records[].expiryDate/shelfLifeDays/daysLeft` | `inventory[]` expiry fields | Needs source confirmation | Also confirm supplies/film shelf-life exclusion rule. |
| `records[].turnoverDays` | `inventory[].turnoverDays` | Ready if backend calculates |
| `records[].status/tone` | `qualityStatus` and `riskLevel` | Needs mapping | Frontend status wording should remain management-readable. |
| `records[].workflow` | Source documents from purchase, production, inventory and shipment | Needs aggregation | Current mock uses display workflow steps; backend does not yet define this nested display shape. |
| `records[].relatedDocuments` | Source documents and alert references | Needs aggregation |
| `risks[].id` | `riskAlerts[].alertId` | Ready |
| `risks[].type` | `riskAlerts[].type` | Ready with mapping | Map codes to Chinese labels. |
| `risks[].itemName/category/batchNo/warehouseName` | `riskAlerts[]` fields | Ready |
| `risks[].metric` | `riskAlerts[].message`, `daysLeft`, turnover/safety fields | Needs formatting |
| `risks[].recommendation` | Not explicit in spec | Needs frontend rule or backend message | Can be generated from alert type in service. |
| `tasks[].id` | `pendingInbound[].taskId`, `pendingOutbound[].taskId` | Ready |
| `tasks[].type` | `taskType` | Ready with mapping | Also support transfer/check tasks when backend adds them. |
| `tasks[].sourceNo` | `documentNo` | Ready |
| `tasks[].owner/dueTime/status` | Task fields | Ready with formatting |
| `tasks[].tone` | Task status, quality status or lateness | Needs mapping |

## Backend Confirmation Needed

| Question | Impact |
| --- | --- |
| Will `/api/v1/warehouse/dashboard` include inventory detail rows, or only summary/category/risk/task datasets? | Determines whether the current detail panel can be populated from the aggregate endpoint or needs `GET /api/v1/warehouse/inventory`. |
| Where are warehouse location and pallet capacity stored? | Blocks accurate `capacities` and pallet utilization display. |
| Does current inventory distinguish on-hand, reserved, quality-hold and available quantity? | Blocks accurate availability and shipment/production readiness. |
| What is the reservation source of truth? | Needed for sales reservations, production material allocation and warehouse pending tasks. |
| Which table/field stores safety stock? | Needed for below-safety alerts. |
| Which cost method should inventory value use? | Needed for `amount`, `reservedAmount`, `availableAmount` and KPI value. |
| Where is material inspection release/hold status stored? | Needed so unreleased batches do not appear as available stock. |
| Can current endpoints return batch expiry and shelf-life data? | Needed for one-third shelf-life rule. |
| Should value trend be backend-calculated from snapshots or frontend-calculated from ledger history? | Needed for category trend display. |

## Frontend Service TODOs After Backend Runtime Report

1. Expand `WarehouseDashboardResponse` to accept the backend API spec shape.
2. Add mapper functions in `src/services/warehouse-api.ts` for category, source type, task type, risk type and tone.
3. Decide whether empty arrays from API mean true empty state or should continue falling back to mock.
4. Add defensive defaults for optional backend fields without hiding schema mismatches.
5. Re-run Warehouse page smoke on desktop and mobile with real API data.

## Current Decision

```txt
ready_for_backend_mapping
```

The frontend page and type shape are stable enough for the engineer to implement or verify the Warehouse read-only aggregate. The main open work is data normalization and backend source confirmation, not page layout redesign.
