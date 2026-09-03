# Backend API Response - ERP2-RECIPE-FORMULA-RO-EXEC-001-BE-UX-SVC-RETEST

## 1. Retest Summary

| Item | Result |
|---|---|
| Work Item | ERP2-RECIPE-FORMULA-RO-EXEC-001-BE-UX-SVC-RETEST |
| Scope | Bounded non-production Recipe / Formula UX-consumable backend service window confirmation |
| Date | 2026-09-03 |
| Result | BLOCKED |
| Classification | ENVIRONMENT_RUNTIME_ONLY |

Frontend / UX has aligned the `/recipe` contract to Backend commit `82c65de` and frontend commit `52980ac`. This retest checked whether Backend can provide a UX-consumable Recipe / Formula service window backed by the Engineering B Shared DEV DB endpoint.

## 2. Non-Secret Environment Check

| Check | Result | Note |
|---|---|---|
| Private DB endpoint TCP reachability | PASS | Network can reach the registered private DB port |
| Shared DEV credential environment variables | MISSING | No Shared DEV DB host/user/password variables are injected in the current Codex process |
| `restserver/package/config/.env.dev` | MISSING | No local authorized runtime env file exists |
| Previously opened BOM service window | CLOSED / NOT RESPONDING | The previous `5027` service window is no longer available |

No raw DB secrets were printed, copied, persisted, or committed during this retest.

## 3. Service Window Status

| Item | Value |
|---|---|
| UX-consumable Recipe service URL | Not available |
| Port | Not allocated |
| DB-backed route smoke | Not executed |
| Close / timeout handling | No new service process was started |

Because the current runtime does not have Shared DEV DB credentials injected, starting a DB-backed Recipe / Formula service window would fail at the database connection layer. A non-DB-backed service would not satisfy the real backend browser validation goal.

## 4. Product / API Defect Classification

This is not classified as a Recipe / Formula product/API defect.

Reason:

1. Backend implementation commit `82c65de` already passed Recipe Formula unit tests, full backend tests, and local HTTP route smoke.
2. The current blocker occurs before DB-backed business route validation, at the runtime credential-injection/service-window layer.
3. The private DB endpoint is reachable, but the authorized credential material is not present in this Codex process.

## 5. Required Next Action

Engineering B or the operator should start the Backend service window with the authorized non-production Shared DEV DB credential injection and the following non-secret runtime settings:

| Setting | Value |
|---|---|
| Service scope | Recipe / Formula read-only UX validation |
| Token test mode | `TOKEN_ENABLED=1` in child process only |
| Required request header | `x-timezone: Asia/Taipei` |
| Required request header | `x-auth-token: ERP2_NON_PRODUCTION_READ_VALIDATION` |

Expected smoke routes:

| Method | URL |
|---|---|
| GET | `/api/v2/recipe-formula/dashboard?count=1` |
| GET | `/api/v2/recipe-formula/{recipe_no}/versions` |
| GET | `/api/v2/recipe-formula/{recipe_no}/versions/{version}/composition` |
| GET | `/api/v2/recipe-formula/by-product/{product_no}` |
| POST | `/api/v2/recipe-formula/dashboard` should return method not allowed or be rejected |

## 6. Final Classification

**RECIPE_FORMULA_UX_SERVICE_WINDOW_BLOCKED_BY_MISSING_SHARED_DEV_CREDENTIAL_INJECTION_ENVIRONMENT_ONLY**

This means Recipe / Formula API implementation is not currently blocked by a known product/API defect. The remaining blocker is that the current runtime cannot start a DB-backed service window without the authorized Shared DEV credential injection.

