# ERP2.0 FM-01 UI/UX/CSS Design Review Package

**Document ID:** `ERP2.0-FM01-UI-UX-CSS-DESIGN-REVIEW-20261019-005`  
**Version:** `FM01-UI-DESIGN-20261019-005`  
**Module:** FM-01 Organization / Location Minimum Operational Module  
**Owner:** Existing Engineering Office D  
**Return target:** CTO Office V2  
**Status:** `DESIGN-ONLY / REVIEWABLE / NOT IMPLEMENTED`  
**Authorization:** Design-only C1/C2 alignment revision; no frontend source, database, SQL, runtime, test, Product-main or production action was performed. This revision preserves accepted interaction patterns and leaves `003` and `004` unchanged.

## 1. Baseline and design posture

This package consumes the following supplied baselines without changing them:

| Baseline | SHA-256 | Use in this review |
|---|---|---|
| `ERP2.0-FM01-Integrated-Design-Spec-Candidate-20261018-001.md` | `5BCAF8D4FC018928364337B6EFA82AE6FA41BE5F4BCA1871DA2119761A06DC37` | FM-01 capability, conditional mutation boundary and API candidate |
| `ERP2.0-FM01-Policy-Binding-Register-20261018-001.md` | `21BE455BCE1FA41CF80BA8B2AE75CB28F2335BA9177FFDC67A3F01F2F4EB8B00` | Role, approval, audit, lifecycle, concurrency and parent-policy gates |
| `ERP2.0-FM01-Coding-UI-Style-Review-Matrix-20261018-001.md` | `5A7B79BB78F41ED605FC524B2AE8BD178A7BB1C145B51C59566709F9EEA73395` | Existing style review baseline and open UI review requirement |

Existing ERP2.0 implementation references reviewed:

- `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0\docs\design-system\ERP_2_0_Design_System_Specification.md`
- `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0\docs\spec\design_coding.md`
- `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0\src\layouts\app-layout.tsx`
- `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0\src\components\common\module-hero.tsx`
- `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0\src\components\common\detail-card.tsx`
- `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0\src\components\common\support-empty-state.tsx`
- `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0\src\components\common\data-source-toggle.tsx`
- `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0\src\app\globals.css`

The existing GET-only surface remains the compatibility baseline. All create, update, lifecycle, approval and audit interactions below are conditional design. They are not an implementation claim or an API release decision.

## 2. UI boundary and screen inventory

Normative navigation placement is **系統設定 > 組織與地點**, using the existing `AppLayout` shell. A new top-level sidebar category is not proposed. The candidate route names below are design identifiers only.

| Screen / panel | Purpose | Primary user | Classification |
|---|---|---|---|
| `OrganizationLocationOverviewScreen` | Hierarchy-first navigation, search, filters and child list | Reader, Maintainer | `MATCH` with existing hierarchy/list baseline |
| `OrganizationLocationDetailPanel` | Read-only identity, parent chain, status and safe metadata | Reader, Maintainer, Audit Reader | `MATCH` with existing detail-card pattern |
| `OrganizationLocationCreateScreen` | Basic create for one entity at a time in a full-page form | Master Data Maintainer | `MATCH` with approved full-page create pattern |
| `OrganizationLocationEditDrawer` | Allowlisted simple update with immutable identity in a right-side drawer | Master Data Maintainer | `MATCH` with approved simple-edit pattern |
| `OrganizationLocationComplexWorkflowScreen` | Full-page lifecycle, approval and audit workflow for complex operations | Maintainer, Approver, Audit Reader | `MATCH` with approved complex-workflow pattern; capability remains conditional |
| `OrganizationLocationApprovalPanel` | Pending approval, approve/reject outcome and evidence summary | Business Approver | `DEFERRED` until approval contract is bound |
| `OrganizationLocationAuditHistoryPanel` | Before/after, actor, approver, reason and correlation readback | Audit Reader | `DEFERRED` until audit endpoint and retention are bound |

The overview is the primary screen. Detail is a right-side panel on wide screens and a full-width stacked section on small screens. Create is a full-page form. A simple allowlisted edit opens in a right-side drawer; lifecycle, approval and audit operations open the full-page complex workflow. Complex operations are never compressed into nested modal forms.

## 3. Information architecture

### 3.1 Hierarchy-first overview

The first viewport contains:

