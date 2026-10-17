# FM02 Item Master DB Test Execution Package

Date: 2026-10-18  
Executor: Test Engineering / ERP2 Integration Functional Validation  
Status: Preparation only; no DB, SQL, migration runtime or cleanup executed

## Package disposition

- `DB_TEST_PACKAGE=HOLD`
- `DB_EXECUTION=NOT_AUTHORIZED`
- `LIVE_DATABASE_VALIDATION=NOT_RUN`
- `TARGET_IDENTITY=HOLD`
- `INITIAL_STATE_AND_RESIDUAL=HOLD / NOT_VERIFIED`
- `CURRENT_REVISION=HOLD / NOT_VERIFIED`
- `PERMISSIONS=HOLD / NOT_VERIFIED`
- `BACKUP_RECOVERY=HOLD / NOT_VERIFIED`
- `CLEANUP_OWNERSHIP=HOLD / NOT_VERIFIED`
- Authoritative source baseline: commit `d73588f5e528538aa6b12225abdcd96884ac11ad`, tree `ba57e39f819f9c17146061fd5b21802a44998710`.
- Migration source-admission evidence: commit `7b9620a25713338c8e6a60a55de8685070fe8538`, tree `7d94dcae515683729490d34d94a373adbcd86892`, manifest SHA-256 `63375DD93BB2E8DB26F4785157B1997205104E2E5CAA31641E98227F9EDC5FE0`.

The named isolated target `127.0.0.1:3345` is currently not listening and no MariaDB process is running. No target, schema, database, credential, backup or cleanup authority has been admitted.

## Scope and counts

- Total DB-dependent cases: `19`.
- `ISOLATED_DB_ELIGIBLE=17`: TC01-TC09, TC13-TC18, TC22, TC24.
- `SHARED_RUNTIME_RESTRICTED=2`: TC10, TC11.
- `REQUIRES_ADDITIONAL_DB_AUTHORIZATION=19`.
- `PRODUCTION_RESTRICTED=0` in this package; Production remains explicitly excluded.
- TC19, TC20, TC21 and TC23 are accepted mock-only evidence and are not DB execution.

## Pre-run read-only admission predicates

Before any execution, Test Engineering must receive and independently verify all predicates below. A failed predicate is a safe stop.

1. Target identity equals the CIO-approved isolated non-production target; host, port, database and schema are recorded.
2. `127.0.0.1:3345` is listening only for the authorized target and the owning process is identified.
3. MariaDB process, version, datadir and configuration match the approved non-production target.
4. Current migration revision, schema fingerprint and table inventory are captured before fixtures.
5. Residual synthetic rows, locks, open transactions and prior test identifiers are zero or explicitly reconciled.
6. Target-scoped credentials and minimum permissions are recorded; no shared or production credential is used.
7. Backup/snapshot identifier, restore owner and recovery procedure are verified before mutation.
8. Fixture source files and hashes match the authoritative baseline and migration admission manifest.
9. Correlation IDs, Run IDs, executor identity and evidence destination are reserved.
10. Cleanup owner, rollback owner and post-run residual readback owner are named.

## Case matrix

All rows are `REQUIRES_ADDITIONAL_DB_AUTHORIZATION`. The listed source reference is the immutable baseline unless a case explicitly names the migration admission manifest.

