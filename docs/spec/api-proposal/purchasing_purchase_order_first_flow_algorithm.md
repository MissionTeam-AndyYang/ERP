# 採購中心採購單主視角 API 後端流程與演算法

> 對應畫面：`PurchasingWorkspaceScreen`  
> 對應預覽：`purchasing_purchase_order_first_static_preview.html`  
> 對應提案：`purchasing_purchase_order_first_proposal.md`  
> 狀態：Proposal / Pending Engineer Review

## 1. 設計原則

1. `purchase_order` 是第一版採購中心的主資料來源；請購、進貨、庫存與 workflow 是輔助關聯。
2. 所有 API 支援任意歷史日期區間，不將日期限制硬編碼為 today、7d 或 30d。
3. API 回傳資料與 enum code，不回傳前端專用中文文案、色彩或操作建議文字。
4. 只使用資料庫文件已定義的欄位與外鍵；沒有正式關聯時回傳空值、空陣列或 unknown code。
5. 庫存資料重用 Warehouse snapshot calculator，不在 Purchasing API 複製月結、delta 或 inventory_record 補算邏輯。
6. Quality Center 延至下一版；本版不可把缺少 Quality 資料解讀為合格、可用或已完成。

## 2. 共用 Step 1：解析任意歷史區間

1. 驗證 `startDate`、`endDate` 是否為 `YYYY-MM-DD`。
2. 驗證 `startDate <= endDate`；不合法回傳既有 validation error response。
3. 依 `timezone` 將起始日轉為 00:00:00、結束日轉為隔日 00:00:00 前一刻，再轉成 UTC timestamp。
4. 不以固定日期跨度取代使用者輸入；若查詢跨度很大，仍由 DB 日期條件、索引、排序與分頁控制資源。
5. `start` 最小為 0，`count` 預設 50、最大 100；不先查出全部資料再由 Python 切片。
6. 對 keyword、supplier、itemCategory、riskLevel 等條件盡可能在 SQLAlchemy query 層套用。

## 3. 共用 Step 2：建立採購單基礎資料列

1. 以 `purchase_order.date` 落在歷史區間的採購單為主集合。
2. 以 `purchase_order.item_ref_no = company.no` 取得供應商。
3. 以 `purchase_order.purchase_request_no = purchase_request.no` left join 請購資料。
4. 以 `purchase_order.no = goods_receipt_note.purchase_order_no` 批次取得進貨單。
5. 品項名稱優先使用 `purchase_order.item_name`；品項類別需依 item no 追溯正式料品主檔，未確認 mapping 前不可使用不存在的交易單據欄位。
6. `sourceOrderNo` 只取已連結請購單的 `product_order_no`；`linkedWorkOrderNo` 只取正式 workflow／APS 關聯。

## 4. 共用 Step 3：數量、金額與收貨狀態

```text
orderedQuantity = purchase_order.count or 0
receivedQuantity = sum(receipt.checkedCount * receipt.sign)
receipt.sign(category=0) = +1
receipt.sign(category=1) = -1
openQuantity = max(orderedQuantity - receivedQuantity, 0)
openPurchaseOrder = openQuantity > 0
```

1. 數量回傳取至小數點第 2 位。
2. 單價取至小數點第 4 位。
3. 金額優先使用資料表金額，回傳前四捨五入取整數。
4. `receivedQuantity` 使用 `checkedCount`，不以 `expectedCount` 或 `feeCount` 代替實際收貨數量。
5. `receivedQuantity <= 0` 且沒有正向進貨資料：`not_arrived`。
6. `0 < receivedQuantity < orderedQuantity`：`partial`。
7. `receivedQuantity >= orderedQuantity`：`received`。
8. 進貨退回造成淨收貨量下降時，保留 `returned` 風險／狀態資訊，不可把退回資料忽略。

## 5. API 1：採購單主視角 Dashboard

### Step 4：查詢、排序與分頁

1. 先在 DB 端篩選 `purchase_order.date` 區間。
2. 套用供應商、品項類別、keyword 等條件。
3. 以 `expectedDate ASC NULLS LAST`、`purchase_order.no ASC` 穩定排序。
4. 先取得本頁 PO identifiers，再批次取得請購、進貨、供應商、workflow 與庫存資料，避免 N+1 query。
5. `summary` 對完整篩選集合計算；`items[]` 才套用分頁。

### Step 5：Dashboard KPI

1. `openPurchaseOrderCount`：淨收貨量小於採購量的 PO 數。
2. `lateOrDueTodayCount`：`expectedDate` 小於或等於查詢基準日且尚有缺口的 PO 數。
3. `purchaseAmount`：篩選集合的 `purchase_order.amount` 加總。
4. `unlinkedPurchaseRequestCount`：`purchase_request_no` 為空或找不到正式請購資料的 PO 數。

