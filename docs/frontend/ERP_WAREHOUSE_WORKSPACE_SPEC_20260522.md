# ERP Warehouse Workspace Spec

日期：2026-05-23

## Status

Warehouse first-version direction confirmed with the user and updated in code.

- Page: `src/app/warehouse/page.tsx`
- Mock data: `src/mock/warehouse.ts`
- Types: `src/types/warehouse.ts`

## User Focus

The first Warehouse page is a management-oriented warehouse dashboard, not a full warehouse CRUD screen.

User-confirmed focus areas:

1. Current inventory value by category: 原料、物料、膠捲、在製品、製成品.
2. Current pallet usage by category and remaining warehouse pallet capacity.
3. Inventory risk and warning:
   - Turnover cycle over one month.
   - Less than one-third shelf life remaining, excluding 物料 and 膠捲.
   - Below safety stock.
4. Today's pending inbound/outbound warehouse work.

## First-Version Goal

Help management answer four questions:

1. Where is inventory capital tied up?
2. Which warehouse spaces are close to capacity?
3. Which inventory items are stale, near expiry, or below safety stock?
4. Which inbound/outbound tasks are still pending today?

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 價值與倉位 | Inventory value, category value ratio, category pallet usage, warehouse available pallets |
| 風險警示 | Turnover over one month, less than one-third shelf life, below safety stock |
| 待處理入出庫 | Today's pending inbound, outbound, transfer, and confirmation tasks |
| 庫存明細 | Batch/item/warehouse/source/detail table with selected workflow panel |

## Data Shape

Inventory detail records are shaped around:

- `itemNo`, `itemName`, `category`
- `warehouseNo`, `warehouseName`
- `batchNo`
- `sourceType`, `sourceNo`
- `quantity`, `unit`, `amount`
- `palletCount`
- `safetyStock`
- `expiryDate`, `shelfLifeDays`, `daysLeft`
- `turnoverDays`
- `workflow`
- `relatedDocuments`

Category summary records are shaped around:

- `category`
- `amount`
- `amountRatio`
- `palletCount`
- `itemCount`

Warehouse capacity records are shaped around:

- `warehouseName`
- `warehouseType`
- `totalPallets`
- `usedPallets`
- `reservedPallets`
- `availablePallets`

Risk records are shaped around:

- `type`
- `itemName`, `category`, `batchNo`, `warehouseName`
- `metric`
- `recommendation`

Task records are shaped around:

- `type`
- `itemName`, `batchNo`
- `quantity`, `unit`, `palletCount`
- `owner`, `dueTime`, `sourceNo`, `status`

## Workflow Basis

```txt
purchase_order -> goods_receipt_note -> batch_number -> inventory_record -> warehouse_record
work_order / process_order -> batch_number -> inventory_record -> production_data
product_order -> shipping_order -> shipping_record
```

Warehouse should show whether stock came from purchasing, production, or another inventory movement.

## First-Version Scope

Included:

- Management KPI strip.
- Inventory value by category.
- Pallet usage by category.
- Warehouse capacity and available pallet count.
- Three warehouse risk groups.
- Today's pending inbound/outbound/transfer tasks.
- Inventory detail table.
- Selected batch detail and workflow panel.

Deferred:

- Warehouse rent/payment detail.
- Actual storage fee calculation.
- Automatic external warehouse placement recommendation.
- Inventory adjustment, transfer, and stocktaking write actions.
- Full gross margin calculation.

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| Inventory list | `inventory` |
| Batch list/detail | `batchnumber`, `batchtrace` |
| Warehouse capacity | `shipwarehouse` |
| Pending inbound/outbound tasks | `inventory`, `purchase`, `sale`, `workorder` |
| Goods receipt source | `purchase` |
| Production source | `workorder`, `work`, `processorder` |
| Shipping source | `sale`, `shipwarehouse` |

## Next Integration Steps

1. Add a Warehouse API adapter that returns the current mock shape.
2. Connect list data first; keep write actions disabled.
3. Confirm how pallet count is stored or derived in EWDB/restserver.
4. Confirm safety stock source table/field.
5. Confirm expiry and shelf-life calculation rules by category.
