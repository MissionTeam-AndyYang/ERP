# FM-01 Step 1 Document Custody Manifest

Manifest: `ERP2-FM01-STEP1-DOCUMENT-CUSTODY-20261020-001`  
Custody baseline: `4ec83b8a08c8912de96aa375fd7d613dc4bb961f`  
Purpose: exact-byte custody of the nine CTO-selected formal documents

## Selected documents

| # | Original source path | Canonical custody path | Raw SHA-256 | Status |
|---|---|---|---|---|
| 1 | `16_Program_Office/ERP2.0-FM01-OWNER-BUSINESS-POLICY-DECISION-REGISTRATION-20261019-001.md` | `01_Foundation/repository_knowledge/fm01_g5/owner/ERP2.0-FM01-OWNER-BUSINESS-POLICY-DECISION-REGISTRATION-20261019-001.md` | `DEA0B767EF824B88F0C998D9D0EAFFBEEA6ED5AD5B9B1DBA3432EDF94F6C474F` | ADDED EXACT |
| 2 | `20_Engineering_Workspace/FM01_I1_D_Isolated_20261019_001/docs/fm01/FM01-F2-A-INTEGRATED-PERSISTENCE-DESIGN-20261019-001.md` | `01_Foundation/repository_knowledge/fm01_g5/db/FM01-F2-A-INTEGRATED-PERSISTENCE-DESIGN-20261019-001.md` | `C123905152A7E32082C248AC13866532166528B4B59C844FD8B0662D113CD925` | ADDED EXACT |
| 3 | `20_Engineering_Workspace/FM02_C2_Implementation_20261013_001/docs/FM01_CONDITIONAL_MAINTENANCE_API_CONTRACT_20261018.md` | `01_Foundation/repository_knowledge/fm01_g5/api/FM01_CONDITIONAL_MAINTENANCE_API_CONTRACT-20261018.md` | `BE74D50556FBBD7F8DDE4E293DC4B758CE195B9B5D28E901E7D510464FA1D30F` | ADDED EXACT |
| 4 | `20_Engineering_Workspace/FM01_Organization_Location_Module_Definition_20261008_001/ERP2.0-FM01-UI-UX-CSS-Design-Review-Package-20261019-005.md` | `01_Foundation/repository_knowledge/fm01_g5/ui/ERP2.0-FM01-UI-UX-CSS-Design-Review-Package-20261019-005.md` | `74F286EC62A89CDBA8167BD40E1F5C358080A3754689B1FB24DA022D3D7C5D02` | ADDED EXACT |
| 5 | `20_Engineering_Workspace/FM01_TEST_Design_Review_20261019_004/Test-Plan.md` | `01_Foundation/repository_knowledge/fm01_g5/test/Test-Plan-20261019-004.md` | `6BF5FC5EB6FC7E165E8E6364CF03FDF3971A696555D423EFADE53F0DB29BDDD3` | ADDED EXACT |
| 6 | `20_Engineering_Workspace/FM01_TEST_Design_Review_20261019_004/Test-Cases.md` | `01_Foundation/repository_knowledge/fm01_g5/test/Test-Cases.md` | `322AEE07F7F540AFD358F4008BAAC8268AB426F3E17F30E075F944D52FDB91F0` | EXISTING EXACT |
| 7 | `20_Engineering_Workspace/FM01_TEST_Design_Review_20261019_004/Design-to-Test-Traceability.md` | `01_Foundation/repository_knowledge/fm01_g5/test/Design-to-Test-Traceability.md` | `1BFEA7F497B7B20BE5D75D1B5555AB94DF14E914F9A028C7807461D62A061C90` | EXISTING EXACT |
| 8 | `20_Engineering_Workspace/FM01_TEST_Design_Review_20261019_004/Execution-Contract-Matrix.md` | `01_Foundation/repository_knowledge/fm01_g5/test/Execution-Contract-Matrix.md` | `8AF6D9EB471B2A91E9A7056B693320AC649E2F1B8EE7D0D8EAE0F90E78BC1696` | EXISTING EXACT |
| 9 | `20_Engineering_Workspace/FM01_TEST_Design_Review_20261019_004/Remote-DB-Test-Package-Design.md` | `01_Foundation/repository_knowledge/fm01_g5/test/Remote-DB-Test-Package-Design.md` | `3A5360346779C639212ED355A954914BF6160A38382D7D0B86F0291F883D1FC9` | EXISTING EXACT |

## Variant preservation

The pre-existing custody file `01_Foundation/repository_knowledge/fm01_g5/test/Test-Plan.md` was preserved unchanged because its raw SHA-256 is `02DACE3BB99E6C40B1D2666F100E5156F9380695193E3F42D039CD2C33488F88`, which differs from the CTO-selected source hash. The exact selected Test Plan is therefore represented at the date-qualified canonical path above; no historical file was overwritten or relabeled.

## Boundary

This manifest records document custody only. It does not approve design, authorize Step 2, authorize source coding, execute tests, perform DB/SQL/migration/runtime work, modify Product `main`, or authorize Production/Cutover/Go-Live.
