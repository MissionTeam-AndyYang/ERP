# company API Group

> Source: `restserver/package/restserver/api/company_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/company](#get-api-v1-company) | GET | 查詢客戶/廠商 | OK | OK |

## GET /api/v1/company

<a id="get-api-v1-company"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/company | GET | 查詢客戶/廠商 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | String | NO | 分頁筆數 |
| start | String | NO | 分頁起始位置 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "total": "Integer",
    "count": "Integer",
    "results": [
      {
        "company": {
            "id": "Integer",
            "no": "String",
            "businessNo": "String",
            "displayName": "String",
            "name": "String",
            "address": "String",
            "phone": "String",
            "fax": "String",
            "contactName": "String",
            "contactPhone": [
                "String"
            ],
            "contactTitle": "String",
            "contactEmail": "String",           
            "bankCurrency": "Integer",
            "bankDisplayName": "String",
            "bankName": "String",
            "bankBranch": "String",
            "bankAccount": "String",
            "bankNo": "String",
            "comment": "String",
            "creationTime": "Integer",
        },
        "paidPayment": {
          "id": "Integer",
          "type": "Integer",
          "source": "Integer",
          "date": "Integer",
          "period": "Integer",
          "creationTime": "Integer"
        },
        "receivedPayment": {
          "id": "Integer",
          "type": "Integer",
          "source": "Integer",
          "date": "Integer",
          "period": "Integer",
          "creationTime": "Integer"
        }
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].company.id | Integer | 棧板群組編號 |  |
| payload.results[].company.no | String | 棧板群組編號 |  |
| payload.results[].company.businessNo | String | 公司統編 |  |
| payload.results[].company.displayName | String | 公司簡稱 |  |
| payload.results[].company.name | String | 公司名稱 |  |
| payload.results[].company.address | String | 公司地址 |  |
| payload.results[].company.phone | String | 公司電話 |  |
| payload.results[].company.fax | String | 公司傳真 |  |
| payload.results[].company.contactName | String | 連絡人姓名 |  |
| payload.results[].company.contactPhone | String Array | 連絡人電話 |  |
| payload.results[].company.contactTitle | String | 連絡人職稱 |  |
| payload.results[].company.contactEmail | String | 連絡人電郵 |  |
| payload.results[].company.bankCurrency | Integer | 收款銀行幣別 |  |
| payload.results[].company.bankDisplayName | String | 收款銀行帳戶簡稱 |  |
| payload.results[].company.bankName | String | 收款銀行名稱 |  |
| payload.results[].company.bankBranch | String | 收款分行名稱 |  |
| payload.results[].company.bankAccount | String | 收款銀行戶名 |  |
| payload.results[].company.bankNo | String | 收款銀行帳號 |  |
| payload.results[].company.comment | String | 備註 |  |
| payload.results[].company.creationTime | Integer | 資料建立時間 |  |
| payload.results[].receivedPayment.id | Integer | 收款帳款資料id |  |
| payload.results[].receivedPayment.type | Integer | 收款類別 | 現結 (0)、月結 (1) |
| payload.results[].receivedPayment.date | Integer | 收款結帳款日 |  |
| payload.results[].receivedPayment.source | Integer | 收款方式 | 現金 (0)、匯款 (1)、支票 (2) |
| payload.results[].receivedPayment.period | Integer | 收款期 |  |
| payload.results[].receivedPayment.creationTime | Integer | 資料建立時間 |  |
| payload.results[].paidPayment.id | Integer | 付款帳款資料id |  |
| payload.results[].paidPayment.type | Integer | 付款類別 | 現結 (0)、月結 (1) |
| payload.results[].paidPayment.date | Integer | 付款結帳款日 |  |
| payload.results[].paidPayment.source | Integer | 付款方式 | 現金 (0)、匯款 (1)、支票 (2) |
| payload.results[].paidPayment.period | Integer | 付款期 |  |
| payload.results[].paidPayment.creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 company、payment 取得客戶/廠商基本資料與帳款資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供客戶/廠商基本資料 |
| payment | 提供客戶/廠商帳款資料 |
