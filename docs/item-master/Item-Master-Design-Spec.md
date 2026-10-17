# FM-02 ITEM MASTER — SCHEMA DESIGN V1.1 / FINAL CIO BASELINE CANDIDATE

**Directive:** `CIO-GOV-ERP2-FM02-SCHEMA-DESIGN-CONVERGENCE-20261012-001`  
**Reference:** `CIO-GOV-ERP2-FM02-ITEM-MASTER-SCHEMA-DESIGN-20261012-001`  
**Review date:** 2026-10-12  
**Mode:** Targeted architecture and physical-design convergence only  
**Mutation status:** No application, schema, migration, DEV database, source, or canonical-main mutation  

## 1. Executive recommendation

V1.1 converges the accepted S01–S09 policy into one preferred Item Master physical candidate without importing the historical 89-table model or duplicating downstream authority.

The preferred structure is:

- retain `item`, `uom`, and `item_legacy_identifier`;
- add nine Item Master tables: `item_category`, `item_specification`, `item_supplier_qualification`, `supplier_item_package`, `item_customer_qualification`, `item_uom`, `uom_conversion`, `item_approval`, and `item_lifecycle_event`;
- absorb specification revision into `item_specification` and identity decisions into `item_approval`;
- remove `item_ownership_profile` from the target design;
- keep Product/FG/SKU, BOM, Inventory/Lot, Production, Purchasing master, Sales, Quality disposition, Traceability, and Costing transaction authority in their owning modules.

**Preferred projection:** 18 business tables (the six FM-01 tables, three current FM-02 tables, and nine new Item Master tables) plus `alembic_version`, for 19 BASE TABLEs before any downstream module additions.

This is ready for CIO/Owner schema-baseline acceptance, not for implementation. The only remaining material questions are owner-policy decisions listed in Section 4; the physical candidate is complete enough to expose those decisions without reopening general discovery.

## 2. Accepted policy versus implementation detail

### 2.1 Binding accepted business policy

The following are treated as design inputs, not reopened questions:

1. Item Code is system-generated, opaque, uppercase alphanumeric, exactly 12 characters, enterprise-wide unique and permanently non-reused.
2. Primary categories are exactly `RAW`, `MATERIAL`, `FILM`, `WIP`, and `FG`, with one controlled primary classification per Item.
3. Item identity is separate from supplier, customer, price, packaging, and ownership variation unless business meaning/specification/intended use/quality/regulatory requirement differs.
4. Customer-supplied versus company-purchased supply context must be controlled, but actual inventory ownership, quantity, reservation, valuation, and cost remain downstream facts.
5. Customer-specific approval of a supplier is distinct from general supplier qualification.
6. Common WIP Item identity may support multiple customers; production/material lots and transfer authorization remain separate.
7. One WIP may support multiple distinct Finished Goods.
8. Product/FG/SKU uses accepted Architecture Option C: Product is distinct from FG Item, SKU/GTIN is not forced 1:1, and own-brand substitution is policy-controlled.
9. Supplier, specification, and quality approval is determined at sampling/selection.
10. Multi-UOM is governed; one base/stock UOM exists per Item, conversions are effective-dated, and original transaction quantity/UOM is retained downstream.
11. Item creation is DRAFT; centralized activation approval is required before ordinary mass-operation use.
12. Lifecycle restrictions are distinct from lot-quality restrictions.
13. Legacy evidence is preserved; duplicate historical codes are not automatically merged, split, recoded, or migrated.

### 2.2 Terminology used in this package

| Classification | Meaning |
|---|---|
| Approved business policy | Binding direction from S01–S09; not reopened here |
| Unresolved implementation detail | Can be fixed by SR-3/API/test convention without changing business meaning |
| Genuinely unresolved owner policy | Requires an owner decision before implementation; isolated below |

## 3. Reconciled owner-decision register

| Decision | Recommended default | Consequence if not accepted |
|---|---|---|
| Final category taxonomy owner | Item Master Business Owner owns the five accepted primary categories; subcategory taxonomy is deferred | `item_category` remains controlled but subcategory implementation cannot start |
| Item Code generator and non-reuse ledger | dedicated service/sequence with durable reservation and never-reuse check | create API cannot be promoted beyond bounded DEV |
| Supplier/customer master keys | opaque `supplier_ref`/`customer_ref` contract owned by Purchasing/Sales master | qualification FKs remain reference-by-contract, not physical cross-module FKs |
| Specification payload | revision row stores canonical summary/hash/reference; detailed quality payload owned by Quality/Engineering | only summary/reference API is admitted until payload owner accepts |
| Supply method | `COMPANY_PURCHASED`, `CUSTOMER_SUPPLIED`, or `BOTH` on customer qualification; actual lot owner/valuation downstream | no Item-level ownership table is created |
| UOM rounding policy | explicit conversion mode, decimal scale and rounding mode per rule; catch-weight requires measured transaction value | transaction implementation remains deferred to Inventory/Production/Finance |
| Lifecycle vocabulary | retain accepted states plus controlled `BLOCKED`, `SUPERSEDED`, and `RETIRED`; exact transition matrix is Item Master owner decision | lifecycle API remains read-only/draft-only |
| Legacy source-record key | immutable source snapshot + dataset + source record locator + duplicate occurrence ordinal | source mapping cannot safely proceed when source rows collide |
| Product/SKU boundary | Product/FG/SKU owner governs downstream keys; no Product/SKU table in this baseline | cross-module contract required before Product Structure work |

No named human owner or future IAM/User Master identity is invented here.

## 4. Revised SR-1 conceptual model

### 4.1 Item Master entities

