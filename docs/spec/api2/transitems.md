# transitems API Group

> Source: `restserver/package/restserver/api/transitems_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/transitems](#get-api-v1-transitems) | GET | 查詢交易品項 | OK | OK |
| [/api/v1/transitems/item](#get-api-v1-transitems-item) | GET | 查詢交易品項 / 品項 | OK | OK |

## GET /api/v1/transitems

<a id="get-api-v1-transitems"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/transitems | GET | 查詢交易品項 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| category | Integer | NO | 類別篩選 |
| count | String | NO | 分頁筆數 |
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

1. 讀取查詢條件：category、count、start、type
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：company、payment、trans_items、trans_items2
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| payment | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| trans_items | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| trans_items2 | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## GET /api/v1/transitems/item

<a id="get-api-v1-transitems-item"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/transitems/item | GET | 查詢交易品項 / 品項 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| item_no | String | YES | 料品/品項編號 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "total": "Object",
    "count": "Object",
    "results": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Object | 符合條件的總筆數 |  |
| payload.count | Object | 本次回傳筆數 |  |
| payload.results | Object | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：item_no
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：company、payment、trans_items
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| payment | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| trans_items | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
