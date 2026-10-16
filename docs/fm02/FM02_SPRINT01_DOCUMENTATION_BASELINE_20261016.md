# FM-02 Item Master Sprint 1 Documentation Baseline

Status: source-reconciled documentation baseline; non-production; no Sprint 2 implementation authorization

Date: 2026-10-16
Repository: `FM02_C2_Implementation_20261013_001`
Branch: `codex/fm02-c2-isolated-20261013-001`

## Purpose and authority

This baseline completes the Sprint 1 documentation record for the bounded FM-02 Item Master C2 slice. It consolidates the existing approved contract, physical migrations, implemented source, UI prototype, test plan, repository rules and operating boundaries. It does not authorize live SQL, migration execution, protected T2 execution, production release or Sprint 2 coding.

The authoritative implementation boundary is `docs/fm02/FM02_C2_MODULE_CONTRACT_20261016.md` together with the four C2 forward migrations and their down scripts. Where a broader repository document describes an older or wider ERP surface, this baseline labels it as reference material rather than silently promoting it to C2 authority.

## D01 — Business requirements and functional specification

### Approved bounded functions

1. Create and read Item Master records within the integrity foundation; creation is draft-only.
2. Maintain item-scoped UOM rows and supplier qualification references.
3. Maintain item-scoped package/customer qualification/conversion structures under effective-period and approval rules.
4. Resolve one active item-specific conversion rule only; there is no global fallback.
5. Reconcile legacy identifiers only through the 0006 zero-row gate and explicit source-record identity; no guessed backfill is allowed.
6. Protect lifecycle transitions with business approval evidence, idempotency and optimistic version checks.

Required validation includes bounded category/UOM/identity fields, non-overlapping effective periods, distinct conversion endpoints, positive fixed factors, required approval evidence for active conversion rules, customer scope sentinels and business-versus-technical actor separation. Expected failures are structured validation, not partial commits.

Explicit exclusions: Product/SKU, BOM, inventory, production transactions, global UOM conversion, customer/supplier master ownership, live credential management, UI-to-live-DB integration, migration execution and production release.

Acceptance is satisfied by the source-reconciled C2 contract, 11 deterministic service cases, six migration contract cases, and separately gated target-bound evidence. No offline result is a live result.

## D02 — Domain model and architecture

The domain root is `item`. The bounded aggregate includes category, base UOM, specification lineage, approval/lifecycle history, item UOM, supplier qualification, package, customer qualification, conversion rule and legacy identifier mapping. Foreign keys and composite keys preserve item ownership and reference scope.

The service owns validation, locking, idempotent replay and transaction commit/rollback. API endpoints adapt transport input and return structured results. The frontend remains a presentation/prototype boundary and must not recalculate backend workflow truth. The migration layer owns revision guards and zero-row gates. Credential, Owner-host and live-test controls remain outside the application implementation.

## D03 — Database schema, ERD, DDL and data dictionary

The physical source is:

- `04_Engineering/Database/fm02_item_master_0003_integrity_foundation.sql`
- `04_Engineering/Database/fm02_item_master_0004_c2_reference_contract.sql`
- `04_Engineering/Database/fm02_item_master_0005_c2_package_customer_conversion.sql`
- `04_Engineering/Database/fm02_item_master_0006_legacy_mapping_reconciliation.sql`

The corresponding `_down.sql` files are data-preserving guarded reversals. The C2 physical contract covers `item_category`, `item_specification`, `item_approval`, `item_lifecycle_event`, `item_supplier_qualification`, `item_uom`, `supplier_item_package`, `item_customer_qualification`, `uom_conversion`, and the revised `item_legacy_identifier` semantics, plus the existing Item/UOM/revision tables that they reference.

