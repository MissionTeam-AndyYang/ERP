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
    "results": [
      {
        "id": "String",
        "no": "String",
        "displayName": "String",
        "unit": "String",
        "data": [
          {
            "version": "String",
            "date": "String",
            "unit": "String",
            "weight": "String",
            "creationTime": "String",
            "comment": "String",
            "items": [
              {
                "id": "Integer",
                "no": "String",
                "displayName": "String",
                "version": "Integer",
                "date": "Integer",
                "unit": "Integer",
                "weight": "Float",
                "comment": "String",
                "creationTime": "Integer"
              }
            ],
            "cost": [
              {
                "id": "Integer",
                "no": "String",
                "displayName": "String",
                "version": "Integer",
                "date": "Integer",
                "unit": "Integer",
                "weight": "Float",
                "comment": "String",
                "creationTime": "Integer"
              }
            ]
          }
        ]
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
| payload.results[].id | String | 資料 ID |  |
| payload.results[].no | String | 編號篩選 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].unit | String | unit 回傳欄位 |  |
| payload.results[].data[].version | String | version 回傳欄位 |  |
| payload.results[].data[].date | String | 日期 |  |
| payload.results[].data[].unit | String | unit 回傳欄位 |  |
| payload.results[].data[].weight | String | weight 回傳欄位 |  |
| payload.results[].data[].creationTime | String | creationTime 回傳欄位 |  |
| payload.results[].data[].comment | String | comment 回傳欄位 |  |
| payload.results[].data[].items[].id | Integer | 資料 ID |  |
| payload.results[].data[].items[].no | String | 編號篩選 |  |
| payload.results[].data[].items[].displayName | String | 顯示名稱 |  |
| payload.results[].data[].items[].version | Integer | version 回傳欄位 |  |
| payload.results[].data[].items[].date | Integer | 日期 |  |
| payload.results[].data[].items[].unit | Integer | unit 回傳欄位 |  |
| payload.results[].data[].items[].weight | Float | weight 回傳欄位 |  |
| payload.results[].data[].items[].comment | String | comment 回傳欄位 |  |
| payload.results[].data[].items[].creationTime | Integer | creationTime 回傳欄位 |  |
| payload.results[].data[].cost[].id | Integer | 資料 ID |  |
| payload.results[].data[].cost[].no | String | 編號篩選 |  |
| payload.results[].data[].cost[].displayName | String | 顯示名稱 |  |
| payload.results[].data[].cost[].version | Integer | version 回傳欄位 |  |
| payload.results[].data[].cost[].date | Integer | 日期 |  |
| payload.results[].data[].cost[].unit | Integer | unit 回傳欄位 |  |
| payload.results[].data[].cost[].weight | Float | weight 回傳欄位 |  |
| payload.results[].data[].cost[].comment | String | comment 回傳欄位 |  |
| payload.results[].data[].cost[].creationTime | Integer | creationTime 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start、type
2. 查詢資料表並套用條件：bom、sample_price
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results[].id、payload.results[].no、payload.results[].displayName、payload.results[].unit、payload.results[].data[].version、payload.results[].data[].date、payload.results[].data[].unit、payload.results[].data[].weight、payload.results[].data[].creationTime、payload.results[].data[].comment、payload.results[].data[].items[].id、payload.results[].data[].items[].no、payload.results[].data[].items[].displayName、payload.results[].data[].items[].version、payload.results[].data[].items[].date、payload.results[].data[].items[].unit、payload.results[].data[].items[].weight、payload.results[].data[].items[].comment、payload.results[].data[].items[].creationTime、payload.results[].data[].cost[].id、payload.results[].data[].cost[].no、payload.results[].data[].cost[].displayName、payload.results[].data[].cost[].version、payload.results[].data[].cost[].date、payload.results[].data[].cost[].unit、payload.results[].data[].cost[].weight、payload.results[].data[].cost[].comment、payload.results[].data[].cost[].creationTime

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
    "results": [
      {
        "id": "Integer",
        "no": "String",
        "creator_no": "String",
        "date": "Integer",
        "ref_no": "String",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "item_no": "String",
        "item_name": "String",
        "unit": "Integer",
        "price": "Float",
        "count": "Float",
        "preparedCount": "Float",
        "amount": "Integer",
        "expectedDate": "Integer",
        "address": "String",
        "payment_type": "Integer",
        "payment_source": "Integer",
        "payment_date": "Integer",
        "payment_period": "Integer",
        "comment": "String",
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
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 編號篩選 |  |
| payload.results[].creator_no | String | creator_no 回傳欄位 |  |
| payload.results[].date | Integer | 日期 |  |
| payload.results[].ref_no | String | ref_no 回傳欄位 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].unit | Integer | unit 回傳欄位 |  |
| payload.results[].price | Float | price 回傳欄位 |  |
| payload.results[].count | Float | 本次回傳筆數 |  |
| payload.results[].preparedCount | Float | preparedCount 回傳欄位 |  |
| payload.results[].amount | Integer | amount 回傳欄位 |  |
| payload.results[].expectedDate | Integer | expectedDate 回傳欄位 |  |
| payload.results[].address | String | address 回傳欄位 |  |
| payload.results[].payment_type | Integer | payment_type 回傳欄位 |  |
| payload.results[].payment_source | Integer | payment_source 回傳欄位 |  |
| payload.results[].payment_date | Integer | payment_date 回傳欄位 |  |
| payload.results[].payment_period | Integer | payment_period 回傳欄位 |  |
| payload.results[].comment | String | comment 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：order_no、product_no
2. 查詢資料表並套用條件：product_order
3. 組裝回傳 payload 欄位：payload.results[].id、payload.results[].no、payload.results[].creator_no、payload.results[].date、payload.results[].ref_no、payload.results[].item_ref_no、payload.results[].item_ref_displayName、payload.results[].item_no、payload.results[].item_name、payload.results[].unit、payload.results[].price、payload.results[].count、payload.results[].preparedCount、payload.results[].amount、payload.results[].expectedDate、payload.results[].address、payload.results[].payment_type、payload.results[].payment_source、payload.results[].payment_date、payload.results[].payment_period、payload.results[].comment、payload.results[].creationTime

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
    "results": [
      {
        "id": "Integer",
        "no": "String",
        "item_no": "String",
        "version": "Integer",
        "date": "Integer"
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
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 編號篩選 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].version | Integer | version 回傳欄位 |  |
| payload.results[].date | Integer | 日期 |  |
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
3. 組裝回傳 payload 欄位：payload.total、payload.results[].id、payload.results[].no、payload.results[].item_no、payload.results[].version、payload.results[].date、payload.count

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
    "results": [
      {
        "id": "Integer",
        "no": "String",
        "category": "Integer",
        "name": "String",
        "unitShipping": "Integer",
        "unitWarehouse": "Integer",
        "unitProduct": "Integer",
        "version": "Integer",
        "comment": "String",
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
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 編號篩選 |  |
| payload.results[].category | Integer | 類別篩選 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].unitShipping | Integer | unitShipping 回傳欄位 |  |
| payload.results[].unitWarehouse | Integer | unitWarehouse 回傳欄位 |  |
| payload.results[].unitProduct | Integer | unitProduct 回傳欄位 |  |
| payload.results[].version | Integer | version 回傳欄位 |  |
| payload.results[].comment | String | comment 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：product_no
2. 查詢資料表並套用條件：product
3. 組裝回傳 payload 欄位：payload.total、payload.results[].id、payload.results[].no、payload.results[].category、payload.results[].name、payload.results[].unitShipping、payload.results[].unitWarehouse、payload.results[].unitProduct、payload.results[].version、payload.results[].comment、payload.results[].creationTime

### Database Tables Used

| Table | Purpose |
|----------|------|
| product | 提供BOM主檔、配方或價格資料 |
