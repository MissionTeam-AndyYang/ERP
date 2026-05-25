# ERP Quality Page Review

Date: 2026-05-25
Scope: Quality V1 frontend UX refinement and API-readiness review.

## Review Metadata

| Field | Value |
| --- | --- |
| Review date | 2026-05-25 |
| Reviewer | Codex |
| Page / route | Quality / `/quality` |
| Related API endpoint | `GET /api/v1/quality/dashboard` |
| Data source during review | `mock` with service-layer API fallback |
| Frontend commit / branch | `main` / `a836dee Refine quality UX interactions` |

## Page Smoke

| Check | Result | Notes |
| --- | --- | --- |
| Page loads without fatal error | Pass | Browser smoke opened `/quality` successfully. |
| No console error from schema mismatch | Pass | Browser console error log was empty during smoke. |
| Loading state is stable | Pass | Page renders mock fallback while service checks API availability. |
| API failure falls back or shows controlled empty/error state | Pass | `useQualityDashboard` returns mock data and exposes a warning message when API is unavailable. |
| Desktop layout has no overlap | Pass | Desktop smoke found no page-level horizontal overflow. |
| Mobile layout has no overlap | Pass | 390px viewport smoke found no page-level horizontal overflow. |
| Navigation/sidebar behavior is usable | Pass | Quality remains reachable through shared app layout. |

## Business Acceptance

| Check | Result | Notes |
| --- | --- | --- |
| Page supports the agreed V1 management concern | Pass | Focuses on inspection queue, release/hold decisions, NCR/document risk and downstream blockers. |
| Highest-priority risk is visible without drilling down | Pass | KPI strip and release/block view expose inventory, shipment and production blockers. |
| Status tones are understandable | Pass | Uses shared `StatusBadge` tones for decisions, stages, documents and block states. |
| Main cards/tables use practical labels | Pass | Table exposes inspection, source, sample/defect, blockers, pending tests/documents and decision. |
| Empty or missing data does not mislead the user | Pass with notes | Search-filtered empty states now show controlled messages; API-empty partial datasets still fall back to mock per current service policy. |
| User can identify next action or owner where relevant | Pass | Detail panel exposes owner, due time, issue reason, documents and quality workflow. |

## API Integration Review

| Check | Result | Notes |
| --- | --- | --- |
| Endpoint path matches service file | Pass | `src/services/quality-api.ts` calls `/api/v1/quality/dashboard`. |
| Top-level datasets are consumed correctly | Pass with notes | Frontend currently consumes `summary` and `inspections`; API spec defines separate `inspectionQueue`, `releaseBlocks`, `processQualitySignals`, `finishedGoodsChecks` and `documentCompleteness`. |
| Partial response uses fallback only where intended | Pass with notes | Empty arrays currently fall back to mock arrays. Revisit after real API returns true empty states. |
| Dates, numbers and units display correctly | Pass | Samples/defects and defect rate are readable; source document and due time are carried by each record. |
| API and mock data have compatible shape | Pass for current frontend shape | Backend aggregate must normalize into the frontend shape or frontend service must map source datasets. |

## I18N Readiness

| Check | Result | Notes |
| --- | --- | --- |
| User-facing labels are easy to extract later | Pass with notes | Page strings are localized in one page file, but not yet moved into `src/i18n/dictionary.ts`. |
| Hard-coded business statuses are documented or typed | Pass with notes | Stage, decision, inspection type, document status and workflow status are typed in `src/types/quality.ts`. |
| Long Chinese labels do not break layout | Pass | Desktop and 390px mobile smoke found no page-level overflow. |
| Future English/Japanese labels would fit with current layout | Pass with notes | Tab buttons wrap; wide tables use local horizontal scroll. Re-check after i18n extraction. |

## UX Refinement Completed

| Item | Result |
| --- | --- |
| Search behavior | Header search now filters by inspection number, batch, item, source document, work order, sales order, supplier, line, status, pending tests and document fields. |
| Detail synchronization | If the current selected inspection does not match the search, the detail panel derives the first matching inspection instead of showing unrelated details. |
| Batch visibility | Detail header now includes batch number so batch-based search can be verified immediately. |
| Release entry | `放行` switches to the release/block view instead of implying an unimplemented mutation. |
| Placeholder action clarity | Advanced filter remains a V1 placeholder with tooltip guidance until API filter fields are confirmed. |
| Empty state | Search-filtered empty results show controlled messages instead of blank panels. |

## Decision

Decision:

```txt
accepted_with_notes
```

Reason:

The Quality page is suitable for V1 API validation as a management-oriented release/blocker workspace. It preserves the agreed scope: material/process/finished/pre-shipment inspections, release/hold decisions, NCR status and document completeness. Remaining notes are API mapping, quality-source confirmation and i18n extraction items, not blockers for read-only integration.

## Follow-Up Items

| Owner | Item | Priority | Due / trigger |
| --- | --- | --- | --- |
| Backend engineer | Confirm where material inspection status is stored today. | High | Before implementing `/api/v1/quality/dashboard` |
| Backend engineer | Confirm whether inventory includes quality hold quantity/status. | High | During Quality/Warehouse integration |
| Backend engineer | Confirm which quality statuses block production, inventory release and shipment. | High | Before cross-module blocker integration |
| Backend engineer | Confirm whether process and finished-goods inspection results are stored in work/product data. | High | During Quality API implementation |
| Frontend | Revisit empty-array fallback policy after real API returns controlled empty datasets. | Medium | After first Quality API runtime report |
| Frontend | Move stable Quality static labels into `src/i18n/dictionary.ts`. | Medium | After Quality API mapping stabilizes |
