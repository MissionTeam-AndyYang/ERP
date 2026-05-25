# ERP Purchasing Page Review

Date: 2026-05-25
Scope: Purchasing V1 frontend UX refinement and API-readiness review.

## Review Metadata

| Field | Value |
| --- | --- |
| Review date | 2026-05-25 |
| Reviewer | Codex |
| Page / route | Purchasing / `/purchasing` |
| Related API endpoint | `GET /api/v1/purchasing/dashboard` |
| Data source during review | `mock` with service-layer API fallback |
| Frontend commit / branch | `main` / `96afae2 Refine purchasing UX interactions` |

## Page Smoke

| Check | Result | Notes |
| --- | --- | --- |
| Page loads without fatal error | Pass | Browser smoke opened `/purchasing` successfully. |
| No console error from schema mismatch | Pass | Browser console error log was empty during smoke. |
| Loading state is stable | Pass | Page renders mock fallback while service checks API availability. |
| API failure falls back or shows controlled empty/error state | Pass | `usePurchasingDashboard` returns mock data and exposes a warning message when API is unavailable. |
| Desktop layout has no overlap | Pass | Desktop smoke found no page-level horizontal overflow. |
| Mobile layout has no overlap | Pass | 390px viewport smoke found no page-level horizontal overflow. |
| Navigation/sidebar behavior is usable | Pass | Purchasing remains reachable through shared app layout. |

## Business Acceptance

| Check | Result | Notes |
| --- | --- | --- |
| Page supports the agreed V1 management concern | Pass | Shows supplier quotes, contracts, purchase orders, receiving and price variance signals. |
| Highest-priority risk is visible without drilling down | Pass | KPI strip, tab views and detail panel expose late arrival, contract and price-risk concerns. |
| Status tones are understandable | Pass | Uses shared `StatusBadge` tones for purchasing state, risk and document readiness. |
| Main cards/tables use practical labels | Pass | Table surfaces supplier, material, expected arrival, receiving progress, risk and owner. |
| Empty or missing data does not mislead the user | Pass with notes | Search-filtered empty states now show controlled messages; API-empty partial datasets still fall back to mock per current service policy. |
| User can identify next action or owner where relevant | Pass | Detail panel exposes owner, quote/contract/PO linkage and receiving status. |

## UX Refinement Completed

| Item | Result |
| --- | --- |
| Search behavior | Header search now filters purchasing records by PO, supplier, material, quote/contract references, owner, status and risk. |
| Detail synchronization | If the selected purchasing record does not match the search, the detail panel derives the first matching row. |
| Receiving entry | Header action now switches to the receiving view instead of implying an unimplemented mutation. |
| Placeholder action clarity | Advanced filter remains a V1 placeholder with tooltip guidance until API filter fields are confirmed. |
| Empty state | Search-filtered empty results show controlled messages instead of blank panels. |

## Decision

Decision:

```txt
accepted_with_notes
```

Reason:

The Purchasing page is suitable for V1 API validation as a procurement visibility workspace. It preserves the agreed boundary: readiness, supplier status and receiving risk visibility, not purchase-order mutation.

## Follow-Up Items

| Owner | Item | Priority | Due / trigger |
| --- | --- | --- | --- |
| Backend engineer | Confirm whether quotations and contracts can be filtered to supplier-side records. | High | Before implementing `/api/v1/purchasing/dashboard` |
| Backend engineer | Confirm planned purchase request versus purchase order source fields. | High | During Purchasing API implementation |
| Backend engineer | Confirm receiving status and late-arrival status values. | High | During Purchasing API implementation |
| Frontend | Revisit empty-array fallback policy after real API returns controlled empty datasets. | Medium | After first Purchasing API runtime report |
| Frontend | Move stable Purchasing static labels into `src/i18n/dictionary.ts`. | Medium | After Purchasing API mapping stabilizes |
