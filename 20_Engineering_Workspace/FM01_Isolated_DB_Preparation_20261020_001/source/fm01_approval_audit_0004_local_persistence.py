"""Add the bounded FM-01-local approval and audit persistence records.

This revision follows the FM-01 0001 -> 0002 -> 0003 lineage. It creates only
FM01-local control tables and does not alter the six GET-only entity tables.
Runtime IAM, transaction orchestration, retention, and restricted readback are
explicitly adapter responsibilities.
"""

from alembic import op
import sqlalchemy as sa


revision = "fm01_approval_audit_0004_local_persistence"
down_revision = "fm01_org_location_0003_mutation_contract"
branch_labels = None
depends_on = None


def upgrade() -> None:
    u64 = sa.BigInteger().with_variant(sa.BIGINT(unsigned=True), "mysql")
    op.create_table(
        "fm01_approval_request",
        sa.Column("approval_request_id", u64, primary_key=True, autoincrement=True),
        sa.Column("request_ref", sa.String(128), nullable=False),
        sa.Column("resource_type", sa.String(64), nullable=False),
        sa.Column("entity_id", u64, nullable=False),
        sa.Column("operation", sa.String(32), nullable=False),
        sa.Column("requester_id", sa.String(128), nullable=False),
        sa.Column("requester_role", sa.String(128), nullable=True),
        sa.Column("approver_id", sa.String(128), nullable=True),
        sa.Column("approver_role", sa.String(128), nullable=True),
        sa.Column("approval_state", sa.String(32), nullable=False),
        sa.Column("requested_at", sa.DateTime(fsp=6), nullable=False),
        sa.Column("decided_at", sa.DateTime(fsp=6), nullable=True),
        sa.Column("decision_code", sa.String(64), nullable=True),
        sa.Column("decision_note", sa.Text(), nullable=True),
        sa.Column("effective_from", sa.DateTime(fsp=6), nullable=True),
        sa.Column("effective_to", sa.DateTime(fsp=6), nullable=True),
        sa.Column("row_version", u64, nullable=False, server_default=sa.text("1")),
        sa.Column("payload_json", sa.JSON(), nullable=False),
        sa.Column("idempotency_scope", sa.String(128), nullable=False),
        sa.Column("idempotency_key", sa.String(255), nullable=False),
        sa.Column("request_fingerprint", sa.String(64), nullable=False),
        sa.Column("replay_of_request_id", u64, nullable=True),
        sa.Column("conflict_code", sa.String(64), nullable=True),
        sa.Column("correlation_id", sa.String(128), nullable=False),
        sa.Column("transaction_id", sa.String(128), nullable=False),
        sa.Column("evidence_ref", sa.String(255), nullable=True),
        sa.Column("audit_event_id", u64, nullable=True),
        sa.UniqueConstraint("request_ref", name="uq_fm01_approval_request_ref"),
        sa.UniqueConstraint("idempotency_scope", "idempotency_key", name="uq_fm01_approval_idempotency"),
        sa.Index("ix_fm01_approval_target", "resource_type", "entity_id"),
        sa.Index("ix_fm01_approval_state", "approval_state", "requested_at"),
        sa.Index("ix_fm01_approval_fingerprint", "request_fingerprint"),
    )
    op.create_table(
        "fm01_audit_event",
        sa.Column("audit_event_id", u64, primary_key=True, autoincrement=True),
        sa.Column("approval_request_id", u64, nullable=False),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("actor_id", sa.String(128), nullable=False),
        sa.Column("actor_role", sa.String(128), nullable=True),
        sa.Column("transaction_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(128), nullable=False),
        sa.Column("before_json", sa.JSON(), nullable=True),
        sa.Column("after_json", sa.JSON(), nullable=True),
        sa.Column("evidence_ref", sa.String(255), nullable=True),
        sa.Column("event_at", sa.DateTime(fsp=6), nullable=False),
        sa.Column("rollback_of_event_id", u64, nullable=True),
        sa.ForeignKeyConstraint(
            ["approval_request_id"],
            ["fm01_approval_request.approval_request_id"],
            name="fk_fm01_audit_request",
            onupdate="RESTRICT",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["rollback_of_event_id"],
            ["fm01_audit_event.audit_event_id"],
            name="fk_fm01_audit_rollback_event",
            onupdate="RESTRICT",
            ondelete="RESTRICT",
        ),
        sa.Index("ix_fm01_audit_request_time", "approval_request_id", "event_at"),
        sa.Index("ix_fm01_audit_transaction", "transaction_id"),
        sa.Index("ix_fm01_audit_correlation", "correlation_id"),
    )


def downgrade() -> None:
    op.drop_table("fm01_audit_event")
    op.drop_table("fm01_approval_request")
