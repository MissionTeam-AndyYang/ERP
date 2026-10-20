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
from fm01_3342_runner import HoldError, plan, SignatureVerifier, canonical_payload, PinnedPublicKeyVerifier, TARGET as CANONICAL_TARGET
from fm01_3342_adapters import FM013342Adapter, LiveAdapterUnavailable, OperationResult, SourceOnlyCapabilityHarness, TargetBoundOperations
from target_secret_provider_interface import NoCredentialProvider, CredentialProviderUnavailable
from fm01_host_adapter_contract import FM013342HostBinding, HostProvidersUnavailable, FM013342ConcreteProviders, WindowsProcessProvider, MariaDBClientProvider, WindowsCredentialHandle, RedactedEvidenceWriter
RUNNER = ROOT / "tools" / "fm01_3342_runner.py"
SOURCE = ROOT / "source"
DATADIR = r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\FM01_Functional_NP_Target_Binding_20261007_001\data"
TARGET = {**CANONICAL_TARGET, "datadir": DATADIR}
HASHES = {
    "fm01_org_location_0001.py": "80CF5745CE9D8538B22EF1597CAD5CC84EB57AFD9371C30CA9F127547018AF0D",
    "fm01_org_location_0002_design_reconciliation.py": "B74A208D8EE1E55EEBCACE8F49011386F0FB1D18072F56CEDF879A73C45E342F",
    "fm01_org_location_0003_mutation_contract.py": "9AD18755FB919EA5E6DD621A3DC6614891A11D6CFBD92C83190E033C183BFED0",
    "fm01_approval_audit_0004_local_persistence.py": "C3898F5500C554909E86D01EA370748131AC12A9433C36B141B619627C6DE94E",
}

def manifest(**changes):
    value = {"authorization_id": "TEST-AUTH", "target": dict(TARGET), "window": {"not_before": "2026-10-20T00:00:00Z", "expires_at": "2099-10-20T00:00:00Z"}, "source_hashes": dict(HASHES), "allowed_operations": ["readback"], "operator": {"identity": "fake-operator", "credential_owner_role": "Engineering B Runtime"}, "reviewer": "CTO V2", "signature": {"algorithm": "ECDSA-SHA256", "key_id": "TEST_ONLY_KEY", "issuer": "TEST_ONLY_ISSUER", "value": "TEST_ONLY_SIGNATURE"}}
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

def case_signature_verifier_requires_approved_shape_and_canonical_payload():
    value = manifest()
    seen = []
    verifier = SignatureVerifier(issuer="TEST_ONLY_ISSUER", key_id="TEST_ONLY_KEY", algorithm="ECDSA-SHA256", verify_callable=lambda payload, value, signature: seen.append(payload) or value == "VALID")
    value["signature"]["value"] = "VALID"
    assert verifier(value) is True
    assert seen == [canonical_payload(value)]
    value["signature"]["key_id"] = "OTHER"
    assert verifier(value) is False
    value["signature"]["key_id"] = "TEST_ONLY_KEY"
    value["signature"]["algorithm"] = "TEST_ONLY_FAKE"
    assert verifier(value) is False
    value["signature"]["algorithm"] = "ECDSA-SHA256"
    value["signature"]["revoked"] = True
    assert verifier(value) is False

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

