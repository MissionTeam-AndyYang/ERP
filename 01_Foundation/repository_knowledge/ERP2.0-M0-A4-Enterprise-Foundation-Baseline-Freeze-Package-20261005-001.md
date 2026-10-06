# ERP2.0-M0-A4 Enterprise Foundation Baseline Freeze Package

- Authorization: `ERP2.0-M0-A4`
- Execution date: `2026-10-05`
- Purpose: foundation baseline consolidation and freeze-package preparation
- Final status: `ERP2.0-M0-A4 FOUNDATION BASELINE = COMPLETE / READY FOR CIO FREEZE DECISION`

## 1. Freeze-package position

This package consolidates M0-A1 discovery, M0-A2 architecture, M0-A3-T1 technical standards, A3-C1 custody/publication, and the BO1/BO2 business clarification results into one CIO-reviewable foundation baseline. It freezes the accepted principles and technical reference set for review; it does not freeze final roadmap priority, unresolved ownership, Source-of-Truth, legal/site scope, security policy, or operational appointments.

No Functional implementation, domain schema, Alembic migration, Track B migration, Production change, Message Bus activation, Authority/route change, Cutover, or Go-Live occurred.

## 2. Authoritative foundation input custody

| Input | Status / SHA-256 |
|---|---|
| M0-A1 Foundation Discovery | report `3CA6CA5D08B3D277CB7C82251982E4BDA9FC50E8807FA346BBF79F2CF496960D`; manifest `17A5212032538B2EAED521602270050175AEBB4E51221AF09787141EB821F134` |
| M0-A2 Foundation Architecture | report `D5DEED37392976F81BD2349EF65A896F10A0F16F02DE5C6495D016BA94805602`; manifest `1F06F4B3391E246AD90D19A59ACD44522053522794AEB7681850C28619252354` |
| M0-A3-T1 Technical Standards | report `99AE5B1CE867876BF13EBF25DC2B09CBA4F7EE7E67849926F279323BEBD9BD52`; manifest `42BFFF5C95EA52556045DE9C8681AEE1A4AC18F595B90C9A0E87F6EABA43850B` |
| M0-A3-C1 Standards Custody/Publication | `561C0D57246878A18A14660E2A7D47D36AD92567E158A8A4C95ED969BBE4457B` |
| M0-A3-BO1 Wave 1 | `8A76F1295CB98098A997D2340357BCAF45607B970EC520D6834B11E3FA281DA9` |
| M0-A3-BO2 Wave 2 | `584A389689AA4FA5FC6357955B6D6A208D50504DBF2FCDA9998798A5F46F8C0D` |

## 3. A — Enterprise Capability Architecture

The accepted capability architecture is:

- Enterprise Foundation / Master Data;
- Product & Engineering;
- Commercial;
- Planning & Supply;
- Inventory & Logistics;
- Manufacturing;
- Quality & Traceability;
- People & Equipment;
- Finance & Cost;
- Knowledge & Improvement;
- Governance, Business Review, and Operational Review as conditional cross-cutting capabilities.

Capability is not Domain, Module, or Feature. Capability classification remains `CORE`, `REQUIRED`, `CONDITIONAL`, `INTEGRATION`, `FUTURE`, or `OUT-OF-SCOPE`; final priority is deferred to M0-A5.

## 4. B — Functional Domain / Module Architecture

| Domain | Candidate modules | Foundation status |
|---|---|---|
| Enterprise Foundation | organization, master data, UOM, site/company, calendar | baseline candidate; legal/site scope deferred |
| Product & Engineering | Item, Product/SKU, Formula/Recipe, Production BOM, Packaging BOM/Structure, Cost BOM, Engineering Change | business principles accepted; named owner/effectivity deferred |
| Commercial | Customer, Sales Order, Pricing, Delivery commitment | Customer SoT and commercial owner deferred |
| Planning & Supply | Demand, Forecast, Planning, Supplier, Purchasing | Supplier SoT and planning authority deferred |
| Inventory & Logistics | Inventory, Warehouse, Location, Lot, Shipment, Transportation | inventory/warehouse SoT and hierarchy deferred |
| Manufacturing | Production Order, consumption, yield, labor | production release/close authority deferred |
| Quality & Traceability | inspection, nonconformance, disposition, genealogy | quality/retention authority deferred |
| People & Equipment | worker, skill, qualification, equipment, maintenance | HR/equipment boundary deferred |
| Finance & Cost | cost center, expense, fixed asset, posting integration | ledger/costing authority deferred |
| Knowledge & Improvement | document, KRO, evidence, CI, review | Track C/F boundaries accepted; CI activation deferred |

