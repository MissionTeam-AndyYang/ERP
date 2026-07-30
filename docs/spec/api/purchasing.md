# Purchasing API Group

> Source: `restserver/package/restserver/api/v2/purchasing_uri.py`
> Proposal Source: `docs/spec/api-proposal/purchasing_purchase_order_first_proposal.md`
> Flow Source: `docs/spec/api-proposal/purchasing_purchase_order_first_flow_algorithm.md`

## API Summary

| URL | Method | Description | Status | Review Note |
|---|---|---|---|---|
| [/api/v2/purchasing/purchase-orders/dashboard](#get-api-v2-purchasing-purchase-orders-dashboard) | GET | 查詢採購單、收貨進度、請購關聯與交期風險總覽。 | OK | 第一版 read-only。 |
| [/api/v2/purchasing/purchase-orders/delivery-risk](#get-api-v2-purchasing-purchase-orders-delivery-risk) | GET | 查詢非正常風險的採購單。 | OK | 風險等級由 `riskLevel` 整數表示，風險原因由 `riskType` 表示。 |
| [/api/v2/purchasing/goods-receipts/dashboard](#get-api-v2-purchasing-goods-receipts-dashboard) | GET | 查詢進貨單與後續入庫交接狀態。 | OK | 第一版 read-only；尚未推導倉庫實際入庫狀態。 |
| [/api/v2/purchasing/suppliers/dashboard](#get-api-v2-purchasing-suppliers-dashboard) | GET | 依供應商彙總採購單與待收貨資訊。 | OK | 彙總範圍依查詢條件取得的採購單資料。 |
| [/api/v2/purchasing/purchase-orders/{purchase_order_no}/detail](#get-api-v2-purchasing-purchase-orders-purchase_order_no-detail) | GET | 查詢單一採購單及其請購、進貨與關聯文件明細。 | OK | 第一版 read-only。 |

## GET /api/v2/purchasing/purchase-orders/dashboard

<a id="get-api-v2-purchasing-purchase-orders-dashboard"></a>

### Basic Information

| URL | Method | Description |
|---|---|---|
| `/api/v2/purchasing/purchase-orders/dashboard` | GET | 查詢指定日期區間的採購單總覽。 |

### Request Header

| Header | Description |
|---|---|
| x-auth-token | 存取金鑰。 |
| x-timezone | 時區代碼，例如 `Asia/Taipei`；未提供時使用系統預設值。 |

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| startDate | String | YES | 查詢起始日，格式 `YYYY-MM-DD`；依 `x-timezone` 解讀。 |
| endDate | String | YES | 查詢結束日，格式 `YYYY-MM-DD`；包含當日且不得早於 `startDate`。 |
| keyword | String | NO | 搜尋採購單號、料品編號或料品名稱。 |
| supplierNo | String | NO | 供應商編號，對應 `company.no`。 |
| riskLevel | Integer | NO | 風險等級篩選；`0` normal、`1` notice、`3` high risk。 |
| start | Integer | NO | 分頁起始位置，預設 `0`。 |
| count | Integer | NO | 分頁筆數，預設 `50`，上限 `100`。 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "timezone": "String",
    "range": {"startDate": "String", "endDate": "String", "startTimestamp": "Integer", "endTimestamp": "Integer"},
    "summary": {"openPurchaseOrderCount": "Integer", "lateOrDueTodayCount": "Integer", "purchaseAmount": "Integer", "unlinkedPurchaseRequestCount": "Integer"},
    "items": [{
      "purchaseOrderNo": "String", "purchaseDateTimestamp": "Integer", "itemNo": "String", "itemName": "String", "unit": "Integer",
      "supplierNo": "String", "supplierName": "String", "orderedCount": "Float", "receivedCount": "Float", "openCount": "Float",
      "unitPrice": "Float", "purchaseAmount": "Integer", "expectedArrivalTimestamp": "Integer", "purchaseRequestNo": "String",
      "purchaseRequestLinkStatusCode": "String", "sourceOrderNo": "String", "linkedWorkOrderNo": "String", "warehouseStatusCode": "String",
      "riskLevel": "Integer", "riskType": "String"
    }],
    "total": "Integer", "start": "Integer", "count": "Integer"
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|---|---|---|---|
| `payload.serverTimestamp` | Integer | API 回應產生時的 UTC timestamp。 | Unix timestamp。 |
| `payload.timezone` | String | 本次日期區間採用的時區。 | IANA timezone。 |
| `payload.range` | Object | 查詢日期及其 UTC 轉換結果。 | `startDate`、`endDate`、`startTimestamp`、`endTimestamp`。 |
| `payload.summary` | Object | 本次查詢範圍內的採購單彙總。 | 見下列欄位。 |
| `payload.summary.openPurchaseOrderCount` | Integer | 尚有未收貨數量的採購單筆數。 | `openCount > 0`。 |
| `payload.summary.lateOrDueTodayCount` | Integer | 風險類型為逾期或今日到期的採購單筆數。 | `late_arrival` 或 `due_today`。 |
| `payload.summary.purchaseAmount` | Integer | 查詢範圍內採購金額合計。 | 金額四捨五入取整數。 |
| `payload.summary.unlinkedPurchaseRequestCount` | Integer | 請購單未成功關聯的採購單筆數。 | link status 非 `linked`。 |
| `payload.items[]` | Array | 採購單明細；此節點不另列說明。 | 依預計到貨日及採購單號排序。 |
| `payload.items[].purchaseOrderNo` | String | 採購單編號。 | `purchase_order.no`。 |
| `payload.items[].purchaseDateTimestamp` | Integer | 採購單建立時間。 | Unix timestamp。 |
| `payload.items[].itemNo` | String | 採購料品編號。 | `purchase_order.item_no`。 |
| `payload.items[].itemName` | String | 採購料品名稱。 | `purchase_order.item_name`。 |
| `payload.items[].unit` | Integer | 料品庫存單位代碼。 | 前端轉換顯示文字。 |
| `payload.items[].supplierNo` | String | 供應商編號。 | `purchase_order.item_ref_no`。 |
| `payload.items[].supplierName` | String | 供應商名稱。 | 取 `company.displayName`。 |
| `payload.items[].orderedCount` | Float | 採購數量。 | 數量取小數點後 2 位。 |
| `payload.items[].receivedCount` | Float | 進貨單已檢收數量合計。 | 進貨加總、退貨扣除。 |
| `payload.items[].openCount` | Float | 尚未完成收貨的數量。 | `max(orderedCount - receivedCount, 0)`。 |
| `payload.items[].unitPrice` | Float | 採購單價。 | 小數點後 4 位。 |
| `payload.items[].purchaseAmount` | Integer | 採購金額。 | 四捨五入取整數。 |
| `payload.items[].expectedArrivalTimestamp` | Integer | 預計到貨時間。 | Unix timestamp。 |
| `payload.items[].purchaseRequestNo` | String | 關聯請購單編號。 | 無關聯時為空字串。 |
| `payload.items[].purchaseRequestLinkStatusCode` | String | 請購單關聯狀態。 | `linked`、`unlinked`、`invalid`。 |
| `payload.items[].sourceOrderNo` | String | 請購單所來源的訂單編號。 | 無關聯時為空字串。 |
| `payload.items[].linkedWorkOrderNo` | String | 關聯工單編號。 | 第一版尚未推導，固定為空字串。 |
| `payload.items[].warehouseStatusCode` | String | 採購單對應的倉儲入庫交接狀態。 | `not_received`、`pending_putaway`、`stocked`、`unknown`。 |
| `payload.items[].riskLevel` | Integer | 採購交期風險等級。 | `0` normal、`1` notice、`3` high risk。 |
| `payload.items[].riskType` | String | 採購交期風險原因。 | `normal`、`late_arrival`、`due_today`、`purchase_request_unlinked`、`open_receipt`。 |
| `payload.total` | Integer | 符合條件的資料總筆數。 | 分頁前。 |
| `payload.start` | Integer | 實際分頁起始位置。 | 最小為 `0`。 |
| `payload.count` | Integer | 本次回傳筆數。 | 不超過 `100`。 |

### Failed Response Data

`startDate` 或 `endDate` 缺少、格式無效或資料不存在時，回傳 HTTP `400`、`code=1`。

### Processing Flow

1. 讀取日期區間、時區、關鍵字、供應商與分頁參數。
2. 將本地日期區間轉換為 UTC timestamp。
3. 查詢日期範圍內的 `purchase_order`，並依條件排序。
4. 批次查詢關聯 `goods_receipt_note`，計算已收貨與未收貨數量。
5. 依預計到貨日、未收貨數量及請購關聯狀態計算 `riskLevel` 與 `riskType`。
6. 計算 summary，最後套用分頁並回傳。

### Database Tables Used

| Table | Purpose |
|---|---|
| purchase_order | 採購單基本資料、數量、金額與預計到貨日。 |
| goods_receipt_note | 進貨及退貨數量。 |
| company | 供應商名稱。 |
| purchase_request | 請購單關聯與來源訂單。 |

## GET /api/v2/purchasing/purchase-orders/delivery-risk

<a id="get-api-v2-purchasing-purchase-orders-delivery-risk"></a>

### Basic Information

| URL | Method | Description |
|---|---|---|
| `/api/v2/purchasing/purchase-orders/delivery-risk` | GET | 查詢採購單交期風險。 |

### Request Header

| Header | Description |
|---|---|
| x-auth-token | 存取金鑰。 |
| x-timezone | 時區代碼，例如 `Asia/Taipei`；未提供時使用系統預設值。 |

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| startDate | String | YES | 查詢起始日，格式 `YYYY-MM-DD`；依 `x-timezone` 解讀。 |
| endDate | String | YES | 查詢結束日，格式 `YYYY-MM-DD`；包含當日且不得早於 `startDate`。 |
| keyword | String | NO | 搜尋採購單號、料品編號或料品名稱。 |
| supplierNo | String | NO | 供應商編號，對應 `company.no`。 |
| riskLevel | Integer | NO | 風險等級篩選；此 API 僅回傳非 `0` 的風險資料。 |
| start | Integer | NO | 分頁起始位置，預設 `0`。 |
| count | Integer | NO | 分頁筆數，預設 `50`，上限 `100`。 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer", "timezone": "String", "range": "Object",
    "summary": {
      "highRiskCount": "Integer", "noticeCount": "Integer", "lateCount": "Integer",
      "affectedWorkOrderCount": "Integer", "averageLateDays": "Float"
    },
    "items": [{
      "purchaseOrderNo": "String", "purchaseDateTimestamp": "Integer", "itemNo": "String",
      "itemName": "String", "unit": "Integer", "supplierNo": "String", "supplierName": "String",
      "orderedCount": "Float", "receivedCount": "Float", "shortageCount": "Float",
      "unitPrice": "Float", "purchaseAmount": "Integer", "expectedArrivalTimestamp": "Integer",
      "purchaseRequestNo": "String", "purchaseRequestLinkStatusCode": "String",
      "sourceOrderNo": "String", "linkedWorkOrderNo": "String", "warehouseStatusCode": "String",
      "riskLevel": "Integer", "riskType": "String", "shortageValue": "Integer",
      "impactSourceType": "String", "impactSourceNo": "String", "followUpCode": "String"
    }],
    "total": "Integer", "start": "Integer", "count": "Integer"
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|---|---|---|---|
| `payload.summary.highRiskCount` | Integer | 高風險採購單筆數。 | `riskLevel=3`。 |
| `payload.summary.noticeCount` | Integer | 注意風險採購單筆數。 | `riskLevel=1`。 |
| `payload.summary.lateCount` | Integer | 已逾期採購單筆數。 | `riskType=late_arrival`。 |
| `payload.summary.affectedWorkOrderCount` | Integer | 受影響工單筆數。 | 第一版固定為 `0`。 |
| `payload.summary.averageLateDays` | Float | 平均逾期天數。 | 第一版固定為 `0.0`。 |
| `payload.items[].purchaseOrderNo` | String | 採購單編號。 | 同採購單總覽。 |
| `payload.items[].purchaseDateTimestamp` | Integer | 採購單建立時間。 | Unix timestamp。 |
| `payload.items[].itemNo` | String | 採購料品編號。 |  |
| `payload.items[].itemName` | String | 採購料品名稱。 |  |
| `payload.items[].unit` | Integer | 料品庫存單位代碼。 | 前端轉換顯示文字。 |
| `payload.items[].supplierNo` | String | 供應商編號。 |  |
| `payload.items[].supplierName` | String | 供應商名稱。 |  |
| `payload.items[].orderedCount` | Float | 採購數量。 | 小數點後 2 位。 |
| `payload.items[].receivedCount` | Float | 進貨單已檢收數量合計。 | 進貨加總、退貨扣除。 |
| `payload.items[].unitPrice` | Float | 採購單價。 | 小數點後 4 位。 |
| `payload.items[].purchaseAmount` | Integer | 採購金額。 | 四捨五入取整數。 |
| `payload.items[].expectedArrivalTimestamp` | Integer | 預計到貨時間。 | Unix timestamp。 |
| `payload.items[].purchaseRequestNo` | String | 關聯請購單編號。 | 無關聯時為空字串。 |
| `payload.items[].purchaseRequestLinkStatusCode` | String | 請購單關聯狀態。 | `linked`、`unlinked`、`invalid`。 |
| `payload.items[].sourceOrderNo` | String | 請購單來源訂單編號。 | 無關聯時為空字串。 |
| `payload.items[].linkedWorkOrderNo` | String | 關聯工單編號。 | 第一版固定為空字串。 |
| `payload.items[].warehouseStatusCode` | String | 採購單倉儲入庫交接狀態。 | `not_received`、`pending_putaway`、`stocked`、`unknown`。 |
| `payload.items[].riskLevel` | Integer | 採購交期風險等級。 | `0` normal、`1` notice、`3` high risk。 |
| `payload.items[].riskType` | String | 採購交期風險原因。 | `late_arrival`、`due_today`、`purchase_request_unlinked`、`open_receipt`。 |
| `payload.items[].shortageCount` | Float | 尚未收貨的數量。 | 原採購單 `openCount`。 |
| `payload.items[].shortageValue` | Integer | 尚未收貨數量的估算金額。 | `shortageCount * unitPrice`，四捨五入取整數。 |
| `payload.items[].impactSourceType` | String | 風險影響來源類型。 | 第一版為 `unknown`。 |
| `payload.items[].impactSourceNo` | String | 風險影響來源單號。 | 第一版為空字串。 |
| `payload.items[].followUpCode` | String | 建議後續處理代碼。 | 第一版為 `confirm_supplier_date`。 |

### Failed Response Data

同採購單總覽 API。

### Processing Flow

先依採購單總覽流程取得資料，再保留 `riskLevel != 0` 的資料，計算風險摘要並將 `openCount` 轉為 `shortageCount`。

### Database Tables Used

| Table | Purpose |
|---|---|
| purchase_order | 採購單及交期風險計算來源。 |
| goods_receipt_note | 已收貨數量計算來源。 |
| company | 供應商名稱。 |
| purchase_request | 請購關聯風險計算來源。 |

## GET /api/v2/purchasing/goods-receipts/dashboard

<a id="get-api-v2-purchasing-goods-receipts-dashboard"></a>

### Basic Information

| URL | Method | Description |
|---|---|---|
| `/api/v2/purchasing/goods-receipts/dashboard` | GET | 查詢日期區間內的進貨單。 |

### Request Header

| Header | Description |
|---|---|
| x-auth-token | 存取金鑰。 |
| x-timezone | 時區代碼，例如 `Asia/Taipei`；未提供時使用系統預設值。 |

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| startDate | String | YES | 查詢起始日，格式 `YYYY-MM-DD`；依 `x-timezone` 解讀。 |
| endDate | String | YES | 查詢結束日，格式 `YYYY-MM-DD`；包含當日且不得早於 `startDate`。 |
| start | Integer | NO | 分頁起始位置，預設 `0`。 |
| count | Integer | NO | 分頁筆數，預設 `50`，上限 `100`。 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer", "message": "String",
  "payload": {
    "serverTimestamp": "Integer", "timezone": "String",
    "range": {"startDate": "String", "endDate": "String", "startTimestamp": "Integer", "endTimestamp": "Integer"},
    "summary": {"receiptCount": "Integer", "pendingPutawayCount": "Integer"},
    "items": [{
      "no": "String", "purchaseOrderNo": "String", "dateTimestamp": "Integer", "category": "Integer",
      "itemNo": "String", "itemName": "String", "expectedCount": "Float", "checkedCount": "Float",
      "receivedCount": "Float", "receivingStatusCode": "String", "warehouseStatusCode": "String",
      "nextOwnerDepartment": "Integer"
    }],
    "total": "Integer", "start": "Integer", "count": "Integer"
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|---|---|---|---|
| `payload.summary.receiptCount` | Integer | 查詢範圍內進貨單筆數。 | 分頁前。 |
| `payload.summary.pendingPutawayCount` | Integer | 尚待入庫處理的進貨單筆數。 | 第一版以查詢結果筆數計算。 |
| `payload.items[].no` | String | 進貨單編號。 | `goods_receipt_note.no`。 |
| `payload.items[].purchaseOrderNo` | String | 關聯採購單編號。 | `goods_receipt_note.purchase_order_no`。 |
| `payload.items[].dateTimestamp` | Integer | 進貨單日期。 | Unix timestamp。 |
| `payload.items[].category` | Integer | 進貨單類別。 | `0` 收貨、`1` 退貨。 |
| `payload.items[].itemNo` | String | 進貨料品編號。 | 來源資料表欄位。 |
| `payload.items[].itemName` | String | 進貨料品名稱。 | 來源資料表欄位。 |
| `payload.items[].expectedCount` | Float | 預計進貨數量。 | 小數點後 2 位。 |
| `payload.items[].checkedCount` | Float | 已檢收數量。 | 小數點後 2 位。 |
| `payload.items[].receivedCount` | Float | 已收貨數量。 | 第一版等同 `checkedCount`。 |
| `payload.items[].receivingStatusCode` | String | 進貨處理狀態。 | `returned`、`received`、`unknown`。 |
| `payload.items[].warehouseStatusCode` | String | 倉庫入庫交接狀態；由最新入庫 workflow task 判斷，並以 inventory evidence 確認實際入庫。 | `pending_putaway`、`stocked`、`unknown`。 |
| `payload.items[].nextOwnerDepartment` | Integer | 最新入庫 workflow task 的下一步負責部門 code；無 task 時為 `0`。 | `workflow_task_state.ownerDepartment`。 |

### Failed Response Data

同採購單總覽 API。

### Processing Flow

1. 解析日期區間與時區。
2. 查詢 `goods_receipt_note` 並依日期、單號排序。
3. 依類別及檢收數量建立進貨狀態 code。
4. 計算摘要、套用分頁並回傳。

### Database Tables Used

| Table | Purpose |
|---|---|
| goods_receipt_note | 進貨單、退貨單與檢收數量。 |

## GET /api/v2/purchasing/suppliers/dashboard

<a id="get-api-v2-purchasing-suppliers-dashboard"></a>

### Basic Information

| URL | Method | Description |
|---|---|---|
| `/api/v2/purchasing/suppliers/dashboard` | GET | 依供應商彙總採購單。 |

### Request Header

| Header | Description |
|---|---|
| x-auth-token | 存取金鑰。 |
| x-timezone | 時區代碼，例如 `Asia/Taipei`；未提供時使用系統預設值。 |

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| startDate | String | YES | 查詢起始日，格式 `YYYY-MM-DD`；依 `x-timezone` 解讀。 |
| endDate | String | YES | 查詢結束日，格式 `YYYY-MM-DD`；包含當日且不得早於 `startDate`。 |
| keyword | String | NO | 搜尋採購單號、料品編號或料品名稱。 |
| supplierNo | String | NO | 供應商編號，對應 `company.no`。 |
| start | Integer | NO | 分頁起始位置，預設 `0`。 |
| count | Integer | NO | 分頁筆數，預設 `50`，上限 `100`。 |

### Request Body

None

### Success Response Data

`payload` 共用採購單總覽的 `serverTimestamp`、`timezone`、`range` 與分頁欄位；`summary` 為空物件，`items[]` 結構如下：

```json
{
  "code": "Integer", "message": "String",
  "payload": {
    "serverTimestamp": "Integer", "timezone": "String", "range": "Object", "summary": {},
    "items": [{
      "supplierNo": "String", "supplierName": "String", "purchaseOrderCount": "Integer",
      "openPurchaseOrderCount": "Integer", "latePurchaseOrderCount": "Integer",
      "purchaseAmount": "Integer", "pendingReceiptCount": "Float", "riskLevel": "Integer"
    }],
    "total": "Integer", "start": "Integer", "count": "Integer"
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|---|---|---|---|
| `payload.items[].supplierNo` | String | 供應商編號。 | 依採購單供應商編號彙總。 |
| `payload.items[].supplierName` | String | 供應商名稱。 | 取 `company.displayName`。 |
| `payload.items[].purchaseOrderCount` | Integer | 供應商採購單筆數。 | 查詢範圍內彙總。 |
| `payload.items[].openPurchaseOrderCount` | Integer | 尚有未收貨數量的採購單筆數。 | `openCount > 0`。 |
| `payload.items[].latePurchaseOrderCount` | Integer | 已逾期採購單筆數。 | `riskType=late_arrival`。 |
| `payload.items[].purchaseAmount` | Integer | 供應商採購金額合計。 | 四捨五入取整數。 |
| `payload.items[].pendingReceiptCount` | Float | 尚待收貨數量合計。 | 小數點後 2 位。 |
| `payload.items[].riskLevel` | Integer | 供應商最高風險等級。 | `0` normal、`1` notice、`3` high risk。 |

### Failed Response Data

同採購單總覽 API。

### Processing Flow

1. 依共同日期及篩選條件取得採購單資料。
2. 依供應商編號分組，累計採購單、待收貨數量、採購金額及逾期筆數。
3. 取每一供應商的最高 `riskLevel`，再回傳彙總結果。

### Database Tables Used

| Table | Purpose |
|---|---|
| purchase_order | 供應商採購單彙總。 |
| goods_receipt_note | 待收貨數量彙總。 |
| company | 供應商名稱。 |
| purchase_request | 採購單請購關聯。 |

## GET /api/v2/purchasing/purchase-orders/{purchase_order_no}/detail

<a id="get-api-v2-purchasing-purchase-orders-purchase_order_no-detail"></a>

### Basic Information

| URL | Method | Description |
|---|---|---|
| `/api/v2/purchasing/purchase-orders/{purchase_order_no}/detail` | GET | 查詢指定採購單明細。 |

### Request Header

| Header | Description |
|---|---|
| x-auth-token | 存取金鑰。 |
| x-timezone | 時區代碼，例如 `Asia/Taipei`。 |

### Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `purchase_order_no` | String | YES | 採購單編號，對應 `purchase_order.no`。 |

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| date | Integer | NO | 狀態與時間計算基準 UTC timestamp；未提供時使用伺服器目前時間。 |

### Request Body

None

### Success Response Data

```json
{"code": "Integer", "message": "String", "payload": {"serverTimestamp": "Integer", "timezone": "String", "purchaseOrder": "Object", "purchaseRequest": "Object|null", "supplier": "Object", "receipts": "Array", "source": "Object", "inventory": "Object", "workflow": "Array", "relatedDocuments": "Object"}}
```

### Field Description

| Field Path | Type | Description | Enum |
|---|---|---|---|
| `payload.purchaseOrder` | Object | 採購單主檔及採購金額、數量與預計到貨資訊。 |
| `payload.purchaseRequest` | Object/null | 關聯請購單；沒有關聯時為 `null`。 |
| `payload.supplier` | Object | 供應商編號與名稱。 |
| `payload.receipts` | Array | 該採購單的進貨單明細。 |
| `payload.source` | Object | 請購來源訂單與關聯工單資訊。 |
| `payload.inventory` | Object | 庫存摘要；第一版回傳數量欄位且目前值為 `0.0`。 |
| `payload.workflow` | Array | 後續任務狀態；第一版回傳空陣列。 |
| `payload.relatedDocuments` | Object | 報價單與合約關聯編號；未取得時為空字串。 |
| `payload.purchaseOrder.purchaseOrderNo` | String | 採購單編號。 |
| `payload.purchaseOrder.purchaseDateTimestamp` | Integer | 採購單建立時間。 |
| `payload.purchaseOrder.itemNo` | String | 採購料品編號。 |
| `payload.purchaseOrder.itemName` | String | 採購料品名稱。 |
| `payload.purchaseOrder.unit` | Integer | 料品單位代碼。 |
| `payload.purchaseOrder.supplierNo` | String | 供應商編號。 |
| `payload.purchaseOrder.supplierName` | String | 供應商名稱。 |
| `payload.purchaseOrder.orderedCount` | Float | 採購數量，小數點後 2 位。 |
| `payload.purchaseOrder.unitPrice` | Float | 採購單價，小數點後 4 位。 |
| `payload.purchaseOrder.purchaseAmount` | Integer | 採購金額，四捨五入取整數。 |
| `payload.purchaseOrder.expectedArrivalTimestamp` | Integer | 預計到貨時間。 |
| `payload.purchaseOrder.comment` | String | 採購單備註。 |
| `payload.receipts[].no` | String | 進貨單編號。 |
| `payload.receipts[].dateTimestamp` | Integer | 進貨單日期。 |
| `payload.receipts[].category` | Integer | 進貨單類別，`0` 收貨、`1` 退貨。 |
| `payload.receipts[].expectedCount` | Float | 預計進貨數量。 |
| `payload.receipts[].checkedCount` | Float | 已檢收數量。 |
| `payload.receipts[].receivedCount` | Float | 已收貨數量，第一版等同 `checkedCount`。 |
| `payload.receipts[].receivingStatusCode` | String | `returned`、`received` 或 `unknown`。 |
| `payload.receipts[].warehouseStatusCode` | String | 倉庫入庫交接狀態；由 workflow 主判斷、inventory evidence 輔助驗證。 | `pending_putaway`、`stocked`、`unknown`。 |
| `payload.receipts[].nextOwnerDepartment` | Integer | 最新入庫 workflow task 的下一步負責部門 code；無 task 時為 `0`。 | `workflow_task_state.ownerDepartment`。 |

### Failed Response Data

採購單不存在時，回傳 HTTP `400`、`code=1`。

### Processing Flow

1. 以 path parameter 查詢 `purchase_order`。
2. 取得供應商、請購單及該採購單的進貨單。
3. 建立採購單、來源、庫存、流程及關聯文件區塊。
4. 無法取得的關聯以 `null`、空字串或空陣列表示，不以料品名稱推測關聯。

### Database Tables Used

| Table | Purpose |
|---|---|
| purchase_order | 採購單主檔。 |
| purchase_request | 關聯請購單及來源訂單。 |
| goods_receipt_note | 該採購單的進貨明細。 |
| company | 供應商名稱。 |

## Frontend Interaction Notes

| UI Action | API Behavior |
|---|---|
| 進入 Purchasing 頁面 | 呼叫 `GET /api/v2/purchasing/purchase-orders/dashboard`，並提供 `startDate`、`endDate` 與 `x-timezone`。 |
| 檢視交期風險 | 呼叫 `GET /api/v2/purchasing/purchase-orders/delivery-risk`。 |
| 檢視進貨交接 | 呼叫 `GET /api/v2/purchasing/goods-receipts/dashboard`。 |
| 檢視供應商彙總 | 呼叫 `GET /api/v2/purchasing/suppliers/dashboard`。 |
| 點選採購單 | 呼叫 `GET /api/v2/purchasing/purchase-orders/{purchase_order_no}/detail` 顯示明細。 |
| 顯示 enum | 前端將 code 轉換為多國語系文字；後端不回傳 UI fallback 字串。 |
