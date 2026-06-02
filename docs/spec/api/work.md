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

1. 讀取查詢條件：count、start
2. 查詢資料表並套用條件：batch_number、batchno_serialno、equipment、process_labor、process_order、production_line、station、work_order
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供製造作業排程、生產或產能資料 |
| batchno_serialno | 提供製造作業排程、生產或產能資料 |
| equipment | 提供製造作業排程、生產或產能資料 |
| process_labor | 提供製造作業排程、生產或產能資料 |
| process_order | 提供製造作業排程、生產或產能資料 |
| production_line | 提供製造作業排程、生產或產能資料 |
| station | 提供製造作業排程、生產或產能資料 |
| work_order | 提供製造作業排程、生產或產能資料 |

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
    "results": "Need Review"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.results | Need Review | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 查詢資料表並套用條件：batch_number、process_order
3. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供製造作業排程、生產或產能資料 |
| process_order | 提供製造作業排程、生產或產能資料 |

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
  "payload": "Need Review"
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload | Need Review | 程式回傳空 payload 物件，無子欄位可展開 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 驗證 request body 欄位：start_time、end_time
2. 查詢資料表並套用條件：work_order

### Database Tables Used

| Table | Purpose |
|----------|------|
| work_order | 提供製造作業排程、生產或產能資料 |

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

1. 讀取查詢條件：count、start、type
2. 查詢資料表並套用條件：employee、production_line、station、work_order
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| employee | 提供製造作業排程、生產或產能資料 |
| production_line | 提供製造作業排程、生產或產能資料 |
| station | 提供製造作業排程、生產或產能資料 |
| work_order | 提供製造作業排程、生產或產能資料 |

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
    "results": "Need Review"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.results | Need Review | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：oneProcess、product_order_no
2. 查詢資料表並套用條件：aps_quantity、inproduct、product、production_data、production_data_output
3. 組裝回傳 payload 欄位：payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| aps_quantity | 提供製造作業排程、生產或產能資料 |
| inproduct | 提供製造作業排程、生產或產能資料 |
| product | 提供製造作業排程、生產或產能資料 |
| production_data | 提供製造作業排程、生產或產能資料 |
| production_data_output | 提供製造作業排程、生產或產能資料 |
