# ERP Batches API Field Readiness

Date: 2026-05-26
Scope: Frontend API readiness notes for the item-centered Batches operational workspace.

## Purpose

This document bridges the accepted Batches workspace direction with a future backend read endpoint.

Batches should become an item-centered batch operations dashboard. The first API contract should support item-level batch aggregation and selected-item batch distribution. It should not return full trace-chain or recall-scope data; that belongs to Traceability.

## Endpoint

Recommended endpoint:

```txt
GET /api/v1/batches/dashboard
```

Current frontend hook:

```txt
useSupportDashboard("/api/v1/batches/dashboard", batchesDashboardMock, "Batches API unavailable")
```

The current page still uses Phase 1.5 lifecycle mock data. The accepted next contract should move toward the item-centered shape below.

## V1 Response Shape

Recommended response:

```ts
type BatchesDashboardResponse = {
  kpis: BatchKpi[];
  itemSummaries: BatchItemSummary[];
};

type BatchKpi = {
  label: string;
  value: string;
  hint: string;
  tone: "success" | "warning" | "danger" | "info" | "neutral";
};

type BatchItemSummary = {
  itemId: string;
  itemName: string;
  itemType: string;
  totalBatchCount: number;
  warehouseCount: number;
  totalQuantity: string;
  availableQuantity: string;
  reservedQuantity: string;
  heldQuantity: string;
  earliestExpiryDate: string;
  qaHoldBatchCount: number;
  quarantineBatchCount: number;
  nearExpiryBatchCount: number;
  demandImpact: string;
  highestRisk: "normal" | "attention" | "highRisk";
  riskLabel: string;
  tone: "success" | "warning" | "danger" | "info" | "neutral";
  ownerArea: string;
  batches: BatchDistributionRow[];
};

type BatchDistributionRow = {
  batchNo: string;
  batchType: "rawMaterial" | "wip" | "finishedGoods" | "shipment" | string;
  warehouse: string;
  location: string;
  quantity: string;
  availableQuantity: string;
  reservedQuantity: string;
  quarantineQuantity: string;
  expiryDate: string;
  qaStatus: string;
  batchStage: string;
  relatedWork: string[];
  riskTags: string[];
  tone: "success" | "warning" | "danger" | "info" | "neutral";
};
```

## Required Fields

| Field | Required | Frontend use |
| --- | --- | --- |
| `kpis` | Yes | Page KPI strip. |
| `itemSummaries` | Yes | Main item-level batch summary list/table. |
| `itemId` | Yes | Primary key for selected item and search. |
| `itemName` | Yes | Main display label. |
| `itemType` | Yes | Item category context. |
| `totalBatchCount` | Yes | Item batch density and risk context. |
| `warehouseCount` | Yes | Shows distribution complexity. |
| `totalQuantity` | Yes | Total physical quantity across batches/locations. |
| `availableQuantity` | Yes | Quantity that can be used. |
| `reservedQuantity` | Yes | Quantity committed to orders/work orders/shipments. |
| `heldQuantity` | Yes | Quantity blocked by QA hold or quarantine. |
| `earliestExpiryDate` | Yes | Expiry risk sorting and display. |
| `qaHoldBatchCount` | Yes | QA risk summary. |
| `quarantineBatchCount` | Yes | Isolation risk summary. |
| `nearExpiryBatchCount` | Yes | Expiry risk summary. |
| `demandImpact` | Yes | Today's or near-term work affected by this item. |
| `highestRisk` | Yes | Sort and risk grouping. |
| `riskLabel` | Yes | Badge label. |
| `tone` | Yes | Badge color. |
| `ownerArea` | Yes | Responsible area for review. |
| `batches` | Yes | Batch distribution rows for selected-item detail. Valid empty array is allowed. |

## Batch Distribution Required Fields

| Field | Required | Frontend use |
| --- | --- | --- |
| `batchNo` | Yes | Row key and batch display id. |
| `batchType` | Yes | Raw material, WIP, finished goods or shipment context. |
| `warehouse` | Yes | Warehouse/area grouping. |
| `location` | Yes | Bin/location display. |
| `quantity` | Yes | Physical quantity. |
| `availableQuantity` | Yes | Usable quantity. |
| `reservedQuantity` | Yes | Reserved quantity. |
| `quarantineQuantity` | Yes | Isolated or quarantined quantity. |
| `expiryDate` | Yes | Expiry display and risk detection. |
| `qaStatus` | Yes | QA release/hold/pending display. |
| `batchStage` | Yes | Received, in production, finished, allocated, shipped, etc. |
| `relatedWork` | Yes | Related PO/MO/QC/SO/shipment/warehouse task ids. |
| `riskTags` | Yes | Near expiry, QA hold, quarantine, mismatch, allocated but unreleased. |
| `tone` | Yes | Row risk badge color. |

