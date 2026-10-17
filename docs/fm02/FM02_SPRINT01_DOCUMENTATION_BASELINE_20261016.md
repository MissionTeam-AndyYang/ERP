# FM-02 Item Master Sprint 1 — Full Module Documentation Baseline

Status: source-reconciled documentation baseline; full Option A scope classified; no Sprint 2 implementation authorization

Date: 2026-10-17
Repository: `FM02_C2_Implementation_20261013_001`
Branch: `codex/fm02-c2-isolated-20261013-001`

## Purpose, authority and scope

This baseline closes the Sprint 1 documentation record for the full FM-02 Item Master Option A scope. It consolidates the available business clarification, prior Sprint 1 delivery, C2 contract, migrations 0001–0006, backend/API and UI source, offline test plan, repository rules, and accepted governance boundaries.

The baseline is a documentation and source-reconciliation artifact. It does not authorize database access, SQL, migration execution, DML, Restore, Restart, Concurrency, production release, GitHub push, or Sprint 2 coding.

The existing C2 contract remains authoritative for the implemented C2 slice. Broader Option A statements below are classified explicitly so that a design reference is not mistaken for approval or implementation.

## Business decision closure B01–B06

The 2026-10-17 CIO/Product Owner decision record establishes the following boundaries. Confirmed boundaries are incorporated into the current documentation; deferred details remain controlled decisions and are not implemented by this closure.

| Decision | Confirmed boundary | Deferred detail and mandatory trigger |
| --- | --- | --- |
| B01 | Item Master / Product Definition owns Item identity, classification and lifecycle business meaning. Product Structure owns relationship context. | Name the incumbent, delegation, escalation and formal authorization before approval workflow or accountable-role coding is frozen. Responsible scope: FM-02 governance / Product Structure. |
| B02 | Item identity is separate from Product / SKU. No unapproved Product/SKU relationship or schema is created. | Decide cardinality, relationship model and authoritative Product Structure source of truth before Product/SKU schema, API or UI coding. Responsible scope: Product Structure / SR-1. |
| B03 | Preserve C2 item-specific UOM conversion, original transaction quantity/UOM, and no unapproved global fallback. | Decide global conversion, precision/rounding, tolerance, catch-weight, exceptions and delegation before conversion policy or dependent API/UI design freeze. Responsible scope: FM-04 / shared data policy. |
| B04 | New Item identity depends on controlled specification, business meaning, intended use and downstream impact; supplier, price or customer label alone is insufficient. | Only case-specific exceptions under existing authority remain open; record the authority before exception implementation. Responsible scope: Item Master Business Owner. |
| B05 | Preserve unique Item identity, controlled code assignment and legacy-code references. No silent recoding, deletion or retired-code reuse. | Decide the final 12-character proposal, charset, sequencing, collision handling, immutable ID/display-code distinction and formal non-reuse policy before code-policy freeze or migration mapping. Responsible scope: FM-02 / data governance. |
| B06 | New Item starts DRAFT; activation needs business approval evidence; technical execution is not business approval; lifecycle evidence is preserved. | Decide the state-transition matrix, approvers/delegates, emergency correction, blocking rules, supersession and audit minimums before lifecycle workflow coding. Responsible scope: FM-02 Product/Business Owner. |

Decision classifications: `BOUNDARY_CONFIRMED` for B01–B03, B05–B06; `DECIDED` for B04 under existing approved business rules; deferred parameters are `DECISION_REQUIRED / CONTROLLED_DEFERRED`; unapproved implementation remains `NOT_AUTHORIZED`.

## Full Option A capability classification

