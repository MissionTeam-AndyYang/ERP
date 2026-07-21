# 工程師提問V3
1. 請將 plannedTimestamp 更名為 dueTimestamp。相同定義的回傳欄位命名，應盡量與資料庫欄位名稱一致，或與已實作 API 的回傳欄位名稱保持一致，不要再產生新的欄位命名。
2. 針對"completedTimestamp 並非 workflow_task_state 既有欄位，第一版任務完成時回傳 0"。是否應該提出解決方法？例如：在資料表中新增欄位，或是從其他來源取得資料，而非直接回傳 0。抑或此欄位並非目前設計畫面所需？

## 工程師提問V3理解與文件更新

| 工程師提問V3 | 理解與確認 | 本次文件更新 |
| --- | --- | --- |
| 將 `plannedTimestamp` 更名為 `dueTimestamp`。 | 採用。該欄位實際來源是 `workflow_task_state.dueTimestamp`，不再建立不同語意的 API 欄位名稱。 | `qualityTasks[].plannedTimestamp` 全面更名為 `qualityTasks[].dueTimestamp`，並同步更新欄位說明、範例與流程文件。 |
| `completedTimestamp` 沒有 `workflow_task_state` 欄位來源。 | 採用移除欄位。第一版畫面可依 `taskStatus` 判斷任務是否完成，數量與保留狀態也已有獨立欄位；目前沒有足夠需求新增完成時間欄位，也不可用 `updateTime` 冒充完成時間。 | 從 Success Response Data、Field Description、範例及流程文件移除 `completedTimestamp`；不新增 Quality DB Schema。 |

# 工程師提問
1. 查詢參數的命名需統一。例如：在`/api/v2/orders/dashboard` 中查詢期間的參數命名為 period，而在此則命名為 dateRange。此命名規則請套用至後續設計的所有 API。
2. 查詢參數的命名規則統一為 xxx_no，因此請將 warehouseNo 修正為 warehouse_no。此命名規則請套用至後續設計的所有 API。
3. 請補全兩個 API 的 Field Description，並重新檢視整份文件。文件的格式規格請以 warehouse_inventory_detail_proposal.md 為基準。

## 工程師提問理解與文件更新

