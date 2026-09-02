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