Alternative boundaries remain valid where evidence is insufficient: Transportation may be an external TMS boundary; Workforce may be HR integration plus operational labor; Equipment/Maintenance remains separate from financial Asset with a link; Expense may be Finance-owned with HR identity input; Quality and Traceability remain linked but distinct.

## 5. C — Canonical Enterprise Data Model

The canonical logical model includes Item, Product/SKU, UOM, Formula/Recipe, Production BOM, Packaging BOM, Packaging Structure, Cost BOM, Supplier, Customer, Employee/Worker, Skill/Qualification, Equipment, Asset, Maintenance Plan/Work Order, Warehouse, Location, Lot/Batch, Inventory, Sales Order, Purchase Order, Production Order, Shipment/Transportation, Quality Inspection, Expense, Cost Center, and Financial Posting Reference.

### Accepted business principles

1. `Item != Product / SKU`; no 1:1 cardinality is assumed. Item supports purchase, manufacture, logistics, inventory, or component meaning; Product/SKU carries sellable/commercial variant meaning. A Product/SKU may depend on multiple Items; one Item may support multiple Product/SKU contexts.
2. BOM/Recipe lanes remain separate but linked:
   - Formula / Recipe;
   - Production BOM;
   - Packaging BOM;
   - Packaging Structure;
   - Cost BOM.
   These are not collapsed into one undifferentiated authority.
3. Inventory meaning is:
   - `Book Inventory = Movement Ledger`;
   - `Official Inventory Balance = Book Inventory + Approved Count Adjustments`;
   - `Physical Count != automatic Book Inventory change`.
4. Finance owns inventory verification; Warehouse owns physical counting/custody; variance requires Finance validation and Warehouse Supervisor confirmation before an approved adjustment.

### Deferred data decisions

Legal Entity → Company → Site → Plant → Warehouse → Location is not yet an authoritative Phase 1 structure. Item owner, lifecycle approval authority, code uniqueness scope, Supplier SoT, Customer SoT, Movement Ledger SoT, Inventory Balance SoT, adjustment posting authority, and Warehouse hierarchy mapping remain deferred.

No physical tables are frozen by A4.

## 6. D — Database / Schema Architecture

The eight technical standards are the reference baseline:

`ERP2-STD-DB-001`, `ERP2-STD-DEV-001`, `ERP2-STD-ADR-001`, `ERP2-STD-MDP-001`, `ERP2-STD-CTX-001`, `ERP2-STD-MIG-001`, `ERP2-STD-EVR-001`, `ERP2-STD-KRO-001`.

Freeze-candidate technical rules:

- MariaDB `11.4.10` remains the approved non-Production platform; Production is separately authorized.
- One governed Alembic lineage; no silent root/head or namespace collision.
- Track C, Track F Core, Runtime Orchestration, Functional Domain, shared/reference, and migration/evidence ownership are explicit.
- Lowercase `snake_case`, immutable surrogate ID, separate business reference, explicit PK/FK, typed cross-domain reference, and junction-key rules.
- Append/history/event facts where material; state projections are not sole truth.
- Audit minimum is applicability-based: actor/assignment, timestamp, correlation/source, AuthorityOrigin, reason/version/evidence where applicable.
- Half-open effective intervals and explicit timezone for temporal relations.
- Logical retirement first; retention and destructive delete require Business/Security decisions.
- Application Service owns transaction boundaries; constraints first, explicit locks for proven races, concurrency/idempotency tests, no blind retry of uncertain effects.
- PK/FK/unique indexes are mandatory; secondary indexes require query-plan evidence.
- JSON is bounded to opaque external payload/extension/metadata; canonical ERP meaning uses typed fields/entities.
- Isolated deterministic test target, fixtures, reset/reseed, cleanup, shutdown, and evidence manifest are mandatory.

