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
    "total": "Object",
    "results": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Object | 符合條件的總筆數 |  |
| payload.results | Object | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 呼叫服務：CLogger.log
2. 查詢或使用資料表：bank_account
3. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| bank_account | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
