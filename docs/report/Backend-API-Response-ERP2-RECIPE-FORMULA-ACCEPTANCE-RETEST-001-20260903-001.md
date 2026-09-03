# Backend API Response - ERP2-RECIPE-FORMULA-ACCEPTANCE-RETEST-001

## 1. Retest Summary

| Item | Result |
|---|---|
| CIO authorization | ERP2-CIO-RECIPE-FORMULA-ACCEPTANCE-RETEST-001 |
| Scope | Bounded non-production Recipe / Formula backend acceptance retest |
| Backend baseline | `82c65de` or later on `main` |
| Runtime source | Engineering Office B governed Shared DEV credential injection wrapper |
| Service URL | `http://127.0.0.1:5029` |
| Service process | `pythonw` PID `6356` |
| Result | PASS |
| Classification | DB_BACKED_RECIPE_FORMULA_BACKEND_SMOKE_PASS_SHARED_DEV_READONLY |

This retest used the Engineering Office B governed child-process credential injection mechanism. No raw DB secret was printed, copied, persisted, or committed.

## 2. Engineering B Runtime Evidence Consumed

| Item | Evidence |
|---|---|
| Coordination response | `Engineering-Office-B-Response-ERP2-CIO-RECIPE-FORMULA-ACCEPTANCE-RETEST-001-Runtime-and-Shared-DEV-Coordination-20260903-001.md` |
| Wrapper path | `20_Engineering_Workspace/Runtime_Connectivity/ERP2-SHARED-DEV-DB-ENDPOINT-A1-ACT-001/tools/invoke_shared_dev_item_transitem_db_access.ps1` |
| Credential class | `ERP2_SHARED_DEV_ITEM_TRANSITEM_NP_READONLY` |
| Injection style | Child-process environment injection |
| Raw secret exposure | `0` |
| Endpoint class | `PRIVATE_INTERNAL_HOST_ADDRESS / NON_PUBLIC / NON_PRODUCTION` |

The backend service was launched through the wrapper. The wrapper injected the governed Shared DEV variables into the child process, and the launch command mapped those variables into the `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` names expected by the existing restserver runtime.

## 3. DB-Backed Confirmation

| Check | Result |
|---|---|
| Private DB TCP reachability | PASS |
| Runtime database identity | `erp2_shared_dev_item_transitem_np` |
| `bom` row count | 1 |
| `bom_item` row count | 1 |
| `product_spec` row count | 1 |
| `product_bom_spec` row count | 1 |
| `inproduct_bom_spec` row count | 1 |

The direct DB sanity check was executed through the same governed wrapper and printed only database identity and row counts.

## 4. Service Window

| Item | Value |
|---|---|
| API base URL | `http://127.0.0.1:5029` |
| Required header | `x-timezone: Asia/Taipei` |
| Required header | `x-auth-token: ERP2_NON_PRODUCTION_READ_VALIDATION` |
| Token treatment | `TOKEN_ENABLED=1` in backend child process only |
| Service host | `127.0.0.1` |
| Service port | `5029` |

This service window is local to this host and is backed by the Engineering B Shared DEV database path. It is not a public endpoint and is not a production deployment.

## 5. Route Smoke Result

| Endpoint | HTTP | API Code | Payload Keys | Result |
|---|---:|---:|---|---|
| GET `/api/v2/recipe-formula/dashboard?count=1` | 200 | 0 | `capabilityBoundary,count,recipes,serverTimestamp,start,summary,total` | PASS |
| GET `/api/v2/recipe-formula/{recipe_no}/versions` | 200 | 0 | `capabilityBoundary,recipe,serverTimestamp,versions` | PASS |
| GET `/api/v2/recipe-formula/{recipe_no}/versions/{version}/composition` | 200 | 0 | `capabilityBoundary,formula,inputs,output,recipe,serverTimestamp,sourceLineage,version,warnings` | PASS |
| GET `/api/v2/recipe-formula/by-product/{product_no}` | 200 | 0 | `capabilityBoundary,productNo,productVersion,recipeVersions,serverTimestamp` | PASS |
| POST `/api/v2/recipe-formula/dashboard` | 405 | N/A | N/A | PASS, read-only negative control |

The smoke test derived recipe/product identifiers internally from successful GET responses and did not print payload identifiers.

## 6. Close / Timeout Handling

| Condition | Handling |
|---|---|
| CTO / user says validation is complete | Stop local process `6356` |
| Frontend / UX validation complete | Stop local process `6356` |
| Timeout or endpoint instability | Stop local process `6356` and rerun through wrapper if needed |
| Credential/security issue | Stop local process `6356` immediately |
| Boundary trigger | Stop local process `6356` immediately |

Manual close command:

`Stop-Process -Id 6356 -Force`

## 7. Limitations

1. This validates the Backend/API read-only Recipe / Formula service window only.
2. This does not grant Product acceptance.
3. This does not redesign Product semantics or change the material API contract.
4. This does not perform Recipe, BOM, Product, Routing, Packaging, Manufacturing Definition, Costing, or Production write behavior.
5. This does not perform migration, Source-of-Truth transition, Engineering Pull, Cutover, or Go-Live.
6. Cross-host frontend access may still require host/network coordination; local browser validation on this host can use `http://127.0.0.1:5029`.

## 8. Final Classification

**DB_BACKED_RECIPE_FORMULA_BACKEND_SMOKE_PASS_SHARED_DEV_READONLY**

This means the Backend/API participant successfully launched a DB-backed non-production Recipe / Formula service window through the governed Engineering B Shared DEV credential-injection path, completed route smoke for the required GET endpoints, and confirmed read-only negative control behavior.

