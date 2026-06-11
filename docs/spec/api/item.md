# item API Group

> Source: `restserver/package/restserver/api/item_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/item/data](#post-item-data) | POST | 資料回傳 | OK | Aligned with `docs/spec/scale/電子智能秤系統REST API_1.06.docx` |
| [/item/data/group](#get-item-data-group) | GET | 查詢設備料品棧板群組資料 | Need Review | Backend route exists, but not listed in REST API 1.06 |
| [/item/data/group](#post-item-data-group) | POST | 成板資料回傳 | OK | Aligned with `docs/spec/scale/電子智能秤系統REST API_1.06.docx` |
| [/item/groupInfo](#get-item-groupInfo) | GET | 品項資訊查詢 - 板號 | OK | Aligned with `docs/spec/scale/電子智能秤系統REST API_1.06.docx` |
| [/item/info](#get-item-info) | GET | 品項資訊查詢 - 批號 | OK | Aligned with `docs/spec/scale/電子智能秤系統REST API_1.06.docx` |
| [/item/manufacture](#get-item-manufacture) | GET | 品項項目取得 - 產製類別項目 | OK | Aligned with `docs/spec/scale/電子智能秤系統REST API_1.06.docx` |
| [/item/other](#get-item-other) | GET | 品項項目取得 - 其他類別項目 | OK | Aligned with `docs/spec/scale/電子智能秤系統REST API_1.06.docx` |
| [/item/purchase](#get-item-purchase) | GET | 品項項目取得 - 採購類別項目 | OK | Aligned with `docs/spec/scale/電子智能秤系統REST API_1.06.docx` |
| [/item/sales](#get-item-sales) | GET | 品項項目取得 - 訂購類別項目 | OK | Aligned with `docs/spec/scale/電子智能秤系統REST API_1.06.docx` |

## POST /item/data

<a id="post-item-data"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /item/data | POST | 回傳的「採購、產製、訂購、其他」品項項目之更新資料 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

```json
{
  "registerNo": "String",
  "total": "Integer",
  "results": [
    {
      "devAction": "Integer",
      "devComment": "String",
      "refNo": "String",
      "refNoSec": "String",
      "itemBatchNo": [
        {
          "batchNo": "String",
          "serialNos": [
            {
              "devDateTimestamp": "Integer",
              "serialNo": "String",
              "value": "Float",
              "isValid": "Boolean"
            }
          ]
        }
      ]
    }
  ]
}
```

| Field Path | Type | Required | Description | Enum |
|----------|----------|------|-----|---|
| registerNo | String | YES | 設備註冊碼 |  |
| total | Integer | NO | 回傳資料筆數 |  |
| results | Array | YES | 資料清單 |  |
| results[].devAction | Integer | YES | 設備端處理行為 (入/出庫、入/出產) | action |
| results[].devComment | String | NO | 設備端備註訊息 |  |
| results[].refNo | String | YES | 相對應品項項目單號 |  |
| results[].refNoSec | String | NO | 相對應品項項目子單號 |  |
| results[].itemBatchNo | Array | YES | 料品批號清單 |  |
| results[].itemBatchNo[].batchNo | String | YES | 相對應品項項目批號 |  |
| results[].itemBatchNo[].serialNos | Array | YES | 流水號清單 |  |
| results[].itemBatchNo[].serialNos[].devDateTimestamp | Integer | YES | 設備端處理時間 (UTC) |  |
| results[].itemBatchNo[].serialNos[].serialNo | String | YES | 相對應品項項目流水號 |  |
| results[].itemBatchNo[].serialNos[].value | Float | YES | 相對應品項項目重量或數量 |  |
| results[].itemBatchNo[].serialNos[].isValid | Boolean | YES | 相對應品項項目是否相符 | valid |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "serverId": "String"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.serverTimestamp | Integer | 伺服器時間戳記 |  |
| payload.serverId | String | 伺服器識別 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 驗證 request body 必填欄位與資料格式：registerNo、results、results[].devAction、results[].refNo、results[].refNoSec、results[].itemBatchNo
2. 建立設備料品資料資料
3. 回傳建立結果與必要識別資訊

### Database Tables Used

| Table | Purpose |
|----------|------|
| device | 確認設備註冊碼、硬體識別與設備角色，決定可執行的料品作業 |
| device_log | 記錄設備端料品作業送出的原始資料與處理結果 |
| goods_receipt_note | 取得採購入庫與採購退回的待作業料品 |
| inventory_order | 取得其他庫存異動的待作業料品 |
| process_order | 取得領料、退料、餘料、廢料或產出相關製造作業料品 |
| shipping_order | 取得銷售出庫與銷售退回的待作業料品 |
| work_order | 提供設備料品作業相關資料 |

## GET /item/data/group

<a id="get-item-data-group"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /item/data/group | GET | 查詢設備料品棧板群組資料 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverId": "String",
    "serverTimestamp": "Integer",
    "count": "Integer",
    "results": [
      {
        "group": "String",
        "batchNo": "String",
        "serialNos": [
          "String"
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
| payload.serverId | String | 伺服器識別 |  |
| payload.serverTimestamp | Integer | 伺服器時間戳記 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].group | String | 群組編號 |  |
| payload.results[].batchNo | String | 批號 |  |
| payload.results[].serialNos[] | String | 流水號清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 取得設備料品棧板群組資料資料
2. 計算符合條件的總筆數與本次回傳筆數
3. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

None

## POST /item/data/group

<a id="post-item-data-group"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /item/data/group | POST | 回傳設備端品項批號與棧板編號資料 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

```json
{
  "registerNo": "String",
  "total": "Integer",
  "results": [
    {
      "devDateTimestamp": "Integer",
      "devGroupNo": "String",
      "devComment": "String",
      "itemBatchNo": [
        {
          "batchNo": "String",
          "serialNos": [
            {
              "serialNo": "String",
              "value": "Float"
            }
          ]
        }
      ]
    }
  ]
}
```

| Field Path | Type | Required | Description | Enum |
|----------|----------|------|-----|---|
| registerNo | String | YES | 設備註冊碼 |  |
| total | Integer | NO | `"results"` 資料檢核碼 (SHA-256 編碼) |  |
| results | Array | YES | 資料清單 |  |
| results[].devDateTimestamp | Integer | YES | 設備端處理時間 (UTC) |  |
| results[].devGroupNo | String | YES | 設備端棧板編號 |  |
| results[].devComment | String | NO | 設備端備註 |  |
| results[].itemBatchNo | Array | YES | 料品批號清單 |  |
| results[].itemBatchNo[].batchNo | String | YES | 相對應品項項目批號 |  |
| results[].itemBatchNo[].serialNos | Array | YES | 流水號清單 |  |
| results[].itemBatchNo[].serialNos[].serialNo | String | YES | 相對應品項項目流水號 |  |
| results[].itemBatchNo[].serialNos[].value | Float | YES | 相對應品項項目重量或數量 |  |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "serverId": "String"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.serverTimestamp | Integer | 伺服器時間戳記 |  |
| payload.serverId | String | 伺服器識別 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 驗證 request body 必填欄位與資料格式：registerNo、total、results、results[].devDateTimestamp、results[].devGroupNo、results[].devComment
2. 建立設備料品棧板群組資料資料
3. 回傳建立結果與必要識別資訊

### Database Tables Used

| Table | Purpose |
|----------|------|
| batchno_serialno_group | 取得或建立棧板群組與批號流水號分派關係 |

## GET /item/groupInfo

<a id="get-item-groupInfo"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /item/groupInfo | GET | 取得「板號」相關品項項目資訊 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| registerNo | String | YES | 設備註冊碼 |
| groupNo | String | YES | 板號 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverId": "String",
    "serverTimestamp": "Integer",
    "count": "Integer",
    "results": [
      {
        "groupNo": "String",
        "itemNo": "String",
        "itemName": "String",
        "itemVendor": "String",
        "itemType": "String",
        "itemCategory": "String",
        "itemComment": "String",
        "itemBatchNo": [
          {
            "batchNo": "String",
            "validDateTimestamp": "Integer",
            "serialNos": [
              {
                "serialNo": "String",
                "value": "String"
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
| payload.serverId | String | 伺服器識別 |  |
| payload.serverTimestamp | Integer | 伺服器時間戳記 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].groupNo | String | 板號 |  |
| payload.results[].itemNo | String | 料品/品項編號 |  |
| payload.results[].itemName | String | 料品名稱 |  |
| payload.results[].itemVendor | String | 料品供應商或交易對象 |  |
| payload.results[].itemType | Integer | 品項類別 | type |
| payload.results[].itemCategory | Integer | 品項類型 | category |
| payload.results[].itemComment | String | 料品備註 |  |
| payload.results[].itemBatchNo[].batchNo | String | 批號 |  |
| payload.results[].itemBatchNo[].validDateTimestamp | Integer | 效期 (UTC) |  |
| payload.results[].itemBatchNo[].serialNos[].serialNo | String | 流水號 |  |
| payload.results[].itemBatchNo[].serialNos[].value | Float | 重量或數量 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：groupNo、registerNo
2. 查詢 batch_number、batchno_serialno_group 取得設備棧板群組資訊資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 取得或確認料品批號、效期、料品類型與類別 |
| batchno_serialno_group | 取得或建立棧板群組與批號流水號分派關係 |

## GET /item/info

<a id="get-item-info"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /item/info | GET | 取得「批號」相關品項資訊 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| registerNo | String | YES | 設備註冊碼 |
| batchNo | String | YES | 批號 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverId": "String",
    "serverTimestamp": "Integer",
    "count": "Integer",
    "results": [
      {
        "itemNo": "String",
        "itemName": "String",
        "itemVendor": "String",
        "itemType": "String",
        "itemCategory": "String",
        "itemBatchNo": "String",
        "validDateTimestamp": "Integer",
        "itemComment": "String"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.serverId | String | 伺服器識別 |  |
| payload.serverTimestamp | Integer | 伺服器時間戳記 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].itemNo | String | 料品/品項編號 |  |
| payload.results[].itemName | String | 料品名稱 |  |
| payload.results[].itemVendor | String | 料品供應商或交易對象 |  |
| payload.results[].itemType | Integer | 品項類別 | type |
| payload.results[].itemCategory | Integer | 品項類型 | category |
| payload.results[].itemBatchNo | String | 料品批號清單 |  |
| payload.results[].validDateTimestamp | Integer | 效期 (UTC) |  |
| payload.results[].itemComment | String | 料品備註 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：batchNo、registerNo
2. 查詢 batch_number 取得設備批號資訊資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 取得或確認料品批號、效期、料品類型與類別 |

## GET /item/manufacture

<a id="get-item-manufacture"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /item/manufacture | GET | 取得「產製」相關品項項目 (倉庫、產間設備適用) |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| dateTimestampUTC | String | YES | 今日時間 (UTC) |
| refProcess | String | NO | 參照製程 |
| registerNo | String | YES | 設備註冊碼 |
| shift | String | YES | 班別 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverId": "String",
    "serverTimestamp": "Integer",
    "count": "Integer",
    "results": [
      {
        "action": "Integer",
        "refNo": "String",
        "refNoSec": "String",
        "refDateTimestamp": "Integer",
        "refProcess": "Integer",
        "itemNo": "String",
        "itemName": "String",
        "itemVendor": "String",
        "itemType": "Integer",
        "itemCategory": "Integer",
        "itemAmount": "Float",
        "itemAmountUnit": "Integer",
        "itemComment": "String",
        "itemPageType": "Integer",
        "itemMaxWeight": "Float",
        "itemMinWeight": "Float",
        "itemBatchNo": [
          {
            "batchNo": "String",
            "validDateTimestamp": "Integer",
            "serialNos": [
              {
                "serialNo": "String",
                "value": "Float"
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
| payload.serverId | String | 伺服器識別 |  |
| payload.serverTimestamp | Integer | 伺服器時間戳記 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].action | Integer | 設備端處理行為 | action |
| payload.results[].refNo | String | 來源單號 |  |
| payload.results[].refNoSec | String | 來源子單號 |  |
| payload.results[].refDateTimestamp | Integer | 來源單據日期時間戳記 |  |
| payload.results[].refProcess | Integer | 派工製程 |  |
| payload.results[].itemNo | String | 料品/品項編號 |  |
| payload.results[].itemName | String | 料品名稱 |  |
| payload.results[].itemVendor | String | 料品供應商或交易對象 |  |
| payload.results[].itemType | Integer | 品項類別 | type |
| payload.results[].itemCategory | Integer | 品項類型 | category |
| payload.results[].itemAmount | Float | 排定數量 |  |
| payload.results[].itemAmountUnit | Integer | 排定數量單位 | unit |
| payload.results[].itemComment | String | 料品備註 |  |
| payload.results[].itemPageType | Integer | 畫面顯示方式 | pageType |
| payload.results[].itemMaxWeight | Float | 最大重量 |  |
| payload.results[].itemMinWeight | Float | 最小重量 |  |
| payload.results[].itemBatchNo[].batchNo | String | 批號 |  |
| payload.results[].itemBatchNo[].validDateTimestamp | Integer | 效期 (UTC) |  |
| payload.results[].itemBatchNo[].serialNos[].serialNo | String | 流水號 |  |
| payload.results[].itemBatchNo[].serialNos[].value | Float | 重量或數量 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：dateTimestampUTC、refProcess、registerNo、shift
2. 查詢 batch_number、batchno_serialno、device、goods_receipt_note 取得設備製造料品資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 取得或確認料品批號、效期、料品類型與類別 |
| batchno_serialno | 取得或寫入批號流水號、預期數量與有效狀態 |
| device | 確認設備註冊碼、硬體識別與設備角色，決定可執行的料品作業 |
| goods_receipt_note | 取得採購入庫與採購退回的待作業料品 |
| inventory_order | 取得其他庫存異動的待作業料品 |
| process_order | 取得領料、退料、餘料、廢料或產出相關製造作業料品 |
| shipping_order | 取得銷售出庫與銷售退回的待作業料品 |

## GET /item/other

<a id="get-item-other"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /item/other | GET | 取得「其他」相關品項項目 (僅倉庫設備適用) |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| dateTimestampUTC | String | YES | 今日時間 (UTC) |
| registerNo | String | YES | 設備註冊碼 |
| shift | String | YES | 班別 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverId": "String",
    "serverTimestamp": "Integer",
    "count": "Integer",
    "results": [
      {
        "action": "Integer",
        "refNo": "String",
        "refNoSec": "String",
        "refDateTimestamp": "Integer",
        "refProcess": "Integer",
        "itemNo": "String",
        "itemName": "String",
        "itemVendor": "String",
        "itemType": "Integer",
        "itemCategory": "Integer",
        "itemAmount": "Float",
        "itemAmountUnit": "Integer",
        "itemComment": "String",
        "itemPageType": "Integer",
        "itemMaxWeight": "Float",
        "itemMinWeight": "Float",
        "itemBatchNo": [
          {
            "batchNo": "String",
            "validDateTimestamp": "Integer",
            "serialNos": [
              {
                "serialNo": "String",
                "value": "Float"
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
| payload.serverId | String | 伺服器識別 |  |
| payload.serverTimestamp | Integer | 伺服器時間戳記 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].action | Integer | 設備端處理行為 | action |
| payload.results[].refNo | String | 來源單號 |  |
| payload.results[].refNoSec | String | 來源子單號 |  |
| payload.results[].refDateTimestamp | Integer | 來源單據日期時間戳記 |  |
| payload.results[].refProcess | Integer | 派工製程 |  |
| payload.results[].itemNo | String | 料品/品項編號 |  |
| payload.results[].itemName | String | 料品名稱 |  |
| payload.results[].itemVendor | String | 料品供應商或交易對象 |  |
| payload.results[].itemType | Integer | 品項類別 | type |
| payload.results[].itemCategory | Integer | 品項類型 | category |
| payload.results[].itemAmount | Float | 排定數量 |  |
| payload.results[].itemAmountUnit | Integer | 排定數量單位 | unit |
| payload.results[].itemComment | String | 料品備註 |  |
| payload.results[].itemPageType | Integer | 畫面顯示方式 | pageType |
| payload.results[].itemMaxWeight | Float | 最大重量 |  |
| payload.results[].itemMinWeight | Float | 最小重量 |  |
| payload.results[].itemBatchNo[].batchNo | String | 批號 |  |
| payload.results[].itemBatchNo[].validDateTimestamp | Integer | 效期 (UTC) |  |
| payload.results[].itemBatchNo[].serialNos[].serialNo | String | 流水號 |  |
| payload.results[].itemBatchNo[].serialNos[].value | Float | 重量或數量 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：dateTimestampUTC、registerNo、shift
2. 查詢 batch_number、batchno_serialno、device、goods_receipt_note 取得設備其他庫存料品資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 取得或確認料品批號、效期、料品類型與類別 |
| batchno_serialno | 取得或寫入批號流水號、預期數量與有效狀態 |
| device | 確認設備註冊碼、硬體識別與設備角色，決定可執行的料品作業 |
| goods_receipt_note | 取得採購入庫與採購退回的待作業料品 |
| inventory_order | 取得其他庫存異動的待作業料品 |
| process_order | 取得領料、退料、餘料、廢料或產出相關製造作業料品 |
| shipping_order | 取得銷售出庫與銷售退回的待作業料品 |

## GET /item/purchase

<a id="get-item-purchase"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /item/purchase | GET | 取得「採購」相關品項項目 (僅倉庫設備適用) |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| dateTimestampUTC | String | YES | 今日時間 (UTC) |
| registerNo | String | YES | 設備註冊碼 |
| shift | String | YES | 班別 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverId": "String",
    "serverTimestamp": "Integer",
    "count": "Integer",
    "results": [
      {
        "action": "Integer",
        "refNo": "String",
        "refNoSec": "String",
        "refDateTimestamp": "Integer",
        "refProcess": "Integer",
        "itemNo": "String",
        "itemName": "String",
        "itemVendor": "String",
        "itemType": "Integer",
        "itemCategory": "Integer",
        "itemAmount": "Float",
        "itemAmountUnit": "Integer",
        "itemComment": "String",
        "itemPageType": "Integer",
        "itemMaxWeight": "Float",
        "itemMinWeight": "Float",
        "itemBatchNo": [
          {
            "batchNo": "String",
            "validDateTimestamp": "Integer",
            "serialNos": [
              {
                "serialNo": "String",
                "value": "Float"
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
| payload.serverId | String | 伺服器識別 |  |
| payload.serverTimestamp | Integer | 伺服器時間戳記 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].action | Integer | 設備端處理行為 | action |
| payload.results[].refNo | String | 來源單號 |  |
| payload.results[].refNoSec | String | 來源子單號 |  |
| payload.results[].refDateTimestamp | Integer | 來源單據日期時間戳記 |  |
| payload.results[].refProcess | Integer | 派工製程 |  |
| payload.results[].itemNo | String | 料品/品項編號 |  |
| payload.results[].itemName | String | 料品名稱 |  |
| payload.results[].itemVendor | String | 料品供應商或交易對象 |  |
| payload.results[].itemType | Integer | 品項類別 | type |
| payload.results[].itemCategory | Integer | 品項類型 | category |
| payload.results[].itemAmount | Float | 排定數量 |  |
| payload.results[].itemAmountUnit | Integer | 排定數量單位 | unit |
| payload.results[].itemComment | String | 料品備註 |  |
| payload.results[].itemPageType | Integer | 畫面顯示方式 | pageType |
| payload.results[].itemMaxWeight | Float | 最大重量 |  |
| payload.results[].itemMinWeight | Float | 最小重量 |  |
| payload.results[].itemBatchNo[].batchNo | String | 批號 |  |
| payload.results[].itemBatchNo[].validDateTimestamp | Integer | 效期 (UTC) |  |
| payload.results[].itemBatchNo[].serialNos[].serialNo | String | 流水號 |  |
| payload.results[].itemBatchNo[].serialNos[].value | Float | 重量或數量 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：dateTimestampUTC、registerNo、shift
2. 查詢 batch_number、batchno_serialno、device、goods_receipt_note 取得設備採購入庫料品資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 取得或確認料品批號、效期、料品類型與類別 |
| batchno_serialno | 取得或寫入批號流水號、預期數量與有效狀態 |
| device | 確認設備註冊碼、硬體識別與設備角色，決定可執行的料品作業 |
| goods_receipt_note | 取得採購入庫與採購退回的待作業料品 |
| inventory_order | 取得其他庫存異動的待作業料品 |
| process_order | 取得領料、退料、餘料、廢料或產出相關製造作業料品 |
| shipping_order | 取得銷售出庫與銷售退回的待作業料品 |

## GET /item/sales

<a id="get-item-sales"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /item/sales | GET | 取得「訂購」相關品項項目 (僅倉庫設備適用) |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| dateTimestampUTC | String | YES | 今日時間 (UTC) |
| registerNo | String | YES | 設備註冊碼 |
| shift | String | YES | 班別 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverId": "String",
    "serverTimestamp": "Integer",
    "count": "Integer",
    "results": [
      {
        "action": "Integer",
        "refNo": "String",
        "refNoSec": "String",
        "refDateTimestamp": "Integer",
        "refProcess": "Integer",
        "itemNo": "String",
        "itemName": "String",
        "itemVendor": "String",
        "itemType": "Integer",
        "itemCategory": "Integer",
        "itemAmount": "Float",
        "itemAmountUnit": "Integer",
        "itemComment": "String",
        "itemPageType": "Integer",
        "itemMaxWeight": "Float",
        "itemMinWeight": "Float",
        "itemBatchNo": [
          {
            "batchNo": "String",
            "validDateTimestamp": "Integer",
            "serialNos": [
              {
                "serialNo": "String",
                "value": "Float"
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
| payload.serverId | String | 伺服器識別 |  |
| payload.serverTimestamp | Integer | 伺服器時間戳記 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].action | Integer | 設備端處理行為 | action |
| payload.results[].refNo | String | 來源單號 |  |
| payload.results[].refNoSec | String | 來源子單號 |  |
| payload.results[].refDateTimestamp | Integer | 來源單據日期時間戳記 |  |
| payload.results[].refProcess | Integer | 派工製程 |  |
| payload.results[].itemNo | String | 料品/品項編號 |  |
| payload.results[].itemName | String | 料品名稱 |  |
| payload.results[].itemVendor | String | 料品供應商或交易對象 |  |
| payload.results[].itemType | Integer | 品項類別 | type |
| payload.results[].itemCategory | Integer | 品項類型 | category |
| payload.results[].itemAmount | Float | 排定數量 |  |
| payload.results[].itemAmountUnit | Integer | 排定數量單位 | unit |
| payload.results[].itemComment | String | 料品備註 |  |
| payload.results[].itemPageType | Integer | 畫面顯示方式 | pageType |
| payload.results[].itemMaxWeight | Float | 最大重量 |  |
| payload.results[].itemMinWeight | Float | 最小重量 |  |
| payload.results[].itemBatchNo[].batchNo | String | 批號 |  |
| payload.results[].itemBatchNo[].validDateTimestamp | Integer | 效期 (UTC) |  |
| payload.results[].itemBatchNo[].serialNos[].serialNo | String | 流水號 |  |
| payload.results[].itemBatchNo[].serialNos[].value | Float | 重量或數量 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：dateTimestampUTC、registerNo、shift
2. 查詢 batch_number、batchno_serialno、device、goods_receipt_note 取得設備銷售出庫料品資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 取得或確認料品批號、效期、料品類型與類別 |
| batchno_serialno | 取得或寫入批號流水號、預期數量與有效狀態 |
| device | 確認設備註冊碼、硬體識別與設備角色，決定可執行的料品作業 |
| goods_receipt_note | 取得採購入庫與採購退回的待作業料品 |
| inventory_order | 取得其他庫存異動的待作業料品 |
| process_order | 取得領料、退料、餘料、廢料或產出相關製造作業料品 |
| shipping_order | 取得銷售出庫與銷售退回的待作業料品 |
