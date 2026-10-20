"""Injected, non-live operational adapters for the FM-01 3342 contract.

The default adapter is deliberately unavailable. A future CIO-approved runtime
executor must inject every side-effecting callable and pass the manifest gate.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from typing import Callable, Mapping
from fm01_3342_runner import HoldError, plan

OPERATIONS = ("backup", "migrate", "readback", "fixture", "restore", "rollback", "reset", "safe_stop")

@dataclass(frozen=True)
class OperationResult:
    operation: str
    status: str
    live_operation_invoked: bool
    evidence: Mapping[str, object]

class LiveAdapterUnavailable(RuntimeError):
    pass


class SourceOnlyCapabilityHarness:
    """Exercise capability sequencing with only temporary, injected fakes."""

    def __init__(self, root: Path | None = None):
        self.root = Path(root or tempfile.mkdtemp(prefix="fm01-3342-source-only-"))
        self._ownership_marker = self.root / ".fm01-source-only-owned"
        if self.root.exists() and any(self.root.iterdir()):
            raise ValueError("HOLD: source-only harness root must be empty and test-owned")
        self.root.mkdir(parents=True, exist_ok=True)
        self._ownership_marker.write_text("TEST_ONLY_SOURCE_ONLY_HARNESS\n", encoding="utf-8")
        self.target = self.root / "target"
        self.backup = self.root / "backup"
        self.target.mkdir(exist_ok=True)
        self.events: list[str] = []
        self.process_running = False
        self.fixture_id: str | None = None
        self.cleanup_status = "PENDING"

    def _event(self, name: str, **details: object) -> dict[str, object]:
        self.events.append(name)
        return {"operation": name, "status": "TEST_ONLY_FAKE", "details": details,
                "live_operation_invoked": False, "secret_values_exposed": False}

    def start_readiness(self) -> dict[str, object]:
        self.process_running = True
        return self._event("start_readiness", ready=True, fake_process=True)

    def stop(self) -> dict[str, object]:
        self.process_running = False
        return self._event("stop", stopped=True, fake_process=True)

    def migrate(self) -> dict[str, object]:
        revisions = ["0001", "0002", "0003", "0004"]
        return self._event("migrate", revisions=revisions, fake_client=True)

    def backup_integrity(self) -> dict[str, object]:
        source = self.target / "identity.json"
        source.write_text(json.dumps({"target": "TEST_ONLY"}, sort_keys=True), encoding="utf-8")
        self.backup.mkdir(exist_ok=True)
        destination = self.backup / source.name
        shutil.copy2(source, destination)
        digest = hashlib.sha256(destination.read_bytes()).hexdigest().upper()
        (self.backup / "manifest.json").write_text(json.dumps({"sha256": digest}, sort_keys=True), encoding="utf-8")
        return self._event("backup", backup_hash=digest, integrity_verified=True)

    def restore_verified(self) -> dict[str, object]:
        manifest = json.loads((self.backup / "manifest.json").read_text(encoding="utf-8"))
        backup_file = self.backup / "identity.json"
        actual = hashlib.sha256(backup_file.read_bytes()).hexdigest().upper()
        if actual != manifest["sha256"]:
            raise HoldError("HOLD: fake backup integrity mismatch")
        shutil.copy2(backup_file, self.target / backup_file.name)
        return self._event("restore", backup_hash=actual, integrity_verified=True)

    def reset_isolated(self) -> dict[str, object]:
        for child in self.target.iterdir():
            if child.is_file():
                child.unlink()
        return self._event("reset", isolated_target=True)

    def fixture_setup_cleanup(self) -> dict[str, object]:
        self.fixture_id = "TEST_ONLY_FM01_FIXTURE_0001"
        fixture = self.target / "fixture.json"
        fixture.write_text(json.dumps({"fixture_id": self.fixture_id}), encoding="utf-8")
        fixture.unlink()
        return self._event("fixture", fixture_id=self.fixture_id, cleanup_owner="TEST_ONLY_FAKE_OPERATOR", cleaned=True)

    def redacted_evidence(self) -> dict[str, object]:
        evidence = {"events": list(self.events), "target": "ERP2-FM01-FUNCTIONAL-NP-001",
                    "secret_values_exposed": False, "live_operation_invoked": False}
        serialized = json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode()
        return {"operation": "evidence", "status": "TEST_ONLY_FAKE", "evidence": evidence,
                "sha256": hashlib.sha256(serialized).hexdigest().upper(),
                "live_operation_invoked": False, "secret_values_exposed": False}

    def close(self) -> None:
        if self.root.exists() and self._ownership_marker.is_file() and self._ownership_marker.read_text(encoding="utf-8") == "TEST_ONLY_SOURCE_ONLY_HARNESS\n":
            try:
                shutil.rmtree(self.root)
                self.cleanup_status = "CLEANED"
            except OSError:
                self.cleanup_status = "CLEANUP_DEFERRED_BY_HOST"

class FM013342Adapter:
    def __init__(self, manifest_path, source_dir, datadir, verifier, executor: Callable | None = None):
        self.plan = plan(manifest_path, source_dir, datadir, verifier)
        self.executor = executor

    def execute(self, operation: str) -> OperationResult:
        if operation not in OPERATIONS:
            raise HoldError(f"HOLD: unsupported operation {operation}")
        if operation not in self.plan["allowed_operations"]:
            raise HoldError(f"HOLD: operation not authorized {operation}")
        if self.executor is None:
            raise LiveAdapterUnavailable("HOLD: no CIO-approved live executor injected")
        result = self.executor(operation, self.plan["target"])
        if not isinstance(result, OperationResult) or result.live_operation_invoked is not True:
            raise HoldError("HOLD: executor returned unverifiable result")
        return result

def fake_executor(operation, target) -> OperationResult:
    return OperationResult(operation, "TEST_ONLY_FAKE", False, {"target": target, "test_only": True, "live_operation_invoked": False, "secret_values_exposed": False})
