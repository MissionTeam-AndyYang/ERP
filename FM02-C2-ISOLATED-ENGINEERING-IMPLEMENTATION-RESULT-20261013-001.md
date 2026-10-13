# FM-02 C2 Isolated Engineering Implementation Result

**Directive:** `CIO-GOV-ERP2-FM02-PHYSICAL-FREEZE-C2-EXECUTION-20261013-001`  
**Baseline:** package 019 plus correction 020  
**Source branch:** `codex/fm02-c2-isolated-20261013-001`  
**Implementation commit:** `4c60ecce55941f861bb7d32db1071ee173660994`  
**Implementation tree:** `29b49939b28bab5552df87f4096ffc247b17f8cc`  
**Parent source commit:** `41e070a58c668505b91e5bcece778a87fc9725c5`  
**Parent source tree:** `f18f6fa7d0a4f8a8b60af3464ed6bc8da77b3c71`

## 1. Scope actually completed

Source-only isolated implementation completed for:

- migration `0004` — item-scoped supplier qualification and Item UOM reference contract;
- migration `0005` — supplier package, customer qualification, and item-specific UOM conversion;
- migration `0006` — zero-row-gated legacy mapping reconciliation;
- bounded Backend/REST validation service for customer qualification and Item-specific UOM conversion;
- isolated migration and service tests.

The implementation includes Option A `DECIMAL(38,18)`, `rounding_scale 0..18`, generated/sentinel customer scope normalization, parent-item transaction locking, effective-period overlap rejection, deterministic conflict/idempotency behavior, fail-closed approval evidence, and no global UOM fallback.

No database connection, DDL, migration execution, DML, credential use, grant, Product main merge, runtime integration, Production or Release action was performed.

## 2. Source admission

The authorized central source branch was read from GitHub and verified:

- branch: `codex/fm02-central-source-completion-20261013-001`;
- commit: `41e070a58c668505b91e5bcece778a87fc9725c5`;
- tree: `f18f6fa7d0a4f8a8b60af3464ed6bc8da77b3c71`;
- 0003 up blob: `f1e96bbd7a0ca13e2d50bfa0afe473a7156a464b`;
- 0003 down blob: `cc0cae5f96525e70bd391f366e96b40591daa0eb`.

The dirty canonical `main` was not modified. Work was performed only in the controlled worktree and implementation branch above.

## 3. Engineering validation

Command:

```text
python -m pytest 04_Engineering/Database/tests 04_Engineering/Application/ERP-2.0/restserver/tests/test_fm02_c2_service.py -q
```

Result: `15 passed`.

Python compilation of `package/fm02_c2` also passed. This is Engineering validation only; it is not Independent TEST certification.

## 4. Database admission result

Target candidate:

- target: `ERP2-DEV-MARIADB-001`;
- database: `erp2_functional_dev_001`;
- endpoint: `127.0.0.1:3344`;
- datadir: `20_Engineering_Workspace/Database_Runtime/ERP2-DEV-MARIADB-001/data`;
- MariaDB: `11.4.10-MariaDB`.

The approved start script first failed because MariaDB could not create the named pipe: `Create named pipe failed: Access is denied`, then aborted. A target-bound direct start with named-pipe creation omitted reached `ready for connections`, but the approved DPAPI-protected `fm01_dev_app` credential could not be decrypted in the current execution context (`ConvertTo-SecureString: Error occurred during a cryptographic operation`). No authenticated SQL session was established.

The target was safely stopped with the approved stop procedure; final status was `DEV_RUNTIME_NOT_RUNNING=TRUE`. Therefore:

- target identity: evidence-supported;
- persistent SQL readback: `NOT VERIFIED`;
- current revision/row counts: `NOT VERIFIED` in this execution;
- backup/reset admission: `NOT VERIFIED` for this execution;
- target-only DDL privilege: `NOT VERIFIED`;
- migration execution: `NOT RUN`;
- database admission: `FAIL / CREDENTIAL CALLABILITY AND APPROVED START PROCEDURE BLOCKED`.

No credential recovery, rotation, grant change, named-pipe policy change or authentication bypass was attempted.

## 5. Independent TEST and closure

Independent TEST was not dispatched because the persistent target admission gate did not pass. The 15 local tests remain Engineering evidence only. A fresh independent TEST context must verify the actual MariaDB version, generated-column behavior, nullable-scope uniqueness, concurrent locking, upgrade/downgrade/reapply, privilege denial, restart/readback and isolation after credential/target admission is repaired.

## 6. Safe-stop conditions

Resume only after all of the following are independently recorded:

1. target-bound MariaDB start/readback works through an approved procedure;
2. non-secret credential callability is restored for the assigned executor;
3. current revision and all affected row counts are read back;
4. backup/reset/restore and target-only privileges are verified;
5. fresh Independent TEST assignment is accepted.

No C2 DDL, migration, business-data backfill, Product merge, runtime integration, Production or Release may begin before those gates pass.

