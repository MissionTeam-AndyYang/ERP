# Backend API Response - ERP2-BOM-PRODUCT-STRUCTURE-RO-EXEC-001-BE-SVC-001

## 1. Active Service Window

| Item | Value |
| --- | --- |
| Service URL | http://127.0.0.1:5027 |
| Port | 5027 |
| Scope | Bounded non-production Backend service window |
| Purpose | Frontend / UX real-backend browser validation for BOM Product Structure read-only slice |

## 2. Process / Window Evidence

| Item | Value |
| --- | --- |
| Process ID | 6192 |
| Process Name | pythonw |
| Start Time | 2026-09-03 18:51:12 +08:00 |
| Window Mode | Hidden background process |
| Working Directory | `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0\restserver` |
| Process Status | Responding |

## 3. Commit Identity

| Item | Value |
| --- | --- |
| Current Branch | main |
| Active Commit | ed954fe Implement BOM product structure tree UX |
| Backend API Implementation Commit | 49242d6 Implement BOM product structure API |
| Compatibility | Current active commit is later than 49242d6 and preserves the accepted read-only Product Structure contract |

## 4. Configuration Boundary

| Item | Value |
| --- | --- |
| Authorization | ERP2-CIO-BOM-PRODUCT-STRUCTURE-RO-EXEC-001 |
| Work Item | ERP2-BOM-PRODUCT-STRUCTURE-RO-EXEC-001-BE-SVC-001 |
| Database Boundary | Shared DEV formal ERP-compatible fixture only |
| Credential Handling | Engineering B wrapper injected credentials into child process only |
| Secret Handling | No raw secret values printed, copied, committed, or persisted |
| Token Treatment | `TOKEN_ENABLED=1` in backend child process only; UX requests must still send `x-auth-token` |
| Production Boundary | No Production DB, Production data, Production credential, deployment, migration, cutover, or Go-Live |

## 5. Shared DEV DB Auth / Fixture Sanity

**Result: PASS**

| Check | Result |
| --- | ---: |
| DB auth | PASS |
| `bom` row count | 1 |
| `product` row count | 1 |
| `product_spec` row count | 1 |

## 6. Required Route Smoke Results

**Result: PASS**

| Endpoint | HTTP Status | API Code | Payload Keys |
| --- | ---: | ---: | --- |
| GET /api/v2/bom/dashboard | 200 | 0 | `count`, `items`, `serverTimestamp`, `start`, `summary`, `total` |
| GET /api/v2/bom/{bom_no}/detail | 200 | 0 | `bom`, `items`, `linkedProducts`, `versions` |
| GET /api/v2/bom/product-structure/{product_no} | 200 | 0 | `bomEvidence`, `children`, `rootProduct`, `serverTimestamp`, `warnings` |

The smoke validation derived the detail/product identifiers internally from successful read-only API responses and did not print database payload identifiers.

## 7. Read-Only Negative Control

**Result: PASS**

| Check | HTTP Status | Result |
| --- | ---: | --- |
| POST /api/v2/bom/product-structure/{product_no} | 405 | PASS_WRITE_METHOD_NOT_ALLOWED_OR_REJECTED |

The Product Structure service window exposes the required read-only GET route only. No Product write, Recipe/Formula write, schema mutation, or migration route was added.

## 8. UX Consumption Instructions

Frontend / UX participant can use:

| Item | Value |
| --- | --- |
| API Base URL | `http://127.0.0.1:5027` |
| Required Header | `x-timezone: Asia/Taipei` |
| Required Header | `x-auth-token: ERP2_NON_PRODUCTION_READ_VALIDATION` |

Routes available for this slice:

- `GET /api/v2/bom/dashboard`
- `GET /api/v2/bom/{bom_no}/detail`
- `GET /api/v2/bom/product-structure/{product_no}`

Do not call write APIs through this service window.

## 9. Duration / Closure Expectation

The service window is currently open as local process `6192`.

When UX / CTO validation is complete, close it with:

`Stop-Process -Id 6192 -Force`

## 10. Limitations

1. This is a local non-production service window only.
2. This validates read-only BOM Product Structure routes against Shared DEV fixture data only.
3. Standard login/session mutation is outside scope; the service uses the previously documented non-production token/session test treatment.
4. Product write, Recipe/Formula implementation, Production access, Source-of-Truth transition, Engineering Pull, Cutover, and Go-Live remain out of scope.

## 11. Final Classification

**BOM_PRODUCT_STRUCTURE_SERVICE_WINDOW_OPEN_DB_AUTH_PASS_ROUTE_SMOKE_PASS_READONLY_CONTROL_PASS_SHARED_DEV_ONLY**

This classification means the bounded non-production Backend service window is open and ready for Frontend / UX real-backend browser validation of the BOM Product Structure read-only slice.
