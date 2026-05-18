-- EWDB Core FK Migration Draft
-- Date: 2026-05-16
-- Source: EWDB_WORD_CONVERTED_SCHEMA_20260515_R01.sql
--
-- Purpose:
-- 1. Validate orphan records before adding FK constraints.
-- 2. Provide first-batch FK constraints for the Phase 2 MVP workflow.
--
-- Important:
-- This file is a review draft. Do not run the ALTER TABLE section until every validation query returns zero rows.

SET NAMES utf8mb4;

-- ============================================================
-- 1. Orphan validation queries
-- ============================================================

-- Master data
SELECT 'member.user_no -> employee.no' AS check_name, child.user_no
FROM member child
LEFT JOIN employee parent ON parent.no = child.user_no
WHERE child.user_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'trans_items.company_no -> company.no' AS check_name, child.company_no
FROM trans_items child
LEFT JOIN company parent ON parent.no = child.company_no
WHERE child.company_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'production_line.factory_no -> factory.no' AS check_name, child.factory_no
FROM production_line child
LEFT JOIN factory parent ON parent.no = child.factory_no
WHERE child.factory_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'production_line.process_no -> process.no' AS check_name, child.process_no
FROM production_line child
LEFT JOIN process parent ON parent.no = child.process_no
WHERE child.process_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'equipment.station_no -> station.no' AS check_name, child.station_no
FROM equipment child
LEFT JOIN station parent ON parent.no = child.station_no
WHERE child.station_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

-- BOM
SELECT 'bom_item.bom_no -> bom.no' AS check_name, child.bom_no
FROM bom_item child
LEFT JOIN bom parent ON parent.no = child.bom_no
WHERE child.bom_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'bom_item.item_no -> material.no' AS check_name, child.item_no
FROM bom_item child
LEFT JOIN material parent ON parent.no = child.item_no
WHERE child.item_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'product_bom_spec.product_no -> product.no' AS check_name, child.product_no
FROM product_bom_spec child
LEFT JOIN product parent ON parent.no = child.product_no
WHERE child.product_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

-- Order and procurement
SELECT 'contract.ref_no -> quotation.no' AS check_name, child.ref_no
FROM contract child
LEFT JOIN quotation parent ON parent.no = child.ref_no
WHERE child.ref_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'product_order.ref_no -> contract.no' AS check_name, child.ref_no
FROM product_order child
LEFT JOIN contract parent ON parent.no = child.ref_no
WHERE child.ref_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'product_order.item_ref_no -> company.no' AS check_name, child.item_ref_no
FROM product_order child
LEFT JOIN company parent ON parent.no = child.item_ref_no
WHERE child.item_ref_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'product_order.item_no -> trans_items.no' AS check_name, child.item_no
FROM product_order child
LEFT JOIN trans_items parent ON parent.no = child.item_no
WHERE child.item_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'shipping_order.product_order_no -> product_order.no' AS check_name, child.product_order_no
FROM shipping_order child
LEFT JOIN product_order parent ON parent.no = child.product_order_no
WHERE child.product_order_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'purchase_request.product_order_no -> product_order.no' AS check_name, child.product_order_no
FROM purchase_request child
LEFT JOIN product_order parent ON parent.no = child.product_order_no
WHERE child.product_order_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'purchase_request_item.purchase_request_no -> purchase_request.no' AS check_name, child.purchase_request_no
FROM purchase_request_item child
LEFT JOIN purchase_request parent ON parent.no = child.purchase_request_no
WHERE child.purchase_request_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'purchase_order.purchase_request_no -> purchase_request.no' AS check_name, child.purchase_request_no
FROM purchase_order child
LEFT JOIN purchase_request parent ON parent.no = child.purchase_request_no
WHERE child.purchase_request_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'goods_receipt_note.purchase_order_no -> purchase_order.no' AS check_name, child.purchase_order_no
FROM goods_receipt_note child
LEFT JOIN purchase_order parent ON parent.no = child.purchase_order_no
WHERE child.purchase_order_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

