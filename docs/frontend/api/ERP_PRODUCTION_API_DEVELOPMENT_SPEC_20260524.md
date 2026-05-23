# ERP Production API Development Spec

Date: 2026-05-24
Route: `/production`
Purpose: Define read-only APIs for Production V1.

## 1. V1 Goal

Production V1 shows scheduled work orders by date/line/process, MES status, material/staff readiness, efficiency, material loss, unit labor cost and quality signal.

## 2. Aggregation API

### `GET /api/v1/production/dashboard`

```json
{
  "summary": {
    "activeWorkOrderCount": 0,
    "delayedWorkOrderCount": 0,
    "averageOee": 0,
    "averageYieldRate": 0,
    "materialLossRate": 0,
    "laborCostPerUnit": 0
  },
  "scheduleByLine": [],
  "todayWorkOrders": [],
  "mesSignals": [],
  "efficiencyMetrics": [],
  "qualitySignals": [],
  "bottlenecks": []
}
```

## 3. Detail APIs

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/production/workorders` | Work-order list by date/line/process |
| `GET /api/v1/production/workorders/{workOrderNo}` | Work-order detail |
| `GET /api/v1/production/schedule` | Schedule board data |
| `GET /api/v1/production/mes` | MES execution status |
| `GET /api/v1/production/metrics` | Efficiency, loss and labor-cost metrics |

## 4. Dataset Structures

### `todayWorkOrders[]`

```json
{
  "workOrderNo": "",
  "sourceOrderNo": "",
  "productNo": "",
  "productName": "",
  "lineId": "",
  "lineName": "",
  "processName": "",
  "plannedStart": "2026-05-24T08:00:00Z",
  "plannedEnd": "2026-05-24T16:00:00Z",
  "plannedQty": 0,
  "actualQty": 0,
  "unit": "",
  "status": "running",
  "materialStatus": "ready",
  "staffStatus": "ready",
  "qualityStatus": "normal",
  "riskLevel": "normal"
}
```

### `efficiencyMetrics[]`

```json
{
  "workOrderNo": "",
  "oee": 0,
  "yieldRate": 0,
  "materialLossRate": 0,
  "unitLaborCost": 0,
  "plannedHours": 0,
  "actualHours": 0,
  "riskLevel": "normal"
}
```

## 5. Existing API Candidates

- `/api/v1/workorder`
- `/api/v1/workorder/productdata`
- `/api/v1/workorder/expecteddata`
- `/api/v1/workorder/statistics`
- `/api/v1/work/assignment`
- `/api/v1/work/process`
- `/api/v1/work/productdata`
- `/api/v1/work/progress`
- `/api/v1/productline`
- `/api/v1/productline/process`
- `/api/v1/plstatistics/mancapacity`
- `/api/v1/plstatistics/itemcapacity`
- `/api/v1/plstatistics/itemloss`
- `/api/v1/plstatistics/itemcost`

## 6. Engineer Confirmation Required

1. Which endpoint provides current MES status?
2. Does workorder include scheduled date, line, process and status?
3. Which endpoints provide actual production quantity and loss?
4. How is unit labor cost calculated today?
5. Where should production quality signal come from?
