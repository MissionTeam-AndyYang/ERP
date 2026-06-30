-- ERP 2.0 Workflow Task Event Column Rename
-- Purpose: rename workflow_task_event.note to workflow_task_event.comment.
-- Apply this migration only if workflow_task_event was already created with the old note column.

ALTER TABLE `workflow_task_event`
  CHANGE COLUMN `note` `comment` TEXT NULL COMMENT '人工備註或系統訊息';
