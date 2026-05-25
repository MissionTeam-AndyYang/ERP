# ERP Finance Page Review

Date: 2026-05-25
Scope: Finance V1 frontend UX refinement and API-readiness review.

## Review Metadata

| Field | Value |
| --- | --- |
| Review date | 2026-05-25 |
| Reviewer | Codex |
| Page / route | Finance / `/finance` |
| Related API endpoint | `GET /api/v1/finance/dashboard` |
| Data source during review | `mock` with service-layer API fallback |
| Frontend commit / branch | `main` / `1dbd0b7 Refine finance UX interactions` |

## Page Smoke

| Check | Result | Notes |
| --- | --- | --- |
| Page loads without fatal error | Pass | Browser smoke opened `/finance` successfully. |
| No compile/schema error | Pass | Lint and production build completed after UX refinement. |
| Loading state is stable | Pass | Page renders mock fallback while service checks API availability. |
| API failure falls back or shows controlled empty/error state | Pass | `useFinanceDashboard` returns mock data and exposes a warning message when API is unavailable. |
| Desktop layout has no overlap | Pass | Browser smoke found no page-level horizontal overflow. |
| Primary action is usable | Pass | Header `請款` action switches to the receivables view. |
| Navigation/sidebar behavior is usable | Pass | Finance remains reachable through shared app layout. |

## Business Acceptance

| Check | Result | Notes |
| --- | --- | --- |
| Page supports the agreed V1 management concern | Pass | Shows estimated/actual margin, cost variance, billing readiness, AR/AP impact and order-level finance trace. |
| Highest-priority risk is visible without drilling down | Pass | KPI strip and margin-risk cards expose low-margin and blocked-billing concerns. |
| Status tones are understandable | Pass | Uses shared `StatusBadge` tones for finance risk, POD and document state. |
| Main cards/tables use practical labels | Pass | Table surfaces financial case/order, customer/product, amount, margin, cost, billing/collection, POD, risk and owner. |
| Empty or missing data does not mislead the user | Pass with notes | Search-filtered empty states now show controlled messages; API-empty partial datasets still fall back to mock per current service policy. |
| User can identify next action or owner where relevant | Pass | Detail panel exposes billing documents, workflow, AR state and cost impact by area. |

## UX Refinement Completed

| Item | Result |
| --- | --- |
| Search behavior | Header search now filters finance cases by case/order, shipment, customer, product, invoice, AR/POD status, owner and risk. |
| Detail synchronization | If the selected finance case does not match the current view/search, the detail panel derives the first matching case. |
| Billing entry | Header action now switches to `應收/請款`, making it a clear view navigation action. |
| Placeholder action clarity | Advanced filter remains a V1 placeholder with tooltip guidance until API filter fields are confirmed. |
| Empty state | Search-filtered empty results show controlled messages instead of blank panels. |

## Decision

Decision:

```txt
accepted_with_notes
```

Reason:

The Finance page is suitable for V1 API validation as a finance visibility workspace. It preserves the agreed boundary: margin, billing readiness and AR/AP traceability, not invoice or payment mutation.

## Follow-Up Items

| Owner | Item | Priority | Due / trigger |
| --- | --- | --- | --- |
| Backend engineer | Confirm AR/AP source of truth. | High | Before implementing `/api/v1/finance/dashboard` |
| Backend engineer | Confirm whether actual order-level cost can be calculated today. | High | During Finance API implementation |
| Backend engineer | Confirm POD and document requirements for billing-ready. | High | During Finance API implementation |
| Backend engineer | Confirm available cost components: material, labor, overhead and logistics. | High | During Finance API implementation |
| Frontend | Revisit empty-array fallback policy after real API returns controlled empty datasets. | Medium | After first Finance API runtime report |
| Frontend | Move stable Finance static labels into `src/i18n/dictionary.ts`. | Medium | After Finance API mapping stabilizes |
