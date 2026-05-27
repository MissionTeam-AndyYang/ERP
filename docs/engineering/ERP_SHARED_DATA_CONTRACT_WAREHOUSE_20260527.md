# ERP Shared Data Contract: Warehouse

Date: 2026-05-27
Scope: DB schema meaning, API dataset meaning and frontend field meaning for the first V1 Warehouse dashboard API.

## Purpose

This document is the shared language between frontend, backend and database work.

It connects:

- DB schema fields in `EWDB_20260526.sql` / `restserver/package/dbwrapper/table.py`
- API datasets for `GET /api/v1/warehouse/dashboard`
- Frontend runtime types in `src/types/warehouse.ts`
- Business meaning confirmed during ERP V1 planning

Use this document as the first backup/coordination layer between Codex and the backend engineer. When a field is unclear, mark it here before implementation assumptions spread into code.

## Ownership Split

| Area | Primary owner | Backup / reviewer |
| --- | --- | --- |
| Frontend UX, service layer and integration | Codex | Backend engineer reviews API contract impact |
| Backend restserver implementation | Backend engineer | Codex reviews code, contract and runtime result |
| DB schema meaning and source-of-truth fields | Backend engineer confirms | Codex documents and maps to frontend |
| API dataset naming and shape | Codex proposes from frontend needs | Backend engineer confirms implementation feasibility |
| Runtime verification | Backend engineer runs in DB environment | Codex reviews report and updates tracker |

## Endpoint

```txt
GET /api/v1/warehouse/dashboard
```

Required top-level datasets:

```txt
kpis
categorySummaries
capacities
records
risks
tasks
```

Supported response wrappers:

- Direct object: `{ "kpis": [], ... }`
- Restserver wrapper: `{ "code": 0, "message": "success", "payload": { "kpis": [], ... } }`
- Generic wrapper: `{ "data": { "kpis": [], ... } }`

## Business Terms

| Term | Meaning | Notes / open confirmation |
| --- | --- | --- |
| Current inventory | Current available stock by item, batch and warehouse/location. | Backend should confirm whether this is derived from `inventory_record`, `inventory_item_month_statistic`, or another source. |
| Inventory value | Monetary value of inventory. | Prefer stored `amount` if reliable; otherwise derive from quantity and price. Cost method needs confirmation. |
| Reserved quantity | Quantity already committed to orders/production/shipment. | Source not yet confirmed. |
| Available quantity | Quantity available for use after reservation/hold. | May be derived as on-hand minus reserved/hold after source confirmation. |
| Pallet count | Space usage unit for warehouse capacity planning. | Source/calculation needs confirmation. |
| Warehouse capacity | Total/used/reserved/available pallet positions in storage space. | Likely source: `ship_wh.maxCapacity` or related warehouse master data. |
| Turnover over one month | Inventory item/batch has not moved or has turnover cycle over 30 days. | Calculation rule needs confirmation. |
| Less than one-third shelf life | Remaining shelf life is below one-third of total valid days, excluding supplies/film categories. | Source likely `batch_number.validDays` and `batch_number.validDate`. |
| Below safety stock | Available stock is below safety threshold. | Safety stock source currently unknown. |
| Pending inbound/outbound | Today's warehouse tasks not completed. | Candidate source: `inventory_order`, `warehouse_record`, receiving/shipping related records. |

## DB Source Candidates

