import json
import hashlib
import hmac
import subprocess
import sys
import tempfile
import shutil
from unittest.mock import patch
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from fm01_3342_runner import HoldError, plan
from fm01_3342_adapters import FM013342Adapter, LiveAdapterUnavailable, OperationResult, SourceOnlyCapabilityHarness
RUNNER = ROOT / "tools" / "fm01_3342_runner.py"
SOURCE = ROOT / "source"
DATADIR = r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\FM01_Functional_NP_Target_Binding_20261007_001\data"
TARGET = {"target_id": "ERP2-FM01-FUNCTIONAL-NP-001", "database": "erp2_fm01_functional_np_001", "host": "127.0.0.1", "port": 3342, "datadir": DATADIR}
HASHES = {
    "fm01_org_location_0001.py": "80CF5745CE9D8538B22EF1597CAD5CC84EB57AFD9371C30CA9F127547018AF0D",
    "fm01_org_location_0002_design_reconciliation.py": "B74A208D8EE1E55EEBCACE8F49011386F0FB1D18072F56CEDF879A73C45E342F",
    "fm01_org_location_0003_mutation_contract.py": "9AD18755FB919EA5E6DD621A3DC6614891A11D6CFBD92C83190E033C183BFED0",
    "fm01_approval_audit_0004_local_persistence.py": "C3898F5500C554909E86D01EA370748131AC12A9433C36B141B619627C6DE94E",
}

def manifest(**changes):
    value = {"authorization_id": "TEST-AUTH", "target": dict(TARGET), "window": {"not_before": "2026-10-20T00:00:00Z", "expires_at": "2099-10-20T00:00:00Z"}, "source_hashes": dict(HASHES), "allowed_operations": ["readback"], "operator": {"identity": "fake-operator", "credential_owner_role": "Engineering B Runtime"}, "reviewer": "CTO V2", "signature": {"algorithm": "TEST_ONLY_FAKE", "key_id": "TEST_ONLY_KEY", "value": "TEST_ONLY_SIGNATURE"}}
    for key, value2 in changes.items():
        if key == "target": value["target"].update(value2)
        else: value[key] = value2
    return value

def run(value):
    path = ROOT / "tests" / "_manifest.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    try: return subprocess.run([sys.executable, str(RUNNER), "--manifest", str(path), "--source-dir", str(SOURCE), "--datadir", DATADIR], capture_output=True, text=True)
    finally: path.unlink(missing_ok=True)

def case_valid_3342_plan():
    value = manifest()
    result = plan(ROOT / "tests" / "_manifest.json", SOURCE, DATADIR, lambda _: True) if False else None
    assert run(value).returncode == 10  # CLI has no configured trust anchor and must reject by default
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(value, f); path = Path(f.name)
    try:
        approved = plan(path, SOURCE, DATADIR, lambda _: True)
        assert approved["target"]["port"] == 3342
    finally:
        path.unlink(missing_ok=True)

def case_rejects_forbidden_ports_and_wrong_target():
    for port in (3344, 3345, 3306):
        result = run(manifest(target={"port": port}))
        assert result.returncode == 10 and "HOLD" in result.stdout
    result = run(manifest(target={"target_id": "PRODUCTION"}))
    assert result.returncode == 10 and "HOLD" in result.stdout

def case_rejects_wrong_datadir_and_source_hash():
    assert run(manifest(target={"datadir": r"C:\wrong\data"})).returncode == 10
    assert run(manifest(source_hashes={**HASHES, "fm01_org_location_0001.py": "BAD"})).returncode == 10

def case_rejects_missing_signature_and_unsupported_operation():
    assert run(manifest(signature=None)).returncode == 10
    assert run(manifest(signature={"algorithm": "TEST_ONLY_FAKE"})).returncode == 10
    assert run(manifest(allowed_operations=["drop-production"])).returncode == 10

