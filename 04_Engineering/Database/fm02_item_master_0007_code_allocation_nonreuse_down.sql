-- FM-02 Item Master 0007 down migration.
-- Allocation history is custody data and is never deleted by rollback.

DELIMITER //
CREATE PROCEDURE fm02_item_master_0007_down_guard()
BEGIN
  DECLARE allocation_rows BIGINT UNSIGNED;
  SELECT COUNT(*) INTO allocation_rows FROM item_code_allocation;
  IF allocation_rows <> 0 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 0007 down requires an empty allocation ledger; no destructive row deletion is allowed';
  END IF;
END//
DELIMITER ;

CALL fm02_item_master_0007_down_guard();
DROP PROCEDURE fm02_item_master_0007_down_guard;

DROP TABLE item_code_allocation;

UPDATE alembic_version
SET version_num = 'fm02_item_master_0006_legacy_mapping_reconciliation'
WHERE version_num = 'fm02_item_master_0007_code_allocation_nonreuse';
