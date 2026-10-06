# R4-X1 Legacy-to-Target Mapping Register

This is a no-move semantic mapping. It does not authorize relocation, deletion, rename, archive, or KRO locator change.

| Current source | Target semantic area | Content class | Authority / owner | Movement eligibility | KRO coupling | Risk |
|---|---|---|---|---|---|---|
| `01_CTO_Office` | `00_Governance`, `01_Foundation`, `04_Engineering` | decisions, architecture, evidence, implementation | CTO Office | split required; no engineering move in Wave 1 | high | HIGH |
| `02_Operating_Model` | `00_Governance/operating_model/current` | active operating-model source | CTO/Program governance | low-risk representations eligible after reconciliation | references in documents | MEDIUM |
| `14_Operating_Model` | `00_Governance/operating_model/historical` | historical/source line | historical operating-model source | retain; no deletion | historical references | HIGH |
| `03_Track_C_Knowledge_Repository` | `01_Foundation/repository_knowledge` | KRO-controlled knowledge | Repository Office/KRO | Git representation only; KRO stays authoritative | direct | CRITICAL |
| `16_Program_Office` | `02_Programs/ERP2.0_Functional_Mainline` | roadmap, program, decisions, evidence | Program Office | selected accepted representations only | direct for governed records | HIGH |
| `17_Planning_Brain_V1_Baseline` | `01_Foundation/Planning_Brain_V1` | frozen knowledge baseline/archive | Repository/Planning Brain | no-move representation only | direct | HIGH |
| `20_Engineering_Workspace` | `04_Engineering` | source, tests, runtimes, evidence, tooling | Engineering/CTO | R4-D/E only; excluded from this wave | high | CRITICAL |
| `FGR1Data`, `G1P313`, `mer1_runtime` | no Git target | runtime/generated state | Engineering | DO NOT MOVE | none | CRITICAL |
| cleanup/execution/candidate roots | governance/program/engineering or legacy | mixed historical/working | owner varies | classify before any future wave | possible | HIGH |

## Wave-1 Materialized Representations

The following approved, low-risk representations are copied into the new canonical Git root without changing their legacy sources:

- M0-A6-P0 operating baseline -> `00_Governance/operating_model/current/`.
- M0-A4 Foundation custody baseline -> `01_Foundation/repository_knowledge/`.
- M0-A3 Technical Foundation Standards custody report and selected MDP/KRO standards -> `01_Foundation/standards/`.
- M0-A5 Functional Mainline Roadmap custody baseline -> `02_Programs/ERP2.0_Functional_Mainline/roadmap/`.

No engineering source, runtime data, generated output, secret, raw evidence forest, or routine dashboard was copied.
