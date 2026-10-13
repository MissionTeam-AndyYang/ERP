# ERP2.0 Milestone 2 Organization Operating Defect Backlog Registration

**Artifact ID:** `ERP2-M2-ORG-DEFECT-BACKLOG-REGISTRATION-20261013-001`

**Knowledge Reference:** `ERP2-KNOWLEDGE:ERP2-M2-ORG-DEFECT-BACKLOG-REGISTRATION-20261013-001`

**Authority:** CIO Governance / backlog registration only

**Scope:** R2 — AI Office / Organization Orchestration

## Parent Linkage

- Intended parent: existing `Milestone 2 / R2 — AI Office / Organization Orchestration` backlog.
- Existing runtime state: `O1 M3 = BLOCKED / SUSPENDED`.
- Formal O3 identifier: `UNRESOLVED / NOT LOCATED IN CURRENT REPOSITORY INDEX`.
- Registration classification: `MILESTONE 2 BACKLOG CANDIDATE; PARENT MAPPING UNRESOLVED`.
- No new organizational baseline, Parent, Gate, WorkItem, authority, or runtime activation is created.

## Registered Defects

Each entry retains the required remediation fields. Current state is informational registration only; proposed correction and acceptance test remain future CI/CIO work.

| ID | Priority | Observed failure / evidence | Impact / risk | Functional owner | Proposed correction | Objective acceptance test | Runtime dependency | Authorization state |
|---|---:|---|---|---|---|---|---|---|
| `M2-ORG-01` | P0 | Wrong or stale cross-Office response accepted against the current task. | Correlation and decision integrity risk. | CTO / Repository / PMO coordination | Require exact Correlation + Commit + Artifact matching before acceptance. | Deliberately stale response is rejected and correct response is accepted. | Organization runtime authority required for automated enforcement. | Backlog only; no activation. |
| `M2-ORG-02` | P0 | Dispatch, receipt, acceptance, execution, callback and terminal-result states are incomplete. | Work may appear complete without terminal evidence. | PMO / CTO / Repository | Define durable lifecycle state and terminal-result record. | One work item can be reconstructed end-to-end from durable records. | Organization runtime authority. | Backlog only; no activation. |
| `M2-ORG-03` | P0 | Fresh Engineering Task/Executor binding and actual execution provenance are inconsistent. | Authorship and execution accountability risk. | CTO / Engineering / PMO | Bind task, executor, capability, timestamps and result evidence. | Readback identifies who executed what, when, and against which task. | Organization runtime authority. | Backlog only; no activation. |
| `M2-ORG-04` | P0 | Custody Receipt PASS is not distinguished from original-artifact, central-Git or remote-engineer retrieval. | False custody/readiness conclusion. | Repository / CTO | Separate custody, content readback, Git readback and remote retrieval states. | Each result reports the exact verified surface and unresolved surfaces. | Organization runtime authority. | Backlog only; no activation. |
| `M2-ORG-05` | P1 | Independent TEST assignment, chronology and return metadata are incomplete. | Validation lineage and defect chronology risk. | TEST / CTO / Repository | Require durable assignment, result, chronology and return metadata. | Independent result can be traced to assignment and source state. | Organization runtime authority. | Backlog only; no activation. |
| `M2-ORG-06` | P1 | Direct Office relay failure and manual fallback lack reliable recovery/correlation controls. | Lost, duplicated or misrouted messages. | CTO / PMO / Repository | Add correlation-preserving fallback and explicit transport error states. | Failed direct delivery produces one attributable fallback and no duplicate task. | Organization runtime authority. | Backlog only; no activation. |
| `M2-ORG-07` | P1 | Cross-product authoritative Git source registry and ownership discovery incomplete. | Source-of-truth and lineage ambiguity. | CTO / Engineering / Repository | Maintain authoritative source registry with owner, commit, branch and status. | A source candidate resolves to one registered owner and Git identity. | Organization runtime authority. | Backlog only; no activation. |
| `M2-ORG-08` | P1 | Repeated governance re-entry occurs instead of bounded conditional execution. | Delivery delay and governance burden. | CIO / CTO / PMO | Use explicit conditions, stop rules and bounded continuation semantics. | Satisfied conditions permit continuation without duplicate authorization. | CIO/CTO governance review; runtime not implied. | Backlog only; no activation. |
| `M2-ORG-09` | P1 | Per-work-item ownership, timestamps, ageing, next action, exception and escalation visibility incomplete. | Stale work and escalation blind spots. | PMO / CTO / Repository | Require a durable work visibility record with ageing and next-action fields. | Current owner, age, next action and exception state are queryable. | Organization runtime authority. | Backlog only; no activation. |

## Preserved Incident Evidence

The cross-Office return-correlation defect is preserved without overwriting either custody record:

- Requested correlation: `FM02-CENTRAL-SOURCE-COMPLETION-20261013-001`.
- Correct current commit: `41e070a58c668505b91e5bcece778a87fc9725c5`.
- Incorrectly returned historical Sprint-01 commit: `aca980b0c2c300ac653ac1b72a6d038ed65bd4af`.
- Current receipt: `ERP2-KNOWLEDGE:ERP2-FM02-ENGINEERING-SOURCE-COMPLETION-CUSTODY-20261013-001`.
- Historical receipt: `ERP2-KNOWLEDGE:ERP2-FM02-SPRINT01-REPOSITORY-CUSTODY-20261013-001`.

## Boundaries

This registration does not authorize O3/O1 M3 reactivation, routing, callbacks, Message Bus changes, Track F implementation, Office authority modification, Product code changes, FM-02 C2/C3, or new organization-runtime engineering. Existing blocked/suspended work remains blocked/suspended.

**Registration status:** `REGISTERED AS MILESTONE 2 BACKLOG CANDIDATE / PARENT MAPPING UNRESOLVED / READBACK READY`