Accepted Route B evidence records a target inventory of 19 tables, 25 foreign-key constraints and 20 unique constraints after 0006. That is preserved as attributable target evidence in `evidence/routeb-20261013-001/`; it is not recreated or generalized here. Current target readback evidence separately records MariaDB 11.4.10, database `erp2_fm02_c2_test_001`, and revision `fm02_item_master_0006_legacy_mapping_reconciliation`. No new live readback is performed by this documentation task.

## D04 — Migration specification and data mapping

The forward sequence is 0003 integrity foundation → 0004 C2 reference contract → 0005 package/customer/conversion → 0006 legacy mapping reconciliation. Each migration verifies the exact prior revision before DDL and writes the next revision only after its own statements. 0006 requires zero rows in `item_legacy_identifier`; non-zero protected data requires a separately approved conversion plan and target-only recovery controls.

Mapping is explicit and source-record based: dataset, snapshot hash, source record, row locator, duplicate ordinal, mapping status and resolution reason are retained. No migration guesses a target Item. Down scripts reject revision drift and do not silently delete business data.

## D05 — Backend/API contract

The bounded C2 service source is `04_Engineering/Application/ERP-2.0/restserver/package/fm02_c2/service.py`. The integrated Flask adapter is `backend/app/services/fm02_c2.py`, with routes registered by `backend/app/api/v1/router.py` and exposed through `backend/app/api/v1/endpoints/fm02_c2.py`.

Implemented routes:

| Method | Route | Responsibility | Status |
| --- | --- | --- | --- |
| POST | `/api/v1/fm02/items/<item_id>/customer-qualifications` | Create item-scoped customer qualification | Implemented; dependency-backed suite pending |
| POST | `/api/v1/fm02/items/<item_id>/uom-conversions` | Create item-specific conversion rule | Implemented; dependency-backed suite pending |
| GET | `/api/v1/fm02/items/<item_id>/uom-conversions/<from_item_uom_id>/<to_item_uom_id>` | Resolve an active item-specific conversion | Implemented; dependency-backed suite pending |

The service uses an injected connection boundary, structured errors and explicit transaction handling. The broader legacy item-center API is a separate prototype surface and is not evidence that these C2 routes are live-wired or database-accepted. No credential is loaded implicitly by the C2 service.

## D06 — UI/UX screen and interaction specification

The current `/items` page and `C2ReferencePanel` provide a bounded item-scoped reference panel. It displays Item UOM, conversion and customer-qualification mock data; offers client-side validation for distinct UOM endpoints, positive fixed factors, effective dates, source references and customer scope; and shows empty, unavailable and error states. The existing design system supplies spacing, status badges, cards, responsive layout and operational-density rules.

The panel explicitly labels package and legacy mapping as unavailable and does not call the live C2 API. It is therefore a mock-ready UI contract, not an accepted live screen. Dedicated package, legacy-mapping, approval workflow and live persistence screens remain future scope pending Product/Frontend acceptance.

## D07 — CSS and design-system mapping

The UI follows `docs/design-system/ERP_2_0_Design_System_Specification.md`, existing shared components, Tailwind tokens and `src/app/globals.css`. C2 uses existing `StatusBadge`, card, border, spacing, focus and responsive patterns; it does not introduce a parallel theme. Accessibility-relevant states are represented with labels and status text, while final browser/build verification remains unavailable until the approved frontend dependency environment is restored.

## D08 — Authorization and permission matrix

| Capability | Technical executor | Business/product owner | Independent TEST | CIO/CTO boundary |
| --- | --- | --- | --- | --- |
| Read source and prepare docs | May inspect and propose | Review/decide business scope | Review evidence | CTO reviews architecture; CIO authorizes protected scope |
| Change C2 source | Only under accepted Engineering route | Approves business intent | Does not implement | CTO accepts integration; CIO scope remains binding |
| Run deterministic tests | Engineering | Not required | Independently reviews/accepts | No live authority implied |
| Execute live SQL/migration/DML | Not authorized by this package | Separate release required | Separate TEST authority required | CIO-specific release required |
| Production or deployment | Not authorized | Not authorized here | Not authorized | Separate governance required |

