# shipwarehouse API Group

> Source: `restserver/package/restserver/api/shipwarehouse_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/shipwarehouse](#get-api-v1-shipwarehouse) | GET | 查詢物流倉儲 | OK | OK |
| [/api/v1/shipwarehouse/contract](#get-api-v1-shipwarehouse-contract) | GET | 查詢物流倉儲 / 合約 | OK | OK |
| [/api/v1/shipwarehouse/shiparap](#get-api-v1-shipwarehouse-shiparap) | GET | 查詢物流倉儲 / 物流應收應付 | OK | OK |
| [/api/v1/shipwarehouse/shippayment](#get-api-v1-shipwarehouse-shippayment) | GET | 查詢物流倉儲 / 物流帳款 | OK | OK |
| [/api/v1/shipwarehouse/shiprec](#get-api-v1-shipwarehouse-shiprec) | GET | 查詢物流倉儲 / 運輸紀錄 | OK | OK |
| [/api/v1/shipwarehouse/warehousearap](#get-api-v1-shipwarehouse-warehousearap) | GET | 查詢物流倉儲 / 倉儲應收應付 | OK | OK |
| [/api/v1/shipwarehouse/warehousepayment](#get-api-v1-shipwarehouse-warehousepayment) | GET | 查詢物流倉儲 / 倉儲帳款 | OK | OK |
| [/api/v1/shipwarehouse/warehouserec](#get-api-v1-shipwarehouse-warehouserec) | GET | 查詢物流倉儲 / 倉儲紀錄 | OK | OK |

## GET /api/v1/shipwarehouse

<a id="get-api-v1-shipwarehouse"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse | GET | 查詢物流倉儲 |

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
        "no": "String",
        "name": "String",
        "category": "Integer",
        "type": "Integer",
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
| payload.results[].no | String | 編號 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].category | Integer | 類別 | 物流 (1)、倉儲 (2) 、其他 (0) |
| payload.results[].type | Integer | 類型 | 自有 (1)、合約 (2) 、客供 (3) 、其他 (0) |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 ship_wh_alias 取得物流倉儲資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| ship_wh_alias | 提供物流倉儲查詢、統計或紀錄資料 |

## GET /api/v1/shipwarehouse/contract

<a id="get-api-v1-shipwarehouse-contract"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/contract | GET | 查詢物流倉儲 / 合約 |

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
        "no": "String",
        "date": "Integer",
        "ref_no": "String",
        "sw_alias_no": "String",
        "displayName": "String",
        "item_no": "String",
        "item_name": "String",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "category": "Integer",
        "type": "Integer",
        "itemStyle": "Integer",
        "region": "Integer",
        "unit": "Integer",
        "price": "Float",
        "fee": "Float",
        "comment": "String",
        "creationTime": "Integer",
        "shipwh": {
            "no": "String",
            "name": "String",
            "attribute": "Integer"
        },
        "vendor": {
            "no": "String",
            "name": "String",
            "paymentType": "Integer",
            "paymentDate": "Integer",
            "paymentPeriod": "Integer"
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
| payload.results[].id | Integer | 物流倉儲ID |  |
| payload.results[].no | String | 物流倉儲編號 |  |
| payload.results[].date | Integer | 日期時間 |  |
| payload.results[].ref_no | String | 來源單號 |  |
| payload.results[].sw_alias_no | String | 物流倉儲別名no，關連至ship_wh_alias資料表 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].item_no | String | 「料品品項」編號 |  |
| payload.results[].item_name | String | 「料品品項」名稱 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].category | Integer | 合約類型 | 物流 (1)、倉儲 (2) |
| payload.results[].type | Integer | 合約樣式 | 合約類別為 <br>1.物流: 宅配 (1)、專車 (2)、併車 (3) 、回頭車 (4) 、貨櫃 (5) <br>2.倉儲: 月租 (1)、日租 (2) 、時租 (3) |
| payload.results[].itemStyle | Integer | 品項樣式 | 物流 (1)、倉儲 (2) |
| payload.results[].region | Integer | 地區 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].price | Float | 單價 |  |
| payload.results[].fee | Float | 作業費 / 次 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |
| payload.results[].shipwh.no | String | 「交易品項」編號 |  |
| payload.results[].shipwh.name | String | 「交易品項」名稱 |  |
| payload.results[].shipwh.attribute | Integer | 「交易品項」屬性 | 常溫 (1)、冷藏 (2)、冷凍 (3) 、其他 (0) |
| payload.results[].vendor.no | String | 公司編號 |  |
| payload.results[].vendor.name | String | 公司名稱 |  |
| payload.results[].vendor.paymentType | Integer | 收付款類別 | 現結 (0)、月結 (1) |
| payload.results[].vendor.paymentDate | Integer | 收付款方式 | 現金 (0)、匯款 (1)、支票 (2) |
| payload.results[].vendor.paymentPeriod | Integer | 收付款期 |  |
### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 company、payment、ship_wh、ship_wh_contract 取得物流倉儲 / 合約資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供物流倉儲查詢、統計或紀錄資料 |
| payment | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh_contract | 提供物流倉儲查詢、統計或紀錄資料 |

## GET /api/v1/shipwarehouse/shiparap

<a id="get-api-v1-shipwarehouse-shiparap"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/shiparap | GET | 查詢物流倉儲 / 物流應收應付 |

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
        "totalAmount": "Integer",
        "dueDate": "Integer",
        "records": [
          {
            "shipRec": {
                "date": "Integer",
                "unit": "Integer",
                "price": "Integer",
                "amount": "Integer",
                "comment": "String"
            },
            "contract": {
                "category": "Integer",
                "type": "Integer",
                "region":"Integer"
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
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].month | String | 年序月 |  |
| payload.results[].companyName | String | 物流公司名稱 |  |
| payload.results[].totalAmount | Integer | 總金額 |  |
| payload.results[].dueDate | Integer | 銷帳日期 |  |
| payload.results[].records[].shipRec.date | Integer | 物流日 |  |
| payload.results[].records[].shipRec.unit | Integer | 物流交易單位 |  |
| payload.results[].records[].shipRec.price | Integer | 物流單價 |  |
| payload.results[].records[].shipRec.amount | Integer | 物流金額 |  |
| payload.results[].records[].shipRec.comment | Integer | 備註 |  |
| payload.results[].records[].contract.category | Integer | 合約類別 |  物流 (1)、倉儲 (2) |
| payload.results[].records[].contract.type | Integer | 合約樣式 | 合約類別為 <br>1.物流: 宅配 (1)、專車 (2)、併車 (3) 、回頭車 (4) 、貨櫃 (5) <br>2.倉儲: 月租 (1)、日租 (2) 、時租 (3) |
| payload.results[].records[].contract.region | region | 合約地區 |  |


### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：order_no
2. 查詢 company、payment、ship_wh_contract、shipping_payment 取得物流倉儲 / 物流應收應付資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供物流倉儲查詢、統計或紀錄資料 |
| payment | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh_contract | 提供物流倉儲查詢、統計或紀錄資料 |
| shipping_payment | 提供物流倉儲查詢、統計或紀錄資料 |
| shipping_record | 提供物流倉儲查詢、統計或紀錄資料 |

## GET /api/v1/shipwarehouse/shippayment

<a id="get-api-v1-shipwarehouse-shippayment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/shippayment | GET | 查詢物流倉儲 / 物流帳款 |

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
        "payment": {
            "no": "String",
            "date": "Integer",
            "month": "String",
            "count": "Integer",
            "amount": "Integer",
            "addDeleteAmount": "Integer",
        },
        "order": {
            "checkedCount": "Integer",
            "expectedCount": "Integer",
            "item_name": "String",
            "item_ref_displayName": "String",
            "unit": "Integer",
            "price": "Integer",
            "contractNo": "String",
            "contractCategory": "Integer",
            "contractType": "Integer",
            "contractItemStyle": "Integer",
            "paymentType": "Integer"
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
| payload.results[].payment.no | String | 帳款編號 |  |
| payload.results[].payment.date | Integer | 帳款費用日期 |  |
| payload.results[].payment.count | Integer | 件 / 車數 |  |
| payload.results[].payment.amount | Integer | 金額 |  |
| payload.results[].payment.addDeleteAmount | Integer | 加 / 扣款金額 |  |
| payload.results[].order.checkedCount | Integer | 計價數量 |  |
| payload.results[].order.expectedCount | Integer | 預期數量 |  |
| payload.results[].order.unit | Integer | 交易單位 |  |
| payload.results[].order.price | Integer | 交易單價 |  |
| payload.results[].order.contractNo | String | 倉儲物流合約編號 |  |
| payload.results[].order.contractCategory  | Integer | 合約類別 |  物流 (1)、倉儲 (2) |
| payload.results[].order.contractType | Integer | 合約樣式 | 合約類別為 <br>1.物流: 宅配 (1)、專車 (2)、併車 (3) 、回頭車 (4) 、貨櫃 (5) <br>2.倉儲: 月租 (1)、日租 (2) 、時租 (3) |
| payload.results[].order.contractItemStyle | Integer | 品項樣式 | 物流 (1)、倉儲 (2) |
| payload.results[].order.paymentType | Integer | 收付款類別 | 現結 (0)、月結 (1) |


### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 ship_wh_contract、shipping_payment、shipping_record 取得物流倉儲 / 物流帳款資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| ship_wh_contract | 提供物流倉儲查詢、統計或紀錄資料 |
| shipping_payment | 提供物流倉儲查詢、統計或紀錄資料 |
| shipping_record | 提供物流倉儲查詢、統計或紀錄資料 |

## GET /api/v1/shipwarehouse/shiprec

<a id="get-api-v1-shipwarehouse-shiprec"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/shiprec | GET | 查詢物流倉儲 / 運輸紀錄 |

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
        "id": "String",
        "date": "Integer",
        "count": "Integer",
        "alias": {
          "name": "String",
          "type": "Integer"
        },
        "contract": {
          "category": "Integer",
          "type": "Integer",
          "region": "Integer",
          "unit": "Integer",
          "price": "Integer"
        },
        "order": {
          "date": "Integer",
          "item_name": "String",
          "item_ref_displayName": "String",
          "unit": "Integer",
          "price": "Float",
          "contractPrice": "Float"
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
| payload.results[].id | String | 資料 ID |  |
| payload.results[].date | String | 物流記錄日期時間 |  |
| payload.results[].count | Integer | 本次回傳筆數 |  |
| payload.results[].alias.name | String | 倉儲物流名稱 |  |
| payload.results[].alias.type | Integer | 樣式 | 自有 (1)、合約 (2) 、客供 (3) 、其他 (0)  |
| payload.results[].contract.category | Integer | 合約類別 |  物流 (1)、倉儲 (2) |
| payload.results[].contract.type | Integer | 合約樣式 | 合約類別為 <br>1.物流: 宅配 (1)、專車 (2)、併車 (3) 、回頭車 (4) 、貨櫃 (5) <br>2.倉儲: 月租 (1)、日租 (2) 、時租 (3) |
| payload.results[].contract.region | Integer | 地區 |  |
| payload.results[].contract.unit | Integer | 計價單位 |  |
| payload.results[].contract.price | Float | 含稅價格 |  | 
| payload.results[].order.date | Integer | 進貨/銷貨日期時間 |  |
| payload.results[].order.item_name | String | 進銷貨「交易品項」名稱 |  |
| payload.results[].order.item_ref_displayName | String | 進銷貨交易對象顯示名稱 |  |
| payload.results[].order.unit | String | 進銷貨交易單位 |  |
| payload.results[].order.price | Float | 進銷貨單價 |  |
| payload.results[].order.contractPrice | Float | 進銷貨合約交易單價 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 goods_receipt_note、payment、product_order、purchase_order 取得物流倉儲 / 運輸紀錄資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| goods_receipt_note | 提供物流倉儲查詢、統計或紀錄資料 |
| payment | 提供物流倉儲查詢、統計或紀錄資料 |
| product_order | 提供物流倉儲查詢、統計或紀錄資料 |
| purchase_order | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh_alias | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh_contract | 提供物流倉儲查詢、統計或紀錄資料 |
| shipping_order | 提供物流倉儲查詢、統計或紀錄資料 |
| shipping_record | 提供物流倉儲查詢、統計或紀錄資料 |

## GET /api/v1/shipwarehouse/warehousearap

<a id="get-api-v1-shipwarehouse-warehousearap"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/warehousearap | GET | 查詢倉儲應收應付(掛帳) |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| order_category | String | NO | order_category 查詢條件 |
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
        "totalAmount": "Integer",
        "dueDate": "Integer",
        "records": [
          {
            "warehouseRec": {
              "date": "Integer",
              "unit": "Integer",
              "price": "Integer",
              "amount": "Integer",
              "countDays": "Integer",
              "comment": "String"
            },
            "contract": {
              "category": "Integer",
              "type": "Integer",
              "region":"Integer"
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
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 帳款編號 |  |
| payload.results[].month | String | 年序月 |  |
| payload.results[].companyName | String | 倉儲公司名稱 |  |
| payload.results[].totalAmount | Integer | 總金額 |  |
| payload.results[].dueDate | Integer | 銷帳日期 |  |
| payload.results[].records[].warehouseRec.date | Integer | 出庫日 |  |
| payload.results[].records[].warehouseRec.unit | Integer | 交易單位 |  |
| payload.results[].records[].warehouseRec.price | Integer | 單價 |  |
| payload.results[].records[].warehouseRec.amount | Integer | 金額 |  |
| payload.results[].records[].warehouseRec.countDays | Integer | 存放積和數 |  |
| payload.results[].records[].warehouseRec.comment | String | 備註 |  |
| payload.results[].records[].contract.category | Integer | 合約類別 |  物流 (1)、倉儲 (2) |
| payload.results[].records[].contract.type | Integer | 合約樣式 | 合約類別為 <br>1.物流: 宅配 (1)、專車 (2)、併車 (3) 、回頭車 (4) 、貨櫃 (5) <br>2.倉儲: 月租 (1)、日租 (2) 、時租 (3) |
| payload.results[].records[].contract.region | region | 合約地區 |  |


### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：order_category、order_no
2. 查詢 company、payment、ship_wh_contract、warehouse_payment 取得物流倉儲 / 倉儲應收應付資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供物流倉儲查詢、統計或紀錄資料 |
| payment | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh_contract | 提供物流倉儲查詢、統計或紀錄資料 |
| warehouse_payment | 提供物流倉儲查詢、統計或紀錄資料 |
| warehouse_record | 提供物流倉儲查詢、統計或紀錄資料 |

## GET /api/v1/shipwarehouse/warehousepayment

<a id="get-api-v1-shipwarehouse-warehousepayment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/warehousepayment | GET | 查詢倉儲帳款 |

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
        "payment": {
            "no": "String",
            "date": "Integer",
            "month": "String",
            "count": "Integer",
            "amount": "Integer",
            "addDeleteAmount": "Integer",
        },
        "order": {
            "count": "Integer",
            "item_name": "String",
            "item_ref_displayName": "String",
            "unit": "Integer",
            "price": "Integer",
            "contractNo": "String",
            "contractCategory": "Integer",
            "contractType": "Integer",
            "contractItemStyle": "Integer",
            "paymentType": "Integer"
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
| payload.results[].id | Integer | 物流倉儲ID |  |
| payload.results[].payment.no | String | 帳款編號 |  |
| payload.results[].payment.date | Integer | 帳款費用日期 |  |
| payload.results[].payment.count | Integer | 計價積和|  |
| payload.results[].payment.amount | Integer | 金額 |  |
| payload.results[].payment.addDeleteAmount | Integer | 加 / 扣款金額 |  |
| payload.results[].order.count | Integer | 倉儲計價數量 |  |
| payload.results[].order.item_name | String | 交易品項名稱 |  |
| payload.results[].order.item_ref_displayName | String | 交易對象 |  |
| payload.results[].order.unit | Integer | 交易單位 |  |
| payload.results[].order.price | Integer | 交易單價 |  |
| payload.results[].order.contractNo | String | 倉儲物流合約編號 |  |
| payload.results[].order.contractCategory  | Integer | 合約類別 |  物流 (1)、倉儲 (2) |
| payload.results[].order.contractType | Integer | 合約樣式 | 合約類別為 <br>1.物流: 宅配 (1)、專車 (2)、併車 (3) 、回頭車 (4) 、貨櫃 (5) <br>2.倉儲: 月租 (1)、日租 (2) 、時租 (3) |
| payload.results[].order.contractItemStyle | Integer | 品項樣式 | 物流 (1)、倉儲 (2) |
| payload.results[].order.paymentType | Integer | 收付款類型 | 現結 (0)、月結 (1) |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 ship_wh_contract、warehouse_payment、warehouse_record 取得物流倉儲 / 倉儲帳款資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| ship_wh_contract | 提供物流倉儲查詢、統計或紀錄資料 |
| warehouse_payment | 提供物流倉儲查詢、統計或紀錄資料 |
| warehouse_record | 提供物流倉儲查詢、統計或紀錄資料 |

## GET /api/v1/shipwarehouse/warehouserec

<a id="get-api-v1-shipwarehouse-warehouserec"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/warehouserec | GET | 查詢倉儲紀錄 |

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
        "id": "String",
        "date": "Integer",
        "count": "Integer",
        "count": "Integer",
        "days": {
          "name": "String",
          "type": "Integer"
        },
        "contract": {
          "category": "Integer",
          "type": "Integer",
          "unit": "Integer",
          "price": "Integer"
        },
        "batch": {
          "no": "String",
          "item_name": "String",
          "itemCategory": "String",
          "itemSubCategory": "Integer",
          "validDate": "Integer"
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
| payload.results[].id | String | 資料 ID |  |
| payload.results[].date | String | 出庫日 |  |
| payload.results[].count | Integer | 件 / 板數 |  |
| payload.results[].days | Integer | 存放天數 |  |
| payload.results[].alias.name | String | 倉儲名稱 |  |
| payload.results[].alias.type | Integer | 樣式 | 自有 (1)、合約 (2) 、客供 (3) 、其他 (0)  |
| payload.results[].contract.category | Integer | 合約類別 |  物流 (1)、倉儲 (2) |
| payload.results[].contract.type | Integer | 合約樣式 | 合約類別為 <br>1.物流: 宅配 (1)、專車 (2)、併車 (3) 、回頭車 (4) 、貨櫃 (5) <br>2.倉儲: 月租 (1)、日租 (2) 、時租 (3) |
| payload.results[].contract.unit | Integer | 計價單位 |  |
| payload.results[].contract.price | Float | 含稅價格 |  | 
| payload.results[].batch.no | String | 批號 |  |
| payload.results[].batch.item_name | String | 「料品品項」名稱 |  |
| payload.results[].batch.itemCategory | String | 「料品品項」類別 |  |
| payload.results[].batch.itemSubCategory | String | 「料品品項」子類別 |  |
| payload.results[].batch.validDate | String | 效期日期 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 batch_number、ship_wh_alias、ship_wh_contract、warehouse_record 取得物流倉儲 / 倉儲紀錄資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh_alias | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh_contract | 提供物流倉儲查詢、統計或紀錄資料 |
| warehouse_record | 提供物流倉儲查詢、統計或紀錄資料 |
