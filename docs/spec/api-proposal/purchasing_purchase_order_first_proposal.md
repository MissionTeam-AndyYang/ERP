# 工程師提問
1. 請檢視所有 API 回傳欄位是否符合目前畫面規劃設計需求，若有不必要的欄位，請先暫時移除。
2. 請檢視所有 API 的 Success Response Data 與 Field Description 是否完整齊全，若有缺漏請補全。
3. 針對 /api/v2/purchasing/purchase-orders/dashboard
   - 請詳細說明 linkedWorkOrderNo 欄位的涵義，並指出其顯示於畫面的具體位置。
   - 由於一張採購單可能對應多張進貨單，請說明 receivingStatusCode、warehouseStatusCode 欄位在此情境下應如何處理；品檢狀態第一版不納入。


# 採購中心採購單主視角 API 提案

> Status: Proposal / Pending Engineer Review  
> Screen: `PurchasingWorkspaceScreen`  
> Route: `/purchasing`  
> Scope: V1 Core、read-only  
> Design Basis: `purchasing_purchase_order_first_static_preview.html`

## 1. 畫面定位

本版以 `purchase_order` 為採購中心的主要資料列，支援管理者與採購主管查詢任意歷史日期區間，並從採購單追蹤供應商、預計到貨、分批進貨、驗收、入庫交接與來源影響。品檢狀態不在 V1 API 處理範圍。

`purchase_request` 僅作為輔助關聯：採購單已連結請購單時顯示來源；未連結時明確顯示資料缺口，不反向推測請購來源。

第一版只提供查詢、篩選、排序、分頁與 detail drill-down，不執行建立或修改採購單、請購單、進貨單、驗收、入庫或付款。

## 2. 任意歷史區間

所有列表 API 支援 `startDate` 與 `endDate`，格式為 `YYYY-MM-DD`。前端送出使用者所在時區的 local date，並以 HTTP header `x-timezone` 指定日期邊界時區；後端再將日期邊界轉成 UTC timestamp 查詢。查詢區間不採用固定 `today`、`7d` 或 `30d` 限制；只要資料仍在系統保存範圍內，即可查詢任意歷史期間。

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
| `supplierNo` | String | No | 供應商 `company.no`。 |
| `itemCategory` | Integer | No | 料品品項類別 code；前端轉換多國語系。 |
| `riskLevel` | String | No | 風險等級 code。 |
| `keyword` | String | No | 採購單 no、進貨單 no、請購單 no、供應商 no／名稱、料號或品名。 |
| `start` | Integer | No | 分頁起點，預設 0。 |
| `count` | Integer | No | 回傳筆數，預設 50，最大 100。 |

日期篩選欄位依 API 固定定義：採購單 API 使用 `purchase_order.date`；進貨單 API 使用 `goods_receipt_note.date`；供應商彙總使用 `purchase_order.date`。

### 4.1 Request Header

| Header | Type | Required | Description |
|---|---|---:|---|
| `x-timezone` | String | Yes | 前端使用的 IANA timezone，例如 `Asia/Taipei`；`startDate` 與 `endDate` 以此時區解讀，資料庫查詢使用轉換後的 UTC timestamp。 |

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
| `items[].itemCategory` | Integer | 料品品項類別 code；依已確認的 item no mapping 追溯正式料品主檔，不使用不存在於交易單據的欄位。 | `purchase_order.item_no -> trans_items -> material/inproduct/product` |
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
| `items[].linkedWorkOrderNo` | String | 已確認且可追溯的生產工單 no；無正式關聯時為空字串。顯示於採購單清單的「來源影響」欄、交期風險清單的「影響來源」欄及明細 panel 的來源區塊。 | 僅取已確認 workflow／APS 關聯 |
| `items[].receivingStatusCode` | String | 以同一採購單全部進貨單的 `checkedCount` 淨值彙總收貨狀態；不是單一進貨單狀態。 | `not_arrived`、`partial`、`received`、`returned`、`unknown` |
| `items[].warehouseStatusCode` | String | 以 workflow 入庫任務作為流程狀態主要依據，並以 Warehouse inventory 作為實際庫存證據；同一 PO 多筆進貨只要仍有未完成入庫交接即回傳 `pending_putaway`。 | `not_received`、`pending_putaway`、`stocked`、`unknown` |
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
| `items[].acceptanceStatusCode` | String | 收貨處理狀態；第一版不包含品檢狀態。 | `received`、`returned`、`unknown` |
| `items[].warehouseStatusCode` | String | 倉庫交接狀態。 | `pending_putaway`、`stocked`、`unknown` |
| `items[].nextOwnerDepartment` | Integer | 已確認 workflow 的下一步負責部門 code。 | `workflow_task_state.ownerDepartment` |

