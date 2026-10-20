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

Every future mutating/runtime action requires a caller-provided, signed/approved
authorization manifest. The manifest must contain an authorization ID, exact
target binding, execution window, all four source hashes, operator identity,
credential-custody role, reviewer, signature/approval proof, and an explicit
operation allowlist. Missing, expired, unsigned, malformed, or mismatched input
is a fail-closed `HOLD`.

The trust verifier is injectable by design. No verifier/trust anchor is
configured in this package, so the default command-line planner rejects even a
syntactically valid manifest. A future CIO-approved execution context must
inject the verifier and the operation executor; this package does not create
or infer either authority.

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
`STANDARD_LIBRARY_CASES=10;PASSED=10;FAILED=0`

The harness is separate from the actual operational PowerShell entrypoints.
`tools/backup_3342.ps1`, `tools/restore_3342.ps1`, `tools/reset_3342.ps1`, and
`tools/safe_stop_3342.ps1` remain explicit fail-closed `HOLD` stubs. They do not
start or stop services, invoke clients, access credentials, execute SQL/Alembic,
or mutate the target. Runtime execution remains blocked until the authorization
verifier, target-specific operator, credential custody, and approved executor
are supplied through a separate CIO-approved context.

No approved signer, public key, certificate, issuer, or trust root was found in
the governed files inspected for this package. CIO must decide who may sign,
which trust root/certificate/issuer is authoritative, and the custody,
rotation, revocation, and expiry policy. Until then live authorization remains
fail-closed. Test-only ephemeral signature mechanics do not satisfy that
decision.

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
