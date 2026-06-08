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
| inventoryType | Integer | NO | 是否庫存資訊: 1. 是 |
| orderCategory | Integer | NO | 訂單類別: 1. 採購 2. 訂購 |
| type | Integer | YES | 類型篩選: 1. 日期 2. 訂單 |

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
        "creationTime": "Integer",
        "price": "Float",
        "costPrice": "Float",
        "ref_order_no": "String",
        "ref_order_category":  "Integer",
        "remaining": "Float",
        "inventory_unit":  "Integer"
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
| payload.results[].ref_no | String | 來源單號 | 進貨單no / 銷貨單no / 領退餘廢產單 no |
| payload.results[].refCategory | Integer | 來源單號類別 | 採購(1)、 製造(2)、 銷貨退回(3) |
| payload.results[].item_no | String | 「料品品項」項編號 |  |
| payload.results[].item_name | String | 「料品品項」名稱 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.results[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.results[].itemType | Integer | 「料品品項」類型 | 新料 (1)、餘料 (2)、廢料 (3) 、其他 (0) |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].expectedCount | Float | 預期數量 |  |
| payload.results[].checkedCount | Float | 已確認數量 |  |
| payload.results[].validDays | Integer | 有效天數 |  |
| payload.results[].validDate | Integer | 效期日期 |  |
| payload.results[].validDateNo | String | 效期日期編號 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |
| payload.results[].price | Float | 銷售/採購單價 |  |
| payload.results[].costPrice | Float | 成本單價 |  |
| payload.results[].ref_order_no | String | 採購/訂購單號 |  |
| payload.results[].ref_order_category | Integer | 溯源類型 |  採購 (1)、訂購 (2) |
| payload.results[].remaining | Float | 庫存數量 |  |
| payload.results[].inventory_unit | Integer | 庫存單位 |  |
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
    "stock": [
        {
          "warehouse_no": "WH4250218PDL",
          "warehouse_displayName": "恆旺_台中",
          "itemCategory": 1,
          "itemType": 1,
          "item_no": "PMB0034005",
          "item_name": "米蛋白穀粒原料",
          "batchNumber": "BN1124071001",
          "validDate": 1751472000,
          "amount": -0.0,
          "count": -0.0,
          "nearExpiryAmount": 0,
          "nearExpiryCount": 0,
          "expiredAmount": -0.0,
          "expiredCount": -0.0,
          "unit": 3,
          "firstInDate": 1720540800
        }
      ],
     "nonWork": [
        {
          "date": 1720540800,
          "source": 1,
          "warehouse_no": "WH4250218PDL",
          "warehouse_displayName": "恆旺_台中",
          "itemCategory": 1,
          "itemType": 1,
          "item_no": "PMB0034005",
          "item_name": "米蛋白穀粒原料",
          "batchNumber": "BN1124071001",
          "serialNo": "00000",
          "validDate": 1751472000,
          "count": 1625.0,
          "amount": 511875.0,
          "unit": 3,
          "order": ""
        }
    ],
    "work": [
      {
        "name": "String",
        "records": [
          {
            "date": 1736870400,
            "order": "Z140115002",
            "data": {
                "oneProcess": 2,
                "secProcess": 2,
                "input": [
                    {
                        "source": 2,
                        "itemCategory": 1,
                        "itemType": 1,
                        "item_no": "PMB0034005",
                        "item_name": "米蛋白穀粒原料",
                        "batch_number": "BN1124071001",
                        "validDate": 1751472000,
                        "count": 31.75,
                        "unit": 3
                    }
                ],
                "output": [
                    {
                        "output_batch_no": "BN1425011502",
                        "output_item_no": "SFE0052002",
                        "output_item_name": "阿華田米蛋白穀物一口脆",
                        "output_itemType": 1,
                        "output_validDate": 1760284800,
                        "output_unit": 3,
                        "output_count": 431.8
                    }
                ]
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


| payload.stock[].warehouse_no | String | 倉儲別名編號 |  |
| payload.stock[].warehouse_displayName | String | 倉儲別名名稱 |  |
| payload.stock[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.stock[].itemType | Integer | 「料品品項」類型 | 新料 (1)、餘料 (2)、廢料 (3) 、其他 (0) |
| payload.stock[].item_no | String | 「料品品項」編號 |  |
| payload.stock[].item_name | String | 「料品品項」名稱 |  |
| payload.stock[].batchNumber | String | 批號 |  |
| payload.stock[].validDate | Integer | 效期日期 |  |
| payload.stock[].unit | Integer | 單位 |  |
| payload.stock[].amount | Float | 金額 |  |
| payload.stock[].count | Float | 數量 |  |
| payload.stock[].nearExpiryAmount | Float | 即期金額 |  |
| payload.stock[].nearExpiryCount | Float | 即期數量 |  |
| payload.stock[].expiredAmount | Float | 過期金額 |  |
| payload.stock[].expiredCount | Float | 過期數量 |  |

| payload.nonWork[].date | Integer | 日期 |  |
| payload.nonWork[].source | Integer | 來源| 採購 (1)、訂購 (2) |
| payload.nonWork[].warehouse_no | String | 倉儲別名編號 |  |
| payload.nonWork[].warehouse_displayName | String | 倉儲別名名稱 |  |
| payload.nonWork[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.nonWork[].itemType | Integer | 「料品品項」類型 | 新料 (1)、餘料 (2)、廢料 (3) 、其他 (0) |
| payload.nonWork[].item_no | String | 「料品品項」編號 |  |
| payload.nonWork[].item_name | String | 「料品品項」名稱 |  |
| payload.nonWork[].batchNumber | String | 批號 |  |
| payload.nonWork[].validDate | Integer | 效期日期 |  |
| payload.nonWork[].unit | Integer | 單位 |  |
| payload.nonWork[].amount | Float | 金額 |  |
| payload.nonWork[].count | Float | 數量 |  |
| payload.nonWork[].order | String | 進貨單/銷貨單 |  |



| payload.work[].name | String | 產出「料品品項」名稱 |  |
| payload.work[].records[].data.oneProcess | Integer | 主製程 |  |
| payload.work[].records[].data.secProcess | Integer | 次製程 |  |
| payload.work[].records[].data.input[].source | Integer | input 的業務資料 |  |
| payload.work[].records[].data.input[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.work[].records[].data.input[].itemType | Integer | 「料品品項」類型 | 新料 (1)、餘料 (2)、廢料 (3) 、其他 (0) |
| payload.work[].records[].data.input[].item_no | String | 「料品品項」編號 |  |
| payload.work[].records[].data.input[].item_name | String | 「料品品項」名稱 |  |
| payload.work[].records[].data.input[].batch_number | String | 批號 |  |
| payload.work[].records[].data.input[].validDate | Integer | 效期日期 |  |
| payload.work[].records[].data.input[].unit | Integer | 單位 |  |
| payload..work[].records[].data.input[].count | Float | 數量 |  |
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