| Entity | Purpose | Authority |
|---|---|---|
| Item | durable identity for a material/part/use identity | Item Master Business Owner |
| UOM | controlled unit reference | Item Master/Operations |
| Item Legacy Identifier | historical/source alias and provenance | Data Migration/source custodian |
| Item Category | one controlled primary classification | Item Master Business Owner |
| Item Specification | versioned specification summary/reference/hash for an Item | Quality/Engineering with Item Master linkage |
| Item Supplier Qualification | general supplier/spec/quality qualification | Purchasing + Quality |
| Supplier Item Package | effective supplier package/purchase representation | Purchasing |
| Item Customer Qualification | customer-approved use and, where restricted, approved supplier qualification | Sales + Quality + Item Master |
| Item UOM | permitted business transaction units and roles | Item Master/Operations |
| UOM Conversion | global or Item-specific effective conversion | Item Master/Operations/Finance constraints |
| Item Approval | activation/specification/identity decision evidence | accountable business role; technical provenance separate |
| Item Lifecycle Event | append-only lifecycle transition history | Item Master authority |

### 4.2 Explicitly non-entities in this baseline

Actual lot ownership, available quantity, reservation/entitlement, cost, valuation, quality disposition, production batch, WIP-to-FG structure, Product, SKU, GTIN, price, supplier master and customer master are not Item Master entities. They consume Item keys through contracts owned by Inventory, Finance, Production, Product/Commercial, Purchasing, Sales, Quality, or Traceability.

## 5. Revised SR-2 logical ERD and authority matrix

### 5.1 Relationship matrix

| Parent | Child | Cardinality | FK/delete rule | Authority/meaning |
|---|---|---:|---|---|
| `uom` | `item.base_uom_code` | 1:N | RESTRICT | exactly one base/stock UOM per Item |
| `item_category` | `item` | 1:N | RESTRICT | exactly one primary category after taxonomy acceptance |
| `item` | `item_legacy_identifier` | 1:N | RESTRICT | source aliases; code alone is not unique |
| `item` | `item_specification` | 1:N | RESTRICT | immutable/effective specification revisions in one table |
| `item` | `item_supplier_qualification` | 1:N | RESTRICT | general supplier qualification |
| `item_supplier_qualification` | `supplier_item_package` | 1:N | RESTRICT | package versions do not create Item identity |
| `item` | `item_customer_qualification` | 1:N | RESTRICT | customer approval and optional supplier restriction |
| `item_supplier_qualification` | `item_customer_qualification` | 1:N | RESTRICT | explicit customer-approved supplier link |
| `item` | `item_uom` | 1:N | RESTRICT | permitted business UOM roles |
| `uom` | `item_uom` / `uom_conversion` | 1:N | RESTRICT | reference integrity |
| `item` | `uom_conversion` | 1:N or global | RESTRICT | Item-specific when non-null; global when null |
| `item` | `item_approval` | 1:N | RESTRICT | activation and identity decisions |
| `item` | `item_lifecycle_event` | 1:N | RESTRICT | append-only status history |

No cross-database FKs and no cascade deletes are admitted.

### 5.2 Authority matrix

| Fact | System of record | Item Master responsibility |
|---|---|---|
| Item identity/category/status | Item Master | owns current identity and lifecycle state |
| Supplier qualification | Purchasing/Quality | Item Master stores approved relationship reference |
| Customer approved supplier | Sales/Quality/Item Master decision | Item Master stores scoped approval row |
| Actual lot owner/quantity | Inventory | Item Master only provides Item and supply-policy keys |
| Reservation/entitlement | Inventory/Sales | no duplicate Item Master state |
| Direct-material cost/valuation | Finance/Costing | no duplicate Item Master valuation table |
| Specification detail | Quality/Engineering | Item Master stores revision identity/hash/reference |
| WIP/FG/Product/SKU | Product/BOM/Production | future contracts consume Item identity |
| Technical execution | CTO/Engineering | recorded as provenance only; never business approval |
| Business approval | accountable role/actor | recorded in `item_approval` with separate technical provenance |

## 6. Corrected six design defects

### 6.1 Customer-specific supplier qualification

`item_supplier_qualification` is the general qualification. `item_customer_qualification` is the customer-specific permission and may reference one exact general qualification.

Preferred row semantics:

- `approval_scope = SPECIFIC_SUPPLIER` requires `supplier_qualification_id`.
- `approval_scope = ANY_GENERAL_QUALIFIED_SUPPLIER` permits a null supplier reference and means the customer approved the Item for any currently active general qualification.
- Customer A + Item + Supplier X creates a row pointing to X's qualification. Supplier Y's active general qualification does not satisfy that row.
- An effective active row is unique by customer, Item, scope, supplier qualification and start time. Overlapping active rows are prohibited by service validation under a transaction lock.

The model therefore rejects Supplier Y for Customer A when only X is approved; it does not infer permission from shared Item identity.

### 6.2 Legacy identifier provenance

The existing uniqueness over `(legacy_system, legacy_entity, legacy_code, alias_role)` is incompatible with the accepted source evidence and must be replaced in a future authorized migration.

Stable source-record identity:

`source_record_id = SHA-256(source_system | source_dataset | source_snapshot_hash | source_row_locator | duplicate_occurrence_ordinal)`

The ordinal is assigned deterministically within the immutable source snapshot after stable row ordering. It is not derived from the legacy code alone.

Preferred `item_legacy_identifier` semantics:

- unique `(source_system, source_dataset, source_record_id, alias_role)`;
- retain `legacy_code` as searchable, non-unique evidence;
- `target_item_id` may be null while mapping is `UNRESOLVED`;
- multiple source records may map to one canonical Item;
- same old code may map to different Items when source records differ;
- source conflict remains unresolved and cannot activate an Item or silently merge/split it.

### 6.3 Ownership and valuation boundary

`item_ownership_profile` is **removed from the target design**. It would duplicate actual inventory-lot ownership, quantity, reservation, valuation, and cost-accounting authority.

The Item Master retains only the approved supply/use policy needed for admission:

