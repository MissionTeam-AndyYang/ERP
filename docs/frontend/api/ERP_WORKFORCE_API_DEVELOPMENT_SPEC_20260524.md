# ERP Workforce API Development Spec

Date: 2026-05-24
Route: `/workforce`
Purpose: Define read-only APIs for Workforce V1.

## 1. V1 Goal

Workforce V1 shows shift coverage, staff skill/certification readiness, overtime/support plans and labor risk against scheduled production.

## 2. Aggregation API

### `GET /api/v1/workforce/dashboard`

```json
{
  "summary": {
    "shiftCoverageRate": 0,
    "skillGapCount": 0,
    "certificationRiskCount": 0,
    "overtimeHours": 0,
    "supportNeededCount": 0
  },
  "shiftCoverage": [],
  "skillGaps": [],
  "certificationRisks": [],
  "overtimePlans": [],
  "lineStaffReadiness": []
}
```

## 3. Detail APIs

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/workforce/shifts` | Shift coverage |
| `GET /api/v1/workforce/skills` | Skill readiness |
| `GET /api/v1/workforce/certifications` | Certification and training risk |
| `GET /api/v1/workforce/line-readiness` | Staff readiness by production line |

## 4. Dataset Structures

### `lineStaffReadiness[]`

```json
{
  "date": "2026-05-24",
  "lineId": "",
  "lineName": "",
  "requiredHeadcount": 0,
  "assignedHeadcount": 0,
  "requiredSkills": [],
  "missingSkills": [],
  "status": "ready",
  "riskLevel": "normal"
}
```

### `certificationRisks[]`

```json
{
  "employeeId": "",
  "employeeName": "",
  "certificationName": "",
  "expiresAt": "2026-06-30",
  "affectsLine": "",
  "riskLevel": "warning"
}
```

## 5. Existing API Candidates

- `/api/v1/work/assignment`
- `/api/v1/plstatistics/mancapacity`
- `/api/v1/productline/station`
- `/api/v1/productline/process`

## 6. Proposed New APIs

Dedicated employee/skill/certification endpoints were not observed. Recommended:

- `/api/v1/workforce/shifts`
- `/api/v1/workforce/skills`
- `/api/v1/workforce/certifications`

## 7. Engineer Confirmation Required

1. Does the current DB include employee, skill and certification tables?
2. Can work assignment represent planned staff by line/date?
3. How should staff gaps be calculated for Planning / APS and Production?
4. Which workforce data is V1 read-only and which needs later mutation?
