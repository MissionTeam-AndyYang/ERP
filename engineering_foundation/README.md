# CF-02 Shared Engineering Foundation

This directory contains disjoint, reusable engineering controls for the FM02
checkout. It does not contain application code, database definitions, or
module-specific business behavior.

## Contents

| Path | Purpose |
| --- | --- |
| `environment/dev_test_profile.md` | Reproducible local development and offline-test profiles. |
| `env/frontend.env.example` | Secret-free frontend configuration template. |
| `env/backend.env.example` | Secret-free backend configuration template. |
| `checks/quality_check.ps1` | Windows/PowerShell local quality-check and report entry point. |
| `checks/quality_check.sh` | POSIX-shell equivalent for CI-compatible execution. |

## Operating rules

- Use the existing root `package.json` and `package-lock.json` for frontend
  commands.
- Use the existing `backend/pyproject.toml` and the repository's isolated
  `backend/.venv` for backend commands.
- Do not install packages, regenerate lockfiles, switch runtimes, or use a
  global Python environment to make a check pass.
- Missing tools or isolated dependencies are reported as `UNAVAILABLE`; they
  are not silently replaced with another runtime.
- Environment templates contain local placeholders only. Copy them to ignored
  local files before use and never add credentials to this directory.

The canonical local entry point is:

```powershell
pwsh -NoProfile -File engineering_foundation/checks/quality_check.ps1 `
  -ReportPath docs/engineering/cf02_offline_verification_20261017.md
```

Use `-FailOnUnavailable` in a CI job when missing dependencies should fail the
job instead of producing a documented hold.
