# Product / WIP 360 Read-Only Overview Flow / Algorithm Proposal

狀態：Proposal Refinement / Pending Engineer Review
對應 API 提案：`docs/spec/api-proposal/product_wip_360_overview_proposal.md`
對應靜態預覽：`docs/spec/api-proposal/product_wip_360_overview_static_preview.html`
目的：說明 `GET /api/v2/product-overview/items/{item_no}/overview` bounded read-only BFF / composition API 的後端流程、模組組合、資料缺漏處理與 read-only 邊界。

## 文件定位

本文件是流程與演算法提案，不代表目前 `restserver/` 已實作。

必須保留：

```txt
API_PROPOSAL_REFINEMENT != API_IMPLEMENTATION
BFF_CONTRACT != NEW_SOURCE_OF_TRUTH
```

## Step 1：解析 Request Identity

輸入：

```txt
item_no
itemCategory
effectiveDate
inventoryDate
productVersion
includeModules
x-timezone
```

規則：

1. `item_no` 不可為空。
2. `itemCategory` 必須為 `EItemCategory.INPRODUCT = 4` 或 `EItemCategory.PRODUCT = 5`。
3. `effectiveDate` 未提供時使用目前 UTC timestamp。
4. `inventoryDate` 未提供時採用 `effectiveDate`。
5. `includeModules` 未提供時使用 `item,transactionItem,warehouse,bom,recipe,routing`。
6. `includeModules` 若包含未定義模組，回傳 validation error。

## Step 2：確認 Product / WIP 主體

主體來源：

| itemCategory | Table | Source code |
| --- | --- | --- |
| 4 | `inproduct` | `inproduct` |
| 5 | `product` | `product` |

處理：

1. 先依 `itemCategory` 查詢對應主檔，不跨表猜測。
2. 主檔不存在時回傳 record not found。
3. 建立 canonical identity：

```txt
subjectKey = itemCategory + ":" + itemNo
```

4. 將主體資料填入 `payload.subject` 與 `payload.requestIdentity`。

## Step 3：建立 Module Execution Plan

依 `includeModules` 建立 module plan：

| Module | Product | WIP | Notes |
| --- | --- | --- | --- |
| item | YES | YES | 主檔與 item detail summary。 |
| transactionItem | YES | CONDITIONAL | WIP 若無交易品項關聯，回傳 missing/unavailable。 |
| warehouse | YES | YES | 以 `itemNo + itemCategory + inventoryDate` 查詢庫存。 |
| bom | YES | PARTIAL | Product 使用 product-structure；WIP root contract 需 review。 |
| recipe | YES | PARTIAL | Product 使用 by-product；WIP root output contract 需 review。 |
| routing | YES | YES | 以 `itemNo + effectiveDate` 查詢 current routing。 |

每個 module 執行結果轉換成內部結構：

```txt
moduleResult = {
  moduleCode,
  statusCode,
  sourceCode,
  warningCodes,
  data
}
```

## Step 4：Item Module

建議重用：

```txt
CItemCenterService.get_detail(itemNo, date=inventoryDate)
```

輸出：

1. `payload.subject` 的單位、主檔狀態與維護風險。
2. `payload.inventoryOverview` 的輕量摘要可先參考 item detail 的 inventory summary，但最終以 Warehouse module 的庫存計算為準。
3. 若 Item detail 與 subject master 不一致，回傳 `item_identity_mismatch` warning。

## Step 5：Transaction Item Module

建議資料來源：

```txt
trans_items.item_no = itemNo
```

處理：

1. 查詢符合 internal itemNo 的 transaction items。
2. Product 可回傳 linked transaction items。
3. WIP 若沒有 transaction items，狀態為 `unavailable` 或 `partial`，不視為錯誤。
4. 不用交易品項反推 Product/WIP 主體。

輸出：

```txt
payload.transactionContext
```

## Step 6：Warehouse Module

建議重用既有 Warehouse 庫存快照共用邏輯。

查詢條件：

```txt
date = inventoryDate
itemCategory = request.itemCategory
item_no = request.item_no
```

處理：

1. 以已確認的庫存快照邏輯計算目前庫存量與庫存價值。
2. 沿用現有 Warehouse API 的已確認零庫存過濾規則：過濾 `currentQuantity == 0`；`currentQuantity < 0` 視為資料異常訊號保留，以利開發與 runtime review 追查。
3. 彙總 `currentQuantity`、`availableQuantity`、`reservedQuantity`、`qualityHoldQuantity`、`inventoryValue`、`availableValue`、`warehouseCount`、`batchCount`。
4. 挑選 `batchHighlights[]`，排序建議為風險高、效期近、可用量大、最新異動。

