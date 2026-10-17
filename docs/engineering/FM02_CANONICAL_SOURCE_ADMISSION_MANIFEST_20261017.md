# FM-02 Canonical Source Admission Manifest — Preparation

Manifest ID: `ERP2-FM02-CANONICAL-SOURCE-ADMISSION-MANIFEST-20261017-001`
Decision reference: `ERP2.0-CIO-GOV-SHARED-FOUNDATION-DECISION-AND-EXECUTION-20261017-119`
Status: `PREPARED / NOT AUTHORIZED FOR REMOTE WRITE`
Date: 2026-10-17

## Source and destination

Current source custody repository: `20_Engineering_Workspace/FM02_C2_Implementation_20261013_001/`, branch `codex/fm02-c2-isolated-20261013-001`, HEAD `575aaa6d3282f92102c146cf46c7818c19c46e74`.

Historical Product destination reference: `https://github.com/MissionTeam-AndyYang/ERP.git`, Product `main` baseline `89b374109312720b3ff6669a9664fb0cf8f9a6ba`. Current remote access and push authority are not verified in this execution context.

Governance/Knowledge custody remains separate in `Canonical_ERP2.0_Monorepo/`; it is not a substitute Product source remote.

## Initial source-admission candidate

The prior twelve-file source-completion candidate is the review baseline. It includes:

1. `04_Engineering/Source_Archive/FM02_Sprint01_Implementation_20261012_001/migrations/fm02_item_master_0001.sql`
2. `04_Engineering/Source_Archive/FM02_Sprint01_Implementation_20261012_001/migrations/fm02_item_master_0002_business_names.sql`
3. `04_Engineering/Source_Archive/FM02_Sprint01_Implementation_20261012_001/src/fm02_item_api.py`
4. `04_Engineering/Source_Archive/FM02_Sprint01_Implementation_20261012_001/tests/test_fm02_item_api.py`
5. `04_Engineering/Database/fm02_item_master_0003_integrity_foundation.sql`
6. `04_Engineering/Database/fm02_item_master_0003_integrity_foundation_down.sql`
7. `04_Engineering/Application/ERP-2.0/restserver/package/fm02_foundation/foundation.py`
8. `04_Engineering/Application/ERP-2.0/restserver/tests/test_fm02_foundation.py`
9. `04_Engineering/evidence/FM02-IM-FOUNDATION-INTEGRITY-01-AS-BUILT-20261012-001.md`
10. `04_Engineering/evidence/FM02-IM-FOUNDATION-INTEGRITY-01-MANIFEST-20261012-001.json`
11. `04_Engineering/evidence/FM02-CENTRAL-SOURCE-COMPLETION-20261013-001.md`
12. `04_Engineering/evidence/FM02-CENTRAL-SOURCE-COMPLETION-MANIFEST-20261013-001.json`

Newer FM-02 Backend/API, UI, test, documentation, CF-01 and CF-02 files are inventoried separately and must not be silently excluded or mixed into this candidate. They require an exact deduplicated manifest with source commits, hashes and destination mapping before admission.

## Newer FM-02 inventory at source HEAD

The following files are the exact tracked delta from source commit `c145cb0` through source HEAD `701b265`. Each maps to the same relative path under the future Product integration branch; no destination admission is implied.

