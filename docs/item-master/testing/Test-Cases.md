# FM-02 TEST Case Catalog

Revision `2026-10-18-002`: retains all DB-dependent and production-restricted cases. The prior migration static-contract FAIL remains in the report; reconciliation classification is `SOURCE_ADMISSION_GAP`.

| Case | Evidence status | Notes |
|---|---|---|
| TC01 valid compatibility | PASS | Engineering and Independent TEST evidence. |
| TC02 invalid category/UOM | PASS | Negative validation evidence. |
| TC03 specification lineage | PASS | Isolated test evidence. |
| TC04 effectivity overlap | PASS | Isolated test evidence. |
| TC05 lifecycle idempotency | PASS | Isolated test evidence. |
| TC06 lifecycle concurrency | PASS | Isolated test evidence. |
| TC07 rollback atomicity | PASS | Isolated test evidence. |
| TC08 technical actor rejection | PASS | Isolated test evidence. |
| TC09 upgrade/downgrade/reapply | PASS | Independently performed in isolated lane. |
| TC10 live shared FM-02 route | NOT VERIFIED | 8087 is FM-01; C3 required. |
| TC11 application-runtime grant | NOT VERIFIED | New write grants were not enabled. |
| TC12 Repository final PASS receipt | PENDING | F03 custody operation required. |

## Current TEST disposition

| Case group | Current disposition | Boundary |
|---|---|---|
| Backend/frontend unit and contract | EXECUTED | Non-live isolated source baseline |
| Mock/stub functional, validation, authorization and negative cases | PARTIAL | Only available exact-baseline suites executed |
| Static schema/migration contract | FAIL / SOURCE_ADMISSION_GAP | 0003-0006 absent from source tree; no repair performed |
| Real-DB uniqueness, locking, persistence, concurrency | DEFERRED_NOT_AUTHORIZED / NOT_RUN | Live DB and SQL prohibited |
| Migration execution, upgrade/downgrade/reapply, restore/restart/recovery | DEFERRED_NOT_AUTHORIZED / NOT_RUN | Runtime mutation prohibited |
| Production/shared runtime/full acceptance | NOT_AUTHORIZED / NOT_RUN | Outside TEST authority |

## Added coverage cases

The following cases close documented design coverage gaps only. They are planned cases, not executed results. Each case has one Primary Test Type and preserves the existing TC01-TC12 history.

### TC13_ITEM_CODE_PERMANENT_NONREUSE

- CaseID: `TC13_ITEM_CODE_PERMANENT_NONREUSE`
- RequirementID: `IM-01 / Design 14.6 Permanent Item Code`
- PrimaryTestType: `Functional`
- EnvironmentClass: `Test DB`
- DBDependency: `YES`
- Mock/StubDependency: `NO`
- Preconditions: approved item-code contract, clean resettable test DB, isolated TEST identity.
- Fixtures: synthetic Item create, collision candidate, abandoned allocation candidate.
- Steps: create/reserve a code; replay the same request; attempt conflicting reuse after abandonment; inspect allocation evidence.
- ExpectedResults: opaque uppercase 12-character code is unique, replay is idempotent, abandoned code is never reused, conflicting allocation is rejected.
- ActualSourceReference: `docs/item-master/Item-Master-Design-Spec.md` Sections 2.1, 7.3, 14.6; `04_Engineering/Application/ERP-2.0/restserver/package/fm02_foundation/foundation.py`.
- ExecutionEligibility: `DEFERRED_NOT_AUTHORIZED`
- EvidenceReference: planned; no execution evidence.

### TC14_NAME_CORRECTION_AUDIT

- CaseID: `TC14_NAME_CORRECTION_AUDIT`
- RequirementID: `IM-02 / Design 14.6 Name correction audit`
- PrimaryTestType: `Functional`
- EnvironmentClass: `Test DB`
- DBDependency: `YES`
- Mock/StubDependency: `NO`
- Preconditions: existing synthetic Item, authorized correction actor, clean audit scope.
- Fixtures: original name, corrected name, material identity-change payload.
- Steps: submit a valid name correction; read before/after audit; submit a material identity change through the name-correction path.
- ExpectedResults: valid correction creates append-only before/after evidence atomically; material identity change is rejected as a name correction.
- ActualSourceReference: `docs/item-master/Item-Master-Design-Spec.md` Sections 6.6, 7.2, 14.4, 14.6.
- ExecutionEligibility: `DEFERRED_NOT_AUTHORIZED`
- EvidenceReference: planned; no execution evidence.

