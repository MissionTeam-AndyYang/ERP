# 程式修正
1. 針對 /api/v2/transitems/dashboard
  - 將公司與交易品項中 dataQualityCode 不為 ready 的總數，請分別獨立存放，不合併加總至 dataQualityIssueCount。
  - 當查詢條件未傳遞 start 與 count 參數時，系統預設會回傳 companies 的 0～50 筆資料，還是 transactionItems 的 0～50 筆資料？是否應將其拆分為兩個 API，並搭配 start 與 count 參數使用，以使查詢邏輯更為明確？
  




# 工程師提問V2
1. 針對 /api/v2/item-trade-master/companies/{company_no}/detail
  - receivableTerms 更名 receivablePayment ; payableTerms 更名 payablelePayment 
  - settlementTypeCode 更名 paymentTypeCode
  - closingDay 更名  paymentDate
  - accountDays 更名  paymentPeriod
  - 新增 paymentSource: 收付款方式；現金 (0)、匯款 (1)、支票 (2)

## 工程師回覆V2

| 項目 | 回覆與調整 |
|---|---|
| receivableTerms / payableTerms 命名 | 已依工程師提問改為 `receivablePayment` 與 `payablePayment`。工程師提問中的 `payablelePayment` 依命名一致性判斷為 typo，本提案採 `payablePayment`。 |
| 帳款欄位命名 | 已將 `settlementTypeCode`、`closingDay`、`accountDays` 改為 `paymentTypeCode`、`paymentDate`、`paymentPeriod`。 |
| 收付款方式 | 已新增 `paymentSource`，表示收付款方式 code：現金(0)、匯款(1)、支票(2)。 |
| 適用範圍 | V2 提問雖以 company detail 為主，但 dashboard 的 `companies[]` 也顯示公司帳款摘要；為避免同一語意出現兩套欄位名稱，已同步調整 dashboard 與 company detail 的公司帳款欄位。 |


# 工程師提問
1. 將/api/v2/item-trade-master/xxx更名為/api/v2/transitems/xxx
2. 目前規劃中不顯示公司交易角色 (companyRoleCode)，請移除相關欄位及畫面設計
3. 交易品項第一版設計請以 trans_items1 為主，後續再行評估並考量 trans_items2 的設計呈現
4. 針對 共用 Query Parameters / Header
   - 移除 dataQualityCode 欄位
   - transactionItemSourceCode 更名 transItemType
   - transactionCategory 更名 transItemCategory
   - hasMaterialItem 更名 hasLinkedItem

5. 針對 /api/v2/item-trade-master/dashboard
   - linkedMaterialItemCount 更名 linkedItemCount
   - transactionItems[].transactionItemxxx 更名 transactionItems[].transItemxxx
   - transactionItems[].transactionxxx 更名 transactionItems[].transItemxxx
   - transactionItems[].transactionItemSourceCode 更名 transactionItems[].transItemType
   - transactionItems[].materialItemxxx 更名 transactionItems[].itemxxx
   - 移除 companies[].paymentSummaryCode 欄位，並新增公司帳款(收款/付款)相關資訊，例如：現結／月結。若為月結，需包含結帳日與帳款天數 (參照資料表company.received_id與company.paid_id)
   - 請評估 dataQualityIssues 欄位資料是否可拆分存放，例如以 transactionItems[].dataQualityCode 與 companies[].dataQualityCode 方式呈現，並確認是否能達到相同效果

