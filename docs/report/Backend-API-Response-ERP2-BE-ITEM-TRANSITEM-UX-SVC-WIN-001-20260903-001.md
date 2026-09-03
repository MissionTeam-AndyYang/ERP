# Backend API Response - ERP2-BE-ITEM-TRANSITEM-UX-SVC-WIN-001

## 1. Service URL

| Item | Value |
| --- | --- |
| Service URL | http://127.0.0.1:5025 |
| Service Scope | Local non-production Backend HTTP service window |
| UX Validation Scope | Read-only Item Center and Transaction Item Master real-backend validation |

## 2. Process / Window Identity

| Item | Value |
| --- | --- |
| Process ID | 17388 |
| Process Name | pythonw |
| Start Time | 2026-09-03 16:22:17 +08:00 |
| Window Mode | Hidden background process |
| Working Directory | `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0\restserver` |

## 3. Configuration Boundary

| Item | Value |
| --- | --- |
| Authorization ID | ERP2-CIO-SHARED-DEV-DB-PRIVATE-ACT-001 |
| Work Item | ERP2-BE-ITEM-TRANSITEM-UX-SVC-WIN-001 |
| Database Boundary | Shared DEV formal ERP-compatible fixture only |
| Production Boundary | No Production DB, data, credential, deployment, migration, cutover, or Source-of-Truth transition |
| Runtime Credential Treatment | Engineering B wrapper injected credentials into child process only |
| Secret Exposure | No raw secret values printed, copied, or persisted |
| Token Treatment | `TOKEN_ENABLED=1` in backend child process only; `x-auth-token` header still required by API header check |

## 4. Shared DEV DB Auth Confirmation

**Result: PASS**

| Sanity Check | Result |
| --- | ---: |
| DB auth | PASS |
| `material` row count | 2 |
| `trans_items` row count | 2 |

## 5. Read-Only Item API Smoke Confirmation

**Result: PASS**

| Endpoint | HTTP Status | API Code | Payload Keys |
| --- | ---: | ---: | --- |
| GET /api/v2/items/dashboard | 200 | 0 | `categorySummary`, `count`, `items`, `maintenanceSuggestions`, `serverTimestamp`, `start`, `summary`, `total` |
| GET /api/v2/items/{item_no}/detail | 200 | 0 | `bomUsage`, `inventorySummary`, `item`, `maintenanceSuggestions`, `recentBatches`, `serverTimestamp` |

## 6. Read-Only Transaction Item API Smoke Confirmation

**Result: PASS**

| Endpoint | HTTP Status | API Code | Payload Keys |
| --- | ---: | ---: | --- |
| GET /api/v2/transitems/dashboard | 200 | 0 | `companies`, `count`, `serverTimestamp`, `start`, `summary`, `total`, `transactionItems` |
| GET /api/v2/transitems/companies/{company_no}/detail | 200 | 0 | `company`, `contracts`, `serverTimestamp`, `transactionItems` |
| GET /api/v2/transitems/transitems/{transaction_item_no}/detail | 200 | 0 | `contracts`, `linkedItems`, `serverTimestamp`, `transItem` |

## 7. UX Consumption Instructions

Frontend / UX participant can consume the local backend service using:

| Item | Value |
| --- | --- |
| API Base URL | `http://127.0.0.1:5025` |
| Required Header | `x-timezone: Asia/Taipei` |
| Required Header | `x-auth-token: ERP2_NON_PRODUCTION_READ_VALIDATION` |

Expected read-only UX validation entry points:

- `GET /api/v2/items/dashboard`
- `GET /api/v2/items/{item_no}/detail`
- `GET /api/v2/transitems/dashboard`
- `GET /api/v2/transitems/companies/{company_no}/detail`
- `GET /api/v2/transitems/transitems/{transaction_item_no}/detail`

Do not call write APIs through this service window. This service window is for read-only UX real-backend validation only.

## 8. Stop Instruction

When the UX validation window is no longer needed, stop the local service process:

`Stop-Process -Id 17388 -Force`

## 9. Final Classification

**UX_BACKEND_SERVICE_WINDOW_OPEN_DB_AUTH_PASS_ITEM_API_SMOKE_PASS_TRANSITEM_API_SMOKE_PASS_READONLY_SHARED_DEV_ONLY**

This classification means the bounded local backend service window is open and ready for read-only UX real-backend validation against the Shared DEV formal ERP-compatible fixture.
