# Backend API Response - ERP2 WH INV Adapter Performance Baseline

## Baseline ID

- Baseline ID: `ERP2-WH-INV-ADAPTER-PERF-BASELINE-001`
- Authority: `ERP2-CTO-BACKLOG-ORCH-NEXT-014`
- Backend code commit under observation: `bcfddcf`
- Local HEAD during measurement: `5836438`
- Scope: Engineering observation / optimization input only
- Date: 2026-09-03 Asia/Taipei

## Boundary Confirmation

No Product acceptance was reopened. No Production, migration, source mutation, Source-of-Truth transition, Cutover, Go-Live, Engineering Pull, Test Engineering activation, new endpoint, new DB object, Product contract change, UOM conversion, or scope/authority expansion was performed.

## Dataset Profile

The shared controlled DB window was already released at the time of this baseline run:

```text
table_count=0
np_present_count=0
```

Therefore, the measurement used a representative synthetic non-production component fixture with the same object profile as the accepted NEXT-014 dataset:

| Object | Rows |
|---|---:|
| `np_stg_inventory_balance_snapshot` | 2 |
| `np_stg_inventory_movement` | 3 |
| `np_stg_lot_snapshot` | 2 |
| `np_xwalk_item_identity` | 2 |
| `np_xwalk_lot_identity` | 2 |
| `np_xwalk_uom` | 1 |
| `np_val_slice_validation_result` | 10 |

## Measurement Method

- Method: component/shared DEV synthetic baseline.
- Runtime: local Python + SQLAlchemy against in-memory synthetic `np_*` tables.
- Repetition: 10 iterations per endpoint.
- Measured dimensions:
  - service-layer API latency;
  - SQLAlchemy DB query count;
  - DB query duration;
  - rows returned;
  - response payload size;
  - N+1 indication;
  - trace node count;
  - crosswalk lookup cost.

Because the shared DB window was no longer open, this report should be treated as adapter implementation baseline rather than shared-MariaDB latency benchmark. Recent real HTTP smoke evidence from the accepted retest showed all four endpoints returning HTTP 200 under the controlled DB window.

## Metric Table

| Endpoint | API Latency Avg | API Latency Max | DB Queries | DB Duration Avg | DB Duration Max | Rows Returned | Payload Size | Trace Nodes | N+1 Indication | Crosswalk Lookup Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| `GET /api/v2/inventory/balances` | 0.221 ms | 0.459 ms | 2 | 0.057 ms | 0.132 ms | 1 | 751 bytes | 0 | No | Included in join; no separate query |
| `GET /api/v2/inventory/movements` | 0.263 ms | 0.467 ms | 2 | 0.066 ms | 0.131 ms | 3 | 1871 bytes | 0 | No | Included in join; no separate query |
| `GET /api/v2/lots` | 0.218 ms | 0.348 ms | 2 | 0.057 ms | 0.103 ms | 1 | 831 bytes | 0 | No | Included in join; no separate query |
| `GET /api/v2/lots/{lot_code}/trace` | 0.194 ms | 0.401 ms | 2 | 0.027 ms | 0.107 ms | 1 batch | 1006 bytes | 2 | No | Included in join; no separate query |

## Query Shape Observation

| Endpoint | Query Pattern | Observation |
|---|---|---|
| `/api/v2/inventory/balances` | `COUNT(*)` + paged `SELECT` with joins to item, lot, UOM crosswalk | Fixed 2-query pattern; no per-row lookup |
| `/api/v2/inventory/movements` | `COUNT(*)` + paged `SELECT` with joins to item, lot, UOM crosswalk | Fixed 2-query pattern; no per-row lookup |
| `/api/v2/lots` | `COUNT(*)` + paged `SELECT` with joins to item, lot, UOM crosswalk | Fixed 2-query pattern; no per-row lookup |
| `/api/v2/lots/{lot_code}/trace` | lot overview `SELECT` + movement trace `SELECT` | Fixed 2-query pattern; trace node count driven by matching lot movement rows |

## Rows Scanned / Returned

Exact DB-level scanned row counts were not available in the component fixture. Practical scan risk is low for the current object profile because:

- all list endpoints use bounded `LIMIT/OFFSET`;
- all crosswalk reads are performed by joins rather than per-row lookups;
- DDL already defines indexes on item, lot, and UOM xwalk references;
- trace query is bounded by a single `lot_xwalk_id`.

For future larger shared-MariaDB tests, use `EXPLAIN` or MariaDB performance schema to collect estimated/actual scanned rows per query.

## Risk Classification

| Risk Area | Classification | Note |
|---|---|---|
| N+1 query risk | Low | All four endpoints use fixed two-query patterns |
| Crosswalk lookup cost | Low | Lookup cost is inside joins; no repeated per-row calls |
| Payload size | Low | Payload sizes are below 2 KB for current synthetic dataset |
| Trace expansion risk | Low for NEXT-014 | Trace endpoint only reads movement rows for a single matched lot |
| Pagination cost | Medium future risk | Large offsets may become inefficient if staging rows grow substantially |
| Count query cost | Medium future risk | Each list endpoint runs `COUNT(*)` plus page query; acceptable now, but may need review at larger scale |

## Targeted Optimization Candidate

Recommended as future targeted optimization input, not required for NEXT-014 closure:

1. For larger datasets, consider keyset pagination for movement and lot list endpoints to avoid high-offset scan cost.
2. Consider making total count optional for UI paths that do not need exact `total`, reducing list endpoint query count from 2 to 1.
3. For shared-MariaDB baselines, capture `EXPLAIN` plans to validate index usage on:
   - `np_stg_inventory_balance_snapshot.item_xwalk_id`
   - `np_stg_inventory_balance_snapshot.lot_xwalk_id`
   - `np_stg_inventory_movement.lot_xwalk_id`
   - `np_stg_lot_snapshot.lot_xwalk_id`
   - crosswalk primary keys.

No immediate code optimization is recommended before larger representative data exists.

## Material Safe Stop

No material Safe Stop is present for this performance baseline. The only limitation is that the shared controlled DB window was released before this baseline run, so measurements are component/shared DEV synthetic numbers rather than live shared-MariaDB latency numbers.
