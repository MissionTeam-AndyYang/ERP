# Product / WIP 360 API Group

> Source: `restserver/package/restserver/api/v2/product_wip_360_uri.py`
> Proposal Source: `docs/spec/api-proposal/product_wip_360_overview_proposal.md`
> Flow Source: `docs/spec/api-proposal/product_wip_360_overview_flow_algorithm.md`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v2/product-wip-360/overview](#get-api-v2-product-wip-360-overview) | GET | 查詢指定製成品或在製品的 360 唯讀總覽 | OK | CP1 read-only BFF composition；組合 Item、交易品項、Warehouse、BOM、Recipe、Routing 既有唯讀能力，不新增 Product/WIP 寫入、不修改資料庫 schema。 |

## GET /api/v2/product-wip-360/overview

<a id="get-api-v2-product-wip-360-overview"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/product-wip-360/overview | GET | 查詢指定製成品或在製品的 360 唯讀總覽 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 時區代碼，例如 Asia/Taipei |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|----------|----------------|
| itemNo | String | YES | 查詢主體的內部料品 no；製成品對應 `product.no`，在製品對應 `inproduct.no`。 |
| itemCategory | Integer | YES | 查詢主體的料品品項類別；僅支援 `4` 在製品、`5` 製成品。 |
| effectiveDate | Integer | NO | BOM、Recipe、Routing 版本判定使用的 UTC timestamp；未提供時使用伺服器目前時間。 |
| inventoryDate | Integer | NO | Warehouse/Inventory 快照計算基準 UTC timestamp；未提供時同 `effectiveDate`。 |
| productVersion | Integer | NO | 製成品版本；僅製成品主體適用，未提供時使用 `product.version`。 |
| includeModules | String | NO | 逗號分隔的模組白名單，允許 `item,transactionItem,warehouse,bom,recipe,routing`；未提供時查詢全部模組。 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "timezone": "String",
    "requestIdentity": {
      "itemNo": "String",
      "itemCategory": "Integer",
      "effectiveDate": "Integer",
      "inventoryDate": "Integer",
      "productVersion": "Integer"
    },
    "subject": {
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "itemSubCategory": "Integer",
      "productVersion": "Integer",
      "unitShipping": "Integer",
      "unitWarehouse": "Integer",
      "unitProduct": "Integer",
      "comment": "String",
      "sourceCode": "String"
    },
    "itemDetail": {},
    "transactionContext": {
      "linkedTransactionItemStatusCode": "String",
      "total": "Integer",
      "transactionItems": [
        {
          "transItemNo": "String",
          "transItemName": "String",
          "transItemCategory": "Integer",
          "companyNo": "String",
          "companyName": "String",
          "linkedItemNo": "String",
          "linkedItemName": "String",
          "contractNo": "String",
          "contractDate": "Integer",
          "tradeUnit": "Integer",
          "tradePrice": "Float"
        }
      ]
    },
    "inventoryOverview": {
      "hasStock": "Boolean",
      "currentQuantity": "Float",
      "availableQuantity": "Float",
      "reservedQuantity": "Float",
      "qualityHoldQuantity": "Float",
      "inventoryValue": "Integer",
      "availableValue": "Integer",
      "warehouseCount": "Integer",
      "batchCount": "Integer",
      "riskTypes": ["String"]
    },
    "batchHighlights": [
      {
        "inventoryId": "String",
        "warehouseNo": "String",
        "warehouseName": "String",
        "itemNo": "String",
        "itemName": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "batchNo": "String",
        "serialNo": "String",
        "currentQuantity": "Float",
        "reservedQuantity": "Float",
        "availableQuantity": "Float",
        "qualityHoldQuantity": "Float",
        "unit": "Integer",
        "unitCost": "Float",
        "inventoryValue": "Integer",
        "reservedValue": "Integer",
        "availableValue": "Integer",
        "qualityHoldValue": "Integer",
        "palletCount": "Float",
        "safetyStock": "Float",
        "validDays": "Integer",
        "validDate": "Integer",
        "firstInboundTimestamp": "Integer",
        "daysInStock": "Integer",
        "sourceNo": "String",
        "sourceRefCategory": "Integer",
        "qualityStatus": "String",
        "riskTypes": ["String"]
      }
    ],
    "productStructure": {},
    "recipeFormula": {},
    "routingProcess": {},
    "moduleReadiness": [
      {
        "moduleCode": "String",
        "statusCode": "String",
        "sourceCode": "String",
        "warningCodes": ["String"]
      }
    ],
    "sourceLineage": {
      "item": {
        "sourceCode": "String",
        "sourceRefNo": "String"
      },
      "transactionItem": {
        "sourceCode": "String",
        "sourceRefNo": "String"
      },
      "warehouse": {
        "sourceCode": "String",
        "sourceRefNo": "String"
      },
      "bom": {
        "sourceCode": "String",
        "sourceRefNo": "String"
      },
      "recipe": {
        "sourceCode": "String",
        "sourceRefNo": "String"
      },
      "routing": {
        "sourceCode": "String",
        "sourceRefNo": "String"
      }
    },
    "warnings": [
      {
        "moduleCode": "String",
        "warningCode": "String",
        "refNo": "String"
      }
    ],
    "capabilityBoundary": {
      "readOnly": "Boolean",
      "productWriteSupported": "Boolean",
      "bomWriteSupported": "Boolean",
      "recipeWriteSupported": "Boolean",
      "routingWriteSupported": "Boolean",
      "wipWriteSupported": "Boolean",
      "sourceOfTruthTransitionSupported": "Boolean",
      "cutoverSupported": "Boolean",
      "goLiveSupported": "Boolean"
    }
  }
}
```

### Field Description

| Field | Type | Description |
|----------|----------|----------------|
| payload.serverTimestamp | Integer | 後端產生回應的 UTC timestamp。 |
| payload.timezone | String | Request header 傳入的時區；未提供時回傳 `UTC`。 |
| payload.requestIdentity | Object | 本次查詢的 canonical request identity。 |
| payload.requestIdentity.itemNo | String | 查詢主體內部料品 no。 |
| payload.requestIdentity.itemCategory | Integer | 查詢主體料品品項類別；4 為在製品，5 為製成品。 |
| payload.requestIdentity.effectiveDate | Integer | BOM、Recipe、Routing 版本判定時間。 |
| payload.requestIdentity.inventoryDate | Integer | Warehouse/Inventory 快照計算時間。 |
| payload.requestIdentity.productVersion | Integer | 製成品版本；在製品或未指定時可為 0。 |
| payload.subject | Object | Product/WIP 主體主檔資料。 |
| payload.subject.itemNo | String | 主體料品 no。 |
| payload.subject.itemName | String | 主體料品名稱。 |
| payload.subject.itemCategory | Integer | 主體料品品項類別。 |
| payload.subject.itemSubCategory | Integer | 主體在原主檔中的細分類別；製成品來自 `product.category`，在製品來自 `inproduct.category`。 |
| payload.subject.productVersion | Integer | 製成品目前版本；在製品為 0。 |
| payload.subject.unitShipping | Integer | 出貨單位代碼。 |
| payload.subject.unitWarehouse | Integer | 倉儲單位代碼。 |
| payload.subject.unitProduct | Integer | 生產單位代碼。 |
| payload.subject.comment | String | 主檔備註。 |
| payload.subject.sourceCode | String | 主體來源代碼；製成品為 `product`，在製品為 `inproduct`。 |
| payload.itemDetail | Object | 既有 `CItemCenterService.get_detail()` 回傳的品項明細資料；若模組不可用則為空物件。 |
| payload.transactionContext.linkedTransactionItemStatusCode | String | 交易品項模組狀態；可能為 `complete`、`partial`、`unavailable`、`error`。 |
| payload.transactionContext.total | Integer | 關聯交易品項筆數。 |
| payload.transactionContext.transactionItems[].transItemNo | String | 交易品項 no。 |
| payload.transactionContext.transactionItems[].transItemName | String | 交易品項名稱。 |
| payload.transactionContext.transactionItems[].transItemCategory | Integer | 交易品項類別代碼。 |
| payload.transactionContext.transactionItems[].companyNo | String | 交易品項對應客戶或供應商 no。 |
| payload.transactionContext.transactionItems[].companyName | String | 交易品項對應客戶或供應商名稱。 |
| payload.transactionContext.transactionItems[].linkedItemNo | String | 交易品項已連結的內部料品 no。 |
| payload.transactionContext.transactionItems[].linkedItemName | String | 交易品項已連結的內部料品名稱。 |
| payload.transactionContext.transactionItems[].contractNo | String | 最新合約 no；依 `contract.item_no = trans_items.no` 並取最新日期。 |
| payload.transactionContext.transactionItems[].contractDate | Integer | 最新合約日期 UTC timestamp。 |
| payload.transactionContext.transactionItems[].tradeUnit | Integer | 最新合約交易單位。 |
| payload.transactionContext.transactionItems[].tradePrice | Float | 最新合約交易單價，取小數點第 4 位。 |
| payload.inventoryOverview.hasStock | Boolean | 是否存在大於 0 的庫存數量。 |
| payload.inventoryOverview.currentQuantity | Float | 目前庫存總數量，取小數點第 2 位。 |
| payload.inventoryOverview.availableQuantity | Float | 目前可用庫存總數量，取小數點第 2 位。 |
| payload.inventoryOverview.reservedQuantity | Float | 目前預留庫存總數量，取小數點第 2 位。 |
| payload.inventoryOverview.qualityHoldQuantity | Float | 目前品檢保留總數量，取小數點第 2 位。 |
| payload.inventoryOverview.inventoryValue | Integer | 目前庫存總價值，金額四捨五入取整數。 |
| payload.inventoryOverview.availableValue | Integer | 目前可用庫存總價值，金額四捨五入取整數。 |
| payload.inventoryOverview.warehouseCount | Integer | 有庫存的倉庫數。 |
| payload.inventoryOverview.batchCount | Integer | 有庫存的批號數。 |
| payload.inventoryOverview.riskTypes | Array | 來自倉庫庫存模組的風險類型代碼集合。 |
| payload.batchHighlights[] | Array | 由 `GET /api/v2/warehouse/inventory` 取得的批號庫存摘要，最多回傳前 10 筆。 |
| payload.productStructure | Object | 製成品 BOM/Product Structure 子模組資料；在製品尚未治理為 root 時回傳空物件並帶 warning。 |
| payload.recipeFormula | Object | 製成品 Recipe Formula 子模組資料；在製品尚未治理為 root 時回傳空物件並帶 warning。 |
| payload.routingProcess | Object | Routing current 子模組資料，保留其 `sourceLineage`、`warnings` 與 `capabilityBoundary`。 |
| payload.moduleReadiness[].moduleCode | String | 子模組代碼：`item`、`transactionItem`、`warehouse`、`bom`、`recipe`、`routing`。 |
| payload.moduleReadiness[].statusCode | String | 子模組狀態：`complete`、`partial`、`unavailable`、`test_support`、`error`。 |
| payload.moduleReadiness[].sourceCode | String | 子模組資料來源代碼。 |
| payload.moduleReadiness[].warningCodes | Array | 子模組警示代碼集合。 |
| payload.sourceLineage | Object | 各子模組資料來源追蹤資訊。 |
| payload.warnings[].moduleCode | String | 發出警示的子模組代碼。 |
| payload.warnings[].warningCode | String | 警示代碼，前端負責多國語言字串轉換。 |
| payload.warnings[].refNo | String | 警示對應參考 no。 |
| payload.capabilityBoundary.readOnly | Boolean | 本 API 是否為唯讀。 |
| payload.capabilityBoundary.productWriteSupported | Boolean | CP1 不支援 Product 寫入，固定 `false`。 |
| payload.capabilityBoundary.bomWriteSupported | Boolean | CP1 不支援 BOM 寫入，固定 `false`。 |
| payload.capabilityBoundary.recipeWriteSupported | Boolean | CP1 不支援 Recipe 寫入，固定 `false`。 |
| payload.capabilityBoundary.routingWriteSupported | Boolean | CP1 不支援 Routing 寫入，固定 `false`。 |
| payload.capabilityBoundary.wipWriteSupported | Boolean | CP1 不支援 WIP 寫入，固定 `false`。 |
| payload.capabilityBoundary.sourceOfTruthTransitionSupported | Boolean | CP1 不進行 Source-of-Truth transition，固定 `false`。 |
| payload.capabilityBoundary.cutoverSupported | Boolean | CP1 不進行 Cutover，固定 `false`。 |
| payload.capabilityBoundary.goLiveSupported | Boolean | CP1 不進行 Go-Live，固定 `false`。 |

### Processing Flow

1. 解析 `itemNo`、`itemCategory`、`effectiveDate`、`inventoryDate`、`productVersion` 與 `includeModules`。
2. 驗證 `itemNo` 不可為空，且 `itemCategory` 僅允許 4 或 5；其他類別回傳 validation error。
3. 依 `itemCategory` 查詢對應主檔：在製品查 `inproduct.no`，製成品查 `product.no`；不得跨表推測主體。
4. 若主檔不存在，回傳 not found。
5. 建立 request identity、subject、capability boundary 與 module execution plan。
6. Item 模組呼叫 `CItemCenterService.get_detail()`，保留既有品項明細回傳。
7. Transaction Item 模組查詢 `trans_items.item_no = itemNo`，並以 `contract.item_no = trans_items.no` 取得最新合約資料。
8. Warehouse 模組呼叫 `CWarehouseInventoryService.get_inventory()`，沿用已確認的庫存快照與零庫存過濾規則，彙總庫存數量與價值。
9. 製成品主體呼叫 BOM Product Structure 與 Recipe by Product；在製品主體若尚未治理為 root，回傳 partial/unavailable warning，不反向推測下游製成品。
10. Routing 模組呼叫 `CRoutingProcessFlowService.get_current()`，保留 routing sourceLineage、warnings 與 test-support 狀態。
11. 彙整 `moduleReadiness[]`、`sourceLineage` 與 `warnings[]`。
12. 回傳唯讀 overview payload；此 endpoint 未註冊 POST/PUT/PATCH/DELETE。

### Database Tables Used

| Table | Usage |
|----------|----------|
| product | 製成品主體主檔。 |
| inproduct | 在製品主體主檔。 |
| trans_items | 查詢內部料品對應的交易品項。 |
| contract | 查詢交易品項最新合約資料。 |
| inventory_record / inventory_item_month_statistic / inventory_delta | 透過 Warehouse 庫存服務計算庫存快照。 |
| batch_number | 透過 Warehouse 庫存服務取得批號與來源資訊。 |
| product_spec / inproduct_bom_spec / bom / bom_item | 透過 BOM 與 Recipe 服務取得產品結構與配方資訊。 |
| product_process / process_flow / process / process_capacity | 透過 Routing 服務取得製程與工序資訊。 |

### Error Response

| HTTP Status | Code | Message | Description |
|----------|----------|----------|----------------|
| 400 | 3001 | itemNo is required | 未提供查詢主體 no。 |
| 400 | 3001 | invalid itemCategory | `itemCategory` 不是 4 或 5。 |
| 404 | 1 | record not found | 查詢主體不存在於指定主檔。 |
| 405 | - | - | 本 API 未提供 POST/PUT/PATCH/DELETE。 |
