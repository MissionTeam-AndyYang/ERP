# Warehouse Dashboard API Proposal

Status: Draft / Need Engineer Review
Date: 2026-06-10
Owner: Frontend UX / API design proposal
Target Reviewers: Backend engineer, DB schema owner

## Purpose

This document defines the proposed read-only Warehouse dashboard APIs based on the approved ERP V1 frontend UX. It is intentionally separated from `docs/spec/api/` because the endpoints below are proposed APIs, not confirmed restserver implementations.

The goal is to let frontend and backend review the same dataset, field semantics, processing flow, and algorithm before implementation.

## UX Scope

The Warehouse first-version page is a management dashboard for:

1. Current inventory value by item category: raw materials, supplies, film, WIP, finished goods.
2. Pallet usage and available warehouse capacity.
3. Inventory risks: turnover over one month, remaining shelf life less than one-third, below safety stock.
4. Today's pending inbound and outbound warehouse tasks.
5. Batch-level traceability for purchase, production, shipping, and warehouse source documents.

## API Summary

| URL | Method | Description | Status | Review Note |
| --- | --- | --- | --- | --- |
| `/api/v1/warehouse/dashboard` | GET | Query Warehouse dashboard aggregate datasets for management view | Proposal | Needs engineer review before implementation |
| `/api/v1/warehouse/inventory` | GET | Query Warehouse inventory detail rows for drill-down and table view | Proposal | Can be implemented together with dashboard or as separate detail API |
| `/api/v1/warehouse/tasks` | GET | Query today's pending Warehouse inbound/outbound/transfer tasks | Proposal | Task source and status algorithm need engineer confirmation |

## Shared Response Wrapper

Proposed response wrapper follows current restserver convention:

```json
{
  "code": "Integer",
  "message": "String",
  "payload": "Object"
}
```

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| code | Integer | API result code. `0` means success. | `EErrorCode.ERROR_SUCCESS = 0` |
| message | String | API result message. |  |
| payload | Object | API-specific response payload. |  |

## GET /api/v1/warehouse/dashboard

