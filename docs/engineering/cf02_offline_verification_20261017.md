# CF-02 Offline Verification Report

Generated: 2026-10-17T10:55:01+08:00
Scope: isolated static/offline checks for this FM02 repository checkout.

| Check | Status | Command | Detail |
| --- | --- | --- | --- |
| git-diff-check | PASS | `git diff --check -- .` | Completed successfully. |
| frontend-lint | FAIL | `npm.cmd run lint` | Exited with code 1. See terminal output for diagnostics. |
| frontend-build | PASS | `npm.cmd run build` | Completed successfully. |
| backend-ruff | FAIL | `backend\.venv\Scripts\python.exe -m ruff check app tests alembic` | Exited with code 1. See terminal output for diagnostics. |
| backend-pytest | PASS | `backend\.venv\Scripts\python.exe -m pytest -p no:cacheprovider` | Completed successfully. |

Summary: PASS=3; FAIL=2; UNAVAILABLE=0.

## Supplementary bounded reference checks

| Check | Status | Evidence |
| --- | --- | --- |
| FM-02 migration contract pytest | PASS | 6/6 deterministic tests passed; no migration executed. |
| FM-02 C2 service pytest | PASS | 11/11 deterministic tests passed; no live database accessed. |
| Direct TypeScript check | FAIL | Five existing iterator/target errors under `tsc --noEmit --ignoreDeprecations 6.0`. |
| Frontend component tests | NOT_RUN | No supported component-test script or configuration is present in `package.json`. |

The Next.js production build completed in the approved local context, including
its internal TypeScript phase. The separate direct TypeScript command remains
FAIL because of the existing repository target/downlevel-iteration findings.

No live MariaDB, migration, credential store, production credential or
application runtime operation was used. Existing source findings were not
rewritten merely to force this foundation check to pass.

No dependency installation, global runtime change, database/migration execution, application-code edit, or evidence rewrite is performed by this entry point.
