# FM-01 Remote DB Test Package Design

**Status:** PACKAGE DESIGN ONLY / NOT DISPATCHABLE / NO TARGET ACCESS

## Package contents

1. Exact source/contract/migration custody manifest.
2. Test Plan, Test Cases and traceability matrix.
3. Target profile with host, port, database, schema, route, owner and expiry.
4. Read-only preflight and privilege readback script specification.
5. Fixture manifest with synthetic IDs, parent graph, duplicate/cycle/stale-version cases and cleanup keys.
6. Runner contract separating STATIC/MOCK/NON_DB from DB_DEPENDENT/E2E.
7. Rollback/reset/rebuild procedure and evidence manifest schema.
8. Final report template with per-case expected/actual/evidence/owner/safe-stop fields.

## Target safeguards

- Require explicit named non-Production target admission; reject Production, shared/default, unknown or unbound targets.
- Verify target identity, port, database/schema, source commit, API contract hash, fixture namespace and credential scope before any connection.
- Permit only the minimum SELECT/transaction privileges needed by the admitted case set; no root, DDL, migration, grant, IAM, cross-database or shared-schema action.
- Require before/after row counts, schema/migration version readback, privilege readback, listener identity and cleanup evidence.
- Keep TC cases requiring business mutation behind BO1/BO4/BO5 and CTO/CIO authorization predicates.
- Abort on ambiguous identity, authority, target, audit, transaction, fixture or evidence state.

## Fixture and rollback design

- Use synthetic, namespaced references that cannot collide with business rows.
- Establish a baseline fingerprint before fixture insertion and re-read it after each case group.
- Create parent graph before children; exercise warehouse/plant consistency and location-local acyclicity.
- Reset by transaction rollback where possible; otherwise delete only the fixture namespace under an explicitly authorized cleanup operation and verify zero residual rows.
- Never repair existing business data, rewrite migrations, downgrade 0001/0002, or delete populated business history.
- A failed cleanup is a hard HOLD and requires owner intervention; do not conceal residuals by rerunning.

## Remote execution lanes

| Lane | Allowed content | Gate |
|---|---|---|
| Static | source/route/migration/contract/hash inspection | exact custody only |
| Mock/non-DB | synthetic actor, approval, idempotency and error behavior | disposable environment |
| DB-dependent | schema, FK, transaction, audit, version, restart and privilege checks | named target + credentials + fixture/reset authorization |
| E2E | browser/API/DB/audit closed loop | UI artifact + target + owner + CIO/CTO execution approval |

## Evidence contract

Every result must include case ID, classification, target profile hash, source/contract hashes, command or route, request/correlation/idempotency IDs, fixture IDs, timestamp, expected, actual, response/error envelope, audit/readback, cleanup/reset result and SHA-256 manifest. A package receipt or custody hash never substitutes for execution evidence. Static/mock/non-DB PASS must never be promoted to live DB or module acceptance.

## Safe stop

The package must return `BLOCKED` for missing target admission, missing Remote Engineer/host binding, unresolved BO1/BO4/BO5 policy, missing fixture cleanup authority, privilege mismatch, hash mismatch, residual rows, or any request to cross into Production, migration, Source-of-Truth, cutover or Go-Live.