1. Existing ERP2.0 top bar and sidebar.
2. Navigation context: `系統設定 > 組織與地點`.
3. Page title: `組織與地點` with a concise operational description.
4. A compact action/search row: search by reference or display name, entity-type filter, active-state filter if the state is approved, and a primary `新增` action visible only to an authorized maintainer.
5. Two-column work area on desktop:
   - left: expandable hierarchy `Legal Entity → Company → Site`, with `Plant` and `Warehouse` as separate Site children, then `Warehouse → Location`;
   - right: selected node detail and permitted actions.
6. On narrow screens, the hierarchy becomes a stacked list with breadcrumb parent context; detail opens below the selected row.

The hierarchy must not flatten all nodes into one parallel table or imply that Warehouse is a child of Plant. Warehouse is Site-scoped; an optional Plant association is shown as a separate relationship only when admitted and validated to the same Site. Location is Warehouse-scoped. V1 does not expose nested Location hierarchy. Each actual child row is visually indented one level, exposes its parent context, and loads children on demand when the API contract supports bounded expansion. A node with no children shows a true empty child state, not mock rows.

### 3.2 Detail/read view

The detail panel uses the existing `DetailCard` pattern:

- identity block: entity type, stable reference, display name and lifecycle/status badge;
- relationship block: parent chain and child count where returned by the API;
- safe metadata block: effective dates or `location_type` only if the policy/API contract approves them;
- action block: `編輯`, `停用` or `重新啟用` only when the server-provided authorization/transition state permits them;
- history block: approval/audit tabs only when the corresponding contract is available.

Technical identifiers and correlation IDs are visible only in a secondary metadata section or audit view. Credentials, SQL, stack traces and internal assignment fields are never displayed.

## 4. User journeys

### Journey A — Read hierarchy and detail

1. User opens `組織與地點`.
2. Screen requests the hierarchy endpoint and displays a loading state in the tree and detail regions.
3. User expands a node or searches by `ref`; Site lists distinguish Plant children from Warehouse children, and Warehouse shows its optional validated Plant association separately.
4. User selects a node; the detail panel shows the safe read contract.
5. User can return to the parent breadcrumb or select another node without losing the current search term.

Success means the screen makes the parent-child chain legible and preserves the existing GET envelope. Empty children, not-found search and API failure remain distinct states.

### Journey B — Basic create

1. Authorized Maintainer chooses an entity type and selects `新增`.
2. The UI opens `OrganizationLocationCreateScreen` as a full-page form with a persistent `返回組織與地點` path.
3. Form shows only fields valid for that entity and its parent level.
4. User selects an eligible parent from a searchable select; free-text parent IDs are not the primary path.
5. Client validates required fields and obvious local format errors.
6. Server validates identity, role, parent, uniqueness, approval and idempotency predicates.
7. On submission, the UI shows `Pending Approval`; it does not represent the entity as finally effective. Only the independently approved and audited result can be shown as completed. On rejection, the UI preserves entered values and maps the safe error code to the field or form summary.

The form never implies that a successful HTTP response means business approval unless the response explicitly contains an approved state and approval evidence.

### Journey C — Controlled update

1. User opens an existing detail and chooses `編輯`.
2. For an allowlisted simple update, the UI opens `OrganizationLocationEditDrawer` from the right side; stable reference and entity type remain read-only.
3. For a lifecycle, approval, parent or other complex operation, the UI navigates to `OrganizationLocationComplexWorkflowScreen`; it does not use a nested modal.
4. Only `display_name` is editable in the current simple-update drawer; parent changes and all other fields remain protected.
5. The UI submits an `expected_row_version` and idempotency binding supplied by the eventual API contract. The allowlisted update remains `Pending Approval` and is not finally applied until independent approval and attributable audit evidence succeed.
6. The requester cannot approve the requester's own change; the approval state and separate approver identity are visible in the full-page complex workflow.
7. A stale-version response returns the user to a conflict review showing current server value, submitted value and reload/review action; the stale update is not applied.
8. Same-key/same-intent retry shows the original result without implying a second change; same-key/changed-intent is shown as an idempotency conflict and requires a newly reviewed submission.
9. No automatic overwrite, silent merge or automatic resubmission is offered.

### Journey D — Deactivate / reactivate

