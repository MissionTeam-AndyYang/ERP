-- FM-02 C2 migration 0004 downgrade.
-- Allowed only after 0005 and 0006 have been downgraded and all rows in the
-- two C2 tables have been removed or restored by an approved target-only
-- rollback. No destructive row deletion is performed here.

DELIMITER //
CREATE PROCEDURE fm02_c2_0004_down_guard()
BEGIN
  DECLARE current_revision VARCHAR(255);
  DECLARE supplier_rows BIGINT UNSIGNED;
  DECLARE uom_rows BIGINT UNSIGNED;
  SELECT version_num INTO current_revision FROM alembic_version LIMIT 1;
  IF current_revision IS NULL
     OR current_revision <> 'fm02_item_master_0004_c2_reference_contract' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 C2 0004 down requires revision fm02_item_master_0004_c2_reference_contract';
  END IF;
  SELECT COUNT(*) INTO supplier_rows FROM item_supplier_qualification;
  SELECT COUNT(*) INTO uom_rows FROM item_uom;
  IF supplier_rows <> 0 OR uom_rows <> 0 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 C2 0004 down requires empty item reference tables';
  END IF;
END//
DELIMITER ;

CALL fm02_c2_0004_down_guard();
DROP PROCEDURE fm02_c2_0004_down_guard;

DROP TABLE item_uom;
DROP TABLE item_supplier_qualification;
ALTER TABLE item_specification
  DROP INDEX uq_item_specification_id_item;

UPDATE alembic_version
SET version_num = 'fm02_item_master_0003_integrity_foundation'
WHERE version_num = 'fm02_item_master_0004_c2_reference_contract';
