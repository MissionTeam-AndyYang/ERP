# Warehouse Inventory Detail API Proposal

> Status: Implemented / Pending Engineer Runtime Review
> Target UI Preview: `docs/frontend/preview/warehouse_inventory_detail_static_preview.html`
> Implementation: `restserver/package/restserver/api/v2/warehouse.py`, `restserver/package/restserver/api/v2/warehouse_uri.py`
> Purpose: 承接 Warehouse Dashboard 的類別、風險警示與待處理任務點擊情境，提供「庫存明細與批號追蹤」畫面所需 API 規格提案。

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| `/api/v2/warehouse/inventory/lots` | GET | 查詢庫存批號明細清單 | Implemented / Pending Runtime Review | 供明細列表、篩選、排序、分頁與 Dashboard drill-down 使用。 |
| `/api/v2/warehouse/inventory/lots/{lotKey}` | GET | 查詢單一庫存批號追蹤明細 | Implemented / Pending Runtime Review | 供右側明細面板顯示來源、預留、品檢、板位、任務與風險。 |

## Numeric Format Rules

| Numeric Meaning | Format |
|----------|----------|
| 單價 | 四捨五入取至小數點第 4 位 |
| 重量或數量 | 四捨五入取至小數點第 2 位 |
| 金額 | 四捨五入取整數 |

## Screen Intent

此畫面回答 Dashboard 無法完整展開的四個問題：

1. 指定類別、倉儲或批號目前有哪些庫存明細？
2. 該批庫存中，多少已預留、多少品檢保留、多少可用？
3. 該批庫存來自哪張進貨、工單或入庫紀錄，後續又被哪些出庫、工單或出貨任務使用？
4. 若該批庫存有風險，應由哪個部門下一步處理？

## GET /api/v2/warehouse/inventory/lots

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| `/api/v2/warehouse/inventory/lots` | GET | 查詢庫存批號明細清單 |

### Request Header

