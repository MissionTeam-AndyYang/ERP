# batchtrace API Group

> Source: `restserver/package/restserver/api/batchtrace_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/batchtrace](#get-api-v1-batchtrace) | GET | 依日期或訂單編號取得批號 | OK | OK |
| [/api/v1/batchtrace/record](#get-api-v1-batchtrace-record) | GET | 取得批號溯源 | OK | OK |

## GET /api/v1/batchtrace

<a id="get-api-v1-batchtrace"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/batchtrace | GET | 依日期或訂單編號取得批號 |

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
| /api/v1/batchtrace/record | GET | 取得批號溯源 |

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
          "warehouse_no": "String",
          "warehouse_displayName": "String",
          "itemCategory": "Integer",
          "itemType": "Integer",
          "item_no": "String",
          "item_name": "String",
          "batchNumber": "String",
          "validDate": "Integer",
          "amount": "Float",
          "count": "Float",
          "nearExpiryAmount": "Float",
          "nearExpiryCount": "Float",
          "expiredAmount": "Float",
          "expiredCount": "Float",
          "unit": "Integer",
          "firstInDate": "Integer"
        }
      ],
     "nonWork": [
        {
          "date": "Integer",
          "source": "Integer",
          "warehouse_no": "String",
          "warehouse_displayName": "String",
          "itemCategory": "Integer",
          "itemType": "Integer",
          "item_no": "String",
          "item_name": "String",
          "batchNumber": "String",
          "serialNo": "String",
          "validDate": "Integer",
          "count": "Float",
          "amount": "Float",
          "unit": "Integer",
          "order": "String"
        }
    ],
    "work": [
      {
        "name": "String",
        "records": [
          {
            "date": "Integer",
            "order": "String",
            "data": {
                "oneProcess": "Integer",
                "secProcess": "Integer",
                "input": [
                    {
                        "source": "Integer",
                        "itemCategory": "Integer",
                        "itemType": "Integer",
                        "item_no": "String",
                        "item_name": "String",
                        "batch_number": "String",
                        "validDate": "Integer",
                        "count": "Float",
                        "unit": "Integer"
                    }
                ],
                "output": [
                    {
                        "output_batch_no": "String",
                        "output_item_no": "String",
                        "output_item_name": "String",
                        "output_itemType": "Integer",
                        "output_validDate": "Integer",
                        "output_unit": "Integer",
                        "output_count": "Float",
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
| payload.work[].records[].data.input[].item_no | String | 投入「料品品項」編號 |  |
| payload.work[].records[].data.input[].item_name | String |  投入「料品品項」名稱 |  |
| payload.work[].records[].data.input[].batch_number | String | 投入「料品品項」批號 |  |
| payload.work[].records[].data.input[].validDate | Integer | 投入「料品品項」效期 |  |
| payload.work[].records[].data.input[].unit | Integer | 投入「料品品項」單位 |  |
| payload.work[].records[].data.input[].count | Float | 投入「料品品項」數量 |  |
| payload.work[].records[].data.output[].output_batch_no | String | 產出「料品品項」批號 |  |
| payload.work[].records[].data.output[].output_item_no | String | 產出「料品品項」編號 |  |
| payload.work[].records[].data.output[].output_item_name | String | 產出「料品品項」名稱 |  |
| payload.work[].records[].data.output[].itemType | Integer | 產出「料品品項」類型 | 新料 (1)、餘料 (2)、廢料 (3) 、其他 (0) |
| payload.work[].records[].data.output[].validDate | Integer | 產出「料品品項」效期 |  |
| payload.work[].records[].data.output[].unit | Integer | 產出「料品品項」單位 |  |
| payload.work[].records[].data.output[].count | Float | 產出「料品品項」數量 |  |

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
