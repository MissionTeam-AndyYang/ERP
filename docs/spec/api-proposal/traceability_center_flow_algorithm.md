# TraceabilityWorkspaceScreen API 後端流程與演算法

> Status: API Proposal / Pending Engineer Review  
> Screen: `TraceabilityWorkspaceScreen`  
> Proposal: `traceability_center_proposal.md`

## 1. 共用處理原則

1. 每次設計與實作前先閱讀 `AGENTS.md`、`docs/spec/database/index.md` 與本提案文件。
2. 第一版以批號為唯一主要追溯入口，不提供訂單、工單、文件作為獨立追溯入口。
3. 後端只回傳 enum code、數值、時間戳與資料庫欄位，不回傳前端顯示用繁中文字串。
4. 目前庫存數量相關邏輯必須重用既有 Warehouse 快照邏輯，例如 `CWarehouseInventorySnapshotCalculator` / `CWarehouseInventoryContextBuilder`，不得建立第二套月結與 delta 補算演算法。
5. 數值精度遵循既有規範：數量/重量取至小數點第 2 位、金額四捨五入取整數、單價取至小數點第 4 位。
6. 第一版為 read-only，不建立召回單、不修改文件、不鎖定庫存、不變更任務狀態。
7. 第一版暫不提供文件完整性與召回評估，因此流程不建立 `documents[]`、`impactSummary`、受影響客戶或召回相關欄位。

## 2. 查詢區間與篩選

1. `startDate` 與 `endDate` 為唯一日期區間條件；不提供 `period` 快速區間。
2. 若同時提供 `startDate` 與 `endDate`，以此作為查詢區間。
3. 若僅提供 `startDate`，查詢 `startDate` 之後的資料。
4. 若僅提供 `endDate`，查詢 `endDate` 之前的資料。
5. 若兩者皆未提供，不以日期區間篩選，但仍需受分頁限制保護。
6. `keyword` 套用於批號、料號、品名、來源單號、工單號、供應商或客戶關鍵字。
7. 第一版不開放 `documentStatusCode`、`traceDirectionCode`、`traceStatusCode`、`riskLevelCode` 作為查詢條件。
8. `start`、`count` 需防護：`start < 0` 視為 0，`count <= 0` 視為預設 50，`count > 100` 限制為 100。

## 3. 追溯方向判斷

1. 原料、物料、膠捲批號：向下追溯，`traceDirectionCode=downstream`。
2. 製成品批號：向上追溯，`traceDirectionCode=upstream`。
3. 在製品批號：若可由資料關聯判斷上下游，回傳 `traceDirectionCode=both`，並呈現可確認的上游投入與下游產出。
4. 若料品類別不足以判斷，回傳 `traceDirectionCode=both`，但僅建立資料表能確認的節點與連線。

## 4. 共用資料集合

### 4.1 批號主檔

1. 查詢 `batch_number` 作為批號主索引。
2. 依 `batchNo`、`itemNo`、`itemCategory`、`keyword` 與日期區間篩選。
3. 若同一批號有多筆主檔資料，以 `date desc`、`creationTime desc`、`id desc` 取最新一筆作為 header。
4. 回填 `batchNo`、`itemNo`、`itemName`、`itemCategory`、`itemSubCategory`、`itemType`、`unit`、`validDate`、`validDays`、`refCategory`、`refNo`。

### 4.2 庫存快照

1. 呼叫 Warehouse 快照共用邏輯，取得查詢批號於查詢結束時間的目前庫存。
2. 僅回傳 `currentQuantity`；第一版不計算召回影響量。
3. 以 `itemNo + batchNo + warehouseNo` 建立 stock key，供 dashboard 與 overview 重用。

### 4.3 生產投入與產出

1. 以 `production_data_input.batch_number` 查詢此批號是否被投入工單。
2. 以 `production_data_output.batch_number` 查詢此批號是否由工單產出。
3. 關聯 `production_data` 取得工單 no、製程、日期與狀態。
4. 建立追溯鏈節點：`production_input`、`production_output`、`work_order`。
5. 若投入與產出可透過同一工單或製程單連接，建立 `consumed_by` 與 `produced_as` edge。
6. 支援一對多與多對多批號關聯：單一原料批號可連到多個在製品批號，多個在製品批號也可再連到多個製成品批號。

### 4.4 庫存異動與任務事件

1. 查詢 `inventory_record.batchNumber=batchNo` 作為時間軸事件來源。
2. 查詢 `workflow_task_state` 與 `workflow_task_event`，補充未完成任務、阻塞事件與下一步負責部門。
3. 事件排序以 `eventTimestamp asc` 為主；同時間時依 `eventTypeCode`、`refNo` 穩定排序。

## 5. 追溯鏈建構策略

