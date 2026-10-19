# FM-01 53-Case Execution Contract Matrix

**Version:** `ERP2.0-FM01-EXECUTION-CONTRACT-MATRIX-20261019-002`  
**Status:** Future runner specification only; no case executed.

## Contract legend

| Code | Meaning |
|---|---|
| `ENV-S` | Static/local source or contract review; no DB, runtime or network target. |
| `ENV-M` | Disposable mock/non-DB harness with synthetic six-entity data and synthetic actor/approval state. |
| `ENV-D` | Named non-Production DB target admitted separately with least privilege, fixture namespace, reset and readback. |
| `ENV-U` | Browser/UI harness bound to Engineering D v002 and an admitted API/mock or named target. |
| `FIX-0` | No data mutation; preserve GET-only baseline. |
| `FIX-M` | Synthetic parent graph, refs, actors, versions, idempotency keys and safe errors. |
| `FIX-D` | Namespaced DB fixture with baseline fingerprint and cleanup key. |
| `FIX-U` | Synthetic/browser UI state with Traditional Chinese dictionary keys and authorization states. |
| `STEP-S` | Future runner reads exact bytes, invokes static checker, records hash and assertion. |
| `STEP-M` | Future mock runner submits request, replay/conflict/error variants, then inspects in-memory result. |
| `STEP-D` | Future DB runner preflights target, applies fixture, executes case, reads back, resets and verifies zero residuals. |
| `STEP-U` | Future browser runner navigates, captures state/response/accessibility evidence and resets session. |
| `E+` | Positive assertion; capture case/result/contract hashes and evidence manifest. |
| `E-` | Negative assertion; capture safe error, no-effect proof and owner/safe-stop on ambiguity. |
| `CL-0` | No cleanup beyond workspace/session teardown. |
| `CL-M` | Dispose synthetic state and record no residual in harness. |
| `CL-D` | Roll back or namespace-clean fixture, verify baseline fingerprint and residual count. |
| `CL-U` | Close browser/session, clear synthetic UI state and retain screenshots/trace. |

## Per-case mapping

