# Packaging Specification Read-Only API Proposal

> Status: Implemented / Pending Runtime Review
> Work Item ID: ERP2-CIO-PACKAGING-SPECIFICATION-RO-RDY-001
> Flow / Algorithm: `docs/spec/api-proposal/packaging_specification_flow_algorithm.md`
> Runtime Source: `restserver/package/restserver/api/v2/packaging_specification.py`

## 文件邊界

本文件定義 Packaging Specification 唯讀 API。第一版僅提供可視化查詢，不提供包裝規格新增、修改、審核、發行或版控切換。

```txt
PACKAGING_SPECIFICATION_READ_ONLY != PACKAGING_WRITE
PACKAGING_SPECIFICATION_READ_ONLY != PACKAGING_APPROVAL
PACKAGING_SPECIFICATION_READ_ONLY != NEW_SOURCE_OF_TRUTH
```

## Existing Repository / Schema / Model Discovery

| Source | Finding | Usage |
| --- | --- | --- |
| `product_bom_spec` | 製成品規格_物料，含 `product_no`、`product_version`、`level`、`bom2_no`、`count`、`unit`、`weight` | Product 包裝規格主來源。 |
| `bom2_number` | 物料 BOM 編碼，含 `no`、`displayName`、`unit`、`weight`、`bom_no`、`bom_version` | 包裝 BOM 主檔與顯示名稱來源。 |
| `bom2` | 物料 BOM 階層，含子料品、數量、重量、耗損與加工數量 | 包裝 BOM 明細來源。 |
| `product_spec` | 製成品與在製品關聯 | WIP 情境用於找出下游 Product 的包裝可視化 context。 |
| `product` | 製成品主檔 | Product 查詢主體。 |
| `inproduct` | 在製品主檔 | WIP 查詢主體。 |

## Domain Contract Interpretation

1. 「包裝規格」在現有 EWDB/restserver 中主要對應 `product_bom_spec` 與 `bom2_number` / `bom2`。
2. Product 情境：以製成品為 root，回傳該製成品版本對應的包裝階層、包裝 BOM、數量、單位、重量與明細。
3. WIP 情境：現有 schema 沒有 WIP 直接擁有包裝規格的權威表；因此第一版僅透過 `product_spec.item_no = WIP itemNo` 找到下游 Product，再回傳該 Product 的包裝 context，狀態標示為 `partial`。
4. API 不以 WIP 的下游 Product 包裝規格反寫、覆蓋或建立 WIP 包裝規格權威。
5. 所有警示與狀態以 enum/code 回傳，前端負責多國語言字串轉換。

## API Summary

| URL | Method | Description | Status | Review Note |
| --- | --- | --- | --- | --- |
| `/api/v2/packaging-specification/overview` | GET | 查詢 Product/WIP 包裝規格唯讀總覽 | Implemented / Pending Runtime Review | Product 直接查 `product_bom_spec`；WIP 以 `product_spec` 查下游 Product 包裝 context 並標示 partial。 |

## Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/packaging-specification/overview` | GET | 查詢 Product/WIP 包裝規格唯讀總覽 |

## Request Header

| Header | Description |
| --- | --- |
| `x-auth-token` | 存取金鑰 |
| `x-timezone` | 時區代碼，例如 Asia/Taipei |

## Query Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `itemNo` | String | YES | 查詢主體 no；Product 對應 `product.no`，WIP 對應 `inproduct.no`。 |
| `itemCategory` | Integer | YES | 查詢主體類別；僅支援 `4` 在製品、`5` 製成品。 |
| `productVersion` | Integer | NO | Product 版本；未提供時 Product 使用 `product.version`，WIP 使用下游 `product_spec.product_version`。 |
| `effectiveDate` | Integer | NO | 保留給後續版本/生效日治理；第一版不做包裝版本生效日篩選。 |

## Success Response Data

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
    "packagingSpecs": [
      {
        "specId": "String",
        "productNo": "String",
        "productVersion": "Integer",
        "wipNo": "String",
        "packagingLevel": "Integer",
        "packagingBomNo": "String",
        "packagingBomName": "String",
        "count": "Integer",
        "unit": "Integer",
        "weight": "Float",
        "masterUnit": "Integer",
        "masterWeight": "Float",
        "linkedBomNo": "String",
        "linkedBomVersion": "Integer",
        "lineCount": "Integer",
        "lines": [
          {
            "parentBomNo": "String",
            "parentBomName": "String",
            "childCategory": "Integer",
            "childNo": "String",
            "childName": "String",
            "childUnit": "Integer",
            "count": "Integer",
            "childUnit2": "Integer",
            "weight": "Float",
            "length": "Float",
            "expectedLoss": "Float",
            "actualLoss": "Float",
            "processCount": "Float",
            "comment": "String"
          }
        ],
        "sourceCode": "String",
        "masterSourceCode": "String",
        "lineSourceCode": "String"
      }
    ],
    "sourceLineage": {
      "subjectSourceCode": "String",
      "packagingSpecSourceCode": "String",
      "packagingBomMasterSourceCode": "String",
      "packagingBomLineSourceCode": "String"
    },
    "warnings": [
      {
        "moduleCode": "String",
        "warningCode": "String",
        "refNo": "String"
      }
    ],
    "moduleReadiness": [
      {
        "moduleCode": "String",
        "statusCode": "String",
        "sourceCode": "String",
        "warningCodes": ["String"]
      }
    ],
    "capabilityBoundary": {
      "readOnly": "Boolean",
      "packagingWriteSupported": "Boolean",
      "packagingApprovalSupported": "Boolean",
      "packagingReleaseSupported": "Boolean",
      "sourceOfTruthTransitionSupported": "Boolean",
      "cutoverSupported": "Boolean",
      "goLiveSupported": "Boolean"
    }
  }
}
```

## Warning Codes

| Code | Description |
| --- | --- |
| `missing_packaging_spec` | 查詢主體或其下游 Product 找不到包裝規格。 |
| `missing_packaging_bom_master` | 包裝規格有 `bom2_no`，但缺少 `bom2_number` 主檔。 |
| `missing_packaging_bom_lines` | 包裝規格有主檔，但缺少 `bom2` 明細。 |
| `wip_packaging_context_from_downstream_product` | WIP 包裝資料來自下游 Product context，非 WIP 自身權威規格。 |
| `module_unavailable` | 包裝規格子模組查詢發生可隔離錯誤。 |

## Local Full-Stack DEV Backend Requirements

`LOCAL DATABASE -> REAL LOCAL BACKEND -> REAL LOCAL READ API` 需要：

1. MariaDB 11.x 或相容版本。
2. 匯入與 `restserver/package/dbwrapper/table.py` 相符的 EWDB schema。
3. 至少包含 `product`、`inproduct`、`product_spec`、`product_bom_spec`、`bom2_number`、`bom2` 測試資料。
4. 後端環境變數：

```txt
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=ewdb
DB_USER=<readonly_or_dev_user>
DB_PASSWORD=<password>
TOKEN_ENABLED=1
ENV=local_dev
```

建議第一條 smoke path：

```txt
GET /api/v2/packaging-specification/overview?itemNo=<product_no>&itemCategory=5
```

第二條 smoke path：

```txt
GET /api/v2/packaging-specification/overview?itemNo=<wip_no>&itemCategory=4
```
