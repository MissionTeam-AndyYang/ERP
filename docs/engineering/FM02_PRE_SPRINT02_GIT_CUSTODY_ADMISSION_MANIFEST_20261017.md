# FM-02 Pre-Sprint-2 Git Custody and Admission Manifest

Manifest ID: `ERP2-FM02-PRE-SPRINT02-GIT-CUSTODY-20261017-123`
Decision reference: `ERP2.0-CIO-GOV-PRE-SPRINT02-GIT-ALIGNMENT-20261017-123`
Prepared: 2026-10-17
Status: `PREPARED / REMOTE ADMISSION NOT AUTHORIZED`

## Verified source and destination

| Role | Identity |
|---|---|
| FM-02 source | `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\FM02_C2_Implementation_20261013_001` |
| FM-02 branch/commit | `codex/fm02-c2-isolated-20261013-001` / `ce4e7e6b4c29b4b5b9fad8e22dd9a664ea84f0e6` |
| Source custody state | Tracked source is clean; pre-existing untracked `evidence/` is preserved and excluded |
| Product repository | `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0` |
| Product branch/commit | `main` / `89b374109312720b3ff6669a9664fb0cf8f9a6ba` |
| Product remote | `https://github.com/MissionTeam-AndyYang/ERP.git` |
| Historical FM-02 remote branch | `codex/fm02-central-source-completion-20261013-001` / `41e070a58c668505b91e5bcece778a87fc9725c5` |
| Remote evidence | Read-only `git ls-remote` verified; no write test performed |

The Product worktree is dirty with unrelated tracked and untracked changes. It was not cleaned, reset, staged, branched or otherwise modified.

The exact source SHA-256 values remain in `FM02_CANONICAL_SOURCE_ADMISSION_MANIFEST_20261017.md` (SHA-256 `80A02D27513EEC8BEE62F22AF7B5BDFAEDB962E0F0264ADAFF289008805A7C7B`) and the classifications remain in `FM02_CANONICAL_INTEGRATION_CLASSIFICATION_20261017.md` (SHA-256 `5B2A3BE1C494A674012D2D4623781095F5A4D24AB9E7040B4EAABFF73BA5A199`).

## Exact custody/admission disposition

### Preserve existing Product files — six `KEEP_TARGET`

These paths are not to be overwritten or replaced by FM-02 source synchronization:

1. `backend/alembic/env.py`
2. `backend/alembic/versions/20260517_0001_ewdb_baseline.py`
3. `backend/app/db/base.py`
4. `backend/app/db/session.py`
5. `backend/app/main.py`
6. `backend/tests/test_health.py`

### Defer to future Compatibility/Coding Sprint — four `MERGE_WITH_REVIEW`

These paths remain explicitly deferred and are not integrated by this manifest:

1. `backend/tests/conftest.py`
2. `package.json`
3. `package-lock.json`
4. `tsconfig.json`

### Source-only Product candidates — fourteen paths

These are source candidates, not integrated Product files. They require the approved Product source workflow, Engineering acceptance and compatibility review:

1. `04_Engineering/Source_Archive/FM02_Sprint01_Implementation_20261012_001/migrations/fm02_item_master_0001.sql`
2. `04_Engineering/Source_Archive/FM02_Sprint01_Implementation_20261012_001/migrations/fm02_item_master_0002_business_names.sql`
3. `04_Engineering/Source_Archive/FM02_Sprint01_Implementation_20261012_001/src/fm02_item_api.py`
4. `04_Engineering/Source_Archive/FM02_Sprint01_Implementation_20261012_001/tests/test_fm02_item_api.py`
5. `04_Engineering/Database/fm02_item_master_0003_integrity_foundation.sql`
6. `04_Engineering/Database/fm02_item_master_0003_integrity_foundation_down.sql`
7. `04_Engineering/Application/ERP-2.0/restserver/package/fm02_foundation/foundation.py`
8. `04_Engineering/Application/ERP-2.0/restserver/tests/test_fm02_foundation.py`
9. `backend/app/api/v1/endpoints/fm02_c2.py`
10. `backend/app/services/fm02_c2.py`
11. `src/components/items/c2-reference-panel.test.tsx`
12. `src/components/items/c2-reference-panel.tsx`
13. `vitest.config.ts`
14. `vitest.setup.ts`

