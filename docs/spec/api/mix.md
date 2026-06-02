# mix API Group

> Source: `restserver/package/restserver/api/mix_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/mix/item](#get-api-v1-mix-item) | GET | 查詢混合品項 / 品項 | OK | OK |
| [/api/v1/mix/itemprice](#get-api-v1-mix-itemprice) | GET | 查詢混合品項 / 品項價格 | OK | OK |

## GET /api/v1/mix/item

<a id="get-api-v1-mix-item"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/mix/item | GET | 查詢混合品項 / 品項 |

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

1. 讀取查詢條件：count、start
2. 呼叫服務：CLogger.log、literal.label、union_all.subquery
3. 查詢或使用資料表：inproduct、inproduct_bom_spec、product、product_bom_spec、product_spec、product_ver
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| inproduct | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| inproduct_bom_spec | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| product | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| product_bom_spec | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| product_spec | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| product_ver | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## GET /api/v1/mix/itemprice

<a id="get-api-v1-mix-itemprice"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/mix/itemprice | GET | 查詢混合品項 / 品項價格 |

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
    "count": "Object",
    "results": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
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
3. 查詢或使用資料表：item_loss、item_price
4. 組裝回傳 payload 欄位：payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| item_loss | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| item_price | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
