# bom API Group

> Source: `restserver/package/restserver/api/bom_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/bom](#get-api-v1-bom) | GET | 查詢BOM | OK | OK |
| [/api/v1/bom/aps](#get-api-v1-bom-aps) | GET | 查詢BOM / APS 資料 | OK | OK |
| [/api/v1/bom/process](#get-api-v1-bom-process) | GET | 查詢BOM / 製程 | OK | OK |
| [/api/v1/bom/tree](#get-api-v1-bom-tree) | GET | 查詢BOM / 樹狀資料 | OK | OK |

## GET /api/v1/bom

<a id="get-api-v1-bom"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/bom | GET | 查詢BOM |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
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
2. 查詢資料表並套用條件：bom、sample_price
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| bom | 提供BOM主檔、配方或價格資料 |
| sample_price | 提供BOM主檔、配方或價格資料 |

## GET /api/v1/bom/aps

<a id="get-api-v1-bom-aps"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/bom/aps | GET | 查詢BOM / APS 資料 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| order_no | String | NO | 訂單編號 |
| product_no | String | NO | 製成品編號 |

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

1. 讀取查詢條件：order_no、product_no
2. 查詢資料表並套用條件：product_order
3. 組裝回傳 payload 欄位：payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| product_order | 提供BOM主檔、配方或價格資料 |

## GET /api/v1/bom/process

<a id="get-api-v1-bom-process"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/bom/process | GET | 查詢BOM / 製程 |

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
    "results": "Need Review",
    "count": "Integer"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.results | Need Review | 查詢結果清單 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 查詢資料表並套用條件：product_process
3. 組裝回傳 payload 欄位：payload.total、payload.results、payload.count

### Database Tables Used

| Table | Purpose |
|----------|------|
| product_process | 提供BOM主檔、配方或價格資料 |

## GET /api/v1/bom/tree

<a id="get-api-v1-bom-tree"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/bom/tree | GET | 查詢BOM / 樹狀資料 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| product_no | String | NO | 製成品編號 |

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

1. 讀取查詢條件：product_no
2. 查詢資料表並套用條件：product
3. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| product | 提供BOM主檔、配方或價格資料 |
