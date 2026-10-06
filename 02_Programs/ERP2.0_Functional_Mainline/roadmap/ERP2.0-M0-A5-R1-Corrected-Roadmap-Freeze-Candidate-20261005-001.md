# ERP2.0-M0-A5-R1 Corrected Roadmap Freeze Candidate

- Authorization: `ERP2.0-M0-A5-R1`
- Execution date: `2026-10-05`
- Source: M0-A5 Functional Roadmap Baseline
- Final status: `ERP2.0-M0-A5-R1 ROADMAP RECONCILIATION = PASS / ACYCLIC ROADMAP READY FOR CIO FREEZE`

## 1. Reconciliation result

The 15 Major Functional Milestone identities, Sprint Standard, Backlog Standard, WorkItem/Track F mapping, PMO rules, CIO Control-Tower model, conditional review triggers, status vocabulary, progress model, governance cadence, KRO model, and Track B principles are preserved.

The inconsistency is resolved by separating:

- full milestone completion;
- minimum foundation slices needed by a downstream milestone;
- parallel design inputs;
- conditional/downstream consumption.

No Major Milestone is required to complete another Major Milestone where only a bounded slice is needed. No semantic business cycle remains in the execution-readiness graph.

`MILESTONE EXECUTION DEPENDENCY GRAPH = ACYCLIC`

## 2. Corrected Hybrid Scenario H

### Canonical activation order

`FM-01 → FM-02 → FM-03 → FM-04 → FM-05 / FM-06 (parallel after shared prerequisites) → FM-09 → FM-10`

In parallel from FM-01/FM-02:

- `FM-07` design and Workforce Slice `WF-S1`;
- `FM-08` design and Equipment Slice `EQ-S1`;
- `FM-14` metric inventory/design;
- B0/B1 source profiling for every affected domain.

Then:

`FM-04 + COMM-S1 → FM-11`

`FM-02 + COMM-S1 + FM-11 contract → FM-12`

`FM-01 + FIN-S1 + relevant domain evidence → FM-13`

`FM-10 + FM-11 + FM-12 + FM-13 + FM-14 relevant gates → FM-15`

The arrow means “implementation-readiness dependency” only when explicitly classified as `HARD_PREREQUISITE` or `MINIMUM_FOUNDATION_SLICE`. Milestone numbering does not define execution order.

## 3. Issue reconciliation

### Issue A — Workforce/Equipment vs Manufacturing

Corrected rule:

`FM-07 full completion` and `FM-08 full completion` are not hard prerequisites for FM-09.

FM-09 requires:

- `WF-S1 Workforce Identity / Skill / Qualification Foundation Slice`;
- `EQ-S1 Equipment Operational Resource Foundation Slice`;
- a production-specific labor/equipment contract.

Full HR integration and full EAM remain parallel or downstream milestones. This removes the inconsistency between the executive narrative and the old `FM-07 + FM-08 → FM-09` shorthand.

### Issue B — Transportation/Commercial cycle

Corrected rule:

- FM-11 requires `COMM-S1 Customer / Ship-to / Fulfillment Identity Slice`, not FM-12 completion.
- FM-12 may consume FM-11 delivery capability as a `CONDITIONAL_DEPENDENCY` or downstream input, not as a hard prerequisite.

The customer slice is a bounded design/identity prerequisite and does not imply completion of the full Commercial milestone.

### Issue C — Equipment/Maintenance cycle

Corrected rule:

- FM-08 does not require FM-09 completion.
- FM-08 does not require FM-13 completion.
- FM-08 may proceed in parallel after FM-01 and the applicable equipment identity decision.
- FM-09 uses EQ-S1; FM-13 uses an equipment/asset link slice where needed.

The full FM-08 milestone may later consume production/finance evidence, but those are `DOWNSTREAM_DEPENDENCY` or `CONDITIONAL_DEPENDENCY`, never prerequisites for its initial design/implementation gate.

### Issue D — Workforce design dependency

