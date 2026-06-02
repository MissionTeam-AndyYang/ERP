# goods API Group

> Source: `restserver/package/restserver/api/goods_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/goods](#get-api-v1-goods) | GET | 查詢貨品 | OK | OK |

## GET /api/v1/goods

<a id="get-api-v1-goods"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/goods | GET | 查詢貨品 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |

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
    "results": "Need Review"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results | Need Review | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 查詢資料表並套用條件：goods
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| goods | 提供貨品主檔、配方或價格資料 |
