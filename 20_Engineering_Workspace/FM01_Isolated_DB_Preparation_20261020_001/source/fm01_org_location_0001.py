"""FM-01 bounded organization/location schema.

This revision is intentionally independent of the Track F runtime lineage.
It creates exactly the six approved FM-01 objects and no seed data.
"""

from alembic import op
import sqlalchemy as sa


revision = "fm01_org_location_0001"
down_revision = None
branch_labels = None
depends_on = None


def _audit_columns():
    return [
        sa.Column("created_at", sa.DateTime(fsp=6), nullable=False),
        sa.Column("created_by_assignment_id", sa.BigInteger().with_variant(sa.BIGINT(unsigned=True), "mysql"), nullable=True),
        sa.Column("updated_at", sa.DateTime(fsp=6), nullable=False),
        sa.Column("updated_by_assignment_id", sa.BigInteger().with_variant(sa.BIGINT(unsigned=True), "mysql"), nullable=True),
        sa.Column("correlation_id", sa.String(128), nullable=True),
    ]


def upgrade():
    u64 = sa.BigInteger().with_variant(sa.BIGINT(unsigned=True), "mysql")
    op.create_table(
        "legal_entity",
        sa.Column("legal_entity_id", u64, primary_key=True, autoincrement=True),
        sa.Column("legal_entity_ref", sa.String(128), nullable=False),
        sa.Column("legal_entity_name", sa.String(255), nullable=False),
        *_audit_columns(),
        sa.UniqueConstraint("legal_entity_ref", name="uq_legal_entity_ref"),
    )
    op.create_table(
        "company",
        sa.Column("company_id", u64, primary_key=True, autoincrement=True),
        sa.Column("legal_entity_id", u64, nullable=False),
        sa.Column("company_ref", sa.String(128), nullable=False),
        sa.Column("company_name", sa.String(255), nullable=False),
        *_audit_columns(),
        sa.UniqueConstraint("legal_entity_id", "company_ref", name="uq_company_legal_entity_ref"),
        sa.ForeignKeyConstraint(["legal_entity_id"], ["legal_entity.legal_entity_id"], name="fk_company_legal_entity", onupdate="RESTRICT", ondelete="RESTRICT"),
    )
    op.create_table(
        "site",
        sa.Column("site_id", u64, primary_key=True, autoincrement=True),
        sa.Column("company_id", u64, nullable=False),
        sa.Column("site_ref", sa.String(128), nullable=False),
        sa.Column("site_name", sa.String(255), nullable=False),
        *_audit_columns(),
        sa.UniqueConstraint("company_id", "site_ref", name="uq_site_company_ref"),
        sa.ForeignKeyConstraint(["company_id"], ["company.company_id"], name="fk_site_company", onupdate="RESTRICT", ondelete="RESTRICT"),
    )
    op.create_table(
        "plant",
        sa.Column("plant_id", u64, primary_key=True, autoincrement=True),
        sa.Column("site_id", u64, nullable=False),
        sa.Column("plant_ref", sa.String(128), nullable=False),
        sa.Column("plant_name", sa.String(255), nullable=False),
        *_audit_columns(),
        sa.UniqueConstraint("site_id", "plant_ref", name="uq_plant_site_ref"),
        sa.ForeignKeyConstraint(["site_id"], ["site.site_id"], name="fk_plant_site", onupdate="RESTRICT", ondelete="RESTRICT"),
    )
    op.create_table(
        "warehouse",
        sa.Column("warehouse_id", u64, primary_key=True, autoincrement=True),
        sa.Column("site_id", u64, nullable=False),
        sa.Column("warehouse_ref", sa.String(128), nullable=False),
        sa.Column("warehouse_name", sa.String(255), nullable=False),
        *_audit_columns(),
        sa.UniqueConstraint("site_id", "warehouse_ref", name="uq_warehouse_site_ref"),
        sa.ForeignKeyConstraint(["site_id"], ["site.site_id"], name="fk_warehouse_site", onupdate="RESTRICT", ondelete="RESTRICT"),
    )
    op.create_table(
        "location",
        sa.Column("location_id", u64, primary_key=True, autoincrement=True),
        sa.Column("warehouse_id", u64, nullable=False),
        sa.Column("parent_location_id", u64, nullable=True),
        sa.Column("location_ref", sa.String(128), nullable=False),
        sa.Column("location_name", sa.String(255), nullable=False),
        *_audit_columns(),
        sa.UniqueConstraint("warehouse_id", "location_ref", name="uq_location_warehouse_ref"),
        sa.ForeignKeyConstraint(["warehouse_id"], ["warehouse.warehouse_id"], name="fk_location_warehouse", onupdate="RESTRICT", ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["parent_location_id"], ["location.location_id"], name="fk_location_parent", onupdate="RESTRICT", ondelete="RESTRICT"),
    )


def downgrade():
    op.drop_table("location")
    op.drop_table("warehouse")
    op.drop_table("plant")
    op.drop_table("site")
    op.drop_table("company")
    op.drop_table("legal_entity")
