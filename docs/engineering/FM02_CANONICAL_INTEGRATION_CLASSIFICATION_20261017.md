# FM-02 Canonical Integration Classification — Directive 122

Record ID: `ERP2-FM02-CANONICAL-INTEGRATION-CLASSIFICATION-20261017-122`
Decision reference: `ERP2.0-CIO-GOV-FM02-CANONICAL-INTEGRATION-COMPLETION-20261017-122`
Prepared: 2026-10-17
Status: `READ-ONLY CLASSIFICATION / ADMISSION NOT AUTHORIZED`

## Evidence baseline

Source custody is the FM-02 repository at branch `codex/fm02-c2-isolated-20261013-001`, local HEAD `305cfdae36397bd66ebe8aae53bbbe932c80810b`. The exact source paths and SHA-256 values are preserved in `FM02_CANONICAL_SOURCE_ADMISSION_MANIFEST_20261017.md`.

The Product destination is `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0`, remote `https://github.com/MissionTeam-AndyYang/ERP.git`, `main` at `89b374109312720b3ff6669a9664fb0cf8f9a6ba`. The Product worktree is dirty and was not modified. Remote read access is verified; push/PR authority is not verified.

This is a CTO-local read-only classification. It is not a formal Engineering Office acceptance, merge approval or CIO admission.

## Classification rules

| Class | Destination rule |
|---|---|
| `PRODUCT_CODE` | Product repository source workflow; requires target architecture review before admission |
| `PRODUCT_DESIGN_DOCUMENT` | Product documentation location after source-of-truth reconciliation |
| `GLOBAL_ENGINEERING_STANDARD` | Canonical shared-standard/Knowledge custody, not Product duplication |
| `SHARED_ENGINEERING_TOOL` | Canonical shared tooling custody, not Product duplication unless separately approved |
| `TEST_SOURCE` | Product or test-source workflow after independent test review |
| `TEST_EVIDENCE` | Evidence/Knowledge custody; not copied as Product code |
| `KNOWLEDGE_RECORD` | Canonical Repository Knowledge custody |
| `EXCLUDE / LOCAL_ONLY` | Retained in source workspace; not part of admission |

## Complete 49-file classification

### Product code and test source

| Source path | Class | Proposed destination | Read-only result |
|---|---|---|---|
| `04_Engineering/Source_Archive/FM02_Sprint01_Implementation_20261012_001/migrations/fm02_item_master_0001.sql` | `PRODUCT_CODE` | Product Alembic migration sequence | `HOLD` — legacy archive path requires migration mapping |
| `04_Engineering/Source_Archive/FM02_Sprint01_Implementation_20261012_001/migrations/fm02_item_master_0002_business_names.sql` | `PRODUCT_CODE` | Product Alembic migration sequence | `HOLD` — legacy archive path requires migration mapping |
| `04_Engineering/Source_Archive/FM02_Sprint01_Implementation_20261012_001/src/fm02_item_api.py` | `PRODUCT_CODE` | Product backend item endpoint/service location | `HOLD` — legacy API path requires architecture mapping |
| `04_Engineering/Source_Archive/FM02_Sprint01_Implementation_20261012_001/tests/test_fm02_item_api.py` | `TEST_SOURCE` | Product backend test location | `HOLD` — legacy test path requires contract mapping |
| `04_Engineering/Database/fm02_item_master_0003_integrity_foundation.sql` | `PRODUCT_CODE` | Product Alembic migration sequence | `HOLD` — migration authority and ordering require review |
| `04_Engineering/Database/fm02_item_master_0003_integrity_foundation_down.sql` | `PRODUCT_CODE` | Product migration rollback source | `HOLD` — rollback mapping requires review |
| `04_Engineering/Application/ERP-2.0/restserver/package/fm02_foundation/foundation.py` | `PRODUCT_CODE` | Product backend service/model location | `HOLD` — legacy application path requires mapping |
| `04_Engineering/Application/ERP-2.0/restserver/tests/test_fm02_foundation.py` | `TEST_SOURCE` | Product backend test location | `HOLD` — legacy test path requires mapping |
| `backend/alembic/env.py` | `PRODUCT_CODE` | `backend/alembic/env.py` | `KEEP_TARGET` — source and Product behavior match in read-only comparison |
| `backend/alembic/versions/20260517_0001_ewdb_baseline.py` | `PRODUCT_CODE` | Existing Product baseline migration | `KEEP_TARGET` — only non-functional formatting difference observed |
| `backend/app/api/v1/endpoints/fm02_c2.py` | `PRODUCT_CODE` | `backend/app/api/v1/endpoints/fm02_c2.py` | `ADMIT_AFTER_REVIEW` — absent on Product `main`; endpoint contract review required |
| `backend/app/db/base.py` | `PRODUCT_CODE` | `backend/app/db/base.py` | `KEEP_TARGET` — existing Product model import is functionally equivalent |
| `backend/app/db/session.py` | `PRODUCT_CODE` | `backend/app/db/session.py` | `KEEP_TARGET` — only non-functional formatting difference observed |
| `backend/app/main.py` | `PRODUCT_CODE` | `backend/app/main.py` | `KEEP_TARGET` — source and Product behavior match in read-only comparison |
| `backend/app/services/fm02_c2.py` | `PRODUCT_CODE` | `backend/app/services/fm02_c2.py` | `ADMIT_AFTER_REVIEW` — absent on Product `main`; service contract review required |
| `backend/tests/conftest.py` | `TEST_SOURCE` | `backend/tests/conftest.py` | `MERGE_WITH_REVIEW` — fixture ID handling differs; preserve Product fixture behavior and test both paths |
| `backend/tests/test_health.py` | `TEST_SOURCE` | `backend/tests/test_health.py` | `KEEP_TARGET` — only non-functional formatting difference observed |
| `package.json` | `PRODUCT_CODE` | `package.json` | `MERGE_WITH_REVIEW` — FM-02 adds Vitest/component-test script and dependencies |
| `package-lock.json` | `PRODUCT_CODE` | `package-lock.json` | `MERGE_WITH_REVIEW` — must be regenerated from the approved package decision |
| `src/components/items/c2-reference-panel.test.tsx` | `TEST_SOURCE` | `src/components/items/c2-reference-panel.test.tsx` | `ADMIT_AFTER_REVIEW` — absent on Product `main` |
| `src/components/items/c2-reference-panel.tsx` | `PRODUCT_CODE` | `src/components/items/c2-reference-panel.tsx` | `ADMIT_AFTER_REVIEW` — absent on Product `main` |
| `tsconfig.json` | `PRODUCT_CODE` | `tsconfig.json` | `MERGE_WITH_REVIEW` — target is ES5 while FM-02 source is ES2015; TypeScript/build regression required |
| `vitest.config.ts` | `TEST_SOURCE` | `vitest.config.ts` | `ADMIT_AFTER_REVIEW` — absent on Product `main` |
| `vitest.setup.ts` | `TEST_SOURCE` | `vitest.setup.ts` | `ADMIT_AFTER_REVIEW` — absent on Product `main` |

