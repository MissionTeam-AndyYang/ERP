# ERP Manager Dashboard V1 Spec

Date: 2026-05-23
Baseline: Management-first ERP V1 for ODM food processing factory

## Purpose

Manager Dashboard V1 is the first screen for department managers and plant supervisors. It should answer one question quickly:

> What needs coordination today so orders can be fulfilled on time, within margin, and without quality or warehouse risk?

This dashboard is not an executive-only financial summary and not a pure production status board. It is a cross-department operating cockpit.

## Primary Users

- Plant manager
- Production control manager
- Warehouse manager
- Quality manager
- Purchasing manager
- Sales/order manager
- R&D/costing manager

Operator-level task screens will remain inside each module.

## First Screen Information Priority

1. Fulfillment risk and delivery commitment
2. Today decisions requiring manager action
3. Cross-department blockers
4. Pre-order development/quotation pipeline
5. Production, quality, warehouse, purchasing, logistics and finance signals

## V1 Sections

### 1. Manager Hero Summary

Shows:

- Fulfillment risk count
- Delivery commitment rate
- Estimated margin signal
- Collection/cash signal
- Quick links to key modules

Module links:

- Orders
- Planning / APS
- Purchasing
- Warehouse
- Quality
- Production
- Logistics
- Finance

### 2. Manager Focus KPIs

V1 metrics:

- Fulfillment risk
- Today's delivery commitment
- Estimated margin
- Manager decision queue

These metrics should be clickable in later versions and filter the relevant work queues.

### 3. Decision Center

Purpose:

Show items that require manager approval or coordination today.

Examples:

- Rush order insertion into production line
- Supplier substitute material release
- Warehouse overflow / consignment decision

Suggested backend data sources:

- Orders and order commitment checks
- Planning / APS schedule suggestions
- Purchasing supplier/quote records
- Quality inspection release status
- Warehouse capacity status

### 4. Today Work Queue

Purpose:

Give managers a time-based view of cross-module tasks that may block today.

Examples:

- Order commitment confirmation
- Warehouse location reservation
- Material inspection release
- Production completion confirmation
- Shipment document readiness

### 5. Department Blockers

Purpose:

Highlight cross-department items that cannot be solved inside a single module.

V1 blocker categories:

- R&D / Sales: samples and customer selection pending
- Planning: material or capacity shortage for scheduled work orders
- Purchasing: supplier quote or contract price differences
- Warehouse / Quality: inspected materials occupying warehouse space

### 6. Pre-order Pipeline

Purpose:

Reflect ODM pre-order workflow before formal sales order creation.

Workflow baseline:

Development request (R&D) -> Formula/material selection (R&D) -> Sample making (R&D) -> Sample delivery (Sales) -> Customer sample confirmation (Sales) -> Supplier quotation/contract (Purchasing) -> Costing and nutrition label (R&D) -> Customer quotation/contract (Sales)

V1 stages:

- Development request
- Sample making / sample delivery
- Supplier quotation
- Customer quotation

### 7. Operational Charts and Signals

Retained from existing dashboard foundation:

- Production plan vs actual
- OEE trend
- Alert distribution
- Quality yield trend
- Production line status
- Alert center

These are secondary on the manager dashboard because they support decisions rather than define the entire homepage.

## Data Integration Notes

The manager dashboard should not duplicate each module's full detail. It should consume summarized API views or aggregated endpoints.

Suggested V1 API groups:

- `/dashboard/manager/summary`
- `/dashboard/manager/focus-kpis`
- `/dashboard/manager/decisions`
- `/dashboard/manager/work-queue`
- `/dashboard/manager/blockers`
- `/dashboard/manager/pre-order-pipeline`
- `/dashboard/manager/operations`

If backend implementation starts module-by-module, the dashboard can initially call each module endpoint and aggregate on the frontend. Long term, backend summary endpoints are preferred.

## Open Items

- Confirm whether the first dashboard role should be named "Manager Dashboard", "Plant Manager Dashboard", or "Management Dashboard".
- Define which alerts require explicit manager acknowledgement.
- Define how many days the dashboard should look ahead for delivery and material risk. Recommended V1 default: today + next 7 days.
- Define whether finance signals should show estimated gross margin only, or include accounts receivable status on the same screen.

## Implementation Status

- V1 page implemented at `/`.
- Mock data implemented in `src/mock/dashboard.ts`.
- Types implemented in `src/types/dashboard.ts`.
- Existing production and chart components are reused where appropriate.