| Path | Source commit | SHA-256 |
|---|---|---|
| `backend/alembic/env.py` | `701b265` | `0079E1F4C82508AE9963BDC0FECB59C498CF200FC03C84BFD9AA6C418DAAE8EE` |
| `backend/alembic/versions/20260517_0001_ewdb_baseline.py` | `701b265` | `1C177FB84CA495647570D97C8641CAFBF0376552906D646DBF74D40F197E0602` |
| `backend/app/api/v1/endpoints/fm02_c2.py` | `701b265` | `A6B3CAA3709424DF4BF1522B03039890CC8729B94F389E4F84D3A89AF07354C1` |
| `backend/app/db/base.py` | `701b265` | `529BF1D3B705B8390BF09A555954D6EBB2065E0250890F07C42B461F5D61BD6F` |
| `backend/app/db/session.py` | `701b265` | `27FDDC78D6C678010B9C02E7F7552C66B3C10B3AB820DB62CF3516E39FB94BB2` |
| `backend/app/main.py` | `701b265` | `E7A08A2C7749B9C457C6534ED17EA593DA8B3E2BD995AD4DBDF0AF897A4EBA7C` |
| `backend/app/services/fm02_c2.py` | `701b265` | `9090B9ED0A5D4B200A88D9D82FCBE94F9660D7FABB985E10C4CD043D71A8B990` |
| `backend/tests/conftest.py` | `701b265` | `095A047A02811E219187B81ED6F1035806EDB5F8FB04AB28402FA4C1B5E63D9E` |
| `backend/tests/test_health.py` | `701b265` | `B2D90D561F4C1829712ED26B9AD20F7BBCE750CEDC670EB60343FD02C3D2E74E` |
| `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/CF01_DOCUMENTATION_WORKING_MECHANISM_20261017.md` | `701b265` plus status correction | `64180CED3A6F645692C658D1D0339450C6E82DB2A1F548D55A442B63602BB88B` |
| `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/README.md` | `701b265` | `91AFE0FBBF078EE17E279440CA67C406A61C64057D8D2D61A4E1F868E9BF429A` |
| `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/validate_cf01_b02.py` | `701b265` | `F4A6250041925F5110430B78C72B44342C481B7A692ADFF5475EAA6016BA33D0` |
| `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/demonstrations/CF01_B02_READ_ONLY_DEMONSTRATION_20261017.md` | `701b265` | `A92478349D6F88D0F73B25699D49613B8A64FC9648B7E09D53C5A6F771E2759B` |
| `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/templates/CF01_CHANGE_IMPACT_SYNC_TEMPLATE.md` | `701b265` | `BBC18FB2A005D6CD0670858A9137B54D75E76ACD3E6ED8E1374D42B56E18E445` |
| `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/templates/CF01_CROSS_MODULE_TRACEABILITY_TEMPLATE.md` | `701b265` | `67826724911365B73B2B96224A53DA7B38621CF459B13943C3FE8813B4539041` |
| `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/templates/CF01_DOCUMENT_IDENTITY_LIFECYCLE_TEMPLATE.md` | `701b265` | `9EC6AA2088E76D2ED5AB035F8AB0E537012F51A966728C1F2CAFBE8522FEE7F3` |
| `docs/engineering/CROSS_MODULE_CODING_CONVENTION_APPROVAL_REQUEST_20261017.md` | `701b265` | `6F5BFF90572883151302AE55DCB72DC22E0E17814604C616C87327E35D9E1C18` |
| `docs/engineering/CROSS_MODULE_FOUNDATION_DELIVERY_20261017.md` | `701b265` | `41EF97A0A6F9373B42B302517BB5BD3C974B146C613B6B062EA5943856E01E66` |
| `docs/engineering/CROSS_MODULE_FOUNDATION_KNOWLEDGE_RELAY_20261017.md` | `701b265` | `D3DD11D18AFF2C1DBF9D92A0CFA41B505AE88AC532EE0FC424800EF6D7D7F36C` |
| `docs/engineering/cf02_module_template_guidance.md` | `701b265` | `E9D5DFECC06E7CC5FC21F1751B1EFC49B8056B874A05E1D01533DF593A5D0CFF` |
| `docs/engineering/cf02_offline_verification_20261017.md` | `701b265` | `F051A63523EF59DE02B1C5800D672AE58E0D0702F8DCE972BCE0166F9F8F0217` |
| `docs/engineering/cf02_shared_engineering_foundation.md` | `701b265` | `C1D9840977F418F3DC634D0651BBAC90B2887C5F2DC899FA9E6A16E54DAE665D` |
| `docs/fm02/FM02_SPRINT01_DOCUMENT_COMPLETION_MATRIX_20261016_104.md` | `701b265` | `C77BB1C7A37804424391DCB61B2002806CE3FE7A59776C96F28E2CDC499D2A28` |
| `docs/fm02/FM02_SPRINT01_REPOSITORY_KNOWLEDGE_UPDATE_RELAY_20261017_105.md` | `701b265` | `7F747F390C74C1D0E7975CBA17023436ADB44820694DD336455602A97E35850E` |
| `engineering_foundation/README.md` | `701b265` | `09280381C897773748D1CE6B9EBB97607CDF6116B15A5DC8436843144DA34B8C` |
| `engineering_foundation/checks/quality_check.ps1` | `701b265` | `5094F6C0DA10BAA72EAC1F412882C2C485E7A9ADF28E44C02CE9934725F875B1` |
| `engineering_foundation/checks/quality_check.sh` | `701b265` | `01F019B17D725A9598F6975E58376872C8E2D7CF826EE18A6C7B99E22CC31F59` |
| `engineering_foundation/env/backend.env.example` | `701b265` | `509B3B5F43C5FAF2DA61579D5698B7518B971C223619E559E12DE7F448D3EE79` |
| `engineering_foundation/env/frontend.env.example` | `701b265` | `3ED2447EDDC613A4E4D773CC67CD6B1C1989B0FB853A87FF4F46B20C53A72350` |
| `engineering_foundation/environment/dev_test_profile.md` | `701b265` | `3A3D78522652127EE348872424A17F3007E3E901CCB2EAC739E2461E86492F77` |
| `package-lock.json` | `701b265` | `1F9FD52610EBAE6CEA3C48DB57F225973A8991722615C8091EE29B16142E3977` |
| `package.json` | `701b265` | `DCF959F3950A4E9779B40972CEB62FFD2B16275F4415A712FB0157431FA554CD` |
| `src/components/items/c2-reference-panel.test.tsx` | `701b265` | `C9AE7162F75A066F50897EB296A89C0BB7E8CB946451853C9AE0C414A1D2873B` |
| `src/components/items/c2-reference-panel.tsx` | `701b265` | `4613501D8B857BBD7392824CA504800B54E8CD9F9290BC128975079B69ADF2D7` |
| `tsconfig.json` | `701b265` | `5C0AEC594B88A24C93C677C3BFFEC29A48C647B874EAC12B997D4235C0704D31` |
| `vitest.config.ts` | `701b265` | `1BD0AC6716A115995DB504730481DA07255731F243C891DE58A645AC06263473` |
| `vitest.setup.ts` | `701b265` | `8FD535EE28C9A2B3AAF066A2AC16B8C80572E685E761AC30ED255CA90DF25C5C` |

The current pre-existing `evidence/` directory is untracked and excluded from admission until separately reviewed.

## Required protected integration method

Use a fresh non-default integration branch from a verified Product `main`, stage only manifest-listed paths, review the source/destination diff and conflicts, preserve untracked evidence, open a pull request into protected `main`, and verify the remote commit/tree from an independent readback. No force-push, direct protected-main update, merge or remote write is authorized by Directive 119.
