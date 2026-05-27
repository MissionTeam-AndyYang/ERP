# ERP V1 System Integration Plan

Date: 2026-05-24
Baseline:

- Database: `docs/database/EWDB_20260526.sql`
- Workflow: `docs/database/EWDB_20260522_WORKFLOW.md`
- Frontend V1 pages: management-first ERP workspaces
- Backend location: `restserver/package`
- Backend API prefix observed in code: `/api/v1`

## 1. Integration Goal

The first integration phase should turn the approved V1 frontend screens from mock data into real operational read-only views first.

The goal is not to open all CRUD functions immediately. The safer goal is:

1. Confirm backend runtime and database schema are aligned.
2. Replace frontend mock data with backend read APIs module by module.
3. Build cross-module risk signals for the manager dashboard.
4. Introduce high-value write actions only after permissions, audit trail and workflow status rules are clear.

## 2. Confirmed Product Direction

The frontend V1 is aligned with the user's planning direction:

- Industry: ODM food processing factory.
- Interface: Web ERP, clear, professional, concise, easy to use and practical.
- Primary V1 users: executives and managers.
- Later users: operators, warehouse staff, quality inspectors, production staff and mobile/PDA users.
- Core business question: Can the company quote, accept, produce, ship and collect payment while controlling material, capacity, quality, warehouse and margin risk?

## 3. Approved V1 Workspaces

| Workspace | Route | V1 role |
| --- | --- | --- |
| Manager Dashboard | `/` | Daily cross-department coordination and fulfillment risk cockpit |
| R&D / Costing | `/rd` | Development request, formula/material selection, sample, BOM version, costing and nutrition label |
| Orders | `/orders` | Quotation, customer contract, formal order and ATP/CTP commitment risk |
| Planning / APS | `/planning` | Production material request, BOM explosion, capacity/staff check and schedule/work-order suggestion |
| Purchasing | `/purchasing` | Pre-order supplier sourcing/quote/contract and post-order mass-production purchasing |
| Warehouse | `/warehouse` | Inventory value, stock status, pallet/location capacity, inbound/outbound and expiry/turnover alerts |
| Quality | `/quality` | Material/item inspection, release/blocking, process/finished/pre-shipment quality status |
| Production | `/production` | Work order schedule, MES status, efficiency, loss, unit labor cost and QC signal |
| Traceability | `/traceability` | Batch, item, order, work-order and recall traceability |
| Logistics | `/logistics` | Shipment readiness, dispatch, cold chain, documents and POD |
| Finance | `/finance` | Estimated/actual margin, cost variance, billing readiness, AR/AP signals |
| Workforce | `/workforce` | Shift coverage, skill/certification readiness and labor risk |
| Settings / Master Data | `/settings` | Master data governance, permissions, integrations and localization |

Supporting pages such as `/items`, `/bom`, `/batches` and `/ai` exist but should not drive first integration unless needed by the above core flow.

## 4. Department Workflow Baseline

### Pre-order

```txt
Development request (R&D)
-> Formula/material selection (R&D)
-> Sample making (R&D)
-> Sample delivery (Sales)
-> Customer sample confirmation (Sales)
-> Supplier quotation/contract (Purchasing)
-> Costing and nutrition label (R&D)
-> Customer quotation/contract (Sales)
```

### Post-order

```txt
Order (Sales)
-> Production material request/scheduling (Production Control / Planning)
-> Material purchasing (Purchasing)
-> Arrival and inbound (Warehouse)
-> Material inspection (Quality)
-> Production (Manufacturing)
-> Quality release / warehouse outbound / logistics delivery
-> Finance billing and collection follow-up
```

## 5. Integration Phases

### Phase 0: Backend Readiness Check

Purpose:

Confirm the backend can run against the expected database and that the API modules needed by V1 are available.

Required checks:

- Runtime starts without import errors.
- DB connection can be established using `.env.example`-based settings.
- ORM/table count remains aligned with `EWDB_20260526.sql`.
- Required workflow tables are present.
- Existing API route list is documented.

Current note:

Previous engineer runtime output showed the backend can load the expected schema. Continue using `docs/backend/runtime-verification/` for engineer output, but raw result files should be reviewed before committing.

### Phase 1: Read-only Module Integration

Purpose:

Replace frontend mock data with backend GET endpoints while preserving the approved V1 screens.

Recommended order:

1. Warehouse
2. Orders
3. Production
4. Quality
5. Purchasing
6. Planning / APS
7. Traceability
8. Logistics
9. Finance
10. R&D / Costing
11. Workforce
12. Settings / Master Data

Reason:

Warehouse, orders, production and quality provide the fastest validation for daily operating risk. R&D/costing and settings are important but can integrate after the daily flow is readable.

### Phase 2: Cross-module Blocking Signals

Purpose:

Make the system behave like one ERP instead of separate pages.

Priority links:

- Quality hold -> Warehouse available inventory and Logistics shipment readiness
- Material shortage -> Planning, Purchasing and Production risk
- Warehouse capacity shortage -> Purchasing arrival planning and Logistics outbound priority
- Work order completion -> Quality, Warehouse and Logistics updates
- POD completion -> Finance billing readiness
- Supplier quotation/contract -> R&D costing and customer quotation basis
- Customer contract -> Formal order, Planning and Finance

