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
`STANDARD_LIBRARY_CASES=10;PASSED=10;FAILED=0`.
Signature fields are structural metadata only; this package does not
authenticate them. Package status remains `HOLD` for live operation readiness.
Offline test-only signature mechanics use an ephemeral fixture key solely to
prove valid/tampered payload behavior; this is not a trusted signer, public key,
issuer, or operational authority.

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
