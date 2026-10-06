# R4-X1 Wave-1 Exclusion and Rollback Record

- Legacy sources remain at their original paths.
- No source file was overwritten, renamed, deleted, or archived.
- No application imports, CI paths, runtime paths, database paths, or KRO locators were changed.
- Excluded from the canonical repository: runtime datadirs, `FGR1Data`, `G1P313`, `mer1_runtime`, logs, secrets, local overrides, dependencies, `.fg4_deps`, generated output, temporary worktrees, raw database state, engineering source, and routine dashboards.
- Rollback: remove the new canonical repository root and its local Git history only; legacy sources and KRO remain the rollback/reference surfaces.
- Remote push: not performed; remote state remains `PENDING / NOT CONFIGURED`.
