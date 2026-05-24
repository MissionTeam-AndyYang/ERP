# ERP V1 Frontend Design Audit

Date: 2026-05-25
Scope: Non-subjective design and usability audit for the V1 frontend while backend API implementation is pending.

## Purpose

This audit checks whether the current first-version pages remain aligned with the agreed ERP direction:

- ODM food processing factory context.
- Web-based, clear, professional, concise and practical operation style.
- First focus on owner/manager roles.
- Ready for backend API integration without redesigning the information structure.

This audit intentionally avoids subjective visual redesign choices that should wait for user review.

## Pages Checked

| Page | Route | Smoke result | Current data source |
| --- | --- | --- | --- |
| Manager Dashboard | `/` | Pass | Mock fallback |
| Warehouse | `/warehouse` | Pass | Mock fallback |
| Orders | `/orders` | Pass | Mock fallback |
| Production | `/production` | Pass | Mock fallback |
| Quality | `/quality` | Pass | Mock fallback |
| Planning / APS | `/planning` | Pass | Mock fallback |
| Purchasing | `/purchasing` | Pass | Mock fallback |
| Logistics | `/logistics` | Pass | Mock fallback |
| Finance | `/finance` | Pass | Mock fallback |
| R&D / Costing | `/rd` | Pass | Mock fallback |
| Workforce | `/workforce` | Pass | Mock fallback |
| Traceability | `/traceability` | Pass | Mock fallback |
| Settings / Master Data | `/settings` | Pass | Mock fallback |
| Items | `/items` | Pass | Mock fallback |
| BOM | `/bom` | Pass | Mock fallback |
| Batches | `/batches` | Pass | Mock fallback |
| AI Center | `/ai` | Pass | Mock fallback |

Browser smoke found no console errors on the checked pages.

Mobile-width smoke also confirmed no page-level horizontal scroll after the layout containment fixes. Wide tables still keep their intended local `overflow-x-auto` behavior inside the table card.

## Confirmed Strengths

| Area | Finding |
| --- | --- |
| Business alignment | Core pages follow the confirmed management priorities: fulfillment risk, warehouse value/space/risk, production schedule/readiness, quality blockers, planning feasibility, purchasing readiness, logistics, finance, R&D/costing, workforce and traceability. |
| API readiness | All first-version pages expose mock fallback and can later switch to API data by endpoint. |
| Status language | `StatusBadge` provides consistent visual language for success, warning, danger, info and neutral states. |
| Page structure | Pages open directly into operating workspaces rather than landing/marketing screens. |
| Navigation | Core modules and support modules are available from the shared layout. |
| Manager fit | The current information hierarchy is management-oriented rather than operator-heavy. |

## Issues Found And Actions Taken

| Issue | Impact | Action |
| --- | --- | --- |
| Core work pages with wide tables could push the whole mobile page horizontally because grid children used default min-width behavior. | Users on narrow screens could get page-level horizontal scrolling instead of table-level scrolling. | Added `min-w-0` to the main content column of Warehouse, Orders, Production, Quality, Planning, Purchasing, Logistics, Finance, R&D, Workforce, Traceability and Settings pages. |
| Mobile module navigation contains many module shortcuts and can visually extend beyond viewport while scrolling horizontally. | Intended local horizontal navigation could feel like whole-page overflow on narrow screens. | Added `w-full max-w-full` to mobile navigation and added global `body { overflow-x: hidden; }` while preserving table-level `overflow-x-auto`. |

## Remaining Non-Blocking Design Risks

| Risk | Recommendation |
| --- | --- |
| Many core pages use the same left-list/right-detail pattern. | Keep this for V1 consistency; later add a shared workspace shell component if maintenance cost grows. |
| Some page headers contain dense status badges and long descriptions. | Keep for now because they explain mock/API state and business scope; refine wording after real API data lands. |
| Large data tables are necessary for manager review but less ideal for phone use. | V1 can accept horizontal table scroll; V1.5 should consider card/list alternatives for mobile operators. |
| Support pages Items/BOM/Batches/AI are less mature than core pages. | Keep them as Phase 1.5 support surfaces until core API integration stabilizes. |
| I18N is structurally started, but many page-level labels remain hard-coded. | After API integration begins, extract stable page labels into dictionary gradually, starting with navigation, shared status labels and page headers. |

## Recommended Next UI Work

| Priority | Work | Trigger |
| --- | --- | --- |
| 1 | Re-check Warehouse page with real API data. | After engineer returns Warehouse API runtime report. |
| 2 | Add module-specific page review reports using `docs/frontend/ERP_V1_FRONTEND_PAGE_REVIEW_TEMPLATE_20260525.md`. | After each API endpoint passes contract verification. |
| 3 | Gradually consolidate repeated workspace layout into shared components. | After two or more modules require the same layout adjustment. |
| 4 | I18N extraction for hard-coded page labels. | After V1 page wording stabilizes. |
| 5 | Mobile operator view patterns. | When operator-role workflows become implementation scope. |

## Acceptance Decision

Decision: `accepted_with_notes`

Reason:

The V1 frontend remains aligned with the user's planning direction and is ready for backend API validation. The main low-risk layout issue found during the audit was addressed. Remaining items are improvement opportunities, not blockers for the next backend/API integration stage.
