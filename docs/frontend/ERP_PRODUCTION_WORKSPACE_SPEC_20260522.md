# ERP Production Workspace Spec

日期：2026-05-23

## Status

Production first-version direction confirmed with the user and updated in code.

- Page: `src/app/production/page.tsx`
- Mock data: `src/mock/production.ts`
- Types: `src/types/production.ts`

## User Focus

The first Production page is a management-oriented production planning and MES dashboard.

User-confirmed focus areas:

1. Work orders should be shown from date and production-line viewpoints.
2. Weekly pre-scheduled work orders should reveal available capacity by process/line.
3. Near-term schedule should show whether required materials and staffing are sufficient.
4. Today's MES work-order status should be visible.
5. Production analysis should include production-time efficiency, material loss rate, and unit labor cost.
6. Quality inspection status should be included in both live work-order status and analysis.

Additional first-version additions:

1. Delivery risk by work order.
2. Changeover/cleaning time in capacity view.
3. Bottleneck process/line ranking.
4. Whether quality status blocks inventory receipt or shipment.
5. Exception categories for missing material, staffing support, QC pending, efficiency loss, and capacity bottleneck.

## First-Version Goal

Help management answer six questions:

1. How are work orders scheduled by date, process, and line?
2. Which process lines still have available capacity for sales orders?
3. Which process is the near-term bottleneck?
4. Can the next week of work orders run on time based on materials, staff, and changeover time?
5. Which work orders are at delivery risk?
6. Are today's production efficiency, material loss, labor cost, and quality results acceptable?

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 週排程與產能 | Date/line/process view of scheduled work orders, available capacity, bottleneck rank, changeover time, material readiness, and staffing readiness |
| MES 工單現況 | Today's work orders, process stage, completion rate, machine/material/staff/quality status, delivery risk |
| 效率損耗品質 | Production-time efficiency, material loss rate, unit labor cost, QC result, and whether QC blocks inventory/shipping |
| 生產明細 | Work order, batch, BOM, material, QC, and inventory workflow details |

## Data Shape

Work-order records are shaped around:

- `id`, `product`, `batchNo`
- `processType`, `line`
- `sourceOrder`, `bomNo`, `customerDueDate`, `deliveryRisk`
- `scheduleDate`, `startTime`, `endTime`, `changeoverMinutes`
- `stage`, `progress`, `priority`
- `plannedQty`, `completedQty`, `unit`
- `materialStatus`, `staffStatus`, `requiredStaff`, `assignedStaff`
- `machineStatus`
- `standardHours`, `actualHours`, `efficiencyRate`
- `standardMaterialQty`, `actualMaterialQty`, `materialLossRate`
- `laborHours`, `laborCost`, `unitLaborCost`
- `quality`, `qualityBlocksInventory`, `qualityBlocksShipment`
- `materials`
- `workflow`
- `relatedDocuments`

Weekly schedule records are shaped around:

- `date`, `label`
- production `line`
- `processType`
- `dailyCapacityHours`, `usedHours`, `availableHours`
- `changeoverHours`
- `bottleneckRank`
- scheduled slots with work order, product, time, material status, staff status, and stage

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| Work order list/detail | `workorder` |
| Weekly schedule by line/process | `aps`, `workorder`, `productline` |
| Bottleneck and available capacity | `aps`, `productline`, `workorder`, process setup data |
| Changeover/cleaning time | process/product-line setup or scheduling rules |
| Material readiness | `bom`, `inventory`, `batchnumber` |
| Staffing readiness | `work`, `processorder`, workforce/personnel data if available |
| Delivery risk | `sale`, `product_order`, `workorder`, shipping due dates |
| MES production data | `processorder`, `work`, `production_data` |
| Production input/output/reuse/machine/labor | `production_data_input`, `production_data_output`, `production_data_reuse`, `production_data_machine`, `production_data_labor` |
| Quality block status | quality-related module/table, or production data extension if no separate QC API exists |

## Next Integration Steps

1. Add a Production API adapter that returns the current mock shape.
2. Confirm how line/process capacity is stored or derived.
3. Confirm how changeover/cleaning time is represented.
4. Confirm how staffing requirements and assigned staff are represented.
5. Confirm where QC status, defect count, pending checks, and inventory/shipping block flags live.
6. Keep write actions disabled until backend workflow permissions are stable.