Manufacturing requires the minimum Workforce slice, not full Workforce/HR Integration completion. Full FM-07 remains independent and may be sequenced later or in parallel, subject to personal-data/IAM decisions.

## 4. Canonical acyclic execution graph

```text
FM-01 Shared Enterprise / Master Data
  └─ HARD → FM-02 Item / Product / SKU
       └─ HARD → FM-03 Product Structure / BOM / Recipe / Change
       └─ HARD → FM-04 Inventory / Warehouse / Location / Lot
            ├─ HARD → FM-05 Purchasing / Supplier / Material Readiness
            ├─ PARALLEL DESIGN → FM-06 Demand / Forecast / Planning / Capacity
            ├─ MINIMUM SLICE → FM-09 Manufacturing / Production
            ├─ MINIMUM SLICE → FM-11 Transportation / Logistics / Delivery
            └─ HARD/SLICE → FM-10 Quality / Traceability after production/lot gate

FM-01 ── PARALLEL DESIGN → FM-07 Workforce / Labor / HR
  └─ MINIMUM SLICE WF-S1 ──→ FM-09

FM-01 ── PARALLEL DESIGN → FM-08 Equipment / Maintenance / EAM
  ├─ MINIMUM SLICE EQ-S1 ──→ FM-09
  └─ MINIMUM SLICE Equipment/Asset Link ──→ FM-13

FM-06 ── MINIMUM SLICE PLAN-S1 ──→ FM-09
FM-05 ── CONDITIONAL PUR-S1 ──→ FM-09
FM-12 ── MINIMUM SLICE COMM-S1 ──→ FM-11
FM-11 ── CONDITIONAL/DOWNSTREAM ──→ FM-12
FM-13 ── MINIMUM SLICE FIN-S1 ──→ finance/cost integrations
FM-14 ── PARALLEL DESIGN; consumes domain metrics ──→ FM-15

FM-09 + FM-10 + FM-11 + FM-12 + FM-13 + FM-14 applicable gates ──→ FM-15
```

The graph has no unresolved circular completion requirement.

## 5. Dependency Classification Matrix

| Source | Target | Classification | Gate meaning |
|---|---|---|---|
| FM-01 | FM-02 | `HARD_PREREQUISITE` | shared identity/reference foundation accepted |
| FM-01 | FM-03 | `HARD_PREREQUISITE` | Item/Product meaning available |
| FM-02 | FM-03 | `HARD_PREREQUISITE` | structure references stable item/product identities |
| FM-01 | FM-04 | `HARD_PREREQUISITE` | site/warehouse design inputs and item identity |
| FM-02 | FM-04 | `HARD_PREREQUISITE` | item/UOM identity for quantity truth |
| FM-04 | FM-05 | `HARD_PREREQUISITE` | receiving/material context available |
| FM-04 | FM-06 | `PARALLEL_DESIGN_INPUT` | planning may design from inventory assumptions; implementation gate remains explicit |
| FM-01 | FM-06 | `HARD_PREREQUISITE` | calendar/reference/identity foundation |
| FM-01 | FM-07 | `HARD_PREREQUISITE` | worker domain can design after enterprise identity |
| FM-01 | FM-08 | `HARD_PREREQUISITE` | equipment identity can design after enterprise identity |
| FM-01 | FM-14 | `PARALLEL_DESIGN_INPUT` | metric inventory may start early |
| WF-S1 | FM-09 | `MINIMUM_FOUNDATION_SLICE` | worker/skill/qualification facts sufficient for production contract |
| EQ-S1 | FM-09 | `MINIMUM_FOUNDATION_SLICE` | operational resource identity sufficient for production contract |
| PLAN-S1 | FM-09 | `MINIMUM_FOUNDATION_SLICE` | bounded material/capacity planning input |
| PUR-S1 | FM-09 | `CONDITIONAL_DEPENDENCY` | required only when production scenario relies on purchasing material readiness |
| INV-S1 | FM-10 | `MINIMUM_FOUNDATION_SLICE` | lot identity and movement link |
| FM-09 | FM-10 | `HARD_PREREQUISITE` | production facts are needed for genealogy/quality |
| COMM-S1 | FM-11 | `MINIMUM_FOUNDATION_SLICE` | customer/ship-to/fulfillment identity only |
| FM-11 | FM-12 | `CONDITIONAL_DEPENDENCY` | commercial scope may consume delivery capability |
| FM-12 | FM-11 | `DOWNSTREAM_DEPENDENCY` | full commercial milestone is not required for logistics design |
| EQ-ASSET-S1 | FM-13 | `MINIMUM_FOUNDATION_SLICE` | equipment/asset link for cost/asset integration |
| FIN-S1 | FM-13 | `MINIMUM_FOUNDATION_SLICE` | posting reference/cost center basis |
| FM-09 | FM-13 | `CONDITIONAL_DEPENDENCY` | production cost integration only when in scope |
| FM-10 | FM-15 | `HARD_PREREQUISITE` when regulated scope | compliance/retention evidence |
| FM-11 | FM-15 | `CONDITIONAL_DEPENDENCY` | only if transport/delivery is in cutover scope |
| FM-12 | FM-15 | `CONDITIONAL_DEPENDENCY` | only if commercial is in cutover scope |
| FM-13 | FM-15 | `CONDITIONAL_DEPENDENCY` | only if financial integration is in cutover scope |
| FM-14 | FM-15 | `PARALLEL_DESIGN_INPUT` | reporting readiness can proceed independently; relevant metrics must be accepted for cutover |
| applicable milestones | FM-15 | `HARD_PREREQUISITE` | B3 accepted and operational/reconciliation gates pass |