def case_injected_target_bound_operations_dispatch_without_real_runtime():
    value = manifest(allowed_operations=["status", "start", "safe_stop", "migrate", "backup", "restore", "reset", "fixture"])
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(value, f); path = Path(f.name)
    calls = []
    class Process:
        def status(self, target): calls.append("status"); return {"ready": True, "pre_target_identity": True, "post_target_identity": True}
        def start(self, target): calls.append("start"); return {"started": True, "pre_target_identity": True, "post_target_identity": True}
        def graceful_stop(self, target): calls.append("stop"); return {"stopped": True, "pre_target_identity": True, "post_target_identity": True}
    class Database:
        def migrate(self, target, revisions): calls.append(("migrate", revisions)); return {"migrated": revisions, "pre_target_identity": True, "post_target_identity": True}
        def readback(self, target): calls.append("readback"); return {"readback": True}
        def fixture_load(self, target, fixture_id): calls.append(("load", fixture_id)); return {"loaded": True, "success": True}
        def fixture_cleanup(self, target, fixture_id): calls.append(("cleanup", fixture_id)); return {"cleaned": True, "success": True}
    class Filesystem:
        def backup(self, target): calls.append("backup"); return {"backup_hash": "TEST_HASH", "pre_target_identity": True, "post_target_identity": True}
        def restore(self, target, backup_hash): calls.append(("restore", backup_hash)); return {"restored": True, "backup_hash": backup_hash, "cleanup_complete": True, "pre_target_identity": True, "post_target_identity": True}
        def reset(self, target): calls.append("reset"); return {"reset": True, "cleanup_complete": True, "post_empty_readback": True, "pre_target_identity": True, "post_target_identity": True}
    class Evidence:
        def write(self, evidence):
            assert evidence["secret_values_exposed"] is False
            assert evidence["live_operation_invoked"] is True
            evidence["cleanup_complete"] = True
            return evidence
    try:
        adapter = FM013342Adapter(path, SOURCE, DATADIR, lambda _: True)
        operations = TargetBoundOperations(adapter, Process(), Database(), Filesystem(), Evidence())
        assert operations.status()["operation"] == "status"
        assert operations.start()["operation"] == "start"
        assert operations.graceful_stop()["operation"] == "safe_stop"
        assert operations.migrate(["0001", "0002", "0003", "0004"])["operation"] == "migrate"
        assert operations.backup()["operation"] == "backup"
        assert operations.restore("TEST_HASH")["operation"] == "restore"
        assert operations.reset()["operation"] == "reset"
        assert operations.fixture("FM01-TEST-0001")["operation"] == "fixture"
        assert "backup" in calls and "reset" in calls
    finally:
        path.unlink(missing_ok=True)

def case_target_bound_operations_reject_unsafe_requests():
    value = manifest(allowed_operations=["migrate", "fixture", "restore"])
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(value, f); path = Path(f.name)
    class Null:
        def __getattr__(self, name): return lambda *args: {}
    try:
        operations = TargetBoundOperations(FM013342Adapter(path, SOURCE, DATADIR, lambda _: True), Null(), Null(), Null(), lambda x: x)
        for action in (lambda: operations.migrate(["0001", "0003"]), lambda: operations.fixture("PROD-1"), lambda: operations.restore("")):
            try:
                action(); assert False, "unsafe request must HOLD"
            except HoldError:
                pass
    finally:
        path.unlink(missing_ok=True)

def case_target_bound_operations_rejects_incomplete_cleanup_and_fixture_authority():
    value = manifest(allowed_operations=["restore", "reset"])
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(value, f); path = Path(f.name)
    class BadFS:
        def restore(self, target, backup_hash): return {"backup_hash": backup_hash, "cleanup_complete": False, "pre_target_identity": True, "post_target_identity": True}
        def reset(self, target): return {"cleanup_complete": False, "post_empty_readback": False, "pre_target_identity": True, "post_target_identity": True}
    class NoEvidence:
        def write(self, evidence): return evidence
    try:
        operations = TargetBoundOperations(FM013342Adapter(path, SOURCE, DATADIR, lambda _: True), object(), object(), BadFS(), NoEvidence())
        for action in (lambda: operations.restore("HASH"), lambda: operations.reset()):
            try:
                action(); assert False, "incomplete cleanup must HOLD"
            except HoldError:
                pass
        try:
            operations.fixture("FM01-TEST-0001")
            assert False, "unauthorized fixture must HOLD before adapter access"
        except HoldError:
            pass
    finally:
        path.unlink(missing_ok=True)

def case_concrete_entrypoint_and_credential_provider_remain_fail_closed():
    from fm01_3342_entrypoint import main
    value = manifest()
    path = ROOT / "tests" / "_entrypoint_manifest.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    try:
        assert main(["--manifest", str(path), "--source-dir", str(SOURCE), "--datadir", DATADIR, "--operation", "backup"]) == 10
        try:
            NoCredentialProvider().acquire(TARGET["target_id"], "test-operator")
            assert False, "credential provider must HOLD"
        except CredentialProviderUnavailable:
            pass
    finally:
        path.unlink(missing_ok=True)

