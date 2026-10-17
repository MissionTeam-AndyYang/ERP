-- FM-02 C2 migration 0006 downgrade.
-- The zero-row gate is mandatory in both directions. Existing rows are never
-- deleted or guessed by this source migration.

DELIMITER //
CREATE PROCEDURE fm02_c2_0006_down_guard()
BEGIN
  DECLARE current_revision VARCHAR(255);
  DECLARE legacy_rows BIGINT UNSIGNED;
  SELECT version_num INTO current_revision FROM alembic_version LIMIT 1;
  IF current_revision IS NULL
     OR current_revision <> 'fm02_item_master_0006_legacy_mapping_reconciliation' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 C2 0006 down requires revision fm02_item_master_0006_legacy_mapping_reconciliation';
  END IF;
  SELECT COUNT(*) INTO legacy_rows FROM item_legacy_identifier;
  IF legacy_rows <> 0 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 C2 0006 down requires zero rows in item_legacy_identifier';
  END IF;
END//
DELIMITER ;

CALL fm02_c2_0006_down_guard();
DROP PROCEDURE fm02_c2_0006_down_guard;

ALTER TABLE item_legacy_identifier
  DROP FOREIGN KEY fk_item_legacy_identifier_target_item,
  DROP INDEX uq_item_legacy_identifier_source,
  DROP INDEX ix_item_legacy_identifier_code,
  DROP INDEX ix_item_legacy_identifier_target_status,
  DROP INDEX ix_item_legacy_identifier_status_dataset,
  DROP CONSTRAINT ck_item_legacy_identifier_mapping_target,
  DROP CONSTRAINT ck_item_legacy_identifier_mapping_status,
  DROP COLUMN source_dataset,
  DROP COLUMN source_snapshot_hash,
  DROP COLUMN source_record_id,
  DROP COLUMN source_row_locator,
  DROP COLUMN duplicate_occurrence_ordinal,
  DROP COLUMN mapping_status,
  DROP COLUMN resolution_reason,
  DROP COLUMN correlation_id,
  DROP COLUMN created_by_assignment_id,
  DROP COLUMN updated_by_assignment_id,
  DROP COLUMN updated_at,
  CHANGE COLUMN target_item_id item_id CHAR(36) NOT NULL,
  ADD UNIQUE KEY uq_item_legacy_identifier
    (legacy_system, legacy_entity, legacy_code, alias_role),
  ADD KEY ix_item_legacy_item (item_id),
  ADD CONSTRAINT fk_item_legacy_identifier_item
    FOREIGN KEY (item_id) REFERENCES item (item_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT;

UPDATE alembic_version
SET version_num = 'fm02_item_master_0005_c2_package_customer_conversion'
WHERE version_num = 'fm02_item_master_0006_legacy_mapping_reconciliation';
