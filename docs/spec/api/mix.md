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
2. 查詢資料表並套用條件：inproduct、inproduct_bom_spec、product、product_bom_spec、product_spec、product_ver
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| inproduct | 提供混合品項主檔、配方或價格資料 |
| inproduct_bom_spec | 提供混合品項主檔、配方或價格資料 |
| product | 提供混合品項主檔、配方或價格資料 |
| product_bom_spec | 提供混合品項主檔、配方或價格資料 |
| product_spec | 提供混合品項主檔、配方或價格資料 |
| product_ver | 提供混合品項主檔、配方或價格資料 |

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
    "count": "Integer",
    "results": "Need Review"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results | Need Review | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：item_no
2. 查詢資料表並套用條件：item_loss、item_price
3. 組裝回傳 payload 欄位：payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| item_loss | 提供混合品項主檔、配方或價格資料 |
| item_price | 提供混合品項主檔、配方或價格資料 |
