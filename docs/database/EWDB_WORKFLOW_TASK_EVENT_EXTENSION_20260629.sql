-- ERP 2.0 Workflow Task Event Extension
-- Source proposal: docs/spec/api-proposal/warehouse_task_workbench_db_extension_proposal.md
-- Purpose: add workflow_task_event for cross-module task timeline history.

CREATE TABLE IF NOT EXISTS `workflow_task_event` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自動遞增流水號',
  `taskId` VARCHAR(80) NOT NULL COMMENT '對應 workflow_task_state.taskId',
  `eventCode` VARCHAR(80) NOT NULL COMMENT '任務事件代碼，前端依 code 轉換顯示文字',
  `eventTimestamp` BIGINT NOT NULL COMMENT '事件發生時間，UTC timestamp',
  `fromStatus` INT NULL COMMENT '事件前任務狀態',
  `toStatus` INT NULL COMMENT '事件後任務狀態',
  `fromDepartment` INT NULL COMMENT '事件前負責部門',
  `toDepartment` INT NULL COMMENT '事件後負責部門',
  `actorId` VARCHAR(60) NULL COMMENT '操作人或系統程序識別碼',
  `actorName` VARCHAR(60) NULL COMMENT '操作人顯示名稱',
  `refCategory` INT NULL COMMENT '事件關聯來源類別',
  `ref_no` VARCHAR(60) NULL COMMENT '事件關聯來源單號',
  `ref_sub_no` VARCHAR(60) NULL COMMENT '事件關聯來源明細編號',
  `warehouse_no` VARCHAR(60) NULL COMMENT '事件關聯倉儲別名 no',
  `item_no` VARCHAR(60) NULL COMMENT '事件關聯料號',
  `batchNumber` VARCHAR(60) NULL COMMENT '事件關聯批號',
  `quantity` DECIMAL(18, 4) NULL COMMENT '事件關聯數量，僅保存正數；方向由 eventCode 判斷',
  `unit` INT NULL COMMENT '數量單位，沿用 Unit enum',
  `reasonCode` VARCHAR(80) NULL COMMENT '阻塞、退回、取消或調整原因代碼',
  `note` TEXT NULL COMMENT '人工備註或系統訊息',
  `creationTime` BIGINT NOT NULL COMMENT '建立時間，UTC timestamp',
  `updateTime` BIGINT NULL COMMENT '更新時間，UTC timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_workflow_task_event_task_time` (`taskId`, `eventTimestamp`, `id`),
  KEY `idx_workflow_task_event_ref` (`refCategory`, `ref_no`, `ref_sub_no`),
  KEY `idx_workflow_task_event_lot` (`warehouse_no`, `item_no`, `batchNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='跨模組 workflow task 歷史事件表';
