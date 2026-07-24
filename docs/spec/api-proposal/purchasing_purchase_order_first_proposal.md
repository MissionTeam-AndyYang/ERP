# 採購中心採購單主視角 API 提案

> Status: Proposal / Pending Engineer Review  
> Screen: `PurchasingWorkspaceScreen`  
> Route: `/purchasing`  
> Scope: V1 Core、read-only  
> Design Basis: `purchasing_purchase_order_first_static_preview.html`

## 1. 畫面定位

本版以 `purchase_order` 為採購中心的主要資料列，支援管理者與採購主管查詢任意歷史日期區間，並從採購單追蹤供應商、預計到貨、分批進貨、驗收／文件、入庫交接與來源影響。

`purchase_request` 僅作為輔助關聯：採購單已連結請購單時顯示來源；未連結時明確顯示資料缺口，不反向推測請購來源。

第一版只提供查詢、篩選、排序、分頁與 detail drill-down，不執行建立或修改採購單、請購單、進貨單、驗收、入庫或付款。

## 2. 任意歷史區間

所有列表 API 支援 `startDate` 與 `endDate`，格式為 `YYYY-MM-DD`，以 `timezone` 解讀日期邊界。查詢區間不採用固定 `today`、`7d` 或 `30d` 限制；只要資料仍在系統保存範圍內，即可查詢任意歷史期間。

為避免歷史大區間造成大量回傳，API 必須搭配 DB 端日期篩選、穩定排序與分頁。頁面大小仍限制在 API 定義的 `count` 上限，但不以固定日期跨度取代使用者指定的歷史區間。

## 3. API 清單

| API | Method | 用途 |
|---|---|---|
| `/api/v2/purchasing/purchase-orders/dashboard` | GET | 採購單主視角 KPI 與採購單清單 |
| `/api/v2/purchasing/purchase-orders/delivery-risk` | GET | 交期風險清單與風險 KPI |
| `/api/v2/purchasing/goods-receipts/dashboard` | GET | 進貨單、驗收與入庫交接清單 |
| `/api/v2/purchasing/suppliers/dashboard` | GET | 供應商採購與交期彙總 |
| `/api/v2/purchasing/purchase-orders/{purchase_order_no}/detail` | GET | 單一採購單追蹤明細 |

以上均為 read-only API；本提案不新增資料表或資料表欄位。

## 4. 共用 Query Parameters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `startDate` | String | Yes | 查詢起始日，`YYYY-MM-DD`；含當日。 |
| `endDate` | String | Yes | 查詢結束日，`YYYY-MM-DD`；含當日，且不得早於 `startDate`。 |
| `timezone` | String | No | 日期邊界使用的 IANA timezone，預設 `Asia/Taipei`。 |
| `supplierNo` | String | No | 供應商 `company.no`。 |
| `itemCategory` | Integer | No | 料品品項類別 code；前端轉換多國語系。 |
| `riskLevel` | String | No | 風險等級 code。 |
| `keyword` | String | No | 採購單 no、進貨單 no、請購單 no、供應商 no／名稱、料號或品名。 |
| `start` | Integer | No | 分頁起點，預設 0。 |
| `count` | Integer | No | 回傳筆數，預設 50，最大 100。 |

日期篩選欄位依 API 固定定義：採購單 API 使用 `purchase_order.date`；進貨單 API 使用 `goods_receipt_note.date`；供應商彙總使用 `purchase_order.date`。

## 5. GET `/api/v2/purchasing/purchase-orders/dashboard`