- `item_customer_qualification.approved_supply_method` = `COMPANY_PURCHASED`, `CUSTOMER_SUPPLIED`, or `BOTH`;
- optional `direct_material_treatment_code` is a policy reference, not a cost amount;
- actual owner, lot, quantity, entitlement, transfer, valuation and cost are recorded by downstream modules;
- exceptional cross-customer transfer requires downstream authorization referencing the customer qualification and Item.

This preserves customer-supplied/company-purchased semantics without creating a second inventory authority.

### 6.4 Multi-UOM and effective conversions

The design supports:

- one `item.base_uom_code`;
- multiple `item_uom` transaction roles (`PURCHASE`, `PRODUCTION`, `BOM`, `SALES`, `STOCK`);
- global conversion (`uom_conversion.item_id IS NULL`) and Item-specific conversion;
- supplier package versions linked to a qualification and package UOM;
- `conversion_mode = FIXED` or `CATCH_WEIGHT`;
- explicit `decimal_scale` and `rounding_mode`;
- non-overlapping active effective periods;
- immutable transaction quantity/UOM retention in downstream transaction tables.

`uom_code CHAR(3)` is retained for compatibility with the accepted DEV vocabulary. The design does not invent longer codes or conversion values. If future owner-approved UOM codes exceed three characters, that is a separate compatibility decision and migration, not a silent widening.

MariaDB has no general exclusion constraint for temporal overlap. Therefore the service transaction must lock the deterministic scope before checking/inserting:

1. Lock the parent Item row for Item-specific conversions, or lock the ordered `from_uom_code/to_uom_code` reference rows for global conversions.
2. Query active rows for the same scope and reject any interval where `new_from < existing_to` and `existing_from < new_to` (open ends treated as infinity).
3. Insert/update only after the overlap check; exact duplicate keys remain DB-unique.
4. Commit conversion and approval evidence atomically.

The same parent-row lock plus overlap validation applies to customer qualification, supplier qualification, specification revisions, packages, and Item-UOM roles. Concurrent conflicting writes must produce one accepted row and one deterministic rejection, never two active overlapping rows.

### 6.5 Business approval versus technical execution

`item_approval` contains separate fields for:

- `business_actor_type` and opaque `business_actor_ref`;
- `accountable_approval_role`;
- `delegated_authorization_ref` when applicable;
- `decision_evidence_ref`;
- `effective_at` and decision time;
- `technical_work_item_id`;
- `technical_executor_assignment_id`;
- `technical_executor_ref`;
- `correlation_id`.

The technical Assignment may prove who executed a change, but it cannot satisfy the business approver field. No named person or future IAM identity is invented.

### 6.6 Table necessity and normalization

| V1 candidate | Disposition | Reason |
|---|---|---|
| `item_category` | REQUIRED | S01/S05/S08 require controlled classification |
| `item_specification` | REQUIRED | S01/S03/S08 require specification identity and effectivity |
| `item_specification_revision` | COMBINE WITH EXISTING (`item_specification`) | separate parent adds no authority; revision rows in one table preserve version history |
| `item_supplier_qualification` | REQUIRED | S01/S03 require general supplier/spec/quality qualification |
| `supplier_item_package` | REQUIRED | S03/S07 require package/effective purchase representation |
| `item_customer_qualification` | REQUIRED | S02/S04/S06 require customer-specific permission and supplier restriction |
| `item_ownership_profile` | REMOVE FROM TARGET DESIGN | duplicates Inventory/Finance ownership and valuation authority |
| `item_uom` | REQUIRED | S07 needs multiple controlled transaction UOM roles |
| `uom_conversion` | REQUIRED | S07 needs global/Item-specific effective conversion |
| `item_approval` | REQUIRED | S08 and approval/identity decisions need auditable business decisions |
| `item_lifecycle_event` | REQUIRED | S08 needs append-only lifecycle history separate from current state |
| `item_identity_decision` | COMBINE WITH EXISTING (`item_approval`) | identity decisions are a typed approval/decision event, not a second authority |

## 7. Revised SR-3 physical candidate

### 7.1 Existing table field-level delta against Sprint-01

#### `item` current baseline

Current `fm02_item_master_0002_business_names` fields are:

`item_id CHAR(36) NOT NULL PK`; `item_code CHAR(12) NOT NULL UNIQUE`; `primary_category VARCHAR(16) NOT NULL CHECK`; `display_name VARCHAR(255) NOT NULL`; `description TEXT NULL`; `ownership_context VARCHAR(128) NOT NULL`; `base_uom_code CHAR(3) NOT NULL FK`; `lifecycle_status VARCHAR(16) NOT NULL DEFAULT 'DRAFT' CHECK`; `specification_summary TEXT NULL`; `specification_reference VARCHAR(255) NULL`; `identity_fingerprint CHAR(64) NOT NULL`; `created_at DATETIME(6) NOT NULL`; `updated_at DATETIME(6) NOT NULL`; `created_by_assignment_id BIGINT UNSIGNED NULL`; `correlation_id VARCHAR(128) NULL`; `source_reference VARCHAR(255) NULL`; `provenance_note TEXT NULL`.

Future candidate delta:

- ADD nullable transitional `item_category_id CHAR(36)` FK to `item_category`; final NOT NULL after category backfill and owner acceptance.
- RETAIN `primary_category` during transition; final service treats it as compatibility/read-only after category authority is accepted.
- RECLASSIFY `ownership_context` as non-authoritative compatibility text; no new ownership table.
- ADD nullable `updated_by_assignment_id BIGINT UNSIGNED`.
- RETAIN `identity_fingerprint` as duplicate-detection evidence only; never a merge key.
- Keep `item_code` 12-character, uppercase, generated, enterprise-unique and non-reused.
- Expand lifecycle CHECK to the accepted governed vocabulary only after owner acceptance; do not silently activate new values.

#### `uom` current baseline and delta

