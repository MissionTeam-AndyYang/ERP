# ERP Traceability Workspace Spec

日期：2026-05-23

## Status

Traceability first-version workspace has been implemented in code.

- Page: `src/app/traceability/page.tsx`
- Mock data: `src/mock/traceability.ts`
- Types: `src/types/traceability.ts`

## Purpose

Traceability is the cross-workflow search and recall workspace. It should connect purchasing, warehouse, production, quality, shipping, and orders through batch numbers and source documents.

## First-Version Goal

Help management answer:

1. Where did this batch come from?
2. Which production orders used it?
3. Which finished goods or customers are affected?
4. Are QC and supplier documents complete?
5. What is the recall impact scope?

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 溯源查詢 | Search by batch, item, sales order, or work order |
| 批號鏈路 | Supplier, receiving, batch, production, QC, inventory, shipping, and customer chain |
| 召回範圍 | Impact quantity, impacted customers, and recall simulation |
| 文件完整性 | COA, temperature records, QC records, shipping documents |

## Data Shape

Trace records are shaped around:

- `queryType`, `queryValue`
- `direction`: 原料到成品 or 成品到原料
- `itemName`, `batchNo`
- `sourceType`, `sourceDocument`
- `supplier`, `customer`
- `workOrder`, `salesOrder`
- `quantity`, `unit`
- `warehouseName`, `shipTo`
- `traceStatus`, `riskReason`
- `impactedQty`, `impactedCustomers`
- `nodes`
- `documents`

## Workflow Basis

Raw material to finished good:

```txt
supplier -> purchase_order -> goods_receipt_note -> batch_number -> inventory_record
inventory_record -> work_order/process_order -> production_data -> finished batch -> shipping_order -> customer
```

Finished good to raw material:

```txt
finished batch -> production_data -> process inputs -> raw material batch -> goods_receipt_note -> supplier
finished batch -> shipping_order/shipping_record -> customer
```

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| Batch search | `batchnumber`, `batchtrace` |
| Inventory records | `inventory` |
| Purchasing source | `purchase` |
| Production source and input/output | `workorder`, `work`, `processorder`, `production_data` |
| Shipping/customer destination | `sale`, `shipwarehouse` |
| QC records/documents | quality-related module/table or production data extension |
| Supplier documents | `purchase`, supplier/company document extension |

## Deferred

- Real graph visualization.
- Full recall workflow actions.
- Batch split/merge visualization.
- Regulatory report export.
- Automatic missing-document notification.
