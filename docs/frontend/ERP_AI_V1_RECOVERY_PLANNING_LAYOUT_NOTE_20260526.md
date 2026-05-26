# ERP AI V1 Planning Boundary Note

Date: 2026-05-26
Scope: AI Center planning boundary after owner discussion.

## Updated Direction

```txt
AI V1.1 = today work status visibility + delayed item presentation.
AI V1.2 = delayed reason analysis.
AI V1.3 = AI-assisted recovery planning.
```

AI should first make today's work status and already-delayed items clear. Recovery planning remains a follow-up phase after managers can trust the delay visibility layer.

AI must not directly execute ERP mutations in V1.

Primary V1.1 spec:

```txt
docs/frontend/ERP_AI_TODAY_WORK_STATUS_WORKSPACE_SPEC_20260526.md
```

## Page Role

The AI Center should not be a chat-only assistant and should not become a hidden automation console. Its V1.1 role is a cross-module work-status workspace that helps managers answer:

1. What is scheduled for today?
2. What is currently in progress?
3. What needs attention?
4. What is already delayed?
5. Which module or department owns the follow-up?
6. What downstream item may be affected?

## Recommended First View

| Zone | Purpose | UI Pattern |
| --- | --- | --- |
| KPI strip | Show today's work, in-progress items, attention items, delayed items and pending reviews. | Existing `ModuleKpiCard` pattern. |
| Today work list | Main work area for all cross-module work scheduled today. | Dense list/table or selected-detail workspace. |
| Delayed item focus | Present items already behind schedule. | Highlight delay state, responsible area and impact summary. |
| Selected work detail | Show source records, current state, blockers and timeline. | Detail panel or card stack. |
| Recovery planning placeholder | Record where future planning can appear. | Documented for V1.3; do not build full recovery plan UI in V1.1. |

## Suggested Data Shape

These names are frontend planning terms, not final backend contract names.

| Field | Meaning |
| --- | --- |
| `workItemId` | Stable work item id, such as order, work order, PO, QC, shipment or invoice readiness id. |
| `module` | Orders, Purchasing, Warehouse, Production, Quality, Logistics, Documents or Finance. |
| `title` | Human-readable work item title. |
| `targetRecord` | Main ERP record affected. |
| `plannedTime` | Expected completion or milestone time. |
| `currentStatus` | Current state in accepted V1 vocabulary. |
| `progressState` | Normal, in progress, attention or delayed. |
| `delayMinutes` | How far behind schedule, if already delayed. |
| `reasonSummary` | Short visible reason summary for V1.1. Full root-cause analysis belongs to V1.2. |
| `impactSummary` | Downstream impact summary. |
| `ownerArea` | Responsible team or role for follow-up. |
| `sourceRecords` | Related ERP records used to support the display. |
| `confidence` | Optional display only; should not be the focus in V1.1. |
| `recoverySteps` | Deferred to V1.3. |
| `estimatedRecoveredTime` | Deferred to V1.3. |
| `riskReduction` | Deferred to V1.3. |

## V1 UI Wording

Use language that makes AI visible and helpful, not authoritative:

| Avoid | Prefer |
| --- | --- |
| AI has processed | AI has flagged |
| Automatic recovery plan | Future suggested plan |
| Execute reschedule now | Production control review needed |
| Notify supplier now | Purchasing follow-up needed |
| AI decision | AI signal |

## Action Boundary

Allowed in V1.1:

- Search or filter today's work items.
- Review normal, attention and delayed items.
- View short reason summary and source records.
- View responsible area and downstream impact.
- Keep CTA labels review/navigation only if needed.

Not allowed in V1.1 unless backend mutation contracts exist:

- Create purchase order.
- Reschedule production.
- Release or block quality result.
- Dispatch shipment.
- Change customer promise date.
- Create invoice or payment record.
- Update master data.
- Generate or execute a full recovery plan.

## Recommended Code Step

Before changing `src/app/ai/page.tsx`, use the accepted V1.1 sequence:

| Step | Scope |
| --- | --- |
| 1 | Update mock data from generic AI insights to today work items and delayed item examples. |
| 2 | Shift layout emphasis from AI assistant tasks to today work status and delayed item review. |
| 3 | Keep recovery plan generation out of the visible V1.1 UI. |
| 4 | Preserve shared search and empty-state components. |

Recommended next code step:

```txt
Implement AI V1.1 today work status visibility first.
Defer recovery plan generation until V1.3 data shape and trust rules are accepted.
```

## Decision

```txt
ai_v1_1_today_work_status_first
```

This note now treats recovery planning as a future enhancement. The next AI frontend pass should focus on read-only today work visibility and delayed item presentation.
