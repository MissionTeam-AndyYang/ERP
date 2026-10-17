-- FM-02 Sprint-01 forward-only physical naming reconciliation.
-- Preconditions are enforced by apply_fm02_naming_reconciliation.py.
-- This migration renames accepted tables; it does not drop/recreate or backfill data.

RENAME TABLE
  fm02_uom_reference TO uom,
  fm02_item TO item,
  fm02_item_legacy_reference TO item_legacy_identifier;

ALTER TABLE item RENAME INDEX uq_fm02_item_code TO uq_item_code;
ALTER TABLE item RENAME INDEX ix_fm02_item_category_status TO ix_item_category_status;
ALTER TABLE item RENAME INDEX ix_fm02_item_identity_fingerprint TO ix_item_identity_fingerprint;
ALTER TABLE item RENAME INDEX fk_fm02_item_uom TO ix_item_base_uom;
ALTER TABLE item_legacy_identifier RENAME INDEX uq_fm02_legacy_reference TO uq_item_legacy_identifier;
ALTER TABLE item_legacy_identifier RENAME INDEX ix_fm02_legacy_item TO ix_item_legacy_item;

ALTER TABLE uom
  DROP CONSTRAINT ck_fm02_uom_lifecycle,
  ADD CONSTRAINT ck_uom_lifecycle CHECK (lifecycle_status IN ('ACTIVE','INACTIVE'));

ALTER TABLE item
  DROP FOREIGN KEY fk_fm02_item_uom,
  ADD CONSTRAINT fk_item_uom FOREIGN KEY (base_uom_code) REFERENCES uom (uom_code) ON UPDATE RESTRICT ON DELETE RESTRICT;

ALTER TABLE item
  DROP CONSTRAINT ck_fm02_item_category,
  ADD CONSTRAINT ck_item_category CHECK (primary_category IN ('RAW','MATERIAL','FILM','WIP','FG'));

ALTER TABLE item
  DROP CONSTRAINT ck_fm02_item_lifecycle,
  ADD CONSTRAINT ck_item_lifecycle CHECK (lifecycle_status IN ('DRAFT','ACTIVE','INACTIVE','RETIRED'));

ALTER TABLE item_legacy_identifier
  DROP FOREIGN KEY fk_fm02_legacy_item,
  ADD CONSTRAINT fk_item_legacy_identifier_item FOREIGN KEY (item_id) REFERENCES item (item_id) ON UPDATE RESTRICT ON DELETE RESTRICT;

UPDATE alembic_version
SET version_num = 'fm02_item_master_0002_business_names'
WHERE version_num = 'fm02_item_master_0001';
