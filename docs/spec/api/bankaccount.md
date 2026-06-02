# bankaccount API Group

> Source: `restserver/package/restserver/api/bankaccount_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/bankaccount](#get-api-v1-bankaccount) | GET | 查詢銀行帳戶 | OK | OK |

## GET /api/v1/bankaccount

<a id="get-api-v1-bankaccount"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/bankaccount | GET | 查詢銀行帳戶 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

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
    "total": "Integer",
    "results": [
      {
        "id": "Integer",
        "category": "Integer",
        "currency": "Integer",
        "displayName": "String",
        "name": "String",
        "branch": "String",
        "account": "String",
        "number": "String",
        "creationTime": "Integer"
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
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].category | Integer | 類別篩選 |  |
| payload.results[].currency | Integer | currency 回傳欄位 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].branch | String | branch 回傳欄位 |  |
| payload.results[].account | String | account 回傳欄位 |  |
| payload.results[].number | String | number 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 查詢資料表並套用條件：bank_account
2. 組裝回傳 payload 欄位：payload.total、payload.results[].id、payload.results[].category、payload.results[].currency、payload.results[].displayName、payload.results[].name、payload.results[].branch、payload.results[].account、payload.results[].number、payload.results[].creationTime

### Database Tables Used

| Table | Purpose |
|----------|------|
| bank_account | 提供銀行帳戶相關資料 |
