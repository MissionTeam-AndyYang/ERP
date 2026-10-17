# ERP2.0 FM-02 Cross-Module Knowledge Baseline and Artifact-Index Update Proposal

Status: `PROPOSAL / NOT A NEW INDEX`
Date: `2026-10-18`
Canonical Index: `01_Foundation/repository_knowledge/Repository-Knowledge-Index-20261010-001.md`

## Purpose

Define a cross-module view over already registered FM-02 custody records. This proposal does not replace the authoritative Knowledge Index, move history, merge Product `main`, or authorize database, runtime, production, or test execution.

## Existing Logical Layers

### Shared Standards / Reusable Templates and Tools

- `ERP2-CF01-DOC-WORKING-MECHANISM-20261017-001`
  - Source: `20_Engineering_Workspace/FM02_C2_Implementation_20261013_001/docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/`
  - Status: `ACTIVE_BOUNDED`; v1.1; source commit `2b800b1dec3c45deae0b653b2c5868d598c71e13`; SHA-256 `64180CED3A6F645692C658D1D0339450C6E82DB2A1F548D55A442B63602BB88B`.
- `ERP2-ENGINEERING-CROSS-MODULE-CODING-CONVENTION-20261016-001`
  - Source: `20_Engineering_Workspace/FM02_C2_Implementation_20261013_001/docs/engineering/CROSS_MODULE_CODING_CONVENTION_20261016.md`
  - Status: `PROPOSED`; normative approval remains unresolved.
- `ERP2-CF02-ENGINEERING-FOUNDATION-20261017-001`
  - Source: `20_Engineering_Workspace/FM02_C2_Implementation_20261013_001/engineering_foundation/` and `docs/engineering/cf02_shared_engineering_foundation.md`.
  - Status: `ACTIVE_BOUNDED`.
- `ERP2-CF02-OFFLINE-VERIFICATION-20261017-001`
  - Status: validation evidence `PASS`; live database `NOT RUN`.
- `ERP2-FM02-REMOTE-TEST-EXECUTION-STANDARD-20261018-001`
  - Remote branch `codex/fm02-item-master-db-test-package-source-custody-20261018-001`, commit `51d2b132aad7531b7fad9dffb80d3e6e8d5f3e37`, tree `09cd5fb766aca278ac4b363e2be877be42d6680b`.
  - Package-scoped Test-Evidence-Contract approval only; DB execution remains `NOT_AUTHORIZED`.

### Module-Specific Evidence

- Design: `ERP2-FM02-SR3-INTEGRATED-DESIGN-20261017-001`; commit `a03859d553541fbd2a4ee89efd4ecbae72ff4bf9`; tree `2fdef10f007e3d55797cf93c84f15a8e3474f8ff`; SHA-256 `16213BDA18A791FE619564E98B536D9FDF34480751F3DC913689DBEF59A30C28`.
- Database implementation: `ERP2-FM02-DATABASE-IMPLEMENTATION-20261017-001`; commit `6c21727f31f1e1dd88377cf06a7af81ff1cd5c93`; exactly 7 files; 12 local checks passed; no live DB or migration execution.
- Backend/API implementation: `ERP2-FM02-BACKEND-API-IMPLEMENTATION-20261017-001`; custody commit `9be1df11d3b16d900c05e9f8725b4b1bcb87fd26`; source implementation commit `44e3a57beef18e04a9e6b5a28ce9f9b3f34fdf3c`; exactly 2 files.
- Frontend/UI implementation: `ERP2-FM02-FRONTEND-UI-IMPLEMENTATION-20261017-001`; commit `f73cf00ae7bfe844e3b9464ca707301f6715c860`; tree `10b0e3edd4354584d1e49932763a3b11fa249dbf`; 11 files; earlier tooling was unavailable.
- Cross-layer candidate: `ERP2-FM02-ITEM-MASTER-CROSS-LAYER-INTEGRATION-20261017-001`; commit `4030d23719d4fd2bdf05223d78039b3d8136fc56`; exactly 16 paths; source-level only.
- UOM integration: `ERP2-FM02-ITEM-MASTER-UOM-INTEGRATION-20261017-001`; final commit `d73588f5e528538aa6b12225abdcd96884ac11ad`; tree `ba57e39f819f9c17146061fd5b21802a44998710`; frontend verification PASS, full E2E/DB/SQL/runtime `NOT RUN`.
- Independent TEST: `ERP2-FM02-ITEM-MASTER-INDEPENDENT-TEST-20261018-001`; final design state `TEST_DESIGN_CLOSURE=HOLD`; execution evidence remains bounded and partial.
- Migration source admission: `ERP2-FM02-MIGRATION-SOURCE-ADMISSION-20261018-001`; commit `7b9620a25713338c8e6a60a55de8685070fe8538`; TC09 corrected contract test 6 passed; historical failure preserved.
- Non-DB harness: `ERP2-FM02-NON-DB-HARNESS-SOURCE-CUSTODY-20261018-001`; commit `13b124592287939bb86d7b2f8b2094de50a6d65c`; four mock-only tests passed.
- DB Test package: `ERP2-FM02-ITEM-MASTER-DB-TEST-EXECUTION-PACKAGE-20261018-001`; commit `dc1cb358f696f44a496107c790d5b1da79ca0d4b`; `DB_TEST_PACKAGE=HOLD`.
- Platform recovery preflight: `ERP2-FM02-ITEMMASTER-PLATFORM-HOST-AUTHORITY-RECOVERY-PREFLIGHT-20261018-001`; read-only; `DB_HOST_AUTHORITY`, `DB_EXECUTOR`, and `SAFE_START_METHOD` remain `HOLD`.

