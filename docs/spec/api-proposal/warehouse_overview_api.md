# 倉庫經營總覽 API 草案

狀態：草案 / 待工程師確認  
日期：2026-06-11  
用途：依據第一版 Warehouse 前端 UX，定義後端 API 開發前的資料集、欄位語意、處理流程與待確認演算法。  
適用對象：後端工程師、DB schema 維護者、前端整合開發者。

## 文件定位

本文件是「API 草案」，不是目前 `restserver/` 已實作 API 的正式文件，因此放置於 `docs/spec/api-proposal/`。  
正式已實作 API 文件仍以 `docs/spec/api/` 為準。

此文件的目標是讓前端、後端與資料庫文件對齊同一套業務語意，先確認 API flow 與 algorithm，再進入後端實作與前後端整合。

## 本次更新摘要

本次已依工程師回覆新增並整理「工程師回覆」欄位，並將可確認項目更新為較明確的狀態。

| 項目 | 更新結果 |
| --- | --- |
| API route | 工程師建議建立新的 Warehouse route，實作目標調整為 `/api/v2/warehouse/*`。 |
| 庫存價值 | 工程師確認以 `inventory_record.amount` 為主要基準；統計表與 delta 可作為彙總與補算來源。 |
| 單位成本 | 工程師建議取自 `item_price.costPriceWeight`。 |
| Enum 多國語言 | 料品品項類別、風險類型、任務狀態等 enum 顯示文字由前端轉換。 |
| 類別庫存量顯示 | 以「料品品項」類別分類顯示庫存量時，因可能混合單位，前端不顯示庫存單位。 |
| 效期警示 | 物料、膠捲排除於「少於三分之一效期」警示。 |
| Dashboard 明細 | Dashboard 預設不包含庫存明細列；明細由 `includeInventory=true` 或獨立 inventory API 取得。 |
| 今日待處理 | 包含今日到期與逾期未完成任務。 |

尚未進行資料庫規劃與程式實作的項目，已另行整理為工程師 review 文件：

1. `docs/spec/database/WAREHOUSE_OVERVIEW_DB_EXTENSION_PLAN.md`
2. `docs/engineering/WAREHOUSE_OVERVIEW_BACKEND_FLOW_ALGORITHM.md`

## 業務名詞對齊

| UX/UI 用語 | DB/API 對應語意 | 說明 | 工程師回覆 |
| --- | --- | --- |--- |
| 原料 | `itemCategory = 1` | 食品加工投入的主要原物料。 |  正確 |
| 物料 | `itemCategory = 2` | 包材、耗材或非主要食品原料。 | 正確 |
| 膠捲 | `itemCategory = 3` | 封膜、膠捲等包裝材料。 | 正確 |
| 在製品 | `itemCategory = 4` | 製程中間品或半成品。 | 正確 |
| 製成品 | `itemCategory = 5` | 可供出貨或銷售的完成品。 | 正確 |
| 貨品 | `itemCategory = 6` | DB 文件保留類別；Warehouse V1 第一版暫不作為主要統計分類。 | 正確 |
| 倉儲別名 | `ship_wh_alias` | 前端顯示的倉庫/倉位/物流倉儲別名。 | 正確 |
| 庫存價值 | `inventory_record.amount`、`inventory_delta`、`inventory_item_month_statistic`、`inventory_month_statistic` | 實際使用來源待工程師確認。 | 注意事項: 資料庫的date/time/creationTime欄位記載的是UTC時間; 若資料表中出現timezone欄位, 此時date紀載的是用戶端的日期。<br>`inventory_record.amount`: 記錄每筆出入庫的「料品品項」金額。<br>`inventory_delta`: 記錄「料品品項」每日入庫累積數量/金額 、採購累積數量/金額 、 出庫累積數量/金額。<br>`inventory_item_month_statistic`:記載每個月底結算的各個倉儲中的各個「料品品項」和 各個「批號」 的庫存量與庫存價值。<br>`inventory_month_statistic`: 記載每個月底結算的各個倉儲中的各個「料品品項」類別的庫存量與庫存價值。 |
| 佔用板數 | `batchno_serialno_group.group` 候選 | 是否以棧板編號計算佔用板數待工程師確認。 | `batchno_serialno_group.group`: 記錄棧板與批號之間的對應關係，設計上允許多個批號存放於同一個棧板。<br> 目前只規劃棧板與批號對應關係，出入庫紀錄與棧板對應關係尚未規劃與實作。 |
| 安全水位 | 尚待確認 | 目前 DB 文件尚未確認明確來源欄位。 | 尚未規劃與實作 |
| 效期 | `batch_number.validDays`、`batch_number.validDate` | 批號有效天數與有效期限。 | 正確 |
| 迴轉週期 | 最早入庫日到查詢日的天數 | 可由 `inventory_record` 同批號同倉儲的最早入庫紀錄推導。 | 正確 |

## 前端使用情境

Warehouse 第一版是管理者視角的倉庫經營總覽，優先回答以下問題：

1. 目前庫存資金分布在哪些類別：原料、物料、膠捲、在製品、製成品。
2. 各倉儲空間目前佔用多少板，還有多少可用板位。
3. 哪些庫存有風險：迴轉超過一個月、少於三分之一效期、低於安全水位。
4. 今天還有哪些入庫、出庫、移倉或確認事項未處理。
5. 管理者能否從批號追溯到來源單據與處理流程。

## API Summary

| URL | Method | 說明 | 狀態 | 備註 |
| --- | --- | --- | --- | --- |
| `/api/v2/warehouse/dashboard` | GET | 查詢倉庫經營總覽聚合資料 | 草案 | 前端第一版主要串接 API。 |
| `/api/v2/warehouse/inventory` | GET | 查詢庫存明細資料 | 草案 | 可作為總覽表格與明細 drill-down API。 |
| `/api/v2/warehouse/tasks` | GET | 查詢待處理入出庫任務 | 草案 | 可獨立供待處理頁籤與任務列表使用。 |

