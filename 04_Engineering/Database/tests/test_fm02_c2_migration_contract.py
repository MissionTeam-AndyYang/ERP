from pathlib import Path
import re


DATABASE_DIR = Path(__file__).resolve().parents[1]


def read(name: str) -> str:
    return (DATABASE_DIR / name).read_text(encoding="utf-8")


def test_migration_lineage_has_explicit_revision_guards_and_no_drift_masking():
    migrations = {
        "0004": read("fm02_item_master_0004_c2_reference_contract.sql"),
        "0005": read("fm02_item_master_0005_c2_package_customer_conversion.sql"),
        "0006": read("fm02_item_master_0006_legacy_mapping_reconciliation.sql"),
    }
    expected = {
        "0004": ("fm02_item_master_0003_integrity_foundation", "fm02_item_master_0004_c2_reference_contract"),
        "0005": ("fm02_item_master_0004_c2_reference_contract", "fm02_item_master_0005_c2_package_customer_conversion"),
        "0006": ("fm02_item_master_0005_c2_package_customer_conversion", "fm02_item_master_0006_legacy_mapping_reconciliation"),
    }
    for key, sql in migrations.items():
        before, after = expected[key]
        assert before in sql
        assert f"SET version_num = '{after}'" in sql
        assert "CREATE PROCEDURE" in sql
        assert "SIGNAL SQLSTATE '45000'" in sql
        assert "CREATE TABLE IF NOT EXISTS" not in sql
        assert "ALTER TABLE IF NOT EXISTS" not in sql


def test_0004_contains_reference_tables_and_item_scoped_contract():
    sql = read("fm02_item_master_0004_c2_reference_contract.sql")
    assert "CREATE TABLE item_supplier_qualification" in sql
    assert "CREATE TABLE item_uom" in sql
    assert "FOREIGN KEY (specification_id, item_id)" in sql
    assert "FOREIGN KEY (uom_code) REFERENCES uom" in sql
    assert "uom_role IN ('BASE', 'PURCHASING', 'PRODUCTION', 'BOM', 'SALES', 'STOCK', 'PACKAGE')" in sql
    assert "BASE row must" in sql


def test_0005_contains_option_a_numeric_domain_and_item_only_conversion():
    sql = read("fm02_item_master_0005_c2_package_customer_conversion.sql")
    assert len(re.findall(r"^\s+(?:conversion_factor|tolerance_value) DECIMAL\(38,18\)", sql, re.MULTILINE)) == 2
    assert "rounding_scale SMALLINT UNSIGNED" in sql
    assert "rounding_scale <= 18" in sql
    assert re.search(r"item_id CHAR\(36\) NOT NULL", sql)
    assert "CREATE TABLE uom_conversion" in sql
    assert "FOREIGN KEY (from_item_uom_id, item_id)" in sql
    assert "FOREIGN KEY (to_item_uom_id, item_id)" in sql
    assert "global conversion is deferred" in sql
    assert "Actual transaction quantities" in sql


def test_0005_contains_non_null_customer_scope_key_and_correction_contract():
    sql = read("fm02_item_master_0005_c2_package_customer_conversion.sql")
    assert "supplier_qualification_scope_key CHAR(36) NOT NULL" in sql
    assert "GENERATED ALWAYS AS" not in sql
    assert "ck_item_customer_qualification_scope_key" in sql
    assert "supplier_qualification_scope_key = '00000000-0000-0000-0000-000000000000'" in sql
    assert "supplier_qualification_scope_key = supplier_qualification_id" in sql
    assert "uq_item_customer_qualification_identity" in sql
    assert "ck_item_customer_qualification_sentinel" in sql
    assert "SELECT the parent item row FOR UPDATE" in sql
    assert "existing.effective_from < new.effective_to" in sql
    assert "identical retry" in sql
    assert "different fingerprint" in sql
    assert "Concurrent writers are serialized" in sql


def test_0006_is_zero_row_gated_and_reconciles_source_record_identity():
    sql = read("fm02_item_master_0006_legacy_mapping_reconciliation.sql")
    for column in (
        "target_item_id CHAR(36) NULL",
        "source_dataset VARCHAR(255) NOT NULL",
        "source_snapshot_hash CHAR(64) NOT NULL",
        "source_record_id CHAR(64) NOT NULL",
        "source_row_locator VARCHAR(255) NOT NULL",
        "duplicate_occurrence_ordinal INT UNSIGNED NOT NULL",
        "mapping_status VARCHAR(16) NOT NULL DEFAULT 'UNRESOLVED'",
    ):
        assert column in sql
    assert "SELECT COUNT(*) INTO legacy_rows FROM item_legacy_identifier" in sql
    assert "requires zero rows in item_legacy_identifier" in sql
    assert "uq_item_legacy_identifier_source" in sql
    assert "mapping_status IN ('UNRESOLVED', 'MAPPED', 'REJECTED')" in sql
    assert "target_item_id IS NULL" in sql
    assert "target_item_id IS NOT NULL" in sql


def test_down_migrations_reverse_order_and_preserve_data():
    down_names = [
        "fm02_item_master_0004_c2_reference_contract_down.sql",
        "fm02_item_master_0005_c2_package_customer_conversion_down.sql",
        "fm02_item_master_0006_legacy_mapping_reconciliation_down.sql",
    ]
    for name in down_names:
        sql = read(name)
        assert "DROP PROCEDURE" in sql
        assert "SIGNAL SQLSTATE '45000'" in sql
        assert "No destructive row deletion" in sql or "never" in sql
        assert "DELETE FROM" not in sql