| Header | Description |
|----------|----------|
| `x-auth-token` | 存取金鑰 |
| `x-timezone` | 前端顯示時區；未提供時以 UTC 回傳 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| `date` | Integer | NO | 查詢基準時間，UTC timestamp；未提供時以伺服器目前時間計算 |
| `warehouse_no` | String | NO | 倉儲別名 no |
| `itemCategory` | Integer | NO | 料品品項類別；原料(1)、物料(2)、膠捲(3)、在製品(4)、製成品(5) |
| `item_no` | String | NO | 料品品項編號 |
| `batchNo` | String | NO | 批號 |
| `riskType` | String | NO | 風險類型；`TURNOVER_OVER_30_DAYS`、`SHELF_LIFE_LT_ONE_THIRD`、`BELOW_SAFETY_STOCK` |
| `taskType` | Integer | NO | 任務類型；請購(1)、採購(2)、進貨(3)、入庫(4)、出庫(5)、移倉(6)、生產(7)、品檢(8)、出貨(9) |
| `availability` | String | NO | 可用狀態；`available`、`reserved`、`quality_hold`、`blocked` |
| `keyword` | String | NO | 模糊搜尋：料號、品名、批號、來源單號、倉儲名稱 |
| `sort` | String | NO | 排序欄位；建議支援 `inventoryValue`、`availableQuantity`、`validDate`、`daysInStock` |
| `order` | String | NO | `asc` 或 `desc` |
| `start` | Integer | NO | 分頁起始位置 |
| `count` | Integer | NO | 分頁筆數；建議預設 50 |

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
    "total": "Integer",
    "count": "Integer",
    "start": "Integer",
    "summary": {
      "lotCount": "Integer",
      "itemCount": "Integer",
      "totalQuantity": "Float",
      "totalInventoryValue": "Integer",
      "totalAvailableQuantity": "Float",
      "totalAvailableValue": "Integer",
      "riskLotCount": "Integer",
      "pendingTaskCount": "Integer"
    },
    "results": [
      {
        "lotKey": "String",
        "warehouseNo": "String",
        "warehouseName": "String",
        "itemCategory": "Integer",
        "itemNo": "String",
        "itemName": "String",
        "batchNo": "String",
        "unit": "Integer",
        "currentQuantity": "Float",
        "reservedQuantity": "Float",
        "qualityHoldQuantity": "Float",
        "availableQuantity": "Float",
        "unitCost": "Float",
        "inventoryValue": "Integer",
        "reservedValue": "Integer",
        "qualityHoldValue": "Integer",
        "availableValue": "Integer",
        "palletCount": "Float",
        "firstInboundTimestamp": "Integer",
        "daysInStock": "Integer",
        "validDays": "Integer",
        "validDate": "Integer",
        "remainingShelfLifeRatio": "Float",
        "safetyStock": "Float",
        "riskTypes": ["String"],
        "openTaskCount": "Integer",
        "lastSourceNo": "String",
        "lastSourceCategory": "Integer"
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| `payload.summary.totalQuantity` | Float | 清單篩選條件下的目前庫存量合計 | Unit |
| `payload.summary.totalInventoryValue` | Integer | 清單篩選條件下的庫存價值合計 |  |
| `payload.summary.totalAvailableQuantity` | Float | 清單篩選條件下的可用數量合計 | Unit |
| `payload.summary.totalAvailableValue` | Integer | 清單篩選條件下的可用價值合計 |  |
| `payload.results[].lotKey` | String | 前端 drill-down 使用的批號庫存識別鍵；建議由 warehouseNo、itemNo、batchNo 組成穩定 key |  |
| `payload.results[].warehouseNo` | String | 倉儲別名 no |  |
| `payload.results[].itemCategory` | Integer | 料品品項類別；前端負責轉換顯示文字 | EItemCategory |
| `payload.results[].currentQuantity` | Float | 目前庫存量 | Unit |
| `payload.results[].reservedQuantity` | Float | 預留數量 | Unit |
| `payload.results[].qualityHoldQuantity` | Float | 品檢保留量 | Unit |
| `payload.results[].availableQuantity` | Float | 可用數量，計算方式為目前庫存量扣除預留數量與品檢保留量 | Unit |
| `payload.results[].unitCost` | Float | 此批庫存計價用單價，取至小數點第 4 位 |  |
| `payload.results[].inventoryValue` | Integer | 目前庫存價值 |  |
| `payload.results[].palletCount` | Float | 此批庫存佔用板數 |  |
| `payload.results[].remainingShelfLifeRatio` | Float | 剩餘效期比例；物料與膠捲可回傳 0 或空值，由前端依類別忽略效期警示 |  |
| `payload.results[].riskTypes[]` | String | 此批庫存命中的風險類型 | EWarehouseRiskType |
| `payload.results[].openTaskCount` | Integer | 此批庫存尚未完成的 workflow 任務數 |  |
| `payload.results[].lastSourceNo` | String | 最近一次入庫或異動來源單號 |  |
| `payload.results[].lastSourceCategory` | Integer | 最近一次來源類別 |  |

### Processing Flow

1. 讀取查詢條件與分頁條件，建立料品、倉儲、批號、風險、任務與可用狀態篩選。
2. 從 `inventory_record` 依倉儲、料品、批號彙總目前庫存量與庫存價值。
3. 從 `batch_number` 補充有效天數、效期日與批號來源資料。
4. 從 `warehouse_inventory_reservation` 彙總有效預留數量與預留價值。
5. 從 `warehouse_quality_hold` 彙總品檢保留量與品檢保留價值。
6. 從 `warehouse_pallet_movement` 彙總此批庫存佔用板數。
7. 從 `item_safety_stock` 判斷是否低於安全水位。
8. 從 `workflow_task_state` 彙總未完成任務數，並支援 `taskType` 篩選。
9. 套用風險判斷：迴轉超過 30 天、剩餘效期低於三分之一、低於安全水位。
10. 回傳 summary 與分頁後 results；所有 enum 顯示文字由前端轉換。

### Database Tables Used

| Table | Purpose |
|----------|------|
| `inventory_record` | 彙總批號庫存量與庫存價值 |
| `batch_number` | 提供批號、效期與來源資訊 |
| `warehouse_inventory_reservation` | 提供預留數量與預留價值 |
| `warehouse_quality_hold` | 提供品檢保留量與品檢保留價值 |
| `warehouse_pallet_movement` | 提供板位佔用狀態 |
| `item_safety_stock` | 提供安全水位 |
| `workflow_task_state` | 提供未完成任務與下一步負責部門 |
| `ship_wh_alias` | 提供倉儲別名與名稱 |

## GET /api/v2/warehouse/inventory/lots/{lotKey}

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| `/api/v2/warehouse/inventory/lots/{lotKey}` | GET | 查詢單一庫存批號追蹤明細 |

### Path Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| `lotKey` | String | YES | 批號庫存識別鍵；需與清單 API 回傳一致 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| `date` | Integer | NO | 查詢基準時間，UTC timestamp |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "lot": {
      "lotKey": "String",
      "warehouseNo": "String",
      "warehouseName": "String",
      "itemCategory": "Integer",
      "itemNo": "String",
      "itemName": "String",
      "batchNo": "String",
      "unit": "Integer",
      "currentQuantity": "Float",
      "reservedQuantity": "Float",
      "qualityHoldQuantity": "Float",
      "availableQuantity": "Float",
      "unitCost": "Float",
      "inventoryValue": "Integer",
      "availableValue": "Integer",
      "palletCount": "Float",
      "validDate": "Integer",
      "riskTypes": ["String"]
    },
    "sourceDocuments": [
      {
        "refCategory": "Integer",
        "refNo": "String",
        "refSubNo": "String",
        "date": "Integer",
        "quantity": "Float",
        "amount": "Integer"
      }
    ],
    "reservations": [
      {
        "reservationNo": "String",
        "refCategory": "Integer",
        "refNo": "String",
        "reservedQuantity": "Float",
        "reservedValue": "Integer",
        "releaseTime": "Integer",
        "status": "Integer"
      }
    ],
    "qualityHolds": [
      {
        "holdNo": "String",
        "inspectionNo": "String",
        "holdQuantity": "Float",
        "holdValue": "Integer",
        "reason": "String",
        "status": "Integer"
      }
    ],
    "palletMovements": [
      {
        "movementNo": "String",
        "date": "Integer",
        "palletGroupNo": "String",
        "palletStatus": "Integer",
        "palletCount": "Float",
        "refCategory": "Integer",
        "refNo": "String"
      }
    ],
    "workflowTasks": [
      {
        "taskId": "String",
        "taskType": "Integer",
        "taskStatus": "Integer",
        "ownerDepartment": "Integer",
        "expectedQuantity": "Float",
        "processedQuantity": "Float",
        "remainingQuantity": "Float",
        "dueTimestamp": "Integer",
        "blockReason": "String"
      }
    ]
  }
}
```

### Processing Flow

1. 解析 `lotKey`，取得 warehouseNo、itemNo、batchNo 或等價查詢鍵。
2. 重新彙總該批庫存目前數量與價值，避免使用前端帶入的暫存值。
3. 查詢該批來源與異動紀錄，組成 `sourceDocuments`。
4. 查詢有效預留、品檢保留、板位異動與未完成 workflow 任務。
5. 回傳 enum code，不回傳多國語言顯示文字。

## Frontend Interaction Notes

| UI Action | API Usage |
|----------|----------|
| 從 Dashboard 點選某個料品類別 | 呼叫 list API，帶入 `itemCategory` |
| 從 Dashboard 點選風險警示 | 呼叫 list API，帶入 `riskType`；再選第一筆或使用者點選後呼叫 detail API |
| 從 Dashboard 點選待處理任務 | 呼叫 list API，帶入 `taskType` 或 `keyword=sourceNo` |
| 使用者點選明細列 | 呼叫 detail API 顯示右側追蹤面板 |
| 使用者切換語系 | 前端依 enum code 轉換顯示文字，API 不需回傳翻譯字串 |

## Engineer Review Questions

| Question | Impact |
|----------|------|
| `lotKey` 是否使用組合字串，或後端需新增穩定 inventory lot id？ | 影響 detail API path 設計與前端路由。 |
| `unitCost` 成本算法採用目前 `inventory_record.amount / count`，或需指定加權平均/批次成本？ | 影響金額、預留價值、可用價值。 |
| `sourceDocuments` 第一版是否只顯示 `inventory_record.ref_no/refCategory`，或要 join 來源單據名稱？ | 影響查詢成本與右側面板資訊完整度。 |
| `quality_holds` 是否先使用 `warehouse_quality_hold`，未來再串接 Quality 模組檢驗單？ | 影響品保釋放流程整合。 |