| Table / ORM class | Likely meaning | Important fields | Warehouse API usage |
| --- | --- | --- | --- |
| `inventory_record` / `CTableInventoryRec` | Raw inventory movement/record rows. | `group`, `refCategory`, `ref_no`, `warehouse_no`, `warehouse_displayName`, `date`, `source`, `category`, `batchNumber`, `serialNo`, `item_no`, `item_name`, `item_ref_no`, `item_ref_displayName`, `itemCategory`, `itemType`, `unit`, `count`, `price`, `amount` | Candidate source for `records`, current quantity, value, warehouse, source document and category. |
| `inventory_order` / `CTableInventoryOrder` | Inventory operation/order request. | `no`, `date`, `category`, `subCategory`, `item_no`, `item_name`, `expectedCount`, `checkedCount`, `amount` | Candidate source for pending `tasks`. |
| `inventory_item_month_statistic` / `CTableInventoryItemMonthStatistic` | Item-level monthly inventory statistics. | `warehouse_no`, `warehouse_displayName`, `date`, `timezone`, `kind`, `category`, `specified_no`, `specified_name`, `unit`, `startCount`, `startAmount`, `inCount`, `inAmount`, `endCount`, `endAmount` | Candidate source for `categorySummaries`, inventory value trend and category KPIs. |
| `inventory_month_statistic` / `CTableInventoryMonthStatistic` | Category-level monthly inventory value. | `warehouse_no`, `date`, `category`, `startAmount`, `inPurchaseAmount`, `inAmount`, `outAmount`, `endAmount` | Candidate source for high-level inventory value KPIs. |
| `inventory_delta` / `CTableInventoryDelta` | Inventory movement delta by date/warehouse/specified item. | `warehouse_no`, `date`, `kind`, `category`, `specified_no`, `inCount`, `inAmount`, `outCount`, `outAmount` | Candidate source for turnover and recent movement. |
| `batch_number` / `CTableBatchNumber` | Batch master. | `date`, `no`, `ref_no`, `refCategory`, `item_no`, `item_name`, `item_ref_no`, `itemCategory`, `itemSubCategory`, `itemType`, `unit`, `expectedCount`, `checkedCount`, `validDays`, `validDate` | Candidate source for `batchNo`, expiry, shelf-life, item category and source reference. |
| `batchno_serialno` / `CTableBatchNoSerialNo` | Batch serial/detail rows. | `batch_number`, `serialNo`, `ref_order_no`, `count`, `validDate`, `warehouse_no` | Candidate source for serial-level inventory detail if required later. |
| `ship_wh_alias` / `CTableShipWarehouseAlias` | Warehouse/storage alias/location group. | `no`, `name`, `category`, `type` | Candidate source for warehouse display and warehouse category/type. |
| `ship_wh` / `CTableShipWarehouse` | Warehousing service/storage master or warehouse contract item. | `no`, `company_no`, `name`, `category`, `attribute`, `maxCapacity`, `unit` | Candidate source for capacity if `maxCapacity` is pallet capacity. Needs confirmation. |
| `warehouse_record` / `CTableWarehouseRec` | Warehouse service/storage record. | `date`, `ref_no`, `batch_no`, `sw_alias_no`, `sw_alias_name`, `item_no`, `item_name`, `contract_no`, `inboundTime`, `unit`, `price`, `count`, `days` | Candidate source for warehouse tasks, inbound/storage days and pallet/storage usage if confirmed. |
| `goods_receipt_note` / `CTableGoodsReceiptNote` | Purchase receiving note. | `no`, `purchase_order_no`, `date`, `item_no`, `item_name`, `itemCategory`, `unit`, `expectedCount`, `checkedCount`, `amount` | Candidate inbound source document for `tasks` and `records`. |
| `shipping_order` / `CTableShippingOrder` | Shipment order. | `no`, `product_order_no`, `item_no`, `item_name`, quantity/date fields | Candidate outbound source document for `tasks`. |
| `item_price` / `CTableItemPrice` | Item price/cost reference. | `item_no`, `date`, price and unit fields | Candidate source for inventory value if `inventory_record.amount` is incomplete. |

## API Dataset Meaning

### `kpis`

Frontend type: `WarehouseKpi[]`

| API field | Meaning | Source / derivation | Status |
| --- | --- | --- | --- |
| `label` | Display label for KPI. | Backend can return agreed label or frontend can map from KPI key later. | V1 acceptable |
| `value` | Human-readable KPI value. | Derived from value/space/risk/task counts. | V1 acceptable |
| `hint` | Short explanation. | Backend or frontend wording. | V1 acceptable |
| `tone` | Status tone: `success`, `warning`, `danger`, `info`, `neutral`. | Derived from thresholds. | Needs threshold confirmation |

Recommended KPI meanings:

- Total inventory value.
- Used/available pallet positions.
- Active risk item count.
- Pending inbound/outbound task count.

### `categorySummaries`

Frontend type: `WarehouseCategorySummary[]`

| API field | Meaning | DB source / derivation | Status |
| --- | --- | --- | --- |
| `category` | Inventory category: raw material, supplies, film/roll, WIP, finished goods. | `itemCategory` / `itemSubCategory` mapping. | Needs enum mapping confirmation |
| `amount` | Total inventory value by category. | `inventory_item_month_statistic.endAmount` or sum of `inventory_record.amount`. | Needs source confirmation |
| `amountRatio` | Percentage of total inventory value. | `amount / totalAmount * 100`. | Derived |
| `reservedAmount` | Reserved inventory value. | Reserved source TBD. | Open |
| `availableAmount` | Available inventory value. | `amount - reservedAmount - holdAmount` if hold source exists. | Open |
| `palletCount` | Pallet usage by category. | Stored/derived pallet count TBD. | Open |
| `itemCount` | Number of distinct items in category. | Distinct item count. | Derivable |
| `trend7Days` | 7-day value change percentage. | `inventory_delta` or statistic snapshots. | Needs source confirmation |
| `tone` | Category status tone. | Threshold/risk derived. | Needs threshold confirmation |

