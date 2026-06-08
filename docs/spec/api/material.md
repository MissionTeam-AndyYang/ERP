# material API Group

> Source: `restserver/package/restserver/api/material_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/material](#get-api-v1-material) | GET | 查詢原物料 | OK | OK |
| [/api/v1/material/itemprice](#get-api-v1-material-itemprice) | GET | 查詢原物料價格 | OK | OK |

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
        "id": "Integer",
        "no": "String",
        "name": "String",
        "category": "Integer",
        "subCategory": "Integer",
        "unitShipping": "Integer",
        "unitWarehouse": "Integer",
        "unitProduct": "Integer",
        "comment": "String",
        "creationTime": "Integer"
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
| payload.results[].no | String | 原物料編號 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].category | Integer | 類型 |  |
| payload.results[].subCategory | Integer | 子類型 | 原料餅體 (1)、拌料 (2)、餡料 (3)、巧克力 (4)、其他 (0)<br>物料紙盒 (1)、紙袋 (2)、塑盒 (3)、塑袋 (4)、鐵盒桶 (5)、外箱 (6)、 膠帶 (7)、膠膜 (8)、內襯 (9) 、環保稅 (10)、其他 (0)<br>膠捲膠捲 (1)、其他 (0)  |
| payload.results[].unitShipping | Integer | 貨運單位 |  |
| payload.results[].unitWarehouse | Integer | 倉儲單位 |  |
| payload.results[].unitProduct | Integer | 	產製單位 |  |
| payload.results[].comment | String | 備註 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start、type
2. 查詢 material 取得原物料資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| material | 提供原物料主檔、配方或價格資料 |

## GET /api/v1/material/itemprice

<a id="get-api-v1-material-itemprice"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/material/itemprice | GET | 查詢原物料價格 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| item_no | String | YES | 「料品品項」編號 |

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
        "estUnit": "Integer",
        "estPrice": "Float",      
        "unit": "Integer",
        "price": "Float",     
        "lossUnit": "Integer",
        "loss": "Float",
        "estLoss": "Float"
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
| payload.results[].estUnit | Integer | 預估成本重量單位 |  |
| payload.results[].estPrice | Float |預估成本重量單位價格 |  |
| payload.results[].unit | Integer | 成本重量單位 |  |
| payload.results[].price | Float | 成本重量單位價格 |  |
| payload.results[].lossUnit | Integer |  損耗單位 |  |
| payload.results[].loss | Float | 損耗比率 |  |
| payload.results[].estLoss | Float | 預估損耗比率 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：item_no
2. 查詢 item_loss、item_price 取得原物料價格與損耗資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| item_loss | 提供原物料損耗資料 |
| item_price | 提供原物料價格資料 |
