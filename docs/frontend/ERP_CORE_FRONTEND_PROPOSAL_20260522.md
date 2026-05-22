# ERP Core Frontend Proposal

日期：2026-05-22

Basis:

- `docs/database/EWDB_20260522.sql`
- `docs/database/EWDB_20260522_WORKFLOW.md`
- `docs/frontend/恆旺_ERP_Web介面.xlsx`
- `docs/frontend/恆旺_ERP_Web Markup.html`
- `restserver/package`

## Goal

Build a simplified, clear, attractive, and easy-to-operate ERP frontend that uses the Excel/HTML work as a screen inventory, but reorganizes it around the actual EWDB workflow.

The new frontend should not expose every Excel tab as top-level UI. It should guide users through the core factory workflows first, while preserving detailed master-data screens where they are needed.

## Design Principles

1. Workflow first, not table first.
2. `product_order` is the main operational pivot.
3. Each workspace should show list, detail, status, and next action in one place.
4. Keep dense ERP information, but make it scannable.
5. Use consistent page structure across modules.
6. Keep master data and setup screens available, but out of the first-level daily workflow.
7. Make backend integration easier by mapping each screen to a small set of APIs.

## Proposed Navigation

```txt
Dashboard
Orders
Purchasing
Production
Warehouse
Traceability
Master Data
Settings
```

## Workspace Model

Each core workspace should use the same layout pattern:

```txt
Top band:
  Page title, date/filter/search, primary action

KPI strip:
  3 to 5 compact metrics for this workspace

Main area:
  Left or center: primary data table
  Right: selected record summary and workflow status

Lower area:
  Related documents, timeline, exceptions, or detail tabs
```

This gives repeated ergonomics:

- Find a record.
- Select it.
- See status.
- See related documents.
- Take the next action.

## Core Screens

### 1. Dashboard

Purpose: daily operating overview.

Shows:

- Today's sales orders.
- Purchasing status.
- Production status.
- Warehouse and batch alerts.
- Shipping/payment exceptions.

Primary data:

- `product_order`
- `purchase_request`
- `purchase_order`
- `goods_receipt_note`
- `work_order`
- `inventory_record`
- `shipping_order`

Recommended panels:

- Orders due soon.
- Production in progress.
- Low/aging inventory.
- Receiving pending inspection.
- Shipments pending.
- Workflow exceptions.

### 2. Orders

Purpose: manage customer demand and see the three downstream flows.

Workflow center:

```txt
contract -> product_order
product_order -> purchase_request
product_order -> aps_quantity -> work_order
product_order -> shipping_order
```

Main table:

- Sales orders from `product_order`.

Right detail:

- Order summary.
- Customer/company.
- Item.
- Quantity.
- Expected date.
- Contract reference.

Workflow status:

- Purchasing: request/order/receipt/batch/inventory.
- Production: APS/work order/process/production data.
- Shipping: shipping order/record/payment.

Tabs:

- Related purchasing.
- Related production.
- Related shipping.
- Documents/history.

### 3. Purchasing

Purpose: handle material demand, purchase orders, receiving, and warehouse handoff.

Workflow:

```txt
purchase_request -> purchase_order -> goods_receipt_note -> batch_number -> inventory_record -> warehouse_record -> warehouse_payment
```

Main table modes:

- Purchase requests.
- Purchase orders.
- Goods receipt notes.

Right detail:

- Supplier.
- Item.
- Quantity.
- Expected date.
- Receiving status.
- Batch status.

Primary actions:

- Create purchase order from request.
- Record receiving.
- Create or link batch number.
- Send to inventory.

### 4. Production

Purpose: plan and execute production.

Workflow:

```txt
product_order -> aps_quantity -> work_order -> batch_number -> process_order -> process_labor
process_order -> inventory_record -> production_data
```

Main table modes:

- APS demand.
- Work orders.
- Process orders.
- Production data.

Right detail:

- Product order link.
- Work order status.
- Production line.
- Batch.
- Process progress.

Detail tabs:

- Inputs.
- Outputs.
- Reuse.
- Machine.
- Labor.

Primary actions:

- Create work order.
- Start process.
- Record production data.
- Close work order.

### 5. Warehouse

Purpose: see stock, batches, warehouse records, and warehouse payments.

Workflow:

```txt
batch_number -> inventory_record -> warehouse_record -> warehouse_payment
```

Main table modes:

- Inventory by item.
- Inventory by batch.
- Warehouse records.
- Warehouse aging/storage.

Right detail:

