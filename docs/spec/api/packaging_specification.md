# Packaging Specification API Group

> Source: `restserver/package/restserver/api/v2/packaging_specification_uri.py`
> Proposal Source: `docs/spec/api-proposal/packaging_specification_proposal.md`
> Flow Source: `docs/spec/api-proposal/packaging_specification_flow_algorithm.md`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v2/packaging-specification/overview](#get-api-v2-packaging-specification-overview) | GET | 查詢 Product/WIP 包裝規格唯讀總覽 | OK | Product 直接查 `product_bom_spec`；WIP 以 `product_spec` 查下游 Product 包裝 context 並標示 partial。 |

## GET /api/v2/packaging-specification/overview

<a id="get-api-v2-packaging-specification-overview"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/packaging-specification/overview | GET | 查詢 Product/WIP 包裝規格唯讀總覽 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 時區代碼，例如 Asia/Taipei |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|----------|----------------|
| itemNo | String | YES | 查詢主體 no；製成品對應 `product.no`，在製品對應 `inproduct.no`。 |
| itemCategory | Integer | YES | 查詢主體類別；僅支援 `4` 在製品、`5` 製成品。 |
| productVersion | Integer | NO | 製成品版本；未提供時製成品使用 `product.version`，在製品使用下游 `product_spec.product_version`。 |
| effectiveDate | Integer | NO | 保留給後續版本/生效日治理；第一版不做包裝版本生效日篩選。 |

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
      "productVersion": "Integer",
      "effectiveDate": "Integer"
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
    "summary": {
      "packagingSpecCount": "Integer",
      "packagingBomCount": "Integer",
      "packageLevelCount": "Integer",
      "materialLineCount": "Integer",
      "totalCount": "Integer",
      "totalWeight": "Float"
    },
    "packagingSpecs": [],
    "sourceLineage": {},
    "warnings": [],
    "moduleReadiness": [],
    "capabilityBoundary": {}
  }
}
```

### Field Description

| Field | Type | Description |
|----------|----------|----------------|
| payload.serverTimestamp | Integer | 後端產生回應的 UTC timestamp。 |
| payload.timezone | String | Request header 傳入的時區；未提供時回傳 `UTC`。 |
| payload.requestIdentity.itemNo | String | 本次查詢主體 no。 |
| payload.requestIdentity.itemCategory | Integer | 本次查詢主體類別；4 為在製品，5 為製成品。 |
| payload.requestIdentity.productVersion | Integer | 本次查詢的製成品版本。 |
| payload.requestIdentity.effectiveDate | Integer | 保留給後續生效日治理的查詢時間。 |
| payload.subject.itemNo | String | 主體料品 no。 |
| payload.subject.itemName | String | 主體料品名稱。 |
| payload.subject.itemCategory | Integer | 主體料品品項類別。 |
| payload.subject.itemSubCategory | Integer | 主體在原主檔中的細分類別。 |
| payload.subject.productVersion | Integer | 製成品目前版本；在製品為 0。 |
| payload.subject.unitShipping | Integer | 出貨單位代碼。 |
| payload.subject.unitWarehouse | Integer | 倉儲單位代碼。 |
| payload.subject.unitProduct | Integer | 生產單位代碼。 |
| payload.subject.comment | String | 主檔備註。 |
| payload.subject.sourceCode | String | 主體來源；製成品為 `product`，在製品為 `inproduct`。 |
| payload.summary.packagingSpecCount | Integer | 包裝規格筆數。 |
| payload.summary.packagingBomCount | Integer | 不重複包裝 BOM 數。 |
| payload.summary.packageLevelCount | Integer | 不重複包裝階層數。 |
| payload.summary.materialLineCount | Integer | 包裝 BOM 明細總列數。 |
| payload.summary.totalCount | Integer | 包裝規格數量加總。 |
| payload.summary.totalWeight | Float | 包裝規格重量加總，取小數點第 2 位。 |
| payload.packagingSpecs[].specId | String | 包裝規格識別字，格式為 `productNo:productVersion:packagingBomNo`。 |
| payload.packagingSpecs[].productNo | String | 包裝規格所屬製成品 no。 |
| payload.packagingSpecs[].productVersion | Integer | 包裝規格所屬製成品版本。 |
| payload.packagingSpecs[].wipNo | String | WIP 查詢情境下的在製品 no；Product 查詢時為空字串。 |
| payload.packagingSpecs[].packagingLevel | Integer | 包裝階層，來源 `product_bom_spec.level`。 |
| payload.packagingSpecs[].packagingBomNo | String | 包裝 BOM no，來源 `product_bom_spec.bom2_no`。 |
| payload.packagingSpecs[].packagingBomName | String | 包裝 BOM 顯示名稱，來源 `bom2_number.displayName`。 |
| payload.packagingSpecs[].count | Integer | 包裝規格數量，來源 `product_bom_spec.count`。 |
| payload.packagingSpecs[].unit | Integer | 包裝規格單位，來源 `product_bom_spec.unit`。 |
| payload.packagingSpecs[].weight | Float | 包裝規格重量，來源 `product_bom_spec.weight`，取小數點第 2 位。 |
| payload.packagingSpecs[].masterUnit | Integer | 包裝 BOM 主檔單位，來源 `bom2_number.unit`。 |
| payload.packagingSpecs[].masterWeight | Float | 包裝 BOM 主檔重量，來源 `bom2_number.weight`，取小數點第 2 位。 |
| payload.packagingSpecs[].linkedBomNo | String | 包裝 BOM 主檔連結的製成品 no，來源 `bom2_number.bom_no`。 |
| payload.packagingSpecs[].linkedBomVersion | Integer | 包裝 BOM 主檔連結的製成品版本，來源 `bom2_number.bom_version`。 |
| payload.packagingSpecs[].lineCount | Integer | 包裝 BOM 明細列數。 |
| payload.packagingSpecs[].lines[].parentBomNo | String | 包裝 BOM 父層 no，來源 `bom2.parent_no`。 |
| payload.packagingSpecs[].lines[].parentBomName | String | 包裝 BOM 父層名稱，來源 `bom2.parent_name`。 |
| payload.packagingSpecs[].lines[].childCategory | Integer | 子級料品類別，來源 `bom2.child_category`。 |
| payload.packagingSpecs[].lines[].childNo | String | 子級料品或子級 BOM no，來源 `bom2.child_id`。 |
| payload.packagingSpecs[].lines[].childName | String | 子級料品或子級 BOM 名稱，來源 `bom2.child_name`。 |
| payload.packagingSpecs[].lines[].childUnit | Integer | 子級料品單位，來源 `bom2.childUnit`。 |
| payload.packagingSpecs[].lines[].count | Integer | 子級料品數量，來源 `bom2.count`。 |
| payload.packagingSpecs[].lines[].childUnit2 | Integer | 子級第二單位，來源 `bom2.childUnit2`。 |
| payload.packagingSpecs[].lines[].weight | Float | 子級料品重量，來源 `bom2.weight`，取小數點第 2 位。 |
| payload.packagingSpecs[].lines[].length | Float | 子級料品長度，來源 `bom2.length`，取小數點第 2 位。 |
| payload.packagingSpecs[].lines[].expectedLoss | Float | 預估耗損，來源 `bom2.expectedLoss`，取小數點第 2 位。 |
| payload.packagingSpecs[].lines[].actualLoss | Float | 實際耗損，來源 `bom2.actualLoss`，取小數點第 2 位。 |
| payload.packagingSpecs[].lines[].processCount | Float | 加工數量，來源 `bom2.processCount`，取小數點第 2 位。 |
| payload.packagingSpecs[].lines[].comment | String | 包裝 BOM 明細備註。 |
| payload.packagingSpecs[].sourceCode | String | 規格來源，第一版為 `product_bom_spec`。 |
| payload.packagingSpecs[].masterSourceCode | String | 主檔來源；存在 `bom2_number` 時為 `bom2_number`，否則 `not_recorded`。 |
| payload.packagingSpecs[].lineSourceCode | String | 明細來源；存在 `bom2` 時為 `bom2`，否則 `not_recorded`。 |
| payload.sourceLineage.subjectSourceCode | String | 主體資料來源。 |
| payload.sourceLineage.packagingSpecSourceCode | String | 包裝規格資料來源。 |
| payload.sourceLineage.packagingBomMasterSourceCode | String | 包裝 BOM 主檔資料來源。 |
| payload.sourceLineage.packagingBomLineSourceCode | String | 包裝 BOM 明細資料來源。 |
| payload.warnings[].moduleCode | String | 發出警示的模組代碼。 |
| payload.warnings[].warningCode | String | 警示代碼。 |
| payload.warnings[].refNo | String | 警示對應參考 no。 |
| payload.moduleReadiness[].moduleCode | String | 模組代碼，第一版為 `packagingSpecification`。 |
| payload.moduleReadiness[].statusCode | String | 模組狀態：`complete`、`partial`、`unavailable`、`error`。 |
| payload.moduleReadiness[].sourceCode | String | 模組主要資料來源。 |
| payload.moduleReadiness[].warningCodes | Array | 模組警示代碼集合。 |
| payload.capabilityBoundary.readOnly | Boolean | 本 API 是否為唯讀，固定 `true`。 |
| payload.capabilityBoundary.packagingWriteSupported | Boolean | 第一版不支援包裝規格寫入，固定 `false`。 |
| payload.capabilityBoundary.packagingApprovalSupported | Boolean | 第一版不支援包裝規格審核，固定 `false`。 |
| payload.capabilityBoundary.packagingReleaseSupported | Boolean | 第一版不支援包裝規格發行，固定 `false`。 |
| payload.capabilityBoundary.sourceOfTruthTransitionSupported | Boolean | 第一版不進行 Source-of-Truth transition，固定 `false`。 |
| payload.capabilityBoundary.cutoverSupported | Boolean | 第一版不進行 Cutover，固定 `false`。 |
| payload.capabilityBoundary.goLiveSupported | Boolean | 第一版不進行 Go-Live，固定 `false`。 |

### Processing Flow

1. 解析 `itemNo`、`itemCategory`、`productVersion`、`effectiveDate`。
2. 驗證 `itemNo` 不可為空，且 `itemCategory` 僅允許 4 或 5。
3. 依 `itemCategory` 查詢 `product` 或 `inproduct` 主體。
4. Product 情境依 `product_bom_spec.product_no + product_version` 查詢包裝規格。
5. WIP 情境依 `product_spec.item_no = WIP itemNo` 找下游 Product，再查詢下游 Product 的包裝 context 並標示 partial warning。
6. 以 `bom2_number.no = product_bom_spec.bom2_no` 補主檔顯示名稱、單位與重量。
7. 以 `bom2.parent_no = product_bom_spec.bom2_no` 補包裝 BOM 明細。
8. 彙總規格數、BOM 數、階層數、明細列數、數量與重量。
9. 建立 `moduleReadiness[]`、`warnings[]`、`sourceLineage` 與 `capabilityBoundary`。
10. 回傳唯讀 response；此 endpoint 未註冊 POST/PUT/PATCH/DELETE。

### Database Tables Used

| Table | Usage |
|----------|----------|
| product | 製成品主體主檔。 |
| inproduct | 在製品主體主檔。 |
| product_spec | WIP 下游 Product context 查詢。 |
| product_bom_spec | Product 包裝規格主來源。 |
| bom2_number | 包裝 BOM 主檔。 |
| bom2 | 包裝 BOM 明細。 |

### Error Response

| HTTP Status | Code | Message | Description |
|----------|----------|----------|----------------|
| 400 | 3001 | itemNo is required | 未提供查詢主體 no。 |
| 400 | 3001 | invalid itemCategory | `itemCategory` 不是 4 或 5。 |
| 404 | 1 | record not found | 查詢主體不存在於指定主檔。 |
| 405 | - | - | 本 API 未提供 POST/PUT/PATCH/DELETE。 |
