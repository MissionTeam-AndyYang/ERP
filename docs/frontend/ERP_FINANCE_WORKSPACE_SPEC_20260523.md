# ERP Finance Workspace Spec

日期：2026-05-23

## Status

Finance first-version workspace updated from the early module page into the management workspace pattern.

- Page: `src/app/finance/page.tsx`
- Mock data: `src/mock/finance.ts`
- Types: `src/types/finance.ts`

## First-Version Goal

Help management answer:

1. Which orders have margin risk?
2. How different are estimated margin and actual margin?
3. Which shipments already have POD and can be invoiced?
4. Which receivables are pending or overdue?
5. Which purchasing, inventory, production, and logistics costs changed the order margin?

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 毛利追蹤 | Estimated margin, actual margin, variance, and low-margin risk |
| 應收/請款 | POD, invoice readiness, payment terms, due date, and collection status |
| 應付影響 | Purchasing and payable impact on order margin |
| 成本差異 | Estimated vs actual cost, including inventory, production, and logistics cost |

## Data Shape

Finance cases are shaped around sales orders:

- `salesOrder`, `shipmentNo`
- `customer`, `product`
- `orderAmount`
- `estimatedCost`, `actualCost`
- `estimatedMarginRate`, `actualMarginRate`, `marginVarianceRate`
- `riskLevel`, `riskReason`
- `arStatus`, `invoiceNo`, `paymentTerm`, `dueDate`, `collectedAmount`
- `payableImpact`
- `inventoryCostImpact`
- `productionCostImpact`
- `logisticsCostImpact`
- `podStatus`
- `documents`
- `workflow`

## Workflow Basis

```txt
product_order
-> planning / purchasing / production / warehouse
-> quality release
-> shipment and POD
-> invoice
-> AR collection
-> margin settlement
```

## Boundary With Other Workspaces

- Orders: owns order amount, customer priority, estimated margin, and payment priority.
- Purchasing: owns purchase requests, purchase orders, supplier delivery, and AP source documents.
- Production: owns production hours, material loss, labor cost, and actual production cost.
- Warehouse: owns inventory valuation and available stock value.
- Logistics: owns shipment, POD, and delivery-related cost signal.
- Finance: owns invoice readiness, AR/AP visibility, margin variance, and collection follow-up.

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| Sales order amount and terms | `sale`, `product_order` |
| Shipment and POD | `shipwarehouse`, shipping receipt tables |
| Estimated margin | `product_order`, item/BOM cost, pricing tables |
| Actual production cost | `production_data`, `workorder`, labor/material cost tables |
| Inventory valuation | `inventory`, warehouse tables |
| Purchasing/AP impact | `purchase`, `arap`, supplier invoice tables |
| AR and collection | `arap`, payment tables |

## First-Version Decisions

- Finance is order-centric because the user prioritizes delivery feasibility first and margin second.
- POD is treated as a practical trigger for invoice readiness.
- Full accounting settlement and GL posting are deferred.

## Deferred

- General ledger.
- Tax and invoice compliance details.
- Bank reconciliation.
- Full AP approval.
- Full AR collection workflow.
- Automated cost allocation engine.

