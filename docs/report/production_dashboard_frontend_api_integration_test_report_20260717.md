# Production Dashboard Frontend API Integration Test Report

Date: 2026-07-17

## Scope

This report covers the frontend integration for:

- `ProductionWorkspaceScreen`
- `ProductionWorkOrderDetailPanel`
- `GET /api/v2/production/dashboard`
- `GET /api/v2/production/work-orders/{work_order_no}/detail`

## Implementation Summary

- Updated `src/services/production-api.ts` to call the confirmed v2 Production APIs.
- Added dashboard payload normalization for `summary`, `scheduleByLine`, `todayWorkOrders`, `readinessSignals`, `productionMetrics`, and `alerts`.
- Added selected work order detail loading for the right-side detail panel.
- Added controlled fallback behavior when dashboard or detail API is unavailable.
- Added `src/i18n/production-enums.ts` so Production enum display strings are handled in the frontend with multilingual support.
- Updated `docs/spec/api-proposal/planned_screen_list_naming.md` with the Production screen, view, panel, and state names.

## API Contract Verification

| API | Frontend Usage | Result |
| --- | --- | --- |
| `GET /api/v2/production/dashboard?period=7d&start=0&count=50` | Loads Production dashboard data for the main screen. | Implemented |
| `GET /api/v2/production/work-orders/{work_order_no}/detail` | Loads selected work order detail for the right-side panel. | Implemented |

## Enum / I18N Verification

Production enum conversion is handled on the frontend for:

- Work order status
- Material status
- Staff status
- Machine status
- Quality status
- Delivery risk
- Capacity status
- Changeover status
- Alert type
- Unit
- Department
- Workflow step labels

Supported language dictionaries:

- `zh-TW`
- `en`
- `ja`
- `vi`

## Fallback Behavior

| Scenario | Expected Behavior | Result |
| --- | --- | --- |
| Dashboard API unavailable | Use `productionDashboardMock` and show API fallback warning. | Implemented |
| Detail API unavailable | Keep selected dashboard row data and show detail fallback warning in panel. | Implemented |
| Empty arrays from API | Use existing mock data for first-version screen continuity. | Implemented |

## Verification Results

| Check | Result | Notes |
| --- | --- | --- |
| `npm.cmd run lint` | Passed | PowerShell `npm.ps1` is blocked by local execution policy, so `npm.cmd` was used. |
| `npm.cmd run build` | Passed | Next.js production build and TypeScript check completed successfully. |
| HTTP smoke test: `GET http://127.0.0.1:3010/production` | Passed | Response status `200`; response content included the production route/page payload. |
| Browser automation smoke test | Not executed | Playwright is not installed in this frontend project, and the Codex Node kernel browser attempt was blocked by local filesystem permission. |

## Verification Commands

Commands executed:

```powershell
npm.cmd run lint
npm.cmd run build
Invoke-WebRequest -Uri http://127.0.0.1:3010/production -UseBasicParsing -TimeoutSec 20
```

Browser smoke test should verify:

- `/production` renders without runtime error.
- The page calls `GET /api/v2/production/dashboard`.
- Selecting a work order calls `GET /api/v2/production/work-orders/{work_order_no}/detail`.
- The right-side detail panel remains readable when detail fallback is used.

## Notes

The first version remains read-only. It does not create work orders, adjust schedules, write MES data, create quality records, or generate inventory/shipping documents.
