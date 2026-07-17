# Quality Dashboard API 後端流程與演算法

> 對應畫面：`QualityWorkspaceScreen`  
> 對應文件：`quality_dashboard_proposal.md`  
> 狀態：Proposal / Pending Engineer Review

## 工程師回覆理解與文件更新

| 工程師回覆／提問 | 理解與確認 | 本次流程更新 |
| --- | --- | --- |
| 查詢期間與倉儲參數命名需統一。 | 採用 `period` 與 `warehouse_no`；`period` 支援 `today`、`7d`、`14d`，預設 `today`。 | Step 1 與所有查詢條件改用正式參數名稱。 |
| `workflow_task_state` 欄位來源不明。 | 依正式 DB schema：預計處理時間是 `dueTimestamp`，任務完成判斷使用 `taskStatus = 3`；schema 沒有 `completedTimestamp`，故第一版回傳 0。品檢單號只從 `warehouse_quality_hold.inspection_no` 取得。 | Step 3、Step 4 與 detail 流程不再假設不存在欄位。 |
| `warehouse_quality_hold` 欄位定義需明確。 | `no` 是對外 hold_no；`status` 為 1 保留中、2 已放行、3 退回、4 報廢。第一版只有 status=1 納入 active hold，未定義部分釋放推導。 | Step 2 與 detail Step 1 補充 status enum 與範圍限制。 |
| `holdValue` NULL 的處理方式。 | 優先使用資料表值；NULL 且數量與單價俱全時，以 `holdQuantity * unitCost` 補算；仍缺資料回傳 0，不回寫資料庫。 | Step 2 與 Step 8 補充 value fallback。 |
| 品檢保留與任務的關聯。 | 沒有直接 task-to-hold foreign key；使用 `refCategory/ref_no/ref_sub_no`，再以 item、batch、warehouse 交叉比對。完全吻合才視為 confirmed。 | Task、timeline 與 detail Step 3 更新關聯判斷。 |
| 品檢單資料表尚未規劃。 | 第一版不假設 inspection header/result/defect table；保留資料以 `warehouse_quality_hold` 為來源，正式品檢單另開 DB extension。 | Detail Step 1 與 Step 4 明確限制來源。 |
| 明細不存在與共用 Warehouse 計算邏輯。 | detail 沿用既有標準 not-found response；共用 Warehouse snapshot calculator，不在 Quality API 重寫補算邏輯。 | Detail Step 1、Step 2 與效能章節更新。 |

## 1. 設計原則

1. 只讀查詢，不修改品檢保留、任務或來源單據。
2. 先由 `workflow_task_state` 與 `warehouse_quality_hold` 取得可確認的資料，再組合畫面 payload。
3. 不推測不存在的 inspection、defect、sampling 或 result table。
4. Enum 回傳 code；多國語系顯示由前端完成。
5. 查詢需使用單一 DB session，避免每一區塊重複建立連線。
6. 大量清單必須在資料庫端套用篩選、排序與分頁，不可先取回全部資料再切片。

## 2. API 1：`GET /api/v2/quality/dashboard`

### Step 1：建立查詢範圍

1. 讀取 `date`，未提供時使用目前 UTC timestamp。
2. 依 `timezone` 將查詢基準日轉為當地日期。
3. `period=today` 使用當日 00:00:00 至 23:59:59；`period=7d` 與 `period=14d` 使用包含基準日在內的連續日期範圍。
4. 將非法 `period` 正規化為 `today`，不可讓錯誤參數造成無限或超大範圍查詢。

### Step 2：查詢有效品檢保留

以 `warehouse_quality_hold` 為主要來源：

```text
status = 1
date <= queryTimestamp
warehouse_no = request.warehouse_no（若有）
item_no 對應 itemCategory（若有）
```

