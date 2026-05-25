# ERP Orders API Field Readiness

Date: 2026-05-25
Scope: Frontend readiness notes for `GET /api/v1/orders/dashboard` while backend integration is pending.

## Purpose

This document bridges the approved Orders V1 UI shape with the backend-facing Orders API spec. It records what the frontend already expects, where normalization can happen and which fields require engineer confirmation.

## Current Frontend Contract

Current frontend service:

- `src/services/orders-api.ts`
- `src/hooks/use-orders-dashboard.ts`
- `src/types/orders.ts`

Current frontend endpoint:

```txt
GET /api/v1/orders/dashboard
```

Current frontend top-level shape:

```txt
summary
orders
```

Current backend API spec top-level shape:

```txt
summary
orders
commitmentChecks
deliveryRisks
marginSignals
paymentSignals
preOrderPipeline
```

## Normalization Decision

Recommended V1 approach:

```txt
Backend may return the API spec shape.
Frontend service should normalize it into the existing OrdersDashboardData shape.
The page component should remain unchanged unless a real user-facing information gap is discovered.
```

Reason:

- The current page layout already answers the approved Orders V1 management priority.
- Keeping normalization in `orders-api.ts` avoids scattering backend field names through UI components.
- The backend can keep separate source datasets for commitment checks, risks, margin and payment while frontend can compose them into each `SalesOrder`.

## Field Readiness Matrix

| Frontend field | Backend spec candidate | Readiness | Notes |
| --- | --- | --- | --- |
| `summary[].label/value/hint/tone` | `summary` | Needs frontend normalization | Derive display KPIs from open orders, high-risk orders, commitment rate, margin and payment risk. |
| `orders[].id` | `orders[].orderNo` | Ready |
| `orders[].customer` | `orders[].customerName` | Ready |
| `orders[].channel` | Not explicit in spec | Needs source confirmation | Could come from customer/order attributes or remain optional. |
| `orders[].product` | `orders[].productName` | Ready |
| `orders[].itemNo` | `orders[].productNo` or item field | Needs source confirmation | Current UI displays product/item identifier below product name. |
| `orders[].quantity/unit` | `orders[].quantity/unit` | Ready |
| `orders[].orderAmount` | `orders[].orderAmount` | Ready |
| `orders[].estimatedCost` | `orders[].estimatedCost` | Ready if backend provides cost basis |
| `orders[].estimatedMarginRate` | `orders[].estimatedMarginRate` or calculation rule | Ready |
| `orders[].actualMarginRate` | `marginSignals[]` or finance data | Needs source confirmation | May be null before fulfillment/cost settlement. |
| `orders[].dueDate` | `orders[].dueDate` | Ready |
| `orders[].shipDate` | Shipping order or fulfillment dataset | Needs source confirmation |
| `orders[].stage` | `orders[].stage` | Ready with mapping | Backend uses codes such as `commitment_check`; frontend displays management-readable labels. |
| `orders[].tone` | Stage/risk mapping | Needs mapping |
| `orders[].deliveryRisk` | `orders[].deliveryRisk` or `deliveryRisks[]` | Ready with mapping |
| `orders[].productionFeasibility` | Commitment checks and capacity result | Needs aggregation | Frontend expects `可生產`, `需協調` or `不可如期`. |
| `orders[].riskReason` | `orders[].riskReason` or `deliveryRisks[]` message | Ready |
| `orders[].materialStatus` | `commitmentChecks[]` material result | Needs aggregation |
| `orders[].productionStatus` | Work order / fulfillment dataset | Needs source confirmation |
| `orders[].qualityStatus` | Quality check or fulfillment dataset | Needs source confirmation |
| `orders[].shippingStatus` | Shipping order / fulfillment dataset | Needs source confirmation |
| `orders[].paymentStatus` | `orders[].paymentStatus` or `paymentSignals[]` | Ready with mapping |
| `orders[].owner` | Not explicit in spec | Needs source confirmation | Important for manager next-action visibility. |
| `orders[].priority` | Risk/due-date derived priority | Needs frontend or backend rule |
| `orders[].committedDate` | `orders[].committedDate` | Ready |
| `orders[].commitmentDecision` | `orders[].commitmentDecision` | Ready with mapping |
| `orders[].commitmentChecks` | `commitmentChecks[]` grouped by orderNo | Needs aggregation | Map check type codes to display labels and tones. |
| `orders[].dependencies` | `deliveryRisks[]`, commitment checks and fulfillment status | Needs aggregation |
| `orders[].workflow` | `GET /orders/{orderNo}/fulfillment` or aggregate fulfillment dataset | Needs aggregation |

## Backend Confirmation Needed

| Question | Impact |
| --- | --- |
| Which endpoint contains formal order due date and committed date? | Blocks core delivery commitment display. |
| Which fields can support ATP/CTP checks today? | Needed for commitment decision, feasibility and blocker visibility. |
| Where should commitment result be stored if it becomes persistent? | Determines whether frontend treats it as calculated runtime state or saved order state. |
| Can quotation distinguish customer quotation from supplier quotation? | Needed before adding pre-order quotation UI. |
| Can contract distinguish customer contract from supplier contract? | Needed before adding customer contract pipeline UI. |
| Which endpoint provides actual margin after fulfillment? | Needed for margin/payment tab accuracy. |
| Which endpoint provides payment or collection status? | Needed for payment risk and billing readiness. |
| Should `preOrderPipeline` appear in Orders first screen or stay deferred? | Product decision after backend source is confirmed. |

## Frontend Service TODOs After Backend Runtime Report

1. Expand `OrdersDashboardResponse` to accept the backend API spec shape.
2. Add mapper functions in `src/services/orders-api.ts` for stage, risk, commitment decision, check type, payment status and tones.
3. Compose backend `commitmentChecks[]` into each frontend `SalesOrder.commitmentChecks`.
4. Decide whether `deliveryRisks[]`, `marginSignals[]` and `paymentSignals[]` should become separate UI panels or stay folded into each order row/detail.
5. Decide whether empty arrays from API mean true empty state or should continue falling back to mock.
6. Re-run Orders page smoke on desktop and mobile with real API data.

## Current Decision

```txt
ready_for_backend_mapping
```

The frontend page and type shape are stable enough for the engineer to implement or verify the Orders read-only aggregate. The main open work is data normalization, ATP/CTP source confirmation and pre-order pipeline scope.
