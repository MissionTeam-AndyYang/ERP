"""Bounded FM-01 test-tool source.

This module provides deterministic non-DB fixture execution and a fail-closed
remote runner interface. It never discovers credentials, chooses targets, or
connects to a database. Test execution remains a separate authorized stage.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Callable, Iterable, Mapping, Protocol


class TestStatus:
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_RUN = "NOT_RUN"
    HOLD = "HOLD"


@dataclass(frozen=True)
class TestCase:
    case_id: str
    description: str
    check: Callable[[], None]


@dataclass
class TestReport:
    runner: str
    status: str = TestStatus.NOT_RUN
    cases: list[dict[str, Any]] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "runner": self.runner,
            "status": self.status,
            "cases": self.cases,
            "limitations": self.limitations,
        }


def run_non_db_cases(cases: Iterable[TestCase]) -> TestReport:
    """Run only deterministic in-memory cases and classify every result."""

    report = TestReport(runner="fm01-non-db-fixtures")
    all_passed = True
    for case in cases:
        try:
            case.check()
        except Exception as exc:  # individual case evidence must be retained
            all_passed = False
            report.cases.append({"case_id": case.case_id, "status": TestStatus.FAIL, "error": str(exc)})
        else:
            report.cases.append({"case_id": case.case_id, "status": TestStatus.PASS, "description": case.description})
    report.status = TestStatus.PASS if all_passed else TestStatus.FAIL
    return report


class CredentialProvider(Protocol):
    """Explicit external credential binding; no implementation is provided."""

    def get(self, target_name: str) -> Mapping[str, str] | None: ...


class RemoteDbTestRunner:
    """Fail-closed remote DB test interface; never runs without explicit binding."""

    def __init__(self, target_name: str | None, credential_provider: CredentialProvider | None):
        self._target_name = target_name
        self._credential_provider = credential_provider

    def plan(self) -> TestReport:
        report = TestReport(runner="fm01-remote-db")
        report.limitations.append("DB execution requires separately authorized target and credential binding")
        if not self._target_name or self._credential_provider is None:
            report.status = TestStatus.NOT_RUN
            return report
        report.status = TestStatus.HOLD
        report.limitations.append("runner is not authorized to resolve credentials or execute DB tests in this stage")
        return report

    def execute(self) -> TestReport:
        report = self.plan()
        report.status = TestStatus.NOT_RUN
        report.limitations.append("execution intentionally disabled until Runtime/Remote DB authorization")
        return report


def build_evidence(report: TestReport, *, commit: str, tree: str) -> dict[str, Any]:
    """Create deterministic report metadata without claiming test execution."""

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "commit": commit,
        "tree": tree,
        "report": report.to_dict(),
        "test_engineering": "DEFERRED / NOT RELEASED",
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    payload["evidence_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def write_report(path: str, evidence: Mapping[str, Any]) -> None:
    """Write caller-selected evidence only; no implicit filesystem discovery."""

    with open(path, "w", encoding="utf-8", newline="\n") as output:
        json.dump(dict(evidence), output, ensure_ascii=True, indent=2, sort_keys=True)
        output.write("\n")
