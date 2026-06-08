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
    "results": [
      {
        "month": "String",
        "pl_no": "String",
        "pl_name": "String",
        "productCount": "Integer",
        "item_no": "String",
        "item_name": "String",
        "assembly_no": "String",
        "assemblyVer": "Integer",
        "bomWeight": "Float",
        "bomUnit": "Integer",
        "unit": "Integer",
        "hourlyOutput": "Float"
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
| payload.results[].month | String | 月份 |  |
| payload.results[].pl_no | String | 產線no，關聯至production_line資料表 |  |
| payload.results[].pl_name | String | 產線名稱，關聯至production_line資料表 |  |
| payload.results[].productCount | Integer | 產製次數 |  |
| payload.results[].item_no | String | 「料品品項」編號 |  |
| payload.results[].item_name | String | 「料品品項」名稱 |  |
| payload.results[].assembly_no | String | 產出「料品品項」組裝編號 |  |
| payload.results[].assemblyVer | Integer | 產出「料品品項」組裝版本 |  |
| payload.results[].bomWeight | Float | 產出「料品品項」Bom重量 |  |
| payload.results[].bomUnit | Integer | 產出「料品品項」成分單位 |  |
| payload.results[].unit | String | 單位 |  |
| payload.results[].hourlyOutput | Float | 產出物時產量 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 pl_item_capacity 取得產線統計 / 品項產能資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
    "results": [
      {
        "month": "String",
        "pl_no": "String",
        "pl_name": "String",
        "productCount": "Integer",
        "item_no": "String",
        "item_name": "String",
        "assembly_no": "String",
        "assemblyVer": "Integer",
        "price": "Float",
        "rawMaterialCost": "Float",
        "materialCost": "Float",
        "laborCost": "Float"
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
| payload.results[].month | String | 月份 |  |
| payload.results[].pl_no | String | 產線no，關聯至production_line資料表 |  |
| payload.results[].pl_name | String | 產線名稱，關聯至production_line資料表 |  |
| payload.results[].productCount | Integer | 產製次數 |  |
| payload.results[].item_no | String | 「料品品項」編號 |  |
| payload.results[].item_name | String | 「料品品項」名稱 |  |
| payload.results[].assembly_no | String | 產出「料品品項」組裝編號 |  |
| payload.results[].assemblyVer | Integer | 產出「料品品項」組裝版本 |  |
| payload.results[].price | Float | 單價 |  |
| payload.results[].rawMaterialCost | Float | 原料費 |  |
| payload.results[].materialCost | Float | 物料費 |  |
| payload.results[].laborCost | Float | 人工費 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 pl_item_capacity 取得產線統計 / 品項成本資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
    "results": [
      {
        "id": "Integer",
        "month": "String",
        "pl_item_capacity_no": "String",
        "item_no": "String",
        "item_name": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "weightRatio": "Float",
        "lossRate": "Float",
        "creationTime": "Integer",
        "output": {
          "pl_no": "String",
          "pl_name": "String",
          "productCount": "Integer",
          "item_no": "String",
          "item_name": "String",
          "assembly_no": "String",
          "assemblyVer": "Integer",
          "bomWeight": "Float",
          "bomUnit": "Integer"
        }
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
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].month | String | 月份 |  |
| payload.results[].pl_item_capacity_no | String | 產線料品產能，關聯至pl_item_capacity資料表 |  |
| payload.results[].item_no | String | 投入「料品品項」編號 |  |
| payload.results[].item_name | String | 投入「料品品項」名稱 |  |
| payload.results[].itemCategory | Integer | 投入「料品品項」類別 |  |
| payload.results[].itemSubCategory | Integer | 投入「料品品項」子類別 |  |
| payload.results[].weightRatio | Float | 投入物之產重比 |  |
| payload.results[].lossRate | Float | 投入物之損耗率 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |
| payload.results[].output.pl_no | String | 產線no，關聯至production_line資料表 |  |
| payload.results[].output.pl_name | String | 產線名稱，關聯至production_line資料表 |  |
| payload.results[].output.productCount | Integer | 產製次數 |  |
| payload.results[].output.item_no | String | 產出「料品品項」編號 |  |
| payload.results[].output.item_name | String | 產出「料品品項」名稱 |  |
| payload.results[].output.assembly_no | String | 產出「料品品項」組裝編號 |  |
| payload.results[].output.assemblyVer | Integer | 產出「料品品項」組裝版本 |  |
| payload.results[].output.bomWeight | Float | 產出「料品品項」Bom重量 |  |
| payload.results[].output.bomUnit | Integer | 產出「料品品項」成分單位 |  |
### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 pl_item_capacity、pl_item_loss 取得產線統計 / 品項損耗資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
    "results": [
      {
        "id": "Integer",
        "month": "String",
        "pl_no": "String",
        "pl_name": "String",
        "productCount": "Integer",
        "laborCount": "Integer",
        "unit": "Integer",
        "hourlyOutput": "Float",
        "creationTime": "Integer"
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
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].month | String | 月份 |  |
| payload.results[].pl_no | String | 產線no，關聯至production_line資料表 |  |
| payload.results[].pl_name | String | 產線名稱，關聯至production_line資料表 |  |
| payload.results[].productCount | Integer | 產製次數 |  |
| payload.results[].laborCount | Integer | 人力需求數 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].hourlyOutput | Float | 產出物時產量 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 pl_man_capacity 取得產線統計 / 人力產能資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| pl_man_capacity | 提供產線統計排程、生產或產能資料 |
