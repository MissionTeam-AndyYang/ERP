-- ERP2-ROUTING-PROCESS-FLOW-SHARED-DEV-DATA-SURFACE-001
-- Purpose: bounded non-production Shared DEV acceptance test-support surface only.
-- Boundary: not a Production schema migration, not target schema authority, and not a Source-of-Truth transition.

CREATE TABLE IF NOT EXISTS `product_process` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NOT NULL,
  `item_no` VARCHAR(60) NOT NULL,
  `version` INT NOT NULL,
  `date` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_product_process_composite` (`no`, `item_no`, `version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `process` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NOT NULL,
  `oneProcess` INT NULL,
  `secProcess` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_process_composite` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `process_capacity` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `date` INT NOT NULL,
  `oneProcess` INT NOT NULL,
  `secProcess` INT NOT NULL,
  `unit` INT NULL,
  `hourlyOutput` DOUBLE NULL,
  `laborCount` INT NULL,
  `comment` VARCHAR(128) NULL,
  `creationTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_process_capacity_composite` (`date`, `oneProcess`, `secProcess`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `process_flow` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NOT NULL,
  `product_process_no` VARCHAR(60) NOT NULL,
  `order` INT NOT NULL,
  `oneProcess` INT NULL,
  `secProcess` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_process_flow_composite` (`no`, `product_process_no`, `order`),
  CONSTRAINT `fk_process_flow_product_process_no` FOREIGN KEY (`product_process_no`) REFERENCES `product_process` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `product_process` (`no`, `item_no`, `version`, `date`)
VALUES
  ('RT-SD-PRD-001-V1', 'PRD-SD-001', 1, 1700000000),
  ('RT-SD-PRD-001-V2', 'PRD-SD-001', 2, 1900000000),
  ('RT-SD-INP-001-V1', 'INP-SD-001', 1, 1700000000)
ON DUPLICATE KEY UPDATE
  `date` = VALUES(`date`);

INSERT INTO `process` (`no`, `oneProcess`, `secProcess`, `comment`, `creationTime`)
VALUES
  ('PROC-SD-PREP-MIX', 1, 1, 'routing.process.preparation_mix', 1700000000),
  ('PROC-SD-PREP-FILL', 1, 2, 'routing.process.preparation_fill', 1700000000),
  ('PROC-SD-PROC-COAT', 2, 1, 'routing.process.processing_coat', 1700000000)
ON DUPLICATE KEY UPDATE
  `oneProcess` = VALUES(`oneProcess`),
  `secProcess` = VALUES(`secProcess`),
  `comment` = VALUES(`comment`),
  `creationTime` = VALUES(`creationTime`);

INSERT INTO `process_capacity` (`date`, `oneProcess`, `secProcess`, `unit`, `hourlyOutput`, `laborCount`, `comment`, `creationTime`)
VALUES
  (1700000000, 1, 1, 101, 120.125, 3, 'Shared DEV routing test-support standard performance', 1700000000),
  (1700000000, 2, 1, 101, 96.5, 4, 'Shared DEV routing test-support standard performance', 1700000000)
ON DUPLICATE KEY UPDATE
  `unit` = VALUES(`unit`),
  `hourlyOutput` = VALUES(`hourlyOutput`),
  `laborCount` = VALUES(`laborCount`),
  `comment` = VALUES(`comment`),
  `creationTime` = VALUES(`creationTime`);

INSERT INTO `process_flow` (`no`, `product_process_no`, `order`, `oneProcess`, `secProcess`)
VALUES
  ('STEP-SD-PRD-001-001', 'RT-SD-PRD-001-V1', 1, 1, 1),
  ('STEP-SD-PRD-001-002', 'RT-SD-PRD-001-V1', 2, 2, 1),
  ('STEP-SD-PRD-001-V2-001', 'RT-SD-PRD-001-V2', 1, 1, 1),
  ('STEP-SD-INP-001-001', 'RT-SD-INP-001-V1', 1, 1, 2)
ON DUPLICATE KEY UPDATE
  `oneProcess` = VALUES(`oneProcess`),
  `secProcess` = VALUES(`secProcess`);
