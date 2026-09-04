# routing API Group

> Source: `restserver/package/restserver/api/v2/routing_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v2/routing/dashboard](#get-api-v2-routing-dashboard) | GET | 查詢 Product / WIP Routing Version 摘要清單 | OK | 依 CTO `ERP2-ROUTING-PROCESS-FLOW-RO-EXEC-001` 最小 read-only 實作 |
| [/api/v2/routing/products/{item_no}/versions](#get-api-v2-routing-products-item_no-versions) | GET | 查詢指定製成品或在製品的 Routing Version 清單 | OK | 第一版以 product_process 作為 Routing Version evidence |
| [/api/v2/routing/versions/{routing_version_id}/steps](#get-api-v2-routing-versions-routing_version_id-steps) | GET | 查詢指定 Routing Version 的 ordered process steps | OK | 第一版以 process_flow.order 作為步驟順序 |
| [/api/v2/routing/products/{item_no}/current](#get-api-v2-routing-products-item_no-current) | GET | 查詢指定製成品或在製品目前生效 Routing | OK | 依 product_process.date 與 version 判斷目前生效版本 |

## GET /api/v2/routing/dashboard

<a id="get-api-v2-routing-dashboard"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/routing/dashboard | GET | 查詢 Product / WIP Routing Version 摘要清單 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示偏好的 IANA timezone；後端仍直接回傳資料庫保存的 UTC timestamp |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| keyword | String | NO | Routing Version、製成品/在製品 no 或名稱關鍵字 |
| routingStatusCode | String | NO | Routing 狀態 code |
| effectiveDate | Integer | NO | Routing Version 狀態判斷基準 UTC timestamp；未提供時使用系統時間 |
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
      "itemCount": "Integer",
      "routingVersionCount": "Integer",
      "completeRoutingCount": "Integer",
      "partialRoutingCount": "Integer",
      "missingRoutingCount": "Integer"
    },
    "routingVersions": [
      {
        "routingVersionId": "String",
        "itemNo": "String",
        "itemName": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "routingVersion": "Integer",
        "versionStateCode": "String",
        "routingStatusCode": "String",
        "dateTimestamp": "Integer",
        "stepCount": "Integer",
        "warningCodes": ["String"]
      }
    ],
    "capabilityBoundary": {
      "routingWriteSupported": "Boolean",
      "processMasterWriteSupported": "Boolean",
      "productWriteSupported": "Boolean",
      "approvalSupported": "Boolean",
      "releaseSupported": "Boolean",
      "freezeSupported": "Boolean",
      "schedulingExecutionSupported": "Boolean",
      "capacityExecutionSupported": "Boolean",
      "packagingSpecificationImplementationSupported": "Boolean",
      "productionActionSupported": "Boolean",
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
| payload.summary.itemCount | Integer | 套用篩選後具有 Routing Version 的不重複製成品/在製品數量 |  |
| payload.summary.routingVersionCount | Integer | 套用篩選後的 Routing Version 總數 |  |
| payload.summary.completeRoutingCount | Integer | Routing 狀態為 complete 的版本數 |  |
| payload.summary.partialRoutingCount | Integer | Routing 狀態為 partial 的版本數 |  |
| payload.summary.missingRoutingCount | Integer | Routing 狀態為 missing 的版本數 |  |
| payload.routingVersions[].routingVersionId | String | Routing Version 識別碼；來源為 product_process.no |  |
| payload.routingVersions[].itemNo | String | 製成品或在製品 no；來源為 product_process.item_no |  |
| payload.routingVersions[].itemName | String | 製成品或在製品名稱；來源為 product.name 或 inproduct.name，無值時回傳空字串 |  |
| payload.routingVersions[].itemCategory | Integer | 品項類別 code；製成品為 5，在製品為 4，未解析時為 0 | EItemCategory |
| payload.routingVersions[].itemSubCategory | Integer | 品項子分類 code；製成品來源為 product.category，在製品來源為 inproduct.category |  |
| payload.routingVersions[].routingVersion | Integer | Routing Version；來源為 product_process.version |  |
| payload.routingVersions[].versionStateCode | String | 版本狀態 code；前端負責轉換顯示文字 | effective / future / historical / unknown |
| payload.routingVersions[].routingStatusCode | String | Routing 完整性狀態 code；前端負責轉換顯示文字 | complete / partial / missing / unknown |
| payload.routingVersions[].dateTimestamp | Integer | Routing Version 生效日期 UTC timestamp；來源為 product_process.date，無值時回傳 0 |  |
| payload.routingVersions[].stepCount | Integer | 此 Routing Version 的步驟數；來源為 process_flow 筆數 |  |
| payload.routingVersions[].warningCodes[] | String | 此 Routing Version 的資料條件 warning code | ERoutingWarningCode |
| payload.capabilityBoundary.routingWriteSupported | Boolean | 是否支援 Routing 寫入；本 API 固定為 false |  |
| payload.capabilityBoundary.processMasterWriteSupported | Boolean | 是否支援 Process Master 寫入；本 API 固定為 false |  |
| payload.capabilityBoundary.productWriteSupported | Boolean | 是否支援 Product 寫入；本 API 固定為 false |  |
| payload.capabilityBoundary.approvalSupported | Boolean | 是否支援核准；本 API 固定為 false |  |
| payload.capabilityBoundary.releaseSupported | Boolean | 是否支援發行；本 API 固定為 false |  |
| payload.capabilityBoundary.freezeSupported | Boolean | 是否支援凍結；本 API 固定為 false |  |
| payload.capabilityBoundary.schedulingExecutionSupported | Boolean | 是否支援排程執行；本 API 固定為 false |  |
| payload.capabilityBoundary.capacityExecutionSupported | Boolean | 是否支援產能執行；本 API 固定為 false |  |
| payload.capabilityBoundary.packagingSpecificationImplementationSupported | Boolean | 是否支援包裝規格實作；本 API 固定為 false |  |
| payload.capabilityBoundary.productionActionSupported | Boolean | 是否支援生產動作；本 API 固定為 false |  |
| payload.capabilityBoundary.costingExcluded | Boolean | 成本計算是否排除於本 API 權限外；本 API 固定為 true |  |
| payload.total | Integer | 套用篩選後的版本總筆數 |  |
| payload.start | Integer | 本次分頁起點 |  |
| payload.count | Integer | 本次實際回傳筆數 |  |

### Processing Flow

1. 讀取 keyword、routingStatusCode、effectiveDate、start、count。
2. 查詢 product_process 作為 Routing Version evidence。
3. 依 product_process.item_no 對應 product / inproduct 主檔，補足品項名稱與品項類別。
4. 依同一 item_no 的 product_process.date 與 version 判斷 versionStateCode。
5. 以 process_flow 統計每個 Routing Version 的 stepCount。
6. 依 item master 與 stepCount 判斷 routingStatusCode 與 warningCodes。
7. 回傳 summary、routingVersions、capabilityBoundary 與分頁資訊。

### Database Tables Used

| Table | Purpose |
|----------|------|
| product_process | 提供 Routing Version evidence |
| process_flow | 提供 Routing Step 統計 |
| product | 提供製成品名稱與分類 |
| inproduct | 提供在製品名稱與分類 |

## GET /api/v2/routing/products/{item_no}/versions

<a id="get-api-v2-routing-products-item_no-versions"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/routing/products/{item_no}/versions | GET | 查詢指定製成品或在製品的 Routing Version 清單 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示偏好的 IANA timezone；後端仍直接回傳資料庫保存的 UTC timestamp |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| effectiveDate | Integer | NO | Routing Version 狀態判斷基準 UTC timestamp；未提供時使用系統時間 |

### Request Body

None

### Success Response Data

```json
{
  "payload": {
    "serverTimestamp": "Integer",
    "item": {
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "itemSubCategory": "Integer",
      "sourceCode": "String"
    },
    "versions": [
      {
        "routingVersionId": "String",
        "itemNo": "String",
        "itemName": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "routingVersion": "Integer",
        "versionStateCode": "String",
        "routingStatusCode": "String",
        "dateTimestamp": "Integer",
        "stepCount": "Integer",
        "warningCodes": ["String"]
      }
    ],
    "capabilityBoundary": {}
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.item.itemNo | String | 查詢的製成品或在製品 no |  |
| payload.item.itemName | String | 製成品或在製品名稱；來源為 product.name 或 inproduct.name |  |
| payload.item.itemCategory | Integer | 品項類別 code | EItemCategory |
| payload.item.itemSubCategory | Integer | 品項子分類 code |  |
| payload.item.sourceCode | String | item master evidence 來源 code | product / inproduct / not_recorded |
| payload.versions[].routingVersionId | String | Routing Version 識別碼；來源為 product_process.no |  |
| payload.versions[].itemNo | String | 製成品或在製品 no |  |
| payload.versions[].itemName | String | 製成品或在製品名稱 |  |
| payload.versions[].itemCategory | Integer | 品項類別 code | EItemCategory |
| payload.versions[].itemSubCategory | Integer | 品項子分類 code |  |
| payload.versions[].routingVersion | Integer | Routing Version |  |
| payload.versions[].versionStateCode | String | 版本狀態 code | effective / future / historical / unknown |
| payload.versions[].routingStatusCode | String | Routing 完整性狀態 code | complete / partial / missing / unknown |
| payload.versions[].dateTimestamp | Integer | Routing Version 生效日期 UTC timestamp |  |
| payload.versions[].stepCount | Integer | Routing Version 的步驟數 |  |
| payload.versions[].warningCodes[] | String | Routing Version warning code | ERoutingWarningCode |

### Processing Flow

1. 讀取 item_no 與 effectiveDate。
2. 查詢 product_process.item_no = item_no 的所有 Routing Version；不存在時回傳 record not found。
3. 查詢 product / inproduct 補足 item header。
4. 判斷各版本 versionStateCode、stepCount、routingStatusCode。
5. 回傳 item、versions 與 capabilityBoundary。

### Database Tables Used

| Table | Purpose |
|----------|------|
| product_process | 提供指定品項的 Routing Version 清單 |
| process_flow | 提供每個 Routing Version 的步驟數 |
| product | 提供製成品主檔 |
| inproduct | 提供在製品主檔 |

## GET /api/v2/routing/versions/{routing_version_id}/steps

<a id="get-api-v2-routing-versions-routing_version_id-steps"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/routing/versions/{routing_version_id}/steps | GET | 查詢指定 Routing Version 的 ordered process steps |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示偏好的 IANA timezone；後端仍直接回傳資料庫保存的 UTC timestamp |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| effectiveDate | Integer | NO | Routing Version 狀態判斷基準 UTC timestamp；未提供時使用系統時間 |

### Request Body

None

### Success Response Data

```json
{
  "payload": {
    "serverTimestamp": "Integer",
    "routingVersion": {
      "routingVersionId": "String",
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "itemSubCategory": "Integer",
      "routingVersion": "Integer",
      "versionStateCode": "String",
      "routingStatusCode": "String",
      "dateTimestamp": "Integer",
      "stepCount": "Integer",
      "warningCodes": ["String"]
    },
    "steps": [
      {
        "stepId": "String",
        "stepOrder": "Integer",
        "oneProcess": "Integer",
        "secProcess": "Integer",
        "processNo": "String",
        "processLabel": "String",
        "stageCode": "String",
        "stageLabel": "String",
        "groupCode": "String",
        "groupLabel": "String",
        "recipeReference": {
          "established": "Boolean",
          "recipeNo": "String",
          "recipeVersion": "Integer",
          "sourceCode": "String"
        },
        "packagingContext": {
          "established": "Boolean",
          "packagingLevel": "Integer",
          "packagingBomNo": "String",
          "quantity": "Integer",
          "unit": "Integer",
          "weight": "Float",
          "sourceCode": "String"
        },
        "resourceEligibility": {
          "governed": "Boolean",
          "eligibleResourceRefs": [],
          "sourceCode": "String"
        },
        "standardPerformance": {
          "governed": "Boolean",
          "hourlyOutput": "Float",
          "laborCount": "Integer",
          "unit": "Integer",
          "sourceDateTimestamp": "Integer",
          "sourceCode": "String"
        },
        "sourceLineage": {
          "stepSourceCode": "String",
          "processSourceCode": "String",
          "standardPerformanceSourceCode": "String"
        }
      }
    ],
    "sourceLineage": {},
    "capabilityBoundary": {},
    "warnings": [
      {
        "warningCode": "String",
        "refNo": "String",
        "stepId": "String"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.routingVersion.routingVersionId | String | Routing Version 識別碼；來源為 product_process.no |  |
| payload.routingVersion.itemNo | String | Routing 所屬製成品或在製品 no |  |
| payload.routingVersion.itemName | String | Routing 所屬製成品或在製品名稱 |  |
| payload.routingVersion.itemCategory | Integer | 品項類別 code | EItemCategory |
| payload.routingVersion.itemSubCategory | Integer | 品項子分類 code |  |
| payload.routingVersion.routingVersion | Integer | Routing Version |  |
| payload.routingVersion.versionStateCode | String | 版本狀態 code | effective / future / historical / unknown |
| payload.routingVersion.routingStatusCode | String | Routing 完整性狀態 code | complete / partial / missing / unknown |
| payload.routingVersion.dateTimestamp | Integer | Routing Version 生效日期 UTC timestamp |  |
| payload.routingVersion.stepCount | Integer | Routing Step 數量 |  |
| payload.routingVersion.warningCodes[] | String | Routing warning code | ERoutingWarningCode |
| payload.steps[].stepId | String | Routing Step 識別碼；來源為 process_flow.no |  |
| payload.steps[].stepOrder | Integer | Routing Step 執行順序；來源為 process_flow.order |  |
| payload.steps[].oneProcess | Integer | 主製程 code；來源為 process_flow.oneProcess | 前備 (1)、加工 (2)、包裝 (3)、其他 (0) |
| payload.steps[].secProcess | Integer | 次製程 code；來源為 process_flow.secProcess | 依主製程定義 |
| payload.steps[].processNo | String | 製程主檔 no；依 oneProcess + secProcess 對應 process.no，無主檔時回傳空字串 |  |
| payload.steps[].processLabel | String | 製程顯示 label key 或資料庫保存文字；來源為 process.comment，無主檔時回傳空字串 |  |
| payload.steps[].stageCode | String | 主製程階段 code；由 oneProcess 派生，前端負責多國語言字串轉換 | preparation / processing / packaging / other / unknown |
| payload.steps[].stageLabel | String | 階段 label key；第一版同 stageCode，前端可依 enum 轉換 |  |
| payload.steps[].groupCode | String | 製程群組 code；第一版格式為 oneProcess:secProcess |  |
| payload.steps[].groupLabel | String | 製程群組 label key；第一版同 groupCode，前端可依 enum 轉換 |  |
| payload.steps[].recipeReference.established | Boolean | 是否已建立 Recipe reference；第一版依 product_spec 是否有 bom_no 判斷 |  |
| payload.steps[].recipeReference.recipeNo | String | 已建立的 Recipe/BOM no；來源為 product_spec.bom_no，未建立時回傳空字串 |  |
| payload.steps[].recipeReference.recipeVersion | Integer | 已建立的 Recipe/BOM version；來源為 product_spec.bom_version，未建立時回傳 0 |  |
| payload.steps[].recipeReference.sourceCode | String | Recipe reference evidence 來源 code | product_spec / not_recorded |
| payload.steps[].packagingContext.established | Boolean | 是否有包裝上下文；第一版依 product_bom_spec 是否存在判斷 |  |
| payload.steps[].packagingContext.packagingLevel | Integer | 包裝階層；來源為 product_bom_spec.level，未建立時回傳 0 |  |
| payload.steps[].packagingContext.packagingBomNo | String | 包裝 BOM no；來源為 product_bom_spec.bom2_no，未建立時回傳空字串 |  |
| payload.steps[].packagingContext.quantity | Integer | 包裝規格份數；來源為 product_bom_spec.count，未建立時回傳 0 |  |
| payload.steps[].packagingContext.unit | Integer | 包裝上下文單位 code；來源為 product_bom_spec.unit，未建立時回傳 0 | Unit enum |
| payload.steps[].packagingContext.weight | Float | 包裝上下文重量；來源為 product_bom_spec.weight，取至小數點第 2 位 |  |
| payload.steps[].packagingContext.sourceCode | String | 包裝上下文 evidence 來源 code | product_bom_spec / not_recorded |
| payload.steps[].resourceEligibility.governed | Boolean | 是否已有受治理資源資格來源；第一版固定 false，避免誤解為設備/人員派工能力 |  |
| payload.steps[].resourceEligibility.eligibleResourceRefs | Array | 合格資源參照；第一版無受治理來源時回傳空陣列 |  |
| payload.steps[].resourceEligibility.sourceCode | String | 資源資格 evidence 來源 code | not_recorded |
| payload.steps[].standardPerformance.governed | Boolean | 是否已建立標準績效參照；依 process_capacity 是否有同一 oneProcess + secProcess 且 date <= effectiveDate 的資料判斷 |  |
| payload.steps[].standardPerformance.hourlyOutput | Float | 標準時產量；來源為 process_capacity.hourlyOutput，取至小數點第 2 位，未建立時回傳 0.0 |  |
| payload.steps[].standardPerformance.laborCount | Integer | 標準人力人數；來源為 process_capacity.laborCount，未建立時回傳 0 |  |
| payload.steps[].standardPerformance.unit | Integer | 標準時產量單位 code；來源為 process_capacity.unit，未建立時回傳 0 | Unit enum |
| payload.steps[].standardPerformance.sourceDateTimestamp | Integer | 採用的 process_capacity 生效時間；未建立時回傳 0 |  |
| payload.steps[].standardPerformance.sourceCode | String | 標準績效 evidence 來源 code | process_capacity / not_recorded |
| payload.steps[].sourceLineage.stepSourceCode | String | Step evidence 來源 code | process_flow |
| payload.steps[].sourceLineage.processSourceCode | String | Process identity evidence 來源 code | process / not_recorded |
| payload.steps[].sourceLineage.standardPerformanceSourceCode | String | Standard performance evidence 來源 code | process_capacity / not_recorded |
| payload.sourceLineage.routingVersionSourceCode | String | Routing Version evidence 來源 code | product_process |
| payload.sourceLineage.stepSourceCode | String | Step evidence 來源 code | process_flow |
| payload.sourceLineage.processIdentitySourceCode | String | Process identity evidence 來源 code | process |
| payload.sourceLineage.recipeReferenceSourceCode | String | Recipe reference evidence 來源 code | product_spec |
| payload.sourceLineage.packagingContextSourceCode | String | Packaging context evidence 來源 code | product_bom_spec |
| payload.sourceLineage.resourceEligibilitySourceCode | String | Resource eligibility evidence 來源 code | not_recorded |
| payload.sourceLineage.routingVersionId | String | Routing Version 識別碼 |  |
| payload.warnings[].warningCode | String | Routing 資料條件 warning code | missing_steps / missing_item_master / missing_process_master / missing_standard_performance / missing_recipe_reference / packaging_context_not_governed / resource_eligibility_not_governed / unknown |
| payload.warnings[].refNo | String | warning 相關 Routing、品項或 reference no |  |
| payload.warnings[].stepId | String | warning 相關 stepId；非步驟層 warning 回傳空字串 |  |

### Processing Flow

1. 讀取 routing_version_id 與 effectiveDate。
2. 查詢 product_process.no = routing_version_id；不存在時回傳 record not found。
3. 查詢同一 item_no 的全部 product_process 版本，判斷目前版本狀態。
4. 查詢 process_flow.product_process_no = routing_version_id，依 process_flow.order 與 id 排序。
5. 依 process_flow.oneProcess + secProcess 對應 process，補足 processNo 與 processLabel。
6. 依 product_process.item_no + version 對應 product_spec，建立 Recipe reference。
7. 依 product_process.item_no + version 對應 product_bom_spec，建立 bounded Packaging context。
8. 依 process_capacity.oneProcess + secProcess 且 date <= effectiveDate 取得最新 standardPerformance。
9. resourceEligibility 第一版無受治理來源，固定 governed=false 並以 warning 標示。
10. 回傳 routingVersion、ordered steps、sourceLineage、capabilityBoundary 與 warnings。

### Database Tables Used

| Table | Purpose |
|----------|------|
| product_process | 提供 Routing Version evidence |
| process_flow | 提供 ordered Routing Steps |
| process | 提供 process identity 與 label evidence |
| process_capacity | 提供 governed standard-performance reference |
| product_spec | 提供已建立 Recipe reference |
| product_bom_spec | 提供 bounded Packaging context |
| product | 提供製成品主檔 |
| inproduct | 提供在製品主檔 |

## GET /api/v2/routing/products/{item_no}/current

<a id="get-api-v2-routing-products-item_no-current"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/routing/products/{item_no}/current | GET | 查詢指定製成品或在製品目前生效 Routing |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示偏好的 IANA timezone；後端仍直接回傳資料庫保存的 UTC timestamp |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| effectiveDate | Integer | NO | Routing Version 狀態判斷基準 UTC timestamp；未提供時使用系統時間 |

### Request Body

None

### Success Response Data

結構同 `GET /api/v2/routing/versions/{routing_version_id}/steps`。

### Processing Flow

1. 讀取 item_no 與 effectiveDate。
2. 查詢 product_process.item_no = item_no 的全部版本；不存在時回傳 record not found。
3. 優先選擇 effective 版本；若無 effective，選擇有 date 的最高版本，否則選擇最高版本。
4. 以選定的 routingVersionId 執行 steps API 同一組解析流程。

### Database Tables Used

| Table | Purpose |
|----------|------|
| product_process | 選擇目前 Routing Version |
| process_flow | 提供 ordered Routing Steps |
| process | 提供 process identity 與 label evidence |
| process_capacity | 提供 governed standard-performance reference |
| product_spec | 提供已建立 Recipe reference |
| product_bom_spec | 提供 bounded Packaging context |
| product | 提供製成品主檔 |
| inproduct | 提供在製品主檔 |

