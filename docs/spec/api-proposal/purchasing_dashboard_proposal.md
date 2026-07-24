# Purchasing Dashboard API 提案

> Status: Superseded by `purchasing_purchase_order_first_proposal.md`; retained for historical reference
> Screen: `PurchasingWorkspaceScreen`  
> Route: `/purchasing`  
> Scope: V1 Core、read-only

## 1. 畫面定位

`PurchasingWorkspaceScreen` 用於管理者與採購主管掌握「訂單／生產需求是否已轉成採購、供應商交期是否影響生產、到貨是否完成驗收與入庫」。第一版優先提供：

1. 採購需求與請購單、採購單、進貨單的關聯進度。
2. 低庫存、缺料、未下採購單、預計到貨逾期等風險。
3. 到貨、驗收與入庫的目前狀態。
4. 供應商報價、採購合約與交期追蹤資訊。

第一版只提供查詢、篩選、排序、分頁與 detail drill-down；不執行建立請購單、建立採購單、修改交期、驗收、入庫或付款等 mutation。

## 2. API 清單

| API | Method | 用途 | Status |
|---|---|---|---|
| `/api/v2/purchasing/dashboard` | GET | 回傳採購 KPI、採購需求列、交期／到貨／供應商風險 | Proposal / Pending Engineer Review |
| `/api/v2/purchasing/requests/{purchase_request_no}/detail` | GET | 回傳單一請購需求的採購、到貨、庫存、來源與 workflow 明細 | Proposal / Pending Engineer Review |

## 3. GET `/api/v2/purchasing/dashboard`

### 3.1 Query Parameters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `date` | Integer | No | 查詢基準時間，UTC timestamp；未提供時使用目前時間。 |
| `period` | String | No | 查詢期間；支援 `today`、`7d`、`30d`，預設 `30d`。以查詢基準日當天起算並往後涵蓋連續曆日。 |
| `timezone` | String | No | 日期分組時區，例如 `Asia/Taipei`。 |
| `item_category` | Integer | No | 料品品項類別 code；前端負責多國語系轉換。 |
| `supplier_no` | String | No | 供應商 company no。 |
| `stage` | String | No | 採購流程階段 code。 |
| `risk_only` | Boolean | No | 只回傳有風險的採購需求列。 |
| `keyword` | String | No | 以請購單 no、採購單 no、料號、品名、供應商 no 或供應商名稱查詢。 |
| `start` | Integer | No | `items[]` 分頁起點，預設 0。 |
| `count` | Integer | No | `items[]` 回傳筆數，預設 50，最大 100。 |

