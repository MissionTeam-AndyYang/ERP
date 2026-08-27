# Traceability Overview Scope and Algorithm Fix Report 20260825

## Scope

- API: `GET /api/v2/trace/batches/{batch_no}/overview`
- Issue 1: overview response time reported at about 1.8 seconds in engineer runtime environment.
- Issue 2: `traceSteps[]` returned unrelated input items or sibling output items when querying a finished goods or raw material batch number.
- Issue 3: WIP batch numbers are not planned as V1 overview query roots, but the prior traversal still attempted to expand them.
- Issue 4: `traceSteps[].outputItems[]` could become empty when input/output rows belonged to the same `work_order_no + group` but one side had an empty or mismatched `process_order_no`.

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
6. Overview now determines traversal direction from the root batch item category:
   - raw material root: downstream path-focused traversal
   - finished goods root: upstream path-focused traversal
   - WIP root: no V1 expansion, empty `traceSteps[]`
7. Production steps now filter the focused side of each step:
   - upstream traversal keeps only the currently traced output batch in `outputItems[]`
   - downstream traversal keeps only the currently traced input batch in `inputItems[]`
8. Added regression tests for sibling output filtering, unrelated downstream input filtering, and WIP root non-expansion.
9. Added counterpart fallback query: strict `work_order_no + process_order_no + group` remains the first lookup, but if one side is empty and `group` is available, the service retries the missing side with `work_order_no + group`.
10. Added batch number normalization before focus filtering to avoid whitespace differences dropping legitimate rows.
11. Confirmed `receipt`, `production`, and future `sale` steps remain in `traceSteps[]`; no separate receipt/sale arrays are introduced for V1.

## Verification

Command:

```powershell
python -m pytest restserver\tests\test_traceability_api.py
```

Result:

```text
11 passed in 1.87s
```

## Notes

- Local verification uses SQLite in-memory test data, so it confirms algorithm correctness but does not replace engineer MariaDB runtime performance verification.
- For MariaDB performance, suggested indexes remain:
  - `production_data_input(batch_number, work_order_no, process_order_no, group)`
  - `production_data_output(batch_number, work_order_no, process_order_no, group)`
  - `production_data_input(work_order_no, process_order_no, group)`
  - `production_data_output(work_order_no, process_order_no, group)`
