# FM-01 Isolated DB Preparation

This package is preparation-only for the CTO-authorized target
`ERP2-FM01-FUNCTIONAL-NP-001` / `erp2_fm01_functional_np_001` / `127.0.0.1:3342`.

It contains copied, hash-verified migration sources, static target guards, and
synthetic checks. It does not start or stop MariaDB, connect to the target,
read DPAPI credentials, execute SQL/Alembic, or modify the target datadir,
runtime configuration, schema, or data.

The reviewable operation contract is in `operation-contract.md`. The
fail-closed planner and injected adapter are `tools/fm01_3342_runner.py` and
`tools/fm01_3342_adapters.py`; they require an injectable trust verifier and
executor. The default CLI has no trust anchor and rejects all manifests. The
dedicated backup/restore/reset/safe-stop entrypoints fail closed until a
separate CIO-approved executor is injected. The future modes `backup`,
`migrate`, `readback`, `fixture`, `restore`, `rollback`, `reset`, and
`safe_stop` remain `NOT RUN / REQUIRES SEPARATE CIO DB EXECUTION AUTHORIZATION`.
The `SourceOnlyCapabilityHarness` in `tools/fm01_3342_adapters.py` provides
test-only injected-fake paths for start/readiness, stop, deterministic 0001 to
0004 invocation, backup/hash manifest creation, verified restore, isolated
reset, fixture setup/cleanup, and redacted evidence generation. It uses only
temporary test directories and never invokes a real process, client, database,
SQL, Alembic, credential, or service. These behaviors are simulation and
source-level contract validation only; they are not runtime validation and do
not authorize any procedure.
The exact offline suite is:
`G1P313\\python-3.13.14\\python.exe 20_Engineering_Workspace\\FM01_Isolated_DB_Preparation_20261020_001\\tests\\test_runner_contract.py`
Expected result for the current package is
`STANDARD_LIBRARY_CASES=24;PASSED=24;FAILED=0`.
Signature fields are structural metadata only; this package does not
authenticate them. Package status remains `HOLD` for live operation readiness.
Offline test-only signature mechanics use an ephemeral fixture key solely to
prove valid/tampered payload behavior; this is not a trusted signer, public key,
issuer, or operational authority.

## CIO bounded Owner-host exception

For this isolated non-production target only, the effective CIO exception
permits the pre-existing Owner-host Windows PowerShell + CurrentUser-DPAPI
boundary from
`20_Engineering_Workspace/FM01_Functional_NP_Target_Binding_20261007_001/tools/Invoke-FM01OwnerHostReadback.ps1`.
It is limited to `127.0.0.1:3342` and database
`erp2_fm01_functional_np_001`; it does not extend to 3344, 3345, Production,
or FM02 secret reuse. DPAPI values are never printed, logged, passed on a
command line, or written to evidence.

Verified launch config:
`20_Engineering_Workspace/FM01_Functional_NP_Target_Binding_20261007_001/runtime/my-erp2-fm01-functional-np-11410.ini`

Config SHA-256: `D386B8D32CC2897D1C1DBEB0CC9DB62BDA365072F3434B6EDF5146506AE61A3D`.

## Copy/paste stage package

Run from the repository root. `TargetCheck` is read-only:

```powershell
& .\20_Engineering_Workspace\FM01_DB_Delivery_20261020_001\20_Engineering_Workspace\FM01_Isolated_DB_Preparation_20261020_001\tools\invoke_fm01_owner_stage.ps1 -Stage TargetCheck
```

The operational stage commands below are reusable only after a real CIO/CTO
execution-release JSON artifact exists and matches the exact target. The
artifact path is not a boolean token and must not be invented. Do not run these
commands in this preparation session.

