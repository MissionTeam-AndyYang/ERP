# FM-02 C2 Database Admission & Persistent Engineering Test Result

**Directive:** `CIO-GOV-ERP2-FM02-C2-DB-FALLBACK-20261013-001`  
**Scope:** Route A recovery, conditional Route B evaluation, persistent C2 continuation  
**Environment:** non-Production only

## 1. Result

`FORMAL ENGINEERING ADOPTION = NOT VERIFIED / SOURCE-ONLY ADOPTION ACCEPTED`  
`ROUTE A = BLOCKED / EXISTING TARGET CREDENTIAL AND START PROCEDURE`  
`ROUTE B = EVALUATED / PLATFORM OWNER ACCEPTANCE REQUIRED BEFORE CREATION`  
`INDEPENDENT TEST = PREPARATION ACCEPTED / TERMINAL VERDICT NOT ISSUED`  
`PERSISTENT MIGRATION = NOT RUN`

No database target was initialized, no credential was created, and no MariaDB process was started in this continuation. The existing corrected source and prior evidence remain preserved.

## 2. Source adoption state

- Fresh adoption context: `Peirce`, task identity `01a13415-8e5e-7271-b407-9bc06fecde1e`.
- Corrected source commit: `4324c31bf2e34a3faa1413bca14022cf6bb4e30a`.
- Corrected tree: `8af3bd1c460db3923f6fc6487be7583ebda77367`.
- Source validation: `16 passed`.
- Adoption decision: `ADOPTION ACCEPT — source-only`.
- Formal organizational Engineering Task/Assignment: **NOT ESTABLISHED** by the available execution platform; original authorship remains attributed to CTO-orchestrated local contexts.

The corrected source includes the REST/migration 0005 status-vocabulary alignment and focused negative tests. No schema or migration source change was required.

## 3. Route A — existing target recovery

Existing target:

- Target: `ERP2-DEV-MARIADB-001`
- Database: `erp2_functional_dev_001`
- Endpoint: `127.0.0.1:3344`
- Engine: MariaDB `11.4.10`
- Datadir: `20_Engineering_Workspace\\Database_Runtime\\ERP2-DEV-MARIADB-001\\data`

Route A is bounded-blocked by already verified evidence:

1. The approved startup procedure failed at named-pipe creation with `Access is denied`.
2. A same-target TCP-only startup reached `ready for connections`, but did not establish admission because no authenticated SQL session followed.
3. The approved DPAPI connection path failed under `SEATTLE\\andyy` with `ConvertTo-SecureString: Error occurred during a cryptographic operation`.
4. The protected secret-file owner was recorded as `Seattle\\CodexSandboxOffline`.
5. The runtime was safely stopped; current status is listener absent and no target process.

No unchanged DPAPI retry was performed. No authentication bypass, secret disclosure, credential rotation, grant change or Windows-identity modification was attempted.

## 4. Route B — new isolated TEST target evaluation

The following is the minimum candidate identity for Platform Owner acceptance; it is a specification only and was **not created**:

| Field | Proposed bounded value |
|---|---|
| Target ID | `ERP2-FM02-C2-TEST-MARIADB-001` |
| Environment class | `LOCAL_DEV_PHASE1_ISOLATED_NONPRODUCTION / SYNTHETIC_ONLY` |
| Database | `erp2_fm02_c2_test_001` |
| Listener | `127.0.0.1:3345` |
| Datadir | `20_Engineering_Workspace\\Database_Runtime\\ERP2-FM02-C2-TEST-MARIADB-001\\data` |
| Engine | Existing bundled MariaDB `11.4.10` binary |
| Source reconstruction | Accepted FM-01/FM-02 migration source through verified 0003 baseline, then C2 0004–0006 only after admission |
| Data policy | Clean synthetic data only; no Production/Actual or protected DEV data copied |
| Credential policy | Fresh test credential through the authorized Platform credential process; no CTO/Engineering bypass |
| Access boundary | Loopback only; target database only; no Track F, Product shared runtime, Production or other listener |
| Backup/reset | Fresh backup, deterministic reset and restore verification before C2 admission |
| Shutdown | Target-bound stop procedure; listener/process absence must be proven |

### Existing targets not eligible for silent reuse

- `ERP2-OTF-P1A-LOCAL-RUNTIME-001` — P1-A schema/assignment boundary, port 3310.
- `ERP2-OTF-P1B-LOCAL-RUNTIME-001` — P1-B schema/assignment boundary, port 3311.
- `ERP2-OTF-P1C-LOCAL-RUNTIME-001` — P1-C schema/assignment boundary, port 3320.
- `ERP2-OTF-P1D-LOCAL-RUNTIME-001` — P1-D integration boundary, port 3330.
- `ERP2-OTF-P1D-TEST-RUNTIME-001` — P1-D TEST validation boundary, port 3331.

Their runbooks explicitly identify different assignments, databases, fixtures and domain surfaces. Reusing or relabeling any of them would violate the new-target and no-cross-domain-contact conditions.

### Route B admission still missing

Before any directory initialization, MariaDB startup, credential provisioning or schema reconstruction, the Platform Owner must accept this exact target specification and record:

1. host/listener/datadir ownership;
2. clean synthetic-only data boundary;
3. approved credential issuance and revocation process;
4. least-privilege policy;
5. backup/reset/restore procedure;
6. shutdown and cleanup procedure;
7. explicit no-contact boundary with `ERP2-DEV-MARIADB-001`, OTF targets, Track F, Product shared runtime and Production.

No such target-specific Platform Owner acceptance is present in the current evidence. Therefore Route B is evaluated but not admitted.

## 5. Independent TEST

Fresh TEST preparation context:

- Executor context: `Euler`.
- Task identity: `01a13415-bb8d-7b23-ad87-6bb7f853b587`.
- Status: `TEST ASSIGNMENT ACCEPTED FOR PREPARATION`.
- Terminal verdict: **NOT ISSUED**.

The queued test contract covers migration 0004–0006, generated scope-key uniqueness, concurrency/idempotency, downgrade/reapply, rollback, privilege denial, restart/readback and no-contact. Persistent execution remains gated on Route A or Route B admission.

## 6. Safe continuation condition

The next executable action is target-specific Platform Owner acceptance of Route B, or restoration of the original Route A DPAPI/start procedure under the authorized identity. Once one route passes admission, CTO may continue with authenticated revision/row-count/privilege/backup readback, then the bounded C2 migration and fresh Independent TEST. Migration 0006 remains subject to its zero/non-zero protected-data gate.

**Result:** `FM-02 C2 DATABASE ADMISSION & PERSISTENT ENGINEERING TEST RESULT = HELD / ROUTE B PLATFORM ACCEPTANCE REQUIRED`
