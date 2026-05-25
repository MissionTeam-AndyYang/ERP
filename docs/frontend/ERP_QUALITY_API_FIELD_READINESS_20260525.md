# ERP Quality API Field Readiness

Date: 2026-05-25
Scope: Frontend readiness notes for `GET /api/v1/quality/dashboard` while backend integration is pending.

## Purpose

This document bridges the approved Quality V1 UI shape with the backend-facing Quality API spec. It records what the frontend already expects, where normalization can happen and which fields require engineer confirmation.

## Current Frontend Contract

Current frontend service:

- `src/services/quality-api.ts`
- `src/hooks/use-quality-dashboard.ts`
- `src/types/quality.ts`

Current frontend endpoint:

```txt
GET /api/v1/quality/dashboard
```

Current frontend top-level shape:

```txt
summary
inspections
```

Current backend API spec top-level shape:

```txt
summary
inspectionQueue
releaseBlocks
processQualitySignals
finishedGoodsChecks
documentCompleteness
```

## Normalization Decision

Recommended V1 approach:

```txt
Backend may return the API spec shape.
Frontend service should normalize it into the existing QualityDashboardData shape.
The page component should remain unchanged unless a real user-facing information gap is discovered.
```

Reason:

- The current page layout already answers the approved Quality V1 management questions.
- Keeping normalization in `quality-api.ts` avoids scattering backend field names through UI components.
- Backend can preserve domain-oriented datasets while the frontend composes inspection, release/block and document signals into stable display records.

## Field Readiness Matrix

| Frontend field | Backend spec candidate | Readiness | Notes |
| --- | --- | --- | --- |
| `summary[].label/value/hint/tone` | `summary` | Needs frontend normalization | Derive display KPIs from pending, released, hold, shipment-blocking and document-missing counts. |
| `inspections[].id` | `inspectionQueue[].inspectionNo` | Ready |
| `inspections[].itemName/itemNo` | `inspectionQueue[].itemName/itemNo` | Ready |
| `inspections[].batchNo` | `inspectionQueue[].batchNo` or `releaseBlocks[].batchNo` | Ready |
| `inspections[].sourceType/sourceNo` | `inspectionQueue[].sourceDocumentNo` and source module | Needs mapping |
| `inspections[].workOrder/salesOrder` | Process/finished/shipment source records | Needs source confirmation |
| `inspections[].supplier` | Receiving/purchase source | Needs source confirmation |
| `inspections[].line` | Process/production source | Needs source confirmation |
| `inspections[].inspectionType` | `inspectionQueue[].inspectionType` | Ready with mapping |
| `inspections[].stage` | `inspectionQueue[].status` | Ready with mapping |
| `inspections[].decision` | `inspectionQueue[].result` and release/block status | Needs mapping |
| `inspections[].tone` | Risk/result mapping | Needs mapping |
| `inspections[].sampleCount/defectCount/defectRate` | Inspection result data | Needs source confirmation | API spec does not yet include sample/defect fields. |
| `inspections[].pendingTests` | `documentCompleteness[]` or inspection detail | Needs aggregation |
| `inspections[].issueReason` | `releaseBlocks[].reason` or inspection message | Ready with mapping |
| `inspections[].blocksInventory` | `releaseBlocks[].blockingModule = warehouse` | Needs mapping |
| `inspections[].blocksShipment` | `releaseBlocks[].blockingModule = logistics` | Needs mapping |
| `inspections[].blocksProduction` | `releaseBlocks[].blockingModule = production` | Needs mapping |
| `inspections[].owner` | `assignedInspector`, `owner` | Ready |
| `inspections[].dueTime` | `inspectionQueue[].dueTime` | Ready with formatting |
| `inspections[].documents` | `documentCompleteness[]` grouped by inspection/batch | Needs aggregation |
| `inspections[].workflow` | Source document, sample, inspection, release/hold and downstream blocker records | Needs aggregation |

## Backend Confirmation Needed

| Question | Impact |
| --- | --- |
| Where is material inspection status stored today? | Blocks receiving-to-available inventory status. |
| Does inventory include quality hold quantity/status? | Needed for Warehouse available quantity and Logistics shipment blockers. |
| Which quality statuses block production and shipment? | Needed for cross-module blocker rules. |
| Are process and finished-goods inspection results stored in work/productdata? | Needed for Production and Quality mapping. |
| Is a dedicated quality endpoint planned by the engineer? | Determines whether frontend normalizes from quality-specific routes or cross-module records. |
| Where are quality documents and missing-document statuses stored? | Needed for document completeness view. |
| Are sample count, defect count and defect rate available from backend records? | Needed for NCR and inspection details. |

## Frontend Service TODOs After Backend Runtime Report

1. Expand `QualityDashboardResponse` to accept the backend API spec shape.
2. Add mapper functions in `src/services/quality-api.ts` for inspection type, stage, result/decision, document status, blocking module and tones.
3. Compose `inspectionQueue[]`, `releaseBlocks[]` and `documentCompleteness[]` into each frontend `QualityInspection`.
4. Decide whether `processQualitySignals[]` and `finishedGoodsChecks[]` should remain folded into `inspections` or become separate view panels.
5. Decide whether empty arrays from API mean true empty state or should continue falling back to mock.
6. Re-run Quality page smoke on desktop and mobile with real API data.

## Current Decision

```txt
ready_for_backend_mapping
```

The frontend page and type shape are stable enough for the engineer to implement or verify the Quality read-only aggregate. The main open work is data normalization, dedicated quality endpoint confirmation and release/block source mapping.