| Case ID | Preconditions/environment | Fixture/data | Steps/future runner | Expected/evidence | Cleanup/recovery |
|---|---|---|---|---|---|
| FM01-GET-01 | ENV-S then ENV-D | FIX-0/FIX-D | STEP-S/STEP-D | E+ six-resource allowlist/envelope; hash, response, row baseline | CL-0/CL-D |
| FM01-GET-02 | ENV-D target admitted | FIX-D | STEP-D ID/ref lookup | E+ correct row or E- safe 404; response/readback | CL-D |
| FM01-GET-03 | ENV-D schema/parent readback | FIX-D parent graph | STEP-D hierarchy traversal | E+ parent chain; relationship evidence | CL-D |
| FM01-GET-04 | ENV-M and ENV-D contract bound | FIX-M/FIX-D | STEP-M/STEP-D bounds | E+ 50/100; E- invalid bounds; response evidence | CL-M/CL-D |
| FM01-GET-05 | ENV-M contract only | FIX-M invalid inputs | STEP-M invalid resource/filter | E- 400/422 safe envelope; no SQL/secrets | CL-M |
| FM01-GET-06 | ENV-D inconsistent-row fixture approved | FIX-D missing/inconsistent reference | STEP-D lookup/read | E- 404/409 and no repair; readback | CL-D; HOLD on residual |
| FM01-GET-07 | GET baseline and target admitted | FIX-0/FIX-D | STEP-D denied write methods | E- 405/denial and unchanged counts | CL-D |
| FM01-GET-08 | DB privilege readback authorized | FIX-D | STEP-S/STEP-D privilege/DDL negative | E- DDL/write denied; privilege and schema hash | CL-D |
| FM01-GET-09 | Approved field list available | FIX-D | STEP-D inspect returned fields | E+ approved fields only; response redaction evidence | CL-D |
| FM01-GET-10 | Restart authority and target admission | FIX-D | STEP-D read, restart permitted service, reread | E+ same read and zero mutation; restart logs | CL-D; stop if service control not authorized |
| FM01-CRE-01 | BO1/BO4/API write contract admitted | FIX-M/FIX-D root identity | STEP-M/STEP-D create | E+ one row/audit/idempotency result; manifest | CL-M/CL-D |
| FM01-CRE-02 | Parent and mutation authority admitted | FIX-M/FIX-D eligible parent | STEP-M/STEP-D child create | E+ child under correct parent; readback/audit | CL-M/CL-D |
| FM01-CRE-03 | Uniqueness contract and target admitted | FIX-M/FIX-D duplicate ref | STEP-M/STEP-D duplicate submit | E- duplicate/no second effect; counts/audit | CL-M/CL-D |
| FM01-CRE-04 | Parent lifecycle fixture admitted | FIX-M/FIX-D missing/inactive parent | STEP-M/STEP-D create negative | E- parent rejection/no row; error/readback | CL-M/CL-D |
| FM01-CRE-05 | Warehouse/plant policy resolved | FIX-M/FIX-D inconsistent pair | STEP-M/STEP-D create negative | E- consistency rejection/no partial row | CL-M/CL-D |
| FM01-CRE-06 | Location locality policy resolved | FIX-M/FIX-D wrong warehouse parent | STEP-M/STEP-D create negative | E- locality rejection/no row | CL-M/CL-D |
| FM01-CRE-07 | Actor/correlation/idempotency contract admitted | FIX-M malformed identity | STEP-M submit missing fields | E- fail-closed before write; request evidence | CL-M |
| FM01-CRE-08 | Idempotency persistence admitted | FIX-M/FIX-D same intent | STEP-M/STEP-D submit twice | E+ preserved result/no duplicate; replay evidence | CL-M/CL-D |
| FM01-CRE-09 | Idempotency conflict contract admitted | FIX-M/FIX-D changed intent same key | STEP-M/STEP-D replay changed payload | E- conflict/no second effect; safe-stop evidence | CL-M/CL-D |
| FM01-UPD-01 | Field catalogue/audit contract admitted | FIX-M/FIX-D existing row | STEP-M/STEP-D allowlisted update | E+ before/after/version/audit; evidence manifest | CL-M/CL-D |
| FM01-UPD-02 | Immutable-field policy admitted | FIX-M/FIX-D existing row | STEP-M/STEP-D immutable update | E- reject/no hierarchy or identity change | CL-M/CL-D |
| FM01-UPD-03 | Row-version contract admitted | FIX-M/FIX-D stale version | STEP-M/STEP-D stale submit | E- stale rejection/no audit success; response | CL-M/CL-D |
| FM01-UPD-04 | BO4 separation and roles admitted | FIX-M/FIX-D maintainer/approver actors | STEP-M/STEP-D self-approval attempt | E- separation rejection; actor evidence | CL-M/CL-D |
| FM01-UPD-05 | Transaction rollback/readback admitted | FIX-D failure-injection fixture | STEP-D fail after validation | E- full rollback including audit/idempotency | CL-D; HOLD on residual |
| FM01-LCY-01 | Lifecycle matrix and authority admitted | FIX-D eligible record | STEP-D deactivate | E+ state/history/downstream block; audit | CL-D |
| FM01-LCY-02 | Downstream conflict policy admitted | FIX-D dependent fixture | STEP-D deactivate conflict | E- rejection/no partial state; evidence | CL-D |
| FM01-LCY-03 | Reactivation policy/approval admitted | FIX-D valid parent/effectivity | STEP-D reactivate | E+ explicit revalidation/audit; readback | CL-D |
| FM01-LCY-04 | Reactivation negative policy admitted | FIX-D invalid parent/effectivity | STEP-D reactivate negative | E- rejection/not automatic inverse | CL-D |
| FM01-LCY-05 | Transition matrix admitted | FIX-M/FIX-D unknown state | STEP-M/STEP-D invalid transition | E- invalid-transition/no write | CL-M/CL-D |
| FM01-AUD-01 | Reader role fixture and BO4 admitted | FIX-M/FIX-D reader | STEP-M/STEP-D mutation attempt | E- denied/no business/audit success | CL-M/CL-D |
| FM01-AUD-02 | Approval-controlled operation admitted | FIX-M/FIX-D maintainer request | STEP-M/STEP-D submit without approval | E- pending/denied, no final mutation | CL-M/CL-D |
| FM01-AUD-03 | Separation-of-duty admitted | FIX-M/FIX-D same actor | STEP-M/STEP-D submit/approve same actor | E- rejection; authorization evidence | CL-M/CL-D |
| FM01-AUD-04 | Technical/business role boundary admitted | FIX-M technical operator | STEP-M present technical actor as approver | E- rejection; safe error | CL-M |
| FM01-AUD-05 | Audit endpoint/retention/readback admitted | FIX-D accepted mutation | STEP-D read audit | E+ required provenance fields; audit evidence | CL-D |
| FM01-AUD-06 | Rejection audit policy admitted | FIX-D rejected request | STEP-D read rejection audit | E+ attribution without secrets/SQL | CL-D |
| FM01-NEG-01 | FK enforcement admitted | FIX-D orphan parent | STEP-D invalid FK create/update | E- rejected/no orphan; counts | CL-D |
| FM01-NEG-02 | Cycle policy admitted | FIX-D self/descendant parent | STEP-D cycle attempt | E- cycle rejection/no corruption | CL-D |
| FM01-NEG-03 | Concurrency and uniqueness admitted | FIX-D same reference | STEP-D parallel create | E+ one winner/one duplicate; locks/audit | CL-D; HOLD on race ambiguity |
| FM01-NEG-04 | Row-version persistence admitted | FIX-D same row/version | STEP-D parallel updates | E+ one winner/stale loser; readback | CL-D |
| FM01-NEG-05 | Lifecycle transaction admitted | FIX-D same lifecycle row | STEP-D parallel transitions | E+ one atomic effect; audit | CL-D |
| FM01-NEG-06 | Replay window/idempotency admitted | FIX-D timeout/replay key | STEP-D retry after simulated timeout/restart | E+ preserved or E- changed-intent halt | CL-D |
| FM01-NEG-07 | Static/security contract admitted | FIX-M injection strings | STEP-S/STEP-M probes | E- parameterized/allowlisted safe error | CL-M |
| FM01-NEG-08 | Scope/authorization contract admitted | FIX-M/FIX-D cross-scope actors | STEP-M/STEP-D unauthorized request | E- denied without leakage | CL-M/CL-D |
| FM01-UI-01 | Engineering D v002 + G2 GET contract | FIX-U hierarchy states | STEP-U navigate/expand/select | E+ hierarchy/keyboard/responsive evidence | CL-U |
| FM01-UI-02 | UI artifact and create API admitted | FIX-U/FIX-M create states | STEP-U full-page create | E+ validation/parent/error/fail-closed trace | CL-U/CL-M |
| FM01-UI-03 | Simple update contract admitted | FIX-U/FIX-M row/version states | STEP-U drawer edit/stale conflict | E+ drawer/immutable/version evidence | CL-U/CL-M |
| FM01-UI-04 | Complex workflow contract admitted | FIX-U lifecycle/approval states | STEP-U escalate drawer to full page | E+ full-page workflow/no nested complex modal | CL-U/CL-M |
| FM01-UI-05 | Lifecycle policy/contract admitted | FIX-U transition states | STEP-U deactivate/reactivate review | E+ explicit state/approval/audit; no inverse | CL-U/CL-M |
| FM01-UI-06 | Authorization capability contract admitted | FIX-U authorized/unauthorized states | STEP-U inspect controls/attempt action | E- visibility/rejection/no mutation | CL-U/CL-M |
| FM01-UI-07 | Error envelope contract admitted | FIX-U loading/empty/error/validation | STEP-U drive each state | E+ distinct safe states/no mock fallback | CL-U |
| FM01-UI-08 | Accessibility/responsive acceptance admitted | FIX-U viewport/keyboard states | STEP-U keyboard, focus, responsive checks | E+ accessibility/viewport evidence | CL-U |
| FM01-UI-09 | Translation key contract admitted | FIX-U Traditional Chinese dictionary | STEP-U inspect labels/locale | E+ translation-ready/no mixed hard-coded copy | CL-U |
| FM01-UI-10 | Audit endpoint and safe field list admitted | FIX-U audit states | STEP-U audit readback | E+ safe provenance; E- unavailable never implies success | CL-U |

## Authority and execution note

All `ENV-D` and `ENV-U` cases remain blocked until target, policy, implementation, credentials and Remote Engineer/host bindings are separately authorized. This matrix is a runner contract, not evidence of execution or PASS.