1. 以 `hold_no`／`no`、item、batch、warehouse 做必要的聚合鍵。
2. `holdQuantity`、`holdValue` 使用資料表值加總。
3. NULL `holdValue` 優先以 `holdQuantity * unitCost` 補算；若任一欄位缺漏則回傳 0，不回寫資料庫。
4. 品檢保留數量小於等於 0 的列不建立 `riskAlerts[]`，但是否保留在摘要計算中需與工程師確認。

### Step 3：查詢品檢 workflow 任務

以 `workflow_task_state` 查詢 `taskType = 8`：

1. 套用日期、倉庫、關鍵字、status 與 `riskOnly` 條件。
2. `workflow_task_state.status` 直接轉為 API 的 `status` code，不在後端轉成中文字串。
3. `ownerDepartment` 直接回傳資料表 code。
4. `refCategory`、`sourceNo` 分別取自 `workflow_task_state.refCategory`、`workflow_task_state.ref_no`；`inspectionNo` 取自關聯 `warehouse_quality_hold.inspection_no`。若來源欄位不存在或無法關聯，回傳空值，不可自行拼接單號。
5. 逾期判斷需使用任務預計完成時間與查詢基準時間：

```text
taskStatus not in completed/cancelled
and dueTimestamp > 0
and dueTimestamp < queryTimestamp
=> status = overdue（僅 API 篩選與風險判斷，不覆寫 DB 狀態）
```

### Step 4：建立摘要

```text
pendingTaskCount = status in pending/in_progress/overdue 的不重複 task 數
overdueTaskCount = status = overdue 的不重複 task 數
blockedTaskCount = status = blocked 的不重複 task 數
activeHoldCount = 有效品檢保留筆數或 hold 單號去重數（需工程師確認）
activeHoldQuantity = sum(holdQuantity)
activeHoldValue = round(sum(holdValue))
affectedItemCount = 不重複 item_no 數
affectedWarehouseCount = 不重複 warehouse_no 數
```

### Step 5：建立分類統計

1. `holdByCategory` 以料品主檔的 `itemCategory` 分組。
2. `holdByWarehouse` 以 `warehouse_no` 分組。
3. 任何無法由正式主檔對應的料品，不可將其歸入任意類別；保留原始 code 並在工程師確認後決定 error／unknown 行為。

### Step 6：建立風險警示

建立以下 code，不產生中文 message：

| alertType | 觸發條件 | riskLevel 建議 |
|---|---|---:|
| `quality_hold` | 有效品檢保留且 holdQuantity > 0 | 3 |
| `quality_task_overdue` | 品檢任務已逾期且未完成 | 3 |
| `quality_task_blocked` | 品檢任務狀態為 blocked | 3 |
| `quality_source_missing` | 任務缺少工程師確認的來源單據關聯 | 1 |

同一 task／hold／item／batch／warehouse 組合只建立一筆相同 `alertType`，避免 dashboard 重複提示。

### Step 7：資料庫分頁與排序

1. `qualityTasks[]` 以 `dueTimestamp` ASC、`taskNo` ASC 排序；API 欄位名稱為 `plannedTimestamp`。
2. `start` 最小為 0，`count` 預設 50、最大 100。
3. `total` 為套用篩選後的任務總筆數，不是本次 page 筆數。
4. `summary`、hold aggregates 與 alerts 不應因 page slicing 而漏算全域摘要。

### Step 8：組裝 response

依 API proposal 的欄位順序組裝：`serverTimestamp`、`timezone`、`range`、`summary`、分類統計、任務、風險、分頁欄位。所有數字在 response 邊界統一格式化：數量兩位小數、金額整數。

## 3. API 2：`GET /api/v2/quality/holds/{hold_no}/detail`

### Step 1：查詢品檢保留

以 `warehouse_quality_hold.no = hold_no` 取得單筆紀錄。若不存在，沿用既有 API 標準 not found error；不得回傳虛構的空 hold。

### Step 2：查詢批號庫存摘要

