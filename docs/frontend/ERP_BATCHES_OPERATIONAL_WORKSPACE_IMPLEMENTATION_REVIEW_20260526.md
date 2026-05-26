# ERP Batches Operational Workspace Implementation Review

Date: 2026-05-26
Scope: Frontend implementation review after refactoring `/batches` to the accepted item-centered workspace direction.

## Summary

The `/batches` page has been refactored from the previous lifecycle-board overview into a read-only item-centered batch operations workspace.

The implemented structure now follows:

```txt
Item batch summary -> Selected item batch distribution -> Selected batch operations detail
```

This matches the accepted boundary:

```txt
Batches = item-centered batch operations dashboard.
Traceability = trace chain, document completeness and recall-scope investigation workspace.
```

## Implemented UX Changes

| Area | Before | After |
| --- | --- | --- |
| Primary view | Batch lifecycle stages. | Item-level batch summary. |
| Main question | Where is a batch in the lifecycle? | Which item has batch-related operational risk? |
| Detail layer | Batch cards and task list. | Selected item distribution plus selected batch detail. |
| Search | Batch, item, work order, location and task. | Item, batch, warehouse, location, QA status, related work and risk tags. |
| Page boundary | Could overlap with Traceability. | Focuses on operational availability, QA, expiry, reservation and quarantine. |

## Current Page Data Shape

The mock fallback now uses the accepted future API-oriented shape:

```ts
type BatchesDashboardData = {
  kpis: BatchKpi[];
  itemSummaries: BatchItemSummary[];
};
```

Each `BatchItemSummary` includes:

- Item id, item name and item type.
- Total, available, reserved and held quantities.
- Batch count and warehouse count.
- Earliest expiry date.
- QA hold, quarantine and near-expiry counts.
- Demand impact and next review owner.
- Nested batch distribution rows.

Each batch distribution row includes:

- Batch number and batch type.
- Warehouse and location.
- Quantity, available quantity, reserved quantity and quarantine quantity.
- Expiry date, QA status and batch stage.
- Related work ids and risk tags.

## Read-Only Boundary

The implementation intentionally does not add mutation actions.

Not included:

- QA release.
- Quarantine or unquarantine.
- Inventory adjustment.
- Warehouse movement.
- Allocation or deallocation.
- Recall action.
- Expiry date edit.
- Batch master edit.

This keeps the page safe before backend authorization, audit and mutation contracts are defined.

## Traceability Boundary Check

The page does not introduce:

- Full upstream/downstream chain visualization.
- Recall-scope customer or shipment calculation.
- Trace document completeness.
- Corrective-action workflow.

Those remain in Traceability.

## Verification

The following checks were run after implementation:

```txt
npm.cmd run lint
npm.cmd run build
GET /batches route smoke
```

Result:

```txt
lint passed
build passed
/batches HTTP route smoke passed
```

Interactive browser smoke remains unavailable in this local session because the Browser plugin runtime is missing its `scripts/browser-client.mjs` file.

## Follow-Up

Recommended next frontend tasks:

1. Wait for the real `/api/v1/batches/dashboard` payload and add a dedicated mapper/service when backend fields are stable.
2. Verify how backend represents quantities: display strings only or numeric amount plus unit.
3. Confirm whether one batch can appear in multiple warehouse/location rows.
4. Decide whether server-side filters are needed after item, batch, warehouse, location and QA status fields stabilize.

## Decision

```txt
batches_item_centered_workspace_implemented_read_only
```