| Capability area | Classification | Evidence / boundary |
| --- | --- | --- |
| Item identity, business meaning and duplicate review | APPROVED_AND_SPECIFIED | Business Owner clarification; identity is not inferred from name, code, supplier, price or package alone. |
| Item code assignment and legacy-code preservation | APPROVED_AND_SPECIFIED | Business clarification and 0006 source-record mapping; final numbering policy remains a decision item. |
| Item category and lifecycle separation | APPROVED_AND_SPECIFIED | Category and lifecycle are separate concepts; current source includes bounded category/lifecycle foundations. |
| Create, read, search and bounded maintenance | IMPLEMENTED | Prior Sprint 1 foundation provides bounded create/detail/list source; creation is DRAFT-only. Full production UI/API wiring is not claimed. |
| UOM reference and item-UOM relationship | IMPLEMENTED | 0001–0005 source and C2 service; item-scoped reference contract is implemented in source. |
| UOM conversion | IMPLEMENTED / BOUNDED | Item-specific conversion and numeric storage are implemented in C2 source; global conversion, rounding/default policy and business approval remain open. |
| Specifications, effective periods and traceability | IMPLEMENTED / BOUNDED | 0003 and service validation provide source-level structures; final enterprise policy is not approved here. |
| Supplier qualification and package references | IMPLEMENTED / BOUNDED | 0004–0005 and C2 service; supplier master ownership is outside FM-02. |
| Customer qualification and packaging relationships | IMPLEMENTED / BOUNDED | 0005 and C2 service; customer/product variant policy remains a Product decision. |
| Approval and lifecycle history | IMPLEMENTED / BOUNDED | 0003 and foundation service; final role/workflow authority is not fully named. |
| Legacy identifier reconciliation | IMPLEMENTED / BOUNDED | 0006 zero-row gate and source-record identity; no guessed backfill or live migration is authorized. |
| Audit, idempotency and optimistic version controls | IMPLEMENTED / BOUNDED | C2 service and integrity foundation source; live database acceptance is separately gated. |
| Cross-module references to Product/SKU, BOM, Inventory, Purchasing, Planning, Production, Warehouse, Sales and Costing | APPROVED_AND_SPECIFIED AS DEPENDENCIES | Business clarification identifies relationships and downstream consumers; no other module is activated or redesigned by this record. |
| Full Product/SKU source-of-truth and relationship model | DECISION_REQUIRED | The Product/SKU decision-readiness package leaves owner, semantics and source-of-truth unresolved. |
| Final business owner, role matrix and lifecycle approval workflow | DECISION_REQUIRED | Current records identify candidate roles but do not establish a current formal appointment. |
| Global UOM conversion, rounding, precision and default policy | DECISION_REQUIRED | C2 supports item-specific conversion; enterprise-wide policy is not approved. |
| Full live API/UI integration and runtime validation | PROPOSED_NOT_APPROVED | Source and mock UI exist; dependency-complete execution and live integration require a later authorization. |
| BOM, Inventory, Production, migration execution and Production release | EXCLUDED | Explicitly outside this Sprint 1 documentation scope. |

## D01 — Business requirements and functional specification

The business clarification establishes Item identity as a business decision based on meaning, specification, lifecycle, intended use, customer/regulatory requirements and downstream use. Name, code, supplier, price, package or ownership alone is not sufficient evidence for merge, split, recode or deletion. Required concepts include category, ownership/control, lifecycle, legacy references, duplicate review, effective use and downstream state restrictions.

The source-reconciled bounded functions are Item create/read/list, DRAFT-only creation, controlled category and UOM, item-scoped references, specifications, qualifications, package/customer relationships, item-specific conversion, approval/lifecycle history, idempotent service behavior and legacy mapping admission. The full Option A document distinguishes these implemented or bounded capabilities from unresolved enterprise policies.

Decision-required questions are now limited to the controlled B01–B06 deferred details and the package/customer-variant rule already identified in the source review. B04 is decided under the existing approved business rule; no new exception policy is created here.

## D02 — Domain model and architecture specification

`item` is the Item Master identity root. Its bounded aggregate includes category, base UOM, specification lineage, approval/lifecycle history, item UOM, supplier qualification, package, customer qualification, conversion rule and legacy identifier mapping. Product Structure, BOM and downstream modules are relationship/dependency contexts, not silently merged into the Item aggregate.

The service owns validation, idempotency, locking and transaction boundaries; adapters own transport conversion; migrations own revision guards and zero-row gates; the UI does not recalculate backend truth. Source-of-truth and relationship cardinality for Product/SKU remain DECISION_REQUIRED.

