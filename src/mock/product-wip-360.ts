import type { ProductWip360OverviewData } from "@/types/product-wip-360";

export const productWip360ProductMock: ProductWip360OverviewData = {
  requestIdentity: { itemNo: "PRD-SD-001", itemCategory: 5 },
  subject: {
    itemNo: "PRD-SD-001",
    itemName: "Shared DEV Product Fixture A",
    itemCategory: 5,
    itemCategoryLabel: "製成品",
    identityType: "product",
    identityTypeLabel: "Product",
    versionLabel: "V1",
    unitWarehouseLabel: "公斤",
    unitProductLabel: "公斤",
    masterStatusLabel: "部分來源待確認",
    sourceLabel: "product",
    tone: "warning"
  },
  moduleReadiness: [
    { moduleCode: "item", moduleLabel: "Item", statusCode: "complete", statusLabel: "完整", sourceLabel: "product", warningCodes: [], tone: "success" },
    { moduleCode: "transactionItem", moduleLabel: "Transaction Item", statusCode: "complete", statusLabel: "已關聯", sourceLabel: "trans_items", warningCodes: [], tone: "success" },
    { moduleCode: "warehouse", moduleLabel: "Warehouse / Inventory", statusCode: "complete", statusLabel: "完整", sourceLabel: "warehouse snapshot", warningCodes: [], tone: "success" },
    { moduleCode: "bom", moduleLabel: "BOM / Product Structure", statusCode: "complete", statusLabel: "完整", sourceLabel: "product_spec", warningCodes: [], tone: "success" },
    { moduleCode: "recipe", moduleLabel: "Recipe / Formula", statusCode: "partial", statusLabel: "部分資料", sourceLabel: "bom / bom_item", warningCodes: ["missing_loss_source"], tone: "warning" },
    { moduleCode: "routing", moduleLabel: "Routing / Process Flow", statusCode: "test_support", statusLabel: "測試支援", sourceLabel: "test_support", warningCodes: ["test_support_only"], tone: "warning" }
  ],
  transactionItems: [
    {
      transItemNo: "TRN-SD-001",
      transItemName: "客戶規格 Product A",
      companyNo: "CUS-001",
      companyDisplayName: "示範客戶",
      contractNo: "CTR-2609-001",
      tradeUnitLabel: "箱",
      tradePrice: 1280,
      dataQualityLabel: "完整",
      tone: "success"
    }
  ],
  inventoryOverview: {
    hasStock: true,
    currentQuantity: 1280,
    availableQuantity: 1020,
    reservedQuantity: 180,
    qualityHoldQuantity: 80,
    inventoryValue: 3861000,
    availableValue: 3078000,
    warehouseCount: 2,
    batchCount: 2,
    riskTypes: ["near_expiry", "quality_hold"]
  },
  batchHighlights: [
    {
      batchNo: "B260904-SD-A",
      warehouseNo: "WH-FG-01",
      warehouseName: "成品倉 A",
      currentQuantity: 900,
      availableQuantity: 720,
      unitLabel: "公斤",
      validDateLabel: "2026/12/31",
      riskLevelLabel: "正常",
      sourceRefLabel: "入庫單 WH-IN-260904",
      tone: "success"
    },
    {
      batchNo: "B260831-SD-B",
      warehouseNo: "WH-FG-02",
      warehouseName: "成品倉 B",
      currentQuantity: 380,
      availableQuantity: 300,
      unitLabel: "公斤",
      validDateLabel: "2026/09/20",
      riskLevelLabel: "接近效期",
      sourceRefLabel: "生產工單 MO-260831",
      tone: "warning"
    }
  ],
  productStructure: {
    statusCode: "complete",
    statusLabel: "完整",
    rootProductNo: "PRD-SD-001",
    rootProductVersion: 1,
    bomNo: "BOM-SD-001",
    bomVersionLabel: "V1 / 目前有效",
    children: [
      { id: "root", itemNo: "PRD-SD-001", itemName: "Shared DEV Product Fixture A", nodeTypeLabel: "製成品 root", quantity: 1, unitLabel: "公斤", level: 0, tone: "info" },
      { id: "wip", itemNo: "WIP-SD-BASE-001", itemName: "半成品基底", nodeTypeLabel: "在製品", quantity: 1, unitLabel: "公斤", level: 1, tone: "neutral" },
      { id: "pack", itemNo: "MAT-SD-PACK-001", itemName: "包材", nodeTypeLabel: "物料", quantity: 1, unitLabel: "個", level: 1, tone: "neutral" }
    ],
    warnings: [],
    tone: "success"
  },
  recipeFormula: {
    statusCode: "partial",
    statusLabel: "部分資料",
    recipeNo: "RCP-SD-001",
    recipeVersionLabel: "V1",
    outputItemNo: "PRD-SD-001",
    outputQuantity: 1,
    outputUnitLabel: "公斤",
    inputs: [
      { itemNo: "WIP-SD-BASE-001", itemName: "半成品基底", quantity: 0.8, weightRatio: 80, lossRate: 1.2, unitLabel: "公斤" },
      { itemNo: "MAT-SD-FLAVOR-001", itemName: "調味料", quantity: 0.2, weightRatio: 20, lossRate: 0.4, unitLabel: "公斤" }
    ],
    warnings: ["missing_loss_source"],
    tone: "warning"
  },
  routingProcess: {
    statusCode: "test_support",
    statusLabel: "測試支援",
    routingVersionId: "TS-ROUTE-SD-001",
    routingVersionLabel: "V1",
    sourceLabel: "test_support",
    steps: [
      {
        stepNo: 10,
        stageLabel: "test_support",
        groupLabel: "前備",
        processLabel: "Synthetic material preparation visibility step",
        recipeRefLabel: "BOM-SD-001",
        resourceLabel: "not governed",
        standardRateLabel: "待確認",
        tone: "warning"
      },
      {
        stepNo: 20,
        stageLabel: "test_support",
        groupLabel: "組成",
        processLabel: "Synthetic product composition visibility step",
        recipeRefLabel: "BOM-SD-001",
        resourceLabel: "not recorded",
        standardRateLabel: "待確認",
        tone: "warning"
      }
    ],
    warnings: ["test_support_only", "missing_standard_performance"],
    tone: "warning"
  },
  sourceLineage: [
    { moduleLabel: "Item", sourceLabel: "product", statusLabel: "read-only", tone: "success" },
    { moduleLabel: "Warehouse", sourceLabel: "inventory snapshot", statusLabel: "read-only", tone: "success" },
    { moduleLabel: "BOM", sourceLabel: "product_spec", statusLabel: "read-only", tone: "success" },
    { moduleLabel: "Recipe", sourceLabel: "bom / bom_item", statusLabel: "partial", tone: "warning" },
    { moduleLabel: "Routing", sourceLabel: "test_support", statusLabel: "non-formal evidence", tone: "warning" }
  ],
  warnings: [
    {
      moduleLabel: "Routing",
      code: "test_support_only",
      message: "Routing 目前資料來自非正式 Shared DEV test-support read-only surface。",
      refNo: "TS-ROUTE-SD-001",
      tone: "warning"
    },
    {
      moduleLabel: "Routing",
      code: "resource_eligibility_not_governed",
      message: "資源資格尚未由正式治理資料提供。",
      refNo: "TS-ROUTE-SD-001",
      tone: "warning"
    }
  ],
  capabilityBoundary: {
    readOnly: true,
    productWriteSupported: false,
    bomWriteSupported: false,
    recipeWriteSupported: false,
    routingWriteSupported: false,
    workflowMutationSupported: false,
    sourceOfTruthTransitionSupported: false
  }
};

