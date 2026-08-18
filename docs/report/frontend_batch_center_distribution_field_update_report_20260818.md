# Frontend Batch Center Distribution Field Update Report - 2026-08-18

## Scope
- `BatchCenterScreen`
- `BatchDistributionView`
- `BatchDetailPanel`

## Changes
- Confirmed `/api/v2/batches/dashboard` frontend mapping supports `items[].unit`.
- Confirmed `/api/v2/batches/items/{item_no}/distribution` frontend mapping supports:
  - `batches[].daysInStock`
  - `batches[].expiryStatusCode`
- Added `存放` and `期限` columns to the batch distribution list.
- Added `存放天數` and `期限狀態` to the selected batch detail summary.
- Added Traditional Chinese enum display for `expiryStatusCode`:
  - `valid` -> `效期品`
  - `near_expiry` -> `即期品`
  - `expired` -> `過期品`
  - `unknown` -> `待確認`
- Updated mock preview data to include the new dashboard unit and distribution expiry/storage fields.
- Removed production-in-progress stage labels from the batch distribution enum display because the adjusted distribution API now returns warehouse stock distribution only.

## Verification
- `npm run lint`: Passed.
- `npm run build`: Passed.
- Local route smoke test:
  - `/batches`: HTTP 200.
- Static code scan confirmed the UI includes:
  - `存放`
  - `期限`
  - `存放天數`
  - `期限狀態`
  - `daysInStock`
  - `expiryStatusCode`

## Notes
- This change is frontend-only.
- Existing API/Mock behavior remains unchanged: API mode shows real empty/error states and does not automatically fall back to mock data.
