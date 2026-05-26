# ERP Batches Operational Workspace Spec

Date: 2026-05-26
Scope: Batches page direction after owner discussion.

## Accepted Direction

```txt
Batches = item-centered batch operations dashboard.
Traceability = trace chain, document completeness and recall-scope investigation workspace.
```

Batches should become a practical batch management workspace centered on item-level batch operations. A single item can have multiple batches across different warehouses, locations, QA states and expiry conditions, so the first view should not be a flat batch-card overview.

## Core UX Principle

The Batches workspace should answer:

1. Which items have batch-related operational risk?
2. How many batches does each item currently have?
3. Where are those batches distributed by warehouse/location?
4. How much quantity is available, reserved, held or quarantined?
5. Which batches are near expiry, QA hold, isolated or blocking today's work?
6. Which batch should an operator/manager inspect next?

It should not answer the full upstream/downstream trace-chain question. That belongs to Traceability.

## Recommended Information Architecture

| Layer | Purpose | Primary question |
| --- | --- | --- |
| Item batch summary | Aggregate batch status by item. | Which item has the highest batch risk? |
| Batch distribution | Show batches and warehouse/location split for the selected item. | Where are this item's batches and can they be used? |
| Batch operations detail | Show selected batch operational state. | What is blocking or enabling this batch right now? |

## First Layer: Item Batch Summary

This is the main table/list. It should aggregate by item, not by individual batch/location rows.

Recommended fields:

| Field | Meaning |
| --- | --- |
| `itemId` | Item/SKU/material id. |
| `itemName` | Display name. |
| `itemType` | Finished goods, WIP, raw material, packaging, etc. |
| `totalBatchCount` | Number of active batches for this item. |
| `warehouseCount` | Number of warehouses/areas containing the item. |
| `totalQuantity` | Total physical quantity across batches/locations. |
| `availableQuantity` | Quantity that can be used. |
| `reservedQuantity` | Quantity reserved for orders/work orders/shipments. |
| `heldQuantity` | Quantity blocked by QA hold or quarantine. |
| `earliestExpiryDate` | Earliest expiry among active batches. |
| `qaHoldBatchCount` | Number of batches currently on QA hold. |
| `quarantineBatchCount` | Number of quarantined batches. |
| `nearExpiryBatchCount` | Number of near-expiry batches. |
| `demandImpact` | Today's or near-term demand affected by this item. |
| `highestRisk` | Display risk: normal, attention, high risk. |
| `ownerArea` | Warehouse, QA, Production, Purchasing, etc. |

Recommended sort:

```txt
high risk -> attention -> normal
then earliest expiry -> held quantity -> demand impact
```

## Second Layer: Batch Distribution

When an item is selected, show the selected item's batch and warehouse distribution.

Recommended fields:

| Field | Meaning |
| --- | --- |
| `batchNo` | Batch number. |
| `batchType` | Raw material, WIP, finished goods or shipment batch. |
| `warehouse` | Warehouse or area. |
| `location` | Bin/shelf/location. |
| `quantity` | Physical quantity in this row. |
| `availableQuantity` | Available quantity. |
| `reservedQuantity` | Reserved quantity. |
| `quarantineQuantity` | Quantity quarantined or isolated. |
| `expiryDate` | Expiry date. |
| `qaStatus` | Released, pending, hold, blocked, etc. |
| `batchStage` | Received, in production, finished, allocated, shipped, etc. |
| `relatedWork` | Related PO, MO, QC, SO or shipment. |
| `riskTags` | Near expiry, QA hold, quarantine, quantity mismatch, allocated but unreleased. |

Display recommendation:

- Use a dense table or compact rows.
- Group by warehouse if there are many locations.
- Show risk badges per batch row.
- Keep row click read-only; it only changes selected batch detail.

## Third Layer: Batch Operations Detail

When a batch is selected, show operational status, not full trace-chain.

Recommended sections:

| Section | Purpose |
| --- | --- |
| Current state | Warehouse, location, quantity, QA status and expiry. |
| Availability | Available, reserved, held and quarantined quantity. |
| Operational blockers | QA hold, expiry risk, missing document, location mismatch, pending receiving, pending release. |
| Related work | PO, MO, QC, SO, shipment or warehouse task currently linked to this batch. |
| Impact | Today's production, shipment or receiving work that may be affected. |
| Next review owner | Department/team that should review next. |

## Batches vs Traceability Boundary

| Question | Batches | Traceability |
| --- | --- | --- |
| Which item has risky batches? | Yes | No |
| Which warehouse/location contains the batch? | Yes | Optional context |
| Is the batch usable now? | Yes | No |
| Is the batch QA hold/quarantined/near expiry? | Yes | Optional context |
| Which work item is blocked by this batch? | Yes | Optional context |
| What is the full upstream/downstream chain? | No | Yes |
| Which customers/shipments are in recall scope? | No | Yes |
| Are trace documents complete? | No | Yes |

## V1 Read-Only Boundary

Allowed in V1:

- Search/filter by item, batch, warehouse, location, QA status, expiry and related work.
- Select item and batch rows.
- View quantities, QA state, expiry and operational blockers.
- Display suggested next review owner.
- Display source records and related work ids.

Not allowed in V1 unless backend mutation contracts exist:

- Release QA hold.
- Quarantine or unquarantine a batch.
- Adjust quantity.
- Move inventory.
- Allocate or deallocate quantity.
- Create recall action.
- Change expiry date.
- Edit batch master data.

## Suggested Data Shape

These are frontend planning names, not final backend contract names.

```ts
type BatchesDashboardResponse = {
  kpis: BatchKpi[];
  itemSummaries: BatchItemSummary[];
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
  batchType: string;
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

## Recommended Implementation Sequence

1. Create Batches API field readiness doc for the item-centered structure.
2. Refactor `/batches` mock data to item summaries and batch distribution rows.
3. Replace the current lifecycle board emphasis with item summary list + selected item distribution.
4. Add selected batch operational detail only after the selected item distribution is stable.
5. Keep all UI read-only and avoid Traceability chain visualization.
6. Run lint/build/route smoke.

## Decision

```txt
accepted_item_centered_batches_operations_workspace
```

The Batches page should become an item-centered batch operations dashboard. This matches the real-world case where one item can have multiple batches distributed across different warehouses, locations and operational states.