export const productWip360WipMock: ProductWip360OverviewData = {
  ...productWip360ProductMock,
  requestIdentity: { itemNo: "WIP-SD-BASE-001", itemCategory: 4 },
  subject: {
    itemNo: "WIP-SD-BASE-001",
    itemName: "半成品基底",
    itemCategory: 4,
    itemCategoryLabel: "在製品",
    identityType: "wip",
    identityTypeLabel: "Standalone WIP",
    versionLabel: "未指定",
    unitWarehouseLabel: "公斤",
    unitProductLabel: "公斤",
    masterStatusLabel: "WIP root 部分治理",
    sourceLabel: "inproduct",
    tone: "warning"
  },
  moduleReadiness: [
    { moduleCode: "item", moduleLabel: "Item", statusCode: "complete", statusLabel: "完整", sourceLabel: "inproduct", warningCodes: [], tone: "success" },
    { moduleCode: "transactionItem", moduleLabel: "Transaction Item", statusCode: "not_applicable", statusLabel: "不適用", sourceLabel: "not_applicable", warningCodes: ["not_applicable"], tone: "info" },
    { moduleCode: "warehouse", moduleLabel: "Warehouse / Inventory", statusCode: "complete", statusLabel: "完整", sourceLabel: "warehouse snapshot", warningCodes: [], tone: "success" },
    { moduleCode: "bom", moduleLabel: "BOM / Product Structure", statusCode: "partial", statusLabel: "部分資料", sourceLabel: "unavailable", warningCodes: ["wip_product_structure_not_governed"], tone: "warning" },
    { moduleCode: "recipe", moduleLabel: "Recipe / Formula", statusCode: "partial", statusLabel: "部分資料", sourceLabel: "unavailable", warningCodes: ["wip_recipe_formula_not_governed"], tone: "warning" },
    { moduleCode: "routing", moduleLabel: "Routing / Process Flow", statusCode: "unavailable", statusLabel: "目前不可用", sourceLabel: "unavailable", warningCodes: ["standalone_wip_routing_not_available"], tone: "warning" }
  ],
  transactionItems: [],
  inventoryOverview: {
    hasStock: true,
    currentQuantity: 420,
    availableQuantity: 360,
    reservedQuantity: 40,
    qualityHoldQuantity: 20,
    inventoryValue: 860000,
    availableValue: 738000,
    warehouseCount: 1,
    batchCount: 1,
    riskTypes: ["partial_wip_governance"]
  },
  batchHighlights: [
    {
      batchNo: "WIP260904-BASE-A",
      warehouseNo: "WH-WIP-01",
      warehouseName: "在製品暫存區",
      currentQuantity: 420,
      availableQuantity: 360,
      unitLabel: "公斤",
      validDateLabel: "未提供",
      riskLevelLabel: "WIP governance partial",
      sourceRefLabel: "生產投入 MO-260904",
      tone: "warning"
    }
  ],
  productStructure: {
    statusCode: "partial",
    statusLabel: "WIP root 尚未完整治理",
    rootProductNo: "WIP-SD-BASE-001",
    rootProductVersion: 0,
    bomNo: "",
    bomVersionLabel: "不適用或待治理",
    children: [],
    warnings: ["wip_product_structure_not_governed"],
    tone: "warning"
  },
  recipeFormula: {
    statusCode: "partial",
    statusLabel: "WIP Recipe 待確認",
    recipeNo: "",
    recipeVersionLabel: "不適用或待治理",
    outputItemNo: "WIP-SD-BASE-001",
    outputQuantity: 0,
    outputUnitLabel: "公斤",
    inputs: [],
    warnings: ["wip_recipe_formula_not_governed"],
    tone: "warning"
  },
  routingProcess: {
    ...productWip360ProductMock.routingProcess,
    statusCode: "unavailable",
    statusLabel: "尚無獨立 WIP Routing",
    routingVersionId: "",
    routingVersionLabel: "未提供",
    sourceLabel: "unavailable",
    steps: [],
    warnings: ["standalone_wip_routing_not_available"],
    tone: "warning"
  },
  sourceLineage: [
    { moduleLabel: "Item", sourceLabel: "inproduct", statusLabel: "read-only", tone: "success" },
    { moduleLabel: "Warehouse", sourceLabel: "inventory snapshot", statusLabel: "read-only", tone: "success" },
    { moduleLabel: "Transaction Item", sourceLabel: "not_applicable", statusLabel: "Standalone WIP", tone: "info" },
    { moduleLabel: "BOM", sourceLabel: "unavailable", statusLabel: "WIP root 待治理", tone: "warning" },
    { moduleLabel: "Recipe", sourceLabel: "unavailable", statusLabel: "WIP output 待治理", tone: "warning" },
    { moduleLabel: "Routing", sourceLabel: "unavailable", statusLabel: "無獨立 WIP route evidence", tone: "warning" }
  ],
  warnings: [
    {
      moduleLabel: "Transaction Item",
      code: "not_applicable",
      message: "Standalone WIP 可沒有交易品項或客戶連結，不列為錯誤。",
      refNo: "WIP-SD-BASE-001",
      tone: "info"
    },
    {
      moduleLabel: "Routing",
      code: "standalone_wip_routing_not_available",
      message: "目前僅能證明 WIP 作為 Product routing 的中間步驟或參照，尚無獨立 WIP Routing Version fixture。",
      refNo: "WIP-SD-BASE-001",
      tone: "warning"
    }
  ]
};

export function productWip360Mock(itemCategory: 4 | 5) {
  return itemCategory === 4 ? productWip360WipMock : productWip360ProductMock;
}
