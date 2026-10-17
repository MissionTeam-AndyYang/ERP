# CF-01 B02 Read-Only Demonstration

Demonstration ID: `ERP2-CF01-B02-READONLY-20261017-001`
Status: `OFFLINE_DETERMINISTIC`

## Objective

Show that the CF-01 mechanism can resolve one cross-module boundary from the existing FM-02 records without creating a local index, changing FM-02 documentation, contacting a live service, or inferring Product/SKU approval.

## Source records used in place

| Role | Existing path | Expected source content |
| --- | --- | --- |
| Decision/requirement matrix | `docs/fm02/FM02_SPRINT01_TRACEABILITY_MATRIX_20261016.md` | B02 row and FR-13 row are present; Product/SKU relationship remains a controlled dependency |
| Document completion matrix | `docs/fm02/FM02_SPRINT01_DOCUMENT_COMPLETION_MATRIX_20261016_104.md` | D01, D02, D03, D05, D06, and D09 identify B02 impact and preserve the deferred boundary |
| Repository Knowledge relay | `docs/fm02/FM02_SPRINT01_REPOSITORY_KNOWLEDGE_REGISTRATION_RELAY_20261016_105A.md` | The existing canonical Repository Knowledge Index is named; the relay is not a competing index and readback remains distinct |

## Demonstrated trace record

| Field | Resolved value |
| --- | --- |
| Trace ID | `ERP2-TRACE-B02-001` |
| Boundary | Item is separate from Product/SKU; cardinality and Product Structure source of truth must be decided before relationship/schema work |
| Origin / affected scope | FM-02 Sprint 1 → Product Structure / SR-1 and future dependent design work |
| Impacted artifacts | D01, D02, D03, D05, D06, D09; Product/SKU schema/API/UI remain unauthorized under the cited boundary |
| Status | `BOUNDARY_CONFIRMED` with `CONTROLLED_DEFERRED` relationship model |
| Verification | Offline text coverage and exact boundary/status assertions |
| Repository Knowledge custody | Reuse existing canonical index reference; no local index created |

## Run

From the FM-02 repository root:

```text
python docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/validate_cf01_b02.py
```

Expected result:

```text
CF01_VALIDATION=PASS
B02_BOUNDARY=PASS
B01_B06_COVERAGE=6/6
FR_COVERAGE=20/20
REPOSITORY_KNOWLEDGE_REUSE=PASS
READ_ONLY_SCOPE=PASS
```

## Interpretation and limitations

This demonstration proves only that the existing source documents contain the expected offline boundary and coverage. It does not approve the Product/SKU relationship, create schema/API/UI behavior, test a live database, validate external Repository Office readback, or authorize Sprint 2 work.
