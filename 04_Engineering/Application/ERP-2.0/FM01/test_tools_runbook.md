# FM-01 Test Tools Runbook

## Scope

The source tool supports deterministic non-DB fixture checks and report
generation. It does not replace the approved 53-case test plan and does not
claim test execution, runtime readiness, or database readiness.

## Non-DB runner

Use `run_non_db_cases()` with explicit `TestCase` objects and in-memory
fixtures. Each case produces `PASS` or `FAIL`; the aggregate report is
`PASS` only when every supplied case passes.

## Remote DB runner

`RemoteDbTestRunner` is intentionally fail-closed. Without an explicitly
authorized target and credential provider it returns `NOT_RUN`. Even when
bindings are supplied, `execute()` remains disabled until a separate
Runtime/Remote DB authorization is recorded.

No credentials, hosts, ports, database names, or target identifiers are stored
in source or fixtures.

## Evidence and cleanup

`build_evidence()` records the caller-provided commit/tree, result status,
limitations, Test Engineering status, and a deterministic hash of the report
payload. `write_report()` writes only to a caller-selected path. Fixture
cleanup is the caller's responsibility and must be deterministic; no live or
governed data may be used.

## Classification

- Tool source: implemented at source level.
- Non-DB execution: available only when explicitly invoked by an authorized test stage.
- Remote DB execution: `NOT_RUN` / runtime authorization required.
- Test Engineering: `DEFERRED / NOT RELEASED`.
