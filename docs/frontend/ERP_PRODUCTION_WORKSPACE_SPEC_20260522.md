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
2. The weekly pre-scheduled work orders should reveal available capacity by process/line.
3. The near-term schedule should show whether required materials and staffing are sufficient.
4. Today's MES work-order status should be visible.
5. Production analysis should include production-time efficiency, material loss rate, and unit labor cost.
6. Quality inspection status should be included in both live work-order status and analysis.

## First-Version Goal

Help management answer four questions:

1. How are work orders scheduled by date, process, and line?
2. Which process lines still have available capacity for sales orders?
3. Can the next week of work orders run on time based on materials and staff?
4. Are today's production efficiency, material loss, labor cost, and quality results acceptable?

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 週排程與產能 | Date/line/process view of scheduled work orders, available capacity, material readiness, and staffing readiness |
| MES 工單現況 | Today's work orders, current process stage, completion rate, machine/material/staff/quality status |
| 效率損耗品質 | Production-time efficiency, material loss rate, unit labor cost, and quality inspection result |
| 生產明細 | Work order, batch, BOM, material, QC, and inventory workflow details |

## Data Shape

Work-order records are shaped around:

- `id`, `product`, `batchNo`
- `processType`, `line`
- `scheduleDate`, `startTime`, `endTime`
- `stage`, `progress`, `priority`
- `plannedQty`, `completedQty`, `unit`
- `materialStatus`, `staffStatus`, `requiredStaff`, `assignedStaff`
- `machineStatus`
- `standardHours`, `actualHours`, `efficiencyRate`
- `standardMaterialQty`, `actualMaterialQty`, `materialLossRate`
- `laborHours`, `laborCost`, `unitLaborCost`
- `quality`
- `materials`
- `workflow`
- `relatedDocuments`

Weekly schedule records are shaped around:

- `date`, `label`
- production `line`
- `processType`
- `dailyCapacityHours`, `usedHours`, `availableHours`
- scheduled slots with work order, product, time, material status, staff status, and stage

Quality records are shaped around:

- `status`
- `sampleCount`
- `defectCount`
- `defectRate`
- `pendingCount`
- `result`

## Workflow Basis

```txt
product_order -> aps_quantity -> work_order -> batch_number -> process_order -> process_labor
process_order -> production_data
production_data -> production_data_input / output / reuse / machine / labor
production_data -> quality inspection -> inventory_record
```

Production should connect sales demand, APS, work orders, material readiness, actual MES progress, QC result, and finished-goods inventory handoff.

## First-Version Scope

Included:

- Management KPI strip.
- Weekly date/line/process schedule view.
- Available capacity by line/process.
- Material and staffing readiness on scheduled slots.
- Today's MES work-order table.
- Quality status in work-order table and detail panel.
- Production efficiency, material loss, unit labor cost, and quality analysis.
- Selected work-order detail and workflow panel.

Deferred:

- Live machine/IoT connection.
- Start/pause/finish work-order write actions.
- Actual shop-floor reporting input.
- Automatic APS optimization.
- Full cost-accounting allocation.
- Multilingual page-level translation of all production labels.

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| Work order list/detail | `workorder` |
| Weekly schedule by line/process | `aps`, `workorder`, `productline` |
| Material readiness | `bom`, `inventory`, `batchnumber` |
| Staffing readiness | `work`, `processorder`, workforce/personnel data if available |
| MES production data | `processorder`, `work`, `production_data` |
| Production input/output/reuse/machine/labor | `production_data_input`, `production_data_output`, `production_data_reuse`, `production_data_machine`, `production_data_labor` |
| Quality status | quality-related module/table, or production data extension if no separate QC API exists |

## Next Integration Steps

1. Add a Production API adapter that returns the current mock shape.
2. Confirm how line/process capacity is stored or derived.
3. Confirm how staffing requirements and assigned staff are represented.
4. Confirm where QC status, defect count, and pending quality checks live in the backend.
5. Keep write actions disabled until backend workflow permissions are stable.