- Batch number.
- Item.
- Quantity.
- Warehouse alias.
- Expiry date.
- Source reference.

Primary actions:

- Adjust inventory.
- View batch trace.
- Create warehouse record.
- Review storage charges.

### 6. Traceability

Purpose: trace a batch through material, production, warehouse, and shipping.

Search first:

- Batch number.
- Item number.
- Product order number.
- Work order number.

Trace sections:

- Source document.
- Batch details.
- Inventory records.
- Production inputs and outputs.
- Shipping records.

Trace rules:

- `batch_number.ref_no` is polymorphic and must be interpreted with source category/context.
- Trace should support both material-to-product and product-to-material directions.

### 7. Master Data

Purpose: keep detailed setup data accessible without crowding daily workflows.

Includes:

- Company.
- Payment/bank account.
- Material.
- Inproduct.
- Product.
- Goods.
- Transaction items.
- Quotation.
- Contract.
- Shipping warehouse.
- Production line/process/station/equipment.

Source mapping:

- Most `1.0`, `2.0`, `11.0`, and `12.0` Excel screens belong here.

### 8. Settings

Purpose: system and configuration screens.

Includes:

- Users.
- Groups.
- Device.
- Session.
- Runtime/API settings.

## User Review Decisions

Recorded on 2026-05-22:

| Question | Decision |
| --- | --- |
| First core page | Warehouse |
| First-version user view | Manager / overall management |
| First-version behavior | Query, review, and workflow status first |
| Excel baseline | `11.0` and `12.0` should be treated as newer and preferred over `1.0` and `2.0` |
| Next workflow | Production |

## First Implementation Slice

Recommended first slice:

```txt
Warehouse workspace
```

Reason:

- It gives management an immediate operating view of stock, batches, expiry, movement, and warehouse cost exposure.
- It touches purchasing, production, shipping, inventory, and traceability without requiring write actions in the first version.
- It is a good read-only/status-first screen while backend review and DB alignment continue.

Minimum Warehouse page:

- KPI strip.
- Inventory/batch table.
- Selected stock or batch detail panel.
- Workflow timeline showing purchasing/production/shipping source.
- Related warehouse/payment records.
- Empty/loading/error states.

## API Mapping Priorities

| Priority | UI Need | Tables / Modules |
| --- | --- | --- |
| P0 | List and view sales orders | `product_order`, `sale` |
| P0 | Show order workflow status | `purchase_request`, `purchase_order`, `goods_receipt_note`, `batch_number`, `aps_quantity`, `work_order`, `shipping_order` |
| P1 | Purchasing drilldown | `purchase`, `inventory`, `batchnumber` |
| P1 | Production drilldown | `aps`, `workorder`, `work`, `processorder` |
| P1 | Shipping drilldown | `sale`, `shipwarehouse` |
| P2 | Master-data maintenance | `company`, `material`, `product`, `transitems`, `contract`, `quotation` |

## Visual Direction

The UI should feel like a work-focused ERP, not a marketing page.

Recommended style:

- Calm neutral background.
- Dense but readable tables.
- Clear status colors.
- Compact KPI tiles.
- Right-side detail panel.
- Timeline/workflow chips.
- Consistent icons for actions.
- Avoid large decorative sections.

Use cards only for repeated records, panels, and detail blocks. Do not nest cards inside cards.

## Relationship To Existing Excel/HTML

The existing Excel/HTML remains the detailed UI inventory.

The new frontend should:

- Preserve the field vocabulary.
- Preserve operational concepts such as `內容`, `資訊`, `新增`, `刪除`.
- Preserve important business notes marked with `**`.
- Reduce first-level navigation complexity.
- Convert tab-heavy screens into workflow workspaces.
- Move detailed setup screens into Master Data.

## Questions For User Review

1. Should `Orders` be the first real page, or should `Dashboard` come first?
2. In daily work, who uses the first version most: owner/manager, sales, purchasing, production, or warehouse?
3. Should the first UI focus on read-only workflow visibility, or include create/edit actions immediately?
4. Are `11.0` and `12.0` intended to replace `1.0` and `2.0`, or are they alternative experiments?
5. Which workflow is most urgent after Orders: Purchasing, Production, Warehouse, or Traceability?

## Proposed Next Steps

1. User reviews this proposal and answers the questions above.
2. Build a small frontend spec for the first page.
3. Implement the first Next.js screen using mock/adapted data.
4. Map the screen to restserver APIs.
5. Replace mock data with real API calls once backend review fixes are ready.
