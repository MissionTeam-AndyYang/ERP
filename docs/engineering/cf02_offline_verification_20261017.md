# CF-02 Offline Verification Report

Generated: 2026-10-17T18:06:50+08:00
Scope: isolated static/offline checks for this FM02 repository checkout.

| Check | Status | Command | Detail |
| --- | --- | --- | --- |
| git-diff-check | PASS | `git diff --check -- .` | Completed successfully. |
| frontend-lint | PASS | `npm.cmd run lint` | Completed successfully. |
| frontend-build | PASS | `npm.cmd run build` | Completed successfully. |
| backend-ruff | PASS | `backend\.venv\Scripts\python.exe -m ruff check app tests alembic` | Completed successfully. |
| backend-pytest | PASS | `backend\.venv\Scripts\python.exe -m pytest -p no:cacheprovider` | Completed successfully. |

Summary: PASS=5; FAIL=0; UNAVAILABLE=0.

## Supplementary bounded reference checks

| Check | Status | Evidence |
| --- | --- | --- |
| FM-02 migration contract pytest | PASS | 6/6 deterministic tests passed; no migration executed. |
| FM-02 C2 service pytest | PASS | 11/11 deterministic tests passed; no live database accessed. |
| Direct TypeScript check | PASS | `tsc --noEmit -p tsconfig.json` passed. |
| Frontend component tests | PASS | Vitest/Testing Library mock-only suite: 6/6 passed. |
| CF-01 validator | PASS | B02 boundary, B01–B06 coverage, FR coverage and read-only scope passed. |

The quality entry point was corrected to treat native informational stderr
warnings as non-failing when the underlying process exit code is zero.
Lint, Ruff, TypeScript, build, pytest and component checks now pass.

No global runtime change, database/migration execution, credential access,
production operation or evidence rewrite was performed by this entry point.
