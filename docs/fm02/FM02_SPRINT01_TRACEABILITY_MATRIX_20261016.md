# FM-02 Sprint 1 Requirement Traceability Matrix

Status: source-reconciled; no live database or production claim

| Requirement | Design / rule | Implementation or source | Acceptance evidence | Status / open decision |
| --- | --- | --- | --- | --- |
| FR-01 Controlled Item identity | Item must have bounded category, display name, ownership context and active base UOM | `04_Engineering/Application/ERP-2.0/restserver/package/fm02_foundation/foundation.py` | `test_fm02_foundation.py`; live result remains separate | COMPLETE in source; dependency-backed suite NOT VERIFIED |
| FR-02 Draft-only Item creation | New Item starts in `DRAFT`; category and UOM are controlled | Foundation service and 0003 migration | Foundation source contract | COMPLETE for bounded source |
| FR-03 Specification lineage | Revision identity, hash, status and effective window are explicit | `foundation.py`; 0003 DDL | Foundation tests and migration contract | COMPLETE in source |
| FR-04 Approval-gated lifecycle | Active transition needs business evidence; technical actor cannot approve | `foundation.py`; approval/event tables in 0003 | 11 deterministic service cases include lifecycle/approval | SYNTHETIC_PASS |
| FR-05 Item-scoped reference contract | Supplier qualification and Item UOM are bound to the Item | 0004 migration; `fm02_c2/service.py` | 11 service cases; 0004 migration cases | SYNTHETIC_PASS |
| FR-06 Package/customer qualification | Customer scope and supplier qualification relationship are explicit | 0005 migration and C2 service | Scope/fingerprint/effective-period cases | SYNTHETIC_PASS |
| FR-07 Item-specific conversion | Fixed/catch-weight rules, distinct endpoints, no global fallback | 0005 migration; `resolve_conversion` | Conversion positive/negative/ambiguity cases | SYNTHETIC_PASS |
| FR-08 Idempotent retry | Same key plus same fingerprint returns durable result; conflict rejects | C2 service transaction logic and unique keys | Replay/conflicting-fingerprint cases | SYNTHETIC_PASS |
| FR-09 Effective-period safety | Overlap rejects; boundary-touching windows allowed | C2 service validation and DDL checks | Effective-period deterministic cases | SYNTHETIC_PASS |
| FR-10 Legacy mapping admission | 0006 requires zero rows and retains source-record identity | 0006 forward/down SQL | Migration contract suite | SYNTHETIC_PASS; live migration not authorized |
| FR-11 C2 API contract | Three item-scoped routes, structured errors, injected connection boundary | `backend/app/api/v1/endpoints/fm02_c2.py`, service, router | Static source review; API collection blocked by missing `pydantic` | HOLD pending dependency-complete environment |
| FR-12 C2 UI reference states | Mock display/forms, field validation, empty/error/unavailable states | `src/components/items/c2-reference-panel.tsx`, types, service, mock | Source review; browser/build tools unavailable | MOCK_READY; Product/Frontend acceptance open |
| FR-13 Evidence and authority | Status vocabulary, custody, review roles and live boundary are explicit | Offline test plan, D11/D12 docs, final manifest | 13/13 final manifest hashes verified in prior evidence | COMPLETE for documentation; remote authority open |

## Acceptance rule

No row marked `SYNTHETIC_PASS` is a live database or production result. `HOLD`, `NOT VERIFIED` and `MOCK_READY` remain visible until the stated dependency, authority or Product decision is resolved.