### Shared standards, tools and Knowledge records

| Source path | Class | Authoritative destination | Read-only result |
|---|---|---|---|
| `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/CF01_DOCUMENTATION_WORKING_MECHANISM_20261017.md` | `GLOBAL_ENGINEERING_STANDARD` | Canonical Repository Knowledge index structure | `HOLD` — Repository Office custody/readback pending |
| `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/README.md` | `SHARED_ENGINEERING_TOOL` | CF-01 canonical standard package | `HOLD` — central custody pending |
| `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/validate_cf01_b02.py` | `SHARED_ENGINEERING_TOOL` | CF-01 validation package | `HOLD` — central custody pending |
| `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/demonstrations/CF01_B02_READ_ONLY_DEMONSTRATION_20261017.md` | `SHARED_ENGINEERING_TOOL` | CF-01 demonstration package | `HOLD` — central custody pending |
| `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/templates/CF01_CHANGE_IMPACT_SYNC_TEMPLATE.md` | `SHARED_ENGINEERING_TOOL` | CF-01 template package | `HOLD` — central custody pending |
| `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/templates/CF01_CROSS_MODULE_TRACEABILITY_TEMPLATE.md` | `SHARED_ENGINEERING_TOOL` | CF-01 template package | `HOLD` — central custody pending |
| `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/templates/CF01_DOCUMENT_IDENTITY_LIFECYCLE_TEMPLATE.md` | `SHARED_ENGINEERING_TOOL` | CF-01 template package | `HOLD` — central custody pending |
| `docs/engineering/CROSS_MODULE_CODING_CONVENTION_APPROVAL_REQUEST_20261017.md` | `KNOWLEDGE_RECORD` | Canonical Repository Knowledge custody | `HOLD` — approval/custody readback pending |
| `docs/engineering/CROSS_MODULE_FOUNDATION_DELIVERY_20261017.md` | `KNOWLEDGE_RECORD` | Canonical Repository Knowledge custody | `HOLD` — custody readback pending |
| `docs/engineering/CROSS_MODULE_FOUNDATION_KNOWLEDGE_RELAY_20261017.md` | `KNOWLEDGE_RECORD` | Canonical Repository Knowledge custody | `HOLD` — relay is not registration evidence |
| `docs/engineering/cf02_module_template_guidance.md` | `GLOBAL_ENGINEERING_STANDARD` | Canonical shared foundation custody | `HOLD` — central custody pending |
| `docs/engineering/cf02_offline_verification_20261017.md` | `KNOWLEDGE_RECORD` | Canonical Repository Knowledge custody | `HOLD` — custody readback pending |
| `docs/engineering/cf02_shared_engineering_foundation.md` | `GLOBAL_ENGINEERING_STANDARD` | Canonical shared foundation custody | `HOLD` — central custody pending |
| `docs/fm02/FM02_SPRINT01_DOCUMENT_COMPLETION_MATRIX_20261016_104.md` | `KNOWLEDGE_RECORD` | Canonical Repository Knowledge custody | `HOLD` — Product documentation must not duplicate Knowledge authority |
| `docs/fm02/FM02_SPRINT01_REPOSITORY_KNOWLEDGE_UPDATE_RELAY_20261017_105.md` | `KNOWLEDGE_RECORD` | Canonical Repository Knowledge custody | `HOLD` — relay is not registration evidence |
| `engineering_foundation/README.md` | `SHARED_ENGINEERING_TOOL` | Canonical shared engineering foundation | `HOLD` — central tool custody pending |
| `engineering_foundation/checks/quality_check.ps1` | `SHARED_ENGINEERING_TOOL` | Canonical shared engineering foundation | `HOLD` — central tool custody pending |
| `engineering_foundation/checks/quality_check.sh` | `SHARED_ENGINEERING_TOOL` | Canonical shared engineering foundation | `HOLD` — central tool custody pending |
| `engineering_foundation/env/backend.env.example` | `SHARED_ENGINEERING_TOOL` | Canonical shared engineering foundation | `HOLD` — central tool custody pending |
| `engineering_foundation/env/frontend.env.example` | `SHARED_ENGINEERING_TOOL` | Canonical shared engineering foundation | `HOLD` — central tool custody pending |
| `engineering_foundation/environment/dev_test_profile.md` | `SHARED_ENGINEERING_TOOL` | Canonical shared engineering foundation | `HOLD` — central tool custody pending |

