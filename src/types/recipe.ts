import type { StatusTone } from "@/types/dashboard";

export type RecipeFormulaDataSource = "api" | "mock";

export type RecipeFormulaStatusCode = "effective" | "draft" | "future" | "historical" | "warning" | "unknown";

export type RecipeFormulaSummary = {
  recipeCount: number;
  versionCount: number;
  effectiveVersionCount: number;
  warningCount: number;
};

export type RecipeFormulaKpi = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type RecipeFormulaListItem = {
  id: string;
  recipeNo: string;
  recipeName: string;
  productNo: string;
  productName: string;
  currentVersion: number;
  statusCode: RecipeFormulaStatusCode;
  statusLabel: string;
  tone: StatusTone;
  inputCount: number;
  warningCount: number;
  owner: string;
  sourceLabel: string;
};

export type RecipeFormulaDashboardData = {
  summary: RecipeFormulaSummary;
  kpis: RecipeFormulaKpi[];
  recipes: RecipeFormulaListItem[];
  total: number;
  start: number;
  count: number;
};

export type RecipeFormulaVersion = {
  version: number;
  statusCode: RecipeFormulaStatusCode;
  statusLabel: string;
  tone: StatusTone;
  effectiveDate: string;
};

export type RecipeFormulaInput = {
  lineNo: string;
  itemNo: string;
  itemName: string;
  itemCategoryLabel: string;
  processStageLabel: string;
  quantity: number;
  weight: number;
  unit: string;
  weightRatio: number;
  inputLossRate: number;
  sourceRef: string;
};

export type RecipeFormulaOutput = {
  itemNo: string;
  itemName: string;
  outputTypeLabel: string;
  quantity: number;
  weight: number;
  unit: string;
  yieldRate: number;
};

export type RecipeFormulaLineage = {
  sourceTypeLabel: string;
  sourceRef: string;
  evidenceLabel: string;
  statusLabel: string;
};

export type RecipeFormulaWarning = {
  code: string;
  message: string;
  refNo: string;
};

export type RecipeFormulaReference = {
  typeLabel: string;
  refNo: string;
  refName: string;
  statusLabel: string;
};

export type RecipeFormulaDetail = {
  recipe: RecipeFormulaListItem;
  versions: RecipeFormulaVersion[];
  inputs: RecipeFormulaInput[];
  output?: RecipeFormulaOutput;
  lineage: RecipeFormulaLineage[];
  warnings: RecipeFormulaWarning[];
  productStructureReferences: RecipeFormulaReference[];
  routingReferences: RecipeFormulaReference[];
};
