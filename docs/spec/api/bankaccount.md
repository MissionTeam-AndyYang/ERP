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
| payload.results[].category | Integer | 類別 |  |
| payload.results[].currency | Integer | 幣別 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].branch | String | 銀行分行 |  |
| payload.results[].account | String | 銀行帳戶名稱 |  |
| payload.results[].number | String | 銀行帳號 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 查詢 bank_account 取得銀行帳戶資料
2. 計算符合條件的總筆數與本次回傳筆數
3. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| bank_account | 提供銀行帳戶相關資料 |
