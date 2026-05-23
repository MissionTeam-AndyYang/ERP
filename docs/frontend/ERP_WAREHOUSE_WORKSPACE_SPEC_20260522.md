# ERP Warehouse Workspace Spec

日期：2026-05-23

## Status

Warehouse first-version direction confirmed with the user and updated in code.

- Page: `src/app/warehouse/page.tsx`
- Mock data: `src/mock/warehouse.ts`
- Types: `src/types/warehouse.ts`

## User Focus

The first Warehouse page is a management-oriented warehouse dashboard, not a full warehouse CRUD screen.

Department ownership clarified by the user: after Purchasing completes material purchasing, Warehouse owns arrival receiving / inbound storage. Quality then performs material inspection before materials become available for production.

User-confirmed focus areas:

1. Current inventory value by category: 原料、物料、膠捲、在製品、製成品.
2. Current pallet usage by category and remaining warehouse pallet capacity.
3. Inventory risk and warning:
   - Turnover cycle over one month.
   - Less than one-third shelf life remaining, excluding 物料 and 膠捲.
   - Below safety stock.
4. Today's pending inbound/outbound warehouse work.
5. Production material arrival receiving and warehouse handoff status.

Additional first-version additions:

1. Distinguish current quantity, reserved quantity, and available quantity.
2. Distinguish total value, reserved value, and available value.
3. Show 7-day inventory value trend by category.
4. Keep batch trace entry visible for purchase/production/shipping source review.

## First-Version Goal

Help management answer five questions:

1. Where is inventory capital tied up?
2. Which warehouse spaces are close to capacity?
3. How much inventory is actually available after reservations?
4. Which inventory items are stale, near expiry, or below safety stock?
5. Which inbound/outbound tasks are still pending today?

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 價值與倉位 | Inventory value, reserved/available value, category value ratio, 7-day value trend, pallet usage, warehouse available pallets |
| 風險警示 | Turnover over one month, less than one-third shelf life, below safety stock |
| 待處理入出庫 | Today's pending inbound, outbound, transfer, and confirmation tasks |
| 庫存明細 | Batch/item/warehouse/source table with current/reserved/available quantity and selected workflow panel |

Post-order receiving workflow:

```txt
material purchasing -> arrival -> warehouse receiving -> quality material inspection -> available inventory / blocked inventory
```

## Data Shape

Inventory detail records are shaped around:

- `itemNo`, `itemName`, `category`
- `warehouseNo`, `warehouseName`
- `batchNo`
- `sourceType`, `sourceNo`
- `quantity`, `reservedQuantity`, `availableQuantity`, `unit`
- `amount`, `reservedAmount`, `availableAmount`
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
- `reservedAmount`
- `availableAmount`
- `palletCount`
- `itemCount`
- `trend7Days`

Warehouse capacity records are shaped around:

- `warehouseName`
- `warehouseType`
- `totalPallets`
- `usedPallets`
- `reservedPallets`
- `availablePallets`

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| Inventory list | `inventory` |
| Reserved/available inventory | `inventory`, `workorder`, `sale`, `shipwarehouse` |
| Batch list/detail | `batchnumber`, `batchtrace` |
| Warehouse capacity | `shipwarehouse` |
| Pending inbound/outbound tasks | `inventory`, `purchase`, `sale`, `workorder` |
| Value trend | inventory ledger or daily snapshot API |
| Purchase arrival receiving | `goods_receipt_note`, `purchase`, `inventory` |
| Quality release/block after receiving | quality-related tables, `batchnumber`, `inventory` |

## Next Integration Steps

1. Add a Warehouse API adapter that returns the current mock shape.
2. Confirm how pallet count is stored or derived.
3. Confirm safety stock source table/field.
4. Confirm reservation logic from production orders, sales orders, and pending warehouse tasks.
5. Confirm whether daily inventory value trend comes from snapshots or calculated ledger history.