Current fields: `uom_code CHAR(3) NOT NULL PK`, `uom_name VARCHAR(64) NOT NULL`, `lifecycle_status VARCHAR(16) NOT NULL DEFAULT 'ACTIVE' CHECK ('ACTIVE','INACTIVE')`, `provenance_note VARCHAR(255) NOT NULL`.

Future candidate delta: ADD nullable `uom_family VARCHAR(32)`, NOT NULL `decimal_precision TINYINT UNSIGNED DEFAULT 6`, plus created/updated timestamps and assignment/correlation provenance. Existing five codes remain unchanged; no historical conversion value is invented.

#### `item_legacy_identifier` current baseline and delta

Current fields: `legacy_reference_id CHAR(36) NOT NULL PK`, `item_id CHAR(36) NOT NULL FK`, `legacy_system VARCHAR(128) NOT NULL`, `legacy_entity VARCHAR(128) NOT NULL`, `legacy_code VARCHAR(191) NOT NULL`, `alias_role VARCHAR(32) NOT NULL DEFAULT 'LEGACY_REFERENCE'`, `provenance_ref VARCHAR(255) NOT NULL`, `created_at DATETIME(6) NOT NULL`, and unique `(legacy_system, legacy_entity, legacy_code, alias_role)`.

Future candidate delta: ADD `source_dataset VARCHAR(255) NOT NULL`, `source_snapshot_hash CHAR(64) NOT NULL`, `source_record_id CHAR(64) NOT NULL`, `source_row_locator VARCHAR(255) NOT NULL`, `duplicate_occurrence_ordinal INT UNSIGNED NOT NULL`, `mapping_status VARCHAR(16) NOT NULL DEFAULT 'UNRESOLVED'`, nullable `target_item_id` only if the current `item_id` is changed to permit unresolved source rows, `valid_from/valid_to DATETIME(6) NULL`, and `correlation_id VARCHAR(128) NULL`. Replace code-only uniqueness with source-record uniqueness. This requires a future migration and a data-semantics decision for existing DEV rows; it is not applied here.

### 7.2 New table data dictionary

All new IDs are `CHAR(36) NOT NULL` PKs. All timestamps are `DATETIME(6) NOT NULL` unless stated. All FKs are `ON DELETE RESTRICT ON UPDATE RESTRICT`; audit fields are `created_by_assignment_id`, `updated_by_assignment_id` where mutable, and `correlation_id` where cross-request attribution is needed.

| Table | Columns (type; null/default) | PK / unique / checks / indexes |
|---|---|---|
| `item_category` | `category_id`; `category_code VARCHAR(32)`; `category_name VARCHAR(128)`; `parent_category_id CHAR(36) NULL`; `lifecycle_status VARCHAR(16) DEFAULT 'DRAFT'`; audit/provenance | PK; unique code; self-FK RESTRICT; allowed status; indexes parent/status |
| `item_specification` | `specification_id`; `item_id CHAR(36)`; `revision_no INT UNSIGNED`; `specification_code VARCHAR(64)`; `specification_hash CHAR(64)`; `specification_summary TEXT`; `specification_reference VARCHAR(255) NULL`; `revision_status VARCHAR(16) DEFAULT 'DRAFT'`; `effective_from DATETIME(6)`; `effective_to DATETIME(6) NULL`; `approved_by_assignment_id BIGINT UNSIGNED NULL`; source/provenance/correlation | PK; FK Item RESTRICT; unique `(item_id, revision_no)`; positive revision; indexes Item/status/effectivity |
| `item_supplier_qualification` | `qualification_id`; `item_id CHAR(36)`; `supplier_ref VARCHAR(128)`; `specification_id CHAR(36) NULL`; `quality_grade VARCHAR(64) NULL`; `qualification_status VARCHAR(16) DEFAULT 'DRAFT'`; effective period; authority/evidence/source/provenance/correlation | PK; Item/spec FKs RESTRICT; unique exact supplier/spec/effective-start; index supplier/status; no overlapping active period by locked service validation |
| `supplier_item_package` | `package_id`; `qualification_id CHAR(36)`; `package_code VARCHAR(64)`; `quantity DECIMAL(20,6)`; `package_uom_code CHAR(3)`; `purchase_only_flag BOOLEAN DEFAULT TRUE`; `effective_from`; `effective_to NULL`; `package_status VARCHAR(16) DEFAULT 'DRAFT'`; audit/provenance | PK; qualification/UOM FKs; unique qualification/package/effective-start; quantity > 0; index qualification/effectivity |
| `item_customer_qualification` | `customer_qualification_id`; `item_id CHAR(36)`; `customer_ref VARCHAR(128)`; `approval_scope VARCHAR(32)`; `supplier_qualification_id CHAR(36) NULL`; `approved_supply_method VARCHAR(24)`; `authorized_use VARCHAR(128)`; `requirement_reference VARCHAR(255) NULL`; `qualification_status VARCHAR(16) DEFAULT 'DRAFT'`; effective period; business approval/evidence/source/provenance/correlation | PK; Item/supplier-qualification FKs; CHECK specific scope requires supplier FK; allowed supply methods; unique scoped customer/Item/supplier/effective-start; index customer/status |
| `item_uom` | `item_uom_id`; `item_id CHAR(36)`; `uom_code CHAR(3)`; `uom_role VARCHAR(16)`; `measurement_mode VARCHAR(16) DEFAULT 'FIXED'`; `decimal_scale TINYINT UNSIGNED`; `rounding_mode VARCHAR(16)`; effective period; `status VARCHAR(16) DEFAULT 'DRAFT'`; audit/provenance | PK; Item/UOM FKs; unique Item/UOM/role/effective-start; one active STOCK role enforced by locked service transaction; indexes Item/role/status |
| `uom_conversion` | `conversion_id`; `item_id CHAR(36) NULL`; `from_uom_code CHAR(3)`; `to_uom_code CHAR(3)`; `conversion_mode VARCHAR(16)`; `factor_numerator DECIMAL(20,9) NULL`; `factor_denominator DECIMAL(20,9) NULL`; `decimal_scale TINYINT UNSIGNED`; `rounding_mode VARCHAR(16)`; effective period; `status VARCHAR(16) DEFAULT 'DRAFT'`; approval/source/provenance/correlation | PK; optional Item/UOM FKs; FIXED requires positive factors; CATCH_WEIGHT cannot claim a fixed factor; exact key unique; overlap rejected under scope lock |
| `item_approval` | `approval_id`; `item_id CHAR(36)`; `approval_type VARCHAR(32)`; `decision VARCHAR(16)`; `business_actor_type VARCHAR(16)`; `business_actor_ref VARCHAR(128)`; `accountable_approval_role VARCHAR(128)`; `delegated_authorization_ref VARCHAR(255) NULL`; `decision_evidence_ref VARCHAR(255)`; `effective_at DATETIME(6)`; technical WorkItem/Executor fields nullable; `correlation_id VARCHAR(128)`; created timestamp | PK; Item FK; allowed decision/type checks; append-only; indexes Item/type/effective/decision |
| `item_lifecycle_event` | `event_id`; `item_id CHAR(36)`; `from_status VARCHAR(16) NULL`; `to_status VARCHAR(16)`; `reason TEXT`; `effective_at DATETIME(6)`; `business_actor_ref VARCHAR(128)`; `accountable_approval_role VARCHAR(128)`; `decision_evidence_ref VARCHAR(255)`; technical provenance/correlation | PK; Item FK; status transition matrix enforced by service; append-only index Item/effective/status |

