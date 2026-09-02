# Inventory Read API Component Test Report - 2026-09-02

## Scope

Work item: `ERP2-API-WH-INV-READ-001`

Implemented read-only endpoint ceiling:

- `GET /api/v2/inventory/balances`
- `GET /api/v2/inventory/movements`
- `GET /api/v2/lots`
- `GET /api/v2/lots/{lot_code}/trace`

## Boundary Confirmation

- No `POST`, `PUT`, `PATCH`, or `DELETE` endpoint was added.
- No inventory posting, adjustment, UOM conversion, migration, production data load, source-of-truth transition, cutover, deployment, or Go-Live behavior was implemented.
- `WH_INV_READ` was defined as the explicit read-only permission code in `EInventoryReadPermissionCode`.
- UOM Option B was preserved: quantity fields keep source unit code in `unit`; no `unitName`, unit translation, or unit conversion is returned by the backend.

## Source Files

| File | Purpose |
|---|---|
| `restserver/package/common/common.py` | Added `EInventoryReadPermissionCode.WH_INV_READ`. |
| `restserver/package/restserver/api/v2/inventory.py` | Added bounded read-only service and endpoint executors. |
| `restserver/package/restserver/api/v2/inventory_uri.py` | Added GET-only v2 route definitions. |
| `restserver/package/restserver/app.py` | Registered `inventory_v2` blueprint. |
| `restserver/package/dbwrapper/dbmgr.py` | Bounded remediation: prevent failed DB initialization from leaving poisoned shared session state. |
| `docs/spec/api/inventory.md` | Added formal v2 API contract sections. |
| `restserver/tests/test_inventory_read_api.py` | Added component tests for read-only inventory branch. |

## Test Evidence

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest restserver/tests/test_inventory_read_api.py restserver/tests/test_warehouse_dashboard.py restserver/tests/test_traceability_api.py
```

Result:

```text
42 passed
```

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest restserver/tests
```

Result:

```text
73 passed
```

## NEXT-011 Bounded Retest Addendum

Retest window:

- Work item: `ERP2-ENG-CROSS-LAYER-VS-WH-INV-INT-TEST-001`
- Authority: `ERP2-CTO-BACKLOG-ORCH-NEXT-011`
- Non-production listener supplied by Engineering Office A: `127.0.0.1:3307`, database `test`

Connectivity result:

- TCP listener probe: reachable.
- SQLAlchemy / MariaDB authentication: blocked by driver-level SSPI credential error in this participant environment.
- Real API -> DB/staging validation: Safe Stop, because usable non-production DB credentials or connection method were not available to the Backend participant.

Bounded remediation performed:

- `CDBMgr` and `CDBMgrTrans` now assign shared engine/session state only after engine creation and metadata initialization complete.
- This prevents a failed first DB connection from poisoning subsequent endpoint calls with a secondary `NoneType` session error.
- The remediation does not change endpoint contract, route ceiling, security boundary, UOM behavior, schema, migration state, or data.

Sanitized HTTP retest after remediation:

| Endpoint | HTTP Status | API Code | Sanitized Result |
|---|---:|---:|---|
| `GET /api/v2/inventory/balances` | 400 | 1001 | DB auth / SSPI credential error |
| `GET /api/v2/inventory/movements` | 400 | 1001 | DB auth / SSPI credential error |
| `GET /api/v2/lots` | 400 | 1001 | DB auth / SSPI credential error |
| `GET /api/v2/lots/INVALID-LOT/trace` | 400 | 1001 | DB auth / SSPI credential error |
| `POST /api/v2/inventory/balances` | 405 | N/A | Method not allowed; read-only route preserved |

Retest evidence:

```text
restserver/tests/test_inventory_read_api.py: 6 passed
restserver/tests/test_inventory_read_api.py + test_warehouse_dashboard.py + test_traceability_api.py: 42 passed
restserver/tests: 73 passed
```

Required external completion:

- Engineering A/B must provide a usable non-secret connection method or execute the four authorized HTTP checks inside the environment that holds the synthetic package `SYNTHETIC-WH-INV-INT-TEST-001`.
- Expected staging/crosswalk row counts during that window remain: balance snapshot 2, movement 3, lot snapshot 2, item crosswalk 2, lot crosswalk 2, UOM crosswalk 1, validation result 10.

## NEXT-012 Synchronized Real HTTP Retest Addendum

Retest window:

- Window ID: `ERP2-WH-INV-RTW-001-20260902`
- Authority: `ERP2-CTO-BACKLOG-ORCH-NEXT-012`
- Backend work item: `ERP2-WH-INV-RTW-001-BACKEND`
- API baseline in current main history: `5c81213 Implement read-only inventory APIs`
- UX minimum baseline in current main history: `e4a928a Align warehouse inventory API integration`

Active-work collision check:

- The synchronized Warehouse / Inventory retest remained limited to the four authorized read-only endpoints.
- No Product acceptance, next Product slice execution, local candidate integration, Engineering Pull, Test Engineering activation, migration, source-of-truth transition, Cutover, or ERP2.0 Go-Live action was performed.

Non-production runtime relationship:

