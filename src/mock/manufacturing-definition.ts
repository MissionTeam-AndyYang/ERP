import type {
  ManufacturingDefinitionData,
  ManufacturingDefinitionQuery,
  ManufacturingDefinitionSubject
} from "@/types/manufacturing-definition";

export function manufacturingDefinitionMock(query: ManufacturingDefinitionQuery): ManufacturingDefinitionData {
  const isWip = query.itemCategory === 4;
  const subject: ManufacturingDefinitionSubject = {
    itemNo: query.itemNo,
    itemName: isWip ? "示範半成品" : "示範製成品",
    itemCategory: query.itemCategory,
    itemCategoryLabel: isWip ? "在製品" : "製成品",
    identityType: isWip ? "wip" : "product",
    identityTypeLabel: isWip ? "Standalone WIP" : "Product",
    versionLabel: isWip ? "不適用" : "V2",
    unitWarehouseLabel: "公斤",
    unitProductLabel: "公斤",
    masterStatusLabel: "可供查閱",
    sourceLabel: "Shared DEV read-only evidence",
    tone: "success" as const
  };
  const bomVersion = {
    domainCode: "bom",
    domainLabel: "BOM / 產品結構",
    referenceNo: isWip ? "BOM-WIP-SD-001" : "BOM-PRD-SD-001",
    versionLabel: "V2",
    statusCode: "effective",
    statusLabel: "目前有效",
    dateLabel: "2026/09/01",
    detailLabel: "產品結構候選",
    tone: "success" as const
  };
  const recipeVersion = {
    domainCode: "recipe",
    domainLabel: "Recipe / Formula",
    referenceNo: "RCP-SD-001",
    versionLabel: "V1",
    statusCode: "effective",
    statusLabel: "目前有效",
    dateLabel: "2026/09/01",
    detailLabel: "配方與投入量候選",
    tone: "success" as const
  };
  const routingVersion = {
    domainCode: "routing",
    domainLabel: "Routing / Process Flow",
    referenceNo: "RT-SD-001",
    versionLabel: "V1",
    statusCode: "test_support",
    statusLabel: "測試支援",
    dateLabel: "2026/09/01",
    detailLabel: "流程順序僅供唯讀參照",
    tone: "warning" as const
  };
  const packagingVersion = {
    domainCode: "packaging",
    domainLabel: "Packaging Specification",
    referenceNo: "PKG-SD-001",
    versionLabel: "V1",
    statusCode: "unavailable",
    statusLabel: "目前不可用",
    dateLabel: "未提供",
    detailLabel: "尚無正式包裝規格候選",
    tone: "warning" as const
  };
  const warnings = [
    {
      domainCode: "packaging",
      domainLabel: "Packaging Specification",
      code: "module_unavailable",
      message: "包裝規格尚未提供正式候選；此畫面不自行推測版本。",
      refNo: query.itemNo,
      tone: "warning" as const
    }
  ];
  const capabilityBoundary = {
    readOnly: true,
    manufacturingDefinitionWriteSupported: false,
    productWriteSupported: false,
    bomWriteSupported: false,
    recipeWriteSupported: false,
    routingWriteSupported: false,
    packagingWriteSupported: false,
    approvalSupported: false,
    releaseSupported: false,
    freezeSupported: false,
    sourceOfTruthTransitionSupported: false,
    cutoverSupported: false,
    goLiveSupported: false
  };

  return {
    serverTimestamp: Math.floor(Date.now() / 1000),
    timezone: "Asia/Taipei",
    requestIdentity: query,
    subject,
    definitionStatus: "partial",
    definitionId: `candidate:${query.itemNo}:${query.itemCategory}:${query.asOfDate ?? 0}`,
    candidateVersions: [bomVersion, recipeVersion, routingVersion, packagingVersion],
    domainReferences: [
      {
        domainCode: "bom",
        domainLabel: "BOM / 產品結構",
        statusCode: "complete",
        statusLabel: "資料可用",
        sourceLabel: "product_structure",
        warningCodes: [],
        versions: [bomVersion],
        detailLabel: "1 個結構版本候選",
        tone: "success"
      },
      {
        domainCode: "recipe",
        domainLabel: "Recipe / Formula",
        statusCode: "complete",
        statusLabel: "資料可用",
        sourceLabel: "recipe_formula",
        warningCodes: [],
        versions: [recipeVersion],
        detailLabel: "1 個配方版本候選",
        tone: "success"
      },
      {
        domainCode: "routing",
        domainLabel: "Routing / Process Flow",
        statusCode: "test_support",
        statusLabel: "測試支援",
        sourceLabel: "routing_process_flow",
        warningCodes: ["test_support_only"],
        versions: [routingVersion],
        detailLabel: "流程證據為測試支援來源",
        tone: "warning"
      },
      {
        domainCode: "packaging",
        domainLabel: "Packaging Specification",
        statusCode: "unavailable",
        statusLabel: "目前不可用",
        sourceLabel: "not_recorded",
        warningCodes: ["module_unavailable"],
        versions: [packagingVersion],
        detailLabel: "無正式包裝規格候選",
        tone: "warning"
      }
    ],
    quantityAuthorities: [
      {
        domainCode: "bom",
        domainLabel: "BOM / 產品結構",
        valueTypeCode: "component_quantity",
        valueTypeLabel: "元件數量",
        value: 2.5,
        unitLabel: "公斤",
        sourceLabel: "product_structure",
        sourceRef: "MAT-SD-001",
        authorityCaveat: "產品結構證據；不是 Recipe 配方數量。",
        tone: "info"
      },
      {
        domainCode: "recipe",
        domainLabel: "Recipe / Formula",
        valueTypeCode: "input_quantity",
        valueTypeLabel: "配方投入數量",
        value: 2.25,
        unitLabel: "公斤",
        sourceLabel: "recipe_formula",
        sourceRef: "MAT-SD-001",
        authorityCaveat: "Recipe / Formula 證據；不是 BOM 結構數量。",
        tone: "info"
      }
    ],
    weightAuthorities: [
      {
        domainCode: "recipe",
        domainLabel: "Recipe / Formula",
        valueTypeCode: "formula_weight",
        valueTypeLabel: "配方重量",
        value: 2.25,
        unitLabel: "公斤",
        sourceLabel: "recipe_formula",
        sourceRef: "RCP-SD-001",
        authorityCaveat: "配方組成證據；不是生產實際重量。",
        tone: "info"
      }
    ],
    effectivityAsOfDateLabel: "2026/09/08",
    effectivity: [
      {
        domainCode: "bom",
        domainLabel: "BOM / 產品結構",
        effectiveFromLabel: "2026/09/01",
        effectiveToLabel: "未設定",
        currentActive: true,
        retiredInactive: false,
        statusCode: "effective",
        statusLabel: "目前有效",
        evidenceRef: "BOM-PRD-SD-001:2",
        conflictState: "無衝突",
        tone: "success"
      },
      {
        domainCode: "recipe",
        domainLabel: "Recipe / Formula",
        effectiveFromLabel: "2026/09/01",
        effectiveToLabel: "未設定",
        currentActive: true,
        retiredInactive: false,
        statusCode: "effective",
        statusLabel: "目前有效",
        evidenceRef: "RCP-SD-001:1",
        conflictState: "無衝突",
        tone: "success"
      }
    ],
    resolutionStatus: "PARTIAL_CANDIDATE",
    resolutionStatusLabel: "部分候選",
    warnings,
    sourceLineage: [
      {
        domainCode: "bom",
        domainLabel: "BOM / 產品結構",
        sourceCode: "product_structure",
        sourceLabel: "產品結構資料",
        sourceRef: "product_wip_360",
        sourceParticipant: "existing_backend_read_surface",
        acceptedEvidenceClass: "ACCEPTED_PRODUCT_EVIDENCE",
        acceptedEvidenceLabel: "可接受的產品證據",
        acceptanceState: "read_only_non_production",
        authorityCaveat: "來源存在不等於業務事實已完成確認。",
        tone: "success"
      },
      {
        domainCode: "packaging",
        domainLabel: "Packaging Specification",
        sourceCode: "not_recorded",
        sourceLabel: "尚未記錄來源",
        sourceRef: "",
        sourceParticipant: "existing_backend_read_surface",
        acceptedEvidenceClass: "UNAVAILABLE",
        acceptedEvidenceLabel: "不可用",
        acceptanceState: "read_only_non_production",
        authorityCaveat: "需要回到包裝規格來源確認。",
        tone: "warning"
      }
    ],
    freezeCompatibility: {
      statusCode: "CANDIDATE_PREPARED_WITH_TARGETED_CONDITIONS",
      statusLabel: "候選已整理，仍有條件",
      resolutionStatus: "PARTIAL_CANDIDATE",
      previewOnly: true,
      freezeReady: false,
      approvalSupported: false,
      releaseSupported: false,
      freezeSupported: false,
      productionOrderFreezeImplemented: false,
      warningCount: warnings.length,
      tone: "warning"
    },
    capabilityBoundary
  };
}
