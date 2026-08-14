# TraceabilityWorkspaceScreen API 後端流程與演算法

> Status: API Proposal / Pending Engineer Review  
> Screen: `TraceabilityWorkspaceScreen`  
> Proposal: `traceability_center_proposal.md`

## 1. 共用處理原則

1. 每次設計與實作前先閱讀 `AGENTS.md`、`docs/spec/database/index.md` 與本提案文件。
2. 對外 service 方法若不需要外部共用 session，應在方法內自行建立 DB session。
3. 後端只回傳 enum code、數值、時間戳與資料庫欄位，不回傳前端顯示用繁中文字串。
4. 目前庫存數量與庫存價值相關邏輯必須重用既有 Warehouse 快照邏輯，例如 `CWarehouseInventorySnapshotCalculator` / `CWarehouseInventoryContextBuilder`，不得建立第二套月結與 delta 補算演算法。
5. 數值精度遵循既有規範：數量/重量取至小數點第 2 位、金額四捨五入取整數、單價取至小數點第 4 位。
6. 第一版為 read-only，不建立召回單、不修改文件、不鎖定庫存、不變更任務狀態。

## 2. 查詢區間與篩選

1. 若 query 同時提供 `startDate` 與 `endDate`，以此作為查詢區間。
2. 若未提供自訂區間，依 `period` 決定區間：
   - `7d`：以 API 執行當日往前 7 日至當下。
   - `30d`：以 API 執行當日往前 30 日至當下。
   - `90d` 或未提供：以 API 執行當日往前 90 日至當下。
3. `keyword` 同時套用於批號、料號、品名、來源單號、工單號、訂單號、供應商名稱與客戶名稱。
4. `traceDirectionCode`：
   - `upstream`：由成品/在製品批號往原料、供應商與進貨來源追溯。
   - `downstream`：由原料/物料批號往製程投入、產出、庫存、出貨與客戶流向追溯。
   - `both`：同時回傳可判定的上游與下游關聯。
5. `start`、`count` 需防護：`start < 0` 視為 0，`count <= 0` 視為預設 50，`count > 100` 限制為 100。

## 3. 共用資料集合

### 3.1 批號主檔

1. 查詢 `batch_number` 作為批號主索引。
2. 依 `batchNo`、`itemNo`、`itemCategory`、`keyword` 與查詢區間篩選。
3. 若同一批號有多筆主檔資料，以 `date desc`、`creationTime desc`、`id desc` 取最新一筆作為 header。
4. 回填 `batchNo`、`itemNo`、`itemName`、`itemCategory`、`itemSubCategory`、`itemType`、`unit`、`validDate`、`validDays`、`sourceRefCategory`、`sourceNo`。

### 3.2 庫存快照

1. 呼叫 Warehouse 快照共用邏輯，取得查詢批號於查詢結束時間的目前庫存。
2. 只在需要呈現目前庫存與召回影響量時使用 `currentQuantity > 0` 的庫存列。
3. 以 `itemNo + batchNo + warehouseNo` 建立 stock key，供 dashboard 與 overview 重用。

### 3.3 生產投入與產出

1. 以 `production_data_input.batch_number` 查詢此批號是否被投入工單。
2. 以 `production_data_output.batch_number` 查詢此批號是否由工單產出。
3. 關聯 `production_data` 取得工單 no、製程、日期與狀態。
4. 建立追溯鏈節點：
   - `production_input`
   - `production_output`
5. 若投入與產出可透過同一工單或製程單連接，建立 `consumed_by` 與 `produced_as` edge。

### 3.4 庫存異動與任務事件

1. 查詢 `inventory_record.batchNumber=batchNo` 作為時間軸事件來源。
2. 查詢 `workflow_task_state` 與 `workflow_task_event`，補充未完成任務、阻塞事件與下一步負責部門。
3. 事件排序以 `eventTimestamp asc` 為主；同時間時依 `eventTypeCode`、`refNo` 穩定排序。

### 3.5 文件完整性

1. 文件資料若有正式文件表，應以正式文件表為主。
2. 若尚無正式文件表，第一版僅依可確認的來源資料表與流程事件建立文件狀態：
   - 進貨來源應有 `receipt` 文件。
   - 採購原料可標示預期 `coa` 與 `temperature`，但若無正式表只能回傳 `unknown` 或 `pending`，不得推測已完成。
   - 生產工單可建立 `production` 文件節點。
   - 品檢任務或品檢保留可建立 `quality` 文件節點。
   - 出貨資料若 schema 尚未確認，不回傳虛構出貨文件。
3. `documents[].statusCode` 判斷：
   - 有明確文件資料：`complete`
   - 流程上應存在但尚未找到、且工程師確認可如此判斷：`pending`
   - 流程必備但明確缺失：`missing`
   - 此批號情境不需要：`not_required`
   - 規則不足：`unknown`

## 4. 追溯狀態與風險判斷

