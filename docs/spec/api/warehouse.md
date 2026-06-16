# warehouse API Group

> Source: `restserver/package/restserver/api/v2/warehouse_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v2/warehouse/dashboard](#get-api-v2-warehouse-dashboard) | GET | 查詢 Warehouse Dashboard 經營總覽資料 | Need Review | [新增] 依 Warehouse 第一版 UX 需求與工程師確認後之資料庫新增規劃建立；待工程師以實際 MariaDB 測試資料確認。 |
| [/api/v2/warehouse/inventory/lots](warehouse_inventory_detail_proposal.md#get-apiv2warehouseinventorylots) | GET | 查詢庫存批號明細清單 | Implemented / Pending Runtime Review | [新增] 供 Warehouse Dashboard drill-down、庫存明細與批號追蹤畫面使用。 |
| [/api/v2/warehouse/inventory/lots/{lotKey}](warehouse_inventory_detail_proposal.md#get-apiv2warehouseinventorylotslotkey) | GET | 查詢單一庫存批號追蹤明細 | Implemented / Pending Runtime Review | [新增] 回傳來源單據、預留、品檢保留、板位異動與 workflow 任務。 |

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
| date | Integer | NO | 查詢基準時間，UTC timestamp；未提供時以伺服器目前時間計算 |
| warehouse_no | String | NO | 倉儲別名 no；提供時只回傳指定倉儲資料 |
| itemCategory | Integer | NO | 料品品項類別；原料(1)、物料(2)、膠捲(3)、在製品(4)、製成品(5) |
| includeInventory | Boolean/String | NO | 是否回傳庫存明細；支援 `1`、`true`、`yes` |
| riskOnly | Boolean/String | NO | 是否僅聚焦風險警示情境；第一版保留參數，聚合資料仍完整回傳 |

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
        "message": "String",
        "recommendedAction": "String"
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
    "valueTrend": [],
    "inventory": [
      {
        "warehouseNo": "String",
        "warehouseName": "String",
        "itemCategory": "Integer",
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
| payload.range.date | String | 查詢基準日期，格式為 YYYY-MM-DD |  |
| payload.range.startTimestamp | Integer | 查詢日期起始時間，UTC timestamp |  |
| payload.range.endTimestamp | Integer | 查詢日期結束時間，UTC timestamp |  |
| payload.summary.totalInventoryValue | Integer | 目前庫存總價值，依 `inventory_record` 入庫金額減出庫金額彙總 |  |
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
| payload.inventoryValueByCategory[].trend7Days | Float | 最近 7 日價值趨勢；第一版保留欄位，尚未計算 |  |
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
| payload.riskAlerts[].message | String | 風險說明文字 |  |
| payload.riskAlerts[].recommendedAction | String | 建議處理方式 |  |
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
| payload.pendingTasks[].warehouseName | String | 任務對應倉儲別名名稱；第一版若任務狀態表未存放名稱則回傳空字串 |  |
| payload.pendingTasks[].dueTimestamp | Integer | 任務預計完成時間，UTC timestamp |  |
| payload.pendingTasks[].taskStatus | Integer | 任務狀態；前端負責轉換顯示文字 | EWorkflowTaskStatus |
| payload.pendingTasks[].ownerDepartment | Integer | 下一步負責部門；前端負責轉換顯示文字 | EDepartment |
| payload.pendingTasks[].blockReason | String | 任務阻塞原因或主管人工判斷備註 |  |
| payload.valueTrend | Array | 庫存價值趨勢；第一版保留空陣列，待交易歷史需求確認後擴充 |  |
| payload.inventory[].warehouseNo | String | 倉儲別名 no；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].warehouseName | String | 倉儲別名名稱；僅 `includeInventory=true` 時回傳 |  |
| payload.inventory[].itemCategory | Integer | 料品品項類別；僅 `includeInventory=true` 時回傳 | EItemCategory |
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

1. 讀取 `date`、`warehouse_no`、`itemCategory`、`includeInventory`、`riskOnly` 查詢條件，並取得 `x-timezone` 作為前端顯示時區。
2. 以 `inventory_record` 依倉儲、料品品項類別、料品、批號、單位彙總目前庫存量與庫存價值；入庫類別加總，出庫類別扣除。
3. 讀取 `batch_number` 補齊批號效期資訊，用於效期警示與庫存迴轉天數分析。
4. 讀取 `warehouse_inventory_reservation` 彙總有效預留數量與預留價值。
5. 讀取 `warehouse_quality_hold` 彙總有效品檢保留量與品檢保留價值。
6. 讀取 `warehouse_pallet_movement` 彙總各倉儲與各料品品項類別的已佔用板數、預留板數。
7. 讀取 `ship_wh_contract`、`ship_wh`、`ship_wh_alias` 計算各倉儲空間總板數與可用板數；因 `ship_wh_contract` 同時存放物流與倉庫合約，僅納入 `ship_wh_contract.category = 2` 的倉儲合約。
8. 讀取 `item_safety_stock` 判斷低於安全水位之庫存風險。
9. 讀取 `warehouse_risk_rule` 補齊風險等級、風險說明文字與建議處理方式；若尚未設定規則，使用 API 內建預設文字。
10. 依庫存迴轉超過 30 天、效期剩餘低於三分之一、安全水位不足建立 `riskAlerts`。
11. 讀取 `workflow_task_state` 取得待處理進貨、入庫、出庫、移倉、品檢、出貨等任務，並依 `ownerDepartment` 回傳下一步負責部門。
12. 整合 `summary`、`inventoryValueByCategory`、`capacityByWarehouse`、`riskAlerts`、`pendingTasks`；若 `includeInventory=true`，額外回傳批號層級庫存明細。

### Database Tables Used

| Table | Purpose |
|----------|------|
| inventory_record | 提供目前庫存量與庫存價值彙總基礎 |
| batch_number | 提供批號效期與有效天數 |
| warehouse_inventory_reservation | 提供預留數量、預留價值 |
| warehouse_quality_hold | 提供品檢保留量、品檢保留價值 |
| warehouse_pallet_movement | 提供各倉儲與各料品品項類別板數佔用狀態 |
| item_safety_stock | 提供料品安全水位 |
| warehouse_risk_rule | 提供風險等級、風險說明文字與建議處理方式 |
| workflow_task_state | 提供待處理任務狀態與下一步負責部門 |
| ship_wh | 提供倉儲空間容量 |
| ship_wh_contract | 提供倉儲別名與倉儲空間對應；僅使用 category = 2 的倉儲合約 |
| ship_wh_alias | 提供倉儲別名名稱與類型 |
