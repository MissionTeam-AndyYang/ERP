# material API Group

> Source: `restserver/package/restserver/api/material_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/material](#get-api-v1-material) | GET | 查詢原物料 | OK | OK |
| [/api/v1/material/itemprice](#get-api-v1-material-itemprice) | GET | 查詢原物料 / 品項價格 | OK | OK |

## GET /api/v1/material

<a id="get-api-v1-material"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/material | GET | 查詢原物料 |

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
    "results": [
      {
        "id": "String",
        "no": "String",
        "name": "String"
      }
    ],
    "count": "Integer"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.results[].id | String | 資料 ID |  |
| payload.results[].no | String | 編號篩選 |  |
| payload.results[].name | String | 名稱 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start、type
2. 查詢資料表並套用條件：material
3. 組裝回傳 payload 欄位：payload.total、payload.results[].id、payload.results[].no、payload.results[].name、payload.count

### Database Tables Used

| Table | Purpose |
|----------|------|
| material | 提供原物料主檔、配方或價格資料 |

## GET /api/v1/material/itemprice

<a id="get-api-v1-material-itemprice"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/material/itemprice | GET | 查詢原物料 / 品項價格 |

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
    "results": [
      {
        "month": "String",
        "estUnit": "String",
        "estPrice": "String",
        "estPrice1": "String",
        "estPrice2": "String",
        "estLaborCost": "String",
        "unit": "String",
        "price": "String",
        "price1": "String",
        "price2": "String",
        "laborCost": "String",
        "lossUnit": "String",
        "loss": "String",
        "estLoss": "String"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].month | String | month 回傳欄位 |  |
| payload.results[].estUnit | String | estUnit 回傳欄位 |  |
| payload.results[].estPrice | String | estPrice 回傳欄位 |  |
| payload.results[].estPrice1 | String | estPrice1 回傳欄位 |  |
| payload.results[].estPrice2 | String | estPrice2 回傳欄位 |  |
| payload.results[].estLaborCost | String | estLaborCost 回傳欄位 |  |
| payload.results[].unit | String | unit 回傳欄位 |  |
| payload.results[].price | String | price 回傳欄位 |  |
| payload.results[].price1 | String | price1 回傳欄位 |  |
| payload.results[].price2 | String | price2 回傳欄位 |  |
| payload.results[].laborCost | String | laborCost 回傳欄位 |  |
| payload.results[].lossUnit | String | lossUnit 回傳欄位 |  |
| payload.results[].loss | String | loss 回傳欄位 |  |
| payload.results[].estLoss | String | estLoss 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：item_no
2. 查詢資料表並套用條件：item_loss、item_price
3. 組裝回傳 payload 欄位：payload.count、payload.results[].month、payload.results[].estUnit、payload.results[].estPrice、payload.results[].estPrice1、payload.results[].estPrice2、payload.results[].estLaborCost、payload.results[].unit、payload.results[].price、payload.results[].price1、payload.results[].price2、payload.results[].laborCost、payload.results[].lossUnit、payload.results[].loss、payload.results[].estLoss

### Database Tables Used

| Table | Purpose |
|----------|------|
| item_loss | 提供原物料主檔、配方或價格資料 |
| item_price | 提供原物料主檔、配方或價格資料 |
