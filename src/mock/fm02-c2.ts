import type { C2ItemReferenceData } from "@/types/fm02-c2";

export const FM02_C2_CUSTOMER_SCOPE_SENTINEL = "00000000-0000-0000-0000-000000000000";

export const fm02C2ItemReferenceMock: Record<string, C2ItemReferenceData> = {
  "RM-001": {
    itemId: "RM-001",
    itemUoms: [
      { id: "RM-001-UOM-KG", code: "KG", label: "公斤", role: "STOCK" },
      { id: "RM-001-UOM-BOX", code: "BOX", label: "盒", role: "PRODUCTION" }
    ],
    conversionRules: [
      {
        id: "C2-CONV-RM-001-001",
        itemId: "RM-001",
        fromItemUomId: "RM-001-UOM-KG",
        toItemUomId: "RM-001-UOM-BOX",
        conversionType: "FIXED",
        conversionFactor: "2.500000000000000000",
        roundingMode: "HALF_UP",
        roundingScale: 2,
        lifecycleStatus: "ACTIVE",
        effectiveFrom: "2026-01-01T00:00:00",
        sourceReference: "mock:c2-conversion:RM-001"
      }
    ],
    customerQualifications: [
      {
        id: "C2-CQ-RM-001-001",
        itemId: "RM-001",
        customerRef: "CUSTOMER-A",
        supplierQualificationScopeKey: FM02_C2_CUSTOMER_SCOPE_SENTINEL,
        approvalScope: "ANY_GENERAL_QUALIFIED_SUPPLIER",
        supplyMethod: "PURCHASED",
        qualificationStatus: "ACTIVE",
        effectiveFrom: "2026-01-01T00:00:00",
        sourceReference: "mock:c2-customer-qualification:RM-001"
      }
    ],
    packageState: "NOT_AVAILABLE",
    legacyMappingState: "NOT_AVAILABLE"
  },
  "FG-MISSING-BOM": {
    itemId: "FG-MISSING-BOM",
    itemUoms: [{ id: "FG-MISSING-BOM-UOM-BOX", code: "BOX", label: "盒", role: "STOCK" }],
    conversionRules: [],
    customerQualifications: [],
    packageState: "NOT_AVAILABLE",
    legacyMappingState: "NOT_AVAILABLE"
  }
};
