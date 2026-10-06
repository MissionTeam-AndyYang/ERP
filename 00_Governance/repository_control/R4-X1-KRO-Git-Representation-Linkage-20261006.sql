START TRANSACTION;

-- Pure representation/storage linkage. KnowledgeItem and KnowledgeVersion identities remain unchanged.
INSERT INTO knowledge_storage (knowledge_representation_id,storage_type,location,stored_at)
SELECT x.representation_id,'GitRepresentation',x.location,UTC_TIMESTAMP(6)
FROM (
  SELECT 96 representation_id,'file:///C:/Users/andyy/Desktop/Codex-workspace/projects/ERP%202.0%20Phase1/Canonical_ERP2.0_Monorepo/01_Foundation/standards/ERP2.0-M0-A3-T1-Consolidated-Technical-Standards-Package-20261005-001.md' location
  UNION ALL SELECT 97,'file:///C:/Users/andyy/Desktop/Codex-workspace/projects/ERP%202.0%20Phase1/Canonical_ERP2.0_Monorepo/01_Foundation/standards/M0-A3-T1-Standards-Manifest-20261005-001.json'
  UNION ALL SELECT 101,'file:///C:/Users/andyy/Desktop/Codex-workspace/projects/ERP%202.0%20Phase1/Canonical_ERP2.0_Monorepo/01_Foundation/standards/ERP2-STD-MDP-001-Module-Development-Pack-Standard-20261005-001.md'
  UNION ALL SELECT 105,'file:///C:/Users/andyy/Desktop/Codex-workspace/projects/ERP%202.0%20Phase1/Canonical_ERP2.0_Monorepo/01_Foundation/standards/ERP2-STD-KRO-001-Technical-Versioning-Supersession-and-KRO-Custody-Standard-20261005-001.md'
  UNION ALL SELECT 106,'file:///C:/Users/andyy/Desktop/Codex-workspace/projects/ERP%202.0%20Phase1/Canonical_ERP2.0_Monorepo/01_Foundation/repository_knowledge/ERP2.0-M0-A4-Enterprise-Foundation-Baseline-Freeze-Package-20261005-001.md'
  UNION ALL SELECT 107,'file:///C:/Users/andyy/Desktop/Codex-workspace/projects/ERP%202.0%20Phase1/Canonical_ERP2.0_Monorepo/01_Foundation/repository_knowledge/M0-A4-Freeze-Package-Manifest-20261005-001.json'
  UNION ALL SELECT 108,'file:///C:/Users/andyy/Desktop/Codex-workspace/projects/ERP%202.0%20Phase1/Canonical_ERP2.0_Monorepo/02_Programs/ERP2.0_Functional_Mainline/roadmap/ERP2.0-M0-A5-R1-Corrected-Roadmap-Freeze-Candidate-20261005-001.md'
  UNION ALL SELECT 109,'file:///C:/Users/andyy/Desktop/Codex-workspace/projects/ERP%202.0%20Phase1/Canonical_ERP2.0_Monorepo/02_Programs/ERP2.0_Functional_Mainline/evidence/M0-A5-R1-Corrected-Roadmap-Evidence-Manifest-20261005-001.json'
  UNION ALL SELECT 110,'file:///C:/Users/andyy/Desktop/Codex-workspace/projects/ERP%202.0%20Phase1/Canonical_ERP2.0_Monorepo/00_Governance/operating_model/current/ERP2.0-M0-A6-P0-Functional-Program-Kickoff-and-Engineering-Readiness-Baseline-20261006-001.md'
  UNION ALL SELECT 111,'file:///C:/Users/andyy/Desktop/Codex-workspace/projects/ERP%202.0%20Phase1/Canonical_ERP2.0_Monorepo/00_Governance/operating_model/current/ERP2.0-M0-A6-P0-Evidence-Manifest-20261006-001.json'
) x
WHERE NOT EXISTS (SELECT 1 FROM knowledge_storage s WHERE s.knowledge_representation_id=x.representation_id AND s.location=x.location);

COMMIT;