These are technical freeze candidates, not schema/migration execution authorization.

## 7. E — Development / Integration Architecture

The accepted engineering baseline is:

`API / Controller → Application Service → Domain Policy / Rules → Repository / Persistence`

Transport adapters do not own business rules or Authority. Domain Services are distinct from Track F Orchestration; no second retry/replay/orchestration engine is allowed. Frontends use feature/domain pages, shared components, typed API clients, and no direct database access. APIs use versioning, stable errors, correlation, idempotency, pagination/search contracts as applicable, compatibility/supersession, and explicit ReturnTarget/failure semantics.

Configuration is typed and environment-separated; secrets are external. Observability is structured and correlation-preserving. Testing follows:

`unit → service/integration → contract → database/migration → concurrency → independent validation`.

Release requires source/schema/API manifest, rollback evidence, environment identity, and explicit operational authorization.

## 8. F — Migration / Track B Architecture

| Stage | Entry | Exit / evidence | A4 position |
|---|---|---|---|
| B0 Source Inventory | access/custody/owner | inventory, hashes, provenance | candidate entry only |
| B1 Profiling / Qualification | B0 accepted | quality, duplicate/null/code profile | candidate entry only |
| B2 Target Mapping | authoritative target logical model | mapping, rules, exceptions accepted | no execution until target accepted |
| B3 Pilot / Reconciliation | B2 accepted, validated physical target, isolated surface | repeatable pilot, identity/count/balance/lineage reconciliation, rollback | dependency-triggered |
| B4 Production / Cutover | B3 accepted, CIO/Business/Production authorization | rehearsal, final reconciliation, rollback/signoff | separately authorized |

`NO AUTHORITATIVE TARGET MODEL → NO MIGRATION EXECUTION`  
`NO VALIDATED PHYSICAL TARGET → NO PILOT MIGRATION`  
`NO ACCEPTED PILOT / RECONCILIATION → NO PRODUCTION MIGRATION`

## 9. G — Engineering Knowledge / AI Onboarding

All future Modules must use the Module Development Pack, Engineering Context Manifest, ADR where material, Evidence/Release Standard, and KRO versioning/custody standard.

The Context Manifest must carry product/version, environment, authoritative hashes, repository/allowed paths, DB/Alembic/API baseline, Domain/Milestone/Sprint/WorkItem, Participant/Assignment/Context/Scope, Authority ceiling, allowed/prohibited actions, dependencies, open decisions, uncertainty/freshness, validation, cleanup, KRO references, ReturnTarget, CorrelationID, and escalation target.

`STALE / INCOMPLETE CONTEXT → SAFE_STOP`.

Track C owns durable knowledge semantics; Track F owns Work/Authority/runtime semantics. Runtime WorkResult, Message, log, or source file does not become Knowledge without explicit promotion.

## 10. H — Roadmap / Milestone / Sprint Operating Framework

Final sequencing is deferred to M0-A5. A4 freezes only the prerequisite discipline:

- Milestone: bounded domain outcome, target model, dependency, acceptance, validation, custody, release gate.
- Sprint: CTO-approved slice with WorkItems, Participant/Assignment, Context/Scope, evidence, and stop conditions.
- WorkItem: purpose, WorkType, AuthorityOrigin, executor, validation/custody, ReturnTarget, and evidence.
- No implementation before identity, target model, prerequisites, route capability, and owner/source decisions are ready.
- Completion means execution, validation, custody, and evidence requirements are all satisfied; technical pass is not Business acceptance.
- TEST is required where validation/certification risk exists; KRO is required for authoritative design, test, migration, release, and decision evidence.
- PMO triggers bounded Work; it does not invent Authority. CIO gates material business risk, Source-of-Truth, Production, migration, or scope exceptions.

