-- Converted from Word schema: 食品管理系統Database Schema_0.0.25.docx
-- Generated on 2026-05-15
-- Notes:
-- 1. Single-target inferred relationships are emitted as FOREIGN KEY constraints.
-- 2. Multi-target relationships are emitted as comments because MySQL cannot enforce polymorphic FK directly.
-- 3. Review this file before applying it to a database.

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
CREATE DATABASE IF NOT EXISTS `ai` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `ai`;

CREATE TABLE IF NOT EXISTS `enterprise` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `businessNo` VARCHAR(20) NULL,
  `displayName` VARCHAR(60) NULL,
  `name` VARCHAR(60) NULL,
  `address` VARCHAR(100) NULL,
  `phone` VARCHAR(100) NULL,
  `fax` VARCHAR(100) NULL,
  `department` INT NULL,
  `lar` VARCHAR(100) NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_enterprise_no` (`no`),
  UNIQUE KEY `uq_enterprise_businessNo` (`businessNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `company` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `businessNo` VARCHAR(20) NULL,
  `displayName` VARCHAR(60) NULL,
  `name` VARCHAR(60) NULL,
  `address` VARCHAR(60) NULL,
  `phone` VARCHAR(60) NULL,
  `fax` VARCHAR(60) NULL,
  `contactName` VARCHAR(60) NULL,
  `contactPhone` VARCHAR(60) NULL,
  `contactTitle` VARCHAR(60) NULL,
  `contactEmail` VARCHAR(60) NULL,
  `received_id` INT NULL,
  `paid_id` INT NULL,
  `bankDisplayName` VARCHAR(60) NULL,
  `bankName` VARCHAR(60) NULL,
  `bankCurrency` INT NULL,
  `bankBranch` VARCHAR(60) NULL,
  `bankAccount` VARCHAR(60) NULL,
  `bankNo` VARCHAR(60) NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_company_no` (`no`),
  UNIQUE KEY `uq_company_businessNo` (`businessNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `bank_account` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `category` INT NULL,
  `currency` INT NULL,
  `displayName` VARCHAR(60) NULL,
  `name` VARCHAR(60) NULL,
  `branch` VARCHAR(60) NULL,
  `account` VARCHAR(60) NULL,
  `number` VARCHAR(60) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_bank_account_number` (`number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `payment` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `type` INT NULL,
  `source` INT NULL,
  `date` INT NULL,
  `period` INT NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_payment_type` (`type`),
  UNIQUE KEY `uq_payment_source` (`source`),
  UNIQUE KEY `uq_payment_date` (`date`),
  UNIQUE KEY `uq_payment_period` (`period`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `material` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `category` INT NULL,
  `subCategory` INT NULL,
  `name` VARCHAR(255) NULL,
  `unitShipping` INT NULL,
  `unitWarehouse` INT NULL,
  `unitProduct` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_material_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `inproduct` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `category` INT NULL,
  `name` VARCHAR(100) NULL,
  `unitShipping` INT NULL,
  `unitWarehouse` INT NULL,
  `unitProduct` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_inproduct_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `inproduct_bom_spec` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `inproduct_no` VARCHAR(60) NULL,
  `category` INT NULL,
  `item_no` VARCHAR(60) NULL,
  `item_version` INT NULL,
  `bom12_no` VARCHAR(60) NULL,
  `count` INT NULL,
  `unit` INT NULL,
  `weight` FLOAT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_inproduct_bom_spec_inproduct_no` (`inproduct_no`),
  UNIQUE KEY `uq_inproduct_bom_spec_item_no` (`item_no`),
  UNIQUE KEY `uq_inproduct_bom_spec_item_version` (`item_version`),
  UNIQUE KEY `uq_inproduct_bom_spec_bom12_no` (`bom12_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `product` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `category` INT NULL,
  `name` VARCHAR(60) NULL,
  `unitShipping` INT NULL,
  `unitWarehouse` INT NULL,
  `unitProduct` INT NULL,
  `version` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_product_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `product_ver` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `item_no` VARCHAR(60) NULL,
  `version` INT NULL,
  `date` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_product_ver_no` (`no`),
  UNIQUE KEY `uq_product_ver_item_no` (`item_no`),
  UNIQUE KEY `uq_product_ver_version` (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `product_spec` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `product_no` VARCHAR(60) NULL,
  `product_version` INT NULL,
  `bom_no` VARCHAR(60) NULL,
  `bom_version` INT NULL,
  `level` INT NULL,
  `item_type` INT NULL,
  `item_no` VARCHAR(60) NULL,
  `count` INT NULL,
  `unit` INT NULL,
  `weight` FLOAT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_product_spec_product_no` (`product_no`),
  UNIQUE KEY `uq_product_spec_product_version` (`product_version`),
  UNIQUE KEY `uq_product_spec_item_no` (`item_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `product_bom_spec` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `product_no` VARCHAR(60) NULL,
  `product_version` INT NULL,
  `level` INT NULL,
  `bom2_no` VARCHAR(60) NULL,
  `count` INT NULL,
  `unit` INT NULL,
  `weight` FLOAT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_product_bom_spec_product_no` (`product_no`),
  UNIQUE KEY `uq_product_bom_spec_product_version` (`product_version`),
  UNIQUE KEY `uq_product_bom_spec_bom2_no` (`bom2_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `goods` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `category` INT NULL,
  `subCategory` INT NULL,
  `name` INT NULL,
  `unitShipping` INT NULL,
  `unitWarehouse` INT NULL,
  `unitProduct` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_goods_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `trans_items` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `name` VARCHAR(100) NULL,
  `category` INT NULL,
  `attribute` INT NULL,
  `company_no` VARCHAR(60) NULL,
  `company_displayName` VARCHAR(60) NULL,
  -- FK candidate: `company_displayName` -> company(`no`), denormalized_or_label,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> material / inproduct / product(`no`), needs_review,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> material / inproduct / product(`no`), denormalized_or_label,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_trans_items_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `trans_items2` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `name` VARCHAR(100) NULL,
  `category` INT NULL,
  `attribute` INT NULL,
  `company_no` VARCHAR(60) NULL,
  `company_displayName` VARCHAR(60) NULL,
  -- FK candidate: `company_displayName` -> company(`no`), denormalized_or_label,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_trans_items2_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `ship_wh_alias` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `name` VARCHAR(60) NULL,
  `category` INT NULL,
  `type` INT NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_ship_wh_alias_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `ship_wh` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `company_no` VARCHAR(60) NULL,
  `company_displayName` VARCHAR(60) NULL,
  -- FK candidate: `company_displayName` -> company(`no`), denormalized_or_label,
  `name` VARCHAR(60) NULL,
  `category` INT NULL,
  `attribute` INT NULL,
  `unit` INT NULL,
  `maxCapacity` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_ship_wh_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `bom` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `displayName` VARCHAR(60) NULL,
  `version` INT NULL,
  `date` INT NULL,
  `unit` INT NULL,
  `weight` FLOAT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_bom_no` (`no`),
  UNIQUE KEY `uq_bom_version` (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `bom_item` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `bom_no` VARCHAR(60) NULL,
  `item_no` VARCHAR(60) NULL,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> material(`no`), denormalized_or_label,
  `unit` INT NULL,
  `weight` FLOAT NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_bom_item_bom_no` (`bom_no`),
  UNIQUE KEY `uq_bom_item_item_no` (`item_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `bom1_number` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `displayName` VARCHAR(60) NULL,
  `unit` INT NULL,
  `weight` FLOAT NULL,
  `bom_no` VARCHAR(60) NULL,
  `bom_version` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_bom1_number_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `bom1` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `parent_no` VARCHAR(60) NULL,
  `parent_name` VARCHAR(60) NULL,
  -- FK candidate: `parent_name` -> bom1_number(`no`), denormalized_or_label,
  `child_category` INT NULL,
  `child_id` VARCHAR(60) NULL,
  -- FK candidate: `child_id` -> material / bom1_number(`id`), needs_review,
  `child_name` VARCHAR(60) NULL,
  -- FK candidate: `child_name` -> material / bom1_number(`no`), denormalized_or_label,
  `childUnit` INT NULL,
  `weight` FLOAT NULL,
  `expectedLoss` FLOAT NULL,
  `actualLoss` FLOAT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_bom1_parent_no` (`parent_no`),
  UNIQUE KEY `uq_bom1_child_id` (`child_id`),
  UNIQUE KEY `uq_bom1_weight` (`weight`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `bom2_number` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `displayName` VARCHAR(60) NULL,
  `unit` INT NULL,
  `weight` FLOAT NULL,
  `bom_no` VARCHAR(60) NULL,
  `bom_version` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_bom2_number_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `bom2` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `parent_no` VARCHAR(60) NULL,
  `parent_name` VARCHAR(60) NULL,
  -- FK candidate: `parent_name` -> bom2_number(`no`), denormalized_or_label,
  `child_category` INT NULL,
  `child_id` VARCHAR(60) NULL,
  -- FK candidate: `child_id` -> material / bom2_number(`id`), needs_review,
  `child_name` VARCHAR(60) NULL,
  -- FK candidate: `child_name` -> material / bom2_number(`no`), denormalized_or_label,
  `childUnit` INT NULL,
  `weight` FLOAT NULL,
  `childUnit2` INT NULL,
  `length` FLOAT NULL,
  `count` INT NULL,
  `expectedLoss` FLOAT NULL,
  `actualLoss` FLOAT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `sample_price` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `item_no` VARCHAR(60) NULL,
  `date` DATE NULL,
  `estWHUnitWeight` INT NULL,
  `estWHPriceWeight` DOUBLE NULL,
  `estCostUnitWeight` INT NULL,
  `estCostPriceWeight` DOUBLE NULL,
  `estLaborCost` DOUBLE NULL,
  `whUnitWeight` INT NULL,
  `whPriceWeight` DOUBLE NULL,
  `costUnitWeight` INT NULL,
  `costPriceWeight` DOUBLE NULL,
  `laborCost` DOUBLE NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_sample_price_item_no` (`item_no`),
  UNIQUE KEY `uq_sample_price_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `item_price` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> material / inproduct / product / goods(`no`), needs_review,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> material / inproduct / product / goods(`no`), denormalized_or_label,
  `itemCategory` INT NULL,
  `date` DATE NULL,
  `whUnitWeight` INT NULL,
  `costUnitWeight` INT NULL,
  `estWHPriceWeight` DOUBLE NULL,
  `estWHPriceWeight1` DOUBLE NULL,
  `estWHPriceWeight2` DOUBLE NULL,
  `estCostPriceWeight` DOUBLE NULL,
  `estCostPriceWeight1` DOUBLE NULL,
  `estCostPriceWeight2` DOUBLE NULL,
  `estLaborCost` DOUBLE NULL,
  `whPriceWeight` DOUBLE NULL,
  `whPriceWeight1` DOUBLE NULL,
  `whPriceWeight2` DOUBLE NULL,
  `costPriceWeight` DOUBLE NULL,
  `costPriceWeight1` DOUBLE NULL,
  `costPriceWeight2` DOUBLE NULL,
  `laborCost` DOUBLE NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_item_price_item_no` (`item_no`),
  UNIQUE KEY `uq_item_price_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `item_loss` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> material / inproduct / product(`no`), needs_review,
  `itemCategory` INT NULL,
  `date` DATE NULL,
  `unit` INT NULL,
  `estValue` DOUBLE NULL,
  `value` DOUBLE NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_item_loss_item_no` (`item_no`),
  UNIQUE KEY `uq_item_loss_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `item_hours` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> inproduct / product(`no`), needs_review,
  `itemCategory` INT NULL,
  `date` INT NULL,
  `unit` INT NULL,
  `estValue` DOUBLE NULL,
  `value` DOUBLE NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_item_hours_item_no` (`item_no`),
  UNIQUE KEY `uq_item_hours_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `process_capacity` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `date` DATE NULL,
  `oneProcess` INT NULL,
  `secProcess` INT NULL,
  `unit` INT NULL,
  `hourlyOutput` DOUBLE NULL,
  `laborCount` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_process_capacity_date` (`date`),
  UNIQUE KEY `uq_process_capacity_oneProcess` (`oneProcess`),
  UNIQUE KEY `uq_process_capacity_secProcess` (`secProcess`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `process_flow` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `product_process_no` VARCHAR(60) NULL,
  `order` INT NULL,
  `oneProcess` INT NULL,
  `secProcess` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_process_flow_no` (`no`),
  UNIQUE KEY `uq_process_flow_product_process_no` (`product_process_no`),
  UNIQUE KEY `uq_process_flow_order` (`order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `product_process` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> inproduct / product(`no`), needs_review,
  `version` INT NULL,
  `date` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_product_process_no` (`no`),
  UNIQUE KEY `uq_product_process_item_no` (`item_no`),
  UNIQUE KEY `uq_product_process_version` (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `batch_number` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `date` INT NULL,
  `no` VARCHAR(60) NULL,
  `creator_no` VARCHAR(60) NULL,
  `ref_no` VARCHAR(60) NULL,
  -- FK candidate: `ref_no` -> goods_receipt_note / work_order / process_order(`no`), needs_review,
  `refCategory` INT NULL,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> material / inproduct / product(`no`), needs_review,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> material / inproduct / product(`no`), denormalized_or_label,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `itemCategory` INT NULL,
  `itemSubCategory` INT NULL,
  `itemType` INT NULL,
  `unit` INT NULL,
  `expectedCount` FLOAT NULL,
  `checkedCount` FLOAT NULL,
  `validDays` INT NULL,
  `validDate` INT NULL,
  `validDateNo` VARCHAR(60) NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_batch_number_no` (`no`),
  UNIQUE KEY `uq_batch_number_ref_no` (`ref_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `batchno_serialno` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `batch_number` VARCHAR(60) NULL,
  `serialNo` VARCHAR(60) NULL,
  `ref_order_no_category` INT NULL,
  `ref_order_no` VARCHAR(60) NULL,
  -- FK candidate: `ref_order_no` -> goods_receipt_note / work_order / process_orderr / inventory_order(`no`), needs_review,
  `warehouse_no` VARCHAR(60) NULL,
  `time` INT NULL,
  `unit` INT NULL,
  `expectedCount` FLOAT NULL,
  `count` FLOAT NULL,
  `vaildDate` INT NULL,
  `updatedTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_batchno_serialno_batch_number` (`batch_number`),
  UNIQUE KEY `uq_batchno_serialno_serialNo` (`serialNo`),
  UNIQUE KEY `uq_batchno_serialno_ref_order_no` (`ref_order_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `inventory_order` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `creator_no` VARCHAR(60) NULL,
  `date` INT NULL,
  `category` INT NULL,
  `subCategory` INT NULL,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> material / inproduct / product(`no`), needs_review,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> material / inproduct / product(`no`), denormalized_or_label,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `itemCategory` INT NULL,
  `itemType` INT NULL,
  `unit` INT NULL,
  `price` FLOAT NULL,
  `expectedCount` FLOAT NULL,
  `checkedCount` FLOAT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_inventory_order_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `inventory_record` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `group` VARCHAR(60) NULL,
  `refCategory` INT NULL,
  `ref_no` VARCHAR(60) NULL,
  -- FK candidate: `ref_no` -> goods_receipt_note / shipping_order / process_order / inventory_order(`no`), needs_review,
  `warehouse_no` VARCHAR(60) NULL,
  `warehouse_displayName` VARCHAR(60) NULL,
  -- FK candidate: `warehouse_displayName` -> ship_wh_alias(`no`), denormalized_or_label,
  `date` INT NULL,
  `category` INT NULL,
  `source` INT NULL,
  `batchNumber` VARCHAR(20) NULL,
  `serialNo` VARCHAR(20) NULL,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> material / inproduct / product(`no`), needs_review,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> material / inproduct / product(`no`), denormalized_or_label,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `itemCategory` INT NULL,
  `itemType` INT NULL,
  `unit` INT NULL,
  `count` FLOAT NULL,
  `price` FLOAT NULL,
  `amount` FLOAT NULL,
  `comment` VARCHAR(128) NULL,
  `registerDevId` VARCHAR(60) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `inventory_delta` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `warehouse_no` VARCHAR(60) NULL,
  `warehouse_displayName` VARCHAR(60) NULL,
  -- FK candidate: `warehouse_displayName` -> ship_wh_alias(`no`), denormalized_or_label,
  `date` DATE NULL,
  `timezone` VARCHAR(60) NULL,
  `kind` INT NULL,
  `category` INT NULL,
  `specified_no` VARCHAR(60) NULL,
  -- FK candidate: `specified_no` -> material / inproduct / product / batch_number(`no`), needs_review,
  `specified_name` VARCHAR(255) NULL,
  -- FK candidate: `specified_name` -> material / inproduct / product(`no`), denormalized_or_label,
  `specified_ref_no` VARCHAR(60) NULL,
  -- FK candidate: `specified_ref_no` -> company / material / inproduct / product(`no`), needs_review,
  `specified_ref_name` VARCHAR(60) NULL,
  -- FK candidate: `specified_ref_name` -> company / material / inproduct / product(`no`), denormalized_or_label,
  `in_ref_id` LONGTEXT NULL,
  `out_ref_id` LONGTEXT NULL,
  `inCount` FLOAT NULL,
  `inAmount` DOUBLE NULL,
  `inPurchaseCount` FLOAT NULL,
  `inPurchaseAmount` DOUBLE NULL,
  `outCount` FLOAT NULL,
  `outAmount` DOUBLE NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_inventory_delta_warehouse_displayName` (`warehouse_displayName`),
  UNIQUE KEY `uq_inventory_delta_date` (`date`),
  UNIQUE KEY `uq_inventory_delta_timezone` (`timezone`),
  UNIQUE KEY `uq_inventory_delta_specified_no` (`specified_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `Inventory_month_statistic` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `warehouse_no` VARCHAR(60) NULL,
  `warehouse_displayName` VARCHAR(60) NULL,
  -- FK candidate: `warehouse_displayName` -> ship_wh_alias(`no`), denormalized_or_label,
  `date` DATE NULL,
  `timezone` VARCHAR(60) NULL,
  `category` INT NULL,
  `startAmount` DOUBLE NULL,
  `inAmount` DOUBLE NULL,
  `outAmount` DOUBLE NULL,
  `inPurchaseAmount` DOUBLE NULL,
  `endAmount` DOUBLE NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_Inventory_month_statistic_warehouse_displayName` (`warehouse_displayName`),
  UNIQUE KEY `uq_Inventory_month_statistic_date` (`date`),
  UNIQUE KEY `uq_Inventory_month_statistic_timezone` (`timezone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `Inventory_item_month_statistic` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `warehouse_no` VARCHAR(60) NULL,
  `warehouse_displayName` VARCHAR(60) NULL,
  -- FK candidate: `warehouse_displayName` -> ship_wh_alias(`no`), denormalized_or_label,
  `date` DATE NULL,
  `timezone` VARCHAR(60) NULL,
  `kind` INT NULL,
  `category` INT NULL,
  `specified_no` VARCHAR(60) NULL,
  -- FK candidate: `specified_no` -> material / inproduct / product / batch_number(`no`), needs_review,
 
  `specified_name` VARCHAR(60) NULL,
  -- FK candidate: `specified_name` -> material / inproduct / product(`no`), denormalized_or_label,
  `specified_ref_no` VARCHAR(60) NULL,
  -- FK candidate: `specified_ref_no` -> company / material / inproduct / product(`no`), needs_review,
  `specified_ref_name` VARCHAR(60) NULL,
  `unit` INT NULL,
  `startCount` FLOAT NULL,
  `startAmount` DOUBLE NULL,
  `inCount` INT NULL,
  `inAmount` DOUBLE NULL,
  `endCount` INT NULL,
  `endAmount` DOUBLE NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_Inventory_item_month_statistic_warehouse_displayName` (`warehouse_displayName`),
  UNIQUE KEY `uq_Inventory_item_month_statistic_date` (`date`),
  UNIQUE KEY `uq_Inventory_item_month_statistic_timezone` (`timezone`),
  UNIQUE KEY `uq_Inventory_item_month_statistic_specified_no` (`specified_no`),
  UNIQUE KEY `uq_Inventory_item_month_statistic_specified_ref_no` (`specified_ref_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `quotation` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `creator_no` VARCHAR(60) NULL,
  `date` INT NULL,
  `category` INT NULL,
  `type` INT NULL,
  `itemStyle` INT NULL,
  `item_no` VARCHAR(255) NULL,
  -- FK candidate: `item_no` -> trans_items / trans_items2(`no`), needs_review,
  `item_name` VARCHAR(255) NULL,
  -- FK candidate: `item_name` -> trans_items / trans_items2(`no`), denormalized_or_label,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `unit` INT NULL,
  `price` VARCHAR(255) NULL,
  `unitConversion` VARCHAR(255) NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_quotation_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `ship_wh_quotation` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `date` INT NULL,
  `item_no` VARCHAR(60) NULL,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> ship_wh(`no`), denormalized_or_label,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `category` INT NULL,
  `type` INT NULL,
  `itemStyle` INT NULL,
  `region` INT NULL,
  `unit` INT NULL,
  `price` FLOAT NULL,
  `fee` FLOAT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_ship_wh_quotation_no` (`no`),
  UNIQUE KEY `uq_ship_wh_quotation_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `contract` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `ref_no` VARCHAR(60) NULL,
  `creator_no` VARCHAR(60) NULL,
  `date` INT NULL,
  `displayName` VARCHAR(60) NULL,
  `category` INT NULL,
  `type` INT NULL,
  `itemStyle` INT NULL,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> trans_items / trans_items2(`no`), needs_review,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> trans_items / trans_items2(`no`), denormalized_or_label,
  `itemCategory` INT NULL,
  `itemSubCategory` INT NULL,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `payment_id` INT NULL,
  `unit` INT NULL,
  `price` DOUBLE NULL,
  `shippingPrice` DOUBLE NULL,
  `unitConversion` DOUBLE NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_contract_no` (`no`),
  UNIQUE KEY `uq_contract_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `ship_wh_contract` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `date` INT NULL,
  `ref_no` VARCHAR(60) NULL,
  `sw_alias_no` VARCHAR(60) NULL,
  `displayName` VARCHAR(60) NULL,
  `item_no` VARCHAR(60) NULL,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> ship_wh(`no`), denormalized_or_label,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `category` INT NULL,
  `type` INT NULL,
  `itemStyle` INT NULL,
  `region` INT NULL,
  `unit` INT NULL,
  `price` DOUBLE NULL,
  `fee` DOUBLE NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_ship_wh_contract_no` (`no`),
  UNIQUE KEY `uq_ship_wh_contract_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `product_order` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `creator_no` VARCHAR(60) NULL,
  `date` INT NULL,
  `ref_no` VARCHAR(60) NULL,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `item_no` VARCHAR(60) NULL,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> trans_items(`no`), denormalized_or_label,
  `unit` INT NULL,
  `price` FLOAT NULL,
  `count` FLOAT NULL,
  `preparedCount` FLOAT NULL,
  `amount` FLOAT NULL,
  `expectedDate` INT NULL,
  `address` VARCHAR(100) NULL,
  `payment_type` INT NULL,
  `payment_source` INT NULL,
  `payment_date` INT NULL,
  `payment_period` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_product_order_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `shipping_order` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `creator_no` VARCHAR(60) NULL,
  `product_order_no` VARCHAR(60) NULL,
  `date` INT NULL,
  `category` INT NULL,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `item_no` VARCHAR(60) NULL,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> trans_items(`no`), denormalized_or_label,
  `itemCategory` INT NULL,
  `itemSubCategory` INT NULL,
  `unit` INT NULL,
  `price` DOUBLE NULL,
  `expectedCount` FLOAT NULL,
  `checkedCount` FLOAT NULL,
  `feeCount` FLOAT NULL,
  `amount` INT NULL,
  `addDeleteAmount` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_shipping_order_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `purchase_request` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `creator_no` VARCHAR(60) NULL,
  `product_order_no` VARCHAR(60) NULL,
  `date` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_purchase_request_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `purchase_request_item` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `purchase_request_no` VARCHAR(60) NULL,
  `item_no` VARCHAR(60) NULL,
  `unit` INT NULL,
  `count` FLOAT NULL,
  `expectedDate` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_purchase_request_item_purchase_request_no` (`purchase_request_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `purchase_order` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `creator_no` VARCHAR(60) NULL,
  `purchase_request_no` VARCHAR(60) NULL,
  `date` INT NULL,
  `ref_no` VARCHAR(60) NULL,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `item_no` VARCHAR(60) NULL,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> trans_items(`no`), denormalized_or_label,
  `unit` INT NULL,
  `price` DOUBLE NULL,
  `count` FLOAT NULL,
  `amount` FLOAT NULL,
  `expectedDate` INT NULL,
  `address` VARCHAR(100) NULL,
  `payment_type` INT NULL,
  `payment_source` INT NULL,
  `payment_date` INT NULL,
  `payment_period` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_purchase_order_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `goods_receipt_note` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `creator_no` VARCHAR(60) NULL,
  `purchase_order_no` VARCHAR(60) NULL,
  `date` INT NULL,
  `category` INT NULL,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `item_no` VARCHAR(255) NULL,
  `item_name` VARCHAR(255) NULL,
  -- FK candidate: `item_name` -> trans_items(`no`), denormalized_or_label,
  `itemCategory` INT NULL,
  `itemSubCategory` INT NULL,
  `unit` INT NULL,
  `price` DOUBLE NULL,
  `expectedCount` FLOAT NULL,
  `checkedCount` FLOAT NULL,
  `feeCount` FLOAT NULL,
  `amount` INT NULL,
  `addDeleteAmount` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_goods_receipt_note_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `order_payment` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `group_no` VARCHAR(60) NULL,
  `date` INT NULL,
  `arapType` INT NULL,
  `refCategory` INT NULL,
  `ref_no` VARCHAR(60) NULL,
  -- FK candidate: `ref_no` -> product_order / purchase_order(`no`), needs_review,
  `ref_sub_no` VARCHAR(60) NULL,
  -- FK candidate: `ref_sub_no` -> goods_receipt_note / shipping_order(`no`), needs_review,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `itemCategory` INT NULL,
  `itemSubCategory` INT NULL,
  `paymentType` INT NULL,
  `month` DATE NULL,
  `price` DOUBLE NULL,
  `count` FLOAT NULL,
  `amount` INT NULL,
  `addDeleteAmount` INT NULL,
  `totalAmount` INT NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `shipping_record` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `date` INT NULL,
  `refCategory` INT NULL,
  `ref_no` VARCHAR(60) NULL,
  -- FK candidate: `ref_no` -> goods_receipt_note / shipping_order(`no`), needs_review,
  `ref_parent_no` VARCHAR(60) NULL,
  -- FK candidate: `ref_parent_no` -> product_order / purchase_order(`no`), needs_review,
  `contract_no` VARCHAR(60) NULL,
  `sw_alias_no` VARCHAR(60) NULL,
  `sw_alias_name` VARCHAR(60) NULL,
  -- FK candidate: `sw_alias_name` -> ship_wh_alias(`no`), denormalized_or_label,
  `item_no` VARCHAR(60) NULL,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> ship_wh(`no`), denormalized_or_label,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `unit` INT NULL,
  `price` DOUBLE NULL,
  `expectedCount` INT NULL,
  `checkedCount` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `warehouse_record` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `date` INT NULL,
  `ref_no` INT NULL,
  -- FK candidate: `ref_no` -> inventory_record(`no`), needs_review,
  `batch_no` VARCHAR(20) NULL,
  `contract_no` VARCHAR(60) NULL,
  `sw_alias_no` VARCHAR(60) NULL,
  `sw_alias_name` VARCHAR(60) NULL,
  -- FK candidate: `sw_alias_name` -> ship_wh_alias(`no`), denormalized_or_label,
  `item_no` VARCHAR(60) NULL,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> ship_wh(`no`), denormalized_or_label,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `inboundTime` INT NULL,
  `unit` INT NULL,
  `price` DOUBLE NULL,
  `count` FLOAT NULL,
  `days` FLOAT NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `shipping_payment` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `group_no` VARCHAR(60) NULL,
  `date` INT NULL,
  `arapType` INT NULL,
  `record_no` VARCHAR(60) NULL,
  -- FK candidate: `record_no` -> shipping_record(`no`), needs_review,
  `refCategory` INT NULL,
  `ref_no` VARCHAR(60) NULL,
  -- FK candidate: `ref_no` -> product_order / purchase_order(`no`), needs_review,
  `ref_sub_no` VARCHAR(60) NULL,
  -- FK candidate: `ref_sub_no` -> goods_receipt_note / shipping_order(`no`), needs_review,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `paymentType` INT NULL,
  `month` DATE NULL,
  `price` DOUBLE NULL,
  `count` INT NULL,
  `amount` INT NULL,
  `addDeleteAmount` INT NULL,
  `totalAmount` INT NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_shipping_payment_no` (`no`),
  UNIQUE KEY `uq_shipping_payment_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `warehouse_payment` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `group_no` VARCHAR(60) NULL,
  `date` INT NULL,
  `arapType` INT NULL,
  `batch_no` VARCHAR(60) NULL,
  `record_no` VARCHAR(60) NULL,
  -- FK candidate: `record_no` -> warehouse_record(`no`), needs_review,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `paymentType` INT NULL,
  `month` DATE NULL,
  `price` DOUBLE NULL,
  `count` INT NULL,
  `amount` INT NULL,
  `addDeleteAmount` INT NULL,
  `totalAmount` INT NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_warehouse_payment_no` (`no`),
  UNIQUE KEY `uq_warehouse_payment_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `order_item_month_statistic` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `date` DATE NULL,
  `timezone` VARCHAR(60) NULL,
  `kind` INT NULL,
  `category` INT NULL,
  `subCategory` INT NULL,
  `type` INT NULL,
  `specified_no` VARCHAR(60) NULL,
  `specified_name` VARCHAR(60) NULL,
  -- FK candidate: `specified_name` -> company(`no`), denormalized_or_label,
  `payment` INT NULL,
  `amount` INT NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_order_item_month_statistic_date` (`date`),
  UNIQUE KEY `uq_order_item_month_statistic_kind` (`kind`),
  UNIQUE KEY `uq_order_item_month_statistic_category` (`category`),
  UNIQUE KEY `uq_order_item_month_statistic_subCategory` (`subCategory`),
  UNIQUE KEY `uq_order_item_month_statistic_specified_no` (`specified_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `factory` (
  `no` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `region` VARCHAR(60) NULL,
  `location` VARCHAR(60) NULL,
  `comment` VARCHAR(128) NULL,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `process` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `oneProcess` INT NULL,
  `secProcess` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_process_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `production_line` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `name` VARCHAR(60) NULL,
  `process_no` VARCHAR(60) NULL,
  `oneProcess` INT NULL,
  `secProcess` INT NULL,
  `factory_no` VARCHAR(60) NULL,
  `location` VARCHAR(60) NULL,
  `capacityUnit` INT NULL,
  `capacity` FLOAT NULL,
  `laborCount` INT NULL,
  `laborEfficiency` FLOAT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_production_line_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `station` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `productionline_no` VARCHAR(60) NULL,
  `name` VARCHAR(60) NULL,
  `stage` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_station_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `equipment` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `station_no` VARCHAR(60) NULL,
  `name` VARCHAR(60) NULL,
  `model` VARCHAR(60) NULL,
  `manufacturer` VARCHAR(60) NULL,
  `purchaseDate` INT NULL,
  `appearance` VARCHAR(128) NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_equipment_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `aps_quantity` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NULL,
  `product_order_no` VARCHAR(60) NULL,
  `oneProcess` INT NULL,
  `secProcess` INT NULL,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> inproduct / product(`no`), needs_review,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> inproduct / product(`no`), denormalized_or_label,
  `itemCategory` INT NULL,
  `unit` INT NULL,
  `amount` FLOAT NULL,
  `minutes` INT NULL,
  `laborCount` INT NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_aps_quantity_no` (`no`),
  UNIQUE KEY `uq_aps_quantity_product_order_no` (`product_order_no`),
  UNIQUE KEY `uq_aps_quantity_oneProcess` (`oneProcess`),
  UNIQUE KEY `uq_aps_quantity_secProcess` (`secProcess`),
  UNIQUE KEY `uq_aps_quantity_item_no` (`item_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `aps_quantity_item` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `product_order_no` VARCHAR(60) NULL,
  `oneProcess` INT NULL,
  `secProcess` INT NULL,
  `item_no` VARCHAR(60) NULL,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> material(`no`), denormalized_or_label,
  `itemCategory` INT NULL,
  `unit` INT NULL,
  `count` FLOAT NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_aps_quantity_item_product_order_no` (`product_order_no`),
  UNIQUE KEY `uq_aps_quantity_item_oneProcess` (`oneProcess`),
  UNIQUE KEY `uq_aps_quantity_item_secProcess` (`secProcess`),
  UNIQUE KEY `uq_aps_quantity_item_item_no` (`item_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `work_order` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `creator_no` VARCHAR(60) NULL,
  `product_order_no` VARCHAR(60) NULL,
  `aps_no` VARCHAR(60) NULL,
  `date` INT NULL,
  `product_no` VARCHAR(60) NULL,
  `product_name` VARCHAR(60) NULL,
  -- FK candidate: `product_name` -> product(`no`), denormalized_or_label,
  `customer_no` VARCHAR(60) NULL,
  `customer_displayName` VARCHAR(60) NULL,
  -- FK candidate: `customer_displayName` -> company(`no`), denormalized_or_label,
  `output_item_no` VARCHAR(255) NULL,
  -- FK candidate: `output_item_no` -> inproduct / product(`no`), needs_review,
  `output_item_name` VARCHAR(60) NULL,
  -- FK candidate: `output_item_name` -> inproduct / product(`no`), denormalized_or_label,
  `production_line_no` VARCHAR(60) NULL,
  `oneProcess` INT NULL,
  `secProcess` INT NULL,
  `startTime` INT NULL,
  `endTime` INT NULL,
  `processUnit` INT NULL,
  `processCount` FLOAT NULL,
  `processTime` INT NULL,
  `laborCount` INT NULL,
  `laborList` LONGTEXT NULL,
  -- FK candidate: `laborList` -> employee(`no`), denormalized_or_label,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_work_order_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `process_order` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `creator_no` VARCHAR(60) NULL,
  `work_order_no` VARCHAR(60) NULL,
  `refProcess` INT NULL,
  `date` INT NULL,
  `category` INT NULL,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> material / inproduct / product(`no`), needs_review,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> material / inproduct / product(`no`), denormalized_or_label,
  `itemCategory` INT NULL,
  `itemSubCategory` INT NULL,
  `item_ref_no` VARCHAR(60) NULL,
  `item_ref_displayName` VARCHAR(60) NULL,
  -- FK candidate: `item_ref_displayName` -> company(`no`), denormalized_or_label,
  `unit` INT NULL,
  `expectedCount` FLOAT NULL,
  `count` FLOAT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_process_order_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `process_labor` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `date` INT NULL,
  `creator_no` VARCHAR(60) NULL,
  `work_order_no` VARCHAR(60) NULL,
  `employee_no` VARCHAR(60) NULL,
  `production_line_no` VARCHAR(60) NULL,
  `station_no` VARCHAR(60) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_process_labor_work_order_no` (`work_order_no`),
  UNIQUE KEY `uq_process_labor_employee_no` (`employee_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `production_data` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `creator_no` VARCHAR(60) NULL,
  `work_order_no` VARCHAR(60) NULL,
  `product_order_no` VARCHAR(60) NULL,
  `customer_no` VARCHAR(60) NULL,
  `customer_displayName` VARCHAR(60) NULL,
  -- FK candidate: `customer_displayName` -> company(`no`), denormalized_or_label,
  `product_no` VARCHAR(60) NULL,
  `product_name` VARCHAR(60) NULL,
  -- FK candidate: `product_name` -> product(`no`), denormalized_or_label,
  `date` INT NULL,
  `production_line_no` VARCHAR(60) NULL,
  `oneProcess` INT NULL,
  `secProcess` INT NULL,
  `item_no` VARCHAR(255) NULL,
  -- FK candidate: `item_no` -> inproduct / product(`no`), needs_review,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> inproduct / product(`no`), denormalized_or_label,
  `materialLoss` FLOAT NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_production_data_work_order_no` (`work_order_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `production_data_output` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `work_order_no` VARCHAR(60) NULL,
  `process_order_no` VARCHAR(60) NULL,
  `group` VARCHAR(60) NULL,
  `time` INT NULL,
  `action` INT NULL,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> inproduct / product(`no`), needs_review,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> inproduct / product(`no`), denormalized_or_label,
  `category` INT NULL,
  `itemSubCategory` INT NULL,
  `batch_number` VARCHAR(60) NULL,
  `serial_no` VARCHAR(60) NULL,
  `valid_date` INT NULL,
  `valid_date_no` VARCHAR(60) NULL,
  `unit` INT NULL,
  `count` FLOAT NULL,
  `comment` VARCHAR(128) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_production_data_output_work_order_no` (`work_order_no`),
  UNIQUE KEY `uq_production_data_output_group` (`group`),
  UNIQUE KEY `uq_production_data_output_action` (`action`),
  UNIQUE KEY `uq_production_data_output_item_no` (`item_no`),
  UNIQUE KEY `uq_production_data_output_batch_number` (`batch_number`),
  UNIQUE KEY `uq_production_data_output_serial_no` (`serial_no`),
  UNIQUE KEY `uq_production_data_output_valid_date_no` (`valid_date_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `production_data_input` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `work_order_no` VARCHAR(60) NULL,
  `process_order_no` VARCHAR(60) NULL,
  `group` VARCHAR(60) NULL,
  `time` INT NULL,
  `action` INT NULL,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> material / product(`no`), needs_review,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> material / product(`no`), denormalized_or_label,
  `category` INT NULL,
  `itemSubCategory` INT NULL,
  `batch_number` VARCHAR(60) NULL,
  `serial_no` VARCHAR(60) NULL,
  `unit` INT NULL,
  `count` FLOAT NULL,
  `comment` VARCHAR(128) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_production_data_input_work_order_no` (`work_order_no`),
  UNIQUE KEY `uq_production_data_input_group` (`group`),
  UNIQUE KEY `uq_production_data_input_action` (`action`),
  UNIQUE KEY `uq_production_data_input_item_no` (`item_no`),
  UNIQUE KEY `uq_production_data_input_batch_number` (`batch_number`),
  UNIQUE KEY `uq_production_data_input_serial_no` (`serial_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `production_data_reuse` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `work_order_no` VARCHAR(60) NULL,
  `process_order_no` VARCHAR(60) NULL,
  `group` VARCHAR(60) NULL,
  `time` INT NULL,
  `action` INT NULL,
  `item_no` VARCHAR(60) NULL,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> inproduct(`no`), denormalized_or_label,
  `category` INT NULL,
  `itemSubCategory` INT NULL,
  `batch_number` VARCHAR(60) NULL,
  `serial_no` VARCHAR(60) NULL,
  `unit` INT NULL,
  `count` FLOAT NULL,
  `comment` VARCHAR(128) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_production_data_reuse_work_order_no` (`work_order_no`),
  UNIQUE KEY `uq_production_data_reuse_process_order_no` (`process_order_no`),
  UNIQUE KEY `uq_production_data_reuse_group` (`group`),
  UNIQUE KEY `uq_production_data_reuse_action` (`action`),
  UNIQUE KEY `uq_production_data_reuse_item_no` (`item_no`),
  UNIQUE KEY `uq_production_data_reuse_category` (`category`),
  UNIQUE KEY `uq_production_data_reuse_batch_number` (`batch_number`),
  UNIQUE KEY `uq_production_data_reuse_serial_no` (`serial_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `production_data_machine` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `work_order_no` VARCHAR(60) NULL,
  `equipment_no` VARCHAR(60) NULL,
  `equipment_name` VARCHAR(60) NULL,
  -- FK candidate: `equipment_name` -> equipment(`no`), denormalized_or_label,
  `time` INT NULL,
  `action` VARCHAR(60) NULL,
  `speed` FLOAT NULL,
  `temperature` FLOAT NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_production_data_machine_work_order_no` (`work_order_no`),
  UNIQUE KEY `uq_production_data_machine_equipment_no` (`equipment_no`),
  UNIQUE KEY `uq_production_data_machine_action` (`action`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `production_data_labor` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `work_order_no` VARCHAR(60) NULL,
  `employee_no` VARCHAR(60) NULL,
  `employee_name` VARCHAR(60) NULL,
  -- FK candidate: `employee_name` -> employee(`no`), denormalized_or_label,
  `employee_type` INT NULL,
  `employee_jobTitle` INT NULL,
  `employee_level` INT NULL,
  `station_no` VARCHAR(60) NULL,
  `stationStage` INT NULL,
  `action` INT NULL,
  `startTime` INT NULL,
  `endTime` INT NULL,
  `hours` FLOAT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_production_data_labor_work_order_no` (`work_order_no`),
  UNIQUE KEY `uq_production_data_labor_employee_no` (`employee_no`),
  UNIQUE KEY `uq_production_data_labor_stationStage` (`stationStage`),
  UNIQUE KEY `uq_production_data_labor_action` (`action`),
  UNIQUE KEY `uq_production_data_labor_startTime` (`startTime`),
  UNIQUE KEY `uq_production_data_labor_endTime` (`endTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `pl_man_capacity` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `month` DATE NULL,
  `pl_no` VARCHAR(60) NULL,
  `pl_name` VARCHAR(60) NULL,
  -- FK candidate: `pl_name` -> production_line(`no`), denormalized_or_label,
  `productCount` INT NULL,
  `laborCount` INT NULL,
  `unit` INT NULL,
  `hourlyOutput` DOUBLE NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_pl_man_capacity_month` (`month`),
  UNIQUE KEY `uq_pl_man_capacity_pl_no` (`pl_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `pl_item_capacity` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `month` DATE NULL,
  `pl_no` VARCHAR(60) NULL,
  `pl_name` VARCHAR(60) NULL,
  -- FK candidate: `pl_name` -> production_line(`no`), denormalized_or_label,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> inproduct / product(`no`), needs_review,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> inproduct / product(`no`), denormalized_or_label,
  `assembly_no` VARCHAR(60) NULL,
  `assemblyVer` INT NULL,
  `bomWeight` DOUBLE NULL,
  `bomUnit` INT NULL,
  `productCount` INT NULL,
  `hours` FLOAT NULL,
  `count` FLOAT NULL,
  `unit` INT NULL,
  `hourlyOutput` DOUBLE NULL,
  `price` DOUBLE NULL,
  `rawMaterialCost` DOUBLE NULL,
  `materialCost` DOUBLE NULL,
  `laborCost` DOUBLE NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_pl_item_capacity_month` (`month`),
  UNIQUE KEY `uq_pl_item_capacity_pl_no` (`pl_no`),
  UNIQUE KEY `uq_pl_item_capacity_item_no` (`item_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `pl_item_loss` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `month` DATE NULL,
  `pl_item_capacity_no` VARCHAR(60) NULL,
  -- FK candidate: `pl_item_capacity_no` -> pl_item_capacity(`no`), needs_review,
  `item_no` VARCHAR(60) NULL,
  -- FK candidate: `item_no` -> material / inproduct(`no`), needs_review,
  `item_name` VARCHAR(60) NULL,
  -- FK candidate: `item_name` -> material / inproduct(`no`), denormalized_or_label,
  `itemCategory` INT NULL,
  `itemSubCategory` INT NULL,
  `weightRatio` DOUBLE NULL,
  `lossRate` DOUBLE NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_pl_item_loss_month` (`month`),
  UNIQUE KEY `uq_pl_item_loss_item_no` (`item_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `employee` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(20) NULL,
  `name` VARCHAR(60) NULL,
  `sex` INT NULL,
  `department` INT NULL,
  `level` INT NULL,
  `jobTitle` VARCHAR(60) NULL,
  `joinedDate` INT NULL,
  `leftDate` INT NULL,
  `identityId` VARCHAR(60) NULL,
  `country` VARCHAR(60) NULL,
  `birthday` INT NULL,
  `phone` VARCHAR(60) NULL,
  `address` VARCHAR(100) NULL,
  `type` INT NULL,
  `category` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_employee_no` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `member` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_no` VARCHAR(60) NULL,
  `account` VARCHAR(60) NULL,
  `password` VARCHAR(100) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_member_user_no` (`user_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `session` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_no` VARCHAR(60) NULL,
  `token` VARCHAR(60) NULL,
  `expiredTime` INT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `user_group` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NULL,
  `role` INT NULL,
  `users` LONGTEXT NULL,
  -- FK candidate: `users` -> employee(`no`), denormalized_or_label,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_user_group_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- High-confidence inferred FK constraints
-- Apply after reviewing existing data quality and target uniqueness.
ALTER TABLE `company` ADD CONSTRAINT `fk_company_received_id` FOREIGN KEY (`received_id`) REFERENCES `payment` (`id`);
ALTER TABLE `company` ADD CONSTRAINT `fk_company_paid_id` FOREIGN KEY (`paid_id`) REFERENCES `payment` (`id`);
ALTER TABLE `inproduct_bom_spec` ADD CONSTRAINT `fk_inproduct_bom_spec_inproduct_no` FOREIGN KEY (`inproduct_no`) REFERENCES `inproduct` (`no`);
ALTER TABLE `product_ver` ADD CONSTRAINT `fk_product_ver_item_no` FOREIGN KEY (`item_no`) REFERENCES `product` (`no`);
ALTER TABLE `product_spec` ADD CONSTRAINT `fk_product_spec_product_no` FOREIGN KEY (`product_no`) REFERENCES `product` (`no`);
ALTER TABLE `product_bom_spec` ADD CONSTRAINT `fk_product_bom_spec_product_no` FOREIGN KEY (`product_no`) REFERENCES `product` (`no`);
ALTER TABLE `product_bom_spec` ADD CONSTRAINT `fk_product_bom_spec_bom2_no` FOREIGN KEY (`bom2_no`) REFERENCES `bom2_number` (`no`);
ALTER TABLE `trans_items` ADD CONSTRAINT `fk_trans_items_company_no` FOREIGN KEY (`company_no`) REFERENCES `company` (`no`);
ALTER TABLE `trans_items2` ADD CONSTRAINT `fk_trans_items2_company_no` FOREIGN KEY (`company_no`) REFERENCES `company` (`no`);
ALTER TABLE `ship_wh` ADD CONSTRAINT `fk_ship_wh_company_no` FOREIGN KEY (`company_no`) REFERENCES `company` (`no`);
ALTER TABLE `bom_item` ADD CONSTRAINT `fk_bom_item_bom_no` FOREIGN KEY (`bom_no`) REFERENCES `bom` (`no`);
ALTER TABLE `bom_item` ADD CONSTRAINT `fk_bom_item_item_no` FOREIGN KEY (`item_no`) REFERENCES `material` (`no`);
ALTER TABLE `bom1_number` ADD CONSTRAINT `fk_bom1_number_bom_no` FOREIGN KEY (`bom_no`) REFERENCES `bom` (`no`);
ALTER TABLE `bom1` ADD CONSTRAINT `fk_bom1_parent_no` FOREIGN KEY (`parent_no`) REFERENCES `bom1_number` (`no`);
ALTER TABLE `bom2_number` ADD CONSTRAINT `fk_bom2_number_bom_no` FOREIGN KEY (`bom_no`) REFERENCES `product` (`no`);
ALTER TABLE `bom2` ADD CONSTRAINT `fk_bom2_parent_no` FOREIGN KEY (`parent_no`) REFERENCES `bom2_number` (`no`);
ALTER TABLE `sample_price` ADD CONSTRAINT `fk_sample_price_item_no` FOREIGN KEY (`item_no`) REFERENCES `bom` (`no`);
ALTER TABLE `process_flow` ADD CONSTRAINT `fk_process_flow_product_process_no` FOREIGN KEY (`product_process_no`) REFERENCES `product_process` (`no`);
ALTER TABLE `batch_number` ADD CONSTRAINT `fk_batch_number_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `batch_number` ADD CONSTRAINT `fk_batch_number_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `inventory_order` ADD CONSTRAINT `fk_inventory_order_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `inventory_order` ADD CONSTRAINT `fk_inventory_order_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `inventory_record` ADD CONSTRAINT `fk_inventory_record_warehouse_no` FOREIGN KEY (`warehouse_no`) REFERENCES `ship_wh_alias` (`no`);
ALTER TABLE `inventory_record` ADD CONSTRAINT `fk_inventory_record_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `inventory_delta` ADD CONSTRAINT `fk_inventory_delta_warehouse_no` FOREIGN KEY (`warehouse_no`) REFERENCES `ship_wh_alias` (`no`);
ALTER TABLE `inventory_delta` ADD CONSTRAINT `fk_inventory_delta_in_ref_id` FOREIGN KEY (`in_ref_id`) REFERENCES `inventory_record` (`id`);
ALTER TABLE `inventory_delta` ADD CONSTRAINT `fk_inventory_delta_out_ref_id` FOREIGN KEY (`out_ref_id`) REFERENCES `inventory_record` (`id`);
ALTER TABLE `Inventory_month_statistic` ADD CONSTRAINT `fk_Inventory_month_statistic_warehouse_no` FOREIGN KEY (`warehouse_no`) REFERENCES `ship_wh_alias` (`no`);
ALTER TABLE `Inventory_item_month_statistic` ADD CONSTRAINT `fk_Inventory_item_month_statistic_warehouse_no` FOREIGN KEY (`warehouse_no`) REFERENCES `ship_wh_alias` (`no`);
ALTER TABLE `quotation` ADD CONSTRAINT `fk_quotation_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `quotation` ADD CONSTRAINT `fk_quotation_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `ship_wh_quotation` ADD CONSTRAINT `fk_ship_wh_quotation_item_no` FOREIGN KEY (`item_no`) REFERENCES `ship_wh` (`no`);
ALTER TABLE `ship_wh_quotation` ADD CONSTRAINT `fk_ship_wh_quotation_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `contract` ADD CONSTRAINT `fk_contract_ref_no` FOREIGN KEY (`ref_no`) REFERENCES `quotation` (`no`);
ALTER TABLE `contract` ADD CONSTRAINT `fk_contract_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `contract` ADD CONSTRAINT `fk_contract_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `contract` ADD CONSTRAINT `fk_contract_payment_id` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`id`);
ALTER TABLE `ship_wh_contract` ADD CONSTRAINT `fk_ship_wh_contract_ref_no` FOREIGN KEY (`ref_no`) REFERENCES `ship_wh_quotation` (`no`);
ALTER TABLE `ship_wh_contract` ADD CONSTRAINT `fk_ship_wh_contract_sw_alias_no` FOREIGN KEY (`sw_alias_no`) REFERENCES `ship_wh_alias` (`no`);
ALTER TABLE `ship_wh_contract` ADD CONSTRAINT `fk_ship_wh_contract_item_no` FOREIGN KEY (`item_no`) REFERENCES `ship_wh` (`no`);
ALTER TABLE `ship_wh_contract` ADD CONSTRAINT `fk_ship_wh_contract_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `product_order` ADD CONSTRAINT `fk_product_order_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `product_order` ADD CONSTRAINT `fk_product_order_ref_no` FOREIGN KEY (`ref_no`) REFERENCES `contract` (`no`);
ALTER TABLE `product_order` ADD CONSTRAINT `fk_product_order_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `product_order` ADD CONSTRAINT `fk_product_order_item_no` FOREIGN KEY (`item_no`) REFERENCES `trans_items` (`no`);
ALTER TABLE `shipping_order` ADD CONSTRAINT `fk_shipping_order_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `shipping_order` ADD CONSTRAINT `fk_shipping_order_product_order_no` FOREIGN KEY (`product_order_no`) REFERENCES `product_order` (`no`);
ALTER TABLE `shipping_order` ADD CONSTRAINT `fk_shipping_order_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `shipping_order` ADD CONSTRAINT `fk_shipping_order_item_no` FOREIGN KEY (`item_no`) REFERENCES `trans_items` (`no`);
ALTER TABLE `purchase_request` ADD CONSTRAINT `fk_purchase_request_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `purchase_request` ADD CONSTRAINT `fk_purchase_request_product_order_no` FOREIGN KEY (`product_order_no`) REFERENCES `product_order` (`no`);
ALTER TABLE `purchase_request_item` ADD CONSTRAINT `fk_purchase_request_item_purchase_request_no` FOREIGN KEY (`purchase_request_no`) REFERENCES `purchase_request` (`no`);
ALTER TABLE `purchase_request_item` ADD CONSTRAINT `fk_purchase_request_item_item_no` FOREIGN KEY (`item_no`) REFERENCES `material` (`no`);
ALTER TABLE `purchase_order` ADD CONSTRAINT `fk_purchase_order_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `purchase_order` ADD CONSTRAINT `fk_purchase_order_purchase_request_no` FOREIGN KEY (`purchase_request_no`) REFERENCES `purchase_request` (`no`);
ALTER TABLE `purchase_order` ADD CONSTRAINT `fk_purchase_order_ref_no` FOREIGN KEY (`ref_no`) REFERENCES `contract` (`no`);
ALTER TABLE `purchase_order` ADD CONSTRAINT `fk_purchase_order_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `purchase_order` ADD CONSTRAINT `fk_purchase_order_item_no` FOREIGN KEY (`item_no`) REFERENCES `trans_items` (`no`);
ALTER TABLE `goods_receipt_note` ADD CONSTRAINT `fk_goods_receipt_note_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `goods_receipt_note` ADD CONSTRAINT `fk_goods_receipt_note_purchase_order_no` FOREIGN KEY (`purchase_order_no`) REFERENCES `purchase_order` (`no`);
ALTER TABLE `goods_receipt_note` ADD CONSTRAINT `fk_goods_receipt_note_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `goods_receipt_note` ADD CONSTRAINT `fk_goods_receipt_note_item_no` FOREIGN KEY (`item_no`) REFERENCES `trans_items` (`no`);
ALTER TABLE `order_payment` ADD CONSTRAINT `fk_order_payment_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `shipping_record` ADD CONSTRAINT `fk_shipping_record_contract_no` FOREIGN KEY (`contract_no`) REFERENCES `ship_wh_contract` (`no`);
ALTER TABLE `shipping_record` ADD CONSTRAINT `fk_shipping_record_sw_alias_no` FOREIGN KEY (`sw_alias_no`) REFERENCES `ship_wh_alias` (`no`);
ALTER TABLE `shipping_record` ADD CONSTRAINT `fk_shipping_record_item_no` FOREIGN KEY (`item_no`) REFERENCES `ship_wh` (`no`);
ALTER TABLE `shipping_record` ADD CONSTRAINT `fk_shipping_record_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `warehouse_record` ADD CONSTRAINT `fk_warehouse_record_batch_no` FOREIGN KEY (`batch_no`) REFERENCES `batch_number` (`no`);
ALTER TABLE `warehouse_record` ADD CONSTRAINT `fk_warehouse_record_contract_no` FOREIGN KEY (`contract_no`) REFERENCES `ship_wh_contract` (`no`);
ALTER TABLE `warehouse_record` ADD CONSTRAINT `fk_warehouse_record_sw_alias_no` FOREIGN KEY (`sw_alias_no`) REFERENCES `ship_wh_alias` (`no`);
ALTER TABLE `warehouse_record` ADD CONSTRAINT `fk_warehouse_record_item_no` FOREIGN KEY (`item_no`) REFERENCES `ship_wh` (`no`);
ALTER TABLE `warehouse_record` ADD CONSTRAINT `fk_warehouse_record_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `shipping_payment` ADD CONSTRAINT `fk_shipping_payment_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `warehouse_payment` ADD CONSTRAINT `fk_warehouse_payment_batch_no` FOREIGN KEY (`batch_no`) REFERENCES `batch_number` (`no`);
ALTER TABLE `warehouse_payment` ADD CONSTRAINT `fk_warehouse_payment_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `order_item_month_statistic` ADD CONSTRAINT `fk_order_item_month_statistic_specified_no` FOREIGN KEY (`specified_no`) REFERENCES `company` (`no`);
ALTER TABLE `production_line` ADD CONSTRAINT `fk_production_line_process_no` FOREIGN KEY (`process_no`) REFERENCES `process` (`no`);
ALTER TABLE `production_line` ADD CONSTRAINT `fk_production_line_factory_no` FOREIGN KEY (`factory_no`) REFERENCES `factory` (`no`);
ALTER TABLE `station` ADD CONSTRAINT `fk_station_productionline_no` FOREIGN KEY (`productionline_no`) REFERENCES `production_line` (`no`);
ALTER TABLE `equipment` ADD CONSTRAINT `fk_equipment_station_no` FOREIGN KEY (`station_no`) REFERENCES `station` (`no`);
ALTER TABLE `aps_quantity` ADD CONSTRAINT `fk_aps_quantity_product_order_no` FOREIGN KEY (`product_order_no`) REFERENCES `product_order` (`no`);
ALTER TABLE `aps_quantity_item` ADD CONSTRAINT `fk_aps_quantity_item_product_order_no` FOREIGN KEY (`product_order_no`) REFERENCES `product_order` (`no`);
ALTER TABLE `aps_quantity_item` ADD CONSTRAINT `fk_aps_quantity_item_item_no` FOREIGN KEY (`item_no`) REFERENCES `material` (`no`);
ALTER TABLE `work_order` ADD CONSTRAINT `fk_work_order_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `work_order` ADD CONSTRAINT `fk_work_order_product_order_no` FOREIGN KEY (`product_order_no`) REFERENCES `product_order` (`no`);
ALTER TABLE `work_order` ADD CONSTRAINT `fk_work_order_aps_no` FOREIGN KEY (`aps_no`) REFERENCES `aps_quantity` (`no`);
ALTER TABLE `work_order` ADD CONSTRAINT `fk_work_order_product_no` FOREIGN KEY (`product_no`) REFERENCES `product` (`no`);
ALTER TABLE `work_order` ADD CONSTRAINT `fk_work_order_customer_no` FOREIGN KEY (`customer_no`) REFERENCES `company` (`no`);
ALTER TABLE `work_order` ADD CONSTRAINT `fk_work_order_production_line_no` FOREIGN KEY (`production_line_no`) REFERENCES `production_line` (`no`);
ALTER TABLE `process_order` ADD CONSTRAINT `fk_process_order_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `process_order` ADD CONSTRAINT `fk_process_order_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `process_order` ADD CONSTRAINT `fk_process_order_item_ref_no` FOREIGN KEY (`item_ref_no`) REFERENCES `company` (`no`);
ALTER TABLE `process_labor` ADD CONSTRAINT `fk_process_labor_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `process_labor` ADD CONSTRAINT `fk_process_labor_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `process_labor` ADD CONSTRAINT `fk_process_labor_employee_no` FOREIGN KEY (`employee_no`) REFERENCES `employee` (`no`);
ALTER TABLE `process_labor` ADD CONSTRAINT `fk_process_labor_production_line_no` FOREIGN KEY (`production_line_no`) REFERENCES `production_line` (`no`);
ALTER TABLE `process_labor` ADD CONSTRAINT `fk_process_labor_station_no` FOREIGN KEY (`station_no`) REFERENCES `station` (`no`);
ALTER TABLE `production_data` ADD CONSTRAINT `fk_production_data_creator_no` FOREIGN KEY (`creator_no`) REFERENCES `employee` (`no`);
ALTER TABLE `production_data` ADD CONSTRAINT `fk_production_data_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `production_data` ADD CONSTRAINT `fk_production_data_product_order_no` FOREIGN KEY (`product_order_no`) REFERENCES `product_order` (`no`);
ALTER TABLE `production_data` ADD CONSTRAINT `fk_production_data_customer_no` FOREIGN KEY (`customer_no`) REFERENCES `company` (`no`);
ALTER TABLE `production_data` ADD CONSTRAINT `fk_production_data_product_no` FOREIGN KEY (`product_no`) REFERENCES `product` (`no`);
ALTER TABLE `production_data` ADD CONSTRAINT `fk_production_data_production_line_no` FOREIGN KEY (`production_line_no`) REFERENCES `production_line` (`no`);
ALTER TABLE `production_data_output` ADD CONSTRAINT `fk_production_data_output_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `production_data_output` ADD CONSTRAINT `fk_production_data_output_process_order_no` FOREIGN KEY (`process_order_no`) REFERENCES `process_order` (`no`);
ALTER TABLE `production_data_input` ADD CONSTRAINT `fk_production_data_input_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `production_data_input` ADD CONSTRAINT `fk_production_data_input_process_order_no` FOREIGN KEY (`process_order_no`) REFERENCES `process_order` (`no`);
ALTER TABLE `production_data_reuse` ADD CONSTRAINT `fk_production_data_reuse_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `production_data_reuse` ADD CONSTRAINT `fk_production_data_reuse_process_order_no` FOREIGN KEY (`process_order_no`) REFERENCES `process_order` (`no`);
ALTER TABLE `production_data_reuse` ADD CONSTRAINT `fk_production_data_reuse_item_no` FOREIGN KEY (`item_no`) REFERENCES `inproduct` (`no`);
ALTER TABLE `production_data_machine` ADD CONSTRAINT `fk_production_data_machine_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `production_data_machine` ADD CONSTRAINT `fk_production_data_machine_equipment_no` FOREIGN KEY (`equipment_no`) REFERENCES `equipment` (`no`);
ALTER TABLE `production_data_labor` ADD CONSTRAINT `fk_production_data_labor_work_order_no` FOREIGN KEY (`work_order_no`) REFERENCES `work_order` (`no`);
ALTER TABLE `production_data_labor` ADD CONSTRAINT `fk_production_data_labor_employee_no` FOREIGN KEY (`employee_no`) REFERENCES `employee` (`no`);
ALTER TABLE `production_data_labor` ADD CONSTRAINT `fk_production_data_labor_station_no` FOREIGN KEY (`station_no`) REFERENCES `station` (`no`);
ALTER TABLE `pl_man_capacity` ADD CONSTRAINT `fk_pl_man_capacity_pl_no` FOREIGN KEY (`pl_no`) REFERENCES `production_line` (`no`);
ALTER TABLE `pl_item_capacity` ADD CONSTRAINT `fk_pl_item_capacity_pl_no` FOREIGN KEY (`pl_no`) REFERENCES `production_line` (`no`);
ALTER TABLE `member` ADD CONSTRAINT `fk_member_user_no` FOREIGN KEY (`user_no`) REFERENCES `employee` (`no`);
ALTER TABLE `session` ADD CONSTRAINT `fk_session_user_no` FOREIGN KEY (`user_no`) REFERENCES `employee` (`no`);

SET FOREIGN_KEY_CHECKS = 1;
