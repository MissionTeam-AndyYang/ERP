-- FM-02 Item Master 0009: approved lifecycle vocabulary and successor relation.
-- Transition ordering and approval are service-transaction contracts.

DELIMITER //
CREATE PROCEDURE fm02_item_master_0009_revision_guard()
BEGIN
  DECLARE current_revision VARCHAR(255);
  SELECT version_num INTO current_revision FROM alembic_version LIMIT 1;
  IF current_revision IS NULL
     OR current_revision <> 'fm02_item_master_0008_name_change_audit' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'FM02 0009 requires revision fm02_item_master_0008_name_change_audit';
  END IF;
END//
DELIMITER ;

CALL fm02_item_master_0009_revision_guard();
DROP PROCEDURE fm02_item_master_0009_revision_guard;

CREATE TABLE item_successor_relationship (
  relationship_id CHAR(36) NOT NULL,
  predecessor_item_id CHAR(36) NOT NULL,
  successor_item_id CHAR(36) NOT NULL,
  reason TEXT NOT NULL,
  approved_by_role VARCHAR(128) NOT NULL,
  approved_by_business_ref VARCHAR(128) NOT NULL,
  approval_evidence_ref VARCHAR(255) NOT NULL,
  effective_at DATETIME(6) NOT NULL,
  created_by_assignment_id BIGINT UNSIGNED NULL,
  correlation_id VARCHAR(128) NOT NULL,
  PRIMARY KEY (relationship_id),
  UNIQUE KEY uq_item_successor_predecessor (predecessor_item_id),
  KEY ix_item_successor_successor (successor_item_id),
  CONSTRAINT fk_item_successor_predecessor
    FOREIGN KEY (predecessor_item_id) REFERENCES item (item_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT fk_item_successor_successor
    FOREIGN KEY (successor_item_id) REFERENCES item (item_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT ck_item_successor_distinct
    CHECK (predecessor_item_id <> successor_item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE item
  DROP CONSTRAINT ck_item_lifecycle,
  ADD CONSTRAINT ck_item_lifecycle
    CHECK (lifecycle_status IN ('DRAFT','ACTIVE','BLOCKED','INACTIVE','SUPERSEDED','RETIRED'));

ALTER TABLE item_lifecycle_event
  ADD COLUMN successor_relationship_id CHAR(36) NULL AFTER approval_id,
  DROP CONSTRAINT ck_item_lifecycle_from_status,
  DROP CONSTRAINT ck_item_lifecycle_to_status,
  ADD CONSTRAINT fk_item_lifecycle_successor
    FOREIGN KEY (successor_relationship_id) REFERENCES item_successor_relationship (relationship_id)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  ADD CONSTRAINT ck_item_lifecycle_from_status
    CHECK (from_status IS NULL OR from_status IN ('DRAFT','ACTIVE','BLOCKED','INACTIVE','SUPERSEDED','RETIRED')),
  ADD CONSTRAINT ck_item_lifecycle_to_status
    CHECK (to_status IN ('DRAFT','ACTIVE','BLOCKED','INACTIVE','SUPERSEDED','RETIRED')),
  ADD CONSTRAINT ck_item_lifecycle_successor_evidence
    CHECK (
      (to_status = 'SUPERSEDED' AND successor_relationship_id IS NOT NULL)
      OR
      (to_status <> 'SUPERSEDED' AND successor_relationship_id IS NULL)
    );

UPDATE alembic_version
SET version_num = 'fm02_item_master_0009_lifecycle_successor'
WHERE version_num = 'fm02_item_master_0008_name_change_audit';
