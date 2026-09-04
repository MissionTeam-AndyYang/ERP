import type { StatusTone } from "@/types/dashboard";

export type ProductWip360DataSource = "api" | "mock";
export type ProductWip360IdentityType = "product" | "wip" | "unknown";
export type ProductWip360StatusCode = "complete" | "partial" | "unavailable" | "test_support" | "error" | "not_applicable";

export type ProductWip360Query = {
  itemNo: string;
  itemCategory: 4 | 5;
  effectiveDate?: number;
  inventoryDate?: number;
  productVersion?: number;
};

export type ProductWip360Subject = {
  itemNo: string;
  itemName: string;
  itemCategory: number;
  itemCategoryLabel: string;
  identityType: ProductWip360IdentityType;
  identityTypeLabel: string;
  versionLabel: string;
  unitWarehouseLabel: string;
  unitProductLabel: string;
  masterStatusLabel: string;
  sourceLabel: string;
  tone: StatusTone;
};

export type ProductWip360ModuleReadiness = {
  moduleCode: string;
  moduleLabel: string;
  statusCode: ProductWip360StatusCode;
  statusLabel: string;
  sourceLabel: string;
  warningCodes: string[];
  tone: StatusTone;
};

export type ProductWip360TransactionItem = {
  transItemNo: string;
  transItemName: string;
  companyNo: string;
  companyDisplayName: string;
  contractNo: string;
  tradeUnitLabel: string;
  tradePrice: number;
  dataQualityLabel: string;
  tone: StatusTone;
};

export type ProductWip360InventoryOverview = {
  hasStock: boolean;
  currentQuantity: number;
  availableQuantity: number;
  reservedQuantity: number;
  qualityHoldQuantity: number;
  inventoryValue: number;
  availableValue: number;
  warehouseCount: number;
  batchCount: number;
  riskTypes: string[];
};

export type ProductWip360BatchHighlight = {
  batchNo: string;
  warehouseNo: string;
  warehouseName: string;
  currentQuantity: number;
  availableQuantity: number;
  unitLabel: string;
  validDateLabel: string;
  riskLevelLabel: string;
  sourceRefLabel: string;
  tone: StatusTone;
};

export type ProductWip360StructureNode = {
  id: string;
  itemNo: string;
  itemName: string;
  nodeTypeLabel: string;
  quantity: number;
  unitLabel: string;
  level: number;
  tone: StatusTone;
};

export type ProductWip360Structure = {
  statusCode: ProductWip360StatusCode;
  statusLabel: string;
  rootProductNo: string;
  rootProductVersion: number;
  bomNo: string;
  bomVersionLabel: string;
  children: ProductWip360StructureNode[];
  warnings: string[];
  tone: StatusTone;
};

export type ProductWip360RecipeInput = {
  itemNo: string;
  itemName: string;
  quantity: number;
  weightRatio: number;
  lossRate: number;
  unitLabel: string;
};

export type ProductWip360Recipe = {
  statusCode: ProductWip360StatusCode;
  statusLabel: string;
  recipeNo: string;
  recipeVersionLabel: string;
  outputItemNo: string;
  outputQuantity: number;
  outputUnitLabel: string;
  inputs: ProductWip360RecipeInput[];
  warnings: string[];
  tone: StatusTone;
};

export type ProductWip360RoutingStep = {
  stepNo: number;
  stageLabel: string;
  groupLabel: string;
  processLabel: string;
  recipeRefLabel: string;
  resourceLabel: string;
  standardRateLabel: string;
  tone: StatusTone;
};

export type ProductWip360Routing = {
  statusCode: ProductWip360StatusCode;
  statusLabel: string;
  routingVersionId: string;
  routingVersionLabel: string;
  sourceLabel: string;
  steps: ProductWip360RoutingStep[];
  warnings: string[];
  tone: StatusTone;
};

export type ProductWip360Lineage = {
  moduleLabel: string;
  sourceLabel: string;
  statusLabel: string;
  tone: StatusTone;
};

export type ProductWip360Warning = {
  moduleLabel: string;
  code: string;
  message: string;
  refNo: string;
  tone: StatusTone;
};

export type ProductWip360CapabilityBoundary = {
  readOnly: boolean;
  productWriteSupported: boolean;
  bomWriteSupported: boolean;
  recipeWriteSupported: boolean;
  routingWriteSupported: boolean;
  workflowMutationSupported: boolean;
  sourceOfTruthTransitionSupported: boolean;
};

export type ProductWip360OverviewData = {
  requestIdentity: ProductWip360Query;
  subject?: ProductWip360Subject;
  moduleReadiness: ProductWip360ModuleReadiness[];
  transactionItems: ProductWip360TransactionItem[];
  inventoryOverview: ProductWip360InventoryOverview;
  batchHighlights: ProductWip360BatchHighlight[];
  productStructure: ProductWip360Structure;
  recipeFormula: ProductWip360Recipe;
  routingProcess: ProductWip360Routing;
  sourceLineage: ProductWip360Lineage[];
  warnings: ProductWip360Warning[];
  capabilityBoundary: ProductWip360CapabilityBoundary;
};