| 工程師提問 | 理解與確認 | 本次文件更新 |
| --- | --- | --- |
| 查詢期間參數需與 Orders API 統一。 | 採用 `period` 作為查詢期間參數；支援 `today`、`7d`、`14d`，預設 `today`。response 的 `range.period` 回傳實際採用的期間代碼。 | 將 query parameter `dateRange` 改為 `period`，並同步更新流程與範例資料。 |
| 查詢參數命名統一為 `xxx_no`。 | 採用 `warehouse_no` 作為查詢參數名稱。response 欄位仍依現有 API camelCase 規則使用 `warehouseNo`。 | 將 query parameter `warehouseNo` 改為 `warehouse_no`；response 欄位維持 `warehouseNo`。 |
| 需明確說明來源欄位。 | 品檢任務來源取自 `workflow_task_state.refCategory` 與 `workflow_task_state.ref_no`；品檢保留來源取自 `warehouse_quality_hold.refCategory` 與 `warehouse_quality_hold.ref_no`。API 的 `sourceNo` 對應資料庫 `ref_no`；不自行拼接或推測來源單號。 | 將 `sourceType` 統一改為 API 欄位 `refCategory`，補充來源資料表與欄位說明。 |
| `dueTimestamp`、`inspectionNo` 的來源。 | `dueTimestamp` 對應 `workflow_task_state.dueTimestamp`；`inspectionNo` 僅取自 `warehouse_quality_hold.inspection_no`，無對應保留紀錄時回傳空字串。任務完成使用 `taskStatus = 3`，不另回傳完成時間。 | 更新任務欄位說明與流程，移除沒有資料來源的 `completedTimestamp`。 |
| `warehouse_quality_hold.no` 是否為 `hold_no`。 | 是。`warehouse_quality_hold.no` 是品檢保留業務識別碼，對應 detail API path parameter `hold_no`；`id` 僅為資料庫流水號，不對外作查詢入口。 | 補充 detail API 查詢規則。 |
| `warehouse_quality_hold.status` 與部分釋放規則。 | 第一版依 schema 使用 `1=保留中、2=已放行、3=退回、4=報廢`；只有 `status=1` 納入 active hold。schema 尚未定義部分釋放專用事件或狀態，故不在本版推導部分釋放流程。 | 更新有效保留、狀態 enum 與非本次範圍說明。 |
| `holdValue` NULL 的處理方式。 | 優先使用 `warehouse_quality_hold.holdValue`；若為 NULL 且 `holdQuantity`、`unitCost` 均有值，使用 `holdQuantity * unitCost` 補算；仍無法計算時回傳 `0`，不改寫資料庫。 | 補充 holdValue fallback 演算法與欄位說明。 |
| 品檢保留與任務的關聯方式。 | 目前 schema 沒有直接 task-to-hold foreign key。第一版使用 `refCategory/ref_no/ref_sub_no`，再以 `item_no/batchNumber/warehouse_no` 交叉比對；能完全對應才列為 confirmed，否則不將候選資料誤列為正式關聯。 | 更新任務、保留與 detail timeline 的關聯規則。 |
| 品檢單資料表尚未規劃。 | 採用工程師回覆，第一版不假設 inspection header/result/defect table。當進貨、入庫、生產或其他流程需要對料品進行品質判定並產生保留時，先由 `warehouse_quality_hold` 保存保留資料；正式品檢單與結果資料另開 Quality DB extension proposal。 | 保留 `inspectionNo` nullable，並在非本次範圍明確標示不新增品檢單表。 |
| 明細不存在時的錯誤處理。 | 沿用 `restserver/package/restserver/api/v2/` 既有標準 not-found response 與 HTTP status；detail 不回傳虛構的空 hold。 | 補充既有 API 錯誤處理規則。 |
| 共用 Warehouse snapshot calculator 的位置。 | 採用共用原則。Quality API 應直接重用既有 snapshot calculator；若需跨模組使用，優先移至既有共用 service／`restserver/package/restserver/api/v2/common.py`，不在 Quality API 複製月結、delta 與 inventory_record 補算邏輯。 | 更新 detail inventory 查詢與維護性說明。 |


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
| `period` | String | No | `today`、`7d`、`14d`，預設 `today`。 |
| `warehouse_no` | String | No | 限定倉儲別名 no。 |
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
    "period": "String"
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
      "refCategory": "Integer",
      "sourceNo": "String",
      "inspectionNo": "String",
      "itemNo": "String",
      "itemName": "String",
      "batchNo": "String",
      "warehouseNo": "String",
      "quantity": "Float",
      "value": "Integer",
      "dueTimestamp": "Integer",
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

### 3.3 Field Description