### Source Custody and Delivery Lineage

- Group 1: `ERP2-FM02-GROUP1-DESIGN-DOCS-SYNC-20261017-001` (existing index family; four document files).
- Group 2: `ERP2-FM02-GROUP2-SHARED-STANDARDS-SYNC-20261017-001`; commit `4fec1489a2f212c5eb03518c4dd5994d39dfc9c4`; eight files; Coding Convention remains `PROPOSED`.
- Group 3: `ERP2-FM02-GROUP3-SOURCE-ASSETS-SYNC-20261017-001`; commit `703433e2527179ca5972ec7bd8e39f4f43f86f91`; exactly 16 files; hash contract reconciled.
- Pre-Sprint-2 custody: `ERP2-FM02-PRESPRINT02-GITHUB-SOURCE-CUSTODY-20261017-001`; commit `06ec463e431cbeef0f4ba6009e345ce53c5390f3`; exactly 14 files.

## Proposed Index Update Shape

Do not create a second index. Add only cross-reference metadata to the existing records, or create one future proposal record after CIO/CTO acceptance. The proposed fields are:

`layer`, `module`, `source_commit`, `custody_commit`, `tree`, `raw_git_hash`, `checkout_hash`, `status`, `test_scope`, `pending_obligation`, `supersedes_or_depends_on`, and `authorization_boundary`.

Every entry must retain its existing Knowledge ID. A commit is not a KnowledgeVersion unless the existing Knowledge governance rules explicitly promote it.

## Pending Obligations

1. Keep Coding Convention `PROPOSED` until normative owner approval is evidenced.
2. Resolve Engineering A migration source admission and the required baseline object before TC09 static retest can proceed.
3. Keep DB execution, live database validation, SQL/migration runtime, credentials, production and Product-main merge unauthorized.
4. Preserve the distinction between mock-only evidence, source custody, test design, test execution and runtime validation.
5. Preserve raw Git blob hashes separately from CRLF checkout hashes where both exist.
6. Do not infer closure from custody/readback alone; later Test Report updates require their own record update and readback.

## Sequencing

1. Commit this proposal as a review artifact.
2. Obtain CTO/CIO acceptance of the proposed cross-module layer labels and pending obligations.
3. Only after acceptance, update existing Index rows with cross-reference fields; do not duplicate records.
4. Register any newly committed final evidence only after its exact branch, commit, tree, path, hash and status are available.
5. Perform independent Index readback and report unresolved obligations without promoting them.

## Boundary

This proposal performs no Product merge, force-push, history rewrite, file movement, database/runtime/test execution, credential action, migration, production action, or new authorization.