6. 針對 /api/v2/item-trade-master/companies/{company_no}/detail
    - 移除 company[].paymentSummaryCode 欄位，並新增公司帳款(收款/付款)相關資訊，例如：現結／月結。若為月結，需包含結帳日與帳款天數 (參照資料表company.received_id與company.paid_id)
   - transactionItems[].transactionItemxxx 更名 transactionItems[].transItemxxx
   - transactionItems[].transactionxxx 更名 transactionItems[].transItemxxx
   - transactionItems[].transactionItemSourceCode 更名 transactionItems[].transItemType
   - transactionItems[].materialItemxxx 更名 transactionItems[].itemxxx
   - contracts[].transactionItemxxx 更名 transactionItems[].transItemxxx
   - transactionItems[] 與 contracts[] 的資料結構相近，是否可合併為單一欄位？或在設計上是否有其他需要考量的因素？
   - 新增 transactionItems[].transItemCategory欄位: 交易品項樣式 code；依來源表分別使用 trans_items.category 或 trans_items2.category

7. 針對 /api/v2/item-trade-master/transaction-items/{transaction_item_no}/detail
    - 將 URI 更名為 /api/v2/transitems/transitems/{transaction_item_no}/detail
   - transactionItems.transactionItemxxx 更名 transactionItems[].transItemxxx
   - transactionItems.transactionxxx 更名 transactionItems[].transItemxxx
   - transactionItems.transactionItemSourceCode 更名 transactionItems[].transItemType
   - transactionItems.materialItemxxx 更名 transactionItems[].itemxxx
   - tradeTerms 更名 contracts
   - relatedMaterialItem 更名 linkedItems
   - 請說明 transactionItem.dataQualityCode 與 dataQualityIssues 在定義上的差異，並評估是否僅需保留其中之一

## 工程師回覆

| 項目 | 回覆與調整 |
|---|---|
| API URI 命名 | 已將本提案正式 API 路徑改為 `/api/v2/transitems/...`。 |
| 公司交易角色 | 第一版畫面不顯示公司交易角色，已移除 `companyRoleCode` 與相關描述。 |
| 第一版交易品項範圍 | 第一版以 `trans_items` 為主。工程師提到的 `trans_items1` 依現行資料庫文件理解為 `trans_items`；`trans_items2` 暫列為下一版評估範圍，本版 API 不查詢、不合併、不回傳。 |
| 共用參數調整 | 已移除 query `dataQualityCode`，並將 `transactionItemSourceCode`、`transactionCategory`、`hasMaterialItem` 分別改為 `transItemType`、`transItemCategory`、`hasLinkedItem`。 |
| 欄位命名調整 | 已將 `transactionItemxxx` / `transactionxxx` 統一改為 `transItemxxx`，並將 `materialItemxxx` 改為 `itemxxx`。 |
| 公司帳款資訊 | 已移除 `paymentSummaryCode`，並依 V2 回覆改以 `receivablePayment` 與 `payablePayment` 回傳收款／付款條件；來源分別參照 `company.received_id` 與 `company.paid_id`。 |
| dataQualityIssues 拆分 | 已移除獨立 `dataQualityIssues[]`。第一版改由 `companies[].dataQualityCode`、`transactionItems[].dataQualityCode` 與 `transItem.dataQualityCode` 表示資料完整度，可達到畫面提示資料缺口的效果，也能避免額外維護一組非資料庫任務的 issue list。 |
| transactionItems[] 與 contracts[] 是否合併 | 不建議合併。`transactionItems[]` 表示公司目前維護的交易品項主檔摘要；`contracts[]` 表示合約與交易條件清單。兩者雖有部分欄位相似，但生命週期與業務問題不同，因此第一版保留分離。 |
| detail dataQualityCode 與 dataQualityIssues 差異 | `dataQualityCode` 是該筆公司或交易品項的整體資料完整度狀態；`dataQualityIssues[]` 原本是拆成多筆缺口事件。第一版只保留 `dataQualityCode`，由前端依 enum 顯示對應提示。 |
# Transaction Item Master API Proposal

> Status: API Proposal / Pending Engineer Review  
> Screen: `ItemAndTransactionMasterScreen`  
> Route: `/items`  
> Scope: V1 read-only Core  
> Design basis: `AGENTS.md`, `docs/spec/database/index.md`, `docs/spec/api-proposal/item_center_proposal.md`, `docs/spec/api-proposal/transaction_item_master_static_preview.html`