| Field | Type | Description |
|---|---|---|
| `serverTimestamp` | Integer | API response 建立時間，UTC timestamp。 |
| `timezone` | String | 本次日期分組所使用的 IANA 時區。 |
| `range.startTimestamp` | Integer | 查詢範圍起始時間，UTC timestamp。 |
| `range.endTimestamp` | Integer | 查詢範圍結束時間，UTC timestamp。 |
| `range.period` | String | 實際採用的查詢期間代碼。 |
| `summary.pendingTaskCount` | Integer | 狀態為待處理或進行中，且未被判定為逾期或阻塞的品檢任務數。 |
| `summary.overdueTaskCount` | Integer | 已超過 `workflow_task_state.dueTimestamp` 且 `taskStatus` 尚未完成或取消的品檢任務數。 |
| `summary.blockedTaskCount` | Integer | `workflow_task_state.taskStatus = 4` 的品檢任務數。 |
| `summary.activeHoldCount` | Integer | `warehouse_quality_hold.status = 1` 的有效品檢保留筆數。 |
| `summary.activeHoldQuantity` | Float | 有效品檢保留的 `holdQuantity` 加總，四捨五入至小數點第 2 位。 |
| `summary.activeHoldValue` | Integer | 有效品檢保留價值加總，四捨五入取整數。 |
| `summary.affectedItemCount` | Integer | 有效品檢保留涉及的不重複 `item_no` 數量。 |
| `summary.affectedWarehouseCount` | Integer | 有效品檢保留涉及的不重複 `warehouse_no` 數量。 |
| `holdByCategory[].itemCategory` | Integer | 料品品項類別，來源為料品主檔對應的類別 code。 |
| `holdByCategory[].holdCount` | Integer | 該料品類別的有效品檢保留筆數。 |
| `holdByCategory[].holdQuantity` | Float | 該料品類別的有效保留數量加總。 |
| `holdByCategory[].holdValue` | Integer | 該料品類別的有效保留價值加總。 |
| `holdByWarehouse[].warehouseNo` | String | 倉儲別名 no，來源為 `warehouse_quality_hold.warehouse_no`。 |
| `holdByWarehouse[].holdCount` | Integer | 該倉儲的有效品檢保留筆數。 |
| `holdByWarehouse[].holdQuantity` | Float | 該倉儲的有效保留數量加總。 |
| `holdByWarehouse[].holdValue` | Integer | 該倉儲的有效保留價值加總。 |
| `qualityTasks[].taskId` | String | `workflow_task_state.taskId` 任務識別碼。 |
| `qualityTasks[].taskNo` | String | 前端顯示用任務編號；若無獨立任務編號，回傳 `taskId`。 |
| `qualityTasks[].taskType` | Integer | 任務類型；本 API 固定查詢品檢 `8`。 |
| `qualityTasks[].status` | String | 由 `taskStatus` 與 due time 推導的 API 狀態 code；前端轉換顯示文字。 |
| `qualityTasks[].riskLevel` | Integer | 風險等級 code；由逾期、阻塞及品檢保留條件判斷。 |
| `qualityTasks[].ownerDepartment` | Integer | `workflow_task_state.ownerDepartment` 下一步負責部門 code。 |
| `qualityTasks[].refCategory` | Integer | `workflow_task_state.refCategory` 主來源類別 code。 |
| `qualityTasks[].sourceNo` | String | `workflow_task_state.ref_no` 主來源單號。 |
| `qualityTasks[].inspectionNo` | String | `warehouse_quality_hold.inspection_no`；無對應保留時為空字串。 |
| `qualityTasks[].itemNo` | String | `workflow_task_state.item_no` 料品編號。 |
| `qualityTasks[].itemName` | String | `workflow_task_state.item_name` 料品名稱。 |
| `qualityTasks[].batchNo` | String | `workflow_task_state.batchNumber` 批號。 |
| `qualityTasks[].warehouseNo` | String | `workflow_task_state.warehouse_no` 倉儲別名 no。 |
| `qualityTasks[].quantity` | Float | 任務預期處理數量，優先使用 `expectedQuantity`，數量缺漏時回傳 0。 |
| `qualityTasks[].value` | Integer | 任務對應品檢保留價值；無法對應時回傳 0。 |
| `qualityTasks[].dueTimestamp` | Integer | `workflow_task_state.dueTimestamp` 預計處理時間；無值時回傳 0。 |
| `qualityTasks[].comment` | String | `workflow_task_state.blockReason` 或資料備註；後端不產生 UI 顯示文案。 |
| `riskAlerts[].alertType` | String | 品質風險類型 code；前端依 code 轉換圖示、顏色與文字。 |
| `riskAlerts[].riskLevel` | Integer | 風險等級 code。 |
| `riskAlerts[].taskId` | String | 關聯任務識別碼；無任務關聯時為空字串。 |
| `riskAlerts[].holdNo` | String | 關聯 `warehouse_quality_hold.no`；無保留關聯時為空字串。 |
| `riskAlerts[].itemNo` | String | 關聯料品編號。 |
| `riskAlerts[].batchNo` | String | 關聯批號。 |
| `riskAlerts[].warehouseNo` | String | 關聯倉儲別名 no。 |
| `riskAlerts[].quantity` | Float | 風險關聯數量，數量缺漏時回傳 0。 |
| `riskAlerts[].value` | Integer | 風險關聯價值，無法計算時回傳 0。 |
| `riskAlerts[].ownerDepartment` | Integer | 關聯任務的下一步負責部門 code。 |
| `total` | Integer | 套用任務篩選條件後的任務總筆數。 |
| `start` | Integer | 本次任務分頁起點。 |
| `count` | Integer | 本次回傳任務筆數。 |

