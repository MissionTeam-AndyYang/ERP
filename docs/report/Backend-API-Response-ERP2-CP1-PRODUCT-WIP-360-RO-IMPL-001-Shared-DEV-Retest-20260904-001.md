# Backend API Response - ERP2-CP1-PRODUCT-WIP-360-RO-IMPL-001 Shared DEV Runtime Retest

## Runtime Identity

| Field | Value |
| --- | --- |
| Classification | PASS WITH FIXTURE LIMITATION - SHARED DEV DB-BACKED PRODUCT/WIP 360 RETEST COMPLETED |
| Endpoint | 172.20.10.3:3307 |
| Database | erp2_shared_dev_item_transitem_np |
| Credential class | ERP2_SHARED_DEV_ITEM_TRANSITEM_NP_READONLY |
| Raw secret exposure | 0 |
| Report generated at | 2026-09-04T11:12:27Z |

## Shared DEV Fixture Limitations

- Shared DEV fixture surface currently exposes inventory_record rows but not the inventory_item_month_statistic table required by the existing Warehouse inventory snapshot service. Product/WIP 360 correctly isolates this as warehouse module_unavailable instead of failing the whole overview response.

## Route Evidence

| Evidence | Result | Detail |
| --- | --- | --- |
| Product complete/partial | PASS | HTTP 200, modules=['item', 'transactionItem', 'warehouse', 'bom', 'recipe', 'routing'], warnings=['module_unavailable', 'test_support_only', 'resource_eligibility_not_governed', 'missing_process_master', 'missing_standard_performance', 'missing_process_master', 'missing_standard_performance'] |
| Standalone WIP partial or fixture limitation | PASS | HTTP 200, code=0, warnings=['missing_transaction_item', 'module_unavailable', 'wip_structure_not_governed', 'wip_recipe_not_governed', 'module_unavailable'] |
| Not found | PASS | HTTP 404, code=1, message=record not found |
| Invalid category | PASS | HTTP 400, code=3001, message=invalid itemCategory |
| Module unavailable/error handling | PASS | HTTP 200, itemStatus=error, warnings=['module_unavailable'] |
| Read-only negative control | PASS | POST returned HTTP 405 |
| Routing test-support | PASS | routingStatus=test_support, routingSource=test_support |
| Source-lineage/warning propagation | PASS | sourceModules=['item', 'transactionItem', 'warehouse', 'bom', 'recipe', 'routing'], warningCodes=['module_unavailable', 'test_support_only', 'resource_eligibility_not_governed', 'missing_process_master', 'missing_standard_performance', 'missing_process_master', 'missing_standard_performance'] |

## Payload Summaries

