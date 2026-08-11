# RDCostWorkspaceScreen API 提案

> Status: Proposal / Pending Engineer Review  
> Screen: `RDCostWorkspaceScreen`  
> Route: `/rd`  
> Scope: V1 read-only Core  
> Design basis: `AGENTS.md`、`src/app/rd/page.tsx`、`src/types/rd.ts`、`docs/spec/database/index.md`、`bom_center_proposal.md`

## 1. 畫面定位

「研發成本」是獨立於「BOM 中心」的成本試算與報價基礎工作區。BOM Center 負責配方版本與直接明細；研發成本負責把產品、BOM、料品成本、人工/製造費用、報價與合約準備度整理成管理者可檢視的 read-only 畫面。

目前資料庫文件尚未確認「開發需求、打樣、送樣、客戶選樣、營養標示」的正式資料表，因此本版 API 不推測這些流程狀態，也不以備註文字生成開發案。第一版以既有正式資料表能支援的產品/BOM/成本/報價/合約資料為主。

## 2. V1 API 清單

| API | Method | 用途 |
|---|---|---|
| `/api/v2/rd/cost/dashboard` | GET | 研發成本總覽、產品/BOM/成本/報價準備度清單 |
| `/api/v2/rd/cost/products/{product_no}/detail` | GET | 指定產品版本的 BOM、成本明細、報價與合約關聯 |
| `/api/v2/rd/cost/products/{product_no}/simulation` | GET | 指定產品版本的成本試算明細與建議報價基礎 |

以上 API 均為 read-only。`simulation` 只回傳計算結果，不寫入成本、不建立報價、不代表研發主管或業務核准。

## 3. 共用 Query Parameters / Header

| Parameter / Header | Type | Required | Description |
|---|---|---:|---|
| `date` | Integer | No | 查詢基準 UTC timestamp；未提供時使用系統時間。 |
| `productNo` | String | No | 製成品 `product.no`；dashboard 可作篩選。 |
| `productVersion` | Integer | No | 產品版本；未提供時使用該產品目前可判定的最高版本。 |
| `bomNo` | String | No | 商品配方 no；dashboard 可作篩選。 |
| `readinessStatusCode` | String | No | 資料準備度狀態 code；前端提供 enum code，不傳顯示文字。 |
| `costStatusCode` | String | No | 成本資料狀態 code；前端提供 enum code，不傳顯示文字。 |
| `keyword` | String | No | 產品 no、產品名稱、BOM no、BOM 名稱或成本明細料品 no/名稱。 |
| `start` | Integer | No | 分頁起點，預設 0。 |
| `count` | Integer | No | 回傳筆數，預設 50，最大 100。 |
| `x-timezone` | Header String | No | 前端顯示偏好的 IANA timezone；後端仍回傳 UTC timestamp。 |

## 4. GET `/api/v2/rd/cost/dashboard`

