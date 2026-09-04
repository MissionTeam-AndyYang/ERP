# Backend API Response - ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-002

## 1. Response Identity

| Field | Value |
| --- | --- |
| Authorization ID | ERP2-CIO-ROUTING-PROCESS-FLOW-SHARED-DEV-DATA-SURFACE-001 |
| Work items | ERP2-ROUTING-PROCESS-FLOW-SHARED-DEV-DATA-SURFACE-001; ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-002 |
| Response date | 2026-09-04 |
| Repository baseline | main |
| Classification | SAFE STOP - SCHEMA-APPLY PATH NOT ACTIVE; SHARED DEV ROUTING DATA SURFACE STILL MISSING |

## 2. Assignment Boundary

CTO/CIO authorized bounded non-production Shared DEV Routing / Process Flow acceptance test-support DDL, fixture data, mapping, adapter, API query, warning, lineage, and test corrections.

Backend/API did not receive authority to perform Production access, write routes, Product write, Routing write, Process Master write, migration, Source-of-Truth transition, Engineering Pull, Cutover, or Go-Live.

## 3. Prepared Test-Support Surface

Backend/API prepared the smallest responsible non-production Routing / Process Flow test-support SQL:

`docs/database/ERP2_ROUTING_PROCESS_FLOW_SHARED_DEV_TEST_SUPPORT_20260904.sql`

Prepared support-surface content:

| Table | Purpose |
| --- | --- |
| `product_process` | Routing Version identity for existing Shared DEV Product and WIP fixtures |
| `process_flow` | ordered Routing Step evidence and stable step identity |
| `process` | reusable Process Master identity and process label evidence |
| `process_capacity` | governed standard performance evidence |

Fixture design:

| Coverage | Evidence |
| --- | --- |
| Product | `PRD-SD-001` via existing Shared DEV Product fixture |
| WIP | `INP-SD-001` via existing Shared DEV Inproduct fixture |
| Effective Product Routing | `RT-SD-PRD-001-V1`, effective at `1700000000` |
| Future Product Routing | `RT-SD-PRD-001-V2`, future at `1900000000` |
| WIP Routing | `RT-SD-INP-001-V1`, effective at `1700000000` |
| Ordered steps | `STEP-SD-PRD-001-001`, `STEP-SD-PRD-001-002`, `STEP-SD-PRD-001-V2-001`, `STEP-SD-INP-001-001` |
| Process / stage evidence | Preparation and processing process master rows |
| Recipe reference | Existing `product_spec` row for `PRD-SD-001` |
| Packaging context | Existing `product_bom_spec` row for `PRD-SD-001` |
| Standard performance | `process_capacity` rows for preparation mix and processing coat |
| Warning coverage | WIP row intentionally retains resource eligibility and missing recipe/packaging conditions under current read-only contract |

This SQL is explicitly marked as Shared DEV acceptance test-support only. It is not a Production schema migration, not target schema authority, and not a Source-of-Truth transition.

## 4. Apply Attempt

Backend/API attempted to use the governed schema-apply DPAPI secret path for the bounded DDL/fixture apply.

Result:

| Check | Result |
| --- | --- |
| Schema-apply DPAPI secret file | Present |
| Schema-apply DPAPI decrypt | FAIL |
| DDL/fixture applied | NO |
| Raw secret exposure | 0 |

PowerShell DPAPI reported a cryptographic operation failure when attempting to decrypt the schema-apply secret. Existing Engineering B closure evidence also records that the schema-apply user was downgraded to `SELECT` only after the earlier formal fixture apply.

Because no active governed schema-apply path was available to Backend/API, the prepared test-support SQL was not applied.

## 5. Shared DEV Read-Only Probe

Backend/API used the governed read-only wrapper successfully against:

| Item | Value |
| --- | --- |
| Runtime | MariaDB Shared DEV |
| Endpoint | `172.20.10.3:3307` |
| Database | `erp2_shared_dev_item_transitem_np` |
| Credential class | `ERP2_SHARED_DEV_ITEM_TRANSITEM_NP_READONLY` |
| Raw secret exposure | 0 |

Current Routing source table status:

| Table | Status |
| --- | --- |
| `product` | PRESENT |
| `inproduct` | PRESENT |
| `product_spec` | PRESENT |
| `product_bom_spec` | PRESENT |
| `product_process` | MISSING |
| `process_flow` | MISSING |
| `process` | MISSING |
| `process_capacity` | MISSING |

Current adjacent fixture counts:

| Table | Count |
| --- | --- |
| `product` | 1 |
| `inproduct` | 1 |
| `product_spec` | 1 |
| `product_bom_spec` | 1 |

## 6. Real DB-Backed Route Probe

Backend/API launched a route probe through the existing Flask app with environment variables mapped from the read-only wrapper to the backend `DB_*` configuration.

Route:

`GET /api/v2/routing/dashboard?effectiveDate=1700000000`

Result:

| Item | Result |
| --- | --- |
| HTTP status | 400 |
| Backend error | `Table 'erp2_shared_dev_item_transitem_np.product_process' doesn't exist` |
| Silent mock fallback | NOT OBSERVED |

The failure proves the backend route is attempting to use the real Shared DEV database and is not silently falling back to frontend mock data. The route cannot complete because the accepted Routing source table is missing.

Because the first required route is blocked at the source table, Backend/API did not continue executing the remaining three route probes:

- `GET /api/v2/routing/products/{item_no}/versions`
- `GET /api/v2/routing/versions/{routing_version_id}/steps`
- `GET /api/v2/routing/products/{item_no}/current`

Continuing would repeat the same missing-source-table failure and would not add meaningful acceptance evidence.

## 7. Local Backend Verification

Existing local backend verification remains valid:

| Verification | Result |
| --- | --- |
| Routing API pytest | PASS, 6 tests |
| Full backend pytest suite | PASS, 92 tests |
| Read-only negative control | PASS, POST route rejected with 405 |

These tests validate Product / WIP resolution, Routing Version state selection, ordered step identity, process reference mapping, recipe reference, packaging context, standard performance, warning codes, source lineage, current Routing selection, missing step warning behavior, and read-only route boundary.

## 8. Disposition

Backend/API cannot complete ERP2-ROUTING-PROCESS-FLOW-PRODUCT-EVIDENCE-RETEST-002 against Shared DEV until the bounded test-support data surface is actually applied or Engineering B provides an active governed schema-apply path.

Current blocker:

`SCHEMA_APPLY_PATH_NOT_ACTIVE_FOR_AUTHORIZED_ROUTING_TEST_SUPPORT_DDL`

Secondary blocker if schema-apply is restored:

`ROUTING_PROCESS_FLOW_DATA_SURFACE_NOT_AVAILABLE_IN_CURRENT_SHARED_DEV_FIXTURE`

Recommendation:

1. Engineering B should reopen or provide an active governed non-production schema-apply path for the current CIO-authorized bounded Routing test-support DDL.
2. Apply `docs/database/ERP2_ROUTING_PROCESS_FLOW_SHARED_DEV_TEST_SUPPORT_20260904.sql`.
3. Preserve read-only participant access after apply.
4. Backend/API should rerun the four real DB-backed GET route probes and preserve POST/PUT/DELETE negative controls.

## 9. Boundary Confirmation

Backend/API prepared but did not apply test-support SQL after the governed schema-apply secret failed to decrypt. Backend/API did not create or modify Shared DEV tables, did not use Production credentials, did not use Production data, did not perform Product write, Routing write, Process Master write, migration, Engineering Pull, Source-of-Truth transition, Cutover, or Go-Live activity.
