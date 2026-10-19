"""FM-01 bounded mutation persistence contract.

This source revision is preparation only. It extends the six existing FM-01
objects with the optimistic-concurrency token required by the approved C1/C2
contract. Pending Approval, idempotency and audit/evidence persistence remain
shared application-core contracts; this revision intentionally creates no new
FM-01 tables and does not alter the GET-only API.
"""

from alembic import op
import sqlalchemy as sa


revision = "fm01_org_location_0003_mutation_contract"
down_revision = "fm01_org_location_0002_design_reconciliation"
branch_labels = None
depends_on = None


_FM01_TABLES = (
    "legal_entity",
    "company",
    "site",
    "plant",
    "warehouse",
    "location",
)


def upgrade():
    """Add a monotonic compare-and-swap token to each approved FM-01 entity."""
    for table_name in _FM01_TABLES:
        op.add_column(
            table_name,
            sa.Column(
                "row_version",
                sa.BigInteger().with_variant(sa.BIGINT(unsigned=True), "mysql"),
                nullable=False,
                server_default=sa.text("1"),
            ),
        )


def downgrade():
    """Remove only the additive concurrency columns from an empty test target."""
    for table_name in reversed(_FM01_TABLES):
        op.drop_column(table_name, "row_version")
