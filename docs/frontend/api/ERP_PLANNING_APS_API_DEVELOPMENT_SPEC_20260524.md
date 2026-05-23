# ERP Planning / APS API Development Spec

Date: 2026-05-24
Route: `/planning`
Purpose: Define read-only APIs for Planning / APS V1.

## 1. V1 Goal

Planning / APS represents Production Control. It turns formal orders into material demand, capacity checks, staff checks and suggested work orders. V1 shows suggestions and blockers; it does not automatically create purchase orders or work orders.

## 2. Aggregation API

### `GET /api/v1/planning/dashboard`

```json
{
  "summary": {
    "planningCaseCount": 0,
    "materialShortageCount": 0,
    "capacityConflictCount": 0,
    "staffGapCount": 0,
    "suggestedPurchaseRequestCount": 0,
    "suggestedWorkOrderCount": 0
  },
  "planningCases": [],
  "materialShortages": [],
  "capacityChecks": [],
  "staffChecks": [],
  "suggestedPurchaseRequests": [],
  "suggestedWorkOrders": []
}
```

## 3. Detail APIs

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/planning/cases` | Orders requiring planning |
| `GET /api/v1/planning/cases/{caseNo}` | Planning case detail |
| `GET /api/v1/planning/cases/{caseNo}/materials` | BOM explosion and shortage check |
| `GET /api/v1/planning/cases/{caseNo}/capacity` | Process/line capacity check |
| `GET /api/v1/planning/cases/{caseNo}/workorders` | Suggested work orders |

## 4. Dataset Structures

### `planningCases[]`

```json
{
  "caseNo": "",
  "sourceOrderNo": "",
  "customerName": "",
  "productNo": "",
  "productName": "",
  "quantity": 0,
  "unit": "",
  "dueDate": "2026-06-01",
  "promisedDate": "2026-06-01",
  "decision": "needs_planning",
  "materialShortageValue": 0,
  "requiredProductionHours": 0,
  "availableProductionHours": 0,
  "purchaseRequestCount": 0,
  "suggestedWorkOrderCount": 0,
  "riskLevel": "warning"
}
```

### `materialShortages[]`

```json
{
  "caseNo": "",
  "materialNo": "",
  "materialName": "",
  "requiredQty": 0,
  "availableQty": 0,
  "shortageQty": 0,
  "unit": "",
  "suggestedAction": "purchase_request",
  "expectedArrivalDate": null,
  "qualityHoldQty": 0,
  "riskLevel": "blocking"
}
```

### `suggestedWorkOrders[]`

```json
{
  "suggestionNo": "",
  "caseNo": "",
  "productNo": "",
  "processName": "",
  "lineId": "",
  "lineName": "",
  "plannedStart": "2026-05-25T08:00:00Z",
  "plannedEnd": "2026-05-25T16:00:00Z",
  "plannedQty": 0,
  "unit": "",
  "status": "suggested",
  "blockingReason": ""
}
```

## 5. Existing API Candidates

- `/api/v1/sale/productorder`
- `/api/v1/aps/quantity`
- `/api/v1/bom/aps`
- `/api/v1/bom/tree`
- `/api/v1/inventory`
- `/api/v1/workorder`
- `/api/v1/productline`
- `/api/v1/productline/process`
- `/api/v1/plstatistics/mancapacity`
- `/api/v1/plstatistics/itemcapacity`

## 6. Engineer Confirmation Required

1. Does `/api/v1/aps/quantity` already return BOM explosion or only quantity calculation?
2. Which endpoint stores formal planning cases, if any?
3. How should suggested purchase requests be represented before mutation APIs exist?
4. Where are staff/skill constraints stored?
5. Can work order suggestions be calculated without persisting records in V1?