1. User selects a lifecycle action from the detail panel.
2. The UI navigates to `OrganizationLocationComplexWorkflowScreen`.
3. The workflow presents current state, applicable effective dates, parent/relationship checks, unresolved active dependent/downstream impact, reason and evidence reference.
4. The confirm action is disabled until required policy inputs are complete.
5. Submission remains `Pending Approval`. The lifecycle transition takes final effect only after independent approval, attributable audit evidence and separately attributable execution succeed; otherwise the UI shows the pending or fail-closed result.
6. Reactivation is an explicit review; it is never presented as an automatic inverse of deactivation.

Hard delete, silent recoding and unrestricted reparenting are not offered.

### Journey E — Approval and audit readback

1. Approver opens the full-page complex workflow from a pending mutation.
2. UI presents requested operation, before/after values, requester, reason, evidence reference, correlation ID and timestamp.
3. Approver can approve or reject only when the server confirms the role and separation-of-duty predicate; the requester is barred from approving the same request.
4. Audit Reader can view the immutable readback in the same workflow but cannot mutate the record.
5. If approval/audit data is unavailable, the UI shows a bounded unavailable state and does not suggest that the operation completed.

## 5. Field-state and entity rules

### 5.1 Common field rules

| Field | Read view | Create | Controlled update | Rule |
|---|---|---|---|---|
| `entity_type` | Read-only | Select once | Read-only | Determines field set and parent level |
| Technical `id` | Read-only when returned | Server-generated | Read-only | Never user-editable |
| Stable `<entity>_ref` | Read-only | Required input if contract permits | Read-only | Immutable by default; duplicate rejected |
| `display_name` | Read-only | Required | Editable if allowlisted | Inline validation plus form summary |
| Parent reference | Read-only | Required for child entities | Read-only by default | Eligible parent required; no free reparenting |
| Lifecycle/status | Badge | Server-derived | Server transition only | Unknown state is fail-closed |
| `active_flag` / effectivity | Conditional read-only | Not user-entered by default | Not user-entered by default | Expose/filter only after policy decision |
| `location_type` | Conditional read-only | Not admitted for V1 mutation | Not editable | Excluded from the current field/API catalogue |
| `effective_from` / `effective_to` | Display when returned | Required/conditional per entity and operation | Controlled lifecycle workflow only | Approved interval must not overlap the same scoped stable identity; no direct lifecycle edit |
| `expected_row_version` | Not shown as editable | Server-provided | Hidden transport field | Required for stale-write protection |
| Idempotency key | Not shown as editable | Generated by client/session | Generated per submission | Exact format/replay window remains policy-dependent |
| Audit/provenance | Audit view only | Server-generated | Server-generated | Never accept client-supplied actor/approver |

### 5.2 Parent and child behavior

| Entity | Parent selection | Create behavior | Reparenting |
|---|---|---|---|
| `legal_entity` | None | Root create | Not applicable |
| `company` | Eligible `legal_entity` | Parent required | Disabled by default |
| `site` | Eligible `company` | Parent required | Disabled by default |
| `plant` | Eligible `site` | Parent required | Disabled by default |
| `warehouse` | Required Site parent; optional Plant association only if admitted | Show Site parent and optional same-Site Plant association separately | Plant association is protected from simple edit; no reparenting |
| `location` | Required Warehouse parent | Warehouse parent required; no nested Location parent in V1 | Parent is protected; no reparenting |

The UI must not invent `warehouse.plant_id` semantics or location parent/successor rules. If the optional Plant association is admitted, it must be validated to the same Site. If eligible-parent, same-Site compatibility, effectivity, uniqueness or transition evidence is unavailable, the operation is blocked with a clear safe explanation.

## 6. Component specification

