# Backend API Response - ERP2-CIO-CP1-READ-ONLY-INTEGRATED-PRODUCT-OVERVIEW-RDY-001

## 1. Response Identity

| Field | Value |
| --- | --- |
| Authorization ID | ERP2-CIO-CP1-READ-ONLY-INTEGRATED-PRODUCT-OVERVIEW-RDY-001 |
| Request source | CTO Office |
| Response date | 2026-09-04 |
| Repository baseline | main |
| Classification | READINESS ASSESSMENT ONLY - NO IMPLEMENTATION AUTHORITY |

## 2. Assignment Boundary

This response assesses backend/API composition readiness for a `PRODUCT / WIP 360 READ-ONLY OVERVIEW`.

Backend/API did not implement a new endpoint, mutate code, apply database/schema changes, introduce Product write capability, perform Production deployment, load Production data, run migration, transition Source-of-Truth, perform Cutover, or authorize ERP2.0 Go-Live.

Boundary statements preserved:

- `API_COMPOSITION_READINESS != API_IMPLEMENTATION_AUTHORITY`
- `READ_ONLY_COMPOSITION != NEW_SOURCE_OF_TRUTH`

## 3. Candidate Composition Approach

Recommended smallest responsible approach:

| Option | Readiness disposition | Rationale |
| --- | --- | --- |
| Frontend composition using existing read-only APIs | Feasible for early UX validation only | Requires no new backend endpoint, but would duplicate Product/WIP identity joining, warning merging, version-date handling, and source-lineage interpretation in the frontend. |
| Backend-for-Frontend read-only composition endpoint | Recommended execution candidate after separate authorization | Gives the Product/WIP 360 screen one stable payload while preserving source lineage from Item, Warehouse, BOM, Recipe, and Routing. Improves latency and consistency for management-facing overview. |
| Service-level composition without public BFF endpoint | Useful internal implementation model | Existing API services can be composed behind a bounded read-only BFF route after authorization; shared logic should avoid duplicated identity and inventory summary calculations. |

Recommended next step is not immediate implementation. The next authorized step should be an API design package for a bounded read-only BFF endpoint, for example:

`GET /api/v2/product-overview/items/{item_no}/overview`

with query parameters such as `itemCategory`, `effectiveDate`, `inventoryDate`, and optional `productVersion`. The exact contract should be proposed and reviewed before implementation.

## 4. Available Accepted API Families / Contracts

The current formal API documents and implemented API families provide usable read-only building blocks:

| Domain | Available contract | CP1 use |
| --- | --- | --- |
| Item Center | `GET /api/v2/items/dashboard`; `GET /api/v2/items/{item_no}/detail` | Product/WIP master header, item category, item subcategory, units, inventory summary, recent batches, BOM usage, and maintenance signals. |
| Transaction Item | `GET /api/v2/transitems/dashboard`; `GET /api/v2/transitems/companies/{company_no}/detail`; `GET /api/v2/transitems/transitems/{transaction_item_no}/detail` | Customer/supplier-facing transaction item relationship, linked internal `itemNo`, contract/pricing readiness, company/payment context. |
| Warehouse / Inventory | `GET /api/v2/warehouse/dashboard`; `GET /api/v2/warehouse/inventory`; `GET /api/v2/warehouse/inventory/lots`; `GET /api/v2/warehouse/inventory/lots/wh/{warehouse_no}/item/{item_no}/batch/{batch_no}`; Warehouse analytics/task read-only APIs | Current inventory quantity/value, available/reserved/quality-hold quantity, batch lots, warehouse distribution, risk types, task status, and inventory value trend. |
| BOM / Product Structure | `GET /api/v2/bom/dashboard`; `GET /api/v2/bom/{bom_no}/detail`; `GET /api/v2/bom/product-structure/{product_no}` | Product structure tree, BOM evidence, linked product relationships, structure status, missing/circular/depth warnings. |
| Recipe / Formula | `GET /api/v2/recipe-formula/dashboard`; `GET /api/v2/recipe-formula/{recipe_no}/versions`; `GET /api/v2/recipe-formula/{recipe_no}/versions/{version}/composition`; `GET /api/v2/recipe-formula/by-product/{product_no}` | Formula input/output evidence, recipe version status, product-structure references, formula completeness warnings. |
| Routing / Process Flow | `GET /api/v2/routing/dashboard`; `GET /api/v2/routing/products/{item_no}/versions`; `GET /api/v2/routing/versions/{routing_version_id}/steps`; `GET /api/v2/routing/products/{item_no}/current` | Product/WIP routing versions, ordered process steps, process/stage grouping, recipe reference, packaging context, standard performance and routing warnings. |