<a id="get-api-v1-warehouse-dashboard"></a>

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v1/warehouse/dashboard` | GET | Query Warehouse dashboard aggregate datasets for management view |

### Request Header

| Header | Description |
| --- | --- |
| x-auth-token | Access token |

### Query Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| date | Integer | NO | Dashboard reference timestamp. Default is current server time. The API converts it to the user's local day range by timezone. |
| timezone | String | NO | User timezone. Default should follow restserver timezone handling, for example `Asia/Taipei`. |
| warehouse_no | String | NO | Filter by warehouse alias number. References `ship_wh_alias.no`. |
| itemCategory | Integer | NO | Filter by item category. |
| includeInventory | Boolean | NO | Whether to include detail inventory rows in the dashboard payload. Default: `false`. |
| riskOnly | Boolean | NO | Whether to return only rows with inventory risks. Default: `false`. |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "timezone": "String",
    "range": {
      "date": "String",
      "startTimestamp": "Integer",
      "endTimestamp": "Integer"
    },
    "summary": {
      "totalInventoryValue": "Float",
      "reservedInventoryValue": "Float",
      "availableInventoryValue": "Float",
      "qualityHoldInventoryValue": "Float",
      "totalPallets": "Integer",
      "usedPallets": "Integer",
      "reservedPallets": "Integer",
      "availablePallets": "Integer",
      "riskAlertCount": "Integer",
      "pendingInboundCount": "Integer",
      "pendingOutboundCount": "Integer"
    },
    "inventoryValueByCategory": [
      {
        "itemCategory": "Integer",
        "categoryName": "String",
        "inventoryValue": "Float",
        "reservedValue": "Float",
        "availableValue": "Float",
        "qualityHoldValue": "Float",
        "quantity": "Float",
        "unit": "Integer",
        "palletCount": "Integer",
        "itemCount": "Integer",
        "valueRatio": "Float",
        "trend7Days": "Float"
      }
    ],
    "capacityByWarehouse": [
      {
        "warehouseNo": "String",
        "warehouseName": "String",
        "warehouseType": "Integer",
        "totalPallets": "Integer",
        "usedPallets": "Integer",
        "reservedPallets": "Integer",
        "availablePallets": "Integer",
        "utilizationRate": "Float",
        "riskLevel": "String"
      }
    ],
    "riskAlerts": [
      {
        "alertId": "String",
        "riskType": "String",
        "riskLevel": "String",
        "itemNo": "String",
        "itemName": "String",
        "itemCategory": "Integer",
        "batchNo": "String",
        "warehouseNo": "String",
        "warehouseName": "String",
        "quantity": "Float",
        "unit": "Integer",
        "inventoryValue": "Float",
        "daysInStock": "Integer",
        "validDate": "Integer",
        "remainingShelfLifeRatio": "Float",
        "safetyStock": "Float",
        "message": "String",
        "recommendedAction": "String"
      }
    ],
    "pendingTasks": [
      {
        "taskId": "String",
        "taskType": "String",
        "sourceType": "String",
        "sourceNo": "String",
        "sourceSubNo": "String",
        "itemNo": "String",
        "itemName": "String",
        "itemCategory": "Integer",
        "batchNo": "String",
        "expectedQuantity": "Float",
        "processedQuantity": "Float",
        "unit": "Integer",
        "palletCount": "Integer",
        "warehouseNo": "String",
        "warehouseName": "String",
        "dueTimestamp": "Integer",
        "status": "String",
        "ownerDepartment": "String"
      }
    ],
    "valueTrend": [
      {
        "date": "String",
        "itemCategory": "Integer",
        "categoryName": "String",
        "inventoryValue": "Float"
      }
    ],
    "inventory": [
      {
        "inventoryId": "String",
        "warehouseNo": "String",
        "warehouseName": "String",
        "itemNo": "String",
        "itemName": "String",
        "itemCategory": "Integer",
        "itemType": "Integer",
        "batchNo": "String",
        "serialNo": "String",
        "currentQuantity": "Float",
        "reservedQuantity": "Float",
        "availableQuantity": "Float",
        "qualityHoldQuantity": "Float",
        "unit": "Integer",
        "unitCost": "Float",
        "inventoryValue": "Float",
        "reservedValue": "Float",
        "availableValue": "Float",
        "palletCount": "Integer",
        "safetyStock": "Float",
        "validDays": "Integer",
        "validDate": "Integer",
        "firstInboundTimestamp": "Integer",
        "daysInStock": "Integer",
        "sourceType": "String",
        "sourceNo": "String",
        "qualityStatus": "String"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| payload.serverTimestamp | Integer | Server time when the dashboard dataset is generated. |  |
| payload.timezone | String | Timezone used to calculate the dashboard date range. |  |
| payload.range.date | String | Dashboard business date in `YYYY-MM-DD` format. |  |
| payload.range.startTimestamp | Integer | Start timestamp of the dashboard date range. |  |
| payload.range.endTimestamp | Integer | End timestamp of the dashboard date range. |  |
| payload.summary.totalInventoryValue | Float | Total on-hand inventory value across selected warehouses and categories. |  |
| payload.summary.reservedInventoryValue | Float | Inventory value reserved by orders, production material allocation, or pending warehouse tasks. | Need engineer confirmation |
| payload.summary.availableInventoryValue | Float | Inventory value available for production or shipment after reservation and quality hold deduction. | Need engineer confirmation |
| payload.summary.qualityHoldInventoryValue | Float | Inventory value not yet released because of material/item inspection or quality hold. | Need engineer confirmation |
| payload.summary.totalPallets | Integer | Total pallet capacity for selected warehouses. | Need engineer confirmation |
| payload.summary.usedPallets | Integer | Pallets currently occupied by inventory batches. |  |
| payload.summary.reservedPallets | Integer | Pallets reserved for pending inbound/outbound/transfer work. | Need engineer confirmation |
| payload.summary.availablePallets | Integer | Pallet capacity still available after occupied and reserved pallets. | Need engineer confirmation |
| payload.summary.riskAlertCount | Integer | Total number of risk alert rows generated by the dashboard rules. |  |
| payload.summary.pendingInboundCount | Integer | Number of inbound warehouse tasks not fully processed for the dashboard date. | Need engineer confirmation |
| payload.summary.pendingOutboundCount | Integer | Number of outbound warehouse tasks not fully processed for the dashboard date. | Need engineer confirmation |
| payload.inventoryValueByCategory[].itemCategory | Integer | Item category code. | 原料(1), 物料(2), 膠捲(3), 在製品(4), 製成品(5), 貨品(6), 其他(0) |
| payload.inventoryValueByCategory[].categoryName | String | Display name of the item category. |  |
| payload.inventoryValueByCategory[].inventoryValue | Float | Current inventory value for this category. Can align with `inventory_month_statistic.endAmount` or real-time stock calculation. | Need engineer confirmation |
| payload.inventoryValueByCategory[].reservedValue | Float | Reserved inventory value for this category. | Need engineer confirmation |
| payload.inventoryValueByCategory[].availableValue | Float | Available inventory value for this category. | Need engineer confirmation |
| payload.inventoryValueByCategory[].qualityHoldValue | Float | Quality-held inventory value for this category. | Need engineer confirmation |
| payload.inventoryValueByCategory[].quantity | Float | Current inventory quantity for this category. |  |
| payload.inventoryValueByCategory[].unit | Integer | Inventory unit code when category summary can be represented by one unit. Use `0` when mixed units exist. | Unit enum |
| payload.inventoryValueByCategory[].palletCount | Integer | Pallets occupied by this category. |  |
| payload.inventoryValueByCategory[].itemCount | Integer | Number of distinct item numbers in this category. |  |
| payload.inventoryValueByCategory[].valueRatio | Float | Category inventory value divided by total inventory value. |  |
| payload.inventoryValueByCategory[].trend7Days | Float | Seven-day inventory value change rate for this category. | Need engineer confirmation |
| payload.capacityByWarehouse[].warehouseNo | String | Warehouse alias number. References `ship_wh_alias.no`. |  |
| payload.capacityByWarehouse[].warehouseName | String | Warehouse alias display name. |  |
| payload.capacityByWarehouse[].warehouseType | Integer | Warehouse alias type. | 自有(1), 合約(2), 客供(3), 其他(0) |
| payload.capacityByWarehouse[].totalPallets | Integer | Total pallet capacity of the warehouse or warehouse alias. | Need engineer confirmation |
| payload.capacityByWarehouse[].usedPallets | Integer | Current occupied pallets. Can be derived from `batchno_serialno_group.group` count by warehouse if confirmed. | Need engineer confirmation |
| payload.capacityByWarehouse[].reservedPallets | Integer | Pallets reserved for pending tasks. | Need engineer confirmation |
| payload.capacityByWarehouse[].availablePallets | Integer | Available pallet capacity. | Need engineer confirmation |
| payload.capacityByWarehouse[].utilizationRate | Float | Used pallets divided by total pallets. |  |
| payload.capacityByWarehouse[].riskLevel | String | Capacity risk level for UI tone mapping. | `normal`, `warning`, `danger` |
| payload.riskAlerts[].alertId | String | Stable alert identifier generated from risk type, warehouse, item, and batch. |  |
| payload.riskAlerts[].riskType | String | Risk category. | `TURNOVER_OVER_30_DAYS`, `SHELF_LIFE_LT_ONE_THIRD`, `BELOW_SAFETY_STOCK` |
| payload.riskAlerts[].riskLevel | String | Risk severity. | `normal`, `warning`, `danger` |
| payload.riskAlerts[].itemNo | String | Item number. |  |
| payload.riskAlerts[].itemName | String | Item name. |  |
| payload.riskAlerts[].itemCategory | Integer | Item category code. | EItemCategory |
| payload.riskAlerts[].batchNo | String | Batch number. References `batch_number.no`. |  |
| payload.riskAlerts[].warehouseNo | String | Warehouse alias number. |  |
| payload.riskAlerts[].warehouseName | String | Warehouse alias display name. |  |
| payload.riskAlerts[].quantity | Float | Current quantity for the alert item/batch/warehouse. |  |
| payload.riskAlerts[].unit | Integer | Inventory unit code. | Unit enum |
| payload.riskAlerts[].inventoryValue | Float | Current inventory value for the alert item/batch/warehouse. |  |
| payload.riskAlerts[].daysInStock | Integer | Days from first inbound timestamp to dashboard date. |  |
| payload.riskAlerts[].validDate | Integer | Expiry timestamp from batch data. |  |
| payload.riskAlerts[].remainingShelfLifeRatio | Float | Remaining shelf-life ratio. |  |
| payload.riskAlerts[].safetyStock | Float | Safety stock threshold used for below-safety-stock calculation. | Need engineer confirmation |
| payload.riskAlerts[].message | String | Business-readable alert message. |  |
| payload.riskAlerts[].recommendedAction | String | Suggested operational action for UI display. |  |
| payload.pendingTasks[].taskId | String | Stable task identifier generated from task type and source document. |  |
| payload.pendingTasks[].taskType | String | Warehouse task type. | `INBOUND`, `OUTBOUND`, `TRANSFER`, `COUNTING` |
| payload.pendingTasks[].sourceType | String | Source document category. | `PURCHASE`, `SALE`, `WORK`, `INVENTORY`, `OTHER` |
| payload.pendingTasks[].sourceNo | String | Source document number. |  |
| payload.pendingTasks[].sourceSubNo | String | Source document line/sub number if available. |  |
| payload.pendingTasks[].itemNo | String | Item number for the task. |  |
| payload.pendingTasks[].itemName | String | Item name for the task. |  |
| payload.pendingTasks[].itemCategory | Integer | Item category code. | EItemCategory |
| payload.pendingTasks[].batchNo | String | Batch number for the task, if already created. |  |
| payload.pendingTasks[].expectedQuantity | Float | Quantity expected by the source document. |  |
| payload.pendingTasks[].processedQuantity | Float | Quantity already processed in warehouse inventory records. |  |
| payload.pendingTasks[].unit | Integer | Task unit. | Unit enum |
| payload.pendingTasks[].palletCount | Integer | Pallet count related to this task. | Need engineer confirmation |
| payload.pendingTasks[].warehouseNo | String | Target or source warehouse alias number. |  |
| payload.pendingTasks[].warehouseName | String | Target or source warehouse alias display name. |  |
| payload.pendingTasks[].dueTimestamp | Integer | Expected processing time. |  |
| payload.pendingTasks[].status | String | Task processing status. | `pending`, `partial`, `done`, `blocked` |
| payload.pendingTasks[].ownerDepartment | String | Department responsible for next action. | Warehouse, Quality, Planning, Sales, Purchasing |
| payload.valueTrend[].date | String | Trend date in `YYYY-MM-DD` format. |  |
| payload.valueTrend[].itemCategory | Integer | Item category code. | EItemCategory |
| payload.valueTrend[].categoryName | String | Display name of the item category. |  |
| payload.valueTrend[].inventoryValue | Float | Inventory value on the trend date. |  |
| payload.inventory[].inventoryId | String | Stable inventory row id generated from warehouse, item, batch, and serial data. |  |
| payload.inventory[].warehouseNo | String | Warehouse alias number. |  |
| payload.inventory[].warehouseName | String | Warehouse alias display name. |  |
| payload.inventory[].itemNo | String | Item number. |  |
| payload.inventory[].itemName | String | Item name. |  |
| payload.inventory[].itemCategory | Integer | Item category code. | EItemCategory |
| payload.inventory[].itemType | Integer | Item type code. | 新料(1), 餘料(2), 廢料(3), 其他(0) |
| payload.inventory[].batchNo | String | Batch number. |  |
| payload.inventory[].serialNo | String | Serial number when detail is serial-level. Empty when row is batch-level. |  |
| payload.inventory[].currentQuantity | Float | On-hand quantity calculated as inbound quantity minus outbound quantity. |  |
| payload.inventory[].reservedQuantity | Float | Quantity reserved by sales, production, or pending warehouse tasks. | Need engineer confirmation |
| payload.inventory[].availableQuantity | Float | Current quantity minus reserved quantity and quality-hold quantity. | Need engineer confirmation |
| payload.inventory[].qualityHoldQuantity | Float | Quantity not released by quality inspection. | Need engineer confirmation |
| payload.inventory[].unit | Integer | Inventory unit code. | Unit enum |
| payload.inventory[].unitCost | Float | Unit cost used for inventory value. | Need engineer confirmation |
| payload.inventory[].inventoryValue | Float | Current inventory value. |  |
| payload.inventory[].reservedValue | Float | Reserved inventory value. | Need engineer confirmation |
| payload.inventory[].availableValue | Float | Available inventory value. | Need engineer confirmation |
| payload.inventory[].palletCount | Integer | Pallet count occupied by this inventory row. | Need engineer confirmation |
| payload.inventory[].safetyStock | Float | Safety stock threshold. | Need engineer confirmation |
| payload.inventory[].validDays | Integer | Shelf-life days from batch data. |  |
| payload.inventory[].validDate | Integer | Expiry timestamp from batch data. |  |
| payload.inventory[].firstInboundTimestamp | Integer | Earliest inbound inventory record date for this warehouse and batch. |  |
| payload.inventory[].daysInStock | Integer | Days between first inbound timestamp and dashboard date. |  |
| payload.inventory[].sourceType | String | Original business source of the inventory row. | `PURCHASE`, `SALE`, `WORK`, `INVENTORY`, `OTHER` |
| payload.inventory[].sourceNo | String | Source document number. |  |
| payload.inventory[].qualityStatus | String | Quality release state used for availability calculation. | Need engineer confirmation |

### Failed Response Data

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| code | Integer | API error code. |  |
| message | String | API error message. |  |
| payload | Object | Error payload. Usually empty if no detailed error fields are defined. |  |

### Processing Flow

1. Read `date`, `timezone`, `warehouse_no`, `itemCategory`, `includeInventory`, and `riskOnly` query parameters and normalize them into dashboard filter conditions.
2. Convert the dashboard reference timestamp into a local business-day range by timezone.
3. Retrieve current inventory quantity and value by warehouse, category, item, and batch. Candidate sources are `inventory_record`, `inventory_delta`, `inventory_item_month_statistic`, and `inventory_month_statistic`.
4. Join batch-level data from `batch_number` to obtain batch number, item information, valid days, valid date, checked quantity, and source document relation.
5. Calculate current quantity as inbound inventory quantity minus outbound inventory quantity.
6. Calculate current inventory value by row and category. Preferred source must be confirmed: existing `inventory_record.amount`, real-time stock amount, or `inventory_month_statistic.endAmount`.
7. Calculate reserved quantity and available quantity after confirming reservation source of truth.
8. Calculate quality-hold quantity after confirming quality inspection release/hold source.
9. Calculate pallet usage by warehouse and category. Candidate source is `batchno_serialno_group.group`, grouped by `warehouse_no`, but total capacity source still needs confirmation.
10. Calculate Warehouse risk alerts:
    - `TURNOVER_OVER_30_DAYS`: `daysInStock > 30`.
    - `SHELF_LIFE_LT_ONE_THIRD`: remaining shelf life is less than or equal to one-third of valid days; exclude item categories `MA` and `AF` if this rule is confirmed.
    - `BELOW_SAFETY_STOCK`: current or available quantity is below safety stock threshold after the safety stock source is confirmed.
11. Retrieve today's pending inbound and outbound warehouse tasks by comparing source document expected quantity against processed inventory records.
12. Build management dashboard datasets: summary, category value, capacity, risk alerts, pending tasks, value trend, and optional inventory detail rows.

### Database Tables Used

| Table | Purpose |
| --- | --- |
| inventory_record | Provides inventory movement records for current stock, inbound/outbound quantities, warehouse, item, batch, source document, price, and amount calculations. |
| inventory_delta | Provides daily inventory movement aggregates when dashboard value or trend can reuse committed daily statistics. |
| inventory_item_month_statistic | Provides item-level monthly/current inventory quantity and value snapshots used by existing `/api/v1/inventory/items`. |
| inventory_month_statistic | Provides category-level monthly inventory values used by existing `/api/v1/inventory/months`. |
| batch_number | Provides batch, item, source document, valid days, valid date, unit, expected quantity, and checked quantity. |
| batchno_serialno | Provides serial-level batch and warehouse relation when inventory detail must be expanded below batch level. |
| batchno_serialno_group | Provides pallet group relation between warehouse, batch, and serial numbers. Candidate source for occupied pallet count. |
| ship_wh_alias | Provides warehouse alias number, warehouse name, and warehouse type used in dashboard capacity grouping. |
| ship_wh | Provides warehouse or logistics master item when warehouse capacity or contract linkage needs the warehouse item definition. |
| ship_wh_contract | Provides warehouse contract and warehouse service metadata when capacity or warehouse cost is contract-based. |
| warehouse_record | Provides warehouse service/storage records and warehouse rental calculation records; may support pallet/day usage analysis. |
| goods_receipt_note | Candidate source for pending purchase inbound tasks. |
| shipping_order | Candidate source for pending sales outbound tasks. |
| process_order | Candidate source for production material issue, return, remaining, waste, and product inbound/outbound tasks. |
| inventory_order | Candidate source for manual inventory inbound/outbound/transfer/counting tasks. |
| item_price | Candidate source for unit cost when inventory value cannot rely on inventory movement amount. |

### Algorithm Review Notes

| Topic | Proposed Rule | Review Status |
| --- | --- | --- |
| Current quantity | Sum `inventory_record.count` where category is inbound minus outbound, grouped by warehouse, item, batch. | Supported by existing `CStatistics` and `CCStockByBatchNo`; OK pending engineer confirmation |
| Inventory value | Prefer current remaining amount from `inventory_record.amount`; use statistics tables when querying committed month/day summaries. | Need Review |
| Category mapping | Use `EItemCategory`: PM=1, MA=2, AF=3, INPRODUCT=4, PRODUCT=5. | OK |
| Near-expiry rule | Use batch `validDate` and `validDays / 3`; existing stock logic already calculates near-expiry and expired amounts. | OK, but confirm excluding MA/AF |
| Turnover rule | Use earliest inbound inventory date per warehouse and batch, then calculate days in stock. | Supported by `CCStockByBatchNo`; OK pending engineer confirmation |
| Safety stock | Compare current or available quantity to safety stock threshold. | Need Review: source table/field not confirmed |
| Reserved quantity | Deduct sales reservations, production material allocation, and pending warehouse tasks from current stock. | Need Review |
| Quality hold | Deduct unreleased material/item inspection quantity from available inventory. | Need Review |
| Pallet usage | Count distinct `batchno_serialno_group.group` by warehouse/category/batch. | Need Review |
| Total pallet capacity | Use warehouse master/config if available; no confirmed capacity field found in current DB docs. | Need Review |
| Pending inbound | Compare expected quantity from purchase receiving source with processed inventory record quantity. | Need Review |
| Pending outbound | Compare expected quantity from shipping/production/manual inventory source with processed inventory record quantity. | Need Review |

## GET /api/v1/warehouse/inventory

<a id="get-api-v1-warehouse-inventory"></a>

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v1/warehouse/inventory` | GET | Query Warehouse inventory detail rows for drill-down and table view |

