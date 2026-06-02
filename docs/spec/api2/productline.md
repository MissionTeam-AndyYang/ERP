# productline API Group

> Source: `restserver/package/restserver/api/productline_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/productline](#get-api-v1-productline) | GET | 查詢產線 | OK | OK |
| [/api/v1/productline/equipment](#get-api-v1-productline-equipment) | GET | 查詢產線 / 設備 | OK | OK |
| [/api/v1/productline/factory](#get-api-v1-productline-factory) | GET | 查詢產線 / 廠區 | OK | OK |
| [/api/v1/productline/process](#get-api-v1-productline-process) | GET | 查詢產線 / 製程 | OK | OK |
| [/api/v1/productline/station](#get-api-v1-productline-station) | GET | 查詢產線 / 站點 | OK | OK |

## GET /api/v1/productline

<a id="get-api-v1-productline"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline | GET | 查詢產線 |

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

1. 呼叫服務：CLogger.log
2. 查詢或使用資料表：production_line
3. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| production_line | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## GET /api/v1/productline/equipment

<a id="get-api-v1-productline-equipment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline/equipment | GET | 查詢產線 / 設備 |

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

1. 呼叫服務：CLogger.log
2. 查詢或使用資料表：equipment
3. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| equipment | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## GET /api/v1/productline/factory

<a id="get-api-v1-productline-factory"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline/factory | GET | 查詢產線 / 廠區 |

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

1. 呼叫服務：CLogger.log
2. 查詢或使用資料表：factory
3. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| factory | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## GET /api/v1/productline/process

<a id="get-api-v1-productline-process"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline/process | GET | 查詢產線 / 製程 |

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

1. 呼叫服務：CLogger.log
2. 查詢或使用資料表：process
3. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| process | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## GET /api/v1/productline/station

<a id="get-api-v1-productline-station"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline/station | GET | 查詢產線 / 站點 |

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

1. 呼叫服務：CLogger.log
2. 查詢或使用資料表：station
3. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| station | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
