# Batch Center API Update Test Report 2026-08-18

## Scope

- `GET /api/v2/batches/dashboard`
  - Added `items[].unit`.
- `GET /api/v2/batches/items/{item_no}/distribution`
  - Adjusted response to warehouse stock distribution rows.
  - Added `batches[].daysInStock`.
  - Added `batches[].expiryStatusCode`.

## Verification

| Check | Command | Result |
|---|---|---|
| Batch Center pytest | `.\\.venv\\Scripts\\pytest.exe restserver\\tests\\test_batch_center_api.py -q` | Passed: 4 tests |
| Frontend lint | `npm.cmd run lint` | Passed |

## Notes

- `expiryStatusCode` uses enum values `valid`, `near_expiry`, `expired`, `unknown`.
- `daysInStock` is calculated from first inbound timestamp to query timestamp.
- Distribution API now returns warehouse inventory rows only; production-in-progress distribution is not returned by this API.