### 4.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "summary": {
    "productCount": "Integer",
    "bomReadyCount": "Integer",
    "costReadyCount": "Integer",
    "quotationReadyCount": "Integer",
    "marginAttentionCount": "Integer"
  },
  "items": [
    {
      "productNo": "String",
      "productName": "String",
      "productVersion": "Integer",
      "productCategory": "Integer",
      "bomNo": "String",
      "bomVersion": "Integer",
      "bomStatusCode": "String",
      "costStatusCode": "String",
      "readinessStatusCode": "String",
      "readinessRiskCode": "String",
      "estimatedUnitCost": "Integer",
      "materialCost": "Integer",
      "packagingCost": "Integer",
      "laborCost": "Integer",
      "overheadCost": "Integer",
      "logisticsCost": "Integer",
      "lossRate": "Float",
      "targetPrice": "Float",
      "minimumQuote": "Float",
      "suggestedQuote": "Float",
      "targetMarginRate": "Float",
      "estimatedMarginRate": "Float",
      "quotationCount": "Integer",
      "contractCount": "Integer"
    }
  ],
  "total": "Integer",
  "start": "Integer",
  "count": "Integer"
}
```

### 4.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `serverTimestamp` | Integer | API 回應建立時間，UTC timestamp。 | 系統時間 |
| `summary.productCount` | Integer | 套用篩選條件後的不重複產品數。 | `product.no` |
| `summary.bomReadyCount` | Integer | BOM 資料狀態為完整的產品版本數。 | `bomStatusCode=complete` |
| `summary.costReadyCount` | Integer | 成本資料狀態為可計算的產品版本數。 | `costStatusCode=complete` |
| `summary.quotationReadyCount` | Integer | 已有可關聯報價或合約資料的產品版本數。 | `quotation`、`contract` |
| `summary.marginAttentionCount` | Integer | 預估毛利低於目標或成本來源缺漏的產品版本數。 | `estimatedMarginRate`、`targetMarginRate`、`readinessRiskCode` |
| `items[].productNo` | String | 製成品 no。 | `product.no` |
| `items[].productName` | String | 製成品名稱；無值時回傳空字串。 | `product.name` |
| `items[].productVersion` | Integer | 產品版本。 | `product.version` 或 `product_spec.product_version` |
| `items[].productCategory` | Integer | 製成品類別 code；前端負責多國語系顯示。 | `product.category` |
| `items[].bomNo` | String | 產品版本關聯的商品配方 no；無正式關聯時回傳空字串。 | `product_spec.bom_no` |
| `items[].bomVersion` | Integer | 產品版本關聯的商品配方版本；無正式關聯時回傳 0。 | `product_spec.bom_version` |
| `items[].bomStatusCode` | String | BOM 資料狀態 code。 | `complete`、`partial`、`missing`、`unknown` |
| `items[].costStatusCode` | String | 成本資料狀態 code。 | `complete`、`missing_source`、`unknown` |
| `items[].readinessStatusCode` | String | 研發成本畫面所需資料準備度 code。 | `ready`、`incomplete`、`unknown` |
| `items[].readinessRiskCode` | String | 主要資料缺口或毛利風險 code。 | `normal`、`bom_missing`、`cost_missing`、`quotation_missing`、`contract_missing`、`margin_low`、`unknown` |
| `items[].estimatedUnitCost` | Integer | 單品預估成本，四捨五入取整數；必要來源不足時回傳 0 並以狀態欄位表示缺漏。 | 成本試算 |
| `items[].materialCost` | Integer | 原料成本加總，四捨五入取整數。 | `bom_item`、`sample_price`、`item_price` |
| `items[].packagingCost` | Integer | 物料、包材與膠捲成本加總，四捨五入取整數。 | `product_bom_spec`、`item_price` |
| `items[].laborCost` | Integer | 人工成本加總，四捨五入取整數；若正式來源不足則回傳 0 並標示缺漏。 | `labor_wage` 或工程師確認來源 |
| `items[].overheadCost` | Integer | 製造費用加總，四捨五入取整數；若正式來源不足則回傳 0 並標示缺漏。 | 待工程師確認 |
| `items[].logisticsCost` | Integer | 物流或倉儲估算成本，四捨五入取整數；若正式來源不足則回傳 0 並標示缺漏。 | `ship_wh_quotation`、`ship_wh_contract` 或工程師確認來源 |
| `items[].lossRate` | Float | 產品/BOM 預估損耗率，取至小數點第 2 位。 | `product_spec.expectedLoss`、BOM 明細 |
| `items[].targetPrice` | Float | 目標售價或客戶目標價，取至小數點第 4 位；無正式來源時回傳 0。 | `quotation` 或工程師確認來源 |
| `items[].minimumQuote` | Float | 依成本與目標毛利計算的最低報價，取至小數點第 4 位。 | 成本試算 |
| `items[].suggestedQuote` | Float | 建議報價，取至小數點第 4 位；計算規則待工程師確認。 | 成本試算 |
| `items[].targetMarginRate` | Float | 目標毛利率，取至小數點第 2 位；無正式來源時回傳 0。 | 工程師確認來源 |
| `items[].estimatedMarginRate` | Float | 預估毛利率，取至小數點第 2 位。 | `(suggestedQuote - estimatedUnitCost) / suggestedQuote` |
| `items[].quotationCount` | Integer | 可由正式關聯取得的報價資料筆數。 | `quotation` |
| `items[].contractCount` | Integer | 可由正式關聯取得的合約資料筆數。 | `contract` |
| `total` | Integer | 套用篩選後的產品版本總筆數。 | 查詢結果 |
| `start` | Integer | 本次分頁起點。 | Query parameter |
| `count` | Integer | 本次實際回傳筆數。 | Query parameter / 實際筆數 |

## 5. GET `/api/v2/rd/cost/products/{product_no}/detail`

### 5.1 Success Response Data

```json
{
  "product": {
    "productNo": "String",
    "productName": "String",
    "productVersion": "Integer",
    "productCategory": "Integer",
    "unitProduct": "Integer",
    "comment": "String"
  },
  "bom": {
    "bomNo": "String",
    "bomVersion": "Integer",
    "bomName": "String",
    "dateTimestamp": "Integer",
    "unit": "Integer",
    "weight": "Float",
    "bomStatusCode": "String"
  },
  "costLines": [
    {
      "lineTypeCode": "String",
      "itemCategory": "Integer",
      "itemNo": "String",
      "itemName": "String",
      "sourceBomNo": "String",
      "sourceBomVersion": "Integer",
      "requiredQuantity": "Float",
      "unit": "Integer",
      "weight": "Float",
      "lossRate": "Float",
      "unitCost": "Float",
      "costAmount": "Integer",
      "costSourceCode": "String"
    }
  ],
  "costSummary": {
    "materialCost": "Integer",
    "packagingCost": "Integer",
    "laborCost": "Integer",
    "overheadCost": "Integer",
    "logisticsCost": "Integer",
    "estimatedUnitCost": "Integer",
    "costStatusCode": "String"
  },
  "commercialReference": {
    "targetPrice": "Float",
    "minimumQuote": "Float",
    "suggestedQuote": "Float",
    "targetMarginRate": "Float",
    "estimatedMarginRate": "Float",
    "quotationCount": "Integer",
    "contractCount": "Integer"
  },
  "readiness": {
    "statusCode": "String",
    "riskCode": "String",
    "missingFieldCodes": ["String"]
  }
}
```

### 5.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `product.productNo` | String | 製成品 no。 | `product.no` |
| `product.productName` | String | 製成品名稱；無值時回傳空字串。 | `product.name` |
| `product.productVersion` | Integer | 本次查詢使用的產品版本。 | `product.version` 或 `product_spec.product_version` |
| `product.productCategory` | Integer | 製成品類別 code。 | `product.category` |
| `product.unitProduct` | Integer | 產品產製單位 code。 | `product.unitProduct` |
| `product.comment` | String | 產品主檔備註；無值時回傳空字串。 | `product.comment` |
| `bom.bomNo` | String | 商品配方 no；無正式關聯時回傳空字串。 | `product_spec.bom_no` |
| `bom.bomVersion` | Integer | 商品配方版本；無正式關聯時回傳 0。 | `product_spec.bom_version` |
| `bom.bomName` | String | 商品配方名稱；無值時回傳空字串。 | `bom.displayName` |
| `bom.dateTimestamp` | Integer | 商品配方生效時間，UTC timestamp；空值時回傳 0。 | `bom.date` |
| `bom.unit` | Integer | 商品配方單位 code。 | `bom.unit` |
| `bom.weight` | Float | 商品配方基準重量，取至小數點第 2 位。 | `bom.weight` |
| `bom.bomStatusCode` | String | BOM 資料狀態 code。 | `complete`、`partial`、`missing`、`unknown` |
| `costLines[].lineTypeCode` | String | 成本明細類型 code；前端負責顯示文字。 | `material`、`packaging`、`labor`、`overhead`、`logistics` |
| `costLines[].itemCategory` | Integer | 料品品項類別 code。 | Item category enum |
| `costLines[].itemNo` | String | 成本明細料品 no；人工/製造費用等無料品時回傳空字串。 | BOM / 成本來源 |
| `costLines[].itemName` | String | 成本明細名稱；無值時回傳空字串。 | BOM / 成本來源 |
| `costLines[].sourceBomNo` | String | 成本明細來源 BOM no；無法追溯時回傳空字串。 | BOM relation |
| `costLines[].sourceBomVersion` | Integer | 成本明細來源 BOM 版本；無法追溯時回傳 0。 | BOM relation |
| `costLines[].requiredQuantity` | Float | 該成本明細需求數量，取至小數點第 2 位。 | BOM 展開或成本來源 |
| `costLines[].unit` | Integer | 成本明細單位 code。 | Unit enum |
| `costLines[].weight` | Float | 該成本明細重量，取至小數點第 2 位。 | BOM 展開或成本來源 |
| `costLines[].lossRate` | Float | 預估損耗率，取至小數點第 2 位。 | `expectedLoss` 或工程師確認來源 |
| `costLines[].unitCost` | Float | 成本單價，取至小數點第 4 位。 | `sample_price`、`item_price` 或工程師確認來源 |
| `costLines[].costAmount` | Integer | 明細成本金額，四捨五入取整數。 | `requiredQuantity * unitCost` 與損耗計算 |
| `costLines[].costSourceCode` | String | 成本來源 code。 | `sample_price`、`item_price`、`labor_wage`、`manual_source_missing`、`unknown` |
| `costSummary.materialCost` | Integer | 原料成本加總。 | `costLines.lineTypeCode=material` |
| `costSummary.packagingCost` | Integer | 物料、包材與膠捲成本加總。 | `costLines.lineTypeCode=packaging` |
| `costSummary.laborCost` | Integer | 人工成本加總。 | `costLines.lineTypeCode=labor` |
| `costSummary.overheadCost` | Integer | 製造費用加總。 | `costLines.lineTypeCode=overhead` |
| `costSummary.logisticsCost` | Integer | 物流/倉儲成本加總。 | `costLines.lineTypeCode=logistics` |
| `costSummary.estimatedUnitCost` | Integer | 單品預估成本。 | cost summary total |
| `costSummary.costStatusCode` | String | 成本資料狀態 code。 | `complete`、`missing_source`、`unknown` |
| `commercialReference.targetPrice` | Float | 目標售價或客戶目標價，取至小數點第 4 位。 | `quotation` 或工程師確認來源 |
| `commercialReference.minimumQuote` | Float | 依成本與目標毛利計算的最低報價，取至小數點第 4 位。 | 成本試算 |
| `commercialReference.suggestedQuote` | Float | 建議報價，取至小數點第 4 位。 | 成本試算 |
| `commercialReference.targetMarginRate` | Float | 目標毛利率，取至小數點第 2 位。 | 工程師確認來源 |
| `commercialReference.estimatedMarginRate` | Float | 預估毛利率，取至小數點第 2 位。 | 成本與建議報價計算 |
| `commercialReference.quotationCount` | Integer | 可關聯報價資料筆數。 | `quotation` |
| `commercialReference.contractCount` | Integer | 可關聯合約資料筆數。 | `contract` |
| `readiness.statusCode` | String | 研發成本資料準備度 code。 | `ready`、`incomplete`、`unknown` |
| `readiness.riskCode` | String | 主要資料缺口或毛利風險 code。 | `normal`、`bom_missing`、`cost_missing`、`quotation_missing`、`contract_missing`、`margin_low`、`unknown` |
| `readiness.missingFieldCodes` | Array<String> | 尚缺少的資料欄位 code；無缺漏時回傳空陣列。 | `bom`、`cost`、`quotation`、`contract`、`margin_rule` |

## 6. GET `/api/v2/rd/cost/products/{product_no}/simulation`

`simulation` 與 detail 的成本結構相同，但只回傳 `costLines`、`costSummary`、`commercialReference` 與 `readiness`，供前端在成本試算視圖中重新查詢單一產品版本。此 API 不回傳開發案 workflow，也不寫入成本資料。

## 7. V1 不包含的功能

- 新增、修改、核准或作廢產品、BOM、成本、報價與合約。
- 以不存在的 DB schema 推導開發需求、打樣、送樣、客戶確認樣品或營養標示。
- 將 enum code 轉換成繁中字串；前端負責多國語系顯示。
- 判斷報價或合約是否已核准、是否仍有效；除非工程師確認正式欄位與規則。
- 將 `CCBOMTree` 完整樹狀展開直接塞進本 API；若需要完整 BOM 樹，需另設計產品 BOM tree API。

## 8. Database Tables Used

| Table | Purpose |
|---|---|
| `product` | 取得製成品主檔、名稱、類別與單位。 |
| `product_spec` | 取得產品版本與商品配方關聯、產品規格數量、單位、重量與損耗。 |
| `bom` | 取得商品配方版本、生效日期、單位與基準重量。 |
| `bom_item` | 取得商品配方直接原料明細。 |
| `product_bom_spec` | 取得製成品包裝/物料 BOM 關聯，是否納入 V1 成本需工程師確認。 |
| `item_price` | 取得料品正式成本單價。 |
| `sample_price` | 取得商品配方樣品或估算成本單價。 |
| `quotation` | 取得報價基礎資料；有效性與類別規則待工程師確認。 |
| `contract` | 取得合約基礎資料；有效性與類別規則待工程師確認。 |
| `labor_wage` | 候選人工成本來源；使用規則待工程師確認。 |
| `ship_wh_quotation` / `ship_wh_contract` | 候選物流/倉儲成本來源；是否納入 V1 待工程師確認。 |

## 9. Engineer Review Gate

後端實作前請工程師確認：

1. API 路徑是否採用 `/api/v2/rd/cost/...`。
2. 第一版 row identity 是否以 `productNo + productVersion` 為準，直到開發案/打樣流程資料表確認。
3. 原料成本來源優先順序：`sample_price`、`item_price` 或其他正式成本表。
4. 物料/包材/膠捲成本是否在本版納入，若納入，是否以 `product_bom_spec + item_price` 為來源。
5. 人工、製造費用、物流成本是否先回傳 0 並標示 `missing_source`，或已有可正式計算的資料表與規則。
6. `minimumQuote`、`suggestedQuote`、`targetMarginRate` 的正式計算規則與來源。