| Component | Existing pattern to reuse | FM-01 behavior |
|---|---|---|
| `AppLayout` shell | `src/layouts/app-layout.tsx` | Existing sidebar/top bar; add route only after navigation approval |
| `ModuleHero` or compact page header | `src/components/common/module-hero.tsx` | Use a restrained header; do not turn maintenance into a marketing hero |
| Search/filter row | `SupportSearchPanel`, existing page search labels | Search by ref/name; keyboard label and clear state required |
| Hierarchy tree | Existing ERP2.0 card/list primitives | Indentation, expand/collapse, `aria-expanded`, selected state and parent breadcrumb |
| `DetailCard` | `src/components/common/detail-card.tsx` | Read-only sections, status badge and safe metadata rows |
| Status badge | `src/components/ui/status-badge.tsx` | Status text plus icon/shape or text; color is never the only signal |
| Form field | Existing Tailwind tokens and 44px input convention | Label, helper text, required marker, error text and focus state |
| Searchable parent select | Existing input/select convention | Only eligible active parents; loading and no-option states |
| `OrganizationLocationCreateForm` | Existing full-page form and input convention | Full-page create; persistent context, summary validation and explicit cancel/return |
| `OrganizationLocationEditDrawer` | Existing right-side detail/drawer convention | `display_name` only; protected identity/parent, Pending Approval status, row-version conflict and idempotency outcomes |
| `OrganizationLocationComplexWorkflow` | Existing full-page workflow and step/status patterns | Lifecycle, approval and audit; show requester/approver, evidence and resulting state; fail closed; no nested complex-operation modal |
| Confirmation dialog | Existing modal convention when available | Reserved for a final low-complexity confirmation inside an admitted workflow; not the primary lifecycle surface |
| Audit timeline/table | Existing low-border table pattern | Pending/decision/execution status and attributable before/after, actor, approver, reason, evidence, correlation and time when returned |
| Translation-ready copy | Existing language-provider/dictionary convention | Traditional Chinese is primary; all new copy uses stable translation keys when implemented |
| Empty/error/loading state | `SupportEmptyState` plus existing info/danger banners | Distinct state copy; API mode never falls back to mock rows |

## 7. State and feedback requirements

| State | UI treatment | Classification |
|---|---|---|
| Loading hierarchy/list/detail | Skeleton rows or compact spinner with `aria-busy=true`; keep layout stable | `MATCH` |
| Empty hierarchy | Explain that no records/children were returned; offer clear search/reset | `MATCH` |
| Empty audit/approval history | State “目前沒有可顯示的紀錄” only when API returns an empty collection | `MATCH` |
| Validation | Field-level error plus summary at form top; focus first invalid field | `MATCH` |
| Unauthorized | No mutation controls; explain required capability without revealing policy internals | `MATCH` |
| Authentication/session failure | Safe sign-in/session message; no retry loop without user action | `MINOR_ADJUSTMENT` |
| Duplicate reference | Mark reference field and show existing-reference conflict if permitted | `MATCH` |
| Parent not found/ineligible | Block submit and identify the parent constraint | `MATCH` |
| Stale version | Show current server value versus submitted value, state no update was applied, and offer reload/review | `MATCH` |
| Idempotency replay | For same key and intent, show the original request result and avoid implying a second change | `MATCH` |
| Idempotency conflict | For same key with changed intent, identify the conflict, retain the draft and require a newly reviewed submission | `MATCH` |
| Downstream conflict | Show blocked lifecycle action and safe impact summary, including unresolved active dependents where returned | `MATCH` |
| Effectivity/overlap conflict | Identify missing/invalid effective date or overlapping interval and block submission without changing lifecycle state | `MATCH` |
| Audit evidence pending/unavailable | Keep request pending or blocked; show safe evidence/audit status and never imply final mutation | `API_CONTRACT_DEPENDENCY` |
| Generic API failure | Structured safe error with retry; do not show mock data | `MATCH` |
| Approval pending/rejected | Persistent workflow status, requester/approver distinction and next allowed action; show no final effect while pending | `API_CONTRACT_DEPENDENCY` |
| Audit unavailable | Keep request pending/blocked; readback unavailable state; never imply evidence or mutation success | `API_CONTRACT_DEPENDENCY` |

## 8. API-to-UI mapping

The following mapping preserves the existing GET contract and keeps prospective writes visibly conditional.

