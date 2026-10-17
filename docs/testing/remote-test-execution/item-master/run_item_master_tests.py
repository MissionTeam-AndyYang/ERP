#!/usr/bin/env python3
"""Fail-closed offline/manual runner for the FM02 Item Master DB package.

This runner never opens a database connection and never controls a service.
It validates package inputs, consumes supplied read-only status evidence, and
emits structured records for a human-authorized runbook execution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ALLOWED_CASES = {
    "TC01", "TC02", "TC03", "TC04", "TC05", "TC06", "TC07", "TC08", "TC09",
    "TC13", "TC14", "TC15", "TC16", "TC17", "TC18", "TC22", "TC24",
}
RESTRICTED_CASES = {"TC10", "TC11"}
MOCK_ONLY_CASES = {"TC19", "TC20", "TC21", "TC23"}
EXPECTED_TARGET = {
    "target_id": "ERP2-FM02-C2-TEST-MARIADB-001",
    "database": "erp2_fm02_c2_test_001",
    "endpoint": "127.0.0.1:3345",
    "environment": "NON_PRODUCTION",
}
FORBIDDEN_TOKENS = (
    "production", "shared", "sql", "ddl", "dml", "migrate", "restore",
    "restart", "credential", "password", "secret", "write", "cleanup",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit(result: str, case_id: str, reason: str, *, command: str = "offline-runner") -> None:
    print(json.dumps({
        "ModuleID": "ERP2-FM02-ITEM-MASTER",
        "CaseID": case_id,
        "RunID": "OFFLINE-PREP-001",
        "DesignVersion": "FM02-DB-TEST-PACKAGE-20261018",
        "SourceCommit": "d73588f5e528538aa6b12225abdcd96884ac11ad",
        "RunnerCommit": "LOCAL-WORKSPACE",
        "TargetID": EXPECTED_TARGET["target_id"],
        "Environment": EXPECTED_TARGET["environment"],
        "Executor": "NOT_ASSIGNED",
        "AuthorizationRef": "NOT_GRANTED",
        "StartTime": now(),
        "EndTime": now(),
        "FixtureHash": "SEE_FIXTURE_MANIFEST",
        "Command": command,
        "BeforeStateRef": "NOT_RUN",
        "AfterStateRef": "NOT_RUN",
        "RawEvidenceHash": "NOT_AVAILABLE",
        "CleanupStatus": "NOT_RUN",
        "RecoveryStatus": "NOT_RUN",
        "ObservedResult": result,
        "Reason": reason,
    }, sort_keys=True))


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def validate_manifest(manifest_path: Path, fixture_path: Path) -> None:
    manifest = load_json(manifest_path)
    fixture = load_json(fixture_path)
    if set(manifest.get("allowed_cases", [])) != ALLOWED_CASES:
        raise ValueError("manifest allowlist mismatch")
    if set(manifest.get("restricted_cases", [])) != RESTRICTED_CASES:
        raise ValueError("manifest restricted-case mismatch")
    if set(manifest.get("mock_only_cases", [])) != MOCK_ONLY_CASES:
        raise ValueError("manifest mock-only-case mismatch")
    if manifest.get("target") != EXPECTED_TARGET:
        raise ValueError("manifest target guard mismatch")
    if fixture.get("fixture_policy") != "deterministic synthetic fixtures only; no credentials":
        raise ValueError("fixture credential policy mismatch")
    fixture_json = json.dumps(fixture, sort_keys=True)
    if re.search(r"(?i)(password|secret|token|BEGIN [A-Z ]+ KEY)", fixture_json):
        raise ValueError("secret-like fixture content rejected")
    for entry in fixture.get("fixtures", []):
        path = fixture_path.parent / entry["path"]
        if sha256(path) != entry["sha256"]:
            raise ValueError(f"fixture hash mismatch: {entry['id']}")


def validate_status(status_path: Path) -> None:
    status = load_json(status_path)
    for key, expected in EXPECTED_TARGET.items():
        if status.get(key) != expected:
            raise ValueError(f"target status mismatch: {key}")
    if status.get("listening") is not True or not status.get("process_id"):
        raise ValueError("current target is not listening with an identified process")
    if status.get("credentials_exposed") is True:
        raise ValueError("credential exposure flag rejected")


def main() -> int:
    raw_args = " ".join(sys.argv[1:]).lower()
    forbidden = [token for token in FORBIDDEN_TOKENS if token in raw_args]
    if forbidden:
        print(json.dumps({"package_check": "BLOCKED", "reason": "forbidden operation token rejected", "tokens": sorted(set(forbidden)), "db_execution": "NOT_AUTHORIZED"}, sort_keys=True))
        return 2
    parser = argparse.ArgumentParser(description="Fail-closed FM02 Item Master test package runner")
    parser.add_argument("--mode", choices=("offline-static-validation", "read-only-target-verification", "manual-authorized-execution"), required=True)
    parser.add_argument("--case", action="append", dest="cases", default=[])
    parser.add_argument("--manifest", type=Path, default=Path(__file__).with_name("execution-manifest.json"))
    parser.add_argument("--fixture-manifest", type=Path, default=Path(__file__).with_name("fixture-manifest.json"))
    parser.add_argument("--status-file", type=Path)
    args = parser.parse_args()

    try:
        validate_manifest(args.manifest, args.fixture_manifest)
        cases = set(args.cases) if args.cases else ALLOWED_CASES
        if not cases.issubset(ALLOWED_CASES):
            unauthorized = sorted(cases - ALLOWED_CASES)
            raise ValueError(f"case allowlist rejected: {','.join(unauthorized)}")
        if args.mode == "offline-static-validation":
            print(json.dumps({"package_check": "PASS", "allowlist_count": len(cases), "db_execution": "NOT_AUTHORIZED"}, sort_keys=True))
            for case_id in sorted(cases):
                emit("NOT_RUN", case_id, "offline validation does not execute a database case")
            return 0
        if args.mode == "read-only-target-verification":
            if args.status_file is None:
                raise ValueError("status evidence file is required; no target connection is attempted")
            validate_status(args.status_file)
            print(json.dumps({"target_verification": "PASS", "database": EXPECTED_TARGET["database"], "db_execution": "NOT_AUTHORIZED"}, sort_keys=True))
            return 0
        for case_id in sorted(cases):
            emit("BLOCKED", case_id, "manual authorized runbook required; automated DB execution is disabled")
        return 2
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"package_check": "BLOCKED", "reason": str(exc), "db_execution": "NOT_AUTHORIZED"}, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
