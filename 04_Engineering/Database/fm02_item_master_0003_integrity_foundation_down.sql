-- FM-02 Sprint-02 bounded DEV downgrade. Use only against the same DEV target
-- after the upgrade's synthetic/business rows have been removed or restored.
ALTER TABLE item DROP FOREIGN KEY fk_item_category_item;
ALTER TABLE item DROP KEY ix_item_category_id;
ALTER TABLE item DROP COLUMN item_category_id;
ALTER TABLE item DROP COLUMN updated_by_assignment_id;
ALTER TABLE item DROP COLUMN row_version;
DROP TABLE item_lifecycle_event;
DROP TABLE item_approval;
DROP TABLE item_specification;
DROP TABLE item_category;
UPDATE alembic_version
SET version_num = 'fm02_item_master_0002_business_names'
WHERE version_num = 'fm02_item_master_0003_integrity_foundation';
