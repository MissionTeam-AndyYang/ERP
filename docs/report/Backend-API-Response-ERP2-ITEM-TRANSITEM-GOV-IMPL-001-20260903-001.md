# ERP2-BE-ITEM-TRANSITEM-GOV-IMPL-001 Backend/API 驗證報告

## 1. 驗證範圍

本報告記錄 `ERP2-BE-ITEM-TRANSITEM-GOV-IMPL-001` bounded non-production Backend/API 實作驗證結果。

### 已納入端點

| Endpoint | Method | 結果 |
|---|---|---|
| `/api/v2/items/dashboard` | GET | 已優化候選品項、庫存摘要與 BOM 摘要查詢流程 |
| `/api/v2/items/{item_no}/detail` | GET | 已優化單一品項主檔查詢與 BOM usage 批次查詢 |
| `/api/v2/transitems/dashboard` | GET | 已將交易品項分頁與 hasContract 篩選前移至資料庫查詢階段 |
| `/api/v2/transitems/companies/{company_no}/detail` | GET | 已納入回歸測試，未變更 API contract |
| `/api/v2/transitems/transitems/{transaction_item_no}/detail` | GET | 已納入回歸測試，未變更 API contract |
| `/api/v2/trace/dashboard` | GET | 已依目前僅查原料與製成品的畫面需求，將 records enrichment 限縮至分頁批號 |

### 刻意延後事項

| 項目 | 說明 |
|---|---|
| Production deployment | 未執行 |
| Production data load | 未執行 |
| Migration execution | 未執行 |
| Source-of-Truth transition | 未執行 |
| Engineering Pull | 未執行 |
| Cutover / Go-Live | 未執行 |

## 2. Data Source / ORM / Table Alignment

| API Family | ORM / Table |
|---|---|
| Item Center | `material`、`inproduct`、`product`、`goods`、`batch_number`、`bom`、`bom_item`、`product_spec`、`product_bom_spec`、`inproduct_bom_spec` |
| Warehouse item inventory signal | `inventory_record`、`warehouse_inventory_reservation`、`warehouse_quality_hold` |
| Transaction Item Master | `trans_items`、`company`、`payment`、`contract`、`material`、`inproduct`、`product`、`goods` |
| Trace Dashboard | `batch_number`、`inventory_record`、`production_data_input`、`production_data_output`、`warehouse_quality_hold`、`workflow_task_event` |

## 3. Adapter / Repository Boundary Evidence

| 區域 | 處理方式 |
|---|---|
| Item Center | 以 service 內部 read-only query helper 收斂主檔查詢、單一品項查詢、BOM 批次查詢與候選品項限定 |
| Warehouse inventory summary | `CWarehouseInventoryContextBuilder.query_item_inventory_summary()` 新增候選品項清單參數，作為 Item Center 與 Warehouse 庫存訊號之間的 read-only boundary |
| Transaction Item Master | 以 service 內部 query builder 集中建立 `trans_items` 篩選條件，並將分頁與 `hasContract` 篩選交由 ORM 查詢處理 |

## 4. ORM / SQL Decision

本次採用 **B：ORM-first with controlled imperative SQL escape hatch**。

本次未新增 imperative SQL。現有 SQLAlchemy ORM 足以處理篩選、分頁、count、批次查詢與輕量 summary refs。若未來進入高資料量壓測，才建議針對 confirmed hot path 以受控 SQL escape hatch 補強。

## 5. Pagination / Count / Query-Count Treatment

| 風險 | 處理 |
|---|---|
| broad item read before filtering | `keyword`、`itemCategory`、`itemSubCategory` 先於品項主檔查詢階段套用 |
| full item set before detail lookup | detail 改為依 `item_no` 查詢單一主檔，不先建立全品項集合 |
| BOM N+1 | `bomUsage[]` 以 BOM no 清單批次查詢 `bom` |
| `trans_items` `.all()` then Python pagination | dashboard 改為 ORM `count()` + `offset()` + `limit()` |
| `hasContract` Python filtering | 改為資料庫查詢階段以 `contract.item_no` 限定 |
| trace dashboard records enrichment | `records[]` 只 enrich 本次分頁批號；summary 使用輕量訊號計算 |

## 6. Tests Run

### Command

```powershell
..\.venv\Scripts\python.exe -m pytest tests
```

### Result

```text
80 passed in 3.79s
```

## 7. Shared DEV Readiness

| 項目 | 結果 |
|---|---|
| Backend unit / component tests | PASS |
| API formal docs alignment | PASS，已更新 `docs/spec/api/item.md`、`docs/spec/api/transitems.md`、`docs/spec/api/trace.md` |
| API contract expansion | 無 |
| DB schema mutation | 無 |
| Production impact | 無 |

結論：可進入 Shared DEV 工程師 review。

## 8. Controlled TEST Recommendation

建議在工程師 review 後，於有資料庫環境執行 controlled TEST：

1. 以實際資料量測 `/api/v2/items/dashboard`、`/api/v2/items/{item_no}/detail`、`/api/v2/transitems/dashboard`、`/api/v2/trace/dashboard` 回應時間。
2. 驗證 `itemType` 未出現在 `/api/v2/items/dashboard` 與 `/api/v2/items/{item_no}/detail`。
3. 驗證 `transitems.dashboard` 的 `total/start/count` 與 `transactionItems[]` 分頁一致。
4. 驗證 `trace.dashboard` 仍僅回傳原料與製成品，且 records 分頁資料完整。

## 9. Safe Stop / CIO Re-entry Conditions

若後續需要以下任一事項，需重新取得 CTO / CIO 處理：

- Production deployment
- Production data load
- migration execution
- source-of-truth transition
- Engineering Pull
- Cutover / Go-Live
- material API contract expansion
- 新增或變更正式資料庫 schema