## 1. 畫面定位

「品項與交易主資料中心」建議作為 `/items` 的下一版資訊架構，將既有料品主資料與商務交易主資料放在同一入口，但在畫面內清楚分成三個視圖：

| View | 主視角 | 本版邊界 |
|---|---|---|
| `CompanyMasterView` | 客戶／廠商主檔 | 檢視公司主檔、聯絡資訊、收付款條件、交易品項數與合約摘要。 |
| `MaterialItemMasterView` | 料品品項 | 延續既有 `ItemCenterScreen`，檢視 `material`、`inproduct`、`product`、`goods` 的主檔、庫存訊號、BOM 關聯與維護建議。 |
| `TransactionItemMasterView` | 交易品項 | 第一版檢視 `trans_items` 及其公司、料品與合約交易條件關聯；`trans_items2` 留待下一版評估。 |

交易品項不應只顯示交易品名與價格，必須同時呈現「客戶／廠商」與「對應料品品項」，才能支援採購、訂購、報價、合約與後續訂單流程的共同理解。

第一版不提供 POST、PUT、DELETE，不新增或修改客戶／廠商、料品、交易品項或合約。後端只回傳 enum code、數值與資料庫欄位；顯示文字、單位文字與多國語言由前端處理。

## 2. V1 API 清單

| API | Method | 用途 |
|---|---|---|
| `/api/v2/transitems/dashboard` | GET | 查詢客戶／廠商摘要、交易品項清單、交易品項 KPI 與資料完整度摘要。 |
| `/api/v2/transitems/companies/{company_no}/detail` | GET | 查詢單一客戶／廠商主檔、交易品項、合約與帳款條件摘要。 |
| `/api/v2/transitems/transitems/{transaction_item_no}/detail` | GET | 查詢單一交易品項的公司、料品、交易條件、合約來源與資料完整度。 |

`MaterialItemMasterView` 仍沿用既有 `GET /api/v2/items/dashboard` 與 `GET /api/v2/items/{item_no}/detail`，不在本提案重複定義。

## 3. 共用 Query Parameters / Header

| Parameter / Header | Type | Required | Description |
|---|---|---:|---|
| `keyword` | String | No | 公司 no、公司簡稱、交易品項 no、交易品項名稱、料品 no、料品名稱或合約 no 關鍵字。 |
| `companyNo` | String | No | 客戶／廠商 no，對應 `company.no`。 |
| `transItemType` | String | No | 交易品項來源 code；第一版固定以 `trans_items` 為主，保留此參數供前端狀態與後續版本延伸。 |
| `transItemCategory` | Integer | No | 交易品項樣式 code，對應 `trans_items.category`。 |
| `hasLinkedItem` | Boolean | No | 是否只顯示已關聯內部料品的交易品項。 |
| `hasContract` | Boolean | No | 是否只顯示已被合約引用的交易品項。 |
| `start` | Integer | No | 分頁起點，預設 0；負值視為 0。 |
| `count` | Integer | No | 回傳筆數，預設 50，最大 100。 |
| `x-timezone` | Header String | No | 前端顯示偏好的 IANA timezone；後端不改寫資料庫 UTC timestamp。 |

## 4. GET `/api/v2/transitems/dashboard`