## 6. Minimum Foundation Slice Register

| Slice | Parent milestone | Minimum meaning | Required decisions | Contract/evidence | Unlocks |
|---|---|---|---|---|---|
| `WF-S1` Workforce Identity / Skill / Qualification | FM-07 | worker identity, minimum qualification, labor attribution | HR SoT, personal-data/IAM, qualification owner | logical/API worker reference, eligibility test, KRO evidence | FM-09 |
| `EQ-S1` Equipment Operational Resource | FM-08 | equipment identity, operational availability, work-center link | equipment owner, maintenance SoT, operational support | logical/API resource contract, identity/readiness test | FM-09 |
| `EQ-ASSET-S1` Equipment/Asset Link | FM-08/FM-13 | link operational equipment to financial asset where needed | Finance/Maintenance boundary, asset SoT | typed link, posting/cost test | FM-13 |
| `INV-S1` Lot / Traceability Foundation | FM-04 | lot identity, movement link, status/effectivity reference | Quality/lot owner, retention/security | lot contract, genealogy seed/readback | FM-10 |
| `PLAN-S1` Planning / Material Requirement | FM-06 | bounded demand/material/capacity input for production | planning SoT and acceptance | planning API/input contract, negative cases | FM-09 |
| `PUR-S1` Supplier / Material Readiness | FM-05 | approved supplier/material/receipt facts | Supplier SoT and procurement approval | supplier/receipt contract, reconciliation | FM-09 conditionally |
| `COMM-S1` Customer / Ship-to / Fulfillment Identity | FM-12 | customer/site/ship-to identity needed for delivery | Customer SoT, privacy/classification | customer/ship-to contract, attribution test | FM-11 |
| `FIN-S1` Financial Posting Reference / Cost Center | FM-13 | cost center and posting reference without full finance | GL/finance SoT, security | typed posting reference, reconciliation | FM-13 |

Slices are prerequisite evidence packages, not new Major Milestones, tables, routes, or implementation authorization.

## 7. Parallel Work Matrix