def case_rejects_wrong_window_and_database():
    assert run(manifest(window={"not_before": "2099-01-01T00:00:00Z", "expires_at": "2099-01-02T00:00:00Z"})).returncode == 10
    assert run(manifest(target={"database": "production"})).returncode == 10

def case_contract_mentions_timeout_cleanup_and_redaction():
    contract = (ROOT / "operation-contract.md").read_text(encoding="utf-8")
    for token in ("timeout", "HOLD", "cleanup", "secret_values_exposed=false", "NOT RUN"):
        assert token in contract

def case_injected_adapter_requires_authorized_operation_and_executor():
    value = manifest()
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(value, f); path = Path(f.name)
    try:
        adapter = FM013342Adapter(path, SOURCE, DATADIR, lambda _: True)
        try:
            adapter.execute("readback")
            assert False, "missing executor must HOLD"
        except LiveAdapterUnavailable:
            pass
        fake = FM013342Adapter(path, SOURCE, DATADIR, lambda _: True, lambda op, target: OperationResult(op, "TEST_ONLY_FAKE", False, {"test_only": True, "live_operation_invoked": False, "secret_values_exposed": False}))
        try:
            fake.execute("readback")
            assert False, "fake executor must not be accepted as live proof"
        except HoldError:
            pass
    finally:
        path.unlink(missing_ok=True)

def case_test_only_ephemeral_signature_mechanics():
    key = b"TEST_ONLY_EPHEMERAL_KEY"
    payload = json.dumps(manifest(), sort_keys=True, separators=(",", ":")).encode()
    signature = hmac.new(key, payload, hashlib.sha256).hexdigest()
    assert hmac.compare_digest(signature, hmac.new(key, payload, hashlib.sha256).hexdigest())
    tampered = payload.replace(b"readback", b"reset")
    assert not hmac.compare_digest(signature, hmac.new(key, tampered, hashlib.sha256).hexdigest())

def case_source_only_capability_harness_covers_required_paths():
    parent_root = (ROOT / "tests").resolve()
    parent_root.mkdir(parents=True, exist_ok=True)
    assert parent_root.is_relative_to(ROOT.resolve() / "tests")
    parent = Path(tempfile.mkdtemp(prefix="fm01-harness-parent-", dir=str(parent_root)))
    root = Path(tempfile.mkdtemp(prefix="owned-", dir=parent))
    harness = SourceOnlyCapabilityHarness(root)
    try:
        assert harness.start_readiness()["details"]["ready"] is True
        assert harness.migrate()["details"]["revisions"] == ["0001", "0002", "0003", "0004"]
        backup = harness.backup_integrity()
        assert backup["details"]["integrity_verified"] is True
        assert harness.restore_verified()["details"]["integrity_verified"] is True
        assert harness.fixture_setup_cleanup()["details"]["cleaned"] is True
        assert harness.reset_isolated()["details"]["isolated_target"] is True
        assert harness.stop()["details"]["stopped"] is True
        evidence = harness.redacted_evidence()
        assert evidence["live_operation_invoked"] is False
        assert evidence["secret_values_exposed"] is False
        assert harness.process_running is False
        assert harness.events == ["start_readiness", "migrate", "backup", "restore", "fixture", "reset", "stop"]
    finally:
        harness.close()
        assert harness.cleanup_status in ("CLEANED", "CLEANUP_DEFERRED_BY_HOST")
        shutil.rmtree(parent, ignore_errors=True)

def case_source_only_capability_harness_rejects_tampered_backup():
    parent_root = (ROOT / "tests").resolve()
    parent_root.mkdir(parents=True, exist_ok=True)
    assert parent_root.is_relative_to(ROOT.resolve() / "tests")
    parent = Path(tempfile.mkdtemp(prefix="fm01-harness-parent-", dir=str(parent_root)))
    root = Path(tempfile.mkdtemp(prefix="owned-", dir=parent))
    harness = SourceOnlyCapabilityHarness(root)
    try:
        harness.backup_integrity()
        (harness.backup / "identity.json").write_text("tampered", encoding="utf-8")
        try:
            harness.restore_verified()
            assert False, "tampered backup must HOLD"
        except HoldError:
            pass
    finally:
        harness.close()
        assert harness.cleanup_status in ("CLEANED", "CLEANUP_DEFERRED_BY_HOST")
        shutil.rmtree(parent, ignore_errors=True)

