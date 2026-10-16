# FM-02 Item Master C2 Module Contract

Status: source-reconciled, non-production implementation contract
Date: 2026-10-16

This document consolidates the currently implemented FM-02 C2 scope. It does not expand the frozen scope and does not authorize live database execution.

## 1. Bounded business scope

The implemented C2 slice covers:

- Item integrity foundation: controlled category, base UOM, draft creation, item read/list, specification lineage, and approval-gated lifecycle transition.
- C2 reference contract: item-scoped supplier qualification, item UOM rows, item-scoped package/customer/conversion structures.
- C2 package/customer/conversion rules: non-null customer scope key, item-specific conversion only, DECIMAL(38,18) numeric storage, effective-period overlap protection, idempotent retry and conflicting-fingerprint rejection.
- Legacy mapping reconciliation: zero-row admission gate and explicit source-record identity fields; no automatic backfill or guessed target mapping.

Explicitly outside this slice: Product/SKU, BOM, inventory, production transactions, global UOM conversion, customer/supplier master ownership, runtime credential management, UI-to-live-DB integration, migration execution, and production release.

## 2. Physical schema and migration binding

Authoritative implementation files:

| Revision | File | Contract |
| --- | --- | --- |
| 0003 | `04_Engineering/Database/fm02_item_master_0003_integrity_foundation.sql` | Item integrity, specifications, approvals and lifecycle events |
| 0004 | `04_Engineering/Database/fm02_item_master_0004_c2_reference_contract.sql` | Item-scoped supplier qualification and UOM reference contract |
| 0005 | `04_Engineering/Database/fm02_item_master_0005_c2_package_customer_conversion.sql` | Package, customer qualification and item-specific conversion |
| 0006 | `04_Engineering/Database/fm02_item_master_0006_legacy_mapping_reconciliation.sql` | Zero-row-gated legacy mapping reconciliation |

Each forward migration has an explicit revision guard and updates `alembic_version`. Down migrations are data-preserving guards; they do not perform destructive row deletion.

## 3. Domain and transaction rules

- Item creation is draft-only and requires a bounded category, display name, ownership context and active base UOM.
- Active lifecycle transitions require business approval evidence; a technical executor cannot satisfy the business approval requirement.
- Customer qualification and conversion writes lock the parent item before scope validation.
- Identical idempotent requests return the existing durable result. A reused key with a different fingerprint is rejected.
- Effective-period overlap is rejected; boundary-touching periods are allowed.
- Conversion endpoints must be item-scoped and distinct. There is no global conversion fallback.
- C2 0006 requires zero rows in `item_legacy_identifier` before changing its mapping semantics.

## 4. Backend/API contract

The isolated C2 Flask service is `04_Engineering/Application/ERP-2.0/restserver/package/fm02_c2/service.py`.

Implemented routes:

- `POST /api/v1/fm02/items/<item_id>/customer-qualifications`
- `POST /api/v1/fm02/items/<item_id>/uom-conversions`
- `GET /api/v1/fm02/items/<item_id>/uom-conversions/<from_item_uom_id>/<to_item_uom_id>`

The service uses injected connection factories and does not load credentials implicitly. Validation failures are structured, transactions are explicitly committed or rolled back, and the conversion resolver fails closed when no unique active item-specific rule exists.

The repository's broader `backend/app` and `src/services/items-master-api.ts` are a separate prototype/API surface. They are not evidence that the C2 routes are wired into the broader application runtime.

## 5. UI/UX and design-system boundary

The existing `/items` page, `src/types/items-master.ts`, `src/services/items-master-api.ts`, `docs/frontend/*`, and `docs/design-system/ERP_2_0_Design_System_Specification.md` provide the current item-center prototype and visual conventions. They use mock/fallback data and existing item-center concepts.

No C2-specific customer-qualification, item-UOM, package, conversion-rule or legacy-mapping screens are implemented or contractually wired to the C2 service. Those screens require a separately accepted UI/API integration scope and therefore remain PARTIAL rather than being represented as complete.

## 6. Authorization and operations

The C2 service and migrations preserve the following boundaries:

- non-production target only;
- no implicit credential access;
- no global grants, Windows service, ACL or firewall changes;
- no Restore, Restart, Migration, DDL, DML or Concurrency execution from this document;
- live database-dependent evidence remains `HOLD` or delegated to the Owner-host/Independent TEST route.

The current source and test evidence is technical platform evidence. It is not a retrospective claim of formal Engineering Office or Independent TEST Office appointment.
