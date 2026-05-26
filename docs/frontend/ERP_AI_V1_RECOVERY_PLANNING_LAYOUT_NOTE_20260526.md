# ERP AI V1 Recovery Planning Layout Note

Date: 2026-05-26
Scope: AI Center information architecture before frontend code refinement.

## Accepted Direction

```txt
AI V1 = read-only insights + recovery planning assist.
```

AI should identify late or at-risk progress across orders, production, purchasing, quality, logistics, workforce, documents and finance, then propose a recovery plan with reasons, affected modules, expected recovered time, risk reduction and confidence.

AI must not directly execute ERP mutations in V1.

## Page Role

The AI Center should not be a chat-only assistant and should not become a hidden automation console. Its V1 role is a cross-module recovery-planning workspace that helps managers answer:

1. What is late or likely to become late?
2. Why is it late?
3. Which modules or records are causing the delay?
4. What recovery plan is recommended?
5. How confident is the recommendation, and what evidence supports it?
6. What should a supervisor review next?

## Recommended First View

| Zone | Purpose | UI Pattern |
| --- | --- | --- |
| KPI strip | Show late items, high-risk recommendations, recovered-time opportunity and pending supervisor reviews. | Existing `ModuleKpiCard` pattern. |
| Late progress queue | Main work area for orders, work orders, arrivals, QA release, shipment, documents or billing items that are behind or at risk. | Dense list or table after API fields exist. |
| Selected recovery plan | Shows root cause, recommended steps, affected modules, estimated recovered time, risk reduction and confidence. | Detail panel or card stack. |
| Evidence | Source records and signals behind the recommendation. | Compact source list with record ids and module labels. |
| Supervisor review | Read-only review state and next review owner. | Status badges and notes, not action buttons that mutate ERP data. |

## Suggested Data Shape

These names are frontend planning terms, not final backend contract names.

| Field | Meaning |
| --- | --- |
| `recommendationId` | Stable AI recommendation id. |
| `targetRecord` | Main order/work order/shipment/etc. affected. |
| `riskLevel` | Accepted risk vocabulary: `正常`, `注意`, `高風險`. |
| `latenessStatus` | Current delay state, such as behind schedule or at risk. |
| `rootCause` | Human-readable reason summary. |
| `affectedModules` | Modules involved in the issue. |
| `recoverySteps` | Read-only recommended plan steps. |
| `estimatedRecoveredTime` | Expected improvement if supervisor follows the plan. |
| `riskReduction` | Expected risk reduction or impact statement. |
| `confidence` | AI confidence score or band. |
| `evidence` | Source records and signals used by AI. |
| `reviewStatus` | Read-only state, such as pending review, read or tracking. |

## V1 UI Wording

Use language that makes AI helpful but not authoritative:

| Avoid | Prefer |
| --- | --- |
| `自動執行` | `建議處理計畫` |
| `立即派工` | `建議調整派工` |
| `自動改交期` | `建議重新確認交期` |
| `已解決` | `待主管確認` |
| `AI 決策` | `AI 建議` |

## Action Boundary

Allowed in V1:

- Search or filter recommendations.
- Review late/at-risk items.
- View root cause and evidence.
- View suggested recovery plan.
- Mark CTA labels as review/navigation only if needed.

Not allowed in V1 unless backend mutation contracts exist:

- Create purchase order.
- Reschedule production.
- Release or block quality result.
- Dispatch shipment.
- Change customer promise date.
- Create invoice or payment record.
- Update master data.

## Recommended Code Step

Before changing `src/app/ai/page.tsx`, decide whether the first implementation should be:

| Option | Benefit | Risk |
| --- | --- | --- |
| Search + empty states only | Matches Items/BOM/Batches low-risk pattern. | Does not yet express recovery-planning value. |
| Static recovery-planning mock layout | Makes the accepted AI direction visible now. | More subjective layout decisions before API contract. |
| Wait for API fields | Avoids churn. | AI page remains less aligned with accepted direction. |

Recommended next code step:

```txt
Add search + empty states only if we want consistency across support pages now.
Wait on larger AI layout changes until the recovery-plan data shape is accepted.
```

## Decision

```txt
ai_recovery_planning_layout_note_created
```

This note gives the next AI frontend pass a clear boundary: read-only recovery planning, not autonomous ERP execution.
