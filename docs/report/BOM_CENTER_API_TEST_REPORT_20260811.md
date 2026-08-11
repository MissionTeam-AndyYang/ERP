# BOM Center API Test Report 2026-08-11

## Scope

- `GET /api/v2/bom/dashboard`
- `GET /api/v2/bom/{bom_no}/detail`

## Verification

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest restserver/tests
```

Result:

- Total tests: 32
- Passed: 32
- Failed: 0

Route registration check:

- `/api/v2/bom/dashboard`: OK
- `/api/v2/bom/<bom_no>/detail`: OK

## BOM Center Cases Covered

1. Dashboard returns one row per BOM version and calculates effective / future / historical state counts.
2. Dashboard supports keyword filtering through BOM item data and version state filtering.
3. Detail defaults to the effective version and returns versions, direct `bom_item` rows, and `product_spec.bom_no` linked products.
4. Detail supports a specific `version` query and returns not found for missing BOM no.

## Notes

- Tests use SQLite in-memory tables for service-level validation.
- Runtime verification against MariaDB still requires the engineer's DB environment.
