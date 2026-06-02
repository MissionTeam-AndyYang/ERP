# purchase API Group

> Source: `restserver/package/restserver/api/purchase_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/purchase/arap](#get-api-v1-purchase-arap) | GET | 查詢採購 / 應收應付 | OK | OK |
| [/api/v1/purchase/contract](#get-api-v1-purchase-contract) | GET | 查詢採購 / 合約 | OK | OK |
| [/api/v1/purchase/goodsreceiptnote](#get-api-v1-purchase-goodsreceiptnote) | GET | 查詢採購 / 進貨單 | OK | OK |
| [/api/v1/purchase/payment](#get-api-v1-purchase-payment) | GET | 查詢採購 / 帳款 | OK | OK |
| [/api/v1/purchase/purchaseorder](#get-api-v1-purchase-purchaseorder) | GET | 查詢採購 / 採購單 | OK | OK |
| [/api/v1/purchase/statistics](#get-api-v1-purchase-statistics) | GET | 查詢採購 / 統計 | OK | OK |

## GET /api/v1/purchase/arap

<a id="get-api-v1-purchase-arap"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/arap | GET | 查詢採購 / 應收應付 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| order_no | String | YES | 訂單編號 |

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
        "no": "String",
        "month": "String",
        "companyName": "String",
        "subOrderNos": [
          "String"
        ],
        "totalAmount": "Float",
        "dueDate": "Integer",
        "records": [
          {
            "time": "Integer",
            "action": "Integer",
            "item_no": "String",
            "item_name": "String",
            "batch_number": "String",
            "serial_no": "String",
            "unit": "Integer",
            "count": "Float"
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
| payload.results[].no | String | 編號篩選 |  |
| payload.results[].month | String | month 回傳欄位 |  |
| payload.results[].companyName | String | companyName 回傳欄位 |  |
| payload.results[].subOrderNos[] | String | subOrderNos[] 回傳欄位 |  |
| payload.results[].totalAmount | Float | totalAmount 回傳欄位 |  |
| payload.results[].dueDate | Integer | dueDate 回傳欄位 |  |
| payload.results[].records[].time | Integer | time 回傳欄位 |  |
| payload.results[].records[].action | Integer | 設備作業方向 |  |
| payload.results[].records[].item_no | String | 料品/品項編號 |  |
| payload.results[].records[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].records[].batch_number | String | 批號 |  |
| payload.results[].records[].serial_no | String | serial_no 回傳欄位 |  |
| payload.results[].records[].unit | Integer | unit 回傳欄位 |  |
| payload.results[].records[].count | Float | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：order_no
2. 查詢資料表並套用條件：company、order_payment、payment
3. 組裝回傳 payload 欄位：payload.total、payload.results[].no、payload.results[].month、payload.results[].companyName、payload.results[].subOrderNos[]、payload.results[].totalAmount、payload.results[].dueDate、payload.results[].records[].time、payload.results[].records[].action、payload.results[].records[].item_no、payload.results[].records[].item_name、payload.results[].records[].batch_number、payload.results[].records[].serial_no、payload.results[].records[].unit、payload.results[].records[].count

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供採購單據、合約、帳款或統計資料 |
| order_payment | 提供採購單據、合約、帳款或統計資料 |
| payment | 提供採購單據、合約、帳款或統計資料 |

## GET /api/v1/purchase/contract

<a id="get-api-v1-purchase-contract"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/contract | GET | 查詢採購 / 合約 |

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
        "date": "Integer",
        "category": "Integer",
        "type": "Integer",
        "itemStyle": "Integer",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "item_no": "String",
        "item_name": "String",
        "unit": "Integer",
        "price": "Float",
        "count": "Float",
        "amount": "Float",
        "comment": "String",
        "creationTime": "Integer",
        "transItemCategory": "Integer",
        "transItemAttr": "Integer",
        "paymentType": "Integer",
        "paymentDate": "Integer",
        "paymentPeriod": "Integer",
        "unitWarehouse": "Integer",
        "quotation_no": "String",
        "quotationDate": "Integer"
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
| payload.results[].date | Integer | 日期 |  |
| payload.results[].category | Integer | 類別篩選 |  |
| payload.results[].type | Integer | 類型篩選 |  |
| payload.results[].itemStyle | Integer | 品項樣式 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].unit | Integer | unit 回傳欄位 |  |
| payload.results[].price | Float | price 回傳欄位 |  |
| payload.results[].count | Float | 本次回傳筆數 |  |
| payload.results[].amount | Float | amount 回傳欄位 |  |
| payload.results[].comment | String | comment 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |
| payload.results[].transItemCategory | Integer | transItemCategory 回傳欄位 |  |
| payload.results[].transItemAttr | Integer | transItemAttr 回傳欄位 |  |
| payload.results[].paymentType | Integer | paymentType 回傳欄位 |  |
| payload.results[].paymentDate | Integer | paymentDate 回傳欄位 |  |
| payload.results[].paymentPeriod | Integer | paymentPeriod 回傳欄位 |  |
| payload.results[].unitWarehouse | Integer | unitWarehouse 回傳欄位 |  |
| payload.results[].quotation_no | String | quotation_no 回傳欄位 |  |
| payload.results[].quotationDate | Integer | quotationDate 回傳欄位 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 查詢資料表並套用條件：company、payment
3. 組裝回傳 payload 欄位：payload.total、payload.results[].id、payload.results[].no、payload.results[].date、payload.results[].category、payload.results[].type、payload.results[].itemStyle、payload.results[].item_ref_no、payload.results[].item_ref_displayName、payload.results[].item_no、payload.results[].item_name、payload.results[].unit、payload.results[].price、payload.results[].count、payload.results[].amount、payload.results[].comment、payload.results[].creationTime、payload.results[].transItemCategory、payload.results[].transItemAttr、payload.results[].paymentType、payload.results[].paymentDate、payload.results[].paymentPeriod、payload.results[].unitWarehouse、payload.results[].quotation_no、payload.results[].quotationDate、payload.count

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供採購單據、合約、帳款或統計資料 |
| payment | 提供採購單據、合約、帳款或統計資料 |

## GET /api/v1/purchase/goodsreceiptnote

<a id="get-api-v1-purchase-goodsreceiptnote"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/goodsreceiptnote | GET | 查詢採購 / 進貨單 |

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
        "creator_no": "String",
        "purchase_order_no": "String",
        "date": "Integer",
        "category": "Integer",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "item_no": "String",
        "item_name": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "unit": "Integer",
        "price": "Float",
        "expectedCount": "Float",
        "checkedCount": "Float",
        "feeCount": "Float",
        "amount": "Integer",
        "addDeleteAmount": "Integer",
        "comment": "String",
        "creationTime": "Integer"
      }
    ],
    "sum": {
      "amount": "Integer",
      "returnAmount": "Integer"
    },
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
| payload.results[].creator_no | String | creator_no 回傳欄位 |  |
| payload.results[].purchase_order_no | String | 採購單號 |  |
| payload.results[].date | Integer | 日期 |  |
| payload.results[].category | Integer | 類別篩選 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].itemSubCategory | Integer | itemSubCategory 回傳欄位 |  |
| payload.results[].unit | Integer | unit 回傳欄位 |  |
| payload.results[].price | Float | price 回傳欄位 |  |
| payload.results[].expectedCount | Float | expectedCount 回傳欄位 |  |
| payload.results[].checkedCount | Float | checkedCount 回傳欄位 |  |
| payload.results[].feeCount | Float | feeCount 回傳欄位 |  |
| payload.results[].amount | Integer | amount 回傳欄位 |  |
| payload.results[].addDeleteAmount | Integer | addDeleteAmount 回傳欄位 |  |
| payload.results[].comment | String | comment 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |
| payload.sum.amount | Integer | amount 回傳欄位 |  |
| payload.sum.returnAmount | Integer | returnAmount 回傳欄位 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start、type
2. 查詢資料表並套用條件：batch_number、goods_receipt_note、inventory_record、material、purchase_order
3. 組裝回傳 payload 欄位：payload.total、payload.results[].id、payload.results[].no、payload.results[].creator_no、payload.results[].purchase_order_no、payload.results[].date、payload.results[].category、payload.results[].item_ref_no、payload.results[].item_ref_displayName、payload.results[].item_no、payload.results[].item_name、payload.results[].itemCategory、payload.results[].itemSubCategory、payload.results[].unit、payload.results[].price、payload.results[].expectedCount、payload.results[].checkedCount、payload.results[].feeCount、payload.results[].amount、payload.results[].addDeleteAmount、payload.results[].comment、payload.results[].creationTime、payload.sum.amount、payload.sum.returnAmount、payload.count

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供採購單據、合約、帳款或統計資料 |
| goods_receipt_note | 提供採購單據、合約、帳款或統計資料 |
| inventory_record | 提供採購單據、合約、帳款或統計資料 |
| material | 提供採購單據、合約、帳款或統計資料 |
| purchase_order | 提供採購單據、合約、帳款或統計資料 |

## GET /api/v1/purchase/payment

<a id="get-api-v1-purchase-payment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/payment | GET | 查詢採購 / 帳款 |

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
    "results": [
      {
        "id": "Integer",
        "no": "String",
        "ref_no": "String",
        "creator_no": "String",
        "date": "Integer",
        "displayName": "String",
        "category": "Integer",
        "type": "Integer",
        "itemStyle": "Integer",
        "item_no": "String",
        "item_name": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "payment_id": "Integer",
        "unit": "Integer",
        "price": "Float",
        "shippingPrice": "Float",
        "unitConversion": "Float",
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
| payload.results[].ref_no | String | ref_no 回傳欄位 |  |
| payload.results[].creator_no | String | creator_no 回傳欄位 |  |
| payload.results[].date | Integer | 日期 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].category | Integer | 類別篩選 |  |
| payload.results[].type | Integer | 類型篩選 |  |
| payload.results[].itemStyle | Integer | 品項樣式 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].itemSubCategory | Integer | itemSubCategory 回傳欄位 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].payment_id | Integer | payment_id 回傳欄位 |  |
| payload.results[].unit | Integer | unit 回傳欄位 |  |
| payload.results[].price | Float | price 回傳欄位 |  |
| payload.results[].shippingPrice | Float | shippingPrice 回傳欄位 |  |
| payload.results[].unitConversion | Float | unitConversion 回傳欄位 |  |
| payload.results[].comment | String | comment 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 查詢資料表並套用條件：contract、order_payment、product_order、shipping_order
3. 組裝回傳 payload 欄位：payload.total、payload.results[].id、payload.results[].no、payload.results[].ref_no、payload.results[].creator_no、payload.results[].date、payload.results[].displayName、payload.results[].category、payload.results[].type、payload.results[].itemStyle、payload.results[].item_no、payload.results[].item_name、payload.results[].itemCategory、payload.results[].itemSubCategory、payload.results[].item_ref_no、payload.results[].item_ref_displayName、payload.results[].payment_id、payload.results[].unit、payload.results[].price、payload.results[].shippingPrice、payload.results[].unitConversion、payload.results[].comment、payload.results[].creationTime

### Database Tables Used

| Table | Purpose |
|----------|------|
| contract | 提供採購單據、合約、帳款或統計資料 |
| order_payment | 提供採購單據、合約、帳款或統計資料 |
| product_order | 提供採購單據、合約、帳款或統計資料 |
| shipping_order | 提供採購單據、合約、帳款或統計資料 |

## GET /api/v1/purchase/purchaseorder

<a id="get-api-v1-purchase-purchaseorder"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/purchaseorder | GET | 查詢採購 / 採購單 |

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
    "sum": {
      "amount": "Integer",
      "realAmount": "Integer",
      "returnAmount": "Integer",
      "itemCategoryAmount": [
        {
          "id": "Integer",
          "no": "String",
          "ref_no": "String",
          "creator_no": "String",
          "date": "Integer",
          "displayName": "String",
          "category": "Integer",
          "type": "Integer",
          "itemStyle": "Integer",
          "item_no": "String",
          "item_name": "String",
          "itemCategory": "Integer",
          "itemSubCategory": "Integer",
          "item_ref_no": "String",
          "item_ref_displayName": "String",
          "payment_id": "Integer",
          "unit": "Integer",
          "price": "Float",
          "shippingPrice": "Float",
          "unitConversion": "Float",
          "comment": "String",
          "creationTime": "Integer"
        }
      ]
    },
    "total": "Integer",
    "count": "Integer",
    "results": [
      {
        "id": "Integer",
        "no": "String",
        "creator_no": "String",
        "purchase_request_no": "String",
        "date": "Integer",
        "ref_no": "String",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "item_no": "String",
        "item_name": "String",
        "unit": "Integer",
        "price": "Float",
        "count": "Float",
        "amount": "Integer",
        "expectedDate": "Integer",
        "address": "String",
        "payment_type": "Integer",
        "payment_source": "Integer",
        "payment_date": "Integer",
        "payment_period": "Integer",
        "comment": "String",
        "creationTime": "Integer",
        "contract": {
          "price": "String",
          "name": "String",
          "type": "String",
          "date": "String",
          "comment": "String"
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
| payload.sum.amount | Integer | amount 回傳欄位 |  |
| payload.sum.realAmount | Integer | realAmount 回傳欄位 |  |
| payload.sum.returnAmount | Integer | returnAmount 回傳欄位 |  |
| payload.sum.itemCategoryAmount[].id | Integer | 資料 ID |  |
| payload.sum.itemCategoryAmount[].no | String | 編號篩選 |  |
| payload.sum.itemCategoryAmount[].ref_no | String | ref_no 回傳欄位 |  |
| payload.sum.itemCategoryAmount[].creator_no | String | creator_no 回傳欄位 |  |
| payload.sum.itemCategoryAmount[].date | Integer | 日期 |  |
| payload.sum.itemCategoryAmount[].displayName | String | 顯示名稱 |  |
| payload.sum.itemCategoryAmount[].category | Integer | 類別篩選 |  |
| payload.sum.itemCategoryAmount[].type | Integer | 類型篩選 |  |
| payload.sum.itemCategoryAmount[].itemStyle | Integer | 品項樣式 |  |
| payload.sum.itemCategoryAmount[].item_no | String | 料品/品項編號 |  |
| payload.sum.itemCategoryAmount[].item_name | String | item_name 回傳欄位 |  |
| payload.sum.itemCategoryAmount[].itemCategory | Integer | 料品類別 |  |
| payload.sum.itemCategoryAmount[].itemSubCategory | Integer | itemSubCategory 回傳欄位 |  |
| payload.sum.itemCategoryAmount[].item_ref_no | String | 交易對象編號 |  |
| payload.sum.itemCategoryAmount[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.sum.itemCategoryAmount[].payment_id | Integer | payment_id 回傳欄位 |  |
| payload.sum.itemCategoryAmount[].unit | Integer | unit 回傳欄位 |  |
| payload.sum.itemCategoryAmount[].price | Float | price 回傳欄位 |  |
| payload.sum.itemCategoryAmount[].shippingPrice | Float | shippingPrice 回傳欄位 |  |
| payload.sum.itemCategoryAmount[].unitConversion | Float | unitConversion 回傳欄位 |  |
| payload.sum.itemCategoryAmount[].comment | String | comment 回傳欄位 |  |
| payload.sum.itemCategoryAmount[].creationTime | Integer | creationTime 回傳欄位 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 編號篩選 |  |
| payload.results[].creator_no | String | creator_no 回傳欄位 |  |
| payload.results[].purchase_request_no | String | purchase_request_no 回傳欄位 |  |
| payload.results[].date | Integer | 日期 |  |
| payload.results[].ref_no | String | ref_no 回傳欄位 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | item_name 回傳欄位 |  |
| payload.results[].unit | Integer | unit 回傳欄位 |  |
| payload.results[].price | Float | price 回傳欄位 |  |
| payload.results[].count | Float | 本次回傳筆數 |  |
| payload.results[].amount | Integer | amount 回傳欄位 |  |
| payload.results[].expectedDate | Integer | expectedDate 回傳欄位 |  |
| payload.results[].address | String | address 回傳欄位 |  |
| payload.results[].payment_type | Integer | payment_type 回傳欄位 |  |
| payload.results[].payment_source | Integer | payment_source 回傳欄位 |  |
| payload.results[].payment_date | Integer | payment_date 回傳欄位 |  |
| payload.results[].payment_period | Integer | payment_period 回傳欄位 |  |
| payload.results[].comment | String | comment 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |
| payload.results[].contract.price | String | price 回傳欄位 |  |
| payload.results[].contract.name | String | 名稱 |  |
| payload.results[].contract.type | String | 類型篩選 |  |
| payload.results[].contract.date | String | 日期 |  |
| payload.results[].contract.comment | String | comment 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start、type
2. 查詢資料表並套用條件：contract、goods_receipt_note、material、product_order、purchase_order、shipping_order
3. 組裝回傳 payload 欄位：payload.sum.amount、payload.sum.realAmount、payload.sum.returnAmount、payload.sum.itemCategoryAmount[].id、payload.sum.itemCategoryAmount[].no、payload.sum.itemCategoryAmount[].ref_no、payload.sum.itemCategoryAmount[].creator_no、payload.sum.itemCategoryAmount[].date、payload.sum.itemCategoryAmount[].displayName、payload.sum.itemCategoryAmount[].category、payload.sum.itemCategoryAmount[].type、payload.sum.itemCategoryAmount[].itemStyle、payload.sum.itemCategoryAmount[].item_no、payload.sum.itemCategoryAmount[].item_name、payload.sum.itemCategoryAmount[].itemCategory、payload.sum.itemCategoryAmount[].itemSubCategory、payload.sum.itemCategoryAmount[].item_ref_no、payload.sum.itemCategoryAmount[].item_ref_displayName、payload.sum.itemCategoryAmount[].payment_id、payload.sum.itemCategoryAmount[].unit、payload.sum.itemCategoryAmount[].price、payload.sum.itemCategoryAmount[].shippingPrice、payload.sum.itemCategoryAmount[].unitConversion、payload.sum.itemCategoryAmount[].comment、payload.sum.itemCategoryAmount[].creationTime、payload.total、payload.count、payload.results[].id、payload.results[].no、payload.results[].creator_no、payload.results[].purchase_request_no、payload.results[].date、payload.results[].ref_no、payload.results[].item_ref_no、payload.results[].item_ref_displayName、payload.results[].item_no、payload.results[].item_name、payload.results[].unit、payload.results[].price、payload.results[].count、payload.results[].amount、payload.results[].expectedDate、payload.results[].address、payload.results[].payment_type、payload.results[].payment_source、payload.results[].payment_date、payload.results[].payment_period、payload.results[].comment、payload.results[].creationTime、payload.results[].contract.price、payload.results[].contract.name、payload.results[].contract.type、payload.results[].contract.date、payload.results[].contract.comment

### Database Tables Used

| Table | Purpose |
|----------|------|
| contract | 提供採購單據、合約、帳款或統計資料 |
| goods_receipt_note | 提供採購單據、合約、帳款或統計資料 |
| material | 提供採購單據、合約、帳款或統計資料 |
| product_order | 提供採購單據、合約、帳款或統計資料 |
| purchase_order | 提供採購單據、合約、帳款或統計資料 |
| shipping_order | 提供採購單據、合約、帳款或統計資料 |

## GET /api/v1/purchase/statistics

<a id="get-api-v1-purchase-statistics"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/purchase/statistics | GET | 查詢採購 / 統計 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| commit | String | NO | 是否提交/確認統計條件 |
| end_time | String | NO | 查詢結束時間 |
| start_time | String | NO | 查詢開始時間 |

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
        "date": "String",
        "oneProcess": "Integer",
        "secProcess": "Integer",
        "total": "Integer"
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
| payload.results[].date | String | 日期 |  |
| payload.results[].oneProcess | Integer | 主製程 |  |
| payload.results[].secProcess | Integer | secProcess 回傳欄位 |  |
| payload.results[].total | Integer | 符合條件的總筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：commit、end_time、start_time
2. 組裝回傳 payload 欄位：payload.count、payload.results[].date、payload.results[].oneProcess、payload.results[].secProcess、payload.results[].total

### Database Tables Used

None
