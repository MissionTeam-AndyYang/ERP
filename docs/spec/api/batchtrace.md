# batchtrace API Group

> Source: `restserver/package/restserver/api/batchtrace_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/batchtrace](#get-api-v1-batchtrace) | GET | 查詢批號追蹤 | OK | OK |
| [/api/v1/batchtrace/record](#get-api-v1-batchtrace-record) | GET | 查詢批號追蹤 / 紀錄 | OK | OK |

## GET /api/v1/batchtrace

<a id="get-api-v1-batchtrace"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/batchtrace | GET | 查詢批號追蹤 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| inventoryType | String | NO | 庫存異動類型 |
| orderCategory | String | NO | 訂單類別 |
| type | String | YES | 類型篩選 |

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
        "date": "Integer",
        "no": "String",
        "creator_no": "String",
        "ref_no": "String",
        "refCategory": "Integer",
        "item_no": "String",
        "item_name": "String",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "itemType": "Integer",
        "unit": "Integer",
        "expectedCount": "Float",
        "checkedCount": "Float",
        "validDays": "Integer",
        "validDate": "Integer",
        "validDateNo": "String",
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
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].date | Integer | 日期 |  |
| payload.results[].no | String | 編號篩選 |  |
| payload.results[].creator_no | String | creator_no 回傳欄位 |  |
| payload.results[].ref_no | String | ref_no 回傳欄位 |  |
| payload.results[].refCategory | Integer | refCategory 回傳欄位 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].itemSubCategory | Integer | itemSubCategory 回傳欄位 |  |
| payload.results[].itemType | Integer | 料品類型 |  |
| payload.results[].unit | Integer | unit 回傳欄位 |  |
| payload.results[].expectedCount | Float | expectedCount 回傳欄位 |  |
| payload.results[].checkedCount | Float | checkedCount 回傳欄位 |  |
| payload.results[].validDays | Integer | validDays 回傳欄位 |  |
| payload.results[].validDate | Integer | validDate 回傳欄位 |  |
| payload.results[].validDateNo | String | validDateNo 回傳欄位 |  |
| payload.results[].comment | String | comment 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：inventoryType、orderCategory、type
2. 查詢資料表並套用條件：batch_number、goods_receipt_note、inventory_record、production_data、production_data_output
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results[].id、payload.results[].date、payload.results[].no、payload.results[].creator_no、payload.results[].ref_no、payload.results[].refCategory、payload.results[].item_no、payload.results[].item_name、payload.results[].item_ref_no、payload.results[].item_ref_displayName、payload.results[].itemCategory、payload.results[].itemSubCategory、payload.results[].itemType、payload.results[].unit、payload.results[].expectedCount、payload.results[].checkedCount、payload.results[].validDays、payload.results[].validDate、payload.results[].validDateNo、payload.results[].comment、payload.results[].creationTime

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 追蹤批號來源、庫存、生產與出入庫關聯 |
| goods_receipt_note | 追蹤批號來源、庫存、生產與出入庫關聯 |
| inventory_record | 追蹤批號來源、庫存、生產與出入庫關聯 |
| production_data | 追蹤批號來源、庫存、生產與出入庫關聯 |
| production_data_output | 追蹤批號來源、庫存、生產與出入庫關聯 |

## GET /api/v1/batchtrace/record

<a id="get-api-v1-batchtrace-record"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/batchtrace/record | GET | 查詢批號追蹤 / 紀錄 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| itemCategory | String | YES | 料品類別 |
| no | String | YES | 編號篩選 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "stock": {},
    "nonWork": [
      {
        "id": "Integer",
        "creator_no": "String",
        "work_order_no": "String",
        "product_order_no": "String",
        "customer_no": "String",
        "customer_displayName": "String",
        "product_no": "String",
        "product_name": "String",
        "date": "Integer",
        "production_line_no": "String",
        "oneProcess": "Integer",
        "secProcess": "Integer",
        "item_no": "String",
        "item_name": "String",
        "materialLoss": "Float",
        "creationTime": "Integer"
      }
    ],
    "work": [
      {
        "name": "String",
        "records": [
          {
            "data": {
              "oneProcess": "String",
              "secProcess": "String",
              "input": "String",
              "output": "String"
            }
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
| payload.nonWork[].id | Integer | 資料 ID |  |
| payload.nonWork[].creator_no | String | creator_no 回傳欄位 |  |
| payload.nonWork[].work_order_no | String | 工單號 |  |
| payload.nonWork[].product_order_no | String | 訂購單號 |  |
| payload.nonWork[].customer_no | String | customer_no 回傳欄位 |  |
| payload.nonWork[].customer_displayName | String | customer_displayName 回傳欄位 |  |
| payload.nonWork[].product_no | String | 製成品編號 |  |
| payload.nonWork[].product_name | String | product_name 回傳欄位 |  |
| payload.nonWork[].date | Integer | 日期 |  |
| payload.nonWork[].production_line_no | String | production_line_no 回傳欄位 |  |
| payload.nonWork[].oneProcess | Integer | 主製程 |  |
| payload.nonWork[].secProcess | Integer | secProcess 回傳欄位 |  |
| payload.nonWork[].item_no | String | 料品/品項編號 |  |
| payload.nonWork[].item_name | String | item_name 回傳欄位 |  |
| payload.nonWork[].materialLoss | Float | materialLoss 回傳欄位 |  |
| payload.nonWork[].creationTime | Integer | creationTime 回傳欄位 |  |
| payload.work[].name | String | 名稱 |  |
| payload.work[].records[].data.oneProcess | String | 主製程 |  |
| payload.work[].records[].data.secProcess | String | secProcess 回傳欄位 |  |
| payload.work[].records[].data.input | String | input 回傳欄位 |  |
| payload.work[].records[].data.output | String | output 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：itemCategory、no
2. 查詢資料表並套用條件：production_data、production_data_input、production_data_output
3. 組裝回傳 payload 欄位：payload.nonWork[].id、payload.nonWork[].creator_no、payload.nonWork[].work_order_no、payload.nonWork[].product_order_no、payload.nonWork[].customer_no、payload.nonWork[].customer_displayName、payload.nonWork[].product_no、payload.nonWork[].product_name、payload.nonWork[].date、payload.nonWork[].production_line_no、payload.nonWork[].oneProcess、payload.nonWork[].secProcess、payload.nonWork[].item_no、payload.nonWork[].item_name、payload.nonWork[].materialLoss、payload.nonWork[].creationTime、payload.work[].name、payload.work[].records[].data.oneProcess、payload.work[].records[].data.secProcess、payload.work[].records[].data.input、payload.work[].records[].data.output

### Database Tables Used

| Table | Purpose |
|----------|------|
| production_data | 追蹤批號來源、庫存、生產與出入庫關聯 |
| production_data_input | 追蹤批號來源、庫存、生產與出入庫關聯 |
| production_data_output | 追蹤批號來源、庫存、生產與出入庫關聯 |
