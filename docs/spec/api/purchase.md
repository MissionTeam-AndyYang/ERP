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
| payload.results[].no | String | 資料編號 |  |
| payload.results[].month | String | 月份 |  |
| payload.results[].companyName | String | company Name 的業務資料 |  |
| payload.results[].subOrderNos[] | String | 子單號清單 |  |
| payload.results[].totalAmount | Float | 總金額 |  |
| payload.results[].dueDate | Integer | 預計收付款日期 |  |
| payload.results[].records[].time | Integer | 作業時間 |  |
| payload.results[].records[].action | Integer | 作業方向 |  |
| payload.results[].records[].item_no | String | 料品/品項編號 |  |
| payload.results[].records[].item_name | String | 料品/品項名稱 |  |
| payload.results[].records[].batch_number | String | 批號 |  |
| payload.results[].records[].serial_no | String | 流水號 |  |
| payload.results[].records[].unit | Integer | 單位 |  |
| payload.results[].records[].count | Float | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：order_no
2. 查詢 company、order_payment、payment 取得採購 / 應收應付資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
| payload.results[].no | String | 資料編號 |  |
| payload.results[].date | Integer | 日期時間 |  |
| payload.results[].category | Integer | 類別 |  |
| payload.results[].type | Integer | 類型 |  |
| payload.results[].itemStyle | Integer | 品項樣式 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | 料品/品項名稱 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].price | Float | 單價 |  |
| payload.results[].count | Float | 本次回傳筆數 |  |
| payload.results[].amount | Float | 金額或需求量 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |
| payload.results[].transItemCategory | Integer | trans Item Category 的業務資料 |  |
| payload.results[].transItemAttr | Integer | trans Item Attr 的業務資料 |  |
| payload.results[].paymentType | Integer | 收付款類別 |  |
| payload.results[].paymentDate | Integer | 收付款日期 |  |
| payload.results[].paymentPeriod | Integer | 付款期間 |  |
| payload.results[].unitWarehouse | Integer | 倉儲單位 |  |
| payload.results[].quotation_no | String | quotation no 的業務資料 |  |
| payload.results[].quotationDate | Integer | quotation Date 的業務資料 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 company、payment 取得採購 / 合約資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
| payload.results[].no | String | 資料編號 |  |
| payload.results[].creator_no | String | 製單人員編號 |  |
| payload.results[].purchase_order_no | String | 採購單號 |  |
| payload.results[].date | Integer | 日期時間 |  |
| payload.results[].category | Integer | 類別 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | 料品/品項名稱 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].itemSubCategory | Integer | 料品子類別 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].price | Float | 單價 |  |
| payload.results[].expectedCount | Float | 預期數量 |  |
| payload.results[].checkedCount | Float | 已確認數量 |  |
| payload.results[].feeCount | Float | 計價數量 (小數點2位) |  |
| payload.results[].amount | Integer | 金額或需求量 |  |
| payload.results[].addDeleteAmount | Integer | 加扣金額 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |
| payload.sum.amount | Integer | 金額或需求量 |  |
| payload.sum.returnAmount | Integer | 退回金額 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start、type
2. 查詢 batch_number、goods_receipt_note、inventory_record、material 取得採購 / 進貨單資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
| payload.results[].no | String | 資料編號 |  |
| payload.results[].ref_no | String | 來源單號 |  |
| payload.results[].creator_no | String | 製單人員編號 |  |
| payload.results[].date | Integer | 日期時間 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].category | Integer | 類別 |  |
| payload.results[].type | Integer | 類型 |  |
| payload.results[].itemStyle | Integer | 品項樣式 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | 料品/品項名稱 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].itemSubCategory | Integer | 料品子類別 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].payment_id | Integer | 帳款資料id，關連至payment資料表 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].price | Float | 單價 |  |
| payload.results[].shippingPrice | Float | 物流價格 |  |
| payload.results[].unitConversion | Float | 規格轉換 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 contract、order_payment、product_order、shipping_order 取得採購 / 帳款資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
| payload.sum.amount | Integer | 金額或需求量 |  |
| payload.sum.realAmount | Integer | real Amount 的業務資料 |  |
| payload.sum.returnAmount | Integer | 退回金額 |  |
| payload.sum.itemCategoryAmount[].id | Integer | 資料 ID |  |
| payload.sum.itemCategoryAmount[].no | String | 資料編號 |  |
| payload.sum.itemCategoryAmount[].ref_no | String | 來源單號 |  |
| payload.sum.itemCategoryAmount[].creator_no | String | 製單人員編號 |  |
| payload.sum.itemCategoryAmount[].date | Integer | 日期時間 |  |
| payload.sum.itemCategoryAmount[].displayName | String | 顯示名稱 |  |
| payload.sum.itemCategoryAmount[].category | Integer | 類別 |  |
| payload.sum.itemCategoryAmount[].type | Integer | 類型 |  |
| payload.sum.itemCategoryAmount[].itemStyle | Integer | 品項樣式 |  |
| payload.sum.itemCategoryAmount[].item_no | String | 料品/品項編號 |  |
| payload.sum.itemCategoryAmount[].item_name | String | 料品/品項名稱 |  |
| payload.sum.itemCategoryAmount[].itemCategory | Integer | 料品類別 |  |
| payload.sum.itemCategoryAmount[].itemSubCategory | Integer | 料品子類別 |  |
| payload.sum.itemCategoryAmount[].item_ref_no | String | 交易對象編號 |  |
| payload.sum.itemCategoryAmount[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.sum.itemCategoryAmount[].payment_id | Integer | 帳款資料id，關連至payment資料表 |  |
| payload.sum.itemCategoryAmount[].unit | Integer | 單位 |  |
| payload.sum.itemCategoryAmount[].price | Float | 單價 |  |
| payload.sum.itemCategoryAmount[].shippingPrice | Float | 物流價格 |  |
| payload.sum.itemCategoryAmount[].unitConversion | Float | 規格轉換 |  |
| payload.sum.itemCategoryAmount[].comment | String | 備註 |  |
| payload.sum.itemCategoryAmount[].creationTime | Integer | 資料建立時間 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].creator_no | String | 製單人員編號 |  |
| payload.results[].purchase_request_no | String | 請購單no，關連至purchase_request資料表 |  |
| payload.results[].date | Integer | 日期時間 |  |
| payload.results[].ref_no | String | 來源單號 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | 料品/品項名稱 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].price | Float | 單價 |  |
| payload.results[].count | Float | 本次回傳筆數 |  |
| payload.results[].amount | Integer | 金額或需求量 |  |
| payload.results[].expectedDate | Integer | 預計交貨日期 |  |
| payload.results[].address | String | 地址 |  |
| payload.results[].payment_type | Integer | 收付款類別 |  |
| payload.results[].payment_source | Integer | 收付款來源 |  |
| payload.results[].payment_date | Integer | 收付款日期 |  |
| payload.results[].payment_period | Integer | 付款期間 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |
| payload.results[].contract.price | String | 單價 |  |
| payload.results[].contract.name | String | 名稱 |  |
| payload.results[].contract.type | String | 類型 |  |
| payload.results[].contract.date | String | 日期時間 |  |
| payload.results[].contract.comment | String | 備註 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start、type
2. 查詢 contract、goods_receipt_note、material、product_order 取得採購 / 採購單資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
| payload.results[].date | String | 日期時間 |  |
| payload.results[].oneProcess | Integer | 主製程 |  |
| payload.results[].secProcess | Integer | 次製程 |  |
| payload.results[].total | Integer | 符合條件的總筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：commit、end_time、start_time
2. 取得採購 / 統計資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

None
