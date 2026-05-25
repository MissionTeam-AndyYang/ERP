# ERP Traceability API Field Readiness

Date: 2026-05-25
Scope: Frontend field-readiness notes for `GET /api/v1/traceability/dashboard`.

## Current Frontend Contract

The current page consumes `TraceabilityDashboardData` from `src/types/traceability.ts` through `useTraceabilityDashboard`.

Expected top-level shape:

```ts
{
  summary: TraceSummary[];
  records: TraceRecord[];
}
```

## Required Field Groups

| Frontend area | Required fields | API spec mapping |
| --- | --- | --- |
| KPI strip | summary label/value/hint/tone | `summary.traceableBatchCount`, `documentMissingCount`, `recallRiskCount`, `openTraceInvestigations` |
| Trace table | query type/value, direction, item, batch, source type/document, work order, sales order, quantity/unit, impact scope, trace status | `recentTraceSearches[]`, `traceChain`, `recallCandidates[]` |
| Chain view | nodes with id, label, ref, status and tone | `traceChain.upstream`, `production`, `downstream` |
| Recall scope | impacted qty, unit, impacted customers/orders | `traceChain.recallScope`, `recallCandidates[]` |
| Documents | type, no, status, owner | `traceChain.documents`, `documentGaps[]` |
| Search | batch/item/order/work-order/supplier/customer/document/status/risk | Should be supported frontend-side first; server-side filters can follow once field names stabilize. |

## API Readiness Notes

| Topic | Status | Note |
| --- | --- | --- |
| Read-only dashboard | Ready for integration | The UI is wired through the service hook and can accept one aggregated dashboard response. |
| Mutation actions | Deferred | Header action only changes view; no corrective-action mutation is implied in V1. |
| Empty arrays | Needs confirmation | Current hook uses mock fallback. Once backend can intentionally return empty arrays, frontend should distinguish empty from unavailable. |
| Relationship depth | Needs confirmation | Frontend needs enough upstream/downstream nodes to explain the trace path. |
| Recall scope | Needs confirmation | API spec asks whether recall scope is stored or derived. |

## Backend Questions

1. Does `/api/v1/batchtrace/record` include both upstream and downstream relationships?
2. Can batch trace connect purchase receipt, work order, inventory and shipping order?
3. Where are required traceability documents stored?
4. Is recall scope calculated today or must it be derived by API aggregation?
