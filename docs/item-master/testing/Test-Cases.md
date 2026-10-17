# FM-02 TEST Case Catalog

Revision `2026-10-18-002`: retains all DB-dependent and production-restricted cases. The prior migration static-contract FAIL remains in the report; reconciliation classification is `SOURCE_ADMISSION_GAP`.

| Case | Evidence status | Notes |
|---|---|---|
| TC01 valid compatibility | PASS | Engineering and Independent TEST evidence. |
| TC02 invalid category/UOM | PASS | Negative validation evidence. |
| TC03 specification lineage | PASS | Isolated test evidence. |
| TC04 effectivity overlap | PASS | Isolated test evidence. |
| TC05 lifecycle idempotency | PASS | Isolated test evidence. |
| TC06 lifecycle concurrency | PASS | Isolated test evidence. |
| TC07 rollback atomicity | PASS | Isolated test evidence. |
| TC08 technical actor rejection | PASS | Isolated test evidence. |
| TC09 upgrade/downgrade/reapply | PASS | Independently performed in isolated lane. |
| TC10 live shared FM-02 route | NOT VERIFIED | 8087 is FM-01; C3 required. |
| TC11 application-runtime grant | NOT VERIFIED | New write grants were not enabled. |
| TC12 Repository final PASS receipt | PENDING | F03 custody operation required. |

## Current TEST disposition

| Case group | Current disposition | Boundary |
|---|---|---|
| Backend/frontend unit and contract | EXECUTED | Non-live isolated source baseline |
| Mock/stub functional, validation, authorization and negative cases | PARTIAL | Only available exact-baseline suites executed |
| Static schema/migration contract | FAIL / SOURCE_ADMISSION_GAP | 0003-0006 absent from source tree; no repair performed |
| Real-DB uniqueness, locking, persistence, concurrency | DEFERRED_NOT_AUTHORIZED / NOT_RUN | Live DB and SQL prohibited |
| Migration execution, upgrade/downgrade/reapply, restore/restart/recovery | DEFERRED_NOT_AUTHORIZED / NOT_RUN | Runtime mutation prohibited |
| Production/shared runtime/full acceptance | NOT_AUTHORIZED / NOT_RUN | Outside TEST authority |

