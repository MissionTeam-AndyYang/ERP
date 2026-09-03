# recipe-formula API Group

> Source: `restserver/package/restserver/api/v2/recipe_formula_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v2/recipe-formula/dashboard](#get-api-v2-recipe-formula-dashboard) | GET | 查詢 Recipe / Formula 版本摘要與狀態清單 | OK | 依 CTO `ERP2-RECIPE-FORMULA-RO-EXEC-001` 最小 read-only 實作 |
| [/api/v2/recipe-formula/{recipe_no}/versions](#get-api-v2-recipe-formula-recipe_no-versions) | GET | 查詢指定 Recipe 的版本清單 | OK | Formula 為 Recipe Version 的組成視圖 |
| [/api/v2/recipe-formula/{recipe_no}/versions/{version}/composition](#get-api-v2-recipe-formula-recipe_no-versions-version-composition) | GET | 查詢指定 Recipe Version 的 Formula composition | OK | 回傳 inputs 與 exactly one defined output 視圖；缺漏以 warning code 表示 |
| [/api/v2/recipe-formula/by-product/{product_no}](#get-api-v2-recipe-formula-by-product-product_no) | GET | 依製成品查詢相關 Recipe / Formula 版本 | OK | Product Structure reference only，不代表產品結構寫入或成本權威 |

## GET /api/v2/recipe-formula/dashboard

<a id="get-api-v2-recipe-formula-dashboard"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/recipe-formula/dashboard | GET | 查詢 Recipe / Formula 版本摘要與狀態清單 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示偏好的 IANA timezone；後端仍直接回傳資料庫保存的 UTC timestamp |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| keyword | String | NO | Recipe no 或 Recipe 名稱關鍵字 |
| formulaStatusCode | String | NO | Formula 狀態 code |
| effectiveDate | Integer | NO | Recipe Version 狀態判斷基準 UTC timestamp；未提供時使用系統時間 |
| start | Integer | NO | 分頁起點，預設 0 |
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
      "recipeCount": "Integer",
      "versionCount": "Integer",
      "completeFormulaCount": "Integer",
      "partialFormulaCount": "Integer",
      "missingFormulaCount": "Integer"
    },
    "recipes": [
      {
        "recipeNo": "String",
        "recipeName": "String",
        "recipeVersion": "Integer",
        "versionStateCode": "String",
        "formulaStatusCode": "String",
        "inputCount": "Integer",
        "outputCount": "Integer",
        "weight": "Float",
        "unit": "Integer",
        "dateTimestamp": "Integer",
        "warningCodes": ["String"]
      }
    ],
    "capabilityBoundary": {
      "recipeWriteSupported": "Boolean",
      "bomWriteSupported": "Boolean",
      "productWriteSupported": "Boolean",
      "productStructureSeparated": "Boolean",
      "routingReferenceOnly": "Boolean",
      "productionObservationSeparated": "Boolean",
      "costingExcluded": "Boolean"
    },
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
| payload.summary.recipeCount | Integer | 套用篩選後的不重複 Recipe 數量；第一版以 bom.no 作為 read-only Recipe definition evidence |  |
| payload.summary.versionCount | Integer | 套用篩選後的 Recipe Version 數量；第一版以 bom.version 作為版本 evidence |  |
| payload.summary.completeFormulaCount | Integer | Formula 狀態為 complete 的版本數 |  |
| payload.summary.partialFormulaCount | Integer | Formula 狀態為 partial 的版本數 |  |
| payload.summary.missingFormulaCount | Integer | Formula 狀態為 missing 的版本數 |  |
| payload.recipes[].recipeNo | String | Recipe 編號；第一版來源為 bom.no |  |
| payload.recipes[].recipeName | String | Recipe 名稱；第一版來源為 bom.displayName，無值時回傳空字串 |  |
| payload.recipes[].recipeVersion | Integer | Recipe Version；第一版來源為 bom.version |  |
| payload.recipes[].versionStateCode | String | 版本狀態 code；前端負責轉換顯示文字 | effective / future / historical / unknown |
| payload.recipes[].formulaStatusCode | String | Formula 組成狀態 code；前端負責轉換顯示文字 | complete / partial / missing / unknown |
| payload.recipes[].inputCount | Integer | 此 Recipe Version 的 input 數量；第一版依 bom_item 筆數統計 |  |
| payload.recipes[].outputCount | Integer | 此 Recipe Version 可對應的 output 數量；第一版依 product_spec.bom_no + bom_version 對應產品去重統計 |  |
| payload.recipes[].weight | Float | Recipe Version 的基準重量；來源為 bom.weight，取至小數點第 2 位 |  |
| payload.recipes[].unit | Integer | Recipe Version 的重量單位 code；來源為 bom.unit | Unit enum |
| payload.recipes[].dateTimestamp | Integer | Recipe Version 生效日期 UTC timestamp；來源為 bom.date，無值時回傳 0 |  |
| payload.recipes[].warningCodes[] | String | 此 Recipe Version 的資料條件 warning code | ERecipeFormulaWarningCode |
| payload.capabilityBoundary.recipeWriteSupported | Boolean | 是否支援 Recipe 寫入；本 API 固定為 false |  |
| payload.capabilityBoundary.bomWriteSupported | Boolean | 是否支援 BOM 寫入；本 API 固定為 false |  |
| payload.capabilityBoundary.productWriteSupported | Boolean | 是否支援 Product 寫入；本 API 固定為 false |  |
| payload.capabilityBoundary.productStructureSeparated | Boolean | Product Structure 是否與 Formula 語意分離；本 API 固定為 true |  |
| payload.capabilityBoundary.routingReferenceOnly | Boolean | Routing 是否僅作參考語境；本 API 固定為 true |  |
| payload.capabilityBoundary.productionObservationSeparated | Boolean | Production Observation 是否與 Recipe authority 分離；本 API 固定為 true |  |
| payload.capabilityBoundary.costingExcluded | Boolean | 成本計算是否排除於本 API 權限外；本 API 固定為 true |  |
| payload.total | Integer | 套用篩選後的版本總筆數 |  |
| payload.start | Integer | 本次分頁起點 |  |
| payload.count | Integer | 本次實際回傳筆數 |  |

### Processing Flow

1. 讀取 keyword、formulaStatusCode、effectiveDate、start、count。
2. 查詢 bom 作為 Recipe definition / Recipe Version evidence。
3. 依 bom.date 與同一 bom.no 的版本判斷 versionStateCode。
4. 以 bom_item 計算 inputCount。
5. 以 product_spec.bom_no + bom_version 對應產品，計算 outputCount。
6. 依 input、output、weight 條件判斷 formulaStatusCode 與 warningCodes。
7. 回傳 summary、recipes、capabilityBoundary 與分頁資訊。

### Database Tables Used

| Table | Purpose |
|----------|------|
| bom | 提供 Recipe definition 與 Recipe Version evidence |
| bom_item | 提供 Formula inputs 統計 |
| product_spec | 提供 Formula output 與產品結構參考 evidence |

## GET /api/v2/recipe-formula/{recipe_no}/versions

<a id="get-api-v2-recipe-formula-recipe_no-versions"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/recipe-formula/{recipe_no}/versions | GET | 查詢指定 Recipe 的版本清單 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示偏好的 IANA timezone；後端仍直接回傳資料庫保存的 UTC timestamp |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| effectiveDate | Integer | NO | Recipe Version 狀態判斷基準 UTC timestamp；未提供時使用系統時間 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "recipe": {
      "recipeNo": "String",
      "recipeName": "String",
      "recipeSourceCode": "String"
    },
    "versions": [
      {
        "recipeNo": "String",
        "recipeVersion": "Integer",
        "versionStateCode": "String",
        "dateTimestamp": "Integer",
        "weight": "Float",
        "unit": "Integer"
      }
    ],
    "capabilityBoundary": {}
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.recipe.recipeNo | String | Recipe 編號；第一版來源為 bom.no |  |
| payload.recipe.recipeName | String | Recipe 名稱；第一版來源為 bom.displayName |  |
| payload.recipe.recipeSourceCode | String | Recipe evidence 來源 code | bom |
| payload.versions[].recipeNo | String | Recipe 編號 |  |
| payload.versions[].recipeVersion | Integer | Recipe Version |  |
| payload.versions[].versionStateCode | String | 版本狀態 code | effective / future / historical / unknown |
| payload.versions[].dateTimestamp | Integer | 版本生效日期 UTC timestamp |  |
| payload.versions[].weight | Float | 版本基準重量；來源為 bom.weight，取至小數點第 2 位 |  |
| payload.versions[].unit | Integer | 版本重量單位 code | Unit enum |

### Processing Flow

1. 讀取 recipe_no 與 effectiveDate。
2. 查詢 bom.no = recipe_no 的全部版本；不存在時回傳 record not found。
3. 判斷各版本 versionStateCode。
4. 回傳 recipe、versions 與 capabilityBoundary。

### Database Tables Used

| Table | Purpose |
|----------|------|
| bom | 提供指定 Recipe 的版本清單 |

## GET /api/v2/recipe-formula/{recipe_no}/versions/{version}/composition

<a id="get-api-v2-recipe-formula-recipe_no-versions-version-composition"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/recipe-formula/{recipe_no}/versions/{version}/composition | GET | 查詢指定 Recipe Version 的 Formula composition |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示偏好的 IANA timezone；後端仍直接回傳資料庫保存的 UTC timestamp |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| effectiveDate | Integer | NO | Recipe Version 狀態判斷基準 UTC timestamp；未提供時使用系統時間 |

### Request Body

None

### Success Response Data

```json
{
  "payload": {
    "recipe": {},
    "version": {},
    "formula": {
      "recipeNo": "String",
      "recipeVersion": "Integer",
      "formulaStatusCode": "String",
      "weight": "Float",
      "unit": "Integer",
      "weightSourceCode": "String"
    },
    "inputs": [
      {
        "inputNo": "String",
        "inputName": "String",
        "inputCategory": "Integer",
        "inputSubCategory": "Integer",
        "quantity": "Integer",
        "weight": "Float",
        "unit": "Integer",
        "lossRate": "Float",
        "lossSourceCode": "String",
        "weightSourceCode": "String"
      }
    ],
    "output": {
      "outputNo": "String",
      "outputName": "String",
      "outputCategory": "Integer",
      "productVersion": "Integer",
      "quantity": "Integer",
      "weight": "Float",
      "unit": "Integer",
      "weightSourceCode": "String",
      "sourceCode": "String"
    },
    "sourceLineage": {
      "recipeSourceCode": "String",
      "inputSourceCode": "String",
      "outputSourceCode": "String",
      "productStructureReference": {
        "productNo": "String",
        "productVersion": "Integer",
        "bomNo": "String",
        "bomVersion": "Integer"
      },
      "routingContextRefs": [],
      "productionObservationRefs": []
    },
    "capabilityBoundary": {},
    "warnings": [
      {
        "warningCode": "String",
        "refNo": "String"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.formula.recipeNo | String | Recipe 編號 |  |
| payload.formula.recipeVersion | Integer | Recipe Version |  |
| payload.formula.formulaStatusCode | String | Formula composition 狀態 code | complete / partial / missing / unknown |
| payload.formula.weight | Float | Formula output 基準重量；來源為 bom.weight，取至小數點第 2 位 |  |
| payload.formula.unit | Integer | Formula output 基準重量單位 code；來源為 bom.unit | Unit enum |
| payload.formula.weightSourceCode | String | Formula weight evidence 來源 code | bom |
| payload.inputs[].inputNo | String | Formula input 料品 no；來源為 bom_item.item_no |  |
| payload.inputs[].inputName | String | Formula input 料品名稱；優先取 item master，否則取 bom_item.item_name |  |
| payload.inputs[].inputCategory | Integer | Formula input 品項類別 code | EItemCategory |
| payload.inputs[].inputSubCategory | Integer | Formula input 子分類 code |  |
| payload.inputs[].quantity | Integer | Formula input 數量；bom_item 無 count 欄位，第一版回傳 0 |  |
| payload.inputs[].weight | Float | Formula input 重量；來源為 bom_item.weight，取至小數點第 2 位 |  |
| payload.inputs[].unit | Integer | Formula input 重量單位 code；來源為 bom_item.unit | Unit enum |
| payload.inputs[].lossRate | Float | input-specific material loss；目前來源未記錄時回傳 0.0，並由 lossSourceCode / warnings 表示未記錄 |  |
| payload.inputs[].lossSourceCode | String | input-specific loss 來源 code | not_recorded |
| payload.inputs[].weightSourceCode | String | input weight evidence 來源 code | bom_item |
| payload.output.outputNo | String | Formula exactly one output 的製成品 no；來源為 product_spec.product_no 正規化後結果；缺漏時回傳空字串 |  |
| payload.output.outputName | String | Formula output 製成品名稱；來源為 product.name，無值時回傳空字串 |  |
| payload.output.outputCategory | Integer | Formula output 品項類別 code；第一版為製成品 | EItemCategory.PRODUCT |
| payload.output.productVersion | Integer | Formula output 對應 product_spec.product_version |  |
| payload.output.quantity | Integer | Formula output 數量；第一版定義為 1 |  |
| payload.output.weight | Float | Formula output 重量；來源為 bom.weight，取至小數點第 2 位 |  |
| payload.output.unit | Integer | Formula output 重量單位 code；來源為 bom.unit | Unit enum |
| payload.output.weightSourceCode | String | output weight evidence 來源 code | bom / not_recorded |
| payload.output.sourceCode | String | output evidence 來源 code | product_spec / not_recorded |
| payload.sourceLineage.recipeSourceCode | String | Recipe definition evidence 來源 code | bom |
| payload.sourceLineage.inputSourceCode | String | Formula input evidence 來源 code | bom_item |
| payload.sourceLineage.outputSourceCode | String | Formula output evidence 來源 code | product_spec / not_recorded |
| payload.sourceLineage.productStructureReference.productNo | String | 相關 Product Structure 參考 productNo；僅供交叉查閱，不代表 Product Structure 權威寫入 |  |
| payload.sourceLineage.productStructureReference.productVersion | Integer | 相關 Product Structure 參考 productVersion |  |
| payload.sourceLineage.productStructureReference.bomNo | String | 相關 Product Structure 參考 bomNo |  |
| payload.sourceLineage.productStructureReference.bomVersion | Integer | 相關 Product Structure 參考 bomVersion |  |
| payload.sourceLineage.routingContextRefs | Array | Routing context reference；第一版無正式來源時回傳空陣列 |  |
| payload.sourceLineage.productionObservationRefs | Array | Production Observation comparison reference；第一版不讀取生產資料，回傳空陣列 |  |
| payload.warnings[].warningCode | String | Formula composition 條件或資料缺漏 warning code | missing_inputs / missing_output / multiple_outputs / missing_input_weight / missing_output_weight / missing_loss_source / unknown |
| payload.warnings[].refNo | String | warning 相關 Recipe、input 或 output 參考 no |  |

### Processing Flow

1. 讀取 recipe_no、version 與 effectiveDate。
2. 查詢 bom.no + bom.version；不存在時回傳 record not found。
3. 查詢 bom_item 作為 Formula inputs；input weight 必須以 bom_item.weight 表示。
4. 查詢 product_spec.bom_no + bom_version，正規化 product_no 後作為 output candidates。
5. 若 output candidates 正好一筆，作為 Formula output；若為 0 或多筆，回傳 warning code。
6. 組成 sourceLineage，明確標示 Product Structure reference、Routing reference only、Production Observation separated、Costing excluded。
7. 不讀取成本資料、不讀取生產觀測資料、不建立或修改 Recipe / BOM / Product。

### Database Tables Used

| Table | Purpose |
|----------|------|
| bom | 提供 Recipe Version 與 Formula output weight evidence |
| bom_item | 提供 Formula inputs 與 input weight evidence |
| product_spec | 提供 Formula exactly one output candidate 與 Product Structure reference |
| product | 提供 output 製成品名稱 |
| material | 提供 input 原料/物料/膠捲主檔名稱與類別 |
| inproduct | 提供 input 在製品主檔名稱與類別 |
| goods | 提供 input 貨品主檔名稱與類別 |

## GET /api/v2/recipe-formula/by-product/{product_no}

<a id="get-api-v2-recipe-formula-by-product-product_no"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/recipe-formula/by-product/{product_no} | GET | 依製成品查詢相關 Recipe / Formula 版本 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示偏好的 IANA timezone；後端仍直接回傳資料庫保存的 UTC timestamp |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| productVersion | Integer | NO | 指定製成品版本；未提供時查詢此製成品全部可讀 product_spec 版本 |
| effectiveDate | Integer | NO | Recipe Version 狀態判斷基準 UTC timestamp；未提供時使用系統時間 |

### Success Response Data

```json
{
  "payload": {
    "serverTimestamp": "Integer",
    "productNo": "String",
    "productVersion": "Integer",
    "recipeVersions": [],
    "capabilityBoundary": {}
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.productNo | String | 查詢製成品 no |  |
| payload.productVersion | Integer | 查詢製成品版本；未指定時回傳 0，表示 recipeVersions 可包含多版本結果 |  |
| payload.recipeVersions[] | Array | 符合製成品條件的 Formula composition；每筆結構同 composition API payload |  |

### Processing Flow

1. 讀取 product_no、productVersion 與 effectiveDate。
2. 查詢 product_spec.product_no = product_no 或 product_no + "_1"。
3. 依 productVersion 篩選；未指定時保留所有版本。
4. 取 product_spec.bom_no + bom_version 去重，逐筆組成 Formula composition。
5. 回傳 recipeVersions 與 capabilityBoundary。

### Database Tables Used

| Table | Purpose |
|----------|------|
| product_spec | 依製成品反查相關 Recipe Version |
| bom | 提供 Recipe Version evidence |
| bom_item | 提供 Formula input evidence |
| product | 提供 output 製成品名稱 |
| material | 提供 input 主檔名稱與類別 |
| inproduct | 提供 input 主檔名稱與類別 |
| goods | 提供 input 主檔名稱與類別 |