## D03 — Database schema, ERD, DDL and data dictionary

The source set is:

- `04_Engineering/Database/fm02_item_master_0001.sql` and `0002_business_names.sql`;
- `04_Engineering/Database/fm02_item_master_0003_integrity_foundation.sql`;
- `04_Engineering/Database/fm02_item_master_0004_c2_reference_contract.sql`;
- `04_Engineering/Database/fm02_item_master_0005_c2_package_customer_conversion.sql`;
- `04_Engineering/Database/fm02_item_master_0006_legacy_mapping_reconciliation.sql`;
- the corresponding guarded down scripts.

The documented physical C2 extension covers item category, specification, approval, lifecycle event, supplier qualification, item UOM, package, customer qualification, conversion and legacy mapping. Prior target evidence records 19 tables, 25 foreign keys and 20 unique constraints after 0006; this is cited evidence, not a new live readback. No DDL or migration execution occurred in this documentation task.

## D04 — Migration specification and data mapping

The documented progression is 0001 normalized foundation, 0002 business naming, 0003 integrity foundation, 0004 reference contract, 0005 package/customer/conversion, and 0006 legacy mapping reconciliation. Each protected migration uses a predecessor revision guard; 0006 requires a zero-row gate and explicit source-record identity. No guessed mapping, automatic recoding, backfill or deletion is authorized.

Global conversion policy, final Product/SKU linkage and historical source qualification remain separate decisions. Down scripts are data-preserving guarded reversals and do not authorize live rollback.

## D05 — Backend/API contract

Implemented source includes the bounded foundation Item create/detail/list service and the C2 routes:

| Method | Route | Classification |
| --- | --- | --- |
| POST | `/api/v1/fm02/items/<item_id>/customer-qualifications` | IMPLEMENTED in source; runtime validation not claimed |
| POST | `/api/v1/fm02/items/<item_id>/uom-conversions` | IMPLEMENTED in source; runtime validation not claimed |
| GET | `/api/v1/fm02/items/<item_id>/uom-conversions/<from_item_uom_id>/<to_item_uom_id>` | IMPLEMENTED in source; runtime validation not claimed |

The API contract uses injected connection boundaries, structured errors and explicit transaction handling. Full live API integration, broader Item Master search/maintenance semantics and Product/SKU endpoints are PROPOSED_NOT_APPROVED or DECISION_REQUIRED, not implied by these routes.

## D06 — UI/UX screen and interaction specification

The `/items` page and `C2ReferencePanel` provide a mock-ready item-scoped reference experience with Item UOM, conversion and customer-qualification states, client validation, empty/unavailable/error states and existing operational-density patterns. The current C2 panel does not call the live C2 API. Dedicated approval, package, legacy mapping, full search/maintenance and live persistence screens require Product/Frontend acceptance and later implementation authorization.

## D07 — CSS and design-system specification

The UI follows the shared ERP2.0 design system, existing Tailwind tokens and shared components. C2 uses existing status badges, cards, focus states, spacing and responsive patterns; no parallel theme is introduced. Browser/build validation remains NOT VERIFIED where the approved frontend dependency environment is unavailable. Accessibility and responsive behavior are specified, not represented as a completed runtime result.

## D08 — Authorization and permission matrix

| Capability | Engineering | Product/Business | Independent TEST | CTO/CIO boundary |
| --- | --- | --- | --- | --- |
| Read source and prepare documentation | May inspect/propose under accepted route | Reviews business meaning | Reviews evidence | CTO reviews architecture; CIO authorizes protected scope |
| Change source | Only under accepted Engineering route | Approves business intent where required | Does not implement | CTO accepts integration; CIO scope remains binding |
| Execute deterministic tests | May execute isolated tests | Not required | Independently reviews/accepts | Live authority is not implied |
| Execute live SQL, DML, migration, restore, restart or concurrency | Not authorized here | Separate decision | Separate TEST authority | CIO-specific release required |
| Approve Product/SKU, lifecycle or enterprise UOM policy | Not an Engineering inference | Named business owner required | Does not approve business policy | CIO/Owner decision where governance requires |

