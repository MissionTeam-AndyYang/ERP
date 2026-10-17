# ERP2.0 Repository Foundation Custody Relay — Directive 120

Relay ID: `ERP2-REPOSITORY-OFFICE-FOUNDATION-CUSTODY-RELAY-20261017-120`
Decision reference: `ERP2.0-CIO-GOV-REPOSITORY-FOUNDATION-EXECUTION-CLOSURE-20261017-120`
Prepared: 2026-10-17
Status: `PREPARED / REPOSITORY OFFICE ACTION REQUIRED`

## Purpose

This is one consolidated relay for Repository Office custody and Knowledge readback of the three artifacts required by Directive 120. It does not claim that Repository Office registration, central custody or readback has occurred.

The authoritative Knowledge index remains:

`Canonical_ERP2.0_Monorepo/01_Foundation/repository_knowledge/Repository-Knowledge-Index-20261010-001.md`

The local source custody repository is:

`20_Engineering_Workspace/FM02_C2_Implementation_20261013_001/`

branch `codex/fm02-c2-isolated-20261013-001`, current local HEAD `305cfdae36397bd66ebe8aae53bbbe932c80810b`.

## A1 — CF-01 custody request

| Field | Value |
|---|---|
| Document ID | `ERP2-CF01-DOC-WORKING-MECHANISM-20261017-001` |
| Title | CF-01 Documentation Working Mechanism |
| Module/category | Shared ERP2.0 documentation control / working mechanism |
| Version/status | `v1.1 / ACTIVE_BOUNDED` |
| Source path | `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/CF01_DOCUMENTATION_WORKING_MECHANISM_20261017.md` |
| Source SHA-256 | `64180CED3A6F645692C658D1D0339450C6E82DB2A1F548D55A442B63602BB88B` |
| Proposed owner | Repository Office: custody, lifecycle, registration and maintenance; CTO: technical review; CIO Governance: cross-office policy approval |
| Requested central path | `01_Foundation/repository_knowledge/` under the existing canonical Knowledge index structure; exact Repository Office path to be confirmed |
| Existing Knowledge ID | `ERP2-KNOWLEDGE:ERP2-CF01-DOC-WORKING-MECHANISM-20261017-001` |
| Existing index state | Older entry is present with v1 metadata and old primary hash `19D700832FE4A1505558A152E082C4327D8F6AF52EF6A22DEB2C208584DE0B0E`; v1.1 update is not read back |
| Requested action | Register v1.1, preserve v1 history, return index location and readback |

The prior v1-versus-v1.1 discrepancy is a status/version reconciliation issue, not a rule conflict. The local v1.1 source is prepared; canonical custody remains unverified.

## A2 — Cross-module Coding Convention custody request

| Field | Value |
|---|---|
| Document ID | `ERP2-ENGINEERING-CROSS-MODULE-CODING-CONVENTION-20261016-001` |
| Source path | `docs/engineering/CROSS_MODULE_CODING_CONVENTION_20261016.md` |
| Version/SHA-256 | `v1 / 85F55A3E8F181893CCCAB1E60F20F70CCF7B9ACE919AEEF71B21FF9AD2B60824` |
| Scope | FM-01, FM-02 and future ERP2.0 modules |
| CTO decision | `CTO_TECHNICAL_APPROVAL=APPROVED` |
| Proposed custody | Repository Office, at the central shared-standard path to be confirmed |
| Normative status | `PROPOSED`; technical approval is not universal CIO policy approval |
| Existing Knowledge ID | `ERP2-KNOWLEDGE:ERP2-ENGINEERING-CROSS-MODULE-CODING-CONVENTION-20261016-001` |
| Existing index state | `PROPOSED`; current index does not read back the technical approval record or a central custody path |
| Requested action | Register the exact v1 source and technical approval record; return central path/version and readback |

No substantive clause requiring correction was identified. The remaining issue is custody and normative approval, not technical content.

## A3 — FM-02 admission manifest registration request

| Field | Value |
|---|---|
| Artifact | `docs/engineering/FM02_CANONICAL_SOURCE_ADMISSION_MANIFEST_20261017.md` |
| SHA-256 | `80A02D27513EEC8BEE62F22AF7B5BDFAEDB962E0F0264ADAFF289008805A7C7B` |
| Status | `PREPARED / NOT AUTHORIZED FOR REMOTE WRITE` |
| Purpose | Planning/source-admission evidence; not a canonical Product admission and not a Sprint 2 authorization |
| Source anchor | Historical candidate anchored to source commit `701b265a1ae5b8d9618bf9df8f539ae6d14f5028`; current local preparation HEAD is `305cfdae36397bd66ebe8aae53bbbe932c80810b` |
| Requested action | Register as planning evidence, preserve its hash, and return index location/readback |

The manifest excludes the pre-existing untracked `evidence/` directory and does not authorize merge, push or remote synchronization.

## Requested Repository Office readback

Return one readback containing the registered index location, document IDs, version/status, owner/reviewer, source path, Git commit, approval reference and last-updated date for A1–A3. If a registration or readback capability is unavailable, return that exact limitation rather than treating this relay as registration.

## Current relay verdict

`CF01_CUSTODY=HOLD`

`CODING_CONVENTION_CUSTODY=HOLD`

`CODING_CONVENTION_NORMATIVE_STATUS=PROPOSED`

`ADMISSION_MANIFEST_REGISTRATION=HOLD`

`KNOWLEDGE_READBACK=HOLD`

Reason: no direct Repository Office write/readback route is available in this execution context, and the canonical index does not yet contain the current A1–A3 registration evidence.
