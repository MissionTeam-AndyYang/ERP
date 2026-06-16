-- Warehouse Dashboard extension schema
-- Base schema: docs/database/EWDB_20260526.sql
-- Source spec: docs/spec/database/WAREHOUSE_OVERVIEW_DB_EXTENSION_PLAN.md
-- Generated on 2026-06-16
-- Notes:
-- 1. This migration creates only the engineer-confirmed Warehouse Dashboard extension tables.
-- 2. Existing tables are not modified.
-- 3. The first Warehouse Dashboard version does not include inventory counting tables.

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
CREATE DATABASE IF NOT EXISTS `ewdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `ewdb`;

CREATE TABLE IF NOT EXISTS `warehouse_inventory_reservation` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NOT NULL,
  `date` INT NOT NULL,
  `refCategory` INT NOT NULL,
  `ref_no` VARCHAR(60) NOT NULL,
  `ref_sub_no` VARCHAR(60) NULL,
  `warehouse_no` VARCHAR(60) NULL,
  `warehouse_displayName` VARCHAR(60) NULL,
  `itemCategory` INT NOT NULL,
  `item_no` VARCHAR(60) NOT NULL,
  `item_name` VARCHAR(255) NULL,
  `batchNumber` VARCHAR(60) NULL,
  `unit` INT NULL,
  `reservedQuantity` FLOAT NOT NULL DEFAULT 0,
  `unitCost` FLOAT NULL,
  `reservedValue` FLOAT NULL,
  `status` INT NOT NULL,
  `releaseTime` INT NULL,
  `comment` TEXT NULL,
  `creationTime` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_warehouse_inventory_reservation_composite` (`no`),
  KEY `idx_wir_item_batch_wh_status` (`item_no`, `batchNumber`, `warehouse_no`, `status`),
  KEY `idx_wir_ref` (`refCategory`, `ref_no`, `ref_sub_no`),
  KEY `idx_wir_date` (`date`),
  KEY `idx_wir_warehouse` (`warehouse_no`),
  KEY `idx_wir_item_category` (`itemCategory`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `warehouse_quality_hold` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NOT NULL,
  `date` INT NOT NULL,
  `refCategory` INT NOT NULL,
  `ref_no` VARCHAR(60) NOT NULL,
  `ref_sub_no` VARCHAR(60) NULL,
  `inspection_no` VARCHAR(60) NULL,
  `warehouse_no` VARCHAR(60) NULL,
  `warehouse_displayName` VARCHAR(60) NULL,
  `itemCategory` INT NOT NULL,
  `item_no` VARCHAR(60) NOT NULL,
  `item_name` VARCHAR(255) NULL,
  `batchNumber` VARCHAR(60) NOT NULL,
  `unit` INT NULL,
  `holdQuantity` FLOAT NOT NULL DEFAULT 0,
  `unitCost` FLOAT NULL,
  `holdValue` FLOAT NULL,
  `status` INT NOT NULL,
  `releaseTime` INT NULL,
  `reason` VARCHAR(255) NULL,
  `comment` TEXT NULL,
  `creationTime` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_warehouse_quality_hold_composite` (`no`),
  KEY `idx_wqh_item_batch_wh_status` (`item_no`, `batchNumber`, `warehouse_no`, `status`),
  KEY `idx_wqh_ref` (`refCategory`, `ref_no`, `ref_sub_no`),
  KEY `idx_wqh_inspection` (`inspection_no`),
  KEY `idx_wqh_date` (`date`),
  KEY `idx_wqh_warehouse` (`warehouse_no`),
  KEY `idx_wqh_item_category` (`itemCategory`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `warehouse_pallet_movement` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NOT NULL,
  `date` INT NOT NULL,
  `inventory_record_id` BIGINT UNSIGNED NULL,
  `refCategory` INT NOT NULL,
  `ref_no` VARCHAR(60) NULL,
  `warehouse_no` VARCHAR(60) NOT NULL,
  `pallet_group_no` VARCHAR(60) NOT NULL,
  `batchNumber` VARCHAR(60) NULL,
  `serialNo` VARCHAR(60) NULL,
  `itemCategory` INT NULL,
  `item_no` VARCHAR(60) NULL,
  `palletStatus` INT NOT NULL,
  `palletCount` FLOAT NOT NULL DEFAULT 0,
  `creationTime` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_warehouse_pallet_movement_composite` (`no`),
  KEY `idx_wpm_inventory_record` (`inventory_record_id`),
  KEY `idx_wpm_ref` (`refCategory`, `ref_no`),
  KEY `idx_wpm_wh_item_batch_status` (`warehouse_no`, `item_no`, `batchNumber`, `palletStatus`),
  KEY `idx_wpm_pallet_group` (`pallet_group_no`),
  KEY `idx_wpm_item_category` (`itemCategory`),
  KEY `idx_wpm_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `item_safety_stock` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NOT NULL,
  `itemCategory` INT NOT NULL,
  `item_no` VARCHAR(60) NOT NULL,
  `item_name` VARCHAR(255) NULL,
  `warehouse_no` VARCHAR(60) NULL,
  `unit` INT NULL,
  `safetyStock` FLOAT NOT NULL DEFAULT 0,
  `effectiveDate` INT NOT NULL,
  `expiryDate` INT NULL,
  `status` INT NOT NULL,
  `comment` TEXT NULL,
  `creationTime` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_item_safety_stock_composite` (`no`),
  KEY `idx_iss_item_wh_status` (`item_no`, `warehouse_no`, `status`),
  KEY `idx_iss_item_category` (`itemCategory`),
  KEY `idx_iss_effective_date` (`effectiveDate`),
  KEY `idx_iss_expiry_date` (`expiryDate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `warehouse_risk_rule` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `riskType` VARCHAR(60) NOT NULL,
  `riskLevel` INT NOT NULL,
  `messageCode` VARCHAR(80) NOT NULL,
  `messageTemplateZhTw` VARCHAR(255) NULL,
  `recommendedActionCode` VARCHAR(80) NOT NULL,
  `recommendedActionTemplateZhTw` VARCHAR(255) NULL,
  `thresholdValue` FLOAT NULL,
  `excludedItemCategories` LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `status` INT NOT NULL,
  `creationTime` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_warehouse_risk_rule_composite` (`riskType`),
  KEY `idx_wrr_status` (`status`),
  KEY `idx_wrr_risk_level` (`riskLevel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `workflow_task_state` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `taskId` VARCHAR(80) NOT NULL,
  `module` INT NOT NULL,
  `taskType` INT NOT NULL,
  `refCategory` INT NOT NULL,
  `ref_no` VARCHAR(60) NOT NULL,
  `ref_sub_no` VARCHAR(60) NULL,
  `itemCategory` INT NULL,
  `item_no` VARCHAR(60) NULL,
  `item_name` VARCHAR(255) NULL,
  `batchNumber` VARCHAR(60) NULL,
  `warehouse_no` VARCHAR(60) NULL,
  `expectedQuantity` FLOAT NULL,
  `processedQuantity` FLOAT NULL,
  `acceptedQuantity` FLOAT NULL,
  `rejectedQuantity` FLOAT NULL,
  `cancelledQuantity` FLOAT NULL,
  `unit` INT NULL,
  `palletCount` FLOAT NULL,
  `dueTimestamp` INT NULL,
  `taskStatus` INT NOT NULL,
  `ownerDepartment` INT NOT NULL,
  `blockReasonCode` VARCHAR(80) NULL,
  `blockReason` VARCHAR(255) NULL,
  `updateTime` INT NULL,
  `creationTime` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_workflow_task_state_composite` (`taskId`),
  KEY `idx_wts_task_status_due` (`taskStatus`, `dueTimestamp`),
  KEY `idx_wts_task_type_status` (`taskType`, `taskStatus`),
  KEY `idx_wts_ref` (`refCategory`, `ref_no`, `ref_sub_no`),
  KEY `idx_wts_warehouse` (`warehouse_no`),
  KEY `idx_wts_item_batch` (`item_no`, `batchNumber`),
  KEY `idx_wts_owner_department` (`ownerDepartment`),
  KEY `idx_wts_module` (`module`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `workflow_next_owner_rule` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NOT NULL,
  `module` INT NOT NULL,
  `taskType` INT NOT NULL,
  `refCategory` INT NULL,
  `taskStatus` INT NULL,
  `blockReasonCode` VARCHAR(80) NULL,
  `fromDepartment` INT NULL,
  `ownerDepartment` INT NOT NULL,
  `rulePriority` INT NOT NULL,
  `status` INT NOT NULL,
  `comment` TEXT NULL,
  `creationTime` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_workflow_next_owner_rule_composite` (`no`),
  KEY `idx_wnor_task_condition` (`module`, `taskType`, `refCategory`, `taskStatus`),
  KEY `idx_wnor_block_reason` (`blockReasonCode`),
  KEY `idx_wnor_from_department` (`fromDepartment`),
  KEY `idx_wnor_owner_department` (`ownerDepartment`),
  KEY `idx_wnor_priority_status` (`rulePriority`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