Formal Assignment IDs and current formal Product appointments are not exposed in this workspace; technical task provenance is retained without inventing organizational authority.

## D09 — Test strategy, plan and acceptance criteria

The canonical plan is `docs/fm02/FM02_C2_OFFLINE_TEST_PLAN_20261016.md`. It distinguishes `SCRIPT_READY`, `SYNTHETIC_PASS`, `LIVE_PASS`, `HOLD` and `NOT_RUN`. Coverage spans unit/deterministic rules, migration contract tests, API contracts, frontend components, static/build checks, negative cases, UAT handoff and live procedures. Reported C2 deterministic results remain source/offline evidence; dependency-complete API/UI execution, current live database results and protected T2 execution remain separately classified.

## D10 — Cross-module coding convention

The shared convention at `docs/engineering/CROSS_MODULE_CODING_CONVENTION_20261016.md` applies to FM-01, FM-02 and future modules. It governs repository layout, backend/frontend/database/test practices, secrets, authorization, evidence, quality gates and Git. Its status remains PROPOSED pending Repository Office custody/approval; it is not an FM-02-only rule and not an active organization-wide standard by implication.

## D11 — Technical architecture, environment and operations

The documented local architecture uses the frontend `src/`, Flask adapters under `backend/`, bounded domain services under `04_Engineering/Application/ERP-2.0/restserver/`, and migration sources under `04_Engineering/Database/`. Dependency requirements, offline validation commands, environment limitations and target boundaries are recorded in `README.md`, `CONTRIBUTING.md`, the conventions and the offline test plan.

No Windows Service, ACL/firewall change, credential rotation, live MariaDB operation, arbitrary host execution, production activation or remote Git delivery is implied.

## D12 — Git, version control and delivery

The canonical delivery repository is the nested FM02 repository on branch `codex/fm02-c2-isolated-20261013-001`. Local Git custody is available; the pre-existing untracked `evidence/` directory remains preserved and unstaged. No remote is configured, so `GITHUB_PUSH=BLOCKED_REMOTE_NOT_VERIFIED`; no owner, destination or remote readback is claimed.

## Full-module open decisions and downstream impact

| Question | Recommended bounded option | Impacted documents | Downstream coding impact |
| --- | --- | --- | --- |
| Who owns Item Master, Product Structure and lifecycle decisions? | Name one accountable owner and a reviewed delegation matrix before new workflow code | D01, D08, D11 | Role checks, approval endpoints, audit actors |
| Is Product/SKU a separate identity or a relationship over Item? | Preserve separate Item identity and decide Product/SKU relationship/cardinality in SR-1 | D01, D02, D03, D05, D06 | Foreign keys, API resources, UI navigation |
| Is conversion global or item-specific? | Retain item-specific C2 behavior until enterprise policy approves global rules | D01, D03, D04, D05, D09 | Conversion lookup, precision, rounding and fixtures |
| When does package/customer variation create a new item? | Require specification/operational meaning evidence; do not infer from name or price | D01, D02, D05, D06 | Identity validation and qualification model |
| What is the final code/retired-code policy? | Preserve legacy aliases and prohibit reuse until owner policy is approved | D01, D03, D04, D09 | Generators, uniqueness, migration mapping |
| Which roles may approve activation/effectivity? | Approver matrix with business and technical actor separation | D01, D08, D09 | State transitions, authorization, audit |

## Review and status

- CTO technical review: completed against the listed source and evidence.
- Engineering technical evidence: prior Hilbert/Lagrange task provenance retained; no formal Assignment ID inferred.
- Independent TEST technical evidence: prior Kierkegaard provenance retained; no current live verdict inferred.
- Product/domain authority: current formal appointment not exposed; open decisions remain visible.
- Repository Knowledge: prior registration/readback is PASS for the earlier document versions; post-correction update is required.

`FM02_SPRINT01_DOCUMENTS=PASS`
`CROSS_MODULE_CODING_CONVENTION=PROPOSED`
`REPOSITORY_KNOWLEDGE_STATUS=PASS`
`SPRINT02_ENTRY=READY_FOR_SEPARATE_AUTHORIZATION`
