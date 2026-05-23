# ERP Planning / APS Workspace Spec

日期：2026-05-23

## Status

Planning / APS first-version workspace added after the Orders ATP/CTP commitment layer.

- Page: `src/app/planning/page.tsx`
- Mock data: `src/mock/planning.ts`
- Types: `src/types/planning.ts`

## Position In Workflow

Orders answers the first commitment question:

```txt
Can this order be promised, and on what date?
```

Planning / APS answers the next execution question:

```txt
How do we turn promised orders into material requests, capacity plans, and work-order suggestions?
```

Department ownership: this workspace represents Production Control / 生管. After Sales creates a formal order, Production Control owns production material request and scheduling.

## First-Version Goal

Help management and planners answer:

1. Which promised or received orders still need planning?
2. Which orders have material shortages after BOM explosion?
3. Which shortages should become purchase requests, transfers, or quality-release follow-ups?
4. Which process lines have enough capacity and staff?
5. Which suggested work orders can be created, and which must be adjusted?
6. Which issues must be resolved before the order can be executed?

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 需求展開 | Convert order demand into item, BOM, material, capacity, QC, and shipping requirements |
| 物料/請購 | Review shortage quantities, available stock, blocked batches, and suggested purchase requests |
| 產能/人員 | Review required hours, available hours, line conflicts, changeover time, and staff gaps |
| 工單建議 | Show suggested work orders that can be created or need adjustment |

## Data Shape

Planning cases are shaped around:

- `sourceOrder`
- `customer`
- `product`, `itemNo`
- `quantity`, `unit`
- `dueDate`, `promisedDate`
- `decision`
- `planningNote`
- `materialShortageValue`
- `requiredProductionHours`
- `availableProductionHours`
- `purchaseRequestCount`
- `suggestedWorkOrderCount`
- `checks`
- `materials`
- `capacity`
- `workOrders`

## Workflow Basis

```txt
product_order
-> ATP/CTP commitment result
-> planning case
-> BOM explosion
-> production material request
-> inventory and batch availability check
-> purchase request / transfer / quality release suggestion
-> capacity and staff check
-> suggested work order
-> production scheduling
```

## Boundary With Other Workspaces

- Orders: owns customer promise, due date risk, margin, payment, and fulfillment risk.
- Planning / APS / Production Control: owns production material request, material demand explosion, capacity feasibility, scheduling, and work-order suggestions.
- Purchasing: owns actual purchase request approval, purchase order, delivery risk, and receiving.
- Production: owns finalized schedule, MES execution, efficiency, loss, and production quality.
- Warehouse: owns available stock, reservation, picking, location, and pallet capacity.
- Quality: owns release, hold, inspection, and quality blocking.

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| Source orders | `sale`, `product_order` |
| BOM explosion | `bom`, item master tables |
| Inventory and batch availability | `inventory`, warehouse tables |
| Purchase request suggestion | `purchase`, `inventory`, `bom` |
| Capacity and line availability | `aps`, `workorder`, `processorder`, production line tables |
| Staff availability | employee/workforce tables |
| Quality release blockers | quality-related tables, production quality data |
| Suggested work order creation | `workorder`, `processorder`, `aps` |

## First-Version Decisions

- Planning shows suggestions and blockers; it does not automatically create purchase orders or finalized work orders yet.
- Purchase request generation and work-order creation should be controlled actions in later versions.
- The first version emphasizes visibility and coordination, not full optimization.

## Deferred

- Automatic schedule optimization.
- Constraint solver.
- Automatic purchase request creation.
- Automatic work-order creation.
- Scenario simulation.
- Frozen schedule control.
- Multi-plant balancing.
