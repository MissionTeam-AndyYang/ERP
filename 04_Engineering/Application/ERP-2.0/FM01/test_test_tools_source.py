from __future__ import annotations

from .test_tools import RemoteDbTestRunner, TestCase, TestStatus, run_non_db_cases


def test_non_db_runner_is_deterministic_for_passing_cases():
    report = run_non_db_cases([
        TestCase("FM01-NDB-001", "synthetic pass", lambda: None),
    ])
    assert report.status == TestStatus.PASS
    assert report.cases[0]["status"] == TestStatus.PASS


def test_non_db_runner_retains_failure_without_stopping_other_cases():
    report = run_non_db_cases([
        TestCase("FM01-NDB-002", "synthetic fail", lambda: (_ for _ in ()).throw(ValueError("expected"))),
        TestCase("FM01-NDB-003", "synthetic pass", lambda: None),
    ])
    assert report.status == TestStatus.FAIL
    assert [case["status"] for case in report.cases] == [TestStatus.FAIL, TestStatus.PASS]


def test_remote_db_runner_is_not_run_without_explicit_binding():
    report = RemoteDbTestRunner(None, None).execute()
    assert report.status == TestStatus.NOT_RUN
    assert any("authorization" in item for item in report.limitations)
