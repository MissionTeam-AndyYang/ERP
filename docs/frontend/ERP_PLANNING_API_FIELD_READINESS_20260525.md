# ERP Planning API Field Readiness

Date: 2026-05-25
Scope: Frontend readiness notes for `GET /api/v1/planning/dashboard` while backend integration is pending.

## Current Frontend Contract

Current frontend service:

- `src/services/planning-api.ts`
- `src/hooks/use-planning-dashboard.ts`
- `src/types/planning.ts`

Current frontend endpoint:

```txt
GET /api/v1/planning/dashboard
```

Current frontend top-level shape:

```txt
summary
cases
```

## Normalization Decision

Recommended V1 approach:

```txt
Backend may return domain-oriented planning datasets.
Frontend service should normalize them into the existing PlanningDashboardData shape.
The page component should remain unchanged unless a real user-facing information gap is discovered.
```

## Field Readiness Matrix

| Frontend field | Backend candidate | Readiness | Notes |
| --- | --- | --- | --- |
| `summary[]` | planning aggregate summary | Needs frontend normalization | Derive display KPIs from pending orders, shortages, capacity conflicts and work-order suggestions. |
| `cases[].sourceOrder/customer/product/itemNo` | sale/productorder + item/product | Ready with mapping |
| `cases[].dueDate/promisedDate` | sale/order commitment result | Needs source confirmation |
| `cases[].decision` | worst-result logic from checks | Needs mapping |
| `cases[].materialShortageValue` | BOM + inventory + price | Needs calculation |
| `cases[].requiredProductionHours/availableProductionHours` | APS/productline/workorder capacity | Needs source confirmation |
| `cases[].checks` | aggregated planning checks | Needs aggregation |
| `cases[].materials` | BOM explosion + inventory + purchase suggestion | Needs aggregation |
| `cases[].capacity` | APS/productline/staff availability | Needs aggregation |
| `cases[].workOrders` | suggested work orders | Needs aggregation |

## Backend Confirmation Needed

| Question | Impact |
| --- | --- |
| Which endpoint provides formal accepted orders and promised dates? | Blocks planning case creation. |
| Which API returns BOM explosion by order/product? | Needed for material demand. |
| Which inventory fields distinguish available stock, blocked batches and reservations? | Needed for shortage and release follow-up. |
| Which endpoint provides process line capacity and changeover time? | Needed for capacity checks. |
| Where are staffing requirements and assignments stored? | Needed for staff readiness. |
| Should suggested work orders be calculated only, or stored persistently? | Determines mapping and future mutation boundary. |

## Frontend Service TODOs After Backend Runtime Report

1. Expand `PlanningDashboardResponse` to accept backend planning datasets.
2. Add mapper functions in `src/services/planning-api.ts` for decision, check area, material action, capacity status and tones.
3. Compose order, BOM, inventory, capacity, staff and quality signals into each `PlanningCase`.
4. Decide whether empty arrays from API mean true empty state or should continue falling back to mock.
5. Re-run Planning page smoke on desktop and mobile with real API data.

## Current Decision

```txt
ready_for_backend_mapping
```

The frontend page and type shape are stable enough for the engineer to implement or verify the Planning read-only aggregate. The main open work is data normalization and APS/BOM/inventory/staff source confirmation.
