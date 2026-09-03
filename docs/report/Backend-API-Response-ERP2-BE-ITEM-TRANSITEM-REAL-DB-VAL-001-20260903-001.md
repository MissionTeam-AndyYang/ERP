# Backend API Response - ERP2-BE-ITEM-TRANSITEM-REAL-DB-VAL-001

## 1. Participant / Project Identity

| Item | Value |
| --- | --- |
| Project | ERP-2.0 |
| Validation Role | Backend/API Codex validation participant |
| Assignment | ERP2-BE-ITEM-TRANSITEM-REAL-DB-VAL-001 |
| Environment Boundary | Non-production Shared DEV DB only |
| Validation Date | 2026-09-03 |

## 2. Commit / Branch

| Item | Value |
| --- | --- |
| Branch | main |
| Validation Base Commit | ebe6bbb Document backend env retest readiness |
| Local Code Modification | No backend code modification in this validation report |

## 3. Wrapper / Equivalent Injection Use

Used the CTO/Engineering-provided bounded wrapper:

`invoke_shared_dev_item_transitem_db_access.ps1`

The wrapper injected child-process environment variables only. No raw secret values were printed, copied, or persisted.

Safe wrapper metadata observed:

| Item | Value |
| --- | --- |
| environment_id | ERP2-SHARED-DEV-DB-ENDPOINT-A1 |
| credential_class | ERP2_SHARED_DEV_ITEM_TRANSITEM_NP_READONLY |
| host | 192.168.10.180 |
| port | 3307 |
| database | erp2_shared_dev_item_transitem_np |
| user | erp2_shared_dev_readonly |
| secret_values_exposed | false |

## 4. DB Auth Result

**Result: PASS**

The bounded read-only credential successfully connected to MariaDB.

| Item | Value |
| --- | --- |
| Database Version | 11.4.10-MariaDB |
| Table Count Observed | 3 |

## 5. Fixture Read Result

**Result: PASS**

Observed fixture tables:

| Table | Row Count |
| --- | ---: |
| shared_dev_environment_registration | 1 |
| item_identity_shared_dev | 2 |
| transaction_item_shared_dev | 2 |

Observed fixture registration:

| Field | Value |
| --- | --- |
| environment_id | ERP2-SHARED-DEV-DB-ENDPOINT-A1 |
| dataset_id | ERP2-ITEM-TRANSITEM-SHARED-DEV-FIXTURE-001 |
| schema_model_id | ERP2-ITEM-TRANSITEM-SHARED-DEV-MODEL-001 |
| environment_state | REGISTERED_NON_PRODUCTION_PRIVATE_SHARED_DEV |
| boundary_label | NON_PRODUCTION_SHARED_DEV_ONLY_NOT_PRODUCTION_NOT_SOURCE_OF_TRUTH |

Observed item fixture rows:

| item_code | item_display_name | item_category | base_uom_code |
| --- | --- | --- | --- |
| SD-ITEM-001 | Shared DEV Synthetic Item A | SYNTHETIC_ITEM_IDENTITY | EA |
| SD-ITEM-002 | Shared DEV Synthetic Item B | SYNTHETIC_ITEM_IDENTITY | KG |

Observed transaction item fixture rows:

| transaction_item_id | item_id | transaction_context |
| --- | --- | --- |
| TRANSITEM-SD-001 | ITEM-SD-001 | SYNTHETIC_RECEIPT_REFERENCE |
| TRANSITEM-SD-002 | ITEM-SD-002 | SYNTHETIC_ISSUE_REFERENCE |

## 6. Backend Config Treatment

The current backend DB wrapper reads the following environment variables:

| Backend Variable | Runtime Mapping |
| --- | --- |
| DB_HOST | ERP2_SHARED_DEV_DB_HOST |
| DB_PORT | ERP2_SHARED_DEV_DB_PORT |
| DB_NAME | ERP2_SHARED_DEV_DB_NAME |
| DB_USER | ERP2_SHARED_DEV_DB_USER |
| DB_PASSWORD | ERP2_SHARED_DEV_DB_PASSWORD |

