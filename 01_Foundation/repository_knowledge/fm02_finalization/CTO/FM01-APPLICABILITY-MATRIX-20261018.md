# FM-01 Applicability Matrix — Cross-Module Delivery Standard

**Document ID:** `ERP2-CTO-FM01-APPLICABILITY-20261018-001`  
**Owner:** CTO Office V2  
**State:** `READY FOR FM-01 REVIEW / NOT AN FM-01 IMPLEMENTATION AUTHORIZATION`

| Control or artifact | FM-01 reuse | FM-01-specific confirmation required | Current status |
|---|---|---|---|
| Foundation lifecycle and stage gates | Direct reuse | Confirm FM-01 milestone/work-item IDs | READY |
| Engineering assignment and executor provenance | Direct reuse | Bind actual FM-01 Engineering Office/session before coding | REQUIRED |
| Design/schema/API/test artifact identity | Direct reuse | Map FM-01 component and requirement IDs | READY |
| Module Delivery Index | Direct reuse | Add FM-01 rows without copying FM-02 authority | READY |
| Remote Test Execution Standard | Direct reuse by reference | Identify qualified Remote Engineer and target | EXTERNAL OBLIGATION |
| Independent TEST separation | Direct reuse | Fresh FM-01 TEST assignment and verdict | REQUIRED |
| Git/Knowledge custody | Direct reuse | Verify FM-01 branch, commit/tree and index readback | REQUIRED |
| Database/migration evidence | Direct reuse | FM-01 target, revision, backup/recovery and credentials authority | NOT VERIFIED |
| Backend/API contracts | Reuse structure | Confirm FM-01 operations and OpenAPI/runtime state | MODULE-SPECIFIC |
| Frontend/UI/CSS controls | Reuse structure | Apply only after FM-01/FM-02 backend/integration gate | DEFERRED |
| Product/SKU boundary | Do not copy as scope | Obtain FM-01-specific business boundary | MODULE-SPECIFIC |
| PM lifecycle/reporting | Direct reuse | Open FM-01 PM record chain | READY |

## FM-01 entry conditions

FM-01 may not be activated from this matrix alone. Before implementation, PMO and CTO must confirm the FM-01 baseline, Engineering assignment, source workspace, design authority, test plan/cases, target and recovery boundary. Repository Office must perform a Knowledge-only retrieval of the standard, FM-02 index, approved design, source objects, API contract, test evidence and gaps before reusing the model.

External database testing, production activity, protected-main merge and release remain separately authorized decisions.

