# EWDB 20260517 UNIQUE KEY Fix Report

日期：2026-05-17

## Rule

- 每個資料表最多保留一組 UNIQUE KEY。
- 若原始資料表有多組 UNIQUE KEY，合併為一組多欄位 composite unique key。
- 所有出現在 UNIQUE KEY 內的欄位均改為 NOT NULL。

## Output

- Input: `docs/database/EWDB_20260517.sql`
- Output: `docs/database/EWDB_20260517_UNIQUE_KEY_FIXED.sql`

## Summary

- Tables scanned: 75
- Tables with unique key: 68
- Tables without unique key: 7
- Tables originally having multiple unique keys: 39

## Table Detail

| Table | Original UNIQUE KEY count | New UNIQUE KEY count | Composite columns |
|---|---:|---:|---|
| `aps_quantity` | 5 | 1 | no, product_order_no, oneProcess, secProcess, item_no |
| `aps_quantity_item` | 4 | 1 | product_order_no, oneProcess, secProcess, item_no |
| `bank_account` | 1 | 1 | number |
| `batch_number` | 2 | 1 | no, ref_no |
| `batchno_serialno` | 3 | 1 | batch_number, serialNo, ref_order_no |
| `bom` | 2 | 1 | no, version |
| `bom_item` | 2 | 1 | bom_no, item_no |
| `bom1` | 3 | 1 | parent_no, child_id, weight |
| `bom1_number` | 1 | 1 | no |
| `bom2` | 0 | 0 |  |
| `bom2_number` | 1 | 1 | no |
| `company` | 2 | 1 | no, businessNo |
| `contract` | 2 | 1 | no, date |
| `employee` | 1 | 1 | no |
| `enterprise` | 2 | 1 | no, businessNo |
| `equipment` | 1 | 1 | no |
| `factory` | 0 | 0 |  |
| `goods` | 1 | 1 | no |
| `goods_receipt_note` | 1 | 1 | no |
| `inproduct` | 1 | 1 | no |
| `inproduct_bom_spec` | 4 | 1 | inproduct_no, item_no, item_version, bom12_no |
| `inventory_delta` | 4 | 1 | warehouse_displayName, date, timezone, specified_no |
| `Inventory_item_month_statistic` | 5 | 1 | warehouse_displayName, date, timezone, specified_no, specified_ref_no |
| `Inventory_month_statistic` | 3 | 1 | warehouse_displayName, date, timezone |
| `inventory_order` | 1 | 1 | no |
| `inventory_record` | 0 | 0 |  |
| `item_hours` | 2 | 1 | item_no, date |
| `item_loss` | 2 | 1 | item_no, date |
| `item_price` | 2 | 1 | item_no, date |
| `material` | 1 | 1 | no |
| `member` | 1 | 1 | user_no |
| `order_item_month_statistic` | 5 | 1 | date, kind, category, subCategory, specified_no |
| `order_payment` | 0 | 0 |  |
| `payment` | 4 | 1 | type, source, date, period |
| `pl_item_capacity` | 3 | 1 | month, pl_no, item_no |
| `pl_item_loss` | 2 | 1 | month, item_no |
| `pl_man_capacity` | 2 | 1 | month, pl_no |
| `process` | 1 | 1 | no |
| `process_capacity` | 3 | 1 | date, oneProcess, secProcess |
| `process_flow` | 3 | 1 | no, product_process_no, order |
| `process_labor` | 2 | 1 | work_order_no, employee_no |
| `process_order` | 1 | 1 | no |
| `product` | 1 | 1 | no |
| `product_bom_spec` | 3 | 1 | product_no, product_version, bom2_no |
| `product_order` | 1 | 1 | no |
| `product_process` | 3 | 1 | no, item_no, version |
| `product_spec` | 3 | 1 | product_no, product_version, item_no |
| `product_ver` | 3 | 1 | no, item_no, version |
| `production_data` | 1 | 1 | work_order_no |
| `production_data_input` | 6 | 1 | work_order_no, group, action, item_no, batch_number, serial_no |
| `production_data_labor` | 6 | 1 | work_order_no, employee_no, stationStage, action, startTime, endTime |
| `production_data_machine` | 3 | 1 | work_order_no, equipment_no, action |
| `production_data_output` | 7 | 1 | work_order_no, group, action, item_no, batch_number, serial_no, valid_date_no |
| `production_data_reuse` | 8 | 1 | work_order_no, process_order_no, group, action, item_no, category, batch_number, serial_no |
| `production_line` | 1 | 1 | no |
| `purchase_order` | 1 | 1 | no |
| `purchase_request` | 1 | 1 | no |
| `purchase_request_item` | 1 | 1 | purchase_request_no |
| `quotation` | 1 | 1 | no |
| `sample_price` | 2 | 1 | item_no, date |
| `session` | 0 | 0 |  |
| `ship_wh` | 1 | 1 | no |
| `ship_wh_alias` | 1 | 1 | no |
| `ship_wh_contract` | 2 | 1 | no, date |
| `ship_wh_quotation` | 2 | 1 | no, date |
| `shipping_order` | 1 | 1 | no |
| `shipping_payment` | 2 | 1 | no, date |
| `shipping_record` | 0 | 0 |  |
| `station` | 1 | 1 | no |
| `trans_items` | 1 | 1 | no |
| `trans_items2` | 1 | 1 | no |
| `user_group` | 1 | 1 | name |
| `warehouse_payment` | 2 | 1 | no, date |
| `warehouse_record` | 0 | 0 |  |
| `work_order` | 1 | 1 | no |
