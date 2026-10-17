from pathlib import Path


DATABASE_DIR = Path(__file__).resolve().parents[1]


def read(name: str) -> str:
    return (DATABASE_DIR / name).read_text(encoding="utf-8")


def test_new_forward_lineage_is_guarded_and_preserves_prior_migrations():
    expected = {
        "0007": (
            "fm02_item_master_0006_legacy_mapping_reconciliation",
            "fm02_item_master_0007_code_allocation_nonreuse",
        ),
        "0008": (
            "fm02_item_master_0007_code_allocation_nonreuse",
            "fm02_item_master_0008_name_change_audit",
        ),
        "0009": (
            "fm02_item_master_0008_name_change_audit",
            "fm02_item_master_0009_lifecycle_successor",
        ),
    }
    for key, (before, after) in expected.items():
        sql = read(f"fm02_item_master_{key}_" + {
            "0007": "code_allocation_nonreuse",
            "0008": "name_change_audit",
            "0009": "lifecycle_successor",
        }[key] + ".sql")
        assert before in sql
        assert f"SET version_num = '{after}'" in sql
        assert "CREATE PROCEDURE" in sql
        assert "SIGNAL SQLSTATE '45000'" in sql


def test_code_allocation_is_unique_and_never_reusable():
    sql = read("fm02_item_master_0007_code_allocation_nonreuse.sql")
    assert "CREATE TABLE item_code_allocation" in sql
    assert "UNIQUE KEY uq_item_code_allocation_code (item_code)" in sql
    assert "UNIQUE KEY uq_item_code_allocation_request" in sql
    assert "allocation_status IN ('RESERVED', 'CONSUMED', 'ABANDONED')" in sql
    assert "CHAR_LENGTH(item_code) = 12" in sql
    assert "item_code NOT REGEXP '[^A-Z0-9]'" in sql
    assert "ABANDONED" in sql
    assert "permanently non-reusable" in sql
    assert "INSERT INTO item_code_allocation" in sql


def test_name_audit_is_append_only_and_has_before_after_evidence():
    sql = read("fm02_item_master_0008_name_change_audit.sql")
    assert "CREATE TABLE item_name_change_audit" in sql
    assert "before_display_name VARCHAR(255) NOT NULL" in sql
    assert "after_display_name VARCHAR(255) NOT NULL" in sql
    assert "approval_evidence_ref VARCHAR(255) NOT NULL" in sql
    assert "UNIQUE KEY uq_item_name_change_audit_idempotency" in sql
    assert "ON UPDATE RESTRICT ON DELETE RESTRICT" in sql
    assert "before_display_name <> after_display_name" in sql


def test_lifecycle_and_successor_contract_is_constrained():
    sql = read("fm02_item_master_0009_lifecycle_successor.sql")
    statuses = "'DRAFT','ACTIVE','BLOCKED','INACTIVE','SUPERSEDED','RETIRED'"
    assert statuses in sql
    assert "CREATE TABLE item_successor_relationship" in sql
    assert "UNIQUE KEY uq_item_successor_predecessor" in sql
    assert "predecessor_item_id <> successor_item_id" in sql
    assert "successor_relationship_id CHAR(36) NULL" in sql
    assert "to_status = 'SUPERSEDED' AND successor_relationship_id IS NOT NULL" in sql


def test_down_migrations_are_guarded_and_do_not_delete_rows():
    for key, name in {
        "0007": "code_allocation_nonreuse",
        "0008": "name_change_audit",
        "0009": "lifecycle_successor",
    }.items():
        sql = read(f"fm02_item_master_{key}_{name}_down.sql")
        assert "CREATE PROCEDURE" in sql
        assert "SIGNAL SQLSTATE '45000'" in sql
        assert "DELETE FROM" not in sql
        assert "requires" in sql


def test_existing_migrations_are_not_rewritten():
    expected = {
        "fm02_item_master_0003_integrity_foundation.sql": "358dc7976b307a6972c3dc845895d4b32eb15a7344db6843b8193ef81bfa3b43",
        "fm02_item_master_0004_c2_reference_contract.sql": "1e89d08f46c512bdf2f64d5bb203679c9820cb27fa29f5fe0c05e40de6232929",
        "fm02_item_master_0005_c2_package_customer_conversion.sql": "e5a636d7f8ee1d53fa57263bacacaa3a0b1102d217cae296a2181fdf33388acd",
        "fm02_item_master_0006_legacy_mapping_reconciliation.sql": "01a1d5067ceb7fb25c178ce189ded03e98e500ba5384422672aa2561b775e769",
    }
    import hashlib

    for name, digest in expected.items():
        actual = hashlib.sha256((DATABASE_DIR / name).read_bytes()).hexdigest()
        assert actual == digest
