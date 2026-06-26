# Warehouse Task Workbench API Proposal

> Status: Proposal / Pending Engineer Review
> Target UI Preview: `docs/spec/api-proposal/warehouse_task_workbench_static_preview.html`
> Flow / Algorithm: `docs/spec/api-proposal/warehouse_task_workbench_flow_algorithm.md`
> DB Extension Proposal: `docs/spec/api-proposal/warehouse_task_workbench_db_extension_proposal.md`
> Purpose: 承接 Warehouse Dashboard 的待處理任務摘要與 Inventory Lot Detail 的批號追蹤資料，提供「倉庫任務工作台」第一版 read-only API 設計，讓管理者與倉庫主管確認今日入庫、出庫、移倉、品檢與出貨待辦是否可如期處理。

## 工程師提問

| 工程師提問 | 工程師回覆 | 提案文件更新 |
| --- | --- | --- |
| 針對 `/api/v2/warehouse/task-workbench/tasks/{taskId}`，請詳細說明 `payload.task.sourceNo` 欄位與 `payload.sourceRefs[]` 欄位的定義與用途。 | 採用並重新定義。`payload.task.refNo/refSubNo/refCategory` 是此 workflow task 的「主任務來源單據」，直接對應 `workflow_task_state.ref_no/ref_sub_no/refCategory`，用於任務標題、主要來源追溯與前端快速顯示。`payload.sourceRefs[]` 是 detail panel 的「關聯來源集合」，第一版至少包含主任務來源；後續可依 `workflow_task_event` 擴充同一任務流程中出現過的進貨單、入庫單、出庫單、品檢單、移倉單、出貨單等關聯來源。 | Detail API 的 JSON、Field Description 與 Processing Flow 已補充兩者用途差異。 |
| `payload.task.sourceNo` 更名為 `payload.task.refNo`。 | 採用。與 `workflow_task_state.ref_no`、既有資料庫命名規則及其他 Warehouse proposal 的 `refNo` 命名一致。 | Detail API `payload.task.sourceNo` 已更名為 `payload.task.refNo`。 |
| `payload.task.sourceSubNo` 更名為 `payload.task.refSubNo`。 | 採用。與 `workflow_task_state.ref_sub_no` 命名一致。 | Detail API `payload.task.sourceSubNo` 已更名為 `payload.task.refSubNo`。 |
| 需要完整的流程歷史，請進行資料表的規劃與設計；完成後，資料表提案文件也請統一集中放置於 `api-proposal`。 | 採用。第一版 Task Workbench 仍維持 read-only，但 timeline 不再只依目前狀態推導；新增 `workflow_task_event` 資料表提案，用於保存任務流程事件、狀態變化、責任部門移轉、關聯來源與數量變化。 | 新增 `docs/spec/api-proposal/warehouse_task_workbench_db_extension_proposal.md`，並更新 `timeline[]` 與 `sourceRefs[]` 的資料來源說明。 |

## Screen Intent

`WarehouseTaskWorkbenchScreen` 回答以下問題：

1. 今天與近期有哪些倉庫任務尚未處理？
2. 任務卡在哪個流程、由哪個部門負責下一步？
3. 任務所需或涉及的批號庫存是否足夠、是否被預留或品檢保留？
4. 進貨、入庫、出庫、移倉、品檢、出貨任務是否有逾期或阻塞風險？

第一版僅設計 read-only API，不設計完成任務、指派、放行、出庫確認等 mutation。待工程師確認資料表流程與部門權責後，再另行設計 mutation API。

## API Summary

| URL | Method | Description | Status | Review Note |
| --- | --- | --- | --- | --- |
| `/api/v2/warehouse/task-workbench` | GET | 查詢倉庫任務工作台清單與看板摘要 | Proposal / Pending Engineer Review | 供任務 kanban/list、篩選、排序、分頁與 Dashboard drill-down 使用。 |
| `/api/v2/warehouse/task-workbench/tasks/{taskId}` | GET | 查詢單一倉庫任務追蹤明細 | Proposal / Pending Engineer Review | 供右側任務 detail panel 顯示來源單據、相關批號、庫存可用性、阻塞原因與任務時間線。 |

