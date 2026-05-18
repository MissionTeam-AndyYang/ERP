# Code Review Checklist

Use this checklist when reviewing code from another engineer before merging it into ERP 2.0.

## Intake Steps

Ask the engineer to provide one of:

- A GitHub branch in this repository.
- A pull request.
- A separate Git repository URL.
- A zip file, only if Git is not available.

Preferred flow:

```text
engineer branch -> review -> requested fixes -> tests -> merge
```

Avoid directly copying files into `main`.

## Initial Checks

Before reviewing code in detail:

- Confirm which branch or code snapshot is being reviewed.
- Check whether it is based on the latest `main`.
- Check whether it modifies backend, frontend, database, or docs.
- Run the relevant test/build commands.
- Identify any generated files, secrets, logs, build output, or dependencies that should not be committed.

## Backend Review

Confirm:

- The backend uses Flask API, not FastAPI.
- Endpoint files use Flask Blueprints.
- Service files contain business logic and database operations.
- Pydantic schemas are used for request/response validation.
- SQLAlchemy models are not casually edited without checking the baseline schema.
- Expected errors use `ApiError`.
- Upstream references are validated before creating linked workflow records.
- Tests cover both success and failure cases.

Required commands:

```powershell
cd backend
.\.venv\Scripts\python.exe -m ruff check app tests alembic
.\.venv\Scripts\python.exe -m pytest
```

## Frontend Review

Confirm:

- Routes follow the Next.js App Router structure.
- Shared components are reused where practical.
- Mock data is typed and separated from page components.
- API integration code is isolated in `src/services/`.
- UI remains consistent with the existing ERP operational dashboard style.
- Navigation still works from the sidebar.
- Responsive layouts do not overlap.

Recommended command:

```powershell
npm run build
```

## Database Review

Confirm:

- Changes are compatible with `docs/database/EWDB_20260517_3.sql`.
- New FK-like relationships are reflected in services and tests.
- Alembic migrations are included when schema changes are required.
- No schema change is made only inside generated model files without a migration or source SQL update.

## Workflow Review

For workflow-related changes, verify:

- `complete` remains correct.
- `missing_steps` moves forward when a CRUD node is created.
- Optional workflow nodes are documented.
- Dashboard/frontend logic uses backend workflow output rather than duplicating inconsistent rules.

Current required workflow tests:

- `order-to-production`
- `order-to-warehouse`
- `work-order-production-report`

## Merge Criteria

Code is merge-ready only when:

- Tests pass.
- Review findings are resolved or explicitly accepted.
- The branch is up to date enough to merge cleanly.
- Docs are updated for behavior, API, or convention changes.
- No local-only files or secrets are included.

## Common Rejection Reasons

Reject or request changes when code:

- Reintroduces FastAPI.
- Bypasses service-layer validation.
- Writes database logic directly in route handlers.
- Breaks existing workflow tests.
- Adds untyped or duplicated frontend data structures.
- Commits build output, venv files, logs, `.env`, or `node_modules`.
- Changes the database schema without a migration or documented reason.