1. 追溯鏈以 `nodes[]` 與 `edges[]` 呈現，不假設一定是單線流程。
2. 從查詢批號建立 root batch node。
3. 依追溯方向遞迴查找可確認的投入、產出、入庫、庫存、品檢與任務節點。
4. 每次擴展節點時以 `nodeTypeCode + refCategory + refNo + itemNo + batchNo` 建立 visited key，避免資料循環造成無限遞迴。
5. 若找到多個下游或上游批號，全部建立節點與 edge。
6. 若無法再找到可確認的下一個節點，停止該路徑追溯。
7. 若停止點屬於資料自然終點，維持 `complete`；若停止點表示來源或去向缺漏，判定 `broken`。
8. 不建立資料表無法支持的推測節點或推測 edge。

## 6. 追溯狀態與風險判斷

1. 若必要來源、投入/產出、庫存或品檢關聯可完整連接，`traceStatusCode=complete`。
2. 若批號找得到，但來源或去向關鍵節點無法連接，`traceStatusCode=broken`。
3. 若資料不足以判定，`traceStatusCode=unknown`。
4. `riskLevelCode` 判斷：
   - `broken`、已過期且仍有目前庫存、品檢保留或阻塞：`high_risk`
   - 近效期、品檢保留、任務阻塞但追溯鏈未斷：`attention`
   - 無風險：`normal`
5. `riskCode` 優先順序：
   - `broken_chain`
   - `expired`
   - `quality_hold`
   - `normal`
   - `unknown`

## 7. GET `/api/v2/trace/dashboard`

1. 驗證 query parameters。
2. 由 `batch_number` 取得候選批號集合。
3. 批次查詢庫存快照、production input/output、inventory record、quality hold、workflow task。
4. 對每個批號建立 dashboard row：
   - 依料品類別決定 `traceDirectionCode`。
   - 回填批號主檔與來源單據。
   - 回填 `partnerTypeCode`、`partnerNo`、`partnerName`；同一 row 僅使用一組 partner 欄位。
   - 彙總 `currentQuantity`。
   - 計算 `traceStatusCode`、`riskLevelCode`、`riskCode`。
   - 取得最近事件時間 `latestEventTimestamp`。
5. 固定排序：
   - `riskLevelCode` 高到低。
   - `traceStatusCode=broken` 優先。
   - `latestEventTimestamp` 新到舊。
   - `batchNo` 穩定排序。
6. 分頁後回傳 `records`、`summary`、`total`、`start`、`count`。

## 8. GET `/api/v2/trace/batches/{batch_no}/overview`

1. 驗證 `batch_no`。
2. 查詢批號主檔；不存在時沿用既有 not-found response contract。
3. 批次取得此批號相關的庫存快照、進出庫紀錄、生產投入/產出、品檢保留、workflow task。
4. 建立 `batch` header。
5. 建立 `nodes[]`：
   - 供應商、收貨、批號、庫存、生產投入、生產產出、工單、品檢、任務等節點。
   - 僅建立可由資料表支持的節點，不建立推測節點。
6. 建立 `edges[]`：
   - 依來源、入庫、庫存、投入、產出與品檢關聯建立連線。
   - 若缺少必要關聯，不建立虛構 edge，改由 `traceStatusCode=broken` 表示。
7. 建立 `timeline[]`：
   - 由 inventory、production、workflow 事件合併。
   - 依時間由早到晚排序。
8. 回傳完整 payload。

## 9. 效能與重構要求

1. Dashboard 不得逐筆批號執行 N+1 查詢；批號主檔、庫存快照、生產、庫存異動、任務資料應批次取得後於記憶體中彙整。
2. Overview 可針對單一批號查詢明細，但仍應避免同一資料表重複查詢。
3. 追溯鏈建立邏輯建議封裝為 `CTraceabilityContextBuilder` 或相似 service，供 dashboard 與 batch overview 共用。
4. 若正式實作需要新增 enum，應集中放置於 `restserver/package/common/common.py`。
5. 正式實作需建立 pytest，至少涵蓋：
   - dashboard 欄位存在性。
   - dashboard 批號查詢、日期區間與分頁。
   - batch overview nodes/edges/timeline 結構。
   - 原料批號向下追溯至多個在製品/製成品。
   - 製成品批號向上追溯至在製品/原料。
   - 追溯斷點對 `traceStatusCode`、`riskLevelCode`、`riskCode` 的影響。

## 10. 工程師待確認項目

| 項目 | 建議處理方式 | 工程師回覆 |
|---|---|---|
| 出貨/客戶資料來源 | 第一版暫不納入召回評估與客戶流向；待下一版再確認出貨、銷貨、訂單明細與客戶欄位。 | 目前暫不規劃設計「召回」的功能。 |
| 文件表來源 | 第一版暫不納入文件完整性；待下一版再確認附件/文件表與欄位。 | 目前暫不規劃設計「文件完整性」的顯示。 |
| 工單 refCategory code | `refCategory` 回傳來源單據類別 code，用於節點建構與前端 drill-down；正式 code 需依資料庫 enum/既有設計確認。 | 需於正式實作前確認 code 對照。 |
| 追溯鏈必要節點 | 第一版追到無法再追溯為止；若缺少必要來源或去向，判定 `broken`。 | 追溯流程持續進行至不可再追溯為止，並於此狀態下判定為 `broken`。 |