### TC15_BASE_UOM_LOCK_AND_EDITABILITY

- CaseID: `TC15_BASE_UOM_LOCK_AND_EDITABILITY`
- RequirementID: `IM-03 / Design 14.6 Base UOM lock`
- PrimaryTestType: `Functional`
- EnvironmentClass: `Test DB`
- DBDependency: `YES`
- Mock/StubDependency: `NO`
- Preconditions: synthetic DRAFT Item with active base UOM; formal-use marker available only in authorized test DB.
- Fixtures: pre-use Item, post-use Item, invalid UOM edit.
- Steps: edit base UOM before formal use; mark formal use; attempt base UOM edit afterward.
- ExpectedResults: pre-use correction follows approved editability; post-use base UOM change is rejected and does not mutate the Item.
- ActualSourceReference: `docs/item-master/Item-Master-Design-Spec.md` Sections 2.1, 6.4, 14.2, 14.6; `src/components/items/item-master-maintenance-panel.tsx`.
- ExecutionEligibility: `DEFERRED_NOT_AUTHORIZED`
- EvidenceReference: planned; no execution evidence.

### TC16_UOM_CONVERSION_REVISION_EFFECTIVITY

- CaseID: `TC16_UOM_CONVERSION_REVISION_EFFECTIVITY`
- RequirementID: `IM-04 / Design 6.4, 14.3, 14.6 Revisions/effective periods`
- PrimaryTestType: `Functional`
- EnvironmentClass: `Test DB`
- DBDependency: `YES`
- Mock/StubDependency: `NO`
- Preconditions: synthetic Item-UOM rows, approved fixed/catch-weight policy, resettable DB.
- Fixtures: valid revision, overlapping interval, invalid factor, catch-weight without authorization.
- Steps: create valid conversion; create overlapping revision; submit invalid factor and unauthorized catch-weight payloads; read history.
- ExpectedResults: valid revision persists with history; overlaps and invalid/unauthorized values are rejected without partial mutation.
- ActualSourceReference: `docs/item-master/Item-Master-Design-Spec.md` Sections 6.4, 7.2, 8.1, 14.3, 14.6; `04_Engineering/Application/ERP-2.0/restserver/package/fm02_c2/service.py`.
- ExecutionEligibility: `DEFERRED_NOT_AUTHORIZED`
- EvidenceReference: planned; no execution evidence.

### TC17_LIFECYCLE_APPROVAL_SUCCESSOR

- CaseID: `TC17_LIFECYCLE_APPROVAL_SUCCESSOR`
- RequirementID: `IM-05 / Design 6.5, 7.2, 14.3, 14.6 Lifecycle`
- PrimaryTestType: `Functional`
- EnvironmentClass: `Test DB`
- DBDependency: `YES`
- Mock/StubDependency: `NO`
- Preconditions: synthetic DRAFT Item, approved business actor fixture, technical executor distinct from approver.
- Fixtures: valid ACTIVE approval, missing approval, SUPERSEDED successor, terminal RETIRED Item.
- Steps: attempt lifecycle transitions with and without approval; supersede with and without successor; attempt reactivation of terminal state.
- ExpectedResults: only approved transitions succeed; successor evidence is required for SUPERSEDED; terminal state cannot reactivate; lifecycle event is retained.
- ActualSourceReference: `docs/item-master/Item-Master-Design-Spec.md` Sections 2.1, 6.5, 7.2, 14.3, 14.4, 14.6.
- ExecutionEligibility: `DEFERRED_NOT_AUTHORIZED`
- EvidenceReference: planned; no execution evidence.

### TC18_BUSINESS_TECHNICAL_ACTOR_SEPARATION

