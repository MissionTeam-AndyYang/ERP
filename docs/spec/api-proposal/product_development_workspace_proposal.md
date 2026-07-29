# ProductDevelopmentWorkspaceScreen API 提案

> Status: Proposal / Pending Engineer Review
> Screen: `ProductDevelopmentWorkspaceScreen`
> Route: `/product-development`
> Scope: V1 read-only Core
> Design basis: `AGENTS.md`、`docs/spec/database/index.md`、既有 product/BOM/quotation/contract schema

## 1. 畫面定位

產品研發工作區位於「研發選材、配方/BOM、成本試算、業務報價」流程的中心，提供管理者、研發主管與採購主管檢視產品版本是否具備可生產與可報價的資料基礎。

第一版只提供查詢、篩選、版本切換、BOM 展開、成本摘要與正式報價/合約關聯，不執行新增或修改產品、BOM、配方、報價及合約。

## 2. V1 API 清單

| API | Method | 用途 |
|---|---|---|
| `/api/v2/product-development/dashboard` | GET | 產品版本、BOM 完整性、成本與報價準備度總覽 |
| `/api/v2/product-development/products/{product_no}/detail` | GET | 單一產品版本、BOM 展開、成本與正式商務關聯明細 |
| `/api/v2/product-development/products/{product_no}/cost-simulation` | GET | 依指定產品版本回傳成本試算所需的明細與計算結果 |

以上 API 均為 read-only。`cost-simulation` 是查詢/計算 API，不寫入成本結果，也不代表已核准報價。

## 3. 共用 Query Parameters / Header

| Parameter / Header | Type | Required | Description |
|---|---|---:|---|
| `productNo` | String | No | 製成品 `product.no`；dashboard 可作篩選。 |
| `productVersion` | Integer | No | `product.version`；未提供時使用目前產品主檔版本。 |
| `itemCategory` | Integer | No | 料品品項類別 code；由前端轉換多國語系。 |
| `keyword` | String | No | 產品 no、產品名稱、BOM no、BOM 名稱或料品 no/名稱。 |
| `start` | Integer | No | 分頁起點，預設 0。 |
| `count` | Integer | No | 回傳筆數，預設 50，最大 100。 |
| `x-timezone` | Header String | Yes | IANA timezone；日期 timestamp 顯示與成本生效日解讀使用。 |

## 4. GET `/api/v2/product-development/dashboard`

