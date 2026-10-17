# ERP2.0 Cross-Module Coding Convention

Status: proposed shared standard for Sprint 2 entry review; applies across backend, frontend, database and test modules

This document consolidates the repository's existing backend and frontend conventions and adds shared delivery controls. It is a local repository standard pending Repository Office confirmation of the final centralized organization-wide location.

## 1. Rule classes

Rules marked **Global** apply to every module. Rules marked **Backend**, **Frontend**, **Database** or **Test** apply only to the named technology area. A technology-specific rule cannot weaken a Global safety or evidence rule.

## 2. Repository and module layout — Global

- `src/app/` contains Next.js route pages; `src/components/` contains reusable UI; `src/types/`, `src/services/` and `src/mock/` hold typed contracts, clients and explicitly temporary fixtures.
- `backend/app/` contains Flask application adapters, API routes, schemas, services, database/session boundaries and shared errors.
- `04_Engineering/Application/ERP-2.0/restserver/` contains bounded domain service sources and their tests when that service is the accepted source of truth.
- `04_Engineering/Database/` contains forward/down migrations and database-specific contract tests.
- `docs/` contains specifications, decision records, runbooks and validation reports. `evidence/` is custody material and must not be rewritten to make a failing result pass.
- New files use lowercase snake_case for Python/SQL and kebab-case or existing repository conventions for TypeScript; names must describe the bounded domain responsibility.

## 3. Correctness and change discipline — Global

Priority is Correctness → Maintainability → Readability → Consistency → Performance. Keep business rules in one authoritative layer. Do not duplicate or silently reinterpret schema, API or workflow truth in another layer. Refactor only when behavior remains covered by tests. Do not modify unrelated files or frozen decisions.

## 4. Backend and Python — Backend

- Use Flask route handlers only for transport parsing, service invocation and response conversion.
- Keep validation, locking, transaction and business rules in services; services must not import Flask request/response objects.
- Use typed Python signatures and narrow `Any` boundaries only for adapters or external client contracts.
- Use structured application errors with stable status and field/category information; do not expose passwords, tokens, raw SQL or unreviewed driver errors.
- Use injected connection/session factories in tests. Explicitly commit successful writes and roll back every failure path.
- Preserve existing Flask/SQLAlchemy/Pydantic architecture. Do not add FastAPI or a second framework without an approved architecture decision.

## 5. TypeScript, React and Next — Frontend

- Use Next.js App Router, React, TypeScript and existing Tailwind/shared components.
- Keep pages compositional; move repeated behavior into typed components and services.
- Types belong in `src/types/`; API/mock access belongs in `src/services/` or `src/mock/` with the source mode explicit.
- Handle loading, empty, error and unavailable states. Do not silently fall back from API mode to mock data.
- Preserve operational density, responsive layout, accessible labels and existing design tokens. Avoid new visual themes or decorative layouts.

## 6. SQL and migrations — Database

- Every protected migration declares its predecessor revision guard and records its next revision only after successful statements.
- Forward and down scripts are paired. Down scripts must detect revision drift and must not delete protected rows unless separately authorized.
- Use explicit constraints, indexes, foreign keys and check conditions. Do not use `IF NOT EXISTS` or silent drift masking on a protected C2 object where the contract requires exact state.
- Transactions, parent-row locks, idempotency fingerprints and effective-period rules must be documented with the owning service when MariaDB cannot express the rule in a table constraint.
- Never place credentials, credential-manager references or production endpoints in SQL or migration source.

## 7. Validation, type safety and errors — Global

- Validate at the boundary and again at the persistence boundary where the invariant matters.
- Reject ambiguous, malformed, stale, conflicting or out-of-scope inputs.
- Stable user/evidence-facing errors contain a predicate or field and safe classification, not raw stack traces or driver output.
- Do not treat a hash as authentication; use hashes for integrity/custody and record the actual authority/provenance separately.

## 8. Security, authorization, logging and secrets — Global

- Least privilege and target binding are mandatory. Transport connectivity does not grant database authority.
- Never print or commit API keys, passwords, DPAPI material, authorization headers, raw credential-manager output or sensitive database rows.
- Preserve the separation between CIO authorization, CTO review, Engineering implementation, Independent TEST verdict, PMO tracking and Repository custody.
- Log lifecycle phase, safe predicate, target class and custody hash where useful; redact payloads by default.
- Fail closed on identity mismatch, uncertain cleanup, unknown target, stale evidence, missing authority or dependency failure.

## 9. Tests and evidence — Test / Global

- Test names describe behavior and failure condition. Cover success, validation, conflict, idempotent replay, rollback, cleanup and unauthorized scope.
- Use deterministic fixtures with isolated roots. Never let synthetic cleanup touch a protected target or unrelated path.
- Record `SCRIPT_READY`, `SYNTHETIC_PASS`, `LIVE_PASS`, `HOLD` and `NOT_RUN` accurately. Static parsing and hash verification are not runtime acceptance.
- Independent TEST must inspect the exact artifact hashes and retain terminal verdict authority. Engineering self-test is not Independent TEST acceptance.
- Live database, migration, restore, concurrency and production tests require separate authorization and must not be implied by offline results.

## 10. Tooling and quality gates — Global

Required where the approved environment provides them: formatter, linter, type checker, unit tests, contract tests, build and source review. Record unavailable tools as `HOLD` or `NOT VERIFIED`; do not install or switch frameworks merely to erase a status. The accepted command set is documented in `CONTRIBUTING.md`, `docs/backend/CODING_CONVENTION.md`, `docs/frontend/CODING_CONVENTION.md` and the module test plan.

## 11. Git, branches and review — Global

- Use focused branches and imperative commits such as `docs: complete FM02 Sprint 1 documentation baseline`.
- Keep commits scoped. Preserve unrelated untracked evidence and never stage it accidentally.
- Update docs when schema/API/workflow/source changes. Review source and tests together.
- Push only to an explicitly verified authorized remote. If no remote is configured, report `GITHUB_PUSH=BLOCKED_REMOTE_NOT_VERIFIED`.
- Record branch, commit, changed paths, reviewer and validation evidence in the delivery matrix.

## 12. Exceptions and ownership

An exception must state the rule, reason, scope, owner, expiry/review point and evidence. CTO may accept technical implementation details within an authorized scope; CIO or Product decisions remain required for protected runtime, business scope, production and other explicitly reserved authorities.
