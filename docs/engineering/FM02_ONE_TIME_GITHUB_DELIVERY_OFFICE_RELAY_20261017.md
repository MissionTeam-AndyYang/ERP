# FM-02 One-Time GitHub Delivery Office Relay

Relay ID: `ERP2-FM02-ONE-TIME-GITHUB-DELIVERY-RELAY-20261017-129`
Decision reference: `ERP2.0-CIO-GOV-ONE-TIME-GITHUB-DELIVERY-20261017-129`
Prepared by: CTO Office
Status: `READY FOR MANUAL TRANSPORT / OFFICE ACCEPTANCE PENDING`

## To: Engineering Office A

CTO Office assigns the following one-time bounded Git delivery task, subject to your explicit acceptance:

**Task:** `ERP2-FM02-GITHUB-DELIVERY-20261017-001`

**Scope:** deliver the existing 14-file FM-02 source-custody commit to one approved non-default branch of the Product repository. This is source custody only, not Product integration.

**Existing custody commit:** `06ec463e431cbeef0f4ba6009e345ce53c5390f3`

**Local branch:** `codex/fm02-pre-sprint02-source-custody-20261017-123`

**Workspace:** `20_Engineering_Workspace/FM02_PreSprint02_Product_Custody_20261017_001`

**Product repository:** `https://github.com/MissionTeam-AndyYang/ERP.git`

**Base:** Product `main` at `89b374109312720b3ff6669a9664fb0cf8f9a6ba` as previously verified; revalidate before any push.

**Manifest:** `FM02_PRE_SPRINT02_GIT_CUSTODY_ADMISSION_MANIFEST_20261017.md`, SHA-256 `5230C09A7466FE85D7EFBE3B9C05C1AFD4278A669925460C47CB0D08A009D94A`.

Before any remote write, return explicit acceptance, actual executor, task binding, workspace, credential custody, permitted branch and CTO reviewer. Push only after Repository Office accepts the scope and branch/PR policy is verified. Read back the remote commit/tree and exact 14-file list. Open a PR only if permitted; leave it unmerged.

Do not touch Product `main`, force-push, clean the dirty Product worktree, modify the six `KEEP_TARGET` files, merge the four deferred files, include shared standards/evidence, run tests, access databases or authorize Sprint 2.

## To: Repository Office

Please return one explicit `ACCEPTED` or `EXCEPTION` disposition for:

1. The exact 14-file source-only custody scope in the manifest.
2. The Product repository destination boundary.
3. Preservation of six `KEEP_TARGET` files.
4. Deferral of four compatibility files.
5. Separation of shared standards and test evidence.
6. The approved non-default branch and PR policy.
7. Knowledge registration/readback after remote delivery.

No Product admission, runtime integration or Sprint 2 authorization is requested.

## Required return to CTO

Engineering Office A: task acceptance, executor and write-route evidence.

Repository Office: scope and branch/PR disposition.

CTO will then authorize only the mechanical source-custody push if all conditions pass.
