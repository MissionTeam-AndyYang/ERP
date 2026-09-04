import type { PackagingIdentityType, PackagingOverviewData } from "@/types/packaging";

export const packagingProductMock: PackagingOverviewData = {
  serverTimestamp: 1788451200,
  timezone: "Asia/Taipei",
  requestIdentity: { itemNo: "PRD-SD-001", itemCategory: 5, productVersion: 1 },
  subject: {
    itemNo: "PRD-SD-001",
    itemName: "Shared DEV Product Fixture A",
    itemCategory: 5,
    itemCategoryLabel: "製成品",
    itemSubCategory: 0,
    productVersion: 1,
    versionLabel: "V1",
    unitShippingLabel: "箱",
    unitWarehouseLabel: "公斤",
    unitProductLabel: "公斤",
    comment: "包裝規格唯讀檢視示範資料",
    sourceLabel: "product",
    tone: "success"
  },
  summary: {
    packagingSpecCount: 2,
    packagingBomCount: 2,
    packageLevelCount: 2,
    materialLineCount: 4,
    totalCount: 13,
    totalWeight: 4.8
  },
  packagingSpecs: [
    {
      specId: "PRD-SD-001:1:BOM2-CASE-001",
      productNo: "PRD-SD-001",
      productVersion: 1,
      wipNo: "",
      packagingLevel: 1,
      packagingLevelLabel: "箱規",
      packagingBomNo: "BOM2-CASE-001",
      packagingBomName: "外箱與箱標組合",
      count: 1,
      unitLabel: "箱",
      weight: 3.2,
      masterUnitLabel: "組",
      masterWeight: 3.2,
      linkedBomNo: "BOM-PACK-CASE",
      linkedBomVersion: 1,
      lineCount: 2,
      lines: [
        {
          parentBomNo: "BOM2-CASE-001",
          parentBomName: "外箱與箱標組合",
          childCategory: 2,
          childCategoryLabel: "物料",
          childNo: "MAT-CARTON-001",
          childName: "標準外箱",
          childUnitLabel: "個",
          count: 1,
          childUnit2Label: "個",
          weight: 2.8,
          length: 0,
          expectedLoss: 0.5,
          actualLoss: 0,
          processCount: 1,
          comment: "外箱",
        },
        {
          parentBomNo: "BOM2-CASE-001",
          parentBomName: "外箱與箱標組合",
          childCategory: 2,
          childCategoryLabel: "物料",
          childNo: "MAT-LABEL-CASE",
          childName: "箱標",
          childUnitLabel: "張",
          count: 1,
          childUnit2Label: "張",
          weight: 0.4,
          length: 0,
          expectedLoss: 1,
          actualLoss: 0,
          processCount: 1,
          comment: "貼附於外箱",
        }
      ],
      sourceLabel: "product_bom_spec",
      masterSourceLabel: "bom2_number",
      lineSourceLabel: "bom2",
      tone: "success"
    },
    {
      specId: "PRD-SD-001:1:BOM2-GROUP-001",
      productNo: "PRD-SD-001",
      productVersion: 1,
      wipNo: "",
      packagingLevel: 2,
      packagingLevelLabel: "組規",
      packagingBomNo: "BOM2-GROUP-001",
      packagingBomName: "內袋與組標",
      count: 12,
      unitLabel: "包",
      weight: 1.6,
      masterUnitLabel: "組",
      masterWeight: 1.6,
      linkedBomNo: "BOM-PACK-GROUP",
      linkedBomVersion: 1,
      lineCount: 2,
      lines: [
        {
          parentBomNo: "BOM2-GROUP-001",
          parentBomName: "內袋與組標",
          childCategory: 2,
          childCategoryLabel: "物料",
          childNo: "MAT-BAG-001",
          childName: "內袋",
          childUnitLabel: "個",
          count: 12,
          childUnit2Label: "個",
          weight: 1.2,
          length: 0,
          expectedLoss: 1,
          actualLoss: 0,
          processCount: 12,
          comment: "一箱十二包",
        },
        {
          parentBomNo: "BOM2-GROUP-001",
          parentBomName: "內袋與組標",
          childCategory: 2,
          childCategoryLabel: "物料",
          childNo: "MAT-LABEL-INNER",
          childName: "內袋標籤",
          childUnitLabel: "張",
          count: 12,
          childUnit2Label: "張",
          weight: 0.4,
          length: 0,
          expectedLoss: 1,
          actualLoss: 0,
          processCount: 12,
          comment: "",
        }
      ],
      sourceLabel: "product_bom_spec",
      masterSourceLabel: "bom2_number",
      lineSourceLabel: "bom2",
      tone: "success"
    }
  ],
  sourceLineage: [
    { sourceTypeLabel: "主體來源", sourceLabel: "product", tone: "success" },
    { sourceTypeLabel: "包裝規格來源", sourceLabel: "product_bom_spec", tone: "success" },
    { sourceTypeLabel: "包材 BOM 主檔來源", sourceLabel: "bom2_number", tone: "success" },
    { sourceTypeLabel: "包材 BOM 明細來源", sourceLabel: "bom2", tone: "success" }
  ],
  moduleReadiness: [
    {
      moduleCode: "packagingSpecification",
      moduleLabel: "包裝規格",
      statusCode: "complete",
      statusLabel: "完整",
      sourceLabel: "product_bom_spec",
      warningCodes: [],
      tone: "success"
    }
  ],
  warnings: [],
  capabilityBoundary: {
    readOnly: true,
    packagingWriteSupported: false,
    packagingApprovalSupported: false,
    packagingReleaseSupported: false,
    sourceOfTruthTransitionSupported: false,
    cutoverSupported: false,
    goLiveSupported: false
  }
};

