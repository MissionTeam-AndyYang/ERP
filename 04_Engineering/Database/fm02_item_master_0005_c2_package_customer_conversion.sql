-- FM-02 C2 migration 0005: package, customer qualification, and conversion.
-- C2 is Option B: item-specific UOM conversion only. item_id is mandatory;
-- global conversion is deferred to the UOM Reference owner and is not modeled
-- by a nullable item, sentinel item, cross-item endpoint, or fallback rule.
-- Numeric storage is CIO-corrected Option A: DECIMAL(38,18). This selects
-- storage capacity only; it does not approve factors, rounding modes,
-- tolerance values, or default ACTIVE behavior.

DELIMITER //
CREATE PROCEDURE fm02_c2_0005_revision_guard()
BEGIN
  DECLARE current_revision VARCHAR(255);
  SELECT version_num INTO current_revision FROM alembic_version LIMIT 1;
  IF current_revision IS NULL
     OR current_revision <> 'fm02_item_master_0004_c2_reference_contract' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 C2 0005 requires revision fm02_item_master_0004_c2_reference_contract';
  END IF;
END//
DELIMITER ;

CALL fm02_c2_0005_revision_guard();
DROP PROCEDURE fm02_c2_0005_revision_guard;

CREATE TABLE supplier_item_package (
  package_id CHAR(36) NOT NULL,
  item_id CHAR(36) NOT NULL,
  supplier_qualification_id CHAR(36) NOT NULL,
  package_code VARCHAR(64) NOT NULL,
  package_name VARCHAR(255) NOT NULL,
  package_uom_code CHAR(3) NOT NULL,
  units_per_package DECIMAL(20,6) NOT NULL,
  package_level VARCHAR(32) NOT NULL DEFAULT 'PRIMARY',
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
  PRIMARY KEY (package_id),
  UNIQUE KEY uq_supplier_item_package_identity
    (item_id, supplier_qualification_id, package_code, effective_from),
  KEY ix_supplier_item_package_status
    (item_id, lifecycle_status, effective_from),
  KEY ix_supplier_item_package_uom_status
    (package_uom_code, lifecycle_status),
  CONSTRAINT fk_supplier_item_package_supplier_qualification
    FOREIGN KEY (supplier_qualification_id, item_id)
    REFERENCES item_supplier_qualification (qualification_id, item_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT fk_supplier_item_package_uom
    FOREIGN KEY (package_uom_code) REFERENCES uom (uom_code)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT ck_supplier_item_package_units
    CHECK (units_per_package > 0),
  CONSTRAINT ck_supplier_item_package_status
    CHECK (lifecycle_status IN ('DRAFT', 'ACTIVE', 'INACTIVE', 'SUPERSEDED')),
  CONSTRAINT ck_supplier_item_package_effective_window
    CHECK (effective_to IS NULL OR effective_to > effective_from)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE item_customer_qualification (
  customer_qualification_id CHAR(36) NOT NULL,
  item_id CHAR(36) NOT NULL,
  customer_ref VARCHAR(128) NOT NULL,
  supplier_qualification_id CHAR(36) NULL,
  specification_id CHAR(36) NULL,
  approval_scope VARCHAR(32) NOT NULL,
  supply_method VARCHAR(32) NOT NULL,
  qualification_status VARCHAR(16) NOT NULL DEFAULT 'DRAFT',
  effective_from DATETIME(6) NOT NULL,
  effective_to DATETIME(6) NULL,
  approved_by_role VARCHAR(128) NULL,
  approved_by_business_ref VARCHAR(128) NULL,
  approval_evidence_ref VARCHAR(255) NULL,
  rejection_reason TEXT NULL,
  source_reference VARCHAR(255) NOT NULL,
  provenance_note TEXT NULL,
  correlation_id VARCHAR(128) NULL,
  created_by_assignment_id BIGINT UNSIGNED NULL,
  updated_by_assignment_id BIGINT UNSIGNED NULL,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  row_version BIGINT UNSIGNED NOT NULL DEFAULT 0,
  supplier_qualification_scope_key CHAR(36)
    GENERATED ALWAYS AS
      (COALESCE(supplier_qualification_id, '00000000-0000-0000-0000-000000000000')) STORED,
  PRIMARY KEY (customer_qualification_id),
  UNIQUE KEY uq_item_customer_qualification_identity
    (customer_ref, item_id, approval_scope, supplier_qualification_scope_key, effective_from),
  KEY ix_item_customer_qualification_status
    (item_id, qualification_status, effective_from),
  KEY ix_item_customer_qualification_customer
    (customer_ref, qualification_status),
  CONSTRAINT fk_item_customer_qualification_supplier
    FOREIGN KEY (supplier_qualification_id, item_id)
    REFERENCES item_supplier_qualification (qualification_id, item_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT fk_item_customer_qualification_specification
    FOREIGN KEY (specification_id, item_id)
    REFERENCES item_specification (specification_id, item_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT ck_item_customer_qualification_scope
    CHECK (
      (approval_scope = 'ANY_GENERAL_QUALIFIED_SUPPLIER'
       AND supplier_qualification_id IS NULL)
      OR
      (approval_scope = 'SPECIFIC_SUPPLIER'
       AND supplier_qualification_id IS NOT NULL)
    ),
  CONSTRAINT ck_item_customer_qualification_sentinel
    CHECK (
      supplier_qualification_id IS NULL
      OR supplier_qualification_id <> '00000000-0000-0000-0000-000000000000'
    ),
  CONSTRAINT ck_item_customer_qualification_status
    CHECK (qualification_status IN ('DRAFT', 'ACTIVE', 'INACTIVE', 'REJECTED', 'SUPERSEDED')),
  CONSTRAINT ck_item_customer_qualification_effective_window
    CHECK (effective_to IS NULL OR effective_to > effective_from)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE uom_conversion (
  conversion_rule_id CHAR(36) NOT NULL,
  item_id CHAR(36) NOT NULL,
  from_item_uom_id CHAR(36) NOT NULL,
  to_item_uom_id CHAR(36) NOT NULL,
  conversion_type VARCHAR(16) NOT NULL,
  conversion_rule_version INT UNSIGNED NOT NULL DEFAULT 1,
  conversion_factor DECIMAL(38,18) NULL,
  rounding_mode VARCHAR(32) NULL,
  rounding_scale SMALLINT UNSIGNED NULL,
  tolerance_value DECIMAL(38,18) NULL,
  lifecycle_status VARCHAR(16) NOT NULL DEFAULT 'DRAFT',
  effective_from DATETIME(6) NOT NULL,
  effective_to DATETIME(6) NULL,
  approved_by_role VARCHAR(128) NULL,
  approved_by_business_ref VARCHAR(128) NULL,
  approval_evidence_ref VARCHAR(255) NULL,
  source_reference VARCHAR(255) NOT NULL,
  provenance_note TEXT NULL,
  correlation_id VARCHAR(128) NULL,
  created_by_assignment_id BIGINT UNSIGNED NULL,
  updated_by_assignment_id BIGINT UNSIGNED NULL,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  row_version BIGINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (conversion_rule_id),
  UNIQUE KEY uq_uom_conversion_identity
    (item_id, from_item_uom_id, to_item_uom_id, conversion_type, conversion_rule_version),
  KEY ix_uom_conversion_status (item_id, lifecycle_status, effective_from),
  KEY ix_uom_conversion_endpoints
    (from_item_uom_id, to_item_uom_id, lifecycle_status),
  CONSTRAINT fk_uom_conversion_from_item_uom
    FOREIGN KEY (from_item_uom_id, item_id)
    REFERENCES item_uom (item_uom_id, item_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT fk_uom_conversion_to_item_uom
    FOREIGN KEY (to_item_uom_id, item_id)
    REFERENCES item_uom (item_uom_id, item_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT ck_uom_conversion_distinct_endpoints
    CHECK (from_item_uom_id <> to_item_uom_id),
  CONSTRAINT ck_uom_conversion_version
    CHECK (conversion_rule_version > 0),
  CONSTRAINT ck_uom_conversion_type_parameters
    CHECK (
      (conversion_type = 'FIXED'
       AND conversion_factor IS NOT NULL AND conversion_factor > 0)
      OR
      (conversion_type = 'CATCH_WEIGHT'
       AND conversion_factor IS NULL)
    ),
  CONSTRAINT ck_uom_conversion_rounding_scale
    CHECK (rounding_scale IS NULL OR rounding_scale <= 18),
  CONSTRAINT ck_uom_conversion_status
    CHECK (lifecycle_status IN ('DRAFT', 'ACTIVE', 'INACTIVE', 'SUPERSEDED')),
  CONSTRAINT ck_uom_conversion_active_approval
    CHECK (
      lifecycle_status <> 'ACTIVE'
      OR (
        approved_by_role IS NOT NULL
        AND approved_by_business_ref IS NOT NULL
        AND approval_evidence_ref IS NOT NULL
      )
    ),
  CONSTRAINT ck_uom_conversion_effective_window
    CHECK (effective_to IS NULL OR effective_to > effective_from)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Mandatory service transaction contract for item_customer_qualification and
-- uom_conversion effectivity:
--   1. SELECT the parent item row FOR UPDATE before scope validation.
--   2. Reject an overlap when existing.effective_from < new.effective_to and
--      new.effective_from < existing.effective_to; boundary-touching windows
--      are allowed. The open-ended NULL endpoint is treated as infinity.
--   3. Compare normalized immutable payloads for an identical retry and return
--      the existing row; reject a same-scope/effective-start collision with a
--      different fingerprint. Never blindly insert a duplicate.
--   4. Concurrent writers are serialized by the parent-item lock; the unique key is the
--      final database guard and only the existing bounded retry convention may
--      retry deadlock/serialization failure.
-- Actual transaction quantities, measured weights, calculated results and
-- applied-rule references remain owned by downstream transaction modules.

UPDATE alembic_version
SET version_num = 'fm02_item_master_0005_c2_package_customer_conversion'
WHERE version_num = 'fm02_item_master_0004_c2_reference_contract';
