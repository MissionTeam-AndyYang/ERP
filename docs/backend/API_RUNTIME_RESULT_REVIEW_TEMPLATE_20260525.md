# API Runtime Result Review Template

Date: 2026-05-25
Purpose: Provide a repeatable review format for engineer-submitted runtime verification output.

## Review Metadata

| Field | Value |
| --- | --- |
| Review date |  |
| Reviewer |  |
| Engineer report path | `docs/backend/runtime-verification/` |
| Module |  |
| Endpoint |  |
| Commit / branch |  |
| Backend base URL |  |
| Database baseline | `EWDB_20260526.sql` |
| Workflow baseline | `EWDB_20260522_WORKFLOW.md` |

## Contract Check

| Check | Result | Notes |
| --- | --- | --- |
| Endpoint path matches frontend service |  |  |
| HTTP status is 2xx |  |  |
| Response is valid JSON |  |  |
| Response wrapper is supported |  | Direct object or `{ data: ... }`. |
| Required top-level datasets exist |  | Compare with `scripts/verify_v1_api_contracts.py`. |
| Dataset names match frontend runtime contract |  |  |
| No secret values in report |  | DB credentials, tokens, customer/supplier confidential values. |
| Error messages are reviewable |  | No opaque stack trace as only evidence. |

## Dataset Review

| Dataset | Present | Shape acceptable | Business meaning acceptable | Notes |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

## Module-Specific Business Checks

| Check | Result | Notes |
| --- | --- | --- |
| Primary V1 management concern is represented |  |  |
| Risk/warning statuses can be mapped to UI tones |  |  |
| Date/time fields are understandable |  | Include timezone or local-date assumption if relevant. |
| Numeric fields include unit or implied unit |  |  |
| Cross-module references are present where needed |  | Order no, work order no, batch no, item no, warehouse/location. |
| Missing data has a clear null/empty convention |  |  |

## Frontend Integration Decision

| Decision | Meaning |
| --- | --- |
| `accept` | Contract is sufficient for frontend integration. |
| `accept_with_notes` | Frontend can integrate, but tracker should document limitation. |
| `revise_backend` | Backend must change response before integration. |
| `revise_frontend_contract` | Frontend/document contract should change because backend source-of-truth is better. |
| `blocked` | Missing schema/data/workflow decision prevents acceptance. |

Decision:

```txt

```

## Follow-Up Items

| Owner | Item | Priority | Due / trigger |
| --- | --- | --- | --- |
|  |  |  |  |
