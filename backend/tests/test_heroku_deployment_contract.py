from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_heroku_backend_contract_declares_runtime_dependencies_and_web_process() -> None:
    assert (ROOT / ".python-version").read_text(encoding="utf-8").strip() == "3.12"
    assert (ROOT / "requirements.txt").read_text(encoding="utf-8") == "-e ./backend\ngunicorn>=23,<24\n"
    assert (ROOT / "Procfile").read_text(encoding="utf-8") == (
        "web: gunicorn --chdir backend --bind 0.0.0.0:$PORT app.main:app\n"
    )


def test_heroku_runbook_keeps_database_and_custody_boundaries_explicit() -> None:
    runbook = (ROOT / "docs" / "deployment" / "HEROKU_NONPROD_BACKEND_RUNBOOK.md").read_text(
        encoding="utf-8"
    )
    assert "DATABASE_URL" in runbook
    assert "secret boundary" in runbook
    assert "Production/Actual" in runbook
