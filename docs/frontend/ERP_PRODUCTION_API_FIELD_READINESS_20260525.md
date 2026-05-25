# ERP Production API Field Readiness

Date: 2026-05-25
Scope: Frontend readiness notes for `GET /api/v1/production/dashboard` while backend integration is pending.

## Purpose

This document bridges the approved Production V1 UI shape with the backend-facing Production API spec. It records what the frontend already expects, where normalization can happen and which fields require engineer confirmation.

## Current Frontend Contract

Current frontend service:

- `src/services/production-api.ts`
- `src/hooks/use-production-dashboard.ts`
- `src/types/production.ts`

Current frontend endpoint:

```txt
GET /api/v1/production/dashboard
```

Current frontend top-level shape:

```txt
summary
orders
weekSchedule
alerts
```

Current backend API spec top-level shape:

```txt
summary
scheduleByLine
todayWorkOrders
mesSignals
efficiencyMetrics
qualitySignals
bottlenecks
```

## Normalization Decision

Recommended V1 approach:

```txt
Backend may return the API spec shape.
Frontend service should normalize it into the existing ProductionDashboardData shape.
The page component should remain unchanged unless a real user-facing information gap is discovered.
```

Reason:

- The current page layout already answers the approved Production V1 management questions.
- Keeping normalization in `production-api.ts` avoids scattering backend field names through UI components.
- Backend can preserve domain-oriented datasets while the frontend composes schedule, work-order, MES, efficiency and quality signals into stable display records.

## Field Readiness Matrix

| Frontend field | Backend spec candidate | Readiness | Notes |
| --- | --- | --- | --- |
| `summary[].label/value/hint/tone` | `summary` | Needs frontend normalization | Derive display KPIs from active/delayed work orders, OEE/yield/loss/labor cost and quality risk. |
| `orders[].id` | `todayWorkOrders[].workOrderNo` | Ready |
| `orders[].product` | `todayWorkOrders[].productName` | Ready |
| `orders[].batchNo` | Not explicit in spec | Needs source confirmation | Needed for detail and traceability handoff. |
| `orders[].processType` | `todayWorkOrders[].processName` | Ready with mapping |
| `orders[].line` | `todayWorkOrders[].lineName` | Ready |
| `orders[].stage` | `todayWorkOrders[].status` | Ready with mapping |
| `orders[].progress` | Derived from planned/actual quantity or MES progress | Needs calculation |
| `orders[].plannedQty/completedQty/unit` | `todayWorkOrders[].plannedQty/actualQty/unit` | Ready |
| `orders[].owner` | Not explicit in spec | Needs source confirmation | Important for next-action visibility. |
| `orders[].eta` | Planned end or MES estimate | Needs mapping |
| `orders[].priority` | Risk/due-date derived priority | Needs frontend or backend rule |
| `orders[].sourceOrder` | `todayWorkOrders[].sourceOrderNo` | Ready |
| `orders[].bomNo` | Not explicit in spec | Needs source confirmation |
| `orders[].customerDueDate` | Order/shipping source | Needs source confirmation |
| `orders[].deliveryRisk` | `riskLevel`, schedule delay or order due-date logic | Needs mapping |
| `orders[].scheduleDate/startTime/endTime` | `plannedStart/plannedEnd` | Ready with date/time formatting |
| `orders[].changeoverMinutes` | Not explicit in spec | Needs source confirmation |
| `orders[].materialStatus` | `todayWorkOrders[].materialStatus` | Ready with mapping |
| `orders[].staffStatus` | `todayWorkOrders[].staffStatus` | Ready with mapping |
| `orders[].requiredStaff/assignedStaff` | Workforce/assignment source | Needs source confirmation |
| `orders[].machineStatus` | `mesSignals[]` | Needs mapping |
| `orders[].standardHours/actualHours` | `efficiencyMetrics[].plannedHours/actualHours` | Ready |
| `orders[].efficiencyRate` | `efficiencyMetrics[].oee` or derived rate | Needs definition | Current UI labels this as production-time efficiency, not necessarily full OEE. |
| `orders[].standardMaterialQty/actualMaterialQty` | Production input/output/loss source | Needs source confirmation |
| `orders[].materialLossRate` | `efficiencyMetrics[].materialLossRate` | Ready |
| `orders[].laborHours/laborCost/unitLaborCost` | `efficiencyMetrics[].unitLaborCost` plus cost source | Needs source confirmation |
| `orders[].quality` | `qualitySignals[]` | Needs aggregation |
| `orders[].qualityBlocksInventory` | `qualitySignals[]` or Quality endpoint | Needs source confirmation |
| `orders[].qualityBlocksShipment` | `qualitySignals[]` or Quality endpoint | Needs source confirmation |
| `orders[].materials` | BOM, inventory and picking/issue records | Needs aggregation |
| `orders[].workflow` | Work order and production workflow records | Needs aggregation |
| `orders[].relatedDocuments` | Source order, BOM, QC, inventory docs | Needs aggregation |
| `weekSchedule[]` | `scheduleByLine[]` | Needs normalization | Current UI groups by date, then line/process, then slots. |
| `weekSchedule[].lines[].bottleneckRank` | `bottlenecks[]` | Needs mapping |
| `alerts[]` | `bottlenecks`, quality signals, delayed work orders | Needs aggregation |

## Backend Confirmation Needed

| Question | Impact |
| --- | --- |
| Which endpoint provides current MES status? | Blocks reliable MES work-order status. |
| Does workorder include scheduled date, line, process and status? | Blocks schedule board and work-order table mapping. |
| Which endpoints provide actual production quantity and loss? | Needed for progress, yield/loss and analytics. |
| How is unit labor cost calculated today? | Needed for production cost signal. |
| Where should production quality signal come from? | Needed for QC status and inventory/shipping block flags. |
| Where is changeover/cleaning time stored or derived? | Needed for capacity view. |
| Where are staffing requirements and assigned staff stored? | Needed for readiness and bottleneck views. |
| Should production-time efficiency equal OEE, or should OEE remain a separate metric? | Needed to avoid mislabeled analytics. |

## Frontend Service TODOs After Backend Runtime Report

1. Expand `ProductionDashboardResponse` to accept the backend API spec shape.
2. Add mapper functions in `src/services/production-api.ts` for work-order stage, material status, staff status, quality status, line/process and tones.
3. Compose `todayWorkOrders[]`, `mesSignals[]`, `efficiencyMetrics[]` and `qualitySignals[]` into each frontend `WorkOrder`.
4. Compose `scheduleByLine[]` and `bottlenecks[]` into the current `weekSchedule` shape.
5. Decide whether empty arrays from API mean true empty state or should continue falling back to mock.
6. Re-run Production page smoke on desktop and mobile with real API data.

## Current Decision

```txt
ready_for_backend_mapping
```

The frontend page and type shape are stable enough for the engineer to implement or verify the Production read-only aggregate. The main open work is data normalization, MES/capacity/staffing source confirmation and quality signal mapping.
