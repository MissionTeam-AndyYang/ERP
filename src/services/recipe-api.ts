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
  recipeVersion?: number;
  versionStateCode?: string;
  formulaStatusCode?: string;
  dateTimestamp?: number;
  weight?: number;
  unit?: string | number;
  warningCodes?: string[];
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
  version?: ApiRecipeFormulaVersion;
  formula?: {
    recipeNo?: string;
    recipeVersion?: number;
    formulaStatusCode?: string;
    weight?: number;
    unit?: string | number;
    weightSourceCode?: string;
  };
  versions?: ApiRecipeFormulaVersion[];
  inputs?: ApiRecipeFormulaInput[];
  output?: ApiRecipeFormulaOutput;
  definedOutput?: ApiRecipeFormulaOutput;
  lineage?: ApiRecipeFormulaLineage[];
  sourceLineage?: ApiRecipeFormulaLineage[] | ApiRecipeFormulaSourceLineage;
  warnings?: ApiRecipeFormulaWarning[];
  productStructureReferences?: ApiRecipeFormulaReference[];
  routingReferences?: ApiRecipeFormulaReference[];
  references?: {
    productStructure?: ApiRecipeFormulaReference[];
    routing?: ApiRecipeFormulaReference[];
  };
};

type ApiRecipeFormulaVersion = {
  recipeVersion?: number;
  versionStateCode?: string;
  dateTimestamp?: number;
  weight?: number;
  unit?: string | number;
  version?: number;
  statusCode?: string;
  recipeStatusCode?: string;
  effectiveDate?: string;
  date?: string;
};