| Work | May start after | Does not imply | Gate that later consumes it |
|---|---|---|---|
| B0 source inventory | A4/C1 foundation | target model acceptance | B1/B2 decision |
| B1 profiling/qualification | B0 usable | mapping or migration authority | B2 |
| Business owner clarification | A4/C1 | implementation approval | affected milestone |
| Security/privacy classification discovery | A4/C1 | policy decision | affected milestone |
| Operational dependency inventory | A4/C1 | CIO-OPS activation | affected milestone |
| FM-07 Workforce design | FM-01 | full HR completion required for FM-09 | WF-S1 |
| FM-08 Equipment design | FM-01 | full EAM completion required for FM-09 | EQ-S1 |
| FM-14 Metrics design | FM-01 | final metric authority | FM-15 relevant gate |
| FM-11 logistics design | FM-04 + COMM-S1 design | full Commercial completion | transport/fulfillment gate |
| FM-12 commercial design | FM-02 + customer design | full Logistics completion | delivery/Commercial gate |

## 8. Revised 15-Milestone Register

| ID | Revised prerequisite gate | Parallel/conditional note | Next trigger |
|---|---|---|---|
| FM-01 | A4 Foundation/C1 custody | none | FM-02 readiness |
| FM-02 | FM-01 hard | owner/SoT gate | FM-03/FM-04 |
| FM-03 | FM-02 hard | structure lanes parallel after Item contract | FM-09 structure input |
| FM-04 | FM-01 + FM-02 hard | lot slice may precede full warehouse completion | FM-05/FM-06/FM-10 |
| FM-05 | FM-04 hard | Supplier B0/B1 can run earlier | FM-06 or PUR-S1 |
| FM-06 | FM-01 hard; FM-04 design input | may run parallel with FM-05 | PLAN-S1/FM-09 |
| FM-07 | FM-01 hard | full HR integration not FM-09 prerequisite | WF-S1 |
| FM-08 | FM-01 hard | full EAM not FM-09/FM-13 prerequisite | EQ-S1/EQ-ASSET-S1 |
| FM-09 | FM-03 + FM-04 + WF-S1 + EQ-S1 + PLAN-S1; PUR-S1 conditional | no full FM-07/FM-08 | FM-10 |
| FM-10 | FM-09 + INV-S1 when applicable | regulated gate conditional by scope | FM-15 |
| FM-11 | FM-04 + COMM-S1 | no full FM-12 dependency | FM-12 conditional |
| FM-12 | FM-02 + COMM-S1; FM-11 conditional downstream | no FM-11 hard cycle | FM-13/15 |
| FM-13 | FM-01 + FIN-S1 + EQ-ASSET-S1 when applicable | production cost link conditional | FM-15 |
| FM-14 | FM-01 + metric design | consumes domain facts downstream | FM-15 |
| FM-15 | relevant accepted FM gates + B3/reconciliation | B4 separately authorized | Production/Cutover decision |

## 9. Revised Track B Map

| Milestone | B0/B1 parallel | B2 entry | B3 entry | B4 entry |
|---|---|---|---|---|
| FM-01/02 | identity/source inventory | owner + logical target accepted | validated physical target | not applicable until migration scope |
| FM-03 | BOM/recipe/source profiling | lanes/effectivity accepted | pilot structure/reconciliation | only with Production/cutover scope |
| FM-04 | movement/warehouse/lot profiling | SoT/hierarchy accepted | count/movement/balance reconciliation | separately authorized |
| FM-05/06 | supplier/planning profile | target/operational decisions | pilot procurement/planning | separately authorized |
| FM-07/08 | HR/equipment inventories | boundary/security/ops accepted | pilot integration if needed | separately authorized |
| FM-09/10 | production/quality/lot profile | target/authority accepted | production/genealogy pilot | separately authorized |
| FM-11/12 | TMS/customer/order inventory | integration/SoT accepted | interface/order reconciliation | separately authorized |
| FM-13/14 | finance/metric source inventory | target/metric owner accepted | financial/reporting reconciliation | separately authorized |
| FM-15 | consumes prior evidence | no new target definition | B3 acceptance required | B4 after CIO/Business/Production authorization |