### 4.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "summary": {
    "companyCount": "Integer",
    "customerCount": "Integer",
    "supplierCount": "Integer",
    "transItemCount": "Integer",
    "linkedItemCount": "Integer",
    "contractLinkedTransItemCount": "Integer",
    "dataQualityIssueCount": "Integer"
  },
  "companies": [
    {
      "companyNo": "String",
      "companyDisplayName": "String",
      "companyName": "String",
      "businessNo": "String",
      "transItemCount": "Integer",
      "contractCount": "Integer",
      "contactName": "String",
      "contactPhone": "String",
      "receivablePayment": {
        "paymentTypeCode": "String",
        "paymentDate": "Integer",
        "paymentPeriod": "Integer",
        "paymentSource": "Integer"
      },
      "payablePayment": {
        "paymentTypeCode": "String",
        "paymentDate": "Integer",
        "paymentPeriod": "Integer",
        "paymentSource": "Integer"
      },
      "dataQualityCode": "String"
    }
  ],
  "transactionItems": [
    {
      "transItemNo": "String",
      "transItemName": "String",
      "transItemType": "String",
      "transItemCategory": "Integer",
      "transItemAttribute": "Integer",
      "companyNo": "String",
      "companyDisplayName": "String",
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "contractNo": "String",
      "contractCategory": "Integer",
      "contractType": "Integer",
      "tradeUnit": "Integer",
      "tradePrice": "Float",
      "shippingPrice": "Float",
      "unitConversion": "Float",
      "dataQualityCode": "String"
    }
  ],
  "total": "Integer",
  "start": "Integer",
  "count": "Integer"
}
```

### 4.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `serverTimestamp` | Integer | API 回應建立時間，UTC timestamp。 | 系統時間 |
| `summary.companyCount` | Integer | 套用篩選後的公司主檔數。 | `company` |
| `summary.customerCount` | Integer | 與訂購合約或銷售交易資料存在關聯的公司數。 | `company`、`contract.category=2` |
| `summary.supplierCount` | Integer | 與採購合約或採購交易資料存在關聯的公司數。 | `company`、`contract.category=1` |
| `summary.transItemCount` | Integer | 第一版交易品項總數。 | `trans_items` |
| `summary.linkedItemCount` | Integer | 已關聯內部料品的交易品項數。 | `trans_items.item_no` |
| `summary.contractLinkedTransItemCount` | Integer | 已被合約引用的交易品項數。 | `contract.item_no` |
| `summary.dataQualityIssueCount` | Integer | 公司與交易品項中 `dataQualityCode` 不為 `ready` 的總數。 | 後端資料完整度規則 |
| `companies[].companyNo` | String | 公司 no。 | `company.no` |
| `companies[].companyDisplayName` | String | 公司簡稱。 | `company.displayName` |
| `companies[].companyName` | String | 公司名稱。 | `company.name` |
| `companies[].businessNo` | String | 統一編號。 | `company.businessNo` |
| `companies[].transItemCount` | Integer | 此公司關聯的第一版交易品項數。 | `trans_items.company_no` |
| `companies[].contractCount` | Integer | 此公司關聯的合約數。 | `contract.item_ref_no` |
| `companies[].contactName` | String | 主要聯絡人。 | `company.contactName` |
| `companies[].contactPhone` | String | 主要聯絡電話；若來源為 JSON 或 longtext，後端只回傳畫面使用的一個摘要字串。 | `company.contactPhone` |
| `companies[].receivablePayment.paymentTypeCode` | String | 收款條件類型 code，例如現結、月結或未知。 | `company.received_id` 對應帳款條件資料 |
| `companies[].receivablePayment.paymentDate` | Integer | 收款月結結帳日；非月結或無資料時回傳 0。 | `company.received_id` 對應帳款條件資料 |
| `companies[].receivablePayment.paymentPeriod` | Integer | 收款帳款天數；非月結或無資料時回傳 0。 | `company.received_id` 對應帳款條件資料 |
| `companies[].receivablePayment.paymentSource` | Integer | 收款方式 code；現金(0)、匯款(1)、支票(2)，無資料時回傳 0。 | `company.received_id` 對應帳款條件資料 |
| `companies[].payablePayment.paymentTypeCode` | String | 付款條件類型 code，例如現結、月結或未知。 | `company.paid_id` 對應帳款條件資料 |
| `companies[].payablePayment.paymentDate` | Integer | 付款月結結帳日；非月結或無資料時回傳 0。 | `company.paid_id` 對應帳款條件資料 |
| `companies[].payablePayment.paymentPeriod` | Integer | 付款帳款天數；非月結或無資料時回傳 0。 | `company.paid_id` 對應帳款條件資料 |
| `companies[].payablePayment.paymentSource` | Integer | 付款方式 code；現金(0)、匯款(1)、支票(2)，無資料時回傳 0。 | `company.paid_id` 對應帳款條件資料 |
| `companies[].dataQualityCode` | String | 公司主檔資料完整度 code，主要檢查聯絡資訊與收付款條件。 | `dataQualityCode` |
| `transactionItems[].transItemNo` | String | 交易品項 no。 | `trans_items.no` |
| `transactionItems[].transItemName` | String | 交易品項名稱。 | `trans_items.name` |
| `transactionItems[].transItemType` | String | 交易品項來源 code。 | `trans_items` |
| `transactionItems[].transItemCategory` | Integer | 交易品項樣式 code。 | `trans_items.category` |
| `transactionItems[].transItemAttribute` | Integer | 交易品項屬性 code。 | `trans_items.attribute` |
| `transactionItems[].companyNo` | String | 關聯公司 no。 | `trans_items.company_no`、fallback `contract.item_ref_no` |
| `transactionItems[].companyDisplayName` | String | 關聯公司簡稱。 | `trans_items.company_displayName`、fallback `company.displayName` |
| `transactionItems[].itemNo` | String | 對應內部料品 no；無關聯時回傳空字串。 | `trans_items.item_no` |
| `transactionItems[].itemName` | String | 對應內部料品名稱。 | `trans_items.item_name` |
| `transactionItems[].itemCategory` | Integer | 對應內部料品類別 code；無料品時回傳 0。 | `contract.itemCategory` 或料品主檔 |
| `transactionItems[].contractNo` | String | 目前可明確關聯的合約 no；無合約時回傳空字串。 | `contract.no` |
| `transactionItems[].contractCategory` | Integer | 合約類別 code。 | 採購(1)、訂購(2) |
| `transactionItems[].contractType` | Integer | 合約樣式 code。 | `contract.type` |
| `transactionItems[].tradeUnit` | Integer | 交易單位 code。 | `contract.unit` |
| `transactionItems[].tradePrice` | Float | 交易單價，取至小數點第 4 位。 | `contract.price` |
| `transactionItems[].shippingPrice` | Float | 物流價格，取至小數點第 4 位。 | `contract.shippingPrice` |
| `transactionItems[].unitConversion` | Float | 交易單位與料品盤點單位的規格轉換。 | `contract.unitConversion` |
| `transactionItems[].dataQualityCode` | String | 此交易品項資料完整度 code。 | `dataQualityCode` |
| `total` | Integer | 套用篩選後的交易品項筆數。 |  |
| `start` | Integer | 本次分頁起點。 |  |
| `count` | Integer | 本次回傳筆數。 |  |

## 5. GET `/api/v2/transitems/companies/{company_no}/detail`

### 5.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "company": {
    "companyNo": "String",
    "businessNo": "String",
    "companyDisplayName": "String",
    "companyName": "String",
    "address": "String",
    "phone": "String",
    "contactName": "String",
    "contactPhone": "String",
    "contactTitle": "String",
    "contactEmail": "String",
    "receivablePayment": {
      "paymentTypeCode": "String",
      "paymentDate": "Integer",
      "paymentPeriod": "Integer",
      "paymentSource": "Integer"
    },
    "payablePayment": {
      "paymentTypeCode": "String",
      "paymentDate": "Integer",
      "paymentPeriod": "Integer",
      "paymentSource": "Integer"
    },
    "dataQualityCode": "String"
  },
  "transactionItems": [
    {
      "transItemNo": "String",
      "transItemName": "String",
      "transItemType": "String",
      "transItemCategory": "Integer",
      "transItemAttribute": "Integer",
      "itemNo": "String",
      "itemName": "String",
      "contractNo": "String",
      "tradeUnit": "Integer",
      "tradePrice": "Float",
      "dataQualityCode": "String"
    }
  ],
  "contracts": [
    {
      "contractNo": "String",
      "contractDisplayName": "String",
      "contractCategory": "Integer",
      "contractType": "Integer",
      "effectiveDate": "Integer",
      "transItemNo": "String",
      "transItemName": "String"
    }
  ]
}
```

