# CF-01 Change-Impact Synchronization Record

> Reusable change-control working record. Use one record per authoritative change event.

## Change identity

| Field | Value |
| --- | --- |
| Change record ID | `ERP2-IMPACT-<source-id>-<YYYYMMDD>-<sequence>` |
| Changed source document ID | `<stable ID>` |
| Changed source path / section | `<repository-relative path> §<section> / row>` |
| Change authority | `<directive, decision, contract, or approved review>` |
| Change date | `<YYYY-MM-DD>` |
| Previous version/status | `<value>` |
| New version/status | `<value>` |
| Change summary | `<concise meaning-level change>` |

## Impact disposition

| Impacted record / module | Relationship | Required action | Disposition | Owner | Due/trigger | Validation route |
| --- | --- | --- | --- | --- | --- | --- |
| `<document or module>` | `<producer/consumer/dependency>` | `<update, review, or no change>` | `<UPDATE_REQUIRED / REVIEW_ONLY / NO_IMPACT_RECORDED / BLOCKED>` | `<role>` | `<date or trigger>` | `<offline check/test/approval/live>` |

## Synchronization completion

- All trace links resolved: `<yes/no>`
- B01–B06 / FR references rechecked where relevant: `<yes/no/not applicable>`
- Source and dependent records synchronized or explicitly held: `<yes/no>`
- Repository Knowledge relay required: `<yes/no>`
- Canonical-index readback received: `<yes/no/pending>`
- Forbidden expansion introduced: `<no / describe and block>`
- Reviewer and date: `<role, YYYY-MM-DD>`
- Limitations: `<scope, live-system, approval, dependency, or custody limits>`
