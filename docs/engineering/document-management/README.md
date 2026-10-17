# CF-01 Documentation Working Mechanism

Mechanism ID: `ERP2-CF01-DOC-WORKING-MECHANISM-20261017-001`
Directive: `ERP2.0-CIO-GOV-CROSS-MODULE-FOUNDATION-EXECUTION-20261017-109`
Scope: shared documentation control and cross-module working records for FM-01, FM-02 and future modules
Status: `DRAFT_FOR_PARENT_REVIEW`

This directory is a reusable, documentation-only working mechanism. It provides:

1. document identity and lifecycle fields;
2. cross-sprint and cross-module traceability fields;
3. a change-impact synchronization procedure;
4. a read-only B02 demonstration using the existing FM-02 B01–B06 and FR records; and
5. a deterministic offline validator with no database, credential, network, package, or application-code dependency.

The mechanism deliberately does not create a local Repository Knowledge Index. Canonical registration remains with the existing Repository Knowledge Index named in the FM-02 repository relay:

`Canonical_ERP2.0_Monorepo/01_Foundation/repository_knowledge/Repository-Knowledge-Index-20261010-001.md`

The existing FM-02 records are inputs, not copies. The validator reads them in place and never edits them.

## Contents

| Path | Purpose |
| --- | --- |
| `CF01_DOCUMENTATION_WORKING_MECHANISM_20261017.md` | Operating rules and end-to-end workflow |
| `templates/CF01_DOCUMENT_IDENTITY_LIFECYCLE_TEMPLATE.md` | Reusable document identity and lifecycle record |
| `templates/CF01_CROSS_MODULE_TRACEABILITY_TEMPLATE.md` | Reusable decision/requirement/module traceability record |
| `templates/CF01_CHANGE_IMPACT_SYNC_TEMPLATE.md` | Reusable change-impact and synchronization record |
| `demonstrations/CF01_B02_READ_ONLY_DEMONSTRATION_20261017.md` | Human-readable B02 demonstration and expected result |
| `validate_cf01_b02.py` | Standard-library-only deterministic validator |

## Run the offline validation

From the FM-02 repository root:

```text
python docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/validate_cf01_b02.py
```

The command reads only the existing FM-02 documentation records and exits non-zero if the required B02 boundary, B01–B06 coverage, FR-01–FR-20 coverage, or canonical-index reuse reference is missing.

## Boundaries

- No live database, credentials, external service, or network access is required or attempted.
- No source, application code, package manifest, evidence file, `docs/fm02` file, or existing engineering convention is edited by this mechanism.
- A `PASS` from the validator means source-document coverage and boundary text were found offline; it is not business approval, live runtime acceptance, Repository Office readback, or Sprint 2 authorization.
