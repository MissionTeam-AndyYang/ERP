import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { defaultLanguage } from "@/i18n/dictionary";
import { bomUnitLabel } from "@/i18n/bom-enums";
import { recipeFormulaDashboardMock, recipeFormulaDetailMock } from "@/mock/recipe";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type {
  RecipeFormulaDashboardData,
  RecipeFormulaDataSource,
  RecipeFormulaDetail,
  RecipeFormulaInput,
  RecipeFormulaKpi,
  RecipeFormulaLineage,
  RecipeFormulaListItem,
  RecipeFormulaOutput,
  RecipeFormulaReference,
  RecipeFormulaStatusCode,
  RecipeFormulaSummary,
  RecipeFormulaVersion,
  RecipeFormulaWarning
} from "@/types/recipe";

type ApiRecipeFormulaDashboardPayload = {
  summary?: Partial<RecipeFormulaSummary>;
  recipes?: ApiRecipeFormulaListItem[];
  items?: ApiRecipeFormulaListItem[];
  total?: number;
  start?: number;
  count?: number;
};

type ApiRecipeFormulaListItem = {
  id?: string;
  recipeNo?: string;
  recipeName?: string;
  productNo?: string;
  productName?: string;
  currentVersion?: number;
  version?: number;
  statusCode?: string;
  recipeStatusCode?: string;
  inputCount?: number;
  warningCount?: number;
  owner?: string;
  sourceLabel?: string;
};

type ApiRecipeFormulaCompositionPayload = {
  recipe?: ApiRecipeFormulaListItem;
  versions?: ApiRecipeFormulaVersion[];
  inputs?: ApiRecipeFormulaInput[];
  output?: ApiRecipeFormulaOutput;
  definedOutput?: ApiRecipeFormulaOutput;
  lineage?: ApiRecipeFormulaLineage[];
  sourceLineage?: ApiRecipeFormulaLineage[];
  warnings?: ApiRecipeFormulaWarning[];
  productStructureReferences?: ApiRecipeFormulaReference[];
  routingReferences?: ApiRecipeFormulaReference[];
  references?: {
    productStructure?: ApiRecipeFormulaReference[];
    routing?: ApiRecipeFormulaReference[];
  };
};

type ApiRecipeFormulaVersion = {
  version?: number;
  statusCode?: string;
  recipeStatusCode?: string;
  effectiveDate?: string;
  date?: string;
};

type ApiRecipeFormulaInput = {
  lineNo?: string | number;
  itemNo?: string;
  itemName?: string;
  itemCategory?: number;
  itemCategoryLabel?: string;
  processStageCode?: string;
  processStageLabel?: string;
  quantity?: number;
  inputQuantity?: number;
  weight?: number;
  inputWeight?: number;
  unit?: string | number;
  unitCode?: number;
  weightRatio?: number;
  inputLossRate?: number;
  lossRate?: number;
  sourceRef?: string;
};

type ApiRecipeFormulaOutput = {
  itemNo?: string;
  itemName?: string;
  outputTypeCode?: string;
  outputTypeLabel?: string;
  quantity?: number;
  outputQuantity?: number;
  weight?: number;
  outputWeight?: number;
  unit?: string | number;
  unitCode?: number;
  yieldRate?: number;
};

type ApiRecipeFormulaLineage = {
  sourceType?: string;
  sourceTypeLabel?: string;
  sourceRef?: string;
  evidenceLabel?: string;
  statusLabel?: string;
};

type ApiRecipeFormulaWarning = {
  code?: string;
  warningCode?: string;
  message?: string;
  refNo?: string;
};

type ApiRecipeFormulaReference = {
  type?: string;
  typeLabel?: string;
  refNo?: string;
  refName?: string;
  statusLabel?: string;
};

export type RecipeFormulaDashboardQuery = {
  keyword?: string;
  start?: number;
  count?: number;
};

export type RecipeFormulaDashboardResult = {
  data: RecipeFormulaDashboardData;
  source: RecipeFormulaDataSource;
  error?: string;
};

