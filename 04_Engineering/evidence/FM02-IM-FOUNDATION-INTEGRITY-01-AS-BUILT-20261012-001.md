# FM02-IM-FOUNDATION-INTEGRITY-01 — As-built evidence

## Assignment and custody

- Authorization: `CIO-GOV-ERP2-FM02-SPRINT02-EXECUTION-RESUME-20261012-001`.
- Supplement: `CIO-GOV-ERP2-FM02-SPRINT02-ENGINEERING-DELEGATION-20261012-001`.
- Work package: `FM02-IM-FOUNDATION-INTEGRITY-01`.
- Executor: Engineering executor with Database/Schema and Backend/API capability.
- Source: `Canonical_ERP2.0_Monorepo`, immutable HEAD `442170014e6b1d5df88a03f1371e7ddbe81cc67d5`.
- Source tree: `6295abc096bbc8269da721958b3ff6171530278c`.
- Isolated worktree: `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\FM02_Sprint02_Engineering_Execution_20261012_001`.
- Worktree state: detached at the source commit; canonical `main` remained dirty and was not cleaned, reset, or edited.

## Implemented files and hashes

| File | SHA-256 |
|---|---|
| `04_Engineering/Database/fm02_item_master_0003_integrity_foundation.sql` | `B748D7C8BC3EFFCD4A0A3B64FA71154C0240AF224D935BA3AD41485EA9A1E3DF` |
| `04_Engineering/Database/fm02_item_master_0003_integrity_foundation_down.sql` | `52A8DAE571DDE09F3E45B24723F0D8F6691D0E14AE484E63A5C835845118469F` |
| `04_Engineering/Application/ERP-2.0/restserver/package/fm02_foundation/foundation.py` | `1FA143C4199F0DC4713C2B40A53765A2FA7652D962281348105C3E5B396DA474` |
| `04_Engineering/Application/ERP-2.0/restserver/tests/test_fm02_foundation.py` | `6E6DB5B8143ED4BEDFEFC8C53B8B6803D8F8F71988245FFB0FD9D41D52B20BD2` |

## Delivered behavior

- Controlled `item_category` seeded with the five accepted primary categories and an FK-compatible `item.item_category_id` while retaining `primary_category` for POST/GET compatibility.
- `item.row_version` and `updated_by_assignment_id` added as the bounded audit/concurrency delta.
- `item_specification` combines independently versioned specification lineages and revisions with scoped uniqueness and effectivity checks.
- `item_approval` is append-only and idempotent by `(item_id, idempotency_key)` plus request fingerprint.
- `item_lifecycle_event` is append-only and linked to the approval record.
- Lifecycle transitions lock the Item row, enforce the expected row version, require business approval evidence, insert approval/event/current-state changes atomically, and roll back together on failure.
- Existing `POST /api/v1/items`, `GET /api/v1/items/{item_id}`, and `GET /api/v1/items` response behavior remains available. New bounded endpoints are specification creation and lifecycle transition under `/api/v1/items/{item_id}/...`.
- No Product/SKU, supplier/customer qualification, legacy backfill, full Multi-UOM, BOM, Inventory, Production, external callback, UI/CSS, Release, or Production behavior was added.

## Protected DEV preflight and target readback

- Target: `ERP2-DEV-MARIADB-001`.
- Database: `erp2_functional_dev_001`.
- Live listener: `127.0.0.1:3344`, MariaDB PID `30352`.
- Live identity: `Seattle`, `11.4.10-MariaDB`, `erp2_functional_dev_001`, `erp2_dev_migrator@127.0.0.1`.
- Pre-apply revision: `fm02_item_master_0002_business_names`.
- Pre-apply affected rows: `item=0`, `item_legacy_identifier=0`, `uom=5`.
- Backup: `backups/erp2_functional_dev_001-20261012-201455.sql`, SHA-256 `3A16BB2BA92616822CBCABE413B8F35D379AC019B24742CB8CB97CBFD8D31527`, 16,776 bytes.
- Post-apply revision: `fm02_item_master_0003_integrity_foundation`.
- Post-apply rows: `item=0`, `item_legacy_identifier=0`, `item_specification=0`, `item_approval=0`, `item_lifecycle_event=0`, `item_category=5`, `uom=5`.
- Checked listener set: DEV `3344` and DEV API `8087`; no `3342`/Track F listener and no Production endpoint was contacted.

## Verification commands and results

1. Read-only target status/connectivity and identity readback: PASS.
2. Target-only backup: PASS; hash recorded above.
3. Upgrade rehearsal from the target backup into a temporary local copy: PASS. Readback showed the new four tables, Item compatibility columns, and revision `fm02_item_master_0003_integrity_foundation`.
4. Downgrade rehearsal on the same temporary copy: PASS. Readback returned revision `fm02_item_master_0002_business_names`, zero new tables, and zero new Item columns. Primary target was unchanged during rehearsal.
5. Target-limited migration application and post-apply schema readback: PASS.
6. Engineering integration tests: `6 passed in 1.01s`.
7. App-role compatibility probe: PASS for bounded Item POST/GET readback with the existing `fm02_dev_app` role. No privileges were widened.

Test coverage includes positive compatibility, negative category/UOM validation, independent specification lineages, active-period overlap rejection, same-key replay, same-key conflicting fingerprint, row-version concurrency, approval/lifecycle atomicity, rollback after approval insertion, and technical-actor/business-authority rejection.

## Limitations and stop conditions

- The pre-existing `fm02_dev_app` credential was deliberately not widened. It can continue the Sprint-01 Item POST/GET compatibility path, while the new specification/lifecycle write path was verified in the controlled DEV engineering lane using the target-limited migrator credential. Any application-runtime activation of those new writes requires a separately approved least-privilege grant change.
- No Independent TEST Office acceptance, Repository custody receipt, Release, or Production action is claimed by this package.
- Stop and obtain a new decision if any affected table is no longer zero-row before downgrade/reapply, if the target identity/revision differs, if a non-DEV listener appears, if a new privilege grant is requested, or if scope expands beyond the listed foundation slice.
