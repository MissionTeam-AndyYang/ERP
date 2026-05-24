# ERP V1 Frontend Acceptance Checklist

Date: 2026-05-25
Purpose: Define the first-version frontend acceptance checklist for manager and management-role screens while backend APIs are being implemented.

## Design Goal

The V1 interface should support an ODM food processing factory with a clear, professional, concise and practical web operation style.

Primary roles for V1:

- Business owner / executive: understand fulfillment risk, production feasibility, inventory value, margin and collection status.
- Manager: identify blockers across Warehouse, Orders, Production, Quality, Planning, Purchasing, Logistics, Finance, R&D, Workforce, Traceability and Settings.
- Operator: later phase; V1 should not block future operator workflow screens.

## Global Acceptance Rules

| Area | Acceptance criteria |
| --- | --- |
| Layout | Each page opens directly into the work surface, not a marketing page. |
| Navigation | Core modules are reachable from the manager dashboard and side navigation. |
| Density | Information is scan-friendly and operational; no unnecessary decorative sections. |
| Status language | Risk, warning, success and neutral states are visually distinct and textually clear. |
| Empty state | If API data is unavailable, page must remain usable with mock fallback or explicit empty state. |
| Loading state | Page must not jump or collapse while loading. |
| Error state | API failure should not break the page; user sees fallback/source indication where applicable. |
| Responsiveness | Desktop and mobile layouts must not overlap text, controls or cards. |
| I18N readiness | Display labels should be centralized enough to support future multi-language switching. |
| Role fit | V1 pages prioritize executive/manager decisions over high-frequency operator transactions. |

## Manager Dashboard

| Focus | Acceptance criteria |
| --- | --- |
| Fulfillment risk | Shows delivery commitment, production feasibility and blockers before secondary metrics. |
| Decision queue | Highlights items that require management decision with owner, due time, impact and action. |
| Cross-module blockers | Connects Warehouse, Orders, Production, Quality, Planning, Purchasing, Logistics and Finance signals. |
| Today work | Shows today tasks without overwhelming the dashboard. |
| Trends | Production, OEE, quality and alert distribution are readable and do not dominate the screen. |
| Shortcut behavior | Module shortcuts lead to the expected workspace pages. |

## Warehouse

| Focus | Acceptance criteria |
| --- | --- |
| Inventory value | Shows value by raw material, supplies, film/roll, WIP and finished goods categories. |
| Space usage | Shows used pallet positions and available space by warehouse/storage area. |
| Rotation warning | Highlights items with turnover cycle over one month. |
| Shelf-life warning | Highlights items with less than one-third shelf life remaining, excluding supplies and film/roll categories. |
| Safety stock | Highlights items below safety level. |
| Pending work | Shows today's unprocessed inbound and outbound tasks. |
| Drill-down readiness | Risk alerts and pending tasks should be structured so a detail drawer/page can be added later. |

## Orders

| Focus | Acceptance criteria |
| --- | --- |
| Fulfillment priority | Delivery and production feasibility are shown before margin and collection signals. |
| Risk management | Orders expose delivery risk, material risk, production risk and quality/shipment blockers. |
| Commercial status | Estimated margin, actual margin and payment/collection status are available as secondary fields. |
| Pre-order link | Development/sample/quotation status can be connected later from R&D, Purchasing and Sales flow. |

## Production

| Focus | Acceptance criteria |
| --- | --- |
| Schedule view | Shows work orders by date and production line/process perspective. |
| Weekly focus | Recent-week schedule can expose material and staff readiness. |
| Capacity signal | Shows available capacity by process line so sales/order planning can see feasibility. |
| MES status | Shows today's work-order production status. |
| Efficiency | Shows production time efficiency, material loss and labor cost/unit indicators. |
| Quality signal | Production cards include first article, in-process inspection or quality decision state. |

## Quality

| Focus | Acceptance criteria |
| --- | --- |
| Inspection queue | Shows material/product inspections by source: receiving, production and pre-shipment. |
| Release/hold | Clearly identifies what blocks inventory release, production continuation or shipment. |
| NCR readiness | Nonconformance/rework/scrap state can be shown or extended later. |
| Documents | Inspection documents/certificates can be tracked for missing or incomplete status. |

## Planning / APS