輸出：

```txt
payload.inventoryOverview
payload.batchHighlights
```

## Step 7：BOM / Product Structure Module

Product 主體：

```txt
GET /api/v2/bom/product-structure/{product_no}
```

WIP 主體：

1. 若後續確認支援 WIP root，依確認 contract 查詢。
2. 若尚未確認，不可由下游 Product 反向推測 WIP structure。
3. 回傳 `statusCode=partial` 或 `unavailable`，並加入 `wip_product_structure_not_governed` warning。

輸出：

```txt
payload.productStructure
```

## Step 8：Recipe / Formula Module

Product 主體：

```txt
GET /api/v2/recipe-formula/by-product/{product_no}
```

WIP 主體：

1. 若後續確認 WIP 可作為 recipe output root，依確認 contract 查詢。
2. 若尚未確認，不可用下游 Product recipe 取代 WIP recipe。
3. 回傳 `statusCode=partial` 或 `unavailable`，並加入 `wip_recipe_formula_not_governed` warning。

輸出：

```txt
payload.recipeFormula
```

## Step 9：Routing / Process Flow Module

Product / WIP 均建議使用：

```txt
GET /api/v2/routing/products/{item_no}/current
```

處理：

1. 傳入 `effectiveDate`。
2. 保留 Routing response 的 `sourceLineage`、`warnings[]`、`capabilityBoundary`。
3. 若為 Shared DEV test-support fallback，module status 應標示為 `test_support`，不可標示為 formal complete。

輸出：

```txt
payload.routingProcess
```

## Step 10：組合 Module Readiness

依每個 module 結果建立：

```txt
payload.moduleReadiness[]
payload.sourceLineage
payload.warnings[]
```

狀態判斷：

| statusCode | 判斷條件 |
| --- | --- |
| complete | 以正式來源取得目前畫面所需資料，且無阻塞 warning |
| partial | 取得部分資料，但存在缺漏、未治理或非阻塞 warning |
| unavailable | 主體不支援該模組或查無必要資料 |
| test_support | 資料來自 Shared DEV test-support readonly surface |
| error | 子模組查詢發生錯誤，但主體仍可確認 |

## Step 11：錯誤處理

1. 主體主檔不存在：直接回傳 not found。
2. 子模組不存在資料：不中斷整體 response，以 `moduleReadiness` 與 warning 表示。
3. 子模組 runtime error：不中斷整體 response，除非造成主體不可確認。
4. 不回傳繁中文字串 fallback；所有顯示文字由前端依 enum / code 轉換。

## Step 12：效能與實作建議

若後續授權實作：

1. 不建議由 BFF 對 HTTP endpoint 再發 HTTP request；應在同一 Flask app 內重用 service 或共用 calculator，避免序列化與網路成本。
2. Warehouse 庫存摘要必須重用現有 snapshot calculator，避免再寫一套月結/delta/inventory_record 補算。
3. Transaction Item、BOM、Recipe、Routing 查詢需以 `itemNo` 或 version key 限定，不可全表載入後篩選。
4. module execution 可先順序執行，待實測後再評估是否需要平行化或快取。
5. Response 只包含 Product/WIP 360 第一版畫面所需欄位，不預留 mutation 或未使用欄位。

## Step 13：Read-Only Boundary Check

實作前後均需確認：

1. 只新增 GET route。
2. 不新增 POST / PUT / DELETE。
3. 不新增 DDL / DML。
4. 不建立 workflow task 或變更任何狀態。
5. 不把 BFF payload 視為新的 Source of Truth。

## Step 14：建議測試案例

若後續另行授權實作，pytest 至少包含：

| Case | Expected result |
| --- | --- |
| Product complete | 回傳 subject、inventory、productStructure、recipeFormula、routingProcess |
| Product partial missing transaction item | transactionContext 標示 missing，不中斷整體 response |
| Product routing test-support | routing module 標示 test_support 並保留 warning |
| WIP partial | subject、inventory、routing 可用；BOM/Recipe 若未治理則 partial/unavailable |
| Invalid itemCategory | validation error |
| Subject not found | record not found |
| Module error isolation | 單一 module error 不造成整體主體查詢失敗 |

## Disposition

```txt
READY FOR ENGINEER REVIEW AS FLOW / ALGORITHM PROPOSAL
NO RUNTIME IMPLEMENTATION AUTHORIZED
```
