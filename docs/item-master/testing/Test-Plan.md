# FM-02 TEST Plan

## Objectives

1. Verify current bounded Item behavior against the approved design/source contract.
2. Verify migration/recovery evidence without substituting Engineering self-test for Independent TEST.
3. Verify isolated API behavior and distinguish it from shared runtime deployment.
4. Preserve target, credential, correlation and custody boundaries.

## Test levels

| Level | Target | Authority | Result |
|---|---|---|---|
| Engineering | FM-02 DEV lane | Engineering bounded execution | Six tests passed. |
| Independent isolated | Resettable `127.0.0.1:3354` | Independent TEST | Six tests passed; downgrade/reapply performed. |
| Shared HTTP | `127.0.0.1:8087` | Not authorized by C1 | Not a FM-02 pass; endpoint is FM-01. |
| Future C3 integration | Named designated FM-02 endpoint | Separate C3 authorization | Not executed. |

## Exit evidence

Source commit/tree, exact commands, environment, target identity, test output, schema/revision readback, rollback/recovery, privilege separation, correlation and Repository receipt are required.