### Phase 3: Controlled Write Actions

Purpose:

Open a small number of real actions that create high operational value.

Recommended first write actions:

1. Manager acknowledgement / note on high-risk order
2. Planning suggestion converted to purchase request
3. Planning suggestion converted to work order
4. Quality release / hold / quarantine decision
5. Warehouse inbound/outbound confirmation
6. Logistics dispatch update and POD upload/status
7. Finance billing-ready flag
8. R&D quotation BOM approval
9. Supplier quotation/contract status update
10. Customer quotation/contract status update

Each write action requires:

- Permission rule
- Status transition rule
- Audit log
- Clear rollback/correction rule

### Phase 4: Operator Workflow and Mobile/PDA

Purpose:

Move from management visibility into shop-floor execution.

Candidate workflows:

- Warehouse receiving and location assignment
- Material picking and outbound confirmation
- Quality inspection result entry
- Production reporting / MES task update
- Logistics loading and POD confirmation

These should be designed after manager and department views are connected to real data.

## 6. Manager Dashboard Integration Priority

Manager Dashboard should be integrated as an aggregated view rather than as an isolated module.

Suggested data groups:

- Fulfillment risk summary
- Today decision queue
- Cross-department blockers
- Today work queue
- Pre-order pipeline
- Production and quality signals
- Warehouse capacity and inventory risk
- Margin and billing readiness signals

Short-term implementation:

- Frontend can assemble dashboard data from module APIs.

Long-term implementation:

- Backend should provide summary endpoints such as:
  - `/api/v1/dashboard/manager/summary`
  - `/api/v1/dashboard/manager/decisions`
  - `/api/v1/dashboard/manager/blockers`
  - `/api/v1/dashboard/manager/workqueue`
  - `/api/v1/dashboard/manager/preorder`

These dashboard endpoints do not exist yet in the observed backend route list, so they should be treated as proposed aggregation endpoints.

## 7. Role and Permission Draft

| Role | V1 access focus | Write permissions in early integration |
| --- | --- | --- |
| Executive | Dashboard, Finance, Orders, Warehouse value, Production risk | Read-only first; later approve high-level exceptions |
| Plant Manager | Dashboard, Planning, Production, Warehouse, Quality, Logistics, Workforce | Acknowledge risks, coordinate decisions |
| Sales Manager | Orders, pre-order customer quotation/contract, delivery commitment | Quotation/contract status, order notes |
| R&D Manager | R&D / Costing, BOM/cost/nutrition label | Approve quotation BOM and costing basis |
| Planning Manager | Planning / APS, Production, Purchasing readiness | Convert suggestions to purchase request/work order after approval |
| Purchasing Manager | Purchasing, supplier quote/contract, arrival risk | Supplier quote/contract and purchase status updates |
| Warehouse Manager | Warehouse, inventory, locations, inbound/outbound | Inbound/outbound/location confirmation |
| Quality Manager | Quality, release/blocking, inspection status | Release/hold/quarantine decisions |
| Production Manager | Production, work orders, MES, efficiency/loss | Work-order execution status and production notes |
| Logistics Manager | Logistics, shipment readiness, POD | Dispatch status and POD status |
| Finance Manager | Finance, margin, billing, AR/AP | Billing-ready and AR/AP status updates |
| System Admin | Settings, users, permissions, master data | Master data, permission and integration settings |

## 8. Status Vocabulary

Use consistent status language across modules.

Recommended V1 status levels:

| Level | Meaning | UI tone |
| --- | --- | --- |
| Normal | No action needed | Success |
| Attention | Needs monitoring, not blocking yet | Info |
| Warning | Needs owner follow-up soon | Warning |
| Blocking | Prevents production, shipment, billing or commitment | Danger |
| Pending | Waiting for upstream decision or document | Neutral / Info |
| Released | Approved for next step | Success |
| Hold | Temporarily blocked by quality, material, contract or manager decision | Warning / Danger |

## 9. Action Classification

Every button or operation should be marked before backend integration:

| Class | Meaning | Example |
| --- | --- | --- |
| Placeholder | UI preview only, no backend call | "View analysis" in early mock |
| Read-only action | Opens detail, filters table, downloads existing data | View order, filter high-risk orders |
| Controlled mutation | Updates status or creates workflow record | Quality release, dispatch status |
| High-risk mutation | Changes contract, financial or production commitment | Approve customer contract, create work order |

V1 should avoid opening high-risk mutations until permission and audit rules are implemented.

## 10. Recommended Next Tasks

1. Confirm the API field mapping document with the engineer.
2. Ask the engineer to identify which existing endpoints already return the fields needed by Warehouse V1.
3. Integrate Warehouse as the first read-only real-data page.
4. Then integrate Orders and Production read-only views.
5. Build dashboard aggregation after at least Warehouse, Orders, Production and Quality are readable from backend data.

## 11. Current Decision

Frontend V1 screen design is considered stable enough for integration planning. The next engineering focus should be API and data mapping, not adding more large pages.
