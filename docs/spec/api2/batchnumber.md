# batchnumber API Group

> Source: `restserver/package/restserver/api/batchnumber_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/batchnumber](#get-api-v1-batchnumber) | GET | 查詢批號 | OK | OK |

## GET /api/v1/batchnumber

<a id="get-api-v1-batchnumber"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/batchnumber | GET | 查詢批號 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | String | NO | 分頁筆數 |
| info | String | NO | 附加資訊類型 |
| start | String | NO | 分頁起始位置 |
| type | String | NO | 類型篩選 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "total": "Integer",
    "count": "Object",
    "results": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.count | Object | 本次回傳筆數 |  |
| payload.results | Object | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：count、info、start、type
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：batch_number
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
