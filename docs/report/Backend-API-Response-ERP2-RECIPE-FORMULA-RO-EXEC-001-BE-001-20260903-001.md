# Backend API Response - ERP2-RECIPE-FORMULA-RO-EXEC-001-BE-001

## 1. 交付摘要

| Item | Result |
|---|---|
| Work Item | ERP2-RECIPE-FORMULA-RO-EXEC-001-BE-001 |
| Authority | ERP2-CIO-RECIPE-FORMULA-RO-EXEC-001 |
| Scope | Recipe / Formula read-only API |
| Result | PASS |
| Commit Type | Backend implementation + Formal API document + Tests |
| Date | 2026-09-03 |

本次依 CTO assignment 完成 Recipe Formula read-only 後端 API。第一版將 Formula 視為 Recipe Version 的組成視圖，資料來源以既有 `bom`、`bom_item`、`product_spec` 與品項主檔為 evidence，不新增寫入行為。

## 2. 實作 API

| Method | URL | Purpose | Result |
|---|---|---|---|
| GET | `/api/v2/recipe-formula/dashboard` | 查詢 Recipe / Formula 版本摘要與狀態清單 | PASS |
| GET | `/api/v2/recipe-formula/{recipe_no}/versions` | 查詢指定 Recipe 的版本清單 | PASS |
| GET | `/api/v2/recipe-formula/{recipe_no}/versions/{version}/composition` | 查詢指定 Recipe Version 的 Formula composition | PASS |
| GET | `/api/v2/recipe-formula/by-product/{product_no}` | 依製成品查詢相關 Recipe / Formula 版本 | PASS |

## 3. 主要程式與文件

| Path | Purpose |
|---|---|
| `restserver/package/restserver/api/v2/recipe_formula.py` | Recipe Formula API service 與 endpoint executor |
| `restserver/package/restserver/api/v2/recipe_formula_uri.py` | Recipe Formula API route binding |
| `restserver/package/restserver/app.py` | 註冊 Recipe Formula v2 blueprint |
| `restserver/package/common/common.py` | 新增 Recipe Formula enum code |
| `restserver/tests/test_recipe_formula_api.py` | Recipe Formula pytest cases |
| `docs/spec/api/recipe_formula.md` | 正式 API 文件 |
| `docs/spec/api/index.md` | API 文件索引 |

## 4. 資料來源與語意邊界

| Domain | Source | Note |
|---|---|---|
| Recipe definition | `bom.no`, `bom.displayName` | 第一版以 BOM 作為 Recipe definition evidence |
| Recipe Version | `bom.version`, `bom.date` | 依同一 Recipe 的所有版本判斷 effective / historical / future / unknown |
| Formula inputs | `bom_item` | input-specific weight 來源為 `bom_item.weight` |
| Formula output | `product_spec.bom_no + bom_version` | 正規化 product_no 後作為 exactly one defined output candidate |
| Item master | `material`, `inproduct`, `goods`, `product` | 補充品名、類別與子分類 |
| Loss | not recorded | 目前無受治理 loss 欄位，回傳 `lossSourceCode=not_recorded` 與 warning code |

## 5. Capability Boundary

API 固定回傳以下邊界，用來避免誤解為寫入或成本權威：

| Field | Value |
|---|---|
| `recipeWriteSupported` | false |
| `bomWriteSupported` | false |
| `productWriteSupported` | false |
| `productStructureSeparated` | true |
| `routingReferenceOnly` | true |
| `productionObservationSeparated` | true |
| `costingExcluded` | true |

## 6. 測試結果

| Test | Command | Result |
|---|---|---|
| Recipe Formula unit tests | `.venv\Scripts\python.exe -m pytest restserver\tests\test_recipe_formula_api.py -q` | 4 passed |
| Full backend tests | `.venv\Scripts\python.exe -m pytest restserver\tests -q` | 86 passed |

## 7. Shared DEV HTTP Smoke

以 non-production validation token 進行實際 HTTP smoke，未列印實際配方編號、產品編號或其他資料值。

| Endpoint | HTTP | API Code | Result |
|---|---:|---:|---|
| GET `/api/v2/recipe-formula/dashboard?count=1` | 200 | 0 | PASS |
| GET `/api/v2/recipe-formula/{recipe_no}/versions` | 200 | 0 | PASS |
| GET `/api/v2/recipe-formula/{recipe_no}/versions/{version}/composition` | 200 | 0 | PASS |
| GET `/api/v2/recipe-formula/by-product/{product_no}` | 200 | 0 | PASS |
| POST `/api/v2/recipe-formula/dashboard` | 405 | N/A | PASS, read-only negative control |

## 8. 注意事項

1. 本次 API 僅提供 read-only 查詢，不提供 Recipe、BOM、Product、Routing、Production Observation 或 Costing 寫入。
2. `lossRate` 第一版因資料庫未提供受治理來源，固定以 `lossSourceCode=not_recorded` 與 `missing_loss_source` warning 表示。
3. 若未來工程師確認 loss 欄位來源，需同步更新 API 文件、後端流程與測試案例。
4. 本次未新增資料表，因此未產生 database migration SQL。

