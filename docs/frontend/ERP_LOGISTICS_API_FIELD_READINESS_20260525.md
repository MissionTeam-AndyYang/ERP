# ERP Logistics API Field Readiness

Date: 2026-05-25
Scope: Frontend field-readiness notes for `GET /api/v1/logistics/dashboard`.

## Current Frontend Contract

The current page consumes `LogisticsDashboardData` from `src/types/logistics.ts` through `useLogisticsDashboard`.

Expected top-level shape:

```ts
{
  summary: LogisticsSummary[];
  shipments: Shipment[];
}
```

## Required Field Groups

| Frontend area | Required fields | API spec mapping |
| --- | --- | --- |
| KPI strip | summary label/value/hint/tone | `summary.todayShipmentCount`, `readyToShipCount`, `blockedShipmentCount`, `podPendingCount`, `documentMissingCount` |
| Shipment table | shipment no, order no, customer, route, destination, product, batch, quantity/unit, requested arrival, planned departure, stage | `todayShipments[]` plus shipment detail fields |
| Dispatch risk | risk level, risk reason, owner module, blocking flag | `dispatchRisks[]` |
| Warehouse/quality readiness | warehouse outbound status, quality release status | `todayShipments[]`, warehouse outbound source, quality release source |
| Cold-chain context | temperature requirement, current temperature, temperature status, vehicle no, driver | `coldChainSignals[]`, `dispatch` detail |
| Documents/POD | documents ready, document list, POD status | `documentStatus[]`, `podStatus[]` |
| Search | shipment/order/customer/route/batch/vehicle/driver/owner/status/risk | Should be supported frontend-side first; server-side filters can follow once field names stabilize. |

## API Readiness Notes

| Topic | Status | Note |
| --- | --- | --- |
| Read-only dashboard | Ready for integration | The UI is wired through the service hook and can accept one aggregated dashboard response. |
| Mutation actions | Deferred | Header action only changes view; no dispatch mutation is implied in V1. |
| Empty arrays | Needs confirmation | Current hook uses mock fallback. Once backend can intentionally return empty arrays, frontend should distinguish empty from unavailable. |
| POD source | Needs confirmation | API spec currently asks where POD status is stored. |
| Cold-chain telemetry | Needs confirmation | Frontend needs temperature value and status, but backend source/thresholds are not confirmed. |

## Backend Questions

1. Where is POD status stored and what values should be exposed?
2. Does shipping order include vehicle and driver data, or should dispatch be joined from a separate source?
3. Where is cold-chain temperature recorded and how are normal/warning/abnormal statuses derived?
4. Which quality release and warehouse statuses block shipment?
5. Which logistics event makes Finance billing-ready?
