# ERP Quality API Development Spec

Date: 2026-05-24
Route: `/quality`
Purpose: Define read-only APIs for Quality V1.

## 1. V1 Goal

Quality V1 focuses on material/item inspection and release/blocking. Material inspection is one main work item, but V1 also needs process, finished goods, pre-shipment inspection, document completeness and exception status.

## 2. Aggregation API

### `GET /api/v1/quality/dashboard`

```json
{
  "summary": {
    "pendingInspectionCount": 0,
    "releasedTodayCount": 0,
    "holdCount": 0,
    "blockingShipmentCount": 0,
    "documentMissingCount": 0
  },
  "inspectionQueue": [],
  "releaseBlocks": [],
  "processQualitySignals": [],
  "finishedGoodsChecks": [],
  "documentCompleteness": []
}
```

## 3. Detail APIs

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/quality/inspections` | Inspection queue and results |
| `GET /api/v1/quality/releases` | Release/hold/quarantine status |
| `GET /api/v1/quality/blockers` | Quality blockers for warehouse, production and logistics |
| `GET /api/v1/quality/documents` | Required quality documents and completeness |

## 4. Dataset Structures

### `inspectionQueue[]`

```json
{
  "inspectionNo": "",
  "inspectionType": "material",
  "sourceDocumentNo": "",
  "itemNo": "",
  "itemName": "",
  "batchNo": "",
  "quantity": 0,
  "unit": "",
  "warehouseName": "",
  "status": "pending",
  "result": null,
  "assignedInspector": "",
  "dueTime": "2026-05-24T14:00:00Z",
  "riskLevel": "warning"
}
```

Allowed `inspectionType`:

- `material`
- `process`
- `finished_goods`
- `pre_shipment`

Allowed `result`:

- `pass`
- `fail`
- `conditional_release`
- `reinspect`

### `releaseBlocks[]`

```json
{
  "blockNo": "",
  "blockType": "quality_hold",
  "itemNo": "",
  "itemName": "",
  "batchNo": "",
  "blockedQty": 0,
  "unit": "",
  "blockingModule": "warehouse",
  "reason": "",
  "owner": "quality",
  "riskLevel": "blocking"
}
```

## 5. Existing API Candidates

- `/api/v1/batchnumber`
- `/api/v1/batchtrace`
- `/api/v1/batchtrace/record`
- `/api/v1/work/productdata`
- `/api/v1/workorder/productdata`
- `/api/v1/inventory`

## 6. Proposed New APIs

No explicit quality endpoint was observed. Recommended new endpoints:

- `/api/v1/quality/inspection`
- `/api/v1/quality/release`
- `/api/v1/quality/blockers`
- `/api/v1/quality/documents`

## 7. Engineer Confirmation Required

1. Where is material inspection status stored today?
2. Does inventory include quality hold quantity/status?
3. Which quality statuses block production and shipment?
4. Are process and finished goods inspection results stored in work/productdata?
5. Is a dedicated quality endpoint planned by the engineer?
