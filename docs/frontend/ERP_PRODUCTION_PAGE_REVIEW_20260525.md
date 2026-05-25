# ERP Production Page Review

Date: 2026-05-25
Scope: Production V1 frontend UX refinement and API-readiness review.

## Review Metadata

| Field | Value |
| --- | --- |
| Review date | 2026-05-25 |
| Reviewer | Codex |
| Page / route | Production / `/production` |
| Related API endpoint | `GET /api/v1/production/dashboard` |
| Data source during review | `mock` with service-layer API fallback |
| Frontend commit / branch | `main` / `d430869 Refine production UX interactions` |

## Page Smoke

| Check | Result | Notes |
| --- | --- | --- |
| Page loads without fatal error | Pass | Browser smoke opened `/production` successfully. |
| No console error from schema mismatch | Pass | Browser console error log was empty during smoke. |
| Loading state is stable | Pass | Page renders mock fallback while service checks API availability. |
| API failure falls back or shows controlled empty/error state | Pass | `useProductionDashboard` returns mock data and exposes a warning message when API is unavailable. |
| Desktop layout has no overlap | Pass | Desktop smoke found no page-level horizontal overflow. |
| Mobile layout has no overlap | Pass | 390px viewport smoke found no page-level horizontal overflow. |
| Navigation/sidebar behavior is usable | Pass | Production remains reachable through shared app layout. |

## Business Acceptance

| Check | Result | Notes |
| --- | --- | --- |
| Page supports the agreed V1 management concern | Pass | Covers weekly schedule/capacity, MES work-order status, efficiency, loss, labor cost and quality signals. |
| Highest-priority risk is visible without drilling down | Pass | KPI strip and alert cards expose material/staff risk, QC pending/abnormal and capacity bottlenecks. |
| Status tones are understandable | Pass | Uses shared `StatusBadge` tones for schedule, material, staff, quality and delivery risk states. |
| Main cards/tables use practical labels | Pass | Table and detail panel expose production date/line/process, progress, material/staff, MES, delivery risk and QC status. |
| Empty or missing data does not mislead the user | Pass with notes | Search-filtered empty states now show controlled messages; API-empty partial datasets still fall back to mock per current service policy. |
| User can identify next action or owner where relevant | Pass with notes | Work orders include owner, material/staff status, QC block flags and related workflow. Backend should later provide owner/owner module consistently. |

## API Integration Review

| Check | Result | Notes |
| --- | --- | --- |
| Endpoint path matches service file | Pass | `src/services/production-api.ts` calls `/api/v1/production/dashboard`. |
| Top-level datasets are consumed correctly | Pass with notes | Frontend consumes `summary`, `orders`, `weekSchedule` and `alerts`; backend spec currently defines source datasets such as `scheduleByLine`, `todayWorkOrders`, `mesSignals`, `efficiencyMetrics`, `qualitySignals` and `bottlenecks`. |
| Partial response uses fallback only where intended | Pass with notes | Empty arrays currently fall back to mock arrays. Revisit after real API returns true empty states. |
| Dates, numbers and units display correctly | Pass | Numbers, money and quantities are formatted in UI; units are carried by each work order/material. |
| API and mock data have compatible shape | Pass for current frontend shape | Backend aggregate must normalize into the frontend shape or frontend service must map source datasets. |

## I18N Readiness

| Check | Result | Notes |
| --- | --- | --- |
| User-facing labels are easy to extract later | Pass with notes | Page strings are localized in one page file, but not yet moved into `src/i18n/dictionary.ts`. |
| Hard-coded business statuses are documented or typed | Pass with notes | Work-order stage, material, staff, quality and process statuses are typed in `src/types/production.ts`. |
| Long Chinese labels do not break layout | Pass | Desktop and 390px mobile smoke found no page-level overflow. |
| Future English/Japanese labels would fit with current layout | Pass with notes | Tab buttons wrap; wide tables use local horizontal scroll. Re-check after i18n extraction. |

## UX Refinement Completed

| Item | Result |
| --- | --- |
| Search behavior | Header search now filters weekly schedule slots, MES/detail table rows and analytics cards by date, line, work order, product, batch, status and quality fields. |
| Detail synchronization | If the current selected work order does not match the search, the detail panel derives the first matching work order instead of showing unrelated details. |
| Schedule entry | `排程` switches back to the weekly schedule/capacity view. |
| Placeholder action clarity | Advanced filter remains a V1 placeholder with tooltip guidance until API filter fields are confirmed. |
| Empty state | Search-filtered empty results show controlled messages instead of blank panels. |

## Decision

Decision:

```txt
accepted_with_notes
```

Reason:

The Production page is suitable for V1 API validation as a management-oriented production planning and MES dashboard. It preserves the agreed scope: schedule/capacity, material/staff readiness, MES status, efficiency/loss/labor-cost signals and quality blockers. Remaining notes are API mapping, source confirmation and i18n extraction items, not blockers for read-only integration.

## Follow-Up Items

| Owner | Item | Priority | Due / trigger |
| --- | --- | --- | --- |
| Backend engineer | Confirm current MES status source endpoint and field mapping. | High | Before implementing `/api/v1/production/dashboard` |
| Backend engineer | Confirm whether workorder includes scheduled date, line, process and status. | High | During Production API implementation |
| Backend engineer | Confirm actual production quantity, material loss and unit labor cost calculation sources. | High | During Production API implementation |
| Backend engineer | Confirm production quality signal source, including QC block flags for inventory/shipping. | High | Before connecting Quality blockers |
| Frontend | Revisit empty-array fallback policy after real API returns controlled empty datasets. | Medium | After first Production API runtime report |
| Frontend | Move stable Production static labels into `src/i18n/dictionary.ts`. | Medium | After Production API mapping stabilizes |
