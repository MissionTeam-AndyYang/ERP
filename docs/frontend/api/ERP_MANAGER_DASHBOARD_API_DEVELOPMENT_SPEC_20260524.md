# ERP Manager Dashboard API Development Spec

Date: 2026-05-24
Route: `/`
Purpose: Define APIs for Manager Dashboard V1.

## 1. V1 Goal

Manager Dashboard V1 is the daily cross-department cockpit. It aggregates fulfillment risk, today decisions, blockers, pre-order pipeline, production/quality/warehouse/logistics/finance signals.

## 2. Aggregation API

### `GET /api/v1/dashboard/manager`

```json
{
  "summary": {
    "fulfillmentRiskCount": 0,
    "deliveryCommitmentRate": 0,
    "estimatedMarginRate": 0,
    "cashSignalAmount": 0,
    "managerDecisionCount": 0
  },
  "focusKpis": [],
  "decisionQueue": [],
  "todayWorkQueue": [],
  "departmentBlockers": [],
  "preOrderPipeline": [],
  "operations": {
    "productionTrend": [],
    "oeeTrend": [],
    "qualityTrend": [],
    "alertDistribution": [],
    "productionLines": [],
    "alerts": []
  }
}
```

## 3. Detail APIs

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/dashboard/manager/summary` | Hero summary and focus KPIs |
| `GET /api/v1/dashboard/manager/decisions` | Manager decision queue |
| `GET /api/v1/dashboard/manager/workqueue` | Today's cross-department tasks |
| `GET /api/v1/dashboard/manager/blockers` | Cross-module blockers |
| `GET /api/v1/dashboard/manager/preorder` | Pre-order pipeline |
| `GET /api/v1/dashboard/manager/operations` | Production/quality/alert charts |

## 4. Dataset Structures

### `decisionQueue[]`

```json
{
  "decisionNo": "",
  "title": "",
  "ownerDepartment": "planning",
  "dueTime": "2026-05-24T11:30:00Z",
  "impact": "",
  "suggestedAction": "",
  "relatedModule": "planning",
  "relatedDocumentNo": "",
  "riskLevel": "blocking"
}
```

### `departmentBlockers[]`

```json
{
  "blockerNo": "",
  "department": "quality",
  "title": "",
  "detail": "",
  "owner": "",
  "relatedModule": "quality",
  "relatedDocumentNo": "",
  "riskLevel": "warning"
}
```

## 5. Existing API Candidates

Manager Dashboard should aggregate from:

- Warehouse dashboard/detail APIs
- Orders dashboard/detail APIs
- Planning / APS APIs
- Purchasing APIs
- Quality APIs
- Production APIs
- Logistics APIs
- Finance APIs
- R&D / Costing APIs

## 6. Implementation Recommendation

Short term:

- Frontend service layer can aggregate module APIs if backend dashboard endpoints are not ready.

Long term:

- Backend should provide dashboard aggregation endpoints to avoid duplicated business logic and multiple frontend requests.

## 7. Engineer Confirmation Required

1. Should dashboard aggregation be implemented in backend now or after module APIs are stable?
2. Which alert types require manager acknowledgement?
3. Should dashboard default risk window be today only or today plus 7 days?
4. Which finance signal should show first: estimated margin, billing-ready amount, AR overdue, or all three?