export const packagingWipMock: PackagingOverviewData = {
  ...packagingProductMock,
  requestIdentity: { itemNo: "INP-SD-001", itemCategory: 4 },
  subject: {
    ...packagingProductMock.subject!,
    itemNo: "INP-SD-001",
    itemName: "Shared DEV WIP Fixture A",
    itemCategory: 4,
    itemCategoryLabel: "在製品",
    productVersion: 0,
    versionLabel: "未指定",
    unitShippingLabel: "組",
    comment: "WIP 包裝規格由下游製成品關聯呈現",
    sourceLabel: "inproduct",
    tone: "warning"
  },
  packagingSpecs: packagingProductMock.packagingSpecs.map((spec) => ({
    ...spec,
    wipNo: "INP-SD-001",
    tone: "warning" as const
  })),
  sourceLineage: [
    { sourceTypeLabel: "主體來源", sourceLabel: "inproduct", tone: "success" },
    { sourceTypeLabel: "包裝規格來源", sourceLabel: "product_spec downstream product", tone: "warning" },
    { sourceTypeLabel: "包材 BOM 主檔來源", sourceLabel: "bom2_number", tone: "success" },
    { sourceTypeLabel: "包材 BOM 明細來源", sourceLabel: "bom2", tone: "success" }
  ],
  moduleReadiness: [
    {
      moduleCode: "packagingSpecification",
      moduleLabel: "包裝規格",
      statusCode: "partial",
      statusLabel: "部分資料",
      sourceLabel: "product_spec",
      warningCodes: ["wip_packaging_context_from_downstream_product"],
      tone: "warning"
    }
  ],
  warnings: [
    {
      moduleLabel: "包裝規格",
      code: "wip_packaging_context_from_downstream_product",
      message: "在製品包裝情境由下游製成品包裝規格關聯呈現，需保留來源產品識別。",
      refNo: "PRD-SD-001",
      tone: "warning"
    }
  ]
};

export function packagingMock(identityType: PackagingIdentityType) {
  return identityType === "wip" ? packagingWipMock : packagingProductMock;
}
