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