export type RecipeFormulaDetailResult = {
  detail?: RecipeFormulaDetail;
  source: RecipeFormulaDataSource;
  error?: string;
};

const locale = defaultLanguage;

export const emptyRecipeFormulaDashboardData: RecipeFormulaDashboardData = {
  summary: {
    recipeCount: 0,
    versionCount: 0,
    effectiveVersionCount: 0,
    warningCount: 0
  },
  kpis: [
    { label: "Recipe 定義", value: "0", hint: "API 尚未提供資料", tone: "info" },
    { label: "版本總數", value: "0", hint: "API 尚未提供資料", tone: "neutral" },
    { label: "目前有效", value: "0", hint: "API 尚未提供資料", tone: "success" },
    { label: "待確認", value: "0", hint: "API 尚未提供資料", tone: "warning" }
  ],
  recipes: [],
  total: 0,
  start: 0,
  count: 0
};

function asNumber(value?: number) {
  return Number.isFinite(value) ? Number(value) : 0;
}

function formatInteger(value?: number) {
  return new Intl.NumberFormat(locale, { maximumFractionDigits: 0 }).format(value ?? 0);
}

function normalizeStatusCode(value?: string): RecipeFormulaStatusCode {
  if (value === "effective" || value === "draft" || value === "future" || value === "historical" || value === "warning") {
    return value;
  }
  return "unknown";
}

function statusLabel(value?: string) {
  const code = normalizeStatusCode(value);
  const labels: Record<RecipeFormulaStatusCode, string> = {
    effective: "目前有效",
    draft: "草稿",
    future: "未來生效",
    historical: "歷史版本",
    warning: "待確認",
    unknown: "待確認"
  };
  return labels[code];
}

function statusTone(value?: string) {
  const code = normalizeStatusCode(value);
  if (code === "effective") {
    return "success" as const;
  }
  if (code === "future") {
    return "info" as const;
  }
  if (code === "historical") {
    return "neutral" as const;
  }
  return "warning" as const;
}

function itemCategoryLabel(value?: number, explicit?: string) {
  if (explicit) {
    return explicit;
  }
  const labels: Record<number, string> = {
    1: "原料",
    2: "物料",
    3: "膠捲",
    4: "在製品",
    5: "製成品",
    6: "貨品"
  };
  return labels[value ?? 0] ?? "未分類";
}

function processStageLabel(value?: string, explicit?: string) {
  if (explicit) {
    return explicit;
  }
  const normalized = String(value ?? "").toLocaleLowerCase();
  const labels: Record<string, string> = {
    pre_prep: "前備",
    preprep: "前備",
    processing: "加工",
    packaging: "包裝"
  };
  return labels[normalized] ?? "未指定";
}

function unitLabel(unit?: string | number, unitCode?: number) {
  if (typeof unit === "string" && unit.trim()) {
    return unit;
  }
  return bomUnitLabel(unitCode ?? (typeof unit === "number" ? unit : undefined), locale);
}

function normalizeSummary(summary?: Partial<RecipeFormulaSummary>): RecipeFormulaSummary {
  return {
    recipeCount: asNumber(summary?.recipeCount),
    versionCount: asNumber(summary?.versionCount),
    effectiveVersionCount: asNumber(summary?.effectiveVersionCount),
    warningCount: asNumber(summary?.warningCount)
  };
}

function kpisFromSummary(summary: RecipeFormulaSummary): RecipeFormulaKpi[] {
  return [
    { label: "Recipe 定義", value: formatInteger(summary.recipeCount), hint: "受治理的配方定義", tone: "info" },
    { label: "版本總數", value: formatInteger(summary.versionCount), hint: "目前查詢條件下的版本", tone: "neutral" },
    { label: "目前有效", value: formatInteger(summary.effectiveVersionCount), hint: "可作 read-only 引用", tone: "success" },
    { label: "待確認", value: formatInteger(summary.warningCount), hint: "存在來源或重量警示", tone: "warning" }
  ];
}