def case_source_only_harness_preserves_preexisting_sibling():
    parent_root = (ROOT / "tests").resolve()
    parent_root.mkdir(parents=True, exist_ok=True)
    assert parent_root.is_relative_to(ROOT.resolve() / "tests")
    parent = Path(tempfile.mkdtemp(prefix="fm01-harness-parent-", dir=str(parent_root)))
    sibling = parent / "preexisting-sibling"
    sibling.mkdir()
    marker = sibling / "keep.txt"
    marker.write_text("must remain", encoding="utf-8")
    root = Path(tempfile.mkdtemp(prefix="owned-", dir=parent))
    harness = SourceOnlyCapabilityHarness(root)
    try:
        harness.start_readiness()
    finally:
        harness.close()
        assert marker.read_text(encoding="utf-8") == "must remain"
        assert sibling.is_dir()
        shutil.rmtree(parent, ignore_errors=True)

def case_dependency_inventory_rejects_duplicate_revision():
    source = ROOT / "tests" / "mocked-source"
    names = list(HASHES)
    texts = {
        names[0]: 'revision = "r0001"\ndown_revision = "None"\n',
        names[1]: 'revision = "r0002"\ndown_revision = "r0001"\n',
        names[2]: 'revision = "r0003"\ndown_revision = "r0002"\n',
        names[3]: 'revision = "r0003"\ndown_revision = "r0003"\n',
    }
    real_read_text = Path.read_text
    def fake_read_text(path, *args, **kwargs):
        name = Path(path).name
        if name in texts:
            return texts[name]
        return real_read_text(path, *args, **kwargs)
    from fm01_3342_runner import dependency_inventory
    with patch.object(Path, "read_text", autospec=True, side_effect=fake_read_text):
        try:
            dependency_inventory(source)
            assert False, "duplicate revision must HOLD"
        except HoldError:
            pass

test_valid_3342_plan = case_valid_3342_plan
test_rejects_forbidden_ports_and_wrong_target = case_rejects_forbidden_ports_and_wrong_target
test_rejects_wrong_datadir_and_source_hash = case_rejects_wrong_datadir_and_source_hash
test_rejects_missing_signature_and_unsupported_operation = case_rejects_missing_signature_and_unsupported_operation
test_rejects_wrong_window_and_database = case_rejects_wrong_window_and_database
test_contract_mentions_timeout_cleanup_and_redaction = case_contract_mentions_timeout_cleanup_and_redaction
test_injected_adapter_requires_authorized_operation_and_executor = case_injected_adapter_requires_authorized_operation_and_executor
test_test_only_ephemeral_signature_mechanics = case_test_only_ephemeral_signature_mechanics
test_source_only_capability_harness_covers_required_paths = case_source_only_capability_harness_covers_required_paths
test_source_only_capability_harness_rejects_tampered_backup = case_source_only_capability_harness_rejects_tampered_backup
test_source_only_harness_preserves_preexisting_sibling = case_source_only_harness_preserves_preexisting_sibling
test_dependency_inventory_rejects_duplicate_revision = case_dependency_inventory_rejects_duplicate_revision

def main():
    cases = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    passed = 0
    failures = []
    for name, case in ((name, value) for name, value in globals().items() if name.startswith("test_") and callable(value)):
        try:
            case()
            passed += 1
        except Exception as exc:
            failures.append(f"{name}: {exc}")
    print(f"STANDARD_LIBRARY_CASES={len(cases)};PASSED={passed};FAILED={len(failures)}")
    for failure in failures:
        print(failure)
    if failures:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
