# ERP Warehouse API Development Spec

Date: 2026-05-24
Route: `/warehouse`
Purpose: Define read-only APIs for Warehouse V1.

## 1. V1 Goal

Warehouse V1 helps managers understand inventory value, warehouse space usage, availability, expiry/turnover risk, safety stock risk and today's inbound/outbound workload.

## 2. Aggregation API

### `GET /api/v1/warehouse/dashboard`

Returns all datasets needed by the Warehouse first screen.

```json
{
  "summary": {
    "totalInventoryValue": 0,
    "reservedInventoryValue": 0,
    "availableInventoryValue": 0,
    "occupiedPallets": 0,
    "availablePallets": 0,
    "pendingInboundCount": 0,
    "pendingOutboundCount": 0,
    "riskAlertCount": 0
  },
  "inventoryValueByCategory": [],
  "capacityByWarehouse": [],
  "riskAlerts": [],
  "pendingInbound": [],
  "pendingOutbound": [],
  "qualityHoldItems": [],
  "valueTrend": []
}
```

## 3. Detail APIs

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/warehouse/inventory` | Inventory detail with filters and pagination |
| `GET /api/v1/warehouse/locations` | Warehouse/location/pallet capacity |
| `GET /api/v1/warehouse/alerts` | Expiry, turnover and safety stock alerts |
| `GET /api/v1/warehouse/tasks` | Pending inbound/outbound/transfer tasks |
| `GET /api/v1/warehouse/quality-holds` | Inventory blocked by quality status |

## 4. Dataset Structures

### `inventoryValueByCategory[]`

```json
{
  "category": "raw_material",
  "label": "原料",
  "itemCount": 0,
  "currentQty": 0,
  "reservedQty": 0,
  "availableQty": 0,
  "inventoryValue": 0,
  "reservedValue": 0,
  "availableValue": 0,
  "palletUsed": 0,
  "turnoverDays": 0,
  "riskLevel": "normal"
}
```

Required categories:

- `raw_material`: 原料
- `supplies`: 物料
- `film`: 膠捲
- `wip`: 在製品
- `finished_goods`: 製成品

### `capacityByWarehouse[]`

```json
{
  "warehouseId": "WH-FZ-01",
  "warehouseName": "冷凍庫 A",
  "warehouseType": "frozen",
  "totalPallets": 0,
  "usedPallets": 0,
  "reservedPallets": 0,
  "availablePallets": 0,
  "utilizationRate": 0,
  "riskLevel": "normal"
}
```

### `riskAlerts[]`

```json
{
  "alertId": "WAL-0001",
  "type": "expiry",
  "severity": "warning",
  "itemNo": "",
  "itemName": "",
  "batchNo": "",
  "category": "raw_material",
  "warehouseName": "",
  "message": "",
  "daysLeft": 0,
  "owner": "warehouse",
  "relatedDocumentNo": ""
}
```

Allowed alert types:

- `turnover_over_30_days`
- `expiry_less_than_one_third`
- `below_safety_stock`
- `capacity_warning`
- `quality_hold`

### `pendingInbound[]` and `pendingOutbound[]`

```json
{
  "taskId": "",
  "taskType": "inbound",
  "documentNo": "",
  "sourceModule": "purchase",
  "itemNo": "",
  "itemName": "",
  "batchNo": "",
  "quantity": 0,
  "unit": "",
  "palletCount": 0,
  "status": "pending",
  "owner": "warehouse",
  "dueTime": "2026-05-24T10:00:00Z",
  "qualityStatus": "pending"
}
```

### `inventory[]` detail

```json
{
  "inventoryId": "",
  "itemNo": "",
  "itemName": "",
  "category": "raw_material",
  "batchNo": "",
  "warehouseId": "",
  "warehouseName": "",
  "locationCode": "",
  "onHandQty": 0,
  "reservedQty": 0,
  "qualityHoldQty": 0,
  "availableQty": 0,
  "unit": "",
  "unitCost": 0,
  "inventoryValue": 0,
  "palletCount": 0,
  "safetyStock": 0,
  "expiryDate": "2026-12-31",
  "shelfLifeDays": 0,
  "daysLeft": 0,
  "turnoverDays": 0,
  "sourceType": "purchase",
  "sourceNo": "",
  "qualityStatus": "released",
  "riskLevel": "normal"
}
```

## 5. Calculation Rules

- `availableQty = onHandQty - reservedQty - qualityHoldQty`.
- `inventoryValue = onHandQty * unitCost`.
- `availableInventoryValue = availableQty * unitCost`.
- Expiry one-third warning applies when `daysLeft < shelfLifeDays / 3`.
- Expiry one-third warning excludes `supplies` and `film` unless a specific item requires expiry control.
- Turnover warning applies when `turnoverDays > 30`.
- Capacity warning applies when `utilizationRate >= 90`.

## 6. Existing API Candidates

- `/api/v1/inventory`
- `/api/v1/inventory/price`
- `/api/v1/inventory/statistics`
- `/api/v1/inventory/items`
- `/api/v1/inventory/months`
- `/api/v1/purchase/goodsreceiptnote`
- `/api/v1/sale/shippingorder`
- `/api/v1/shipwarehouse/warehouserec`
- `/api/v1/batchnumber`
- `/api/v1/batchtrace`

## 7. Engineer Confirmation Required

1. Where are warehouse location and pallet capacity stored?
2. Does inventory currently distinguish on-hand, reserved, quality-hold and available quantity?
3. Which table stores safety stock?
4. Which cost method should `unitCost` use?
5. Where is material inspection release/hold status stored?
6. Can current endpoints return batch expiry and shelf-life data?