| UI capability | API candidate | UI input/output | Current status |
|---|---|---|---|
| Load hierarchy | `GET /api/v1/fm01/hierarchy` | Tree nodes, parent chain, child collections | Existing GET baseline |
| Load collection | `GET /api/v1/fm01/<resource>?limit=<n>&offset=<n>` | List rows, pagination, true empty state | Existing GET baseline |
| Lookup by ID/ref | `GET /api/v1/fm01/<resource>?id=<id>` or `?ref=<ref>` | Detail panel | Existing GET baseline |
| Create | `POST /api/v1/fm01/<resource>` | Entity type, ref, display name, parent, policy inputs; returns Pending Approval, not final effect | Conditional; route not implemented |
| Controlled update | `PATCH /api/v1/fm01/<resource>/{id}` | `display_name` only; `expected_row_version`, idempotency binding and Pending Approval workflow result | Conditional; route not implemented |
| Deactivate | `POST /api/v1/fm01/<resource>/{id}/deactivate` | Reason, evidence reference, confirmation; pending independent approval | Conditional; route not implemented |
| Reactivate | `POST /api/v1/fm01/<resource>/{id}/reactivate` | Review reason/evidence, confirmation; pending independent approval | Conditional; route not implemented |
| Approval read/decision | Separate approval contract required | Pending request, approve/reject, evidence | `DEFERRED` |
| Audit readback | Separate audit/readback contract required | Actor/role, operation/entity, before/after, reason, independent approver, correlation/idempotency/version and execution result where authorized | `DEFERRED` |

### 8.1 G2 conditional API alignment

The revised UI is aligned to the G2 conditional API direction without promoting any conditional route to an implementation contract:

- Existing hierarchy, collection and detail reads remain GET-only and preserve the response envelope, pagination and true-empty semantics.
- Full-page Create maps only to the conditional create operation after role, parent, uniqueness and idempotency predicates are admitted; submission remains Pending Approval until independent approval and audit evidence succeed.
- The right-side Edit drawer may submit only `display_name` with `expected_row_version`; submission remains Pending Approval until independent approval and audit evidence succeed. Complex operations remain on the full-page workflow.
- Deactivate/reactivate, approval and audit controls are rendered only when the server returns an authorized transition/capability and the relevant contract is available.
- Unknown capability, unknown lifecycle state, missing parent eligibility, stale version, conflict or API failure fails closed: no mock rows, no optimistic completion and no silent retry.
- Approval status is separate from Active/Inactive lifecycle state; requester and approver must be distinct, and the UI cannot show final effect before approval plus attributable audit evidence.
- The Traditional Chinese UI copy is translation-ready and must not encode API codes as user-facing text.

The current verified GET API returns safe identity, reference, display and relationship fields. It does not provide an approval or audit endpoint. UI design therefore reserves those areas without fabricating endpoint names, response fields or completion states.

### 8.2 C1/C2 UI contract alignment

- **Field boundary:** simple Edit exposes only `display_name`. Technical IDs, stable references, entity type, parent IDs, lifecycle/effectivity, approval, audit, provenance, `warehouse.plant_id`, `location.parent_location_id` and `location_type` remain protected from ordinary edit.
- **Approval and lifecycle:** Create, allowlisted Update, Deactivate and Reactivate show Pending Approval until independent approval and attributable audit evidence succeed. Pending Approval remains separate from Active/Inactive; Approved is not itself Active, and the final transition is shown only after the separately attributable execution result.
- **Requester/approver:** show requester identity and approval owner/status; block self-approval and do not expose an approve action when domain/scope authority is absent.
- **Concurrency/idempotency:** stale `row_version` shows current versus submitted values and confirms no mutation occurred. Same-key/same-intent replay shows the original result; same-key/changed-intent shows a conflict and requires a newly reviewed submission.
- **Audit/evidence:** show request, approval and technical-execution states separately. Readback, when authorized, includes actor/role, timestamp, operation/entity, before/after, reason, approver where applicable, correlation, request/idempotency identity, version and execution result. Missing evidence leaves the operation pending or rejected; it never appears complete.
- **Parent/lifecycle validation:** render Plant and Warehouse as separate Site children; show an optional Warehouse-to-Plant association separately and validate same-Site compatibility when admitted. Location is Warehouse-scoped with no nested parent operation in V1. Show missing/invalid effectivity, overlapping interval, invalid parent, unresolved active dependent or downstream conflict as a blocking reason.
- **Fail closed:** unknown authority, appointment, field catalogue, parent, evidence, audit, version, idempotency or transaction outcome blocks the mutation and preserves GET-only behavior.

## 9. ERP2.0 design-system alignment

### 9.1 Typography, color and spacing

