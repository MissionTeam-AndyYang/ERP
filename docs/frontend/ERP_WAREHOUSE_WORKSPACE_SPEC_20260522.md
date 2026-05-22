# ERP Warehouse Workspace Spec

日期：2026-05-22

## Status

Implemented first prototype:

- Page: `src/app/warehouse/page.tsx`
- Mock data: `src/mock/warehouse.ts`
- Types: `src/types/warehouse.ts`

This is the first core workspace selected by the user.

## Purpose

Warehouse is the first practical operations workspace because it touches purchasing, production, inventory, traceability, and warehouse cost exposure. The first version focuses on query, review, and workflow status.

## Workflow Basis

```txt
purchase_order -> goods_receipt_note -> batch_number -> inventory_record -> warehouse_record -> warehouse_payment
work_order / process_order -> batch_number -> inventory_record -> production_data
product_order -> shipping_order -> shipping_record -> shipping_payment
```

Warehouse should show whether stock came from purchasing, production, or another inventory movement.

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 庫存總覽 | Management view of stock by item and warehouse |
| 批號效期 | Batch, expiry, source, and trace status |
| 進出紀錄 | Inbound/outbound movement and source document review |
| 倉租帳款 | Storage-related records and payment exposure |

## Current Data Shape

Each visible record is shaped around:

- `itemNo`, `itemName`, `category`
- `warehouseNo`, `warehouseName`
- `batchNo`
- `sourceType`, `sourceNo`
- `quantity`, `unit`, `amount`
- `expiryDate`, `daysLeft`
- `storageDays`, `storageCharge`, `paymentStatus`
- `workflow`
- `relatedDocuments`

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| Inventory list | `inventory` |
| Batch list/detail | `batchnumber`, `batchtrace` |
| Warehouse records | `shipwarehouse` |
| Warehouse payments | `shipwarehouse`, `arap` |
| Goods receipt source | `purchase` |
| Production source | `workorder`, `work`, `processorder` |
| Shipping source | `sale`, `shipwarehouse` |

## Next Integration Steps

1. Add a Warehouse API adapter that returns the current mock shape.
2. Connect list data first; keep write actions disabled.
3. Add real filters after endpoint query parameters are confirmed.
4. Link the trace button to Traceability once that workspace exists.
