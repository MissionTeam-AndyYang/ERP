# ERP Planning Page Review

Date: 2026-05-25
Scope: Planning / APS V1 frontend UX refinement and API-readiness review.

## Review Metadata

| Field | Value |
| --- | --- |
| Review date | 2026-05-25 |
| Reviewer | Codex |
| Page / route | Planning / `/planning` |
| Related API endpoint | `GET /api/v1/planning/dashboard` |
| Data source during review | `mock` with service-layer API fallback |
| Frontend commit / branch | `main` / `121f030 Refine planning UX interactions` |

## Page Smoke

| Check | Result | Notes |
| --- | --- | --- |
| Page loads without fatal error | Pass | Browser smoke opened `/planning` successfully. |
| No console error from schema mismatch | Pass | Browser console error log was empty during smoke. |
| Loading state is stable | Pass | Page renders mock fallback while service checks API availability. |
| API failure falls back or shows controlled empty/error state | Pass | `usePlanningDashboard` returns mock data and exposes a warning message when API is unavailable. |
| Desktop layout has no overlap | Pass | Desktop smoke found no page-level horizontal overflow. |
| Mobile layout has no overlap | Pass | 390px viewport smoke found no page-level horizontal overflow. |
| Navigation/sidebar behavior is usable | Pass | Planning remains reachable through shared app layout. |

## Business Acceptance

| Check | Result | Notes |
| --- | --- | --- |
| Page supports the agreed V1 management concern | Pass | Converts promised orders into demand expansion, material/PR suggestions, capacity/staff checks and work-order suggestions. |
| Highest-priority risk is visible without drilling down | Pass | KPI strip and material/capacity views expose shortage and capacity conflicts. |
| Status tones are understandable | Pass | Uses shared `StatusBadge` tones for planning decision, materials, capacity and suggested work-order states. |
| Main cards/tables use practical labels | Pass | Table surfaces order, due date, planning decision, shortage value, capacity, PR/work-order counts and owner. |
| Empty or missing data does not mislead the user | Pass with notes | Search-filtered empty states now show controlled messages; API-empty partial datasets still fall back to mock per current service policy. |
| User can identify next action or owner where relevant | Pass | Detail panel exposes checks, suggested work orders, owner and priority. |

## UX Refinement Completed

| Item | Result |
| --- | --- |
| Search behavior | Header search now filters planning cases, material cards and capacity cards by order, plan, product, line, material, status and notes. |
| Detail synchronization | If the current selected case does not match the search, the detail panel derives the first matching planning case. |
| Work-order entry | Header action now switches to `工單建議` instead of implying an unimplemented scheduling mutation. |
| Placeholder action clarity | Advanced filter remains a V1 placeholder with tooltip guidance until API filter fields are confirmed. |
| Empty state | Search-filtered empty results show controlled messages instead of blank panels. |

## Decision

Decision:

```txt
accepted_with_notes
```

Reason:

The Planning page is suitable for V1 API validation as a Production Control planning workspace. It preserves the agreed boundary: visibility and suggestions, not automatic purchase request or work-order creation.

## Follow-Up Items

| Owner | Item | Priority | Due / trigger |
| --- | --- | --- | --- |
| Backend engineer | Confirm source order and promised-date fields. | High | Before implementing `/api/v1/planning/dashboard` |
| Backend engineer | Confirm BOM explosion, inventory availability and quality-release blocker sources. | High | During Planning API implementation |
| Backend engineer | Confirm capacity, changeover and staff source fields. | High | During Planning API implementation |
| Frontend | Revisit empty-array fallback policy after real API returns controlled empty datasets. | Medium | After first Planning API runtime report |
| Frontend | Move stable Planning static labels into `src/i18n/dictionary.ts`. | Medium | After Planning API mapping stabilizes |