## 11. I — Accepted Business Principle Register

| Principle | Status |
|---|---|
| `Item != Product / SKU` | `ACCEPTED FOUNDATION PRINCIPLE` |
| Item/Product cardinality is not assumed 1:1 | `ACCEPTED BOUNDARY; DETAILED CARDINALITY DEFERRED` |
| Formula/Recipe, Production BOM, Packaging BOM, Packaging Structure, and Cost BOM are separate-but-linked lanes | `ACCEPTED FOUNDATION PRINCIPLE` |
| `Book Inventory = Movement Ledger` | `ACCEPTED BUSINESS PRINCIPLE` |
| `Official Inventory Balance = Book Inventory + Approved Count Adjustments` | `ACCEPTED BUSINESS PRINCIPLE` |
| `Physical Count != automatic Book Inventory change` | `ACCEPTED CONTROL PRINCIPLE` |
| Finance verifies inventory; Warehouse counts/custodies; approved adjustment requires Finance + Warehouse Supervisor path | `ACCEPTED CONTROL PRINCIPLE` |
| Item, supplier, customer, company/site/warehouse and other identity semantics must not be inferred from technical artifacts | `ACCEPTED GOVERNANCE PRINCIPLE` |

## 12. J — Deferred Decision Register

| Decision | Status |
|---|---|
| Phase 1 Legal Entity/Company/Site/Plant/Warehouse/Location list and ownership | `DEFERRED / NAMED OWNER REQUIRED / SOURCE-OF-TRUTH REQUIRED` |
| Item owner and lifecycle approval authority | `DEFERRED / NAMED OWNER REQUIRED` |
| Item code uniqueness scope and retired-code reuse | `DEFERRED / NAMED OWNER REQUIRED / SOURCE-OF-TRUTH REQUIRED` |
| Supplier authoritative system | `DEFERRED / NAMED OWNER REQUIRED / SOURCE-OF-TRUTH REQUIRED` |
| Customer authoritative system | `DEFERRED / NAMED OWNER REQUIRED / SOURCE-OF-TRUTH REQUIRED` |
| BOM/Recipe revision, effectivity, release, and named authority | `DEFERRED / NAMED OWNER REQUIRED / SOURCE-OF-TRUTH REQUIRED` |
| Movement Ledger final artifact/system | `DEFERRED / NAMED OWNER REQUIRED / SOURCE-OF-TRUTH REQUIRED` |
| Inventory Balance final Source-of-Truth | `DEFERRED / NAMED OWNER REQUIRED / SOURCE-OF-TRUTH REQUIRED` |
| Adjustment posting/reversal authority | `DEFERRED / NAMED OWNER REQUIRED` |
| Warehouse/location hierarchy mapping | `DEFERRED / NAMED OWNER REQUIRED / SOURCE-OF-TRUTH REQUIRED` |
| Final roadmap priority | `DEFERRED TO M0-A5` |

## 13. K — Security / Privacy Dependency Register

| Dependency | Required before |
|---|---|
| Personal-data classification for Worker/HR/Customer contact data | People, HR, Commercial implementation |
| Financial classification and access segregation | Finance, Expense, Fixed Asset, inventory valuation |
| Regulated/food-compliance data classification and retention | Quality/Traceability implementation |
| Masking, export, audit, legal hold, deletion, and retention policy | physical schema/API/release decisions involving classified data |
| IAM/least privilege and service credential ownership | runtime activation or external integration |

No Security/Privacy policy was decided by A4.

## 14. L — Operational Dependency Register

- named owners for Item Master, Product, Procurement, Inventory, Warehouse, Production, Quality, Logistics, Finance, HR, Maintenance, and Reporting;
- legal/company/site/plant/warehouse operational hierarchy;
- warehouse/location custody and adjustment workflow;
- TMS/HR/CRM/GL/Maintenance integration ownership;
- support/availability posture for bounded runtime;
- operational acceptance and rollback owner per milestone;
- CI Office, BOR, and CIO-OPS activation triggers.

All remain `OPERATIONAL DECISION DEPENDENT` or `DEFERRED` where not already clarified.

