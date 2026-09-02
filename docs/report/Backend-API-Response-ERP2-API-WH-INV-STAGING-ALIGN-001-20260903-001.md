# Backend API Response - ERP2-API-WH-INV-STAGING-ALIGN-001

## Work Item

- Work item: `ERP2-API-WH-INV-STAGING-ALIGN-001`
- Authority: `ERP2-CTO-BACKLOG-ORCH-NEXT-014`
- Scope: existing Warehouse/Inventory read-only API staging alignment
- Date: 2026-09-03

## Authorized Endpoint Scope

Only the following existing read-only endpoints were changed:

| Endpoint | Method | Result |
|---|---|---|
| `/api/v2/inventory/balances` | GET | Staging read path implemented |
| `/api/v2/inventory/movements` | GET | Staging read path implemented |
| `/api/v2/lots` | GET | Staging read path implemented |
| `/api/v2/lots/{lot_code}/trace` | GET | Staging read path implemented |

No new endpoint, mutating behavior, production migration behavior, UOM conversion, security expansion, or new DB object was introduced.

## Root Cause

The prior V2 inventory implementation still delegated to formal ERP ORM services/tables:

- `inventory_item_month_statistic`
- `inventory_delta`
- `inventory_record`
- `batch_number`
- related formal Warehouse/Traceability tables

During the controlled non-production retest window, only the authorized `np_*` staging/crosswalk/validation objects were available. Because the implementation required formal ERP tables, the real HTTP test path failed before producing valid endpoint payloads.

## Implementation Approach

Added a bounded controlled staging path behind environment flag:

```text
ERP2_WH_INV_STAGING_MODE=1
```

When the flag is not enabled, existing formal ERP behavior remains unchanged. When enabled:

- the four authorized endpoints use `CInventoryStagingReadService`;
- the implementation reads only the seven authorized `np_*` objects;
- the code uses SQLAlchemy textual read queries without defining ORM classes for `np_*`;
- the staging path does not call `CDBMgr`, so it does not trigger ORM `create_all`;
- only rows with `validation_state = READY_FOR_READ_ONLY_API` are returned;
- zero-quantity balance/lot rows are filtered;
- `itemCategory` filter returns an empty set in staging mode because the authorized `np_*` objects do not contain a formal item category field;
- UOM Option B is preserved: source/display UOM is returned, candidate canonical UOM is metadata only, and no quantity conversion is performed.

## Authorized Data Object Use

| Object | Use |
|---|---|
| `np_stg_inventory_balance_snapshot` | Balance endpoint staging source |
| `np_stg_inventory_movement` | Movement and lot trace staging source |
| `np_stg_lot_snapshot` | Lot list and lot overview staging source |
| `np_xwalk_item_identity` | Source/candidate item identity metadata |
| `np_xwalk_lot_identity` | Source/candidate lot identity metadata |
| `np_xwalk_uom` | Source display UOM and candidate canonical UOM metadata |
| `np_val_slice_validation_result` | Validation evidence object, retained within authorized object scope |

## Files Changed

| File | Purpose |
|---|---|
| `restserver/package/restserver/api/v2/inventory.py` | Added bounded staging read service and staging-mode dispatch for the four existing endpoints |
| `restserver/tests/test_inventory_read_api.py` | Added component tests for staging read path, zero-quantity filtering, UOM Option B, bounded lot trace, and DB manager bypass |
| `docs/spec/api/inventory.md` | Updated formal API document to describe NEXT-014 controlled staging path and field behavior |
| `docs/report/Backend-API-Response-ERP2-API-WH-INV-STAGING-ALIGN-001-20260903-001.md` | Completion and verification package |

## Tests

Command:

```text
cd restserver
..\.venv\Scripts\python.exe -m pytest tests -q
```

Result:

```text
78 passed
```

Component coverage added:

- `/api/v2/inventory/balances` staging payload uses `np_stg_inventory_balance_snapshot`;
- `/api/v2/inventory/movements` staging payload uses `np_stg_inventory_movement`;
- `/api/v2/lots` staging payload uses `np_stg_lot_snapshot`;
- `/api/v2/lots/{lot_code}/trace` staging payload uses `np_xwalk_lot_identity`, `np_stg_lot_snapshot`, and `np_stg_inventory_movement`;
- zero-quantity balance/lot rows are filtered;
- source/display UOM is preserved as `公斤`;
- candidate canonical UOM is returned as metadata (`KG`) without conversion;
- staging mode bypasses formal `CDBMgr`.

## Controlled DB Access Evidence

Wrapper direct DB access succeeded, but the current controlled DB window no longer contains the seven authorized `np_*` objects:

```text
np_table_count=0
np_stg_inventory_balance_snapshot_present=0
np_stg_inventory_movement_present=0
np_stg_lot_snapshot_present=0
np_xwalk_item_identity_present=0
np_xwalk_lot_identity_present=0
np_xwalk_uom_present=0
np_val_slice_validation_result_present=0
```

Because the authorized staging objects are currently absent, final real HTTP retest against the shared controlled DB window was not executed in this pass.

## Four-Endpoint Result

| Endpoint | Component Result | Shared Controlled DB HTTP Result |
|---|---|---|
| `/api/v2/inventory/balances` | PASS | Safe Stop: authorized `np_*` tables absent |
| `/api/v2/inventory/movements` | PASS | Safe Stop: authorized `np_*` tables absent |
| `/api/v2/lots` | PASS | Safe Stop: authorized `np_*` tables absent |
| `/api/v2/lots/{lot_code}/trace` | PASS | Safe Stop: authorized `np_*` tables absent |

## Auth / Permission / Read-only Confirmation

- Existing route auth behavior is unchanged.
- Permission code remains `WH_INV_READ`.
- The API remains GET-only.
- No insert, update, delete, DDL, ORM `np_*` class, or auto-create behavior was added for the controlled staging path.

## Contract Drift

Controlled staging path preserves existing field names where possible. The following field value differences are intentional and documented:

- `unit` may be a source display UOM string such as `公斤` in staging mode, because the authorized `np_*` staging model preserves source UOM rather than formal ERP unit enum.
- `category`, `source`, and `refCategory` may be staging source codes in movement results.
- `candidateCanonicalUomCode` and `sourceProvenanceRef` are included in staging responses as controlled metadata.
- `itemCategory` and `itemSubCategory` are returned as `0` in staging rows because the authorized `np_*` objects do not contain formal item category semantics.

## Remaining Defect / Safe Stop

No component-level code defect remains for the authorized staging path. Final shared DB HTTP retest is blocked until the controlled test DB window again contains the seven authorized `np_*` objects.

## Readiness for Controlled Retest

Ready for controlled retest when Engineering/CTO opens or reloads the seven authorized `np_*` staging/crosswalk/validation objects. Retest should start the backend with:

```text
ERP2_WH_INV_STAGING_MODE=1
```

and use the existing `x-auth-token` / `WH_INV_READ` read-only access path.
