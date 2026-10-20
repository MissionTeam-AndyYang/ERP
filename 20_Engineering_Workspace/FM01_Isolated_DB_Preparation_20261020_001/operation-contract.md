# FM-01 3342 Operation Contract

## Fixed Binding

- Target: `ERP2-FM01-FUNCTIONAL-NP-001`
- Database: `erp2_fm01_functional_np_001`
- Endpoint: `127.0.0.1:3342`
- Datadir: `20_Engineering_Workspace/FM01_Functional_NP_Target_Binding_20261007_001/data`
- Source lineage: `0001 -> 0002 -> 0003 -> 0004`
- Accepted source commit: `38efa0d5a45c6425cdb5139d27bdc682db5a49d1`

Any mismatch is `HOLD`; no fallback target, port, database, datadir, source copy,
or credential is allowed. Ports `3306`, `3341`, `3344`, and `3345` are explicit
negative controls.

## Review-Only Cross-Module Sequence

The Repository-controlled exchange records the following unverified sequence:
`Module-Isolated Validation 3342 -> Shared DEV Integration Candidate 3344 ->
System Integration Acceptance`. This is planning metadata only, not an adopted
operational procedure. Port `3345` is FM02 and remains untouched. Ownership,
credential/operator boundaries, Independent TEST evidence transfer, recovery
custody, and Git/Knowledge custody are documented in
`evidence/controlled-exchange/FM01-3342-TARGET-BINDING-ADDENDUM-20261020-001.md`.

## Authorization Gate

Every future side-effecting action requires a caller-provided Owner-host
execution-release JSON artifact. It must contain exact target binding,
per-stage allowlist, Owner identity, expiry, and a unique one-time nonce. The
wrapper atomically consumes the nonce under the target evidence directory and
rejects replay. Missing, expired, malformed, mismatched, or reused input is a
fail-closed `HOLD`; separate human confirmation is still required.

For this isolated non-production 3342 target only, CIO's effective signed-
manifest exception permits the bounded Owner-host Windows PowerShell and
CurrentUser-DPAPI mechanism already recorded in the accepted FM01 Owner-host
readback script. This exception is not a new PKI/trust-root platform and does
not extend to 3344, 3345, Production, or any other target. The target-specific
credential filename and owner context must be reused exactly from that accepted
script; no credential name may be invented or copied from FM02. Secret values
must remain only in the child-process environment at execution time and must
never appear in arguments, logs, reports, evidence, or chat.

Broader manifest controls remain required for any operation: exact target,
operation allowlist, execution window, operator identity, explicit human
confirmation for side-effecting stages, pre/post target/config/source/backup
checks, expiry/replay protection, least privilege, and fail-closed mismatch
handling. This package does not create or infer execution authority.

The preparation package does not invent authorization IDs, credentials, signatures,
or approval metadata. Secret values must never appear in arguments, logs, reports,
or evidence.

## Source-Only Capability Harness

`tools/fm01_3342_adapters.py` contains `SourceOnlyCapabilityHarness`, an
injected-fake, temporary-directory harness for source-level validation only. It
simulates start/readiness, stop, deterministic migration invocation
`0001 -> 0002 -> 0003 -> 0004`, backup with SHA-256 manifest, hash-verified
restore, isolated reset, fixture setup/cleanup ownership, and redacted evidence
generation. It never invokes a real process, client, database, SQL, Alembic,
credential, service, or target datadir.

This harness is TEST_ONLY simulation and source-level contract validation. It is
not runtime validation, does not prove target/database behavior, and does not
authorize any operation. The exact offline suite is:

`G1P313\\python-3.13.14\\python.exe 20_Engineering_Workspace\\FM01_Isolated_DB_Preparation_20261020_001\\tests\\test_runner_contract.py`

Current expected result:
`STANDARD_LIBRARY_CASES=24;PASSED=24;FAILED=0`

The harness is separate from the actual operational PowerShell entrypoints.
`tools/backup_3342.ps1`, `tools/restore_3342.ps1`, `tools/reset_3342.ps1`, and
`tools/safe_stop_3342.ps1` remain explicit fail-closed `HOLD` stubs. The
Owner-host stage wrapper is `tools/invoke_fm01_owner_stage.ps1`; its default
preflight/read-only mode does not invoke runtime, and every side-effecting mode
requires explicit human confirmation plus a future execution release. None do
start or stop services, invoke clients, access credentials, execute SQL/Alembic,
or mutate the target. Runtime execution remains blocked until the authorization
window, target-specific operator, and approved execution release are supplied
through the CIO-approved Owner-host context.

The generic trust-root blocker is superseded for this bounded 3342 exception.
The exception does not establish credential/operator capability in Engineering B
and does not authorize execution in this preparation session.

## Future Modes (all NOT RUN)