- Font family: `Inter`, `Noto Sans TC`, `Microsoft JhengHei` fallback, matching `globals.css`.
- Page title: existing `text-lg`/`text-xl` shell title; section title `text-lg` or `text-xl`; body/table text `text-sm`; labels `text-xs`.
- Color tokens: `primary`, `primaryDark`, `success`, `warning`, `danger`, `info`, `appBg`, `border`, `textPrimary`, `textSecondary` only.
- Spacing: existing 4/8/16/24/32/48 rhythm. Use `p-4`/`p-5` for operational panels and `gap-3`/`gap-4` for field groups.
- Controls: 44px minimum height for primary inputs and actions; existing `rounded-button`/`rounded-input` tokens.
- Cards: use existing border, white surface and `shadow-card`; avoid card-inside-card nesting for page sections.

### 9.2 Navigation and responsive behavior

- Reuse `AppLayout` with the existing 280px desktop sidebar, 72px header and 24px desktop content padding.
- Keep FM-01 at `系統設定 > 組織與地點`; do not create a new shell.
- Desktop: hierarchy/detail split with a bounded detail panel.
- Tablet: hierarchy and detail remain stacked columns; the simple Edit drawer may occupy the full content width when opened, while complex operations remain full-page.
- Mobile/PDA: search and entity filter stack; hierarchy becomes a touch-friendly list; detail fields become one-column; the simple Edit drawer becomes a full-width bottom/stacked panel; complex operations remain full-page; tables become labeled rows/cards or horizontal scroll with a visible table caption.
- All controls must remain usable at 44px touch target size; no action should depend on hover.

### 9.3 Accessibility

- Every input has a visible label and programmatic association.
- Expandable nodes expose `aria-expanded`, `aria-controls` and selected state.
- Tree/list keyboard path supports Tab, arrow navigation where a true tree is used, Enter/Space selection and Escape for dialogs.
- Dialogs use `role="dialog"`, labelled title, focus trap, Escape close only when safe, and focus return to the triggering control.
- Error summary is announced with `role="alert"` or `aria-live`; field errors reference their inputs.
- Status must use text and not color alone; warning/danger actions include an icon or explicit label.
- Loading state uses `aria-busy`; empty state remains readable by screen readers.
- Responsive layouts must preserve reading order: hierarchy context before detail, validation summary before fields, and action outcome before related audit history.

## 10. Coding / UI Style Conformance Matrix

| EXISTING_STANDARD | FM01_DESIGN | MATCH/DEVIATION | RECOMMENDATION | OWNER_DECISION |
|---|---|---|---|---|
| Existing `AppLayout` shell, 280px sidebar and 72px header | FM-01 entry under existing settings/navigation | MATCH | Reuse shell and approved route placement | NONE |
| Existing settings navigation | `系統設定 > 組織與地點` | MATCH | Use the approved existing settings grouping; no new top-level category | NONE |
| `globals.css` ERP tokens | Use primary/status/neutral tokens and existing radius/shadow tokens | MATCH | Do not add FM-01-only colors or CSS variables | NONE |
| `ModuleHero` / compact page header | Operational hierarchy-first header with restrained actions | MATCH | Prefer compact header over oversized dashboard hero | NONE |
| `DetailCard` and low-border table patterns | Detail panel, list and audit history | MATCH | Reuse existing components or extract shared primitives during implementation | NONE |
| Existing `StatusBadge` | Lifecycle/approval/error states with explicit text | MATCH | Never use color as the only status signal | NONE |
| Existing input convention | 44px labelled fields and searchable selects | MATCH | Keep labels/helper/error text stable across breakpoints | NONE |
| Existing empty/loading/error patterns | True empty, loading, unauthorized and safe error states | MATCH | API failure must not fall back to mock data | NONE |
| Existing API naming/versioning | Preserve `/api/v1/fm01/...` and GET envelope | MATCH | Do not add write routes until API authorization | CTO/API owner |
| Existing frontend language support | Traditional Chinese first; translation-ready labels | MINOR_ADJUSTMENT | Keep display text in dictionary-ready keys when implemented | NONE for primary locale; localization owner for key namespace |
| Existing form patterns | Full-page Create form | MATCH | Use a full-page create route/surface with persistent context and summary validation | NONE |
| Existing drawer/detail patterns | Right-side drawer for simple allowlisted Edit | MATCH | Limit drawer to simple edits; move complex operations to full-page workflow | NONE |
| Existing workflow/status patterns | Full-page workflow for lifecycle, approval and audit | MATCH | Keep capability checks and fail-closed states visible throughout the workflow | NONE |
| Existing table/card responsive patterns | Tree on desktop, stacked list/detail on mobile | MINOR_ADJUSTMENT | Define a reusable hierarchy component before implementation | NONE |
| Existing button radius in design system | Design system documents 12px; some current screens use `rounded-lg` | MINOR_ADJUSTMENT | Prefer `rounded-button`/tokenized controls for new FM-01 UI | CTO style review |
| Existing role/status data patterns | Reader, Maintainer, Approver, Audit Reader, Technical Operator; separate requester/approver | BUSINESS_POLICY_BINDING_REQUIRED + API_CONTRACT_DEPENDENCY | Enforce scope/appointment and no-self-approval; show capability from admitted response | Business Owner / IAM / API owner |
| Existing audit/readback pattern | Pending, approval, execution and immutable audit/evidence readback | API_CONTRACT_DEPENDENCY | Bind event/status fields, authorized readback and safe response before display | Records authority / API owner |
| Lifecycle transition conventions | Active/Inactive plus separate Pending Approval, effectivity and downstream guards | API_CONTRACT_DEPENDENCY | Bind effective-date, overlap, dependency-check and execution-result responses | CTO / API owner |
| Parent/FK integrity | Site children Plant and Warehouse; Warehouse-scoped Location; optional same-Site Plant association | API_CONTRACT_DEPENDENCY | Bind eligible-parent and same-Site association validation; nested Location remains disabled | CTO / API owner |
| API mutation contract | `POST`, `PATCH`, deactivate/reactivate with version/idempotency | API_CONTRACT_DEPENDENCY | UI may be reviewed, but integration waits for admitted contract | CTO/API owner |
| Approval contract | Pending/approve/reject state | BUSINESS_POLICY_BINDING_REQUIRED + API_CONTRACT_DEPENDENCY | Do not implement an invented approval endpoint or threshold | Business Owner / API owner |

