# FM-01 Test Tools Runbook

## Scope

The source tool supports deterministic non-DB fixture checks and report
generation. It does not replace the approved 53-case test plan and does not
claim test execution, runtime readiness, or database readiness.

## Non-DB runner

Use `run_non_db_cases()` with explicit `TestCase` objects and in-memory
fixtures. Each case produces `PASS` or `FAIL`; the aggregate report is
`PASS` only when every supplied case passes.

## Remote DB runner

`RemoteDbTestRunner` is intentionally fail-closed. Without an explicitly
authorized target and credential provider it returns `NOT_RUN`. Even when
bindings are supplied, `execute()` remains disabled until a separate
Runtime/Remote DB authorization is recorded.

No credentials, hosts, ports, database names, or target identifiers are stored
in source or fixtures.

## Evidence and cleanup

`build_evidence()` records the caller-provided commit/tree, result status,
limitations, Test Engineering status, and a deterministic hash of the report
payload. `write_report()` writes only to a caller-selected path. Fixture
cleanup is the caller's responsibility and must be deterministic; no live or
governed data may be used.

## Frontend static checks

The FM-01 frontend recovery reuses the FM-02 Vitest/Testing Library shape and
the existing FM-01 ESLint flat-config shape. From the frontend repository root,
run:

```powershell
npm ci --ignore-scripts --no-audit --no-fund
npm run lint
node_modules\\.bin\\tsc.cmd --noEmit -p tsconfig.json
npm run build
npm run test:component
```

The component runner is `vitest.config.ts` with `jsdom` and
`vitest.setup.ts` using Testing Library cleanup and `jest-dom` matchers. The
test command is intentionally project-local: `test:component: vitest run`.

## Frontend recovery evidence

The FM-01 recovery baseline is `82c44625fd34d55fc2fc51fa8ff57ad87d26db47`.
The original `package-lock.json` lineage is
`6016E28CE6F8460881B8795CE067265BA4B0E8E1F1655A01976173C73F3AB899`.
After the Owner/CIO-approved test-tool installation, the current Windows
checkout hashes are `A028FDE38AB1352FCC677949B19F1495336E0E27FA9FBA85D17E932D61C90805`
for `package-lock.json` and
`A208C6B6FD613E306F65E5AD0B74DEC3FA578BCE22F21BD053EB1FEFA1105754` for
`package.json`. Because this checkout has `core.autocrlf=true`, the Git
repository-content hashes used for remote readback are
`1769AEDA966BD04EEF62F1D655D8C11350C0273BA438A50250B62D328F0287BE` for
`package-lock.json` and
`AB19E106E98525156FEDE5EC91957E36F529C64204B55F235E54A10C11F3BECD` for
`package.json`.

The approved package source was `https://registry.npmjs.org/`, with
`--ignore-scripts --save-exact`. The six direct test packages and lock
integrities are:

| Package | Version | Integrity |
| --- | --- | --- |
| `@testing-library/jest-dom` | `7.0.1` | `sha512-oMDTC3oA+6CXSO2JZnvOI7CA6oVub6kij5ggk9ohwye5slmkwxYDXcPOVxgMw/RQlticjtO0C1RZkR97HgrWMw==` |
| `@testing-library/react` | `16.3.3` | `sha512-Uo193NgQbPMz6lrrhtRQQFcMC6Re/ELLFbbuVL30WDlZxlpZf9/lMHTAVxPRLw1q1iu9OJmR1c2BLiENRstdBg==` |
| `@testing-library/dom` | `10.4.2` | `sha512-yzr2S9HyAIdhz2/6qHgbs665Q7PKVcDF05vsOlHPxG1mo36gKVesdYVeDLnXgfjJ03CrKRk08knc6+E/9m8v2Q==` |
| `@vitejs/plugin-react` | `6.1.2` | `sha512-fhJNGUdscQa4HkI0xFxwonWyhnVReCPDbXI7FH7jmzpnVCrFQI7PRrhWecO263610vOrs9tr2Y4xcf8uAdFxbw==` |
| `jsdom` | `30.1.3` | `sha512-hQMUPvRgN7KxsfIytDQji7bimuJeRQa6Qo5+iuiZQk5CafeRxLIA10/cG5YCBFNpD9RO3oqIiN4CO1Y44kxqXg==` |
| `vitest` | `5.0.5` | `sha512-cPODOMF8YnkiiYtDdHo6n4wWmBrOBBbOIYH2d33M4l3CdNn72h+qMmO6uXffUN6A5AZFXNND/d+krS9mgkXRfg==` |

