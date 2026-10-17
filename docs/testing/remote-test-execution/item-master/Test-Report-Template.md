# Item Master Test Report Template

## Run identity

```text
ModuleID=ERP2-FM02-ITEM-MASTER
CaseID=<TCxx>
RunID=<unique-run-id>
DesignVersion=<version>
SourceCommit=<sha>
RunnerCommit=<sha>
TargetID=<approved-target>
Environment=NON_PRODUCTION_ONLY
Executor=<named-executor>
AuthorizationRef=<authorization>
StartTime=<ISO-8601>
EndTime=<ISO-8601>
FixtureHash=<sha256>
Command=<bounded command or runbook reference; no secrets>
BeforeStateRef=<evidence-ref>
AfterStateRef=<evidence-ref or NOT_RUN>
RawEvidenceHash=<sha256>
CleanupStatus=<PASS|FAIL|BLOCKED|NOT_RUN>
RecoveryStatus=<PASS|FAIL|BLOCKED|NOT_RUN>
ObservedResult=<PASS|FAIL|BLOCKED|NOT_RUN>
```

## Observation

- Expected result:
- Observed result:
- First failed predicate:
- Safe-stop action:
- Residual readback:
- Owner follow-up:

## Classification

`ORDINARY` / `MIGRATION` / `CONCURRENCY` / `RESTART` / `RESTORE` / `RECOVERY`

Classification must match the authorized case and must not be broadened by the report author.
