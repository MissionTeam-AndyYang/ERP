# ERP Frontend Service Schema Guard Review

Date: 2026-05-26
Scope: Frontend service/hook guard review for API integration readiness.

## Summary

The dashboard service layer now has a consistent array fallback policy:

```txt
Use API value when it is an array, including [].
Fallback to mock only when the field is missing or not an array.
```

This matters because Backend API Integration needs to distinguish:

- API unavailable: use mock fallback.
- API available but no records: show a valid empty state.
- API available but field/schema mismatch: fallback that field and keep the page stable.

## Code Guard Completed

| File | Change |
| --- | --- |
| `src/services/api-client.ts` | Added `withFallbackArray<T>(value, fallback)` helper. |
| `src/services/dashboard-api.ts` | Replaced non-icon array `.length` fallback checks with `withFallbackArray`. |
| `src/services/warehouse-api.ts` | Normalized all array fields with `withFallbackArray`. |
| `src/services/orders-api.ts` | Normalized all array fields with `withFallbackArray`. |
| `src/services/planning-api.ts` | Normalized all array fields with `withFallbackArray`. |
| `src/services/production-api.ts` | Normalized all array fields with `withFallbackArray`. |
| `src/services/quality-api.ts` | Normalized all array fields with `withFallbackArray`. |
| `src/services/purchasing-api.ts` | Normalized all array fields with `withFallbackArray`. |
| `src/services/logistics-api.ts` | Normalized all array fields with `withFallbackArray`. |
| `src/services/finance-api.ts` | Normalized all array fields with `withFallbackArray`. |
| `src/services/rd-api.ts` | Normalized all array fields with `withFallbackArray`. |
| `src/services/workforce-api.ts` | Normalized all array fields with `withFallbackArray`. |
| `src/services/traceability-api.ts` | Normalized all array fields with `withFallbackArray`. |
| `src/services/settings-api.ts` | Normalized all array fields with `withFallbackArray`. |

## Hook Review

| Pattern | Current state | Decision |
| --- | --- | --- |
| Initial render | Hooks initialize with module mock data and `isLoading: true`. | Keep for stable first paint during API probing. |
| Successful API call | Hooks set normalized data, `source: "api"` and `isLoading: false`. | Keep. |
| API failure | Services return mock data, `source: "mock"` and error text. | Keep until backend availability is stable. |
| Component empty states | First-round refined pages show controlled empty states for filtered empty results. | Keep; revisit API-empty full-page states after backend returns real empty arrays. |
| Cancellation | Hooks use `isMounted` guard before state update. | Keep for V1. |

## Remaining Guard Gaps

| Gap | Risk | Recommendation |
| --- | --- | --- |
| Runtime object validation | TypeScript types are compile-time only; malformed object fields can still reach UI. | Add schema validation only after backend payload shape stabilizes. |
| Status vocabulary mapping | API may return values outside frontend union types. | Confirm canonical status values per module before strict validation. |
| Dashboard icon-bearing arrays | Manager dashboard `managerFocusItems` and `moduleShortcuts` still require local icon functions. | Keep mock fallback for these icon-bearing arrays unless API returns icon keys and frontend maps them. |
| Empty summary arrays | Empty `summary` arrays are now considered valid API data. | Backend should avoid empty summary if KPI tiles are expected; otherwise page may show no KPI cards. |
| Support dashboard pages | Items, BOM, Batches and AI use `getSupportDashboard` shallow merge fallback. | Review in a later pass when those pages enter refinement scope. |

## Verification

Run after this local change:

```txt
npm.cmd run lint
npm.cmd run build
```

Expected result:

```txt
Both pass.
```

## Upload Plan

Do not push this local work until the user confirms the next morning.

Suggested commit message when ready:

```txt
Prepare frontend API integration readiness guardrails
```