-- Production
SELECT 'aps_quantity.product_order_no -> product_order.no' AS check_name, child.product_order_no
FROM aps_quantity child
LEFT JOIN product_order parent ON parent.no = child.product_order_no
WHERE child.product_order_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'work_order.product_order_no -> product_order.no' AS check_name, child.product_order_no
FROM work_order child
LEFT JOIN product_order parent ON parent.no = child.product_order_no
WHERE child.product_order_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'work_order.aps_no -> aps_quantity.no' AS check_name, child.aps_no
FROM work_order child
LEFT JOIN aps_quantity parent ON parent.no = child.aps_no
WHERE child.aps_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'work_order.product_no -> product.no' AS check_name, child.product_no
FROM work_order child
LEFT JOIN product parent ON parent.no = child.product_no
WHERE child.product_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'work_order.production_line_no -> production_line.no' AS check_name, child.production_line_no
FROM work_order child
LEFT JOIN production_line parent ON parent.no = child.production_line_no
WHERE child.production_line_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'process_order.work_order_no -> work_order.no' AS check_name, child.work_order_no
FROM process_order child
LEFT JOIN work_order parent ON parent.no = child.work_order_no
WHERE child.work_order_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'production_data.work_order_no -> work_order.no' AS check_name, child.work_order_no
FROM production_data child
LEFT JOIN work_order parent ON parent.no = child.work_order_no
WHERE child.work_order_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'production_data_output.work_order_no -> work_order.no' AS check_name, child.work_order_no
FROM production_data_output child
LEFT JOIN work_order parent ON parent.no = child.work_order_no
WHERE child.work_order_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'production_data_input.work_order_no -> work_order.no' AS check_name, child.work_order_no
FROM production_data_input child
LEFT JOIN work_order parent ON parent.no = child.work_order_no
WHERE child.work_order_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'production_data_machine.equipment_no -> equipment.no' AS check_name, child.equipment_no
FROM production_data_machine child
LEFT JOIN equipment parent ON parent.no = child.equipment_no
WHERE child.equipment_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'production_data_labor.employee_no -> employee.no' AS check_name, child.employee_no
FROM production_data_labor child
LEFT JOIN employee parent ON parent.no = child.employee_no
WHERE child.employee_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

-- Inventory and batch
SELECT 'batch_number.creator_no -> employee.no' AS check_name, child.creator_no
FROM batch_number child
LEFT JOIN employee parent ON parent.no = child.creator_no
WHERE child.creator_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'inventory_order.creator_no -> employee.no' AS check_name, child.creator_no
FROM inventory_order child
LEFT JOIN employee parent ON parent.no = child.creator_no
WHERE child.creator_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'inventory_record.warehouse_no -> ship_wh_alias.no' AS check_name, child.warehouse_no
FROM inventory_record child
LEFT JOIN ship_wh_alias parent ON parent.no = child.warehouse_no
WHERE child.warehouse_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

SELECT 'warehouse_record.batch_no -> batch_number.no' AS check_name, child.batch_no
FROM warehouse_record child
LEFT JOIN batch_number parent ON parent.no = child.batch_no
WHERE child.batch_no IS NOT NULL AND parent.no IS NULL
LIMIT 50;

-- ============================================================
-- 2. First-batch FK constraints
-- ============================================================

-- Run these only after validation queries return no orphan rows.

ALTER TABLE `member` ADD CONSTRAINT `fk_member_user_no` FOREIGN KEY (`user_no`) REFERENCES `employee` (`no`);
ALTER TABLE `session` ADD CONSTRAINT `fk_session_user_no` FOREIGN KEY (`user_no`) REFERENCES `employee` (`no`);
ALTER TABLE `trans_items` ADD CONSTRAINT `fk_trans_items_company_no` FOREIGN KEY (`company_no`) REFERENCES `company` (`no`);
ALTER TABLE `trans_items2` ADD CONSTRAINT `fk_trans_items2_company_no` FOREIGN KEY (`company_no`) REFERENCES `company` (`no`);
ALTER TABLE `ship_wh` ADD CONSTRAINT `fk_ship_wh_company_no` FOREIGN KEY (`company_no`) REFERENCES `company` (`no`);
ALTER TABLE `production_line` ADD CONSTRAINT `fk_production_line_factory_no` FOREIGN KEY (`factory_no`) REFERENCES `factory` (`no`);
ALTER TABLE `production_line` ADD CONSTRAINT `fk_production_line_process_no` FOREIGN KEY (`process_no`) REFERENCES `process` (`no`);
ALTER TABLE `equipment` ADD CONSTRAINT `fk_equipment_station_no` FOREIGN KEY (`station_no`) REFERENCES `station` (`no`);

