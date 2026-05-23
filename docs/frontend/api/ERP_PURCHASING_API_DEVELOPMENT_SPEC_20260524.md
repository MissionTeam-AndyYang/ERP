# ERP Purchasing API Development Spec

Date: 2026-05-24
Route: `/purchasing`
Purpose: Define read-only APIs for Purchasing V1.

## 1. V1 Goal

Purchasing covers two flows:

1. Pre-order supplier sourcing, sample material, supplier quotation and supplier contract.
2. Post-order mass-production material purchasing after Planning / APS.

## 2. Aggregation API

### `GET /api/v1/purchasing/dashboard`

```json
{
  "summary": {
    "openPurchaseOrderCount": 0,
    "lateArrivalCount": 0,
    "supplierQuotePendingCount": 0,
    "contractCoverageRate": 0,
    "priceVarianceRiskCount": 0
  },
  "supplierQuotes": [],
  "supplierContracts": [],
  "purchaseOrders": [],
  "arrivalRisks": [],
  "priceVarianceSignals": []
}
```

## 3. Detail APIs

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/purchasing/supplier-quotes` | Supplier quote list |
| `GET /api/v1/purchasing/supplier-contracts` | Supplier contract list |
| `GET /api/v1/purchasing/purchase-orders` | Purchase order list |
| `GET /api/v1/purchasing/receipts` | Goods receipt notes and arrival status |
| `GET /api/v1/purchasing/price-variance` | Contract/quote/current-price variance |

## 4. Dataset Structures

### `supplierQuotes[]`

```json
{
  "quoteNo": "",
  "supplierId": "",
  "supplierName": "",
  "materialNo": "",
  "materialName": "",
  "quotePrice": 0,
  "currency": "TWD",
  "validFrom": "2026-05-24",
  "validTo": "2026-08-24",
  "status": "pending",
  "relatedRdCaseNo": "",
  "riskLevel": "normal"
}
```

### `purchaseOrders[]`

```json
{
  "purchaseOrderNo": "",
  "supplierName": "",
  "materialNo": "",
  "materialName": "",
  "orderQty": 0,
  "receivedQty": 0,
  "unit": "",
  "expectedArrivalDate": "2026-05-28",
  "status": "open",
  "relatedPlanningCaseNo": "",
  "relatedWorkOrderNo": "",
  "riskLevel": "warning"
}
```

## 5. Existing API Candidates

- `/api/v1/purchase/purchaseorder`
- `/api/v1/purchase/goodsreceiptnote`
- `/api/v1/purchase/statistics`
- `/api/v1/purchase/contract`
- `/api/v1/purchase/payment`
- `/api/v1/purchase/arap`
- `/api/v1/material`
- `/api/v1/material/itemprice`
- `/api/v1/quotation`
- `/api/v1/contract`

## 6. Engineer Confirmation Required

1. Can `/api/v1/quotation` distinguish supplier quotes from customer quotes?
2. Can `/api/v1/contract` distinguish supplier contracts from customer contracts?
3. Are planned purchase requests stored separately from purchase orders?
4. Which statuses represent ordered, partially received, received and delayed?
5. Which table should supply current material price for costing?
