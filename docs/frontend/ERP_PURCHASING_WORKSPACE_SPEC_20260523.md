# ERP Purchasing Workspace Spec

日期：2026-05-23

## Status

Purchasing first-version workspace has been implemented in code.

- Page: `src/app/purchasing/page.tsx`
- Mock data: `src/mock/purchasing.ts`
- Types: `src/types/purchasing.ts`

## Purpose

Purchasing should support both pre-order ODM development and mass-production purchasing. It is not only a purchase order list. The first version should show which suppliers and materials are needed for R&D sampling, supplier quotation, supplier contract basis, formal production material purchasing, receiving, QC documents, and warehouse availability.

## First-Version Goal

Help management answer:

1. Which purchase demands are urgent because they affect orders or work orders?
2. Which materials are below safety stock or have no available stock?
3. Which purchase orders may miss delivery dates?
4. Which arrivals need receiving, QC documents, or warehouse handoff?
5. Which suppliers need follow-up or replacement decisions?
6. Which supplier material candidates are being used by R&D projects?
7. Which supplier quotes or supplier contracts are needed before costing and sales quotation?
8. Which production material purchase orders are required by Planning / APS after a formal order is received?

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 採購需求 | Material demand from orders, work orders, safety stock, and available stock |
| 交期風險 | Purchase items that may block production or customer delivery |
| 到貨驗收入庫 | Today's arrivals, receiving status, QC document status, and warehouse handoff |
| 供應商追蹤 | Supplier delays, document gaps, and alternative supplier decisions |

Future first-version refinement should explicitly include pre-order views:

| View | Purpose |
| --- | --- |
| 供應商找料 | Supplier material candidates and sample material status for R&D projects |
| 供應商報價 | Supplier quotes used by costing and sales quotation |
| 供應商合約 | Contract price, effective date, MOQ, lead time, and validity |

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

Pre-order ODM workflow:

```txt
R&D development request -> supplier material sourcing -> sample material -> supplier quote -> supplier contract basis -> costing -> sales quotation
```

Post-order mass-production purchasing workflow:

```txt
formal order -> production material request / schedule from Production Control -> material purchasing -> arrival -> warehouse receiving -> quality material inspection -> available inventory for production
```

Purchasing should connect back to:

- Orders: delivery risk and customer due date.
- Planning / APS / Production Control: production material requests, schedule-driven demand, and required arrival dates.
- Production: material readiness for scheduled work orders.
- Warehouse: inbound receiving, available stock, safety stock, and handoff after quality release.
- Quality: material inspection and release/blocking after receiving.
- R&D / Costing: supplier material candidates, sample materials, supplier quote, supplier contract basis.
- Orders: sales quotation and customer contract should use supplier quotation/contract assumptions when available.

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
| Supplier quote | supplier quotation table if available, `purchase` extension |
| Supplier contract | supplier contract table if available, `purchase` extension |
| R&D material candidates | item master extension, supplier item mapping |

## Deferred

- Create/edit purchase request.
- Purchase approval workflow actions.
- Supplier quotation comparison.
- Supplier material sourcing workflow.
- Supplier quote approval.
- Supplier contract management.
- Automatic reorder logic.
- Full supplier scorecard.
- Payment/AP integration.
