# FM-02 Product Source Admission Preflight — Directive 120

Record ID: `ERP2-FM02-PRODUCT-SOURCE-ADMISSION-PREFLIGHT-20261017-120`
Decision reference: `ERP2.0-CIO-GOV-REPOSITORY-FOUNDATION-EXECUTION-CLOSURE-20261017-120`
Prepared: 2026-10-17
Status: `READ-ONLY PREFLIGHT / ADMISSION NOT AUTHORIZED`

## Repository identities

| Role | Repository | Evidence |
|---|---|---|
| FM-02 source custody | `20_Engineering_Workspace/FM02_C2_Implementation_20261013_001/` | branch `codex/fm02-c2-isolated-20261013-001`; local HEAD `305cfdae36397bd66ebe8aae53bbbe932c80810b`; clean tracked state with pre-existing untracked `evidence/` preserved |
| Product source/destination | `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0` | local HEAD `89b374109312720b3ff6669a9664fb0cf8f9a6ba`; branch `main...origin/main`; dirty worktree; no mutation performed |
| Product remote | `https://github.com/MissionTeam-AndyYang/ERP.git` | read-only `git ls-remote` succeeded for `main` and historical FM-02 branch |
| Historical FM-02 branch | `codex/fm02-central-source-completion-20261013-001` | remote tip `41e070a58c668505b91e5bcece778a87fc9725c5` |
| Knowledge repository | `Canonical_ERP2.0_Monorepo/` | local `main` HEAD `526b78fbfce16d96afc4310446c49a8568501a1b`; existing untracked governance files preserved; no current A1–A3 readback |

Remote read access is verified. Push authority is not verified; no write or push test was performed.

## Admission candidate

The exact deduplicated candidate is the 49-file inventory in `FM02_CANONICAL_SOURCE_ADMISSION_MANIFEST_20261017.md`: 12 historical source/evidence files and 37 newer Backend/API/UI/test/foundation/document files. The inventory is planning evidence only.

The current Product `main` tree contains 10 of the 49 destination paths and does not contain 39. A path already present is not treated as safe to overwrite; it requires byte-level source/destination review and an explicit conflict decision.

| Destination-state class | Count | Decision |
|---|---:|---|
| Absent on Product `main` | 39 | Candidate for later admission review; no automatic copy or merge |
| Present on Product `main` | 10 | Reconciliation required before admission |
| Pre-existing untracked Product evidence | outside candidate | Preserve; do not stage or delete |

## Present-path conflict set

These paths exist on Product `main` and require explicit source/destination diff review:

| Path | Product `main` blob |
|---|---|
| `backend/alembic/env.py` | `d58a708742ddd1676bfdb59ea80d36c6963b9638` |
| `backend/alembic/versions/20260517_0001_ewdb_baseline.py` | `8a3f8c772eeb1ef076b053323756128eff92fd05` |
| `backend/app/db/base.py` | `47749b68e5d0a593442e609930ed3dd8f6df2bf3` |
| `backend/app/db/session.py` | `07dae885740eab9f022a7f2978ea5c1f3ed1442e` |
| `backend/app/main.py` | `4da3414b8d3f0ba01a37e7bef8dbe80f193e70e1` |
| `backend/tests/conftest.py` | `e0393fd60c54eeee0317f1d9bf08ec35d5f09c4f` |
| `backend/tests/test_health.py` | `8613d3ee533673accc5e58f4bc12e8e402bc788a` |
| `package-lock.json` | `dd1e525b18a2ba46051b26ab1f9d8653f40ccddc` |
| `package.json` | `5af1ec7bb78a26d82335e5a5d40943f054ce39cc` |
| `tsconfig.json` | `9510a915d16e102c305a50ca78d5dda0c15635a1` |

The remaining 39 paths are absent from Product `main` and are not listed individually here because their exact source path/hash is already preserved in the 49-entry canonical manifest. No destination path is admitted by this preflight.

## Required protected integration method

If later authorized, create a fresh non-default integration branch from verified Product `main`; stage only manifest-listed paths; review source/destination diff, conflicts and untracked evidence; open a PR into protected `main`; and independently read back the remote commit/tree. No force push, direct protected-main update, merge or remote write is authorized by this preflight.

## Current verdicts

`FM02_SOURCE_DIFF_REVIEW=HOLD`

`FM02_ADMISSION_SCOPE=HOLD`

Reason: the Product worktree is dirty and 10 candidate paths collide with Product `main`; exact conflict resolution and authorized integration branch/PR execution remain outstanding.
