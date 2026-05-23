# ERP Finance API Development Spec

Date: 2026-05-24
Route: `/finance`
Purpose: Define read-only APIs for Finance V1.

## 1. V1 Goal

Finance V1 focuses on estimated/actual margin, cost variance, billing readiness, AR/AP signals and order-level financial trace.

## 2. Aggregation API

### `GET /api/v1/finance/dashboard`

```json
{
  "summary": {
    "estimatedMarginRate": 0,
    "actualMarginRate": 0,
    "marginRiskCount": 0,
    "billingReadyAmount": 0,
    "arOutstandingAmount": 0,
    "apUpcomingAmount": 0
  },
  "marginByOrder": [],
  "costVariance": [],
  "billingReadiness": [],
  "arSignals": [],
  "apSignals": []
}
```

## 3. Detail APIs

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/finance/orders` | Order-level financial status |
| `GET /api/v1/finance/margins` | Estimated and actual margin |
| `GET /api/v1/finance/cost-variance` | Material, labor, production and logistics variance |
| `GET /api/v1/finance/billing-readiness` | POD/document/billing status |
| `GET /api/v1/finance/arap` | AR/AP summary |

## 4. Dataset Structures

### `marginByOrder[]`

```json
{
  "orderNo": "",
  "customerName": "",
  "orderAmount": 0,
  "estimatedCost": 0,
  "actualCost": 0,
  "estimatedMarginRate": 0,
  "actualMarginRate": 0,
  "marginVarianceRate": 0,
  "riskLevel": "normal"
}
```

### `billingReadiness[]`

```json
{
  "orderNo": "",
  "shipmentNo": "",
  "podStatus": "completed",
  "documentStatus": "ready",
  "billingStatus": "ready",
  "billingAmount": 0,
  "blockReason": ""
}
```

## 5. Existing API Candidates

- `/api/v1/sale/arap`
- `/api/v1/sale/payment`
- `/api/v1/purchase/arap`
- `/api/v1/purchase/payment`
- `/api/v1/shipwarehouse/shiparap`
- `/api/v1/shipwarehouse/warehousearap`
- `/api/v1/plstatistics/itemcost`
- `/api/v1/inventory/price`
- `/api/v1/sale/productorder`
- `/api/v1/quotation`

## 6. Engineer Confirmation Required

1. Which endpoint is source of truth for AR and AP?
2. Can order-level actual cost be calculated today?
3. Is POD required before billing-ready?
4. Which cost components are available now: material, labor, overhead, logistics?
5. Is estimated margin stored or calculated from quotation/BOM/purchase price?
