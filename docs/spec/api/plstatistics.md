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
        "productCount": "String",
        "item_no": "String",
        "item_name": "String",
        "assembly_no": "String",
        "assemblyVer": "String",
        "bomWeight": "String",
        "bomUnit": "String",
        "unit": "String",
        "hourlyOutput": "String"
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
| payload.results[].month | String | month 回傳欄位 |  |
| payload.results[].pl_no | String | pl_no 回傳欄位 |  |
| payload.results[].pl_name | String | pl_name 回傳欄位 |  |
| payload.results[].productCount | String | productCount 回傳欄位 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].assembly_no | String | assembly_no 回傳欄位 |  |
| payload.results[].assemblyVer | String | assemblyVer 回傳欄位 |  |
| payload.results[].bomWeight | String | bomWeight 回傳欄位 |  |
| payload.results[].bomUnit | String | bomUnit 回傳欄位 |  |
| payload.results[].unit | String | unit 回傳欄位 |  |
| payload.results[].hourlyOutput | String | hourlyOutput 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 查詢資料表並套用條件：pl_item_capacity
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results[].month、payload.results[].pl_no、payload.results[].pl_name、payload.results[].productCount、payload.results[].item_no、payload.results[].item_name、payload.results[].assembly_no、payload.results[].assemblyVer、payload.results[].bomWeight、payload.results[].bomUnit、payload.results[].unit、payload.results[].hourlyOutput

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
        "productCount": "String",
        "item_no": "String",
        "item_name": "String",
        "assembly_no": "String",
        "assemblyVer": "String",
        "price": "String",
        "rawMaterialCost": "String",
        "materialCost": "String",
        "laborCost": "String"
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
| payload.results[].month | String | month 回傳欄位 |  |
| payload.results[].pl_no | String | pl_no 回傳欄位 |  |
| payload.results[].pl_name | String | pl_name 回傳欄位 |  |
| payload.results[].productCount | String | productCount 回傳欄位 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].assembly_no | String | assembly_no 回傳欄位 |  |
| payload.results[].assemblyVer | String | assemblyVer 回傳欄位 |  |
| payload.results[].price | String | price 回傳欄位 |  |
| payload.results[].rawMaterialCost | String | rawMaterialCost 回傳欄位 |  |
| payload.results[].materialCost | String | materialCost 回傳欄位 |  |
| payload.results[].laborCost | String | laborCost 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 查詢資料表並套用條件：pl_item_capacity
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results[].month、payload.results[].pl_no、payload.results[].pl_name、payload.results[].productCount、payload.results[].item_no、payload.results[].item_name、payload.results[].assembly_no、payload.results[].assemblyVer、payload.results[].price、payload.results[].rawMaterialCost、payload.results[].materialCost、payload.results[].laborCost

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
        "output": {}
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
| payload.results[].month | String | month 回傳欄位 |  |
| payload.results[].pl_item_capacity_no | String | pl_item_capacity_no 回傳欄位 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].itemSubCategory | Integer | itemSubCategory 回傳欄位 |  |
| payload.results[].weightRatio | Float | weightRatio 回傳欄位 |  |
| payload.results[].lossRate | Float | lossRate 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 查詢資料表並套用條件：pl_item_capacity、pl_item_loss
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results[].id、payload.results[].month、payload.results[].pl_item_capacity_no、payload.results[].item_no、payload.results[].item_name、payload.results[].itemCategory、payload.results[].itemSubCategory、payload.results[].weightRatio、payload.results[].lossRate、payload.results[].creationTime

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
| payload.results[].month | String | month 回傳欄位 |  |
| payload.results[].pl_no | String | pl_no 回傳欄位 |  |
| payload.results[].pl_name | String | pl_name 回傳欄位 |  |
| payload.results[].productCount | Integer | productCount 回傳欄位 |  |
| payload.results[].laborCount | Integer | laborCount 回傳欄位 |  |
| payload.results[].unit | Integer | unit 回傳欄位 |  |
| payload.results[].hourlyOutput | Float | hourlyOutput 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 查詢資料表並套用條件：pl_man_capacity
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results[].id、payload.results[].month、payload.results[].pl_no、payload.results[].pl_name、payload.results[].productCount、payload.results[].laborCount、payload.results[].unit、payload.results[].hourlyOutput、payload.results[].creationTime

### Database Tables Used

| Table | Purpose |
|----------|------|
| pl_man_capacity | 提供產線統計排程、生產或產能資料 |
