# inventory API Group

> Source: `restserver/package/restserver/api/inventory_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/inventory](#get-api-v1-inventory) | GET | 查詢庫存 | OK | OK |
| [/api/v1/inventory/items](#get-api-v1-inventory-items) | GET | 查詢庫存 / 品項清單 | OK | OK |
| [/api/v1/inventory/months](#get-api-v1-inventory-months) | GET | 查詢庫存 / 月資料 | OK | OK |
| [/api/v1/inventory/price](#get-api-v1-inventory-price) | GET | 查詢庫存 / 價格 | OK | OK |
| [/api/v1/inventory/statistics](#get-api-v1-inventory-statistics) | GET | 查詢庫存 / 統計 | OK | OK |

## GET /api/v1/inventory

<a id="get-api-v1-inventory"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory | GET | 查詢庫存 |

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

1. 讀取查詢條件：count、start
2. 查詢資料表並套用條件：batch_number、inventory_record、process_order
3. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results[].id、payload.results[].date、payload.results[].no、payload.results[].creator_no、payload.results[].ref_no、payload.results[].refCategory、payload.results[].item_no、payload.results[].item_name、payload.results[].item_ref_no、payload.results[].item_ref_displayName、payload.results[].itemCategory、payload.results[].itemSubCategory、payload.results[].itemType、payload.results[].unit、payload.results[].expectedCount、payload.results[].checkedCount、payload.results[].validDays、payload.results[].validDate、payload.results[].validDateNo、payload.results[].comment、payload.results[].creationTime

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供庫存查詢、統計或紀錄資料 |
| inventory_record | 提供庫存查詢、統計或紀錄資料 |
| process_order | 提供庫存查詢、統計或紀錄資料 |

## GET /api/v1/inventory/items

<a id="get-api-v1-inventory-items"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory/items | GET | 查詢庫存 / 品項清單 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| commit | String | NO | 是否提交/確認統計條件 |
| date | String | NO | 日期 |
| end_time | String | NO | 查詢結束時間 |
| itemCategory | String | NO | 料品類別 |
| item_no | String | NO | 料品/品項編號 |
| start_time | String | NO | 查詢開始時間 |
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
        "kind": "Integer",
        "specified_no": "String",
        "specified_name": "String",
        "specified_ref_no": "String",
        "beginCount": "Float",
        "beginAmount": "Float",
        "inCount": "Float",
        "inAmount": "Float",
        "outCount": "Float",
        "outAmount": "Float",
        "endCount": "Float",
        "endAmount": "Float",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "unit": "Integer",
        "price": "Float",
        "nearExpiryCount": "Float",
        "nearExpiryAmount": "Float",
        "expiredCount": "Float",
        "expiredAmount": "Float",
        "batchNo": [
          {
            "specified_no": "String",
            "specified_name": "String",
            "specified_ref_no": "String",
            "endCount": "Float",
            "endAmount": "Float",
            "validDate": "Integer",
            "itemType": "Integer"
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
| payload.results[].kind | Integer | kind 回傳欄位 |  |
| payload.results[].specified_no | String | specified_no 回傳欄位 |  |
| payload.results[].specified_name | String | specified_name 回傳欄位 |  |
| payload.results[].specified_ref_no | String | specified_ref_no 回傳欄位 |  |
| payload.results[].beginCount | Float | beginCount 回傳欄位 |  |
| payload.results[].beginAmount | Float | beginAmount 回傳欄位 |  |
| payload.results[].inCount | Float | inCount 回傳欄位 |  |
| payload.results[].inAmount | Float | inAmount 回傳欄位 |  |
| payload.results[].outCount | Float | outCount 回傳欄位 |  |
| payload.results[].outAmount | Float | outAmount 回傳欄位 |  |
| payload.results[].endCount | Float | endCount 回傳欄位 |  |
| payload.results[].endAmount | Float | endAmount 回傳欄位 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].itemSubCategory | Integer | itemSubCategory 回傳欄位 |  |
| payload.results[].unit | Integer | unit 回傳欄位 |  |
| payload.results[].price | Float | price 回傳欄位 |  |
| payload.results[].nearExpiryCount | Float | nearExpiryCount 回傳欄位 |  |
| payload.results[].nearExpiryAmount | Float | nearExpiryAmount 回傳欄位 |  |
| payload.results[].expiredCount | Float | expiredCount 回傳欄位 |  |
| payload.results[].expiredAmount | Float | expiredAmount 回傳欄位 |  |
| payload.results[].batchNo[].specified_no | String | specified_no 回傳欄位 |  |
| payload.results[].batchNo[].specified_name | String | specified_name 回傳欄位 |  |
| payload.results[].batchNo[].specified_ref_no | String | specified_ref_no 回傳欄位 |  |
| payload.results[].batchNo[].endCount | Float | endCount 回傳欄位 |  |
| payload.results[].batchNo[].endAmount | Float | endAmount 回傳欄位 |  |
| payload.results[].batchNo[].validDate | Integer | validDate 回傳欄位 |  |
| payload.results[].batchNo[].itemType | Integer | 料品類型 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：commit、date、end_time、itemCategory、item_no、start_time、type
2. 組裝回傳 payload 欄位：payload.total、payload.results[].kind、payload.results[].specified_no、payload.results[].specified_name、payload.results[].specified_ref_no、payload.results[].beginCount、payload.results[].beginAmount、payload.results[].inCount、payload.results[].inAmount、payload.results[].outCount、payload.results[].outAmount、payload.results[].endCount、payload.results[].endAmount、payload.results[].itemCategory、payload.results[].itemSubCategory、payload.results[].unit、payload.results[].price、payload.results[].nearExpiryCount、payload.results[].nearExpiryAmount、payload.results[].expiredCount、payload.results[].expiredAmount、payload.results[].batchNo[].specified_no、payload.results[].batchNo[].specified_name、payload.results[].batchNo[].specified_ref_no、payload.results[].batchNo[].endCount、payload.results[].batchNo[].endAmount、payload.results[].batchNo[].validDate、payload.results[].batchNo[].itemType

### Database Tables Used

None

## GET /api/v1/inventory/months

<a id="get-api-v1-inventory-months"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory/months | GET | 查詢庫存 / 月資料 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
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
    "total": "Integer",
    "results": [
      {
        "id": "Integer",
        "warehouse_no": "String",
        "warehouse_displayName": "String",
        "date": "String",
        "timezone": "String",
        "category": "Integer",
        "startAmount": "Float",
        "inAmount": "Float",
        "outAmount": "Float",
        "inPurchaseAmount": "Float",
        "endAmount": "Float",
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
| payload.results[].warehouse_no | String | warehouse_no 回傳欄位 |  |
| payload.results[].warehouse_displayName | String | warehouse_displayName 回傳欄位 |  |
| payload.results[].date | String | 日期 |  |
| payload.results[].timezone | String | timezone 回傳欄位 |  |
| payload.results[].category | Integer | 類別篩選 |  |
| payload.results[].startAmount | Float | startAmount 回傳欄位 |  |
| payload.results[].inAmount | Float | inAmount 回傳欄位 |  |
| payload.results[].outAmount | Float | outAmount 回傳欄位 |  |
| payload.results[].inPurchaseAmount | Float | inPurchaseAmount 回傳欄位 |  |
| payload.results[].endAmount | Float | endAmount 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：end_time、start_time
2. 查詢資料表並套用條件：inventory_month_statistic
3. 組裝回傳 payload 欄位：payload.total、payload.results[].id、payload.results[].warehouse_no、payload.results[].warehouse_displayName、payload.results[].date、payload.results[].timezone、payload.results[].category、payload.results[].startAmount、payload.results[].inAmount、payload.results[].outAmount、payload.results[].inPurchaseAmount、payload.results[].endAmount、payload.results[].creationTime

### Database Tables Used

| Table | Purpose |
|----------|------|
| inventory_month_statistic | 提供庫存查詢、統計或紀錄資料 |

## GET /api/v1/inventory/price

<a id="get-api-v1-inventory-price"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory/price | GET | 查詢庫存 / 價格 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |
| type | Integer | YES | 類型篩選 |

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
        "contract": {
          "contract": {
            "displayName": "String",
            "category": "String",
            "type": "String",
            "itemStyle": "String",
            "unit": "String",
            "price": "String",
            "comment": "String"
          }
        }
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
| payload.results[].contract.contract.displayName | String | 顯示名稱 |  |
| payload.results[].contract.contract.category | String | 類別篩選 |  |
| payload.results[].contract.contract.type | String | 類型篩選 |  |
| payload.results[].contract.contract.itemStyle | String | 品項樣式 |  |
| payload.results[].contract.contract.unit | String | unit 回傳欄位 |  |
| payload.results[].contract.contract.price | String | price 回傳欄位 |  |
| payload.results[].contract.contract.comment | String | comment 回傳欄位 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start、type
2. 查詢資料表並套用條件：item_price、trans_items
3. 組裝回傳 payload 欄位：payload.total、payload.results[].contract.contract.displayName、payload.results[].contract.contract.category、payload.results[].contract.contract.type、payload.results[].contract.contract.itemStyle、payload.results[].contract.contract.unit、payload.results[].contract.contract.price、payload.results[].contract.contract.comment、payload.count

### Database Tables Used

| Table | Purpose |
|----------|------|
| item_price | 提供庫存查詢、統計或紀錄資料 |
| trans_items | 提供庫存查詢、統計或紀錄資料 |

## GET /api/v1/inventory/statistics

<a id="get-api-v1-inventory-statistics"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/inventory/statistics | GET | 查詢庫存 / 統計 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| batchNumber | String | YES | 批號 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "results": {
      "warehouse": [
        {
          "id": "Integer",
          "creator_no": "String",
          "group": "String",
          "refCategory": "Integer",
          "ref_no": "String",
          "warehouse_no": "String",
          "warehouse_displayName": "String",
          "date": "Integer",
          "category": "Integer",
          "source": "Integer",
          "batchNumber": "String",
          "serialNo": "String",
          "item_no": "String",
          "item_name": "String",
          "item_ref_no": "String",
          "item_ref_displayName": "String",
          "itemCategory": "Integer",
          "itemType": "Integer",
          "unit": "Integer",
          "count": "Float",
          "price": "Float",
          "amount": "Integer",
          "comment": "String",
          "registerDevId": "String",
          "creationTime": "Integer"
        }
      ]
    }
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.results.warehouse[].id | Integer | 資料 ID |  |
| payload.results.warehouse[].creator_no | String | creator_no 回傳欄位 |  |
| payload.results.warehouse[].group | String | group 回傳欄位 |  |
| payload.results.warehouse[].refCategory | Integer | refCategory 回傳欄位 |  |
| payload.results.warehouse[].ref_no | String | ref_no 回傳欄位 |  |
| payload.results.warehouse[].warehouse_no | String | warehouse_no 回傳欄位 |  |
| payload.results.warehouse[].warehouse_displayName | String | warehouse_displayName 回傳欄位 |  |
| payload.results.warehouse[].date | Integer | 日期 |  |
| payload.results.warehouse[].category | Integer | 類別篩選 |  |
| payload.results.warehouse[].source | Integer | source 回傳欄位 |  |
| payload.results.warehouse[].batchNumber | String | 批號 |  |
| payload.results.warehouse[].serialNo | String | 流水號 |  |
| payload.results.warehouse[].item_no | String | 料品/品項編號 |  |
| payload.results.warehouse[].item_name | String | item_name 回傳欄位 |  |
| payload.results.warehouse[].item_ref_no | String | 交易對象編號 |  |
| payload.results.warehouse[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results.warehouse[].itemCategory | Integer | 料品類別 |  |
| payload.results.warehouse[].itemType | Integer | 料品類型 |  |
| payload.results.warehouse[].unit | Integer | unit 回傳欄位 |  |
| payload.results.warehouse[].count | Float | 本次回傳筆數 |  |
| payload.results.warehouse[].price | Float | price 回傳欄位 |  |
| payload.results.warehouse[].amount | Integer | amount 回傳欄位 |  |
| payload.results.warehouse[].comment | String | comment 回傳欄位 |  |
| payload.results.warehouse[].registerDevId | String | registerDevId 回傳欄位 |  |
| payload.results.warehouse[].creationTime | Integer | creationTime 回傳欄位 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：batchNumber
2. 查詢資料表並套用條件：inventory_record
3. 組裝回傳 payload 欄位：payload.results.warehouse[].id、payload.results.warehouse[].creator_no、payload.results.warehouse[].group、payload.results.warehouse[].refCategory、payload.results.warehouse[].ref_no、payload.results.warehouse[].warehouse_no、payload.results.warehouse[].warehouse_displayName、payload.results.warehouse[].date、payload.results.warehouse[].category、payload.results.warehouse[].source、payload.results.warehouse[].batchNumber、payload.results.warehouse[].serialNo、payload.results.warehouse[].item_no、payload.results.warehouse[].item_name、payload.results.warehouse[].item_ref_no、payload.results.warehouse[].item_ref_displayName、payload.results.warehouse[].itemCategory、payload.results.warehouse[].itemType、payload.results.warehouse[].unit、payload.results.warehouse[].count、payload.results.warehouse[].price、payload.results.warehouse[].amount、payload.results.warehouse[].comment、payload.results.warehouse[].registerDevId、payload.results.warehouse[].creationTime

### Database Tables Used

| Table | Purpose |
|----------|------|
| inventory_record | 提供庫存查詢、統計或紀錄資料 |