## 前端顯示與多國語言規則

1. 後端以 enum code 或穩定 code 作為資料交換基準，例如 `itemCategory = 1`、`riskType = TURNOVER_OVER_30_DAYS`、`status = pending`。
2. 前端負責 enum 到多國語言字串的轉換，例如 `itemCategory = 1` 顯示為「原料」。後端不回傳 `categoryName` 作為繁中 fallback。
3. 類別層級的庫存量因可能混合不同單位，Warehouse 第一版畫面不顯示庫存單位；後端若回傳 `unit`，混合單位時建議回傳 `0`。
4. 明細層級、風險警示與任務列仍保留 `unit` 欄位，因這些資料通常可對應單一料品與單位。
5. 風險說明文字與建議處理方式由前端依 `messageCode`、`messageParams` 與 `recommendedActionCode` 轉換；後端不回傳 `message` 與 `recommendedAction` 繁中 fallback。

## 共用回傳格式

建議沿用現有 `restserver` 回傳慣例：

```json
{
  "code": 0,
  "message": "success",
  "payload": {}
}
```

| Field Path | Type | 說明 | Enum |
| --- | --- | --- | --- |
| code | Integer | API 回傳代碼；`0` 表示成功。 | `EErrorCode.ERROR_SUCCESS = 0` |
| message | String | API 回傳訊息。 |  |
| payload | Object | 各 API 實際資料內容。 |  |

## GET /api/v2/warehouse/dashboard

### API 說明

查詢 Warehouse 第一版畫面所需的經營總覽資料，包含 KPI、庫存價值分類、倉儲容量、風險警示、待處理任務、價值趨勢與可選的庫存明細列。