1. 若必要來源、投入/產出、庫存或出貨關聯可完整連接，`traceStatusCode=complete`。
2. 若主要追溯鏈可連接，但文件存在 `pending` 或 `missing`，`traceStatusCode=document_pending`。
3. 若批號找得到但來源或去向關鍵節點無法連接，`traceStatusCode=broken`。
4. 若資料不足以判定，`traceStatusCode=unknown`。
5. `riskLevelCode` 判斷：
   - `broken`、必要文件 `missing`、已過期且仍有影響量：`high_risk`
   - `document_pending`、近效期、品檢保留或召回影響量大於 0：`attention`
   - 無風險：`normal`
6. `primaryRiskCode` 優先順序：
   - `broken_chain`
   - `document_missing`
   - `expired`
   - `quality_hold`
   - `recall_scope`
   - `document_pending`
   - `normal`
   - `unknown`

## 5. GET `/api/v2/traceability/dashboard`

1. 驗證 query parameters。
2. 建立候選批號集合：
   - 優先由 `batch_number` 取得批號。
   - 若 `queryTypeCode=order` 或 `work_order`，由可確認的訂單/工單關聯反查批號。
   - 若 `queryTypeCode=document`，由文件或 workflow 來源反查批號；無正式資料時不推測。
3. 批次查詢庫存快照、production input/output、inventory record、quality hold、workflow task。
4. 對每個批號建立 dashboard row：
   - 決定 `queryTypeCode`、`queryValue`。
   - 回填批號主檔與來源單據。
   - 彙總 `currentQuantity`。
   - 彙總 `impactedQuantity` 與 `impactedCustomerCount`。
   - 計算 `traceStatusCode`、`riskLevelCode`、`primaryRiskCode`、`documentPendingCount`。
   - 取得最近事件時間 `latestEventTimestamp`。
5. 套用 `traceStatusCode`、`documentStatusCode`、`riskLevelCode` 等後置篩選。
6. 固定排序：
   - `riskLevelCode` 高到低。
   - `documentPendingCount` 多到少。
   - `latestEventTimestamp` 新到舊。
   - `batchNo` 穩定排序。
7. 分頁後回傳 `records`、`summary`、`total`、`start`、`count`。

## 6. GET `/api/v2/traceability/batches/{batch_no}/overview`

1. 驗證 `batch_no`。
2. 查詢批號主檔；不存在時沿用既有 not-found response contract。
3. 批次取得此批號的庫存快照、進出庫紀錄、生產投入/產出、品檢保留、workflow task 與文件資料。
4. 建立 `batch` header。
5. 建立 `impactSummary`：
   - `currentQuantity`：目前庫存數量。
   - `inProductionQuantity`：可判定仍在製程中或由投入未結案推導的數量。
   - `shippedQuantity`：由出貨/訂單資料可確認的已流向客戶數量；schema 未確認時回傳 0。
   - `impactedQuantity`：三者加總。
   - `impactedCustomerCount`：不重複客戶數。
   - `pendingDocumentCount`：文件待補/缺失數。
6. 建立 `nodes[]`：
   - 供應商、收貨、批號、庫存、生產投入、生產產出、品檢、出貨、客戶、文件等節點。
   - 僅建立可由資料表支持的節點，不建立推測節點。
7. 建立 `edges[]`：
   - 依來源、入庫、庫存、投入、產出、品檢、出貨與文件關聯建立連線。
   - 若缺少必要關聯，不建立虛構 edge，改由 `traceStatusCode=broken` 或 `document_pending` 表示。
8. 建立 `timeline[]`：
   - 由 inventory、production、workflow、document 事件合併。
   - 依時間由早到晚排序。
9. 建立 `documents[]` 並計算文件完整性。
10. 回傳完整 payload。

## 7. 效能與重構要求

1. Dashboard 不得逐筆批號執行 N+1 查詢；批號主檔、庫存快照、生產、庫存異動、任務與文件資料應批次取得後於記憶體中彙整。
2. Overview 可針對單一批號查詢明細，但仍應避免同一資料表重複查詢。
3. 追溯鏈建立邏輯建議封裝為 `CTraceabilityContextBuilder` 或相似 service，供 dashboard 與 batch overview 共用。
4. 若文件完整性判斷日後也供品保或出貨中心使用，應再抽出文件檢查共用物件。
5. 若正式實作需要新增 enum，應集中放置於 `restserver/package/common/common.py`。
6. 正式實作需建立 pytest，至少涵蓋：
   - dashboard 欄位存在性。
   - dashboard 篩選與分頁。
   - batch overview nodes/edges/timeline/documents 結構。
   - 文件 pending/missing 對 trace status 與 risk 的影響。
   - 無出貨 schema 時不得回傳虛構客戶流向。

## 8. 工程師待確認項目

| 項目 | 建議處理方式 | 工程師回覆 |
|---|---|---|
| 出貨/客戶資料來源 | 請工程師確認正式出貨、銷貨、訂單明細與客戶欄位；未確認前不推測 `shippedQuantity` 與 `customerName`。 | Pending |
| 文件表來源 | 若已有附件/文件表，請指定表名與欄位；若尚無，第一版只能以 workflow 與來源文件推導文件狀態。 | Pending |
| 工單 refCategory code | 請確認工單、製程單、出貨單在 `refCategory` 中的正式 code。 | Pending |
| 追溯鏈必要節點 | 請確認食品加工第一版中哪些節點為必備，例如 COA、溫度、品檢、出貨文件。 | Pending |

