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
        "company": {},
        "paidPayment": {},
        "receivedPayment": {}
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

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 查詢資料表並套用條件：company、payment
3. 組裝回傳 payload 欄位：payload.total、payload.count

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供客戶/廠商相關資料 |
| payment | 提供客戶/廠商相關資料 |
