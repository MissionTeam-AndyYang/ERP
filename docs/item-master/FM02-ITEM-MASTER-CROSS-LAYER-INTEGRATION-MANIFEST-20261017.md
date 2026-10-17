# FM-02 Item Master Cross-Layer Integration Manifest

Integration branch: `codex/fm02-item-master-cross-layer-integration-20261017-001`
Integration base: Product `main` `89b374109312720b3ff6669a9664fb0cf8f9a6ba`

This manifest records exact source-to-target provenance for the bounded Item
Master candidate. It does not authorize database, runtime, migration, or
production execution.

## Design

| Target path | Source commit | Source path | Source SHA-256 |
|---|---|---|---|
| `docs/item-master/Item-Master-Design-Spec.md` | `0715b26515492ef622eb1c70ca9d5cecad64d115` | `docs/item-master/Item-Master-Design-Spec.md` | `D7A9D8851F3A0B652461ED40A0B994D1F1B479D53CB30572C8A0F0CE3FA4A3E6` |

## Database

Database source commit: `6c21727f31f1e1dd88377cf06a7af81ff1cd5c93`

| Target path | SHA-256 |
|---|---|
| `04_Engineering/Database/fm02_item_master_0007_code_allocation_nonreuse.sql` | `E7B3CC8E6E167D5B05708B06C6312E4768EB5C36B3C8FBDA2F501AD37A28173C` |
| `04_Engineering/Database/fm02_item_master_0007_code_allocation_nonreuse_down.sql` | `BCD38D279615424B22EB9EBA257BA663CE369944D84E4D9813DB7872C8FC1780` |
| `04_Engineering/Database/fm02_item_master_0008_name_change_audit.sql` | `98255C83A0A337199220A94E49DA5E74141235652A2DAFEE6BE021F32D91AF1A` |
| `04_Engineering/Database/fm02_item_master_0008_name_change_audit_down.sql` | `D12956F1D8BC8F5CDD24251A43A7B0FC3738AB97E2E6220E629A74A9A3E4D2A0` |
| `04_Engineering/Database/fm02_item_master_0009_lifecycle_successor.sql` | `D1BF26C1760407C85287FE7B407DF5BB2F680B4F757D7B1997D4FFD3AF63A86F` |
| `04_Engineering/Database/fm02_item_master_0009_lifecycle_successor_down.sql` | `35129B2C353F528BA48CE3B5A04AF1986E0CA54D7A8D6CE5FE09D92A897A2B8E` |
| `04_Engineering/Database/tests/test_fm02_item_master_approved_contract.py` | `B430EE96A06FC89EF84CC146C4A7631EF8151090C880F9077BEAA15E99F2FE6C` |

Migrations `0003–0006` are not included in this integration diff and remain
unchanged.

## Backend/API

Engineering C implementation correction commit: `f894380c7b30b759ea7bec9564ccbd3f50b8c612`
Original Engineering C custody commit: `9be1df11d3b16d900c05e9f8725b4b1bcb87fd26`
Engineering C remains the implementation executor; this integration is custody
assembly by Engineering A.

| Target path | Source path | Source SHA-256 |
|---|---|---|
| `04_Engineering/Application/ERP-2.0/restserver/package/fm02_foundation/foundation.py` | `04_Engineering/Application/ERP-2.0/restserver/package/fm02_foundation/foundation.py` | `89CFFD93E00A34EB7EC2AEDC2B83B0D085FF3989E476313746A4F12861B83028` |
| `backend/tests/test_fm02_item_master_contract.py` | `backend/tests/test_fm02_item_master_contract.py` | `72078E33BEEA234D321875825D91234D7F6A476C2C9E16587BF141CE0442D63A` |

## Frontend

Prior frontend remote commit: `f73cf00ae7bfe844e3b9464ca707301f6715c860`
Corrected Engineering D commits: `d9b69d56a701755a15224c3ab1ebeb9eeabbbf58`,
`7a9065549cafcb88d5f6839020a98db516b6b78b`.

| Target path | Corrected source commit | Source SHA-256 |
|---|---|---|
| `src/components/items/item-master-maintenance-panel.test.tsx` | `d9b69d56a701755a15224c3ab1ebeb9eeabbbf58` | `02B54B38C3550A9D4CFC4AE3967FC5DEC68F77B27A98CD202CDD47ADEBF28AEE` |
| `src/components/items/item-master-maintenance-panel.tsx` | `d9b69d56a701755a15224c3ab1ebeb9eeabbbf58` | `9CD77488829232F47B524053303B3948BCDF3A693E36F0D490C64157253486B5` |
| `src/services/api-client.ts` | `7a9065549cafcb88d5f6839020a98db516b6b78b` | `957AB6105632CB98C1D3E72A559150BA1D9D0FFDFA5E5D11CEC311997EDA91A8` |
| `src/services/item-master-governance-api.ts` | `d9b69d56a701755a15224c3ab1ebeb9eeabbbf58` | `C914B0E1378D7836DCAE7D1C5EA11740B76F05DA7B8D7E6758A221CC0F8AEB46` |
| `src/types/item-master-governance.ts` | `d9b69d56a701755a15224c3ab1ebeb9eeabbbf58` | `FF454CB48BC3A6C696230B3BC69FD4BF9C93897088C7CDA824ED03EBDA6131CD` |

## Execution boundary

No SQL, database, runtime, production, Product `main`, force-push, or merge
operation is authorized by this manifest.