```json
{
  "productCompleteOrPartial": {
    "httpStatus": 200,
    "code": 0,
    "message": "success",
    "elapsedMs": 259.31,
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
    "requestIdentity": {
      "itemNo": "PRD-SD-001",
      "itemCategory": 5,
      "effectiveDate": 1700000000,
      "inventoryDate": 1700000000,
      "productVersion": 1
    },
    "moduleReadiness": {
      "item": {
        "moduleCode": "item",
        "statusCode": "complete",
        "sourceCode": "product",
        "warningCodes": []
      },
      "transactionItem": {
        "moduleCode": "transactionItem",
        "statusCode": "complete",
        "sourceCode": "trans_items",
        "warningCodes": []
      },
      "warehouse": {
        "moduleCode": "warehouse",
        "statusCode": "error",
        "sourceCode": "not_recorded",
        "warningCodes": [
          "module_unavailable"
        ]
      },
      "bom": {
        "moduleCode": "bom",
        "statusCode": "complete",
        "sourceCode": "product_structure",
        "warningCodes": []
      },
      "recipe": {
        "moduleCode": "recipe",
        "statusCode": "complete",
        "sourceCode": "recipe_formula",
        "warningCodes": []
      },
      "routing": {
        "moduleCode": "routing",
        "statusCode": "test_support",
        "sourceCode": "test_support",
        "warningCodes": [
          "test_support_only",
          "resource_eligibility_not_governed",
          "missing_process_master",
          "missing_standard_performance",
          "missing_process_master",
          "missing_standard_performance"
        ]
      }
    },
    "sourceLineage": {
      "item": {
        "sourceCode": "product",
        "sourceRefNo": ""
      },
      "transactionItem": {
        "sourceCode": "trans_items",
        "sourceRefNo": ""
      },
      "warehouse": {
        "sourceCode": "not_recorded",
        "sourceRefNo": ""
      },
      "bom": {
        "sourceCode": "product_structure",
        "sourceRefNo": ""
      },
      "recipe": {
        "sourceCode": "recipe_formula",
        "sourceRefNo": ""
      },
      "routing": {
        "sourceCode": "test_support",
        "sourceRefNo": "TS-ROUTE-SD-001"
      }
    },
    "warningCodes": [
      "module_unavailable",
      "test_support_only",
      "resource_eligibility_not_governed",
      "missing_process_master",
      "missing_standard_performance",
      "missing_process_master",
      "missing_standard_performance"
    ],
    "inventoryOverview": {
      "hasStock": false,
      "currentQuantity": 0.0,
      "availableQuantity": 0.0,
      "reservedQuantity": 0.0,
      "qualityHoldQuantity": 0.0,
      "inventoryValue": 0,
      "availableValue": 0,
      "warehouseCount": 0,
      "batchCount": 0,
      "riskTypes": []
    },
    "transactionItemCount": 1,
    "batchHighlightCount": 0,
    "capabilityBoundary": {
      "readOnly": true,
      "productWriteSupported": false,
      "bomWriteSupported": false,
      "recipeWriteSupported": false,
      "routingWriteSupported": false,
      "wipWriteSupported": false,
      "sourceOfTruthTransitionSupported": false,
      "cutoverSupported": false,
      "goLiveSupported": false
    }
  },
  "standaloneWipPartial": {
    "httpStatus": 200,
    "code": 0,
    "message": "success",
    "elapsedMs": 18.17,
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
    "requestIdentity": {
      "itemNo": "INP-SD-001",
      "itemCategory": 4,
      "effectiveDate": 1700000000,
      "inventoryDate": 1700000000,
      "productVersion": 0
    },
    "moduleReadiness": {
      "item": {
        "moduleCode": "item",
        "statusCode": "complete",
        "sourceCode": "product",
        "warningCodes": []
      },
      "transactionItem": {
        "moduleCode": "transactionItem",
        "statusCode": "unavailable",
        "sourceCode": "not_recorded",
        "warningCodes": [
          "missing_transaction_item"
        ]
      },
      "warehouse": {
        "moduleCode": "warehouse",
        "statusCode": "error",
        "sourceCode": "not_recorded",
        "warningCodes": [
          "module_unavailable"
        ]
      },
      "bom": {
        "moduleCode": "bom",
        "statusCode": "partial",
        "sourceCode": "not_recorded",
        "warningCodes": [
          "wip_structure_not_governed"
        ]
      },
      "recipe": {
        "moduleCode": "recipe",
        "statusCode": "partial",
        "sourceCode": "not_recorded",
        "warningCodes": [
          "wip_recipe_not_governed"
        ]
      },
      "routing": {
        "moduleCode": "routing",
        "statusCode": "unavailable",
        "sourceCode": "not_recorded",
        "warningCodes": [
          "module_unavailable"
        ]
      }
    },
    "sourceLineage": {
      "item": {
        "sourceCode": "product",
        "sourceRefNo": ""
      },
      "transactionItem": {
        "sourceCode": "not_recorded",
        "sourceRefNo": ""
      },
      "warehouse": {
        "sourceCode": "not_recorded",
        "sourceRefNo": ""
      },
      "bom": {
        "sourceCode": "not_recorded",
        "sourceRefNo": ""
      },
      "recipe": {
        "sourceCode": "not_recorded",
        "sourceRefNo": ""
      },
      "routing": {
        "sourceCode": "not_recorded",
        "sourceRefNo": ""
      }
    },
    "warningCodes": [
      "missing_transaction_item",
      "module_unavailable",
      "wip_structure_not_governed",
      "wip_recipe_not_governed",
      "module_unavailable"
    ],
    "inventoryOverview": {
      "hasStock": false,
      "currentQuantity": 0.0,
      "availableQuantity": 0.0,
      "reservedQuantity": 0.0,
      "qualityHoldQuantity": 0.0,
      "inventoryValue": 0,
      "availableValue": 0,
      "warehouseCount": 0,
      "batchCount": 0,
      "riskTypes": []
    },
    "transactionItemCount": 0,
    "batchHighlightCount": 0,
    "capabilityBoundary": {
      "readOnly": true,
      "productWriteSupported": false,
      "bomWriteSupported": false,
      "recipeWriteSupported": false,
      "routingWriteSupported": false,
      "wipWriteSupported": false,
      "sourceOfTruthTransitionSupported": false,
      "cutoverSupported": false,
      "goLiveSupported": false
    }
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
    "elapsedMs": 2.74,
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
    "requestIdentity": {
      "itemNo": "PRD-SD-001",
      "itemCategory": 5,
      "effectiveDate": 1700000000,
      "inventoryDate": 1700000000,
      "productVersion": 1
    },
    "moduleReadiness": {
      "item": {
        "moduleCode": "item",
        "statusCode": "error",
        "sourceCode": "not_recorded",
        "warningCodes": [
          "module_unavailable"
        ]
      }
    },
    "sourceLineage": {
      "item": {
        "sourceCode": "not_recorded",
        "sourceRefNo": ""
      }
    },
    "warningCodes": [
      "module_unavailable"
    ],
    "inventoryOverview": {
      "hasStock": false,
      "currentQuantity": 0.0,
      "availableQuantity": 0.0,
      "reservedQuantity": 0.0,
      "qualityHoldQuantity": 0.0,
      "inventoryValue": 0,
      "availableValue": 0,
      "warehouseCount": 0,
      "batchCount": 0,
      "riskTypes": []
    },
    "transactionItemCount": 0,
    "batchHighlightCount": 0,
    "capabilityBoundary": {
      "readOnly": true,
      "productWriteSupported": false,
      "bomWriteSupported": false,
      "recipeWriteSupported": false,
      "routingWriteSupported": false,
      "wipWriteSupported": false,
      "sourceOfTruthTransitionSupported": false,
      "cutoverSupported": false,
      "goLiveSupported": false
    }
  },
  "readOnlyNegativeControl": {
    "httpStatus": 405,
    "code": null,
    "message": ""
  }
}
```

## Boundary Confirmation

No material database/schema change was performed.

No Product write, Routing write, Process Master write, Production action, migration, Source-of-Truth transition, Engineering Pull, Cutover, or ERP2.0 Go-Live was performed.