### 4.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "timezone": "String",
  "summary": {
    "productCount": "Integer",
    "versionCount": "Integer",
    "bomMissingCount": "Integer",
    "costMissingCount": "Integer",
    "quotationMissingCount": "Integer",
    "contractMissingCount": "Integer"
  },
  "items": [
    {
      "productNo": "String",
      "productName": "String",
      "productCategory": "Integer",
      "productVersion": "Integer",
      "productUnit": "Integer",
      "bomNo": "String",
      "bomVersion": "Integer",
      "bomItemCount": "Integer",
      "bomStatusCode": "String",
      "estimatedCost": "Integer",
      "costPrice": "Float",
      "quotationCount": "Integer",
      "contractCount": "Integer",
      "readinessStatusCode": "String",
      "readinessRiskCode": "String"
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
| `serverTimestamp` | Integer | 回應建立時間，UTC timestamp。 |  |
| `timezone` | String | 本次回應使用的 IANA timezone。 | `x-timezone` |
| `summary.productCount` | Integer | 符合篩選條件的產品數。 | `product` |
| `summary.versionCount` | Integer | 符合篩選條件的產品版本資料數。 | `product.version` |
| `summary.bomMissingCount` | Integer | 找不到正式 BOM 版本的產品版本數。 | `product_spec.bom_no`、`bom` |
| `summary.costMissingCount` | Integer | 無法取得成本價格資料的產品版本數。 | `item_price`、BOM 明細 |
| `summary.quotationMissingCount` | Integer | 找不到採購或訂購報價資料的產品數。 | `quotation` |
| `summary.contractMissingCount` | Integer | 找不到正式合約資料的產品數。 | `contract` |
| `items[]` | Array | 產品版本摘要資料列，依產品 no、版本穩定排序；此節點不另列說明。 |  |
| `items[].productNo` | String | 製成品 no。 | `product.no` |
| `items[].productName` | String | 製成品名稱。 | `product.name` |
| `items[].productCategory` | Integer | 製成品類別 code。 | `product.category` |
| `items[].productVersion` | Integer | 製成品版本。 | `product.version` |
| `items[].productUnit` | Integer | 製成品產製單位 code。 | `product.unitProduct` |
| `items[].bomNo` | String | 產品版本關聯的商品配方 no；無正式關聯時為空字串。 | `product_spec.bom_no`、`bom.no` |
| `items[].bomVersion` | Integer | 商品配方版本；無正式關聯時為 0。 | `product_spec.bom_version`、`bom.version` |
| `items[].bomItemCount` | Integer | 該產品版本正式 BOM 明細筆數。 | `product_spec`、`product_bom_spec` |
| `items[].bomStatusCode` | String | BOM 狀態 code。 | `complete`、`partial`、`missing`、`unknown` |
| `items[].estimatedCost` | Integer | 產品版本成本試算總額，四捨五入取整數；無法計算時為 0。 | `item_price`、BOM 明細計算 |
| `items[].costPrice` | Float | 單位成本價格，取至小數點第 4 位；無法取得時為 0。 | `item_price.costPriceWeight` 或正式成本欄位 |
| `items[].quotationCount` | Integer | 可由正式品項關聯取得的報價資料筆數。 | `quotation.item_no` |
| `items[].contractCount` | Integer | 可由正式品項關聯取得的合約資料筆數。 | `contract.item_no` |
| `items[].readinessStatusCode` | String | 產品版本是否具備目前畫面所需資料的 code。 | `ready`、`incomplete`、`unknown` |
| `items[].readinessRiskCode` | String | 主要資料缺口 code。 | `bom_missing`、`cost_missing`、`quotation_missing`、`contract_missing`、`unknown` |
| `total` | Integer | 套用篩選後的產品版本總筆數。 |  |
| `start` | Integer | 本次分頁起點。 |  |
| `count` | Integer | 本次回傳筆數。 |  |

## 5. GET `/api/v2/product-development/products/{product_no}/detail`

### 5.1 Success Response Data

```json
{
  "product": {
    "productNo": "String",
    "productName": "String",
    "productCategory": "Integer",
    "productVersion": "Integer",
    "unitShipping": "Integer",
    "unitWarehouse": "Integer",
    "unitProduct": "Integer",
    "comment": "String"
  },
  "bom": {
    "bomNo": "String",
    "bomName": "String",
    "bomVersion": "Integer",
    "dateTimestamp": "Integer",
    "unit": "Integer",
    "weight": "Float",
    "comment": "String"
  },
  "bomItems": [
    {
      "level": "Integer",
      "itemNo": "String",
      "itemName": "String",
      "itemType": "Integer",
      "requiredCount": "Float",
      "unit": "Integer",
      "weight": "Float",
      "expectedLoss": "Float",
      "actualLoss": "Float",
      "sourceBomNo": "String",
      "sourceBomVersion": "Integer"
    }
  ],
  "costSummary": {
    "materialCost": "Integer",
    "laborCost": "Integer",
    "estimatedCost": "Integer",
    "costStatusCode": "String"
  },
  "quotations": [
    {
      "quotationNo": "String",
      "dateTimestamp": "Integer",
      "category": "Integer",
      "itemStyle": "Integer",
      "itemNo": "String",
      "itemName": "String",
      "supplierNo": "String",
      "supplierName": "String",
      "unit": "Integer",
      "unitPrice": "Float"
    }
  ],
  "contracts": [
    {
      "contractNo": "String",
      "refNo": "String",
      "dateTimestamp": "Integer",
      "category": "Integer",
      "itemStyle": "Integer",
      "itemNo": "String",
      "itemName": "String",
      "supplierNo": "String",
      "supplierName": "String",
      "unit": "Integer",
      "unitPrice": "Float"
    }
  ],
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
| `product` | Object | 指定產品版本的產品主檔資料；查無產品時依既有 not-found response 處理。 | `product` |
| `product.productNo` | String | 製成品 no。 | `product.no` |
| `product.productName` | String | 製成品名稱。 | `product.name` |
| `product.productCategory` | Integer | 製成品類別 code。 | `product.category` |
| `product.productVersion` | Integer | 本次明細使用的產品版本。 | `product.version` |
| `product.unitShipping` | Integer | 產品貨運單位 code。 | `product.unitShipping` |
| `product.unitWarehouse` | Integer | 產品倉儲單位 code。 | `product.unitWarehouse` |
| `product.unitProduct` | Integer | 產品產製單位 code。 | `product.unitProduct` |
| `product.comment` | String | 產品主檔備註。 | `product.comment` |
| `bom` | Object / Null | 該產品版本正式關聯的商品配方主檔；無關聯時為 `null`。 | `bom`、`product_spec` |
| `bom.bomNo` | String | 商品配方 no。 | `bom.no` |
| `bom.bomName` | String | 商品配方名稱。 | `bom.displayName` |
| `bom.bomVersion` | Integer | 商品配方版本。 | `bom.version` |
| `bom.dateTimestamp` | Integer | 商品配方日期，UTC timestamp。 | `bom.date` |
| `bom.unit` | Integer | 商品配方計算單位 code。 | `bom.unit` |
| `bom.weight` | Float | 商品配方基準重量，取至小數點第 2 位。 | `bom.weight` |
| `bom.comment` | String | 商品配方備註。 | `bom.comment` |
| `bomItems` | Array | 依產品版本與 BOM 關聯展開的 BOM 明細；此節點不另列說明。 | `product_spec`、`product_bom_spec`、正式 BOM tables |
| `bomItems[].level` | Integer | BOM 階層。 | `product_spec.level` / `product_bom_spec.level` |
| `bomItems[].itemNo` | String | BOM 明細料品或子 BOM no。 | `product_spec.item_no`、正式 BOM child no |
| `bomItems[].itemName` | String | BOM 明細料品或子 BOM 名稱。 | 正式料品主檔或 BOM 明細名稱 |
| `bomItems[].itemType` | Integer | BOM 明細類型 code。 | `product_spec.item_type` |
| `bomItems[].requiredCount` | Float | 該明細所需數量，取至小數點第 2 位。 | `product_spec.count`、`product_bom_spec.count` |
| `bomItems[].unit` | Integer | BOM 明細數量單位 code。 | `product_spec.unit`、`product_bom_spec.unit` |
| `bomItems[].weight` | Float | BOM 明細重量，取至小數點第 2 位。 | `product_spec.weight`、`product_bom_spec.weight` |
| `bomItems[].expectedLoss` | Float | 預估損耗率，取至小數點第 2 位。 | `product_spec.expectedLoss` 或正式 BOM loss 欄位 |
| `bomItems[].actualLoss` | Float | 實際損耗率，取至小數點第 2 位；無資料時為 0 並由狀態欄位表達缺漏。 | `product_spec.actualLoss` 或正式 BOM loss 欄位 |
| `bomItems[].sourceBomNo` | String | 該明細來源 BOM no；無法追溯時為空字串。 | 正式 BOM relation |
| `bomItems[].sourceBomVersion` | Integer | 該明細來源 BOM 版本；無法追溯時為 0。 | 正式 BOM relation |
| `costSummary` | Object | 指定產品版本的成本摘要；不代表已核准成本。 | `item_price`、BOM 計算 |
| `costSummary.materialCost` | Integer | 原料/物料成本加總，四捨五入取整數。 | 正式成本來源與 BOM 明細 |
| `costSummary.laborCost` | Integer | 人工成本加總，四捨五入取整數；來源不足時為 0 並回傳缺漏狀態。 | `labor_wage` 或工程師確認來源 |
| `costSummary.estimatedCost` | Integer | 目前可計算成本項目加總，四捨五入取整數。 | 成本試算結果 |
| `costSummary.costStatusCode` | String | 成本資料狀態 code。 | `complete`、`missing_source`、`unknown` |
| `quotations` | Array | 可由正式關聯取得的報價資料；無資料時為空陣列。 | `quotation` |
| `quotations[].quotationNo` | String | 報價單 no。 | `quotation.no` |
| `quotations[].dateTimestamp` | Integer | 報價日期，UTC timestamp。 | `quotation.date` |
| `quotations[].category` | Integer | 報價類別 code。 | `quotation.category` |
| `quotations[].itemStyle` | Integer | 報價品項樣式 code。 | `quotation.itemStyle` |
| `quotations[].itemNo` | String | 報價交易品項 no。 | `quotation.item_no` |
| `quotations[].itemName` | String | 報價交易品項名稱。 | `quotation.item_name` |
| `quotations[].supplierNo` | String | 報價供應商 no；非採購報價時可為空字串。 | `quotation.item_ref_no` |
| `quotations[].supplierName` | String | 報價供應商名稱；無正式公司關聯時為空字串。 | `company.displayName` |
| `quotations[].unit` | Integer | 報價單位 code。 | `quotation.unit` |
| `quotations[].unitPrice` | Float | 報價單價，取至小數點第 4 位。 | `quotation.price` |
| `contracts` | Array | 可由正式關聯取得的合約資料；無資料時為空陣列。 | `contract` |
| `contracts[].contractNo` | String | 合約 no。 | `contract.no` |
| `contracts[].refNo` | String | 合約來源或關聯 no；無值時為空字串。 | `contract.ref_no` |
| `contracts[].dateTimestamp` | Integer | 合約日期，UTC timestamp。 | `contract.date` |
| `contracts[].category` | Integer | 合約類別 code。 | `contract.category` |
| `contracts[].itemStyle` | Integer | 合約品項樣式 code。 | `contract.itemStyle` |
| `contracts[].itemNo` | String | 合約交易品項 no。 | `contract.item_no` |
| `contracts[].itemName` | String | 合約交易品項名稱。 | `contract.item_name` |
| `contracts[].supplierNo` | String | 合約供應商 no；非採購合約時可為空字串。 | `contract.item_ref_no` |
| `contracts[].supplierName` | String | 合約供應商名稱；無正式公司關聯時為空字串。 | `company.displayName` |
| `contracts[].unit` | Integer | 合約單位 code。 | `contract.unit` |
| `contracts[].unitPrice` | Float | 合約單價，取至小數點第 4 位。 | `contract.price` |
| `readiness` | Object | 產品版本資料準備度，不代表研發、客戶或量產核准。 | 計算欄位 |
| `readiness.statusCode` | String | 準備度狀態 code。 | `ready`、`incomplete`、`unknown` |
| `readiness.riskCode` | String | 主要資料缺口 code；無缺口時為 `normal`。 | `bom_missing`、`cost_missing`、`quotation_missing`、`contract_missing`、`unknown`、`normal` |
| `readiness.missingFieldCodes` | Array<String> | 尚缺少的資料欄位 code；無缺漏時為空陣列。 | `bom`、`cost`、`quotation`、`contract` |

`readiness` 只呈現資料完整性 code，不代表研發主管核准、生產核准或客戶確認樣品。

## 6. GET `/api/v2/product-development/products/{product_no}/cost-simulation`

### 6.1 Success Response Data

```json
{
  "productNo": "String",
  "productVersion": "Integer",
  "bomNo": "String",
  "bomVersion": "Integer",
  "items": [
    {
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "requiredQuantity": "Float",
      "unit": "Integer",
      "unitCost": "Float",
      "lossRate": "Float",
      "estimatedAmount": "Integer",
      "costStatusCode": "String"
    }
  ],
  "materialCost": "Integer",
  "laborCost": "Integer",
  "estimatedCost": "Integer",
  "costStatusCode": "String"
}
```

### 6.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `productNo` | String | 成本試算的製成品 no。 | `product.no` |
| `productVersion` | Integer | 成本試算使用的產品版本。 | `product.version` |
| `bomNo` | String | 成本試算使用的商品配方 no；無 BOM 時為空字串。 | `bom.no` |
| `bomVersion` | Integer | 成本試算使用的商品配方版本；無 BOM 時為 0。 | `bom.version` |
| `items` | Array | 成本試算明細；此節點不另列說明。 | BOM 明細與成本來源 |
| `items[].itemNo` | String | 成本明細料品 no。 | BOM 明細 item no |
| `items[].itemName` | String | 成本明細料品名稱。 | 正式料品主檔或 BOM 明細名稱 |
| `items[].itemCategory` | Integer | 成本明細料品類別 code。 | 正式料品主檔 |
| `items[].requiredQuantity` | Float | 成本計算所需數量，取至小數點第 2 位。 | BOM 明細 |
| `items[].unit` | Integer | 成本明細數量單位 code。 | BOM 明細 |
| `items[].unitCost` | Float | 成本明細單位成本，取至小數點第 4 位。 | `item_price` 或工程師確認的正式成本來源 |
| `items[].lossRate` | Float | 成本計算採用的損耗率，取至小數點第 2 位。 | BOM expected/actual loss |
| `items[].estimatedAmount` | Integer | 成本明細估算金額，四捨五入取整數。 | `requiredQuantity * unitCost` 加損耗計算 |
| `items[].costStatusCode` | String | 個別成本明細狀態 code。 | `complete`、`missing_source`、`unknown` |
| `materialCost` | Integer | 原料與物料成本加總，四捨五入取整數。 | 成本明細分類加總 |
| `laborCost` | Integer | 人工成本加總，四捨五入取整數；未確認人工來源時為 0 並標示缺漏。 | `labor_wage` 或工程師確認來源 |
| `estimatedCost` | Integer | 產品版本預估總成本，四捨五入取整數。 | `materialCost + laborCost` 及其他已確認成本 |
| `costStatusCode` | String | 整體成本試算狀態 code。 | `complete`、`missing_source`、`invalid_bom`、`unknown` |

成本計算只使用已存在且可追溯的 BOM、料品成本與人工成本資料；缺少正式成本來源時回傳 `costStatusCode=missing_source`，不可用零值宣稱成本為零。

## 7. Frontend Responsibility

1. 將產品類別、BOM 狀態、準備度、風險與成本狀態 code 轉換為繁中、英文及其他語系。
2. 前端負責版本切換、篩選、排序、分頁與 detail panel 狀態，不自行計算 BOM 成本。
3. 不將 `readinessStatusCode=ready` 解讀為客戶已確認樣品或正式可量產。
4. 目前沒有正式營養標示 schema，因此 V1 不回傳營養數值；畫面應保留「營養標示資料尚未納入 V1」狀態，待 schema 確認後另行設計。

## 8. Engineer Review Questions

1. `product_spec` 與 `product_bom_spec` 是否是產品版本 BOM 的唯一正式來源，或需同時展開 `bom1`/`bom2`？
2. `item_price` 中哪一個成本欄位是第一版成本試算的正式來源；`est*` 與正式 `cost*` 欄位如何區分？
3. 人工成本是否依 `labor_wage` 與產品/製程資料計算，或 V1 只回傳料品成本？
4. 報價與合約是否以 `quotation.item_no`、`contract.item_no` 對應產品/BOM，且採購與訂購 category 的篩選規則是否固定？
5. 是否已有開發需求、打樣、客戶樣品確認及營養標示的正式資料表？若沒有，是否同意從 V1 Core 排除並另開 DB extension proposal？
6. `readinessStatusCode=ready` 的必要條件是否僅為 BOM 與成本資料完整，或必須包含報價/合約？

## 9. Non-Goals

- 不設計產品、BOM、配方、報價、合約的 POST/PUT/DELETE。
- 不新增未經工程師確認的 DB schema 或 SQL。
- 不推導不存在的樣品確認、營養標示、客戶核准或量產核准狀態。
