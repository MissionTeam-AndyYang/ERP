"""Concrete FM01 Windows-host provider shell with explicit injected effects."""
from __future__ import annotations

from pathlib import Path
from typing import Mapping, Protocol
import hashlib
import json
import os
import shutil
import subprocess
import time
import tempfile

from fm01_3342_runner import HoldError, TARGET, APPROVED_DATADIR


class CredentialHandleProvider(Protocol):
    def acquire_handle(self, target_id: str, operator_identity: str) -> object: ...
    def release_handle(self, handle: object) -> None: ...


class HostProcessProvider(Protocol):
    def status(self, *, executable: Path, config: Path, target: Mapping[str, object]) -> Mapping[str, object]: ...
    def start(self, *, executable: Path, config: Path, target: Mapping[str, object]) -> Mapping[str, object]: ...
    def graceful_stop(self, *, executable: Path, config: Path, target: Mapping[str, object], credential_handle: object) -> Mapping[str, object]: ...


class HostDatabaseProvider(Protocol):
    def migrate(self, *, client: Path, target: Mapping[str, object], credential_handle: object, revisions: list[str]) -> Mapping[str, object]: ...
    def readback(self, *, client: Path, target: Mapping[str, object], credential_handle: object) -> Mapping[str, object]: ...
    def fixture_load(self, *, client: Path, target: Mapping[str, object], credential_handle: object, fixture_id: str) -> Mapping[str, object]: ...
    def fixture_cleanup(self, *, client: Path, target: Mapping[str, object], credential_handle: object, fixture_id: str) -> Mapping[str, object]: ...


class HostFilesystemProvider(Protocol):
    def backup(self, *, dump_client: Path, target: Mapping[str, object], credential_handle: object) -> Mapping[str, object]: ...
    def restore(self, *, target: Mapping[str, object], backup_hash: str, credential_handle: object) -> Mapping[str, object]: ...
    def reset(self, *, target: Mapping[str, object], credential_handle: object) -> Mapping[str, object]: ...


class FM013342HostBinding:
    """Validate FM01 host paths without starting a process or accessing secrets."""

    def __init__(self, *, executable: Path, config: Path, client: Path, dump_client: Path, datadir: Path):
        if TARGET["port"] != 3342 or datadir.resolve() != Path(APPROVED_DATADIR).resolve():
            raise HoldError("HOLD: FM01 target binding mismatch")
        self.executable = executable
        self.config = config
        self.client = client
        self.dump_client = dump_client
        self.datadir = datadir

    def validate_paths(self) -> Mapping[str, object]:
        if any(not path.is_absolute() for path in (self.executable, self.config, self.client, self.dump_client, self.datadir)):
            raise HoldError("HOLD: host paths must be absolute")
        return {"target": TARGET, "datadir": str(self.datadir), "live_operation_invoked": False, "secret_values_exposed": False}


class HostProvidersUnavailable:
    def __getattr__(self, name: str):
        def unavailable(*args, **kwargs):
            raise HoldError(f"HOLD: FM01 host provider not configured: {name}")
        return unavailable


class WindowsCredentialHandle:
    """Opaque secret callback; value is never returned by this package."""
    def __init__(self, secret_callback):
        if not callable(secret_callback):
            raise HoldError("HOLD: credential callback is not configured")
        self._secret_callback = secret_callback
    def with_secret(self, operation):
        return operation(self._secret_callback())


