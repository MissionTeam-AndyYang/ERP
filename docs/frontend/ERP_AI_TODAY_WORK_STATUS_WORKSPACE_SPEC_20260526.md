# ERP AI Today Work Status Workspace Spec

Date: 2026-05-26
Scope: AI Center next-step UX direction after owner discussion.

## Accepted Direction

```txt
AI V1.1 = today work status visibility + delayed item presentation.
AI V1.2 = delayed reason analysis.
AI V1.3 = AI-assisted recovery planning.
```

The AI page should first help managers see today's work clearly. For items that are already behind schedule, V1.1 should present the delay state, impact and responsible area. Recovery plan generation should be added later after the delay visibility model is stable.

## Why This Direction

This is a better ERP rollout sequence than jumping directly to recovery planning:

1. Visibility is lower risk than recommendation.
2. It fits the accepted V1 read-only boundary.
3. It does not require mutation, scheduling or approval APIs.
4. It lets managers trust the data before trusting AI suggestions.
5. It creates a stable foundation for later root-cause analysis and recovery planning.

## Page Goal

The first screen should answer:

1. What is scheduled for today?
2. What is currently in progress?
3. What needs attention?
4. What is already delayed?
5. Which module or department is responsible for the delay?
6. What downstream work, shipment, document or billing item may be affected?

## Recommended Information Architecture

| Zone | Purpose | V1.1 Behavior |
| --- | --- | --- |
| KPI strip | Show today's work counts and delay pressure. | Read-only summary cards. |
| Search/filter | Find work by record id, module, customer, item, line, status or owner. | Existing support search pattern. |
| Today work list | Main work surface for all today items. | Sort by risk first: delayed, attention, in progress, normal. |
| Delayed items focus | Highlight items already behind schedule. | Present delay, reason summary, impact and owner. |
| Selected work detail | Show source records, status timeline and blockers. | Read-only panel or card stack. |
| Future recovery plan slot | Reserve conceptual space for later planning. | Documented only; do not build full plan UI yet. |

## Suggested V1.1 KPI Set

| KPI | Meaning |
| --- | --- |
| Today's work | Total cross-module work items scheduled today. |
| In progress | Items currently moving and not blocked. |
| Attention | Items at risk but not late yet. |
| Delayed | Items already behind expected time. |
| Pending review | Items that need manager review or department follow-up. |

## Today Work Item Fields

These are frontend planning terms, not final backend contract names.

| Field | Meaning |
| --- | --- |
| `workItemId` | Stable display id, such as order, work order, PO, QC, shipment or invoice readiness id. |
| `module` | Orders, Purchasing, Warehouse, Production, Quality, Logistics, Documents or Finance. |
| `title` | Human-readable work item name. |
| `customerOrTarget` | Customer, line, warehouse, supplier or department target. |
| `plannedTime` | Expected completion or milestone time. |
| `currentStatus` | Current state in accepted V1 vocabulary. |
| `progressState` | Normal, in progress, attention or delayed. |
| `delayMinutes` | How far behind schedule, if already delayed. |
| `reasonSummary` | Short visible reason, not full AI root-cause analysis yet. |
| `impactSummary` | Downstream impact such as shipment, production start, QA release or billing readiness. |
| `ownerArea` | Responsible team or role for follow-up. |
| `sourceRecords` | Related ERP records used to support the display. |

## V1.1 Status Language

Use operational visibility language:

| Concept | Recommended label |
| --- | --- |
| Normal | `正常` |
| In progress | `進行中` |
| Needs attention | `注意` |
| Delayed | `已落後` |
| Pending review | `待確認` |
| Blocked | `阻擋` |

Avoid wording that implies AI is executing actions:

| Avoid | Prefer |
| --- | --- |
| `AI 已處理` | `AI 已標示` |
| `自動恢復計畫` | `後續可加入建議計畫` |
| `立即調整排程` | `需生管確認` |
| `立即通知供應商` | `需採購追蹤` |

## Implementation Sequence

Recommended next frontend sequence:

1. Update AI page mock data from generic insights to today work items and delayed items.
2. Replace the current `ProcessBoard + insight cards + assistant task list` emphasis with a work-status list and selected detail pattern.
3. Keep search and empty states using the shared support components.
4. Keep all CTA behavior read-only or navigation-only.
5. Document recovery planning as a later phase, not a visible V1.1 promise.

## Deferred Phases

| Phase | Scope | Requirement |
| --- | --- | --- |
| V1.2 | Delayed reason analysis | Stable source records and reason categories. |
| V1.3 | AI-assisted recovery planning | Accepted data shape, confidence rule, evidence rule and audit trail. |
| V2 | Executable recovery actions | Mutation APIs, authorization and audit. |

## Decision

```txt
accepted_ai_v1_1_today_work_status_first
```

The next AI page refinement should prioritize today's work visibility and delayed-item presentation. Recovery planning remains a later enhancement after managers can clearly trust and review the delay data.
