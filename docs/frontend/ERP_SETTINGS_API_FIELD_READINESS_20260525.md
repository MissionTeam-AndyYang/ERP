# ERP Settings API Field Readiness

Date: 2026-05-25
Scope: Frontend field-readiness notes for `GET /api/v1/settings/dashboard`.

## Current Frontend Contract

The current page consumes `SettingsDashboardData` from `src/types/settings.ts` through `useSettingsDashboard`.

Expected top-level shape:

```ts
{
  summary: SettingsSummary[];
  items: MasterDataItem[];
}
```

## Required Field Groups

| Frontend area | Required fields | API spec mapping |
| --- | --- | --- |
| KPI strip | summary label/value/hint/tone | `summary.masterDataIssueCount`, `permissionRoleCount`, `integrationIssueCount`, `localizationCoverageRate` |
| Settings table | item id, name, domain, status, affected workspaces, risk, owner, last updated | `masterDataHealth[]`, `permissionRoles[]`, `integrationStatus[]`, `localizationStatus[]` |
| Permission view | role/module permission status and risk | `permissionRoles[]` |
| Integration view | database/API/PDA/device/external system readiness | `integrationStatus[]`, existing device/company endpoints |
| Localization view | language coverage and terminology consistency | `localizationStatus[]` |
| Search | item/domain/status/risk/owner/workspace/update date | Should be supported frontend-side first; server-side filters can follow once field names stabilize. |

## API Readiness Notes

| Topic | Status | Note |
| --- | --- | --- |
| Read-only dashboard | Ready for integration | The UI is wired through the service hook and can accept one aggregated dashboard response. |
| Mutation actions | Deferred | Header action only changes view; no settings mutation is implied in V1. |
| Empty arrays | Needs confirmation | Current hook uses mock fallback. Once backend can intentionally return empty arrays, frontend should distinguish empty from unavailable. |
| Permission model | Needs confirmation | API spec notes role and localization endpoints were not obvious in backend routes. |
| Domain vocabulary | Needs confirmation | Frontend needs stable master-data domain names for filtering. |

## Backend Questions

1. Are roles and permissions already stored in the database?
2. Does user login return role/module permission data?
3. Where should localization coverage be stored?
4. Which master data domains are mandatory for V1 integration?
