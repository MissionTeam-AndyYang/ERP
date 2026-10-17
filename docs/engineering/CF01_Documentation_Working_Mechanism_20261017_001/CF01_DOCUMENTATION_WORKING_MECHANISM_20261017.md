# CF-01 Documentation Working Mechanism

Mechanism ID: `ERP2-CF01-DOC-WORKING-MECHANISM-20261017-001`
Owner: CF-01 technical executor, subject to parent review
Repository scope: shared ERP2.0 documentation control for FM-01, FM-02 and future modules; demonstrated in `FM02_C2_Implementation_20261013_001`
Created: 2026-10-17
Status: `DRAFT_FOR_PARENT_REVIEW`

## 1. Purpose and non-duplication rule

CF-01 gives a module team a small, repeatable way to create, relate, and synchronize documentation across sprints and modules. It is a working mechanism, not a new knowledge repository. The authoritative Repository Knowledge Index remains the existing canonical record referenced by `docs/fm02/FM02_SPRINT01_REPOSITORY_KNOWLEDGE_REGISTRATION_RELAY_20261016_105A.md`:

`Canonical_ERP2.0_Monorepo/01_Foundation/repository_knowledge/Repository-Knowledge-Index-20261010-001.md`

When a document is ready for canonical registration, create or update a relay record that points to the canonical index. Do not create a second index, invent a local retrieval URI, or treat a relay as proof that the Repository Office has completed registration.

## 2. Document identity and lifecycle

Every controlled document receives one stable identity before review. The identity is independent of its filename and remains stable across revisions.

Required identity fields:

| Field | Rule |
| --- | --- |
| `document_id` | Globally unique, immutable identifier; recommended form `ERP2-<module-or-cross-module>-<type>-<YYYYMMDD>-<sequence>` |
| `title` | Human-readable title that states the subject and scope |
| `document_type` | One of `BASELINE`, `DECISION`, `TRACEABILITY`, `SPECIFICATION`, `REVIEW`, `RELAY`, `VALIDATION`, or `WORKING_MECHANISM` |
| `scope` | Sprint, module, cross-module concern, or explicit combination |
| `version` | Content revision, independent of the identity |
| `status` | One lifecycle value from the controlled vocabulary below |
| `owner` / `reviewer` | Named accountable roles; do not infer appointment from a source filename |
| `authoritative_source` | Decision, directive, contract, or approved record that supports the content |
| `source_path` | Repository-relative path of the working document |
| `last_updated` | ISO date of the content update |
| `classification` | For example `SOURCE`, `SYNTHETIC`, `RELAY`, or `EVIDENCE`; do not conflate this with approval |
| `canonical_retrieval_reference` | Existing Repository Knowledge retrieval reference, or `PENDING_REPOSITORY_OFFICE_READBACK` |

Controlled lifecycle:

`DRAFT` → `IN_REVIEW` → `ACTIVE_BOUNDED` → `SUPERSEDED` → `RETIRED`

`HOLD` may be entered from `DRAFT`, `IN_REVIEW`, or `ACTIVE_BOUNDED` when a required decision, source, or dependency is unavailable. A held document returns to the prior working state only after the missing condition is recorded. `ACTIVE_BOUNDED` means usable for the stated scope; it does not mean globally approved or live-accepted.

Lifecycle controls:

- A revision changes `version`, `last_updated`, and the change summary; it does not silently change `document_id`.
- A change to authoritative meaning requires a new review record and an impact scan before the document can return to `ACTIVE_BOUNDED`.
- A superseded document remains discoverable through its identity and replacement reference.
- A relay can record `PENDING_REPOSITORY_OFFICE_READBACK`; it cannot self-issue a canonical retrieval reference.

## 3. Cross-sprint and cross-module traceability

Traceability is a relationship record, not a duplicate of the source document. Each row should connect one decision or requirement to its source, document section, impacted module/sprint, trigger, and verification route.

Minimum row fields:

