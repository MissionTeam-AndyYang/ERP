# ERP Orders Workspace Spec

日期：2026-05-23

## Status

Orders first-version direction confirmed with the user and implemented in code.

- Page: `src/app/orders/page.tsx`
- Mock data: `src/mock/orders.ts`
- Types: `src/types/orders.ts`

## User Focus

Priority confirmed by the user:

1. Delivery date and whether production can make it on time.
2. Estimated and actual margin.
3. Payment/collection.

The first version does not need quotation or contract status.

Orders should first be a fulfillment-risk management workspace, and only secondarily a sales-order entry or logistics management page.

## First-Version Goal

Help management answer:

1. Which orders are in progress?
2. Which orders have delivery risk?
3. Can production make the order on time?
4. Are material, production, QC, and shipping dependencies blocking fulfillment?
5. Which orders have margin risk?
6. What is the payment status after fulfillment?

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 訂單總覽 | In-progress orders, customers, products, due dates, current stage, delivery risk, production feasibility |
| 交期風險 | Orders blocked by material, production capacity, QC, shipping, or urgent due dates |
| 履約進度 | Fulfillment workflow from order to material, production, QC, shipping, and payment |
| 毛利與收款 | Estimated margin, actual margin when available, and payment status |

## Data Shape

Sales order records are shaped around:

- `id`, `customer`, `channel`
- `product`, `itemNo`
- `quantity`, `unit`
- `orderAmount`, `estimatedCost`
- `estimatedMarginRate`, `actualMarginRate`
- `dueDate`, `shipDate`
- `stage`
- `deliveryRisk`
- `productionFeasibility`
- `riskReason`
- `materialStatus`
- `productionStatus`
- `qualityStatus`
- `shippingStatus`
- `paymentStatus`
- `dependencies`
- `workflow`

## Workflow Basis

First-version workflow:

```txt
product_order -> material readiness -> work_order -> production_data -> quality check -> shipping_order -> payment
```

Quotation and contract are intentionally excluded from the first-version Orders workspace.

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| Order list/detail | `sale`, `product_order` |
| Material readiness | `inventory`, `bom`, `purchase` |
| Production feasibility | `aps`, `workorder`, `processorder` |
| QC status | quality-related module/table or production data extension |
| Shipping status | `sale`, `shipwarehouse` |
| Margin estimate/actual | `sale`, `product_order`, `production_data`, finance/accounting data |
| Payment status | `arap`, `payment`, sales payment table if available |

## Deferred

- Create/edit sales orders.
- Quotation and contract workflow.
- Automatic purchasing generation.
- Automatic production scheduling.
- Full financial settlement.
- Full logistics dispatch management.
