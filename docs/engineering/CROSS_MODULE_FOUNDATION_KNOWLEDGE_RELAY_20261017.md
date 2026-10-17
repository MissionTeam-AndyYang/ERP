# Cross-Module Foundation Repository Knowledge Relay

Relay ID: `ERP2-CROSS-MODULE-FOUNDATION-KNOWLEDGE-RELAY-20261017-109`
Directive: `ERP2.0-CIO-GOV-CROSS-MODULE-FOUNDATION-EXECUTION-20261017-109`
Source branch: `codex/fm02-c2-isolated-20261013-001`

## Purpose

This single relay requests Repository Office registration/update for the new CF-01 and CF-02 artifacts using the existing canonical Repository Knowledge Index. It does not create a second index, issue retrieval references, or claim approval.

Canonical index to reuse:

`Canonical_ERP2.0_Monorepo/01_Foundation/repository_knowledge/Repository-Knowledge-Index-20261010-001.md`

## Records requested

| Proposed record | Title | Source path | Classification | Requested status |
| --- | --- | --- | --- | --- |
| `ERP2-CF01-DOC-WORKING-MECHANISM-20261017-001` | CF-01 Documentation Working Mechanism | `docs/engineering/CF01_Documentation_Working_Mechanism_20261017_001/` | WORKING_MECHANISM / SHARED | ACTIVE_BOUNDED after review |
| `ERP2-CF02-ENGINEERING-FOUNDATION-20261017-001` | CF-02 Shared Engineering Foundation | `engineering_foundation/` and `docs/engineering/cf02_shared_engineering_foundation.md` | FOUNDATION / SHARED | ACTIVE_BOUNDED after review |
| `ERP2-CF02-OFFLINE-VERIFICATION-20261017-001` | CF-02 Offline Verification Report | `docs/engineering/cf02_offline_verification_20261017.md` | VALIDATION / EVIDENCE | PARTIAL — four tools unavailable |
| `ERP2-CROSS-MODULE-FOUNDATION-DELIVERY-20261017-001` | Cross-Module Foundation Delivery | `docs/engineering/CROSS_MODULE_FOUNDATION_DELIVERY_20261017.md` | REVIEW / DELIVERY | PARTIAL |

## Required readback

For every record, return the final ID/title, canonical relative path, version, owner/reviewer, status, source hash, local commit, decision reference, dependencies, last-updated date, searchable retrieval reference and any rejected/deferred field with reason.

The CF-02 quality report must retain `UNAVAILABLE` results until the isolated runtimes are actually prepared. Coding Convention approval remains separate from Repository Knowledge registration. No GitHub remote or push destination is claimed.

Current state before Repository Office action:

`KNOWLEDGE_READBACK=PENDING`

`GITHUB_PUSH=BLOCKED_REMOTE_NOT_VERIFIED`