## Numeric Format Rules

| Numeric Meaning | Format |
| --- | --- |
| 單價 | 四捨五入取至小數點第 4 位 |
| 重量或數量 | 四捨五入取至小數點第 2 位 |
| 金額 | 四捨五入取整數 |

## GET /api/v2/warehouse/task-workbench

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/warehouse/task-workbench` | GET | 查詢倉庫任務工作台清單與看板摘要 |

### Request Header

| Header | Description |
| --- | --- |
| `x-auth-token` | 存取金鑰 |
| `x-timezone` | 前端顯示時區；未提供時以 UTC 回傳 |

### Query Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `date` | Integer | NO | 查詢基準時間，UTC timestamp；未提供時以伺服器目前時間計算 |
| `dateRange` | String | NO | 任務日期範圍；允許值：`today`、`next_7_days`、`overdue`、`all_open`；預設 `today` |
| `warehouse_no` | String | NO | 倉儲別名 no |
| `taskType` | Integer | NO | 任務類型；請購(1)、採購(2)、進貨(3)、入庫(4)、出庫(5)、移倉(6)、生產(7)、品檢(8)、出貨(9) |
| `status` | String/Integer | NO | 任務狀態；支援 `pending`、`partial`、`blocked`、`done`、`cancelled` 或狀態代碼 |
| `ownerDepartment` | Integer | NO | 下一步負責部門 |
| `riskOnly` | Boolean/String | NO | 是否僅回傳有逾期、阻塞、庫存不足或品檢保留風險的任務 |
| `keyword` | String | NO | 模糊搜尋：任務 ID、來源單號、料號、品名、批號、倉儲名稱 |
| `sort` | String | NO | 排序欄位；允許值：`dueTimestamp`、`taskType`、`remainingQuantity`、`riskLevel` |
| `order` | String | NO | 排序方向；允許值：`asc`、`desc` |
| `start` | Integer | NO | 分頁起始位置 |
| `count` | Integer | NO | 分頁筆數；預設 50 |

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
      "mode": "String",
      "startTimestamp": "Integer",
      "endTimestamp": "Integer"
    },
    "summary": {
      "openTaskCount": "Integer",
      "overdueTaskCount": "Integer",
      "blockedTaskCount": "Integer",
      "inboundTaskCount": "Integer",
      "outboundTaskCount": "Integer",
      "qualityTaskCount": "Integer",
      "shipmentTaskCount": "Integer",
      "inventoryShortageTaskCount": "Integer"
    },
    "lanes": [
      {
        "laneCode": "String",
        "taskCount": "Integer",
        "riskCount": "Integer"
      }
    ],
    "total": "Integer",
    "count": "Integer",
    "start": "Integer",
    "results": [
      {
        "taskId": "String",
        "taskType": "Integer",
        "taskStatus": "Integer",
        "refCategory": "Integer",
        "refNo": "String",
        "refSubNo": "String",
        "itemCategory": "Integer",
        "itemNo": "String",
        "itemName": "String",
        "batchNo": "String",
        "unit": "Integer",
        "expectedQuantity": "Float",
        "processedQuantity": "Float",
        "remainingQuantity": "Float",
        "warehouseNo": "String",
        "warehouseName": "String",
        "dueTimestamp": "Integer",
        "ownerDepartment": "Integer",
        "riskLevel": "Integer",
        "riskTypes": ["String"],
        "blockReasonCode": "String",
        "blockReason": "String",
        "availableQuantity": "Float",
        "reservedQuantity": "Float",
        "qualityHoldQuantity": "Float",
        "inventoryValue": "Integer",
        "nextActionCode": "String"
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| `payload.serverTimestamp` | Integer | 後端產生資料的 UTC timestamp |  |
| `payload.timezone` | String | 本次查詢使用的時區；來源為 `x-timezone`，未提供時為 UTC |  |
| `payload.range.mode` | String | 查詢日期範圍模式 | `today`、`next_7_days`、`overdue`、`all_open` |
| `payload.range.startTimestamp` | Integer | 查詢範圍起始 UTC timestamp |  |
| `payload.range.endTimestamp` | Integer | 查詢範圍結束 UTC timestamp |  |
| `payload.summary.openTaskCount` | Integer | 篩選條件下未完成任務數 |  |
| `payload.summary.overdueTaskCount` | Integer | 已逾期且未完成任務數 |  |
| `payload.summary.blockedTaskCount` | Integer | 狀態為阻塞的任務數 | EWorkflowTaskStatus |
| `payload.summary.inboundTaskCount` | Integer | 任務類型為進貨(3)或入庫(4)的任務數 | EWorkflowTaskType |
| `payload.summary.outboundTaskCount` | Integer | 任務類型為出庫(5)的任務數 | EWorkflowTaskType |
| `payload.summary.qualityTaskCount` | Integer | 任務類型為品檢(8)的任務數 | EWorkflowTaskType |
| `payload.summary.shipmentTaskCount` | Integer | 任務類型為出貨(9)的任務數 | EWorkflowTaskType |
| `payload.summary.inventoryShortageTaskCount` | Integer | 需要出庫、出貨或生產領料但可用庫存不足的任務數 |  |
| `payload.lanes[].laneCode` | String | 看板 lane 代碼；前端負責轉換顯示文字 | `inbound`、`outbound`、`quality`、`shipment`、`blocked` |
| `payload.lanes[].taskCount` | Integer | 該 lane 任務數 |  |
| `payload.lanes[].riskCount` | Integer | 該 lane 命中任一風險的任務數 |  |
| `payload.total` | Integer | 符合篩選條件且分頁前的總筆數 |  |
| `payload.count` | Integer | 本次回傳筆數 |  |
| `payload.start` | Integer | 本次分頁起始位置 |  |
| `payload.results[].taskId` | String | workflow 任務識別碼；來源為 `workflow_task_state.taskId` |  |
| `payload.results[].taskType` | Integer | 任務類型；前端負責轉換顯示文字 | EWorkflowTaskType |
| `payload.results[].taskStatus` | Integer | 任務狀態；前端負責轉換顯示文字 | EWorkflowTaskStatus |
| `payload.results[].refCategory` | Integer | 來源單據類別；來源為 `workflow_task_state.refCategory` |  |
| `payload.results[].refNo` | String | 來源單號；來源為 `workflow_task_state.ref_no` |  |
| `payload.results[].refSubNo` | String | 來源明細編號；來源為 `workflow_task_state.ref_sub_no` |  |
| `payload.results[].itemCategory` | Integer | 料品品項類別；前端負責轉換顯示文字 | EItemCategory |
| `payload.results[].itemNo` | String | 料品品項編號 |  |
| `payload.results[].itemName` | String | 料品品項名稱 |  |
| `payload.results[].batchNo` | String | 批號；若任務尚未指定批號可回傳空字串 |  |
| `payload.results[].unit` | Integer | 數量單位；前端負責轉換顯示文字 | Unit |
| `payload.results[].expectedQuantity` | Float | 任務預計處理數量 |  |
| `payload.results[].processedQuantity` | Float | 任務已處理數量 |  |
| `payload.results[].remainingQuantity` | Float | 任務剩餘待處理數量，計算方式為 `max(expectedQuantity - processedQuantity, 0)` |  |
| `payload.results[].warehouseNo` | String | 任務對應倉儲別名 no |  |
| `payload.results[].warehouseName` | String | 倉儲別名名稱；來源為 `ship_wh_alias.name` |  |
| `payload.results[].dueTimestamp` | Integer | 任務預計完成時間，UTC timestamp |  |
| `payload.results[].ownerDepartment` | Integer | 下一步負責部門；前端負責轉換顯示文字 | EDepartment |
| `payload.results[].riskLevel` | Integer | 任務風險等級；前端負責轉換顯示文字與樣式 | EWarehouseRiskLevel |
| `payload.results[].riskTypes[]` | String | 任務命中的風險類型 | `OVERDUE`、`BLOCKED`、`INVENTORY_SHORTAGE`、`QUALITY_HOLD`、`BATCH_NOT_ASSIGNED` |
| `payload.results[].blockReasonCode` | String | 阻塞原因代碼；來源為 `workflow_task_state.blockReasonCode` |  |
| `payload.results[].blockReason` | String | 阻塞原因或主管人工判斷備註；來源為 `workflow_task_state.blockReason` |  |
| `payload.results[].availableQuantity` | Float | 該任務對應批號或料品的可用數量；未能穩定對應時回傳 0 |  |
| `payload.results[].reservedQuantity` | Float | 該任務對應批號或料品的預留數量；未能穩定對應時回傳 0 |  |
| `payload.results[].qualityHoldQuantity` | Float | 該任務對應批號或料品的品檢保留數量；未能穩定對應時回傳 0 |  |
| `payload.results[].inventoryValue` | Integer | 該任務對應批號或料品的庫存價值；未能穩定對應時回傳 0 |  |
| `payload.results[].nextActionCode` | String | 下一步動作代碼；前端依 code 與 taskType 顯示操作提示，不代表此 API 可執行 mutation |  |

### Processing Flow

1. 讀取查詢條件與 `x-timezone`，建立查詢日期範圍。
2. 查詢 `workflow_task_state`，依任務狀態、任務類型、負責部門、倉儲、日期範圍與關鍵字過濾。
3. 讀取 `ship_wh_alias` 補齊倉儲名稱。
4. 對每筆任務嘗試以 `warehouse_no + item_no + batchNumber` 對應目前庫存快照；若批號未指定，僅能以 `warehouse_no + item_no` 彙總可用性。
5. 計算 `remainingQuantity`、庫存不足、逾期、阻塞、品檢保留與未指定批號等風險。
6. 依 taskType 與 riskTypes 決定 laneCode、riskLevel 與 nextActionCode。
7. 套用排序、分頁，回傳 summary、lanes 與 results。

### Database Tables Used

| Table | Purpose |
| --- | --- |
| `workflow_task_state` | 提供任務狀態、來源單號、料品、批號、數量、負責部門與阻塞原因 |
| `inventory_item_month_statistic` | 提供批號層級月結庫存量與庫存價值，作為目前庫存快照主計算基準 |
| `inventory_delta` | 提供月結日後每日入庫/出庫數量與金額異動，補算至查詢營業日 |
| `inventory_record` | 在統計資料缺漏或日期覆蓋不足時作為防護性補算依據 |
| `warehouse_inventory_reservation` | 提供預留數量與預留價值 |
| `warehouse_quality_hold` | 提供品檢保留量與品檢保留價值 |
| `ship_wh_alias` | 提供倉儲別名名稱 |

## GET /api/v2/warehouse/task-workbench/tasks/{taskId}

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/warehouse/task-workbench/tasks/{taskId}` | GET | 查詢單一倉庫任務追蹤明細 |

