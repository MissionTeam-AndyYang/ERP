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

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 batch_number、inventory_record、process_order 取得庫存資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
| payload.results[].kind | Integer | 庫存統計類型 |  |
| payload.results[].specified_no | String | 指定料品或批號編號 |  |
| payload.results[].specified_name | String | 指定料品或批號名稱 |  |
| payload.results[].specified_ref_no | String | 指定料品參照編號 |  |
| payload.results[].beginCount | Float | 期初庫存數量 |  |
| payload.results[].beginAmount | Float | 期初庫存金額 |  |
| payload.results[].inCount | Float | 入庫數量 |  |
| payload.results[].inAmount | Float | 入庫金額 |  |
| payload.results[].outCount | Float | 出庫數量 |  |
| payload.results[].outAmount | Float | 出庫金額 |  |
| payload.results[].endCount | Float | 期末庫存數量 |  |
| payload.results[].endAmount | Float | 期末庫存金額 |  |
| payload.results[].itemCategory | Integer | 料品類別 |  |
| payload.results[].itemSubCategory | Integer | 料品子類別 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].price | Float | 單價 |  |
| payload.results[].nearExpiryCount | Float | 即期庫存數量 |  |
| payload.results[].nearExpiryAmount | Float | 即期庫存金額 |  |
| payload.results[].expiredCount | Float | 已過期庫存數量 |  |
| payload.results[].expiredAmount | Float | 已過期庫存金額 |  |
| payload.results[].batchNo[].specified_no | String | 指定料品或批號編號 |  |
| payload.results[].batchNo[].specified_name | String | 指定料品或批號名稱 |  |
| payload.results[].batchNo[].specified_ref_no | String | 指定料品參照編號 |  |
| payload.results[].batchNo[].endCount | Float | 期末庫存數量 |  |
| payload.results[].batchNo[].endAmount | Float | 期末庫存金額 |  |
| payload.results[].batchNo[].validDate | Integer | 效期日期 |  |
| payload.results[].batchNo[].itemType | Integer | 料品類型 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：commit、date、end_time、itemCategory、item_no、start_time、type
2. 取得庫存 / 品項清單資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
| payload.results[].warehouse_no | String | 倉庫no，關連至ship_wh_alias |  |
| payload.results[].warehouse_displayName | String | 倉儲別名名稱，關聯至ship_wh_alias資料表 |  |
| payload.results[].date | String | 日期時間 |  |
| payload.results[].timezone | String | 用戶端時區 |  |
| payload.results[].category | Integer | 類別 |  |
| payload.results[].startAmount | Float | 期初庫存價值 (含稅價，小數點4位) |  |
| payload.results[].inAmount | Float | 入庫金額 |  |
| payload.results[].outAmount | Float | 出庫金額 |  |
| payload.results[].inPurchaseAmount | Float | 採購累計庫存價值 (含稅價，小數點4位) |  |
| payload.results[].endAmount | Float | 期末庫存金額 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：end_time、start_time
2. 查詢 inventory_month_statistic 取得庫存 / 月資料資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
| payload.results[].contract.contract.category | String | 類別 |  |
| payload.results[].contract.contract.type | String | 類型 |  |
| payload.results[].contract.contract.itemStyle | String | 品項樣式 |  |
| payload.results[].contract.contract.unit | String | 單位 |  |
| payload.results[].contract.contract.price | String | 單價 |  |
| payload.results[].contract.contract.comment | String | 備註 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start、type
2. 查詢 item_price、trans_items 取得庫存 / 價格資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

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
| payload.results.warehouse[].creator_no | String | 製單人員編號 |  |
| payload.results.warehouse[].group | String | 群組編號 |  |
| payload.results.warehouse[].refCategory | Integer | 來源類別 |  |
| payload.results.warehouse[].ref_no | String | 來源單號 |  |
| payload.results.warehouse[].warehouse_no | String | 倉庫no，關連至ship_wh_alias |  |
| payload.results.warehouse[].warehouse_displayName | String | 倉儲別名名稱，關聯至ship_wh_alias資料表 |  |
| payload.results.warehouse[].date | Integer | 日期時間 |  |
| payload.results.warehouse[].category | Integer | 類別 |  |
| payload.results.warehouse[].source | Integer | 源由 |  |
| payload.results.warehouse[].batchNumber | String | 出入庫批號 |  |
| payload.results.warehouse[].serialNo | String | 流水號 |  |
| payload.results.warehouse[].item_no | String | 料品/品項編號 |  |
| payload.results.warehouse[].item_name | String | 料品/品項名稱 |  |
| payload.results.warehouse[].item_ref_no | String | 交易對象編號 |  |
| payload.results.warehouse[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results.warehouse[].itemCategory | Integer | 料品類別 |  |
| payload.results.warehouse[].itemType | Integer | 料品類型 |  |
| payload.results.warehouse[].unit | Integer | 單位 |  |
| payload.results.warehouse[].count | Float | 本次回傳筆數 |  |
| payload.results.warehouse[].price | Float | 單價 |  |
| payload.results.warehouse[].amount | Integer | 金額或需求量 |  |
| payload.results.warehouse[].comment | String | 備註 |  |
| payload.results.warehouse[].registerDevId | String | 註冊之設備ID |  |
| payload.results.warehouse[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：batchNumber
2. 查詢 inventory_record 取得庫存 / 統計資料
3. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| inventory_record | 提供庫存查詢、統計或紀錄資料 |
