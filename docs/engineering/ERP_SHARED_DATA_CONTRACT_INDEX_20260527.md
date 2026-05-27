# ERP Shared Data Contract Index

Date: 2026-05-27
Purpose: Track shared DB/API/frontend data-contract documents.

## Why This Exists

ERP 2.0 development now requires a shared understanding layer between:

- DB schema field meaning.
- Restserver API GET/SET dataset meaning.
- Frontend runtime type meaning.
- Business workflow meaning.

This lets Codex and the backend engineer become backups for each other while keeping frontend and backend development aligned.

## Ownership Model

| Area | Primary owner | Backup / reviewer |
| --- | --- | --- |
| Frontend pages, UX, service integration | Codex | Backend engineer reviews API impact |
| Restserver implementation | Backend engineer | Codex reviews code, API contract and runtime result |
| DB field meaning | Backend engineer confirms | Codex documents and maps usage |
| Shared data contract | Codex drafts | Backend engineer confirms/updates |

## Contract Documents

| Module | Status | Document |
| --- | --- | --- |
| Warehouse | Drafted, awaiting engineer field confirmation | `docs/engineering/ERP_SHARED_DATA_CONTRACT_WAREHOUSE_20260527.md` |
| Orders | Pending | TBD |
| Production | Pending | TBD |
| Quality | Pending | TBD |
| Planning / APS | Pending | TBD |
| Purchasing | Pending | TBD |
| Logistics | Pending | TBD |
| Finance | Pending | TBD |
| Traceability | Pending | TBD |
| R&D / Costing | Pending | TBD |
| Workforce | Pending | TBD |
| Settings / Master Data | Pending | TBD |

## Standard Contract Sections

Each module contract should include:

1. Endpoint and required datasets.
2. Business terms.
3. Candidate DB source tables and fields.
4. API GET dataset field meanings.
5. API SET/mutation dataset meanings, if in scope.
6. Enum/status mapping.
7. Open questions for engineer.
8. Current agreement and implementation decision.

## Current Priority

1. Complete Warehouse field confirmation.
2. Implement `GET /api/v1/warehouse/dashboard`.
3. Use Warehouse contract as the template for Orders and Production.

