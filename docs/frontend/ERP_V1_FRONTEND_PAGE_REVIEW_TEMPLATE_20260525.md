# ERP V1 Frontend Page Review Template

Date: 2026-05-25
Purpose: Provide a repeatable checklist for reviewing each frontend page after API integration or UI refinement.

## Review Metadata

| Field | Value |
| --- | --- |
| Review date |  |
| Reviewer |  |
| Page / route |  |
| Related API endpoint |  |
| Data source during review | `api` / `mock` / `mixed` |
| Frontend commit / branch |  |

## Page Smoke

| Check | Result | Notes |
| --- | --- | --- |
| Page loads without fatal error |  |  |
| No console error from schema mismatch |  |  |
| Loading state is stable |  |  |
| API failure falls back or shows controlled empty/error state |  |  |
| Desktop layout has no overlap |  |  |
| Mobile layout has no overlap |  |  |
| Navigation/sidebar behavior is usable |  |  |

## Business Acceptance

| Check | Result | Notes |
| --- | --- | --- |
| Page supports the agreed V1 management concern |  |  |
| Highest-priority risk is visible without drilling down |  |  |
| Status tones are understandable |  |  |
| Main cards/tables use practical labels |  |  |
| Empty or missing data does not mislead the user |  |  |
| User can identify next action or owner where relevant |  |  |

## API Integration Review

| Check | Result | Notes |
| --- | --- | --- |
| Endpoint path matches service file |  |  |
| Top-level datasets are consumed correctly |  |  |
| Partial response uses fallback only where intended |  |  |
| Dates, numbers and units display correctly |  |  |
| API and mock data have compatible shape |  |  |

## I18N Readiness

| Check | Result | Notes |
| --- | --- | --- |
| User-facing labels are easy to extract later |  |  |
| Hard-coded business statuses are documented or typed |  |  |
| Long Chinese labels do not break layout |  |  |
| Future English/Japanese labels would fit with current layout |  |  |

## Decision

| Decision | Meaning |
| --- | --- |
| `accepted` | Page can proceed to next module or deeper API integration. |
| `accepted_with_notes` | Page is usable, but tracker should record limitations. |
| `revise_ui` | Layout, wording or interaction must be revised. |
| `revise_api_mapping` | Frontend mapping must change before acceptance. |
| `blocked` | Waiting for backend, data or business decision. |

Decision:

```txt

```

## Follow-Up Items

| Owner | Item | Priority | Due / trigger |
| --- | --- | --- | --- |
|  |  |  |  |