```powershell
& .\20_Engineering_Workspace\FM01_DB_Delivery_20261020_001\20_Engineering_Workspace\FM01_Isolated_DB_Preparation_20261020_001\tools\invoke_fm01_owner_stage.ps1 -Stage SafeStart -ConfirmHumanExecution -ExecutionReleaseArtifact <REAL_RELEASE_JSON>
& .\20_Engineering_Workspace\FM01_DB_Delivery_20261020_001\20_Engineering_Workspace\FM01_Isolated_DB_Preparation_20261020_001\tools\invoke_fm01_owner_stage.ps1 -Stage BackupRecoveryCheck -ConfirmHumanExecution -ExecutionReleaseArtifact <REAL_RELEASE_JSON> -BackupPath <FM01_BACKUPS_PATH>
& .\20_Engineering_Workspace\FM01_DB_Delivery_20261020_001\20_Engineering_Workspace\FM01_Isolated_DB_Preparation_20261020_001\tools\invoke_fm01_owner_stage.ps1 -Stage Migrations0001To0004 -ConfirmHumanExecution -ExecutionReleaseArtifact <REAL_RELEASE_JSON>
& .\20_Engineering_Workspace\FM01_DB_Delivery_20261020_001\20_Engineering_Workspace\FM01_Isolated_DB_Preparation_20261020_001\tools\invoke_fm01_owner_stage.ps1 -Stage DbTests -ConfirmHumanExecution -ExecutionReleaseArtifact <REAL_RELEASE_JSON>
& .\20_Engineering_Workspace\FM01_DB_Delivery_20261020_001\20_Engineering_Workspace\FM01_Isolated_DB_Preparation_20261020_001\tools\invoke_fm01_owner_stage.ps1 -Stage EvidenceExport -ConfirmHumanExecution -ExecutionReleaseArtifact <REAL_RELEASE_JSON> -EvidencePath <FM01_EVIDENCE_PATH>
& .\20_Engineering_Workspace\FM01_DB_Delivery_20261020_001\20_Engineering_Workspace\FM01_Isolated_DB_Preparation_20261020_001\tools\invoke_fm01_owner_stage.ps1 -Stage GracefulStop -ConfirmHumanExecution -ExecutionReleaseArtifact <REAL_RELEASE_JSON>
```

Migration execution is specifically blocked because accepted source bytes and
hashes exist but this package has no exact approved DB/Alembic execution
adapter. The other stage implementations are real but remain unauthorized in
this session. `IdentityPreflight` is a read-only identity check, not a DB test
suite. `DbTests` remains HOLD because the accepted FM-01 DB catalogue contains
53 design cases but no approved executable DB test runner is available; no DB
TEST PASS is claimed. Independent TEST
evidence authority remains `DEFERRED / NOT RELEASED`. Restore/reset to the 3342
datadir is destructive and remains `NOT TO EXECUTE` without a specific release.

Repository-controlled exchange addendum:
`evidence/controlled-exchange/FM01-3342-TARGET-BINDING-ADDENDUM-20261020-001.md`.
It records the review-only sequence `3342 Module-Isolated Validation -> 3344
Shared DEV Integration Candidate -> System Integration Acceptance`, keeps 3345
FM02 untouched, and documents ownership, credential/operator boundaries, TEST
evidence transfer, recovery controls, and Git/Knowledge custody. It is
preparation-only, unverified, and not an adopted operational procedure.

The approved source lineage is `0001 -> 0002 -> 0003 -> 0004` from source
commit `38efa0d5a45c6425cdb5139d27bdc682db5a49d1` (tree
`6095d409859e89889c7fd02a285fbcc648d5196a`).

## Guarded Source Entrypoints

The concrete guarded operation entrypoint is `tools/fm01_3342_entrypoint.py`.
It accepts operation names but returns `HOLD` unless an approved verifier and
target-bound executor context are supplied. `tools/target_secret_provider_interface.py`
defines target-specific credential custody without retrieving or storing secret
values. `SignatureVerifier` requires canonical-payload asymmetric signing with
`ECDSA-SHA256` or `RSA-PSS-SHA256`, pinned issuer/key ID, and non-expired,
non-revoked metadata. No trust root, public key, certificate, or private key is
present in this package.