| Field | Meaning |
| --- | --- |
| `trace_id` | Stable row identity, e.g. `ERP2-TRACE-B02-001` |
| `source_record` | Existing authoritative record and exact section/row |
| `decision_or_requirement` | B01–B06, FR-01–FR-20, or another approved identifier |
| `boundary_or_expected_behavior` | Short normalized statement; preserve deferred conditions |
| `origin_sprint` / `target_sprint` | Where the decision originated and where it may affect work |
| `producer_module` / `consumer_modules` | Owning and consuming modules; use explicit module IDs |
| `mandatory_trigger` | Event that permits design or implementation expansion |
| `impacted_artifacts` | Documents, schemas, APIs, UI, tests, or evidence that require review |
| `status` | `CONFIRMED`, `DECIDED`, `CONTROLLED_DEFERRED`, `IMPLEMENTED_BOUNDED`, `HOLD`, or `NOT_AUTHORIZED` |
| `verification_route` | Offline source review, deterministic validation, test, approval, or live acceptance |
| `custody` | Local path, commit if known, and Repository Knowledge retrieval state |

For the existing FM-02 baseline, the source-of-truth inputs are:

- `docs/fm02/FM02_SPRINT01_TRACEABILITY_MATRIX_20261016.md` for the B01–B06 and FR-01–FR-20 rows;
- `docs/fm02/FM02_SPRINT01_DOCUMENT_COMPLETION_MATRIX_20261016_104.md` for document-to-decision coverage; and
- `docs/fm02/FM02_SPRINT01_REPOSITORY_KNOWLEDGE_REGISTRATION_RELAY_20261016_105A.md` for canonical-index custody and readback limits.

Do not copy those tables into this mechanism. Link to the exact path and row/section instead.

## 4. Change-impact synchronization

Use the following sequence whenever an authoritative decision, requirement, contract, or lifecycle status changes.

1. **Capture** — Create a change-impact record using the template in `templates/CF01_CHANGE_IMPACT_SYNC_TEMPLATE.md`. Record the changed source identity, old/new status, reason, and decision authority.
2. **Resolve** — Follow the traceability links to every affected sprint, module, document, API/schema/UI/test concern, and Repository Knowledge relay.
3. **Classify** — Mark each affected item `UPDATE_REQUIRED`, `REVIEW_ONLY`, `NO_IMPACT_RECORDED`, or `BLOCKED`. A deferred decision remains deferred; it is not converted to approval by synchronization.
4. **Synchronize** — Update only the owning document in its authorized path. Update dependent records in the same change set or record an explicit hold with an owner and trigger. Keep source, synthetic, relay, and live evidence classifications distinct.
5. **Validate** — Run deterministic offline checks where available. Confirm that B01–B06 and FR references still resolve, that no forbidden implementation was introduced, and that the Repository Knowledge reference still points to the existing canonical index.
6. **Review and custody** — Record reviewer, date, source path, version, and local Git custody. If canonical registration is needed, send a relay/update to the Repository Office; do not modify or replace the canonical index from this nested repository.

Synchronization completion requires all impacted rows to have a disposition. “No impact” is a recorded conclusion, not an omitted row.

## 5. Read-only B02 demonstration

B02 is used because it crosses Item Master, Product/SKU, Product Structure, schema, API, UI, and test planning while intentionally keeping the relationship model deferred. The demonstration in `demonstrations/CF01_B02_READ_ONLY_DEMONSTRATION_20261017.md` reads the existing source row, confirms FR-13’s dependency treatment, and verifies the D03/D05/D06 completion references. It makes no database call and writes no source or document.

Run from the repository root:

```text
python docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/validate_cf01_b02.py
```

Expected outcome: `CF01_VALIDATION=PASS`. The result proves only deterministic offline source coverage and the B02 boundary; it does not prove Product/SKU approval, live API/UI behavior, database state, or Repository Office readback.

## 6. Review handoff

Parent review should decide whether to accept this mechanism as a reusable CF-01 pattern, whether the identifier vocabulary fits cross-module governance, and whether a future central operating model should publish the templates. This delivery intentionally leaves existing FM-02 records and application behavior unchanged.
