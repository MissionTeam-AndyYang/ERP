# CF-02 Isolated Development and Offline-Test Profile

Status: shared foundation definition; no dependency installation performed

## Purpose

Provide one reproducible profile for local development and deterministic
offline checks without changing global runtimes, connecting to a protected
database, or requiring production credentials.

## Source-of-truth inputs

| Area | Existing repository input | Use |
| --- | --- | --- |
| Frontend dependencies | `package.json`, `package-lock.json` | npm package graph and scripts. |
| Frontend runtime | existing Next.js App Router and TypeScript configuration | lint/build/static validation. |
| Backend dependencies | `backend/pyproject.toml` | Flask, SQLAlchemy, pytest and ruff definitions. |
| Backend environment shape | `backend/.env.example` | existing variable names and local defaults. |
| Backend test scope | `backend/pyproject.toml` `testpaths = ["tests"]` | pytest discovery boundary. |

## Profiles

### Local development

- Frontend: Node.js LTS compatible with the existing Next.js dependency and
  npm using `package-lock.json`.
- Backend: Python `>=3.12` in a repository-local `backend/.venv`.
- Frontend environment: copy `env/frontend.env.example` to the ignored
  `.env.local` file at repository root when an API endpoint is needed.
- Backend environment: copy `env/backend.env.example` to the ignored
  `backend/.env` file and replace only local, non-production placeholders.
- Database connectivity is optional for UI/static work and is not part of the
  offline acceptance gate.

### Offline test

- Use the same repository-local runtimes as local development.
- Do not start MariaDB, run migrations, perform DDL/DML, use production data,
  or access credential stores.
- Run the quality entry point from the repository root.
- Backend checks use the existing `backend/.venv`; frontend checks use the
  existing `node_modules` installed from the lockfile. Neither is created by
  the quality entry point.
- A missing isolated runtime or dependency is a documented `UNAVAILABLE`
  result, not a reason to install or substitute dependencies.

## Reproduction sequence

The following is the setup contract for a new checkout. Installation is an
engineer-owned preparation step and is intentionally not performed by the
CF-02 check entry point.

```powershell
# From the repository root
npm ci
python -m venv backend/.venv
Set-Location backend
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
Set-Location ..
```

The third command is shown only as the existing project setup shape; it is
not a command executed by CF-02 and must follow the repository's dependency
approval process. If dependency installation is not authorized or not
available, run the checks and record the resulting `UNAVAILABLE` statuses.

## Isolation and safety boundaries

- All generated local state must stay under ignored paths such as
  `node_modules/`, `backend/.venv/`, `.next/`, and `.env*` files.
- Do not place credentials, access tokens, private keys, production URLs, or
  database dumps in templates, reports, or command output.
- Do not modify application source, database/migration files, existing FM02
  documents, the cross-module convention, or `evidence/` as part of this
  profile.
- The check entry point is static/offline only. It does not claim live,
  database, migration, concurrency, or Independent TEST acceptance.
