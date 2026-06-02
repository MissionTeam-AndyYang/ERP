# quotation API Group

> Source: `restserver/package/restserver/api/quotation_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/quotation](#get-api-v1-quotation) | GET | 查詢報價 | OK | OK |

## GET /api/v1/quotation

<a id="get-api-v1-quotation"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/quotation | GET | 查詢報價 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |
| type | Integer | NO | 類型篩選 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "total": "Integer",
    "results": "Need Review",
    "count": "Integer"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.results | Need Review | 查詢結果清單 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start、type
2. 組裝回傳 payload 欄位：payload.total、payload.results、payload.count

### Database Tables Used

None
