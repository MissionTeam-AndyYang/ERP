"""Injected, non-live operational adapters for the FM-01 3342 contract.

The default adapter is deliberately unavailable. A future CIO-approved runtime
executor must inject every side-effecting callable and pass the manifest gate.
"""
from __future__ import annotations
from dataclasses import dataclass
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
