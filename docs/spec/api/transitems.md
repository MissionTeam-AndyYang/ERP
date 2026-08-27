# transitems API Group

> Source: `restserver/package/restserver/api/v2/transitems_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v2/transitems/dashboard](#get-api-v2-transitems-dashboard) | GET | 查詢客戶／廠商摘要、交易品項清單、交易品項 KPI 與資料完整度摘要 | OK | 依 `transaction_item_master_proposal.md` 已確認內容實作；第一版僅使用 `trans_items` |
| [/api/v2/transitems/companies/{company_no}/detail](#get-api-v2-transitems-companies-company_no-detail) | GET | 查詢單一客戶／廠商主檔、交易品項、合約與帳款條件摘要 | OK | 已依工程師 V2 命名調整為 `receivablePayment` / `payablePayment` |
| [/api/v2/transitems/transitems/{transaction_item_no}/detail](#get-api-v2-transitems-transitems-transaction_item_no-detail) | GET | 查詢單一交易品項的公司、料品、交易條件、合約來源與資料完整度 | OK | 第一版不查詢 `trans_items2` |
| /api/v1/transitems | GET | 查詢交易品項 | Legacy | 舊版 API，保留既有程式，不作為本次前端新畫面整合基準 |
| /api/v1/transitems/item | GET | 查詢交易品項 / 品項 | Legacy | 舊版 API，保留既有程式 |

## GET /api/v2/transitems/dashboard

<a id="get-api-v2-transitems-dashboard"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/transitems/dashboard | GET | 查詢客戶／廠商摘要、交易品項清單、交易品項 KPI 與資料完整度摘要 |

### Request Header

| Header | Description |
|----------|----------|
| x-timezone | 前端顯示偏好的 IANA timezone；本 API 不改寫資料庫 UTC timestamp |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| keyword | String | NO | 公司 no、公司簡稱、交易品項 no、交易品項名稱、料品 no、料品名稱或合約 no 關鍵字 |
| companyNo | String | NO | 客戶／廠商 no，對應 `company.no` |
| transItemType | String | NO | 交易品項來源 code；第一版僅支援 `trans_items` |
| transItemCategory | Integer | NO | 交易品項樣式 code，對應 `trans_items.category` |
| hasLinkedItem | Boolean | NO | 是否只顯示已關聯內部料品的交易品項 |
| hasContract | Boolean | NO | 是否只顯示已被合約引用的交易品項 |
| start | Integer | NO | 分頁起點，預設 0，負值視為 0 |
| count | Integer | NO | 回傳筆數，預設 50，最大 100 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
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
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.serverTimestamp | Integer | API 回應建立時間，UTC timestamp |  |
| payload.summary.companyCount | Integer | 本次交易品項集合關聯的公司主檔數 |  |
| payload.summary.customerCount | Integer | 與合約存在關聯的公司數；第一版不另外推測公司角色 |  |
| payload.summary.supplierCount | Integer | 與合約存在關聯的公司數；第一版不另外推測公司角色 |  |
| payload.summary.transItemCount | Integer | 套用篩選後的第一版交易品項總數 |  |
| payload.summary.linkedItemCount | Integer | 已關聯內部料品的交易品項數 |  |
| payload.summary.contractLinkedTransItemCount | Integer | 已被合約引用的交易品項數 |  |
| payload.summary.dataQualityIssueCount | Integer | 公司與交易品項中 `dataQualityCode` 不為 `ready` 的總數 |  |
| payload.companies[].companyNo | String | 公司 no |  |
| payload.companies[].companyDisplayName | String | 公司簡稱 |  |
| payload.companies[].companyName | String | 公司名稱 |  |
| payload.companies[].businessNo | String | 統一編號 |  |
| payload.companies[].transItemCount | Integer | 此公司關聯的第一版交易品項數 |  |
| payload.companies[].contractCount | Integer | 此公司關聯的合約數 |  |
| payload.companies[].contactName | String | 主要聯絡人 |  |
| payload.companies[].contactPhone | String | 主要聯絡電話摘要 |  |
| payload.companies[].receivablePayment.paymentTypeCode | String | 收款條件類型 code | cash、monthly、unknown |
| payload.companies[].receivablePayment.paymentDate | Integer | 收款月結結帳日；非月結或無資料時回傳 0 |  |
| payload.companies[].receivablePayment.paymentPeriod | Integer | 收款帳款天數；非月結或無資料時回傳 0 |  |
| payload.companies[].receivablePayment.paymentSource | Integer | 收款方式 code | 現金(0)、匯款(1)、支票(2) |
| payload.companies[].payablePayment.paymentTypeCode | String | 付款條件類型 code | cash、monthly、unknown |
| payload.companies[].payablePayment.paymentDate | Integer | 付款月結結帳日；非月結或無資料時回傳 0 |  |
| payload.companies[].payablePayment.paymentPeriod | Integer | 付款帳款天數；非月結或無資料時回傳 0 |  |
| payload.companies[].payablePayment.paymentSource | Integer | 付款方式 code | 現金(0)、匯款(1)、支票(2) |
| payload.companies[].dataQualityCode | String | 公司主檔資料完整度 code | ready、missing_payment_terms、unknown、missing_company |
| payload.transactionItems[].transItemNo | String | 交易品項 no |  |
| payload.transactionItems[].transItemName | String | 交易品項名稱 |  |
| payload.transactionItems[].transItemType | String | 交易品項來源 code | trans_items |
| payload.transactionItems[].transItemCategory | Integer | 交易品項樣式 code |  |
| payload.transactionItems[].transItemAttribute | Integer | 交易品項屬性 code |  |
| payload.transactionItems[].companyNo | String | 關聯公司 no |  |
| payload.transactionItems[].companyDisplayName | String | 關聯公司簡稱 |  |
| payload.transactionItems[].itemNo | String | 對應內部料品 no；無關聯時回傳空字串 |  |
| payload.transactionItems[].itemName | String | 對應內部料品名稱 |  |
| payload.transactionItems[].itemCategory | Integer | 對應內部料品類別 code；無料品時回傳 0 |  |
| payload.transactionItems[].contractNo | String | 目前可明確關聯的最新合約 no；無合約時回傳空字串 |  |
| payload.transactionItems[].contractCategory | Integer | 合約類別 code | 採購(1)、訂購(2) |
| payload.transactionItems[].contractType | Integer | 合約樣式 code |  |
| payload.transactionItems[].tradeUnit | Integer | 交易單位 code |  |
| payload.transactionItems[].tradePrice | Float | 交易單價，取至小數點第 4 位 |  |
| payload.transactionItems[].shippingPrice | Float | 物流價格，取至小數點第 4 位 |  |
| payload.transactionItems[].unitConversion | Float | 交易單位與料品盤點單位的規格轉換 |  |
| payload.transactionItems[].dataQualityCode | String | 此交易品項資料完整度 code | ready、missing_company、missing_linked_item、missing_contract_price、unknown |
| payload.total | Integer | 套用篩選後的交易品項筆數 |  |
| payload.start | Integer | 本次分頁起點 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Processing Flow

1. 讀取 query parameters 並轉換為後端型別。
2. 以 `trans_items` 作為第一版唯一交易品項來源，不查詢 `trans_items2`。
3. 套用 `keyword`、`companyNo`、`transItemType`、`transItemCategory`、`hasLinkedItem`、`hasContract` 篩選。
4. 依交易品項集合批次查詢 `company`、`payment`、`contract` 與內部料品主檔。
5. 每個交易品項選取目前可明確關聯的最新合約摘要；單價與物流價格取至小數點第 4 位。
6. 依公司聯絡、帳款條件、交易品項公司關聯、內部料品關聯與合約價格計算 `dataQualityCode`。
7. 回傳摘要、公司清單、交易品項分頁清單與分頁資訊。

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 客戶／廠商主檔、聯絡資訊與帳款資料關聯 |
| payment | 公司收款／付款條件資料 |
| trans_items | 第一版交易品項主檔 |
| contract | 合約與交易條件 |
| material | 原料、物料、膠捲主檔 |
| inproduct | 在製品主檔 |
| product | 製成品主檔 |
| goods | 貨品主檔 |

## GET /api/v2/transitems/companies/{company_no}/detail

<a id="get-api-v2-transitems-companies-company_no-detail"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/transitems/companies/{company_no}/detail | GET | 查詢單一客戶／廠商主檔、交易品項、合約與帳款條件摘要 |

### Request Header

| Header | Description |
|----------|----------|
| x-timezone | 前端顯示偏好的 IANA timezone |

### Query Parameters

None

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
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
    "transactionItems": [],
    "contracts": []
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.serverTimestamp | Integer | API 回應建立時間，UTC timestamp |  |
| payload.company.companyNo | String | 公司 no |  |
| payload.company.businessNo | String | 公司統編 |  |
| payload.company.companyDisplayName | String | 公司簡稱 |  |
| payload.company.companyName | String | 公司名稱 |  |
| payload.company.address | String | 公司地址 |  |
| payload.company.phone | String | 公司電話 |  |
| payload.company.contactName | String | 聯絡人姓名 |  |
| payload.company.contactPhone | String | 聯絡電話摘要 |  |
| payload.company.contactTitle | String | 聯絡人職稱 |  |
| payload.company.contactEmail | String | 聯絡人 email |  |
| payload.company.receivablePayment.paymentTypeCode | String | 收款條件類型 code | cash、monthly、unknown |
| payload.company.receivablePayment.paymentDate | Integer | 收款月結結帳日；非月結或無資料時回傳 0 |  |
| payload.company.receivablePayment.paymentPeriod | Integer | 收款帳款天數；非月結或無資料時回傳 0 |  |
| payload.company.receivablePayment.paymentSource | Integer | 收款方式 code | 現金(0)、匯款(1)、支票(2) |
| payload.company.payablePayment.paymentTypeCode | String | 付款條件類型 code | cash、monthly、unknown |
| payload.company.payablePayment.paymentDate | Integer | 付款月結結帳日；非月結或無資料時回傳 0 |  |
| payload.company.payablePayment.paymentPeriod | Integer | 付款帳款天數；非月結或無資料時回傳 0 |  |
| payload.company.payablePayment.paymentSource | Integer | 付款方式 code | 現金(0)、匯款(1)、支票(2) |
| payload.company.dataQualityCode | String | 公司主檔資料完整度 code | ready、missing_payment_terms、unknown、missing_company |
| payload.transactionItems[] | Array | 此公司關聯的第一版交易品項摘要 |  |
| payload.contracts[] | Array | 此公司相關合約清單；不與 `transactionItems[]` 合併 |  |

### Processing Flow

1. 驗證 `company_no` 並查詢 `company`。
2. 查詢此公司關聯的 `trans_items`。
3. 依交易品項 no 查詢 `contract`，並依公司 `received_id` / `paid_id` 查詢 `payment`。
4. 建立公司主檔、交易品項摘要與合約清單。
5. 若公司不存在，沿用既有 not-found response contract。

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 公司主檔 |
| payment | 公司收款／付款條件資料 |
| trans_items | 此公司關聯的交易品項 |
| contract | 此公司交易品項相關合約 |

## GET /api/v2/transitems/transitems/{transaction_item_no}/detail

<a id="get-api-v2-transitems-transitems-transaction_item_no-detail"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/transitems/transitems/{transaction_item_no}/detail | GET | 查詢單一交易品項的公司、料品、交易條件、合約來源與資料完整度 |

### Request Header

| Header | Description |
|----------|----------|
| x-timezone | 前端顯示偏好的 IANA timezone |

### Query Parameters

None

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
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
    "contracts": [],
    "linkedItems": []
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.serverTimestamp | Integer | API 回應建立時間，UTC timestamp |  |
| payload.transItem.transItemNo | String | 交易品項 no |  |
| payload.transItem.transItemName | String | 交易品項名稱 |  |
| payload.transItem.transItemType | String | 交易品項來源 code | trans_items |
| payload.transItem.transItemCategory | Integer | 交易品項樣式 code |  |
| payload.transItem.transItemAttribute | Integer | 交易品項屬性 code |  |
| payload.transItem.companyNo | String | 關聯公司 no |  |
| payload.transItem.companyDisplayName | String | 關聯公司簡稱 |  |
| payload.transItem.itemNo | String | 對應內部料品 no；無關聯時回傳空字串 |  |
| payload.transItem.itemName | String | 對應內部料品名稱 |  |
| payload.transItem.itemCategory | Integer | 對應內部料品類別 code；無關聯時回傳 0 |  |
| payload.transItem.comment | String | 規格或備註 |  |
| payload.transItem.creationTime | Integer | 資料建立時間 UTC timestamp；無資料時回傳 0 |  |
| payload.transItem.dataQualityCode | String | 此交易品項整體資料完整度 code | ready、missing_company、missing_linked_item、missing_contract_price、unknown |
| payload.contracts[] | Array | 此交易品項相關合約清單；無合約時回傳空陣列 |  |
| payload.linkedItems[] | Array | 此交易品項對應的內部料品清單；第一版通常為 0 或 1 筆 |  |

### Processing Flow

1. 驗證 `transaction_item_no` 並查詢 `trans_items`。
2. 查詢交易品項關聯公司、合約與內部料品主檔。
3. 合約依生效日期與建立時間排序，回傳交易條件清單。
4. 依公司、內部料品與合約價格計算 `dataQualityCode`。
5. 若交易品項不存在，沿用既有 not-found response contract。

### Database Tables Used

| Table | Purpose |
|----------|------|
| trans_items | 第一版交易品項主檔 |
| company | 關聯公司 |
| contract | 合約與交易條件 |
| material | 原料、物料、膠捲主檔 |
| inproduct | 在製品主檔 |
| product | 製成品主檔 |
| goods | 貨品主檔 |