### 5.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `company.companyNo` | String | 公司 no。 | `company.no` |
| `company.businessNo` | String | 公司統編。 | `company.businessNo` |
| `company.companyDisplayName` | String | 公司簡稱。 | `company.displayName` |
| `company.companyName` | String | 公司名稱。 | `company.name` |
| `company.address` | String | 公司地址。 | `company.address` |
| `company.phone` | String | 公司電話。 | `company.phone` |
| `company.contactName` | String | 聯絡人姓名。 | `company.contactName` |
| `company.contactPhone` | String | 聯絡電話摘要。 | `company.contactPhone` |
| `company.contactTitle` | String | 聯絡人職稱。 | `company.contactTitle` |
| `company.contactEmail` | String | 聯絡人 email。 | `company.contactEmail` |
| `company.receivablePayment.paymentTypeCode` | String | 收款條件類型 code，例如現結、月結或未知。 | `company.received_id` 對應帳款條件資料 |
| `company.receivablePayment.paymentDate` | Integer | 收款月結結帳日；非月結或無資料時回傳 0。 | `company.received_id` 對應帳款條件資料 |
| `company.receivablePayment.paymentPeriod` | Integer | 收款帳款天數；非月結或無資料時回傳 0。 | `company.received_id` 對應帳款條件資料 |
| `company.receivablePayment.paymentSource` | Integer | 收款方式 code；現金(0)、匯款(1)、支票(2)，無資料時回傳 0。 | `company.received_id` 對應帳款條件資料 |
| `company.payablePayment.paymentTypeCode` | String | 付款條件類型 code，例如現結、月結或未知。 | `company.paid_id` 對應帳款條件資料 |
| `company.payablePayment.paymentDate` | Integer | 付款月結結帳日；非月結或無資料時回傳 0。 | `company.paid_id` 對應帳款條件資料 |
| `company.payablePayment.paymentPeriod` | Integer | 付款帳款天數；非月結或無資料時回傳 0。 | `company.paid_id` 對應帳款條件資料 |
| `company.payablePayment.paymentSource` | Integer | 付款方式 code；現金(0)、匯款(1)、支票(2)，無資料時回傳 0。 | `company.paid_id` 對應帳款條件資料 |
| `company.dataQualityCode` | String | 公司主檔資料完整度 code。 | `dataQualityCode` |
| `transactionItems[]` | Array | 此公司關聯的第一版交易品項摘要。 | `trans_items`、`contract` |
| `transactionItems[].transItemNo` | String | 交易品項 no。 | `trans_items.no` |
| `transactionItems[].transItemName` | String | 交易品項名稱。 | `trans_items.name` |
| `transactionItems[].transItemType` | String | 交易品項來源 code。 | `trans_items` |
| `transactionItems[].transItemCategory` | Integer | 交易品項樣式 code。 | `trans_items.category` |
| `transactionItems[].transItemAttribute` | Integer | 交易品項屬性 code。 | `trans_items.attribute` |
| `transactionItems[].itemNo` | String | 對應內部料品 no。 | `trans_items.item_no` |
| `transactionItems[].itemName` | String | 對應內部料品名稱。 | `trans_items.item_name` |
| `transactionItems[].contractNo` | String | 目前可明確關聯的合約 no。 | `contract.no` |
| `transactionItems[].tradeUnit` | Integer | 交易單位 code。 | `contract.unit` |
| `transactionItems[].tradePrice` | Float | 交易單價，取至小數點第 4 位。 | `contract.price` |
| `transactionItems[].dataQualityCode` | String | 此交易品項資料完整度 code。 | `dataQualityCode` |
| `contracts[]` | Array | 此公司相關合約清單；不與 `transactionItems[]` 合併，因合約與交易品項主檔生命週期不同。 | `contract` |
| `contracts[].contractNo` | String | 合約 no。 | `contract.no` |
| `contracts[].contractDisplayName` | String | 合約簡稱。 | `contract.displayName` |
| `contracts[].contractCategory` | Integer | 合約類別。 | `contract.category` |
| `contracts[].contractType` | Integer | 合約樣式。 | `contract.type` |
| `contracts[].effectiveDate` | Integer | 生效日期 UTC timestamp。 | `contract.date` |
| `contracts[].transItemNo` | String | 合約引用交易品項 no。 | `contract.item_no` |
| `contracts[].transItemName` | String | 合約引用交易品項名稱。 | `contract.item_name` |

