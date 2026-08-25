# Traceability Overview Scope and Performance Fix Report 20260825

## Scope

- API: `GET /api/v2/trace/batches/{batch_no}/overview`
- Issue 1: overview response time reported at about 1.8 seconds in engineer runtime environment.
- Issue 2: `traceSteps[]` returned unrelated input items when querying finished goods batch numbers.

## Changes

1. Production step scope now uses `work_order_no + process_order_no + group`.
2. Overview no longer builds a production step by loading every input/output row under the same `work_order_no`.
3. Added per-request cache for:
   - batch header lookup
   - production input rows by batch
   - production output rows by batch
   - production input rows by work scope
   - production output rows by work scope
   - production data by work order
4. Removed unused work-order-only helper functions to avoid future confusion.
5. Added regression test for unrelated work-order group data.

## Verification

Command:

```powershell
python -m pytest restserver\tests\test_traceability_api.py
```

Result:

```text
6 passed in 0.69s
```

## Notes

- Local verification uses SQLite in-memory test data, so it confirms algorithm correctness but does not replace engineer MariaDB runtime performance verification.
- For MariaDB performance, suggested indexes remain:
  - `production_data_input(batch_number, work_order_no, process_order_no, group)`
  - `production_data_output(batch_number, work_order_no, process_order_no, group)`
  - `production_data_input(work_order_no, process_order_no, group)`
  - `production_data_output(work_order_no, process_order_no, group)`
