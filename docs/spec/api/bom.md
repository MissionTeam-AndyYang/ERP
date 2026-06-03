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
| payload.results[].no | String | 資料編號 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].unit | String | 單位 |  |
| payload.results[].data[].version | String | 版本 |  |
| payload.results[].data[].date | String | 日期時間 |  |
| payload.results[].data[].unit | String | 單位 |  |
| payload.results[].data[].weight | String | 重量 |  |
| payload.results[].data[].creationTime | String | 資料建立時間 |  |
| payload.results[].data[].comment | String | 備註 |  |
| payload.results[].data[].items[].id | Integer | 資料 ID |  |
| payload.results[].data[].items[].no | String | 資料編號 |  |
| payload.results[].data[].items[].displayName | String | 顯示名稱 |  |
| payload.results[].data[].items[].version | Integer | 版本 |  |
| payload.results[].data[].items[].date | Integer | 日期時間 |  |
| payload.results[].data[].items[].unit | Integer | 單位 |  |
| payload.results[].data[].items[].weight | Float | 重量 |  |
| payload.results[].data[].items[].comment | String | 備註 |  |
| payload.results[].data[].items[].creationTime | Integer | 資料建立時間 |  |
| payload.results[].data[].cost[].id | Integer | 資料 ID |  |
| payload.results[].data[].cost[].no | String | 資料編號 |  |
| payload.results[].data[].cost[].displayName | String | 顯示名稱 |  |
| payload.results[].data[].cost[].version | Integer | 版本 |  |
| payload.results[].data[].cost[].date | Integer | 日期時間 |  |
| payload.results[].data[].cost[].unit | Integer | 單位 |  |
| payload.results[].data[].cost[].weight | Float | 重量 |  |
| payload.results[].data[].cost[].comment | String | 備註 |  |
| payload.results[].data[].cost[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start、type
2. 查詢 bom、sample_price 取得BOM資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
| payload.results[].no | String | 資料編號 |  |
| payload.results[].creator_no | String | 製單人員編號 |  |
| payload.results[].date | Integer | 日期時間 |  |
| payload.results[].ref_no | String | 來源單號 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | 料品/品項名稱 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].price | Float | 單價 |  |
| payload.results[].count | Float | 本次回傳筆數 |  |
| payload.results[].preparedCount | Float | 已備數量 |  |
| payload.results[].amount | Integer | 金額或需求量 |  |
| payload.results[].expectedDate | Integer | 預計交貨日期 |  |
| payload.results[].address | String | 地址 |  |
| payload.results[].payment_type | Integer | 收付款類別 |  |
| payload.results[].payment_source | Integer | 收付款來源 |  |
| payload.results[].payment_date | Integer | 收付款日期 |  |
| payload.results[].payment_period | Integer | 付款期間 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：order_no、product_no
2. 查詢 product_order 取得BOM / APS 資料資料
3. 整理查詢結果清單並展開回傳欄位語意

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
| payload.results[].no | String | 資料編號 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].version | Integer | 版本 |  |
| payload.results[].date | Integer | 日期時間 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 product_process 取得BOM / 製程資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
| payload.results[].no | String | 資料編號 |  |
| payload.results[].category | Integer | 類別 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].unitShipping | Integer | 貨運單位 |  |
| payload.results[].unitWarehouse | Integer | 倉儲單位 |  |
| payload.results[].unitProduct | Integer | 產製單位 |  |
| payload.results[].version | Integer | 版本 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：product_no
2. 查詢 product 取得BOM / 樹狀資料資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| product | 提供BOM主檔、配方或價格資料 |
