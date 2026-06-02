# aps API Group

> Source: `restserver/package/restserver/api/aps_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/aps/quantity](#get-api-v1-aps-quantity) | GET | 查詢APS 資料 / 製造需求數量 | OK | OK |

## GET /api/v1/aps/quantity

<a id="get-api-v1-aps-quantity"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/aps/quantity | GET | 查詢APS 資料 / 製造需求數量 |

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
    "results": "Object",
    "count": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.results | Object | 查詢結果清單 |  |
| payload.count | Object | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：aps_quantity、contract、product_order
4. 組裝回傳 payload 欄位：payload.total、payload.results、payload.count

### Database Tables Used

| Table | Purpose |
|----------|------|
| aps_quantity | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| contract | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| product_order | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
