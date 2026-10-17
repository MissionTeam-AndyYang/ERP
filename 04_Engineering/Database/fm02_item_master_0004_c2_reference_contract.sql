-- FM-02 C2 migration 0004: bounded reference contract.
-- Authority: CIO-GOV-ERP2-FM02-PHYSICAL-FREEZE-C2-EXECUTION-20261013-001,
-- frozen package 019 plus physical-integrity correction 020.
-- Scope: item_supplier_qualification, item_uom, and the item-scoped
-- item_specification composite reference key only. No Product/SKU, BOM,
-- Inventory, Production, customer master, supplier master, runtime, grants,
-- or global UOM conversion is introduced.
--
-- Re-application contract: the explicit revision guard must pass before any
-- DDL. IF NOT EXISTS is intentionally not used to hide drift.

DELIMITER //
CREATE PROCEDURE fm02_c2_0004_revision_guard()
BEGIN
  DECLARE current_revision VARCHAR(255);
  SELECT version_num INTO current_revision
    FROM alembic_version
    LIMIT 1;
  IF current_revision IS NULL
     OR current_revision <> 'fm02_item_master_0003_integrity_foundation' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 C2 0004 requires revision fm02_item_master_0003_integrity_foundation';
  END IF;
END//
DELIMITER ;

CALL fm02_c2_0004_revision_guard();
DROP PROCEDURE fm02_c2_0004_revision_guard;

ALTER TABLE item_specification
  ADD UNIQUE KEY uq_item_specification_id_item (specification_id, item_id);

CREATE TABLE item_supplier_qualification (
  qualification_id CHAR(36) NOT NULL,
  item_id CHAR(36) NOT NULL,
  supplier_ref VARCHAR(128) NOT NULL,
  qualification_code VARCHAR(64) NOT NULL,
  specification_id CHAR(36) NULL,
  qualification_status VARCHAR(16) NOT NULL DEFAULT 'DRAFT',
  effective_from DATETIME(6) NOT NULL,
  effective_to DATETIME(6) NULL,
  approved_by_role VARCHAR(128) NULL,
  approved_by_business_ref VARCHAR(128) NULL,
  approval_evidence_ref VARCHAR(255) NULL,
  revoked_at DATETIME(6) NULL,
  revocation_reason TEXT NULL,
  source_reference VARCHAR(255) NOT NULL,
  provenance_note TEXT NULL,
  correlation_id VARCHAR(128) NULL,
  created_by_assignment_id BIGINT UNSIGNED NULL,
  updated_by_assignment_id BIGINT UNSIGNED NULL,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  row_version BIGINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (qualification_id),
  UNIQUE KEY uq_item_supplier_qualification_id_item (qualification_id, item_id),
  UNIQUE KEY uq_item_supplier_qualification_identity
    (item_id, supplier_ref, qualification_code, effective_from),
  KEY ix_item_supplier_qualification_status
    (item_id, qualification_status, effective_from),
  KEY ix_item_supplier_qualification_supplier
    (supplier_ref, qualification_status),
  CONSTRAINT fk_item_supplier_qualification_item
    FOREIGN KEY (item_id) REFERENCES item (item_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT fk_item_supplier_qualification_specification
    FOREIGN KEY (specification_id, item_id)
    REFERENCES item_specification (specification_id, item_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT ck_item_supplier_qualification_status
    CHECK (qualification_status IN ('DRAFT', 'ACTIVE', 'INACTIVE', 'REVOKED')),
  CONSTRAINT ck_item_supplier_qualification_effective_window
    CHECK (effective_to IS NULL OR effective_to > effective_from)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE item_uom (
  item_uom_id CHAR(36) NOT NULL,
  item_id CHAR(36) NOT NULL,
  uom_code CHAR(3) NOT NULL,
  uom_role VARCHAR(32) NOT NULL,
  conversion_type VARCHAR(16) NOT NULL DEFAULT 'FIXED',
  lifecycle_status VARCHAR(16) NOT NULL DEFAULT 'DRAFT',
  effective_from DATETIME(6) NOT NULL,
  effective_to DATETIME(6) NULL,
  source_reference VARCHAR(255) NOT NULL,
  provenance_note TEXT NULL,
  correlation_id VARCHAR(128) NULL,
  created_by_assignment_id BIGINT UNSIGNED NULL,
  updated_by_assignment_id BIGINT UNSIGNED NULL,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  row_version BIGINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (item_uom_id),
  UNIQUE KEY uq_item_uom_id_item (item_uom_id, item_id),
  UNIQUE KEY uq_item_uom_identity (item_id, uom_code, uom_role, effective_from),
  KEY ix_item_uom_role_status (item_id, uom_role, lifecycle_status, effective_from),
  KEY ix_item_uom_code_status (uom_code, lifecycle_status),
  CONSTRAINT fk_item_uom_item
    FOREIGN KEY (item_id) REFERENCES item (item_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT fk_item_uom_reference
    FOREIGN KEY (uom_code) REFERENCES uom (uom_code)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT ck_item_uom_role
    CHECK (uom_role IN ('BASE', 'PURCHASING', 'PRODUCTION', 'BOM', 'SALES', 'STOCK', 'PACKAGE')),
  CONSTRAINT ck_item_uom_conversion_type
    CHECK (conversion_type IN ('FIXED', 'CATCH_WEIGHT')),
  CONSTRAINT ck_item_uom_lifecycle_status
    CHECK (lifecycle_status IN ('DRAFT', 'ACTIVE', 'INACTIVE', 'SUPERSEDED')),
  CONSTRAINT ck_item_uom_effective_window
    CHECK (effective_to IS NULL OR effective_to > effective_from)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Contract rule, enforced by the owning service transaction: a BASE row must
-- mirror item.base_uom_code. No cross-table CHECK is used because MariaDB
-- CHECK expressions cannot safely query the parent row.

UPDATE alembic_version
SET version_num = 'fm02_item_master_0004_c2_reference_contract'
WHERE version_num = 'fm02_item_master_0003_integrity_foundation';