此 API 建議作為前端 Warehouse 頁面的第一個 read-only integration target。

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/warehouse/dashboard` | GET | 查詢倉庫經營總覽聚合資料 |

### Request Header

| Header | 說明 |
| --- | --- |
| x-auth-token | 存取金鑰。 |

### Query Parameters

| Parameter | Type | Required | 說明 | 工程師回覆 |
| --- | --- | --- | --- | --- |
| date | Integer | NO | 查詢基準時間戳。未提供時使用伺服器目前時間。 | 注意事項: 資料庫的date/time/creationTime欄位記載的是UTC時間; 若資料表中出現timezone欄位, 此時date紀載的是用戶端的日期。記得進行local time 與 utc timestamp的轉換| 
| timezone | String | NO | 使用者時區，例如 `Asia/Taipei`。未提供時沿用 restserver 既有時區處理。 ||
| warehouse_no | String | NO | 依倉儲別名編號篩選，對應 `ship_wh_alias.no`。 ||
| itemCategory | Integer | NO | 依料品品項類別篩選。 ||
| includeInventory | Boolean | NO | 是否在總覽回傳中包含庫存明細列。預設 `false`。 ||
| riskOnly | Boolean | NO | 是否只回傳有風險的庫存資料。預設 `false`。 ||

### Request Body

None

### Success Response Data

```json
{
  "code": 0,
  "message": "success",
  "payload": {
    "serverTimestamp": 1781126400,
    "timezone": "Asia/Taipei",
    "range": {
      "date": "2026-06-11",
      "startTimestamp": 1781107200,
      "endTimestamp": 1781193599
    },
    "summary": {
      "totalInventoryValue": 7420000,
      "reservedInventoryValue": 2600000,
      "availableInventoryValue": 4820000,
      "qualityHoldInventoryValue": 180000,
      "totalPallets": 428,
      "usedPallets": 310,
      "reservedPallets": 24,
      "availablePallets": 94,
      "riskAlertCount": 18,
      "pendingInboundCount": 8,
      "pendingOutboundCount": 11
    },
    "inventoryValueByCategory": [
      {
        "itemCategory": 1,
        "inventoryValue": 2140000,
        "reservedValue": 380000,
        "availableValue": 1760000,
        "qualityHoldValue": 120000,
        "quantity": 12800,
        "unit": 0,
        "palletCount": 128,
        "itemCount": 94,
        "valueRatio": 29.0,
        "trend7Days": 4.2
      }
    ],
    "capacityByWarehouse": [
      {
        "warehouseNo": "FZ-A03",
        "warehouseName": "原料冷凍庫",
        "warehouseType": 2,
        "totalPallets": 160,
        "usedPallets": 128,
        "reservedPallets": 8,
        "availablePallets": 24,
        "utilizationRate": 80.0,
        "riskLevel": "warning"
      }
    ],
    "riskAlerts": [
      {
        "alertId": "EXP-RM260506-CORN-FZ-A03",
        "riskType": "SHELF_LIFE_LT_ONE_THIRD",
        "riskLevel": "danger",
        "itemNo": "RM-CORN-001",
        "itemName": "冷凍玉米粒",
        "itemCategory": 1,
        "batchNo": "RM260506-CORN",
        "warehouseNo": "FZ-A03",
        "warehouseName": "原料冷凍庫",
        "quantity": 180,
        "unit": 2,
        "inventoryValue": 12600,
        "daysInStock": 36,
        "validDate": 1782547200,
        "remainingShelfLifeRatio": 0.18,
        "safetyStock": 420,
        "messageCode": "warehouse.risk.shelfLifeLtOneThird",
        "messageParams": {
          "currentQuantity": 180,
          "daysInStock": 36,
          "validDate": 1782547200,
          "remainingShelfLifeRatio": 0.18,
          "safetyStock": 420
        },
        "recommendedActionCode": "warehouse.action.prioritizeIssueOrProduction"
      }
    ],
    "pendingTasks": [
      {
        "taskId": "WH-IN-GRN-20260611-018",
        "taskType": "INBOUND",
        "sourceType": "PURCHASE",
        "sourceNo": "GRN-20260611-018",
        "sourceSubNo": "",
        "itemNo": "RM-CHK-001",
        "itemName": "雞胸肉原料",
        "itemCategory": 1,
        "batchNo": "RM260611-CHK",
        "expectedQuantity": 600,
        "processedQuantity": 0,
        "unit": 2,
        "palletCount": 10,
        "warehouseNo": "FZ-A03",
        "warehouseName": "原料冷凍庫",
        "dueTimestamp": 1781145600,
        "status": "pending",
        "ownerDepartment": "倉庫部"
      }
    ],
    "valueTrend": [
      {
        "date": "2026-06-10",
        "itemCategory": 1,
        "inventoryValue": 2100000
      }
    ],
    "inventory": []
  }
}
```

### Success Response Field Description

| Field Path | Type | 說明 | Enum / 備註 | 工程師回覆 |
| --- | --- | --- | --- | --- |
| payload.serverTimestamp | Integer | 產生本次總覽資料的伺服器時間。 |  |  |
| payload.timezone | String | 本次查詢採用的時區。 |  |  |
| payload.range.date | String | 查詢營業日期，格式 `YYYY-MM-DD`。 |  |  |
| payload.range.startTimestamp | Integer | 查詢日期起始時間戳。 |  |  |
| payload.range.endTimestamp | Integer | 查詢日期結束時間戳。 |  |  |
| payload.summary.totalInventoryValue | Float | 查詢範圍內庫存總價值。 |  |  |
| payload.summary.reservedInventoryValue | Float | 已被訂單、工單備料或倉庫任務預留的庫存價值。 | 待確認預留邏輯 | 尚未規劃與實作 |
| payload.summary.availableInventoryValue | Float | 扣除預留量與品檢保留量後可使用的庫存價值。 | 待確認可用量邏輯 | 尚未規劃與實作 |
| payload.summary.qualityHoldInventoryValue | Float | 因品檢未放行或保留而不可用的庫存價值。 | 待確認品檢來源 | 尚未規劃與實作 |
| payload.summary.totalPallets | Integer | 查詢範圍內倉儲總可用板位。 | 待確認容量來源 | 尚未規劃與實作 |
| payload.summary.usedPallets | Integer | 目前已佔用板數。 | 候選來源：`batchno_serialno_group` | 尚未規劃與實作 |
| payload.summary.reservedPallets | Integer | 已被待處理任務預留的板數。 | 待確認 | 尚未規劃與實作 |
| payload.summary.availablePallets | Integer | 尚可使用板數。 | `totalPallets - usedPallets - reservedPallets` | 尚未規劃與實作 |
| payload.summary.riskAlertCount | Integer | 風險警示總筆數。 |  | 尚未規劃與實作 |
| payload.summary.pendingInboundCount | Integer | 今日與逾期待處理入庫任務數。 | 任務來源與狀態見 `warehouse_task_state` 規劃 | 尚未規劃與實作 |
| payload.summary.pendingOutboundCount | Integer | 今日與逾期待處理出庫任務數。 | 任務來源與狀態見 `warehouse_task_state` 規劃 | 尚未規劃與實作 |
| payload.inventoryValueByCategory[].itemCategory | Integer | 料品品項類別代碼。 | 原料(1)、物料(2)、膠捲(3)、在製品(4)、製成品(5)、貨品(6)、其他(0) | 前端依 enum code 轉換多國語言顯示文字 |
| payload.inventoryValueByCategory[].inventoryValue | Float | 該類別目前庫存價值。 | 以 `inventory_record.amount` 為主要基準，統計表與 delta 支援彙總補算 | 已確認方向 |
| payload.inventoryValueByCategory[].reservedValue | Float | 該類別已預留庫存價值。 | 待確認 | 尚未規劃與實作 |
| payload.inventoryValueByCategory[].availableValue | Float | 該類別可用庫存價值。 | 待確認 | 尚未規劃與實作 |
| payload.inventoryValueByCategory[].qualityHoldValue | Float | 該類別品檢保留庫存價值。 | 待確認 | 尚未規劃與實作 |
| payload.inventoryValueByCategory[].quantity | Float | 該類別目前庫存數量。 | 混合單位時僅作參考 ||
| payload.inventoryValueByCategory[].unit | Integer | 庫存單位。若類別內混合單位，建議回傳 `0`。 | Unit 單位定義 | 類別庫存量畫面不顯示庫存單位 |
| payload.inventoryValueByCategory[].palletCount | Integer | 該類別佔用板數。 | 待確認計算來源 | 尚未規劃與實作 |
| payload.inventoryValueByCategory[].itemCount | Integer | 該類別不同料品品項數。 |  |  |
| payload.inventoryValueByCategory[].valueRatio | Float | 該類別庫存價值佔總庫存價值比例。 |  |  |
| payload.inventoryValueByCategory[].trend7Days | Float | 該類別近 7 日庫存價值變化率。 | 待確認是否由後端計算 | 由後端計算, 尚未規劃與實作 |
| payload.capacityByWarehouse[].warehouseNo | String | 倉儲別名編號。 | `ship_wh_alias.no` |  |
| payload.capacityByWarehouse[].warehouseName | String | 倉儲別名名稱。 | `ship_wh_alias.name` 或統計表 displayName |  |
| payload.capacityByWarehouse[].warehouseType | Integer | 倉儲別名類型。 | 自有(1)、合約(2)、客供(3)、其他(0) |  |
| payload.capacityByWarehouse[].totalPallets | Integer | 該倉儲總板位。 | 待確認來源 | 尚未規劃與實作 |
| payload.capacityByWarehouse[].usedPallets | Integer | 該倉儲已佔用板數。 | 待確認 | 尚未規劃與實作 |
| payload.capacityByWarehouse[].reservedPallets | Integer | 該倉儲預留板數。 | 待確認 | 尚未規劃與實作 |
| payload.capacityByWarehouse[].availablePallets | Integer | 該倉儲可用板數。 | 待確認 | 尚未規劃與實作 |
| payload.capacityByWarehouse[].utilizationRate | Float | 倉儲使用率。 | `usedPallets / totalPallets` | 尚未規劃與實作 |
| payload.capacityByWarehouse[].riskLevel | String | 倉儲容量風險等級。 | `normal`、`warning`、`danger` | 尚未規劃與實作 |
| payload.riskAlerts[].alertId | String | 風險警示識別碼。 | 建議由風險類型、倉儲、料品、批號組成 | 尚未規劃與實作 |
| payload.riskAlerts[].riskType | String | 風險類型。 | `TURNOVER_OVER_30_DAYS`、`SHELF_LIFE_LT_ONE_THIRD`、`BELOW_SAFETY_STOCK` | 尚未規劃與實作 |
| payload.riskAlerts[].riskLevel | String | 風險嚴重度。 | `normal`、`warning`、`danger` | 尚未規劃與實作 |
| payload.riskAlerts[].itemNo | String | 料品品項編號。 |  |  |
| payload.riskAlerts[].itemName | String | 料品品項名稱。 |  |  |
| payload.riskAlerts[].itemCategory | Integer | 料品品項類別。 | EItemCategory |  |
| payload.riskAlerts[].batchNo | String | 批號。 | `batch_number.no` |  |
| payload.riskAlerts[].warehouseNo | String | 倉儲別名編號。 |  |  |
| payload.riskAlerts[].warehouseName | String | 倉儲別名名稱。 |  |  |
| payload.riskAlerts[].quantity | Float | 該風險批號目前庫存數量。 |  | 尚未規劃與實作 |
| payload.riskAlerts[].unit | Integer | 庫存單位。 | Unit 單位定義 |  |
| payload.riskAlerts[].inventoryValue | Float | 該風險批號目前庫存價值。 |  | 尚未規劃與實作 |
| payload.riskAlerts[].daysInStock | Integer | 從最早入庫日到查詢日的天數。 |  |  |
| payload.riskAlerts[].validDate | Integer | 批號有效期限。 | `batch_number.validDate` |  |
| payload.riskAlerts[].remainingShelfLifeRatio | Float | 剩餘效期比例。 |  |  |
| payload.riskAlerts[].safetyStock | Float | 安全水位數量。 | 待確認來源 | 尚未規劃與實作 |
| payload.riskAlerts[].messageCode | String | 風險說明多國語言代碼。 | 前端依 code 與 params 轉換顯示 | 已調整為前端轉換 |
| payload.riskAlerts[].messageParams.currentQuantity | Float | 風險訊息參數：目前庫存量。 |  | 已調整為前端轉換 |
| payload.riskAlerts[].messageParams.daysInStock | Integer | 風險訊息參數：庫存天數。 |  | 已調整為前端轉換 |
| payload.riskAlerts[].messageParams.validDate | Integer | 風險訊息參數：效期日。 |  | 已調整為前端轉換 |
| payload.riskAlerts[].messageParams.remainingShelfLifeRatio | Float | 風險訊息參數：剩餘效期比例。 |  | 已調整為前端轉換 |
| payload.riskAlerts[].messageParams.safetyStock | Float | 風險訊息參數：安全水位。 |  | 已調整為前端轉換 |
| payload.riskAlerts[].recommendedActionCode | String | 建議處理方式多國語言代碼。 | 前端依 code 轉換顯示 | 已調整為前端轉換 |
| payload.pendingTasks[].taskId | String | 任務識別碼。 | 建議由任務類型與來源單號組成 |  |
| payload.pendingTasks[].taskType | String | 任務類型。 | `INBOUND`、`OUTBOUND`、`TRANSFER`、`COUNTING` |  |
| payload.pendingTasks[].sourceType | String | 來源單據類型。 | `PURCHASE`、`SALE`、`WORK`、`INVENTORY`、`OTHER` |  |
| payload.pendingTasks[].sourceNo | String | 來源單號。 |  |  |
| payload.pendingTasks[].sourceSubNo | String | 來源單據明細編號；若無則回傳空字串。 |  |  |
| payload.pendingTasks[].itemNo | String | 料品品項編號。 |  | |
| payload.pendingTasks[].itemName | String | 料品品項名稱。 |  | |
| payload.pendingTasks[].itemCategory | Integer | 料品品項類別。 | EItemCategory | |
| payload.pendingTasks[].batchNo | String | 批號；尚未產生批號時可回傳空字串。 |  | |
| payload.pendingTasks[].expectedQuantity | Float | 來源單據預期處理數量。 |  | |
| payload.pendingTasks[].processedQuantity | Float | 已完成入庫或出庫處理數量。 |  | |
| payload.pendingTasks[].unit | Integer | 任務數量單位。 | Unit 單位定義 |  |
| payload.pendingTasks[].palletCount | Integer | 任務相關板數。 | 待確認 | 尚未規劃與實作 |
| payload.pendingTasks[].warehouseNo | String | 目標或來源倉儲別名編號。 |  | |
| payload.pendingTasks[].warehouseName | String | 目標或來源倉儲別名名稱。 |  | |
| payload.pendingTasks[].dueTimestamp | Integer | 預計處理時間。 |  | 尚未規劃與實作 |
| payload.pendingTasks[].status | String | 任務狀態。 | `pending`、`partial`、`done`、`blocked` | 尚未規劃與實作 |
| payload.pendingTasks[].ownerDepartment | String | 下一步負責部門。 | 倉庫部、品保部、生管部、業務部、採購部 | 尚未規劃與實作 |
| payload.valueTrend[].date | String | 趨勢日期，格式 `YYYY-MM-DD`。 |  |  |
| payload.valueTrend[].itemCategory | Integer | 料品品項類別。 | EItemCategory |  |
| payload.valueTrend[].inventoryValue | Float | 該日期該類別庫存價值。 |  |  |
| payload.inventory[] | Array | 可選的庫存明細列。若 `includeInventory=false`，可回傳空陣列。 |  |  |

### Processing Flow

1. 讀取 `date`、`timezone`、`warehouse_no`、`itemCategory`、`includeInventory`、`riskOnly` 查詢參數。
2. 依時區將 `date` 轉換為查詢營業日的起訖時間。
3. 查詢目前庫存資料，依倉儲別名、料品品項、批號彙總庫存數量與庫存價值。
4. 查詢批號資料，取得批號、有效天數、有效期限、料品類別、單位、來源單據關係。
5. 以入庫數量減出庫數量計算目前庫存數量。
6. 依工程師確認的成本/金額來源計算庫存價值。
7. 依 `WAREHOUSE_OVERVIEW_DB_EXTENSION_PLAN.md` 的新增規劃計算預留數量、預留價值、可用數量與可用價值。
8. 依 `WAREHOUSE_OVERVIEW_DB_EXTENSION_PLAN.md` 的新增規劃計算品檢保留量與品檢保留價值。
9. 依 `WAREHOUSE_OVERVIEW_DB_EXTENSION_PLAN.md` 的新增規劃計算各類別與各倉儲佔用板數。
10. 計算風險警示：
    - 迴轉超過一個月：`daysInStock > 30`。
    - 少於三分之一效期：`validDate - 查詢日 <= validDays / 3`；物料、膠捲排除。
    - 低於安全水位：目前數量或可用數量低於安全水位。
11. 比對來源單據預期數量與 `inventory_record` 已處理數量，並依新增任務狀態規劃建立今日與逾期待處理入出庫任務。
12. 組裝 `summary`、`inventoryValueByCategory`、`capacityByWarehouse`、`riskAlerts`、`pendingTasks`、`valueTrend` 與可選 `inventory` 資料集。

### Database Tables Used

| Table | 用途 | 工程師回覆 |
| --- | --- | --- |
| inventory_record | 取得入庫/出庫紀錄、目前庫存數量、倉儲別名、料品、批號、來源單據、單價與金額。 | 正確 |
| inventory_delta | 取得每日庫存異動彙總，可支援趨勢與即時補算。 |正確 |
| inventory_item_month_statistic | 取得每月料品或批號層級庫存數量與庫存價值。 | 正確 |
| inventory_month_statistic | 取得每月類別層級庫存價值。 | 正確 |
| batch_number | 取得批號、料品、有效天數、有效期限、預期數量、確認數量與來源單據關係。 | 來源單據關聯至進貨單號、領退餘廢產單號、銷貨單號, 當進貨單號或領退餘廢產單號產生時，系統會同時建立對應的批號; 預期數量取自來源單據上的數量、確認數量取自實際出入庫紀錄的數量 |
| batchno_serialno | 取得批號流水號與倉庫關係，用於更細層級追溯。 |正確 |
| batchno_serialno_group | 取得棧板編號與批號/流水號關係，候選用於佔用板數計算。 | 正確 |
| ship_wh_alias | 取得倉儲別名編號、名稱與類型。 |正確 |
| ship_wh | 取得物流/倉儲交易品項資料，可能支援倉儲容量或倉儲合約關聯。 | 正確 |
| ship_wh_contract | 取得倉儲合約與計價單位，可能支援倉儲容量或倉儲成本分析。 | 正確 |
| warehouse_record | 取得倉儲紀錄，可支援存放天數、倉租或板數使用分析。 | 更正: 此資料表用來記錄倉儲類型為「合約」, 利於後續計算倉租費用; 倉儲類型為「自有」, 並未被記錄。  |
| goods_receipt_note | 候選來源：採購到貨與入庫待處理任務。 | 正確; 統稱「進貨單」 | 
| shipping_order | 候選來源：銷貨出庫待處理任務。 | 正確; 統稱「銷貨單」 | 
| process_order | 候選來源：生產領料、退料、餘料、廢料、產品入庫/出庫任務。 | 正確; 統稱「領退餘廢產」單」 | 
| inventory_order | 候選來源：人工出入庫、移倉或盤點任務。 | 正確; 統稱「銷貨單」 | 
| item_price | 候選來源：若庫存紀錄金額不足，作為單位成本計算來源。 | 正確 | 

### 備註與待確認事項

| 項目 | 建議規則 | 狀態 | 工程師回覆 |
| --- | --- | --- | --- |
| 目前庫存數量 | 以月結統計搭配每日異動補算；明細必要時以 `inventory_record` 入庫數量減出庫數量，依倉儲、料品、批號分組。 | 已確認方向 | 建議採用每月的庫存數量與庫存價值(`inventory_month_statistic` 或 `inventory_item_month_statistic`) 搭配每日庫存異動彙總 `inventory_delta` 進行目前庫存數量計算。 |
| 庫存價值 | 以 `inventory_record.amount` 為主要基準；統計表與 delta 可支援彙總與補算。 | 已確認方向 | 庫存價值以 `inventory_record.amount`。 |
| 料品類別 | 使用 DB 文件與 `EItemCategory`：原料(1)、物料(2)、膠捲(3)、在製品(4)、製成品(5)。 | OK |  |
| 少於三分之一效期 | 使用 `batch_number.validDays` 與 `batch_number.validDate`。 | OK，但需確認物料、膠捲排除規則 | 將物料、膠捲排除 |
| 迴轉週期 | 使用同倉儲同批號最早入庫日計算。 | 基本可行 | |
| 安全水位 | 以目前數量或可用數量低於安全水位判斷。 | 需新增規劃 | 尚未規劃與實作；建議見 `item_safety_stock`。 |
| 預留數量 | 需扣除訂單、工單備料與待處理倉庫任務。 | 需新增規劃 | 尚未規劃與實作；建議見 `warehouse_inventory_reservation`。 |
| 品檢保留量 | 需扣除品保未放行或隔離量。 | 需新增規劃 | 尚未規劃與實作；建議見 `warehouse_quality_hold`。 |
| 佔用板數 | 候選使用棧板異動與棧板狀態計算。 | 需新增規劃 | 尚未規劃與實作；建議見 `warehouse_pallet_movement`。 |
| 倉儲總板位 | 目前 DB 文件未找到明確欄位。 | 需新增規劃 | 尚未規劃與實作；建議見 `warehouse_capacity`。 |
| 今日待處理 | 建議包含今日到期與逾期未完成任務。 | 已確認 | 同意。 |

## GET /api/v2/warehouse/inventory

### API 說明

查詢 Warehouse 頁面的庫存明細列，用於「庫存明細」頁籤、風險 drill-down、批號追溯與明細側欄。

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/warehouse/inventory` | GET | 查詢庫存明細資料 |

