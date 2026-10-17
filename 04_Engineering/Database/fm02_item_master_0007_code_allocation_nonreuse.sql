-- FM-02 Item Master 0007: durable Item Code allocation and non-reuse.
-- This migration preserves 0003-0006 and adds only the approved allocation
-- ledger. Allocation is service-owned; no SQL is executed by this package.

DELIMITER //
CREATE PROCEDURE fm02_item_master_0007_revision_guard()
BEGIN
  DECLARE current_revision VARCHAR(255);
  SELECT version_num INTO current_revision FROM alembic_version LIMIT 1;
  IF current_revision IS NULL
     OR current_revision <> 'fm02_item_master_0006_legacy_mapping_reconciliation' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 0007 requires revision fm02_item_master_0006_legacy_mapping_reconciliation';
  END IF;
END//
DELIMITER ;

CALL fm02_item_master_0007_revision_guard();
DROP PROCEDURE fm02_item_master_0007_revision_guard;

CREATE TABLE item_code_allocation (
  allocation_id CHAR(36) NOT NULL,
  item_code CHAR(12) NOT NULL,
  allocation_status VARCHAR(16) NOT NULL,
  item_id CHAR(36) NULL,
  request_idempotency_key VARCHAR(128) NOT NULL,
  reserved_at DATETIME(6) NOT NULL,
  consumed_at DATETIME(6) NULL,
  abandoned_at DATETIME(6) NULL,
  reservation_reason VARCHAR(255) NOT NULL,
  created_by_assignment_id BIGINT UNSIGNED NULL,
  correlation_id VARCHAR(128) NOT NULL,
  provenance_note TEXT NULL,
  PRIMARY KEY (allocation_id),
  UNIQUE KEY uq_item_code_allocation_code (item_code),
  UNIQUE KEY uq_item_code_allocation_request (request_idempotency_key),
  UNIQUE KEY uq_item_code_allocation_item (item_id),
  KEY ix_item_code_allocation_status_time (allocation_status, reserved_at),
  CONSTRAINT fk_item_code_allocation_item
    FOREIGN KEY (item_id) REFERENCES item (item_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT ck_item_code_allocation_code_format
    CHECK (CHAR_LENGTH(item_code) = 12 AND item_code NOT REGEXP '[^A-Z0-9]'),
  CONSTRAINT ck_item_code_allocation_status
    CHECK (allocation_status IN ('RESERVED', 'CONSUMED', 'ABANDONED')),
  CONSTRAINT ck_item_code_allocation_state_evidence
    CHECK (
      (allocation_status = 'RESERVED' AND item_id IS NULL AND consumed_at IS NULL AND abandoned_at IS NULL)
      OR
      (allocation_status = 'CONSUMED' AND item_id IS NOT NULL AND consumed_at IS NOT NULL AND abandoned_at IS NULL)
      OR
      (allocation_status = 'ABANDONED' AND item_id IS NULL AND consumed_at IS NULL AND abandoned_at IS NOT NULL)
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Existing Items receive consumed ledger rows. Invalid historical codes fail
-- the approved format check rather than being silently rewritten or reused.
INSERT INTO item_code_allocation (
  allocation_id, item_code, allocation_status, item_id,
  request_idempotency_key, reserved_at, consumed_at,
  reservation_reason, correlation_id, provenance_note
)
SELECT
  UUID(), item_code, 'CONSUMED', item_id,
  CONCAT('LEGACY-ITEM-', item_id), created_at, created_at,
  'LEGACY_ITEM_REGISTRATION', CONCAT('LEGACY-ITEM-', item_id),
  'Registered by FM-02 0007; Item Code is permanently non-reusable.'
FROM item;

UPDATE alembic_version
SET version_num = 'fm02_item_master_0007_code_allocation_nonreuse'
WHERE version_num = 'fm02_item_master_0006_legacy_mapping_reconciliation';
