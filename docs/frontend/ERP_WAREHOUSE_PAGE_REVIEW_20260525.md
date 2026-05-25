# ERP Warehouse Page Review

Date: 2026-05-25
Scope: Warehouse V1 frontend UX refinement and API-readiness review.

## Review Metadata

| Field | Value |
| --- | --- |
| Review date | 2026-05-25 |
| Reviewer | Codex |
| Page / route | Warehouse / `/warehouse` |
| Related API endpoint | `GET /api/v1/warehouse/dashboard` |
| Data source during review | `mock` with service-layer API fallback |
| Frontend commit / branch | `main` / `4d86005 Refine warehouse UX interactions` |

## Page Smoke

| Check | Result | Notes |
| --- | --- | --- |
| Page loads without fatal error | Pass | Browser smoke opened `/warehouse` successfully. |
| No console error from schema mismatch | Pass | Browser console error log was empty during smoke. |
| Loading state is stable | Pass | Page renders mock fallback while service checks API availability. |
| API failure falls back or shows controlled empty/error state | Pass | `useWarehouseDashboard` returns mock data and exposes a warning message when API is unavailable. |
| Desktop layout has no overlap | Pass | Desktop smoke found no page-level horizontal overflow. |
| Mobile layout has no overlap | Pass | 390px viewport smoke found no page-level horizontal overflow. |
| Navigation/sidebar behavior is usable | Pass | Warehouse remains reachable through shared app layout. |

## Business Acceptance

| Check | Result | Notes |
| --- | --- | --- |
| Page supports the agreed V1 management concern | Pass | Covers inventory value, warehouse capacity, risk alerts, pending work and inventory detail. |
| Highest-priority risk is visible without drilling down | Pass | KPI strip and risk tab expose stale, expiry and safety-stock risk. |
| Status tones are understandable | Pass | Uses shared `StatusBadge` tones for info, success, warning and danger. |
| Main cards/tables use practical labels | Pass | Pending task quantity label was corrected to `任務數量` to avoid implying on-hand/reserved/available stock. |
| Empty or missing data does not mislead the user | Pass with notes | Search-filtered empty states now show controlled messages; API-empty partial datasets still fall back to mock per current service policy. |
| User can identify next action or owner where relevant | Pass | Pending tasks include task type, source document, owner, due time and status. |

## API Integration Review

| Check | Result | Notes |
| --- | --- | --- |
| Endpoint path matches service file | Pass | `src/services/warehouse-api.ts` calls `/api/v1/warehouse/dashboard`. |
| Top-level datasets are consumed correctly | Pass with notes | Frontend consumes `kpis`, `categorySummaries`, `capacities`, `records`, `risks` and `tasks`; backend spec currently names source datasets differently. |
| Partial response uses fallback only where intended | Pass with notes | Empty arrays currently fall back to mock arrays. This is useful for design preview but should be revisited once backend returns true empty states. |
| Dates, numbers and units display correctly | Pass | Numbers use `Intl.NumberFormat("zh-TW")`; units are carried by each record/task. |
| API and mock data have compatible shape | Pass for current frontend shape | Backend aggregate must normalize into the frontend shape or the frontend service must map backend dataset names. |

## I18N Readiness

| Check | Result | Notes |
| --- | --- | --- |
| User-facing labels are easy to extract later | Pass with notes | Page strings are localized in one page file, but not yet moved into `src/i18n/dictionary.ts`. |
| Hard-coded business statuses are documented or typed | Pass with notes | Category, task type, risk type and workflow status are typed in `src/types/warehouse.ts`. |
| Long Chinese labels do not break layout | Pass | Desktop and 390px mobile smoke found no page-level overflow. |
| Future English/Japanese labels would fit with current layout | Pass with notes | Tab buttons wrap; table columns use local horizontal scroll. Re-check after i18n extraction. |

## UX Refinement Completed

| Item | Result |
| --- | --- |
| Search behavior | Header search now filters risk cards, pending tasks and inventory detail rows by batch, item, warehouse, source document, owner and status fields. |
| Trace entry | `追溯` switches to the inventory-detail view so the selected batch workflow and related documents are visible. |
| Placeholder action clarity | Advanced filter remains a V1 placeholder with tooltip guidance until API filter fields are confirmed. |
| Empty state | Search-filtered empty results show controlled messages instead of blank panels. |
| Task wording | Pending-task table now labels task quantity as `任務數量`. |

## Decision

Decision:

```txt
accepted_with_notes
```

Reason:

The Warehouse page is suitable as the first frontend baseline for backend API validation. The layout and interactions support the confirmed V1 management questions without expanding scope into operator CRUD. Remaining notes are API mapping and i18n extraction items, not blockers for Warehouse read-only integration.

## Follow-Up Items

| Owner | Item | Priority | Due / trigger |
| --- | --- | --- | --- |
| Backend engineer | Confirm Warehouse aggregate response shape and whether backend will return frontend-shaped datasets or source datasets from the API spec. | High | Before implementing `/api/v1/warehouse/dashboard` |
| Backend engineer | Confirm pallet/location capacity source, reserved quantity rules, quality-hold quantity and safety-stock source. | High | During Warehouse API implementation |
| Frontend | Revisit empty-array fallback policy after real API returns controlled empty datasets. | Medium | After first Warehouse API runtime report |
| Frontend | Move stable Warehouse static labels into `src/i18n/dictionary.ts`. | Medium | After Warehouse API mapping stabilizes |
| Product/user | Decide whether `篩選` should open a drawer, inline filter row or saved-view control in V1.5. | Low | After backend exposes filterable fields |