def case_clone_manifest_completeness_for_secret_interface():
    interface = ROOT / "tools" / "target_secret_provider_interface.py"
    ignored_name = ROOT / "tools" / "credential_provider_contract.py"
    assert interface.is_file()
    assert not ignored_name.exists()
    text = interface.read_text(encoding="utf-8").lower()
    for token in ("password=", "secret=", "private_key", "dpapi", "credential_value"):
        assert token not in text

def case_fm01_host_binding_is_exact_and_provider_defaults_hold():
    binding = FM013342HostBinding(
        executable=Path(r"C:\fm01\mariadbd.exe"), config=Path(r"C:\fm01\fm01-3342.ini"),
        client=Path(r"C:\fm01\mariadb.exe"), dump_client=Path(r"C:\fm01\mariadb-dump.exe"),
        datadir=Path(DATADIR))
    evidence = binding.validate_paths()
    assert evidence["target"]["port"] == 3342
    assert evidence["live_operation_invoked"] is False
    try:
        FM013342HostBinding(executable=Path("relative.exe"), config=Path(r"C:\fm01\fm01-3342.ini"), client=Path(r"C:\fm01\mariadb.exe"), dump_client=Path(r"C:\fm01\mariadb-dump.exe"), datadir=Path(DATADIR)).validate_paths()
        assert False, "relative host path must HOLD"
    except HoldError:
        pass

def case_concrete_provider_sequences_handles_and_redacts_evidence():
    binding = FM013342HostBinding(executable=Path(r"C:\fm01\mariadbd.exe"), config=Path(r"C:\fm01\fm01-3342.ini"), client=Path(r"C:\fm01\mariadb.exe"), dump_client=Path(r"C:\fm01\mariadb-dump.exe"), datadir=Path(DATADIR))
    calls = []
    class Credentials:
        def acquire_handle(self, target_id, operator_identity): calls.append(("acquire", target_id, operator_identity)); return WindowsCredentialHandle(lambda: "TEST_ONLY_SECRET")
        def release_handle(self, handle): calls.append("release")
    class Process:
        def status(self, **kwargs): calls.append("status"); return {"pre_target_identity": True}
        def start(self, **kwargs): calls.append("start"); return {"pre_target_identity": True}
        def graceful_stop(self, **kwargs): calls.append("stop"); return {"pre_target_identity": True}
    class Database:
        def migrate(self, **kwargs): calls.append(("migrate", kwargs["revisions"])); return {"success": True}
        def fixture_load(self, **kwargs): calls.append("load"); return {"success": True}
        def fixture_cleanup(self, **kwargs): calls.append("cleanup"); return {"success": True}
    class Filesystem:
        def backup(self, **kwargs): calls.append("backup"); return {"success": True, "secret_values_exposed": False}
        def restore(self, **kwargs): calls.append("restore"); return {"success": True}
        def reset(self, **kwargs): calls.append("reset"); return {"success": True}
    class Evidence:
        def write(self, evidence):
            assert evidence.get("secret_values_exposed") is False
            calls.append("evidence")
            return {"cleanup_complete": True, "secret_values_exposed": False}
    providers = FM013342ConcreteProviders(binding, Process(), Database(), Filesystem(), Credentials(), Evidence())
    assert providers.start("operator")["pre_target_identity"] is True
    assert providers.migrate("operator")["success"] is True
    assert providers.backup("operator")["success"] is True
    assert providers.fixture("operator", "FM01-TEST-1")["cleanup_complete"] is True
    assert calls.count("release") == 3

