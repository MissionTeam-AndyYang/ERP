# ERP Workforce API Field Readiness

Date: 2026-05-25
Scope: Frontend field-readiness notes for `GET /api/v1/workforce/dashboard`.

## Current Frontend Contract

The current page consumes `WorkforceDashboardData` from `src/types/workforce.ts` through `useWorkforceDashboard`.

Expected top-level shape:

```ts
{
  summary: WorkforceSummary[];
  cases: WorkforceCase[];
}
```

## Required Field Groups

| Frontend area | Required fields | API spec mapping |
| --- | --- | --- |
| KPI strip | summary label/value/hint/tone | `summary.shiftCoverageRate`, `skillGapCount`, `certificationRiskCount`, `overtimeHours`, `supportNeededCount` |
| Workforce table | case id, department, line/area, shift, related plan/work order, required/assigned staff, skill, certification, risk, owner | `shiftCoverage[]`, `lineStaffReadiness[]`, `skillGaps[]`, `certificationRisks[]` |
| Overtime/support | overtime hours, support needed, support reason | `overtimePlans[]`, `lineStaffReadiness[]` |
| Detail panel | requirement breakdown by production/warehouse/quality/logistics area | Aggregated dashboard fields plus detail endpoint fields |
| Search | line/area/department/shift/plan/work-order/skill/certification/owner/risk | Should be supported frontend-side first; server-side filters can follow once field names stabilize. |

## API Readiness Notes

| Topic | Status | Note |
| --- | --- | --- |
| Read-only dashboard | Ready for integration | The UI is wired through the service hook and can accept one aggregated dashboard response. |
| Mutation actions | Deferred | Header action only changes view; no shift assignment mutation is implied in V1. |
| Empty arrays | Needs confirmation | Current hook uses mock fallback. Once backend can intentionally return empty arrays, frontend should distinguish empty from unavailable. |
| Employee/skill tables | Needs confirmation | API spec notes dedicated employee/skill/certification endpoints were not observed. |
| Gap calculation | Needs confirmation | Frontend needs canonical required versus assigned headcount and missing skill logic. |

## Backend Questions

1. Does the current DB include employee, skill and certification tables?
2. Can work assignment represent planned staff by line/date?
3. How should staff gaps be calculated for Planning / APS and Production?
4. Which workforce data is V1 read-only and which needs later mutation?