## 11. Review findings

### MATCH

- Hierarchy-first navigation, detail panel, cards, low-border tables, status badges and true empty/error/loading states align with existing ERP2.0 patterns.
- Typography, color tokens, spacing rhythm, shell layout and responsive direction align with `ERP_2_0_Design_System_Specification.md` and `globals.css`.
- Existing GET API naming, envelope, pagination and safe error boundary are preserved.
- No hard delete, silent recoding or unrestricted reparenting is introduced.

### MINOR_ADJUSTMENT

- New FM-01 implementation should use tokenized `rounded-button`, `rounded-input` and `rounded-card` classes consistently; current screens contain some `rounded-lg`/`shadow-sm` variations.
- A reusable hierarchy component and dictionary-ready labels should be established before coding to avoid repeating tree, breadcrumb and parent-selection logic.
- Authentication/session-expired feedback should be standardized with the existing safe error banner pattern.

### BUSINESS_POLICY_BINDING_REQUIRED

- Screen acceptance owner and field-level acceptance for each entity.
- Role grants, delegation and separation-of-duty behavior.
- Actual role appointments, entitlement grants, approval delegates and their scope/duration.
- Records/legal confirmation of proposed retention and evidence-store/readback assignment.
- Approval thresholds, evidence type and audit retention/readback boundary.
- Translation-key namespace ownership and localization review remain implementation governance items; Traditional Chinese is the approved primary design language.

### API_CONTRACT_DEPENDENCY

- Role/capability and lifecycle-transition response contracts.
- Eligible-parent lookup and controlled mutation contracts, including version/idempotency fields.
- Approval decision and audit/readback endpoint contracts, including safe response fields.
- Write API implementation and integration.
- API version/idempotency persistence changes and any migration execution.
- UI test plan, independent TEST assignment and target-bound runtime validation.

## 12. Policy dependencies and safe implementation boundary

The following dependencies are unresolved and must remain visible to CTO/CIO review:

1. Actual role appointments, entitlement grants, approver/delegate scope and duration.
2. Exact DB/API field catalogue and admitted `display_name` update operation.
3. Evidence-store, authorized audit-readback, and legal/corporate retention confirmation.
4. Row-version and idempotency persistence representation, replay window and transaction outcome contract.
5. Approval, audit, lifecycle/effectivity, downstream-dependency and eligible-parent API response contracts.
6. Separate implementation, TEST, target/runtime and activation authorization.

Until these bindings are accepted, the safe implementation boundary is: preserve and consume GET-only read views; prepare design review only; fail closed for mutation controls whose authority or contract is unknown; and do not claim UI implementation.

