# ERP Warehouse Workspace Spec

日期：2026-05-22

Decision source:

- User answer: `1E, 2F, 3A, 4A, 5B`
- First workspace: Warehouse
- Primary user view: manager / overall management
- First version behavior: query, review, and workflow status only
- Excel baseline preference: `11.0` / `12.0` are newer and should take priority over `1.0` / `2.0`
- Next workflow after Warehouse: Production

## Purpose

Warehouse should become the first real frontend workspace because it is a practical operations control point and touches purchasing, production, inventory, traceability, and payment/storage cost.

The first version should not start with full CRUD. It should help management answer:

- What inventory do we have?
- Which batches are urgent or risky?
- Which inbound/outbound/warehouse records are pending?
- Which batch can be traced back to purchasing or production?
- Which records are creating warehouse/storage payment exposure?

## Workflow Basis

Warehouse is centered on this EWDB workflow segment:

```txt
purchase_order -> goods_receipt_note -> batch_number -> inventory_record -> warehouse_record -> warehouse_payment
work_order / process_order -> batch_number -> inventory_record -> production_data
product_order -> shipping_order -> shipping_record -> shipping_payment
```

Warehouse is not isolated. It must show whether stock came from purchasing, production, or another inventory movement.

## Primary Tables

| Purpose | Tables |
| --- | --- |
| Batch identity | `batch_number`, `batchno_serialno`, `batchno_serialno_group` |
| Inventory ledger | `inventory_record`, `inventory_order`, `inventory_delta` |
| Warehouse location/service | `ship_wh`, `ship_wh_alias`, `warehouse_record` |
| Storage/payment | `warehouse_payment`, `ship_wh_contract` |
| Purchasing source | `purchase_order`, `goods_receipt_note` |
| Production source | `work_order`, `process_order`, `production_data` |
| Shipping source | `shipping_order`, `shipping_record` |
| Item master | `material`, `inproduct`, `product`, `goods`, `trans_items` |

## Existing Excel/HTML Source Mapping

Relevant Excel/HTML areas:

- `3.0 選單`: 倉儲管理
- `3.0` sections: 倉儲設施, 盤點價格, 料品批號, 料品進出, 料品庫存, 存放週期, 倉租帳款
- `7.0 選單`: 料品追溯
- `11.0 選單`: newer master-data hierarchy for item and transaction setup

These should be consolidated into one daily workspace rather than exposed as many top-level tabs.

## Proposed Page Name

```txt
Warehouse 倉儲工作台
```

## Page Layout

```txt
Header
  Title: 倉儲工作台
  Search: batch no / item no / warehouse / source no
  Filters: warehouse, category, expiry risk, source type, date range

KPI Strip
  Total stock items
  Batches near expiry
  Pending inbound/outbound
  Low stock / shortage
  Storage charge risk

Main Split
  Left: Inventory and batch table
  Right: Selected batch/stock detail panel

Lower Panels
  Workflow timeline
  Related records
  Exception list
```

## First-Version Tabs

Keep the first version to four tabs.

| Tab | Purpose | Main Tables |
| --- | --- | --- |
| 庫存總覽 | Management view of stock by item and warehouse | `inventory_record`, `inventory_delta`, item masters |
| 批號效期 | Batch, expiry, source, and trace status | `batch_number`, `batchno_serialno` |
| 進出紀錄 | Inbound/outbound movement records | `inventory_record`, `warehouse_record`, `shipping_record` |
| 倉租帳款 | Storage-related records and payment exposure | `warehouse_record`, `warehouse_payment` |

Do not include full setup screens in this first page. Warehouse facilities and price setup should move to Master Data or Settings until needed for daily operations.

## Table Columns

### 庫存總覽

| UI Column | Source |
| --- | --- |
| 品項編號 | `item_no` |
| 品項名稱 | `item_name` |
| 類別 | `itemCategory`, item master |
| 倉庫 | `warehouse_no`, `warehouse_displayName` |
| 批號數 | derived from `batchNumber` |
| 目前數量 | `count` / aggregation |
| 單位 | `unit` |
| 金額 | `amount` |
| 狀態 | derived: normal / low / expiry / pending |

