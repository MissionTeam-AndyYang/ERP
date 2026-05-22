# ERP Core Frontend Proposal

日期：2026-05-22

## Current Baseline

來源基準：

- `docs/database/EWDB_20260522.sql`
- `docs/database/EWDB_20260522_WORKFLOW.md`
- `docs/frontend/恆旺_ERP_Web介面.xlsx`
- `docs/frontend/恆旺_ERP_Web Markup.html`
- `restserver/package`

已實作並推送到 `main`：

- Warehouse workspace: `src/app/warehouse/page.tsx`
- Production workspace: `src/app/production/page.tsx`
- ESLint 9 / Next 16 lint baseline: `eslint.config.mjs`

## Goal

建立一個簡化、清晰、好看、易操作的 ERP 前端。Excel/HTML 應作為畫面與欄位盤點來源，但新的前端不應直接把所有 Excel 分頁變成一層層選單，而是以 EWDB workflow 為核心重整。

## User Decisions

| Question | Decision |
| --- | --- |
| First core page | Warehouse |
| First-version user view | Manager / overall management |
| First-version behavior | Query, review, and workflow status first |
| Excel baseline | `11.0` and `12.0` are newer and preferred over `1.0` and `2.0` |
| Next workflow | Production |

## Design Principles

1. Workflow first, not table first.
2. Use table + selected detail + workflow status as the repeated workspace pattern.
3. Keep ERP data dense, but make it scannable.
4. Start with query/review/status before create/edit actions.
5. Map each screen to a small set of backend APIs.
6. Keep master data and setup screens outside the first-level daily workflow.

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

## Standard Workspace Pattern

```txt
Header:
  Title, status badges, search, filters, primary action

KPI strip:
  3 to 5 compact metrics

Main split:
  Left: primary table / mode tabs
  Right: selected record detail and workflow timeline

Lower panels:
  Exceptions, related records, schedule, alerts, or trace links
```

## Implemented Core Workspaces

### Warehouse

Purpose: management view for stock, batches, movement, expiry, and warehouse cost exposure.

Current first-version tabs:

- 庫存總覽
- 批號效期
- 進出紀錄
- 倉租帳款

Primary data shape:

- Batch number
- Item number/name/category
- Warehouse number/name
- Source type/source document
- Quantity/unit/amount
- Expiry and storage charge status
- Related workflow and documents

### Production

Purpose: management view for work orders, material readiness, quality handoff, and production line load.

Current first-version tabs:

- 工單總覽
- 備料狀態
- 品檢入庫
- 產線產能

Primary data shape:

- Work order and product
- Batch number
- Production line and schedule window
- Source sales order and BOM
- Planned/completed quantity
- Material and quality status
- Related workflow and documents

## API Mapping Priorities

| Priority | UI Need | Candidate Modules / Tables |
| --- | --- | --- |
| P0 | Warehouse inventory and batch list | `inventory_record`, `batch_number`, `warehouse_record` |
| P0 | Production work order list | `work_order`, `process_order`, `production_data` |
| P0 | Workflow status summary | `purchase_order`, `goods_receipt_note`, `aps_quantity`, `shipping_order` |
| P1 | Material readiness | `bom`, `inventory_record`, `purchase_request` |
| P1 | Quality and finished-goods handoff | `production_data`, `inventory_record`, `batch_number` |
| P1 | Traceability | `batch_number`, purchase/production/shipping source refs |
| P2 | Master-data maintenance | `company`, `material`, `product`, `trans_items`, `contract`, `quotation` |

## Relationship To Excel/HTML

The existing Excel/HTML remains the detailed UI inventory. The new frontend should:

- Preserve field vocabulary.
- Preserve operational concepts such as 內容, 資訊, 新增, 刪除.
- Preserve important business notes marked with `**`.
- Convert tab-heavy screens into workflow workspaces.
- Move setup-heavy screens into Master Data or Settings.

## Next Suggested Work

1. Map Warehouse mock data to restserver API response shape.
2. Map Production mock data to restserver API response shape.
3. Add Traceability as the cross-workflow search page.
4. Add Orders or Purchasing after backend review confirms endpoint readiness.