- Backend API process was started locally at `http://127.0.0.1:5012`.
- Backend process was configured to target non-production MariaDB `127.0.0.1:3307`, database `test`.
- Engineering A reported the synchronized DB/staging window open with synthetic package `SYNTHETIC-WH-INV-INT-TEST-001` and expected row counts: balance snapshot 2, movement 3, lot snapshot 2, item crosswalk 2, lot crosswalk 2, UOM crosswalk 1, validation result 10.

Connectivity evidence:

| Probe | Result |
|---|---|
| DB TCP listener `127.0.0.1:3307` | Reachable |
| API TCP listener `127.0.0.1:5012` | Reachable |
| Direct MariaDB connection using configured non-production environment | Blocked by DB auth / driver credential error |

Sanitized real HTTP evidence:

| Request | HTTP Status | API Code | Sanitized Result |
|---|---:|---:|---|
| `GET /api/v2/inventory/balances?count=5` | 400 | 1001 | DB auth / driver credential error |
| `GET /api/v2/inventory/movements?count=5` | 400 | 1001 | DB auth / driver credential error |
| `GET /api/v2/lots?count=5` | 400 | 1001 | DB auth / driver credential error |
| `GET /api/v2/lots/INVALID-LOT/trace` | 400 | 1001 | DB auth / driver credential error |
| `POST /api/v2/inventory/balances` | 405 | N/A | Method not allowed; read-only route preserved |

Authentication / permission evidence:

| Request | HTTP Status | API Code | Result |
|---|---:|---:|---|
| `GET /api/v2/inventory/balances?count=1` without `x-auth-token` | 400 | 2101 | Missing token parameter |

Bounded response evidence:

- All four authorized GET endpoints were reached through the real Flask HTTP service.
- The responses did not reach the payload contract validation layer because DB authentication failed before staging data could be read.
- No-data, invalid identifier, upstream incomplete, UOM Option B, and bounded row-count assertions could not be completed in this participant lane because the backend process could not authenticate to the synchronized non-production MariaDB runtime.

Observability evidence:

- `restserver.log` recorded request receipt for `CInventoryBalancesURI`, `CInventoryMovementsURI`, `CInventoryLotsURI`, and `CInventoryLotTraceURI`.
- `restserver.log` recorded the DB auth / driver credential error for the four GET requests.
- `restserver.log` recorded `missing token parameter` for the missing-token authentication check.

Safe Stop:

- Classification for this real HTTP retest lane remains `SAFE_STOP_DB_AUTH_OR_DRIVER_CREDENTIAL_BLOCKED`.
- Required completion path: Engineering A/B should either provide a usable non-secret connection method for this participant lane or execute the same four real HTTP requests in the environment where the synchronized DB credentials and synthetic package are valid.
- Boundaries preserved: no new endpoint, mutating endpoint, security boundary expansion, Production API, Production credential, migration, source mutation, Cutover, or ERP2.0 Go-Live.

## NEXT-013 Backend DB / Service Closure Addendum

Closure assignment:

- Authority: `ERP2-CTO-BACKLOG-ORCH-NEXT-013`
- Work item: `ERP2-NONPROD-PARTICIPANT-RUNTIME-ACCESS-001`
- Expected response package: `Backend-API-Response-ERP2-NONPROD-PARTICIPANT-RUNTIME-ACCESS-001-Backend-DB-Service-Closure-20260902-001.md`

Driver / service result:

| Check | Result |
|---|---|
| MariaDB Python driver | Available |
| SQLAlchemy | Available |
| Flask | Available |
| Backend local service | Started at `http://127.0.0.1:5012` |
| Backend -> DB direct probe | Failed: DB auth / driver credential error |

Sanitized real HTTP retest:

| Request | HTTP Status | API Code | Sanitized Result |
|---|---:|---:|---|
| `GET /api/v2/inventory/balances?count=5` | 400 | 1001 | DB auth / driver credential error |
| `GET /api/v2/inventory/movements?count=5` | 400 | 1001 | DB auth / driver credential error |
| `GET /api/v2/lots?count=5` | 400 | 1001 | DB auth / driver credential error |
| `GET /api/v2/lots/INVALID-LOT/trace` | 400 | 1001 | DB auth / driver credential error |
| `GET /api/v2/inventory/balances?count=1` without token | 400 | 2101 | Missing token parameter |
| `POST /api/v2/inventory/balances` | 405 | N/A | Method not allowed; read-only route preserved |

Closure classification:

`C - ACCESS REMEDIATION STILL REQUIRED`

Backend participant-side root cause:

`PARTICIPANT_CONSUMABLE_NONPRODUCTION_DB_CREDENTIAL_INJECTION_STILL_NOT_AVAILABLE_FOR_BACKEND_PROCESS`

UX real-backend smoke:

- UX should not run a real-backend PASS smoke test against this Backend service yet.
- UX may only validate unavailable/error UI behavior until Backend -> DB real HTTP payload evidence passes.

Command:

```powershell
python -m py_compile restserver/package/restserver/api/v2/inventory.py restserver/package/restserver/api/v2/inventory_uri.py restserver/package/restserver/app.py restserver/package/common/common.py restserver/tests/test_inventory_read_api.py
```

Result:

```text
Passed with no syntax errors
```

## Classification

`COMPONENT_IMPLEMENTED_PENDING_ENGINEER_RUNTIME_REVIEW`

The component-level implementation is complete and tested in isolated SQLite test fixtures. Engineer runtime verification against the intended non-production MariaDB environment remains outside this execution and should be performed separately.
