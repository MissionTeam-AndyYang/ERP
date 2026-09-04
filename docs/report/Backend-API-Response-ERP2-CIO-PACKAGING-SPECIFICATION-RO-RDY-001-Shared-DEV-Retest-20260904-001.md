# Backend API Response - ERP2-CIO-PACKAGING-SPECIFICATION-RO-RDY-001 Shared DEV Runtime Retest

## Runtime Identity

| Field | Value |
| --- | --- |
| Classification | PASS WITH FIXTURE LIMITATION - SHARED DEV DB-BACKED PACKAGING SPECIFICATION RETEST COMPLETED |
| Endpoint | 172.20.10.3:3307 |
| Database | erp2_shared_dev_item_transitem_np |
| Credential class | ERP2_SHARED_DEV_ITEM_TRANSITEM_NP_READONLY |
| Raw secret exposure | 0 |
| Report generated at | 2026-09-04T13:50:57Z |

## Shared DEV Fixture Limitations

- Shared DEV returned Product subject but no visible packagingSpecs for PRD-SD-001.
- Shared DEV Product packaging scenario returned module_unavailable, indicating the current Shared DEV packaging table/support surface is not fully aligned with the formal packaging_specification implementation path.

## Route Evidence

| Evidence | Result | Detail |
| --- | --- | --- |
| Product packaging scenario | PASS | HTTP 200, specCount=0, warnings=['module_unavailable'] |
| WIP packaging scenario | PASS | HTTP 200, specCount=0, warnings=['missing_packaging_spec'] |
| Not found | PASS | HTTP 404, code=1, message=record not found |
| Invalid category | PASS | HTTP 400, code=3001, message=invalid itemCategory |
| Module unavailable/error handling | PASS | HTTP 200, warnings=['module_unavailable'] |
| Read-only negative control | PASS | POST returned HTTP 405 |
| Source-lineage/warning propagation | PASS | sourceLineage={'subjectSourceCode': 'product', 'packagingSpecSourceCode': 'not_recorded', 'packagingBomMasterSourceCode': 'bom2_number', 'packagingBomLineSourceCode': 'bom2'}, warnings=['module_unavailable'] |

## Payload Summaries

