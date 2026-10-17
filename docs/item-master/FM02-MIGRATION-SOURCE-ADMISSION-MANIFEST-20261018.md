# FM-02 Migration Source Admission Manifest

Manifest ID: `ERP2-FM02-MIGRATION-SOURCE-ADMISSION-20261018-001`
Baseline commit: `d73588f5e528538aa6b12225abdcd96884ac11ad`
Baseline parent: `190485851fe30c36716f2a79debf3b58e3154b5d`
Baseline tree: `ba57e39f819f9c17146061fd5b21802a44998710`
Target branch: `codex/fm02-item-master-migration-source-admission-20261018-001`

## Admission scope

Only the eight missing 0003-0006 forward/rollback source files are admitted. Existing Product files and migrations 0007-0009 are unchanged. This is source custody only; it does not authorize SQL execution, database mutation, migration runtime, production, or merge.

| Destination path | Authoritative source custody | SHA-256 |
| --- | --- | --- |
| `04_Engineering/Database/fm02_item_master_0003_integrity_foundation.sql` | `_fm02int_source_completion_89b`, accepted source commit `561b964d28aeecf228cadd7132bdeb7ca15f97c8`; Physical Integrity Correction receipt `ERP2-FM02-PHYSICAL-INTEGRITY-CORRECTION-CUSTODY-20261013-020` | `B748D7C8BC3EFFCD4A0A3B64FA71154C0240AF224D935BA3AD41485EA9A1E3DF` |
| `04_Engineering/Database/fm02_item_master_0003_integrity_foundation_down.sql` | same authoritative custody | `52A8DAE571DDE09F3E45B24723F0D8F6691D0E14AE484E63A5C835845118469F` |
| `04_Engineering/Database/fm02_item_master_0004_c2_reference_contract.sql` | Group3 source-assets custody receipt `ERP2-FM02-GROUP3-SOURCE-ASSETS-SYNC-20261017-001`, remote commit `703433e2527179ca5972ec7bd8e39f4f43f86f91` | `308DFCAE4B8B8BE23425F70F323E0A4A428D32893B5C45DE380FF07A8B11F892` |
| `04_Engineering/Database/fm02_item_master_0004_c2_reference_contract_down.sql` | same Group3 custody | `1E6BC21FF1E68890C5FB87745024589A1EDDA99FA554D8E3A151D15738EA156F` |
| `04_Engineering/Database/fm02_item_master_0005_c2_package_customer_conversion.sql` | same Group3 custody | `C59140F64F7DD36B6276F908DEF8825EB7B713C4BAEC016E8DF67FD318D42F83` |
| `04_Engineering/Database/fm02_item_master_0005_c2_package_customer_conversion_down.sql` | same Group3 custody | `CB2DFA8A05497382A94FCC5C49F95014EBAD5A032554353AE135DEA6882AA487` |
| `04_Engineering/Database/fm02_item_master_0006_legacy_mapping_reconciliation.sql` | same Group3 custody | `E151550606F97924C831C8FA2B1D204A8B3A50EBB44B48D6911B6A5A6E436451` |
| `04_Engineering/Database/fm02_item_master_0006_legacy_mapping_reconciliation_down.sql` | same Group3 custody | `F3A7D2485B288CF5329BFAC02B8B8CCF56459565E4DCA7CA170C1123030634C7` |

## Lineage and discrepancy

Static lineage is 0003 -> 0004 -> 0005 -> 0006. Existing 0007 -> 0008 -> 0009 files remain in the baseline and retain their existing dependency chain from 0006 onward.

The local C2 implementation copy recorded stale 0003 hashes `358DC797...` and `B2C487B8...`. The authoritative correction explicitly selects the hashes above and identifies those older values as stale/transcription references. The stale files were not admitted.

## Boundaries

No SQL was executed. No database, migration runtime, Product `main`, production, merge, force-push, or unrelated source was modified.