### Request Header

| Header | Description |
| --- | --- |
| x-auth-token | Access token |

### Query Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| date | Integer | NO | Inventory reference timestamp. Default is current server time. |
| timezone | String | NO | User timezone for date range calculation. |
| warehouse_no | String | NO | Filter by warehouse alias number. |
| itemCategory | Integer | NO | Filter by item category. |
| item_no | String | NO | Filter by item number. |
| batchNo | String | NO | Filter by batch number. |
| riskType | String | NO | Filter by generated risk type. |
| count | Integer | NO | Page size. |
| start | Integer | NO | Page offset. |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "total": "Integer",
    "count": "Integer",
    "results": [
      {
        "inventoryId": "String",
        "warehouseNo": "String",
        "warehouseName": "String",
        "itemNo": "String",
        "itemName": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "itemType": "Integer",
        "batchNo": "String",
        "serialNo": "String",
        "currentQuantity": "Float",
        "reservedQuantity": "Float",
        "availableQuantity": "Float",
        "qualityHoldQuantity": "Float",
        "unit": "Integer",
        "unitCost": "Float",
        "inventoryValue": "Float",
        "reservedValue": "Float",
        "availableValue": "Float",
        "palletCount": "Integer",
        "safetyStock": "Float",
        "validDays": "Integer",
        "validDate": "Integer",
        "firstInboundTimestamp": "Integer",
        "daysInStock": "Integer",
        "sourceType": "String",
        "sourceNo": "String",
        "sourceRefCategory": "Integer",
        "qualityStatus": "String",
        "riskTypes": [
          "String"
        ]
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| payload.total | Integer | Total detail rows matching filters. |  |
| payload.count | Integer | Number of rows returned in this page. |  |
| payload.results[].inventoryId | String | Stable inventory row id generated from warehouse, item, batch, and serial data. |  |
| payload.results[].warehouseNo | String | Warehouse alias number. |  |
| payload.results[].warehouseName | String | Warehouse alias display name. |  |
| payload.results[].itemNo | String | Item number. |  |
| payload.results[].itemName | String | Item name. |  |
| payload.results[].itemCategory | Integer | Item category code. | EItemCategory |
| payload.results[].itemSubCategory | Integer | Item subcategory code from item master relation. |  |
| payload.results[].itemType | Integer | Item type code. | 新料(1), 餘料(2), 廢料(3), 其他(0) |
| payload.results[].batchNo | String | Batch number. |  |
| payload.results[].serialNo | String | Serial number when serial-level detail is requested or available. |  |
| payload.results[].currentQuantity | Float | On-hand quantity calculated from inventory movement records. |  |
| payload.results[].reservedQuantity | Float | Quantity reserved by sales, production, or pending warehouse tasks. | Need engineer confirmation |
| payload.results[].availableQuantity | Float | Current quantity minus reserved and quality-hold quantity. | Need engineer confirmation |
| payload.results[].qualityHoldQuantity | Float | Quantity blocked by quality inspection or release status. | Need engineer confirmation |
| payload.results[].unit | Integer | Inventory unit code. | Unit enum |
| payload.results[].unitCost | Float | Unit cost used for inventory value calculation. | Need engineer confirmation |
| payload.results[].inventoryValue | Float | Current inventory value. |  |
| payload.results[].reservedValue | Float | Reserved inventory value. | Need engineer confirmation |
| payload.results[].availableValue | Float | Available inventory value. | Need engineer confirmation |
| payload.results[].palletCount | Integer | Pallet count occupied by this inventory row. | Need engineer confirmation |
| payload.results[].safetyStock | Float | Safety stock threshold. | Need engineer confirmation |
| payload.results[].validDays | Integer | Shelf-life days from batch data. |  |
| payload.results[].validDate | Integer | Expiry timestamp from batch data. |  |
| payload.results[].firstInboundTimestamp | Integer | Earliest inbound inventory record date for the same warehouse and batch. |  |
| payload.results[].daysInStock | Integer | Days between first inbound timestamp and query date. |  |
| payload.results[].sourceType | String | Business source of the inventory row. | PURCHASE, SALE, WORK, INVENTORY, OTHER |
| payload.results[].sourceNo | String | Source document number. |  |
| payload.results[].sourceRefCategory | Integer | Inventory reference category from source record. | `EInventoryRefCategory` |
| payload.results[].qualityStatus | String | Quality release state used in availability calculation. | Need engineer confirmation |
| payload.results[].riskTypes[] | String | Risk types attached to this row. | `TURNOVER_OVER_30_DAYS`, `SHELF_LIFE_LT_ONE_THIRD`, `BELOW_SAFETY_STOCK` |

### Processing Flow

1. Read inventory filters and pagination parameters.
2. Retrieve inventory records grouped by warehouse, item, batch, and optional serial number.
3. Calculate current quantity and inventory value from inbound and outbound records.
4. Join batch data to obtain expiry fields, valid days, checked quantity, and source document relation.
5. Join warehouse alias data to obtain warehouse display name and type.
6. Calculate reserved, quality-hold, available quantity, pallet count, safety stock, and risk types after the relevant source rules are confirmed.
7. Apply risk-only and pagination filters.
8. Return normalized detail rows for frontend drill-down and table display.

### Database Tables Used

| Table | Purpose |
| --- | --- |
| inventory_record | Provides inventory movement details and current stock calculation. |
| batch_number | Provides batch-level item, expiry, valid days, and source document data. |
| batchno_serialno | Provides serial-level detail when inventory rows need serial number expansion. |
| batchno_serialno_group | Provides pallet group relation for batch/serial inventory. |
| ship_wh_alias | Provides warehouse alias and warehouse type display data. |
| item_price | Candidate source for unit cost when movement amount is insufficient. |

## GET /api/v1/warehouse/tasks

<a id="get-api-v1-warehouse-tasks"></a>

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v1/warehouse/tasks` | GET | Query today's pending Warehouse inbound/outbound/transfer tasks |

### Request Header

| Header | Description |
| --- | --- |
| x-auth-token | Access token |

### Query Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| date | Integer | NO | Task reference timestamp. Default is current server time. |
| timezone | String | NO | User timezone for business-day calculation. |
| taskType | String | NO | Filter by task type. |
| warehouse_no | String | NO | Filter by warehouse alias number. |
| status | String | NO | Filter by task processing status. |
| count | Integer | NO | Page size. |
| start | Integer | NO | Page offset. |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "total": "Integer",
    "count": "Integer",
    "results": [
      {
        "taskId": "String",
        "taskType": "String",
        "sourceType": "String",
        "sourceNo": "String",
        "sourceSubNo": "String",
        "itemNo": "String",
        "itemName": "String",
        "itemCategory": "Integer",
        "batchNo": "String",
        "expectedQuantity": "Float",
        "processedQuantity": "Float",
        "remainingQuantity": "Float",
        "unit": "Integer",
        "palletCount": "Integer",
        "warehouseNo": "String",
        "warehouseName": "String",
        "dueTimestamp": "Integer",
        "status": "String",
        "ownerDepartment": "String",
        "blockReason": "String"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| payload.total | Integer | Total task rows matching filters. |  |
| payload.count | Integer | Number of task rows returned in this page. |  |
| payload.results[].taskId | String | Stable task identifier. |  |
| payload.results[].taskType | String | Warehouse task type. | `INBOUND`, `OUTBOUND`, `TRANSFER`, `COUNTING` |
| payload.results[].sourceType | String | Business source document type. | `PURCHASE`, `SALE`, `WORK`, `INVENTORY`, `OTHER` |
| payload.results[].sourceNo | String | Source document number. |  |
| payload.results[].sourceSubNo | String | Source document line/sub number if available. |  |
| payload.results[].itemNo | String | Item number. |  |
| payload.results[].itemName | String | Item name. |  |
| payload.results[].itemCategory | Integer | Item category code. | EItemCategory |
| payload.results[].batchNo | String | Batch number if generated. |  |
| payload.results[].expectedQuantity | Float | Source document expected quantity. |  |
| payload.results[].processedQuantity | Float | Quantity already processed into inventory records. |  |
| payload.results[].remainingQuantity | Float | Expected quantity minus processed quantity. |  |
| payload.results[].unit | Integer | Task unit. | Unit enum |
| payload.results[].palletCount | Integer | Pallet count for this task. | Need engineer confirmation |
| payload.results[].warehouseNo | String | Warehouse alias number. |  |
| payload.results[].warehouseName | String | Warehouse alias display name. |  |
| payload.results[].dueTimestamp | Integer | Expected processing timestamp. |  |
| payload.results[].status | String | Task status. | `pending`, `partial`, `done`, `blocked` |
| payload.results[].ownerDepartment | String | Department responsible for next action. |  |
| payload.results[].blockReason | String | Reason why task cannot proceed, such as quality hold or missing warehouse assignment. |  |

### Processing Flow

1. Convert query date and timezone into a business-day range.
2. Collect source documents that can generate Warehouse work:
   - purchase inbound from `goods_receipt_note`;
   - sales outbound from `shipping_order`;
   - production issue/return/remaining/waste/product movement from `process_order`;
   - manual inventory movement from `inventory_order`.
3. Match each source document with processed `inventory_record` rows by source number, item, batch, and warehouse when available.
4. Calculate expected, processed, and remaining quantity for each task.
5. Derive task status:
   - `pending`: processed quantity is zero;
   - `partial`: processed quantity is greater than zero but less than expected quantity;
   - `done`: processed quantity is greater than or equal to expected quantity;
   - `blocked`: task cannot proceed because quality, warehouse assignment, or source data is incomplete.
6. Assign owner department based on task type and block reason.
7. Return pending or filtered task rows for the Warehouse page.

### Database Tables Used

| Table | Purpose |
| --- | --- |
| goods_receipt_note | Provides purchase receiving source rows for inbound warehouse tasks. |
| shipping_order | Provides sales shipping source rows for outbound warehouse tasks. |
| process_order | Provides production material issue, return, remaining, waste, and product movement source rows. |
| inventory_order | Provides manual inventory movement source rows. |
| inventory_record | Provides processed quantity for task completion calculation. |
| batch_number | Provides batch and expiry information for task rows when a batch exists. |
| ship_wh_alias | Provides warehouse display data for task assignment and filtering. |

## Engineer Review Checklist

| Question | Impact | Status |
| --- | --- | --- |
| Should Warehouse dashboard be implemented as new `/api/v1/warehouse/*` routes or as extensions of existing `/api/v1/inventory/*` and `/api/v1/shipwarehouse/*` routes? | Determines route ownership and API grouping. | Need Review |
| Can current inventory value rely on `inventory_record.amount`, or should the API use `inventory_item_month_statistic` / `inventory_month_statistic` snapshots? | Determines value accuracy and performance. | Need Review |
| What is the official reservation source of truth for sales, production, and warehouse tasks? | Required for reserved and available quantity/value. | Need Review |
| Which table/field stores safety stock? | Required for below-safety-stock alert. | Need Review |
| Which table/field stores quality inspection release/hold status? | Required before calculating available inventory. | Need Review |
| Which table/field stores warehouse total pallet capacity? | Required for capacity dashboard. | Need Review |
| Is `batchno_serialno_group.group` the correct pallet identifier for occupied pallet counting? | Required for used pallet and category pallet usage. | Need Review |
| Should supplies and film be excluded from the one-third shelf-life warning? | User requested exclusion; backend rule should confirm item category mapping. | Need Review |
| Should dashboard include inventory detail rows by default? | Impacts response size and frontend mapper. | Need Review |
| Should pending inbound/outbound tasks include only today's due tasks or all overdue plus today tasks? | Impacts task count and management urgency. | Need Review |

## Frontend Mapping Notes

The current frontend service expects:

```txt
kpis
categorySummaries
capacities
records
risks
tasks
```

The proposed backend payload maps as follows:

| Frontend field group | Proposed backend dataset |
| --- | --- |
| `kpis` | `payload.summary` |
| `categorySummaries` | `payload.inventoryValueByCategory` |
| `capacities` | `payload.capacityByWarehouse` |
| `records` | `payload.inventory` or `GET /api/v1/warehouse/inventory` |
| `risks` | `payload.riskAlerts` |
| `tasks` | `payload.pendingTasks` or `GET /api/v1/warehouse/tasks` |

Frontend should keep API normalization inside `src/services/warehouse-api.ts` so page components can remain stable while backend field names stay domain-oriented.

