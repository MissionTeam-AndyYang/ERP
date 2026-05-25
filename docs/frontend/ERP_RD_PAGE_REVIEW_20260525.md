# ERP R&D Page Review

Date: 2026-05-25
Scope: R&D / Costing V1 frontend UX refinement and API-readiness review.

## Review Metadata

| Field | Value |
| --- | --- |
| Review date | 2026-05-25 |
| Reviewer | Codex |
| Page / route | R&D / `/rd` |
| Related API endpoint | `GET /api/v1/rd/dashboard` |
| Data source during review | `mock` with service-layer API fallback |
| Frontend commit / branch | `main` / `435dee3 Refine R&D UX interactions` |

## Page Smoke

| Check | Result | Notes |
| --- | --- | --- |
| Page loads without fatal error | Pass | Browser smoke opened `/rd` successfully. |
| No compile/schema error | Pass | Lint and production build completed after UX refinement. |
| Loading state is stable | Pass | Page renders mock fallback while service checks API availability. |
| API failure falls back or shows controlled empty/error state | Pass | `useRdDashboard` returns mock data and exposes a warning message when API is unavailable. |
| Desktop layout has no overlap | Pass | Browser smoke found no page-level horizontal overflow. |
| Primary action is usable | Pass | Header `報價` action switches to the quotation view. |
| Navigation/sidebar behavior is usable | Pass | R&D remains reachable through shared app layout. |

## Business Acceptance

| Check | Result | Notes |
| --- | --- | --- |
| Page supports the agreed V1 management concern | Pass | Shows development projects, BOM versions, costing, quotation basis and transfer readiness. |
| Highest-priority risk is visible without drilling down | Pass | KPI strip, costing cards and decision badges expose margin and BOM readiness issues. |
| Status tones are understandable | Pass | Uses shared `StatusBadge` tones for stage, decision, workflow and cost-line status. |
| Main cards/tables use practical labels | Pass | Table surfaces project/customer, product, BOM, unit cost, margin, quote, stage, decision and owner. |
| Empty or missing data does not mislead the user | Pass with notes | Search-filtered empty states now show controlled messages; API-empty partial datasets still fall back to mock per current service policy. |
| User can identify next action or owner where relevant | Pass | Detail panel exposes quote judgment, cost lines, workflow and transfer readiness. |

## UX Refinement Completed

| Item | Result |
| --- | --- |
| Search behavior | Header search now filters R&D projects by project, customer, product, channel, BOM, stage, decision, owner and risk notes. |
| Detail synchronization | If the selected project does not match the current view/search, the detail panel derives the first matching project. |
| Quotation entry | Header action now switches to `報價基礎`, making it a clear view navigation action. |
| Placeholder action clarity | Advanced filter remains a V1 placeholder with tooltip guidance until API filter fields are confirmed. |
| Empty state | Search-filtered empty results show controlled messages instead of blank panels. |

## Decision

Decision:

```txt
accepted_with_notes
```

Reason:

The R&D page is suitable for V1 API validation as a development and costing visibility workspace. It preserves the agreed boundary: costing and quotation basis review, not quote creation or BOM approval mutation.

## Follow-Up Items

| Owner | Item | Priority | Due / trigger |
| --- | --- | --- | --- |
| Backend engineer | Confirm whether development request/project records exist today. | High | Before implementing `/api/v1/rd/dashboard` |
| Backend engineer | Confirm how development BOM versions differ from approved production BOM. | High | During R&D API implementation |
| Backend engineer | Confirm nutrition label and sample status sources. | High | During R&D API implementation |
| Backend engineer | Confirm supplier quote linkage to costing cases. | High | During R&D API implementation |
| Frontend | Revisit empty-array fallback policy after real API returns controlled empty datasets. | Medium | After first R&D API runtime report |
| Frontend | Move stable R&D static labels into `src/i18n/dictionary.ts`. | Medium | After R&D API mapping stabilizes |
