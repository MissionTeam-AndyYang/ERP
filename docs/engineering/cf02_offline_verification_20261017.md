# CF-02 Offline Verification Report

Generated: 2026-10-17T10:03:57+08:00
Scope: isolated static/offline checks for this FM02 repository checkout.

| Check | Status | Command | Detail |
| --- | --- | --- | --- |
| git-diff-check | PASS | `git diff --check -- .` | Completed successfully. |
| frontend-lint | UNAVAILABLE | `npm.cmd run lint` | eslint is absent from node_modules; npm ci was not run by this check. |
| frontend-build | UNAVAILABLE | `npm.cmd run build` | next is absent from node_modules; npm ci was not run by this check. |
| backend-ruff | UNAVAILABLE | `backend\.venv\Scripts\python.exe -m ruff check app tests alembic` | backend/.venv is absent; global Python was not used. |
| backend-pytest | UNAVAILABLE | `backend\.venv\Scripts\python.exe -m pytest -p no:cacheprovider` | backend/.venv is absent; global Python was not used. |

Summary: PASS=1; FAIL=0; UNAVAILABLE=4.

No dependency installation, global runtime change, database/migration execution, application-code edit, or evidence rewrite is performed by this entry point.
