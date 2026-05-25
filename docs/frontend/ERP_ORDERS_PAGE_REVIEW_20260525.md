# ERP Orders Page Review

Date: 2026-05-25
Scope: Orders V1 frontend UX refinement and API-readiness review.

## Review Metadata

| Field | Value |
| --- | --- |
| Review date | 2026-05-25 |
| Reviewer | Codex |
| Page / route | Orders / `/orders` |
| Related API endpoint | `GET /api/v1/orders/dashboard` |
| Data source during review | `mock` with service-layer API fallback |
| Frontend commit / branch | `main` / `8975325 Refine orders UX interactions` |

## Page Smoke

| Check | Result | Notes |
| --- | --- | --- |
| Page loads without fatal error | Pass | Browser smoke opened `/orders` successfully. |
| No console error from schema mismatch | Pass | Browser console error log was empty during smoke. |
| Loading state is stable | Pass | Page renders mock fallback while service checks API availability. |
| API failure falls back or shows controlled empty/error state | Pass | `useOrdersDashboard` returns mock data and exposes a warning message when API is unavailable. |
| Desktop layout has no overlap | Pass | Desktop smoke found no page-level horizontal overflow. |
| Mobile layout has no overlap | Pass | 390px viewport smoke found no page-level horizontal overflow. |
| Navigation/sidebar behavior is usable | Pass | Orders remains reachable through shared app layout. |

## Business Acceptance

| Check | Result | Notes |
| --- | --- | --- |
| Page supports the agreed V1 management concern | Pass | Prioritizes delivery commitment, production feasibility and fulfillment blockers before margin/payment. |
| Highest-priority risk is visible without drilling down | Pass | KPI strip and delivery-risk tab expose high-risk orders and risk reasons. |
| Status tones are understandable | Pass | Uses shared `StatusBadge` tones for delivery risk, commitment decision, stage and dependency states. |
| Main cards/tables use practical labels | Pass | Commitment date copy now distinguishes `可承諾`, `建議協調日` and `最早可行日`. |
| Empty or missing data does not mislead the user | Pass with notes | Search-filtered empty states now show controlled messages; API-empty partial datasets still fall back to mock per current service policy. |
| User can identify next action or owner where relevant | Pass with notes | Details expose dependencies and workflow. API should later include owner/owner module for commitment checks and blockers. |

## API Integration Review

| Check | Result | Notes |
| --- | --- | --- |
| Endpoint path matches service file | Pass | `src/services/orders-api.ts` calls `/api/v1/orders/dashboard`. |
| Top-level datasets are consumed correctly | Pass with notes | Frontend currently consumes `summary` and `orders`; API spec also defines `commitmentChecks`, `deliveryRisks`, `marginSignals`, `paymentSignals` and `preOrderPipeline`. |
| Partial response uses fallback only where intended | Pass with notes | Empty arrays currently fall back to mock arrays. Revisit after real API returns true empty states. |
| Dates, numbers and units display correctly | Pass | Money and quantities are formatted in UI; units are carried by each order. |
| API and mock data have compatible shape | Pass for current frontend shape | Backend aggregate must normalize into the frontend shape or frontend service must map source datasets. |

## I18N Readiness

| Check | Result | Notes |
| --- | --- | --- |
| User-facing labels are easy to extract later | Pass with notes | Page strings are localized in one page file, but not yet moved into `src/i18n/dictionary.ts`. |
| Hard-coded business statuses are documented or typed | Pass with notes | Stage, risk, commitment decision, dependency area and workflow status are typed in `src/types/orders.ts`. |
| Long Chinese labels do not break layout | Pass | Desktop and 390px mobile smoke found no page-level overflow. |
| Future English/Japanese labels would fit with current layout | Pass with notes | Tab buttons wrap; table columns use local horizontal scroll. Re-check after i18n extraction. |

## UX Refinement Completed

| Item | Result |
| --- | --- |
| Search behavior | Header search now filters orders by order, customer, channel, product, item, dates, risk, feasibility, statuses, owner and commitment fields. |
| Fulfillment entry | `履約` switches to the fulfillment view so the selected order workflow is visible. |
| Commitment wording | Non-committable orders no longer display a misleading `可承諾` date; copy now reflects coordination or earliest feasible date. |
| Placeholder action clarity | Advanced filter remains a V1 placeholder with tooltip guidance until API filter fields are confirmed. |
| Empty state | Search-filtered empty results show controlled messages instead of blank panels. |

## Decision

Decision:

```txt
accepted_with_notes
```

Reason:

The Orders page is suitable for V1 API validation as a fulfillment-risk management workspace. It preserves the agreed priority order: delivery commitment and production feasibility first, margin second, payment/collection third. Remaining notes are API mapping, pre-order pipeline expansion and i18n extraction items, not blockers for read-only integration.

## Follow-Up Items

| Owner | Item | Priority | Due / trigger |
| --- | --- | --- | --- |
| Backend engineer | Confirm formal order due date, committed date and delivery status source fields. | High | Before implementing `/api/v1/orders/dashboard` |
| Backend engineer | Confirm which current APIs can support ATP/CTP checks: finished goods ATP, material, capacity, staff, quality and shipping. | High | During Orders API implementation |
| Backend engineer | Confirm whether quotation and contract endpoints can distinguish customer-side records from supplier-side records. | Medium | Before adding pre-order pipeline UI |
| Frontend | Revisit empty-array fallback policy after real API returns controlled empty datasets. | Medium | After first Orders API runtime report |
| Frontend | Move stable Orders static labels into `src/i18n/dictionary.ts`. | Medium | After Orders API mapping stabilizes |
| Product/user | Decide whether pre-order quotation/contract should become tabs in Orders V1.5 or stay in R&D/Purchasing/Orders cross-flow. | Low | After customer quotation and contract source is confirmed |
