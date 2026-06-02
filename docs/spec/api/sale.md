# sale API Group

> Source: `restserver/package/restserver/api/sale_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/sale/arap](#get-api-v1-sale-arap) | GET | 查詢銷售 / 應收應付 | OK | OK |
| [/api/v1/sale/contract](#get-api-v1-sale-contract) | GET | 查詢銷售 / 合約 | OK | OK |
| [/api/v1/sale/payment](#get-api-v1-sale-payment) | GET | 查詢銷售 / 帳款 | OK | OK |
| [/api/v1/sale/productorder](#get-api-v1-sale-productorder) | GET | 查詢銷售 / 訂購單 | OK | OK |
| [/api/v1/sale/shippingorder](#get-api-v1-sale-shippingorder) | GET | 查詢銷售 / 銷貨單 | OK | OK |
| [/api/v1/sale/statistics](#get-api-v1-sale-statistics) | GET | 查詢銷售 / 統計 | OK | OK |

## GET /api/v1/sale/arap

<a id="get-api-v1-sale-arap"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/sale/arap | GET | 查詢銷售 / 應收應付 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| order_no | String | YES | 訂單編號 |

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

1. 讀取查詢條件：order_no
2. 查詢資料表並套用條件：shipping_order
3. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| shipping_order | 提供銷售單據、合約、帳款或統計資料 |

## GET /api/v1/sale/contract

<a id="get-api-v1-sale-contract"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/sale/contract | GET | 查詢銷售 / 合約 |

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
2. 組裝回傳 payload 欄位：payload.total、payload.results、payload.count

### Database Tables Used

None

## GET /api/v1/sale/payment

<a id="get-api-v1-sale-payment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/sale/payment | GET | 查詢銷售 / 帳款 |

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
2. 查詢資料表並套用條件：contract、order_payment、product_order、shipping_order
3. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| contract | 提供銷售單據、合約、帳款或統計資料 |
| order_payment | 提供銷售單據、合約、帳款或統計資料 |
| product_order | 提供銷售單據、合約、帳款或統計資料 |
| shipping_order | 提供銷售單據、合約、帳款或統計資料 |

## GET /api/v1/sale/productorder

<a id="get-api-v1-sale-productorder"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/sale/productorder | GET | 查詢銷售 / 訂購單 |

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
    "sum": {
      "amount": "Integer",
      "realAmount": "Integer",
      "returnAmount": "Integer",
      "itemCategoryAmount": "Need Review"
    },
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
| payload.sum.amount | Integer | amount 回傳欄位 |  |
| payload.sum.realAmount | Integer | realAmount 回傳欄位 |  |
| payload.sum.returnAmount | Integer | returnAmount 回傳欄位 |  |
| payload.sum.itemCategoryAmount | Need Review | itemCategoryAmount 回傳欄位 |  |
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
2. 查詢資料表並套用條件：contract、product_order、shipping_order
3. 組裝回傳 payload 欄位：payload.sum.amount、payload.sum.realAmount、payload.sum.returnAmount、payload.sum.itemCategoryAmount、payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| contract | 提供銷售單據、合約、帳款或統計資料 |
| product_order | 提供銷售單據、合約、帳款或統計資料 |
| shipping_order | 提供銷售單據、合約、帳款或統計資料 |

## GET /api/v1/sale/shippingorder

<a id="get-api-v1-sale-shippingorder"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/sale/shippingorder | GET | 查詢銷售 / 銷貨單 |

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
    "sum": {
      "amount": "Integer",
      "returnAmount": "Integer"
    },
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
| payload.sum.amount | Integer | amount 回傳欄位 |  |
| payload.sum.returnAmount | Integer | returnAmount 回傳欄位 |  |
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
2. 查詢資料表並套用條件：batch_number、inventory_record、product_order、shipping_order
3. 組裝回傳 payload 欄位：payload.sum.amount、payload.sum.returnAmount、payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供銷售單據、合約、帳款或統計資料 |
| inventory_record | 提供銷售單據、合約、帳款或統計資料 |
| product_order | 提供銷售單據、合約、帳款或統計資料 |
| shipping_order | 提供銷售單據、合約、帳款或統計資料 |

## GET /api/v1/sale/statistics

<a id="get-api-v1-sale-statistics"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/sale/statistics | GET | 查詢銷售 / 統計 |

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

1. 讀取查詢條件：commit、end_time、start_time
2. 組裝回傳 payload 欄位：payload.count、payload.results

### Database Tables Used

None
