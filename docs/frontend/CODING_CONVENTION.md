# Frontend Coding Convention

Frontend stack:

```text
Next.js App Router + React + TypeScript + Tailwind CSS + Recharts
```

## Directory Rules

```text
src/app/             Route pages
src/components/      Reusable UI components
src/components/common/
src/components/dashboard/
src/components/production/
src/components/warehouse/
src/components/charts/
src/layouts/         App shell and navigation
src/mock/            Temporary mock data
src/types/           Shared TypeScript types
src/services/        Future API clients
```

## Page Rules

Pages should:

- Compose existing layout and components.
- Keep business display logic readable.
- Move repeated UI into components.
- Use typed mock/API data.

Pages should not:

- Duplicate sidebar or app shell logic.
- Hard-code large repeated data blocks when a mock/service file is more appropriate.
- Introduce unrelated visual themes.

## Component Rules

Components should:

- Use typed props.
- Keep styling consistent with existing ERP dashboard patterns.
- Prefer existing shared components such as KPI cards, detail cards, process boards, and status badges.
- Keep visual density appropriate for operational ERP screens.

Components should not:

- Create one-off card styles when a shared component fits.
- Use marketing-style hero layouts for internal tools.
- Add decorative visuals that reduce scanability.

## Styling Rules

Use Tailwind classes already consistent with the project.

Keep:

- Compact dashboards.
- Clear tables/lists.
- Stable spacing.
- Readable status colors.
- Responsive layouts that do not overlap on mobile.

Avoid:

- Large decorative gradients.
- Nested cards.
- Oversized hero text inside operational modules.
- UI text that explains obvious controls.

## API Integration Rules

When replacing mock data with API calls:

- Add typed service functions in `src/services/`.
- Keep response types in `src/types/`.
- Preserve existing page layout unless the data requires a clear change.
- Handle loading, empty, and error states.

Suggested service naming:

```text
src/services/product-orders.ts
src/services/purchase-requests.ts
src/services/workflows.ts
```

## Workflow Display Rules

Use workflow API responses to drive:

- Status badges.
- Missing step warnings.
- Dashboard counts.
- Module task lists.

Do not recalculate workflow completeness differently on the frontend if the backend already provides `complete` and `missing_steps`.

## Test / Verification

For frontend changes:

```powershell
npm run build
```

For visual changes, preview locally and check:

- Sidebar navigation works.
- Text does not overflow.
- Mobile and desktop layouts remain coherent.
- Charts render with real dimensions.
