-- FM-02 Sprint-01 bounded DEV migration.
-- Target: ERP2-DEV-MARIADB-001 / erp2_functional_dev_001 only.
-- No Product/SKU tables; no legacy data migration; no operational SoT claim.

CREATE TABLE IF NOT EXISTS fm02_uom_reference (
  uom_code CHAR(3) NOT NULL,
  uom_name VARCHAR(64) NOT NULL,
  lifecycle_status VARCHAR(16) NOT NULL DEFAULT 'ACTIVE',
  provenance_note VARCHAR(255) NOT NULL,
  PRIMARY KEY (uom_code),
  CONSTRAINT ck_fm02_uom_lifecycle CHECK (lifecycle_status IN ('ACTIVE','INACTIVE'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS fm02_item (
  item_id CHAR(36) NOT NULL,
  item_code CHAR(12) NOT NULL,
  primary_category VARCHAR(16) NOT NULL,
  display_name VARCHAR(255) NOT NULL,
  description TEXT NULL,
  ownership_context VARCHAR(128) NOT NULL,
  base_uom_code CHAR(3) NOT NULL,
  lifecycle_status VARCHAR(16) NOT NULL DEFAULT 'DRAFT',
  specification_summary TEXT NULL,
  specification_reference VARCHAR(255) NULL,
  identity_fingerprint CHAR(64) NOT NULL,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  created_by_assignment_id BIGINT UNSIGNED NULL,
  correlation_id VARCHAR(128) NULL,
  source_reference VARCHAR(255) NULL,
  provenance_note TEXT NULL,
  PRIMARY KEY (item_id),
  UNIQUE KEY uq_fm02_item_code (item_code),
  KEY ix_fm02_item_category_status (primary_category, lifecycle_status),
  KEY ix_fm02_item_identity_fingerprint (identity_fingerprint),
  CONSTRAINT fk_fm02_item_uom FOREIGN KEY (base_uom_code) REFERENCES fm02_uom_reference (uom_code) ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT ck_fm02_item_category CHECK (primary_category IN ('RAW','MATERIAL','FILM','WIP','FG')),
  CONSTRAINT ck_fm02_item_lifecycle CHECK (lifecycle_status IN ('DRAFT','ACTIVE','INACTIVE','RETIRED'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS fm02_item_legacy_reference (
  legacy_reference_id CHAR(36) NOT NULL,
  item_id CHAR(36) NOT NULL,
  legacy_system VARCHAR(128) NOT NULL,
  legacy_entity VARCHAR(128) NOT NULL,
  legacy_code VARCHAR(191) NOT NULL,
  alias_role VARCHAR(32) NOT NULL DEFAULT 'LEGACY_REFERENCE',
  provenance_ref VARCHAR(255) NOT NULL,
  created_at DATETIME(6) NOT NULL,
  PRIMARY KEY (legacy_reference_id),
  UNIQUE KEY uq_fm02_legacy_reference (legacy_system, legacy_entity, legacy_code, alias_role),
  KEY ix_fm02_legacy_item (item_id),
  CONSTRAINT fk_fm02_legacy_item FOREIGN KEY (item_id) REFERENCES fm02_item (item_id) ON UPDATE RESTRICT ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO fm02_uom_reference (uom_code, uom_name, lifecycle_status, provenance_note) VALUES
  ('KG', 'Kilogram', 'ACTIVE', 'BR-07 bounded synthetic DEV vocabulary'),
  ('G', 'Gram', 'ACTIVE', 'BR-07 bounded synthetic DEV vocabulary'),
  ('EA', 'Each', 'ACTIVE', 'BR-07 bounded synthetic DEV vocabulary'),
  ('L', 'Litre', 'ACTIVE', 'BR-07 bounded synthetic DEV vocabulary'),
  ('ML', 'Millilitre', 'ACTIVE', 'BR-07 bounded synthetic DEV vocabulary');

UPDATE alembic_version
SET version_num = 'fm02_item_master_0001'
WHERE version_num = 'fm01_org_location_0002_design_reconciliation';