| Focus | Acceptance criteria |
| --- | --- |
| Order feasibility | Converts accepted orders into material, capacity, staff and work-order checks. |
| Material demand | Shows shortage quantity, required date and suggested action. |
| Capacity demand | Shows required hours, available hours, staff requirement and bottleneck process. |
| Work-order suggestion | Shows planned work orders and whether they can be scheduled. |

## Purchasing

| Focus | Acceptance criteria |
| --- | --- |
| Development purchasing | Supports supplier quote/contract after sample confirmation. |
| Mass-production purchasing | Supports purchase requests, purchase orders, arrival risk and receiving status. |
| Price control | Shows price variance and supplier contract status where available. |
| Receiving link | Connects purchase arrival to Warehouse inbound and Quality inspection. |

## Logistics

| Focus | Acceptance criteria |
| --- | --- |
| Shipment readiness | Shows whether finished goods, quality release, documents and dispatch are ready. |
| Delivery execution | Shows shipment status, carrier/dispatch and proof-of-delivery readiness. |
| Billing readiness | Indicates whether logistics/shipment completion can trigger billing or collection workflow. |

## Finance

| Focus | Acceptance criteria |
| --- | --- |
| Margin | Shows estimated and actual margin as secondary priority after delivery feasibility. |
| Cost variance | Exposes material, production or logistics cost variance where available. |
| AR/AP | Shows receivable/payable and collection/payment risk. |
| Billing blockers | Links missing shipment, quality or document status to billing readiness. |

## R&D / Costing

| Focus | Acceptance criteria |
| --- | --- |
| Development flow | Supports development request, formula material selection, trial sample, customer sample selection and costing. |
| BOM control | Shows BOM/formula version, approval status and change impact. |
| Costing | Supports production cost estimation for quotation management. |
| Nutrition label | Tracks nutrition label readiness as part of customer quotation/contract preparation. |

## Workforce

| Focus | Acceptance criteria |
| --- | --- |
| Staff readiness | Shows whether scheduled production has enough assigned staff. |
| Skill fit | Exposes missing skills/certifications where data exists. |
| Line readiness | Connects labor readiness to production line schedule. |

## Traceability

| Focus | Acceptance criteria |
| --- | --- |
| Batch chain | Connects material lots, production batches, inventory movement and shipped orders. |
| Recall scope | Can identify affected customers/orders from a batch. |
| Hold/release | Shows whether batch status blocks inventory or shipment. |

## Settings / Master Data

| Focus | Acceptance criteria |
| --- | --- |
| Master data health | Shows item, BOM, warehouse, line and customer/supplier data quality issues. |
| Governance | Shows permission/role or approval-flow readiness where available. |
| Localization | Keeps language and display settings ready for future multi-language support. |
| Integration health | Shows API/system connection state when backend provides it. |

## Page Acceptance Procedure

For each page before marking it accepted:

1. Open the page on desktop viewport.
2. Open the page on mobile viewport.
3. Confirm loading, API failure and fallback behavior.
4. Confirm all primary V1 user concerns are visible without unrelated distractions.
5. Confirm action labels and status wording match management language.
6. Confirm the page can later receive real API data without redesigning its information structure.

## Current V1 Acceptance Status

| Page | Status | Note |
| --- | --- | --- |
| Manager Dashboard | `ready_for_api_validation` | Frontend service layer exists with mock fallback. |
| Warehouse | `ready_for_api_validation` | First backend implementation target. |
| Orders | `ready_for_api_validation` | Depends on sale/order/quotation/contract mapping. |
| Production | `ready_for_api_validation` | Depends on workorder/MES/quality signal mapping. |
| Quality | `ready_for_api_validation` | Dedicated backend model likely required. |
| Planning / APS | `ready_for_api_validation` | Depends on APS, BOM and inventory mapping. |
| Purchasing | `ready_for_api_validation` | Covers development and mass-production purchasing concerns. |
| Logistics | `ready_for_api_validation` | POD/cold-chain fields require backend confirmation. |
| Finance | `ready_for_api_validation` | Margin and AR/AP source-of-truth require backend confirmation. |
| R&D / Costing | `ready_for_api_validation` | Dedicated development/project fields likely required. |
| Workforce | `ready_for_api_validation` | Employee/skill/certification source requires confirmation. |
| Traceability | `ready_for_api_validation` | Depends on batchtrace and inventory movement mapping. |
| Settings / Master Data | `ready_for_api_validation` | Governance/localization/integration fields require confirmation. |