### 7.3 Common physical constraints

- UTF-8 `utf8mb4` and InnoDB remain the baseline.
- All FKs are restrictive; no cross-database FK or cascade is allowed.
- All active effective periods must be non-overlapping within their scope; MariaDB service locking is required because no general exclusion constraint is available.
- Every approval/event is append-only; corrections are compensating decisions, not overwrites.
- `source_reference`, `provenance_note`, `decision_evidence_ref`, and `correlation_id` are evidence fields, not business identity keys.
- Numeric conversion values must be positive and bounded by the selected precision; rounding occurs at the transaction boundary owned by the consuming module.

## 8. Scenario-to-schema acceptance matrix

Statuses mean design support only; none is an executed TEST result.

| Case | Facts | Required entities/relationship | Expected outcome | Enforcer | Status |
|---|---|---|---|---|---|
| C01/S01 | Supplier changes; meaning/spec/quality/use same | Item + general supplier qualification | same Item permitted | Item Master service | SUPPORTED IN PROPOSED FM-02 SCHEMA |
| C02/S01/S03 | Supplier changes grade/spec/quality | Item + specification revision + supplier qualification | new Item or explicit identity decision required | Item Master + Quality | SUPPORTED IN PROPOSED FM-02 SCHEMA |
| C03/S02 | Customer A approves Supplier X only; Y generally qualified | customer qualification -> exact supplier qualification | X permitted; Y rejected | Item Master service | SUPPORTED IN PROPOSED FM-02 SCHEMA |
| C04/S02 | Company-purchased vs customer-supplied | customer qualification supply method; downstream lot owner | policy differs without Item duplication; actual owner downstream | Item Master + Inventory/Finance | SUPPORTED BY DEFINED CROSS-MODULE CONTRACT |
| C05/S04 | Shared WIP used for multiple customers | Item + customer qualification + downstream lots/transfer | shared Item; transfer requires authorization | Inventory/Production/Sales | SUPPORTED BY DEFINED CROSS-MODULE CONTRACT |
| C06/S05 | One WIP supports multiple FG | Item keys + future Product Structure | multiple distinct FG permitted later | Product/BOM/Production | SUPPORTED BY DEFINED CROSS-MODULE CONTRACT |
| C07/S06 | Product distinct from FG; SKU/GTIN not 1:1 | Item key + deferred Product/SKU contract | no forced Item/Product identity | Product/Commercial | SUPPORTED BY DEFINED CROSS-MODULE CONTRACT |
| C08/S07 | Base KG; purchase EA; production KG | Item + Item-UOM + UOM refs | approved roles only | Item Master/Operations | SUPPORTED IN PROPOSED FM-02 SCHEMA |
| C09/S07 | Global conversion vs Item-specific; package version | UOM conversion + supplier package + effectivity | scoped conversion selected; package is not identity | Item Master/Purchasing | SUPPORTED IN PROPOSED FM-02 SCHEMA |
| C10/S08 | DRAFT needs activation; lot is on quality hold | Item status + approval + lifecycle event; Quality disposition later | DRAFT blocked for mass operation; lot hold does not disable Item globally | Item Master + Quality | SUPPORTED BY DEFINED CROSS-MODULE CONTRACT |
| C11/S09 | Same old code in different source records | source-record identity + legacy rows | both records preserved; may map differently | Data Migration/Item Master | SUPPORTED IN PROPOSED FM-02 SCHEMA |
| C12/S09 | Multiple source records map to one Item | multiple legacy rows -> one Item | permitted only with explicit mapping evidence | Data Migration/Item Master | SUPPORTED IN PROPOSED FM-02 SCHEMA |

### 8.1 Required negative cases

