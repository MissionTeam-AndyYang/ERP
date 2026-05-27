# Restserver And DB Recheck

Date: 2026-05-27
Engineer update commit: `f2cbc8f Update sql and Revise code to support wsgi`

## Baseline

| Area | Current baseline |
| --- | --- |
| Database | `docs/database/EWDB_20260526.sql` |
| Workflow | `docs/database/EWDB_20260522_WORKFLOW.md` |
| Backend app factory | `restserver/package/restserver/app.py` |
| Development entrypoint | `restserver/package/restserver/run.py` |
| WSGI entrypoint | `restserver/package/restserver/wsgi.py` |

## Summary

The engineer update was fast-forwarded from GitHub `main`. The backend now uses a Flask application factory and WSGI-compatible entrypoint. The new database file is present and keeps the same schema object counts as the previous `EWDB_20260522.sql` baseline.

## Static Verification

| Check | Result | Notes |
| --- | --- | --- |
| `EWDB_20260526.sql` exists | Pass | File located under `docs/database/`. |
| SQL table count | Pass | 79 `CREATE TABLE IF NOT EXISTS` statements. |
| SQL foreign key count | Pass | 118 `ALTER TABLE ... FOREIGN KEY` statements. |
| SQL unique key count | Pass | 73 `UNIQUE KEY` definitions. |
| Added/removed tables vs `EWDB_20260522.sql` | Pass | No table added or removed. |
| ORM class count | Pass | 79 `CTable*` classes in `restserver/package/dbwrapper/table.py`. |
| Python syntax compile | Pass | `python -m compileall -q restserver/package` completed successfully. |
| Runtime app factory | Pass | `backend/.venv/Scripts/python.exe scripts/verify_restserver_runtime.py` created the Flask app successfully. |
| Blueprint count | Pass | 26 blueprints registered. |
| Route count | Pass | 70 routes registered. |
| Heartbeat smoke | Pass | `/heartbeat` returned HTTP 200. |
| Local DB connection | Expected fail | No local DB server is installed on this machine; engineer-side DB runtime verification is still required. |

## Backend Architecture Change

| Previous | Current |
| --- | --- |
| `restserver/package/restserver/restserver.py` owned global Flask object `g_obj_flask` and direct `app.run`. | `restserver/package/restserver/app.py` exposes `create_app()`. |
| Script and WSGI concerns were combined. | `run.py` handles local/dev server; `wsgi.py` exposes WSGI `app`. |
| Verification script imported `package.restserver.restserver.g_obj_flask`. | Verification script now calls `package.restserver.app.create_app()`. |

## Code Review Notes

| Priority | Finding | Recommendation |
| --- | --- | --- |
| P2 | `CMaria.gen_connection_str()` appends host/database only when both `DB_USER` and `DB_PASSWORD` are non-empty. This is acceptable for the current credentialed `.env` path, but passwordless/local DB configurations would generate an incomplete URL. | Ask engineer whether passwordless DB is intentionally unsupported. If not, host/database should be appended regardless of credential presence. |
| P3 | `restserver.conf` still referenced old `restserver.py` in a commented example. | Updated the comment to reference `run.py`. |

## Local Runtime Verification Output

Command:

```powershell
backend\.venv\Scripts\python.exe scripts\verify_restserver_runtime.py
```

Result summary:

```txt
restserver.ok: true
orm_table_count: 79
orm_missing_required_tables: []
blueprint_count: 26
route_count: 70
heartbeat_status: 200
database.ok: false
database.error: Can't connect to server on 'localhost' (expected on this machine)
```

## Follow-Up For Engineer

Please confirm:

1. `EWDB_20260526.sql` is now the active DB baseline for subsequent API work.
2. `EWDB_20260522_WORKFLOW.md` remains the active workflow baseline unless a newer workflow file is provided.
3. Runtime verification should now use `create_app()` / `wsgi.py` rather than the deleted `restserver.py`.
4. Whether passwordless DB connection strings should be supported by `CMaria.gen_connection_str()`.
