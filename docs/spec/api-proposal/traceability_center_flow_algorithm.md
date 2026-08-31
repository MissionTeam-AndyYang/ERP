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
8. Dashboard API 僅負責批號追溯摘要，不建立完整 `traceSteps[]`；完整追溯流程只由單批號 overview API 建立。

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

1. 原料批號：向下追溯，`traceDirectionCode=downstream`。
2. 製成品批號：向上追溯，`traceDirectionCode=upstream`。
3. 在製品批號：第一版暫不作為 overview 查詢起點展開，回傳 `traceDirectionCode=both`、空 `traceSteps[]`、`traceStatusCode=unknown` 與 `riskCode=unknown`。
4. 物料、膠捲與其他料品類別：第一版暫不展開，回傳 header 與空 `traceSteps[]`。
5. `traceDirectionCode` 是後端依 root 批號類別提供的追溯方向 code；overview 只沿查詢批號的路徑聚焦展開，不建立無限制完整上下游圖。

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

1. 追溯鏈以 `traceSteps[]` 呈現，不假設一定是單線流程。
2. 從查詢批號建立 root batch node。
3. 依查詢批號類別建立路徑聚焦的投產追溯流程：
   - 查詢製成品批號時，先由 `production_data_output.batch_number` 找出產出工單，再由同一 `work_order_no` 的 `production_data_input` 找出投入在製品/原物料；該 step 的 `outputItems[]` 只保留目前追溯中的製成品或在製品批號；若投入批號仍可由 `production_data_output` 找到產出來源，繼續往上游展開。
   - 查詢原料批號時，先由 `batch_number.refCategory/ref_no`、`goods_receipt_note`、`inventory_record` 建立採購/進貨/入庫來源，再由 `production_data_input.batch_number` 找出使用此批號的工單，並由同一 `work_order_no` 的 `production_data_output` 找出產出的在製品/製成品；該 step 的 `inputItems[]` 只保留目前追溯中的原料或在製品批號，下一層只沿在製品產出批號往下游展開。
   - 查詢在製品批號時，第一版不展開 production step；在製品僅作為原料往下游或製成品往上游追溯時的中間批號。
4. 每次擴展節點時以 `nodeTypeCode + refCategory + refNo + itemNo + batchNo` 建立 visited key，避免資料循環造成無限遞迴。
5. 若找到多個與目前追溯批號直接相關的下游或上游批號，建立對應 `traceSteps[]`；不得反向展開旁支投入或旁支產出。
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
2. 由 `batch_number` 取得候選批號集合，先套用 query 條件、排序與分頁，避免對全量批號建立追溯摘要。
3. 僅針對本頁批號集合批次查詢庫存快照、production input/output 存在性、inventory record 最新時間、quality hold、workflow task。
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
6. Dashboard 不建立完整追溯圖，也不得逐批號呼叫 overview。
7. 回傳 `records`、`summary`、`total`、`start`、`count`。

## 8. GET `/api/v2/trace/batches/{batch_no}/overview`

1. 驗證 `batch_no`。
2. 查詢批號主檔；不存在時沿用既有 not-found response contract。
3. 取得此批號相關的庫存快照、進出庫紀錄、生產投入/產出、品檢保留、workflow task。
4. 建立 `batch` header。
5. 若查詢批號的料品類別不是原料(1)或製成品(5)，回傳 `batch` header 與空 `traceSteps[]`；在製品(4)第一版不作為查詢起點。
6. 建立 `traceSteps[]`：
   - 採購/進貨來源建立 `receipt` step。
   - 產製資料建立 `production` step，第一版範圍以同一 `work_order_no` 為主。
   - 僅建立可由資料表支持的 step，不建立推測 step。
