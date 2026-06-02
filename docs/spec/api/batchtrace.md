# batchtrace API Group

> Source: `restserver/package/restserver/api/batchtrace_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/batchtrace](#get-api-v1-batchtrace) | GET | 查詢批號追蹤 | OK | OK |
| [/api/v1/batchtrace/record](#get-api-v1-batchtrace-record) | GET | 查詢批號追蹤 / 紀錄 | OK | OK |

## GET /api/v1/batchtrace

<a id="get-api-v1-batchtrace"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/batchtrace | GET | 查詢批號追蹤 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| inventoryType | String | NO | 庫存異動類型 |
| orderCategory | String | NO | 訂單類別 |
| type | String | YES | 類型篩選 |

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

1. 讀取查詢條件：inventoryType、orderCategory、type
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：batch_number、goods_receipt_note、inventory_record、production_data、production_data_output
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| goods_receipt_note | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| inventory_record | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| production_data | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| production_data_output | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## GET /api/v1/batchtrace/record

<a id="get-api-v1-batchtrace-record"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/batchtrace/record | GET | 查詢批號追蹤 / 紀錄 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| itemCategory | String | YES | 料品類別 |
| no | String | YES | 編號篩選 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "stock": "Object",
    "nonWork": "Object",
    "work": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.stock | Object | 批號庫存資訊 |  |
| payload.nonWork | Object | 非生產來源追蹤資料 |  |
| payload.work | Object | 生產來源追蹤資料 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：itemCategory、no
2. 呼叫服務：CCStockByBatchNo.get、CLogger.log
3. 查詢或使用資料表：production_data、production_data_input、production_data_output
4. 組裝回傳 payload 欄位：payload.stock、payload.nonWork、payload.work

### Database Tables Used

| Table | Purpose |
|----------|------|
| production_data | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| production_data_input | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| production_data_output | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
