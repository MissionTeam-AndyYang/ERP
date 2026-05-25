# ERP Settings Page Review

Date: 2026-05-25
Scope: Settings / Master Data V1 frontend UX refinement and API-readiness review.

## Review Metadata

| Field | Value |
| --- | --- |
| Review date | 2026-05-25 |
| Reviewer | Codex |
| Page / route | Settings / `/settings` |
| Related API endpoint | `GET /api/v1/settings/dashboard` |
| Data source during review | `mock` with service-layer API fallback |
| Frontend commit / branch | `main` / `d643656 Refine settings UX interactions` |

## Page Smoke

| Check | Result | Notes |
| --- | --- | --- |
| Page loads without fatal error | Pass | Browser smoke opened `/settings` successfully. |
| No compile/schema error | Pass | Lint and production build completed after UX refinement. |
| Loading state is stable | Pass | Page renders mock fallback while service checks API availability. |
| API failure falls back or shows controlled empty/error state | Pass | `useSettingsDashboard` returns mock data and exposes a warning message when API is unavailable. |
| Desktop layout has no overlap | Pass | Browser smoke found no page-level horizontal overflow. |
| Primary action is usable | Pass | Header `設定` action switches to the integrations view. |
| Navigation/sidebar behavior is usable | Pass | Settings remains reachable through shared app layout. |

## Business Acceptance

| Check | Result | Notes |
| --- | --- | --- |
| Page supports the agreed V1 management concern | Pass | Shows master-data health, role/permission governance, integration readiness and localization coverage. |
| Highest-priority risk is visible without drilling down | Pass | KPI strip, table risk badges and detail panel expose governance risks. |
| Status tones are understandable | Pass | Uses shared `StatusBadge` tones for item status and governance risk. |
| Main cards/tables use practical labels | Pass | Table surfaces master-data item, domain, status, affected workspace, risk, owner and update date. |
| Empty or missing data does not mislead the user | Pass with notes | Search-filtered empty states now show controlled messages; API-empty partial datasets still fall back to mock per current service policy. |
| User can identify next action or owner where relevant | Pass | Detail panel exposes owner, status, risk reason and affected workspaces. |

## UX Refinement Completed

| Item | Result |
| --- | --- |
| Search behavior | Header search now filters settings items by id, name, domain, status, risk, owner, update date and affected workspaces. |
| Detail synchronization | If the selected setting does not match the current view/search, the detail panel derives the first matching item. |
| Settings entry | Header action now switches to `系統串接`, making it a clear view navigation action. |
| Placeholder action clarity | Advanced filter remains a V1 placeholder with tooltip guidance until API filter fields are confirmed. |
| Empty state | Search-filtered empty results show controlled messages instead of blank panels. |

## Decision

Decision:

```txt
accepted_with_notes
```

Reason:

The Settings page is suitable for V1 API validation as a read-only governance workspace. It preserves the agreed boundary: master-data, permission, integration and localization visibility, not configuration mutation.

## Follow-Up Items

| Owner | Item | Priority | Due / trigger |
| --- | --- | --- | --- |
| Backend engineer | Confirm whether roles and permissions are already stored. | High | Before implementing `/api/v1/settings/dashboard` |
| Backend engineer | Confirm whether login returns role/module permission data. | High | During Settings API implementation |
| Backend engineer | Confirm localization coverage source. | High | During Settings API implementation |
| Backend engineer | Confirm mandatory master-data domains for V1 integration. | High | During Settings API implementation |
| Frontend | Revisit empty-array fallback policy after real API returns controlled empty datasets. | Medium | After first Settings API runtime report |
| Frontend | Move stable Settings static labels into `src/i18n/dictionary.ts`. | Medium | After Settings API mapping stabilizes |
