# ERP Warehouse / Orders Mock-To-API Mapping Checklist

Date: 2026-05-26
Scope: Pre-integration mapping checklist for the first two recommended API integrations.

## Purpose

Warehouse and Orders are the first two recommended runtime verification targets. This checklist narrows the mapping work that can be prepared before backend endpoints are complete.

## Warehouse Mapping

Endpoint:

```txt
GET /api/v1/warehouse/dashboard
```

Frontend service:

```txt
src/services/warehouse-api.ts
```

Frontend type:

```txt
src/types/warehouse.ts
```

| Frontend group | Current field expectation | Backend candidate | Status | Mapping note |
| --- | --- | --- | --- | --- |
| KPI | `kpis[]` | `summary` | Needs mapper | Derive display-ready KPI cards from backend numeric summary. |
| Category value | `categorySummaries[]` | `inventoryValueByCategory[]` | Needs mapper | Map category code/label, value, reserved, available, pallet and item counts. |
| Capacity | `capacities[]` | `capacityByWarehouse[]` | Needs mapper | Map warehouse id/name/type, pallet totals and utilization tone. |
| Inventory rows | `records[]` | Inventory detail or separate endpoint | Pending backend | Dashboard may need detail rows or a joined aggregate. |
| Risk rows | `risks[]` | `riskAlerts[]` | Needs mapper | Map risk code to label, tone, metric and recommendation. |
| Tasks | `tasks[]` | `pendingInbound[]`, `pendingOutbound[]` | Needs mapper | Merge inbound/outbound into one task list. |

Warehouse mapper TODO after runtime response:

1. Add `WarehouseApiDashboardResponse` that accepts backend spec shape.
2. Add `mapWarehouseSummaryToKpis`.
3. Add `mapInventoryValueByCategory`.
4. Add `mapCapacityByWarehouse`.
5. Add `mapRiskAlerts`.
6. Add `mapPendingWarehouseTasks`.
7. Keep page component unchanged unless a user-facing field is truly missing.

Warehouse backend confirmation needed:

| Question | Why it matters |
| --- | --- |
| Does dashboard include inventory detail rows? | Required for current table and detail panel. |
| Where are location and pallet fields stored? | Required for capacity and warehouse row display. |
| Can on-hand, reserved, quality-hold and available quantities be separated? | Required for availability and readiness. |
| Which cost method supplies inventory value? | Required for value KPIs and row values. |
| Where are expiry/shelf-life fields stored? | Required for expiry risk. |

## Orders Mapping

Endpoint:

```txt
GET /api/v1/orders/dashboard
```

Frontend service:

```txt
src/services/orders-api.ts
```

Frontend type:

```txt
src/types/orders.ts
```

| Frontend group | Current field expectation | Backend candidate | Status | Mapping note |
| --- | --- | --- | --- | --- |
| KPI | `summary[]` | `summary` | Needs mapper | Derive open orders, high risk, commitment rate, margin/payment signals. |
| Main rows | `orders[]` | `orders[]` | Partially ready | Basic order fields likely direct; stage/status require vocabulary mapping. |
| Commitment checks | `orders[].commitmentChecks[]` | `commitmentChecks[]` | Needs grouping | Group backend checks by `orderNo`. |
| Delivery risk | `orders[].deliveryRisk`, `riskReason` | `deliveryRisks[]` | Needs grouping | Fold risk records into row/detail. |
| Margin signals | `estimatedCost`, `estimatedMarginRate`, `actualMarginRate` | `marginSignals[]` | Pending source | Actual margin may be Finance-derived. |
| Payment signals | `paymentStatus` | `paymentSignals[]` | Pending source | Confirm billing/collection source. |
| Workflow | `orders[].workflow[]` | Fulfillment/detail endpoint | Pending backend | Keep mock workflow until source confirmed. |

Orders mapper TODO after runtime response:

1. Add `OrdersApiDashboardResponse` that accepts backend spec shape.
2. Add status mappers for order stage, risk, commitment decision and payment state.
3. Group `commitmentChecks[]` by order.
4. Group `deliveryRisks[]`, `marginSignals[]` and `paymentSignals[]` by order.
5. Decide whether pre-order pipeline enters first screen or remains deferred.
6. Keep page component unchanged unless a user-facing field is truly missing.

Orders backend confirmation needed:

| Question | Why it matters |
| --- | --- |
| Which endpoint owns due date and committed date? | Required for delivery promise display. |
| Which fields support ATP/CTP checks? | Required for commitment decision. |
| Is commitment result calculated or persisted? | Affects refresh behavior and audit trail. |
| Can quotation/contract distinguish customer-side records? | Required before pre-order pipeline UI expands. |
| Which endpoint owns actual margin and payment status? | Required for margin/payment accuracy. |

## First Integration Acceptance

Warehouse and Orders should be accepted only when:

1. API source badge shows `API data`.
2. Empty arrays remain empty and do not repopulate mock rows.
3. Missing fields fallback narrowly without crashing.
4. Status values map to readable labels and badge tones.
5. Search, tab switching and detail sync still work.
6. Desktop and mobile smoke checks pass.
