# Traceability Trace Steps Aggregation Test Report

## Scope

- Updated `/api/v2/trace/batches/{batch_no}/overview` trace step item handling.
- `traceSteps[].inputItems[]` and `traceSteps[].outputItems[]` now aggregate duplicated rows by `itemNo + batchNo + itemCategory + unit`.
- Material items (`itemCategory=2`) are excluded from `traceSteps` item lists for the current version.
- Existing film exclusion remains unchanged.

## Files Verified

- `restserver/package/restserver/api/v2/trace.py`
- `restserver/tests/test_traceability_api.py`
- `docs/spec/api/trace.md`
- `docs/spec/api-proposal/traceability_center_proposal.md`

## Test Commands

```powershell
.\.venv\Scripts\python.exe -m pytest restserver\tests\test_traceability_api.py
.\.venv\Scripts\python.exe -m pytest restserver\tests
```

## Result

| Test Scope | Result |
|---|---|
| Traceability API tests | 5 passed |
| Full restserver tests | 41 passed |

## Notes

- The test data includes duplicated production input/output rows for the same batch and verifies they are returned as one aggregated item.
- The test data includes a material input row and verifies it is not returned in `traceSteps[].inputItems[]`.
