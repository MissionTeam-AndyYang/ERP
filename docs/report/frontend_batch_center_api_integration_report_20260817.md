# Frontend Batch Center API Integration Report - 2026-08-17

## Scope
- `BatchCenterScreen`
- `BatchItemSummaryView`
- `BatchDistributionView`
- `BatchDetailPanel`

## Implementation Summary
- Added frontend API integration for:
  - `GET /api/v2/batches/dashboard`
  - `GET /api/v2/batches/items/{item_no}/distribution`
  - `GET /api/v2/batches/{batch_no}/detail`
- Added API/Mock data source toggle.
- API mode now shows real empty/error states and does not fall back to mock data automatically.
- Converted backend enum/code fields to Traditional Chinese display strings in the frontend.
- Removed the previous development-stage batch center copy such as `API data`, `Mock fallback`, `read-only`, and quarantine wording.
- Updated `planned_screen_list_naming.md` to mark Batch Center frontend integration as completed and pending integration testing.

## Verification
- `npm run lint`: Passed.
- `npm run build`: Passed.
- Local route smoke test:
  - `/batches`: HTTP 200.
  - Confirmed old development strings are not present in rendered page content:
    - `API data`
    - `Mock fallback`
    - `Batches API 尚未可用`
    - `隔離量`
    - `read-only`
    - `Item Batch Summary`
    - `Batch Distribution`

## Notes
- The page language is implemented as Traditional Chinese for this phase.
- Backend API contract was treated as engineer-confirmed; no backend code was changed in this work.
