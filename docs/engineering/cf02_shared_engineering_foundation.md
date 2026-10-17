# CF-02 Shared Engineering Foundation

Work package: `ERP2.0-CIO-GOV-CROSS-MODULE-FOUNDATION-EXECUTION-20261017-109`

Scope: CF-02 only, within the nested FM02 repository checkout.

## Delivered artifacts

| Artifact | Role |
| --- | --- |
| `engineering_foundation/environment/dev_test_profile.md` | Defines isolated local-development and offline-test profiles, source-of-truth manifests, and safety boundaries. |
| `engineering_foundation/env/frontend.env.example` | Secret-free frontend environment template. |
| `engineering_foundation/env/backend.env.example` | Secret-free backend environment template with local placeholders only. |
| `engineering_foundation/checks/quality_check.ps1` | Local quality-check and Markdown-report entry point for PowerShell/Windows. |
| `engineering_foundation/checks/quality_check.sh` | Equivalent POSIX-shell entry point for CI-compatible execution. |
| `docs/engineering/cf02_module_template_guidance.md` | Guidance for future module ownership, placement, contracts, tests and handoff. |
| `docs/engineering/cf02_offline_verification_20261017.md` | Run result and dependency availability record for this checkout. |

## Quality entry point

From the repository root:

```powershell
pwsh -NoProfile -File engineering_foundation/checks/quality_check.ps1 `
  -ReportPath docs/engineering/cf02_offline_verification_20261017.md
```

For a CI gate that requires every declared tool:

```powershell
pwsh -NoProfile -File engineering_foundation/checks/quality_check.ps1 `
  -FailOnUnavailable `
  -ReportPath docs/engineering/cf02_offline_verification_20261017.md
```

The entry point runs only the repository's existing quality commands:

- `git diff --check -- .`
- `npm run lint`
- `npm run build`
- `backend/.venv/Scripts/python.exe -m ruff check app tests alembic`
- `backend/.venv/Scripts/python.exe -m pytest -p no:cacheprovider`

It never installs dependencies, edits manifests, changes global runtimes,
starts a database, runs migrations, accesses credentials, or rewrites
`evidence/`. A missing isolated runtime or dependency is recorded as
`UNAVAILABLE`; `-FailOnUnavailable` converts that state into a non-zero CI
exit code.

## Explicit exclusions

This CF-02 package does not modify application source, database or migration
files, existing `docs/fm02` files, the existing
`docs/engineering/CROSS_MODULE_CODING_CONVENTION_20261016.md`, `evidence/`, or
any CF-01 path. It does not establish live-database, migration, concurrency,
production, or Independent TEST acceptance.