### 3.4 欄位規則

| 欄位 | 說明 |
|---|---|
| `summary.activeHold*` | 只計算 `warehouse_quality_hold.status = 1` 且 `date <= 查詢基準時間` 的資料；數量取 `holdQuantity` 加總，價值依 `holdValue` fallback 規則計算。 |
| `holdByCategory` | 依 `warehouse_quality_hold.item_no` 對應料品主檔的料品類別分組；若料品主檔無法對應，該列須標示資料缺漏，不得自行推測類別。 |
| `holdByWarehouse` | 依 `warehouse_quality_hold.warehouse_no` 分組；顯示名稱由前端使用 warehouse enum／主檔轉換。 |
| `qualityTasks` | 以 `workflow_task_state.taskType = 8` 為主要來源，並依查詢條件判斷狀態、日期、負責部門與來源單據。 |
| `riskAlerts` | 由逾期、阻塞、有效品檢保留及保留數量大於 0 的資料組成；不回傳前端顯示用 message 或 recommendedAction。 |
| Enum 欄位 | `taskType`、`status`、`ownerDepartment`、`refCategory`、`itemCategory` 僅回傳 code，由前端負責多國語系轉換。 |
| 數字精度 | 數量／重量小數點 2 位；金額四捨五入至整數。 |
| `holdValue` fallback | 優先使用資料表 `holdValue`；若為 NULL 且 `holdQuantity`、`unitCost` 均有值，使用 `holdQuantity * unitCost`；仍無法計算時回傳 0，不回寫資料庫。 |

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
    "refCategory": "Integer",
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

### 4.2 Field Description

| Field | Type | Description |
|---|---|---|
| `hold.holdNo` | String | `warehouse_quality_hold.no` 品檢保留業務識別碼；由 path parameter `hold_no` 查詢。 |
| `hold.inspectionNo` | String | `warehouse_quality_hold.inspection_no` 品檢單號；第一版可為空字串。 |
| `hold.status` | Integer | `warehouse_quality_hold.status`：1 保留中、2 已放行、3 退回、4 報廢。 |
| `hold.itemNo` | String | `warehouse_quality_hold.item_no` 料品編號。 |
| `hold.itemName` | String | `warehouse_quality_hold.item_name` 料品名稱；若資料為 NULL 回傳空字串。 |
| `hold.itemCategory` | Integer | `warehouse_quality_hold.itemCategory` 料品品項類別 code。 |
| `hold.batchNo` | String | `warehouse_quality_hold.batchNumber` 批號。 |
| `hold.warehouseNo` | String | `warehouse_quality_hold.warehouse_no` 倉儲別名 no。 |
| `hold.holdQuantity` | Float | `warehouse_quality_hold.holdQuantity` 品檢保留數量。 |
| `hold.holdValue` | Integer | 優先取 `warehouse_quality_hold.holdValue`；NULL 時依 `holdQuantity * unitCost` 補算，仍無法計算時為 0。 |
| `hold.dateTimestamp` | Integer | `warehouse_quality_hold.date` 保留建立時間，UTC timestamp。 |
| `hold.refCategory` | Integer | `warehouse_quality_hold.refCategory` 保留來源類別 code。 |
| `hold.sourceNo` | String | `warehouse_quality_hold.ref_no` 保留來源單號。 |
| `hold.comment` | String | `warehouse_quality_hold.reason` 保留原因；後端原樣回傳，不產生 UI 文案。 |
| `inventory.quantity` | Float | Warehouse snapshot calculator 計算的批號目前庫存數量。 |
| `inventory.inventoryValue` | Integer | Warehouse snapshot calculator 計算的批號目前庫存價值。 |
| `inventory.availableQuantity` | Float | 扣除預留與品檢保留後的可用數量。 |
| `inventory.availableValue` | Integer | 扣除預留與品檢保留後的可用價值。 |
| `inventory.qualityHoldQuantity` | Float | 該批號有效品檢保留數量。 |
| `inventory.qualityHoldValue` | Integer | 該批號有效品檢保留價值。 |
| `tasks[]` | Array | 依已確認關聯規則取得的品檢 workflow 任務；無法確認關聯時回傳空陣列。 |
| `timeline[]` | Array | 依 `workflow_task_event.eventTimestamp`、`id` 排序的任務事件；無事件時回傳空陣列。 |
| `relatedDocuments[]` | Array | 可由 `refCategory/ref_no/ref_sub_no` 追溯的實際來源單據；未確認來源類型時回傳空陣列。 |