## 15. M — Functional Milestone Prerequisite Matrix

`Implementation may start = NO` unless every required prerequisite is satisfied. Design preparation may proceed only under a separate bounded authorization.

| Candidate Domain/Milestone | Foundation-ready now | Business decision | Security/Privacy | Operational | Source-of-Truth | Technical standard | Earliest Track B stage | Implementation readiness |
|---|---|---|---|---|---|---|---|---|
| Master Data / Item / Product | Item≠Product/SKU; identity standards; P0 runtime; technical standards | named Item owner, lifecycle, code uniqueness, legal/site scope | personal/customer classification as applicable | data stewardship and approval workflow | Item/Product/SKU SoT | DB, DEV, MDP, CTX, EVR, KRO | B0/B1; B2 after target acceptance | `READY AFTER NAMED OWNER DECISION` |
| BOM / Recipe | separate linked lanes; revision/effectivity design | lane owners, approval/release authority | formula/regulated classification | production/release operating rule | WB-004 and Engineering SoT role | DB, MDP, ADR, EVR | B0/B1; B2 after logical target | `READY AFTER SOURCE-OF-TRUTH DECISION` |
| Inventory / Warehouse | movement/count principle; Finance/Warehouse separation | hierarchy, adjustment authority, site scope | financial/regulated retention | count/custody and reconciliation operation | Movement Ledger and Balance SoT | DB, MDP, CTX, MIG, EVR | B0/B1; B2 after source/target mapping | `READY AFTER SOURCE-OF-TRUTH DECISION` |
| Purchasing / Supplier | supplier identity/reference principle | Supplier owner/SoT, approval, receipt | supplier financial/confidential class | procurement approval and exception | Supplier SoT | DB, DEV, MDP, MIG | B0/B1; B2 after mapping | `READY AFTER SOURCE-OF-TRUTH DECISION` |
| Planning | candidate domain boundary and dependencies | planning authority, forecast acceptance | demand/confidential classification | planning review/exception process | forecast/plan SoT | DEV, MDP, CTX, EVR | B0/B1; B2 after target | `READY AFTER OPERATIONAL DECISION` |
| Manufacturing | runtime spine, production domain candidate | release/pause/close and BOM authority | worker/regulated data | plant/work-center operating model | production/consumption SoT | DB, DEV, MDP, EVR | B0/B1; B2/B3 after target | `READY AFTER NAMED OWNER DECISION` |
| Quality / Traceability | lot/evidence principles; TEST/KRO custody | disposition/retention authority | regulated classification/retention | inspection/release/recall process | quality/lot genealogy SoT | DB, MDP, EVR, KRO | B0/B1; B2 after target | `READY AFTER SECURITY DECISION` |
| Workforce / Labor | worker/skill candidate entities | HR/Operations owner and scope | personal-data/IAM policy | labor approval and time model | HR SoT | DB, DEV, CTX, EVR | B0/B1 integration profile | `READY AFTER SECURITY DECISION` |
| Equipment / Maintenance | equipment/asset separation principle | maintenance vs asset ownership | asset/worker classification | maintenance close/support model | maintenance/asset SoT | DB, MDP, MIG, EVR | B0/B1; B2 after boundary | `READY AFTER OPERATIONAL DECISION` |
| Transportation / Logistics | integration-first boundary | TMS/ERP owner and delivery close | customer/location confidentiality | carrier/3PL operating model | TMS/ERP SoT | DEV, MDP, MIG, EVR | B0/B1 integration profile | `READY AFTER OPERATIONAL DECISION` |
| Commercial / Delivery | Item/Product distinction and P0 runtime | Customer SoT, order/delivery authority | customer/privacy/financial policy | fulfillment/exception operation | CRM/ERP/TMS SoT | DB, DEV, MDP, CTX | B0/B1; B2 after mapping | `READY AFTER SOURCE-OF-TRUTH DECISION` |
| Finance / Expense / Fixed Asset | cost center/posting candidates | ledger, costing, expense, asset authority | financial classification/retention | close/approval/reconciliation | GL/expense/asset SoT | DB, MDP, MIG, EVR, KRO | B0/B1; B2 after target | `READY AFTER SECURITY DECISION` |
| Reporting / Analytics | governed metric principle | metric owner and authoritative report | access/export classification | refresh/SLA/acceptance | source metric SoT | DEV, CTX, EVR, KRO | B0/B1; B2 after metric mapping | `READY AFTER NAMED OWNER DECISION` |

