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
| `GET /api/v2/trace/batches/{batch_no}/overview` | PASS | Uses `work_order_no` as the V1 production step scope, keeps focused input/output batches, and stops downstream expansion after finished-goods output. |

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
| Trace production output | Production steps retain direct output rows by `work_order_no`, keep focused input/output batches, and avoid unrelated downstream finished-goods expansion. |

## 2026-08-27 Traceability V3 Retest Fix

After engineer runtime feedback, the traceability overview algorithm was rechecked and strengthened:

- Production rows are now loaded by `work_order_no`. `process_order_no` and `group` are retained as data fields but are not used as V1 grouping filters because their relationships are not yet complete.
- Finished-goods overview keeps the queried finished-goods batch in `outputItems[]`.
- Production output item category is resolved from `production_data_output.batch_number -> batch_number.itemCategory` first, then falls back to `EOutputCategory`, so old or inconsistent output category values do not drop finished-goods outputs or keep expanding them as non-finished items.
- Raw-material downstream tracing only enqueues output rows confirmed as `EItemCategory.INPRODUCT`. Finished goods, unknown outputs and other non-inproduct outputs are returned only in the current step, preventing downstream finished-goods branches from expanding.
- Added regression tests for work-order scoped counterpart rows and stopping downstream expansion after finished-goods output.

## 2026-08-28 Traceability Program Correction

After engineer review of `traceability_center_proposal.md` 「程式修正」:

- `/api/v2/trace/batches/{batch_no}/overview` now uses `work_order_no` as the V1 production step scope.
- `process_order_no` and `group` remain source fields but are not used for V1 production step grouping or input/output filtering because their relationships are not yet complete.
- Production step comments were added in `trace.py` to make this limitation explicit for future maintenance.
- Proposal, flow algorithm and formal API documents were updated to match the implementation.

Verification:

```powershell
.\.venv\Scripts\python.exe -m py_compile restserver\package\restserver\api\v2\trace.py
.\.venv\Scripts\python.exe -m pytest restserver\tests
```

Result: PASS, 57 tests passed in 6.09s.

## 2026-08-29 Traceability Program Correction V2

After engineer review of `traceability_center_proposal.md` 「程式修正V2」:

- `traceSteps[].inputItems[].quantity` now uses net input quantity: `production_data_input.action=1` issue quantity minus `action=2` return quantity.
- Duplicate production step hits now merge focus input/output items into the existing step instead of skipping the later relationship.
- Existing output items are deduplicated by `itemNo + batchNo + itemCategory + unit`, so shared output batches are not counted twice when multiple input batches point to the same output.
- Proposal, flow algorithm and formal API documents were updated to match the implementation.

Verification:

```powershell
.\.venv\Scripts\python.exe -m py_compile restserver\package\restserver\api\v2\trace.py
.\.venv\Scripts\python.exe -m pytest restserver\tests
```

Result: PASS, 59 tests passed in 2.93s.

## 2026-08-31 Traceability Program Correction V3 and TransItems Correction

After engineer review of `traceability_center_proposal.md` 「程式修正V3」 and `transaction_item_master_proposal.md` 「程式修正」:

- `traceSteps[].inputItems[].quantity` continues to use net input quantity, and input items with net quantity `0` are now excluded from `inputItems[]`.
- When a zero-net input batch is the current trace focus, the production step is not created and its outputs are not enqueued for further trace expansion.
- Finished-goods upstream tracing no longer follows input batches whose net input quantity is `0`.
- `/api/v2/transitems/dashboard` no longer returns the combined `summary.dataQualityIssueCount`.
- `/api/v2/transitems/dashboard` now returns `summary.companyDataQualityIssueCount` and `summary.transItemDataQualityIssueCount` as independent counts.
- `start` / `count` are clarified as applying only to `transactionItems[]`; `companies[]` remains the company summary for the filtered transaction item set.
- Proposal, flow algorithm and formal API documents were updated to match the implementation.

Verification:

```powershell
.\.venv\Scripts\python.exe -m py_compile restserver\package\restserver\api\v2\trace.py restserver\package\restserver\api\v2\transitems.py
.\.venv\Scripts\python.exe -m pytest restserver\tests
```

Result: PASS, 61 tests passed in 3.91s.

## Remaining External Verification

- Engineer should run the same API endpoints against MariaDB with current EWDB data to confirm real-data distribution and runtime behavior.
- No database schema migration is required for this implementation.