## 6. GET `/api/v2/transitems/transitems/{transaction_item_no}/detail`

### 6.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "transItem": {
    "transItemNo": "String",
    "transItemName": "String",
    "transItemType": "String",
    "transItemCategory": "Integer",
    "transItemAttribute": "Integer",
    "companyNo": "String",
    "companyDisplayName": "String",
    "itemNo": "String",
    "itemName": "String",
    "itemCategory": "Integer",
    "comment": "String",
    "creationTime": "Integer",
    "dataQualityCode": "String"
  },
  "contracts": [
    {
      "contractNo": "String",
      "contractDisplayName": "String",
      "contractCategory": "Integer",
      "contractType": "Integer",
      "tradeUnit": "Integer",
      "tradePrice": "Float",
      "shippingPrice": "Float",
      "unitConversion": "Float",
      "effectiveDate": "Integer"
    }
  ],
  "linkedItems": [
    {
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "unitWarehouse": "Integer"
    }
  ]
}
```

### 6.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `transItem.transItemNo` | String | 交易品項 no。 | `trans_items.no` |
| `transItem.transItemName` | String | 交易品項名稱。 | `trans_items.name` |
| `transItem.transItemType` | String | 交易品項來源 code。 | `trans_items` |
| `transItem.transItemCategory` | Integer | 交易品項樣式 code。 | `trans_items.category` |
| `transItem.transItemAttribute` | Integer | 交易品項屬性 code。 | `trans_items.attribute` |
| `transItem.companyNo` | String | 關聯公司 no。 | `trans_items.company_no`、合約 fallback |
| `transItem.companyDisplayName` | String | 關聯公司簡稱。 | `trans_items.company_displayName`、fallback `company.displayName` |
| `transItem.itemNo` | String | 對應內部料品 no；無關聯時回傳空字串。 | `trans_items.item_no` |
| `transItem.itemName` | String | 對應內部料品名稱。 | `trans_items.item_name` |
| `transItem.itemCategory` | Integer | 對應內部料品類別 code；無關聯時回傳 0。 | `contract.itemCategory` 或料品主檔 |
| `transItem.comment` | String | 規格或備註。 | `trans_items.comment` |
| `transItem.creationTime` | Integer | 資料建立時間 UTC timestamp；無資料時回傳 0。 | `trans_items.creationTime` |
| `transItem.dataQualityCode` | String | 此交易品項整體資料完整度 code。 | `dataQualityCode` |
| `contracts[]` | Array | 此交易品項相關合約清單；無合約時回傳空陣列。 | `contract` |
| `contracts[].contractNo` | String | 合約 no。 | `contract.no` |
| `contracts[].contractDisplayName` | String | 合約簡稱。 | `contract.displayName` |
| `contracts[].contractCategory` | Integer | 合約類別。 | `contract.category` |
| `contracts[].contractType` | Integer | 合約樣式。 | `contract.type` |
| `contracts[].tradeUnit` | Integer | 交易單位 code。 | `contract.unit` |
| `contracts[].tradePrice` | Float | 交易單價，取至小數點第 4 位。 | `contract.price` |
| `contracts[].shippingPrice` | Float | 物流價格，取至小數點第 4 位。 | `contract.shippingPrice` |
| `contracts[].unitConversion` | Float | 規格轉換。 | `contract.unitConversion` |
| `contracts[].effectiveDate` | Integer | 合約生效日期 UTC timestamp。 | `contract.date` |
| `linkedItems[]` | Array | 此交易品項對應的內部料品清單；第一版通常為 0 或 1 筆。 | `trans_items.item_no` 與料品主檔 |
| `linkedItems[].itemNo` | String | 內部料品 no。 | 料品主檔 |
| `linkedItems[].itemName` | String | 內部料品名稱。 | 料品主檔 |
| `linkedItems[].itemCategory` | Integer | 內部料品類別 code。 | 料品主檔 |
| `linkedItems[].unitWarehouse` | Integer | 料品盤點或倉庫單位 code。 | 料品主檔 |

## 7. Enum 建議

| Enum | Values | Description |
|---|---|---|
| `transItemType` | `trans_items` | 交易品項來源。第一版僅回傳 `trans_items`；`trans_items2` 留待下一版評估後再納入。 |
| `dataQualityCode` | `ready`、`missing_company`、`missing_linked_item`、`missing_contract_price`、`missing_payment_terms`、`unknown` | 公司或交易品項資料完整度狀態。 |
| `paymentTypeCode` | `cash`、`monthly`、`unknown` | 收款或付款條件類型，由帳款條件資料推導，前端負責顯示文字與多國語言轉換。 |
| `paymentSource` | `0`、`1`、`2` | 收付款方式 code；0=現金、1=匯款、2=支票。 |

## 8. Database Tables Used

| Table | Purpose |
|---|---|
| `company` | 客戶／廠商主檔、聯絡資訊與帳款資料關聯；收款條件參照 `received_id`，付款條件參照 `paid_id`。 |
| `trans_items` | 第一版交易品項主檔，包含公司與內部料品關聯。 |
| `contract` | 合約與交易條件，提供交易單位、單價、物流價格、規格轉換與交易品項引用。 |
| `material` | 原料、物料、膠捲主檔；用於交易品項對應內部料品。 |
| `inproduct` | 在製品主檔；用於交易品項對應內部料品。 |
| `product` | 製成品主檔；用於交易品項對應內部料品。 |
| `goods` | 貨品主檔；若合約或交易品項指向貨品時作為補充。 |
| `payment` | 公司收款／付款條件資料，供 `receivablePayment` 與 `payablePayment` 摘要使用。 |

## 9. 備註

1. 第一版交易品項主資料以 `trans_items` 為唯一資料來源；`trans_items2` 不納入本版查詢、統計或回傳欄位，以避免不同資料型態混合造成畫面與 API 語意不清。
2. 本提案不顯示公司交易角色，也不回傳 `companyRoleCode`。若未來管理者需要區分客戶／廠商視角，建議另以合約類別或交易流程資料建立可驗證的篩選邏輯，再進入下一版提案。
3. `receivablePayment` 與 `payablePayment` 只回傳帳款條件 code 與必要數值；現結／月結、收付款方式等顯示文字由前端依 enum 與多國語言字典轉換。
4. `dataQualityCode` 是 read-only 資料完整度提示，不代表 workflow task，也不建立待辦或部門轉交。第一版不再提供獨立 `dataQualityIssues[]`。
5. `tradePrice` 與 `shippingPrice` 來源為 `contract`，若同一交易品項有多筆合約，第一版可優先回傳目前生效或最新生效日期的合約摘要；若無法唯一判定，應回傳空合約摘要並以 `dataQualityCode=missing_contract_price` 或 `unknown` 提示。
6. 本提案不取代 `ItemCenterScreen` 既有料品 API；料品主資料仍由 `item_center_proposal.md` 維護。
