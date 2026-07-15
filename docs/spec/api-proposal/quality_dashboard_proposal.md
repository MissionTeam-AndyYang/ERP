# Quality Dashboard API 提案

> Status: Proposal / Pending Engineer Review  
> Screen: `QualityWorkspaceScreen`  
> Route: `/quality`  
> Scope: V1 Core、read-only

## 1. 畫面定位

`QualityWorkspaceScreen` 提供品保主管與管理者檢視目前品質風險、待處理品檢任務，以及已被品檢保留的料品／批號。第一版優先回答：

1. 今天或查詢期間有多少品檢任務待處理、逾期或阻塞？
2. 哪些批號因品檢保留而不能投入、生產或出貨？
3. 品檢保留數量與價值分布在哪些料品類別與倉庫？
4. 選取一筆品檢保留或任務後，應由哪個部門處理、來源單據是什麼、目前卡在哪裡？

第一版只提供查詢與 drill-down，不執行放行、判定、建立品檢單、修改保留量或重新安排生產等動作。

## 2. API 清單

| API | Method | 用途 | Status |
|---|---|---|---|
| `/api/v2/quality/dashboard` | GET | 回傳品質 KPI、待處理任務、品檢保留摘要與風險清單 | Proposal / Pending Engineer Review |
| `/api/v2/quality/holds/{hold_no}/detail` | GET | 回傳單一品檢保留紀錄、批號庫存摘要、來源單據與關聯任務 | Proposal / Pending Engineer Review |

## 3. GET /api/v2/quality/dashboard

### 3.1 Query Parameters

| Parameter | Type | Required | 說明 |
|---|---|---:|---|
| `date` | Integer | No | 查詢基準時間，UTC timestamp；未提供時由後端使用目前時間。 |
| `timezone` | String | No | 日期分組時區，例如 `Asia/Taipei`。 |
| `dateRange` | String | No | `today`、`7d`、`14d`，預設 `today`。 |
| `warehouseNo` | String | No | 限定倉儲別名 no。 |
| `itemCategory` | Integer | No | 限定料品類別；enum 顯示文字由前端轉換。 |
| `taskType` | Integer | No | 限定 workflow 品檢任務類型，預設為 8。 |
| `status` | String | No | `pending`、`in_progress`、`blocked`、`overdue`、`hold`。 |
| `riskOnly` | Boolean | No | 只回傳有風險的任務或品檢保留資料。 |
| `keyword` | String | No | 以任務單號、品檢單號、料號、批號或品名查詢。 |
| `start` | Integer | No | `qualityTasks[]` 分頁起點，預設 0。 |
| `count` | Integer | No | `qualityTasks[]` 回傳筆數，預設 50，最大 100。 |