def case_builtin_host_providers_build_fixed_scoped_calls_without_invoking_runtime():
    calls = []
    class Result:
        returncode = 0
        stdout = ""
        stderr = ""
    def runner(*args, **kwargs):
        calls.append((args, kwargs)); return Result()
    process = WindowsProcessProvider(runner=runner, starter=runner)
    client = MariaDBClientProvider(runner=runner)
    binding = FM013342HostBinding(executable=Path(r"C:\fm01\mariadbd.exe"), config=Path(r"C:\fm01\fm01-3342.ini"), client=Path(r"C:\fm01\mariadb.exe"), dump_client=Path(r"C:\fm01\mariadb-dump.exe"), datadir=Path(DATADIR))
    assert binding.validate_paths()["target"]["port"] == 3342
    temp_parent = Path(tempfile.mkdtemp(prefix="fm01-evidence-parent-", dir=str((ROOT / "tests").resolve())))
    try:
        writer = RedactedEvidenceWriter(temp_parent / "evidence.json")
        result = writer.write({"target": TARGET, "secret": "must-drop", "secret_values_exposed": True})
        assert result["secret_values_exposed"] is False
        assert "must-drop" not in Path(result["path"]).read_text(encoding="utf-8")
    finally:
        shutil.rmtree(temp_parent, ignore_errors=True)
    status = process.status(executable=binding.executable, config=binding.config, target=CANONICAL_TARGET)
    assert status["process_identity_verified"] is False
    assert status["status"] == "HOLD_REQUIRES_PID_AND_CONFIG_PROOF"
    try:
        process.status(executable=binding.executable, config=binding.config, target={**CANONICAL_TARGET, "port": 3344})
        assert False, "wrong target must HOLD"
    except HoldError:
        pass
    try:
        client.migrate(client=binding.client, target=CANONICAL_TARGET, credential_handle=WindowsCredentialHandle(lambda: "TEST_ONLY_SECRET"), revisions=["0001", "0003"])
        assert False, "wrong migration order must HOLD"
    except HoldError:
        pass
    assert len(calls) == 1

def case_pinned_verifier_holds_without_external_key_or_verifier_command():
    value = manifest()
    verifier = PinnedPublicKeyVerifier(key_path=ROOT / "tests" / "missing-public-key.pem", issuer="TEST_ONLY_ISSUER", key_id="TEST_ONLY_KEY", algorithm="ECDSA-SHA256", verifier_command=None)
    assert verifier(value) is False

def case_powerShell_entrypoints_hold_without_external_authority():
    for name in ("backup_3342.ps1", "restore_3342.ps1", "reset_3342.ps1", "safe_stop_3342.ps1"):
        text = (ROOT / "tools" / name).read_text(encoding="utf-8").lower()
        assert "hold:" in text
        assert "fm01_approved_executor" not in text
    try:
        HostProvidersUnavailable().start()
        assert False, "missing host provider must HOLD"
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
test_signature_verifier_requires_approved_shape_and_canonical_payload = case_signature_verifier_requires_approved_shape_and_canonical_payload
test_source_only_capability_harness_covers_required_paths = case_source_only_capability_harness_covers_required_paths
test_source_only_capability_harness_rejects_tampered_backup = case_source_only_capability_harness_rejects_tampered_backup
test_source_only_harness_preserves_preexisting_sibling = case_source_only_harness_preserves_preexisting_sibling
test_dependency_inventory_rejects_duplicate_revision = case_dependency_inventory_rejects_duplicate_revision
test_injected_target_bound_operations_dispatch_without_real_runtime = case_injected_target_bound_operations_dispatch_without_real_runtime
test_target_bound_operations_reject_unsafe_requests = case_target_bound_operations_reject_unsafe_requests
test_target_bound_operations_rejects_incomplete_cleanup_and_fixture_authority = case_target_bound_operations_rejects_incomplete_cleanup_and_fixture_authority
test_concrete_entrypoint_and_credential_provider_remain_fail_closed = case_concrete_entrypoint_and_credential_provider_remain_fail_closed
test_clone_manifest_completeness_for_secret_interface = case_clone_manifest_completeness_for_secret_interface
test_fm01_host_binding_is_exact_and_provider_defaults_hold = case_fm01_host_binding_is_exact_and_provider_defaults_hold
test_concrete_provider_sequences_handles_and_redacts_evidence = case_concrete_provider_sequences_handles_and_redacts_evidence
test_powerShell_entrypoints_hold_without_external_authority = case_powerShell_entrypoints_hold_without_external_authority
test_builtin_host_providers_build_fixed_scoped_calls_without_invoking_runtime = case_builtin_host_providers_build_fixed_scoped_calls_without_invoking_runtime
test_pinned_verifier_holds_without_external_key_or_verifier_command = case_pinned_verifier_holds_without_external_key_or_verifier_command

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
