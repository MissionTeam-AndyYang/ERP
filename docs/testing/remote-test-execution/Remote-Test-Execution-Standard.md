# Remote Test Execution Standard

Status: READY FOR CTO REVIEW; preparation only
Version: 0.1

## Purpose

This standard defines a reusable, module-neutral protocol for bounded remote test execution. It does not grant database, migration, production, runtime, or credential authority.

## Execution modes

- `offline-static-validation`: inspect source, manifests, hashes, mappings, and runner behavior without contacting a target.
- `read-only-target-verification`: consume an approved current status evidence file; the runner never starts a service or opens a database connection.
- `manual-authorized-execution`: a named executor follows an approved runbook after all admission predicates pass. Database and migration operations remain separately authorized.

## Fail-closed controls

1. Target identity, environment, endpoint, authorization reference, executor, and run ID are mandatory.
2. Production, shared runtime, unrestricted endpoint, credential values, SQL text, migration execution, restore, restart, and cleanup commands are rejected by the automated runner.
3. The runner accepts only the module's explicit case allowlist.
4. A missing, stale, malformed, or contradictory status evidence file produces `BLOCKED`.
5. No result is inferred from a fixture, source check, mock, or historical report.

## Admission sequence

1. Verify source commit, runner commit, manifest and fixture hashes.
2. Verify target identity and non-production isolation using current read-only evidence.
3. Verify schema/revision, initial state, residual inventory, permissions, backup/recovery owner and cleanup owner.
4. Reserve a unique Run ID and evidence destination.
5. Execute only the approved case and record before/after state references.
6. Stop on the first predicate failure; do not repair the target during a run.
7. Complete owner-controlled cleanup/recovery and independent residual readback.

## Result vocabulary

`PASS` means the approved procedure completed and all assertions passed. `FAIL` means execution occurred and an assertion failed. `BLOCKED` means a prerequisite or authority predicate failed. `NOT_RUN` means the case was outside the selected run.

## Special case separation

Ordinary validation cases must not be represented as migration, concurrency, restart, restore, or recovery evidence. Such cases require their named authorization, owner and evidence fields even when a shared fixture is used.

## Safe stop

On any mismatch, unauthorized operation, missing recovery artifact, unexpected residual, or production/shared-system signal: emit structured `BLOCKED`, preserve raw evidence, perform no mutation, and hand off to the named owner.
