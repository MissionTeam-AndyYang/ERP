# FM-02 C2 Engineering Executor Verification & Database Admission Recovery

**Directive:** `CIO-GOV-ERP2-FM02-C2-EXECUTION-RECOVERY-20261013-001`  
**Scope:** preserve source-only work; verify execution provenance; recover bounded database admission  
**Environment:** non-Production local development target only

## 1. Terminal disposition

`FM-02 C2 SOURCE = PRESERVED / PROVISIONAL EXECUTION PROVENANCE`  
`FM-02 C2 DATABASE ADMISSION = BLOCKED / CREDENTIAL CALLABILITY AND APPROVED START PROCEDURE`  
`FM-02 C2 INDEPENDENT TEST = NOT DISPATCHED / ADMISSION GATE NOT PASSED`

The source work and its 15 local Engineering tests are preserved. No persistent migration, DDL, DML, credential rotation, grant change, Product-main merge, runtime integration, Release or Production action was performed.

## 2. Actual execution provenance

| Required provenance element | Evidence-backed result |
|---|---|
| Formal Engineering Task ID | **NOT ESTABLISHED** in the available records for this execution |
| Formal Engineering Assignment ID | **NOT ESTABLISHED** in the available records for this execution |
| Actual technical execution | Two local bounded sub-agent contexts were used under CTO orchestration |
| Migration/source context | Local sub-agent `01a133ff-45d6-7683-b5c3-70dc78c09e0b` (`Leibniz`), migration contract/source-test scope |
| Backend/service context | Local sub-agent `01a133ff-468e-7ec1-ba4c-3cb172ac21cf` (`Locke`), backend/service/test scope; context was closed after bounded completion |
| Organizational Engineering Office acceptance | **NOT VERIFIED**; no formal task acceptance record was fabricated |
| CTO technical review | Verified source diff, corrected the bounded service implementation, reviewed the combined test result and committed evidence |
| Independent Engineering review | **NOT VERIFIED** |

Therefore the implementation is attributable to **CTO-orchestrated local execution with two identifiable sub-agent contexts**, but remains **provisional source work** until an authorized Engineering capability independently adopts, inspects and accepts it under a distinct Task/Assignment.

## 3. Source and evidence identity

| Artifact | Identity |
|---|---|
| Parent source commit | `41e070a58c668505b91e5bcece778a87fc9725c5` |
| Isolated implementation commit | `4c60ecce55941f861bb7d32db1071ee173660994` |
| Implementation tree | `29b49939b28bab5552df87f4096ffc247b17f8cc` |
| Evidence commit | `8b8c05b76a7727e239044a5248720a50a076da37` |
| Evidence tree | `04da4d228aaf4757cbfbc783f43312ba1007e701` |
| Engineering result report | `FM02-C2-ISOLATED-ENGINEERING-IMPLEMENTATION-RESULT-20261013-001.md` — SHA-256 `120663A5A05F06FF02928747218881A59484BCA57265C4235548D3D3D076C18E` |
| Existing evidence manifest | `FM02-C2-ISOLATED-IMPLEMENTATION-EVIDENCE-MANIFEST-20261013-001.json` — SHA-256 `F4B9C2A0D6758D332DD771F7BEFB5DC9F16B54A9C6EC7AE96DBB76656EB63DA5` |
| Repository custody | `ERP2-FM02-C2-ISOLATED-IMPLEMENTATION-CUSTODY-20261013-001`; Knowledge URI `ERP2-KNOWLEDGE:ERP2-FM02-C2-ISOLATED-IMPLEMENTATION-CUSTODY-20261013-001`; receipt SHA-256 `337FE485D6B1BA7E813A9CD121684F17D83649F38576BB52C20CA6C6FB033F40` |

The dirty canonical `main` was not changed. The implementation branch/worktree remains the isolated source surface.

## 4. Engineering validation versus Independent TEST

The bounded Engineering command completed with `15 passed`; Python compilation of `package/fm02_c2` also completed. These are technical source-validation facts only.

`Independent TEST = PENDING / NOT DISPATCHED`. It was not dispatched because the persistent target admission gate did not pass. No Engineering result is represented as Independent TEST certification.

## 5. Database admission recovery evidence

Target identity under review:

