# Recipe / Formula Frontend Acceptance Retest - 2026-09-03

## Scope

This report records the bounded Frontend / UX acceptance retest for `ERP2-CIO-RECIPE-FORMULA-ACCEPTANCE-RETEST-001`.

Retest scope was limited to the read-only `/recipe` Recipe / Formula frontend against the DB-backed Backend service window:

- API base URL: `http://127.0.0.1:5029`
- Backend classification consumed: `DB_BACKED_RECIPE_FORMULA_BACKEND_SMOKE_PASS_SHARED_DEV_READONLY`
- Backend evidence report: `docs/report/Backend-API-Response-ERP2-RECIPE-FORMULA-ACCEPTANCE-RETEST-001-20260903-001.md`

No Product redesign, write controls, Recipe/BOM/Product write, Routing/Packaging/Manufacturing Definition implementation, Production, migration, Source-of-Truth transition, Engineering Pull, Cutover, Go-Live, or scope expansion was performed.

## Real Backend Evidence

DB-backed read-only API calls were executed against the active service window. Raw validation token and raw Recipe/Product identifiers were not recorded.

| Check | Result | Evidence |
|---|---|---|
| Service window reachable | PASS | `127.0.0.1:5029` TCP reachable |
| Dashboard API | PASS | `code=0`, one Recipe row returned |
| Summary payload | PASS | `recipeCount`, `versionCount`, `completeFormulaCount`, `partialFormulaCount`, `missingFormulaCount` present |
| Capability boundary | PASS | Recipe, BOM, and Product write flags are false |
| Versions API | PASS | `code=0`, one Recipe Version row returned |
| Composition API | PASS | `code=0`, `recipe`, `version`, `formula`, `inputs`, `output`, `sourceLineage`, `warnings` present |
| Recipe / Product selection data | PASS | Dashboard returned selectable Recipe row and composition returned defined output data |
| Formula composition | PASS | One input row returned |
| Input quantity / UOM / weight | PASS | Input row includes `quantity`, `unit`, and `weight` |
| Input-specific loss | PASS | Input row includes `lossSourceCode` |
| Controlled warning | PASS | `missing_loss_source` warning returned; acceptable for current read-only contract |
| Defined output | PASS | Output object includes output identifier field |
| Source lineage | PASS | `sourceLineage` object returned |
| Product Structure reference | PASS | `sourceLineage.productStructureReference` returned |
| Routing context | PASS | `sourceLineage.routingContextRefs` returned as an array |
| By-product API | PASS | `code=0`, one related Recipe Version returned |

## Frontend Evidence

Frontend was started with:

- `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5029`
- `NEXT_PUBLIC_API_TIMEZONE=Asia/Taipei`
- non-production validation token supplied through environment variable; raw value not recorded

| Check | Result | Evidence |
|---|---|---|
| `/recipe` route response | PASS | Frontend dev server returned HTTP 200 for `/recipe` |
| `/recipe` route markup | PASS | Response contains `Recipe / Formula` route content and Next app markup |
| API/mock separation | PASS | API mode catch path returns empty API data with visible error and does not return mock data |
| Manual mock mode | PASS BY EXISTING IMPLEMENTATION | Mock data is reachable only through `DataSourceToggle` user selection |
| Loading state | PASS BY CODE INSPECTION | Dashboard hook starts with `isLoading=true`; detail panel shows loading indicator while detail is pending |
| Empty state | PASS BY CODE INSPECTION | Recipe selector, Formula input, defined output, reference, and lineage panels use empty states |
| Error state | PASS BY CODE INSPECTION | Dashboard/detail API errors show visible error text and state that mock data was not substituted |
| No silent mock fallback | PASS BY CODE INSPECTION | `getRecipeFormulaDashboard` and `getRecipeFormulaComposition` return mock data only when `dataSourceMode === "mock"` |
| No write/edit/approve/release controls | PASS BY CODE INSPECTION | `/recipe` page contains no create, edit, approve, release, delete, or write controls |

## Validation Commands

| Command | Result |
|---|---|
| `npm run lint` | PASS |
| `npm run build` | PASS |

`npm run test` was not rerun for this retest because the project currently has no frontend `test` script. This remains the existing `FRONTEND_TEST_SCRIPT_STANDARDIZATION_GAP`.

## Screenshot / Browser Automation Limitation

Screenshot capture was not practical in this run:

- the project does not include Playwright;
- the available tool-side Playwright import failed before page execution;
- no local `msedge.exe`, `chrome.exe`, or `chromium.exe` command was available on PATH for headless DOM/screenshot capture.

This limitation affects screenshot evidence only. It does not invalidate the DB-backed API evidence, frontend route readiness, lint/build result, or code-path validation for API/mock separation and read-only controls.

## Service Window Close Note

Backend report instructed that the local service process should be stopped after Frontend / UX validation completes. The UX retest used the open service window only for read-only GET validation.

## Final Classification

**RECIPE_FORMULA_FRONTEND_ACCEPTANCE_RETEST_PASS_WITH_SCREENSHOT_AUTOMATION_LIMITATION**

The `/recipe` frontend is aligned to the confirmed DB-backed Backend Recipe / Formula read-only contract, the active service window returned the required dashboard, version, composition, source lineage, Product Structure reference, Routing context, warning, and by-product evidence, lint/build passed, and no silent mock fallback or write/edit/approve/release controls were found. The only limitation is unavailable local screenshot/browser automation tooling for this retest.