```json
{
  "productScenario": {
    "httpStatus": 200,
    "code": 0,
    "message": "success",
    "elapsedMs": 189.96,
    "subject": {
      "itemNo": "PRD-SD-001",
      "itemName": "Shared DEV Product Fixture A",
      "itemCategory": 5,
      "itemSubCategory": 1,
      "productVersion": 1,
      "unitShipping": 101,
      "unitWarehouse": 101,
      "unitProduct": 101,
      "comment": "Synthetic formal-compatible Shared DEV fixture only",
      "sourceCode": "product"
    },
    "summary": {
      "packagingSpecCount": 0,
      "packagingBomCount": 0,
      "packageLevelCount": 0,
      "materialLineCount": 0,
      "totalCount": 0,
      "totalWeight": 0.0
    },
    "moduleReadiness": [
      {
        "moduleCode": "packagingSpecification",
        "statusCode": "error",
        "sourceCode": "not_recorded",
        "warningCodes": [
          "module_unavailable"
        ]
      }
    ],
    "sourceLineage": {
      "subjectSourceCode": "product",
      "packagingSpecSourceCode": "not_recorded",
      "packagingBomMasterSourceCode": "bom2_number",
      "packagingBomLineSourceCode": "bom2"
    },
    "warningCodes": [
      "module_unavailable"
    ],
    "capabilityBoundary": {
      "readOnly": true,
      "packagingWriteSupported": false,
      "packagingApprovalSupported": false,
      "packagingReleaseSupported": false,
      "sourceOfTruthTransitionSupported": false,
      "cutoverSupported": false,
      "goLiveSupported": false
    },
    "packagingSpecCount": 0
  },
  "wipScenario": {
    "httpStatus": 200,
    "code": 0,
    "message": "success",
    "elapsedMs": 5.63,
    "subject": {
      "itemNo": "INP-SD-001",
      "itemName": "Shared DEV Inproduct Fixture A",
      "itemCategory": 4,
      "itemSubCategory": 1,
      "productVersion": 0,
      "unitShipping": 101,
      "unitWarehouse": 101,
      "unitProduct": 101,
      "comment": "Synthetic formal-compatible Shared DEV fixture only",
      "sourceCode": "inproduct"
    },
    "summary": {
      "packagingSpecCount": 0,
      "packagingBomCount": 0,
      "packageLevelCount": 0,
      "materialLineCount": 0,
      "totalCount": 0,
      "totalWeight": 0.0
    },
    "moduleReadiness": [
      {
        "moduleCode": "packagingSpecification",
        "statusCode": "unavailable",
        "sourceCode": "not_recorded",
        "warningCodes": [
          "missing_packaging_spec"
        ]
      }
    ],
    "sourceLineage": {
      "subjectSourceCode": "inproduct",
      "packagingSpecSourceCode": "not_recorded",
      "packagingBomMasterSourceCode": "bom2_number",
      "packagingBomLineSourceCode": "bom2"
    },
    "warningCodes": [
      "missing_packaging_spec"
    ],
    "capabilityBoundary": {
      "readOnly": true,
      "packagingWriteSupported": false,
      "packagingApprovalSupported": false,
      "packagingReleaseSupported": false,
      "sourceOfTruthTransitionSupported": false,
      "cutoverSupported": false,
      "goLiveSupported": false
    },
    "packagingSpecCount": 0
  },
  "notFound": {
    "httpStatus": 404,
    "code": 1,
    "message": "record not found"
  },
  "invalidCategory": {
    "httpStatus": 400,
    "code": 3001,
    "message": "invalid itemCategory"
  },
  "moduleUnavailable": {
    "httpStatus": 200,
    "code": 0,
    "message": "success",
    "elapsedMs": 1.96,
    "subject": {
      "itemNo": "PRD-SD-001",
      "itemName": "Shared DEV Product Fixture A",
      "itemCategory": 5,
      "itemSubCategory": 1,
      "productVersion": 1,
      "unitShipping": 101,
      "unitWarehouse": 101,
      "unitProduct": 101,
      "comment": "Synthetic formal-compatible Shared DEV fixture only",
      "sourceCode": "product"
    },
    "summary": {
      "packagingSpecCount": 0,
      "packagingBomCount": 0,
      "packageLevelCount": 0,
      "materialLineCount": 0,
      "totalCount": 0,
      "totalWeight": 0.0
    },
    "moduleReadiness": [
      {
        "moduleCode": "packagingSpecification",
        "statusCode": "error",
        "sourceCode": "not_recorded",
        "warningCodes": [
          "module_unavailable"
        ]
      }
    ],
    "sourceLineage": {
      "subjectSourceCode": "product",
      "packagingSpecSourceCode": "not_recorded",
      "packagingBomMasterSourceCode": "bom2_number",
      "packagingBomLineSourceCode": "bom2"
    },
    "warningCodes": [
      "module_unavailable"
    ],
    "capabilityBoundary": {
      "readOnly": true,
      "packagingWriteSupported": false,
      "packagingApprovalSupported": false,
      "packagingReleaseSupported": false,
      "sourceOfTruthTransitionSupported": false,
      "cutoverSupported": false,
      "goLiveSupported": false
    },
    "packagingSpecCount": 0
  },
  "readOnlyNegativeControl": {
    "httpStatus": 405,
    "code": null,
    "message": ""
  }
}
```

## Local Full-Stack DEV Backend Requirements

Required environment variables:

```txt
DB_HOST=<local_or_shared_dev_host>
DB_PORT=<mariadb_port>
DB_NAME=<database_name>
DB_USER=<readonly_or_dev_user>
DB_PASSWORD=<password>
TOKEN_ENABLED=1
ENV=local_dev
```

Recommended first smoke path:

```txt
GET /api/v2/packaging-specification/overview?itemNo=<product_no>&itemCategory=5
GET /api/v2/packaging-specification/overview?itemNo=<wip_no>&itemCategory=4
```

## Boundary Confirmation

No material database/schema change was performed.

No Packaging write, Packaging approval/release, Product write, Production action, migration, Source-of-Truth transition, Engineering Pull, Cutover, or ERP2.0 Go-Live was performed.