class WindowsProcessProvider:
    def __init__(self, *, runner=subprocess.run, starter=subprocess.Popen, clock=time.monotonic):
        self.runner, self.starter, self.clock = runner, starter, clock

    def _assert_target(self, target):
        if target != TARGET:
            raise HoldError("HOLD: process target mismatch")

    def status(self, *, executable: Path, config: Path, target):
        self._assert_target(target)
        if not executable.is_absolute() or not config.is_absolute(): raise HoldError("HOLD: process paths must be absolute")
        result = self.runner(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", "Get-NetTCPConnection -LocalPort 3342 -State Listen"], capture_output=True, text=True, check=False)
        return {"listening": result.returncode == 0, "process_identity_verified": False, "config_identity_verified": False, "datadir_identity_verified": False, "pre_target_identity": False, "post_target_identity": False, "secret_values_exposed": False, "status": "HOLD_REQUIRES_PID_AND_CONFIG_PROOF"}

    def start(self, *, executable: Path, config: Path, target):
        self._assert_target(target)
        if target["port"] != 3342 or not executable.is_absolute() or not config.is_absolute():
            raise HoldError("HOLD: FM01 start binding mismatch")
        raise HoldError("HOLD: start requires approved manifest gate and post-start PID/executable/config/datadir/listener proof")

    def graceful_stop(self, *, executable: Path, config: Path, target, credential_handle):
        self._assert_target(target)
        if not isinstance(credential_handle, WindowsCredentialHandle):
            raise HoldError("HOLD: target credential handle required")
        return {"stopped": False, "requires_authenticated_shutdown": True, "pre_target_identity": True, "post_target_identity": False, "secret_values_exposed": False}


class MariaDBClientProvider:
    def __init__(self, *, runner=subprocess.run):
        self.runner = runner

    def _invoke(self, client: Path, target, handle: WindowsCredentialHandle, sql: str):
        if target != TARGET or not client.is_absolute() or not isinstance(handle, WindowsCredentialHandle):
            raise HoldError("HOLD: MariaDB client binding or credential handle mismatch")
        env = {"FM01_CREDENTIAL_HANDLE": handle.env_name}
        args = [str(client), "--protocol=TCP", "--host=127.0.0.1", "--port=3342", "--database=erp2_fm01_functional_np_001", "--batch", "--skip-column-names"]
        result = self.runner(args, input=sql, env=env, capture_output=True, text=True, check=False)
        return {"exit_code": result.returncode, "stdout": "[REDACTED]" if result.stdout else "", "stderr": "[REDACTED]" if result.stderr else "", "pre_target_identity": True, "post_target_identity": result.returncode == 0, "secret_values_exposed": False}

    def migrate(self, *, client, target, credential_handle, revisions):
        if revisions != ["0001", "0002", "0003", "0004"]: raise HoldError("HOLD: migration order mismatch")
        raise HoldError("HOLD: FM01 migration executor is not approved/configured")

    def readback(self, *, client, target, credential_handle):
        return self._invoke(client, target, credential_handle, "SELECT DATABASE(),@@port,@@datadir;")

    def fixture_load(self, *, client, target, credential_handle, fixture_id):
        if not fixture_id.startswith("FM01-"): raise HoldError("HOLD: fixture ownership mismatch")
        raise HoldError("HOLD: FM01 fixture executor is not approved/configured")

    def fixture_cleanup(self, *, client, target, credential_handle, fixture_id):
        raise HoldError("HOLD: FM01 fixture executor is not approved/configured")


class TargetFilesystemProvider:
    def __init__(self, *, backup_root: Path):
        self.backup_root = backup_root

    def backup(self, *, dump_client, target, credential_handle):
        if target != TARGET or not isinstance(credential_handle, WindowsCredentialHandle): raise HoldError("HOLD: backup binding mismatch")
        raise HoldError("HOLD: backup requires approved target-bound backup executor")

    def restore(self, *, target, backup_hash, credential_handle):
        if not backup_hash or target != TARGET: raise HoldError("HOLD: restore binding/hash mismatch")
        raise HoldError("HOLD: restore requires separately approved target executor")

    def reset(self, *, target, credential_handle):
        if target != TARGET: raise HoldError("HOLD: reset target mismatch")
        raise HoldError("HOLD: reset requires separate destructive authorization")


class RedactedEvidenceWriter:
    def __init__(self, path: Path): self.path = path
    def write(self, evidence):
        safe = {k: v for k, v in evidence.items() if k not in {"password", "secret", "credential", "credential_value"}}
        safe["secret_values_exposed"] = False
        payload = json.dumps(safe, sort_keys=True, separators=(",", ":"))
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        temp.write_text(payload, encoding="utf-8")
        os.replace(temp, self.path)
        return {"path": str(self.path), "sha256": hashlib.sha256(payload.encode()).hexdigest().upper(), "cleanup_complete": True, "secret_values_exposed": False}


class FM013342ConcreteProviders:
    """Concrete dispatch shell; every host effect must be injected explicitly."""

    def __init__(self, binding: FM013342HostBinding, process, database, filesystem, credentials, evidence):
        self.binding = binding
        self.process = process
        self.database = database
        self.filesystem = filesystem
        self.credentials = credentials
        self.evidence = evidence

    def _handle(self, operator_identity: str):
        return self.credentials.acquire_handle("ERP2-FM01-FUNCTIONAL-NP-001", operator_identity)

    def status(self, operator_identity: str):
        self.binding.validate_paths()
        return self.process.status(executable=self.binding.executable, config=self.binding.config, target=TARGET)

    def start(self, operator_identity: str):
        self.binding.validate_paths()
        return self.process.start(executable=self.binding.executable, config=self.binding.config, target=TARGET)

    def graceful_stop(self, operator_identity: str):
        handle = self._handle(operator_identity)
        try:
            self.binding.validate_paths()
            return self.process.graceful_stop(executable=self.binding.executable, config=self.binding.config, target=TARGET, credential_handle=handle)
        finally:
            self.credentials.release_handle(handle)

    def migrate(self, operator_identity: str):
        handle = self._handle(operator_identity)
        try:
            return self.database.migrate(client=self.binding.client, target=TARGET, credential_handle=handle, revisions=["0001", "0002", "0003", "0004"])
        finally:
            self.credentials.release_handle(handle)

    def backup(self, operator_identity: str):
        handle = self._handle(operator_identity)
        try:
            return self.filesystem.backup(dump_client=self.binding.dump_client, target=TARGET, credential_handle=handle)
        finally:
            self.credentials.release_handle(handle)

    def restore(self, operator_identity: str, backup_hash: str):
        if not backup_hash:
            raise HoldError("HOLD: verified backup hash required")
        handle = self._handle(operator_identity)
        try:
            return self.filesystem.restore(target=TARGET, backup_hash=backup_hash, credential_handle=handle)
        finally:
            self.credentials.release_handle(handle)

    def reset(self, operator_identity: str):
        handle = self._handle(operator_identity)
        try:
            return self.filesystem.reset(target=TARGET, credential_handle=handle)
        finally:
            self.credentials.release_handle(handle)

    def fixture(self, operator_identity: str, fixture_id: str):
        if not fixture_id.startswith("FM01-"):
            raise HoldError("HOLD: FM01 fixture ownership required")
        handle = self._handle(operator_identity)
        try:
            loaded = self.database.fixture_load(client=self.binding.client, target=TARGET, credential_handle=handle, fixture_id=fixture_id)
            cleaned = self.database.fixture_cleanup(client=self.binding.client, target=TARGET, credential_handle=handle, fixture_id=fixture_id)
            if loaded.get("success") is not True or cleaned.get("success") is not True:
                raise HoldError("HOLD: fixture cleanup incomplete")
            return self.evidence.write({"target": TARGET, "fixture_id": fixture_id, "loaded": loaded, "cleaned": cleaned, "secret_values_exposed": False})
        finally:
            self.credentials.release_handle(handle)
