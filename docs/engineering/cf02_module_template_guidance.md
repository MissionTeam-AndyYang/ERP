# CF-02 Module Template Guidance

Status: shared guidance for future module work; it does not create or alter a
module.

## Intent

Give a new module a predictable home for ownership, contracts, tests and
offline verification while preserving the repository's existing frontend and
Flask/SQLAlchemy boundaries.

## Module intake template

Before implementation, create a module-owned design note using this outline:

```text
# <Module> implementation note

Owner and scope:
Authoritative source of truth:
In-scope workflows:
Explicitly out of scope:
Input/output contract:
Persistence and transaction boundary:
Failure and authorization behavior:
Offline test cases:
Live-test prerequisites and separate authority:
```

The note must identify the authoritative source instead of duplicating schema,
API, workflow, or UI truth in a second location.

## Existing repository placement

Use the current layout according to the technology area:

| Area | Preferred placement | Required companion |
| --- | --- | --- |
| Next.js route | `src/app/<route>/` | typed components/services as needed; no business rules copied into pages. |
| Shared frontend UI | `src/components/<module>/` | loading, empty, error and unavailable states. |
| Frontend contract/client | `src/types/`, `src/services/` | explicit API/mock mode and typed mapping. |
| Frontend fixtures | `src/mock/` | clearly labeled temporary/demo data only. |
| Flask backend | `backend/app/` | route adapter, service boundary, schema/model boundary and tests. |
| Backend tests | `backend/tests/` | success, validation, conflict, rollback and authorization cases. |
| Legacy bounded service | `restserver/package/` | follow the existing legacy package convention and isolated tests. |
| Module documentation | `docs/engineering/` or the accepted module docs path | validation status and handoff notes. |

Do not introduce a second backend framework, a second package manager, or a
new source tree merely to satisfy a module request.

## Minimum quality contract

Every new module should define:

1. A deterministic local/offline test entry point.
2. A no-secrets environment template if configuration is required.
3. A test inventory covering success and failure paths, including rollback or
   idempotency where the workflow has writes.
4. A report that distinguishes `PASS`, `FAIL`, `UNAVAILABLE`, `HOLD` and
   `NOT_RUN`; static checks must not be described as live acceptance.
5. A cleanup and scope statement proving that protected targets, credentials,
   production data and unrelated paths are not touched.

## Review checklist

- [ ] The module boundary and source of truth are explicit.
- [ ] Existing manifests and lockfiles are reused.
- [ ] The local environment is isolated and reproducible.
- [ ] No secret or production endpoint is committed.
- [ ] Tests use deterministic fixtures and isolated roots.
- [ ] Unavailable dependencies are reported rather than installed or hidden.
- [ ] Database and migration changes, if any, have their own authorized
      scope and are not implied by an offline report.
- [ ] Existing module docs, `evidence/`, and unrelated source remain unchanged.
