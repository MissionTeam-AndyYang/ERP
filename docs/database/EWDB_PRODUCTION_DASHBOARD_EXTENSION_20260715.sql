-- Production Dashboard API confirmed schema extension
-- Source: production_dashboard_proposal.md / production_dashboard_flow_algorithm.md
-- Status: confirmed by engineer; execute after the current EWDB baseline.

CREATE TABLE IF NOT EXISTS `production_line_daily_capacity` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NOT NULL,
  `effectiveDate` INT NOT NULL,
  `production_line_no` VARCHAR(60) NOT NULL,
  `availableMinutes` INT NOT NULL,
  `status` INT NOT NULL,
  `comment` TEXT NULL,
  `creator_no` VARCHAR(60) NULL,
  `creationTime` INT NOT NULL,
  `lastUpdateTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_production_line_daily_capacity_no` (`no`),
  UNIQUE KEY `uq_production_line_daily_capacity_effective_line` (`effectiveDate`, `production_line_no`),
  KEY `idx_production_line_daily_capacity_line_effective` (`production_line_no`, `effectiveDate`),
  KEY `idx_production_line_daily_capacity_status` (`status`),
  CONSTRAINT `fk_production_line_daily_capacity_line`
    FOREIGN KEY (`production_line_no`) REFERENCES `production_line` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `production_line_downtime` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `no` VARCHAR(60) NOT NULL,
  `production_line_no` VARCHAR(60) NOT NULL,
  `startTime` INT NOT NULL,
  `endTime` INT NOT NULL,
  `durationMinutes` INT NOT NULL,
  `reasonType` INT NOT NULL,
  `status` INT NOT NULL,
  `comment` TEXT NULL,
  `creator_no` VARCHAR(60) NULL,
  `creationTime` INT NOT NULL,
  `lastUpdateTime` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_production_line_downtime_no` (`no`),
  KEY `idx_production_line_downtime_line_time` (`production_line_no`, `startTime`, `endTime`),
  KEY `idx_production_line_downtime_status` (`status`),
  CONSTRAINT `fk_production_line_downtime_line`
    FOREIGN KEY (`production_line_no`) REFERENCES `production_line` (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
