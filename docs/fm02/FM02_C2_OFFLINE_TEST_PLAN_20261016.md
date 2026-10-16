# FM-02 C2 Offline Test Plan and Evidence Contract

Status: source-only and deterministic validation plan
Date: 2026-10-16

## Evidence status vocabulary

- `SCRIPT_READY`: procedure exists and passed static/source review.
- `SYNTHETIC_PASS`: deterministic test passed without the protected database.
- `LIVE_PASS`: attributable target execution passed; not established by this package.
- `HOLD`: a predicate failed or cleanup/identity is uncertain.
- `NOT_RUN`: intentionally not executed under the current authorization.

## Test inventory

| Area | Tests | Current status | Evidence |
| --- | --- | --- | --- |
| C2 service validation | Status vocabulary, scope-key normalization, approval gating, conversion validation, item-specific resolver, ambiguity rejection, transaction locking/idempotent replay, REST injection | `SYNTHETIC_PASS` | `04_Engineering/Application/ERP-2.0/restserver/tests/test_fm02_c2_service.py` — 11 passed in the current offline run |
| Foundation service validation | Existing item/specification/lifecycle fixture suite | `NOT_VERIFIED` in this context | Collection requires `pymysql`; no live or credential retry was made |
| Migration contract | Revision guards, physical constraints, zero-row gate, down-migration safety | `SYNTHETIC_PASS` | `04_Engineering/Database/tests/test_fm02_c2_migration_contract.py` — 6 passed |
| Backend/API contract suite | Existing generic Flask backend tests | `HOLD` | Collection blocked by missing isolated environment dependency `pydantic`; no package installation was performed |
| Frontend static/build validation | TypeScript/Next build | `HOLD` | `npm run build` blocked because `next` is unavailable; offline dependency repair is not authorized |
| Direct T2-15 functional harness | CRUD smoke and T2-15 procedures | `SCRIPT_READY` / `NOT_RUN` | `20_Engineering_Workspace/FM02_TEST_Evidence_20261014_011/cleanup/FM02_C2_T2_15_CRUD_SMOKE_TEST_20261016_099.ps1` and prior accepted harness evidence; live DML remains separately gated |
| T2-15 residual recovery | Read-only inventory, cleanup procedure and secret-safe diagnostic | `SCRIPT_READY` / `HOLD` | Existing run `38498cb2d1ab4452af1fe761ac91ca14`; residual cleanup and retry are not authorized here |
| T2-14B/T2-14C | Restore/restart/readback procedures | `SCRIPT_READY` / `NOT_RUN` | Existing accepted combined runner; standalone T2-14C remains excluded |

## Offline acceptance cases

The deterministic suite must continue to cover:

1. Valid and invalid status vocabulary and approval evidence.
2. Customer scope sentinel and supplier-scoped identity.
3. Fixed versus catch-weight conversion parameters.
4. Item-specific resolution, ambiguity and no-global-fallback behavior.
5. Parent-row locking, identical-request replay and conflicting fingerprint rejection.
6. Migration revision lineage, physical constraints, zero-row admission and data-preserving down-migration guards.
7. Failure paths that return structured, non-secret errors and roll back before commit.

No offline test may be reported as a live database result. No test may use the Owner credential, DPAPI, MariaDB lifecycle, SQL mutation or production data.

## Live handoff contract

The separately authorized Owner-host procedure must report target identity, process/listener identity, authenticated database identity, exact phase, evidence custody hash and cleanup state. Independent TEST owns the terminal verdict. A missing, stale, conflicting or uncertain result is `HOLD`, not a pass.