`tasks[]`、`timeline[]` 與 `relatedDocuments[]` 不假設存在 inspection header、inspection result 或 defect table。`tasks[]` 只使用 `workflow_task_state`，`timeline[]` 只使用 `workflow_task_event`；若未來建立正式品檢單／結果表，另開 Quality DB extension proposal。

## 5. 前端責任

1. 將 enum code 轉換為繁體中文、英文及其他語系字串。
2. 依 `riskAlerts[].alertType` 選擇顏色、圖示與篩選狀態，不由後端產生 UI message。
3. 依目前的 `warehouse_no`、`itemCategory`、`status` 組合導向 query string。
4. API 空資料、部分資料與錯誤狀態均須保留可辨識的空狀態，不以 mock 資料冒充正式結果。

## 6. 工程師需確認

| 項目 | 目前提案 | 需確認內容  | 工程師回覆 |
|---|---|---|---|
| 品檢任務來源 | `workflow_task_state.taskType = 8` | `refCategory`、`sourceNo` 是否可直接追到正式來源單據。 | 已依 schema 明確定義：`refCategory` 取自 `workflow_task_state.refCategory`，`sourceNo` 取自 `workflow_task_state.ref_no`；來源單據實體再依 refCategory 對應，API 不自行拼接。|
| 品檢保留資料 | `warehouse_quality_hold` | `status = 1` 是否代表有效保留；釋放、部分釋放與取消是否另有 event 或 status 定義。 | 依正式 schema：1=保留中、2=已放行、3=退回、4=報廢；第一版只有 1 納入 active hold，部分釋放沒有獨立事件或狀態，不作推導。 |
| 品檢單資料 | 目前不新增或假設 inspection table | 是否已有工程師尚未納入 schema 的品檢主檔／結果表；若有，請提供正式 table 與欄位。 | 目前尚未規劃品檢單資料表；第一版只使用 `warehouse_quality_hold.inspection_no`（可為空），正式品檢單與結果另開 Quality DB extension proposal。 |
| `holdValue` | 優先使用資料表值 | 若為 NULL，是否應回傳 0，或需依庫存單價補算。 | NULL 且 `holdQuantity`、`unitCost` 俱備時，以 `holdQuantity * unitCost` 補算；仍缺資料回傳 0，不回寫資料庫。 |
| 明細不存在 | 建議回傳標準 not found error | 是否沿用既有 API 的錯誤 code 與 HTTP status。 | 沿用 `restserver/package/restserver/api/v2/` 既有標準 not-found response 與 HTTP status；不回傳虛構空 hold。 |
| 任務與保留關聯 | 以來源單據與 item/batch/warehouse 交集關聯 | 是否存在明確 task-to-hold reference，若存在應優先使用。 | 目前沒有直接 task-to-hold foreign key；使用兩者的 `refCategory/ref_no/ref_sub_no` 並交叉比對 `item_no/batchNumber/warehouse_no`，完全吻合才視為 confirmed。 |

## 7. 範例資料

```json
{
  "serverTimestamp": 1784073600,
  "timezone": "Asia/Taipei",
  "range": {"startTimestamp": 1783987200, "endTimestamp": 1784073599, "period": "today"},
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
      "refCategory": 1,
      "sourceNo": "GRN-20260715-003",
      "inspectionNo": "INS-20260715-003",
      "itemNo": "RM-00031",
      "itemName": "原料示例",
      "batchNo": "B20260715003",
      "warehouseNo": "WH-RM",
      "quantity": 840.00,
      "value": 172000,
      "dueTimestamp": 1784066400,
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
