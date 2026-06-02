# work API Group

> Source: `restserver/package/restserver/api/work_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/work/assignment](#get-api-v1-work-assignment) | GET | 查詢製造作業 / 作業分派 | OK | OK |
| [/api/v1/work/process](#get-api-v1-work-process) | GET | 查詢製造作業 / 製程 | OK | OK |
| [/api/v1/work/process](#post-api-v1-work-process) | POST | 新增製造作業 / 製程 | OK | OK |
| [/api/v1/work/productdata](#get-api-v1-work-productdata) | GET | 查詢製造作業 / 生產數據 | OK | OK |
| [/api/v1/work/progress](#get-api-v1-work-progress) | GET | 查詢製造作業 / 作業進度 | OK | OK |

## GET /api/v1/work/assignment

<a id="get-api-v1-work-assignment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/assignment | GET | 查詢製造作業 / 作業分派 |

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
3. 查詢或使用資料表：batch_number、batchno_serialno、equipment、process_labor、process_order、production_line、station、work_order
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| batchno_serialno | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| equipment | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| process_labor | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| process_order | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| production_line | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| station | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| work_order | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## GET /api/v1/work/process

<a id="get-api-v1-work-process"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/process | GET | 查詢製造作業 / 製程 |

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
    "results": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
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
3. 查詢或使用資料表：batch_number、process_order
4. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| process_order | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## POST /api/v1/work/process

<a id="post-api-v1-work-process"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/process | POST | 新增製造作業 / 製程 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

```json
{
  "start_time": "Integer",
  "end_time": "Integer"
}
```

| Field Path | Type | Required | Description | Enum |
|----------|----------|------|-----|---|
| start_time | Integer | YES | 查詢開始時間 |  |
| end_time | Integer | YES | 查詢結束時間 |  |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 驗證 request body 欄位：start_time、end_time
2. 呼叫服務：CCProcessOrder.gen_process_order、CLogger.log
3. 查詢或使用資料表：work_order

### Database Tables Used

| Table | Purpose |
|----------|------|
| work_order | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## GET /api/v1/work/productdata

<a id="get-api-v1-work-productdata"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/productdata | GET | 查詢製造作業 / 生產數據 |

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

## GET /api/v1/work/progress

<a id="get-api-v1-work-progress"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/progress | GET | 查詢製造作業 / 作業進度 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| oneProcess | String | YES | 主製程 |
| product_order_no | String | YES | 訂購單號 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "results": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.results | Object | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：oneProcess、product_order_no
2. 呼叫服務：CLaborHours.get、CLogger.log、case.label
3. 查詢或使用資料表：aps_quantity、inproduct、product、production_data、production_data_output
4. 組裝回傳 payload 欄位：payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| aps_quantity | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| inproduct | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| product | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| production_data | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| production_data_output | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