| Negative case | Expected rejection/hold | Physical/service control | Status |
|---|---|---|---|
| Unapproved Supplier Y used for restricted Customer A | reject | customer row must point to active Supplier X qualification; locked active-scope check | SUPPORTED IN PROPOSED FM-02 SCHEMA |
| Unauthorized customer-supplied WIP transfer | reject/hold | downstream transfer authorization must reference customer qualification and lot owner; no Item-only bypass | SUPPORTED BY DEFINED CROSS-MODULE CONTRACT |
| DRAFT Item used for mass production | reject | lifecycle/approval service gate; Item current status remains DRAFT | SUPPORTED IN PROPOSED FM-02 SCHEMA |
| Duplicate historical codes represent different Items | preserve and keep unresolved/independent | source-record unique key, not legacy-code unique key | SUPPORTED IN PROPOSED FM-02 SCHEMA |
| Simultaneous conflicting UOM conversions | one commit, one deterministic reject | parent/scope row lock, overlap query, exact-key unique constraint | SUPPORTED IN PROPOSED FM-02 SCHEMA |
| Overlapping specification revisions | reject second overlap | Item row lock + interval check before commit | SUPPORTED IN PROPOSED FM-02 SCHEMA |
| Wrong OEM FG/version substitution | reject downstream fulfillment | Product/SKU/FG contract must reference approved Item/spec/version; not an Item Master-only check | SUPPORTED BY DEFINED CROSS-MODULE CONTRACT |
| Lot-quality hold disables all Item inventory | reject that semantic | Quality disposition is lot-level and separate from Item lifecycle | SUPPORTED BY DEFINED CROSS-MODULE CONTRACT |

## 9. FM-02 versus Item Master boundary

### A. Item Master foundation

Physically implementable later: Item, UOM, legacy/source identity, category, specification revisions, general supplier qualification, customer-specific qualification, package representation, Item-UOM roles, conversions, approval, and lifecycle history.

### B. Required future logical contracts

Item Master must expose stable `item_id`, permanent `item_code`, category, lifecycle, base UOM, approved specification revision, qualification references, and provenance/correlation. Product/FG/SKU may reference these keys but must not be assumed 1:1. Transaction services must preserve original quantity/UOM and actual lot/owner/cost facts.

### C. Later FM-02 Product/SKU work

Product family, FG-to-Product relationship, SKU/GTIN, own-brand substitution, customer variant and fulfillment versioning require a separate Product/SKU work package and owner decisions.

### D. Other owning modules

| Capability | Owning module | Required Item contract |
|---|---|---|
| BOM/Product Structure | FM-03 BOM/Planning/Production | Item and approved specification revision references |
| Inventory/Lot/Reservation | Inventory/Traceability | Item, UOM, actual owner, lot, quantity and transfer authorization |
| Purchasing/Supplier Master | Purchasing | supplier reference + Item supplier qualification |
| Sales/Customer Master | Sales | customer reference + customer qualification |
| Quality | Quality | specification revision, sampling/approval, lot disposition |
| Costing/Finance | Finance/Costing | Item and supply method policy; actual valuation/cost owned here |

### E. Approved Product/SKU boundary

This milestone is limited to Item Master identity, fields, status, lifecycle, and applicable Item-scoped reference contracts. Product, Product Structure, FG, SKU/GTIN, Customer Variant, and downstream Product/SKU functionality remain outside this Create/Edit implementation scope. No new Product/SKU schema, endpoint, UI feature, or transaction is authorized by this milestone. Item Master may expose only the approved bounded reference/contract surface needed by owning modules; it must not create Product/SKU records or infer Item-to-Product/SKU identity.

Authority: `Business-Owner-Review-Response-FM02-Item-Master-Create-Edit-Bounded-Business-Decision-20261017-001`, Decision Table E=APPROVED, with references to `FM02-ITEM-MASTER-SCHEMA-DESIGN-V1.1-FINAL-CIO-BASELINE-CANDIDATE-20261012-001` Sections 2.1(7), 4.2 and 9, and `ERP2-BOR-RESP-FM02-SPRINT01-BUSINESS-DECISION-CLOSURE-20261017-106` B02.

## 10. API, UI, migration, and recovery contract

### 10.1 Existing API delta

The current bounded APIs may remain:

- `POST /api/v1/items`: generated 12-character Item Code, DRAFT only, no implicit approval/merge.
- `GET /api/v1/items/{item_id}` and list: current identity/readback.

Future write groups require separate implementation work packages:

1. category and identity submission;
2. specification revision submission/approval;
3. supplier qualification and package version;
4. customer qualification and supplier restriction;
5. Item-UOM/conversion management;
6. activation/lifecycle and identity-decision approval;
7. legacy mapping/readback.

Every write requires request correlation, idempotency, AuthorityOrigin, business actor/approval role, technical executor provenance, validation and append-only evidence.

### 10.2 UI/role requirements

Draft entry, identity evidence, specification, qualification, package, UOM, lifecycle, and approval history must be distinct views/permissions. A technical Engineering Assignment cannot satisfy the business approval control. Product/SKU, lot ownership, quality hold and cost screens remain downstream.

### 10.3 Future migration order

No migration is executed here. The candidate order is:

1. preflight and zero-data/data-conversion decision;
2. `item_category` and `item` category compatibility;
3. `item_specification` revision table;
4. general supplier qualification and package;
5. customer qualification with supplier link;
6. Item-UOM and UOM conversion;
7. `item_approval` and lifecycle event history;
8. legacy source-record key reconciliation;
9. API/readback and cross-module contract validation.

Each step needs immutable source/commit, exact migration hash, backup/reset, downgrade/reapply evidence where safe, independent TEST, and Repository custody. Existing FM-01 six-table schema is not changed by this sequence.

### 10.4 Rollback/recovery

Use forward migration with a preflight snapshot, target-only privilege envelope, transaction boundaries, and a verified backup. Rollback means controlled downgrade/reapply or restore of the isolated DEV target under a later authorization; no destructive rollback is implied by this design. Data conversion must be separately approved because legacy conflicts can be unresolved.

## 11. Future engineering and TEST packages

| Package | Scope | Required evidence |
|---|---|---|
| IM-01 | immutable baseline, category and Item delta | commit/tree, migration hash, data dictionary conformance |
| IM-02 | specification revisions and approvals | business actor versus technical executor proof, overlap negatives |
| IM-03 | supplier/customer qualification and packages | Customer A/X versus Y negative, effective uniqueness |
| IM-04 | Item-UOM/conversion | fixed/catch-weight, rounding, concurrent overlap test |
| IM-05 | lifecycle and identity decisions | DRAFT activation gate, no merge/split/recode negatives |
| IM-06 | legacy source reconciliation | duplicate-code/source-record mapping and unresolved conflict evidence |
| IM-07 | cross-module contract stubs | Product/SKU, BOM, Inventory, Quality, Finance interface tests only |

