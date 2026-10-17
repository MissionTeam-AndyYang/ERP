# Item Master Test Runbook

Status: READY FOR CTO REVIEW; no execution performed

## Scope

The approved DB package permits preparation for `TC01-TC09`, `TC13-TC18`, `TC22`, and `TC24` only. `TC10` and `TC11` remain shared-runtime/IAM restricted. TC19, TC20, TC21 and TC23 are mock-only evidence and are not DB execution.

## Required preflight

The named executor must obtain current evidence for:

1. `ERP2-FM02-C2-TEST-MARIADB-001`, database `erp2_fm02_c2_test_001`, endpoint `127.0.0.1:3345`, and owning process.
2. MariaDB version, datadir, configuration and current migration revision.
3. Schema fingerprint, table inventory, zero/reconciled residuals, locks and open transactions.
4. Minimum target-scoped read/test permissions without exposing credential material.
5. Snapshot/backup ID, recovery owner, cleanup owner and post-run residual reader.
6. Fixture source and SHA-256 manifest matching the admitted source baseline.

Any missing predicate is `BLOCKED`. Do not start or stop the service, restore a snapshot, run SQL, or alter the target as part of preflight.

## Manual case procedure

1. Reserve RunID and record executor and AuthorizationRef.
2. Run the offline runner against the case allowlist and current status evidence.
3. Capture before-state evidence before any authorized mutation.
4. Execute the exact case procedure from `FM02-ITEM-MASTER-DB-TEST-EXECUTION-PACKAGE-20261018.md` under the separate authorization.
5. Capture after-state evidence, raw evidence hash, cleanup status and recovery status.
6. Stop and report `FAIL` or `BLOCKED` on any unexpected row, identity, revision, grant, lock, residual, or recovery condition.

## Special cases

- TC06 is concurrency evidence and requires an explicitly authorized two-transaction procedure.
- TC09 and TC24 are migration/recovery evidence and require a separately approved migration-runtime and recovery owner.
- No ordinary case may be reported as migration, concurrency, restart, restore, or recovery evidence.

## Current package limitation

The target was observed stopped with no listener at `127.0.0.1:3345`. No DB execution is admitted until Platform/Host returns current target and ownership evidence.
