# Contributing

This project uses GitHub as the source of truth for collaboration. All feature work should go through branches and pull requests.

## Branch Strategy

Use `main` as the stable branch.

Create feature branches from `main`:

```text
feature/<short-topic>
fix/<short-topic>
docs/<short-topic>
codex/<short-topic>
```

Examples:

```text
feature/warehouse-crud
fix/product-order-validation
docs/api-reference
codex/migrate-backend-to-flask
```

## Commit Style

Use short imperative commit messages:

```text
Add purchase order CRUD
Fix inventory workflow validation
Document backend coding convention
```

Keep commits focused. A commit should usually represent one logical change.

## Pull Request Rules

Before opening a PR:

- Run backend tests if backend code changed.
- Run frontend build/lint if frontend code changed.
- Update docs when API behavior, schema, workflow, or conventions change.
- Include screenshots or notes for UI changes.
- Mention any migration or environment changes.

Do not merge code that breaks existing workflow tests.

## Backend Verification

From `backend/`:

```powershell
.\.venv\Scripts\python.exe -m ruff check app tests alembic
.\.venv\Scripts\python.exe -m pytest
```

Current required backend framework:

```text
Flask API + SQLAlchemy
```

Do not introduce FastAPI dependencies or patterns unless the team explicitly approves a framework change.

## Frontend Verification

From the project root:

```powershell
npm run build
```

Use existing Next.js App Router, component, mock data, and layout patterns unless a task explicitly changes the frontend architecture.

## Code Review Expectations

Review should focus on:

- Correctness and workflow closure.
- Data integrity and FK-like validation.
- API response consistency.
- Test coverage for success and failure paths.
- Separation of endpoint, service, schema, and model responsibilities.
- UI consistency with the existing ERP dashboard style.

See also:

- `docs/backend/CODING_CONVENTION.md`
- `docs/frontend/CODING_CONVENTION.md`
- `docs/engineering/CODE_REVIEW_CHECKLIST.md`
