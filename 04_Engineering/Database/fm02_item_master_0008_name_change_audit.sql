-- FM-02 Item Master 0008: append-only Item Name correction evidence.

DELIMITER //
CREATE PROCEDURE fm02_item_master_0008_revision_guard()
BEGIN
  DECLARE current_revision VARCHAR(255);
  SELECT version_num INTO current_revision FROM alembic_version LIMIT 1;
  IF current_revision IS NULL
     OR current_revision <> 'fm02_item_master_0007_code_allocation_nonreuse' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 0008 requires revision fm02_item_master_0007_code_allocation_nonreuse';
  END IF;
END//
DELIMITER ;

CALL fm02_item_master_0008_revision_guard();
DROP PROCEDURE fm02_item_master_0008_revision_guard;

CREATE TABLE item_name_change_audit (
  audit_id CHAR(36) NOT NULL,
  item_id CHAR(36) NOT NULL,
  before_display_name VARCHAR(255) NOT NULL,
  after_display_name VARCHAR(255) NOT NULL,
  change_reason TEXT NOT NULL,
  changed_at DATETIME(6) NOT NULL,
  business_actor_type VARCHAR(16) NOT NULL,
  business_actor_ref VARCHAR(128) NOT NULL,
  approval_evidence_ref VARCHAR(255) NOT NULL,
  technical_work_item_id VARCHAR(128) NULL,
  technical_executor_ref VARCHAR(128) NULL,
  correlation_id VARCHAR(128) NOT NULL,
  idempotency_key VARCHAR(128) NOT NULL,
  PRIMARY KEY (audit_id),
  UNIQUE KEY uq_item_name_change_audit_idempotency (item_id, idempotency_key),
  KEY ix_item_name_change_audit_history (item_id, changed_at),
  CONSTRAINT fk_item_name_change_audit_item
    FOREIGN KEY (item_id) REFERENCES item (item_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT ck_item_name_change_audit_changed
    CHECK (before_display_name <> after_display_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

UPDATE alembic_version
SET version_num = 'fm02_item_master_0008_name_change_audit'
WHERE version_num = 'fm02_item_master_0007_code_allocation_nonreuse';
