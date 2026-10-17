-- FM-02 C2 migration 0006: bounded legacy mapping reconciliation.
-- This migration is admitted only on the mandatory zero-row gate. It changes
-- metadata/identity mapping semantics; it never backfills or guesses targets.
-- Any non-zero protected-data case requires a separately approved conversion
-- plan and target-only backup/restore. No destructive conversion is embedded.

DELIMITER //
CREATE PROCEDURE fm02_c2_0006_revision_and_zero_gate()
BEGIN
  DECLARE current_revision VARCHAR(255);
  DECLARE legacy_rows BIGINT UNSIGNED;
  SELECT version_num INTO current_revision FROM alembic_version LIMIT 1;
  IF current_revision IS NULL
     OR current_revision <> 'fm02_item_master_0005_c2_package_customer_conversion' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 C2 0006 requires revision fm02_item_master_0005_c2_package_customer_conversion';
  END IF;
  SELECT COUNT(*) INTO legacy_rows FROM item_legacy_identifier;
  IF legacy_rows <> 0 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 C2 0006 requires zero rows in item_legacy_identifier';
  END IF;
END//
DELIMITER ;

CALL fm02_c2_0006_revision_and_zero_gate();
DROP PROCEDURE fm02_c2_0006_revision_and_zero_gate;

ALTER TABLE item_legacy_identifier
  DROP FOREIGN KEY fk_item_legacy_identifier_item,
  DROP INDEX uq_item_legacy_identifier,
  DROP INDEX ix_item_legacy_item,
  CHANGE COLUMN item_id target_item_id CHAR(36) NULL,
  ADD COLUMN source_dataset VARCHAR(255) NOT NULL,
  ADD COLUMN source_snapshot_hash CHAR(64) NOT NULL,
  ADD COLUMN source_record_id CHAR(64) NOT NULL,
  ADD COLUMN source_row_locator VARCHAR(255) NOT NULL,
  ADD COLUMN duplicate_occurrence_ordinal INT UNSIGNED NOT NULL,
  ADD COLUMN mapping_status VARCHAR(16) NOT NULL DEFAULT 'UNRESOLVED',
  ADD COLUMN resolution_reason TEXT NULL,
  ADD COLUMN correlation_id VARCHAR(128) NULL,
  ADD COLUMN created_by_assignment_id BIGINT UNSIGNED NULL,
  ADD COLUMN updated_by_assignment_id BIGINT UNSIGNED NULL,
  ADD COLUMN updated_at DATETIME(6) NOT NULL;

ALTER TABLE item_legacy_identifier
  ADD UNIQUE KEY uq_item_legacy_identifier_source
    (legacy_system, source_dataset, source_record_id, alias_role),
  ADD KEY ix_item_legacy_identifier_code (legacy_code, legacy_system),
  ADD KEY ix_item_legacy_identifier_target_status (target_item_id, mapping_status),
  ADD KEY ix_item_legacy_identifier_status_dataset (mapping_status, source_dataset),
  ADD CONSTRAINT fk_item_legacy_identifier_target_item
    FOREIGN KEY (target_item_id) REFERENCES item (item_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  ADD CONSTRAINT ck_item_legacy_identifier_mapping_status
    CHECK (mapping_status IN ('UNRESOLVED', 'MAPPED', 'REJECTED')),
  ADD CONSTRAINT ck_item_legacy_identifier_mapping_target
    CHECK (
      (mapping_status IN ('UNRESOLVED', 'REJECTED') AND target_item_id IS NULL)
      OR
      (mapping_status = 'MAPPED' AND target_item_id IS NOT NULL)
    );

UPDATE alembic_version
SET version_num = 'fm02_item_master_0006_legacy_mapping_reconciliation'
WHERE version_num = 'fm02_item_master_0005_c2_package_customer_conversion';
