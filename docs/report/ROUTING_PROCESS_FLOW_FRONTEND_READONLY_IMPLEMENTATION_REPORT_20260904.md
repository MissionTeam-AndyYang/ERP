# Routing / Process Flow Frontend Read-Only Implementation Report

- Work item: ERP2-ROUTING-PROCESS-FLOW-RO-EXEC-001-UX-001
- Authorization: ERP2-CIO-ROUTING-PROCESS-FLOW-RO-EXEC-001
- Date: 2026-09-04
- Scope: bounded non-production read-only Frontend / UX implementation

## Route / Page

Implemented:

- `RoutingProcessFlowScreen`
- Route: `/routing`

The screen is a read-only Product / WIP surface for inspecting the applicable manufacturing process path. It is separate from Recipe / Formula, BOM, Product Structure, Production, Scheduling, Packaging Specification, Manufacturing Definition, and Costing.

## Component And State Summary

The implementation includes:

- `RoutingProductWipSelectorView`: Product / WIP selector with keyword search.
- `RoutingVersionSummaryPanel`: selected item, Routing no, Routing Version, version status, step count, Recipe reference count, and warning count.
- `OrderedProcessFlowView`: ordered process-flow rows with step number, stage, group, process identity, process label, standard output, standard time, performance rate, resource eligibility, and source reference.
- `RoutingContextReferenceView`: established Recipe references and bounded Packaging context.
- `RoutingGovernanceReferenceView`: governed resource eligibility and governed standard-performance reference.
- `RoutingLineageWarningPanel`: source lineage and controlled warnings.
- Loading states for dashboard/detail fetching.
- Empty states for selector, process flow, references, lineage, and unselected item.
- Error states for dashboard/detail API failure, explicitly stating that mock data was not substituted.

## API Integration Summary

Frontend service files:

- `src/services/routing-api.ts`
- `src/hooks/use-routing-dashboard.ts`
- `src/types/routing.ts`
- `src/mock/routing.ts`

Candidate read-only API routes prepared for Backend integration:

- `GET /api/v2/routing-process-flow/dashboard`
- `GET /api/v2/routing-process-flow/items/{item_no}/versions/{version}`

API mode does not silently fallback to mock data. Mock data is returned only when the user explicitly switches the data source to `mock`.

The API mapper is tolerant of likely Backend field variants while keeping frontend view-model fields stable:

- Product / WIP identity: `itemNo`, `productNo`, `wipNo`
- Routing identity: `routingNo`, `productProcessNo`
- Version: `routingVersion`, `version`
- Ordered steps: `steps`, `processFlow`
- Step order: `stepNo`, `order`
- Stage/group enum: `oneProcess`, `secProcess`
- Standard performance: `standardQuantity`, `processCount`, `standardMinutes`, `processTime`, `hourlyOutput`
- References: Recipe, Packaging, resource eligibility, standard performance
- Source lineage and warnings

## No-Write-Control Evidence

Code inspection confirms `/routing` contains no create, edit, delete, approve, release, freeze, schedule, dispatch, production, or write controls.

Capability boundary preserved:

- no Routing write
- no Process Master write
- no Recipe / BOM / Product write
- no Packaging Specification implementation
- no Manufacturing Definition implementation
- no Scheduling / Capacity execution
- no Production action or Production data load
- no Costing / valuation
- no migration, Source-of-Truth transition, Engineering Pull, Cutover, or Go-Live

## Warning / Source-Lineage Display

Mock fixtures cover:

- normal established Recipe reference
- bounded Packaging context
- governed resource eligibility
- governed standard performance
- source lineage from `product_process`, `process_flow`, and `process_capacity`
- controlled warning for missing standard performance

Warnings are displayed as controlled UX states, not as write prompts.

## Product / WIP And Ordered-Step Rendering

The mock dataset includes:

- one finished Product with four ordered process steps
- one WIP item with a controlled warning

Ordered process-flow rendering includes:

- step number
- stage label
- group label
- process no
- process label
- standard quantity and UOM
- standard time
- output per hour display
- resource eligibility
- source reference

## Validation

| Check | Result |
|---|---|
| `npm run lint` | PASS |
| `npm run build` | PASS |
| `/routing` frontend route HTTP smoke | PASS, HTTP 200 |
| `/routing` generated in Next build | PASS |
| `npm run test` | NOT AVAILABLE |

The project currently has no frontend `test` script in `package.json`. This remains `FRONTEND_TEST_SCRIPT_STANDARDIZATION_GAP`.

Browser screenshot automation was not used in this run because this workspace does not include Playwright and no local headless browser command was available on PATH. The route-level HTTP smoke, lint, build, and code-path checks were completed.

## Limitations

- Backend Routing / Process Flow API is not yet present in `main`; real-backend validation remains pending Backend `ERP2-ROUTING-PROCESS-FLOW-RO-EXEC-001-BE-001`.
- Candidate API routes may need field-level alignment after Backend publishes the confirmed contract.
- Current implementation uses mock fixtures only for manual preview and API-unavailable UX validation.
- No production, scheduling, dispatch, write, migration, cutover, or Go-Live behavior is included.

## Final Classification

**ROUTING_PROCESS_FLOW_FRONTEND_READONLY_IMPLEMENTATION_PASS_REAL_BACKEND_PENDING**

The bounded read-only Routing / Process Flow UX surface is implemented at `/routing`, screen naming is documented, API/mock separation is preserved, no write controls were added, and lint/build/route smoke passed. Final real-backend PASS remains pending confirmed Backend API contract and a DB-backed non-production service window.