ALTER TABLE `bom_item` ADD CONSTRAINT `fk_bom_item_bom_no` FOREIGN KEY (`bom_no`) REFERENCES `bom` (`no`);
ALTER TABLE `bom_item` ADD CONSTRAINT `fk_bom_item_item_no` FOREIGN KEY (`item_no`) REFERENCES `material` (`no`);
ALTER TABLE `product_ver` ADD CONSTRAINT `fk_product_ver_item_no` FOREIGN KEY (`item_no`) REFERENCES `product` (`no`);
ALTER TABLE `product_spec` ADD CONSTRAINT `fk_product_spec_product_no` FOREIGN KEY (`product_no`) REFERENCES `product` (`no`);
ALTER TABLE `product_bom_spec` ADD CONSTRAINT `fk_product_bom_spec_product_no` FOREIGN KEY (`product_no`) REFERENCES `product` (`no`);
ALTER TABLE `product_bom_spec` ADD CONSTRAINT `fk_product_bom_spec_bom2_no` FOREIGN KEY (`bom2_no`) REFERENCES `bom2_number` (`no`);

ALTER TABLE `quotation` ADD CONSTRAINT `fk_quotation_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `quotation` ADD CONSTRAINT `fk_quotation_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `contract` ADD CONSTRAINT `fk_contract_ref_no` FOREIGN KEY (`ref_no`) REFERENCES `quotation` (`no`);
ALTER TABLE `contract` ADD CONSTRAINT `fk_contract_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `contract` ADD CONSTRAINT `fk_contract_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `product_order` ADD CONSTRAINT `fk_product_order_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `product_order` ADD CONSTRAINT `fk_product_order_ref_no` FOREIGN KEY (`ref_no`) REFERENCES `contract` (`no`);
ALTER TABLE `product_order` ADD CONSTRAINT `fk_product_order_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `product_order` ADD CONSTRAINT `fk_product_order_item_no` FOREIGN KEY (`item_no`) REFERENCES `trans_items` (`no`);
ALTER TABLE `shipping_order` ADD CONSTRAINT `fk_shipping_order_product_order_no` FOREIGN KEY (`product_order_no`) REFERENCES `product_order` (`no`);
ALTER TABLE `purchase_request` ADD CONSTRAINT `fk_purchase_request_product_order_no` FOREIGN KEY (`product_order_no`) REFERENCES `product_order` (`no`);
ALTER TABLE `purchase_request_item` ADD CONSTRAINT `fk_purchase_request_item_purchase_request_no` FOREIGN KEY (`purchase_request_no`) REFERENCES `purchase_request` (`no`);
ALTER TABLE `purchase_request_item` ADD CONSTRAINT `fk_purchase_request_item_item_no` FOREIGN KEY (`item_no`) REFERENCES `material` (`no`);
ALTER TABLE `purchase_order` ADD CONSTRAINT `fk_purchase_order_purchase_request_no` FOREIGN KEY (`purchase_request_no`) REFERENCES `purchase_request` (`no`);
ALTER TABLE `goods_receipt_note` ADD CONSTRAINT `fk_goods_receipt_note_purchase_order_no` FOREIGN KEY (`purchase_order_no`) REFERENCES `purchase_order` (`no`);

