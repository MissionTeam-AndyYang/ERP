# Backend API Response - ERP2-BE-ITEM-TRANSITEM-REAL-DB-VAL-RERUN-001

## 1. Participant / Project Identity

| Item | Value |
| --- | --- |
| Project | ERP-2.0 |
| Validation Role | Backend/API Codex validation participant |
| Authorization ID | ERP2-CIO-SHARED-DEV-DB-PRIVATE-ACT-001 |
| Work Item | ERP2-BE-ITEM-TRANSITEM-REAL-DB-VAL-RERUN-001 |
| Environment Boundary | Non-production Shared DEV DB only |
| Validation Date | 2026-09-03 |

## 2. Commit / Branch Used

| Item | Value |
| --- | --- |
| Branch | main |
| Validation Base Commit | 9f18e68 Document shared dev backend DB validation |
| Git Sync Before Rerun | `git pull origin main` completed; already up to date |
| Backend Product Code Change | None in this rerun |

## 3. DB Auth Result

**Result: PASS**

The bounded read-only participant credential successfully connected to the Shared DEV MariaDB instance through the Engineering B wrapper.

| Item | Value |
| --- | --- |
| Environment ID | ERP2-SHARED-DEV-DB-ENDPOINT-A1 |
| Database | erp2_shared_dev_item_transitem_np |
| Database Version | 11.4.10-MariaDB |
| Credential Class | ERP2_SHARED_DEV_ITEM_TRANSITEM_NP_READONLY |
| Secret Exposure | No raw secret values printed, copied, or persisted |

## 4. Formal Table Visibility / Row Count Sanity

**Result: PASS**

The rerun confirmed that Engineering A's formal ERP-compatible fixture package is now visible through the read-only participant credential.

| Table | Row Count |
| --- | ---: |
| session | 1 |
| material | 2 |
| inproduct | 1 |
| product | 1 |
| goods | 1 |
| trans_items | 2 |
| company | 2 |
| contract | 2 |
| payment | 2 |

Additional visible fixture/support tables:

`batch_number`, `bom`, `bom_item`, `inproduct_bom_spec`, `inventory_record`, `item_identity_shared_dev`, `product_bom_spec`, `product_spec`, `shared_dev_environment_registration`, `transaction_item_shared_dev`, `warehouse_inventory_reservation`, `warehouse_quality_hold`.

## 5. Real HTTP Startup Result

**Result: PASS**

The Flask backend application started locally against the Shared DEV DB through the wrapper.

| Item | Value |
| --- | --- |
| Local URL | http://127.0.0.1:5020 |
| Runtime Config | Wrapper-injected child-process environment variables mapped to backend `DB_*` variables |
| Token Test Mode | `TOKEN_ENABLED=1` used for HTTP business endpoint validation; see token/session treatment below |
| Production Boundary | Flask development server only; no production deployment |

## 6. Authorized Item API Endpoint Results

**Result: PASS**

The Item endpoints were validated through real HTTP calls against the formal ERP-compatible Shared DEV fixture. Detail validation used a dashboard-derived identifier internally and did not print database payload identifiers.

| Endpoint | HTTP Status | API Code | Payload Keys | Result |
| --- | ---: | ---: | --- | --- |
| GET /api/v2/items/dashboard | 200 | 0 | `categorySummary`, `count`, `items`, `maintenanceSuggestions`, `serverTimestamp`, `start`, `summary`, `total` | PASS |
| GET /api/v2/items/{item_no}/detail | 200 | 0 | `bomUsage`, `inventorySummary`, `item`, `maintenanceSuggestions`, `recentBatches`, `serverTimestamp` | PASS |

## 7. Authorized Transaction Item API Endpoint Results

**Result: PASS**

The Transaction Item endpoints were validated through real HTTP calls against the formal ERP-compatible Shared DEV fixture. Detail validation used dashboard-derived identifiers internally and did not print database payload identifiers.

| Endpoint | HTTP Status | API Code | Payload Keys | Result |
| --- | ---: | ---: | --- | --- |
| GET /api/v2/transitems/dashboard | 200 | 0 | `companies`, `count`, `serverTimestamp`, `start`, `summary`, `total`, `transactionItems` | PASS |
| GET /api/v2/transitems/companies/{company_no}/detail | 200 | 0 | `company`, `contracts`, `serverTimestamp`, `transactionItems` | PASS |
| GET /api/v2/transitems/transitems/{transaction_item_no}/detail | 200 | 0 | `contracts`, `linkedItems`, `serverTimestamp`, `transItem` | PASS |

## 8. Token / Session Test Treatment

**Treatment: CONTROLLED NON-PRODUCTION BYPASS FOR BUSINESS ENDPOINT VALIDATION**

Code inspection confirms the standard API token path calls `CAuth.reset_alive_time()`, which updates `session.expiredTime`. Because the schema-apply credential was downgraded and the participant credential is read-only, the standard session alive-time refresh path is not suitable for this read-only endpoint rerun.

For the real HTTP business endpoint validation:

- `x-auth-token` header was still supplied to satisfy the common API header check.
- `TOKEN_ENABLED=1` was set only in the child process to skip `session.expiredTime` refresh.
- No live session token was printed or persisted.
- A separate attempt to read/use live session token material was not performed after safety review blocked session-material probing.

Implication:

- Business query compatibility is validated.
- Full login/session mutation behavior is intentionally outside this bounded read-only rerun and requires a separately authorized non-production credential/path that permits session updates.

## 9. Read-Only / Unauthorized Write Negative Control

**Result: PASS_WRITE_DENIED**

A controlled write-negative check was executed through the wrapper. The participant credential rejected the write attempt as expected.

| Check | Result |
| --- | --- |
| Unauthorized write through participant credential | PASS_WRITE_DENIED |
| Error Type | OperationalError |

## 10. UX Real-Backend Validation Readiness

**Result: CAN PROCEED WITH READ-ONLY BUSINESS ENDPOINT VALIDATION**

UX real-backend validation can proceed for the current read-only Item Center and Transaction Item Master flows when the frontend/runtime uses the same bounded non-production backend configuration and the same token/session test treatment.

Important scope limit:

- This does not validate production readiness.
- This does not validate write APIs.
- This does not validate standard login/session refresh under SELECT-only credentials.
- This does not authorize schema mutation, migration, cutover, or Source-of-Truth transition.

## 11. Defects / Blockers

No blocker remains for read-only Item / Transaction Item real-backend UX validation against the formal ERP-compatible Shared DEV fixture.

Remaining controlled limitation:

1. Standard token/session alive-time refresh requires update permission on `session.expiredTime`; this rerun used the non-production bypass because the participant credential is read-only.
2. If future validation must include login/session lifecycle, CTO/Engineering should provide a separate non-production auth validation path or credential explicitly authorized for session mutation only.

## 12. Final Classification

**DB_AUTH_PASS_FORMAL_TABLE_SANITY_PASS_HTTP_START_PASS_ITEM_API_PASS_TRANSITEM_API_PASS_READONLY_CONTROL_PASS_UX_READONLY_VALIDATION_CAN_PROCEED_WITH_TOKEN_BYPASS_LIMITATION**

This classification means:

- The Shared DEV formal ERP-compatible fixture is visible.
- The read-only participant credential can run Item / Transaction Item business queries.
- The implemented backend APIs now align with the formal fixture for the tested read-only flows.
- UX real-backend validation may proceed for these read-only screens, with token/session refresh excluded from scope.
