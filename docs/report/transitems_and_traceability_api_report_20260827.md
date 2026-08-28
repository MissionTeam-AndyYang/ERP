# Transitems and Traceability API Verification Report 2026-08-27

## Scope

- Rechecked `traceability_center_proposal.md` 演算法修正V3 and updated `/api/v2/trace/batches/{batch_no}/overview`.
- Implemented confirmed Transaction Item Master backend APIs from `transaction_item_master_proposal.md`.
- Updated formal API documentation and planned screen API references.

## Implemented APIs

| API | Status | Notes |
| --- | --- | --- |
| `GET /api/v2/transitems/dashboard` | PASS | Returns company summary, transaction item list, contract linkage, payment summary and data quality codes. |
| `GET /api/v2/transitems/companies/{company_no}/detail` | PASS | Returns company detail, payment terms, related transaction items and contracts. |
| `GET /api/v2/transitems/transitems/{transaction_item_no}/detail` | PASS | Returns transaction item detail, linked internal item, contract data and quality status. |
| `GET /api/v2/trace/batches/{batch_no}/overview` | PASS | Keeps direct production output items when input/output `process_order_no` or `group` is blank, inconsistent or padded with spaces; stops downstream expansion after finished-goods output. |

## Verification

Command:

```powershell
.\.venv\Scripts\python.exe -m py_compile restserver\package\restserver\api\v2\trace.py restserver\package\restserver\api\v2\transitems.py restserver\package\restserver\api\v2\transitems_uri.py restserver\package\restserver\app.py
```

Result: PASS

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest restserver\tests\test_traceability_api.py restserver\tests\test_transitems_v2_api.py
```

Result: PASS, 17 tests passed in 0.95s.

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest restserver\tests
```

Result: PASS, 57 tests passed in 2.64s.

## Field Logic Review

| Area | Result |
| --- | --- |
| Transaction item keyword search | Includes company, transaction item, linked item and contract number search. |
| Transaction item summary | `customerCount` and `supplierCount` are derived from contract category instead of a shared generic contract count. |
| Linked internal item category | Material categories are returned from `material.category`; inproduct, product and goods keep their own source category mapping. |
| Payment code | Backend returns enum-like `paymentTypeCode`; display text remains frontend/i18n responsibility. |
| Trace production output | Production steps retain direct output rows, normalize `process_order_no/group` scope comparison, and avoid unrelated downstream finished-goods expansion. |

## 2026-08-27 Traceability V3 Retest Fix

After engineer runtime feedback, the traceability overview algorithm was rechecked and strengthened:

- Work-scope rows are now loaded by `work_order_no` and filtered in code with normalized `process_order_no` and `group`, preventing single-side blanks or surrounding spaces from dropping valid counterpart rows.
- Finished-goods overview keeps the queried finished-goods batch in `outputItems[]`.
- Production output item category is resolved from `production_data_output.batch_number -> batch_number.itemCategory` first, then falls back to `EOutputCategory`, so old or inconsistent output category values do not drop finished-goods outputs or keep expanding them as non-finished items.
- Raw-material downstream tracing only enqueues output rows confirmed as `EItemCategory.INPRODUCT`. Finished goods, unknown outputs and other non-inproduct outputs are returned only in the current step, preventing unrelated steps such as another downstream `group_2` production from appearing.
- Added regression tests for normalized group matching and stopping downstream expansion after finished-goods output.

## Remaining External Verification

- Engineer should run the same API endpoints against MariaDB with current EWDB data to confirm real-data distribution and runtime behavior.
- No database schema migration is required for this implementation.