### Test evidence and Knowledge-only records

| Source path | Class | Authoritative destination | Read-only result |
|---|---|---|---|
| `04_Engineering/evidence/FM02-IM-FOUNDATION-INTEGRITY-01-AS-BUILT-20261012-001.md` | `TEST_EVIDENCE` | Evidence/Knowledge custody | `EXCLUDE_FROM_PRODUCT` |
| `04_Engineering/evidence/FM02-IM-FOUNDATION-INTEGRITY-01-MANIFEST-20261012-001.json` | `TEST_EVIDENCE` | Evidence/Knowledge custody | `EXCLUDE_FROM_PRODUCT` |
| `04_Engineering/evidence/FM02-CENTRAL-SOURCE-COMPLETION-20261013-001.md` | `TEST_EVIDENCE` | Evidence/Knowledge custody | `EXCLUDE_FROM_PRODUCT` |
| `04_Engineering/evidence/FM02-CENTRAL-SOURCE-COMPLETION-MANIFEST-20261013-001.json` | `TEST_EVIDENCE` | Evidence/Knowledge custody | `EXCLUDE_FROM_PRODUCT` |

## Integration and testing disposition

The ten existing Product conflicts have been behavior-screened read-only. Six are functionally equivalent or formatting-only (`env.py`, baseline migration, `base.py`, `session.py`, `main.py`, `test_health.py`), two require explicit dependency/configuration merge (`package.json`, `package-lock.json`), `tsconfig.json` requires a TypeScript target decision, and `conftest.py` requires fixture regression. The absent endpoint/service/UI/test paths require contract review before admission.

No clean isolated integration candidate was assembled because formal Engineering assignment acceptance and a push-capable Git executor were not exposed. No offline integrated test suite was run against an assembled candidate. No live database or migration operation was performed.

## Final classification verdict

`49_FILE_FINAL_CLASSIFICATION=HOLD`

`10_CONFLICT_RESOLUTIONS=HOLD`

`39_NEW_PATHS=HOLD`

`INTEGRATION_CANDIDATE=NOT_AUTHORIZED`

`OFFLINE_INTEGRATION_TEST=NOT_RUN`

`DOCUMENT_SOURCE_ALIGNMENT=HOLD`

`GLOBAL_STANDARD_PLACEMENT=HOLD`

`PUSH_ACTOR_AND_PR_AUTHORITY=HOLD`

`FINAL_ADMISSION_PACKAGE=HOLD`

`REMOTE_SYNCHRONIZATION=NOT_AUTHORIZED`

Minimum next action: obtain formal Engineering acceptance for the compatibility work, Repository Office custody/readback for shared artifacts, and a verified push-capable PR executor. Then assemble a clean integration candidate and run the required offline regressions before seeking CIO admission approval.
