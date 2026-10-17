# FM-02 Independent TEST Report

## Independent verdict

`INDEPENDENT TEST VERDICT = FAIL / STATIC MIGRATION CONTRACT BASELINE DEFECT; NON-DB APPLICATION TESTS PASS`

This is an independent Test Engineering result against the exact CIO-authorized baseline. It is not an Engineering self-test result and does not authorize database/runtime acceptance.

## Baseline and custody

- Repository: `https://github.com/MissionTeam-AndyYang/ERP.git`
- Checkout: `_fm02-uom-correction-20261018-001`
- Source branch reference: `codex/fm02-item-master-uom-integration-20261017-001`
- Source commit: `d73588f5e528538aa6b12225abdcd96884ac11ad`
- Source tree: `ba57e39f819f9c17146061fd5b21802a44998710`
- Delivery branch: `codex/fm02-item-master-independent-test-20261018-001`
- Delivery branch custody: Test-document artifacts only; Product source delta from `d73588f5...` is limited to `docs/item-master/testing/*`.
- Design SHA-256: `1D6B7350576BC2DD8C5851420ED253FE3C17AEAA6143350DD20D000754B5599C`
- Test executor: Test Engineering / ERP2 Integration Functional Validation
- Return target: CTO Office V2
- Existing authority reused: `FM02-TEST-PLAN-20261013-001.md` and `FM02-TEST-CASE-CATALOG-20261013-001.md`
- Source mutation: none

## Executed cases

| Case / command | Result | Count / evidence |
|---|---|---|
| Frontend component: `npm run test:component -- --reporter=verbose` | PASS | 1 file, 5 tests passed |
| Backend FM02 contract: `python -m pytest -q 04_Engineering\\Application\\ERP-2.0\\restserver\\tests\\test_fm02_c2_service.py` | PASS | 11 passed |
| Static migration/schema contract: `python -m pytest -q 04_Engineering\\Database\\tests\\test_fm02_item_master_approved_contract.py` | FAIL | 5 passed, 1 failed at required legacy-file read |
| ESLint: `npm run lint` | PASS | exit 0 |
| TypeScript: `npx tsc --noEmit` | PASS | exit 0 |

## Defect

- FAILURE SURFACE: `test_existing_migrations_are_not_rewritten` in the approved static migration contract test.
- EXPECTED: exact baseline contains `fm02_item_master_0003_integrity_foundation.sql`, `0004_c2_reference_contract.sql`, `0005_c2_package_customer_conversion.sql`, and `0006_legacy_mapping_reconciliation.sql` at `04_Engineering/Database` so their hashes can be verified.
- ACTUAL: exact baseline contains only 0007, 0008 and 0009 migration SQL at that path; the test raises `FileNotFoundError` on the 0003 file before completing the hash assertions.
- EVIDENCE: `migration-static-output.txt` SHA-256 `13B767BBA6444C73A915E905041067C892143A06F81995E8329CA4D11384C75E`.
- CLASSIFICATION: `SOURCE_ADMISSION_GAP`.
- LIKELY OWNER: CTO/Engineering source admission and repository custody.
- SAFE-STOP STATE: no source repair, no migration execution, no database access, no credentials, no runtime start, and no protected-main action.

This is recorded as a source/test baseline defect, not silently repaired by Test Engineering.

### Reconciliation history

The previous report recorded the exact FileNotFoundError and overall FAIL. Alignment review confirmed the approved design and current test expectation are consistent with the stated 0003-0009 lineage; the specified source tree admits only 0007-0009. Therefore the prior FAIL is retained, but its cause is refined from a generic baseline defect to `SOURCE_ADMISSION_GAP`. It is not classified as `OUTDATED_TEST_BASELINE` and is not claimed as an `ACTUAL_MIGRATION_CONTRACT_DEFECT` because 0003-0006 cannot be inspected in this source baseline.

## Non-DB result matrix

- Validation/negative cases: PASS through the 5 frontend draft-validation tests and 11 backend FM02 contract tests.
- Authorization/error contract cases: covered by the passing backend/frontend cases; no live authorization grant was attempted.
- Mock/stub UI/API integration: no dedicated additional suite was present in the exact baseline; NOT RUN beyond the available component/contract coverage.
- Static schema/migration contract: FAIL as documented above.

## Explicitly not authorized / not run

- Live MariaDB or SQL: `NOT AUTHORIZED / NOT RUN`
- Migration execution, upgrade/downgrade/reapply runtime: `NOT AUTHORIZED / NOT RUN`
- Real-DB uniqueness, locking, persistence, concurrency, restore, restart, recovery: `NOT AUTHORIZED / NOT RUN`
- Credentials, production, protected-main merge, shared runtime and full runtime acceptance: `NOT AUTHORIZED / NOT RUN`
- Engineering self-test evidence was not relabeled as independent TEST evidence.

## Evidence manifest

- Acceptance: `FM02-INDEPENDENT-TEST-ACCEPTANCE-20261018-001.md` SHA-256 `0759B767848701F2D937E29CAF2642C6F2C039E89531261FAE3DACCDF0B20197`
- Frontend output SHA-256 `32C5BC3A0853A783CE49D8695E772359536E555447E634D0D268E472D909E6BF`
- Backend output SHA-256 `6EBD974CF73E865B9E8FDA33312DE770BC9BC141CBE221E0B10C7906493E8388`
- Migration static output SHA-256 `13B767BBA6444C73A915E905041067C892143A06F81995E8329CA4D11384C75E`
- Lint output SHA-256 `39EF1A894110FC4E6164501F7BF25F840FD2DAF2FB3FAAE10492B4340935C4B0`
- TypeScript output SHA-256 `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`

## Recommendation

CTO/Engineering should reconcile the exact baseline's migration file custody with the approved static contract test, then return a new immutable baseline or explicit corrected test contract. Test Engineering should not claim overall FM02 independent PASS until the failed static migration contract is resolved and rerun under a newly accepted baseline.

## Formal return fields

- `DESIGN_TEST_ALIGNMENT=GAP`
- `TEST_PLAN=APPROVED`
- `TEST_CASES=APPROVED`
- `MIGRATION_TEST_BASELINE=RECONCILED / SOURCE_ADMISSION_GAP; EXECUTION HOLD`
- `NON_DB_TEST_EXECUTION=COMPLETE`
- `NON_DB_TEST_VERDICT=FAIL`
- `TEST_REPORT=COMPLETE`
- `REMOTE_TEST_DOCUMENT_READBACK=PENDING DELIVERY READBACK`
- `KNOWLEDGE_READBACK=HOLD / NO KNOWLEDGE CONNECTOR AUTHORIZED`
- `DB_DEPENDENT_TEST=DEFERRED_NOT_AUTHORIZED`
- `PRODUCTION_TEST=NOT_AUTHORIZED`
- `CIO_NOTIFICATION=MANUAL_REQUIRED`
- `MANUAL_RELAY_REQUIRED=YES`
