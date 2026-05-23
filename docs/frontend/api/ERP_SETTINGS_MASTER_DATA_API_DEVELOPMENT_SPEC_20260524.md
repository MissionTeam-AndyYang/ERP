# ERP Settings / Master Data API Development Spec

Date: 2026-05-24
Route: `/settings`
Purpose: Define read-only APIs for Settings / Master Data V1.

## 1. V1 Goal

Settings / Master Data V1 governs users, permissions, company data, item/material/product/BOM master data, integrations and localization readiness.

## 2. Aggregation API

### `GET /api/v1/settings/dashboard`

```json
{
  "summary": {
    "masterDataIssueCount": 0,
    "permissionRoleCount": 0,
    "integrationIssueCount": 0,
    "localizationCoverageRate": 0
  },
  "masterDataHealth": [],
  "permissionRoles": [],
  "integrationStatus": [],
  "localizationStatus": []
}
```

## 3. Detail APIs

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/settings/master-data-health` | Master data completeness and duplicate warnings |
| `GET /api/v1/settings/permissions` | Roles, modules and permission matrix |
| `GET /api/v1/settings/integrations` | Integration status |
| `GET /api/v1/settings/localization` | Language coverage status |
| `GET /api/v1/settings/audit` | Configuration change audit summary |

## 4. Dataset Structures

### `masterDataHealth[]`

```json
{
  "domain": "items",
  "recordCount": 0,
  "missingRequiredFieldCount": 0,
  "duplicateCount": 0,
  "lastUpdatedAt": "2026-05-24T08:00:00Z",
  "riskLevel": "normal"
}
```

### `permissionRoles[]`

```json
{
  "roleId": "",
  "roleName": "Warehouse Manager",
  "modulePermissions": [
    {
      "module": "warehouse",
      "canRead": true,
      "canWrite": false,
      "canApprove": false
    }
  ]
}
```

## 5. Existing API Candidates

- `/api/v1/user/login`
- `/api/v1/company`
- `/api/v1/enterprise`
- `/api/v1/product`
- `/api/v1/goods`
- `/api/v1/material`
- `/api/v1/bom`
- `/api/v1/bankaccount`
- `/api/v1/device`

## 6. Proposed New APIs

Permission role and localization endpoints were not obvious in the observed backend route list. Recommended:

- `/api/v1/settings/permissions`
- `/api/v1/settings/localization`
- `/api/v1/settings/integrations`
- `/api/v1/settings/audit`

## 7. Engineer Confirmation Required

1. Are roles and permissions already stored in the database?
2. Does user login return role/module permission data?
3. Where should localization coverage be stored?
4. Which master data domains are mandatory for V1 integration?
