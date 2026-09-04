# Packaging Specification Read-Only Flow / Algorithm

狀態：Implemented / Pending Runtime Review
對應 API 提案：`docs/spec/api-proposal/packaging_specification_proposal.md`
Runtime Source：`restserver/package/restserver/api/v2/packaging_specification.py`

## Step 1：解析 Request

輸入：

```txt
itemNo
itemCategory
productVersion
effectiveDate
x-timezone
```

規則：

1. `itemNo` 不可為空。
2. `itemCategory` 僅允許 `EItemCategory.INPRODUCT = 4` 或 `EItemCategory.PRODUCT = 5`。
3. `productVersion` 未提供時，Product 使用 `product.version`；WIP 使用 `product_spec.product_version`。
4. `effectiveDate` 第一版僅保留，不做版本生效日篩選。

## Step 2：確認查詢主體

| itemCategory | Table | Source code |
| --- | --- | --- |
| 4 | `inproduct` | `inproduct` |
| 5 | `product` | `product` |

處理：

1. Product 查詢 `product.no = itemNo`。
2. WIP 查詢 `inproduct.no = itemNo`。
3. 主體不存在時回傳 HTTP 404 / `record not found`。
4. 不跨表推測主體。

## Step 3：Product 包裝規格查詢

Product 查詢來源：

```txt
product_bom_spec.product_no = itemNo
product_bom_spec.product_version = productVersion（若有）
```

排序：

```txt
product_version desc, level asc, id asc
```

取得欄位：

1. `level` -> `packagingLevel`
2. `bom2_no` -> `packagingBomNo`
3. `count` -> `count`
4. `unit` -> `unit`
5. `weight` -> `weight`

## Step 4：WIP 包裝 context 查詢

WIP 不具備現有包裝規格權威表。

第一版處理：

```txt
product_spec.item_no = WIP itemNo
```

找出下游 Product 後，再查詢該 Product 的 `product_bom_spec`。此情境必須加入：

```txt
warningCode = wip_packaging_context_from_downstream_product
statusCode = partial
```

不得將下游 Product 包裝資料視為 WIP 自身權威來源。

## Step 5：包裝 BOM 主檔與明細

包裝 BOM 主檔：

```txt
bom2_number.no = product_bom_spec.bom2_no
```

包裝 BOM 明細：

```txt
bom2.parent_no = product_bom_spec.bom2_no
```

若缺少 `bom2_number`，該 spec 的 `masterSourceCode = not_recorded`。

若缺少 `bom2` 明細，該 spec 的 `lineSourceCode = not_recorded`。

## Step 6：彙總

計算：

1. `packagingSpecCount`
2. `packagingBomCount`
3. `packageLevelCount`
4. `materialLineCount`
5. `totalCount`
6. `totalWeight`

數字規則：

1. 數量/重量取小數點第 2 位。
2. 金額欄位本 API 第一版不回傳。

## Step 7：Status / Warning

狀態判斷：

| Status | Condition |
| --- | --- |
| `complete` | 有包裝規格，且主檔與明細來源完整，無 warning。 |
| `partial` | 有包裝規格，但 WIP context、主檔/明細缺漏或其他 warning 存在。 |
| `unavailable` | 無包裝規格。 |
| `error` | 查詢過程出現可隔離錯誤。 |

Warning codes：

1. `missing_packaging_spec`
2. `missing_packaging_bom_master`
3. `missing_packaging_bom_lines`
4. `wip_packaging_context_from_downstream_product`
5. `module_unavailable`

## Step 8：Read-Only Boundary

本 endpoint 僅註冊 GET。

```txt
POST /api/v2/packaging-specification/overview -> HTTP 405
PUT /api/v2/packaging-specification/overview -> HTTP 405
PATCH /api/v2/packaging-specification/overview -> HTTP 405
DELETE /api/v2/packaging-specification/overview -> HTTP 405
```

`capabilityBoundary` 固定：

```txt
readOnly = true
packagingWriteSupported = false
packagingApprovalSupported = false
packagingReleaseSupported = false
sourceOfTruthTransitionSupported = false
cutoverSupported = false
goLiveSupported = false
```