`summary` 包含 `receiptCount` 與 `pendingPutawayCount`；V1 不回傳 `pendingQualityCount`，也不處理品檢狀態。

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

| 項目 | 提案內容 | 需確認事項 | 工程師回覆 |
|---|---|---|---|
| 任意歷史區間 | `startDate`／`endDate`，不固定 7d／30d | 日期由前端送 local time 還是 UTC time？ | 前端送 local `YYYY-MM-DD`，並以 `x-timezone` header 指定 IANA timezone；後端依 header 將邊界轉成 UTC timestamp。 |
| 品項類別 | 由 item no 追溯正式料品主檔 | `purchase_order.item_no -> trans_items -> material/inproduct/product` 的實際 mapping 是否固定？ | 是；依此 mapping 實作。 |
| 請購關聯 | `purchase_order.purchase_request_no` 為唯一直接關聯 | 若欄位為空，是否存在其他已確認的正式關聯？ | 目前沒有；欄位為空即回傳 `unlinked`，不得推測。 |
| 收貨數量 | checkedCount 依進貨／退回加減 | 進貨退回是否一律扣除 `checkedCount`？ | 是；`category=1` 一律扣除。 |
| 預計到貨 | 使用 `purchase_order.expectedDate` | 是否有分批進貨的未來到貨日期欄位；若沒有，畫面顯示 PO expectedDate？ | 預覽仍包含預計到貨欄位；V1 使用 PO `expectedDate`，不推導分批進貨未來日期。 |
| 品檢狀態 | 第一版不提供品質欄位 | Quality 延後時是否接受不顯示實際品檢結果？ | V1 完全不納入品檢狀態欄位與 KPI；Quality 後續版本再規劃。 |
| 入庫狀態 | workflow／inventory evidence | 是否已有正式事件或任務可判斷 `pending_putaway` 與 `stocked`？ | V1 以 workflow 入庫任務的狀態作為流程判斷，Warehouse inventory 作為已實際入庫的證據；若兩者無法對應則回傳 `unknown`。 |
| 來源影響 | 只接受正式工單／訂單關聯 | APS／工單關聯來源欄位與優先順序為何？ | 「來源影響」指畫面上的來源訂單／工單欄位：先取 `purchase_request.product_order_no` 作為 `sourceOrderNo`；`linkedWorkOrderNo` 僅取已確認 workflow／APS 關聯，不相似推測。 |
| 供應商彙總 | 依 company no 聚合 | 同一供應商是否允許不同 company 顯示名稱，應以哪一筆為準？ | 供應商與 company 一對一，以 `company.no` 與 `company.displayName` 為準。 |

## 12. 工程師回覆後確認結論

1. 日期查詢使用前端 local date + `x-timezone`，後端轉 UTC timestamp；不新增 timezone query parameter。
2. 品項 mapping、請購關聯與進貨退回扣除規則已確認，依文件演算法執行。
3. 預計到貨欄位保留，V1 來源固定為 `purchase_order.expectedDate`。
4. V1 移除所有品檢狀態與品檢 KPI，避免回傳未實作的 Quality 資料。
5. 入庫狀態以 workflow 為流程主來源、inventory 為實際結果證據；多筆進貨以 PO 層級彙總。
6. 目前沒有資料保存政策限制；本文件所稱資料保存政策，是指未來若因法規、備份、封存或刪除策略導致歷史資料不可查詢時，需另定義標準錯誤。V1 不自行縮短使用者指定的查詢期間。

## 13. 非本次範圍

- 不實作 POST／PUT／DELETE。
- 不新增資料表或欄位。
- 不設計 Quality inspection API；Quality Center 延至下一版。
- 不推導供應商評分、替代供應商推薦、APS shortage 演算法或付款完成狀態。
