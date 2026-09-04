import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { bomUnitLabel } from "@/i18n/bom-enums";
import { defaultLanguage } from "@/i18n/dictionary";
import { productWip360Mock } from "@/mock/product-wip-360";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { StatusTone } from "@/types/dashboard";
import type {
  ProductWip360BatchHighlight,
  ProductWip360CapabilityBoundary,
  ProductWip360DataSource,
  ProductWip360InventoryOverview,
  ProductWip360Lineage,
  ProductWip360ModuleReadiness,
  ProductWip360OverviewData,
  ProductWip360Query,
  ProductWip360Recipe,
  ProductWip360RecipeInput,
  ProductWip360Routing,
  ProductWip360RoutingStep,
  ProductWip360StatusCode,
  ProductWip360Structure,
  ProductWip360StructureNode,
  ProductWip360Subject,
  ProductWip360TransactionItem,
  ProductWip360Warning
} from "@/types/product-wip-360";

type ApiProductWip360Payload = {
  requestIdentity?: Partial<ProductWip360Query>;
  subject?: Partial<ProductWip360Subject> & {
    unitWarehouse?: number;
    unitProduct?: number;
    masterStatusCode?: string;
    subjectSourceCode?: string;
  };
  moduleReadiness?: ApiModuleReadiness[];
  transactionContext?: {
    transactionItems?: ApiTransactionItem[];
  };
  inventoryOverview?: Partial<ProductWip360InventoryOverview>;
  batchHighlights?: ApiBatchHighlight[];
  productStructure?: ApiProductStructure;
  recipeFormula?: ApiRecipeFormula;
  routingProcess?: ApiRoutingProcess;
  sourceLineage?: ApiLineage[] | Record<string, string | undefined>;
  warnings?: ApiWarning[];
  capabilityBoundary?: Partial<ProductWip360CapabilityBoundary>;
};

type ApiModuleReadiness = {
  moduleCode?: string;
  statusCode?: string;
  sourceCode?: string;
  sourceLabel?: string;
  warningCodes?: string[];
};

type ApiTransactionItem = {
  transItemNo?: string;
  transItemName?: string;
  companyNo?: string;
  companyDisplayName?: string;
  contractNo?: string;
  tradeUnit?: number;
  tradeUnitLabel?: string;
  tradePrice?: number;
  dataQualityCode?: string;
  dataQualityLabel?: string;
};

type ApiBatchHighlight = {
  batchNo?: string;
  warehouseNo?: string;
  warehouseName?: string;
  currentQuantity?: number;
  availableQuantity?: number;
  unit?: number;
  unitLabel?: string;
  validDate?: number;
  validDateLabel?: string;
  riskLevelCode?: string;
  riskLevelLabel?: string;
  refCategory?: number;
  refNo?: string;
};

type ApiProductStructure = {
  statusCode?: string;
  statusLabel?: string;
  rootProductNo?: string;
  rootProductVersion?: number;
  bomNo?: string;
  bomVersion?: number;
  bomVersionLabel?: string;
  children?: ApiStructureNode[];
  warnings?: string[];
};

type ApiStructureNode = {
  id?: string;
  itemNo?: string;
  itemName?: string;
  nodeTypeCode?: string;
  nodeTypeLabel?: string;
  quantity?: number;
  unit?: number;
  unitLabel?: string;
  level?: number;
};

type ApiRecipeFormula = {
  statusCode?: string;
  statusLabel?: string;
  recipeNo?: string;
  recipeVersion?: number;
  recipeVersionLabel?: string;
  outputItemNo?: string;
  outputQuantity?: number;
  outputUnit?: number;
  outputUnitLabel?: string;
  inputs?: ApiRecipeInput[];
  warnings?: string[];
};

type ApiRecipeInput = {
  itemNo?: string;
  itemName?: string;
  quantity?: number;
  weightRatio?: number;
  lossRate?: number;
  unit?: number;
  unitLabel?: string;
};

