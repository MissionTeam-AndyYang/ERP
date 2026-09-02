# Backend API Response - ERP2 WH INV NEXT-014 Real HTTP Retest

## Assignment

- Authority: `ERP2-CTO-BACKLOG-ORCH-NEXT-014`
- Work item: `ERP2-API-WH-INV-STAGING-ALIGN-001`
- Backend commit under test: `bcfddcf`
- Controlled DB window ID: `ERP2-WH-INV-NEXT014-DB-WINDOW-20260903-001`
- Dataset: `SYNTHETIC-WH-INV-INT-TEST-001`
- Test date/time: 2026-09-03 Asia/Taipei
- Service URL: `http://127.0.0.1:5016`
- Service classification: local development server for controlled non-production real HTTP retest only
- Staging mode: `ERP2_WH_INV_STAGING_MODE=1`

## Authorized Scope

Only these four existing read-only endpoints were retested:

| Endpoint | Method |
|---|---|
| `/api/v2/inventory/balances` | GET |
| `/api/v2/inventory/movements` | GET |
| `/api/v2/lots` | GET |
| `/api/v2/lots/{lot_code}/trace` | GET |

No Production access, migration, source mutation, new endpoint, mutating API, UOM conversion, source-of-truth transition, cutover, or Go-Live activity was performed.

## Authorized `np_*` Object Access Confirmation

The controlled DB window contained exactly the seven authorized `np_*` objects required for NEXT-014:

| Object | Row Count |
|---|---:|
| `np_stg_inventory_balance_snapshot` | 2 |
| `np_stg_inventory_movement` | 3 |
| `np_stg_lot_snapshot` | 2 |
| `np_xwalk_item_identity` | 2 |
| `np_xwalk_lot_identity` | 2 |
| `np_xwalk_uom` | 1 |
| `np_val_slice_validation_result` | 10 |

Post-HTTP DB boundary check:

```text
table_count_after_http=7
tables_after_http=[
  'np_stg_inventory_balance_snapshot',
  'np_stg_inventory_movement',
  'np_stg_lot_snapshot',
  'np_val_slice_validation_result',
  'np_xwalk_item_identity',
  'np_xwalk_lot_identity',
  'np_xwalk_uom'
]
formal_required_table_present_count=0
authorized_np_table_present_count=7
```

This confirms the real HTTP retest did not require or instantiate formal ERP operational tables.

## Four-Endpoint Real HTTP Result

| Endpoint | HTTP | API Code | Message | Payload Count | Elapsed |
|---|---:|---:|---|---:|---:|
| `/api/v2/inventory/balances` | 200 | 0 | success | 2 balances | 264 ms |
| `/api/v2/inventory/movements` | 200 | 0 | success | 3 movements | 18 ms |
| `/api/v2/lots` | 200 | 0 | success | 2 lots | 7 ms |
| `/api/v2/lots/WHINV-FG-LOT-001/trace` | 200 | 0 | success | 2 trace steps | 8 ms |

## Field / Contract Evidence

### `/api/v2/inventory/balances`

- `permissionCode`: `WH_INV_READ`
- `balanceId`: `BAL-SNAP-001`
- `warehouseNo`: `WH-SYN-01`
- `itemNo`: `WHINV-FG-001`
- `lotCode`: `WHINV-FG-LOT-001`
- `currentQuantity`: `125.5`
- `availableQuantity`: `125.5`
- `unit`: `公斤`
- `candidateCanonicalUomCode`: `KG`
- `qualityStatus`: `READY_FOR_READ_ONLY_API`
- `sourceProvenanceRef`: `SYNTHETIC_NON_PRODUCTION::TC-WH-INV-001`

### `/api/v2/inventory/movements`

- `permissionCode`: `WH_INV_READ`
- first returned movement: `MOV-STG-003`
- `category`: `TRANSFER`
- `source`: `NP_STAGING`
- `quantity`: `5.0`
- `unit`: `公斤`
- `candidateCanonicalUomCode`: `KG`
- `refCategory`: `NP_STAGING_SOURCE_DOCUMENT`
- `refNo`: `SYN-DOC-003`
- `sourceProvenanceRef`: `SYNTHETIC_NON_PRODUCTION::TC-WH-INV-004`

### `/api/v2/lots`

