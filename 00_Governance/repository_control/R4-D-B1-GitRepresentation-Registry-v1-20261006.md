# R4-D-B1 GitRepresentation Registry v1

## Control Record

- Admission: `R4-D-B1-ITEM-API-READONLY-SLICE`
- Source repository: `ERP-2.0`
- Source branch: `main`
- Frozen source commit: `89b374109312720b3ff6669a9664fb0cf8f9a6ba`
- Canonical repository: `ERP2.0-GOVERNED-MONOREPO-R4-X1`
- Canonical branch: `main`
- Canonical target prefix: `04_Engineering/Application/ERP-2.0/`
- Revised closure: `16 files`
- Source history ref: `refs/source-history/erp-2.0/89b374109312720b3ff6669a9664fb0cf8f9a6ba`
- KnowledgeItem / KnowledgeVersion / Representation / Storage: `not created for ordinary source code`
- Custodian: `Repository Office / KRO`

## Registry Entries

| # | Source path | Canonical path | SHA-256 | State |
|---:|---|---|---|---|
| 1 | `restserver/package/items/__init__.py` | `04_Engineering/Application/ERP-2.0/restserver/package/items/__init__.py` | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` | ACTIVE / VERIFIED |
| 2 | `restserver/package/items/items.py` | `04_Engineering/Application/ERP-2.0/restserver/package/items/items.py` | `F2E3A0248064387E8E016669DF2B6BA6FDFE966A4C19FB010E0CA3E9CD1D775E` | ACTIVE / VERIFIED |
| 3 | `restserver/package/restserver/api/v2/items.py` | `04_Engineering/Application/ERP-2.0/restserver/package/restserver/api/v2/items.py` | `88F2F631BFE2F1B85C78F6715A02C49C8EEC938C10DAC05995D757F0367C90DB` | ACTIVE / VERIFIED |
| 4 | `restserver/package/restserver/api/v2/items_uri.py` | `04_Engineering/Application/ERP-2.0/restserver/package/restserver/api/v2/items_uri.py` | `5CDF6625FC7D91F849373DA7BAC9BEC7C7A22EF48BC81B375D1BF75981367E91` | ACTIVE / VERIFIED |
| 5 | `restserver/tests/test_items_v2_api.py` | `04_Engineering/Application/ERP-2.0/restserver/tests/test_items_v2_api.py` | `7B7D31813C30CA505F21BAC66D49A396292176FC714984D215EB8B589041EA1C` | ACTIVE / VERIFIED |
| 6 | `restserver/package/auth/auth.py` | `04_Engineering/Application/ERP-2.0/restserver/package/auth/auth.py` | `FCA4F69DB95F546DFC26D1A400253A7285D5C654608666B4D57C02F94ACB7B9D` | ACTIVE / VERIFIED |
| 7 | `restserver/package/common/common.py` | `04_Engineering/Application/ERP-2.0/restserver/package/common/common.py` | `9C93154397E427B5303162F7C9A3F0FE12B299E63B4E3607BFEA458A03D11A99` | ACTIVE / VERIFIED |
| 8 | `restserver/package/dbwrapper/dbmgr.py` | `04_Engineering/Application/ERP-2.0/restserver/package/dbwrapper/dbmgr.py` | `B2BAAA34B2BB1784893829C510880A52C7E99F605459D10E1E4E2A760AC4DB36` | ACTIVE / VERIFIED |
| 9 | `restserver/package/dbwrapper/table.py` | `04_Engineering/Application/ERP-2.0/restserver/package/dbwrapper/table.py` | `488967840856D7639B7BA879F46C4D4DFD3F6E1626E9F128ECAEE01322D3A9F2` | ACTIVE / VERIFIED |
| 10 | `restserver/package/dbwrapper/maria.py` | `04_Engineering/Application/ERP-2.0/restserver/package/dbwrapper/maria.py` | `9968F40374070B175BCBF5C47CB60C814056CA0556C2AB31573D27CB27304395` | ACTIVE / VERIFIED |
| 11 | `restserver/package/log/log.py` | `04_Engineering/Application/ERP-2.0/restserver/package/log/log.py` | `9E6E8A3DDD8AEEC7AFC2E40439169A73E346FCA880E392CCD1CD7BA8F257D9EC` | ACTIVE / VERIFIED |
| 12 | `restserver/package/restserver/api/apibase.py` | `04_Engineering/Application/ERP-2.0/restserver/package/restserver/api/apibase.py` | `64706850AD9973671A0133BCBD637A6C2C3DCA43CF57ABB407EC0E5470D6EA1E` | ACTIVE / VERIFIED |
| 13 | `restserver/package/restserver/api/common.py` | `04_Engineering/Application/ERP-2.0/restserver/package/restserver/api/common.py` | `2479337726363462AA52912E7F1060D40F6D6034DE9FC06DFF27E1E91B33C262` | ACTIVE / VERIFIED |
| 14 | `restserver/package/restserver/api/util.py` | `04_Engineering/Application/ERP-2.0/restserver/package/restserver/api/util.py` | `C1B10CE07839BA4E1DB12658C8716F85BD4774A9A638E5F7A597B3059FE40B62` | ACTIVE / VERIFIED |
| 15 | `restserver/package/restserver/api/v2/warehouse.py` | `04_Engineering/Application/ERP-2.0/restserver/package/restserver/api/v2/warehouse.py` | `706C6E84B0AE9C2D0F4547CB79DB09884EE0A5E3F3D046B81B6952E9C91298C2` | ACTIVE / VERIFIED / UNCHANGED |
| 16 | `restserver/package/util/util.py` | `04_Engineering/Application/ERP-2.0/restserver/package/util/util.py` | `7E6F139253E244C1EEF811F07B68CFF0FFB99113EBAD3A89DD7BA5DC59D4AE49` | ACTIVE / VERIFIED |

## Validation and Boundary

- Source bytes came from a clean clone at the frozen commit; the original dirty source worktree was not used or changed.
- Python 3.13.14 compile passed for the admitted closure.
- Import and Flask route registration passed for dashboard and detail routes.
- Seven bounded Item API tests passed against SQLite `:memory:`.
- `maria.py` was import-safe and did not create a database connection.
- No frontend, config template, migration, runtime, schema, production, release, or deployment content was admitted.
- No persistent MariaDB, credentials, or production access was used.
- Registry state is `ACTIVE / IN_SYNC / READBACK VERIFIED` after canonical acceptance.
