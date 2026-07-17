# Quality Dashboard API 後端流程與演算法

> 對應畫面：`QualityWorkspaceScreen`  
> 對應文件：`quality_dashboard_proposal.md`  
> 狀態：Proposal / Pending Engineer Review

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
3. `today` 使用當日 00:00:00 至 23:59:59；`7d` 與 `14d` 使用包含基準日在內的連續日期範圍。
4. 將非法 `dateRange` 正規化為 `today`，不可讓錯誤參數造成無限或超大範圍查詢。

### Step 2：查詢有效品檢保留

以 `warehouse_quality_hold` 為主要來源：

```text
status = 1
date <= queryTimestamp
warehouse_no = warehouseNo（若有）
item_no 對應 itemCategory（若有）
```

1. 以 `hold_no`／`no`、item、batch、warehouse 做必要的聚合鍵。
2. `holdQuantity`、`holdValue` 使用資料表值加總。
3. NULL `holdValue` 的處理方式需工程師確認；未確認前不得以其他價格來源補算。
4. 品檢保留數量小於等於 0 的列不建立 `riskAlerts[]`，但是否保留在摘要計算中需與工程師確認。

### Step 3：查詢品檢 workflow 任務

以 `workflow_task_state` 查詢 `taskType = 8`：

1. 套用日期、倉庫、關鍵字、status 與 `riskOnly` 條件。
2. `workflow_task_state.status` 直接轉為 API 的 `status` code，不在後端轉成中文字串。
3. `ownerDepartment` 直接回傳資料表 code。
4. `sourceType`、`sourceNo`、`inspectionNo` 的實際欄位來源依工程師確認結果實作；若來源欄位不存在，回傳空值並建立資料缺漏狀態，不可自行拼接單號。
5. 逾期判斷需使用任務預計完成時間與查詢基準時間：

```text
status not in completed/cancelled
and plannedTimestamp > 0
and plannedTimestamp < queryTimestamp
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

1. `qualityTasks[]` 以 `plannedTimestamp` ASC、`taskNo` ASC 排序。
2. `start` 最小為 0，`count` 預設 50、最大 100。
3. `total` 為套用篩選後的任務總筆數，不是本次 page 筆數。
4. `summary`、hold aggregates 與 alerts 不應因 page slicing 而漏算全域摘要。

### Step 8：組裝 response

依 API proposal 的欄位順序組裝：`serverTimestamp`、`timezone`、`range`、`summary`、分類統計、任務、風險、分頁欄位。所有數字在 response 邊界統一格式化：數量兩位小數、金額整數。

## 3. API 2：`GET /api/v2/quality/holds/{hold_no}/detail`

### Step 1：查詢品檢保留

以 `warehouse_quality_hold.no = hold_no` 取得單筆紀錄。若不存在，沿用既有 API 標準 not found error；不得回傳虛構的空 hold。

### Step 2：查詢批號庫存摘要

使用既有 Warehouse inventory snapshot calculator／服務查詢同一 `warehouseNo + itemNo + batchNo`：

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

只回傳實際存在且可由來源欄位追溯的單據。若工程師尚未確認 `sourceType` 對應規則，`relatedDocuments[]` 暫不得擴充未知單據類型。

## 4. 效能與一致性

1. Dashboard 使用單一 session；hold aggregates、tasks 與 detail queries 不可各自建立 session。
2. 聚合與分頁在 SQLAlchemy query 層完成。
3. 不在 Python 端逐筆查 item、warehouse 或 task，避免 N+1 query；應先批次載入主檔並以 dictionary join。
4. detail 的 Warehouse snapshot calculator 必須沿用既有統計／delta／inventory_record 缺漏補算策略。
5. 只選取 API 實際需要欄位；不將整張表的未使用欄位轉成 JSON。
6. 對 `warehouse_quality_hold` 建議確認 `(status, date, warehouse_no, item_no, batchNumber)` 查詢索引是否足夠；若需調整，另產生 DB extension proposal，不在本 API 提案直接修改正式 schema。

## 5. 需工程師確認的實作阻塞點

1. `workflow_task_state` 的實際欄位是否包含 `plannedTimestamp`、`completedTimestamp`、`inspectionNo`；若名稱不同請指定正式欄位。
    - 工程師回覆: 目前無法明確得知 plannedTimestamp、completedTimestamp、inspectionNo 欄位的定義，因此工程師將無法回覆相關問題。此外，workflow_task_state 乃由你規劃設計，各欄位定義理應比工程師更清楚。若仍不清楚，請詳閱資料庫文件（docs\spec\database\index.md）。
2. `warehouse_quality_hold.no` 是否為可直接對外使用的 hold_no。
    - 工程師回覆: warehouse_quality_hold 乃由你規劃設計，各欄位定義理應比工程師更清楚。若仍不清楚，請詳閱資料庫文件（docs\spec\database\index.md）。
3. `warehouse_quality_hold.status` 的完整 enum 與部分釋放規則。
    - 工程師回覆: warehouse_quality_hold 乃由你規劃設計，各欄位定義理應比工程師更清楚。若仍不清楚，請詳閱資料庫文件（docs\spec\database\index.md）。
4. `holdValue` NULL 的處理方式。
    - 工程師回覆: 請詳細說明問題，目前僅提及 holdValue，資訊不足。若未能明確補充說明，工程師將無法回覆相關問題。
5. 品檢保留與任務的正式關聯 key。
    - 工程師回覆: 請詳細描述問題，否則工程師將無法回覆相關問題。
6. Quality API 是否可直接 import Warehouse snapshot calculator，或需新增一個共用 service facade。
    - 工程師回覆: 若函式能共用，請盡量共用。若認為程式碼的擺放位置不佳，則可將共用函式集中放置於 restserver\package\restserver\api\v2\common.py。