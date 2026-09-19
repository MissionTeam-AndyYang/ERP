# Candidate A Heroku Non-Production Backend Runbook

## Scope

This runbook applies only to the structured Flask backend at `backend/app.main:app`.
It does not authorize a deployment, database migration, production access, or a change to application business behavior.

## Build and web-process contract

- Python runtime: `.python-version` declares Python `3.12`.
- Root dependency manifest: `requirements.txt`; it installs `./backend` and the Gunicorn WSGI server.
- Root `Procfile` declares one web process:

  ```text
  web: gunicorn --chdir backend --bind 0.0.0.0:$PORT app.main:app
  ```

- The process must bind to the platform-provided `PORT`; it must not rely on the local development port or Flask debug server.

## Non-secret configuration boundary

The authorized platform custodian may set configuration values only through the non-Production app configuration boundary. Names recognized by the structured backend are:

- `APP_NAME`
- `APP_ENV`
- `DEBUG`
- `API_PREFIX`
- `DATABASE_URL` (secret boundary; do not place its value in source, logs, or evidence)
- `DB_POOL_SIZE`
- `DB_MAX_OVERFLOW`
- `CORS_ORIGINS`

For staging, `APP_ENV` must identify the non-Production environment and `DEBUG` must be disabled. `DATABASE_URL` is optional for basic startup health only; it is required only when the authorized non-Production database dependency is in scope.

## Startup and health verification

After an authorized deployment, verify the deployed release using:

1. `GET /` returns HTTP 200 with `status: ok`.
2. `GET /api/v1/health` returns HTTP 200 with `status: ok` and the non-Production environment identifier.
3. If a non-Production database is expressly admitted, `GET /api/v1/health/db` returns HTTP 200 with `database: reachable`.
4. If no database dependency is admitted, the database endpoint may report `database: unreachable`; that result does not invalidate the two basic startup checks.

Do not use a database health check to trigger schema creation, migration, fixture mutation, or credential recovery.

## Release evidence, rollback, and custody

- Record the Git SHA supplied to the platform for the release and verify it against the approved immutable shared commit before declaring the release running.
- Record the prior non-Production release as the rollback candidate before any first deployment. If no prior release exists, record that rollback is unavailable rather than inferring one.
- A rollback must select a known prior release through the authorized platform custodian. It must not change source, database state, credentials, or Production/Actual systems.
- The platform owner/custodian retains account access, app ownership, configuration administration, credential rotation, and revocation. Deployment authority remains with CTO V2 only within a separately approved action.