| Case | Requirement | Classification | DB operation and fixture/reference | Expected before/after | Minimum permission | Cleanup/rollback | Stop conditions |
|---|---|---|---|---|---|---|---|
| TC01 | IM-01 valid Item compatibility | ISOLATED_DB_ELIGIBLE | Create/read synthetic Item; baseline `d73588f5...` / `ba57e39f...` | Before no test Item; after one governed Item and readback identity | Item schema/DML test role | Delete/reset synthetic scope; verify zero residual | Target mismatch, unexpected existing row, identity collision |
| TC02 | IM-01 invalid category/UOM | ISOLATED_DB_ELIGIBLE | Submit invalid category and UOM payloads | Before clean fixture; after validation errors and zero partial rows | Item validation DML | Roll back transaction; residual scan | Any invalid payload persists |
| TC03 | IM-02 specification lineage | ISOLATED_DB_ELIGIBLE | Create/read valid and stale specification lineage | Before no fixture; after valid lineage only, stale rejected | Item/specification DML | Reset fixture and verify lineage rows absent | Fingerprint or provenance mismatch |
| TC04 | IM-03 effectivity overlap | ISOLATED_DB_ELIGIBLE | Insert valid revision, overlapping interval, invalid factor | Valid revision persists; overlap/invalid rows absent | Item-UOM/specification DML | Roll back rejected attempts; remove valid fixture | Partial revision or overlap accepted |
| TC05 | IM-04 lifecycle idempotency | ISOLATED_DB_ELIGIBLE | Replay identical lifecycle request and conflicting key | One approval/event; replay no duplicate; conflict rejected | Lifecycle DML | Reset Item and audit rows | Duplicate event or changed replay result |
| TC06 | IM-04 lifecycle concurrency | ISOLATED_DB_ELIGIBLE | Two isolated transactions against same row/version | One winner, one deterministic conflict; no lost update | Transaction/locking test role | Roll back both branches; verify row/version | Deadlock without controlled recovery, lost update |
| TC07 | IM-05 rollback atomicity | ISOLATED_DB_ELIGIBLE | Valid transaction plus forced failure | Failed unit leaves no partial Item/audit state | Transaction rollback permission | Restore snapshot or rollback transaction | Destructive delete, partial commit, restore failure |
| TC08 | IM-06 technical actor rejection | ISOLATED_DB_ELIGIBLE | Technical-only actor, valid business approval, missing delegation | Technical actor rejected; valid distinct approval succeeds | Approval/provenance test role | Remove approval fixtures; audit residual scan | Unauthorized approval or privilege drift |
| TC09 | IM-12 migration lineage / upgrade-downgrade-reapply | ISOLATED_DB_ELIGIBLE | Verify 0003-0009 files/hashes, execute only after migration authorization | Ordered revision; guarded rollback; deterministic reapply; rows preserved | Explicit migration-runtime role | Snapshot restore and revision/table readback | Hash/path mismatch, destructive SQL, non-deterministic reapply |
| TC10 | IM-11 live shared FM-02 route | SHARED_RUNTIME_RESTRICTED | Named C3 endpoint only; no current target admitted | Separate shared-runtime authorization required; no execution in this package | Separate C3 route permission | Owner-controlled reset; not this package | Any shared endpoint contact under this package |
| TC11 | IM-06 application-runtime grant | SHARED_RUNTIME_RESTRICTED | Target-scoped grant/readback only under separate IAM authorization | Grant and effective role must match approved matrix | Separate IAM/credential authority | Owner-controlled revoke/readback; not this package | Any unauthorized grant or shared credential |
| TC13 | IM-01 permanent Item code non-reuse | ISOLATED_DB_ELIGIBLE | Reserve/replay/conflict/abandon allocation fixtures | Unique opaque code; replay idempotent; abandoned code never reused | Allocation DML | Reset allocation and Item fixtures | Reused code, duplicate allocation, residual allocation |
| TC14 | IM-02 name correction audit | ISOLATED_DB_ELIGIBLE | Original/corrected name and material identity-change payload | Append-only before/after audit; material change rejected | Item/audit DML | Remove Item and audit fixture | Missing before/after, mutable audit, partial mutation |
| TC15 | IM-03 base UOM lock | ISOLATED_DB_ELIGIBLE | Pre-use and post-use Item plus invalid UOM edit | Pre-use rule applies; post-use edit rejected without mutation | Item/UOM DML | Reset formal-use marker and Item | Locked field changes or marker drift |
| TC16 | IM-04 UOM conversion effectivity | ISOLATED_DB_ELIGIBLE | Fixed/catch-weight valid revision, overlap, invalid/unauthorized payload | Valid history persists; invalid/overlap/unauthorized rows absent | Item-UOM DML | Roll back invalid attempts; remove valid rows | Partial history or unauthorized catch-weight |
| TC17 | IM-05 lifecycle approval/successor | ISOLATED_DB_ELIGIBLE | ACTIVE approval, missing approval, SUPERSEDED successor, RETIRED Item | Only approved transition succeeds; successor required; terminal state stays terminal | Lifecycle/approval DML | Reset Item lifecycle and events | Transition without approval, terminal reactivation |
| TC18 | IM-06 business/technical separation | ISOLATED_DB_ELIGIBLE | Separate approver/executor and missing delegation fixtures | Technical executor cannot approve; missing delegation leaves no state | Approval/provenance DML | Remove approval/delegation fixtures | Actor conflation or audit gap |
| TC22 | IM-10 customer/supplier/package scope | ISOLATED_DB_ELIGIBLE | Customer A, Supplier X/Y, approval and package overlap fixtures | Approved X accepted; unapproved Y rejected; overlap rejected | Qualification/package DML | Remove all scoped rows; verify zero residual | Cross-customer leakage or duplicate active rows |
| TC24 | IM-12 migration lineage/rollback/recovery | ISOLATED_DB_ELIGIBLE | Complete admitted 0003-0009 chain, snapshots and row fixtures | Forward/rollback/reapply deterministic; no destructive deletion or partial revision | Migration/recovery role | Restore snapshot; post-run schema/row readback | Missing companion file, deletion, restore/reapply failure |

## Evidence and recovery requirements

Each case requires a unique Run ID, exact command, target identity, executor identity, fixture hash, pre/post readback, output hash, cleanup result and stop disposition. DB execution must be serialized by batch unless concurrency is the subject of TC06.

No case may proceed if the target is shared, production, unidentifiable, already dirty, missing a recoverable snapshot, or using credentials broader than the approved minimum.

## Explicit exclusions

- TC19, TC20, TC21 and TC23 mock-only evidence is not persistence or runtime evidence.
- No Production, shared runtime, live API, SQL migration runtime, restore, restart, cutover or Go-Live operation is included.
- No credentials, permissions, schemas, fixtures or source files may be created or changed by Test Engineering to make a case executable.
- `DB_EXECUTION=NOT_AUTHORIZED` and `LIVE_DATABASE_VALIDATION=NOT_RUN` remain in force.

## CIO authorization request

Authorize one resettable isolated non-production database target for the 17 `ISOLATED_DB_ELIGIBLE` cases only, with target-scoped minimum credentials, approved fixture custody, pre-run read-only admission, backup/restore ownership, cleanup ownership and post-run residual/schema/privilege readback. Authorize TC10 and TC11 only through a separate C3/shared-runtime/IAM decision. Do not authorize Production, shared runtime, SQL/migration runtime, restore/restart or Go-Live through this package without explicit additional approval.

Until that request is approved and every pre-run predicate passes, all 19 cases remain `REQUIRES_ADDITIONAL_DB_AUTHORIZATION`, with execution stopped safely.