### Request Header

| Header | Description |
| --- | --- |
| `x-auth-token` | 存取金鑰 |
| `x-timezone` | 前端顯示時區；未提供時以 UTC 回傳 |

### Path Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `taskId` | String | YES | workflow 任務識別碼 |

### Query Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `date` | Integer | NO | 查詢基準時間，UTC timestamp；未提供時以伺服器目前時間計算 |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "task": {
      "taskId": "String",
      "taskType": "Integer",
      "taskStatus": "Integer",
      "refCategory": "Integer",
      "refNo": "String",
      "refSubNo": "String",
      "ownerDepartment": "Integer",
      "warehouseNo": "String",
      "warehouseName": "String",
      "dueTimestamp": "Integer",
      "blockReasonCode": "String",
      "blockReason": "String",
      "riskLevel": "Integer",
      "riskTypes": ["String"],
      "nextActionCode": "String"
    },
    "quantity": {
      "itemCategory": "Integer",
      "itemNo": "String",
      "itemName": "String",
      "batchNo": "String",
      "unit": "Integer",
      "expectedQuantity": "Float",
      "processedQuantity": "Float",
      "remainingQuantity": "Float",
      "availableQuantity": "Float",
      "reservedQuantity": "Float",
      "qualityHoldQuantity": "Float"
    },
    "relatedLots": [
      {
        "lotKey": "String",
        "warehouseNo": "String",
        "itemNo": "String",
        "itemName": "String",
        "batchNo": "String",
        "currentQuantity": "Float",
        "availableQuantity": "Float",
        "qualityHoldQuantity": "Float",
        "validDate": "Integer",
        "riskTypes": ["String"]
      }
    ],
    "sourceRefs": [
      {
        "refCategory": "Integer",
        "refNo": "String",
        "refSubNo": "String",
        "descriptionCode": "String"
      }
    ],
    "timeline": [
      {
        "eventCode": "String",
        "eventTimestamp": "Integer",
        "department": "Integer",
        "status": "Integer",
        "note": "String"
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| `payload.task.taskId` | String | workflow 任務識別碼 |  |
| `payload.task.taskType` | Integer | 任務類型；前端負責轉換顯示文字 | EWorkflowTaskType |
| `payload.task.taskStatus` | Integer | 任務狀態；前端負責轉換顯示文字 | EWorkflowTaskStatus |
| `payload.task.refCategory` | Integer | 來源類別；來源為 `workflow_task_state.refCategory` |  |
| `payload.task.refNo` | String | 主任務來源單號；來源為 `workflow_task_state.ref_no`，用於任務標題、主要來源追溯與前端快速顯示 |  |
| `payload.task.refSubNo` | String | 主任務來源明細編號；來源為 `workflow_task_state.ref_sub_no` |  |
| `payload.task.ownerDepartment` | Integer | 下一步負責部門；前端負責轉換顯示文字 | EDepartment |
| `payload.task.warehouseNo` | String | 任務對應倉儲別名 no |  |
| `payload.task.warehouseName` | String | 倉儲別名名稱 |  |
| `payload.task.dueTimestamp` | Integer | 任務預計完成時間，UTC timestamp |  |
| `payload.task.blockReasonCode` | String | 阻塞原因代碼 |  |
| `payload.task.blockReason` | String | 阻塞原因或主管人工判斷備註 |  |
| `payload.task.riskLevel` | Integer | 任務風險等級 | EWarehouseRiskLevel |
| `payload.task.riskTypes[]` | String | 任務命中的風險類型 |  |
| `payload.task.nextActionCode` | String | 下一步動作代碼；前端顯示提示用，不代表可執行 mutation |  |
| `payload.quantity.itemCategory` | Integer | 料品品項類別 | EItemCategory |
| `payload.quantity.itemNo` | String | 料品品項編號 |  |
| `payload.quantity.itemName` | String | 料品品項名稱 |  |
| `payload.quantity.batchNo` | String | 批號；任務未指定批號時回傳空字串 |  |
| `payload.quantity.unit` | Integer | 數量單位 | Unit |
| `payload.quantity.expectedQuantity` | Float | 任務預計處理數量 |  |
| `payload.quantity.processedQuantity` | Float | 任務已處理數量 |  |
| `payload.quantity.remainingQuantity` | Float | 任務剩餘待處理數量 |  |
| `payload.quantity.availableQuantity` | Float | 對應批號或料品可用數量 |  |
| `payload.quantity.reservedQuantity` | Float | 對應批號或料品預留數量 |  |
| `payload.quantity.qualityHoldQuantity` | Float | 對應批號或料品品檢保留數量 |  |
| `payload.relatedLots[]` | Array | 任務可對應的批號庫存列；若任務已有 batchNo，通常只回傳同批號庫存列 |  |
| `payload.sourceRefs[]` | Array | 任務關聯來源集合；第一版至少包含 `payload.task.refCategory/refNo/refSubNo` 對應的主任務來源，後續可由 `workflow_task_event` 補充流程中出現的其他關聯單據 |  |
| `payload.timeline[]` | Array | 任務流程時間線；資料來源建議為新增的 `workflow_task_event`，若尚未導入事件資料則可暫回傳空陣列 |  |

### Processing Flow

1. 以 `taskId` 查詢 `workflow_task_state`。
2. 補齊倉儲名稱與任務數量欄位。
3. 依任務的 `warehouse_no + item_no + batchNumber` 查詢目前庫存快照；若 `batchNumber` 為空，回傳該倉儲同料品可用批號清單。
4. 計算任務風險與下一步動作代碼。
5. 組成 sourceRefs 與 timeline；`payload.task.refNo/refSubNo/refCategory` 表示主任務來源，`sourceRefs[]` 表示關聯來源集合，timeline 建議由新增的 `workflow_task_event` 提供完整流程歷史。

### Database Tables Used

| Table | Purpose |
| --- | --- |
| `workflow_task_state` | 單一任務主資料、來源欄位、狀態、數量與阻塞原因 |
| `workflow_task_event` | 提供任務流程事件、狀態變化、責任部門移轉、關聯來源與完整時間線；資料表設計見 `warehouse_task_workbench_db_extension_proposal.md` |
| `inventory_item_month_statistic` | 目前庫存快照主計算基準 |
| `inventory_delta` | 庫存快照補算 |
| `inventory_record` | 庫存快照防護性補算與批號參考 |
| `warehouse_inventory_reservation` | 預留數量與價值 |
| `warehouse_quality_hold` | 品檢保留量與價值 |
| `batch_number` | 批號效期與批號來源資料 |
| `ship_wh_alias` | 倉儲別名名稱 |

## Frontend Interaction Notes

| UI Action | API Usage |
| --- | --- |
| 從 Dashboard 點選今日待處理入庫 | 呼叫 `GET /api/v2/warehouse/task-workbench?dateRange=today&taskType=4` |
| 從 Dashboard 點選今日待處理出庫 | 呼叫 `GET /api/v2/warehouse/task-workbench?dateRange=today&taskType=5` |
| 使用者切換看板 lane | 使用 `taskType`、`status` 或 `riskOnly` 重新查詢 list API |
| 使用者點選任務列 | 呼叫 detail API 顯示右側任務追蹤面板 |
| 使用者切換語系 | 前端依 enum code 與 nextActionCode 轉換顯示文字，API 不回傳翻譯字串 |

## Engineer Review Questions

| 項目 | 需確認原因 | 工程師回覆 |
| --- | --- | --- |
| `task-workbench` 是否以 read-only 作為第一版 | 避免尚未確認主管人工判斷與各部門責任流程前即設計 mutation。 | 同意, 第一版先完成read-only |
| `dateRange` 的允許值是否足夠 | 影響任務看板首頁與 Dashboard drill-down 的查詢邏輯。 | 第一版先行定義上述數值，作為初始參考。後續若有新增需求或擴充情境，再依實際情況進行補充與調整。 |
| 任務可用庫存是否可用 `warehouse_no + item_no + batchNumber` 對應 | 若任務未指定批號，需確認是否允許以同倉同料品彙總候選批號。 | 可以 |
| 是否需要新增任務歷史表 | 第一版 timeline 只能呈現目前狀態；若需完整流程歷史，可能需要新增資料表。 | 需要完整的流程歷史，請進行資料表的規劃與設計。完成後，資料表提案文件也請統一集中放置於 api-proposal  |
