# Item / Trace Dashboard Optimization Verification Report

## Scope

- `/api/v2/trace/dashboard`
- `/api/v2/items/dashboard`
- `/api/v2/items/{item_no}/detail`
- Warehouse item inventory quantity summary shared logic

## Change Summary

1. `/api/v2/trace/dashboard` now limits the first-version dashboard query scope to raw materials (`itemCategory=1`) and finished goods (`itemCategory=5`) when `itemCategory` is not specified.
2. If `/api/v2/trace/dashboard` receives an unsupported `itemCategory` for the first-version dashboard scope, it returns an empty result set instead of scanning unrelated batch categories.
3. `/api/v2/items/dashboard` and `/api/v2/items/{item_no}/detail` no longer accept or return `itemType`.
4. Item Center inventory quantity lookup now uses a lightweight Warehouse item-level inventory summary instead of building the full Warehouse Dashboard payload.
5. API documents and proposal/flow documents were updated to match the backend behavior.

## Performance Design Note

The previous Item Center flow used `CWarehouseInventoryContextBuilder.build()`, which created the full Warehouse Dashboard context before the Item Center could read item-level stock quantity. The new `query_item_inventory_summary()` path only queries the item-level stock fields needed by Item Center:

- `inventory_record` for current quantity and batch/warehouse counts.
- `warehouse_inventory_reservation` for reserved quantity.
- `warehouse_quality_hold` for quality hold quantity.

This avoids unnecessary risk, pallet, capacity, task, and trend calculations for Item Center screens.

## Verification

### Syntax Check

```text
.venv\Scripts\python.exe -m py_compile restserver\package\restserver\api\v2\items.py restserver\package\restserver\api\v2\trace.py restserver\package\restserver\api\v2\warehouse.py
```

Result: Passed.

### Targeted API Tests

```text
.venv\Scripts\python.exe -m pytest restserver\tests\test_items_v2_api.py restserver\tests\test_traceability_api.py
```

Result: 25 passed.

### Full Backend Tests

```text
.venv\Scripts\python.exe -m pytest restserver\tests
```

Result: 67 passed.