- `permissionCode`: `WH_INV_READ`
- first returned lot: `LOT-SNAP-001`
- `lotCode`: `WHINV-FG-LOT-001`
- `currentQuantity`: `125.5`
- `availableQuantity`: `125.5`
- `unit`: `公斤`
- `candidateCanonicalUomCode`: `KG`
- `qualityStatus`: `AVAILABLE_DISPLAY_ONLY`
- `sourceProvenanceRef`: `SYNTHETIC_NON_PRODUCTION::TC-WH-INV-003`

### `/api/v2/lots/WHINV-FG-LOT-001/trace`

- `permissionCode`: `WH_INV_READ`
- `batch.batchNo`: `WHINV-FG-LOT-001`
- `batch.itemNo`: `WHINV-FG-001`
- `batch.unit`: `公斤`
- `batch.sourceProvenanceRef`: `SYNTHETIC_NON_PRODUCTION::TC-WH-INV-003`
- `traceSteps[0].stepId`: `MOV-STG-001`
- `traceSteps[0].stepType`: `RECEIPT`
- `traceSteps[0].sourceProvenanceRef`: `SYNTHETIC_NON_PRODUCTION::TC-WH-INV-002`
- `traceSteps[1].stepId`: `MOV-STG-003`
- `traceSteps[1].stepType`: `TRANSFER`
- `traceSteps[1].sourceProvenanceRef`: `SYNTHETIC_NON_PRODUCTION::TC-WH-INV-004`

## Auth / Permission Evidence

Missing token result:

```text
GET /api/v2/inventory/balances without x-auth-token
HTTP 400
code=2101
message=missing token parameter
payload={}
```

Authorized GET requests used `x-auth-token` and returned `permissionCode = WH_INV_READ`.

## Read-only / Mutation Guard Evidence

POST rejection result:

```text
POST /api/v2/inventory/balances
HTTP 405 METHOD NOT ALLOWED
Allow: HEAD, OPTIONS, GET
```

No insert, update, delete, DDL, source mutation, or formal schema instantiation was performed.

## No-data / Invalid Identifier / Upstream Incomplete Evidence

Invalid lot trace result:

```text
GET /api/v2/lots/NO-DATA-CANDIDATE/trace
HTTP 400
code=1
message=record not found
payload={}
```

Validation ledger rows present in `np_val_slice_validation_result`:

```text
INVALID-ID-CANDIDATE|PASS_WITH_CONDITION|INFO|ROW_COUNT
NO-DATA-CANDIDATE|PASS_WITH_CONDITION|INFO|ROW_COUNT
UPSTREAM-INCOMPLETE-CANDIDATE|PASS_WITH_CONDITION|WARN|PROVENANCE
```

The API does not synthesize missing business data; upstream incomplete/no-data conditions remain represented by the controlled validation evidence.

## UOM Option B Evidence

- Source/display UOM returned as `公斤`.
- Candidate canonical UOM returned as `KG`.
- `canonical_quantity` remains unused for conversion.
- No conversion was performed by the API.

## Observability / Log Evidence

Development server access log confirmed the authorized requests and boundary checks:

```text
GET /api/v2/inventory/balances HTTP/1.1 200
GET /api/v2/inventory/movements HTTP/1.1 200
GET /api/v2/lots HTTP/1.1 200
GET /api/v2/lots/WHINV-FG-LOT-001/trace HTTP/1.1 200
GET /api/v2/inventory/balances HTTP/1.1 400
POST /api/v2/inventory/balances HTTP/1.1 405
GET /api/v2/lots/NO-DATA-CANDIDATE/trace HTTP/1.1 400
GET /api/v2/inventory/balances?itemCategory=1 HTTP/1.1 200
```

## Tests

Automated backend tests were rerun before real HTTP retest:

```text
78 passed
```

## Defects / Safe Stop

No blocking defect was found in the NEXT-014 controlled real HTTP retest.

Known bounded behavior:

- In `ERP2_WH_INV_STAGING_MODE=1`, `itemCategory` filter returns an empty result because the seven authorized `np_*` objects do not contain formal ERP item category semantics.
- Some response field values differ from formal ERP enum typing in staging mode, as documented in `docs/spec/api/inventory.md`; this preserves source staging semantics and avoids unauthorized semantic inference.

## UX Real-backend Smoke Retest Readiness

Ready for UX real-backend smoke retest against the same controlled non-production DB window, limited to the four authorized read-only endpoints and with `ERP2_WH_INV_STAGING_MODE=1`.
