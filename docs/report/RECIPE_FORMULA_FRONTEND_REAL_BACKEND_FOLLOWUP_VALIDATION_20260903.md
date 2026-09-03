# Recipe / Formula Frontend Real Backend Follow-up Validation - 2026-09-03

## Scope

This report closes the UX follow-up check for `ERP2-RECIPE-FORMULA-RO-EXEC-001-UX-001` after Backend / API delivered commit `82c65de`.

Validated scope is bounded to the read-only Recipe / Formula frontend surface:

- `/recipe` page rendering readiness
- confirmed read-only API contract alignment
- API mode must not silently display mock data
- source lineage and warning behavior remain visible
- no write, edit, approve, release, Recipe write, BOM write, Routing write, Production, migration, Source-of-Truth transition, Engineering Pull, Cutover, or Go-Live scope

## Backend Contract Confirmed

Backend commit `82c65de` provides the confirmed GET route family:

- `GET /api/v2/recipe-formula/dashboard`
- `GET /api/v2/recipe-formula/{recipe_no}/versions`
- `GET /api/v2/recipe-formula/{recipe_no}/versions/{version}/composition`
- `GET /api/v2/recipe-formula/by-product/{product_no}`

Backend report reviewed:

- `docs/report/Backend-API-Response-ERP2-RECIPE-FORMULA-RO-EXEC-001-BE-001-20260903-001.md`

## Frontend Contract Alignment

Frontend Recipe / Formula API mapper was updated to align with the confirmed backend payload fields:

- Dashboard item version field: `recipeVersion`
- Version status field: `versionStateCode`
- Formula status field: `formulaStatusCode`
- Formula input fields: `inputNo`, `inputName`, `inputCategory`, `inputSubCategory`
- Formula output fields: `outputNo`, `outputName`, `outputCategory`, `productVersion`
- Source lineage object: `sourceLineage.recipeSourceCode`, `inputSourceCode`, `outputSourceCode`
- Product Structure reference object: `sourceLineage.productStructureReference`
- Routing references: `sourceLineage.routingContextRefs`
- Warning codes: `missing_inputs`, `missing_output`, `multiple_outputs`, `missing_input_weight`, `missing_output_weight`, `missing_loss_source`

The mapper remains tolerant of earlier frontend proposal field names, but the confirmed backend names are now first-class supported inputs.

## Validation Results

| Check | Result | Note |
|---|---|---|
| `npm run lint` | PASS | ESLint completed successfully. |
| `npm run build` | PASS | Next.js production build completed successfully and `/recipe` was generated. |
| `npm run test` | NOT AVAILABLE | Project has no `test` script in `package.json`; retained as `FRONTEND_TEST_SCRIPT_STANDARDIZATION_GAP`. |
| Backend Recipe Formula pytest | PASS | `.venv\Scripts\python.exe -m pytest restserver\tests\test_recipe_formula_api.py -q` returned 4 passed. |
| Direct HTTP backend route reachability | PARTIAL | Flask route responded, but DB-backed request could not complete because local MariaDB was not reachable. |
| API mode silent mock fallback | PASS BY CODE PATH | API-mode catch path returns empty API data with visible error and does not return mock data. |
| Write controls | PASS BY CODE INSPECTION | `/recipe` includes no create/edit/approve/release/delete controls. |

## Real Backend Service Window Result

Local restserver was started on `http://127.0.0.1:5000`.

Unauthenticated request result:

- `GET /api/v2/recipe-formula/dashboard?count=2`
- HTTP response payload: `code=2101`, `message=missing token parameter`
- Result: PASS for token-required behavior

Authenticated non-production request result:

- `GET /api/v2/recipe-formula/dashboard?count=2`
- Header: `x-auth-token` supplied with non-production validation value; raw token not recorded
- Backend response reached Recipe / Formula route, then failed on database connectivity:
  - `mariadb.OperationalError`
  - cannot connect to server on `localhost`

Therefore, full browser validation against real DB-backed Recipe / Formula data is blocked by the current UX task environment service window, not by the frontend implementation or route registration.

## Browser Automation Note

Automated browser smoke could not be rerun in this follow-up because the current project does not include Playwright and the available tool-side Playwright import failed before page execution. This is recorded separately from the product implementation status.

Prior `/recipe` browser smoke from the initial implementation remains valid for UI rendering, no silent mock fallback under API error mode, manual mock visibility, no write controls, and zero captured console errors. This follow-up additionally fixed confirmed backend payload field mapping.

## Remaining Limitation

`REAL_BACKEND_DB_SERVICE_WINDOW_UNAVAILABLE`

Full real-backend browser validation should be rerun when the UX task environment has a reachable non-production MariaDB / restserver service window with the Recipe / Formula fixture enabled.

## Final Classification

**RECIPE_FORMULA_FRONTEND_CONTRACT_ALIGNED_LINT_BUILD_BACKEND_UNIT_PASS_REAL_DB_BROWSER_VALIDATION_BLOCKED_BY_SERVICE_WINDOW**

The frontend implementation has been updated to the confirmed backend Recipe / Formula read-only contract. Lint/build pass, backend Recipe / Formula unit tests pass, API mode preserves no-silent-mock behavior by code path, and write controls remain absent. The only remaining evidence gap is real DB-backed browser validation, blocked by local MariaDB service availability in this UX task environment.
