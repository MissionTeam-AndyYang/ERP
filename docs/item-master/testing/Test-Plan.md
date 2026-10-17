# FM-02 TEST Plan

Revision `2026-10-18-002`: aligned to source commit `d73588f5e528538aa6b12225abdcd96884ac11ad`. The prior migration assertion FAIL is preserved in Test-Report.md and classified as `SOURCE_ADMISSION_GAP`.

## Objectives

1. Verify current bounded Item behavior against the approved design/source contract.
2. Verify migration/recovery evidence without substituting Engineering self-test for Independent TEST.
3. Verify isolated API behavior and distinguish it from shared runtime deployment.
4. Preserve target, credential, correlation and custody boundaries.

## Test levels

| Level | Target | Authority | Result |
|---|---|---|---|
| Engineering | FM-02 DEV lane | Engineering bounded execution | Six tests passed. |
| Independent isolated | Resettable `127.0.0.1:3354` | Independent TEST | Six tests passed; downgrade/reapply performed. |
| Shared HTTP | `127.0.0.1:8087` | Not authorized by C1 | Not a FM-02 pass; endpoint is FM-01. |
| Future C3 integration | Named designated FM-02 endpoint | Separate C3 authorization | Not executed. |

## Exit evidence

Source commit/tree, exact commands, environment, target identity, test output, schema/revision readback, rollback/recovery, privilege separation, correlation and Repository receipt are required.

## Current independent non-DB envelope

The current authorized execution is limited to backend/frontend unit and contract tests, mock/stub functional and cross-layer checks, validation/negative cases, authorization/error contracts, and static schema/migration contract checks. Live MariaDB, SQL, migration execution, credentials, production, protected-main merge, and full runtime acceptance are outside this TEST envelope.

## Migration baseline reconciliation

The approved design and `FM02_C2_MODULE_CONTRACT_20261016.md` require immutable migration lineage 0003-0006 and new lineage 0007-0009. The exact source baseline contains 0007-0009 but no Git path/provenance for 0003-0006. This is classified as `SOURCE_ADMISSION_GAP`; no historical SQL was copied into Product and no migration runtime was executed. The DB-dependent migration cases remain retained and deferred.

## Coverage taxonomy

Each case has exactly one Primary Test Type: Unit, API/Contract, Functional, Integration, Security/Authorization, Migration/Database, or E2E/UAT. EnvironmentClass is one of Static/Pure, Mock/Stub, Isolated Runtime without DB, Test DB, or Live DB/Production. DB-dependent cases require a designated authorized test database; Mock/Stub cases must not be interpreted as persistence evidence.

The foundation covers positive, negative, boundary, authorization, lifecycle, isolation, and error-contract behavior. Required prerequisites are: exact source commit/tree, approved design, clean isolated checkout, case-specific fixture ownership, explicit environment authorization, distinct TEST identity where required, and evidence custody. DB-dependent cases additionally require a resettable test database, target-scoped credentials, migration/recovery approval, and pre/post cleanup evidence. Live DB/Production execution remains prohibited.

## Coverage boundary

Mock/Stub and pure cases may be executed within the non-DB envelope but cannot prove persistence, uniqueness, locking, migration lineage, recovery, or runtime grants. Test DB cases are retained for future authorized execution and are currently `DEFERRED_NOT_AUTHORIZED / NOT_RUN`. E2E/UAT and Production-restricted cases require separate C3/owner authorization.

