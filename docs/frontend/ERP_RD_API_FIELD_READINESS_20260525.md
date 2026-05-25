# ERP R&D API Field Readiness

Date: 2026-05-25
Scope: Frontend field-readiness notes for `GET /api/v1/rd/dashboard`.

## Current Frontend Contract

The current page consumes `RdDashboardData` from `src/types/rd.ts` through `useRdDashboard`.

Expected top-level shape:

```ts
{
  summary: RdSummary[];
  projects: RdProject[];
}
```

## Required Field Groups

| Frontend area | Required fields | API spec mapping |
| --- | --- | --- |
| KPI strip | summary label/value/hint/tone | `summary.activeDevelopmentCount`, `samplePendingCount`, `costingPendingCount`, `nutritionLabelPendingCount`, `readyForQuotationCount` |
| Project table | project id, customer, product, channel, stage, decision, priority, owner, launch/sample dates | `developmentProjects[]`, `sampleTasks[]` |
| BOM context | BOM no, version, status, transfer readiness | `bomVersions[]` |
| Costing context | target price, suggested quote, minimum quote, target/estimated margin, unit cost, cost components and loss rate | `costingCases[]`, `bomVersions[]` |
| Detail panel | cost lines, workflow, quotation judgment and owner | Aggregated dashboard fields plus detail endpoint fields |
| Search | project/customer/product/channel/BOM/stage/decision/owner/risk notes | Should be supported frontend-side first; server-side filters can follow once field names stabilize. |

## API Readiness Notes

| Topic | Status | Note |
| --- | --- | --- |
| Read-only dashboard | Ready for integration | The UI is wired through the service hook and can accept one aggregated dashboard response. |
| Mutation actions | Deferred | Header action only changes view; no quote creation or BOM approval mutation is implied in V1. |
| Empty arrays | Needs confirmation | Current hook uses mock fallback. Once backend can intentionally return empty arrays, frontend should distinguish empty from unavailable. |
| R&D source table | Needs confirmation | API spec notes no explicit R&D endpoint was observed. |
| BOM version semantics | Needs confirmation | Frontend needs development, trial, quotation and production version states. |

## Backend Questions

1. Is there an existing table for development requests/projects?
2. Can BOM distinguish development version from approved production BOM?
3. Where should nutrition label status be stored?
4. How should sample delivery status connect to Sales/Orders?
5. Can supplier quote data be linked to costing cases?
