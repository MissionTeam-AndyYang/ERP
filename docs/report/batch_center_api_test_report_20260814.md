# Batch Center API Test Report - 2026-08-14

## Scope

- Implemented Batch Center V2 backend API.
- Verified API service logic and Flask route envelope.
- Confirmed no regression in existing Warehouse, BOM, Orders, Production and Purchasing pytest suite.

## Commands

```powershell
.\.venv\Scripts\python.exe -m pytest restserver\tests\test_batch_center_api.py -q
.\.venv\Scripts\python.exe -m pytest restserver\tests\test_warehouse_dashboard.py restserver\tests\test_bom_center_api.py restserver\tests\test_batch_center_api.py -q
.\.venv\Scripts\python.exe -m pytest restserver\tests -q
```

## Results

| Test Set | Result |
|---|---|
| `restserver/tests/test_batch_center_api.py` | 4 passed |
| Warehouse + BOM + Batch related tests | 25 passed |
| Full `restserver/tests` suite | 36 passed |

## Verified Items

- `GET /api/v2/batches/dashboard`
  - Field existence and summary aggregation.
  - Current, available, reserved and quality hold quantity calculation.
  - Item-level risk level and primary risk code.
  - Owner department from open workflow task.
- `GET /api/v2/batches/items/{item_no}/distribution`
  - Warehouse stock distribution row.
  - Production output distribution row.
  - `batchStageCode` remains String enum code.
  - `relatedDocuments[]` returns traceable document references.
- `GET /api/v2/batches/{batch_no}/detail`
  - Batch header.
  - Stock by warehouse.
  - Inventory records.
  - Reservations.
  - Quality holds.
  - Pallet movements.
  - Workflow tasks.

## Notes

- System Python does not include pytest. Tests were executed with the project `.venv`.
- No live MariaDB runtime verification was executed in this environment.
