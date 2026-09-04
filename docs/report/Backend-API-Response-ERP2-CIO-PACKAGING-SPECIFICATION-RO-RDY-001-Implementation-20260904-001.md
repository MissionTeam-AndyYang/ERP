# Backend API Response: ERP2-CIO-PACKAGING-SPECIFICATION-RO-RDY-001

## Implementation Summary

已完成 Packaging Specification Read-Only API contract、bounded backend implementation、unit/regression tests，以及 Shared DEV runtime retest evidence。

新增 endpoint：

```txt
GET /api/v2/packaging-specification/overview
```

本次實作僅提供唯讀 visibility：

1. Product 情境直接以 `product_bom_spec` 查詢包裝規格。
2. WIP 情境以 `product_spec.item_no = WIP itemNo` 找到下游 Product，回傳其包裝 context，並以 warning 標示此資料不是 WIP 自身包裝規格權威。
3. 以 `bom2_number` 補包裝 BOM 主檔名稱、單位與重量。
4. 以 `bom2` 補包裝 BOM 明細。
5. 回傳 `sourceLineage`、`warnings[]`、`moduleReadiness[]` 與 `capabilityBoundary`。

## Evidence Discovery

| Source | Interpretation |
| --- | --- |
| `docs/spec/database/index.md` | `product_bom_spec` 為「製成品規格_物料」，其中 `level` 表示包裝階層，`bom2_no` 對應 `bom2_number.no`。 |
| `restserver/package/dbwrapper/table.py` | 已有 `CTableProductBOMSpec`、`CTableBOM2Number`、`CTableBOM2`、`CTableProductSpec` ORM class，不需要新增 schema。 |
| `restserver/package/restserver/api/v2/routing.py` | Routing 已使用 `product_bom_spec` 建立 bounded packaging context，證明此來源可作為包裝可視化 evidence。 |

## Changed Files

| File | Purpose |
| --- | --- |
| `restserver/package/restserver/api/v2/packaging_specification.py` | Packaging Specification read-only service and executor。 |
| `restserver/package/restserver/api/v2/packaging_specification_uri.py` | v2 Flask blueprint 與 GET route。 |
| `restserver/package/restserver/app.py` | 註冊 `packaging_specification_v2` blueprint。 |
| `restserver/tests/test_packaging_specification_api.py` | Product/WIP/error/read-only pytest。 |
| `docs/spec/api-proposal/packaging_specification_proposal.md` | API proposal and data contract。 |
| `docs/spec/api-proposal/packaging_specification_flow_algorithm.md` | Backend flow / algorithm。 |
| `docs/spec/api/packaging_specification.md` | 正式 API 文件。 |
| `docs/spec/api/index.md` | 新增 Packaging Specification API 索引。 |
| `scripts/verify_packaging_specification_shared_dev.py` | Shared DEV DB-backed runtime retest script。 |
| `docs/report/Backend-API-Response-ERP2-CIO-PACKAGING-SPECIFICATION-RO-RDY-001-Shared-DEV-Retest-20260904-001.md` | Shared DEV runtime retest report。 |

## Test Results

已執行：

```txt
.\.venv\Scripts\python.exe -m pytest restserver\tests\test_packaging_specification_api.py
```

結果：

```txt
7 passed
```

已執行相關 regression：

```txt
.\.venv\Scripts\python.exe -m pytest restserver\tests\test_packaging_specification_api.py restserver\tests\test_product_wip_360_api.py restserver\tests\test_bom_center_api.py restserver\tests\test_routing_process_flow_api.py
```

結果：

```txt
29 passed
```

## Shared DEV Runtime Retest

Shared DEV wrapper retest 已完成。

| Item | Value |
| --- | --- |
| Report | `docs/report/Backend-API-Response-ERP2-CIO-PACKAGING-SPECIFICATION-RO-RDY-001-Shared-DEV-Retest-20260904-001.md` |
| SHA-256 | `5FF4F21FFB378AEECB4A5AE982E5064B0D64D709B9691FFDDFDD64D062FE12A5` |
| Classification | PASS WITH FIXTURE LIMITATION |

Observed limitation：

Shared DEV Product subject 可查詢，但目前包裝資料表/support surface 尚未完整對齊正式 implementation path；Product 情境回傳 `module_unavailable`，WIP 情境回傳 `missing_packaging_spec`。API 本身正確隔離子模組不可用狀態，未中斷整體 response。

## Local Full-Stack DEV Backend Requirements

`LOCAL DATABASE -> REAL LOCAL BACKEND -> REAL LOCAL READ API` 需要：

1. MariaDB 11.x 或相容版本。
2. 匯入與 `restserver/package/dbwrapper/table.py` 相符的 EWDB schema。
3. 至少包含下列表與測試資料：
   - `product`
   - `inproduct`
   - `product_spec`
   - `product_bom_spec`
   - `bom2_number`
   - `bom2`
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

建議 smoke path：

```txt
GET /api/v2/packaging-specification/overview?itemNo=<product_no>&itemCategory=5
GET /api/v2/packaging-specification/overview?itemNo=<wip_no>&itemCategory=4
POST /api/v2/packaging-specification/overview  -> should return HTTP 405
```

## Boundary Confirmation

No Packaging write.

No Packaging approval / release.

No material schema change.

No Production credential, data, endpoint, or deployment.

No migration, Source-of-Truth transition, Engineering Pull, Cutover, or ERP2.0 Go-Live.