### 3.2 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "timezone": "String",
  "range": {
    "period": "String",
    "startTimestamp": "Integer",
    "endTimestamp": "Integer"
  },
  "summary": {
    "openPurchaseRequestCount": "Integer",
    "openPurchaseOrderCount": "Integer",
    "lateArrivalCount": "Integer",
    "receivingPendingCount": "Integer",
    "supplierQuotePendingCount": "Integer",
    "contractMissingCount": "Integer",
    "purchaseAmount": "Integer"
  },
  "items": [
    {
      "purchaseRequestNo": "String",
      "purchaseOrderNo": "String",
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "unit": "Integer",
      "requestedQuantity": "Float",
      "orderedQuantity": "Float",
      "receivedQuantity": "Float",
      "purchaseAmount": "Integer",
      "supplierNo": "String",
      "supplierName": "String",
      "requiredTimestamp": "Integer",
      "expectedArrivalTimestamp": "Integer",
      "stageCode": "String",
      "riskLevel": "String",
      "riskCode": "String",
      "sourceOrderNo": "String",
      "linkedWorkOrderNo": "String",
      "currentQuantity": "Float",
      "reservedQuantity": "Float",
      "availableQuantity": "Float",
      "safetyStock": "Float",
      "receivingStatusCode": "String",
      "qualityStatusCode": "String",
      "warehouseStatusCode": "String",
      "ownerDepartment": "Integer"
    }
  ],
  "total": "Integer",
  "start": "Integer",
  "count": "Integer"
}
```

### 3.3 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `serverTimestamp` | Integer | Response 建立時間，UTC timestamp。 |  |
| `timezone` | String | 本次日期分組使用的 IANA timezone。 |  |
| `range.period` | String | 實際採用的查詢期間。 | `today`、`7d`、`30d` |
| `range.startTimestamp` | Integer | 查詢基準日當地時間 00:00:00 的 UTC timestamp。 |  |
| `range.endTimestamp` | Integer | 查詢期間最後一日 23:59:59 的 UTC timestamp。 |  |
| `summary.openPurchaseRequestCount` | Integer | 查詢期間內仍有未完成採購需求的請購單需求數；依 `purchase_request` 與已訂／已收數量判斷。 |  |
| `summary.openPurchaseOrderCount` | Integer | 仍有未完成到貨數量的採購單需求數。 |  |
| `summary.lateArrivalCount` | Integer | `expectedDate` 已過查詢基準時間，且實際收貨數量尚未達應收數量的需求數。 |  |
| `summary.receivingPendingCount` | Integer | 已有進貨單但仍未完成實際收貨或入庫確認的需求數。 |  |
| `summary.supplierQuotePendingCount` | Integer | 找不到可對應的採購類別報價資料的需求數；目前不推測報價的有效期限或核准狀態。 | `quotation.category = 1`；有效性規則待工程師確認 |
| `summary.contractMissingCount` | Integer | 找不到可對應的採購類別合約的需求數；目前不推測合約的有效期限或核准狀態。 | `contract.category = 1`；有效性規則待工程師確認 |
| `summary.purchaseAmount` | Integer | 查詢結果採購金額加總；四捨五入取整數。 | `purchase_order.amount` 優先，尚未下單時不計入。 |
| `items[]` | Array | 採購需求列；依 `requiredTimestamp` ASC、`purchaseRequestNo` ASC 排序並於 DB 端分頁。 |  |
| `items[].purchaseRequestNo` | String | 請購單 no。 | `purchase_request.no` |
| `items[].purchaseOrderNo` | String | 採購單 no；尚未下單時為空字串。 | `purchase_order.no` |
| `items[].itemNo` | String | 採購料品 no。 | `purchase_request.item_no` 或 `purchase_order.item_no` |
| `items[].itemName` | String | 採購料品名稱。 | 正式料品主檔或來源單據名稱欄位 |
| `items[].itemCategory` | Integer | 料品品項類別 code；依 `itemNo` 追溯正式料品主檔，不以交易單據中不存在的欄位補值。 | 請購原料／物料／膠捲以 `material.category` 為基準；採購單／進貨單的 `item_no` 透過 `trans_items` 追溯正式料品主檔；具體跨主檔對應待工程師確認 |
| `items[].unit` | Integer | 採購數量單位 code。 | `purchase_request.unit` 或 `purchase_order.unit` |
| `items[].requestedQuantity` | Float | 請購數量，取至小數點第 2 位。 | `purchase_request.count` |
| `items[].orderedQuantity` | Float | 已轉採購單數量，取至小數點第 2 位。 | `purchase_order.count`；無採購單為 0 |
| `items[].receivedQuantity` | Float | 已進貨實際數量，取至小數點第 2 位。 | 關聯 `goods_receipt_note.checkedCount` 加總 |
| `items[].purchaseAmount` | Integer | 採購金額；四捨五入取整數。 | `purchase_order.amount` |
| `items[].supplierNo` | String | 供應商 company no。 | `purchase_order.item_ref_no` 或 `goods_receipt_note.item_ref_no` |
| `items[].supplierName` | String | 供應商顯示名稱。 | `company.displayName` |
| `items[].requiredTimestamp` | Integer | 需求／預期到貨時間，UTC timestamp。 | `purchase_request.expectedDate`，無請購單時使用採購單 `expectedDate` |
| `items[].expectedArrivalTimestamp` | Integer | 採購單預計進貨時間；未下單時為 0。 | `purchase_order.expectedDate` |
| `items[].stageCode` | String | 採購流程階段 code，由請購、採購、進貨資料與 workflow 狀態推導。 | `request_pending`、`quote_pending`、`ordered`、`arrival_pending`、`receiving`、`stocked`、`unknown` |
| `items[].riskLevel` | String | 風險等級 code。 | `normal`、`notice`、`high_risk`、`unknown` |
| `items[].riskCode` | String | 主要風險代碼；前端依 code 轉換多國語系文字。 | `stock_below_safety`、`purchase_request_open`、`purchase_order_missing`、`late_arrival`、`supplier_quote_missing`、`contract_missing`、`receiving_pending`、`workflow_blocked`、`unknown` |
| `items[].sourceOrderNo` | String | 需求來源訂單 no。 | `purchase_request.product_order_no` |
| `items[].linkedWorkOrderNo` | String | 關聯生產工單 no；無正式關聯時為空字串。 | 只取已確認的 workflow／APS 關聯，不自行推測。 |
| `items[].currentQuantity` | Float | 目前庫存數量，取至小數點第 2 位。 | 共用 Warehouse inventory snapshot calculator |
| `items[].reservedQuantity` | Float | 預留數量，取至小數點第 2 位。 | Warehouse reservation snapshot |
| `items[].availableQuantity` | Float | 可用庫存數量，取至小數點第 2 位。 | 共用 Warehouse inventory snapshot calculator |
| `items[].safetyStock` | Float | 安全水位，取至小數點第 2 位。 | `item_safety_stock` |
| `items[].receivingStatusCode` | String | 到貨／收貨狀態 code。 | `not_arrived`、`partial`、`received`、`returned`、`unknown` |
| `items[].qualityStatusCode` | String | 品檢文件狀態 code；第一版尚無正式 Quality inspection schema 時不得假造結果。 | `deferred`、`available`、`unknown` |
| `items[].warehouseStatusCode` | String | 入庫狀態 code。 | `not_received`、`pending_putaway`、`stocked`、`unknown` |
| `items[].ownerDepartment` | Integer | 目前 workflow 下一步負責部門 code。 | `workflow_task_state.ownerDepartment` |
| `total` | Integer | 套用篩選條件後的需求列總筆數。 |  |
| `start` | Integer | 本次分頁起點。 |  |
| `count` | Integer | 本次回傳需求列筆數。 |  |

## 4. GET `/api/v2/purchasing/requests/{purchase_request_no}/detail`

### 4.1 Success Response Data

```json
{
  "request": {
    "purchaseRequestNo": "String",
    "sourceOrderNo": "String",
    "itemNo": "String",
    "itemName": "String",
    "itemCategory": "Integer",
    "unit": "Integer",
    "requestedQuantity": "Float",
    "requiredTimestamp": "Integer",
    "comment": "String"
  },
  "purchaseOrders": [],
  "receipts": [],
  "inventory": {
    "currentQuantity": "Float",
    "reservedQuantity": "Float",
    "availableQuantity": "Float",
    "safetyStock": "Float"
  },
  "supplier": {
    "supplierNo": "String",
    "supplierName": "String",
    "quoteNo": "String",
    "contractNo": "String",
    "quotePrice": "Float",
    "contractPrice": "Float"
  },
  "workflow": [],
  "relatedDocuments": []
}
```

`purchaseOrders[]`、`receipts[]`、`workflow[]` 與 `relatedDocuments[]` 只回傳正式存在且可由 foreign key 或已確認 `refCategory/ref_no/ref_sub_no` 追溯的資料；不存在時回傳空陣列，不建立虛構的採購、進貨或 Quality 文件。

## 5. 前端責任

1. 將 `stageCode`、`riskLevel`、`riskCode`、`receivingStatusCode`、`qualityStatusCode`、`warehouseStatusCode`、`ownerDepartment` 與 item enum code 轉換為繁中、英文及其他語系。
2. 依 `riskCode` 選擇色彩、圖示與篩選狀態；後端不回傳 UI 專用中文 `riskReason`。
3. 依 `purchaseRequestNo` 組合 detail API path；前端不自行推導供應商、採購單或進貨單關聯。
4. 空資料、部分資料與 API 錯誤須呈現可辨識狀態，不以 mock 資料冒充正式 API 結果。

## 6. 工程師需確認

| 項目 | 目前提案 | 需確認內容 |
|---|---|---|
| 供應商報價與合約 | `quotation.category = 1`、`contract.category = 1` | 是否以 `item_ref_no` 對應 `company.no`，並以 `quotation.ref_no` 對應 `contract.ref_no`？ |
| 採購單狀態 | `purchase_order` 無 status 欄位 | 是否採用 `workflow_task_state.taskType = 2` 的人工任務狀態判斷採購完成／阻塞？ |
| 進貨數量 | `goods_receipt_note.checkedCount` | 同一採購單多筆進貨單是否直接加總 `checkedCount`，進貨退回 `category = 1` 是否扣除？ |
| 入庫狀態 | Warehouse inventory snapshot | 是否有正式進貨到入庫的關聯欄位或任務 event 可判斷 `pending_putaway`？ |
| 品檢文件 | 第一版回傳 `deferred`／`unknown` | Quality 畫面延至下一版時，採購畫面是否暫不顯示品檢文件細節？ |
| 生產需求關聯 | `product_order_no` 與已確認 workflow 關聯 | 是否存在可直接對應 `work_order_no` 的 APS／請購來源欄位？未確認前不推導。 |
| 庫存快照 | 重用 Warehouse snapshot calculator | 是否允許 Purchasing API 直接重用既有物件，或需抽取到共用 service facade？ |

## 7. 非本次範圍

- 不設計 `POST`、`PUT`、`DELETE` 採購、請購、進貨、驗收或入庫 API。
- 不在本版新增採購或 Quality DB Schema；若工程師確認現有 schema 不足，另開 DB extension proposal。
- 不推導不存在的供應商評分、替代供應商推薦、APS shortage algorithm 或付款完成狀態。