- CaseID: `TC18_BUSINESS_TECHNICAL_ACTOR_SEPARATION`
- RequirementID: `IM-06 / Design 6.5, 14.6 Authorization/provenance`
- PrimaryTestType: `Security/Authorization`
- EnvironmentClass: `Test DB`
- DBDependency: `YES`
- Mock/StubDependency: `NO`
- Preconditions: separate business approver and technical executor identities; approved role matrix.
- Fixtures: valid business approval, technical-only actor, missing delegated authorization.
- Steps: submit activation using technical executor as approver; submit with distinct approved approver; submit missing delegation evidence.
- ExpectedResults: technical executor cannot satisfy business approval; valid distinct approval succeeds; missing delegation is rejected and leaves no state change.
- ActualSourceReference: `docs/item-master/Item-Master-Design-Spec.md` Sections 6.5, 7.2, 10.2, 14.6.
- ExecutionEligibility: `DEFERRED_NOT_AUTHORIZED`
- EvidenceReference: planned; no execution evidence.

### TC19_CREATE_EDIT_API_VALIDATION

- CaseID: `TC19_CREATE_EDIT_API_VALIDATION`
- RequirementID: `IM-07 / Design 14.4 Create/Edit API contract`
- PrimaryTestType: `API/Contract`
- EnvironmentClass: `Mock/Stub`
- DBDependency: `NO`
- Mock/StubDependency: `YES`
- Preconditions: API client/service contract stub, approved payload schema, no live endpoint.
- Fixtures: valid create, missing required field, invalid category/UOM, forbidden server-only field, stale row version.
- Steps: invoke create/edit contract stub with positive and negative payloads; inspect status and structured field errors.
- ExpectedResults: valid payload shape is accepted by the contract; invalid payloads produce documented validation/conflict errors; server-only fields are not client-controlled.
- ActualSourceReference: `docs/item-master/Item-Master-Design-Spec.md` Sections 10.1, 14.4, 14.5; `04_Engineering/Application/ERP-2.0/restserver/package/fm02_foundation/foundation.py`.
- ExecutionEligibility: `ELIGIBLE_NON_DB`
- EvidenceReference: planned; no new execution in this coverage correction.

### TC20_CREATE_EDIT_IDEMPOTENCY_CONFLICT

- CaseID: `TC20_CREATE_EDIT_IDEMPOTENCY_CONFLICT`
- RequirementID: `IM-08 / Design 14.4 idempotency and conflict`
- PrimaryTestType: `API/Contract`
- EnvironmentClass: `Mock/Stub`
- DBDependency: `NO`
- Mock/StubDependency: `YES`
- Preconditions: contract stub with deterministic request fingerprint behavior.
- Fixtures: identical retry, conflicting fingerprint, stale row version.
- Steps: replay identical create/edit request; replay same key with changed payload; submit stale row version.
- ExpectedResults: identical retry returns the original logical result; conflicting fingerprint and stale version return conflict without mutation.
- ActualSourceReference: `docs/item-master/Item-Master-Design-Spec.md` Sections 10.1, 14.4, 14.6; `04_Engineering/Application/ERP-2.0/restserver/package/fm02_c2/service.py`.
- ExecutionEligibility: `ELIGIBLE_NON_DB`
- EvidenceReference: planned; no new execution in this coverage correction.

### TC21_ROLE_AWARE_FRONTEND_CONTROLS

- CaseID: `TC21_ROLE_AWARE_FRONTEND_CONTROLS`
- RequirementID: `IM-09 / Design 10.2, 14.5, 14.6 role-aware UI`
- PrimaryTestType: `Unit`
- EnvironmentClass: `Mock/Stub`
- DBDependency: `NO`
- Mock/StubDependency: `YES`
- Preconditions: component test harness with read-only, editor and approver role fixtures.
- Fixtures: valid draft, locked base UOM, lifecycle action, permission/error response.
- Steps: render each role state; inspect visible controls, locked fields, validation errors and server-error presentation.
- ExpectedResults: controls match role and lifecycle state; no Product/SKU controls appear; permission, field and conflict errors remain visible.
- ActualSourceReference: `docs/item-master/Item-Master-Design-Spec.md` Sections 10.2, 14.5, 14.6; `src/components/items/item-master-maintenance-panel.tsx` and its test.
- ExecutionEligibility: `ELIGIBLE_NON_DB`
- EvidenceReference: planned; no new execution in this coverage correction.

