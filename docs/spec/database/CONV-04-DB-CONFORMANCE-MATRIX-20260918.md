# CONV-04 DB Conformance Matrix

Status: `CONV-04 DB RECONCILIATION = PASS / GATE ELIGIBLE`

This document records a bounded, documentation-only reconciliation of the committed database baseline, schema index, and ORM table inventory. It does not establish canonical schema authority, execute a migration, or authorize Production/Actual use.

## Provenance

| Item | Value |
| --- | --- |
| Dispatch | `ERP2-CTO-V2-CONV-04-DB-RECONCILIATION-ENG-B-001` |
| PM request | `ERP2-PM-REQ-20260918-POST-PHASE12-CONV04-CONV05-EXECUTION-001` |
| CIO authority | `ERP2-CIO-GOV-V3-DEC-20260918-POST-PHASE12-CONV04-CONV05-PARENT-EXECUTION-001` |
| Authorized branch | `codex/erp2-common-baseline-20260918-001` |
| Entry HEAD | `89b374109312720b3ff6669a9664fb0cf8f9a6ba` |
| Worktree | `C:/Users/andyy/Desktop/Codex-workspace/worktrees/ERP-2.0-common-baseline-20260918-001` |
| Baseline | `docs/database/EWDB_20260526.sql` |
| Baseline SHA-256 | `23520B547FFF2A55B2B2590C6B6CD5EB52C14C885DB74AAFA62012C0E3405643` |

## Deterministic Reconciliation

The SQL parser counted `CREATE TABLE` names in the baseline, the index parser counted `##` table headings, and the ORM parser counted `__tablename__` values in `restserver/package/dbwrapper/table.py`.

| Surface | Count | Result |
| --- | ---: | --- |
| `EWDB_20260526.sql` core tables | 79 | Baseline parsed successfully |
| `docs/spec/database/index.md` table headings | 89 | Current combined index |
| `table.py` ORM `__tablename__` values | 89 | Exact set match with index |
| Baseline tables absent from index | 0 | Pass |
| Index tables absent from ORM inventory | 0 | Pass |

The 10 index headings beyond the 79-table core baseline are:

`item_safety_stock`, `production_line_daily_capacity`, `production_line_downtime`, `warehouse_inventory_reservation`, `warehouse_pallet_movement`, `warehouse_quality_hold`, `warehouse_risk_rule`, `workflow_next_owner_rule`, `workflow_task_event`, `workflow_task_state`.

## Extension Applicability

| SQL document | SHA-256 | Reconciliation treatment |
| --- | --- | --- |
| `docs/database/EWDB_WAREHOUSE_DASHBOARD_EXTENSION_20260616.sql` | `2D325C80226D978C3C8B8A0E5864008F42B766D6AA29D1610C5DA62E2855437F` | Seven Warehouse/workflow extension tables; existing tables are not modified by the document. |
| `docs/database/EWDB_WORKFLOW_TASK_EVENT_EXTENSION_20260629.sql` | `4EA3C976CB7B354200003292D4351007C911456E0991B6AA224ADDA9709D24B0` | Adds `workflow_task_event`, already represented in the index and ORM inventory. |
| `docs/database/EWDB_WORKFLOW_TASK_EVENT_RENAME_NOTE_TO_COMMENT_20260630.sql` | `E1C24F185D707B419B5AB416D87D61C8C9EFBE1F85463DB8BB5E5EAFBC3BA352` | Historical column rename note; no table-count effect. |
| `docs/database/EWDB_PRODUCTION_DASHBOARD_EXTENSION_20260715.sql` | `A524CBF516553FF2F9319DC1272BF06FB54ACE506FA5A711B8D2F44BAC5E4FBD` | Adds `production_line_daily_capacity` and `production_line_downtime`, both indexed and modeled. |
| `docs/database/ERP2_ROUTING_PROCESS_FLOW_SHARED_DEV_TEST_SUPPORT_20260904.sql` | `1210BFA0C44693765ABEAA4AD580209CEEDBDBE25F41DDFA40C1BA8965E88E57` | Shared DEV bounded test-support overlay for existing routing tables; not a new index table and not a Production migration. |

Historical baseline documents remain preserved and were not edited: `EWDB_20260517.sql` (`A726BCEE006624040807B2A909629839F3E3473FED824EDF8061DDD5E8FC7435`), `EWDB_20260521.sql` (`E2780F01F992BD1E2BE649FD0D0DDF190E0855832986D98AF3A74B05955E471B`), and `EWDB_20260522.sql` (`4DBAF28BC00DA5C61B865AD74AB528F0BCDCDDD7BA75A26216CC9DAB5D118A3E`).

## Cross-Layer Candidate Mapping

This mapping records existing committed source references only. It is not an implementation or schema approval.

| Surface | Existing source/API evidence | Referenced table/model groups | DB conformance status |
| --- | --- | --- | --- |
| Product/WIP 360 | `restserver/package/restserver/api/v2/product_wip_360.py`; read-only Product/WIP composition | `contract`, `inproduct`, `product`, plus delegated item/BOM/recipe/routing/warehouse models | Core baseline plus existing extension references; no DB change in CONV-04 |
| Packaging | `restserver/package/restserver/api/v2/packaging_specification.py`; read-only Packaging visibility | `bom2`, `bom2_number`, `inproduct`, `product`, `product_bom_spec`, `product_spec` | Core baseline; no write or schema change in CONV-04 |
| Inventory/Warehouse | `restserver/package/restserver/api/v2/inventory.py`, `warehouse.py`; read-only query surfaces | Core inventory models plus `warehouse_inventory_reservation`, `warehouse_quality_hold`, `warehouse_pallet_movement`, `warehouse_risk_rule`, `workflow_task_state`, `workflow_next_owner_rule`, `workflow_task_event` | Core plus Warehouse/workflow extensions represented in index and ORM |
| Trace | `restserver/package/restserver/api/v2/trace_uri.py`; `GET /api/v2/trace/dashboard` and `GET /api/v2/trace/batches/{batch_no}/overview` | `batch_number`, `inventory_record`, `production_data`, `production_data_input`, `production_data_output`, `goods_receipt_note`, `warehouse_quality_hold`, `workflow_task_event` | Core plus existing extension references; no runtime invocation or DB access in CONV-04 |
| Manufacturing Definition | Frontend binding in `src/services/manufacturing-definition-api.ts`; proposed `GET /api/v2/manufacturing-definition/overview` | Candidate composition is documented by the frontend/proposal; backend implementation is absent at the authorized entry HEAD | Not a DB implementation in this worktree; deferred for separate authority and execution |

## Validation and Boundaries

- `git status --short --untracked-files=all` was clean at entry.
- No SQL file, ORM model, API source, frontend source, test, fixture, dependency, runtime configuration, schema, credential, IAM, network, Production/Actual state, or remote state was modified.
- No migration, database connection, runtime startup, reset, push, fetch, pull, merge, rebase, reset, clean, or protected-main operation was performed.
- `PHASE 12 CLOSED WITH CONDITIONS` is preserved.
- CONV-05, CONV-07, L5, Product Version 3, Migration, Source-of-Truth transition, Cutover, and Go-Live are outside this result.
