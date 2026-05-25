# ERP Workforce Page Review

Date: 2026-05-25
Scope: Workforce V1 frontend UX refinement and API-readiness review.

## Review Metadata

| Field | Value |
| --- | --- |
| Review date | 2026-05-25 |
| Reviewer | Codex |
| Page / route | Workforce / `/workforce` |
| Related API endpoint | `GET /api/v1/workforce/dashboard` |
| Data source during review | `mock` with service-layer API fallback |
| Frontend commit / branch | `main` / `a8208c2 Refine workforce UX interactions` |

## Page Smoke

| Check | Result | Notes |
| --- | --- | --- |
| Page loads without fatal error | Pass | Browser smoke opened `/workforce` successfully. |
| No compile/schema error | Pass | Lint and production build completed after UX refinement. |
| Loading state is stable | Pass | Page renders mock fallback while service checks API availability. |
| API failure falls back or shows controlled empty/error state | Pass | `useWorkforceDashboard` returns mock data and exposes a warning message when API is unavailable. |
| Desktop layout has no overlap | Pass | Browser smoke found no page-level horizontal overflow. |
| Primary action is usable | Pass | Header `排班` action switches to the overtime/support view. |
| Navigation/sidebar behavior is usable | Pass | Workforce remains reachable through shared app layout. |

## Business Acceptance

| Check | Result | Notes |
| --- | --- | --- |
| Page supports the agreed V1 management concern | Pass | Shows shift coverage, skill gaps, overtime/support and certification risks. |
| Highest-priority risk is visible without drilling down | Pass | KPI strip and risk cards expose staff shortage and certification concerns. |
| Status tones are understandable | Pass | Uses shared `StatusBadge` tones for risk and requirement gaps. |
| Main cards/tables use practical labels | Pass | Table surfaces area/shift, plan/work order, staffing, skills, overtime/support, certification, risk and owner. |
| Empty or missing data does not mislead the user | Pass with notes | Search-filtered empty states now show controlled messages; API-empty partial datasets still fall back to mock per current service policy. |
| User can identify next action or owner where relevant | Pass | Detail panel exposes headcount, support need, risk reason and requirement breakdown. |

## UX Refinement Completed

| Item | Result |
| --- | --- |
| Search behavior | Header search now filters workforce cases by area, department, shift, plan, work order, skill, certification, owner and risk. |
| Detail synchronization | If the selected workforce case does not match the current view/search, the detail panel derives the first matching case. |
| Scheduling entry | Header action now switches to `加班/支援`, making it a clear view navigation action. |
| Placeholder action clarity | Advanced filter remains a V1 placeholder with tooltip guidance until API filter fields are confirmed. |
| Empty state | Search-filtered empty results show controlled messages instead of blank panels. |

## Decision

Decision:

```txt
accepted_with_notes
```

Reason:

The Workforce page is suitable for V1 API validation as a labor readiness workspace. It preserves the agreed boundary: visibility for coverage, skill and certification risk, not shift mutation.

## Follow-Up Items

| Owner | Item | Priority | Due / trigger |
| --- | --- | --- | --- |
| Backend engineer | Confirm whether employee, skill and certification tables exist. | High | Before implementing `/api/v1/workforce/dashboard` |
| Backend engineer | Confirm planned staff by line/date source fields. | High | During Workforce API implementation |
| Backend engineer | Confirm staff-gap calculation rule against Planning and Production. | High | During Workforce API implementation |
| Frontend | Revisit empty-array fallback policy after real API returns controlled empty datasets. | Medium | After first Workforce API runtime report |
| Frontend | Move stable Workforce static labels into `src/i18n/dictionary.ts`. | Medium | After Workforce API mapping stabilizes |
