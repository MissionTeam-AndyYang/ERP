# ERP2.0 Module Closure Sync Template / Checklist

**Template ID:** `ERP2.0-MODULE-CLOSURE-SYNC-TEMPLATE-CHECKLIST-20261018-006`
**Status:** `REUSABLE BOUNDED OPERATING TEMPLATE`
**Owner:** Program Management Office
**Date:** 2026-10-18 (Asia/Taipei)

## 1. Required Traceability Chain

Every module closure must trace the following chain without skipping a stage:

`Milestone → Sprint → Backlog → Assignment → Delivery Evidence → TEST → Acceptance → PM Closure → Git Remote → Knowledge Readback`

| Stage | Required identity / evidence | Accountable Office | PASS condition | HOLD condition |
|---|---|---|---|---|
| Milestone | Milestone ID, scope, entry/exit boundary | PMO | Scope and gate are explicit | Scope or gate is inferred |
| Sprint | Sprint ID, authorized work and exclusions | PMO / CTO | Sprint authorization and boundary are recorded | Planning candidate is treated as active |
| Backlog | WorkItem/Backlog ID, dependency and owner | PMO / Business Owner | Item is attributable and dispositioned | No owner, duplicate or stale item |
| Assignment | Assignment, capability, executor acceptance and target | CTO | Current assignment and executor are evidenced | Historical or role-only assignment |
| Delivery Evidence | Branch/commit/tree/path and artifact hash | Engineering / Repository | Source and artifact identity read back | Hash-only, missing source or wrong target |
| TEST | Case/run ID, environment, verdict and limitation | TEST / CTO | Actual independent result is attributable | Package custody only, not execution |
| Acceptance | Business/technical acceptance authority and decision | Business Owner / CTO / CIO as applicable | Correct authority accepts exact scope | `READY`, `CUSTODY`, or mock PASS is substituted |
| PM Closure | Current report, conditions and deferred obligations | PMO | Closure record consumes verified child results | Child delivery is mistaken for closure |
| Git Remote | Remote repo, branch, commit/tree/blob and authorized route | Repository Office | Remote readback confirms exact artifact | Local file or proposed branch only |
| Knowledge Readback | Knowledge ID/URI, index locator, version and status | Repository Office | Index readback matches identity/hash/status | Registration is asserted without readback |

## 2. Status Vocabulary

Use only evidence-supported values:

- `PLANNED`, `READY`, `DISPATCHED`, `IN_PROGRESS`, `WAITING_RETURN`;
- `COMPLETE WITH CONDITIONS`, `CUSTODY VERIFIED`, `PASS WITH CONDITIONS`;
- `NOT VERIFIED`, `BLOCKED`, `HELD`, `NOT EXECUTED`, `RESTRICTED`;
- `EFFECTIVE` only when the authorized decision and administrative registration are both recorded;
- `REMOTE READBACK PASS` only when the remote state was actually read back.

## 3. Closure Checklist

- [ ] Parent module, milestone and Sprint are identified.
- [ ] All WorkItems have unique identities and current states.
- [ ] Assignment and executor binding are current and attributable.
- [ ] Delivery source, artifact hashes and scope are read back.
- [ ] Independent TEST result is separated from custody/readiness.
- [ ] Defects and retests are linked to the exact result.
- [ ] Business and technical acceptance authority is explicit.
- [ ] PM closure report lists conditions and deferred obligations.
- [ ] Git remote commit/tree/blob are independently read back.
- [ ] Knowledge Index ID/URI/version/hash are read back.
- [ ] Product main merge, DB/runtime, release and Production boundaries are explicit.
- [ ] Historical records are preserved; corrections are additive.

## 4. Required Final Status Record

```text
MODULE_CLOSURE = <COMPLETE / COMPLETE_WITH_CONDITIONS / HOLD>
DEV_DELIVERY = <status>
INDEPENDENT_TEST = <status and bounded scope>
BUSINESS_ACCEPTANCE = <status>
PM_CLOSURE = <status>
GIT_REMOTE_READBACK = <PASS / HOLD>
KNOWLEDGE_READBACK = <PASS / HOLD>
FORMAL_INTEGRATION = <status>
PRODUCT_MAIN_MERGE = <authorized status>
PRODUCTION_RELEASE = <authorized status>
DEFERRED_OBLIGATIONS = <list>
```

