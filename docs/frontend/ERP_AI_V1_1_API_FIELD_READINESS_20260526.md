# ERP AI V1.1 API Field Readiness

Date: 2026-05-26
Scope: Frontend API readiness notes for AI V1.1 today work status visibility.

## Purpose

This document bridges the implemented AI V1.1 frontend with a future backend read endpoint.

AI V1.1 is intentionally read-only. It presents today's cross-module work status and already-delayed items. It does not generate recovery plans, execute ERP actions or mutate operational records.

## Endpoint

Recommended endpoint:

```txt
GET /api/v1/ai/dashboard
```

Current frontend hook:

```txt
useSupportDashboard("/api/v1/ai/dashboard", aiDashboardMock, "AI API unavailable")
```

The frontend currently accepts:

1. A raw payload.
2. A `{ data: ... }` envelope.
3. Mock fallback if the API is unavailable.

## V1.1 Response Shape

Recommended minimum response:

```ts
type AiDashboardV11Response = {
  kpis: AiKpi[];
  todayWorkItems: AiTodayWorkItem[];
};

type AiKpi = {
  label: string;
  value: string;
  hint: string;
  tone: "success" | "warning" | "danger" | "info" | "neutral";
};

type AiTodayWorkItem = {
  workItemId: string;
  module: AiWorkModule;
  title: string;
  customerOrTarget: string;
  plannedTime: string;
  currentStatus: string;
  progressState: "normal" | "inProgress" | "attention" | "delayed";
  progressLabel: string;
  tone: "success" | "warning" | "danger" | "info" | "neutral";
  delayMinutes: number;
  reasonSummary: string;
  impactSummary: string;
  ownerArea: string;
  sourceRecords: AiSourceRecord[];
};

type AiSourceRecord = {
  id: string;
  module: AiWorkModule | string;
  detail: string;
};

type AiWorkModule =
  | "Orders"
  | "Purchasing"
  | "Warehouse"
  | "Production"
  | "Quality"
  | "Logistics"
  | "Documents"
  | "Finance"
  | "Planning"
  | "BOM"
  | "Batches"
  | "Items"
  | "R&D";
```

## Required Fields

| Field | Required | Frontend use |
| --- | --- | --- |
| `kpis` | Yes | KPI strip. Missing array falls back to mock data in current generic support hook. |
| `todayWorkItems` | Yes | Work list, delayed focus, selected detail and search. |
| `workItemId` | Yes | Primary display id and selected-row key. |
| `module` | Yes | Module label, search and source context. |
| `title` | Yes | Main work item label. |
| `customerOrTarget` | Yes | Customer, line, warehouse, supplier or department target. |
| `plannedTime` | Yes | Displayed expected milestone time. |
| `currentStatus` | Yes | Current operational state. |
| `progressState` | Yes | Sort order and delayed/attention/in-progress grouping. |
| `progressLabel` | Yes | Display badge text. |
| `tone` | Yes | Display badge color. |
| `delayMinutes` | Yes | Delayed focus and time-difference display. Use `0` when not delayed. |
| `reasonSummary` | Yes | Short V1.1 reason summary. Not full root-cause analysis. |
| `impactSummary` | Yes | Downstream impact summary. |
| `ownerArea` | Yes | Responsible area for follow-up. |
| `sourceRecords` | Yes | Evidence/source record list. May be an empty array if no related records exist. |

## Progress State Mapping

| `progressState` | Display label | Tone | Meaning |
| --- | --- | --- | --- |
| `normal` | `正常` | `success` or `neutral` | Work is on track and does not need manager attention. |
| `inProgress` | `進行中` | `info` | Work is moving and not currently blocked. |
| `attention` | `注意` | `warning` | Work is not late yet but has risk or needs follow-up. |
| `delayed` | `已落後` | `danger` | Work is behind expected time or milestone. |

Frontend sort order:

```txt
delayed -> attention -> inProgress -> normal
```

When items have the same `progressState`, higher `delayMinutes` appears first.

## Source Record Expectations

`sourceRecords` should contain the records used to explain why the work item is visible on the AI page.

Examples:

| Module | Example id | Detail example |
| --- | --- | --- |
| Warehouse | `RM240506-CORN` | Available inventory 180 kg. |
| Purchasing | `PO-240508-014` | Supplier ETA 17:30. |
| Planning | `APS-B2-1610` | Original schedule 16:20. |
| Quality | `QC-240512-018` | QA release pending. |
| Logistics | `SH-240512-08` | 18:00 dispatch schedule. |
| Batches | `B240512-A101` | Finished batch awaiting QA release. |
| Documents | `COA-240512-011` | COA pending confirmation. |

## V1.1 Boundary

Allowed:

- Return today work item visibility.
- Return delayed item summaries.
- Return source records that support the display.
- Return display-ready labels while backend status codes are still stabilizing.
- Return empty arrays as valid data.

Not required for V1.1:

- Recovery plan generation.
- Recommended steps.
- Expected recovered time.
- Risk reduction score.
- Confidence score.
- AI audit trail.
- Mutation links or executable action payloads.
- Chat messages.

Deferred:

| Phase | Deferred fields |
| --- | --- |
| V1.2 delayed reason analysis | `reasonCategory`, `rootCause`, `blockerType`, `confidence`, richer evidence metadata. |
| V1.3 recovery planning | `recoverySteps`, `estimatedRecoveredTime`, `riskReduction`, `planConfidence`, `reviewStatus`, `auditTrail`. |
| V2 executable actions | Mutation endpoint ids, permission checks, action payloads and audit records. |

## Backend Confirmation Questions

| Question | Why it matters |
| --- | --- |
| Should AI V1.1 aggregate from existing dashboard/module endpoints or from a dedicated backend service? | Determines whether `/api/v1/ai/dashboard` is an aggregator or a stored AI signal endpoint. |
| Which module names should be canonical? | Keeps search, filters and source records stable. |
| Should `plannedTime` be ISO timestamp, local datetime or display-ready string? | Frontend can display all, but contract should be consistent. |
| Should `progressLabel` be returned by backend or mapped by frontend from `progressState`? | Backend-owned labels reduce frontend mapping; frontend-owned labels ease i18n later. |
| Is `delayMinutes` always non-negative? | Frontend currently treats `0` as not delayed. |
| Can `sourceRecords` include external document ids or only ERP primary keys? | Determines traceability and future drill-down behavior. |
| Can this endpoint intentionally return an empty `todayWorkItems` array? | Frontend will show empty state and should not refill mock data if API is valid. |

## Frontend Integration Notes

- The current page uses local mock data and generic support fallback.
- A dedicated service/type file can be added when backend implements the endpoint.
- The existing search is local and covers all visible work item/source fields.
- Server-side filters should wait until field names and canonical module/status values are stable.
- The page is suitable for read-only API integration once `kpis` and `todayWorkItems` are confirmed.

## Decision

```txt
ai_v1_1_api_field_readiness_created
```

The frontend is ready for a read-only AI V1.1 dashboard endpoint focused on today's work status and delayed item visibility. Recovery planning remains outside this contract.