No candidate is labelled `FOUNDATION READY` for implementation because all listed milestones retain at least one owner, Source-of-Truth, security, or operational prerequisite. This does not block architecture freeze; it prevents premature implementation.

## 16. Foundation-to-Technical-Standard Reference Map

| Foundation concern | Primary standards |
|---|---|
| entity identity, PK/FK, lifecycle, temporal, audit | `ERP2-STD-DB-001` |
| repository, service, API, integration, testing, release | `ERP2-STD-DEV-001` |
| material architecture decisions | `ERP2-STD-ADR-001` |
| module completeness and milestone gates | `ERP2-STD-MDP-001` |
| Human/AI/Remote worker context and safe-stop | `ERP2-STD-CTX-001` |
| source inventory through cutover | `ERP2-STD-MIG-001` |
| hashes, tests, cleanup, release evidence | `ERP2-STD-EVR-001` |
| version, supersession, provenance, KRO custody | `ERP2-STD-KRO-001` |

## 17. Foundation-to-Track-B Stage Map

| Foundation/Milestone condition | Track B stage |
|---|---|
| source ownership and artifact inventory | B0 |
| source quality, identity, duplicate, null, code profile | B1 |
| accepted canonical/logical target and mapping | B2 |
| validated physical target, pilot, reconciliation, rollback | B3 |
| accepted pilot, Production authorization, cutover rehearsal | B4 |

No domain may use migration to define its target truth.

## 18. Proposed CIO Freeze Decision Matrix

| CIO decision | Recommendation |
|---|---|
| Accept M0-A4 foundation structure | accept for foundation freeze |
| Accept Item/Product separation | accept as foundation principle; defer cardinality/owners |
| Accept separate-but-linked BOM/Recipe lanes | accept; defer named authorities/effectivity |
| Accept Inventory movement/count model | accept; defer final systems/artifacts/posting authority |
| Freeze eight technical standards | approve the A3-T1/A3-C1 references, retaining dependency labels |
| Freeze implementation readiness labels | approve as gate labels; no premature `IMPLEMENTATION READY` |
| Freeze final roadmap | do not freeze in A4; defer to M0-A5 |
| KRO custody/publication | retain A3-C1 custody; future changes require explicit publication/custody action |
| Domain implementation | separate milestone authorization after prerequisite matrix passes |

## 19. Evidence / provenance manifest summary

| Artifact | Hash |
|---|---|
| A3-T1 standards package | `99AE5B1CE867876BF13EBF25DC2B09CBA4F7EE7E67849926F279323BEBD9BD52` |
| A3-T1 standards manifest | `42BFFF5C95EA52556045DE9C8681AEE1A4AC18F595B90C9A0E87F6EABA43850B` |
| A3-C1 custody/publication result | `561C0D57246878A18A14660E2A7D47D36AD92567E158A8A4C95ED969BBE4457B` |
| BO1 clarification | `8A76F1295CB98098A997D2340357BCAF45607B970EC520D6834B11E3FA281DA9` |
| BO2 clarification | `584A389689AA4FA5FC6357955B6D6A208D50504DBF2FCDA9998798A5F46F8C0D` |

## 20. Boundary confirmation

- No Functional modules implemented.
- No domain schema created or altered.
- No Alembic or Track B migration executed.
- No Production change, Message Bus activation, Authority change, route creation, Cutover, or Go-Live.
- No final roadmap priority frozen.
- No Business Owner, Security, Privacy, or Operations truth invented.

## 21. Final status

`ERP2.0-M0-A4 FOUNDATION BASELINE = COMPLETE / READY FOR CIO FREEZE DECISION`