Formal Assignment IDs are not exposed by the local platform. The recorded technical task IDs and executor provenance are retained, but no formal Engineering or TEST Office appointment is inferred. Database credentials, DPAPI custody and MariaDB lifecycle controls remain outside this document set.

## D09 — Test strategy, plan and acceptance criteria

The canonical plan is `docs/fm02/FM02_C2_OFFLINE_TEST_PLAN_20261016.md`. It distinguishes `SCRIPT_READY`, `SYNTHETIC_PASS`, `LIVE_PASS`, `HOLD` and `NOT_RUN`.

Coverage includes unit/deterministic service rules, migration contract tests, API contract tests, frontend component/UI tests, static/build checks, integration/functional scripts, negative cases, migration/restore/restart procedures, UAT handoff and evidence custody. Current attributable results are 11/11 C2 service tests and 6/6 migration contract tests offline. Backend/API collection is HOLD because `pydantic` is unavailable; foundation collection is not verified because `pymysql` is unavailable; frontend build/component execution is HOLD because the approved Next/TypeScript test environment is unavailable. T2-15 and T2-14B/14C remain separately gated and are not represented as passed here.

## D10 — Engineering standards applicability

The shared convention is `docs/engineering/CROSS_MODULE_CODING_CONVENTION_20261016.md`. It unifies repository layout, Python/Flask/SQL conventions, TypeScript/React/Next conventions, validation, errors, secrets, tests, formatting, lint, typing, build, Git and evidence rules. Existing backend/frontend convention files remain source references; the new document marks global rules versus technology-specific rules and calls out known environment verification gaps.

## D11 — Technical architecture, deployment and operations

The local architecture is a monorepo-style ERP prototype with `src/` frontend, `backend/` Flask application, `04_Engineering/Application/ERP-2.0/restserver/` bounded service source, and `04_Engineering/Database/` migration source. Local development and deterministic test commands are recorded in `README.md`, `CONTRIBUTING.md`, the backend/frontend convention files and the offline test plan.

Operations limits are explicit: no Windows Service, global ACL/firewall change, credential rotation, production activation, live MariaDB operation or arbitrary host execution is implied. Owner-host target operations and Independent TEST terminal verdicts are separate runbooks and remain held unless specifically released.

## D12 — Source control, Git and module delivery

The canonical delivery repository for this package is the nested FM02 repository on branch `codex/fm02-c2-isolated-20261013-001`. Documentation changes are committed locally with focused commits. The existing untracked `evidence/` directory is preserved and is not staged. No remote is configured; therefore no GitHub owner, push destination or remote readback is claimed. Repository Office must verify any future remote and push path.

## Requirement traceability

The detailed requirement-to-design/source/test map is maintained in `FM02_SPRINT01_TRACEABILITY_MATRIX_20261016.md`. Every bounded requirement is mapped to a source or document reference, a current validation state and an explicit open decision where evidence is unavailable.

## Review status and remaining decisions

- CTO technical review: completed in the current workspace against the listed source and evidence.
- Engineering evidence review: attributable to Hilbert backend task `01a14421-8bf5-7531-a63c-88f8f3903ba9` and Lagrange frontend task `01a14421-8cad-7683-9e5e-f00e69211ca3`; no formal Assignment ID is inferred.
- Independent TEST evidence review: attributable to Kierkegaard task `01a14421-8d45-7a82-a485-ffd1460724bb`; its broader P0-C verdict remains HOLD where dependencies or live execution were unavailable.
- Product/domain review: not exposed as a formal current appointment; broader item-center and C2 UI decisions therefore remain explicitly marked as Product/Frontend decisions.
- Repository review: local custody is verified; authorized remote custody is not verified.

The documentation baseline is complete for the bounded, source-verifiable Sprint 1 record. Sprint 2 entry remains not ready until the Product/Frontend scope decision, dependency-complete offline validation, centralized convention location and any required Engineering/TEST authority are resolved.
