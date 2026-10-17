-- FM-02 Item Master 0008 down migration.
-- Name correction history is never deleted by rollback.

DELIMITER //
CREATE PROCEDURE fm02_item_master_0008_down_guard()
BEGIN
  DECLARE audit_rows BIGINT UNSIGNED;
  SELECT COUNT(*) INTO audit_rows FROM item_name_change_audit;
  IF audit_rows <> 0 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 0008 down requires an empty name audit table; no destructive row deletion is allowed';
  END IF;
END//
DELIMITER ;

CALL fm02_item_master_0008_down_guard();
DROP PROCEDURE fm02_item_master_0008_down_guard;

DROP TABLE item_name_change_audit;

UPDATE alembic_version
SET version_num = 'fm02_item_master_0007_code_allocation_nonreuse'
WHERE version_num = 'fm02_item_master_0008_name_change_audit';
