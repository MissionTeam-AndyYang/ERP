"""Align the six FM-01 organization/location tables with the approved design.

This bounded revision changes only the existing six objects created by 0001.
It does not create seed data, a seventh table, or a second migration lineage.
"""

from alembic import op
import sqlalchemy as sa


revision = "fm01_org_location_0002_design_reconciliation"
down_revision = "fm01_org_location_0001"
branch_labels = None
depends_on = None


_name_columns = {
    "legal_entity": "legal_entity_name",
    "company": "company_name",
    "site": "site_name",
    "plant": "plant_name",
    "warehouse": "warehouse_name",
    "location": "location_name",
}


def _add_design_columns(table: str) -> None:
    op.add_column(table, sa.Column("active_flag", sa.Boolean(), nullable=False, server_default=sa.text("1")))
    op.add_column(table, sa.Column("effective_from", sa.DateTime(fsp=6), nullable=False))
    op.add_column(table, sa.Column("effective_to", sa.DateTime(fsp=6), nullable=True))
    op.add_column(table, sa.Column("source_reference", sa.String(255), nullable=True))
    op.add_column(table, sa.Column("provenance_note", sa.Text(), nullable=True))


def _drop_design_columns(table: str) -> None:
    for column in ("provenance_note", "source_reference", "effective_to", "effective_from", "active_flag"):
        op.drop_column(table, column)


def upgrade() -> None:
    for table, old_name in _name_columns.items():
        op.alter_column(
            table,
            old_name,
            new_column_name="display_name",
            existing_type=sa.String(255),
            existing_nullable=False,
        )
        _add_design_columns(table)

    op.add_column(
        "warehouse",
        sa.Column("plant_id", sa.BigInteger().with_variant(sa.BIGINT(unsigned=True), "mysql"), nullable=True),
    )
    op.create_index("ix_warehouse_plant_id", "warehouse", ["plant_id"], unique=False)
    op.create_foreign_key(
        "fk_warehouse_plant",
        "warehouse",
        "plant",
        ["plant_id"],
        ["plant_id"],
        onupdate="RESTRICT",
        ondelete="RESTRICT",
    )
    op.add_column("location", sa.Column("location_type", sa.String(64), nullable=True))


def downgrade() -> None:
    op.drop_column("location", "location_type")
    op.drop_constraint("fk_warehouse_plant", "warehouse", type_="foreignkey")
    op.drop_index("ix_warehouse_plant_id", table_name="warehouse")
    op.drop_column("warehouse", "plant_id")

    for table, old_name in reversed(tuple(_name_columns.items())):
        _drop_design_columns(table)
        op.alter_column(
            table,
            "display_name",
            new_column_name=old_name,
            existing_type=sa.String(255),
            existing_nullable=False,
        )
