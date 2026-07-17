# Production Dashboard API Test Report

## Scope

- `GET /api/v2/production/dashboard`
- `GET /api/v2/production/work-orders/{work_order_no}/detail`
- ORM mapping for `production_line_daily_capacity` and `production_line_downtime`
- Standard Flask API response envelope

## Verification Environment

- Python: project `.venv`
- Database: in-memory SQLite with SQLAlchemy ORM fixtures
- Test command: `.\.venv\Scripts\python.exe -m pytest -q restserver/tests`

## Result

| Test Scope | Result |
| --- | --- |
| Production Dashboard dedicated tests | PASS: 4 passed |
| Full restserver test suite | PASS: 24 passed |
| Python compile check | PASS |

## Covered Behaviors

- Latest `effectiveDate <= queryDate` daily capacity version is selected.
- Confirmed downtime intervals are merged, clipped to the query day, and deducted once.
- `baseCapacityMinutes`, `downtimeMinutes`, `dailyCapacityMinutes`, and remaining capacity are returned.
- Completed output without manufacturing inbound is distinguishable from `pending_inventory`.
- Material readiness does not become `ready` when APS/input data is insufficient.
- Production input, output, labor, machine, waste, loss, and labor cost fields are calculated.
- Missing labor wage data produces a `labor_cost_missing` alert.
- Both Production routes return the standard `{code, message, payload}` envelope.

## Residual Runtime Note

The local machine does not provide the engineer's MariaDB runtime dataset. The tests therefore validate ORM/query behavior and business calculations with SQLite fixtures. MariaDB runtime verification remains required after the engineer imports `EWDB_PRODUCTION_DASHBOARD_EXTENSION_20260715.sql` and runs the endpoint against the target database.

## 2026-07-17 Enum and Response-Code Review

- Shared Production enum values are centralized in `restserver/package/common/common.py`.
- Code-generated alert and readiness comments now return stable codes for frontend translation and localization; backend code contains no generated Traditional Chinese display strings.
- Alert construction is unified through `CProductionDashboardService.__alert()`.
- Python compile check: PASS.
- Full restserver test suite: PASS: 24 passed.
