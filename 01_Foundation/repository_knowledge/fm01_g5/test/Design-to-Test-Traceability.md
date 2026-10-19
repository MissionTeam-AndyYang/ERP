# FM-01 Design-to-Test Traceability

**Revision:** `ERP2.0-FM01-DESIGN-TO-TEST-20261019-003`
**Exact current Integrated Design Specification:** `ERP2.0-FM01-Integrated-Design-Spec-Candidate-20261018-001.md`, SHA-256 `5BCAF8D4FC018928364337B6EFA82AE6FA41BE5F4BCA1871DA2119761A06DC37`  
**Exact Engineering D UI v002:** `ERP2.0-FM01-UI-UX-CSS-Design-Review-Package-20261018-002.md`, SHA-256 `16132E378C62D14F917AEB85D119CE5EF3F43E67C24FB138C5EE97CC6B49A54D`  
**Execution contract:** `Execution-Contract-Matrix.md`, 53 explicit Case ID mappings.

**API identity note:** Current G2 contract bytes are verified at the exact supplied path with SHA-256 `BE74D50556FBBD7F8DDE4E293DC4B758CE195B9B5D28E901E7D510464FA1D30`. Earlier `F1B193FAC1FB6793E480CA7F197152875E6AAF1880263A835154AF296825ED2A` remains a historical reference; its source bytes are unavailable for independent comparison, so semantic delta is `NOT_VERIFIED` and no mapping is changed by inference.

**Status:** Design mapping prepared; no execution result is inferred.

| Design requirement / source | Test cases | Classification | Coverage state |
|---|---|---|---|
| Six-resource allowlist and GET envelope | GET-01, GET-02, GET-05 | CONTRACT / DB_DEPENDENT | Existing GET-only baseline; mutation-era rerun required |
| Hierarchy `legal_entity -> company -> site -> plant -> warehouse -> location` | GET-03, NEG-01, NEG-02, CRE-02, CRE-05, CRE-06 | UNIT / DB_DEPENDENT | Design covered; live mutation not authorized |
| Pagination default 50, maximum 100 | GET-04 | UNIT / CONTRACT | Existing baseline plus future contract rerun |
| GET-only compatibility and denied writes | GET-07, GET-08, GET-10 | STATIC / CONTRACT / DB_DEPENDENT | Preserved regression baseline |
| Safe errors and sensitive-field exclusion | GET-05, GET-06, GET-09, NEG-07, NEG-08 | CONTRACT / STATIC | Bounded design coverage |
| Create parent, identity and atomic transaction rules | CRE-01 through CRE-09 | UNIT / MOCK / DB_DEPENDENT | Prospective; requires implementation and target admission |
| Immutable business references and controlled field catalogue | UPD-01, UPD-02, UPD-03 | UNIT / CONTRACT / DB_DEPENDENT | Prospective; BO2 subclauses remain open |
| Lifecycle/effectivity/successor rules | LCY-01 through LCY-05 | CONTRACT / DB_DEPENDENT | Prospective; exact policy matrix required |
| Role, approval and technical/business separation | UPD-04, AUD-01 through AUD-06 | MOCK / DB_DEPENDENT | Prospective; BO1/BO4 bindings held |
| Audit/provenance and safe readback | UPD-01, UPD-05, AUD-05, AUD-06, UI-07 | DB_DEPENDENT / E2E | Prospective; retention/readback owner unresolved |
| Idempotency and canonical request fingerprint | CRE-08, CRE-09, NEG-06 | UNIT / DB_DEPENDENT | Contract design covered; persistence owner conditional |
| Optimistic concurrency | UPD-03, NEG-03 through NEG-05 | UNIT / DB_DEPENDENT | Prospective; row-version persistence required |
| FK, locality and cycle safety | CRE-05, CRE-06, NEG-01, NEG-02 | UNIT / DB_DEPENDENT | Prospective; target fixture/reset required |
| UI design mode: full-page Create | UI-02 | MOCK / E2E | Covered by Engineering D v002; implementation/execution not authorized |
| UI design mode: right-side drawer simple Edit | UI-03 | MOCK / E2E | Covered by Engineering D v002; field catalogue/API implementation pending |
| UI escalation for complex operations | UI-04, UI-05 | MOCK / E2E | Covered by Engineering D v002; complex-operation policy and implementation pending |
| Unauthorized action visibility and rejection | UI-06, AUD-01 | CONTRACT / MOCK / E2E | Covered by Engineering D v002; server/UI authorization binding pending |
| Validation and stale-version conflict | UI-03, UI-07, UPD-03 | CONTRACT / MOCK / E2E | Covered by Engineering D v002; row-version contract remains conditional |
| Responsive/accessibility | UI-01, UI-08 | STATIC / E2E | Covered by Engineering D v002; implementation execution not authorized |
| Traditional Chinese / translation-ready structure | UI-09 | STATIC / MOCK / E2E | Covered by Engineering D v002; translation resource contract pending |
| UI style and remaining state coverage | UI-01 through UI-10 | STATIC / MOCK / E2E | `PASS_WITH_CONDITIONS`: Engineering D v002 is attributable and exact-hash verified; owner/policy/implementation/execution gates remain open |
| Rollback/reset/rebuild and evidence custody | GET-10, DB package design, all DB cases | STATIC / DB_DEPENDENT | Design only; no runtime action authorized |

## Classification summary

- `UNIT`: CRE-01/02/03/04/08/09, UPD-01/02/03, LCY-05, NEG-01/02/07.
- `CONTRACT`: GET-01/02/04/05/06/07, CRE-07, UPD-01/04, LCY-01/05, NEG-07/08, UI-01/05.
- `STATIC`: GET-08/09, NEG-07, UI-06, source/route/migration/custody checks.
- `MOCK`: CRE-01/04/07/08/09, UPD-04, AUD-01/02/03/04, UI-02/03/04/05/07.
- `NON_DB`: local synthetic rule and contract checks only; no current execution claim.
- `DB_DEPENDENT`: all target schema, FK, transaction, audit, version, concurrency, restart and permission cases.
- `E2E`: UI/API/audit flows only after UI artifact, implementation, target and owner acceptance.

## Known gaps / re-entry predicates

1. BO1 stewardship and mutation-service binding must be resolved.
2. BO4 role grants, approval thresholds, separation, audit retention and readback must be resolved.
3. Engineering D v002 is now attributable and exact-hash verified; BO5/UI owner acceptance, field-level policy and implementation authorization remain required for UI execution.
4. Exact row-version, idempotency, audit and evidence persistence contract must be admitted.
5. Named non-Production DB target, fixture/reset authority, least-privilege credentials and remote engineer/host binding must be separately authorized.

