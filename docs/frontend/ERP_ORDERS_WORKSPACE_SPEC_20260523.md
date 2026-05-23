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

Earlier planning deferred quotation and contract status from the first page implementation. After clarifying the ODM workflow, quotation and customer contract are now recognized as part of the pre-order flow. The implemented Orders page can still remain fulfillment-risk focused for the first screen, but the Orders domain should include sales quotation, negotiation, customer contract, and then formal order fulfillment.

Orders should first be a fulfillment-risk management workspace on screen, and secondarily a sales quotation / customer contract / sales-order entry page as the workflow deepens.

Department ownership clarified by the user:

- Before order: Sales owns sample submission, customer sample confirmation, customer quotation/negotiation, and customer contract.
- After order: Sales owns the formal order and customer commitment; Production Control then owns production material request and scheduling.

After the user raised the order-to-material-request and work-order scheduling question, the first layer of ATP/CTP commitment checking is now included in Orders. Full APS/MRP generation remains a later Planning / APS workspace.

## First-Version Goal

Help management answer:

1. Which orders are in progress?
2. Which orders have delivery risk?
3. Which sales quotations and customer contracts are ready to become formal orders?
4. After receiving the order, can the promised delivery date be committed?
5. Are ATP inventory, material gaps, capacity, staff, QC, or shipping constraints blocking the commitment?
6. Can production make the order on time?
7. Are material, production, QC, and shipping dependencies blocking fulfillment?
8. Which orders have margin risk?
9. What is the payment status after fulfillment?

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 訂單總覽 | In-progress orders, customers, products, due dates, commitment result, current stage, delivery risk, production feasibility |
| 接單承諾 | ATP/CTP check after order receipt: inventory, material gap, capacity, staff, QC/shipping limits, and committed date |
| 交期風險 | Orders blocked by material, production capacity, QC, shipping, or urgent due dates |
| 履約進度 | Fulfillment workflow from order to material, production, QC, shipping, and payment |
| 毛利與收款 | Estimated margin, actual margin when available, and payment status |

Future first-version refinement should include pre-order views:

| View | Purpose |
| --- | --- |
| 業務報價 | Suggested quote, minimum quote, target margin, sales quote version, customer negotiation status |
| 客戶合約 | Customer contract price, validity, payment terms, delivery terms, and conversion to formal order |

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
- `committedDate`
- `commitmentDecision`
- `commitmentChecks`
- `dependencies`
- `workflow`

## Workflow Basis

First-version workflow:

```txt
product_order -> ATP/CTP commitment check -> material readiness -> work_order -> production_data -> quality check -> shipping_order -> payment
```

Pre-order ODM workflow:

```txt
R&D sample/costing basis -> sample submission -> customer sample confirmation -> supplier quote / contract assumptions -> sales quote / negotiation -> customer contract -> formal order -> ATP/CTP commitment check
```

Quotation and customer contract are not yet fully implemented on the page, but they are now part of the Orders domain roadmap.

## ATP/CTP Commitment Layer

This layer belongs in Orders because it answers the first management question before full planning starts:

```txt
Can this order be promised, and on what date?
```

It checks:

- ATP inventory: whether finished goods are already available.
- Material gap: whether BOM materials and packaging are short.
- Capacity: whether the required process and line capacity can fit the due date.
- Staff: whether scheduled staff and required skills are enough.
- QC/shipping constraints: whether quality release or shipping slots block the promise.

The result is one of:

- `可承諾`
- `需協調`
- `不可承諾`

Orders should show this result, but should not automatically create purchase requests or work-order schedules in the first version. Those belong to the later Planning / APS workspace.

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| Order list/detail | `sale`, `product_order` |
| Sales quotation | `sale`, quotation table if available |
| Customer contract | `sale`, customer contract table if available |
| Material readiness | `inventory`, `bom`, `purchase` |
| Production feasibility | `aps`, `workorder`, `processorder` |
| ATP/CTP commitment check | `inventory`, `bom`, `aps`, `workorder`, `employee`, `quality`, `shipwarehouse` |
| QC status | quality-related module/table or production data extension |
| Shipping status | `sale`, `shipwarehouse` |
| Margin estimate/actual | `sale`, `product_order`, `production_data`, finance/accounting data |
| Payment status | `arap`, `payment`, sales payment table if available |

## Deferred

- Create/edit sales orders.
- Full quotation and customer contract workflow.
- Automatic purchasing generation.
- Automatic production scheduling.
- Full financial settlement.
- Full logistics dispatch management.