function mapRecipeListItem(item: ApiRecipeFormulaListItem): RecipeFormulaListItem {
  const statusCode = normalizeStatusCode(item.statusCode ?? item.recipeStatusCode);
  const recipeNo = item.recipeNo ?? "";
  const currentVersion = asNumber(item.currentVersion ?? item.version);
  return {
    id: item.id ?? `${recipeNo || "recipe"}-v${currentVersion}`,
    recipeNo,
    recipeName: item.recipeName ?? "",
    productNo: item.productNo ?? "",
    productName: item.productName ?? "",
    currentVersion,
    statusCode,
    statusLabel: statusLabel(statusCode),
    tone: statusTone(statusCode),
    inputCount: asNumber(item.inputCount),
    warningCount: asNumber(item.warningCount),
    owner: item.owner ?? "未提供",
    sourceLabel: item.sourceLabel ?? "未提供"
  };
}

function mapVersion(version: ApiRecipeFormulaVersion): RecipeFormulaVersion {
  const statusCode = normalizeStatusCode(version.statusCode ?? version.recipeStatusCode);
  return {
    version: asNumber(version.version),
    statusCode,
    statusLabel: statusLabel(statusCode),
    tone: statusTone(statusCode),
    effectiveDate: version.effectiveDate ?? version.date ?? ""
  };
}

function mapInput(input: ApiRecipeFormulaInput): RecipeFormulaInput {
  return {
    lineNo: String(input.lineNo ?? ""),
    itemNo: input.itemNo ?? "",
    itemName: input.itemName ?? "",
    itemCategoryLabel: itemCategoryLabel(input.itemCategory, input.itemCategoryLabel),
    processStageLabel: processStageLabel(input.processStageCode, input.processStageLabel),
    quantity: asNumber(input.inputQuantity ?? input.quantity),
    weight: asNumber(input.inputWeight ?? input.weight),
    unit: unitLabel(input.unit, input.unitCode),
    weightRatio: asNumber(input.weightRatio),
    inputLossRate: asNumber(input.inputLossRate ?? input.lossRate),
    sourceRef: input.sourceRef ?? ""
  };
}

function mapOutput(output?: ApiRecipeFormulaOutput): RecipeFormulaOutput | undefined {
  if (!output) {
    return undefined;
  }
  return {
    itemNo: output.itemNo ?? "",
    itemName: output.itemName ?? "",
    outputTypeLabel: output.outputTypeLabel ?? "唯一定義產出",
    quantity: asNumber(output.outputQuantity ?? output.quantity),
    weight: asNumber(output.outputWeight ?? output.weight),
    unit: unitLabel(output.unit, output.unitCode),
    yieldRate: asNumber(output.yieldRate)
  };
}

function mapLineage(lineage: ApiRecipeFormulaLineage): RecipeFormulaLineage {
  return {
    sourceTypeLabel: lineage.sourceTypeLabel ?? lineage.sourceType ?? "來源",
    sourceRef: lineage.sourceRef ?? "",
    evidenceLabel: lineage.evidenceLabel ?? "未提供",
    statusLabel: lineage.statusLabel ?? "待確認"
  };
}

function mapWarning(warning: ApiRecipeFormulaWarning): RecipeFormulaWarning {
  const code = warning.code ?? warning.warningCode ?? "unknown";
  const messages: Record<string, string> = {
    unresolved_weight_basis: "重量基準尚未確認。",
    missing_defined_output: "尚未提供唯一定義產出。",
    multiple_defined_outputs: "回傳包含多個定義產出，需後端確認。",
    missing_input: "尚未提供配方輸入項目。",
    unknown: "Recipe / Formula 資料需確認。"
  };
  return {
    code,
    message: warning.message ?? messages[code] ?? messages.unknown,
    refNo: warning.refNo ?? ""
  };
}

function mapReference(reference: ApiRecipeFormulaReference): RecipeFormulaReference {
  return {
    typeLabel: reference.typeLabel ?? reference.type ?? "參照",
    refNo: reference.refNo ?? "",
    refName: reference.refName ?? "",
    statusLabel: reference.statusLabel ?? "參照中"
  };
}

