# inventory API Group

> Source: `restserver/package/restserver/api/inventory_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/inventory](#get-api-v1-inventory) | GET | 查詢庫存 | OK | OK |
| [/api/v1/inventory/items](#get-api-v1-inventory-items) | GET | 查詢庫存 / 品項清單 | OK | OK |
| [/api/v1/inventory/months](#get-api-v1-inventory-months) | GET | 查詢庫存 / 月資料 | OK | OK |
| [/api/v1/inventory/price](#get-api-v1-inventory-price) | GET | 查詢庫存 / 價格 | OK | OK |
| [/api/v1/inventory/statistics](#get-api-v1-inventory-statistics) | GET | 查詢庫存 / 統計 | OK | OK |

## GET /api/v1/inventory

<a id="get-api-v1-inventory"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory | GET | 查詢庫存 |

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
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：batch_number、inventory_record、process_order
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| inventory_record | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| process_order | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## GET /api/v1/inventory/items

<a id="get-api-v1-inventory-items"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory/items | GET | 查詢庫存 / 品項清單 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| commit | String | NO | 是否提交/確認統計條件 |
| date | String | NO | 日期 |
| end_time | String | NO | 查詢結束時間 |
| itemCategory | String | NO | 料品類別 |
| item_no | String | NO | 料品/品項編號 |
| start_time | String | NO | 查詢開始時間 |
| type | String | NO | 類型篩選 |

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

1. 讀取查詢條件：commit、date、end_time、itemCategory、item_no、start_time、type
2. 呼叫服務：CInventoryDeltaBatchNo.calculate、CInventoryDeltaItem.calculate、CInventoryItemMonth.calculate、CInventoryItemMonth.retrieve_realTime、CLogger.log
3. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

None

## GET /api/v1/inventory/months

<a id="get-api-v1-inventory-months"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory/months | GET | 查詢庫存 / 月資料 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| end_time | String | NO | 查詢結束時間 |
| start_time | String | NO | 查詢開始時間 |

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

1. 讀取查詢條件：end_time、start_time
2. 呼叫服務：CInventoryMonth.retrieve、CLogger.log
3. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

None

## GET /api/v1/inventory/price

<a id="get-api-v1-inventory-price"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory/price | GET | 查詢庫存 / 價格 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |
| type | Integer | YES | 類型篩選 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "total": "Object",
    "results": "Object",
    "count": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Object | 符合條件的總筆數 |  |
| payload.results | Object | 查詢結果清單 |  |
| payload.count | Object | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：count、start、type
2. 呼叫服務：CLogger.log、selectinload.selectinload
3. 查詢或使用資料表：item_price、trans_items
4. 組裝回傳 payload 欄位：payload.total、payload.results、payload.count

### Database Tables Used

| Table | Purpose |
|----------|------|
| item_price | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| trans_items | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## GET /api/v1/inventory/statistics

<a id="get-api-v1-inventory-statistics"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory/statistics | GET | 查詢庫存 / 統計 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| batchNumber | String | YES | 批號 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "results": {
      "warehouse": []
    }
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.results.warehouse | Array | warehouse 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：batchNumber
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：inventory_record
4. 組裝回傳 payload 欄位：payload.results.warehouse

### Database Tables Used

| Table | Purpose |
|----------|------|
| inventory_record | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
