# warehouse API Group

> Source: `restserver/package/restserver/api/v2/warehouse_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v2/warehouse/dashboard](#get-api-v2-warehouse-dashboard) | GET | 查詢 Warehouse Dashboard 經營總覽資料 | Need Review | [新增] 依 Warehouse 第一版 UX 需求與工程師確認後之資料庫新增規劃建立；待工程師以實際 MariaDB 測試資料確認。 |
| [/api/v2/warehouse/inventory](#get-api-v2-warehouse-inventory) | GET | 查詢 Warehouse 庫存明細資料 | Implemented / Pending Runtime Review | [新增] 工程師已確認之 Warehouse Dashboard 庫存明細 API。 |
| [/api/v2/warehouse/inventory/lots](#get-api-v2-warehouse-inventory-lots) | GET | 查詢庫存批號明細清單 | Implemented / Pending Runtime Review | [新增] 依已確認之 `warehouse_inventory_detail_proposal.md` 整合至正式 API 文件。 |
| [/api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}](#get-api-v2-warehouse-inventory-lots-detail) | GET | 查詢單一庫存批號追蹤明細 | Implemented / Pending Runtime Review | [新增] 依已確認之 `warehouse_inventory_detail_proposal.md` 整合至正式 API 文件。 |
| [/api/v2/warehouse/tasks](#get-api-v2-warehouse-tasks) | GET | 查詢 Warehouse 待處理任務 | Implemented / Pending Runtime Review | [新增] 工程師已確認之 Warehouse Dashboard 待處理入出庫任務 API。 |

## GET /api/v2/warehouse/dashboard

<a id="get-api-v2-warehouse-dashboard"></a>

### Numeric Format Rules

| Numeric Meaning | Format |
|----------|----------|
| 單價 | 四捨五入取至小數點第 4 位 |
| 重量或數量 | 四捨五入取至小數點第 2 位 |
| 金額 | 四捨五入取整數 |

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/warehouse/dashboard | GET | 查詢 Warehouse Dashboard 經營總覽資料 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示時區；未提供時以 UTC 回傳 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| date | Integer | NO | 查詢基準時間，UTC timestamp；後端依 `x-timezone` 換算查詢營業日，未提供時以伺服器目前時間計算 |
| warehouse_no | String | NO | 倉儲別名 no；提供時只回傳指定倉儲資料 |
| itemCategory | Integer | NO | 料品品項類別；原料(1)、物料(2)、膠捲(3)、在製品(4)、製成品(5) |
| includeInventory | Boolean/String | NO | 是否回傳庫存明細；支援 `1`、`true`、`yes` |
| riskOnly | Boolean/String | NO | 是否僅聚焦風險警示情境；聚合資料仍完整回傳，`includeInventory=true` 時庫存明細只回傳有風險的列 |

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
      "totalInventoryValue": "Integer",
      "reservedInventoryValue": "Integer",
      "availableInventoryValue": "Integer",
      "qualityHoldInventoryValue": "Integer",
      "totalPallets": "Float",
      "usedPallets": "Float",
      "reservedPallets": "Float",
      "availablePallets": "Float",
      "riskAlertCount": "Integer",
      "pendingInboundCount": "Integer",
      "pendingOutboundCount": "Integer"
    },
    "inventoryValueByCategory": [
      {
        "itemCategory": "Integer",
        "inventoryValue": "Integer",
        "reservedValue": "Integer",
        "availableValue": "Integer",
        "qualityHoldValue": "Integer",
        "quantity": "Float",
        "unit": "Integer",
        "palletCount": "Float",
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
        "totalPallets": "Float",
        "usedPallets": "Float",
        "reservedPallets": "Float",
        "availablePallets": "Float",
        "utilizationRate": "Float",
        "riskLevel": "Integer"
      }
    ],
    "riskAlerts": [
      {
        "alertId": "String",
        "riskType": "String",
        "riskLevel": "Integer",
        "itemNo": "String",
        "itemName": "String",
        "itemCategory": "Integer",
        "batchNo": "String",
        "warehouseNo": "String",
        "warehouseName": "String",
        "quantity": "Float",
        "unit": "Integer",
        "inventoryValue": "Integer",
        "daysInStock": "Integer",
        "validDate": "Integer",
        "remainingShelfLifeRatio": "Float",
        "safetyStock": "Float",
        "messageCode": "String",
        "messageParams": {
          "currentQuantity": "Float",
          "daysInStock": "Integer",
          "validDate": "Integer",
          "remainingShelfLifeRatio": "Float",
          "safetyStock": "Float"
        },
        "recommendedActionCode": "String"
      }
    ],
    "pendingTasks": [
      {
        "taskId": "String",
        "taskType": "Integer",
        "refCategory": "Integer",
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
        "palletCount": "Float",
        "warehouseNo": "String",
        "warehouseName": "String",
        "dueTimestamp": "Integer",
        "taskStatus": "Integer",
        "ownerDepartment": "Integer",
        "blockReason": "String"
      }
    ],
    "valueTrend": [
      {
        "date": "String",
        "itemCategory": "Integer",
        "inventoryValue": "Integer"
      }
    ],
    "inventory": [
      {
        "warehouseNo": "String",
        "warehouseName": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "itemType": "Integer",
        "itemNo": "String",
        "itemName": "String",
        "batchNo": "String",
        "unit": "Integer",
        "currentQuantity": "Float",
        "reservedQuantity": "Float",
        "availableQuantity": "Float",
        "qualityHoldQuantity": "Float",
        "inventoryValue": "Integer",
        "reservedValue": "Integer",
        "availableValue": "Integer",
        "qualityHoldValue": "Integer",
        "firstInboundTimestamp": "Integer",
        "validDays": "Integer",
        "validDate": "Integer"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 | EErrorCode |
| message | String | API 回傳訊息 |  |
| payload.serverTimestamp | Integer | API 查詢基準時間，UTC timestamp |  |
| payload.timezone | String | 前端指定或系統預設的顯示時區 |  |
| payload.range.date | String | 依 `x-timezone` 換算後的查詢營業日期，格式為 YYYY-MM-DD |  |
| payload.range.startTimestamp | Integer | 查詢營業日起始時間，UTC timestamp |  |
| payload.range.endTimestamp | Integer | 查詢營業日結束時間，UTC timestamp |  |
| payload.summary.totalInventoryValue | Integer | 目前庫存總價值，第一版以 `inventory_item_month_statistic` 月結批號層級結存搭配 `inventory_delta` 每日異動補算至查詢營業日 |  |
| payload.summary.reservedInventoryValue | Integer | 已被訂單、工單或倉庫任務預留的庫存價值 |  |
| payload.summary.availableInventoryValue | Integer | 可用庫存價值，計算方式為庫存價值扣除預留價值與品檢保留價值 |  |
| payload.summary.qualityHoldInventoryValue | Integer | 品檢保留庫存價值 |  |
| payload.summary.totalPallets | Float | 可管理倉儲空間總板數 |  |
| payload.summary.usedPallets | Float | 已佔用板數 |  |
| payload.summary.reservedPallets | Float | 已預留板數 |  |
| payload.summary.availablePallets | Float | 可用板數 |  |
| payload.summary.riskAlertCount | Integer | 庫存風險警示筆數 |  |
| payload.summary.pendingInboundCount | Integer | 今日或待處理進貨/入庫任務數 | EWorkflowTaskType |
| payload.summary.pendingOutboundCount | Integer | 今日或待處理出庫/出貨任務數 | EWorkflowTaskType |
| payload.inventoryValueByCategory[].itemCategory | Integer | 料品品項類別 | EItemCategory |
| payload.inventoryValueByCategory[].inventoryValue | Integer | 該類別目前庫存價值 |  |
| payload.inventoryValueByCategory[].reservedValue | Integer | 該類別預留價值 |  |
| payload.inventoryValueByCategory[].availableValue | Integer | 該類別可用價值 |  |
| payload.inventoryValueByCategory[].qualityHoldValue | Integer | 該類別品檢保留價值 |  |
| payload.inventoryValueByCategory[].quantity | Float | 該類別目前庫存量彙總；因實務可能混合單位，第一版僅供比較參考 |  |
| payload.inventoryValueByCategory[].unit | Integer | 數量單位；混合單位彙總時回傳 0 | Unit |
| payload.inventoryValueByCategory[].palletCount | Float | 該類別已佔用板數 |  |
| payload.inventoryValueByCategory[].itemCount | Integer | 該類別不同料品品項數 |  |
| payload.inventoryValueByCategory[].valueRatio | Float | 該類別庫存價值佔總庫存價值百分比 |  |
| payload.inventoryValueByCategory[].trend7Days | Float | 最近 7 日庫存價值變化率；第一版固定以 7 日計算，base value 為 0 時回傳 0.0 |  |
| payload.capacityByWarehouse[].warehouseNo | String | 倉儲別名 no |  |
| payload.capacityByWarehouse[].warehouseName | String | 倉儲別名名稱 |  |
| payload.capacityByWarehouse[].warehouseType | Integer | 倉儲空間類型 | ship_wh_alias.type |
| payload.capacityByWarehouse[].totalPallets | Float | 該倉儲可用總板數 |  |
| payload.capacityByWarehouse[].usedPallets | Float | 該倉儲已佔用板數 |  |
| payload.capacityByWarehouse[].reservedPallets | Float | 該倉儲已預留板數 |  |
| payload.capacityByWarehouse[].availablePallets | Float | 該倉儲剩餘可用板數 |  |
| payload.capacityByWarehouse[].utilizationRate | Float | 該倉儲板位使用率百分比 |  |
| payload.capacityByWarehouse[].riskLevel | Integer | 倉儲使用率風險等級；前端負責轉換顯示文字與樣式 | EWarehouseRiskLevel |
| payload.riskAlerts[].alertId | String | 風險警示唯一識別字串 |  |
| payload.riskAlerts[].riskType | String | 風險類型 | TURNOVER_OVER_30_DAYS、SHELF_LIFE_LT_ONE_THIRD、BELOW_SAFETY_STOCK |
| payload.riskAlerts[].riskLevel | Integer | 風險嚴重度；前端負責轉換顯示文字與樣式 | EWarehouseRiskLevel |
| payload.riskAlerts[].itemNo | String | 料品品項編號 |  |
| payload.riskAlerts[].itemName | String | 料品品項名稱 |  |
| payload.riskAlerts[].itemCategory | Integer | 料品品項類別 | EItemCategory |
| payload.riskAlerts[].batchNo | String | 批號 |  |
| payload.riskAlerts[].warehouseNo | String | 倉儲別名 no |  |
| payload.riskAlerts[].warehouseName | String | 倉儲別名名稱 |  |
| payload.riskAlerts[].quantity | Float | 目前庫存量 |  |
| payload.riskAlerts[].unit | Integer | 庫存量單位 | Unit |
| payload.riskAlerts[].inventoryValue | Integer | 該批庫存價值 |  |
| payload.riskAlerts[].daysInStock | Integer | 該批庫存自首次入庫起算的庫存天數 |  |
| payload.riskAlerts[].validDate | Integer | 批號效期日，UTC timestamp |  |
| payload.riskAlerts[].remainingShelfLifeRatio | Float | 剩餘效期比例；0.3333 表示剩餘三分之一效期 |  |
| payload.riskAlerts[].safetyStock | Float | 安全水位數量 |  |
| payload.riskAlerts[].messageCode | String | 風險說明多國語言代碼；前端依 code 與 params 產生顯示文字 |  |
| payload.riskAlerts[].messageParams.currentQuantity | Float | 風險訊息參數：目前庫存量 |  |
| payload.riskAlerts[].messageParams.daysInStock | Integer | 風險訊息參數：庫存天數 |  |
| payload.riskAlerts[].messageParams.validDate | Integer | 風險訊息參數：效期日 |  |
| payload.riskAlerts[].messageParams.remainingShelfLifeRatio | Float | 風險訊息參數：剩餘效期比例 |  |
| payload.riskAlerts[].messageParams.safetyStock | Float | 風險訊息參數：安全水位 |  |
| payload.riskAlerts[].recommendedActionCode | String | 建議處理方式多國語言代碼；前端依 code 轉換顯示文字 |  |
| payload.pendingTasks[].taskId | String | 流程任務識別碼 |  |
| payload.pendingTasks[].taskType | Integer | 任務類型 | 請購(1)、採購(2)、進貨(3)、入庫(4)、出庫(5)、移倉(6)、生產(7)、品檢(8)、出貨(9) |
| payload.pendingTasks[].refCategory | Integer | 來源類別；與資料表欄位 `refCategory` 保持一致 |  |
| payload.pendingTasks[].sourceNo | String | 來源單號 |  |
| payload.pendingTasks[].sourceSubNo | String | 來源明細編號 |  |
| payload.pendingTasks[].itemNo | String | 料品品項編號 |  |
| payload.pendingTasks[].itemName | String | 料品品項名稱 |  |
| payload.pendingTasks[].itemCategory | Integer | 料品品項類別 | EItemCategory |
| payload.pendingTasks[].batchNo | String | 批號 |  |
| payload.pendingTasks[].expectedQuantity | Float | 任務預計處理數量 |  |
| payload.pendingTasks[].processedQuantity | Float | 任務已處理數量 |  |
| payload.pendingTasks[].remainingQuantity | Float | 任務剩餘待處理數量 |  |
| payload.pendingTasks[].unit | Integer | 任務數量單位 | Unit |
| payload.pendingTasks[].palletCount | Float | 任務涉及板數 |  |
| payload.pendingTasks[].warehouseNo | String | 任務對應倉儲別名 no |  |
| payload.pendingTasks[].warehouseName | String | 任務對應倉儲別名名稱，來源為 `ship_wh_alias.name`；若查無則回傳空字串 |  |
| payload.pendingTasks[].dueTimestamp | Integer | 任務預計完成時間，UTC timestamp |  |
| payload.pendingTasks[].taskStatus | Integer | 任務狀態；前端負責轉換顯示文字 | EWorkflowTaskStatus |
| payload.pendingTasks[].ownerDepartment | Integer | 下一步負責部門；前端負責轉換顯示文字 | EDepartment |
| payload.pendingTasks[].blockReason | String | 任務阻塞原因或主管人工判斷備註 |  |
| payload.valueTrend | Array | 庫存價值趨勢，第一版回傳 7 日類別層級趨勢資料 |  |
| payload.inventory[].warehouseNo | String | 倉儲別名 no；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].warehouseName | String | 倉儲別名名稱；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].itemCategory | Integer | 料品品項類別；僅 `includeInventory=true` 時回傳 | EItemCategory |
| payload.inventory[].itemSubCategory | Integer | 料品品項子類別；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].itemType | Integer | 料品類型；僅 `includeInventory=true` 時回傳 | EItemType |
| payload.inventory[].itemNo | String | 料品品項編號；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].itemName | String | 料品品項名稱；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].batchNo | String | 批號；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].unit | Integer | 庫存數量單位；僅 `includeInventory=true` 時回傳 | Unit |
| payload.inventory[].currentQuantity | Float | 目前庫存量；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].reservedQuantity | Float | 預留數量；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].availableQuantity | Float | 可用數量；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].qualityHoldQuantity | Float | 品檢保留量；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].inventoryValue | Integer | 目前庫存價值；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].reservedValue | Integer | 預留價值；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].availableValue | Integer | 可用價值；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].qualityHoldValue | Integer | 品檢保留價值；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].firstInboundTimestamp | Integer | 該庫存批號首次入庫時間；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].validDays | Integer | 該批號有效天數；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].validDate | Integer | 該批號效期日；僅 `includeInventory=true` 時回傳 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 | EErrorCode |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤時通常為空物件 |  |

### Processing Flow

1. 讀取 `date`、`warehouse_no`、`itemCategory`、`includeInventory`、`riskOnly` 查詢條件，並取得 `x-timezone` 換算查詢營業日起訖 UTC timestamp。
2. 以 `inventory_item_month_statistic` 取得查詢營業日以前最新的批號層級月結庫存量與庫存價值，並以 `inventory_delta` 加總月結日後至查詢營業日的入庫/出庫數量與金額，補算目前庫存量與庫存價值。
3. 讀取 `inventory_record` 取得批號最早入庫時間；若統計結果為空、`inventory_delta` 最新日期早於查詢營業日，或特定 `warehouseNo + itemNo + batchNo` 未出現在月結統計與每日異動結果中，才以 `inventory_record` 作為防護性補算依據。
4. 過濾 `currentQuantity <= 0` 的批號庫存列；此類批號不回傳於庫存明細，也不產生風險警示。
5. 讀取 `batch_number` 補齊批號效期資訊，用於效期警示與庫存迴轉天數分析。
6. 讀取 `warehouse_inventory_reservation` 彙總有效預留數量與預留價值。
7. 讀取 `warehouse_quality_hold` 彙總有效品檢保留量與品檢保留價值。
8. 讀取 `warehouse_pallet_movement` 彙總各倉儲與各料品品項類別的已佔用板數、預留板數。
9. 讀取 `ship_wh_contract`、`ship_wh`、`ship_wh_alias` 計算各倉儲空間總板數與可用板數；因 `ship_wh_contract` 同時存放物流與倉庫合約，僅納入 `ship_wh_contract.category = 2` 的倉儲合約。
10. 讀取 `item_safety_stock`，以可用數量 `availableQuantity` 判斷低於安全水位之庫存風險。
11. 讀取 `warehouse_risk_rule` 補齊風險等級、`messageCode` 與 `recommendedActionCode`；後端不回傳繁中 fallback 文字，前端依 code 與 params 轉換顯示。
12. 依庫存迴轉超過 30 天、效期剩餘低於三分之一、安全水位不足建立 `riskAlerts`。
13. 讀取 `workflow_task_state` 取得查詢營業日結束前仍未完成的進貨、入庫、出庫、移倉、品檢、出貨等任務，並依 `ownerDepartment` 回傳下一步負責部門。
14. 整合 `summary`、`inventoryValueByCategory`、`capacityByWarehouse`、`riskAlerts`、`pendingTasks`；若 `includeInventory=true`，額外回傳批號層級庫存明細；若同時 `riskOnly=true`，庫存明細只回傳有風險的列。

### Database Tables Used

| Table | Purpose |
|----------|------|
| inventory_item_month_statistic | 提供批號層級月結庫存量與庫存價值，作為第一版目前庫存主計算基準 |
| inventory_delta | 提供月結日後每日入庫/出庫數量與金額異動，補算至查詢營業日 |
| inventory_record | 提供批號最早入庫時間；在統計結果為空、delta 日期未覆蓋查詢營業日，或統計資料未涵蓋特定庫存列時作為防護性補算依據 |
| batch_number | 提供批號效期、有效天數與批號來源資料 |
| warehouse_inventory_reservation | 提供預留數量、預留價值 |
| warehouse_quality_hold | 提供品檢保留量、品檢保留價值 |
| warehouse_pallet_movement | 提供各倉儲與各料品品項類別板數佔用狀態 |
| item_safety_stock | 提供料品安全水位 |
| warehouse_risk_rule | 提供風險等級、風險訊息代碼與建議處理方式代碼 |
| workflow_task_state | 提供待處理任務狀態與下一步負責部門 |
| ship_wh | 提供倉儲空間容量 |
| ship_wh_contract | 提供倉儲別名與倉儲空間對應；僅使用 category = 2 的倉儲合約 |
| ship_wh_alias | 提供倉儲別名名稱與類型 |

## GET /api/v2/warehouse/inventory

<a id="get-api-v2-warehouse-inventory"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/warehouse/inventory | GET | 查詢 Warehouse 庫存明細資料 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示時區；未提供時以 UTC 回傳 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| date | Integer | NO | 查詢基準時間，UTC timestamp；後端只納入此時間以前的庫存、預留、品檢與板位資料，未提供時以伺服器目前時間計算 |
| warehouse_no | String | NO | 倉儲別名 no |
| itemCategory | Integer | NO | 料品品項類別 |
| item_no | String | NO | 料品品項編號 |
| batchNo | String | NO | 批號 |
| riskType | String | NO | 風險類型；如 TURNOVER_OVER_30_DAYS、SHELF_LIFE_LT_ONE_THIRD、BELOW_SAFETY_STOCK |
| start | Integer | NO | 分頁起始位置 |
| count | Integer | NO | 分頁筆數；預設 50 |

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
        "inventoryValue": "Integer",
        "reservedValue": "Integer",
        "availableValue": "Integer",
        "qualityHoldValue": "Integer",
        "palletCount": "Float",
        "safetyStock": "Float",
        "validDays": "Integer",
        "validDate": "Integer",
        "firstInboundTimestamp": "Integer",
        "daysInStock": "Integer",
        "sourceNo": "String",
        "sourceRefCategory": "Integer",
        "qualityStatus": "String",
        "riskTypes": ["String"]
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.total | Integer | 符合條件的庫存明細總筆數 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.start | Integer | 分頁起始位置 |  |
| payload.results[].inventoryId | String | 庫存列識別碼，由倉儲、料品、批號、流水號組成 |  |
| payload.results[].warehouseNo | String | 倉儲別名 no |  |
| payload.results[].warehouseName | String | 倉儲別名名稱 |  |
| payload.results[].itemNo | String | 料品品項編號 |  |
| payload.results[].itemName | String | 料品品項名稱 |  |
| payload.results[].itemCategory | Integer | 料品品項類別；前端負責轉換顯示文字 | EItemCategory |
| payload.results[].itemSubCategory | Integer | 料品品項子類別；優先取 `batch_number.itemSubCategory`，不足時依料品類別取 `material.subCategory`、`inproduct.category`、`product.category` 或 `goods.subCategory` |  |
| payload.results[].itemType | Integer | 料品類型；優先取 `batch_number.itemType`，不足時取最近一筆 `inventory_record.itemType` 作為回退，前端負責轉換顯示文字 | EItemType |
| payload.results[].batchNo | String | 批號 |  |
| payload.results[].serialNo | String | 流水號；批號層級資料可為空字串 |  |
| payload.results[].currentQuantity | Float | 目前庫存量，數量欄位取至小數點第 2 位 |  |
| payload.results[].reservedQuantity | Float | 有效預留數量 |  |
| payload.results[].availableQuantity | Float | 可用數量，計算方式為目前庫存量扣除預留與品檢保留量 |  |
| payload.results[].qualityHoldQuantity | Float | 品檢保留量 |  |
| payload.results[].unit | Integer | 庫存單位；前端負責轉換顯示文字 | Unit |
| payload.results[].unitCost | Float | 庫存單位成本，取至小數點第 4 位 |  |
| payload.results[].inventoryValue | Integer | 目前庫存價值，金額四捨五入取整數 |  |
| payload.results[].reservedValue | Integer | 預留庫存價值 |  |
| payload.results[].availableValue | Integer | 可用庫存價值 |  |
| payload.results[].qualityHoldValue | Integer | 品檢保留庫存價值 |  |
| payload.results[].palletCount | Float | 佔用板數 |  |
| payload.results[].safetyStock | Float | 安全水位數量 |  |
| payload.results[].validDays | Integer | 批號有效天數 |  |
| payload.results[].validDate | Integer | 批號效期日，UTC timestamp |  |
| payload.results[].firstInboundTimestamp | Integer | 同倉儲同批號首次入庫時間，UTC timestamp |  |
| payload.results[].daysInStock | Integer | 庫存迴轉天數 |  |
| payload.results[].sourceNo | String | 批號來源單號，來源為 `batch_number.ref_no` |  |
| payload.results[].sourceRefCategory | Integer | 批號來源類別，來源為 `batch_number.refCategory`；與舊欄位 `sourceType` 為同一來源語意，正式回傳僅保留此數值 enum。前端不得再讀取 `sourceType`，需依此欄位轉換顯示來源文字。 | EInventoryRefCategory：其他/調整(0)、採購/進貨(1)、生產/製造(2)、銷貨退回或倉庫來源(3) |
| payload.results[].qualityStatus | String | 品檢狀態穩定代碼；目前依品檢保留量回傳 released 或 hold |  |
| payload.results[].riskTypes[] | String | 此庫存列符合的風險類型 | EWarehouseRiskType |

### Processing Flow

1. 讀取庫存篩選條件與分頁參數。
2. 沿用 Warehouse Dashboard 已確認的庫存彙總邏輯，以 `inventory_item_month_statistic` 月結批號層級結存搭配 `inventory_delta` 每日異動補算目前庫存量與庫存價值。
3. 過濾 `currentQuantity <= 0` 的批號庫存列；此類批號不回傳於庫存明細，也不產生風險警示。
4. 由 `batch_number` 補齊 `itemSubCategory`、`itemType`、有效天數、效期日、`sourceNo` 與 `sourceRefCategory`；若批號資料缺漏，`itemSubCategory` 依料品類別回查料品主檔。
5. 彙總有效預留量、品檢保留量與板位使用量，計算可用數量與可用價值。
6. 補齊首次入庫時間、安全水位與風險類型。
7. 套用 item_no、batchNo、riskType 與分頁條件後回傳結果。

### Database Tables Used

| Table | Purpose |
|----------|------|
| inventory_item_month_statistic | 提供批號層級月結庫存量與庫存價值，作為目前庫存主計算基準 |
| inventory_delta | 提供月結日後每日入庫/出庫數量與金額異動，補算至查詢營業日 |
| inventory_record | 提供首次入庫時間；在統計結果為空、delta 日期未覆蓋查詢營業日，或統計資料未涵蓋特定庫存列時作為防護性補算依據 |
| batch_number | 提供批號效期資訊、料品品項子類別、料品類型與批號來源單據；`sourceNo/sourceRefCategory` 以 `batch_number.ref_no/refCategory` 為準 |
| warehouse_inventory_reservation | 提供預留數量與預留價值 |
| warehouse_quality_hold | 提供品檢保留量與品檢保留價值 |
| warehouse_pallet_movement | 提供板數佔用狀態 |
| item_safety_stock | 提供安全水位 |
| warehouse_risk_rule | 提供風險訊息代碼與建議處理方式代碼 |
| material / inproduct / product / goods | 當 `batch_number.itemSubCategory` 缺漏時，依料品類別補齊料品品項子類別 |

## GET /api/v2/warehouse/inventory/lots

<a id="get-api-v2-warehouse-inventory-lots"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/warehouse/inventory/lots | GET | 查詢庫存批號明細清單 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示時區；未提供時以 UTC 回傳 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| date | Integer | NO | 查詢基準時間，UTC timestamp；未提供時以伺服器目前時間計算 |
| warehouse_no | String | NO | 倉儲別名 no |
| itemCategory | Integer | NO | 料品品項類別；原料(1)、物料(2)、膠捲(3)、在製品(4)、製成品(5) |
| item_no | String | NO | 料品品項編號 |
| batchNo | String | NO | 批號 |
| riskType | String | NO | 風險類型；TURNOVER_OVER_30_DAYS、SHELF_LIFE_LT_ONE_THIRD、BELOW_SAFETY_STOCK |
| taskType | Integer | NO | 任務類型；請購(1)、採購(2)、進貨(3)、入庫(4)、出庫(5)、移倉(6)、生產(7)、品檢(8)、出貨(9) |
| availability | String | NO | 可用狀態代碼；允許值：available、reserved、quality_hold、blocked |
| keyword | String | NO | 模糊搜尋：料號、品名、批號、來源單號、倉儲名稱 |
| sort | String | NO | 排序欄位代碼；允許值：inventoryValue、availableQuantity、validDate、daysInStock |
| order | String | NO | 排序方向代碼；允許值：asc、desc |
| start | Integer | NO | 分頁起始位置 |
| count | Integer | NO | 分頁筆數；預設 50 |

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
        "refNo": "String",
        "refCategory": "Integer"
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.total | Integer | 符合篩選條件且分頁前的總筆數 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.start | Integer | 本次分頁起始位置 |  |
| payload.summary.lotCount | Integer | 清單篩選條件下的批號庫存列數 |  |
| payload.summary.itemCount | Integer | 清單篩選條件下的不同料品品項數 |  |
| payload.summary.totalQuantity | Float | 清單篩選條件下的目前庫存量合計 | Unit |
| payload.summary.totalInventoryValue | Integer | 清單篩選條件下的庫存價值合計 |  |
| payload.summary.totalAvailableQuantity | Float | 清單篩選條件下的可用數量合計 | Unit |
| payload.summary.totalAvailableValue | Integer | 清單篩選條件下的可用價值合計 |  |
| payload.summary.riskLotCount | Integer | 清單篩選條件下命中任一風險類型的批號庫存列數 |  |
| payload.summary.pendingTaskCount | Integer | 清單篩選條件下未完成 workflow 任務數合計 |  |
| payload.results[].lotKey | String | 前端 drill-down 使用的批號庫存識別鍵，由 warehouseNo、itemNo、batchNo 組成 |  |
| payload.results[].warehouseNo | String | 倉儲別名 no |  |
| payload.results[].warehouseName | String | 倉儲別名名稱 |  |
| payload.results[].itemCategory | Integer | 料品品項類別；前端負責轉換顯示文字 | EItemCategory |
| payload.results[].itemNo | String | 料品品項編號 |  |
| payload.results[].itemName | String | 料品品項名稱 |  |
| payload.results[].batchNo | String | 批號 |  |
| payload.results[].unit | Integer | 庫存數量單位；前端負責轉換顯示文字 | Unit |
| payload.results[].currentQuantity | Float | 目前庫存量；`0` 不回傳，負數於開發階段保留以利追查資料異常 | Unit |
| payload.results[].reservedQuantity | Float | 預留數量 | Unit |
| payload.results[].qualityHoldQuantity | Float | 品檢保留量 | Unit |
| payload.results[].availableQuantity | Float | 可用數量，計算方式為目前庫存量扣除預留數量與品檢保留量 | Unit |
| payload.results[].unitCost | Float | 此批庫存計價用單價，計算方式為 inventoryValue / currentQuantity，取至小數點第 4 位 |  |
| payload.results[].inventoryValue | Integer | 目前庫存價值 |  |
| payload.results[].reservedValue | Integer | 預留庫存價值 |  |
| payload.results[].qualityHoldValue | Integer | 品檢保留庫存價值 |  |
| payload.results[].availableValue | Integer | 可用庫存價值 |  |
| payload.results[].palletCount | Float | 此批庫存佔用板數 |  |
| payload.results[].firstInboundTimestamp | Integer | 此批庫存在此倉儲的首次入庫時間，UTC timestamp |  |
| payload.results[].daysInStock | Integer | 從首次入庫日至查詢日的庫存天數 |  |
| payload.results[].validDays | Integer | 批號有效天數；來源為 batch_number.validDays |  |
| payload.results[].validDate | Integer | 批號效期日，UTC timestamp；來源為 batch_number.validDate |  |
| payload.results[].remainingShelfLifeRatio | Float | 剩餘效期比例 |  |
| payload.results[].safetyStock | Float | 此料品於此倉儲或全倉通用的安全水位數量 |  |
| payload.results[].riskTypes[] | String | 此批庫存命中的風險類型 | EWarehouseRiskType |
| payload.results[].openTaskCount | Integer | 此批庫存尚未完成的 workflow 任務數 |  |
| payload.results[].refNo | String | 批號來源單號；來源為 batch_number.ref_no |  |
| payload.results[].refCategory | Integer | 批號來源類別；來源為 batch_number.refCategory | EInventoryRefCategory |

### Processing Flow

1. 讀取查詢條件與分頁條件，建立料品、倉儲、批號、風險、任務與可用狀態篩選。
2. 透過 `CWarehouseInventorySnapshotCalculator` 取得目前庫存快照；主路徑以 `inventory_item_month_statistic` 搭配 `inventory_delta` 補算目前庫存量與庫存價值，當統計資料缺漏或日期覆蓋不足時才由 `inventory_record` 防護性補算。
3. 過濾 `currentQuantity == 0` 的批號庫存列；`currentQuantity < 0` 視為資料異常但保留回傳，方便開發與測試階段追查。
4. 從 `batch_number` 補充有效天數、效期日與批號來源資料；`refNo/refCategory` 以 `batch_number.ref_no/refCategory` 為準。
5. 從 `warehouse_inventory_reservation` 彙總有效預留數量與預留價值。
6. 從 `warehouse_quality_hold` 彙總品檢保留量與品檢保留價值。
7. 從 `warehouse_pallet_movement` 彙總此批庫存佔用板數。
8. 從 `item_safety_stock` 判斷是否低於安全水位。
9. 從 `workflow_task_state` 彙總未完成任務數，並支援 `taskType` 篩選。
10. 套用風險判斷：迴轉超過 30 天、剩餘效期低於三分之一、低於安全水位。
11. 回傳 summary 與分頁後 results；所有 enum 顯示文字由前端轉換。

### Database Tables Used

| Table | Purpose |
|----------|------|
| inventory_item_month_statistic | 提供批號層級月結庫存量與庫存價值，作為目前庫存主計算基準 |
| inventory_delta | 提供月結日後每日入庫/出庫數量與金額異動，補算至查詢營業日 |
| inventory_record | 提供首次入庫時間；在統計資料缺漏或日期覆蓋不足時作為防護性補算依據 |
| batch_number | 提供批號、效期與批號來源資訊；refNo/refCategory 以 batch_number.ref_no/refCategory 為準 |
| warehouse_inventory_reservation | 提供預留數量與預留價值 |
| warehouse_quality_hold | 提供品檢保留量與品檢保留價值 |
| warehouse_pallet_movement | 提供板位佔用狀態 |
| item_safety_stock | 提供安全水位 |
| workflow_task_state | 提供未完成任務與下一步負責部門 |
| ship_wh_alias | 提供倉儲別名與名稱 |

## GET /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}

<a id="get-api-v2-warehouse-inventory-lots-detail"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo} | GET | 查詢單一庫存批號追蹤明細 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示時區；未提供時以 UTC 回傳 |

### Path Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| warehouseNo | String | YES | 倉儲別名 no |
| itemNo | String | YES | 料品品項編號 |
| batchNo | String | YES | 批號 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| date | Integer | NO | 查詢基準時間，UTC timestamp；未提供時以伺服器目前時間計算 |

### Request Body

None

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
    "inventoryRecords": [
      {
        "refCategory": "Integer",
        "refNo": "String",
        "refSubNo": "String",
        "date": "Integer",
        "category": "Integer",
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

### Field Description

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.lot.lotKey | String | 前端 row key；由 warehouseNo、itemNo、batchNo 組成，僅供前端識別與選取狀態使用 |  |
| payload.lot.warehouseNo | String | 倉儲別名 no |  |
| payload.lot.warehouseName | String | 倉儲別名名稱 |  |
| payload.lot.itemCategory | Integer | 料品品項類別；前端負責轉換顯示文字 | EItemCategory |
| payload.lot.itemNo | String | 料品品項編號 |  |
| payload.lot.itemName | String | 料品品項名稱 |  |
| payload.lot.batchNo | String | 批號 |  |
| payload.lot.unit | Integer | 庫存數量單位；前端負責轉換顯示文字 | Unit |
| payload.lot.currentQuantity | Float | 目前庫存量；0 不回傳 detail，負數於開發階段保留以利 debug |  |
| payload.lot.reservedQuantity | Float | 有效預留數量 |  |
| payload.lot.qualityHoldQuantity | Float | 品檢保留數量 |  |
| payload.lot.availableQuantity | Float | 可用數量，計算方式為 max(currentQuantity - reservedQuantity - qualityHoldQuantity, 0) |  |
| payload.lot.unitCost | Float | 成本單價，計算方式為 inventoryValue / currentQuantity，單價取至小數點第 4 位 |  |
| payload.lot.inventoryValue | Integer | 目前庫存價值，金額四捨五入取整數 |  |
| payload.lot.availableValue | Integer | 可用庫存價值 |  |
| payload.lot.palletCount | Float | 此批庫存目前佔用板數 |  |
| payload.lot.validDate | Integer | 批號效期日，UTC timestamp |  |
| payload.lot.riskTypes[] | String | 此批庫存命中的風險類型 | EWarehouseRiskType |
| payload.inventoryRecords[].refCategory | Integer | 庫存異動來源單據類別；來源為 inventory_record.refCategory | EInventoryRefCategory |
| payload.inventoryRecords[].refNo | String | 庫存異動來源單號；來源為 inventory_record.ref_no |  |
| payload.inventoryRecords[].refSubNo | String | 庫存異動來源明細編號；第一版若無穩定來源則回傳空字串 |  |
| payload.inventoryRecords[].date | Integer | 庫存異動時間，UTC timestamp；來源為 inventory_record.date |  |
| payload.inventoryRecords[].category | Integer | 庫存異動類別；來源為 inventory_record.category，前端可依此判斷入庫或出庫方向 | EInventoryCategory：入庫(1)、出庫(2) |
| payload.inventoryRecords[].quantity | Float | 庫存異動數量；來源為 inventory_record.count，前端需帶方向統計時依 category 轉換 |  |
| payload.inventoryRecords[].amount | Integer | 庫存異動金額；來源為 inventory_record.amount，前端需帶方向統計時依 category 轉換 |  |
| payload.reservations[].reservationNo | String | 預留單識別碼 |  |
| payload.reservations[].refCategory | Integer | 預留來源類別；來源為 warehouse_inventory_reservation.refCategory | ReservationRefCategory：銷售/訂購(1)、生產/工單(2)、倉庫任務(3)、其他(0) |
| payload.reservations[].refNo | String | 預留來源單號；來源為 warehouse_inventory_reservation.ref_no |  |
| payload.reservations[].reservedQuantity | Float | 預留數量 |  |
| payload.reservations[].reservedValue | Integer | 預留庫存價值 |  |
| payload.reservations[].releaseTime | Integer | 預留釋放時間，UTC timestamp；無釋放時間可回傳 0 |  |
| payload.reservations[].status | Integer | 預留狀態 |  |
| payload.qualityHolds[].holdNo | String | 品檢保留識別碼 |  |
| payload.qualityHolds[].inspectionNo | String | 對應檢驗單號；第一版若尚未串接 Quality 模組可回傳空字串 |  |
| payload.qualityHolds[].holdQuantity | Float | 品檢保留數量 |  |
| payload.qualityHolds[].holdValue | Integer | 品檢保留庫存價值 |  |
| payload.qualityHolds[].reason | String | 品檢保留原因或備註 |  |
| payload.qualityHolds[].status | Integer | 品檢保留狀態 |  |
| payload.palletMovements[].movementNo | String | 板位異動識別碼 |  |
| payload.palletMovements[].date | Integer | 板位異動時間，UTC timestamp |  |
| payload.palletMovements[].palletGroupNo | String | 棧板或板位群組編號；若資料表未提供穩定欄位可回傳空字串 |  |
| payload.palletMovements[].palletStatus | Integer | 板位狀態 |  |
| payload.palletMovements[].palletCount | Float | 板數 |  |
| payload.palletMovements[].refCategory | Integer | 板位異動來源類別；來源為 warehouse_pallet_movement.refCategory | PalletMovementRefCategory：入庫(1)、出庫(2)、移倉(3)、預留(4)、品檢保留(5)、釋放(6) |
| payload.palletMovements[].refNo | String | 板位異動來源單號；來源為 warehouse_pallet_movement.ref_no |  |
| payload.workflowTasks[].taskId | String | workflow 任務識別碼 |  |
| payload.workflowTasks[].taskType | Integer | 任務類型 | EWorkflowTaskType |
| payload.workflowTasks[].taskStatus | Integer | 任務狀態；第一版僅回傳未完成任務 | EWorkflowTaskStatus |
| payload.workflowTasks[].ownerDepartment | Integer | 下一步負責部門；前端負責轉換顯示文字 | EDepartment |
| payload.workflowTasks[].expectedQuantity | Float | 預計處理數量 |  |
| payload.workflowTasks[].processedQuantity | Float | 已處理數量 |  |
| payload.workflowTasks[].remainingQuantity | Float | 剩餘待處理數量，計算方式為 max(expectedQuantity - processedQuantity, 0) |  |
| payload.workflowTasks[].dueTimestamp | Integer | 任務預計完成時間，UTC timestamp |  |
| payload.workflowTasks[].blockReason | String | 任務阻塞原因或主管人工判斷備註 |  |

### Processing Flow

1. 解析 path parameters，取得 warehouseNo、itemNo、batchNo；不採信前端其他暫存資料。
2. 重新彙總該批庫存目前數量與價值，避免使用前端帶入的暫存值。
3. 查詢該批庫存異動紀錄，組成 inventoryRecords；category=1 表示入庫，category=2 表示出庫。API 不回傳 signed 欄位，前端若需帶方向統計，可依 category 搭配 quantity/amount 自行換算。
4. 查詢有效預留、品檢保留、板位異動與未完成 workflow 任務。
5. 回傳 enum code，不回傳多國語言顯示文字。

### Database Tables Used

| Table | Purpose |
|----------|------|
| inventory_item_month_statistic | 提供批號層級月結庫存量與庫存價值，作為目前庫存主計算基準 |
| inventory_delta | 提供月結日後每日入庫/出庫數量與金額異動，補算至查詢營業日 |
| inventory_record | 提供 detail 庫存異動紀錄與防護性補算依據 |
| batch_number | 提供批號來源、效期與料品資訊 |
| warehouse_inventory_reservation | 提供有效預留資料 |
| warehouse_quality_hold | 提供品檢保留資料 |
| warehouse_pallet_movement | 提供板位異動資料 |
| item_safety_stock | 提供安全水位 |
| workflow_task_state | 提供未完成任務與下一步負責部門 |
| ship_wh_alias | 提供倉儲別名與名稱 |

## GET /api/v2/warehouse/tasks

<a id="get-api-v2-warehouse-tasks"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/warehouse/tasks | GET | 查詢 Warehouse 待處理任務 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示時區；未提供時以 UTC 回傳 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| date | Integer | NO | 查詢基準時間，UTC timestamp；提供時回傳到該日結束前仍待處理的任務 |
| taskType | Integer | NO | 任務類型 |
| warehouse_no | String | NO | 倉儲別名 no |
| status | String/Integer | NO | 任務狀態；支援 pending、partial、done、blocked、cancelled 或狀態代碼 |
| start | Integer | NO | 分頁起始位置 |
| count | Integer | NO | 分頁筆數；預設 50 |

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
    "results": [
      {
        "taskId": "String",
        "taskType": "Integer",
        "refCategory": "Integer",
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
        "palletCount": "Float",
        "warehouseNo": "String",
        "warehouseName": "String",
        "dueTimestamp": "Integer",
        "taskStatus": "Integer",
        "ownerDepartment": "Integer",
        "blockReason": "String"
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.total | Integer | 符合條件的任務總筆數 |  |
| payload.count | Integer | 本次回傳任務筆數 |  |
| payload.start | Integer | 分頁起始位置 |  |
| payload.results[].taskId | String | 任務識別碼 |  |
| payload.results[].taskType | Integer | 任務類型；前端負責轉換顯示文字 | EWorkflowTaskType |
| payload.results[].refCategory | Integer | 來源類別 |  |
| payload.results[].sourceNo | String | 來源單號 |  |
| payload.results[].sourceSubNo | String | 來源明細編號 |  |
| payload.results[].itemNo | String | 料品品項編號 |  |
| payload.results[].itemName | String | 料品品項名稱 |  |
| payload.results[].itemCategory | Integer | 料品品項類別 | EItemCategory |
| payload.results[].batchNo | String | 批號 |  |
| payload.results[].expectedQuantity | Float | 預計處理數量 |  |
| payload.results[].processedQuantity | Float | 已處理數量 |  |
| payload.results[].remainingQuantity | Float | 剩餘待處理數量 |  |
| payload.results[].unit | Integer | 任務數量單位 | Unit |
| payload.results[].palletCount | Float | 任務涉及板數 |  |
| payload.results[].warehouseNo | String | 任務對應倉儲別名 no |  |
| payload.results[].warehouseName | String | 任務對應倉儲別名名稱，來源為 `ship_wh_alias.name`；若查無則回傳空字串 |  |
| payload.results[].dueTimestamp | Integer | 任務預計完成時間，UTC timestamp |  |
| payload.results[].taskStatus | Integer | 任務狀態；前端負責轉換顯示文字 | EWorkflowTaskStatus |
| payload.results[].ownerDepartment | Integer | 下一步負責部門；前端負責轉換顯示文字 | EDepartment |
| payload.results[].blockReason | String | 任務阻塞原因或主管人工判斷備註 |  |

### Processing Flow

1. 讀取 date、taskType、warehouse_no、status 與分頁條件。
2. 若提供 status，依指定狀態查詢；若未提供，預設回傳 pending、partial、blocked。
3. 若提供 date，依 `x-timezone` 換算查詢營業日，回傳該營業日結束前仍待處理的任務。
4. 依 dueTimestamp 由早到晚排序，套用分頁。
5. 計算 remainingQuantity = expectedQuantity - processedQuantity 後回傳任務清單。

### Database Tables Used

| Table | Purpose |
|----------|------|
| workflow_task_state | 提供待處理任務狀態、數量、來源單號與下一步負責部門 |
