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
| payload.results[].date | Integer | 日期時間 |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].creator_no | String | 製單人員編號 |  |
| payload.results[].ref_no | String | 來源單號 |  |
| payload.results[].refCategory | Integer | 來源類別 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | 料品/品項名稱 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].itemSubCategory | Integer | 料品子類別 |  |
| payload.results[].itemType | Integer | 料品類型 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].expectedCount | Float | 預期數量 |  |
| payload.results[].checkedCount | Float | 已確認數量 |  |
| payload.results[].validDays | Integer | 有效天數 |  |
| payload.results[].validDate | Integer | 效期日期 |  |
| payload.results[].validDateNo | String | 效期日期編號 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：inventoryType、orderCategory、type
2. 查詢 batch_number、goods_receipt_note、inventory_record、production_data 取得批號追蹤資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
| payload.nonWork[].creator_no | String | 製單人員編號 |  |
| payload.nonWork[].work_order_no | String | 工單號 |  |
| payload.nonWork[].product_order_no | String | 訂購單號 |  |
| payload.nonWork[].customer_no | String | 客戶no，關連至company資料表 |  |
| payload.nonWork[].customer_displayName | String | 客戶公司簡稱，關連至company資料表 |  |
| payload.nonWork[].product_no | String | 製成品no，關連至product 資料表 |  |
| payload.nonWork[].product_name | String | 交易品項名稱，關連至product 資料表 |  |
| payload.nonWork[].date | Integer | 日期時間 |  |
| payload.nonWork[].production_line_no | String | 產線編號 |  |
| payload.nonWork[].oneProcess | Integer | 主製程 |  |
| payload.nonWork[].secProcess | Integer | 次製程 |  |
| payload.nonWork[].item_no | String | 料品/品項編號 |  |
| payload.nonWork[].item_name | String | 料品/品項名稱 |  |
| payload.nonWork[].materialLoss | Float | 損耗 (產出物重量-投入物重量-餘料重量-廢料重量 |  |
| payload.nonWork[].creationTime | Integer | 資料建立時間 |  |
| payload.work[].name | String | 名稱 |  |
| payload.work[].records[].data.oneProcess | String | 主製程 |  |
| payload.work[].records[].data.secProcess | String | 次製程 |  |
| payload.work[].records[].data.input | String | input 的業務資料 |  |
| payload.work[].records[].data.output | String | output 的業務資料 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：itemCategory、no
2. 查詢 production_data、production_data_input、production_data_output 取得批號追蹤 / 紀錄資料
3. 整理查詢結果並回傳

### Database Tables Used

| Table | Purpose |
|----------|------|
| production_data | 追蹤批號來源、庫存、生產與出入庫關聯 |
| production_data_input | 追蹤批號來源、庫存、生產與出入庫關聯 |
| production_data_output | 追蹤批號來源、庫存、生產與出入庫關聯 |