Trace and Batch APIs are not part of the CTO-listed minimum accepted capabilities, but may be used later as supporting drill-down once CP1 scope explicitly includes batch traceability.

## 5. Common Product / WIP Identity Feasibility

Common identity is feasible, but should be made explicit in the CP1 contract.

| Identity element | Current evidence | Readiness finding |
| --- | --- | --- |
| Internal item key | Database uses `product.no` for finished goods and `inproduct.no` for WIP; `EItemCategory.PRODUCT = 5`, `EItemCategory.INPRODUCT = 4`. | Use `itemNo + itemCategory` as the canonical Product/WIP overview key. |
| Product version | `product.version`, `product_spec.product_version`, `product_bom_spec.product_version`, and recipe/routing version references exist. | CP1 must separate item identity from version/effective-date selection. Do not infer a single version without reporting the selection rule. |
| Transaction item mapping | `trans_items.item_no` links transaction-facing item records to internal material/inproduct/product item numbers. | Feasible for linked transaction items. Missing `item_no` must be surfaced as data-quality warning, not silently omitted. |
| Inventory identity | Warehouse APIs use `itemNo`, `itemCategory`, `batchNo`, `warehouseNo`, and `refCategory/refNo`. | Feasible for Product/WIP stock overview if filtered to `itemCategory in (4,5)` or a specific `itemNo`. |
| BOM identity | Product Structure is product-oriented through `product_no`; WIP composition is available through `inproduct_bom_spec` inside structure expansion. | Product root is mature. Standalone WIP root Product Structure may require explicit contract confirmation. |
| Recipe identity | Recipe/Formula currently treats `bom.no` as read-only recipe evidence and links output by `product_spec`. | Feasible for Product-facing formula evidence; WIP formula root semantics need explicit confirmation if CP1 requires WIP as root output. |
| Routing identity | Routing uses `product_process.item_no` for product/inproduct routes. Shared DEV fallback currently has Product route evidence and WIP only as intermediate step reference. | Formal contract supports Product/WIP; Shared DEV evidence still needs standalone WIP route data if WIP acceptance evidence is required. |

## 6. Source-Lineage / Warning Preservation Requirements

CP1 must preserve source and warning evidence from each subdomain instead of flattening them into one generic status.

Minimum preservation requirements:

1. Keep per-domain `statusCode` / `riskCode` / `warningCode` values as enum codes; frontend performs display text and multilingual conversion.
2. Keep BOM `warnings[]` such as missing item master, missing product spec, circular reference, and depth limit.
3. Keep Recipe `sourceLineage` and `warnings[]`, including recipe/input/output evidence sources and missing/multiple output warnings.
4. Keep Routing `sourceLineage`, `capabilityBoundary`, and `warnings[]`, especially `test_support_only`, missing process master, missing standard performance, missing recipe reference, and resource eligibility warnings.
5. Keep Warehouse risk, reservation, quality-hold, and inventory calculation boundaries. Current Warehouse contracts state that zero-quantity lots are filtered and inventory uses month-statistic + delta with inventory-record fallback.
6. The composition payload should include a module-level readiness section, for example `moduleReadiness[]`, so partial data does not appear as complete Product/WIP authority.

## 7. API / Data-Contract Gaps

