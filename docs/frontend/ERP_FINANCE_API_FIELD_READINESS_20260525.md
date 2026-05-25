# ERP Finance API Field Readiness

Date: 2026-05-25
Scope: Frontend field-readiness notes for `GET /api/v1/finance/dashboard`.

## Current Frontend Contract

The current page consumes `FinanceDashboardData` from `src/types/finance.ts` through `useFinanceDashboard`.

Expected top-level shape:

```ts
{
  summary: FinanceSummary[];
  cases: FinanceOrderCase[];
}
```

## Required Field Groups

| Frontend area | Required fields | API spec mapping |
| --- | --- | --- |
| KPI strip | summary label/value/hint/tone | `summary.estimatedMarginRate`, `actualMarginRate`, `marginRiskCount`, `billingReadyAmount`, `arOutstandingAmount`, `apUpcomingAmount` |
| Finance table | finance case id, order no, shipment no, customer, product, order amount, cost, margin, AR status, POD, risk, owner | `marginByOrder[]`, `billingReadiness[]`, `arSignals[]` |
| Cost variance | estimated cost, actual cost, margin variance, material/AP, inventory, production and logistics cost impacts | `costVariance[]`, `apSignals[]` |
| Billing readiness | invoice no, AR status, POD status, document readiness, due date, collected amount | `billingReadiness[]`, `arSignals[]` |
| Detail panel | finance documents, workflow, risk reason and owners | Aggregated dashboard fields plus detail endpoint fields |
| Search | order/case/shipment/customer/product/invoice/status/owner/risk | Should be supported frontend-side first; server-side filters can follow once field names stabilize. |

## API Readiness Notes

| Topic | Status | Note |
| --- | --- | --- |
| Read-only dashboard | Ready for integration | The UI is wired through the service hook and can accept one aggregated dashboard response. |
| Mutation actions | Deferred | Header action only changes view; no invoice or payment mutation is implied in V1. |
| Empty arrays | Needs confirmation | Current hook uses mock fallback. Once backend can intentionally return empty arrays, frontend should distinguish empty from unavailable. |
| Actual cost | Needs confirmation | Frontend can display `null` as not settled, but backend must define when actual cost becomes reliable. |
| Billing-ready rule | Needs confirmation | API spec asks whether POD is required before billing-ready. |

## Backend Questions

1. Which endpoint is source of truth for AR and AP?
2. Can order-level actual cost be calculated today, and at what lifecycle stage?
3. Is POD required before billing-ready?
4. Which cost components are available now: material, labor, overhead and logistics?
5. Is estimated margin stored directly or calculated from quotation, BOM and purchase price?