7. 建立 production step 時，第一版以 `work_order_no` 查詢工單投入與產出；`process_order_no` 尚未建立穩定關聯、`group` 資料尚未完整，因此不作為本版分組與過濾條件。
8. 若同一 `work_order_no` 同時混有多組尚未透過資料欄位可靠區隔的投入與產出，第一版無法保證可在工單內切分每一組批號關係；待未來 `group` 或正式關聯欄位完成資料治理後，再提升至更細粒度的 production step。
9. 製成品查詢採 upstream：`outputItems[]` 只保留目前追溯中的批號，下一層改由該 step 的 `inputItems[]` 繼續往上游展開；第一層不得讓查詢製成品批號的 `outputItems[]` 為空。
10. 原料查詢採 downstream：`inputItems[]` 只保留目前追溯中的批號，`outputItems[]` 顯示同一工單可確認的核心產出；下一層只由已確認為 `EItemCategory.INPRODUCT` 的 output 批號繼續往下游展開，製成品 output 只作為目前 step 的終點。
11. `receipt`、`production`、`sale` 維持在同一 `traceSteps[]`，不拆成獨立陣列；前端可用 `stepTypeCode` 判斷時間軸與製程階層呈現方式。
12. 單次 overview 請求需快取已查詢的 batch header、batch input/output、work order input/output 與 production data，降低重複查詢成本。
13. `inputItems[]` 與 `outputItems[]` 依 `itemNo + batchNo + itemCategory + unit` 彙整；投入物需依 `production_data_input.action` 計算淨投入量：`action=1` 領料為正數、`action=2` 退料為負數，最後加總為 `inputItems[].quantity`。淨投入量為 0 的投入項目不回傳；若該投入批號為目前追溯路徑的 focus input，該 production step 不建立，也不將產出批號加入下一層 trace queue。物料與膠捲不列入第一版 trace step item。
14. 若同一 `work_order_no` 因多個追溯批號被重複命中同一 `stepId`，需合併新的 focus `inputItems[]` / `outputItems[]` 至既有 step；相同 `itemNo + batchNo + itemCategory + unit` 的既有 output 不可重複加總。
15. 回傳完整 payload。
16. 若查詢批號為製成品，必須可由製成品產出工單往上游展開至在製品與原物料投入；若查詢批號為原料，必須可由採購/進貨來源往下游展開至使用此原料的工單與產出的在製品/製成品；若查詢批號為在製品，第一版回傳空 `traceSteps[]`。

## 9. 效能與重構要求

1. Dashboard 不得逐筆批號執行 N+1 查詢；批號主檔、庫存快照、生產、庫存異動、任務資料應批次取得後於記憶體中彙整。
2. Dashboard 應先完成 DB 層分頁，再對本頁批號集合做 bounded 查詢；不可先對全部批號計算完整追溯資訊後再分頁。
3. Overview 可針對單一批號查詢明細，但仍應避免同一資料表重複查詢。
4. 若現有 Warehouse 快照 context 對 dashboard 全量資料成本過高，建議抽出批號集合專用 snapshot helper，只取本頁批號需要的 `currentQuantity`、主要倉庫與品檢保留訊號。
5. 建議確認或新增查詢索引：`batch_number(no)`、`batch_number(item_no)`、`batch_number(itemCategory, date)`、`inventory_record(batchNumber, date)`、`production_data_input(batch_number, work_order_no)`、`production_data_output(batch_number, work_order_no)`、`production_data_input(work_order_no)`、`production_data_output(work_order_no)`、`warehouse_quality_hold(batchNumber, date)`。
6. 追溯鏈建立邏輯建議封裝為 `CTraceabilityContextBuilder` 或相似 service，供 dashboard 與 batch overview 共用；dashboard 僅使用摘要能力，overview 才使用路徑聚焦展開能力。
7. 若正式實作需要新增 enum，應集中放置於 `restserver/package/common/common.py`。
8. 正式實作需建立 pytest，至少涵蓋：
   - dashboard 欄位存在性。
   - dashboard 批號查詢、日期區間與分頁。
   - batch overview `traceSteps[]` 結構。
   - 製成品查詢時，查詢批號所在 production step 的 `outputItems[]` 不可因過濾或 `process_order_no` 空值而漏失。
   - 原料批號由採購/進貨來源往下游追溯至直接相關的在製品/製成品，且不混入下游製成品的其他非查詢原料。
   - 原料往下游查詢時，若 input/output 的 `process_order_no` 或 `group` 單側空值，仍需依 `work_order_no` 回傳可確認的 `outputItems[]`。
   - 製成品批號由產出工單往上游追溯至在製品/原物料投入，且 `outputItems[]` 只保留目前追溯批號。
   - 投入物數量需扣除 `production_data_input.action=2` 退料數量。
   - 同一 `stepId` 被多個追溯批號命中時，需保留所有 focus input 關係，且共同 output 不重複加總。
   - 在製品批號作為查詢起點時回傳空 `traceSteps[]`。
   - Dashboard 不建立完整 overview 流程、不逐批號呼叫 overview。
   - 追溯斷點對 `traceStatusCode`、`riskLevelCode`、`riskCode` 的影響。

## 10. 工程師待確認項目

| 項目 | 建議處理方式 | 工程師回覆 |
|---|---|---|
| 出貨/客戶資料來源 | 第一版暫不納入召回評估與客戶流向；待下一版再確認出貨、銷貨、訂單明細與客戶欄位。 | 目前暫不規劃設計「召回」的功能。 |
| 文件表來源 | 第一版暫不納入文件完整性；待下一版再確認附件/文件表與欄位。 | 目前暫不規劃設計「文件完整性」的顯示。 |
| 工單 refCategory code | `refCategory` 回傳來源單據類別 code，用於節點建構與前端 drill-down；正式 code 需依資料庫 enum/既有設計確認。 | 需於正式實作前確認 code 對照。 |
| 追溯鏈必要節點 | 第一版追到無法再追溯為止；若缺少必要來源或去向，判定 `broken`。 | 追溯流程持續進行至不可再追溯為止，並於此狀態下判定為 `broken`。 |
