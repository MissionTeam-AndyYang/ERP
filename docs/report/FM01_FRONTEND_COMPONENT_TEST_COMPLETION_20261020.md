# FM-01 Frontend Component Test Completion

## Scope

Bounded non-DB component verification for FM-01 Organization / Location V1.
No database, SQL, migration, credential, runtime, Product-main, or business
mutation operation was performed.

## Environment

| Field | Value |
| --- | --- |
| Workspace | `FM01_I1_D_Isolated_20261019_001` |
| Branch | `codex/fm01-i1-d-20261019-001` |
| Baseline commit | `82c44625fd34d55fc2fc51fa8ff57ad87d26db47` |
| Node | `v24.15.0` |
| npm | `11.12.1` |
| Package source | `https://registry.npmjs.org/` (Owner/CIO approved) |
| Original lock SHA-256 | `6016E28CE6F8460881B8795CE067265BA4B0E8E1F1655A01976173C73F3AB899` |
| Windows checkout `package.json` SHA-256 | `A208C6B6FD613E306F65E5AD0B74DEC3FA578BCE22F21BD053EB1FEFA1105754` |
| Windows checkout `package-lock.json` SHA-256 | `A028FDE38AB1352FCC677949B19F1495336E0E27FA9FBA85D17E932D61C90805` |
| Git remote-content `package.json` SHA-256 | `AB19E106E98525156FEDE5EC91957E36F529C64204B55F235E54A10C11F3BECD` |
| Git remote-content `package-lock.json` SHA-256 | `1769AEDA966BD04EEF62F1D655D8C11350C0273BA438A50250B62D328F0287BE` |

## Toolchain

Installed exact dev packages:

```text
@testing-library/jest-dom@7.0.1
@testing-library/react@16.3.3
@testing-library/dom@10.4.2
@vitejs/plugin-react@6.1.2
jsdom@30.1.3
vitest@5.0.5
```

Configuration:

- `vitest.config.ts`: React plugin, `@` alias, jsdom, test include pattern.
- `vitest.setup.ts`: Testing Library cleanup and `jest-dom` matchers.
- `package.json`: `test:component: vitest run`.

## Test Evidence

| Command | Result |
| --- | --- |
| `npm ci --ignore-scripts --no-audit --no-fund` | PASS; 485 packages installed from the approved registry |
| `npm run lint` | PASS |
| `node_modules\\.bin\\tsc.cmd --noEmit -p tsconfig.json` | PASS |
| `npm run build` | PASS |
| `npm run test:component -- --reporter=dot` | PASS; 2 files, 7 tests, 7 passed |

The component cases cover hierarchy, detail loading/error/empty states,
controlled edit validation, create validation/API failure, and workflow
fail-closed controls. All fixtures are in-memory.

The final lock resolution made unavoidable hoisted/peer changes required by
the approved exact test toolchain and the existing manifest's `latest`
ranges: `@jridgewell/sourcemap-codec` `1.5.5` to `1.6.0`, `nanoid` `3.3.12`
to `3.3.20`, `postcss` `8.5.14` to `8.5.31`, `react-is` `19.2.6` to
`17.0.2`, `source-map-js` `1.2.1` to `1.2.2`, and `tinyglobby` `0.2.16` to
`0.2.17`. The direct peer `@testing-library/dom@10.4.2` was added because
the exact Testing Library React package requires it. No application dependency
was intentionally upgraded and `npm audit fix` was deliberately not run
because dependency changes outside the approved exact test toolchain are out
of scope. The install reported 15 npm audit findings; they remain unchanged
and are recorded as a limitation.

The repository was checked out with `core.autocrlf=true`, so the Windows
checkout hashes and the Git remote-content hashes are intentionally different
line-ending representations of the same committed files.

## Limitations

These results do not claim backend/API integration, remote database behavior,
migration safety, production readiness, release acceptance, or PM closure.
