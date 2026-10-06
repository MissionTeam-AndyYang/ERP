# ERP2-STD-KRO-001 Technical Versioning, Supersession and KRO Custody Standard

Status: `FREEZE-READY_WITH_PUBLICATION_DEFERRED`

Source: `ERP2.0-M0-A3-T1-Consolidated-Technical-Standards-Package-20261005-001.md`, section 10.

## Custody Model

Every technical standard/evidence artifact uses:

`KnowledgeItem identity -> KnowledgeVersion -> KnowledgeRepresentation -> KnowledgeStorage`

Required metadata includes owner assignment, provenance, creation/review event, content hash, representation type, storage locator, effective/superseded state, and downstream freshness relationship.

## Versioning and Publication Rules

- Stable KnowledgeItem identity is not a file path or DB revision.
- Version changes retain prior versions.
- Representation is not storage.
- Source commit/release/Alembic identity is not automatically a KnowledgeVersion.
- Publication requires an explicit governance/custody event.
- Supersession creates a new version and retains lineage.
- Stale downstream context must be detected and safe-stopped.
- Runtime Work/Message/Result is not Knowledge without explicit promotion semantics.

KRO publication of these candidates remains separately governed and is not implied by the source package alone.