## 13. Final status

`FM01_UI_DESIGN_STATUS=OWNER-POLICY-ALIGNED DESIGN PACKAGE / IMPLEMENTATION NOT AUTHORIZED`

`FM01_UI_STYLE_REVIEW=PASS`

`FM01_CODING_UI_CONFORMANCE=MATCH WITH MINOR_ADJUSTMENTS`

`FM01_EXECUTION_BINDINGS=OPEN / ACTIVATION NOT AUTHORIZED`

This artifact is suitable for CTO Office V2 owner-policy alignment review. It is not a frontend implementation, API approval, database authorization, test result or release evidence.

## 14. Design revision delta

This `002` artifact revises `001` using the approved Owner UI Style and G2 conditional API direction:

1. Navigation is normative at `系統設定 > 組織與地點` and reuses `AppLayout`.
2. Traditional Chinese is the primary design language; new copy is translation-ready.
3. Create is a full-page form.
4. Simple allowlisted Edit is a right-side drawer.
5. Lifecycle, approval and audit are full-page complex workflows; the lifecycle dialog is no longer the primary surface.
6. User journeys, component contracts, responsive behavior and the Coding/UI Style Conformance Matrix were updated accordingly.
7. G2 API alignment, GET-only compatibility, fail-closed restrictions and deferred capabilities remain explicit.
8. No frontend source, API implementation, database, runtime, test, Product-main or production change was made.

## 15. Editorial correction record

This `003` version applies only the requested editorial corrections to `002`:

1. Corrected the duplicated ordered-list number in section 3.1.
2. Reclassified role, audit, lifecycle, parent and approval policy questions as `BUSINESS_POLICY_BINDING_REQUIRED` where policy ownership is needed.
3. Reclassified route, response, capability, parent-eligibility, approval and audit interface dependencies as `API_CONTRACT_DEPENDENCY` where API definition is needed.
4. Updated the corresponding state table, conformance matrix and findings headings. Approved navigation, locale, Create, Edit and complex-workflow interaction patterns are unchanged.
5. Original `002` SHA-256 is preserved: `16132E378C62D14F917AEB85D119CE5EF3F43E67C24FB138C5EE97CC6B49A54D`.

## 16. T3 owner-policy alignment amendment

This `004` version adds the behavior required by the registered Owner Policy Decision `ERP2.0-FM01-OWNER-BUSINESS-POLICY-20261019-001` and T1 technical closure:

1. Create, allowlisted Controlled Update, Deactivate and Reactivate remain Pending Approval with no final business effect until independent approval and attributable audit evidence succeed.
2. Requester/approver separation is explicit in the user journey and approval workflow; self-approval is prohibited.
3. Pending Approval is a workflow status separate from Active/Inactive and is not stored in `active_flag`.
4. Missing execution bindings fail closed; GET-only compatibility and the approved System Settings, Traditional Chinese, full-page Create, right-side simple Edit and full-page complex-workflow patterns are preserved.
5. The accepted `003` design source hash is preserved: `524D80938A91CFC3783EF571A131E814E2C624B24DC30FA8BA09EB1227F62323`.

## 17. C3 C1/C2 UI alignment amendment

This `005` version adds only the UI behavior needed to align with the C1 lifecycle/field contract and C2 persistence/API contracts:

1. The simple Edit allowlist is exactly `display_name`; immutable references/IDs, parent links, lifecycle/effectivity, approval, audit, provenance and other excluded fields remain protected.
2. The hierarchy renders Site as parent of both Plant and Warehouse; the optional same-Site Warehouse/Plant association is separate, and nested Location parent operations are excluded from V1.
3. Pending Approval remains separate from Active/Inactive; the final approved lifecycle effect appears only after attributable execution succeeds.
4. The UI distinguishes stale row-version conflicts, same-intent idempotent replay and changed-intent idempotency conflicts with explicit no-mutation feedback.
5. Audit/evidence status, effectivity/overlap validation, parent checks and active-dependent/downstream conflicts have explicit visible pending or blocking states.
6. GET-only behavior and approved navigation, Traditional Chinese, full-page Create, right-side simple Edit and full-page complex workflow remain preserved.
7. Accepted `004` remains unchanged with SHA-256 `47FFCE3106AD3F0A74F5FE10F231FCD752D1D8243CC60ED763CE2455CD838AEA`.
