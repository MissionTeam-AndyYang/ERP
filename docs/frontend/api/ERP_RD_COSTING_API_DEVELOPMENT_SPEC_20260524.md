# ERP R&D / Costing API Development Spec

Date: 2026-05-24
Route: `/rd`
Purpose: Define read-only APIs for R&D / Costing V1.

## 1. V1 Goal

R&D / Costing V1 supports development request, formula/material selection, sample making, BOM version control, production cost simulation, nutrition label status and transfer to formal item/BOM.

## 2. Aggregation API

### `GET /api/v1/rd/dashboard`

```json
{
  "summary": {
    "activeDevelopmentCount": 0,
    "samplePendingCount": 0,
    "costingPendingCount": 0,
    "nutritionLabelPendingCount": 0,
    "readyForQuotationCount": 0
  },
  "developmentProjects": [],
  "sampleTasks": [],
  "bomVersions": [],
  "costingCases": [],
  "nutritionLabelStatus": []
}
```

## 3. Detail APIs

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/rd/projects` | Development projects |
| `GET /api/v1/rd/projects/{projectNo}` | Development project detail |
| `GET /api/v1/rd/samples` | Sample making and sample delivery status |
| `GET /api/v1/rd/bom-versions` | Development BOM/formula versions |
| `GET /api/v1/rd/costing` | Cost simulation |
| `GET /api/v1/rd/nutrition` | Nutrition label status |

## 4. Dataset Structures

### `developmentProjects[]`

```json
{
  "projectNo": "",
  "customerName": "",
  "productName": "",
  "stage": "formula_selection",
  "owner": "rd",
  "targetCost": 0,
  "estimatedCost": 0,
  "estimatedMarginRate": 0,
  "sampleStatus": "not_started",
  "supplierQuoteStatus": "pending",
  "costingStatus": "pending",
  "nutritionLabelStatus": "pending",
  "riskLevel": "normal"
}
```

### `bomVersions[]`

```json
{
  "projectNo": "",
  "bomVersionNo": "",
  "versionName": "",
  "status": "draft",
  "totalMaterialCost": 0,
  "totalProcessingCost": 0,
  "totalEstimatedCost": 0,
  "approvedForQuotation": false
}
```

## 5. Existing API Candidates

- `/api/v1/bom`
- `/api/v1/bom/tree`
- `/api/v1/bom/process`
- `/api/v1/material`
- `/api/v1/material/itemprice`
- `/api/v1/product`
- `/api/v1/goods`
- `/api/v1/quotation`
- `/api/v1/contract`

## 6. Proposed New APIs

No explicit R&D endpoint was observed. Recommended new endpoints:

- `/api/v1/rd/projects`
- `/api/v1/rd/samples`
- `/api/v1/rd/costing`
- `/api/v1/rd/nutrition`

## 7. Engineer Confirmation Required

1. Is there an existing table for development requests/projects?
2. Can BOM distinguish development version from approved production BOM?
3. Where should nutrition label status be stored?
4. How should sample delivery status connect to Sales/Orders?
5. Can supplier quote data be linked to costing cases?