| Gap | Impact | Recommended handling |
| --- | --- | --- |
| No integrated Product/WIP 360 read-only endpoint currently exists. | Frontend would need multiple calls and merge logic. | Create a separate API proposal and flow-algorithm document before implementation. |
| No single documented CP1 identity envelope exists across Item, Transaction Item, Warehouse, BOM, Recipe, and Routing. | Risk of confusing `productNo`, `itemNo`, `transItemNo`, `recipeNo`, and `routingVersionId`. | Define CP1 header as `itemNo`, `itemCategory`, optional `itemVersion`, `effectiveDate`, and source references. |
| Date semantics differ by module. | Inventory uses `date`; Recipe/Routing/BOM use `effectiveDate` or version selection. | CP1 should expose both `inventoryDate` and `effectiveDate` or explicitly map a single `asOfDate` into module-specific parameters. |
| WIP as root is not equally mature in all contracts. | Product 360 can be composed more confidently than standalone WIP 360. | Require WIP-specific acceptance fixtures and examples before declaring WIP parity. |
| Transaction item linkage may be missing. | Commercial item context can be absent even when internal product exists. | Return `linkedTransactionItemStatusCode` or data-quality warning rather than guessing. |
| Shared DEV Routing fallback is test-support-only. | It supports acceptance evidence but must not be treated as Production-ready source. | Preserve `sourceCode = test_support` and `warningCode = test_support_only`. |

## 8. Material Schema-Gap Observations

No immediate schema mutation is recommended for this readiness stage.

Potential schema observations for later review:

1. If CP1 requires a governed one-to-many mapping between commercial transaction items and internal Product/WIP versions, the current `trans_items.item_no` relationship may be insufficient when version, customer-specific spec, or packaging variant matters.
2. If CP1 requires WIP as a first-class root across Product Structure, Recipe/Formula, and Routing, the current formal documentation should add WIP-root examples and acceptance fixtures before implementation.
3. Routing Shared DEV support currently proves Product route evidence only; WIP route evidence should be added by Engineering B if required for CP1 acceptance.

## 9. No-Write / Mutation-Control Confirmation

The CP1 composition approach must remain read-only:

| Control | Required behavior |
| --- | --- |
| HTTP methods | GET only for the CP1 overview candidate. |
| Database access | Read-only queries only; no DDL, no DML, no fixture write by Backend/API. |
| Product authority | No Product write, version promotion, release, approval, freeze, or source-of-truth update. |
| Workflow behavior | No task creation, state transition, or owner reassignment. |
| Frontend behavior | Frontend may display and filter; it must not infer missing master data as approved/complete. |

## 10. Implementation Risk

| Risk | Level | Comment |
| --- | --- | --- |
| Identity mismatch across Product/WIP/Transaction Item | Medium | Manageable if CP1 contract requires `itemNo + itemCategory` and keeps transaction item as related context. |
| Partial source evidence being mistaken as complete authority | Medium | Must preserve module-level warnings and sourceLineage. |
| Latency from frontend-only composition | Medium | Multiple endpoint calls may be acceptable for prototype but should be measured before management use. |
| WIP parity | Medium | Existing formal direction supports WIP, but test data and examples are less complete than Product. |
| Schema change need | Low for readiness, medium for later governed CP1 | No schema change needed to assess or prototype; later may need governed mapping if CP1 expands scope. |

## 11. Recommended Next Authorization

If CTO/CIO wants CP1 execution to proceed, request a separate authorization for:

`ERP2-CIO-CP1-READ-ONLY-INTEGRATED-PRODUCT-OVERVIEW-API-DESIGN-001`

Scope:

1. Produce API proposal, backend flow/algorithm document, and frontend static preview under `docs/spec/api-proposal/`.
2. Define Product/WIP 360 identity envelope and module readiness/warning contract.
3. Specify BFF read-only endpoint candidate and response payload without implementation.
4. Include Product and WIP example scenarios, including missing transaction item, missing BOM, missing recipe output, missing routing, test-support routing, and inventory-no-stock cases.
5. Ask Engineering B to provide or confirm Shared DEV Product and standalone WIP test rows across Item, Warehouse, BOM, Recipe, and Routing before implementation authorization.

Implementation should occur only after proposal review and explicit implementation authorization.

## 12. Disposition

Backend/API readiness result:

`READY FOR CP1 API DESIGN PROPOSAL - NOT AUTHORIZED FOR IMPLEMENTATION`

The accepted read-only API families are sufficient to begin CP1 Product/WIP 360 API design. A bounded read-only BFF composition endpoint is the recommended execution candidate, but it must be separately proposed, reviewed, and authorized before code changes.
