# Warehouse Analytics Backend API Test Report

Date: 2026-07-03

## Scope

Implemented and verified first-version read-only Warehouse Analytics backend APIs:

| API | Method | Status |
| --- | --- | --- |
| `/api/v2/warehouse/analytics/overview` | GET | PASS |
| `/api/v2/warehouse/analytics/value-trend` | GET | PASS |
| `/api/v2/warehouse/analytics/space-utilization` | GET | PASS |
| `/api/v2/warehouse/analytics/risk-breakdown` | GET | PASS |
| `/api/v2/warehouse/analytics/task-sla` | GET | PASS |

## Verification Commands

```powershell
.\.venv\Scripts\python.exe -m py_compile restserver\package\restserver\api\v2\warehouse.py restserver\package\restserver\api\v2\warehouse_uri.py
.\.venv\Scripts\python.exe -m pytest restserver\tests -q
```

## Result

```txt
17 passed in 2.45s
```

## Coverage Notes

| Area | Verification |
| --- | --- |
| Field existence | Service tests assert `kpi`, `valueTrend`, `spaceTrend`, `riskBreakdown`, `taskSla`, detail endpoint sections, and API envelope payloads. |
| Field value logic | Tests verify inventory value, used pallets, open tasks, deduplicated risk lot count, trend length, capacity utilization, top risk lot, and task SLA open/completed counts. |
| API route behavior | Flask blueprint smoke test verifies all five Analytics routes return existing API envelope format. |
| Frontend separation | Tests and implementation confirm `drilldownQuery` is not returned; frontend is responsible for query string composition. |
| Date-period rule | Implementation uses `date + period`; `dateFrom/dateTo` are not accepted as first-version Analytics query parameters. |
| Query timestamp rule | Task SLA department and overdue trend calculations use the query end timestamp instead of wall-clock now, so historical checks are reproducible. |

## Residual Runtime Risk

Tests use SQLite in-memory fixtures. Engineer runtime verification on MariaDB remains recommended after deployment because production data volume, indexes, timezone data, and MariaDB date behavior can differ from SQLite.