### 批號效期

| UI Column | Source |
| --- | --- |
| 批號 | `batch_number.no` |
| 來源類型 | `refCategory` |
| 來源單號 | `ref_no` |
| 品項 | `item_no`, `item_name` |
| 數量 | `checkedCount` / related inventory |
| 效期 | `validDate` |
| 倉庫 | related inventory/warehouse record |
| 追溯狀態 | derived |

### 進出紀錄

| UI Column | Source |
| --- | --- |
| 日期 | `date` |
| 樣式 | derived from `refCategory` / source |
| 來源單號 | `ref_no` |
| 批號 | `batchNumber` / `batch_no` |
| 倉庫 | `warehouse_no` |
| 品項 | `item_no`, `item_name` |
| 數量 | `count` |
| 金額 | `amount` |

### 倉租帳款

| UI Column | Source |
| --- | --- |
| 紀錄編號 | `warehouse_record.id` |
| 合約 | `contract_no` |
| 批號 | `batch_no` |
| 倉庫 | `sw_alias_no`, `sw_alias_name` |
| 存放天數 | `days` |
| 數量 | `count` |
| 倉租金額 | `warehouse_payment.amount` |
| 結算狀態 | derived |

## Selected Detail Panel

When the user selects a row, show:

- Batch number.
- Item name and category.
- Current quantity and unit.
- Warehouse location.
- Expiry date and risk label.
- Source type and source document.
- Related purchasing/production/shipping documents.
- Traceability shortcut.

## Workflow Timeline

Show a compact lane based on source type.

### Purchasing Source

```txt
purchase_order -> goods_receipt_note -> batch_number -> inventory_record -> warehouse_record -> warehouse_payment
```

### Production Source

```txt
work_order -> process_order -> batch_number -> inventory_record -> production_data
```

### Shipping Source

```txt
inventory_record -> shipping_order -> shipping_record -> shipping_payment
```

## First-Version States

Required states:

- Loading.
- Empty table.
- No selected row.
- DB/API unavailable.
- Data exists but workflow relationship missing.
- Expiry danger.
- Low stock warning.
- Storage/payment pending.

## API Needs

First version can start from mock/adapted data, but should shape data as if these API needs exist:

| Need | Candidate restserver Module |
| --- | --- |
| Inventory list | `inventory` |
| Batch list/detail | `batchnumber`, `batchtrace` |
| Warehouse records | `shipwarehouse` |
| Warehouse payments | `shipwarehouse`, `arap` |
| Goods receipt source | `purchase` |
| Production source | `workorder`, `work`, `processorder` |
| Shipping source | `sale`, `shipwarehouse` |

## Visual Direction

Use a calm ERP workspace design:

- No large hero section.
- No marketing layout.
- Dense table-first interface.
- Clear right detail panel.
- Status chips for expiry, low stock, pending, completed.
- Compact KPI strip.
- Icons only for common actions where possible.
- Stable table and panel dimensions.

The current `src/app/warehouse/page.tsx` can be evolved, but it should move away from card-only inventory display toward a table + detail + workflow workspace.

## Implementation Slice

Phase 1:

- Mock data shaped around real EWDB fields.
- Four tabs: 庫存總覽, 批號效期, 進出紀錄, 倉租帳款.
- Selectable table row.
- Right detail panel.
- Workflow timeline.
- KPI strip.

Phase 2:

- Add API adapter layer.
- Connect list endpoints.
- Add query filters.
- Add traceability shortcut.

Phase 3:

- Add create/edit actions only after backend workflow and permissions are stable.

## Open Decisions

1. Should Warehouse use one table with mode tabs, or separate table layouts per tab?
2. Should expiry risk be based on fixed 7/14/30 day thresholds?
3. Should storage charge risk be visible in the first version even if payment data is incomplete?
4. Should Traceability open inside Warehouse or navigate to a separate Traceability workspace?
