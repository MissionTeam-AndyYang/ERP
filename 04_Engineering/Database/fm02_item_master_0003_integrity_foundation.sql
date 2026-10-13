-- FM-02 Sprint-02 bounded DEV migration: Item Master integrity foundation.
-- Target: ERP2-DEV-MARIADB-001 / erp2_functional_dev_001 only.
-- No legacy backfill, supplier/customer qualification, Product/SKU, BOM,
-- Inventory, Production, callbacks, or UI behavior is introduced here.

CREATE TABLE item_category (
  category_id CHAR(36) NOT NULL,
  category_code VARCHAR(32) NOT NULL,
  category_name VARCHAR(128) NOT NULL,
  parent_category_id CHAR(36) NULL,
  lifecycle_status VARCHAR(16) NOT NULL DEFAULT 'ACTIVE',
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  created_by_assignment_id BIGINT UNSIGNED NULL,
  updated_by_assignment_id BIGINT UNSIGNED NULL,
  source_reference VARCHAR(255) NOT NULL,
  provenance_note TEXT NULL,
  PRIMARY KEY (category_id),
  UNIQUE KEY uq_item_category_code (category_code),
  KEY ix_item_category_parent_status (parent_category_id, lifecycle_status),
  CONSTRAINT fk_item_category_parent FOREIGN KEY (parent_category_id)
    REFERENCES item_category (category_id) ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT ck_item_category_lifecycle CHECK (lifecycle_status IN ('DRAFT','ACTIVE','INACTIVE'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO item_category
  (category_id, category_code, category_name, lifecycle_status, created_at, updated_at,
   source_reference, provenance_note)
VALUES
  ('00000000-0000-0000-0000-000000000001', 'RAW',      'Raw material', 'ACTIVE', CURRENT_TIMESTAMP(6), CURRENT_TIMESTAMP(6), 'FM02-S02-accepted-primary-taxonomy', 'Bounded DEV taxonomy; business owner accepted five primary categories'),
  ('00000000-0000-0000-0000-000000000002', 'MATERIAL', 'Material',     'ACTIVE', CURRENT_TIMESTAMP(6), CURRENT_TIMESTAMP(6), 'FM02-S02-accepted-primary-taxonomy', 'Bounded DEV taxonomy; business owner accepted five primary categories'),
  ('00000000-0000-0000-0000-000000000003', 'FILM',     'Film',         'ACTIVE', CURRENT_TIMESTAMP(6), CURRENT_TIMESTAMP(6), 'FM02-S02-accepted-primary-taxonomy', 'Bounded DEV taxonomy; business owner accepted five primary categories'),
  ('00000000-0000-0000-0000-000000000004', 'WIP',      'Work in process','ACTIVE', CURRENT_TIMESTAMP(6), CURRENT_TIMESTAMP(6), 'FM02-S02-accepted-primary-taxonomy', 'Bounded DEV taxonomy; business owner accepted five primary categories'),
  ('00000000-0000-0000-0000-000000000005', 'FG',       'Finished good', 'ACTIVE', CURRENT_TIMESTAMP(6), CURRENT_TIMESTAMP(6), 'FM02-S02-accepted-primary-taxonomy', 'Bounded DEV taxonomy; business owner accepted five primary categories');

ALTER TABLE item
  ADD COLUMN item_category_id CHAR(36) NULL AFTER primary_category,
  ADD COLUMN updated_by_assignment_id BIGINT UNSIGNED NULL AFTER created_by_assignment_id,
  ADD COLUMN row_version BIGINT UNSIGNED NOT NULL DEFAULT 0 AFTER updated_at,
  ADD KEY ix_item_category_id (item_category_id),
  ADD CONSTRAINT fk_item_category_item FOREIGN KEY (item_category_id)
    REFERENCES item_category (category_id) ON UPDATE RESTRICT ON DELETE RESTRICT;

UPDATE item i
JOIN item_category c ON c.category_code = i.primary_category
SET i.item_category_id = c.category_id
WHERE i.item_category_id IS NULL;

CREATE TABLE item_specification (
  specification_id CHAR(36) NOT NULL,
  item_id CHAR(36) NOT NULL,
  specification_lineage_id CHAR(36) NOT NULL,
  revision_no INT UNSIGNED NOT NULL,
  specification_code VARCHAR(64) NOT NULL,
  specification_name VARCHAR(255) NOT NULL,
  specification_hash CHAR(64) NOT NULL,
  specification_summary TEXT NOT NULL,
  specification_reference VARCHAR(255) NULL,
  revision_status VARCHAR(16) NOT NULL DEFAULT 'DRAFT',
  effective_from DATETIME(6) NOT NULL,
  effective_to DATETIME(6) NULL,
  approved_by_assignment_id BIGINT UNSIGNED NULL,
  correlation_id VARCHAR(128) NULL,
  source_reference VARCHAR(255) NOT NULL,
  provenance_note TEXT NULL,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  PRIMARY KEY (specification_id),
  UNIQUE KEY uq_item_spec_lineage_revision (item_id, specification_lineage_id, revision_no),
  KEY ix_item_spec_status_effective (item_id, revision_status, effective_from),
  CONSTRAINT fk_item_spec_item FOREIGN KEY (item_id)
    REFERENCES item (item_id) ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT ck_item_spec_revision CHECK (revision_no > 0),
  CONSTRAINT ck_item_spec_status CHECK (revision_status IN ('DRAFT','ACTIVE','INACTIVE','SUPERSEDED')),
  CONSTRAINT ck_item_spec_effective_window CHECK (effective_to IS NULL OR effective_to > effective_from)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE item_approval (
  approval_id CHAR(36) NOT NULL,
  item_id CHAR(36) NOT NULL,
  approval_type VARCHAR(32) NOT NULL,
  decision VARCHAR(16) NOT NULL,
  business_actor_type VARCHAR(16) NOT NULL,
  business_actor_ref VARCHAR(128) NOT NULL,
  accountable_approval_role VARCHAR(128) NOT NULL,
  delegated_authorization_ref VARCHAR(255) NULL,
  decision_evidence_ref VARCHAR(255) NOT NULL,
  effective_at DATETIME(6) NOT NULL,
  request_id VARCHAR(128) NOT NULL,
  idempotency_key VARCHAR(128) NOT NULL,
  request_fingerprint CHAR(64) NOT NULL,
  technical_work_item_id VARCHAR(128) NULL,
  technical_executor_assignment_id BIGINT UNSIGNED NULL,
  technical_executor_ref VARCHAR(128) NULL,
  correlation_id VARCHAR(128) NOT NULL,
  created_at DATETIME(6) NOT NULL,
  PRIMARY KEY (approval_id),
  UNIQUE KEY uq_item_approval_idempotency (item_id, idempotency_key),
  KEY ix_item_approval_decision (item_id, approval_type, decision, effective_at),
  CONSTRAINT fk_item_approval_item FOREIGN KEY (item_id)
    REFERENCES item (item_id) ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT ck_item_approval_type CHECK (approval_type IN ('ACTIVATION','LIFECYCLE','SPECIFICATION','IDENTITY')),
  CONSTRAINT ck_item_approval_decision CHECK (decision IN ('APPROVED','REJECTED','REVOKED'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE item_lifecycle_event (
  event_id CHAR(36) NOT NULL,
  item_id CHAR(36) NOT NULL,
  approval_id CHAR(36) NULL,
  from_status VARCHAR(16) NULL,
  to_status VARCHAR(16) NOT NULL,
  reason TEXT NOT NULL,
  effective_at DATETIME(6) NOT NULL,
  business_actor_ref VARCHAR(128) NOT NULL,
  accountable_approval_role VARCHAR(128) NOT NULL,
  decision_evidence_ref VARCHAR(255) NOT NULL,
  technical_work_item_id VARCHAR(128) NULL,
  technical_executor_assignment_id BIGINT UNSIGNED NULL,
  technical_executor_ref VARCHAR(128) NULL,
  correlation_id VARCHAR(128) NOT NULL,
  source_reference VARCHAR(255) NOT NULL,
  provenance_note TEXT NULL,
  created_at DATETIME(6) NOT NULL,
  PRIMARY KEY (event_id),
  UNIQUE KEY uq_item_lifecycle_event_approval (approval_id),
  KEY ix_item_lifecycle_history (item_id, effective_at, to_status),
  CONSTRAINT fk_item_lifecycle_item FOREIGN KEY (item_id)
    REFERENCES item (item_id) ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT fk_item_lifecycle_approval FOREIGN KEY (approval_id)
    REFERENCES item_approval (approval_id) ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT ck_item_lifecycle_from_status CHECK (from_status IS NULL OR from_status IN ('DRAFT','ACTIVE','INACTIVE','RETIRED')),
  CONSTRAINT ck_item_lifecycle_to_status CHECK (to_status IN ('DRAFT','ACTIVE','INACTIVE','RETIRED'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

UPDATE alembic_version
SET version_num = 'fm02_item_master_0003_integrity_foundation'
WHERE version_num = 'fm02_item_master_0002_business_names';