### 5.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "timezone": "String",
  "range": {
    "startDate": "String",
    "endDate": "String",
    "startTimestamp": "Integer",
    "endTimestamp": "Integer"
  },
  "summary": {
    "openPurchaseOrderCount": "Integer",
    "lateOrDueTodayCount": "Integer",
    "purchaseAmount": "Integer",
    "unlinkedPurchaseRequestCount": "Integer"
  },
  "items": [
    {
      "purchaseOrderNo": "String",
      "purchaseDateTimestamp": "Integer",
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "unit": "Integer",
      "supplierNo": "String",
      "supplierName": "String",
      "orderedQuantity": "Float",
      "receivedQuantity": "Float",
      "openQuantity": "Float",
      "unitPrice": "Float",
      "purchaseAmount": "Integer",
      "expectedArrivalTimestamp": "Integer",
      "purchaseRequestNo": "String",
      "purchaseRequestLinkStatusCode": "String",
      "sourceOrderNo": "String",
      "linkedWorkOrderNo": "String",
      "receivingStatusCode": "String",
      "qualityStatusCode": "String",
      "warehouseStatusCode": "String",
      "riskLevel": "String",
      "riskCode": "String"
    }
  ],
  "total": "Integer",
  "start": "Integer",
  "count": "Integer"
}
```

### 5.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `serverTimestamp` | Integer | Response 建立時間，UTC timestamp。 |  |
| `timezone` | String | 本次日期邊界使用的 IANA timezone。 |  |
| `range.startDate` | String | 使用者指定的查詢起始日。 |  |
| `range.endDate` | String | 使用者指定的查詢結束日。 |  |
| `range.startTimestamp` | Integer | 起始日當地時間 00:00:00 的 UTC timestamp。 |  |
| `range.endTimestamp` | Integer | 結束日當地時間 23:59:59 的 UTC timestamp。 |  |
| `summary.openPurchaseOrderCount` | Integer | 查詢期間內，淨收貨數量小於採購數量的採購單數。 | `purchase_order.count`、`goods_receipt_note.checkedCount` |
| `summary.lateOrDueTodayCount` | Integer | 預計到貨日已逾期或等於查詢基準日，且尚有未收數量的採購單數。 | `purchase_order.expectedDate` |
| `summary.purchaseAmount` | Integer | 查詢期間採購單金額加總，四捨五入取整數。 | `purchase_order.amount` |
| `summary.unlinkedPurchaseRequestCount` | Integer | 查詢期間內沒有可對應 `purchase_request.no` 的採購單數。 | `purchase_order.purchase_request_no` |
| `items[]` | Array | 採購單主資料列，依預計到貨日、採購單 no 穩定排序。 |  |
| `items[].purchaseOrderNo` | String | 採購單 no。 | `purchase_order.no` |
| `items[].purchaseDateTimestamp` | Integer | 採購日期，UTC timestamp。 | `purchase_order.date` |
| `items[].itemNo` | String | 採購交易品項 no。 | `purchase_order.item_no` |
| `items[].itemName` | String | 採購交易品項名稱。 | `purchase_order.item_name` |
| `items[].itemCategory` | Integer | 料品品項類別 code；需依 `itemNo` 追溯正式料品主檔，不使用不存在於交易單據的欄位。 | `material.category` 或正式料品主檔；跨 `trans_items` 對應待工程師確認 |
| `items[].unit` | Integer | 採購交易單位 code。 | `purchase_order.unit` |
| `items[].supplierNo` | String | 供應商 company no。 | `purchase_order.item_ref_no` |
| `items[].supplierName` | String | 供應商顯示名稱。 | `company.displayName` |
| `items[].orderedQuantity` | Float | 採購數量，取至小數點第 2 位。 | `purchase_order.count` |
| `items[].receivedQuantity` | Float | 進貨實際數量淨值，取至小數點第 2 位。 | `goods_receipt_note.checkedCount`；進貨 `category=0` 加總、進貨退回 `category=1` 扣除 |
| `items[].openQuantity` | Float | `orderedQuantity - receivedQuantity`，小於 0 時回傳 0，取至小數點第 2 位。 | 計算欄位 |
| `items[].unitPrice` | Float | 採購單價，取至小數點第 4 位。 | `purchase_order.price` |
| `items[].purchaseAmount` | Integer | 採購單金額，四捨五入取整數。 | `purchase_order.amount` |
| `items[].expectedArrivalTimestamp` | Integer | 採購單預計進貨日期，UTC timestamp。 | `purchase_order.expectedDate` |
| `items[].purchaseRequestNo` | String | 關聯請購單 no；未連結時為空字串。 | `purchase_order.purchase_request_no` |
| `items[].purchaseRequestLinkStatusCode` | String | 請購關聯狀態 code。 | `linked`、`unlinked`、`invalid` |
| `items[].sourceOrderNo` | String | 請購單來源訂購單 no；無已確認請購關聯時為空字串。 | `purchase_request.product_order_no` |
| `items[].linkedWorkOrderNo` | String | 已確認的生產工單 no；無正式關聯時為空字串。 | 僅取已確認 workflow／APS 關聯 |
| `items[].receivingStatusCode` | String | 收貨狀態 code。 | `not_arrived`、`partial`、`received`、`returned`、`unknown` |
| `items[].qualityStatusCode` | String | 品檢／文件狀態 code；品保中心延期時不得假造結果。 | `deferred`、`unknown` |
| `items[].warehouseStatusCode` | String | 入庫交接狀態 code。 | `not_received`、`pending_putaway`、`stocked`、`unknown` |
| `items[].riskLevel` | String | 風險等級 code。 | `normal`、`notice`、`high_risk`、`unknown` |
| `items[].riskCode` | String | 主要風險代碼，前端依 code 轉換文字與色彩。 | `late_arrival`、`due_today`、`open_receipt`、`purchase_request_unlinked`、`workflow_blocked`、`unknown` |
| `total` | Integer | 套用篩選後的採購單總筆數。 |  |
| `start` | Integer | 本次分頁起點。 |  |
| `count` | Integer | 本次回傳採購單筆數。 |  |

## 6. GET `/api/v2/purchasing/purchase-orders/delivery-risk`

查詢參數與日期規則同第 4 節；只回傳 `riskLevel != normal` 的採購單。`items[]` 使用採購單主資料列，並額外回傳：

| Field Path | Type | Description |
|---|---|---|
| `items[].shortageQuantity` | Float | 尚未收貨數量，取至小數點第 2 位。 |
| `items[].shortageValue` | Integer | 尚未收貨數量對應採購金額，四捨五入取整數；不以庫存成本取代採購金額。 |
| `items[].impactSourceType` | String | 已確認的影響來源類型 code。 | `work_order`、`sales_order`、`safety_stock`、`unknown` |
| `items[].impactSourceNo` | String | 影響來源單號；無正式關聯時為空字串。 |
| `items[].followUpCode` | String | 前端追蹤動作 code，不是後端產生的中文建議。 | `confirm_supplier_date`、`check_document`、`check_putaway`、`review_source_impact`、`unknown` |

回傳 `summary` 包含 `highRiskCount`、`noticeCount`、`lateCount` 與 `affectedWorkOrderCount`；`affectedWorkOrderCount` 只計算正式關聯工單，不依品號或日期相似度推測。

## 7. GET `/api/v2/purchasing/goods-receipts/dashboard`

以 `goods_receipt_note.date` 篩選任意歷史區間，`items[]` 以進貨單為主：

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `items[].goodsReceiptNoteNo` | String | 進貨單 no。 | `goods_receipt_note.no` |
| `items[].purchaseOrderNo` | String | 關聯採購單 no；無關聯時為空字串。 | `goods_receipt_note.purchase_order_no` |
| `items[].receiptDateTimestamp` | Integer | 進貨／進貨退回日期。 | `goods_receipt_note.date` |
| `items[].receiptCategory` | Integer | 進貨單類別 code。 | 進貨單 `0`、進貨退回 `1` |
| `items[].itemNo` | String | 進貨交易品項 no。 | `goods_receipt_note.item_no` |
| `items[].itemName` | String | 進貨交易品項名稱。 | `goods_receipt_note.item_name` |
| `items[].checkedQuantity` | Float | 本張進貨單實際數量，取至小數點第 2 位。 | `goods_receipt_note.checkedCount` |
| `items[].cumulativeReceivedQuantity` | Float | 該採購單截至本筆日期的收貨淨值。 | 同採購單按日期累計 `checkedCount`，退回扣除 |
| `items[].acceptanceStatusCode` | String | 收貨處理狀態；第一版不假造 Quality 結果。 | `received`、`returned`、`unknown` |
| `items[].qualityStatusCode` | String | 品檢／文件狀態。 | `deferred`、`unknown` |
| `items[].warehouseStatusCode` | String | 倉庫交接狀態。 | `pending_putaway`、`stocked`、`unknown` |
| `items[].nextOwnerDepartment` | Integer | 已確認 workflow 的下一步負責部門 code。 | `workflow_task_state.ownerDepartment` |

`summary` 包含 `receiptCount`、`pendingQualityCount` 與 `pendingPutawayCount`。其中品檢數量在 Quality schema 未完成時不得宣稱為實際品檢結果，只能表示資料延期或未知。

## 8. GET `/api/v2/purchasing/suppliers/dashboard`

以 `purchase_order.date` 篩選任意歷史區間，依供應商彙總：

| Field Path | Type | Description | Source |
|---|---|---|---|
| `items[].supplierNo` | String | 供應商 company no。 | `purchase_order.item_ref_no` |
| `items[].supplierName` | String | 供應商名稱。 | `company.displayName` |
| `items[].purchaseOrderCount` | Integer | 查詢期間採購單數。 | `purchase_order` |
| `items[].openPurchaseOrderCount` | Integer | 尚有未收數量的採購單數。 | PO 與進貨單數量計算 |
| `items[].latePurchaseOrderCount` | Integer | 逾期且尚未收足的採購單數。 | `purchase_order.expectedDate` |
| `items[].purchaseAmount` | Integer | 採購金額加總，四捨五入取整數。 | `purchase_order.amount` |
| `items[].pendingReceiptQuantity` | Float | 尚未收貨淨數量，取至小數點第 2 位。 | PO 數量減進貨淨數量 |
| `items[].riskLevel` | String | 供應商彙總風險 code。 | `normal`、`notice`、`high_risk`、`unknown` |

## 9. GET `/api/v2/purchasing/purchase-orders/{purchase_order_no}/detail`

回傳單一採購單及其正式關聯：

```json
{
  "purchaseOrder": {},
  "purchaseRequest": null,
  "supplier": {},
  "receipts": [],
  "source": {},
  "inventory": {},
  "workflow": [],
  "relatedDocuments": {}
}
```

- `purchaseOrder` 取自 `purchase_order`，包含數量、單價、金額、預計進貨日與原始備註。
- `purchaseRequest` 以 `purchase_order.purchase_request_no` 查詢；無關聯時為 `null`，不可依品號自行補接。
- `supplier` 以 `purchase_order.item_ref_no` 對應 `company`。
- `receipts[]` 以 `goods_receipt_note.purchase_order_no` 查詢，依日期與 no 排序。
- `source` 僅回傳已確認的 `purchase_request.product_order_no` 與正式 workflow／APS 關聯。
- `inventory` 重用 Warehouse inventory snapshot calculator；不複製庫存補算邏輯。
- `workflow[]` 只回傳正式可追溯的 `workflow_task_state`／`workflow_task_event` 關聯。
- `relatedDocuments` 僅取 `quotation.category = 1`、`contract.category = 1` 且可由 `ref_no` 對應的採購資料；不推測有效期限或核准狀態。

## 10. 前端責任

1. 將所有 enum code 轉換成繁中、英文及其他語系，不依賴後端回傳 UI 中文字串。
2. 由前端保存 `startDate`、`endDate`、篩選條件與目前 view，組合 API query string。
3. 使用 `purchaseOrderNo` 導向 detail API，不自行推導採購單、請購單、進貨單或工單關聯。
4. 對 `deferred`、`unknown`、空陣列與資料關聯缺口呈現可辨識狀態，不以 mock 或推測值代替。

## 11. 工程師需確認

| 項目 | 提案內容 | 需確認事項 |
|---|---|---|
| 任意歷史區間 | `startDate`／`endDate`，不固定 7d／30d | 現有日期欄位與索引是否足以支援歷史查詢？ |
| 品項類別 | 由 item no 追溯正式料品主檔 | `purchase_order.item_no -> trans_items -> material/inproduct/product` 的實際 mapping 是否固定？ |
| 請購關聯 | `purchase_order.purchase_request_no` 為唯一直接關聯 | 若欄位為空，是否存在其他已確認的正式關聯？ |
| 收貨數量 | checkedCount 依進貨／退回加減 | 進貨退回是否一律扣除 `checkedCount`？ |
| 預計到貨 | 使用 `purchase_order.expectedDate` | 是否有分批進貨的未來到貨日期欄位；若沒有，畫面顯示 PO expectedDate？ |
| 品檢狀態 | 第一版 `deferred`／`unknown` | Quality 延後時是否接受不顯示實際品檢結果？ |
| 入庫狀態 | inventory／workflow evidence | 是否已有正式事件或任務可判斷 `pending_putaway` 與 `stocked`？ |
| 來源影響 | 只接受正式工單／訂單關聯 | APS／工單關聯來源欄位與優先順序為何？ |
| 供應商彙總 | 依 company no 聚合 | 同一供應商是否允許不同 company 顯示名稱，應以哪一筆為準？ |

## 12. 非本次範圍

- 不實作 POST／PUT／DELETE。
- 不新增資料表或欄位。
- 不設計 Quality inspection API；Quality Center 延至下一版。
- 不推導供應商評分、替代供應商推薦、APS shortage 演算法或付款完成狀態。
