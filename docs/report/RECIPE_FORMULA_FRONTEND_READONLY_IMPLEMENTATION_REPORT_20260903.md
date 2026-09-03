# Recipe / Formula Frontend Read-Only Implementation Report

- Work item: ERP2-RECIPE-FORMULA-RO-EXEC-001-UX-001
- Authorization: ERP2-CIO-RECIPE-FORMULA-RO-EXEC-001
- Execution mode: bounded non-production Frontend / UX implementation
- Project: ERP-2.0
- Branch: main
- Route: `/recipe`
- Date: 2026-09-03

## Scope

Implemented the bounded read-only Recipe / Formula product surface.

The implementation preserves the accepted semantic boundary:

- Recipe / Formula is one governed product lane.
- Formula is the quantitative composition / transformation view of a Recipe Version.
- One Recipe Version has one or more inputs and exactly one defined output.
- Weight, UOM, weight ratio, and input-specific loss are represented.
- Product Structure and Routing are shown only as references.
- BOM, Product Structure, Recipe / Formula, Routing, Packaging, Production Observation, and Costing remain distinct.
- No write, edit, approval, release, mutation, Recipe write, BOM write, Routing implementation, Packaging implementation, Manufacturing Definition implementation, Production, migration, Source-of-Truth transition, Engineering Pull, Cutover, or Go-Live behavior was added.

## Files Changed

- `src/types/recipe.ts`
  - Added Recipe / Formula dashboard, detail, version, input, output, lineage, warning, and reference view-model types.
- `src/services/recipe-api.ts`
  - Added read-only API client for the candidate route family:
    - `GET /api/v2/recipe-formula/dashboard`
    - `GET /api/v2/recipe-formula/{recipe_no}/versions/{version}/composition`
  - Added API-to-view-model mapping and enum/code display conversion.
  - Preserved no silent mock fallback in API mode.
- `src/hooks/use-recipe-formula-dashboard.ts`
  - Added dashboard loading/error/source state hook.
- `src/mock/recipe.ts`
  - Added explicit mock fixtures for manual mock mode only.
- `src/app/recipe/page.tsx`
  - Added the read-only Recipe / Formula screen.
- `src/layouts/app-layout.tsx`
  - Added `/recipe` navigation entry.
- `src/i18n/dictionary.ts`
  - Added `nav.recipe` label for existing language dictionaries.
- `docs/spec/api-proposal/planned_screen_list_naming.md`
  - Added Recipe / Formula screen roadmap and component naming.

## UX States Implemented

- Recipe selection.
- Recipe Version summary and version selector.
- Formula composition table.
- Input item, quantity, UOM, weight, weight ratio, and input-specific loss display.
- Exactly-one defined output panel.
- Source lineage panel.
- Warning panel.
- Related Product Structure reference panel.
- Related Routing context reference panel.
- Empty state.
- Not-found style state when defined output or references are absent.
- Loading state.
- Error state.
- Read-only negative-control visibility by absence of write/edit/approve/release controls.

## Mock Fixture Treatment

Mock data is only used when the operator manually selects `示範資料`.

In API mode, API failure remains visible and does not silently show mock data.

## API / Backend Status

Backend read-only API contract is pending `ERP2-RECIPE-FORMULA-RO-EXEC-001-BE-001`.

The frontend currently aligns to the CTO candidate route family:

- `GET /api/v2/recipe-formula/dashboard`
- `GET /api/v2/recipe-formula/{recipe_no}/versions/{version}/composition`

The frontend mapper is tolerant of common response field variants while keeping the UI view model separate from database and ORM names. Final real-backend validation must be performed after Backend / API returns the confirmed route contract, service-window evidence, and authorized non-production fixture.

## Validation

- `npm run lint`: PASS
- `npm run build`: PASS
- `npm run test`: NOT AVAILABLE

The project currently has no `test` script in `package.json`. This remains `FRONTEND_TEST_SCRIPT_STANDARDIZATION_GAP`.

Browser smoke result:

- `/recipe` route renders successfully.
- API mode against an unavailable backend shows a visible Recipe / Formula error state.
- API mode does not silently display mock Recipe data.
- Manual mock mode displays Recipe selector, Recipe Version summary, Formula composition table, defined output panel, source lineage panel, warning panel, and Product Structure / Routing reference panel.
- No write/edit/approve/release controls were visible.
- No browser console errors were captured during smoke validation.

## Limitations

- Real-backend browser validation is pending Backend / API delivery of `ERP2-RECIPE-FORMULA-RO-EXEC-001-BE-001`.
- Browser smoke used manual mock fixtures for complete UX-state visibility and an intentionally unavailable API URL for error/no-silent-mock validation.
- Broader real fixture coverage is still needed for unresolved warning, not-found output, empty input, and multiple version cases after backend service-window availability.

## Final Classification

**RECIPE_FORMULA_FRONTEND_READONLY_IMPLEMENTATION_PASS_REAL_BACKEND_PENDING**

The bounded read-only Recipe / Formula UX surface is implemented, screen naming is documented, API/mock separation is preserved, and lint/build/browser smoke passed. Final real-backend PASS remains pending the confirmed Backend / API contract and active non-production service window.