### `capacities`

Frontend type: `WarehouseCapacity[]`

| API field | Meaning | DB source / derivation | Status |
| --- | --- | --- | --- |
| `id` | Warehouse capacity row id. | `ship_wh_alias.no` or `ship_wh.no`. | Needs confirmation |
| `warehouseName` | Warehouse/storage display name. | `ship_wh_alias.name`, `ship_wh.name`, or `warehouse_displayName`. | Needs confirmation |
| `warehouseType` | Storage type/category. | `ship_wh_alias.type/category` or `ship_wh.category/attribute`. | Needs enum mapping |
| `totalPallets` | Total capacity in pallet positions. | `ship_wh.maxCapacity` if confirmed. | Open |
| `usedPallets` | Used pallet positions. | Sum stored/derived pallet usage. | Open |
| `reservedPallets` | Reserved pallet positions. | Reservation source TBD. | Open |
| `availablePallets` | Remaining pallet positions. | `totalPallets - usedPallets - reservedPallets`. | Derived after source confirmation |
| `tone` | Capacity risk tone. | Used ratio threshold. | Needs threshold confirmation |

### `records`

Frontend type: `WarehouseRecord[]`

| API field | Meaning | DB source / derivation | Status |
| --- | --- | --- | --- |
| `id` | UI record id. | `inventory_record.id` or generated from item/batch/warehouse. | Confirm preferred key |
| `itemNo` | Item number. | `inventory_record.item_no` / `batch_number.item_no`. | Likely confirmed |
| `itemName` | Item name. | `inventory_record.item_name` / `batch_number.item_name`. | Likely confirmed |
| `category` | Frontend category label. | Map from `itemCategory` / `itemSubCategory`. | Needs enum mapping |
| `warehouseNo` | Warehouse/location number. | `inventory_record.warehouse_no`. | Likely confirmed |
| `warehouseName` | Warehouse/location name. | `inventory_record.warehouse_displayName`. | Likely confirmed |
| `batchNo` | Batch number. | `inventory_record.batchNumber` / `batch_number.no`. | Likely confirmed |
| `sourceType` | Purchase/production/shipment/adjustment. | Map from `refCategory` / `source` / source table. | Needs enum mapping |
| `sourceNo` | Source document number. | `inventory_record.ref_no`. | Likely confirmed |
| `quantity` | On-hand quantity. | Sum movement counts or latest statistic. | Needs calculation rule |
| `reservedQuantity` | Reserved quantity. | TBD. | Open |
| `availableQuantity` | Available quantity. | Derived after reserved/hold source confirmation. | Open |
| `unit` | Display unit. | Map from numeric `unit` enum. | Needs enum mapping |
| `amount` | Inventory value. | `inventory_record.amount` or derived. | Needs source confirmation |
| `reservedAmount` | Reserved value. | TBD. | Open |
| `availableAmount` | Available value. | Derived. | Open |
| `palletCount` | Pallet count. | Stored/derived TBD. | Open |
| `safetyStock` | Safety stock threshold. | TBD. | Open |
| `expiryDate` | Expiry date display. | `batch_number.validDate`. | Likely source; date format conversion needed |
| `shelfLifeDays` | Total shelf-life days. | `batch_number.validDays`. | Likely source |
| `daysLeft` | Days until expiry. | `validDate - today`. | Derived |
| `turnoverDays` | Days since last movement or turnover cycle. | `inventory_delta` or latest movement date. | Needs rule |
| `status` | Business status. | Derived from risk/hold/availability. | Needs mapping |
| `tone` | UI status tone. | Derived from status. | Needs mapping |
| `workflow` | Related workflow steps. | Derived from source records. | Optional for first backend API |
| `relatedDocuments` | Source documents. | `ref_no`, GRN, PO, WO, shipping, contract. | Optional first version |

### `risks`

Frontend type: `WarehouseRisk[]`

| API field | Meaning | Source / derivation | Status |
| --- | --- | --- | --- |
| `id` | Risk id. | Generated from risk type + batch/item. | Derivable |
| `type` | Risk category. | One of turnover, shelf-life, low safety stock. | Confirm labels or use frontend mapping |
| `itemName` | Item name. | Inventory/batch source. | Likely confirmed |
| `category` | Inventory category. | Item category mapping. | Needs enum mapping |
| `batchNo` | Batch number. | `batch_number.no`. | Likely confirmed |
| `warehouseName` | Warehouse name. | Inventory/warehouse source. | Likely confirmed |
| `metric` | Human-readable risk metric. | Derived, e.g. `turnover 45 days`, `days left 12`. | Backend or frontend wording |
| `recommendation` | Suggested action. | Rule-based text. | Can be frontend-generated later |
| `tone` | Warning/danger/info. | Threshold derived. | Needs threshold confirmation |