type ApiRoutingProcess = {
  statusCode?: string;
  statusLabel?: string;
  routingVersionId?: string;
  routingVersion?: number;
  routingVersionLabel?: string;
  sourceCode?: string;
  sourceLabel?: string;
  steps?: ApiRoutingStep[];
  warnings?: string[];
};

type ApiRoutingStep = {
  stepNo?: number;
  stepOrder?: number;
  stageLabel?: string;
  groupLabel?: string;
  processLabel?: string;
  processName?: string;
  recipeRefLabel?: string;
  recipeNo?: string;
  resourceLabel?: string;
  resourceEligibilityLabel?: string;
  standardRateLabel?: string;
};

type ApiLineage = {
  moduleCode?: string;
  moduleLabel?: string;
  sourceCode?: string;
  sourceLabel?: string;
  statusCode?: string;
  statusLabel?: string;
};

type ApiWarning = {
  moduleCode?: string;
  moduleLabel?: string;
  warningCode?: string;
  code?: string;
  message?: string;
  refNo?: string;
};

export type ProductWip360Result = {
  data: ProductWip360OverviewData;
  source: ProductWip360DataSource;
  error?: string;
};

export const emptyProductWip360OverviewData: ProductWip360OverviewData = {
  requestIdentity: { itemNo: "", itemCategory: 5 },
  subject: undefined,
  moduleReadiness: [],
  transactionItems: [],
  inventoryOverview: {
    hasStock: false,
    currentQuantity: 0,
    availableQuantity: 0,
    reservedQuantity: 0,
    qualityHoldQuantity: 0,
    inventoryValue: 0,
    availableValue: 0,
    warehouseCount: 0,
    batchCount: 0,
    riskTypes: []
  },
  batchHighlights: [],
  productStructure: emptyStructure("unavailable"),
  recipeFormula: emptyRecipe("unavailable"),
  routingProcess: emptyRouting("unavailable"),
  sourceLineage: [],
  warnings: [],
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

const locale = defaultLanguage;

function asNumber(value?: number) {
  return Number.isFinite(value) ? Number(value) : 0;
}

function statusTone(statusCode?: string): StatusTone {
  const normalized = normalizeStatusCode(statusCode);
  if (normalized === "complete") {
    return "success";
  }
  if (normalized === "error") {
    return "danger";
  }
  if (normalized === "not_applicable") {
    return "info";
  }
  if (normalized === "partial" || normalized === "test_support" || normalized === "unavailable") {
    return "warning";
  }
  return "neutral";
}

function normalizeStatusCode(value?: string): ProductWip360StatusCode {
  if (
    value === "complete" ||
    value === "partial" ||
    value === "unavailable" ||
    value === "test_support" ||
    value === "error" ||
    value === "not_applicable"
  ) {
    return value;
  }
  if (value === "linked" || value === "ready") {
    return "complete";
  }
  if (value === "missing" || value === "unknown") {
    return "partial";
  }
  return "unavailable";
}

function statusLabel(statusCode?: string) {
  const labels: Record<ProductWip360StatusCode, string> = {
    complete: "完整",
    partial: "部分資料",
    unavailable: "目前不可用",
    test_support: "測試支援",
    error: "取得失敗",
    not_applicable: "不適用"
  };
  return labels[normalizeStatusCode(statusCode)];
}

function moduleLabel(moduleCode?: string) {
  const labels: Record<string, string> = {
    item: "Item",
    transactionItem: "Transaction Item",
    warehouse: "Warehouse / Inventory",
    bom: "BOM / Product Structure",
    recipe: "Recipe / Formula",
    routing: "Routing / Process Flow"
  };
  return labels[moduleCode ?? ""] ?? moduleCode ?? "Unknown Module";
}

function itemCategoryLabel(value?: number) {
  if (value === 5) {
    return "製成品";
  }
  if (value === 4) {
    return "在製品";
  }
  return "未分類";
}

function formatTimestamp(value?: number) {
  if (!value) {
    return "";
  }
  return new Date(value * 1000).toLocaleDateString(locale);
}

function unitLabel(unit?: number, explicit?: string) {
  return explicit || bomUnitLabel(unit, locale) || "";
}

function emptyStructure(statusCode: ProductWip360StatusCode): ProductWip360Structure {
  return {
    statusCode,
    statusLabel: statusLabel(statusCode),
    rootProductNo: "",
    rootProductVersion: 0,
    bomNo: "",
    bomVersionLabel: "",
    children: [],
    warnings: [],
    tone: statusTone(statusCode)
  };
}

function emptyRecipe(statusCode: ProductWip360StatusCode): ProductWip360Recipe {
  return {
    statusCode,
    statusLabel: statusLabel(statusCode),
    recipeNo: "",
    recipeVersionLabel: "",
    outputItemNo: "",
    outputQuantity: 0,
    outputUnitLabel: "",
    inputs: [],
    warnings: [],
    tone: statusTone(statusCode)
  };
}

function emptyRouting(statusCode: ProductWip360StatusCode): ProductWip360Routing {
  return {
    statusCode,
    statusLabel: statusLabel(statusCode),
    routingVersionId: "",
    routingVersionLabel: "",
    sourceLabel: "",
    steps: [],
    warnings: [],
    tone: statusTone(statusCode)
  };
}

function mapSubject(subject: ApiProductWip360Payload["subject"], query: ProductWip360Query): ProductWip360Subject | undefined {
  if (!subject?.itemNo && !query.itemNo) {
    return undefined;
  }
  const category = subject?.itemCategory ?? query.itemCategory;
  return {
    itemNo: subject?.itemNo ?? query.itemNo,
    itemName: subject?.itemName ?? "",
    itemCategory: category,
    itemCategoryLabel: subject?.itemCategoryLabel ?? itemCategoryLabel(category),
    identityType: category === 4 ? "wip" : category === 5 ? "product" : "unknown",
    identityTypeLabel: category === 4 ? "Standalone WIP" : category === 5 ? "Product" : "Unknown",
    versionLabel: subject?.versionLabel ?? (query.productVersion ? `V${query.productVersion}` : "未指定"),
    unitWarehouseLabel: subject?.unitWarehouseLabel ?? unitLabel(subject?.unitWarehouse),
    unitProductLabel: subject?.unitProductLabel ?? unitLabel(subject?.unitProduct),
    masterStatusLabel: subject?.masterStatusLabel ?? statusLabel(subject?.masterStatusCode),
    sourceLabel: subject?.sourceLabel ?? subject?.subjectSourceCode ?? "",
    tone: subject?.tone ?? statusTone(subject?.masterStatusCode ?? "complete")
  };
}

function mapModuleReadiness(item: ApiModuleReadiness): ProductWip360ModuleReadiness {
  const statusCode = normalizeStatusCode(item.statusCode);
  return {
    moduleCode: item.moduleCode ?? "",
    moduleLabel: moduleLabel(item.moduleCode),
    statusCode,
    statusLabel: statusLabel(statusCode),
    sourceLabel: item.sourceLabel ?? item.sourceCode ?? "",
    warningCodes: withFallbackArray<string>(item.warningCodes, []),
    tone: statusTone(statusCode)
  };
}

function mapTransactionItem(item: ApiTransactionItem): ProductWip360TransactionItem {
  const status = item.dataQualityCode ?? "complete";
  return {
    transItemNo: item.transItemNo ?? "",
    transItemName: item.transItemName ?? "",
    companyNo: item.companyNo ?? "",
    companyDisplayName: item.companyDisplayName ?? "",
    contractNo: item.contractNo ?? "",
    tradeUnitLabel: item.tradeUnitLabel ?? unitLabel(item.tradeUnit),
    tradePrice: asNumber(item.tradePrice),
    dataQualityLabel: item.dataQualityLabel ?? statusLabel(status),
    tone: statusTone(status)
  };
}

function mapInventoryOverview(value?: Partial<ProductWip360InventoryOverview>): ProductWip360InventoryOverview {
  return {
    hasStock: Boolean(value?.hasStock),
    currentQuantity: asNumber(value?.currentQuantity),
    availableQuantity: asNumber(value?.availableQuantity),
    reservedQuantity: asNumber(value?.reservedQuantity),
    qualityHoldQuantity: asNumber(value?.qualityHoldQuantity),
    inventoryValue: asNumber(value?.inventoryValue),
    availableValue: asNumber(value?.availableValue),
    warehouseCount: asNumber(value?.warehouseCount),
    batchCount: asNumber(value?.batchCount),
    riskTypes: withFallbackArray<string>(value?.riskTypes, [])
  };
}

function mapBatchHighlight(item: ApiBatchHighlight): ProductWip360BatchHighlight {
  const status = item.riskLevelCode ?? "complete";
  return {
    batchNo: item.batchNo ?? "",
    warehouseNo: item.warehouseNo ?? "",
    warehouseName: item.warehouseName ?? "",
    currentQuantity: asNumber(item.currentQuantity),
    availableQuantity: asNumber(item.availableQuantity),
    unitLabel: item.unitLabel ?? unitLabel(item.unit),
    validDateLabel: item.validDateLabel ?? formatTimestamp(item.validDate),
    riskLevelLabel: item.riskLevelLabel ?? statusLabel(status),
    sourceRefLabel: item.refNo ? `${item.refCategory ?? ""} ${item.refNo}`.trim() : "",
    tone: statusTone(status)
  };
}

function mapStructure(value?: ApiProductStructure): ProductWip360Structure {
  if (!value) {
    return emptyStructure("unavailable");
  }
  const statusCode = normalizeStatusCode(value.statusCode);
  return {
    statusCode,
    statusLabel: value.statusLabel ?? statusLabel(statusCode),
    rootProductNo: value.rootProductNo ?? "",
    rootProductVersion: asNumber(value.rootProductVersion),
    bomNo: value.bomNo ?? "",
    bomVersionLabel: value.bomVersionLabel ?? (value.bomVersion ? `V${value.bomVersion}` : ""),
    children: withFallbackArray<ApiStructureNode>(value.children, []).map(mapStructureNode),
    warnings: withFallbackArray<string>(value.warnings, []),
    tone: statusTone(statusCode)
  };
}

function mapStructureNode(item: ApiStructureNode, index: number): ProductWip360StructureNode {
  const level = asNumber(item.level);
  return {
    id: item.id ?? `${item.itemNo ?? "node"}-${index}`,
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    nodeTypeLabel: item.nodeTypeLabel ?? item.nodeTypeCode ?? "節點",
    quantity: asNumber(item.quantity),
    unitLabel: item.unitLabel ?? unitLabel(item.unit),
    level,
    tone: level === 0 ? "info" : "neutral"
  };
}

function mapRecipe(value?: ApiRecipeFormula): ProductWip360Recipe {
  if (!value) {
    return emptyRecipe("unavailable");
  }
  const statusCode = normalizeStatusCode(value.statusCode);
  return {
    statusCode,
    statusLabel: value.statusLabel ?? statusLabel(statusCode),
    recipeNo: value.recipeNo ?? "",
    recipeVersionLabel: value.recipeVersionLabel ?? (value.recipeVersion ? `V${value.recipeVersion}` : ""),
    outputItemNo: value.outputItemNo ?? "",
    outputQuantity: asNumber(value.outputQuantity),
    outputUnitLabel: value.outputUnitLabel ?? unitLabel(value.outputUnit),
    inputs: withFallbackArray<ApiRecipeInput>(value.inputs, []).map(mapRecipeInput),
    warnings: withFallbackArray<string>(value.warnings, []),
    tone: statusTone(statusCode)
  };
}

function mapRecipeInput(item: ApiRecipeInput): ProductWip360RecipeInput {
  return {
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    quantity: asNumber(item.quantity),
    weightRatio: asNumber(item.weightRatio),
    lossRate: asNumber(item.lossRate),
    unitLabel: item.unitLabel ?? unitLabel(item.unit)
  };
}

function mapRouting(value?: ApiRoutingProcess): ProductWip360Routing {
  if (!value) {
    return emptyRouting("unavailable");
  }
  const source = value.sourceLabel ?? value.sourceCode ?? "";
  const statusCode = source === "test_support" ? "test_support" : normalizeStatusCode(value.statusCode);
  return {
    statusCode,
    statusLabel: value.statusLabel ?? statusLabel(statusCode),
    routingVersionId: value.routingVersionId ?? "",
    routingVersionLabel: value.routingVersionLabel ?? (value.routingVersion ? `V${value.routingVersion}` : ""),
    sourceLabel: source,
    steps: withFallbackArray<ApiRoutingStep>(value.steps, []).map(mapRoutingStep),
    warnings: withFallbackArray<string>(value.warnings, []),
    tone: statusTone(statusCode)
  };
}

function mapRoutingStep(item: ApiRoutingStep): ProductWip360RoutingStep {
  return {
    stepNo: asNumber(item.stepNo ?? item.stepOrder),
    stageLabel: item.stageLabel ?? "待確認",
    groupLabel: item.groupLabel ?? "待確認",
    processLabel: item.processLabel ?? item.processName ?? "未命名製程",
    recipeRefLabel: item.recipeRefLabel ?? item.recipeNo ?? "未提供",
    resourceLabel: item.resourceLabel ?? item.resourceEligibilityLabel ?? "待確認",
    standardRateLabel: item.standardRateLabel ?? "待確認",
    tone: item.resourceLabel || item.resourceEligibilityLabel ? "neutral" : "warning"
  };
}

function mapLineage(value?: ApiProductWip360Payload["sourceLineage"]): ProductWip360Lineage[] {
  if (Array.isArray(value)) {
    return value.map((item) => {
      const status = normalizeStatusCode(item.statusCode);
      return {
        moduleLabel: item.moduleLabel ?? moduleLabel(item.moduleCode),
        sourceLabel: item.sourceLabel ?? item.sourceCode ?? "",
        statusLabel: item.statusLabel ?? statusLabel(status),
        tone: statusTone(status)
      };
    });
  }
  if (!value) {
    return [];
  }
  return Object.entries(value)
    .filter(([, source]) => Boolean(source))
    .map(([key, source]) => ({
      moduleLabel: key,
      sourceLabel: String(source),
      statusLabel: String(source) === "test_support" ? "測試支援" : "read-only",
      tone: String(source) === "test_support" ? "warning" : "success"
    }));
}

function warningMessage(code: string) {
  const messages: Record<string, string> = {
    test_support_only: "目前資料來自非正式 Shared DEV test-support read-only surface。",
    resource_eligibility_not_governed: "資源資格尚未建立治理來源。",
    missing_standard_performance: "標準表現尚未建立治理來源。",
    wip_product_structure_not_governed: "Standalone WIP 的產品結構 root 尚未建立正式治理來源。",
    wip_recipe_formula_not_governed: "Standalone WIP 的 Recipe / Formula output root 尚未建立正式治理來源。",
    standalone_wip_routing_not_available: "尚無獨立 WIP Routing Version evidence。",
    identity_name_mismatch: "跨模組品項名稱不一致，需回到 domain page 追查。",
    identity_category_mismatch: "跨模組品項類別不一致，需回到 domain page 追查。"
  };
  return messages[code] ?? "Product / WIP 360 資料需確認。";
}

function mapWarning(item: ApiWarning): ProductWip360Warning {
  const code = item.warningCode ?? item.code ?? "unknown";
  const tone = code === "not_applicable" ? "info" : "warning";
  return {
    moduleLabel: item.moduleLabel ?? moduleLabel(item.moduleCode),
    code,
    message: item.message ?? warningMessage(code),
    refNo: item.refNo ?? "",
    tone
  };
}

function mapPayload(payload: ApiProductWip360Payload, query: ProductWip360Query): ProductWip360OverviewData {
  const requestIdentity = {
    ...query,
    ...payload.requestIdentity,
    itemNo: payload.requestIdentity?.itemNo ?? query.itemNo,
    itemCategory: (payload.requestIdentity?.itemCategory ?? query.itemCategory) as 4 | 5
  };
  const capabilityBoundary = {
    ...emptyProductWip360OverviewData.capabilityBoundary,
    ...(payload.capabilityBoundary ?? {})
  };
  return {
    requestIdentity,
    subject: mapSubject(payload.subject, requestIdentity),
    moduleReadiness: withFallbackArray<ApiModuleReadiness>(payload.moduleReadiness, []).map(mapModuleReadiness),
    transactionItems: withFallbackArray<ApiTransactionItem>(payload.transactionContext?.transactionItems, []).map(mapTransactionItem),
    inventoryOverview: mapInventoryOverview(payload.inventoryOverview),
    batchHighlights: withFallbackArray<ApiBatchHighlight>(payload.batchHighlights, []).map(mapBatchHighlight),
    productStructure: mapStructure(payload.productStructure),
    recipeFormula: mapRecipe(payload.recipeFormula),
    routingProcess: mapRouting(payload.routingProcess),
    sourceLineage: mapLineage(payload.sourceLineage),
    warnings: withFallbackArray<ApiWarning>(payload.warnings, []).map(mapWarning),
    capabilityBoundary: {
      readOnly: Boolean(capabilityBoundary.readOnly),
      productWriteSupported: Boolean(capabilityBoundary.productWriteSupported),
      bomWriteSupported: Boolean(capabilityBoundary.bomWriteSupported),
      recipeWriteSupported: Boolean(capabilityBoundary.recipeWriteSupported),
      routingWriteSupported: Boolean(capabilityBoundary.routingWriteSupported),
      workflowMutationSupported: Boolean(capabilityBoundary.workflowMutationSupported),
      sourceOfTruthTransitionSupported: Boolean(capabilityBoundary.sourceOfTruthTransitionSupported)
    }
  };
}

function buildOverviewPath(query: ProductWip360Query) {
  const params = new URLSearchParams();
  params.set("itemNo", query.itemNo);
  params.set("itemCategory", String(query.itemCategory));
  if (query.effectiveDate !== undefined) {
    params.set("effectiveDate", String(query.effectiveDate));
  }
  if (query.inventoryDate !== undefined) {
    params.set("inventoryDate", String(query.inventoryDate));
  }
  if (query.productVersion !== undefined) {
    params.set("productVersion", String(query.productVersion));
  }
  return `/api/v2/product-wip-360/overview?${params.toString()}`;
}

export async function getProductWip360Overview(
  query: ProductWip360Query,
  dataSourceMode: DataSourceMode = "api"
): Promise<ProductWip360Result> {
  if (dataSourceMode === "mock") {
    return {
      data: productWip360Mock(query.itemCategory),
      source: "mock"
    };
  }

  try {
    const payload = await apiGet<ApiProductWip360Payload>(buildOverviewPath(query));
    return {
      data: mapPayload(payload, query),
      source: "api"
    };
  } catch (error) {
    return {
      data: {
        ...emptyProductWip360OverviewData,
        requestIdentity: query
      },
      source: "api",
      error: error instanceof Error ? error.message : "Product / WIP 360 API unavailable"
    };
  }
}
