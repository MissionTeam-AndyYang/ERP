# FM-02 Item Master UOM Integration Manifest

Integration base: `4030d23719d4fd2bdf05223d78039b3d8136fc56`
Target branch: `codex/fm02-item-master-uom-integration-20261017-001`

This bounded delivery adds only the approved C2 UOM source/contract and the
corrected Engineering D UOM frontend files. No migration or database schema
file is included.

## Backend C2 UOM source

Source workspace branch: `codex/fm02-backend-api-implementation-20261017-001`

| Target/source path | SHA-256 |
|---|---|
| `04_Engineering/Application/ERP-2.0/restserver/package/fm02_c2/service.py` | `310CBD0940C58303FB1B6A47F28A35CACE82B6CBB97BD7F4DDE56D136F97E791` |
| `04_Engineering/Application/ERP-2.0/restserver/tests/test_fm02_c2_service.py` | `B2ECB5C17A2A280644BC8D4A6F75C9C37BDE715C60928C800D618F6BAB2A7693` |
| `backend/app/api/v1/endpoints/fm02_c2.py` | `A6B3CAA3709424DF4BF1522B03039890CC8729B94F389E4F84D3A89AF07354C1` |
| `backend/app/services/fm02_c2.py` | `9090B9ED0A5D4B200A88D9D82FCBE94F9660D7FABB985E10C4CD043D71A8B990` |
| `docs/fm02/FM02_C2_MODULE_CONTRACT_20261016.md` | `23F785E90F1E1C751D31069004808FD9A8E78356FF55973FC80D722B859AEA3D` |

Existing C2 backend provenance is preserved; no Backend correction was applied
by this delivery.

## Corrected Engineering D UOM frontend source

Source commit: `7a7eba54bebde4c7e263564e2989b83377c31f9b`  
Parent: `7a9065549cafcb88d5f6839020a98db516b6b78b`

| Target path | SHA-256 |
|---|---|
| `src/components/items/item-master-maintenance-panel.test.tsx` | `461085967D4C860E9C4BFBCD092460AF460A13613897BDCA401DAC311FA76080` |
| `src/components/items/item-master-maintenance-panel.tsx` | `410046D73C8C50F528156F2B40912A0D41C7EF575CE725800F40B42EAF289F33` |
| `src/services/item-master-governance-api.ts` | `E27D5FF2EE35E874355BA4F49EE743AB7D56CE4ECBA15DC78E7722181EC1D397` |
| `src/types/item-master-governance.ts` | `920059677EB4983B81A3966E1B36D7911809C34DC0EAD56BF1668F3808FD6ED5` |

No SQL, database, runtime, production, Product `main`, force-push, or merge
operation is authorized by this manifest.
