# ERP Orders API Development Spec

Date: 2026-05-24
Route: `/orders`
Purpose: Define read-only APIs for Orders V1.

## 1. V1 Goal

Orders V1 helps managers determine whether an order can be promised, produced, shipped and later collected, with delivery feasibility as the first priority, margin as second, and payment/collection as third.

## 2. Aggregation API

### `GET /api/v1/orders/dashboard`

```json
{
  "summary": {
    "openOrderCount": 0,
    "highRiskOrderCount": 0,
    "commitmentRate": 0,
    "estimatedMarginRate": 0,
    "paymentRiskCount": 0
  },
  "orders": [],
  "commitmentChecks": [],
  "deliveryRisks": [],
  "marginSignals": [],
  "paymentSignals": [],
  "preOrderPipeline": []
}
```

## 3. Detail APIs

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/orders` | Formal order list |
| `GET /api/v1/orders/{orderNo}` | Formal order detail |
| `GET /api/v1/orders/{orderNo}/commitment` | ATP/CTP commitment result |
| `GET /api/v1/orders/quotations` | Customer quotations and negotiation status |
| `GET /api/v1/orders/contracts` | Customer contract status |
| `GET /api/v1/orders/{orderNo}/fulfillment` | Material, production, quality, shipping and payment workflow |

## 4. Dataset Structures

### `orders[]`

```json
{
  "orderNo": "",
  "customerId": "",
  "customerName": "",
  "productNo": "",
  "productName": "",
  "quantity": 0,
  "unit": "",
  "orderAmount": 0,
  "estimatedCost": 0,
  "estimatedMarginRate": 0,
  "actualMarginRate": null,
  "orderDate": "2026-05-24",
  "dueDate": "2026-06-01",
  "committedDate": "2026-06-01",
  "stage": "commitment_check",
  "commitmentDecision": "can_commit",
  "deliveryRisk": "normal",
  "riskReason": "",
  "paymentStatus": "not_billed"
}
```

### `commitmentChecks[]`

```json
{
  "orderNo": "",
  "checkType": "material",
  "result": "pass",
  "message": "",
  "blocking": false,
  "ownerModule": "planning",
  "relatedDocumentNo": ""
}
```

Allowed `checkType`:

- `finished_goods_atp`
- `material`
- `capacity`
- `staff`
- `quality`
- `shipping`
- `margin`

Allowed `commitmentDecision`:

- `can_commit`
- `needs_coordination`
- `cannot_commit`

### `preOrderPipeline[]`

```json
{
  "caseNo": "",
  "customerName": "",
  "productName": "",
  "stage": "customer_quotation",
  "ownerDepartment": "sales",
  "supplierQuoteStatus": "completed",
  "costingStatus": "completed",
  "customerQuoteStatus": "pending",
  "customerContractStatus": "not_started",
  "estimatedMarginRate": 0,
  "riskLevel": "normal"
}
```

## 5. Existing API Candidates

- `/api/v1/sale/productorder`
- `/api/v1/sale/shippingorder`
- `/api/v1/sale/statistics`
- `/api/v1/sale/contract`
- `/api/v1/sale/payment`
- `/api/v1/sale/arap`
- `/api/v1/quotation`
- `/api/v1/contract`
- `/api/v1/inventory`
- `/api/v1/bom/aps`
- `/api/v1/aps/quantity`
- `/api/v1/workorder`

## 6. Calculation Rules

- `estimatedMarginRate = (orderAmount - estimatedCost) / orderAmount`.
- Commitment decision should use worst-result logic from ATP/CTP checks.
- Orders must not automatically create purchase requests or work orders in V1.

## 7. Engineer Confirmation Required

1. Which endpoint contains formal order due date and committed date?
2. Can quotation distinguish customer quotation from supplier quotation?
3. Can contract distinguish customer contract from supplier contract?
4. Which fields can support ATP/CTP checks today?
5. Where should commitment result be stored if it becomes persistent?