### 3.2 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "timezone": "String",
  "range": {
    "startTimestamp": "Integer",
    "endTimestamp": "Integer",
    "dateRange": "String"
  },
  "summary": {
    "pendingTaskCount": "Integer",
    "overdueTaskCount": "Integer",
    "blockedTaskCount": "Integer",
    "activeHoldCount": "Integer",
    "activeHoldQuantity": "Float",
    "activeHoldValue": "Integer",
    "affectedItemCount": "Integer",
    "affectedWarehouseCount": "Integer"
  },
  "holdByCategory": [
    {
      "itemCategory": "Integer",
      "holdCount": "Integer",
      "holdQuantity": "Float",
      "holdValue": "Integer"
    }
  ],
  "holdByWarehouse": [
    {
      "warehouseNo": "String",
      "holdCount": "Integer",
      "holdQuantity": "Float",
      "holdValue": "Integer"
    }
  ],
  "qualityTasks": [
    {
      "taskId": "String",
      "taskNo": "String",
      "taskType": "Integer",
      "status": "String",
      "riskLevel": "Integer",
      "ownerDepartment": "Integer",
      "sourceType": "Integer",
      "sourceNo": "String",
      "inspectionNo": "String",
      "itemNo": "String",
      "itemName": "String",
      "batchNo": "String",
      "warehouseNo": "String",
      "quantity": "Float",
      "value": "Integer",
      "plannedTimestamp": "Integer",
      "completedTimestamp": "Integer",
      "comment": "String"
    }
  ],
  "riskAlerts": [
    {
      "alertType": "String",
      "riskLevel": "Integer",
      "taskId": "String",
      "holdNo": "String",
      "itemNo": "String",
      "batchNo": "String",
      "warehouseNo": "String",
      "quantity": "Float",
      "value": "Integer",
      "ownerDepartment": "Integer"
    }
  ],
  "total": "Integer",
  "start": "Integer",
  "count": "Integer"
}
```

### 3.3 欄位規則

| 欄位 | 說明 |
|---|---|
| `summary.activeHold*` | 只計算 `warehouse_quality_hold.status = 1` 且 `date <= 查詢基準時間` 的資料；數量取 `holdQuantity` 加總，價值取 `holdValue` 加總。 |
| `holdByCategory` | 依 `warehouse_quality_hold.item_no` 對應料品主檔的料品類別分組；若料品主檔無法對應，該列須標示資料缺漏，不得自行推測類別。 |
| `holdByWarehouse` | 依 `warehouse_quality_hold.warehouse_no` 分組；顯示名稱由前端使用 warehouse enum／主檔轉換。 |
| `qualityTasks` | 以 `workflow_task_state.taskType = 8` 為主要來源，並依查詢條件判斷狀態、日期、負責部門與來源單據。 |
| `riskAlerts` | 由逾期、阻塞、有效品檢保留及保留數量大於 0 的資料組成；不回傳前端顯示用 message 或 recommendedAction。 |
| Enum 欄位 | `taskType`、`status`、`ownerDepartment`、`sourceType`、`itemCategory` 僅回傳 code，由前端負責多國語系轉換。 |
| 數字精度 | 數量／重量小數點 2 位；金額四捨五入至整數。 |

## 4. GET /api/v2/quality/holds/{hold_no}/detail

### 4.1 Success Response Data

```json
{
  "hold": {
    "holdNo": "String",
    "inspectionNo": "String",
    "status": "Integer",
    "itemNo": "String",
    "itemName": "String",
    "itemCategory": "Integer",
    "batchNo": "String",
    "warehouseNo": "String",
    "holdQuantity": "Float",
    "holdValue": "Integer",
    "dateTimestamp": "Integer",
    "sourceType": "Integer",
    "sourceNo": "String",
    "comment": "String"
  },
  "inventory": {
    "quantity": "Float",
    "inventoryValue": "Integer",
    "availableQuantity": "Float",
    "availableValue": "Integer",
    "qualityHoldQuantity": "Float",
    "qualityHoldValue": "Integer"
  },
  "tasks": [],
  "timeline": [],
  "relatedDocuments": []
}
```

`tasks[]`、`timeline[]` 與 `relatedDocuments[]` 的實際欄位須待工程師確認 `workflow_task_state`、`workflow_task_event` 及品檢保留來源單據的關聯方式後定稿；在確認前不得假設存在 inspection header、inspection result 或 defect table。

## 5. 前端責任

1. 將 enum code 轉換為繁體中文、英文及其他語系字串。
2. 依 `riskAlerts[].alertType` 選擇顏色、圖示與篩選狀態，不由後端產生 UI message。
3. 依目前的 `warehouseNo`、`itemCategory`、`status` 組合導向 query string。
4. API 空資料、部分資料與錯誤狀態均須保留可辨識的空狀態，不以 mock 資料冒充正式結果。

## 6. 工程師需確認

| 項目 | 目前提案 | 需確認內容 |
|---|---|---|
| 品檢任務來源 | `workflow_task_state.taskType = 8` | `sourceType`、`sourceNo` 是否可直接追到 `goods_receipt_note`、`production_data` 或其他來源單據。 |
| 品檢保留資料 | `warehouse_quality_hold` | `status = 1` 是否代表有效保留；釋放、部分釋放與取消是否另有 event 或 status 定義。 |
| 品檢單資料 | 目前不新增或假設 inspection table | 是否已有工程師尚未納入 schema 的品檢主檔／結果表；若有，請提供正式 table 與欄位。 |
| `holdValue` | 直接使用資料表值 | 若為 NULL，是否應回傳 0，或需依庫存單價補算。 |
| 明細不存在 | 建議回傳標準 not found error | 是否沿用既有 API 的錯誤 code 與 HTTP status。 |
| 任務與保留關聯 | 以來源單據與 item/batch/warehouse 交集關聯 | 是否存在明確 task-to-hold reference，若存在應優先使用。 |

## 7. 範例資料

```json
{
  "serverTimestamp": 1784073600,
  "timezone": "Asia/Taipei",
  "range": {"startTimestamp": 1783987200, "endTimestamp": 1784073599, "dateRange": "today"},
  "summary": {
    "pendingTaskCount": 8,
    "overdueTaskCount": 2,
    "blockedTaskCount": 1,
    "activeHoldCount": 5,
    "activeHoldQuantity": 1260.50,
    "activeHoldValue": 248000,
    "affectedItemCount": 4,
    "affectedWarehouseCount": 2
  },
  "holdByCategory": [
    {"itemCategory": 1, "holdCount": 3, "holdQuantity": 840.00, "holdValue": 172000},
    {"itemCategory": 5, "holdCount": 2, "holdQuantity": 420.50, "holdValue": 76000}
  ],
  "holdByWarehouse": [
    {"warehouseNo": "WH-RM", "holdCount": 3, "holdQuantity": 840.00, "holdValue": 172000},
    {"warehouseNo": "WH-FG", "holdCount": 2, "holdQuantity": 420.50, "holdValue": 76000}
  ],
  "qualityTasks": [
    {
      "taskId": "TASK-20260715-001",
      "taskNo": "WT-20260715-001",
      "taskType": 8,
      "status": "blocked",
      "riskLevel": 3,
      "ownerDepartment": 8,
      "sourceType": 1,
      "sourceNo": "GRN-20260715-003",
      "inspectionNo": "INS-20260715-003",
      "itemNo": "RM-00031",
      "itemName": "原料示例",
      "batchNo": "B20260715003",
      "warehouseNo": "WH-RM",
      "quantity": 840.00,
      "value": 172000,
      "plannedTimestamp": 1784066400,
      "completedTimestamp": 0,
      "comment": "等待品保判定"
    }
  ],
  "riskAlerts": [
    {
      "alertType": "quality_hold",
      "riskLevel": 3,
      "taskId": "TASK-20260715-001",
      "holdNo": "QH-20260715-001",
      "itemNo": "RM-00031",
      "batchNo": "B20260715003",
      "warehouseNo": "WH-RM",
      "quantity": 840.00,
      "value": 172000,
      "ownerDepartment": 8
    }
  ],
  "total": 8,
  "start": 0,
  "count": 1
}
```

## 8. 非本次範圍

- 不設計 `POST /quality/inspections`、`PUT /quality/holds` 或任何放行／判退 mutation API。
- 不新增 Quality DB Schema；若工程師確認現有 schema 無法支援，另開 DB extension proposal，再由工程師 review。
- 不在本版推導抽樣標準、檢驗項目、缺失分類、檢驗數值與合格率，因目前正式 schema 尚未提供可核對來源。
