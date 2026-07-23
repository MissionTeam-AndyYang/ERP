# Purchasing Dashboard API 後端流程與演算法

> 對應畫面：`PurchasingWorkspaceScreen`  
> 對應文件：`purchasing_dashboard_proposal.md`  
> 狀態：Proposal / Pending Engineer Review

## 1. 設計原則

1. V1 read-only；不修改請購、採購、進貨、驗收、入庫或付款資料。
2. API 只組合正式資料表欄位與已確認關聯，不將前端中文文案、UI tone 或圖示放入 response。
3. Dashboard 與 detail 各使用單一 DB session；聚合、篩選、排序與分頁盡量在 SQLAlchemy query 層完成。
4. 庫存數量與可用量重用 Warehouse snapshot calculator，不在 Purchasing API 複製月結、delta 或 inventory_record 補算邏輯。
5. 不以缺少 Quality、APS 或 supplier rating 資料推測正常狀態；缺漏回傳明確 code。

## 2. 共用 Step 1：解析查詢條件

1. 讀取 `date`，未提供時使用目前 UTC timestamp。
2. 依 `timezone` 取得查詢基準日；`period=today` 為當日，`7d` 為當日加後續 6 日，`30d` 為當日加後續 29 日。
3. 非法 `period` fallback 為 `30d`；不可建立無限或超大查詢範圍。
4. `start` 最小為 0；`count` 預設 50、最大 100。
5. `supplier_no`、`item_category`、`stage`、`risk_only` 與 `keyword` 在資料庫端套用。

## 3. API 1：Dashboard

### Step 2：建立採購需求基礎列

1. 以 `purchase_request` 為主要需求來源。
2. 依 `purchase_request.no` left join `purchase_order.purchase_request_no`。
3. 依 `purchase_order.no` left join 多筆 `goods_receipt_note.purchase_order_no`。
4. 供應商優先取 `purchase_order.item_ref_no`，若尚未下單則使用已存在且可由正式關聯追溯的採購報價／合約資料；不能從未知欄位猜測供應商。
5. `sourceOrderNo` 取 `purchase_request.product_order_no`；`linkedWorkOrderNo` 只有在正式 workflow／APS 關聯存在時才回傳。

### Step 3：計算數量與金額

```text
requestedQuantity = purchase_request.count or 0
orderedQuantity = sum(purchase_order.count) or 0
receivedQuantity = sum(goods_receipt_note.checkedCount * sign(category))
sign(category=0) = +1
sign(category=1) = -1
openRequest = requestedQuantity > orderedQuantity
openPurchaseOrder = orderedQuantity > receivedQuantity
purchaseAmount = purchase_order.amount or 0
```

1. 數量取至小數點第 2 位。
2. 金額優先使用資料表金額，回傳前四捨五入取整數。
3. 進貨退回 `goods_receipt_note.category = 1` 扣除 `checkedCount`；此規則需工程師確認後才可實作。

### Step 4：計算庫存可用性

1. 以需求列的 `itemNo`、必要時加上倉儲條件呼叫共用 Warehouse snapshot calculator。
2. 回傳 `currentQuantity`、`reservedQuantity`、`availableQuantity`。
3. 從 `item_safety_stock` 取得 `safetyStock`；若無安全水位資料，回傳 0 並產生 `unknown`／資料缺漏狀態，不視為正常。
4. `availableQuantity < safetyStock` 觸發 `stock_below_safety`。

### Step 5：計算採購階段

1. 無請購來源或資料不完整：`unknown`。
2. 請購數量尚未轉成採購數量：`purchase_request_open`／`request_pending`。
3. 已有請購但缺採購類別 quotation：`supplier_quote_missing`／`quote_pending`。
4. 已有採購需求但缺採購類別 contract：`contract_missing`／`quote_pending`。
5. 已有採購單且尚未達收到數量：`ordered` 或 `arrival_pending`，依 expectedDate 與收貨狀態判斷。
6. 有進貨但尚未完成入庫：`receiving`。
7. 收貨數量已達應收量且 Warehouse snapshot 已反映：`stocked`。
8. 多個條件同時成立時，stage 以阻塞／缺料優先，risk 以最高風險優先。