### TC22_CUSTOMER_SUPPLIER_PACKAGE_SCOPE

- CaseID: `TC22_CUSTOMER_SUPPLIER_PACKAGE_SCOPE`
- RequirementID: `IM-10 / Design 6.1, 7.2, 14.6 supplier/customer qualification and packages`
- PrimaryTestType: `Functional`
- EnvironmentClass: `Test DB`
- DBDependency: `YES`
- Mock/StubDependency: `NO`
- Preconditions: synthetic Item, Customer A, Supplier X/Y, general qualifications and package rows.
- Fixtures: Customer A/X approval, Customer A/Y negative, any-qualified scope, effective package overlap.
- Steps: create scoped qualification/package rows; resolve Customer A against X and Y; submit overlapping effective rows.
- ExpectedResults: X is accepted only when approved; Y is rejected when not approved; any-qualified scope follows approved rule; overlap is rejected without duplicate active rows.
- ActualSourceReference: `docs/item-master/Item-Master-Design-Spec.md` Sections 6.1, 7.2, 8.1; `04_Engineering/Application/ERP-2.0/restserver/package/fm02_c2/service.py`.
- ExecutionEligibility: `DEFERRED_NOT_AUTHORIZED`
- EvidenceReference: planned; no execution evidence.

### TC23_PRODUCT_SKU_BOUNDARY_NEGATIVE

- CaseID: `TC23_PRODUCT_SKU_BOUNDARY_NEGATIVE`
- RequirementID: `IM-11 / Design 4.2, 9, 14.4, 14.6 Product boundary`
- PrimaryTestType: `Integration`
- EnvironmentClass: `Mock/Stub`
- DBDependency: `NO`
- Mock/StubDependency: `YES`
- Preconditions: API/UI contract stub with Item-only scope.
- Fixtures: create/edit payload containing Product/SKU/GTIN fields; attempted downstream side-effect request.
- Steps: submit forbidden Product/SKU fields and inspect API/UI route surface.
- ExpectedResults: Product/SKU/GTIN/BOM/Production side effects are rejected or absent; Item contract remains bounded.
- ActualSourceReference: `docs/item-master/Item-Master-Design-Spec.md` Sections 4.2, 9, 14.4, 14.5; `docs/fm02/FM02_C2_MODULE_CONTRACT_20261016.md`.
- ExecutionEligibility: `ELIGIBLE_NON_DB`
- EvidenceReference: planned; no new execution in this coverage correction.

### TC24_MIGRATION_LINEAGE_ROLLBACK_RECOVERY

- CaseID: `TC24_MIGRATION_LINEAGE_ROLLBACK_RECOVERY`
- RequirementID: `IM-12 / Design 10.3, 10.4, 14.3; TC09 migration lineage`
- PrimaryTestType: `Migration/Database`
- EnvironmentClass: `Test DB`
- DBDependency: `YES`
- Mock/StubDependency: `NO`
- Preconditions: complete immutable 0003-0009 source admission, resettable test DB, approved migration/recovery authorization.
- Fixtures: lineage chain, forward/rollback companion files, pre/post revision and row snapshots.
- Steps: verify paths/hashes and guards; execute authorized forward/rollback/reapply; read revision, schema and row preservation.
- ExpectedResults: lineage is complete and ordered; rollback is data-preserving and guarded; reapply is deterministic; no destructive deletion or partial revision state occurs.
- ActualSourceReference: `docs/item-master/Item-Master-Design-Spec.md` Sections 10.3, 10.4, 12, 14.3; `04_Engineering/Database/fm02_item_master_0007-0009*.sql`; expected 0003-0006 paths remain absent in current source.
- ExecutionEligibility: `DEFERRED_NOT_AUTHORIZED`
- EvidenceReference: `TC09_MIGRATION_GAP=OPEN`; no execution evidence.