Risk rules to confirm:

- Turnover risk: `turnoverDays > 30`.
- Shelf-life risk: `daysLeft / shelfLifeDays < 1/3`, excluding supplies and film/roll.
- Safety stock risk: `availableQuantity < safetyStock`.

### `tasks`

Frontend type: `WarehouseTask[]`

| API field | Meaning | Source / derivation | Status |
| --- | --- | --- | --- |
| `id` | Task id. | Source record id or generated id. | Confirm preferred key |
| `type` | Inbound/outbound/move/count. | Source category mapping. | Needs enum mapping |
| `itemName` | Item name. | Source record. | Likely confirmed |
| `batchNo` | Batch number. | Source record / batch. | Likely confirmed |
| `quantity` | Task quantity. | `expectedCount`, `checkedCount`, `count`. | Needs source selection |
| `unit` | Unit label. | Unit enum mapping. | Needs enum mapping |
| `palletCount` | Task pallet count. | Stored/derived TBD. | Open |
| `owner` | Responsible person/team. | `creator_no`, assigned user, or department default. | Open |
| `dueTime` | Due time display. | Date/time source. | Needs source/format |
| `sourceNo` | Source document number. | PO/GRN/WO/shipping/inventory order. | Needs source mapping |
| `status` | Task status. | Source workflow/status field. | Open |
| `tone` | UI status tone. | Derived from status/time risk. | Needs mapping |

## Enum Mapping Needed

These numeric/backend enums must be translated into frontend labels:

| Backend field | Frontend meaning | Status |
| --- | --- | --- |
| `itemCategory` | `InventoryCategory` | Need mapping to 原料 / 物料 / 膠捲 / 在製品 / 製成品. |
| `itemSubCategory` | More detailed item grouping | Optional for V1. |
| `unit` | Display unit string | Need mapping from backend `EUnit`. |
| `refCategory` | Source type / source document domain | Need mapping. |
| `source` | Inventory source/reason | Need mapping. |
| `category` on inventory records | In/out/movement category | Need mapping. |
| Warehouse `category/type/attribute` | Warehouse/storage type | Need mapping. |

## API Get/Set Dataset Policy

V1 Warehouse dashboard is read-only:

| Operation | Dataset | Status |
| --- | --- | --- |
| GET | `kpis`, `categorySummaries`, `capacities`, `records`, `risks`, `tasks` | Required |
| POST | none | Not in V1 scope |
| PUT | none | Not in V1 scope |
| DELETE | none | Not in V1 scope |

Future mutation APIs should be documented separately when workflows are ready, for example inbound confirmation, outbound confirmation, warehouse transfer or cycle count.

## Open Questions For Engineer

| ID | Question | Blocking level |
| --- | --- | --- |
| Q1 | Is `ship_wh.maxCapacity` the correct source for total warehouse/storage capacity? | Blocks accurate `capacities`. |
| Q2 | Which table/field stores reserved quantity or reservation by order/work order/shipment? | Blocks `reservedQuantity` and `availableQuantity`. |
| Q3 | Which table/field stores safety stock? | Blocks low-stock risk. |
| Q4 | Should inventory value use `inventory_record.amount`, `inventory_item_month_statistic.endAmount`, or latest `item_price`? | Blocks value accuracy. |
| Q5 | Which field indicates quality hold/release? | Blocks quality-hold risk and available stock calculation. |
| Q6 | What are the official mappings for `itemCategory`, `unit`, `refCategory`, `source` and inventory `category`? | Blocks stable frontend labels. |
| Q7 | What is the task status source for pending inbound/outbound? | Blocks `tasks.status`. |
| Q8 | Should backend return display labels, or return enum codes plus frontend maps labels? | Important for I18N and maintainability. |

## Current Agreement

| Topic | Decision |
| --- | --- |
| Frontend owner | Codex owns frontend design, service layer and API integration. |
| Backend owner | Engineer owns restserver implementation; Codex reviews code and runtime reports. |
| Shared contract | This document is the first shared DB/API/frontend contract for Warehouse. |
| First API | Start with `GET /api/v1/warehouse/dashboard`. |
| Wrapper | Restserver `{ payload: ... }` wrapper is supported by frontend and verifier. |
| Verification | Use `scripts/verify_v1_api_contracts.py --module warehouse`. |

