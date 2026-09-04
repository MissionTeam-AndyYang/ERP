# Product / WIP 360 Read-Only Overview API Proposal

> Status: Proposal Refinement / Pending Engineer Review
> Work Item ID: ERP2-CP1-PRODUCT-WIP-360-RO-DESIGN-REFINE-001
> Authority Reference: ERP2-CIO-CP1-PRODUCT-WIP-360-RO-DESIGN-REFINE-001
> Target UI Preview: `docs/spec/api-proposal/product_wip_360_overview_static_preview.html`
> Flow / Algorithm: `docs/spec/api-proposal/product_wip_360_overview_flow_algorithm.md`
> Purpose: 依 CTO Office 要求，細化 Product / WIP 360 read-only overview 的 bounded BFF / composition API 提案。本文件不代表 runtime endpoint 已實作。

## 文件邊界

本文件只進行 API proposal refinement，不授權後端 endpoint 實作、不修改 `restserver/` 程式、不新增或修改資料庫 schema、不建立 Product write、不進行 Production、migration、Source-of-Truth transition、Cutover 或 Go-Live。

必須保留：

```txt
API_PROPOSAL_REFINEMENT != API_IMPLEMENTATION
BFF_CONTRACT != NEW_SOURCE_OF_TRUTH
```

## API Summary

| URL | Method | Description | Status | Review Note |
| --- | --- | --- | --- | --- |
| `/api/v2/product-overview/items/{item_no}/overview` | GET | 查詢指定製成品或在製品的 360 read-only overview | Proposal / Pending Engineer Review | Bounded BFF composition candidate；僅組合既有 read-only Item / TransItems / Warehouse / BOM / Recipe / Routing 能力，不建立新權威來源。 |

