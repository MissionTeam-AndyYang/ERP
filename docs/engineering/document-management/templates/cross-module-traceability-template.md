# CF-01 Cross-Module Traceability Record

> Reusable relationship template. Point to authoritative source rows; do not copy a competing index or replace the source matrix.

## Record identity

| Field | Value |
| --- | --- |
| Trace record ID | `ERP2-TRACE-<decision-or-requirement>-<sequence>` |
| Source document ID | `<stable source document ID>` |
| Source path and section/row | `<repository-relative path> §<section> / row <identifier>` |
| Created / updated | `<YYYY-MM-DD>` |
| Custody | `<local branch/commit; canonical readback state>` |

## Trace row

| Field | Value |
| --- | --- |
| Decision / requirement | `<B01–B06, FR-01–FR-20, or approved identifier>` |
| Boundary / expected behavior | `<normalized statement preserving conditions>` |
| Origin sprint | `<sprint>` |
| Target sprint(s) | `<sprint(s)>` |
| Producer module / role | `<module or owner>` |
| Consumer module(s) / role(s) | `<explicit list>` |
| Mandatory trigger | `<decision, approval, contract, or event>` |
| Impacted artifacts | `<docs, schema, API, UI, tests, evidence>` |
| Status | `<CONFIRMED / DECIDED / CONTROLLED_DEFERRED / IMPLEMENTED_BOUNDED / HOLD / NOT_AUTHORIZED>` |
| Verification route | `<offline review / deterministic check / test / approval / live acceptance>` |
| Repository Knowledge reference | `<existing canonical retrieval reference or pending readback>` |

## Disposition

- Current disposition: `<UPDATE_REQUIRED / REVIEW_ONLY / NO_IMPACT_RECORDED / BLOCKED>`
- Dependent record owners notified: `<yes/no; record or reason>`
- Next trigger: `<event or NONE>`
- Notes and limits: `<no approval, live, or implementation claim unless independently evidenced>`