使用既有 Warehouse inventory snapshot calculator／服務查詢同一 `warehouse_no + itemNo + batchNo`：

```text
quantity = snapshot.quantity
inventoryValue = snapshot.inventoryValue
availableQuantity = snapshot.availableQuantity
availableValue = snapshot.availableValue
qualityHoldQuantity = snapshot.qualityHoldQuantity
qualityHoldValue = snapshot.qualityHoldValue
```

若共用服務無法以指定條件查詢，應由工程師確認可重用介面後再實作，不得在 Quality API 重寫月結、delta、inventory_record 補算邏輯。

### Step 3：查詢關聯任務與時間線

1. 優先使用工程師確認的 task-to-hold reference。
2. 若沒有明確 reference，才可依來源單據、item、batch、warehouse 與日期交集查詢候選資料，且 response 必須能區分 `confirmed` 與 `inferred` 關聯。
3. `workflow_task_event` 依 event timestamp ASC、id ASC 排序。
4. `comment` 原樣回傳；不改寫成 UI 文案。

### Step 4：查詢關聯單據

只回傳實際存在且可由 `refCategory/ref_no/ref_sub_no` 追溯的單據；不得擴充未由正式 schema 確認的單據類型。

## 4. 效能與一致性

1. Dashboard 使用單一 session；hold aggregates、tasks 與 detail queries 不可各自建立 session。
2. 聚合與分頁在 SQLAlchemy query 層完成。
3. 不在 Python 端逐筆查 item、warehouse 或 task，避免 N+1 query；應先批次載入主檔並以 dictionary join。
4. detail 的 Warehouse snapshot calculator 必須沿用既有統計／delta／inventory_record 缺漏補算策略。
5. 只選取 API 實際需要欄位；不將整張表的未使用欄位轉成 JSON。
6. 對 `warehouse_quality_hold` 建議確認 `(status, date, warehouse_no, item_no, batchNumber)` 查詢索引是否足夠；若需調整，另產生 DB extension proposal，不在本 API 提案直接修改正式 schema。

## 5. 工程師回覆

| 項目 | 工程師回覆 | 理解與流程定義 |
| --- | --- | --- |
| `workflow_task_state` 時間與品檢欄位 | 工程師指出需依正式資料庫文件確認欄位定義。 | `plannedTimestamp` 對應 `dueTimestamp`；完成狀態使用 `taskStatus = 3`，因 schema 沒有完成時間欄位，`completedTimestamp` 固定回傳 0；`inspectionNo` 只從 `warehouse_quality_hold.inspection_no` 取得。 |
| `warehouse_quality_hold.no` | `warehouse_quality_hold` 為本次規劃的正式資料表，欄位定義需由提案文件明確化。 | `no` 是對外 hold_no；detail 以 `no = hold_no` 查詢，`id` 不作 API 查詢入口。 |
| `warehouse_quality_hold.status` | 需依提案與資料庫文件明確說明狀態。 | 1=保留中、2=已放行、3=退回、4=報廢；第一版只有 1 納入 active hold，部分釋放沒有獨立事件或狀態，不作推導。 |
| `holdValue` NULL | 工程師要求補充明確的 fallback 定義。 | 使用 `holdValue`；NULL 且 `holdQuantity`、`unitCost` 都有值時補算，否則回傳 0，不回寫資料庫。 |
| 品檢保留與任務關聯 | 工程師要求說明來源與關聯方式。 | 使用 `refCategory/ref_no/ref_sub_no` 並交叉比對 `item_no/batchNumber/warehouse_no`；完全吻合才視為 confirmed，沒有直接 task-to-hold foreign key。 |
| 共用 Warehouse snapshot calculator | 若能共用應盡量共用；必要時可集中至 `restserver/package/restserver/api/v2/common.py`。 | Quality detail 重用既有 calculator，不複製庫存月結、delta 與 `inventory_record` 補算邏輯；只有實際跨 API 共用時才移至共用 facade。 |