## Risk Mapping

| `highestRisk` | Display label examples | Tone | Meaning |
| --- | --- | --- | --- |
| `normal` | `正常` | `success` or `neutral` | No immediate batch operations risk. |
| `attention` | `注意` | `warning` | Needs follow-up due to expiry, reservation, low available quantity or pending QA. |
| `highRisk` | `高風險` | `danger` | Blocks production, shipment, receiving or QA release. |

Recommended item sort:

```txt
highRisk -> attention -> normal
then earliestExpiryDate -> heldQuantity -> demandImpact
```

## Status / Vocabulary Notes

These values can be backend-owned strings in V1, as long as `tone` and risk fields are stable.

Recommended display vocabularies:

| Concept | Suggested labels |
| --- | --- |
| QA status | `已放行`, `待判定`, `檢驗中`, `QA Hold`, `阻擋` |
| Batch stage | `已入庫`, `製程中`, `成品待放行`, `可出貨`, `已分配`, `已出貨` |
| Risk tags | `即期`, `逾期`, `QA Hold`, `隔離`, `數量異常`, `已分配未放行` |
| Owner area | `倉庫`, `品保`, `生管`, `採購`, `物流`, `業務` |

## Batches vs Traceability API Boundary

Allowed in Batches:

- Item-level batch aggregation.
- Warehouse/location split.
- Quantity availability and reservation.
- QA release/hold state.
- Expiry and quarantine risk.
- Related operational work ids.
- Next review owner.

Not Batches:

- Full upstream/downstream trace chain.
- Recall-scope customer/shipment calculation.
- Trace document completeness.
- Chain graph.
- Corrective action workflow.

Those belong to:

```txt
GET /api/v1/traceability/dashboard
```

or future Traceability detail endpoints.

## V1 Read-Only Boundary

Allowed:

- Return item summaries and batch distribution rows.
- Return empty arrays as valid API data.
- Return display-ready strings while canonical backend codes are stabilizing.
- Support frontend local search and selected-row detail.

Not required for V1:

- Release QA hold.
- Quarantine or unquarantine.
- Adjust quantity.
- Move inventory.
- Allocate or deallocate quantity.
- Create recall action.
- Change expiry date.
- Edit batch master data.

## Backend Confirmation Questions

| Question | Why it matters |
| --- | --- |
| Should `itemSummaries` include all active batch-managed items or only risky items? | Defines default density and performance. |
| Are quantities returned as display strings or numeric amount + unit? | Numeric values help sorting; strings are faster for V1 UI. |
| Which warehouse/location tables are authoritative? | Required for distribution view. |
| Which status owns QA hold/release: Quality, Warehouse, Inventory or Batch? | Prevents inconsistent status mapping. |
| Can one batch appear in multiple warehouses/locations? | Determines whether `BatchDistributionRow` should represent batch-location rows. |
| How should reserved quantity be sourced? | Could come from sales orders, work orders, shipment allocations or production reservations. |
| Should expired/near-expiry be calculated by backend or frontend? | Backend calculation is safer if shelf-life rules differ by item. |
| Can `batches` intentionally be an empty array? | Frontend should show empty state and not refill mock data when API is valid. |
| Do we need a detail endpoint later, such as `/api/v1/batches/{batchNo}`? | V1 dashboard may be enough; V1.5 may need detail/drill-down. |

## Frontend Integration Notes

- Current `/batches` UI still uses the old lifecycle overview shape.
- The accepted next UI should refactor to `itemSummaries` and selected item distribution.
- A dedicated `batches-api` service/type file should be added when this endpoint is implemented.
- Server-side filters can wait until `itemId`, `batchNo`, `warehouse`, `location`, `qaStatus` and `riskTags` are stable.
- No mutation UI should be introduced until backend authorization and audit rules exist.

## Decision

```txt
batches_item_centered_api_field_readiness_created
```

The frontend is ready to plan a read-only item-centered Batches dashboard endpoint. The next UI refactor should use item summaries as the first layer and batch distribution rows as the second layer.