### Request Header

| Header | 說明 |
| --- | --- |
| x-auth-token | 存取金鑰。 |

### Query Parameters

| Parameter | Type | Required | 說明 | 工程師回覆 |
| --- | --- | --- | --- | --- |
| date | Integer | NO | 查詢基準時間戳。 | 注意事項: 資料庫的date/time/creationTime欄位記載的是UTC時間; 若資料表中出現timezone欄位, 此時date紀載的是用戶端的日期。記得進行local time 與 utc timestamp的轉換。 |
| timezone | String | NO | 使用者時區。 | |
| warehouse_no | String | NO | 依倉儲別名編號篩選。 | |
| itemCategory | Integer | NO | 依料品品項類別篩選。 | |
| item_no | String | NO | 依料品品項編號篩選。 | |
| batchNo | String | NO | 依批號篩選。 | |
| riskType | String | NO | 依風險類型篩選。 | |
| count | Integer | NO | 分頁筆數。 | |
| start | Integer | NO | 分頁起始位置。 | |

### Request Body

None

### Success Response Data

```json
{
  "code": 0,
  "message": "success",
  "payload": {
    "total": 1,
    "count": 1,
    "results": [
      {
        "inventoryId": "INV-FZ-A03-RM260506-CORN",
        "warehouseNo": "FZ-A03",
        "warehouseName": "原料冷凍庫",
        "itemNo": "RM-CORN-001",
        "itemName": "冷凍玉米粒",
        "itemCategory": 1,
        "itemSubCategory": 0,
        "itemType": 1,
        "batchNo": "RM260506-CORN",
        "serialNo": "",
        "currentQuantity": 180,
        "reservedQuantity": 180,
        "availableQuantity": 0,
        "qualityHoldQuantity": 0,
        "unit": 2,
        "unitCost": 70,
        "inventoryValue": 12600,
        "reservedValue": 12600,
        "availableValue": 0,
        "palletCount": 3,
        "safetyStock": 420,
        "validDays": 90,
        "validDate": 1782547200,
        "firstInboundTimestamp": 1777996800,
        "daysInStock": 36,
        "sourceType": "PURCHASE",
        "sourceNo": "GRN-20260506-018",
        "sourceRefCategory": 1,
        "qualityStatus": "released",
        "riskTypes": [
          "SHELF_LIFE_LT_ONE_THIRD"
        ]
      }
    ]
  }
}
```