Before any package: verify Engineering capability/Assignment, immutable source, clean isolated worktree, DEV target, credential/preflight, allowed paths, and exact ReturnTarget/correlation. Independent TEST must use a distinct execution identity where required and must not be substituted by Engineering results.

## 12. Evidence and custody requirements

The following reviewed inputs remain authoritative only within their existing scope:

- V1 review package: `FM02-ITEM-MASTER-COMPLETE-SCHEMA-DESIGN-REVIEW-PACKAGE-V1-20261012-001.md`;
- current FM-02 migrations `fm02_item_master_0001.sql` and `fm02_item_master_0002_business_names.sql`;
- FM-01 physical inventory SHA-256 `5078CD7D29E88B7450C387E18DF142FD94F975841DEA2902CA2DF4AFE8B93092`;
- Business Owner clarification SHA-256 `46ADDC1B155720AD59DD531C4429C11A75CEDE24A179B8910A34480C27B553B3`;
- FM-02 completion report SHA-256 `97012C3043F4A04B11E5A0DFE226D74E606AE2F56AD5BF8D469D2636511F8613`;
- historical C1/C4 artifacts remain design references only.

The V1.1 package itself is the new design artifact; no Engineering, TEST, Repository Office, database, or production execution is claimed.

## 13. CIO/Owner acceptance request

Recommended decision:

`FM-02 ITEM MASTER V1.1 = READY FOR CIO SCHEMA BASELINE ACCEPTANCE`

Acceptance should approve the preferred physical candidate and the explicit cross-module contracts, while separately recording the owner-policy register in Section 3. Acceptance should not authorize DDL, migration, API/UI implementation, Product/SKU implementation, or a new Sprint.

### Final status

`FM-02 ITEM MASTER — SCHEMA DESIGN V1.1 = COMPLETE / READY FOR CIO SCHEMA BASELINE ACCEPTANCE`

### Explicit non-authorizations

`DDL = NOT AUTHORIZED`  
`MIGRATION = NOT AUTHORIZED`  
`APPLICATION/API/UI IMPLEMENTATION = NOT AUTHORIZED`  
`PRODUCT/SKU/BOM/INVENTORY/PRODUCTION IMPLEMENTATION = NOT AUTHORIZED`  
`PRODUCTION / RELEASE / GO-LIVE = NOT AUTHORIZED`

## 14. Integrated Item Master Design Amendment — 2026-10-17

### 14.1 Amendment authority and scope

This section records the CIO/Product Owner confirmation of the A–E Item Master policy expressed by the explicit A–E boundary sections in Section 9 and the CTO cross-layer design review by Engineering A (Database/Schema), Engineering C (Backend/API), and Engineering D (Frontend/UI). It amends this authoritative candidate specification; it does not create a competing design document.

Approved policy decisions:

- Item Code is server-generated, opaque uppercase alphanumeric, exactly 12 characters, enterprise-wide unique, atomically reserved, immutable and permanently non-reusable.
- Create requires `display_name`, `primary_category`, `ownership_context`, and `base_uom_code`, and always creates `DRAFT`.
- Category changes are controlled Item Owner corrections; after formal use they require affected-domain review and audit. Material identity changes use identity governance.
- Base UOM cannot change after transaction, BOM or other formal business use.
- UOM/specification records are Item-scoped, revised rather than overwritten, effective-period non-overlapping, historically retained and have no unapproved global fallback. Internal precision is preserved and rounding occurs only at approved output boundaries. Catch-weight requires Item-level authorization.
- Lifecycle transitions are exactly: `DRAFT -> ACTIVE|BLOCKED|INACTIVE`; `ACTIVE -> BLOCKED|INACTIVE|SUPERSEDED|RETIRED`; `BLOCKED -> ACTIVE`; `INACTIVE -> ACTIVE`; `SUPERSEDED -> RETIRED`; `RETIRED -> none`. All other transitions are prohibited.
- `SUPERSEDED` and `RETIRED` cannot reactivate. `SUPERSEDED` retains successor traceability. Every transition requires business authority, applicable delegation, reason, evidence, timestamp, prior/new state and audit provenance.
- Product Structure, Product, SKU/GTIN, customer variants and downstream Product behavior remain outside this Item Master scope.

The following new forward/rollback migration source is authorized but has not been executed:

1. Item Name before/after field-change audit history.
2. Item-level `BLOCKED` lifecycle support.
3. Item-level `SUPERSEDED` lifecycle support and successor relationship.
4. Durable Item Code allocation/non-reuse ledger.

Existing migrations 0003–0006 remain immutable.

### 14.2 Field and permission matrix

| Field/operation | Create | Post-create | Authority and audit | API/UI behavior |
|---|---|---|---|---|
| `item_code` | Server only | Locked forever | Allocation ledger; no reuse | Never an input; read-only output |
| `item_id` | Server only | Locked | Server provenance | Never an input |
| `display_name` | Required | Controlled name-correction action | Before/after, reason, business actor, approver/role, timestamp, evidence, correlation | Separate correction action; material identity change is rejected/routed |
| `primary_category` | Required; controlled vocabulary | Authorized Item Owner correction; after formal use requires affected-domain review | Reason, actor, review and audit evidence | Controlled edit; never a free-form value |
| `ownership_context` | Required compatibility attribute | Controlled by authorized Owner; never actual lot ownership/valuation | Actor, reason and audit | Not presented as inventory ownership |
| `base_uom_code` | Required valid UOM | Locked after transaction, BOM or formal business use | Controlled correction before use; audit and review | Lock state shown; no direct edit after use |
| specification/conversion | Optional initial reference | New revision; no destructive overwrite; active periods cannot overlap | Approval, effective dates, history and evidence | Revision workflow, not overwrite |
| lifecycle | Server sets `DRAFT` | Explicit lifecycle action only | Actor, approver, reason, timestamp, before/after, evidence | No status dropdown; action-specific controls |
| `row_version`, timestamps and provenance | Server only | Server only | Optimistic concurrency and traceability | Read-only display where appropriate |