type ApiRecipeFormulaInput = {
  lineNo?: string | number;
  inputNo?: string;
  inputName?: string;
  inputCategory?: number;
  inputSubCategory?: number;
  lossSourceCode?: string;
  weightSourceCode?: string;
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
  outputNo?: string;
  outputName?: string;
  outputCategory?: number;
  productVersion?: number;
  sourceCode?: string;
  weightSourceCode?: string;
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

type ApiRecipeFormulaSourceLineage = {
  recipeSourceCode?: string;
  inputSourceCode?: string;
  outputSourceCode?: string;
  productStructureReference?: {
    productNo?: string;
    productVersion?: number;
    bomNo?: string;
    bomVersion?: number;
  };
  routingContextRefs?: ApiRecipeFormulaReference[];
  productionObservationRefs?: ApiRecipeFormulaReference[];
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
  if (value === "complete") {
    return "effective";
  }
  if (value === "partial" || value === "missing") {
    return "warning";
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
  const warningCount =
    summary?.warningCount ??
    asNumber((summary as { partialFormulaCount?: number } | undefined)?.partialFormulaCount) +
      asNumber((summary as { missingFormulaCount?: number } | undefined)?.missingFormulaCount);
  return {
    recipeCount: asNumber(summary?.recipeCount),
    versionCount: asNumber(summary?.versionCount),
    effectiveVersionCount: asNumber(
      summary?.effectiveVersionCount ?? (summary as { completeFormulaCount?: number } | undefined)?.completeFormulaCount
    ),
    warningCount: asNumber(warningCount)
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
  const statusCode = normalizeStatusCode(item.statusCode ?? item.recipeStatusCode ?? item.versionStateCode ?? item.formulaStatusCode);
  const recipeNo = item.recipeNo ?? "";
  const currentVersion = asNumber(item.currentVersion ?? item.version ?? item.recipeVersion);
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
    warningCount: asNumber(item.warningCount ?? item.warningCodes?.length),
    owner: item.owner ?? "未提供",
    sourceLabel: item.sourceLabel ?? (item.formulaStatusCode ? formulaStatusLabel(item.formulaStatusCode) : "未提供")
  };
}

function mapVersion(version: ApiRecipeFormulaVersion): RecipeFormulaVersion {
  const statusCode = normalizeStatusCode(version.statusCode ?? version.recipeStatusCode ?? version.versionStateCode);
  return {
    version: asNumber(version.version ?? version.recipeVersion),
    statusCode,
    statusLabel: statusLabel(statusCode),
    tone: statusTone(statusCode),
    effectiveDate: version.effectiveDate ?? version.date ?? formatTimestamp(version.dateTimestamp)
  };
}

function mapInput(input: ApiRecipeFormulaInput): RecipeFormulaInput {
  return {
    lineNo: String(input.lineNo ?? ""),
    itemNo: input.itemNo ?? input.inputNo ?? "",
    itemName: input.itemName ?? input.inputName ?? "",
    itemCategoryLabel: itemCategoryLabel(input.itemCategory ?? input.inputCategory, input.itemCategoryLabel),
    processStageLabel: processStageLabel(input.processStageCode, input.processStageLabel),
    quantity: asNumber(input.inputQuantity ?? input.quantity),
    weight: asNumber(input.inputWeight ?? input.weight),
    unit: unitLabel(input.unit, input.unitCode),
    weightRatio: asNumber(input.weightRatio),
    inputLossRate: asNumber(input.inputLossRate ?? input.lossRate),
    sourceRef: input.sourceRef ?? input.weightSourceCode ?? input.lossSourceCode ?? ""
  };
}

function mapOutput(output?: ApiRecipeFormulaOutput): RecipeFormulaOutput | undefined {
  if (!output) {
    return undefined;
  }
  return {
    itemNo: output.itemNo ?? output.outputNo ?? "",
    itemName: output.itemName ?? output.outputName ?? "",
    outputTypeLabel: output.outputTypeLabel ?? "唯一定義產出",
    quantity: asNumber(output.outputQuantity ?? output.quantity),
    weight: asNumber(output.outputWeight ?? output.weight),
    unit: unitLabel(output.unit, output.unitCode),
    yieldRate: asNumber(output.yieldRate)
  };
}

function formulaStatusLabel(value?: string) {
  const labels: Record<string, string> = {
    complete: "Formula 完整",
    partial: "Formula 待確認",
    missing: "Formula 缺漏",
    unknown: "Formula 待確認"
  };
  return labels[String(value ?? "unknown").toLocaleLowerCase()] ?? labels.unknown;
}

function formatTimestamp(value?: number) {
  if (!value) {
    return "";
  }
  return new Date(value * 1000).toLocaleDateString(locale);
}

function mapLineage(lineage: ApiRecipeFormulaLineage): RecipeFormulaLineage {
  return {
    sourceTypeLabel: lineage.sourceTypeLabel ?? lineage.sourceType ?? "來源",
    sourceRef: lineage.sourceRef ?? "",
    evidenceLabel: lineage.evidenceLabel ?? "未提供",
    statusLabel: lineage.statusLabel ?? "待確認"
  };
}

function mapSourceLineage(lineage?: ApiRecipeFormulaLineage[] | ApiRecipeFormulaSourceLineage): RecipeFormulaLineage[] {
  if (Array.isArray(lineage)) {
    return lineage.map(mapLineage);
  }
  if (!lineage) {
    return [];
  }
  return [
    {
      sourceTypeLabel: "Recipe 定義來源",
      sourceRef: lineage.recipeSourceCode ?? "",
      evidenceLabel: "Recipe definition evidence",
      statusLabel: "read-only"
    },
    {
      sourceTypeLabel: "Formula input 來源",
      sourceRef: lineage.inputSourceCode ?? "",
      evidenceLabel: "Formula input evidence",
      statusLabel: "read-only"
    },
    {
      sourceTypeLabel: "定義產出來源",
      sourceRef: lineage.outputSourceCode ?? "",
      evidenceLabel: "Formula output evidence",
      statusLabel: "read-only"
    }
  ].filter((item) => item.sourceRef);
}

function mapWarning(warning: ApiRecipeFormulaWarning): RecipeFormulaWarning {
  const code = warning.code ?? warning.warningCode ?? "unknown";
  const messages: Record<string, string> = {
    unresolved_weight_basis: "重量基準尚未確認。",
    missing_defined_output: "尚未提供唯一定義產出。",
    multiple_defined_outputs: "回傳包含多個定義產出，需後端確認。",
    missing_input: "尚未提供配方輸入項目。",
    missing_inputs: "尚未提供配方輸入項目。",
    missing_output: "尚未提供唯一定義產出。",
    multiple_outputs: "回傳包含多個定義產出，需後端確認。",
    missing_input_weight: "投入品項重量尚未確認。",
    missing_output_weight: "產出重量基準尚未確認。",
    missing_loss_source: "個別損耗來源尚未記錄。",
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

function mapProductStructureReference(lineage?: ApiRecipeFormulaLineage[] | ApiRecipeFormulaSourceLineage): RecipeFormulaReference[] {
  if (!lineage || Array.isArray(lineage) || !lineage.productStructureReference) {
    return [];
  }
  const reference = lineage.productStructureReference;
  if (!reference.productNo && !reference.bomNo) {
    return [];
  }
  return [
    {
      typeLabel: "Product Structure",
      refNo: reference.productNo ?? reference.bomNo ?? "",
      refName: `BOM ${reference.bomNo ?? "未提供"} / V${asNumber(reference.bomVersion)}`,
      statusLabel: "參照中"
    }
  ];
}

function mapRoutingReferences(lineage?: ApiRecipeFormulaLineage[] | ApiRecipeFormulaSourceLineage): RecipeFormulaReference[] {
  if (!lineage || Array.isArray(lineage)) {
    return [];
  }
  return withFallbackArray<ApiRecipeFormulaReference>(lineage.routingContextRefs, []).map(mapReference);
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
  const recipe = payload.recipe ? mapRecipeListItem({
    ...payload.recipe,
    recipeVersion: payload.version?.recipeVersion ?? payload.formula?.recipeVersion ?? payload.recipe.recipeVersion,
    versionStateCode: payload.version?.versionStateCode ?? payload.recipe.versionStateCode,
    formulaStatusCode: payload.formula?.formulaStatusCode ?? payload.recipe.formulaStatusCode
  }) : fallback;
  if (!recipe?.recipeNo) {
    return undefined;
  }
  const inputs = withFallbackArray<ApiRecipeFormulaInput>(payload.inputs, []).map(mapInput);
  const output = mapOutput(payload.definedOutput ?? payload.output);
  const ratioBase = output?.weight || asNumber(payload.formula?.weight);
  const inputsWithRatios = inputs.map((input) => ({
    ...input,
    weightRatio: input.weightRatio || (ratioBase > 0 ? (input.weight / ratioBase) * 100 : 0)
  }));
  const sourceLineage = payload.sourceLineage ?? payload.lineage;
  return {
    recipe,
    versions: withFallbackArray<ApiRecipeFormulaVersion>(
      payload.versions,
      payload.version ? [payload.version] : []
    ).map(mapVersion),
    inputs: inputsWithRatios,
    output,
    lineage: mapSourceLineage(sourceLineage),
    warnings: withFallbackArray<ApiRecipeFormulaWarning>(payload.warnings, []).map(mapWarning),
    productStructureReferences: withFallbackArray<ApiRecipeFormulaReference>(
      payload.productStructureReferences ?? payload.references?.productStructure,
      []
    ).map(mapReference).concat(mapProductStructureReference(sourceLineage)),
    routingReferences: withFallbackArray<ApiRecipeFormulaReference>(
      payload.routingReferences ?? payload.references?.routing,
      []
    ).map(mapReference).concat(mapRoutingReferences(sourceLineage))
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