- Runtime target: `ERP2-DEV-MARIADB-001`
- Database: `erp2_functional_dev_001`
- Endpoint: `127.0.0.1:3344`
- Datadir: `20_Engineering_Workspace\Database_Runtime\ERP2-DEV-MARIADB-001\data`
- Engine: MariaDB `11.4.10`
- Final state after bounded attempt: `DEV_RUNTIME_NOT_RUNNING=TRUE`

### 5.1 Approved start path

The approved start script was verified by its recorded SHA-256:

`A1FF7AC8F6FEE9E4EAF58E97F3A7FA7512E240745BB6C802A564FB48A19E79CF`

It failed before normal availability because MariaDB could not create the named pipe: `Create named pipe failed: Access is denied`, followed by process abort. This is a concrete start-procedure permission failure.

### 5.2 Bounded operational recovery attempt

A same-target direct start omitting named-pipe creation reached `ready for connections` on port `3344`. This did not establish database admission because it was not the approved full start procedure and no authenticated SQL session followed.

The approved connection path then failed at DPAPI decryption with:

`ConvertTo-SecureString: Error occurred during a cryptographic operation`

The current Windows execution identity was `SEATTLE\\andyy`. The protected secret-file owner recorded in the local evidence was `Seattle\\CodexSandboxOffline`; filesystem access did not establish DPAPI decryption authority. No secret was printed, exported or transferred.

The target was stopped with the approved stop procedure and the listener/process absence was verified. No credential recovery, rotation, grant change, authentication bypass or unrelated-runtime action was attempted.

### 5.3 Readback status

| Admission item | Status |
|---|---|
| Target identity | Evidence-supported |
| MariaDB process/listener during bounded attempt | Observed, then safely stopped |
| Authenticated SQL session | **NOT ESTABLISHED** |
| Current Alembic revision | **NOT VERIFIED in this execution** |
| Current row counts | **NOT VERIFIED in this execution** |
| Current grants / DDL denial | **NOT VERIFIED in this execution** |
| Backup/reset/restore admission | **NOT VERIFIED in this execution** |
| Persistent migration 0004–0006 | **NOT RUN** |
| Database admission | **BLOCKED** |

Historical target handover material reports earlier successful operation, but it does not establish the prior Windows security identity or a currently callable authentication path. Historical assertions are retained as historical evidence and are not substituted for current readback.

## 6. Exact recovery requirement

The next safe action is one owner/platform-operated recovery step, not another unchanged client retry:

1. Run the existing approved local database start/readback procedure under the Windows/DPAPI-protecting execution identity, **or** have the authorized local owner provision a target-bound, non-secret-callable DEV credential path for the assigned executor.
2. Preserve the existing datadir and verify backup/reset readiness before any SQL readback.
3. Keep the operation limited to `ERP2-DEV-MARIADB-001` / `erp2_functional_dev_001` / `127.0.0.1:3344`.
4. Do not paste or reveal passwords, DPAPI material or decrypted credentials in chat or evidence.
5. Do not rotate credentials, alter grants, change authentication policy or change named-pipe policy under this directive; those require separate exact authority.

The accountable next owner is the authorized local Platform/Database operator or project owner who controls the DPAPI-protecting Windows context. The minimum approval is authorization to run that target-bound recovery path; it is not authority for schema migration.

## 7. Organization improvement record

Observed gap: the source execution used identifiable local sub-agent contexts, but no formal Engineering Task/Assignment acceptance record was available before coding. This is recorded as an **existing Organization Milestone 2 execution-provenance / task-binding defect candidate**. No separate remediation cycle or new governance gate was created by this recovery.

## 8. Resume gates

Resume C2 only after all are evidenced:

1. authorized Engineering capability adopts the source under a distinct Task/Assignment;
2. target-bound MariaDB start/readback works through an approved procedure;
3. approved credential callability is restored without disclosure or bypass;
4. current revision, row counts, grants and target-only DDL boundary are read back;
5. backup/reset/restore readiness is verified;
6. a fresh independent TEST Assignment is accepted.

Only then may the previously authorized bounded C2 migration/testing sequence be resumed.

**Result:** `FM-02 C2 ENGINEERING EXECUTOR VERIFICATION & DATABASE ADMISSION RECOVERY = SOURCE PRESERVED / PROVISIONAL; DATABASE ADMISSION BLOCKED; INDEPENDENT TEST PENDING`
