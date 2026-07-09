# Orders Dashboard Backend API Test Report

Date: 2026-07-09

## Scope

Implemented and tested:

- `GET /api/v2/orders/dashboard`
- `GET /api/v2/orders/{order_no}/fulfillment`

Related implementation files:

- `restserver/package/restserver/api/v2/orders.py`
- `restserver/package/restserver/api/v2/orders_uri.py`
- `restserver/package/restserver/app.py`

Related specification files:

- `docs/spec/api/orders.md`
- `docs/spec/api-proposal/orders_dashboard_proposal.md`
- `docs/spec/api-proposal/orders_dashboard_flow_algorithm.md`

## Verification Command

```powershell
.\.venv\Scripts\python.exe -m pytest restserver\tests --junitxml docs\report\ORDERS_DASHBOARD_BACKEND_TEST_20260709.xml
```

## Result

```text
20 passed in 1.95s
```

## Key Checks

- Orders dashboard service returns summary, orders, shipments, deferred ATP/CTP fields, margin signals, payment signals.
- Orders fulfillment service returns workflow steps and dependencies.
- Route tests confirm existing API envelope: `code`, `message`, `payload`.
- Flask `create_app()` route check confirmed `/api/v2/orders/dashboard` and `/api/v2/orders/<order_no>/fulfillment` are registered.
- Existing Warehouse v2 tests still pass.
- Monthly payment due date implementation uses existing `g_cal_due_date` behavior through Orders service logic.

## Output Files

- `docs/report/ORDERS_DASHBOARD_BACKEND_TEST_20260709.xml`
- `docs/report/ORDERS_DASHBOARD_BACKEND_TEST_20260709.md`
