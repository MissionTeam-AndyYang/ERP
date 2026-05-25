# ERP Purchasing API Field Readiness

Date: 2026-05-25
Scope: Frontend field-readiness notes for `GET /api/v1/purchasing/dashboard`.

## Current Frontend Contract

The current page consumes `PurchasingDashboardData` from `src/types/purchasing.ts` through `usePurchasingDashboard`.

Expected top-level shape:

```ts
{
  summary: PurchasingSummary[];
  records: PurchasingRecord[];
}
```

## Required Field Groups

| Frontend area | Required fields | API spec mapping |
| --- | --- | --- |
| KPI strip | summary label/value/hint/tone | `summary.openPurchaseOrderCount`, `lateArrivalCount`, `supplierQuotePendingCount`, `contractCoverageRate`, `priceVarianceRiskCount` |
| Main table | record id, supplier, material, quantity/unit, expected arrival, status, risk, owner | `purchaseOrders[]`, `supplierQuotes[]`, `supplierContracts[]`, `arrivalRisks[]`, `priceVarianceSignals[]` |
| Quote/contract context | quote no, contract no, valid date, price, currency | `supplierQuotes[]`, `supplierContracts[]` |
| Receiving context | ordered quantity, received quantity, arrival status | `purchaseOrders[]`, `receipts[]` |
| Detail panel | owner, related planning/work-order/RD reference, risk reason, workflow | Aggregated dashboard fields plus detail endpoint fields |
| Search | PO/quote/contract id, supplier, material, owner, status, risk reason | Should be supported frontend-side first; server-side filters can follow once field names stabilize. |

## API Readiness Notes

| Topic | Status | Note |
| --- | --- | --- |
| Read-only dashboard | Ready for integration | The UI is already wired through the service hook and can accept one aggregated dashboard response. |
| Mutation actions | Deferred | Header action only changes view; no create/update mutation is implied in V1. |
| Empty arrays | Needs confirmation | Current hook uses mock fallback. Once backend can intentionally return empty arrays, frontend should distinguish empty from unavailable. |
| Status vocabulary | Needs confirmation | Backend should confirm purchase, quote, contract, receiving and price-variance status values. |
| Supplier/customer split | Needs confirmation | API spec flags quotation and contract source ambiguity. Frontend needs supplier-side filtering. |

## Backend Questions

1. Can `/api/v1/quotation` and `/api/v1/contract` reliably return supplier-side records only?
2. Are purchase requests available separately from purchase orders?
3. Which field is canonical for expected arrival and late-arrival risk?
4. Which status values represent ordered, partially received, received, delayed and cancelled?
5. Which source supplies current material price for variance checks?
