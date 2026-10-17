# CF-01 Document Identity and Lifecycle Record

> Reusable record template. This is not a Repository Knowledge Index entry.

## Identity

| Field | Value |
| --- | --- |
| Document ID | `ERP2-<scope>-<type>-<YYYYMMDD>-<sequence>` |
| Title | `<human-readable title>` |
| Document type | `<BASELINE / DECISION / TRACEABILITY / SPECIFICATION / REVIEW / RELAY / VALIDATION / WORKING_MECHANISM>` |
| Scope | `<module, sprint, or cross-module scope>` |
| Version | `<vN>` |
| Status | `<DRAFT / IN_REVIEW / ACTIVE_BOUNDED / HOLD / SUPERSEDED / RETIRED>` |
| Owner | `<accountable role or named owner>` |
| Reviewer | `<review role or named reviewer>` |
| Authoritative source | `<directive, decision, contract, or approved record>` |
| Source path | `<repository-relative path>` |
| Last updated | `<YYYY-MM-DD>` |
| Classification | `<SOURCE / SYNTHETIC / RELAY / EVIDENCE>` |
| Canonical retrieval reference | `<existing reference or PENDING_REPOSITORY_OFFICE_READBACK>` |

## Lifecycle record

| Event | From | To | Authority / reason | Date | Reviewer / custody |
| --- | --- | --- | --- | --- | --- |
| `<created / submitted / approved-bounded / held / superseded / retired>` | `<state>` | `<state>` | `<reason and supporting source>` | `<YYYY-MM-DD>` | `<role; commit if known>` |

## Content change summary

- Change reason: `<why this version changed>`
- Impact record: `<CF-01 impact record ID or NONE>`
- Replacement/supersession: `<document ID or NONE>`
- Known limitations: `<live, approval, dependency, custody, or scope limits>`