The existing manifest uses `latest` for several unrelated development
packages. npm therefore made unavoidable hoisted/peer resolution changes
needed by the approved Vitest/Vite graph: `@jridgewell/sourcemap-codec`
`1.5.5` to `1.6.0`, `nanoid` `3.3.12` to `3.3.20`, `postcss` `8.5.14` to
`8.5.31`, `react-is` `19.2.6` to `17.0.2`, `source-map-js` `1.2.1` to
`1.2.2`, and `tinyglobby` `0.2.16` to `0.2.17`. The direct peer
`@testing-library/dom@10.4.2` was added because it is required by the exact
Testing Library React package. No `npm audit fix`, uncontrolled upgrade, or
deliberate application dependency upgrade was performed. Installation
reported 15 audit findings; they were recorded and left unchanged under this
bounded task.

The recovery pass corrected seven confirmed lint findings without disabling
rules: effect-start state resets were moved to user actions or request-keyed
state, the workflow route is derived from `useSearchParams` under a Suspense
boundary, the edit draft is keyed to the selected record, and hierarchy icons
use stable conditional rendering instead of a dynamically created component.

Verified commands for this pass:

```powershell
npm ci --ignore-scripts --no-audit --no-fund
npm run lint
node_modules\\.bin\\tsc.cmd --noEmit -p tsconfig.json
npm run build
npm run test:component -- --reporter=dot
```

`lint`, TypeScript, production build, and component tests completed
successfully. The final component result was **2 test files, 7 tests, 7/7
passed**. Coverage is limited to in-memory FM-01 UI behavior:

- hierarchy construction/rendering, selection callback, and empty state;
- detail loading, API error/retry, empty selection, and successful detail;
- edit draft validation and disabled update submission;
- create-page validation, API failure fail-closed behavior, and disabled
  create submission;
- workflow record loading and disabled submit/approve/reject controls.

The default sandbox build initially returned a Windows `EPERM` while Next.js
created `.next` output directories; the same command completed successfully
with approved elevated filesystem access. Generated `.next` output is not
source evidence and is not committed. Vitest emitted a non-failing config-loader
warning because the repository remains CommonJS-default; no warning
suppression was added.

This runbook records frontend static checks and non-DB component evidence only.
It does not authorize DB, SQL, migration, credentials, runtime mutation,
Product-main changes, or PM closure.

## Classification

- Tool source: implemented at source level.
- Non-DB execution: available only when explicitly invoked by an authorized test stage.
- Remote DB execution: `NOT_RUN` / runtime authorization required.
- Test Engineering: component toolchain complete for this bounded non-DB scope;
  broader integration, remote DB, and release acceptance remain deferred.

## Preparation-Only Target Sequence Notice

This notice is preparation metadata only and is **not an adopted operational
runbook**. The review-only future sequence is:

1. Module-Isolated Validation on selected FM-01 target `ERP2-FM01-FUNCTIONAL-NP-001` / `127.0.0.1:3342`;
2. Shared DEV Integration candidate `ERP2-DEV-MARIADB-001` / `127.0.0.1:3344`;
3. System Integration Acceptance after separate authorization.

No database execution, service start/stop, SQL, migration, fixture, backup,
restore, reset, runtime credential use, or assignment activation occurred for
this notice. Port `3344` is a candidate only; port `3345` is FM02 and remains
untouched. The current 3342 runner, backup, restore, reset, and safe-stop
procedures remain `HOLD` / planning-only pending an external trusted verifier,
executor, and separate CIO DB execution authorization.

Independent TEST evidence must be produced independently and transferred back
through the owner-host/CTO evidence route with target, source, operator,
authorization, timing, and cleanup provenance. This notice does not grant TEST
authority, runtime credentials, Product acceptance, release, or Go-Live
authority. Target-binding addendum:
`FM01_Isolated_DB_Preparation_20261020_001/evidence/controlled-exchange/FM01-3342-TARGET-BINDING-ADDENDUM-20261020-001.md`.
\n+## CTO-REQ-20261020-FM01-3342-003 source/tool implementation checkpoint\n+\n+The package now contains a concrete fail-closed Python entrypoint and target-bound operation dispatch interfaces for start/readiness, graceful stop, migration order 0001 -> 0004, backup, restore, reset, fixture lifecycle, and redacted evidence. Offline adversarial coverage verifies operation allowlists, explicit `start` authorization, fixture authorization before adapter access, target identity gates, backup-hash/cleanup/post-empty evidence gates, canonical signature policy shape, and credential-provider HOLD behavior.\n+\n+This checkpoint is not runtime validation. The operational PowerShell scripts remain HOLD gates; no MariaDB binary/service adapter, DB client/driver, credential provider, evidence sink, public-key/certificate trust store, revocation source, or private key is installed or configured. CIO must separately approve signer/trust policy, credential custody/injection, service/binary/config identity, and runtime evidence acquisition before any 3342 operation.\n+
