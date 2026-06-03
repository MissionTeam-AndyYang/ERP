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
    "results": [
      {
        "no": "String",
        "name": "String",
        "category": "String",
        "subCategory": "String",
        "unitWarehouse": "String",
        "unitProduct": "String",
        "bom": "String"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].category | String | 類別 |  |
| payload.results[].subCategory | String | 子類別 |  |
| payload.results[].unitWarehouse | String | 倉儲單位 |  |
| payload.results[].unitProduct | String | 產製單位 |  |
| payload.results[].bom | String | bom 的業務資料 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 inproduct、inproduct_bom_spec、product、product_bom_spec 取得混合品項 / 品項資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
| payload.results[].month | String | 月份 |  |
| payload.results[].estUnit | String | est Unit 的業務資料 |  |
| payload.results[].estPrice | String | est Price 的業務資料 |  |
| payload.results[].estPrice1 | String | est Price1 的業務資料 |  |
| payload.results[].estPrice2 | String | est Price2 的業務資料 |  |
| payload.results[].estLaborCost | String | 預估人工費 |  |
| payload.results[].unit | String | 單位 |  |
| payload.results[].price | String | 單價 |  |
| payload.results[].price1 | String | price1 的業務資料 |  |
| payload.results[].price2 | String | price2 的業務資料 |  |
| payload.results[].laborCost | String | 人工費 |  |
| payload.results[].lossUnit | String | loss Unit 的業務資料 |  |
| payload.results[].loss | String | loss 的業務資料 |  |
| payload.results[].estLoss | String | est Loss 的業務資料 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：item_no
2. 查詢 item_loss、item_price 取得混合品項 / 品項價格資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| item_loss | 提供混合品項主檔、配方或價格資料 |
| item_price | 提供混合品項主檔、配方或價格資料 |
