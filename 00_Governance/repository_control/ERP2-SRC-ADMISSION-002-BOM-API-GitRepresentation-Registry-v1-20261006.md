# ERP2-SRC-ADMISSION-002-BOM-API-READONLY-SLICE

## Batch Identity

- Pattern: `ERP2.0-SOURCE-ADMISSION-PATTERN-001`
- Cycle: `ERP2-SOURCE-ADMISSION-AUTO-PROGRESSION-001`
- Batch: `ERP2-SRC-ADMISSION-002-BOM-API-READONLY-SLICE`
- Correlation: `ERP2-SRC-ADMISSION-002-BOM-API-READONLY-SLICE-20261006-001`
- ReturnTarget: `ERP-2.0 CTO V2`
- Source repository / branch / commit: `ERP-2.0` / `main` / `89b374109312720b3ff6669a9664fb0cf8f9a6ba`
- Canonical repository / branch: `ERP2.0-GOVERNED-MONOREPO-R4-X1` / `main`
- Canonical target prefix: `04_Engineering/Application/ERP-2.0/`
- Owner / Assignment: Engineering C / `3500021` / `3500024`
- Validation surface: `ERP2-GATE1-PYTHON313-RUNTIME-001`, Python `3.13.14`, SQLite `:memory:`
- KRO custodian: Knowledge Repository / KRO

## Primary Registry Entries

| Source path | Canonical path | SHA-256 | State |
|---|---|---|---|
| `restserver/package/bom/__init__.py` | `04_Engineering/Application/ERP-2.0/restserver/package/bom/__init__.py` | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` | ACTIVE / VERIFIED |
| `restserver/package/bom/bom.py` | `04_Engineering/Application/ERP-2.0/restserver/package/bom/bom.py` | `A19515587A58E76B1C515686C5239DAD49CD211FB8BACD286D264AACEEFC76C9` | ACTIVE / VERIFIED |
| `restserver/package/restserver/api/v2/bom.py` | `04_Engineering/Application/ERP-2.0/restserver/package/restserver/api/v2/bom.py` | `A3BA4086C929C686EF2679EE3ADE92880F74A9C53A50EBE88BC888206E93892C` | ACTIVE / VERIFIED |
| `restserver/package/restserver/api/v2/bom_uri.py` | `04_Engineering/Application/ERP-2.0/restserver/package/restserver/api/v2/bom_uri.py` | `2519F60F0ADB6932E9F69F1E5F12A8059A3488ADEC946E179463AD6C2B3003AF` | ACTIVE / VERIFIED |
| `restserver/tests/test_bom_center_api.py` | `04_Engineering/Application/ERP-2.0/restserver/tests/test_bom_center_api.py` | `D556A81A46C3E29F2F407370A344521709AD9DCD25D7B1926BB9BD209737B2BD` | ACTIVE / VERIFIED |

## Dependency Classification

| Dependency set | Classification | Result |
|---|---|---|
| Existing B1 16-file Item API support closure | REQUIRED_CLOSURE / already canonical | Reused; no new source admission |
| Frontend consumers | DEFERRED | Not admitted |
| Config templates, requirements, migrations, runtime state | EXCLUDED / SUPPORT_PREREQUISITE | Not admitted or mutated |
| New local source dependency beyond B1 closure | HELD_DEPENDENCY | None discovered |

Ordinary source code has no KnowledgeItem / KnowledgeVersion. Git history and KRO control evidence remain distinct from Knowledge authority.