## 1. Request Identity Contract

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/product-overview/items/{item_no}/overview` | GET | 查詢指定製成品或在製品的 360 read-only overview |

### Request Header

| Header | Description |
| --- | --- |
| `x-auth-token` | 存取金鑰 |
| `x-timezone` | 前端顯示偏好的 IANA timezone；後端不改寫資料庫 UTC timestamp |

### Path Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `item_no` | String | YES | 查詢主體的內部料品 no；Product 對應 `product.no`，WIP 對應 `inproduct.no` |

### Query Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `itemCategory` | Integer | YES | 查詢主體料品品項類別；僅允許 `4` 在製品或 `5` 製成品 |
| `effectiveDate` | Integer | NO | BOM / Recipe / Routing 版本選擇基準 UTC timestamp；未提供時使用伺服器目前時間 |
| `inventoryDate` | Integer | NO | Warehouse / Inventory 快照計算基準 UTC timestamp；未提供時同 `effectiveDate`，若兩者皆未提供則使用伺服器目前時間 |
| `productVersion` | Integer | NO | 製成品版本；僅 Product 主體適用。未提供時由 Product Structure / Recipe / Routing 各模組依既有規則選擇並回報來源 |
| `includeModules` | String | NO | 逗號分隔模組白名單；允許值 `item,transactionItem,warehouse,bom,recipe,routing`。未提供時查詢全部模組 |

## 2. Product / WIP Subject Type Handling

| Subject | itemCategory | Primary table | Handling |
| --- | --- | --- | --- |
| Product / 製成品 | `5` | `product` | 可組合 Item、TransItems、Warehouse、BOM Product Structure、Recipe by product、Routing current/versions。 |
| WIP / 在製品 | `4` | `inproduct` | 可組合 Item、Warehouse、Routing current/versions；BOM / Recipe 能力需依 `inproduct_bom_spec` 與既有 Product Structure / Recipe contract 可追溯程度回傳 partial 或 unavailable。 |

處理規則：

1. `itemCategory` 必須由前端明確傳入，避免同一 `item_no` 在不同主檔表可能存在時產生歧義。
2. 後端只接受 Product / WIP，其他類別回傳 validation error。
3. Product/WIP 360 的 canonical key 為 `itemNo + itemCategory`。
4. 若主檔不存在，回傳 not found，不由其他模組推測主體。

## 3. Module Composition Model

此 API 是 read-only BFF composition candidate，組合下列既有 API/service contract：

| Module code | Source API family | Composition purpose |
| --- | --- | --- |
| `item` | `GET /api/v2/items/{item_no}/detail` | 主檔、單位、主檔狀態、庫存摘要、近期批號、BOM usage。 |
| `transactionItem` | `GET /api/v2/transitems/dashboard` / detail family | 交易品項、客戶/供應商、合約與商務資料完整度。 |
| `warehouse` | `GET /api/v2/warehouse/inventory` / lots family | 目前庫存、可用/預留/品檢保留、庫存價值、批號與倉庫分布。 |
| `bom` | `GET /api/v2/bom/product-structure/{product_no}` | Product Structure tree、BOM evidence、structure warnings。 |
| `recipe` | `GET /api/v2/recipe-formula/by-product/{product_no}` | Formula input/output、Recipe version、Recipe warnings 與 sourceLineage。 |
| `routing` | `GET /api/v2/routing/products/{item_no}/current` | 目前生效 Routing、ordered steps、process context、capabilityBoundary 與 warnings。 |

BFF 不重新定義業務邏輯權威。若某模組無資料或尚未支援 WIP root，必須回傳 module status 與 warning，不得用空成功資料假裝完整。

## 4. Response Payload Proposal

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
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
      "unitWarehouse": "Integer",
      "unitProduct": "Integer",
      "masterStatusCode": "String",
      "subjectSourceCode": "String"
    },
    "moduleReadiness": [
      {
        "moduleCode": "String",
        "statusCode": "String",
        "sourceCode": "String",
        "warningCodes": ["String"]
      }
    ],
    "transactionContext": {
      "linkedTransactionItemStatusCode": "String",
      "transactionItems": [
        {
          "transItemNo": "String",
          "transItemName": "String",
          "companyNo": "String",
          "companyDisplayName": "String",
          "contractNo": "String",
          "tradeUnit": "Integer",
          "tradePrice": "Float",
          "dataQualityCode": "String"
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
        "batchNo": "String",
        "warehouseNo": "String",
        "warehouseName": "String",
        "currentQuantity": "Float",
        "availableQuantity": "Float",
        "unit": "Integer",
        "validDate": "Integer",
        "riskLevelCode": "String",
        "refCategory": "Integer",
        "refNo": "String"
      }
    ],
    "productStructure": {
      "statusCode": "String",
      "rootProductNo": "String",
      "rootProductVersion": "Integer",
      "bomEvidence": [],
      "children": [],
      "warnings": []
    },
    "recipeFormula": {
      "statusCode": "String",
      "recipeVersions": [],
      "sourceLineage": {},
      "warnings": []
    },
    "routingProcess": {
      "statusCode": "String",
      "routingVersion": {},
      "steps": [],
      "sourceLineage": {},
      "capabilityBoundary": {},
      "warnings": []
    },
    "sourceLineage": {
      "itemSourceCode": "String",
      "transactionItemSourceCode": "String",
      "warehouseSourceCode": "String",
      "bomSourceCode": "String",
      "recipeSourceCode": "String",
      "routingSourceCode": "String"
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
      "workflowMutationSupported": "Boolean",
      "sourceOfTruthTransitionSupported": "Boolean"
    }
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| `payload.serverTimestamp` | Integer | API 回應建立時間，UTC timestamp |  |
| `payload.requestIdentity.itemNo` | String | 本次查詢主體料品 no |  |
| `payload.requestIdentity.itemCategory` | Integer | 本次查詢主體料品品項類別 | EItemCategory，僅 4 / 5 |
| `payload.requestIdentity.effectiveDate` | Integer | BOM / Recipe / Routing 採用的版本判斷基準時間 |  |
| `payload.requestIdentity.inventoryDate` | Integer | Warehouse 庫存快照採用的查詢基準時間 |  |
| `payload.requestIdentity.productVersion` | Integer | 指定或採用的製成品版本；WIP 或未指定時可回傳 0 |  |
| `payload.subject.itemNo` | String | 主體料品 no |  |
| `payload.subject.itemName` | String | 主體料品名稱 |  |
| `payload.subject.itemCategory` | Integer | 主體料品類別 code | EItemCategory |
| `payload.subject.itemSubCategory` | Integer | 主體料品子類別 code |  |
| `payload.subject.unitWarehouse` | Integer | 倉庫庫存單位 code | Unit |
| `payload.subject.unitProduct` | Integer | 生產用量單位 code | Unit |
| `payload.subject.masterStatusCode` | String | 主檔狀態 code | ready / maintenance_needed / unknown |
| `payload.subject.subjectSourceCode` | String | 主體主檔來源 code | product / inproduct |
| `payload.moduleReadiness[].moduleCode` | String | 子模組代碼 | item / transactionItem / warehouse / bom / recipe / routing |
| `payload.moduleReadiness[].statusCode` | String | 子模組資料可用狀態 | complete / partial / unavailable / test_support / error |
| `payload.moduleReadiness[].sourceCode` | String | 子模組主要來源 code；若為 test-support 必須明確回傳 |  |
| `payload.moduleReadiness[].warningCodes[]` | String | 子模組 warning code 清單 |  |
| `payload.transactionContext.linkedTransactionItemStatusCode` | String | 交易品項關聯狀態 code | linked / missing / unavailable / unknown |
| `payload.transactionContext.transactionItems[]` | Array | 與主體料品關聯的交易品項摘要 |  |
| `payload.inventoryOverview` | Object | 指定 Product/WIP 的庫存摘要，欄位語意沿用 Item / Warehouse API |  |
| `payload.batchHighlights[]` | Array | 指定 Product/WIP 的重點批號與倉庫分布摘要，優先取仍有庫存且風險較高批號 |  |
| `payload.productStructure` | Object | Product Structure summary；Product 主體優先提供，WIP 主體若無受治理 root contract 則回傳 partial 或 unavailable |  |
| `payload.recipeFormula` | Object | Recipe / Formula summary；Product 主體優先提供，WIP 主體若無受治理 root output contract 則回傳 partial 或 unavailable |  |
| `payload.routingProcess` | Object | Routing / Process Flow summary；Product 與 WIP 均以 `itemNo` 查詢 routing current |  |
| `payload.sourceLineage` | Object | CP1 composition 層對各模組主要資料來源的摘要，不取代各模組內部 sourceLineage |  |
| `payload.warnings[]` | Array | CP1 composition 層彙整 warning；必須保留 moduleCode、warningCode、refNo |  |
| `payload.capabilityBoundary.readOnly` | Boolean | 本 API 是否為 read-only；固定 true |  |
| `payload.capabilityBoundary.productWriteSupported` | Boolean | 是否支援 Product 寫入；固定 false |  |
| `payload.capabilityBoundary.bomWriteSupported` | Boolean | 是否支援 BOM 寫入；固定 false |  |
| `payload.capabilityBoundary.recipeWriteSupported` | Boolean | 是否支援 Recipe 寫入；固定 false |  |
| `payload.capabilityBoundary.routingWriteSupported` | Boolean | 是否支援 Routing 寫入；固定 false |  |
| `payload.capabilityBoundary.workflowMutationSupported` | Boolean | 是否支援 workflow mutation；固定 false |  |
| `payload.capabilityBoundary.sourceOfTruthTransitionSupported` | Boolean | 是否支援 Source-of-Truth transition；固定 false |  |

## 5. Domain References

| Domain | Formal API document | Primary tables |
| --- | --- | --- |
| Item | `docs/spec/api/item.md` | `material`、`inproduct`、`product`、`goods` |
| Transaction Item | `docs/spec/api/transitems.md` | `company`、`payment`、`trans_items`、`contract` |
| Warehouse | `docs/spec/api/warehouse.md` | `inventory_item_month_statistic`、`inventory_delta`、`inventory_record`、`batch_number`、warehouse extension tables |
| BOM | `docs/spec/api/bom.md` | `bom`、`bom_item`、`product_spec`、`product_bom_spec`、`inproduct_bom_spec` |
| Recipe / Formula | `docs/spec/api/recipe_formula.md` | `bom`、`bom_item`、`product_spec` |
| Routing / Process Flow | `docs/spec/api/routing.md` | `product_process`、`process_flow`、`process`、`process_capacity`、`product_spec`、`product_bom_spec` |

## 6. Source-Lineage And Warning Model

規則：

1. 各子模組原有 `sourceLineage`、`warnings[]`、`warningCodes[]`、`capabilityBoundary` 不得被 BFF 合併時移除。
2. BFF 可新增 CP1 層的 `moduleReadiness[]` 與 `warnings[]`，但不得改寫子模組 warning code。
3. test-support evidence 必須以 `statusCode=test_support` 或 `sourceCode=test_support` 顯示，不得當成 complete formal source。
4. 後端只回傳 enum / code；多國語系顯示文字由前端負責。

## 7. Partial / Unavailable / Test-Support Treatment

| Treatment | Meaning | Payload behavior |
| --- | --- | --- |
| `complete` | 模組可依正式資料來源回傳目前畫面所需資料 | 回傳資料集與空 warning 或非阻塞 warning |
| `partial` | 模組可回傳部分資料，但存在資料缺漏或主體 coverage 不完整 | 保留可得資料，回傳 warning code |
| `unavailable` | 模組不支援該主體或查無必要資料 | 回傳空物件或空陣列，並回傳 warning code |
| `test_support` | 模組資料來自 Shared DEV test-support readonly surface | 保留資料，但明確標示 test-support source |
| `error` | 子模組呼叫或查詢發生錯誤 | 不中斷整體 payload，除非主體主檔不存在；回傳 module warning |

## 8. Version / Date Selector Treatment

| Selector | Applies to | Rule |
| --- | --- | --- |
| `effectiveDate` | BOM / Recipe / Routing | 作為版本狀態與 current version 判斷基準。 |
| `inventoryDate` | Warehouse / Inventory | 作為庫存快照計算基準。未提供時同 `effectiveDate`。 |
| `productVersion` | Product Structure / Recipe | Product 主體可指定；未指定時依各模組既有 current/highest-version 規則處理並回報 warning/source。 |

若同一查詢涉及不同日期語意，BFF 必須在 `requestIdentity` 回傳實際採用值，避免畫面與資料解讀不一致。

## 9. Error Behavior

| Scenario | Expected behavior |
| --- | --- |
| `itemCategory` 不是 4 或 5 | 回傳 validation error |
| `item_no` 空值 | 回傳 validation error |
| Product/WIP 主檔不存在 | 回傳 record not found，payload 可為空 |
| 子模組查無資料 | 整體回傳 200，對應 moduleReadiness 為 unavailable 或 partial |
| 子模組查詢錯誤 | 整體可回傳 200 with module error warning；若錯誤導致主體不可確認，回傳 failed response |
| `includeModules` 包含未定義模組 | 回傳 validation error |

## 10. Read-Only Boundary

本 API candidate 僅允許 GET。

不得執行：

1. Product / WIP 主檔新增、修改、停用、版本晉升。
2. BOM / Recipe / Routing 新增、修改、核准、發行或凍結。
3. Workflow task 建立、狀態轉換、部門指派。
4. Inventory reservation、quality hold、pallet movement 或 batch mutation。
5. 資料庫 DDL / DML、Production data load、migration、Source-of-Truth transition、Cutover、Go-Live。

## 11. Product Scenario

Example request:

```txt
GET /api/v2/product-overview/items/PRD-SD-001/overview?itemCategory=5&effectiveDate=1700000000&inventoryDate=1700000000
```

Expected Product behavior:

1. `subject` 由 `product` / Item Center 取得。
2. `transactionContext` 以 `trans_items.item_no = PRD-SD-001` 取得交易品項與合約摘要。
3. `inventoryOverview` 以 Warehouse inventory summary 取得目前庫存、價值、可用量與風險。
4. `productStructure` 呼叫 Product Structure contract 取得產品結構。
5. `recipeFormula` 以 by-product contract 取得 Recipe / Formula evidence。
6. `routingProcess` 以 Product/WIP routing current contract 取得 ordered process steps。
7. 若 Routing 使用 Shared DEV test-support fallback，必須於 moduleReadiness 與 warnings 標示。

## 12. Standalone WIP Scenario

Example request:

```txt
GET /api/v2/product-overview/items/INP-SD-001/overview?itemCategory=4&effectiveDate=1700000000&inventoryDate=1700000000
```

Expected WIP behavior:

1. `subject` 由 `inproduct` / Item Center 取得。
2. `transactionContext` 通常可能為 missing 或 unavailable，除非存在 `trans_items.item_no = INP-SD-001`。
3. `inventoryOverview` 可依 Warehouse inventory summary 回傳 WIP 庫存與批號。
4. `routingProcess` 可依 `product_process.item_no = INP-SD-001` 回傳 WIP routing；若 Shared DEV 尚無 standalone WIP route，回傳 unavailable 或 test-support warning。
5. `productStructure` 若沒有正式 WIP root product-structure contract，回傳 partial / unavailable，不反向推測成品結構。
6. `recipeFormula` 若沒有 WIP root output contract，回傳 partial / unavailable；不可用下游 Product 的 recipe 代替 WIP 權威 recipe。

## 13. Material Schema Or Authority Gap

目前不建議為本 refinement 直接新增 schema。

需工程師 review 的 gap：

| Gap | Impact | Suggested next action |
| --- | --- | --- |
| WIP root Product Structure / Recipe contract 尚未完全等同 Product root | WIP 360 可能只能呈現主檔、庫存與 routing，BOM / Recipe 需 partial | 在 API design review 中確認 WIP root 是否需要獨立 contract 或 acceptance fixture |
| Transaction item 與 internal item version 的關聯不足 | 客戶專屬規格、版本或包裝差異可能無法只用 `trans_items.item_no` 表達 | CP1 V1 先只回傳 linked transaction items；版本治理留待後續 authority review |
| Routing Shared DEV test-support 目前 Product evidence 較完整，standalone WIP evidence 不足 | WIP routing acceptance 可能無法完整驗證 | 請 Engineering B 提供 standalone WIP routing support rows |

## 14. Recommended Implementation Envelope

若後續另行授權 implementation，建議 envelope：

1. 新增 `restserver/package/restserver/api/v2/product_overview.py` 與對應 uri 檔，遵循既有 v2 API style。
2. 服務層以 composition/orchestration 為主，優先重用 Item、Warehouse inventory summary、BOM、Recipe、Routing 既有 service，不複製核心演算法。
3. 每個 module call 需回傳或轉換為 `{statusCode, sourceCode, warningCodes, data}` 內部結構。
4. pytest 需覆蓋 Product complete、Product partial、WIP partial、invalid category、not found、test-support routing、module unavailable。
5. 實作完成後再更新正式 API 文件 `docs/spec/api/`，並產生測試報告於 `docs/report/`。

Disposition:

```txt
READY FOR ENGINEER REVIEW AS API PROPOSAL REFINEMENT
NOT READY FOR RUNTIME IMPLEMENTATION WITHOUT SEPARATE AUTHORIZATION
```
