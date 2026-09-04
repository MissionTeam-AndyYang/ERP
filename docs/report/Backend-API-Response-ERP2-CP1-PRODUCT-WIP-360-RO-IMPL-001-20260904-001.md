# Backend API Response: ERP2-CP1-PRODUCT-WIP-360-RO-IMPL-001

## Implementation Summary

已依 CTO Office / CIO bounded non-production read-only authorization 實作 Product / WIP 360 overview BFF API。

新增 endpoint：

```txt
GET /api/v2/product-wip-360/overview
```

本次實作僅進行 read-only composition：

1. 以 `itemNo + itemCategory` 查詢 Product/WIP 主體。
2. 組合既有 Item、Transaction Item、Warehouse、BOM、Recipe、Routing read-only 能力。
3. 回傳 `moduleReadiness[]`、`sourceLineage`、`warnings[]` 與 `capabilityBoundary`。
4. 保留 CP1 邊界：不新增 Product/WIP write、不修改 DB schema、不進行 Production、migration、Source-of-Truth transition、Cutover 或 Go-Live。

## Changed Files

| File | Purpose |
| --- | --- |
| `restserver/package/restserver/api/v2/product_wip_360.py` | Product / WIP 360 read-only BFF service and executor。 |
| `restserver/package/restserver/api/v2/product_wip_360_uri.py` | v2 Flask blueprint 與 GET route。 |
| `restserver/package/restserver/app.py` | 註冊 `product_wip_360_v2` blueprint。 |
| `restserver/tests/test_product_wip_360_api.py` | Backend evidence pytest。 |
| `docs/spec/api/product_wip_360.md` | 正式 API 文件。 |
| `docs/spec/api/index.md` | 新增 Product / WIP 360 API 索引。 |
| `docs/spec/api-proposal/product_wip_360_overview_proposal.md` | 更新狀態與 implementation boundary。 |
| `docs/spec/api-proposal/product_wip_360_overview_flow_algorithm.md` | 更新狀態與 implementation boundary。 |

## Backend Evidence Coverage

| Evidence | Status | Test Coverage |
| --- | --- | --- |
| Product complete | PASS | `test_product_complete_overview_uses_confirmed_module_contracts` |
| Product partial | PASS | `test_warning_propagation_from_child_modules` |
| Standalone WIP partial | PASS | `test_standalone_wip_partial_returns_missing_module_signals` |
| Not found | PASS | `test_not_found_returns_none` |
| Invalid category | PASS | `test_invalid_category_returns_controlled_response` |
| Module unavailable | PASS | `test_module_unavailable_is_reported` |
| Routing test-support | PASS | `test_routing_test_support_status_and_source_lineage_are_preserved` |
| Source-lineage | PASS | `test_product_complete_overview_uses_confirmed_module_contracts`、`test_routing_test_support_status_and_source_lineage_are_preserved` |
| Warning propagation | PASS | `test_warning_propagation_from_child_modules` |
| Read-only negative control | PASS | `test_read_only_negative_control_rejects_post` |

## Verification

已執行：

```txt
.\.venv\Scripts\python.exe -m pytest restserver\tests\test_product_wip_360_api.py
```

結果：

```txt
9 passed
```

已執行相關 v2 module regression：

```txt
.\.venv\Scripts\python.exe -m pytest restserver\tests\test_product_wip_360_api.py restserver\tests\test_items_v2_api.py restserver\tests\test_bom_center_api.py restserver\tests\test_recipe_formula_api.py restserver\tests\test_routing_process_flow_api.py restserver\tests\test_warehouse_dashboard.py
```

結果：

```txt
50 passed
```

## Known Boundaries

1. 本 API 為 CP1 read-only BFF composition，不建立新資料權威來源。
2. WIP root 的 BOM / Recipe governance 若尚未由正式 domain API 支援，回傳 partial/unavailable warning，不反向推測下游 Product。
3. Warehouse 庫存資料沿用 `CWarehouseInventoryService.get_inventory()` 的既有計算與零庫存過濾規則。
4. 子模組錯誤會被隔離為該模組 `statusCode=error` 與 `module_unavailable` warning，不中斷整包 overview response。
5. POST/PUT/PATCH/DELETE 未註冊於此 endpoint。
