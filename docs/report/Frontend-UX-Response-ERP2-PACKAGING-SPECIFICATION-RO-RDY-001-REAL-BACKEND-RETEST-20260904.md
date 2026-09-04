# Frontend UX Response - ERP2 Packaging Specification Real Backend Retest

Date: 2026-09-04  
Scope: `ERP2-CIO-PACKAGING-SPECIFICATION-RO-RDY-001` bounded frontend retest  
Frontend route: `/packaging`  
Backend endpoint: `GET /api/v2/packaging-specification/overview`  
Backend reference commit: `be9cd9d Implement packaging specification read-only API`  
Frontend reference commit: `7ffb3f8 Implement packaging specification read-only UX`

## Retest Summary

Performed a bounded frontend browser retest against a real local Flask backend route.

The current participant environment does not contain Shared DEV DB connection variables and has no local MariaDB service reachable on `localhost:3306`, so the browser retest could verify the real backend route/CORS/API-base path up to the controlled DB connection blocker, but could not reproduce the DB-backed Shared DEV HTTP 200 payloads reported by the backend engineer.

Disposition:

```text
FRONTEND_PACKAGING_SPECIFICATION_REAL_BACKEND_RETEST_COMPLETE_WITH_LOCAL_DB_RUNTIME_BLOCKER
```

## Backend Reports Reviewed

| Report | Key Result |
| --- | --- |
| `docs/report/Backend-API-Response-ERP2-CIO-PACKAGING-SPECIFICATION-RO-RDY-001-Implementation-20260904-001.md` | Backend implemented read-only endpoint, tests passed, Shared DEV retest completed. |
| `docs/report/Backend-API-Response-ERP2-CIO-PACKAGING-SPECIFICATION-RO-RDY-001-Shared-DEV-Retest-20260904-001.md` | Product scenario returned HTTP 200 with `module_unavailable`; WIP scenario returned HTTP 200 with `missing_packaging_spec`; both had empty `packagingSpecs[]` under Shared DEV fixture limitations. |

## Environment

| Item | Value |
| --- | --- |
| Flask backend URL | `http://127.0.0.1:5057` |
| Frontend URL | `http://127.0.0.1:3043/packaging` |
| Frontend API base | `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5057` |
| API token header | Present through `NEXT_PUBLIC_API_TOKEN` test value |
| Timezone header | `Asia/Taipei` |
| Shared DEV DB env vars | Not present in this participant environment |
| Local MariaDB | Not reachable on `localhost:3306` |

## Direct Backend Route Check

| Check | Result | Evidence |
| --- | --- | --- |
| Product API route exists | PASS WITH ENV BLOCKER | `GET /api/v2/packaging-specification/overview?itemNo=PRD-SD-001&itemCategory=5&productVersion=1` reached Flask and returned HTTP 400 from DB connection failure, not 404. |
| WIP API route exists | PASS WITH ENV BLOCKER | `GET /api/v2/packaging-specification/overview?itemNo=INP-SD-001&itemCategory=4` reached Flask and returned HTTP 400 from DB connection failure, not 404. |
| CORS preflight | PASS | Flask log showed `OPTIONS /api/v2/packaging-specification/overview... 200`. |

Observed backend blocker:

```text
mariadb.OperationalError Can't connect to server on 'localhost' (10061)
```

This is an environment/service-window limitation in the frontend participant runtime. It is not a frontend implementation failure and does not contradict the backend Shared DEV retest report.

## Browser Retest

| Check | Result | Evidence |
| --- | --- | --- |
| Frontend calls real backend packaging endpoint | PASS | Flask log showed browser `OPTIONS` and `GET` requests from `/packaging` to `/api/v2/packaging-specification/overview`. |
| API mode does not hit Next.js fallback route | PASS | Browser displayed `API request failed: 400`; not `API request failed: 404`. |
| Product scenario no silent mock fallback | PASS | API mode did not display `BOM2-CASE-001` or mock Product packaging rows after backend error. |
| WIP scenario no silent mock fallback | PASS | API mode did not display WIP mock downstream-product packaging text before manual mock selection. |
| Manual mock mode explicit only | PASS | Mock packaging rows appeared only after selecting `示範資料`. |
| No write/approval/release controls | PASS | No buttons matching create/update/delete/approve/release/save/submit labels were present. |
| Browser console errors | PASS | No browser console errors captured during the retest. |

## Shared DEV Payload Retest Limitation

The backend Shared DEV report expects:

- Product: HTTP 200, `packagingSpecs=[]`, warning `module_unavailable`
- WIP: HTTP 200, `packagingSpecs=[]`, warning `missing_packaging_spec`

This participant browser session could not confirm those exact HTTP 200 DB-backed payloads because it lacks the Shared DEV DB environment variables:

```text
ERP2_SHARED_DEV_DB_HOST
ERP2_SHARED_DEV_DB_PORT
ERP2_SHARED_DEV_DB_NAME
ERP2_SHARED_DEV_DB_USER
ERP2_SHARED_DEV_DB_PASSWORD
```

The frontend mapper and screen remain prepared to display those payload groups when the backend returns them:

- `summary`
- `packagingSpecs[]`
- `sourceLineage`
- `warnings[]`
- `moduleReadiness[]`
- `capabilityBoundary`

## Boundary Confirmation

No Product write, Packaging write, Packaging approval/release, Production action, migration, Source-of-Truth transition, Engineering Pull, Cutover, or ERP2.0 Go-Live behavior was added or exercised.