ALTER TABLE `aps_quantity` ADD CONSTRAINT `fk_aps_quantity_product_order_no` FOREIGN KEY (`product_order_no`) REFERENCES `product_order` (`no`);
ALTER TABLE `aps_quantity_item` ADD CONSTRAINT `fk_aps_quantity_item_product_order_no` FOREIGN KEY (`product_order_no`) REFERENCES `product_order` (`no`);
ALTER TABLE `aps_quantity_item` ADD CONSTRAINT `fk_aps_quantity_item_item_no` FOREIGN KEY (`item_no`) REFERENCES `material` (`no`);
ALTER TABLE `work_order` ADD CONSTRAINT `fk_work_order_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `work_order` ADD CONSTRAINT `fk_work_order_product_order_no` FOREIGN KEY (`product_order_no`) REFERENCES `product_order` (`no`);
ALTER TABLE `work_order` ADD CONSTRAINT `fk_work_order_aps_no` FOREIGN KEY (`aps_no`) REFERENCES `aps_quantity` (`no`);
ALTER TABLE `work_order` ADD CONSTRAINT `fk_work_order_product_no` FOREIGN KEY (`product_no`) REFERENCES `product` (`no`);
ALTER TABLE `work_order` ADD CONSTRAINT `fk_work_order_customer_no` FOREIGN KEY (`customer_no`) REFERENCES `company` (`no`);
ALTER TABLE `work_order` ADD CONSTRAINT `fk_work_order_production_line_no` FOREIGN KEY (`production_line_no`) REFERENCES `production_line` (`no`);
ALTER TABLE `process_order` ADD CONSTRAINT `fk_process_order_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `process_labor` ADD CONSTRAINT `fk_process_labor_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `process_labor` ADD CONSTRAINT `fk_process_labor_employee_no` FOREIGN KEY (`employee_no`) REFERENCES `employee` (`no`);
ALTER TABLE `process_labor` ADD CONSTRAINT `fk_process_labor_station_no` FOREIGN KEY (`station_no`) REFERENCES `station` (`no`);
ALTER TABLE `production_data` ADD CONSTRAINT `fk_production_data_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `production_data` ADD CONSTRAINT `fk_production_data_product_order_no` FOREIGN KEY (`product_order_no`) REFERENCES `product_order` (`no`);
ALTER TABLE `production_data` ADD CONSTRAINT `fk_production_data_product_no` FOREIGN KEY (`product_no`) REFERENCES `product` (`no`);
ALTER TABLE `production_data` ADD CONSTRAINT `fk_production_data_production_line_no` FOREIGN KEY (`production_line_no`) REFERENCES `production_line` (`no`);
ALTER TABLE `production_data_output` ADD CONSTRAINT `fk_production_data_output_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `production_data_output` ADD CONSTRAINT `fk_production_data_output_process_order_no` FOREIGN KEY (`process_order_no`) REFERENCES `process_order` (`no`);
ALTER TABLE `production_data_input` ADD CONSTRAINT `fk_production_data_input_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `production_data_input` ADD CONSTRAINT `fk_production_data_input_process_order_no` FOREIGN KEY (`process_order_no`) REFERENCES `process_order` (`no`);
ALTER TABLE `production_data_machine` ADD CONSTRAINT `fk_production_data_machine_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `production_data_machine` ADD CONSTRAINT `fk_production_data_machine_equipment_no` FOREIGN KEY (`equipment_no`) REFERENCES `equipment` (`no`);
ALTER TABLE `production_data_labor` ADD CONSTRAINT `fk_production_data_labor_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `production_data_labor` ADD CONSTRAINT `fk_production_data_labor_employee_no` FOREIGN KEY (`employee_no`) REFERENCES `employee` (`no`);
ALTER TABLE `production_data_labor` ADD CONSTRAINT `fk_production_data_labor_station_no` FOREIGN KEY (`station_no`) REFERENCES `station` (`no`);

ALTER TABLE `batch_number` ADD CONSTRAINT `fk_batch_number_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `inventory_order` ADD CONSTRAINT `fk_inventory_order_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `inventory_record` ADD CONSTRAINT `fk_inventory_record_warehouse_no` FOREIGN KEY (`warehouse_no`) REFERENCES `ship_wh_alias` (`no`);
ALTER TABLE `warehouse_record` ADD CONSTRAINT `fk_warehouse_record_batch_no` FOREIGN KEY (`batch_no`) REFERENCES `batch_number` (`no`);
ALTER TABLE `warehouse_payment` ADD CONSTRAINT `fk_warehouse_payment_batch_no` FOREIGN KEY (`batch_no`) REFERENCES `batch_number` (`no`);
