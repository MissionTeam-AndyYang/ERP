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
Signature fields are structural metadata only; this package does not
authenticate them. Package status remains `HOLD` for live operation readiness.

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
