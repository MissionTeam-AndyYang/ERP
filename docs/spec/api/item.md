# item API Group

> Source: `restserver/package/restserver/api/item_uri.py`

## V2 Item Center APIs

> Source: `restserver/package/restserver/api/v2/items_uri.py`
> Proposal basis: `docs/spec/api-proposal/item_center_proposal.md`

## V2 API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v2/items/dashboard](#get-api-v2-items-dashboard) | GET | 查詢品項中心 KPI、分類摘要、品項清單與主檔待維護事項 | OK | 已依工程師確認提案實作 |
| [/api/v2/items/{item_no}/detail](#get-api-v2-items-item_no-detail) | GET | 查詢單一品項主檔、庫存摘要、批號摘要、BOM 使用情形與主檔維護建議 | OK | 已依工程師確認提案實作 |

## GET /api/v2/items/dashboard

<a id="get-api-v2-items-dashboard"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/items/dashboard | GET | 查詢品項中心 KPI、分類摘要、品項清單與主檔待維護事項 |

### Request Header

| Header | Description |
|----------|----------|
| x-timezone | 前端顯示偏好的 IANA timezone；後端不改寫資料庫 UTC timestamp |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| date | Integer | NO | 查詢基準時間 UTC timestamp；未提供時使用系統時間 |
| keyword | String | NO | 料品 no 或料品名稱關鍵字 |
| itemCategory | Integer | NO | 料品品項類別 code |
| itemSubCategory | Integer | NO | 料品品項子類別 code |
| masterStatusCode | String | NO | 主檔狀態 code；ready、maintenance_needed、unknown |
| hasStock | Boolean | NO | 是否只查詢目前仍有庫存的料品 |
| hasBom | Boolean | NO | 是否只查詢已關聯 BOM 或被 BOM 使用的料品 |
| start | Integer | NO | 分頁起點，預設 0；負值視為 0 |
| count | Integer | NO | 回傳筆數，預設 50，最大 100 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "summary": {
      "totalItemCount": "Integer",
      "activeItemCount": "Integer",
      "finishedGoodsCount": "Integer",
      "maintenanceItemCount": "Integer"
    },
    "categorySummary": [
      {
        "itemCategory": "Integer",
        "itemCount": "Integer",
        "stockItemCount": "Integer",
        "bomLinkedItemCount": "Integer",
        "maintenanceItemCount": "Integer"
      }
    ],
    "items": [
      {
        "itemNo": "String",
        "itemName": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "unitWarehouse": "Integer",
        "unitProduct": "Integer",
        "masterStatusCode": "String",
        "maintenanceRiskCode": "String",
        "hasStock": "Boolean",
        "currentQuantity": "Float",
        "batchCount": "Integer",
        "bomCount": "Integer"
      }
    ],
    "maintenanceSuggestions": [
      {
        "suggestionId": "String",
        "itemNo": "String",
        "suggestionTypeCode": "String",
        "riskLevelCode": "String"
      }
    ],
    "total": "Integer",
    "start": "Integer",
    "count": "Integer"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.serverTimestamp | Integer | API 回應建立時間，UTC timestamp |  |
| payload.summary.totalItemCount | Integer | 套用篩選後可納入品項中心的料品總數 |  |
| payload.summary.activeItemCount | Integer | 主檔可被業務流程引用的料品數；第一版以可查得主檔者視為 active |  |
| payload.summary.finishedGoodsCount | Integer | 製成品品項數 | itemCategory=5 |
| payload.summary.maintenanceItemCount | Integer | 主檔狀態為 maintenance_needed 的料品數 |  |
| payload.categorySummary[].itemCategory | Integer | 料品品項類別 code | EItemCategory |
| payload.categorySummary[].itemCount | Integer | 此品項類別的料品數 |  |
| payload.categorySummary[].stockItemCount | Integer | 此品項類別目前仍有庫存的料品數 |  |
| payload.categorySummary[].bomLinkedItemCount | Integer | 此品項類別已與 BOM 或產品規格建立關聯的料品數 |  |
| payload.categorySummary[].maintenanceItemCount | Integer | 此品項類別需要維護的料品數 |  |
| payload.items[].itemNo | String | 料品 no |  |
| payload.items[].itemName | String | 料品名稱 |  |
| payload.items[].itemCategory | Integer | 料品品項類別 code | EItemCategory |
| payload.items[].itemSubCategory | Integer | 料品品項子類別 code；主檔無此欄位時回傳 0 |  |
| payload.items[].unitWarehouse | Integer | 倉庫庫存單位 code |  |
| payload.items[].unitProduct | Integer | 生產用量單位 code |  |
| payload.items[].masterStatusCode | String | 主檔狀態 code | ready、maintenance_needed、unknown |
| payload.items[].maintenanceRiskCode | String | 主檔主要維護風險 code | normal、missing_unit、missing_bom、missing_stock_signal、unknown |
| payload.items[].hasStock | Boolean | 此料品目前是否仍有庫存量大於 0 |  |
| payload.items[].currentQuantity | Float | 此料品目前庫存數量總和，取至小數點第 2 位 |  |
| payload.items[].batchCount | Integer | 此料品目前仍有庫存或近期建立的不重複批號數 |  |
| payload.items[].bomCount | Integer | 此料品已關聯或被使用的 BOM / 產品規格數 |  |
| payload.maintenanceSuggestions[].suggestionId | String | 主檔維護建議識別值；不是 workflow task id |  |
| payload.maintenanceSuggestions[].itemNo | String | 維護建議對應料品 no |  |
| payload.maintenanceSuggestions[].suggestionTypeCode | String | 維護建議類型 code | missing_unit、missing_bom、missing_stock_signal |
| payload.maintenanceSuggestions[].riskLevelCode | String | 維護建議風險等級 code | normal、attention、high_risk |
| payload.total | Integer | 套用篩選後的料品筆數 |  |
| payload.start | Integer | 本次分頁起點 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Processing Flow

1. 讀取 query parameters 並轉換為後端型別。
2. 從 `material`、`inproduct`、`product`、`goods` 建立料品主檔候選集合。
3. 使用 Warehouse 輕量品項庫存摘要共用邏輯取得目前庫存、可用數量、預留數量、品檢保留數量、批號數與倉庫數；此流程只查詢品項庫存摘要所需欄位，不建立完整 Warehouse Dashboard payload。
4. 查詢 `bom_item`、`product_spec`、`product_bom_spec`、`inproduct_bom_spec`，彙總每個料品的 `bomCount`。
5. 依缺單位、製成品/在製品缺 BOM、原料/物料/膠捲缺庫存與近期批號訊號，判斷 `masterStatusCode` 與 `maintenanceRiskCode`。
6. 套用篩選、排序與分頁，建立 `summary`、`categorySummary`、`items[]` 與 read-only `maintenanceSuggestions[]`。

### Database Tables Used

| Table | Purpose |
|----------|------|
| material | 原料、物料、膠捲主檔 |
| inproduct | 在製品主檔 |
| product | 製成品主檔 |
| goods | 貨品主檔 |
| batch_number | 料品近期批號 |
| inventory_record | Warehouse 輕量品項庫存摘要共用邏輯使用的庫存異動來源 |
| warehouse_inventory_reservation | Warehouse 輕量品項庫存摘要共用邏輯使用的預留數量來源 |
| warehouse_quality_hold | Warehouse 輕量品項庫存摘要共用邏輯使用的品檢保留數量來源 |
| bom | BOM 版本與有效日期 |
| bom_item | BOM 直接配方明細 |
| product_spec | 製成品與 BOM / 料品規格關聯 |
| product_bom_spec | 製成品 BOM 階層關聯 |
| inproduct_bom_spec | 在製品 BOM 關聯 |

## GET /api/v2/items/{item_no}/detail

<a id="get-api-v2-items-item_no-detail"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/items/{item_no}/detail | GET | 查詢單一品項主檔、庫存摘要、批號摘要、BOM 使用情形與主檔維護建議 |

### Request Header

| Header | Description |
|----------|----------|
| x-timezone | 前端顯示偏好的 IANA timezone；後端不改寫資料庫 UTC timestamp |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| date | Integer | NO | 查詢基準時間 UTC timestamp；未提供時使用系統時間 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "item": {
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "itemSubCategory": "Integer",
      "unitWarehouse": "Integer",
      "unitProduct": "Integer",
      "masterStatusCode": "String",
      "maintenanceRiskCode": "String",
      "creationTime": "Integer"
    },
    "inventorySummary": {
      "hasStock": "Boolean",
      "currentQuantity": "Float",
      "availableQuantity": "Float",
      "reservedQuantity": "Float",
      "qualityHoldQuantity": "Float",
      "warehouseCount": "Integer",
      "batchCount": "Integer"
    },
    "bomUsage": [
      {
        "bomNo": "String",
        "bomVersion": "Integer",
        "quantity": "Float",
        "unit": "Integer",
        "effectiveTimestamp": "Integer"
      }
    ],
    "recentBatches": [
      {
        "batchNo": "String",
        "refCategory": "Integer",
        "refNo": "String",
        "currentQuantity": "Float",
        "unit": "Integer",
        "validDate": "Integer",
        "riskLevelCode": "String"
      }
    ],
    "maintenanceSuggestions": [
      {
        "suggestionId": "String",
        "suggestionTypeCode": "String",
        "riskLevelCode": "String"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.serverTimestamp | Integer | API 回應建立時間，UTC timestamp |  |
| payload.item.itemNo | String | 查詢料品 no |  |
| payload.item.itemName | String | 料品名稱 |  |
| payload.item.itemCategory | Integer | 料品品項類別 code | EItemCategory |
| payload.item.itemSubCategory | Integer | 料品品項子類別 code；主檔無此欄位時回傳 0 |  |
| payload.item.unitWarehouse | Integer | 倉庫庫存單位 code |  |
| payload.item.unitProduct | Integer | 生產用量單位 code |  |
| payload.item.masterStatusCode | String | 主檔狀態 code | ready、maintenance_needed、unknown |
| payload.item.maintenanceRiskCode | String | 主檔主要維護風險 code | normal、missing_unit、missing_bom、missing_stock_signal、unknown |
| payload.item.creationTime | Integer | 主檔建立時間 UTC timestamp；無資料時回傳 0 |  |
| payload.inventorySummary.hasStock | Boolean | 此料品目前是否仍有庫存量大於 0 |  |
| payload.inventorySummary.currentQuantity | Float | 此料品目前庫存數量總和，取至小數點第 2 位 |  |
| payload.inventorySummary.availableQuantity | Float | 此料品目前可用數量總和，取至小數點第 2 位 |  |
| payload.inventorySummary.reservedQuantity | Float | 此料品目前預留數量總和，取至小數點第 2 位 |  |
| payload.inventorySummary.qualityHoldQuantity | Float | 此料品目前品檢保留數量總和，取至小數點第 2 位 |  |
| payload.inventorySummary.warehouseCount | Integer | 此料品目前庫存所在的不重複倉庫數 |  |
| payload.inventorySummary.batchCount | Integer | 此料品目前仍有庫存的不重複批號數 |  |
| payload.bomUsage[].bomNo | String | 關聯 BOM no |  |
| payload.bomUsage[].bomVersion | Integer | 關聯 BOM 版本 |  |
| payload.bomUsage[].quantity | Float | 此 BOM 關聯用量，取至小數點第 2 位 |  |
| payload.bomUsage[].unit | Integer | 此 BOM 關聯單位 code |  |
| payload.bomUsage[].effectiveTimestamp | Integer | BOM 版本有效日期 UTC timestamp；無資料時回傳 0 |  |
| payload.recentBatches[].batchNo | String | 此料品近期批號 |  |
| payload.recentBatches[].refCategory | Integer | 批號來源單據類別 |  |
| payload.recentBatches[].refNo | String | 批號來源單號 |  |
| payload.recentBatches[].currentQuantity | Float | 此批號目前庫存數量，取至小數點第 2 位 |  |
| payload.recentBatches[].unit | Integer | 批號單位 code |  |
| payload.recentBatches[].validDate | Integer | 批號有效期限 UTC timestamp |  |
| payload.recentBatches[].riskLevelCode | String | 批號風險等級 code | normal、attention、high_risk |
| payload.maintenanceSuggestions[].suggestionId | String | 主檔維護建議識別值；不是 workflow task id |  |
| payload.maintenanceSuggestions[].suggestionTypeCode | String | 維護建議類型 code | missing_unit、missing_bom、missing_stock_signal |
| payload.maintenanceSuggestions[].riskLevelCode | String | 維護建議風險等級 code | normal、attention、high_risk |

### Processing Flow

1. 驗證 `item_no`，若空字串或查無主檔則回傳錯誤。
2. 從 `material`、`inproduct`、`product`、`goods` 讀取單一料品主檔。
3. 使用 Warehouse 輕量品項庫存摘要共用邏輯彙總庫存摘要。
4. 查詢 BOM 相關資料表建立 `bomUsage[]`。
5. 查詢 `batch_number` 建立最多 20 筆近期批號摘要。
6. 使用 dashboard 同一套規則建立 read-only `maintenanceSuggestions[]`。

### Database Tables Used

| Table | Purpose |
|----------|------|
| material | 原料、物料、膠捲主檔 |
| inproduct | 在製品主檔 |
| product | 製成品主檔 |
| goods | 貨品主檔 |
| batch_number | 料品近期批號、來源單據與效期 |
| inventory_record | Warehouse 輕量品項庫存摘要共用邏輯使用的庫存異動來源 |
| warehouse_inventory_reservation | Warehouse 輕量品項庫存摘要共用邏輯使用的預留數量來源 |
| warehouse_quality_hold | Warehouse 輕量品項庫存摘要共用邏輯使用的品檢保留數量來源 |
| bom | BOM 版本與有效日期 |
| bom_item | BOM 直接配方明細 |
| product_spec | 製成品與 BOM / 料品規格關聯 |
| product_bom_spec | 製成品 BOM 階層關聯 |
| inproduct_bom_spec | 在製品 BOM 關聯 |

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