| Mode | Required pre/post checks | Required authorization | Current state |
|---|---|---|---|
| `backup` | process/config identity, target identity, dump exit status, file hash, post-state | `backup` | NOT RUN |
| `migrate` | backup first, source hashes, revision order, schema/readback, rollback plan | `migrate` | NOT RUN |
| `readback` | process/PID/config identity, target identity, read-only query contract, no secret output | `readback` | NOT RUN |
| `fixture` | deterministic fixture ID/owner, target identity, row/table readback, cleanup owner | `fixture` | NOT RUN |
| `restore` | approved backup hash, exact target/datadir, pre/post schema and revision, cleanup | `restore` | NOT RUN |
| `rollback` | approved rollback operation, backup/hash, revision and object readback | `rollback` | NOT RUN |
| `reset` | explicit reset approval, backup/hash, exact target/datadir, post-empty readback | `reset` | NOT RUN |
| `safe_stop` | PID path/config/process identity, graceful stop, timeout, final no-listener/no-process proof | `safe_stop` | NOT RUN |

Uncertainty, timeout, partial backup, ambiguous PID, mismatched executable/config,
unexpected listener, failed cleanup, or missing post-readback produces `HOLD` and
must not be force-terminated or silently retried.

Dedicated gated stubs exist at `tools/backup_3342.ps1`,
`tools/restore_3342.ps1`, `tools/reset_3342.ps1`, and
`tools/safe_stop_3342.ps1`. Each is an auditable fail-closed gate and currently
returns `HOLD`; none invokes a client, service, credential, or target.

## Fixture and Cleanup Ownership

Fixtures are synthetic, deterministic, FM-01-only, and owned by the authorized
Engineering B runtime operator for the approved window. Fixture IDs must be
recorded in evidence. No business or Production data is permitted. Cleanup is
performed only by the same authorized operator or explicitly named replacement;
ownership transfer must be recorded in the authorization manifest. A failed or
uncertain cleanup remains `HOLD`.

## Evidence

Evidence uses `evidence-contract.schema.json` and records status, target,
database, endpoint, datadir, source hashes, operator identity, custody role,
authorization ID, operation list, timings, exit status, backup hash, schema/table
readback, migration revision, and cleanup state. It must explicitly state
`live_operation_invoked=false` when preparation or a rejected operation is being
reported, and `secret_values_exposed=false`.

## Concrete Guarded Entrypoints

`tools/fm01_3342_entrypoint.py` is the concrete command entrypoint for plan,
status, start, safe_stop, migrate, backup, restore, reset, and fixture. It
validates manifest/source/target binding and returns `HOLD` by default because
no approved verifier, credential provider, process adapter, database adapter,
filesystem adapter, or evidence sink is configured here.

`SignatureVerifier` validates canonical UTF-8 JSON formed by removing
`signature` and serializing with sorted keys and compact separators. Only
`ECDSA-SHA256` and `RSA-PSS-SHA256` are accepted. Issuer and key ID are pinned
by the injected verifier; expired or revoked metadata is rejected. SHA-256 is
used for content integrity only, never as a signature algorithm. No trust root,
public key, certificate, issuer trust store, private key, or revocation service
is included.

`tools/target_secret_provider_interface.py` defines target-specific ephemeral
credential acquire/release without exposing secret values to command lines,
repository files, logs, evidence, or assistant output. `NoCredentialProvider`
always returns `HOLD`. CIO must approve custody role, injection mechanism,
rotation, expiry, revocation, and audit policy before runtime use.

## Host-effect boundary

The Python source-only providers and harness do not call host processes, MariaDB,
DPAPI, or network endpoints. The Owner-host PowerShell stage wrapper is the
separate operational boundary and is fully gated as described above. Tests in
this package are offline/synthetic only and do not prove runtime readiness.

## Owner-host exception and stage order

The effective CIO exception is limited to Owner-host Windows PowerShell,
CurrentUser-DPAPI, and target `127.0.0.1:3342` / database
`erp2_fm01_functional_np_001`. The verified launch config is
`20_Engineering_Workspace/FM01_Functional_NP_Target_Binding_20261007_001/runtime/my-erp2-fm01-functional-np-11410.ini`
with SHA-256
`D386B8D32CC2897D1C1DBEB0CC9DB62BDA365072F3434B6EDF5146506AE61A3D`.
The runtime binaries are under the approved MariaDB 11.4.10 installation path.

Copy/paste stage order is:

1. `TargetCheck` — read-only binding/config/source/hash checks; no runtime side effect.
2. `SafeStart` — changes runtime; NOT TO EXECUTE without a separate execution release.
3. `BackupRecoveryCheck` — may create/read backup artifacts; NOT TO EXECUTE without release.
4. `Migrations0001To0004` — changes database; NOT TO EXECUTE. Exact execution adapter is not admitted by this package.
5. `DbTests` — DB access; NOT TO EXECUTE and TEST evidence authority remains separate.
6. `EvidenceExport` — may write evidence; NOT TO EXECUTE against live results in this session.
7. `GracefulStop` — changes runtime; NOT TO EXECUTE without release.

`tools/invoke_fm01_owner_stage.ps1` is the bounded command wrapper. It is
fail-closed by default, rejects non-3342 targets, requires exact config/source
hashes, requires `-ConfirmHumanExecution` for side-effecting stages, and never
prints secrets. Recovery/restore is not allowed to target any datadir other
than the exact FM01 binding and remains NOT TO EXECUTE absent a specific
release.