The mapping was applied inside the child process only. No repository config file was changed.

For HTTP endpoint validation, `TOKEN_ENABLED=1` was set in the child process to bypass session alive-time refresh, because the Shared DEV DB fixture does not include the backend `session` table. The API request still supplied an `x-auth-token` header to pass the common API header check.

## 7. Real HTTP Startup

**Result: PASS**

The Flask application started locally against the Shared DEV DB through the wrapper.

| Item | Value |
| --- | --- |
| Local URL | http://127.0.0.1:5017 |
| Framework | Flask development server |
| Scope | Runtime verification only; not production deployment |

Initial HTTP attempt without `TOKEN_ENABLED=1` returned `missing token parameter` or failed at `session` table lookup. The second HTTP attempt used the non-production test switch described above and reached the actual business query layer.

## 8. Authorized Item / Transaction Item Endpoint Results

**Result: BLOCKED BY SCHEMA / MODEL ALIGNMENT**

The backend endpoints are reachable, but the Shared DEV fixture database currently contains only the governed fixture tables listed above. The implemented API code queries the formal ERP ORM tables, which are not present in this Shared DEV DB.

| Endpoint | HTTP Status | API Code | Result |
| --- | ---: | ---: | --- |
| GET /api/v2/items/dashboard?count=5 | 400 | 1001 | Missing formal table `material` |
| GET /api/v2/items/SD-ITEM-001/detail | 400 | 1001 | Missing formal table `material` |
| GET /api/v2/transitems/dashboard?count=5 | 400 | 1001 | Missing formal table `trans_items` |
| GET /api/v2/transitems/companies/CUST-001/detail | 400 | 1001 | Missing formal table `company` |
| GET /api/v2/transitems/transitems/TRANSITEM-SD-001/detail | 400 | 1001 | Missing formal table `trans_items` |

Required formal tables expected by the current Item / Transaction Item API implementation include at least:

`material`, `inproduct`, `product`, `goods`, `trans_items`, `company`, `contract`, `payment`.

## 9. Read-Only Negative Control

**Result: PASS_WRITE_DENIED**

A controlled write-negative check was executed through the wrapper. The read-only credential rejected the write attempt as expected.

## 10. UX Real-Backend Validation Readiness

**UX real-backend validation cannot proceed yet for Item / Transaction Item endpoints against this Shared DEV fixture database.**

The blocker is not DB authentication. The blocker is that the current Shared DEV fixture model and the backend API ORM model are not aligned:

- Shared DEV DB currently provides governed fixture tables: `item_identity_shared_dev`, `transaction_item_shared_dev`, and `shared_dev_environment_registration`.
- Current backend API implementation queries formal ERP tables such as `material`, `trans_items`, and `company`.

## 11. Blockers

1. Shared DEV DB does not contain the formal ERP tables required by the current implemented API.
2. Shared DEV DB does not contain the `session` table required by the standard token alive-time refresh path.
3. The current governed fixture tables are useful for DB credential and fixture-read validation, but they are not directly compatible with the implemented API contracts.

## 12. Recommended Next Action

Choose one of the following paths before rerunning UX real-backend validation:

1. Engineering/DB owner provides formal ERP-compatible non-production tables and fixture rows for Item / Transaction Item validation.
2. CTO/CIO explicitly authorizes a bounded adapter layer that maps the current governed fixture tables to the existing API contract for validation only.
3. Engineering provides a separate non-production MariaDB database seeded with the formal ORM tables used by the current backend implementation.

## 13. Final Classification

**DB_AUTH_PASS_FIXTURE_READ_PASS_READONLY_CONTROL_PASS_HTTP_START_PASS_API_BLOCKED_BY_SCHEMA_MODEL_ALIGNMENT**

This classification means:

- Shared DEV DB connectivity is valid.
- Bounded read-only fixture access is valid.
- The backend server can start with wrapper-based runtime configuration.
- The implemented API cannot complete real-backend endpoint validation until the Shared DEV database schema/fixture model is aligned with the current API implementation.