### Shared standards, tools and Knowledge custody — twenty-one paths

These are not Product source files and must retain separate Repository Office/Knowledge custody:

1. `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/CF01_DOCUMENTATION_WORKING_MECHANISM_20261017.md`
2. `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/README.md`
3. `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/validate_cf01_b02.py`
4. `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/demonstrations/CF01_B02_READ_ONLY_DEMONSTRATION_20261017.md`
5. `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/templates/CF01_CHANGE_IMPACT_SYNC_TEMPLATE.md`
6. `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/templates/CF01_CROSS_MODULE_TRACEABILITY_TEMPLATE.md`
7. `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/templates/CF01_DOCUMENT_IDENTITY_LIFECYCLE_TEMPLATE.md`
8. `docs/engineering/CROSS_MODULE_CODING_CONVENTION_APPROVAL_REQUEST_20261017.md`
9. `docs/engineering/CROSS_MODULE_FOUNDATION_DELIVERY_20261017.md`
10. `docs/engineering/CROSS_MODULE_FOUNDATION_KNOWLEDGE_RELAY_20261017.md`
11. `docs/engineering/cf02_module_template_guidance.md`
12. `docs/engineering/cf02_offline_verification_20261017.md`
13. `docs/engineering/cf02_shared_engineering_foundation.md`
14. `docs/fm02/FM02_SPRINT01_DOCUMENT_COMPLETION_MATRIX_20261016_104.md`
15. `docs/fm02/FM02_SPRINT01_REPOSITORY_KNOWLEDGE_UPDATE_RELAY_20261017_105.md`
16. `engineering_foundation/README.md`
17. `engineering_foundation/checks/quality_check.ps1`
18. `engineering_foundation/checks/quality_check.sh`
19. `engineering_foundation/env/backend.env.example`
20. `engineering_foundation/env/frontend.env.example`
21. `engineering_foundation/environment/dev_test_profile.md`

### Test evidence — four paths

These remain evidence/Knowledge artifacts and are excluded from Product admission:

1. `04_Engineering/evidence/FM02-IM-FOUNDATION-INTEGRITY-01-AS-BUILT-20261012-001.md`
2. `04_Engineering/evidence/FM02-IM-FOUNDATION-INTEGRITY-01-MANIFEST-20261012-001.json`
3. `04_Engineering/evidence/FM02-CENTRAL-SOURCE-COMPLETION-20261013-001.md`
4. `04_Engineering/evidence/FM02-CENTRAL-SOURCE-COMPLETION-MANIFEST-20261013-001.json`

The four groups plus six preserved and four deferred paths account for all 49 reviewed paths.

## Required delivery authorization

Before any remote delivery, CIO/Repository Office must identify and authorize:

- named push-capable Git executor;
- credential custody and permitted remote scope;
- exact source-only Product candidate list above;
- target non-default integration branch from verified Product `main`;
- protected-main PR policy and reviewer/merge authority;
- independent remote commit/tree readback.

No direct `main` write, force-push, merge, destructive cleanup or remote synchronization is permitted by this manifest.

## Verdicts

`SOURCE_CUSTODY=PASS`

`PRODUCT_REMOTE_IDENTITY=VERIFIED`

`BRANCH_PR_AUTHORITY=HOLD`

`PRE_SPRINT02_ADMISSION_MANIFEST=READY`

`REMOTE_SYNC=BLOCKED`

`REMOTE_READBACK=NOT_PERFORMED`

`KNOWLEDGE_SOURCE_ALIGNMENT=HOLD`

`DEFERRED_COMPATIBILITY_ITEMS=4`

`INTEGRATION_TEST=DEFERRED_TO_SPRINT05_06`

`FM02_SPRINT02_CODING_AUTHORIZATION=NOT_GRANTED`
