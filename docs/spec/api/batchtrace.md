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

1. 讀取查詢條件：inventoryType、orderCategory、type
2. 查詢資料表並套用條件：batch_number、goods_receipt_note、inventory_record、production_data、production_data_output
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 追蹤批號來源、庫存、生產與出入庫關聯 |
| goods_receipt_note | 追蹤批號來源、庫存、生產與出入庫關聯 |
| inventory_record | 追蹤批號來源、庫存、生產與出入庫關聯 |
| production_data | 追蹤批號來源、庫存、生產與出入庫關聯 |
| production_data_output | 追蹤批號來源、庫存、生產與出入庫關聯 |

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
    "stock": "Need Review",
    "nonWork": "Need Review",
    "work": "Need Review"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.stock | Need Review | 批號庫存資訊 |  |
| payload.nonWork | Need Review | 非生產來源追蹤資料 |  |
| payload.work | Need Review | 生產來源追蹤資料 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：itemCategory、no
2. 查詢資料表並套用條件：production_data、production_data_input、production_data_output
3. 組裝回傳 payload 欄位：payload.stock、payload.nonWork、payload.work

### Database Tables Used

| Table | Purpose |
|----------|------|
| production_data | 追蹤批號來源、庫存、生產與出入庫關聯 |
| production_data_input | 追蹤批號來源、庫存、生產與出入庫關聯 |
| production_data_output | 追蹤批號來源、庫存、生產與出入庫關聯 |
