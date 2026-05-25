# ERP API Runtime Verification Template

Date: 2026-05-26
Scope: Reusable frontend verification template for backend API integration.

## How To Use

Copy this template for each endpoint after the backend engineer confirms it is available.

Recommended file name:

```txt
docs/frontend/ERP_<WORKSPACE>_API_RUNTIME_VERIFICATION_YYYYMMDD.md
```

## Verification Metadata

| Field | Value |
| --- | --- |
| Verification date |  |
| Verifier |  |
| Workspace / route |  |
| Endpoint |  |
| Frontend branch / commit |  |
| Backend branch / commit |  |
| API base URL |  |
| Environment | local / staging / production |

## Endpoint Availability

| Check | Result | Notes |
| --- | --- | --- |
| Endpoint responds | Pending |  |
| HTTP status is 2xx | Pending |  |
| Response is JSON | Pending |  |
| Response uses accepted envelope | Pending | Raw payload or `{ data: ... }` are both accepted by `apiGet`. |
| Timeout behavior is controlled | Pending | Frontend default timeout is 8000 ms. |

## Response Shape

| Field group | Expected frontend shape | Actual API shape | Result | Notes |
| --- | --- | --- | --- | --- |
| Summary/KPI |  |  | Pending |  |
| Main rows |  |  | Pending |  |
| Risk/blocker rows |  |  | Pending |  |
| Detail/workflow data |  |  | Pending |  |
| Document/status data |  |  | Pending |  |

## Empty And Fallback Behavior

| Scenario | Expected frontend behavior | Result | Notes |
| --- | --- | --- | --- |
| API unavailable | Page uses mock fallback, shows `Mock fallback` and warning text. | Pending |  |
| API returns empty array | Empty array is accepted as real API data. | Pending |  |
| API omits optional array field | Only that field falls back to mock. | Pending |  |
| API returns non-array where array expected | Only that field falls back to mock. | Pending |  |
| API returns unknown status value | Page remains stable; tone mapping issue is recorded. | Pending |  |

## UI Smoke

| Check | Result | Notes |
| --- | --- | --- |
| Page loads without fatal error | Pending |  |
| Source badge shows `API data` when endpoint succeeds | Pending |  |
| Search filters rows | Pending |  |
| Tab/view switching works | Pending |  |
| Detail panel syncs to selected/filtered row | Pending |  |
| Empty state is visible for no matching rows | Pending |  |
| Header CTA remains view navigation unless mutation is contracted | Pending |  |
| Desktop layout has no page-level horizontal overflow | Pending |  |
| Mobile 390px layout has no page-level horizontal overflow | Pending |  |

## Mapping Decisions

| Decision | Owner | Status | Notes |
| --- | --- | --- | --- |
| Status vocabulary confirmed | Backend / Frontend | Pending |  |
| Tone mapping confirmed | Frontend | Pending |  |
| Owner/team field confirmed | Backend | Pending |  |
| Date/time format confirmed | Backend / Frontend | Pending |  |
| Detail endpoint needed for V1 | Backend / Frontend | Pending |  |

## Result

Decision:

```txt
pending
```

Allowed values:

```txt
accepted
accepted_with_notes
blocked_by_api_shape
blocked_by_missing_endpoint
blocked_by_status_vocabulary
```

## Follow-Up Items

| Owner | Item | Priority | Due / trigger |
| --- | --- | --- | --- |
|  |  |  |  |