## 6. API 2：交期風險

1. 先執行採購單基礎列與數量演算法。
2. 只保留 `riskLevel` 不是 `normal` 的 PO。
3. 風險判斷優先順序：
   - `late_arrival`：expectedDate 已過且有未收缺口。
   - `due_today`：expectedDate 等於查詢基準日且有未收缺口。
   - `purchase_request_unlinked`：無正式請購關聯。
   - `workflow_blocked`：已確認 workflow 任務阻塞。
   - `open_receipt`：已部分收貨但仍有缺口。
   - `unknown`：必要資料不足，不能標示 normal。
4. `shortageQuantity = openQuantity`。
5. `shortageValue` 以採購單價乘缺口數量計算，四捨五入取整數；若單價缺漏則回傳 0 並保留 unknown 狀態。
6. 影響來源只取正式工單、訂單或安全水位資料；不得以料號或日期相似度推測工單。

## 7. API 3：進貨單、驗收與入庫交接

1. 以 `goods_receipt_note.date` 篩選任意歷史區間。
2. 以 `purchase_order_no` 批次取得採購單資訊；無 PO 關聯時仍保留進貨單資料，並回傳關聯缺口 code。
3. 使用同一採購單、同一品項、日期與 no 排序，計算截至當筆進貨單日期的淨收貨量。
4. `qualityStatusCode` 在 Quality schema 尚未提供前只回傳 `deferred` 或 `unknown`。
5. `warehouseStatusCode` 只有在 Warehouse inventory 或已確認 workflow event 能證明交接狀態時才回傳 `pending_putaway`／`stocked`；否則回傳 `unknown`。
6. `nextOwnerDepartment` 只取已存在 workflow task 的 `ownerDepartment`，不由畫面文字推導。

## 8. API 4：供應商彙總

1. 先查詢日期區間內的採購單，再以 `supplierNo` 聚合。
2. `purchaseOrderCount`、`openPurchaseOrderCount`、`latePurchaseOrderCount` 與採購金額依 PO 計算。
3. `pendingReceiptQuantity` 為各 PO 缺口加總，取至小數點第 2 位。
4. 供應商風險取該供應商最嚴重的 PO risk level；若所有 PO 的必要資料不足，回傳 unknown。
5. 不建立供應商評分、替代推薦或交期預測模型。

## 9. API 5：採購單 Detail

1. 以 `purchase_order.no` 查詢單筆 PO；不存在時沿用既有 not-found response。
2. 依 `purchase_request_no` 查詢請購；欄位為空時回傳 `purchaseRequest = null`。
3. 依 `purchase_order_no` 查詢所有進貨單，按日期與 no 排序。
4. 依 `item_ref_no` 取得供應商 company。
5. `source` 只回傳正式請購來源訂單與已確認 workflow／APS 關聯。
6. `inventory` 呼叫共用 Warehouse snapshot calculator；不可在 Detail API 另寫庫存補算。
7. `relatedDocuments` 只取 `quotation.category = 1`、`contract.category = 1` 的正式採購資料，且不得把存在資料解讀為已核准或仍有效。
8. Timeline 由已確認的 PO、請購、進貨與 workflow 時間資料建立；缺少資料時顯示對應 code，不補造事件。

## 10. 效能與一致性

1. 日期欄位、`purchase_request_no`、`purchase_order_no`、`item_ref_no` 與 `supplier_no` 查詢條件應使用既有索引或由工程師確認索引狀態。
2. Dashboard 不先取回所有歷史 PO；使用 SQL `COUNT`、`SUM`、`GROUP BY` 與分頁。
3. 同一 request 內批次載入關聯資料，避免逐列 session query。
4. 庫存快照與 workflow 查詢應限定在本頁 PO 的 item／reference identifiers。
5. 任意歷史區間查詢仍須避免無界限 response；透過 `count` 控制頁面資料量，並回傳 `total`。
6. 若資料保存政策需要日期範圍限制，應由系統層明確回傳 validation code，不在 API 內默默縮短使用者指定區間。

## 11. 工程師需確認

1. `purchase_order.date`、`expectedDate`、`goods_receipt_note.date` 是否都是 UTC timestamp，日期邊界是否採 `Asia/Taipei`。
2. PO item no 經 `trans_items` 追溯 material／inproduct／product 的正式 mapping。
3. 進貨退回是否一律以 `category = 1` 扣除 `checkedCount`。
4. 是否有分批進貨的未來預計日期；若沒有，畫面只使用 PO `expectedDate`。
5. Quality 與 Warehouse 交接狀態的正式來源。
6. workflow task type 2／3／4 與 PO、進貨、入庫的正式 refCategory／ref_no 關聯。
7. 任意歷史區間是否受資料保存政策限制，以及限制時應回傳的標準錯誤 code。
