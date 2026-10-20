"""Fail-closed FM-01 3342 operation planner; never invokes live operations."""
from __future__ import annotations
import hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TARGET = {"target_id": "ERP2-FM01-FUNCTIONAL-NP-001", "database": "erp2_fm01_functional_np_001", "host": "127.0.0.1", "port": 3342}
APPROVED_DATADIR = r"C:\Users\andyy\Desktop\Codex-workspace\projects\ERP 2.0 Phase1\20_Engineering_Workspace\FM01_Functional_NP_Target_Binding_20261007_001\data"
FORBIDDEN_PORTS = {3306, 3341, 3344, 3345}
SOURCE_HASHES = {
    "fm01_org_location_0001.py": "80CF5745CE9D8538B22EF1597CAD5CC84EB57AFD9371C30CA9F127547018AF0D",
    "fm01_org_location_0002_design_reconciliation.py": "B74A208D8EE1E55EEBCACE8F49011386F0FB1D18072F56CEDF879A73C45E342F",
    "fm01_org_location_0003_mutation_contract.py": "9AD18755FB919EA5E6DD621A3DC6614891A11D6CFBD92C83190E033C183BFED0",
    "fm01_approval_audit_0004_local_persistence.py": "C3898F5500C554909E86D01EA370748131AC12A9433C36B141B619627C6DE94E",
}
OPS = {"backup", "migrate", "readback", "fixture", "restore", "rollback", "reset", "safe_stop"}

class HoldError(ValueError): pass
def fail(message: str) -> None: raise HoldError(f"HOLD: {message}")

def validate_manifest(manifest: dict[str, Any], expected_datadir: str, verifier) -> dict[str, Any]:
    if not isinstance(manifest, dict): fail("authorization manifest must be an object")
    if not callable(verifier): fail("authorization verifier is not configured")
    for key in ("authorization_id", "target", "window", "source_hashes", "allowed_operations", "operator", "reviewer", "signature"):
        if key not in manifest or not manifest[key]: fail(f"missing authorization field: {key}")
    target = manifest["target"]
    if not isinstance(target, dict): fail("target shape malformed")
    for key, value in TARGET.items():
        if target.get(key) != value: fail(f"target mismatch: {key}")
    if target.get("port") in FORBIDDEN_PORTS: fail("forbidden port")
    if not isinstance(target.get("datadir"), str) or target["datadir"] != APPROVED_DATADIR or expected_datadir != APPROVED_DATADIR: fail("datadir mismatch")
    window = manifest["window"]
    if not isinstance(window, dict): fail("authorization window shape malformed")
    try:
        not_before_text, expires_at_text = window["not_before"], window["expires_at"]
        if not isinstance(not_before_text, str) or not isinstance(expires_at_text, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", not_before_text) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", expires_at_text): fail("authorization window must use canonical UTC Z timestamps")
        not_before = datetime.fromisoformat(not_before_text.replace("Z", "+00:00"))
        expires_at = datetime.fromisoformat(expires_at_text.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
    except (KeyError, TypeError, ValueError, HoldError):
        fail("authorization window malformed")
    if not_before.tzinfo is None or expires_at.tzinfo is None or not_before >= expires_at or now < not_before or now >= expires_at:
        fail("authorization window is inactive")
    if not isinstance(manifest["source_hashes"], dict) or manifest["source_hashes"] != SOURCE_HASHES: fail("source hash set mismatch")
    if not isinstance(manifest["allowed_operations"], list) or not manifest["allowed_operations"] or any(not isinstance(op, str) or op not in OPS for op in manifest["allowed_operations"]): fail("unsupported operation")
    if not isinstance(manifest["operator"], dict) or not isinstance(manifest["operator"].get("identity"), str) or not isinstance(manifest["operator"].get("credential_owner_role"), str) or not manifest["operator"]["identity"] or not manifest["operator"]["credential_owner_role"]: fail("operator/custody role malformed")
    signature = manifest["signature"]
    if not isinstance(signature, dict) or not all(isinstance(signature.get(key), str) and signature[key] for key in ("algorithm", "key_id", "value")):
        fail("authorization signature malformed")
    if not verifier(manifest): fail("authorization verification unavailable or failed")
    return {"authorization_id": manifest["authorization_id"], "operations": manifest["allowed_operations"], "target": TARGET}

def source_inventory(source_dir: Path) -> dict[str, str]:
    actual = {}
    for name, expected in SOURCE_HASHES.items():
        path = source_dir / name
        if not path.is_file(): fail(f"source missing: {name}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        if digest != expected: fail(f"source hash mismatch: {name}")
        actual[name] = digest
    return actual

def plan(manifest_path: Path, source_dir: Path, expected_datadir: str, verifier) -> dict[str, Any]:
    binding = validate_manifest(json.loads(manifest_path.read_text(encoding="utf-8")), expected_datadir, verifier)
    return {"status": "AUTHORIZED_PLAN_ONLY", "target": binding["target"], "authorization_id": binding["authorization_id"], "allowed_operations": binding["operations"], "source_hashes": source_inventory(source_dir), "live_operation_invoked": False, "db_client_invoked": False, "service_invoked": False, "secret_accessed": False, "evidence_contract": "fm01-3342-evidence-v1"}

def main(argv: list[str]) -> int:
    if len(argv) != 7 or argv[1] != "--manifest" or argv[3] != "--source-dir" or argv[5] != "--datadir": print("HOLD: usage requires --manifest <manifest> --source-dir <source-dir> --datadir <approved-datadir>"); return 2
    try:
        def default_verifier(_: dict[str, Any]) -> bool: return False
        result = plan(Path(argv[2]), Path(argv[4]), argv[6], default_verifier)
    except (OSError, json.JSONDecodeError, HoldError) as exc: print(str(exc)); return 10
    print(json.dumps(result, sort_keys=True)); return 0

if __name__ == "__main__": raise SystemExit(main(sys.argv))
