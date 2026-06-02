# plstatistics API Group

> Source: `restserver/package/restserver/api/plstatistics_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/plstatistics/itemcapacity](#get-api-v1-plstatistics-itemcapacity) | GET | 查詢產線統計 / 品項產能 | OK | OK |
| [/api/v1/plstatistics/itemcost](#get-api-v1-plstatistics-itemcost) | GET | 查詢產線統計 / 品項成本 | OK | OK |
| [/api/v1/plstatistics/itemloss](#get-api-v1-plstatistics-itemloss) | GET | 查詢產線統計 / 品項損耗 | OK | OK |
| [/api/v1/plstatistics/mancapacity](#get-api-v1-plstatistics-mancapacity) | GET | 查詢產線統計 / 人力產能 | OK | OK |

## GET /api/v1/plstatistics/itemcapacity

<a id="get-api-v1-plstatistics-itemcapacity"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/plstatistics/itemcapacity | GET | 查詢產線統計 / 品項產能 |

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
2. 查詢資料表並套用條件：pl_item_capacity
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| pl_item_capacity | 提供產線統計排程、生產或產能資料 |

## GET /api/v1/plstatistics/itemcost

<a id="get-api-v1-plstatistics-itemcost"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/plstatistics/itemcost | GET | 查詢產線統計 / 品項成本 |

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
2. 查詢資料表並套用條件：pl_item_capacity
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| pl_item_capacity | 提供產線統計排程、生產或產能資料 |

## GET /api/v1/plstatistics/itemloss

<a id="get-api-v1-plstatistics-itemloss"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/plstatistics/itemloss | GET | 查詢產線統計 / 品項損耗 |

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
2. 查詢資料表並套用條件：pl_item_capacity、pl_item_loss
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| pl_item_capacity | 提供產線統計排程、生產或產能資料 |
| pl_item_loss | 提供產線統計排程、生產或產能資料 |

## GET /api/v1/plstatistics/mancapacity

<a id="get-api-v1-plstatistics-mancapacity"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/plstatistics/mancapacity | GET | 查詢產線統計 / 人力產能 |

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
2. 查詢資料表並套用條件：pl_man_capacity
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| pl_man_capacity | 提供產線統計排程、生產或產能資料 |