function mapDashboardPayload(payload: ApiRecipeFormulaDashboardPayload): RecipeFormulaDashboardData {
  const summary = normalizeSummary(payload.summary);
  const recipes = withFallbackArray<ApiRecipeFormulaListItem>(payload.recipes ?? payload.items, []).map(mapRecipeListItem);
  return {
    summary,
    kpis: kpisFromSummary(summary),
    recipes,
    total: payload.total ?? recipes.length,
    start: payload.start ?? 0,
    count: payload.count ?? recipes.length
  };
}

function mapCompositionPayload(
  payload: ApiRecipeFormulaCompositionPayload,
  fallback?: RecipeFormulaListItem
): RecipeFormulaDetail | undefined {
  const recipe = payload.recipe ? mapRecipeListItem(payload.recipe) : fallback;
  if (!recipe?.recipeNo) {
    return undefined;
  }
  return {
    recipe,
    versions: withFallbackArray<ApiRecipeFormulaVersion>(payload.versions, []).map(mapVersion),
    inputs: withFallbackArray<ApiRecipeFormulaInput>(payload.inputs, []).map(mapInput),
    output: mapOutput(payload.definedOutput ?? payload.output),
    lineage: withFallbackArray<ApiRecipeFormulaLineage>(payload.sourceLineage ?? payload.lineage, []).map(mapLineage),
    warnings: withFallbackArray<ApiRecipeFormulaWarning>(payload.warnings, []).map(mapWarning),
    productStructureReferences: withFallbackArray<ApiRecipeFormulaReference>(
      payload.productStructureReferences ?? payload.references?.productStructure,
      []
    ).map(mapReference),
    routingReferences: withFallbackArray<ApiRecipeFormulaReference>(
      payload.routingReferences ?? payload.references?.routing,
      []
    ).map(mapReference)
  };
}

function buildDashboardPath(query: RecipeFormulaDashboardQuery = {}) {
  const params = new URLSearchParams();
  if (query.keyword) {
    params.set("keyword", query.keyword);
  }
  if (query.start !== undefined) {
    params.set("start", String(query.start));
  }
  params.set("count", String(query.count ?? 50));
  return `/api/v2/recipe-formula/dashboard?${params.toString()}`;
}

export async function getRecipeFormulaDashboard(
  query: RecipeFormulaDashboardQuery = {},
  dataSourceMode: DataSourceMode = "api"
): Promise<RecipeFormulaDashboardResult> {
  if (dataSourceMode === "mock") {
    return {
      data: recipeFormulaDashboardMock,
      source: "mock"
    };
  }

  try {
    const payload = await apiGet<ApiRecipeFormulaDashboardPayload>(buildDashboardPath(query));
    return {
      data: mapDashboardPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: emptyRecipeFormulaDashboardData,
      source: "api",
      error: error instanceof Error ? error.message : "Recipe / Formula API unavailable"
    };
  }
}

export async function getRecipeFormulaComposition(
  recipeNo: string,
  version: number,
  fallback?: RecipeFormulaListItem,
  dataSourceMode: DataSourceMode = "api"
): Promise<RecipeFormulaDetailResult> {
  if (dataSourceMode === "mock") {
    return {
      detail:
        recipeFormulaDetailMock[recipeNo] ??
        (fallback ? { recipe: fallback, versions: [], inputs: [], lineage: [], warnings: [], productStructureReferences: [], routingReferences: [] } : undefined),
      source: "mock"
    };
  }

  try {
    const payload = await apiGet<ApiRecipeFormulaCompositionPayload>(
      `/api/v2/recipe-formula/${encodeURIComponent(recipeNo)}/versions/${encodeURIComponent(String(version))}/composition`
    );
    return {
      detail: mapCompositionPayload(payload, fallback),
      source: "api"
    };
  } catch (error) {
    return {
      detail: fallback
        ? { recipe: fallback, versions: [], inputs: [], lineage: [], warnings: [], productStructureReferences: [], routingReferences: [] }
        : undefined,
      source: "api",
      error: error instanceof Error ? error.message : "Recipe / Formula composition API unavailable"
    };
  }
}