### Success Response Field Description

| Field Path | Type | 說明 | Enum / 備註 | 工程師回覆 |
| --- | --- | --- | --- | --- |
| payload.total | Integer | 符合條件的庫存明細總筆數。 |  |  |
| payload.count | Integer | 本次回傳筆數。 |  |  |
| payload.results[].inventoryId | String | 庫存列識別碼，建議由倉儲、料品、批號、流水號組成。 |  |  |
| payload.results[].warehouseNo | String | 倉儲別名編號。 | `ship_wh_alias.no` |  |
| payload.results[].warehouseName | String | 倉儲別名名稱。 |  |  |
| payload.results[].itemNo | String | 料品品項編號。 |  |  |
| payload.results[].itemName | String | 料品品項名稱。 |  |  |
| payload.results[].itemCategory | Integer | 料品品項類別。 | 原料(1)、物料(2)、膠捲(3)、在製品(4)、製成品(5)、貨品(6)、其他(0) |  |
| payload.results[].itemSubCategory | Integer | 料品品項子類別。 | 依 material / inproduct / product / goods 定義 |  |
| payload.results[].itemType | Integer | 料品類型。 | 新料(1)、餘料(2)、廢料(3)、其他(0) |  |
| payload.results[].batchNo | String | 批號。 |  |  |
| payload.results[].serialNo | String | 流水號；批號層級資料可回傳空字串。 |  |  |
| payload.results[].currentQuantity | Float | 目前庫存數量。 | 入庫 - 出庫；可搭配月結統計與每日異動補算 | 建議採用每月的庫存數量與庫存價值(`inventory_month_statistic` 或 `inventory_item_month_statistic`) 搭配每日庫存異動彙總 `inventory_delta` 進行目前庫存數量計算。 |
| payload.results[].reservedQuantity | Float | 預留數量。 | 待確認 | 尚未規劃與實作 |
| payload.results[].availableQuantity | Float | 可用數量。 | 待確認 | 尚未規劃與實作 |
| payload.results[].qualityHoldQuantity | Float | 品檢保留數量。 | 待確認 | 尚未規劃與實作 |
| payload.results[].unit | Integer | 庫存單位。 | Unit 單位定義 | | 
| payload.results[].unitCost | Float | 庫存單位成本。 | 待確認成本來源 |取自 `item_price.costPriceWeight`|
| payload.results[].inventoryValue | Float | 目前庫存價值。 |  | |
| payload.results[].reservedValue | Float | 預留庫存價值。 | 待確認 | 尚未規劃與實作 |
| payload.results[].availableValue | Float | 可用庫存價值。 | 待確認 | 尚未規劃與實作 |
| payload.results[].palletCount | Integer | 佔用板數。 | 待確認 | 尚未規劃與實作 |
| payload.results[].safetyStock | Float | 安全水位。 | 待確認 | 尚未規劃與實作 |
| payload.results[].validDays | Integer | 有效天數。 | `batch_number.validDays` | |
| payload.results[].validDate | Integer | 有效期限。 | `batch_number.validDate` | |
| payload.results[].firstInboundTimestamp | Integer | 同倉儲同批號最早入庫時間。 |  | |
| payload.results[].daysInStock | Integer | 迴轉週期天數。 |  | |
| payload.results[].sourceType | String | 來源單據類型。 | `PURCHASE`、`SALE`、`WORK`、`INVENTORY`、`OTHER` | |
| payload.results[].sourceNo | String | 來源單號。 |  | |
| payload.results[].sourceRefCategory | Integer | 庫存來源類別。 | `EInventoryRefCategory` | |
| payload.results[].qualityStatus | String | 品檢狀態。 | 待確認 | 尚未規劃與實作 |
| payload.results[].riskTypes[] | String | 此庫存列符合的風險類型。 |  | 尚未規劃與實作 |

