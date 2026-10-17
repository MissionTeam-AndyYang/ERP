-- FM-02 Item Master 0009 down migration.
-- Expanded lifecycle and successor evidence are retained; rollback is gated.

DELIMITER //
CREATE PROCEDURE fm02_item_master_0009_down_guard()
BEGIN
  DECLARE successor_rows BIGINT UNSIGNED;
  DECLARE expanded_status_rows BIGINT UNSIGNED;
  SELECT COUNT(*) INTO successor_rows FROM item_successor_relationship;
  SELECT COUNT(*) INTO expanded_status_rows
  FROM item
  WHERE lifecycle_status IN ('BLOCKED', 'SUPERSEDED');
  IF successor_rows <> 0 OR expanded_status_rows <> 0 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 0009 down requires no successor rows or expanded Item lifecycle states';
  END IF;
END//
DELIMITER ;

CALL fm02_item_master_0009_down_guard();
DROP PROCEDURE fm02_item_master_0009_down_guard;

ALTER TABLE item_lifecycle_event
  DROP CONSTRAINT ck_item_lifecycle_successor_evidence,
  DROP FOREIGN KEY fk_item_lifecycle_successor,
  DROP CONSTRAINT ck_item_lifecycle_from_status,
  DROP CONSTRAINT ck_item_lifecycle_to_status,
  DROP COLUMN successor_relationship_id,
  ADD CONSTRAINT ck_item_lifecycle_from_status
    CHECK (from_status IS NULL OR from_status IN ('DRAFT','ACTIVE','INACTIVE','RETIRED')),
  ADD CONSTRAINT ck_item_lifecycle_to_status
    CHECK (to_status IN ('DRAFT','ACTIVE','INACTIVE','RETIRED'));

ALTER TABLE item
  DROP CONSTRAINT ck_item_lifecycle,
  ADD CONSTRAINT ck_item_lifecycle
    CHECK (lifecycle_status IN ('DRAFT','ACTIVE','INACTIVE','RETIRED'));

DROP TABLE item_successor_relationship;

UPDATE alembic_version
SET version_num = 'fm02_item_master_0008_name_change_audit'
WHERE version_num = 'fm02_item_master_0009_lifecycle_successor';
