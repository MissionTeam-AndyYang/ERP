-- FM-02 C2 migration 0005 downgrade.
-- Rows must be removed/restored by an approved target-only rollback first.
-- No destructive row deletion is performed here.
-- The materialized customer scope key is removed with its table; no separate
-- generated-column or trigger cleanup is required.

DELIMITER //
CREATE PROCEDURE fm02_c2_0005_down_guard()
BEGIN
  DECLARE current_revision VARCHAR(255);
  DECLARE package_rows BIGINT UNSIGNED;
  DECLARE customer_rows BIGINT UNSIGNED;
  DECLARE conversion_rows BIGINT UNSIGNED;
  SELECT version_num INTO current_revision FROM alembic_version LIMIT 1;
  IF current_revision IS NULL
     OR current_revision <> 'fm02_item_master_0005_c2_package_customer_conversion' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 C2 0005 down requires revision fm02_item_master_0005_c2_package_customer_conversion';
  END IF;
  SELECT COUNT(*) INTO package_rows FROM supplier_item_package;
  SELECT COUNT(*) INTO customer_rows FROM item_customer_qualification;
  SELECT COUNT(*) INTO conversion_rows FROM uom_conversion;
  IF package_rows <> 0 OR customer_rows <> 0 OR conversion_rows <> 0 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 C2 0005 down requires empty package/customer/conversion tables';
  END IF;
END//
DELIMITER ;

CALL fm02_c2_0005_down_guard();
DROP PROCEDURE fm02_c2_0005_down_guard;

DROP TABLE uom_conversion;
DROP TABLE item_customer_qualification;
DROP TABLE supplier_item_package;

UPDATE alembic_version
SET version_num = 'fm02_item_master_0004_c2_reference_contract'
WHERE version_num = 'fm02_item_master_0005_c2_package_customer_conversion';