No B2/B3/B4 authorization is created by A5-R1.

## 10. PMO Trigger Compatibility Matrix

| Milestone | Prerequisite/slice | Trigger gate | Allowed parallel preparation | Held condition | CIO re-entry |
|---|---|---|---|---|---|
| FM-01 | A4/C1 | foundation in custody, Work scoped | owner/question/source inventory | A4 contradiction | new foundation scope/authority |
| FM-02 | FM-01 + Item owner/SoT | identity design gate | B0/B1 Item sources | owner/code unresolved | identity/SoT change |
| FM-03 | FM-02 | lane/effectivity gate | lane design | BOM authority unresolved | lane collapse/new authority |
| FM-04 | FM-01/02 | inventory model gate | movement/warehouse profiling | balance/warehouse SoT unresolved | adjustment/financial authority |
| FM-05 | FM-04 | supplier/material gate | Supplier B0/B1 | Supplier SoT unresolved | external authority change |
| FM-06 | FM-01 + planning inputs | planning design gate | forecast/capacity profiling | operational plan authority unresolved | priority/scope change |
| FM-07 | FM-01 | HR boundary gate | HR B0/B1 | security/IAM unresolved | personal-data policy exception |
| FM-08 | FM-01 | equipment boundary gate | asset/maintenance profiling | support/ownership unresolved | operational/financial conflict |
| FM-09 | FM-03/04 + WF-S1/EQ-S1/PLAN-S1 | production implementation gate | PUR-S1 if needed | any slice missing | Production authority/schema change |
| FM-10 | FM-09 + INV-S1 | compliance gate | lot/quality profiling | retention/security unresolved | regulated risk |
| FM-11 | FM-04 + COMM-S1 | logistics gate | TMS/interface B0/B1 | TMS/ops unresolved | external integration scope |
| FM-12 | FM-02 + COMM-S1 | commercial gate | customer/order profiling | Customer SoT unresolved | business acceptance |
| FM-13 | FM-01 + FIN-S1 | finance gate | GL/asset/expense profiling | financial/security unresolved | financial authority/Production |
| FM-14 | FM-01 + metrics | metric gate | metric inventory | owner/definition unresolved | executive metric conflict |
| FM-15 | relevant gates + B3 | cutover-readiness gate | runbook/rollback prep | any reconciliation/approval gap | Production/Cutover/Go-Live |

PMO must read the gate/slice facts; it must not infer readiness from milestone numbering or from a previous task being marked complete.

## 11. Preserved Standards

Sprint Standard, Backlog Standard, WorkItem/Track F Mapping, PMO Auto-Trigger Ruleset, CIO Control-Tower Model, BOR/CIO-OPS/CI triggers, status vocabulary, progress measurement, governance cadence, KRO custody, and Track B principles remain valid. Only their dependency inputs are corrected.

## 12. First Milestone Revalidation

`M0-FM-01 Shared Enterprise / Master Data Foundation` remains the recommended first milestone. An Item/Product identity design slice may remain inside FM-01 as preparation, provided it does not bypass FM-02 owner, code uniqueness, Source-of-Truth, or implementation gates.

Before Item/Product implementation, CIO/Business Owner must still resolve:

- named Item/Product owner and lifecycle authority;
- Item code uniqueness scope and retired-code policy;
- legal/company/site/plant/warehouse scope;
- Item/Product/SKU Source-of-Truth and cardinality;
- security classification where applicable.

## 13. Boundary confirmation

- M0-A4 Foundation semantics unchanged.
- 15 Major Milestone identities unchanged.
- No Functional implementation, schema, migration, PMO Functional Program activation, Message Bus, Authority, Route, Production, Cutover, or Go-Live action.
- No Business/Security/Operations truth invented.
- No new Major Milestone created; named slices are prerequisite evidence only.

## 14. Final status

`ERP2.0-M0-A5-R1 ROADMAP RECONCILIATION = PASS / ACYCLIC ROADMAP READY FOR CIO FREEZE`
