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
| `GET /api/v2/trace/batches/{batch_no}/overview` | PASS | Keeps direct production output items when input/output `process_order_no` is blank or inconsistent on one side. |

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

Result: PASS, 53 tests passed in 2.43s.

## Field Logic Review

| Area | Result |
| --- | --- |
| Transaction item keyword search | Includes company, transaction item, linked item and contract number search. |
| Transaction item summary | `customerCount` and `supplierCount` are derived from contract category instead of a shared generic contract count. |
| Linked internal item category | Material categories are returned from `material.category`; inproduct, product and goods keep their own source category mapping. |
| Payment code | Backend returns enum-like `paymentTypeCode`; display text remains frontend/i18n responsibility. |
| Trace production output | Production steps retain direct output rows and avoid unrelated work-order group expansion. |

## Remaining External Verification

- Engineer should run the same API endpoints against MariaDB with current EWDB data to confirm real-data distribution and runtime behavior.
- No database schema migration is required for this implementation.
