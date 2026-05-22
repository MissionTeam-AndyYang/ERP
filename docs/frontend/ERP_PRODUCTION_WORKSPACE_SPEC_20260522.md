# ERP Production Workspace Spec

日期：2026-05-22

## Status

Implemented first prototype:

- Page: `src/app/production/page.tsx`
- Mock data: `src/mock/production.ts`
- Types: `src/types/production.ts`

This is the second core workspace after Warehouse.

## Purpose

Production gives management a clear view of work orders, material readiness, quality handoff, and production line load. The first version focuses on query, review, and workflow status.

## Workflow Basis

```txt
product_order -> aps_quantity -> work_order -> batch_number -> process_order -> process_labor
process_order -> inventory_record -> production_data
```

Production must connect demand, BOM/material readiness, actual production progress, QC status, and finished-goods inventory handoff.

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 工單總覽 | Work order, product, batch, line, quantity, progress |
| 備料狀態 | Material shortages, issued quantity, BOM relation |
| 品檢入庫 | QC pending, packaging, finished-goods handoff |
| 產線產能 | Line utilization and schedule slots |

## Current Data Shape

Each visible work order is shaped around:

- `id`, `product`, `batchNo`
- `line`, `startTime`, `endTime`
- `sourceOrder`, `bomNo`
- `stage`, `progress`, `priority`
- `plannedQty`, `completedQty`, `unit`
- `owner`, `eta`
- `qualityStatus`, `materialStatus`
- `materials`
- `workflow`
- `relatedDocuments`

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| Work order list/detail | `workorder` |
| Process order progress | `processorder`, `work` |
| Material readiness | `bom`, `inventory`, `batchnumber` |
| APS/order source | `aps`, `sale` |
| QC and production output | `work`, `production_data`, `inventory` |

## Next Integration Steps

1. Add a Production API adapter that returns the current mock shape.
2. Connect work order list and selected detail first.
3. Add material readiness from inventory and BOM once endpoint fields are confirmed.
4. Keep write actions disabled until backend workflow permissions are stable.