### 14.3 Physical design and migration contract

#### Item Code allocation/non-reuse ledger

Add `item_code_allocation` with a non-deletable row for every generated code:

- `allocation_id CHAR(36)` primary key;
- `item_code CHAR(12) NOT NULL` with uppercase-alphanumeric and length checks;
- `allocation_status` in `RESERVED`, `CONSUMED`, `ABANDONED`;
- nullable `item_id` foreign key, required for `CONSUMED`;
- unique `request_idempotency_key`;
- `reserved_at`, nullable `consumed_at`, nullable `abandoned_at`;
- allocation reason, assignment provenance, correlation and source note.

Allocation rows are never deleted. Abandoned codes remain unavailable. Create uses a strong opaque candidate generator, retries unique-key collisions, reserves under transaction protection, and consumes or abandons the reservation without recycling a code. The implementation must preserve idempotency and concurrency determinism.

#### Item Name audit

Add append-only `item_name_change_audit`:

- `audit_id CHAR(36)` primary key;
- `item_id` foreign key with restricted deletion;
- `before_display_name`, `after_display_name`, `change_reason`;
- change timestamp, business actor, accountable approval role, evidence reference;
- technical assignment/executor provenance and correlation/request reference.

The audit row and Item update are atomic. A material identity/specification/intended-use/quality/regulatory change cannot be represented as a name correction.

#### Lifecycle extension

Extend the Item lifecycle vocabulary to include `BLOCKED` and `SUPERSEDED`. Add a restricted successor relationship for `SUPERSEDED` Items; a supersession must identify an approved successor Item and preserve the historical event. Lifecycle events remain append-only and enforce the transition matrix in the service transaction. `RETIRED` remains terminal.

All new migration source must have a forward and rollback companion, preserve 0003–0006, document rollback limits, and pass static migration-contract checks before any target execution is considered.

### 14.4 Create/Edit and lifecycle API contract

#### Create

`POST /api/v1/items` accepts the four required business fields plus correlation and idempotency metadata. Item Code, Item ID, lifecycle, row version, timestamps and provenance are server generated. The response returns the generated identity, `DRAFT` state, `row_version` and provenance reference. A repeated idempotency key with the same canonical fingerprint returns the original result; a conflicting fingerprint returns `409` without mutation. Product/SKU/GTIN/BOM/production records are never created by Item Create.

#### Edit and revisions

Edit operations require `row_version` and an idempotency key. Stale writes return `409` without overwrite. Name correction, category correction, specification revision, UOM/conversion revision and lifecycle actions are distinct operations; they are not hidden behind an unrestricted generic update. Every successful write records actor, authority/delegation evidence, reason where required, technical executor provenance, correlation and before/after values.

The technical error contract is:

- `400` for malformed or field validation failure with stable field-level errors;
- `401` for missing/invalid authentication;
- `403` for authenticated but unauthorized operation;
- `409` for duplicate allocation, idempotency conflict, overlap, stale version or prohibited transition;
- database constraint failures roll back and return a stable non-secret conflict code.

#### Lifecycle actions

Lifecycle actions are explicit endpoints or an equivalent action contract. `ACTIVE` requires business approval evidence; the technical executor cannot self-approve. `BLOCKED`, `INACTIVE`, `SUPERSEDED` and `RETIRED` require the approved authority, reason, timestamp and evidence. `SUPERSEDED` requires successor linkage. No action may reactivate `SUPERSEDED` or `RETIRED`.

### 14.5 Frontend/UI contract

The Create form exposes only approved business inputs and displays server-only fields as read-only. It must validate required fields, category vocabulary, valid UOM, effective-date ordering, non-overlap, positive conversion values and catch-weight eligibility. It must present permission failures, field errors, overlap conflicts and stale `row_version` conflicts without masking server results.

Name correction is a separate audited action. Category correction shows the Owner/review requirement. Base UOM becomes visibly locked after formal use. Specification and conversion changes create revisions. Lifecycle changes use explicit action controls and show before/after status, business actor, approver/role, reason, effective timestamp, evidence and correlation. No Product/SKU UI is added.

### 14.6 Requirement traceability and future tests

| Requirement | Database | API | UI | Required future test |
|---|---|---|---|---|
| Permanent Item Code | allocation ledger, unique constraints | server allocation and idempotent Create | read-only code | collision, retry, abandonment, replay and non-reuse |
| Name correction audit | append-only name audit | dedicated correction operation | audited correction action | before/after atomicity and material-change rejection |
| Base UOM lock | Item/UOM references and use checks | reject after formal use | lock state | transaction/BOM/use negative |
| Revisions/effective periods | revision/effective fields and scope constraints | overlap conflict and revision creation | revision workflow | overlap, history and concurrency |
| Lifecycle | lifecycle vocabulary, successor FK and event history | explicit transition/approval actions | action controls and audit display | every allowed transition plus every prohibited transition |
| Authorization/provenance | approval/event/audit references | 401/403, actor/approver separation | role-aware controls | technical executor cannot approve |
| Product boundary | no Product/SKU tables or writes in this scope | no Product/SKU side effects | no Product/SKU controls | side-effect exclusion |

### 14.7 Design review disposition

Engineering A, C and D completed the bounded technical design review against this shared baseline. CTO cross-layer review finds the contracts consistent. This section is the design baseline for the next approval and Git/Knowledge custody step. No migration, database, runtime, production or full integration test has been executed.
