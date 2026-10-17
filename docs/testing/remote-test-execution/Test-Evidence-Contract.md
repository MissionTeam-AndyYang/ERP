# Test Evidence Contract

Status: PROPOSED FOR CTO REVIEW; package contract only
Version: 0.1

Every run record must contain these fields. Values must be explicit; `unknown` is not a PASS.

| Field | Requirement |
|---|---|
| ModuleID | Stable module identifier |
| CaseID | Approved case identifier |
| RunID | Unique run correlation identifier |
| DesignVersion | Design or contract version under test |
| SourceCommit | Immutable source baseline |
| RunnerCommit | Commit containing the runner |
| TargetID | Approved target identity |
| Environment | Must identify non-production status |
| Executor | Named human or approved executor identity |
| AuthorizationRef | Governing authorization reference |
| StartTime / EndTime | ISO-8601 timestamps |
| FixtureHash | Hash of deterministic fixture manifest |
| Command | Exact bounded command or manual procedure reference; no secrets |
| BeforeStateRef | Readback evidence reference |
| AfterStateRef | Readback evidence reference, or `NOT_RUN` |
| RawEvidenceHash | SHA-256 of raw evidence |
| CleanupStatus | `PASS`, `FAIL`, `BLOCKED`, or `NOT_RUN` |
| RecoveryStatus | `PASS`, `FAIL`, `BLOCKED`, or `NOT_RUN` |
| ObservedResult | `PASS`, `FAIL`, `BLOCKED`, or `NOT_RUN` |

## Contract rules

- Credentials and secret values are never evidence fields.
- Fixture hashes identify inputs, not execution results.
- Canonical custody hashes are SHA-256 over `git cat-file blob <exact-commit>:<path>` bytes (LF/no BOM). Checkout and `git archive` bytes are diagnostic representations and must be recorded separately with their line-ending policy; they must never replace the canonical raw hash.
- A clean Windows checkout with `core.autocrlf=false` is the LF representation; `core.autocrlf=true` may produce CRLF checkout/archive bytes. Both are accepted only against their explicit representation hashes.
- Mock, static, source, and historical evidence must be labeled and cannot substitute for current database evidence.
- For concurrency, migration, restart, restore, or recovery cases, the case-specific owner and authorization must be recorded.
- A report must preserve the first failed predicate and the exact safe-stop action.