### Step 6：計算到貨與風險

1. `expectedArrivalTimestamp < queryTimestamp` 且 `receivedQuantity < orderedQuantity`：`late_arrival`、`high_risk`。
2. 尚未下採購單但已低於安全水位或有已確認生產需求：`purchase_order_missing`、`high_risk`。
3. 低於安全水位但尚未逾期：`stock_below_safety`、`notice`。
4. 缺 quotation／contract 或 workflow blocked：`notice` 或 `high_risk`，依工程師確認的規則排序。
5. 無足夠來源資料：`unknown`、`unknown`，不可標示為正常。

### Step 7：計算到貨、品質與入庫狀態

1. 無進貨單：`receivingStatusCode = not_arrived`。
2. 實際收貨量大於 0 但小於訂購量：`partial`。
3. 實際收貨量達訂購量：`received`。
4. 若存在進貨退回且造成未達量，保留 `returned` 或依工程師確認規則判斷。
5. 第一版沒有正式 Quality inspection/result table，不可把缺少品質資料當作已合格；`qualityStatusCode` 只回傳 `deferred` 或 `unknown`。
6. `warehouseStatusCode` 需由 Warehouse inventory snapshot 或已確認 workflow event 判斷；無法確認時回傳 `unknown`。

### Step 8：建立 summary 與分頁

1. Summary 先針對完整篩選結果計算，再對 `items[]` 分頁。
2. `total` 為完整需求列總數，不是本頁數量。
3. 排序使用 `requiredTimestamp ASC`、`purchaseRequestNo ASC`，確保分頁穩定。
4. Supplier view 由 items 依 `supplierNo` 聚合；不需另建立 supplier dashboard API。

## 4. API 2：請購明細

1. 以 `purchase_request.no = purchase_request_no` 查詢單筆請購；不存在時沿用既有 API not-found response。
2. 以 `purchase_order.purchase_request_no` 查詢所有關聯採購單，按採購日期 ASC、no ASC 排序。
3. 以 `goods_receipt_note.purchase_order_no` 查詢所有關聯進貨單，按日期 ASC、no ASC 排序。
4. 以 `purchase_order.item_ref_no` join `company.no` 取得供應商；quotation／contract 僅限 `category = 1` 的採購資料，且不在目前提案中假設有效期限或核准狀態欄位。
5. 以 `purchase_request.product_order_no` 回傳來源訂單；其他來源只在 foreign key 或已確認 workflow relation 存在時加入。
6. 重用 Warehouse snapshot calculator 回傳 inventory；不得複製 Warehouse 庫存補算邏輯。
7. `workflow[]` 只取 `workflow_task_state` 與 `workflow_task_event` 的已確認關聯；不自行由日期或 item 相似度拼接任務。

## 5. 效能與一致性

1. 先取得分頁需求列的 identifiers，再批次查詢採購單、進貨單、供應商、quotation、contract 與 workflow，避免 N+1 query。
2. Summary 聚合使用 SQL `COUNT`／`SUM`；不先取回所有明細再於 Python 切片。
3. `purchase_request.product_order_no`、`purchase_order.purchase_request_no`、`goods_receipt_note.purchase_order_no`、`item_ref_no` 與日期欄位應確認索引。
4. Supplier view 使用已載入 items 聚合，避免同一頁重複查詢供應商。
5. 若後續需要供應商交期統計、替代供應商推薦或 APS shortage 計算，另開 proposal，不在本 API 偷加推測邏輯。

## 6. 工程師需確認的阻塞點

1. `quotation` 與 `contract` 的採購類別篩選是否固定使用 `category = 1`。
2. 進貨退回是否一律以 `goods_receipt_note.category = 1` 扣除 `checkedCount`。
3. `purchase_request` 是否可能一筆需求對應多筆 `purchase_order`；若可，`purchaseOrders[]` 聚合規則依本文件處理。
4. `warehouseStatusCode` 是否已有可確認的 Warehouse event／task 關聯。
5. 第一版 Purchasing 是否接受 Quality 狀態暫為 `deferred`／`unknown`。
6. `purchase_request.product_order_no` 是否是第一版唯一正式需求來源，APS／工單關聯是否另有正式欄位。
