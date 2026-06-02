# workorder API Group

> Source: `restserver/package/restserver/api/workorder_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/workorder](#get-api-v1-workorder) | GET | 查詢工單 | OK | OK |
| [/api/v1/workorder/expecteddata](#get-api-v1-workorder-expecteddata) | GET | 查詢工單 / 預期資料 | OK | OK |
| [/api/v1/workorder/productdata](#get-api-v1-workorder-productdata) | GET | 查詢工單 / 生產數據 | OK | OK |
| [/api/v1/workorder/statistics](#get-api-v1-workorder-statistics) | GET | 查詢工單 / 統計 | OK | OK |

## GET /api/v1/workorder

<a id="get-api-v1-workorder"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder | GET | 查詢工單 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

None

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

1. 呼叫服務：CLogger.log
2. 查詢或使用資料表：production_data_output、work_order
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| production_data_output | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| work_order | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## GET /api/v1/workorder/expecteddata

<a id="get-api-v1-workorder-expecteddata"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder/expecteddata | GET | 查詢工單 / 預期資料 |

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
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：batch_number、batchno_serialno、process_order、production_line、work_order
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| batchno_serialno | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| process_order | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| production_line | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| work_order | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## GET /api/v1/workorder/productdata

<a id="get-api-v1-workorder-productdata"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder/productdata | GET | 查詢工單 / 生產數據 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |
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

1. 讀取查詢條件：count、start、type
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：employee、production_line、station、work_order
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| employee | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| production_line | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| station | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| work_order | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## GET /api/v1/workorder/statistics

<a id="get-api-v1-workorder-statistics"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder/statistics | GET | 查詢工單 / 統計 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| commit | String | NO | 是否提交/確認統計條件 |
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

1. 讀取查詢條件：commit、end_time、start_time
2. 呼叫服務：CLogger.log、COrdersProcessMonth.calculate
3. 組裝回傳 payload 欄位：payload.count、payload.results

### Database Tables Used

None