### Processing Flow

1. 讀取庫存篩選條件與分頁參數。
2. 依倉儲、料品、批號、流水號彙總 `inventory_record`。
3. 以入庫數量減出庫數量計算目前庫存數量。
4. 關聯 `batch_number` 取得有效天數、有效期限、料品資料與來源單據。
5. 關聯 `ship_wh_alias` 取得倉儲別名名稱與類型。
6. 依確認後規則計算預留量、品檢保留量、可用量、庫存價值、佔用板數、安全水位與風險類型。
7. 套用 `riskOnly`、`riskType` 與分頁條件。
8. 回傳前端庫存明細列。

### Database Tables Used

| Table | 用途 |
| --- | --- |
| inventory_record | 取得庫存異動與目前庫存數量。 |
| batch_number | 取得批號、料品、效期與來源資料。 |
| batchno_serialno | 取得批號流水號明細。 |
| batchno_serialno_group | 取得棧板編號與佔用板數候選資料。 |
| ship_wh_alias | 取得倉儲別名資料。 |
| item_price | 候選來源：單位成本。 |

## GET /api/v2/warehouse/tasks

### API 說明

查詢 Warehouse 頁面的「待處理入出庫」任務，用於管理今天尚未完成或已逾期的入庫、出庫、移倉、盤點或確認事項。

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/warehouse/tasks` | GET | 查詢待處理入出庫任務 |

### Request Header

| Header | 說明 |
| --- | --- |
| x-auth-token | 存取金鑰。 |

### Query Parameters

| Parameter | Type | Required | 說明 |
| --- | --- | --- | --- |
| date | Integer | NO | 查詢基準時間戳。 |
| timezone | String | NO | 使用者時區。 |
| taskType | String | NO | 任務類型篩選。 |
| warehouse_no | String | NO | 倉儲別名篩選。 |
| status | String | NO | 任務狀態篩選。 |
| count | Integer | NO | 分頁筆數。 |
| start | Integer | NO | 分頁起始位置。 |

### Request Body

None

### Success Response Data

```json
{
  "code": 0,
  "message": "success",
  "payload": {
    "total": 1,
    "count": 1,
    "results": [
      {
        "taskId": "WH-OUT-WO-20260611-001-RM260506-CORN",
        "taskType": "OUTBOUND",
        "sourceType": "WORK",
        "sourceNo": "WO-20260611-001",
        "sourceSubNo": "",
        "itemNo": "RM-CORN-001",
        "itemName": "冷凍玉米粒",
        "itemCategory": 1,
        "batchNo": "RM260506-CORN",
        "expectedQuantity": 180,
        "processedQuantity": 0,
        "remainingQuantity": 180,
        "unit": 2,
        "palletCount": 3,
        "warehouseNo": "FZ-A03",
        "warehouseName": "原料冷凍庫",
        "dueTimestamp": 1781149200,
        "status": "pending",
        "ownerDepartment": "倉庫部",
        "blockReason": ""
      }
    ]
  }
}
```

### Success Response Field Description

| Field Path | Type | 說明 | Enum / 備註 | 工程師回覆 | 
| --- | --- | --- | --- | --- |
| payload.total | Integer | 符合條件的任務總筆數。 |  |  |
| payload.count | Integer | 本次回傳任務筆數。 |  |  |
| payload.results[].taskId | String | 任務識別碼。 |  |  |
| payload.results[].taskType | String | 任務類型。 | `INBOUND`、`OUTBOUND`、`TRANSFER`、`COUNTING` |  |
| payload.results[].sourceType | String | 來源單據類型。 | `PURCHASE`、`SALE`、`WORK`、`INVENTORY`、`OTHER` |  |
| payload.results[].sourceNo | String | 來源單號。 |  |  |
| payload.results[].sourceSubNo | String | 來源明細編號。 | 無則空字串 |  |
| payload.results[].itemNo | String | 料品品項編號。 |  |  |
| payload.results[].itemName | String | 料品品項名稱。 |  |  |
| payload.results[].itemCategory | Integer | 料品品項類別。 | EItemCategory |  |
| payload.results[].batchNo | String | 批號。 |  |  |
| payload.results[].expectedQuantity | Float | 預期處理數量。 |  |  |
| payload.results[].processedQuantity | Float | 已處理數量。 |  |  |
| payload.results[].remainingQuantity | Float | 尚未處理數量。 | `expectedQuantity - processedQuantity` |  |
| payload.results[].unit | Integer | 任務單位。 | Unit 單位定義 |  |
| payload.results[].palletCount | Integer | 任務板數。 | 待確認 |  |
| payload.results[].warehouseNo | String | 倉儲別名編號。 |  |  |
| payload.results[].warehouseName | String | 倉儲別名名稱。 |  |  |
| payload.results[].dueTimestamp | Integer | 預計處理時間。 |  | 尚未規劃與實作 |
| payload.results[].status | String | 任務處理狀態。 | `pending`、`partial`、`done`、`blocked` | 尚未規劃與實作 |
| payload.results[].ownerDepartment | String | 下一步負責部門。 |  | 尚未規劃與實作 |
| payload.results[].blockReason | String | 阻塞原因，例如品檢未放行或倉儲未指定。 |  |尚未規劃與實作 |

### Processing Flow

1. 依 `date` 與 `timezone` 取得查詢營業日起訖時間。
2. 蒐集會產生倉庫作業的來源單據：
   - 採購入庫：`goods_receipt_note`。
   - 銷售出庫：`shipping_order`。
   - 生產領料、退料、餘料、廢料、產品入庫/出庫：`process_order`。
   - 人工出入庫、移倉、盤點：`inventory_order`。
3. 依來源單號、料品、批號與倉儲，比對 `inventory_record` 已處理數量。
4. 計算預期數量、已處理數量與尚未處理數量。
5. 產生任務狀態：
   - `pending`：尚未處理。
   - `partial`：已部分處理。
   - `done`：已完成。
   - `blocked`：因品檢、倉儲指派或資料不足而無法處理。
6. 依任務類型與阻塞原因判斷下一步負責部門。
7. 回傳待處理任務清單。

### Database Tables Used

| Table | 用途 |
| --- | --- |
| goods_receipt_note | 取得採購到貨入庫來源。 |
| shipping_order | 取得銷售出庫來源。 |
| process_order | 取得生產領料、退料、餘料、廢料、產品入庫/出庫來源。 |
| inventory_order | 取得人工出入庫、移倉或盤點來源。 |
| inventory_record | 取得已處理入庫/出庫數量。 |
| batch_number | 取得批號與效期資料。 |
| ship_wh_alias | 取得倉儲別名資料。 |

## 工程師 Review Checklist

| 問題 | 影響 | 狀態 | 工程師回覆 | 
| --- | --- | --- | --- |
| 倉庫經營總覽是否建立新的 `/api/v2/warehouse/*` route，或擴充現有 `/api/v1/inventory/*`、`/api/v1/shipwarehouse/*`？ | 影響 API group 與 route ownership。 | 已確認 | 建立新的 route，並將版本升級為 v2 `/api/v2/warehouse/*`。 |
| 庫存價值以 `inventory_record.amount`、統計表，還是 `item_price` 重新計算為準？ | 影響財務數字一致性。 | 已確認 | 庫存價值以 `inventory_record.amount`。 |
| 預留數量的正式來源是訂單、工單、倉庫任務中的哪些資料？ | 影響可用庫存。 | 需新增規劃 | 尚未規劃與實作；建議新增 `warehouse_inventory_reservation`。 |
| 安全水位來源 table/field 是哪一個？ | 影響低於安全水位警示。 | 需新增規劃 | 尚未規劃與實作；建議新增 `item_safety_stock`。 |
| 品檢放行/保留狀態來源是哪些 table/field？ | 影響可用量與品檢保留量。 | 需新增規劃 | 尚未規劃與實作；建議新增 `warehouse_quality_hold`。 |
| 倉儲總板位來源是哪些 table/field？ | 影響容量與可用板位。 | 需新增規劃 | 尚未規劃與實作；建議新增 `warehouse_capacity`。 |
| `batchno_serialno_group.group` 是否可作為佔用板數計算依據？ | 影響板數統計。 | 需新增規劃 | 目前只規劃棧板與批號對應關係，出入庫紀錄與棧板對應關係尚未規劃與實作；建議新增 `warehouse_pallet_movement`。 |
| 物料、膠捲是否排除於少於三分之一效期警示？ | 使用者已提出排除方向，需後端規則確認。 | 已確認 | 物料、膠捲排除。 |
| Dashboard 是否預設包含庫存明細列？ | 影響 response size 與前端 mapper。 | 已確認 | 預設不包含庫存明細列。 |
| 今日待處理是否包含逾期未完成任務？ | 影響管理者看到的風險與任務數量。 | 已確認 | 包含。 |

## 前端對應

目前前端 Warehouse 頁面使用下列資料群組：

```txt
kpis
categorySummaries
capacities
records
risks
tasks
```

建議後端資料集與前端 mapper 對應如下：

| 前端資料群組 | API 資料集 |
| --- | --- |
| `kpis` | `payload.summary` |
| `categorySummaries` | `payload.inventoryValueByCategory` |
| `capacities` | `payload.capacityByWarehouse` |
| `records` | `payload.inventory` 或 `GET /api/v2/warehouse/inventory` |
| `risks` | `payload.riskAlerts` |
| `tasks` | `payload.pendingTasks` 或 `GET /api/v2/warehouse/tasks` |

前端應將轉換邏輯集中在 `src/services/warehouse-api.ts`，避免頁面元件直接綁定後端欄位名稱。
