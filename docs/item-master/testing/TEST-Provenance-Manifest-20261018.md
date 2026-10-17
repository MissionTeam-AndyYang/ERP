# FM-02 Independent TEST Provenance Manifest

## Delivery baseline

- Repository: `https://github.com/MissionTeam-AndyYang/ERP.git`
- Source branch: `codex/fm02-item-master-uom-integration-20261017-001`
- Baseline commit: `d73588f5e528538aa6b12225abdcd96884ac11ad`
- Baseline tree: `ba57e39f819f9c17146061fd5b21802a44998710`
- Delivery branch: `codex/fm02-item-master-independent-test-20261018-001`
- Source mutation: none

## Artifact custody

| Source artifact | Delivered path | SHA-256 |
|---|---|---|
| `20_Engineering_Workspace/FM02_C1_Evidence_Completion_20261013_001/FM02-TEST-PLAN-20261013-001.md` | `docs/item-master/testing/Test-Plan.md` | `682A31FC64E863ED1F989E1F736A2768BBF76BD63A89247EC99A96D4B3443567` |
| `20_Engineering_Workspace/FM02_C1_Evidence_Completion_20261013_001/FM02-TEST-CASE-CATALOG-20261013-001.md` | `docs/item-master/testing/Test-Cases.md` | `A48491E03B115A2E381D16958A5017A15B2D4C13FB486D13288CA4B0A568B1C9` |
| `20_Engineering_Workspace/FM02_TEST_Evidence_20261018_012/Test-Report.md` | `docs/item-master/testing/Test-Report.md` | `B8467058B8F9E076EAE65A43223F7F1361583776B2CBBB8311ECBAF26C903586` |

## Actual result counts

| Check | Result | Count / evidence |
|---|---|---|
| Frontend Item Master component test | PASS | 1 file, 5 tests passed |
| Backend FM02 contract test | PASS | 11 passed |
| Static migration/schema contract | FAIL | 5 passed, 1 failed because required legacy migration file `0003` is absent |
| ESLint | PASS | exit 0 |
| TypeScript | PASS | exit 0 |

## Independent verdict

`INDEPENDENT TEST VERDICT = FAIL / STATIC MIGRATION CONTRACT BASELINE DEFECT; NON-DB APPLICATION TESTS PASS`

The exact baseline contains the approved 0007-0009 migration sources but not the legacy 0003-0006 files required by the static migration contract test. No migration, database, SQL, runtime, credential or production operation was performed.

## Scope boundary

- No existing TEST artifact was modified.
- No Product `main` merge or force-push was performed.
- Live MariaDB, SQL execution, migration execution, runtime acceptance and full E2E were not run.
