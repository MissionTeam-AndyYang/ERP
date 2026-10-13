# FM-02 C2 Engineering Adoption + Platform Recovery Admission Result

**Directive:** `CIO-GOV-ERP2-FM02-C2-PARALLEL-RECOVERY-20261013-001`  
**Scope:** fresh source adoption, bounded platform recovery, Independent TEST preparation  
**Environment:** isolated non-Production development target only

## 1. Consolidated checkpoint

`SOURCE ADOPTION = ACCEPT / SOURCE-ONLY`  
`DATABASE ADMISSION = BLOCKED / CREDENTIAL CALLABILITY AND APPROVED START PROCEDURE`  
`INDEPENDENT TEST = ACCEPTED FOR PREPARATION / TERMINAL VERDICT NOT ISSUED`  
`C2 PERSISTENT MIGRATION = NOT RUN`

The original source work remains historically attributed to CTO-orchestrated local sub-agent contexts. The new adoption context independently inspected and corrected one material source/API contract defect, then accepted the corrected source for source-only adoption. No database, credential, runtime, canonical-main, Production or persistent migration action was performed.

## 2. Fresh Engineering adoption

| Item | Evidence |
|---|---|
| Fresh adoption task identity | `01a13415-8e5e-7271-b407-9bc06fecde1e` (`Peirce`) |
| Formal organizational Engineering Task/Assignment | **NOT ESTABLISHED** by the available platform records; no organizational acceptance is fabricated |
| Source reviewed | `4c60ecce55941f861bb7d32db1071ee173660994` and resulting corrected source |
| Corrected commit | `4324c31bf2e34a3faa1413bca14022cf6bb4e30a` |
| Corrected tree | `8af3bd1c460db3923f6fc6487be7583ebda77367` |
| Worktree status | Clean |
| Source test result | `16 passed in 0.24s` using `pytest -p no:cacheprovider` |
| Adoption decision | `ADOPTION ACCEPT — source adoption only` |

### Corrected defect

The adoption review found a material mismatch:

- REST had accepted `PENDING`, `APPROVED`, `EXPIRED`, `REVOKED`.
- Migration 0005 constraints allowed `DRAFT`, `ACTIVE`, `INACTIVE`, `REJECTED`, `SUPERSEDED`.

The correction aligned the REST status vocabulary and overlap filters to migration 0005 and added focused negative tests. No migration or schema change was required. The obsolete status values are now rejected at the bounded service boundary.

Changed-file hashes:

- `04_Engineering/Application/ERP-2.0/restserver/package/fm02_c2/service.py` — `F3B6F0849F30226C580525D6EA4104B1757B292B82FEEE165BB0E01A17BECE01`
- `04_Engineering/Application/ERP-2.0/restserver/tests/test_fm02_c2_service.py` — `2BBC968184914F2F4096A6BC50D866741F65EBA97D9CB0E3ABF55A66B079608B`

The original 15-pass evidence, original implementation commit and the pre-correction recovery report remain preserved as historical evidence.

## 3. Independent TEST preparation

| Item | Evidence |
|---|---|
| Fresh TEST preparation task identity | `01a13415-bb8d-7b23-ad87-6bb7f853b587` (`Euler`) |
| Preparation status | `TEST ASSIGNMENT ACCEPTED FOR PREPARATION` |
| Terminal Independent TEST verdict | **NOT ISSUED** |
| Persistent execution | **BLOCKED pending Database Admission PASS** |
| Database/credentials/runtime accessed | **NO** |

The prepared test contract covers target/revision readback, 0004–0006 constraints, generated scope-key uniqueness, concurrency/idempotency, zero-row gate, downgrade/reapply, rollback, privilege denial, restart/readback and no-contact boundaries. These checks remain queued until authenticated target admission succeeds.

## 4. Platform recovery result

Target:

- `ERP2-DEV-MARIADB-001`
- database `erp2_functional_dev_001`
- `127.0.0.1:3344`
- datadir `20_Engineering_Workspace\\Database_Runtime\\ERP2-DEV-MARIADB-001\\data`
- MariaDB `11.4.10`

Verified status at this checkpoint: target stopped, listener absent, no `mariadbd` process identified.

Existing recovery evidence remains:

1. Approved start script failed because `Create named pipe failed: Access is denied`.
2. A bounded same-target TCP-only start reached `ready for connections`, but it was not sufficient for admission because no authenticated SQL session followed.
3. Approved DPAPI connection path failed under `SEATTLE\\andyy` with `ConvertTo-SecureString: Error occurred during a cryptographic operation`.
4. Secret-file owner was recorded as `Seattle\\CodexSandboxOffline`; no secret material was disclosed.
5. Target was safely stopped with the approved stop procedure.

The CIO directive permits the Platform Owner to evaluate an equivalent target-bound TCP-only start when named-pipe startup fails. That evaluation has evidence of process availability, but still requires a callable approved credential path and read-only SQL verification before it becomes an approved recovery route.

Not verified in the current checkpoint:

- authenticated SQL session;
- current Alembic revision and affected row counts;
- current grants and DDL denial;
- backup/reset/restore readiness;
- persistent migration execution.

## 5. Exact remaining external action

An authorized local Platform/Database operator or project owner must either:

1. run the target-bound start/readback procedure under the DPAPI-protecting Windows identity; or
2. approve a target-only, non-Production credential provisioning path with explicit credential custody, expiry/revocation, backup/reset and rollback controls.

No authentication bypass, uncontrolled rotation, privilege expansion, destructive reset or unrelated-system contact is allowed. No secret may be copied into ChatGPT, Codex messages or evidence.

## 6. Resume rule

Only after source adoption, target admission, authenticated readback, backup/reset verification and Independent TEST execution acceptance are all recorded may CTO resume the previously authorized C2 persistent migration/testing sequence. Migration 0006 remains subject to the separate zero/non-zero protected-data gate.

**Result:** `FM-02 C2 ENGINEERING ADOPTION + PLATFORM RECOVERY ADMISSION = SOURCE ADOPTION ACCEPTED / DATABASE ADMISSION BLOCKED / TEST PREPARATION ACCEPTED`
