# ERP Purchasing Workspace Spec

日期：2026-05-23

## Status

Purchasing first-version workspace has been implemented in code.

- Page: `src/app/purchasing/page.tsx`
- Mock data: `src/mock/purchasing.ts`
- Types: `src/types/purchasing.ts`

## Purpose

Purchasing should support order fulfillment and production readiness. It is not only a purchase order list. The first version should show which materials are blocking orders, production, receiving, QC documents, or warehouse availability.

## First-Version Goal

Help management answer:

1. Which purchase demands are urgent because they affect orders or work orders?
2. Which materials are below safety stock or have no available stock?
3. Which purchase orders may miss delivery dates?
4. Which arrivals need receiving, QC documents, or warehouse handoff?
5. Which suppliers need follow-up or replacement decisions?

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 採購需求 | Material demand from orders, work orders, safety stock, and available stock |
| 交期風險 | Purchase items that may block production or customer delivery |
| 到貨驗收入庫 | Today's arrivals, receiving status, QC document status, and warehouse handoff |
| 供應商追蹤 | Supplier delays, document gaps, and alternative supplier decisions |

## Data Shape

Purchase item records are shaped around:

- `requestNo`, `purchaseOrderNo`
- `itemNo`, `itemName`, `category`
- `supplier`
- `quantity`, `unit`, `amount`
- `requiredDate`, `expectedArrivalDate`
- `stage`
- `riskLevel`, `riskReason`
- `sourceOrder`, `linkedWorkOrder`
- `currentStock`, `reservedStock`, `availableStock`, `safetyStock`
- `leadTimeDays`, `delayDays`
- `qualityDocumentStatus`
- `receivingStatus`, `warehouseStatus`
- `dependencies`
- `workflow`

## Workflow Basis

```txt
purchase_request -> purchase_order -> goods_receipt_note -> QC/document check -> batch_number -> inventory_record
```

Purchasing should connect back to:

- Orders: delivery risk and customer due date.
- Production: material readiness for scheduled work orders.
- Warehouse: available stock, safety stock, and inbound receiving.

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| Purchase requests | `purchase` |
| Purchase orders | `purchase` |
| Receiving records | `goods_receipt_note`, `purchase` |
| Stock availability | `inventory`, `batchnumber` |
| Order/work-order dependency | `sale`, `product_order`, `workorder`, `aps` |
| Supplier status | supplier/company data, `purchase` |
| QC documents | quality-related module/table or receiving extension |

## Deferred

- Create/edit purchase request.
- Purchase approval workflow actions.
- Supplier quotation comparison.
- Automatic reorder logic.
- Full supplier scorecard.
- Payment/AP integration.
