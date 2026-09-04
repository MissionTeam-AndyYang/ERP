import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { defaultLanguage } from "@/i18n/dictionary";
import { bomUnitLabel } from "@/i18n/bom-enums";
import {
  normalizeRoutingVersionStateCode,
  routingMainProcessLabel,
  routingSubProcessLabel,
  routingVersionStateLabel,
  routingVersionStateTone
} from "@/i18n/routing-enums";
import { routingDashboardMock, routingDetailMock } from "@/mock/routing";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type {
  RoutingDashboardData,
  RoutingDataSource,
  RoutingDetail,
  RoutingKpi,
  RoutingLineage,
  RoutingProcessStep,
  RoutingProductItem,
  RoutingSummary,
  RoutingVersion,
  RoutingWarning,
  RoutingContextReference
} from "@/types/routing";

type ApiRoutingDashboardPayload = {
  summary?: Partial<RoutingSummary> & {
    itemCount?: number;
    productCount?: number;
    wipCount?: number;
    versionCount?: number;
    routingVersionCount?: number;
    effectiveRoutingCount?: number;
    completeRoutingCount?: number;
    partialRoutingCount?: number;
    missingRoutingCount?: number;
    warningCount?: number;
  };
  routingVersions?: ApiRoutingProductItem[];
  items?: ApiRoutingProductItem[];
  products?: ApiRoutingProductItem[];
  results?: ApiRoutingProductItem[];
  total?: number;
  start?: number;
  count?: number;
};

type ApiRoutingProductItem = {
  id?: string;
  routingVersionId?: string;
  itemNo?: string;
  itemName?: string;
  itemCategory?: number;
  itemSubCategory?: number;
  productNo?: string;
  productName?: string;
  wipNo?: string;
  wipName?: string;
  itemTypeCode?: string;
  itemTypeLabel?: string;
  routingNo?: string;
  productProcessNo?: string;
  routingVersion?: number;
  version?: number;
  versionStateCode?: string;
  stateCode?: string;
  stepCount?: number;
  warningCount?: number;
  warningCodes?: string[];
  sourceLabel?: string;
};

type ApiRoutingDetailPayload = {
  item?: ApiRoutingProductItem;
  routing?: ApiRoutingProductItem;
  routingVersion?: ApiRoutingProductItem;
  version?: ApiRoutingVersion;
  versions?: ApiRoutingVersion[];
  steps?: ApiRoutingProcessStep[];
  processFlow?: ApiRoutingProcessStep[];
  recipeReferences?: ApiRoutingContextReference[];
  recipeRefs?: ApiRoutingContextReference[];
  packagingContexts?: ApiRoutingContextReference[];
  packagingRefs?: ApiRoutingContextReference[];
  resourceEligibility?: ApiRoutingContextReference[];
  resourceEligibilityRefs?: ApiRoutingContextReference[];
  standardPerformance?: ApiRoutingContextReference[];
  standardPerformanceRefs?: ApiRoutingContextReference[];
  lineage?: ApiRoutingLineage[];
  sourceLineage?: ApiRoutingLineage[] | ApiRoutingSourceLineage;
  warnings?: ApiRoutingWarning[];
};

type ApiRoutingVersion = {
  version?: number;
  routingVersion?: number;
  versionStateCode?: string;
  stateCode?: string;
  effectiveDate?: string;
  date?: string;
  dateTimestamp?: number;
  sourceLabel?: string;
};

type ApiRoutingProcessStep = {
  stepId?: string;
  stepOrder?: number;
  stepNo?: number;
  order?: number;
  processNo?: string;
  no?: string;
  processLabel?: string;
  processName?: string;
  oneProcess?: number;
  secProcess?: number;
  stageLabel?: string;
  groupLabel?: string;
  standardQuantity?: number;
  processCount?: number;
  unit?: number | string;
  processUnit?: number;
  standardMinutes?: number;
  processTime?: number;
  hourlyOutput?: number;
  laborCount?: number;
  resourceEligibilityLabel?: string;
  recipeReference?: {
    established?: boolean;
    recipeNo?: string;
    recipeVersion?: number;
    sourceCode?: string;
  };
  packagingContext?: {
    established?: boolean;
    packagingLevel?: number;
    packagingBomNo?: string;
    quantity?: number;
    unit?: number;
    weight?: number;
    sourceCode?: string;
  };
  resourceEligibility?: {
    governed?: boolean;
    eligibleResourceRefs?: string[];
    sourceCode?: string;
  };
  standardPerformance?: {
    governed?: boolean;
    hourlyOutput?: number;
    laborCount?: number;
    unit?: number;
    sourceDateTimestamp?: number;
    sourceCode?: string;
  };
  sourceLineage?: {
    stepSourceCode?: string;
    processSourceCode?: string;
    standardPerformanceSourceCode?: string;
  };
  sourceRef?: string;
};

type ApiRoutingContextReference = {
  typeLabel?: string;
  type?: string;
  refNo?: string;
  refName?: string;
  statusLabel?: string;
  statusCode?: string;
};

type ApiRoutingLineage = {
  sourceTypeLabel?: string;
  sourceType?: string;
  sourceRef?: string;
  evidenceLabel?: string;
  statusLabel?: string;
};

type ApiRoutingSourceLineage = {
  routingVersionSourceCode?: string;
  stepSourceCode?: string;
  processIdentitySourceCode?: string;
  recipeReferenceSourceCode?: string;
  packagingContextSourceCode?: string;
  resourceEligibilitySourceCode?: string;
  routingVersionId?: string;
};

type ApiRoutingWarning = {
  code?: string;
  warningCode?: string;
  message?: string;
  refNo?: string;
};

export type RoutingDashboardQuery = {
  keyword?: string;
  start?: number;
  count?: number;
};

export type RoutingDashboardResult = {
  data: RoutingDashboardData;
  source: RoutingDataSource;
  error?: string;
};

export type RoutingDetailResult = {
  detail?: RoutingDetail;
  source: RoutingDataSource;
  error?: string;
};

const locale = defaultLanguage;

export const emptyRoutingDashboardData: RoutingDashboardData = {
  summary: {
    itemCount: 0,
    routingVersionCount: 0,
    effectiveRoutingCount: 0,
    warningCount: 0
  },
  kpis: [
    { label: "Product / WIP", value: "0", hint: "API 尚未提供資料", tone: "info" },
    { label: "Routing 版本", value: "0", hint: "API 尚未提供資料", tone: "neutral" },
    { label: "目前有效", value: "0", hint: "API 尚未提供資料", tone: "success" },
    { label: "待確認", value: "0", hint: "API 尚未提供資料", tone: "warning" }
  ],
  items: [],
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

function formatNumber(value?: number) {
  return new Intl.NumberFormat(locale, { maximumFractionDigits: 2, minimumFractionDigits: 2 }).format(value ?? 0);
}

function formatTimestamp(value?: number) {
  if (!value) {
    return "";
  }
  return new Date(value * 1000).toLocaleDateString(locale);
}

function normalizeItemType(value?: string, explicit?: string) {
  const normalized = String(value ?? "").toLocaleLowerCase();
  if (explicit) {
    return explicit;
  }
  if (normalized === "product" || normalized === "5") {
    return "製成品";
  }
  if (normalized === "wip" || normalized === "inproduct" || normalized === "4") {
    return "在製品";
  }
  return "未分類";
}

function normalizedItemTypeCode(value?: string | number, itemNo?: string): RoutingProductItem["itemTypeCode"] {
  const normalized = String(value ?? "").toLocaleLowerCase();
  if (normalized === "product" || normalized === "5") {
    return "product";
  }
  if (normalized === "wip" || normalized === "inproduct" || normalized === "4") {
    return "wip";
  }
  if (String(itemNo ?? "").startsWith("WIP")) {
    return "wip";
  }
  return "unknown";
}

function normalizeSummary(summary?: ApiRoutingDashboardPayload["summary"]): RoutingSummary {
  const itemCount =
    summary?.itemCount ??
    asNumber(summary?.productCount) + asNumber(summary?.wipCount);
  return {
    itemCount: asNumber(itemCount),
    routingVersionCount: asNumber(summary?.routingVersionCount ?? summary?.versionCount),
    effectiveRoutingCount: asNumber(summary?.effectiveRoutingCount ?? summary?.completeRoutingCount),
    warningCount: asNumber(
      summary?.warningCount ??
        asNumber(summary?.partialRoutingCount) + asNumber(summary?.missingRoutingCount)
    )
  };
}

function kpisFromSummary(summary: RoutingSummary): RoutingKpi[] {
  return [
    { label: "Product / WIP", value: formatInteger(summary.itemCount), hint: "可查閱製程路線的品項", tone: "info" },
    { label: "Routing 版本", value: formatInteger(summary.routingVersionCount), hint: "目前查詢條件下的版本", tone: "neutral" },
    { label: "目前有效", value: formatInteger(summary.effectiveRoutingCount), hint: "可作 read-only 引用", tone: "success" },
    { label: "待確認", value: formatInteger(summary.warningCount), hint: "資源、標準表現或參照缺口", tone: "warning" }
  ];
}

function mapProductItem(item: ApiRoutingProductItem): RoutingProductItem {
  const itemNo = item.itemNo ?? item.productNo ?? item.wipNo ?? "";
  const itemName = item.itemName ?? item.productName ?? item.wipName ?? "";
  const routingVersion = asNumber(item.routingVersion ?? item.version);
  const stateCode = normalizeRoutingVersionStateCode(item.versionStateCode ?? item.stateCode);
  const routingVersionId = item.routingVersionId ?? item.routingNo ?? item.productProcessNo ?? "";
  return {
    id: item.id ?? `${itemNo || "item"}-${routingVersionId || "routing"}-v${routingVersion}`,
    itemNo,
    itemName,
    itemTypeCode: normalizedItemTypeCode(item.itemTypeCode ?? item.itemCategory, itemNo),
    itemTypeLabel: normalizeItemType(String(item.itemTypeCode ?? item.itemCategory ?? ""), item.itemTypeLabel),
    routingNo: item.routingNo ?? item.productProcessNo ?? routingVersionId,
    routingVersionId,
    routingVersion,
    versionStateCode: stateCode,
    versionStateLabel: routingVersionStateLabel(stateCode, locale),
    tone: routingVersionStateTone(stateCode),
    stepCount: asNumber(item.stepCount),
    warningCount: asNumber(item.warningCount ?? item.warningCodes?.length),
    sourceLabel: item.sourceLabel ?? "product_process / process_flow"
  };
}

function mapVersion(version: ApiRoutingVersion): RoutingVersion {
  const stateCode = normalizeRoutingVersionStateCode(version.versionStateCode ?? version.stateCode);
  return {
    version: asNumber(version.routingVersion ?? version.version),
    versionStateCode: stateCode,
    versionStateLabel: routingVersionStateLabel(stateCode, locale),
    tone: routingVersionStateTone(stateCode),
    effectiveDate: version.effectiveDate ?? version.date ?? formatTimestamp(version.dateTimestamp),
    sourceLabel: version.sourceLabel ?? "product_process"
  };
}

function unitLabel(unit?: string | number, unitCode?: number) {
  if (typeof unit === "string" && unit.trim()) {
    return unit;
  }
  return bomUnitLabel(unitCode ?? (typeof unit === "number" ? unit : undefined), locale);
}

function standardRateLabel(quantity: number, unit: string, minutes: number, hourlyOutput?: number) {
  const output = hourlyOutput && hourlyOutput > 0 ? hourlyOutput : minutes > 0 ? (quantity / minutes) * 60 : 0;
  return output > 0 ? `${formatNumber(output)} ${unit || "單位"} / hr` : "待確認";
}

function mapStep(step: ApiRoutingProcessStep): RoutingProcessStep {
  const oneProcess = step.oneProcess;
  const secProcess = step.secProcess;
  const performance = step.standardPerformance;
  const unit = unitLabel(step.unit, step.processUnit ?? performance?.unit);
  const hourlyOutput = asNumber(step.hourlyOutput ?? performance?.hourlyOutput);
  const quantity = asNumber(step.standardQuantity ?? step.processCount ?? hourlyOutput);
  const minutes = asNumber(step.standardMinutes ?? step.processTime ?? (hourlyOutput > 0 ? 60 : 0));
  const laborCount = asNumber(step.laborCount ?? performance?.laborCount);
  const resourceRefs = step.resourceEligibility?.eligibleResourceRefs ?? [];
  return {
    stepNo: asNumber(step.stepNo ?? step.stepOrder ?? step.order),
    processNo: step.processNo ?? step.no ?? step.stepId ?? "",
    processLabel: processDisplayLabel(step.processLabel ?? step.processName, oneProcess, secProcess),
    stageLabel: processStageDisplayLabel(step.stageLabel, oneProcess),
    groupLabel: processGroupDisplayLabel(step.groupLabel, oneProcess, secProcess),
    standardQuantity: quantity,
    standardUnit: unit,
    standardMinutes: minutes,
    standardRateLabel: standardRateLabel(quantity, unit, minutes, hourlyOutput),
    resourceEligibilityLabel:
      step.resourceEligibilityLabel ??
      (step.resourceEligibility?.governed && resourceRefs.length ? resourceRefs.join(" / ") : laborCount ? `${formatInteger(laborCount)} 人` : "待確認"),
    sourceRef: step.sourceRef ?? step.sourceLineage?.stepSourceCode ?? "process_flow"
  };
}

function processStageDisplayLabel(value?: string, oneProcess?: number) {
  const labels: Record<string, string> = {
    preparation: "前備",
    processing: "加工",
    packaging: "包裝",
    other: "其他",
    unknown: "待確認"
  };
  return labels[String(value ?? "").toLocaleLowerCase()] ?? routingMainProcessLabel(oneProcess, locale);
}

function processGroupDisplayLabel(value?: string, oneProcess?: number, secProcess?: number) {
  if (!value || value.includes(":")) {
    return routingSubProcessLabel(oneProcess, secProcess, locale);
  }
  return value;
}

function processDisplayLabel(value?: string, oneProcess?: number, secProcess?: number) {
  if (!value || value.includes(":") || value === "preparation" || value === "processing" || value === "packaging") {
    return routingSubProcessLabel(oneProcess, secProcess, locale);
  }
  return value;
}

function toneFromStatus(value?: string) {
  const normalized = String(value ?? "").toLocaleLowerCase();
  if (normalized === "ok" || normalized === "effective" || normalized === "governed") {
    return "success" as const;
  }
  if (normalized === "warning" || normalized === "missing") {
    return "warning" as const;
  }
  return "neutral" as const;
}

function mapReference(reference: ApiRoutingContextReference): RoutingContextReference {
  return {
    typeLabel: reference.typeLabel ?? reference.type ?? "參照",
    refNo: reference.refNo ?? "",
    refName: reference.refName ?? "",
    statusLabel: reference.statusLabel ?? "參照中",
    tone: toneFromStatus(reference.statusCode ?? reference.statusLabel)
  };
}

function mapLineage(lineage: ApiRoutingLineage): RoutingLineage {
  return {
    sourceTypeLabel: lineage.sourceTypeLabel ?? lineage.sourceType ?? "來源",
    sourceRef: lineage.sourceRef ?? "",
    evidenceLabel: lineage.evidenceLabel ?? "未提供",
    statusLabel: lineage.statusLabel ?? "read-only"
  };
}

function mapSourceLineage(lineage?: ApiRoutingLineage[] | ApiRoutingSourceLineage): RoutingLineage[] {
  if (Array.isArray(lineage)) {
    return lineage.map(mapLineage);
  }
  if (!lineage) {
    return [];
  }
  return [
    {
      sourceTypeLabel: "Routing 版本來源",
      sourceRef: lineage.routingVersionSourceCode ?? "",
      evidenceLabel: "Routing version evidence",
      statusLabel: "read-only"
    },
    {
      sourceTypeLabel: "流程步驟來源",
      sourceRef: lineage.stepSourceCode ?? "",
      evidenceLabel: "ordered process-flow evidence",
      statusLabel: "read-only"
    },
    {
      sourceTypeLabel: "製程主檔來源",
      sourceRef: lineage.processIdentitySourceCode ?? "",
      evidenceLabel: "process identity evidence",
      statusLabel: "read-only"
    },
    {
      sourceTypeLabel: "Recipe 參照來源",
      sourceRef: lineage.recipeReferenceSourceCode ?? "",
      evidenceLabel: "Recipe reference evidence",
      statusLabel: "read-only"
    },
    {
      sourceTypeLabel: "Packaging context 來源",
      sourceRef: lineage.packagingContextSourceCode ?? "",
      evidenceLabel: "bounded packaging context evidence",
      statusLabel: "read-only"
    },
    {
      sourceTypeLabel: "資源資格來源",
      sourceRef: lineage.resourceEligibilitySourceCode ?? "",
      evidenceLabel: "resource eligibility evidence",
      statusLabel: "read-only"
    }
  ].filter((item) => item.sourceRef);
}

function mapWarning(warning: ApiRoutingWarning): RoutingWarning {
  const code = warning.code ?? warning.warningCode ?? "unknown";
  const messages: Record<string, string> = {
    missing_process_flow: "尚未建立製程流程步驟。",
    missing_steps: "尚未建立製程流程步驟。",
    missing_item_master: "品項主檔尚未建立或無法解析。",
    missing_process_master: "製程主檔尚未建立或無法解析。",
    missing_recipe_reference: "尚未建立 Recipe 參照。",
    missing_packaging_context: "包裝 context 尚未建立。",
    packaging_context_not_governed: "包裝 context 尚未建立治理來源。",
    missing_resource_eligibility: "資源資格尚未建立治理來源。",
    resource_eligibility_not_governed: "資源資格尚未建立治理來源。",
    missing_standard_performance: "標準表現尚未建立治理來源。",
    unknown: "Routing / Process Flow 資料需確認。"
  };
  return {
    code,
    message: warning.message ?? messages[code] ?? messages.unknown,
    refNo: warning.refNo ?? ""
  };
}

function mapDashboardPayload(payload: ApiRoutingDashboardPayload): RoutingDashboardData {
  const summary = normalizeSummary(payload.summary);
  const items = withFallbackArray<ApiRoutingProductItem>(
    payload.routingVersions ?? payload.items ?? payload.products ?? payload.results,
    []
  ).map(mapProductItem);
  return {
    summary,
    kpis: kpisFromSummary(summary),
    items,
    total: payload.total ?? items.length,
    start: payload.start ?? 0,
    count: payload.count ?? items.length
  };
}

function mapDetailPayload(payload: ApiRoutingDetailPayload, fallback?: RoutingProductItem): RoutingDetail | undefined {
  const routingVersion = payload.routingVersion ?? payload.item ?? payload.routing;
  const item = routingVersion
    ? mapProductItem({
        ...routingVersion,
        routingVersion: payload.version?.routingVersion ?? payload.version?.version ?? routingVersion.routingVersion,
        versionStateCode: payload.version?.versionStateCode ?? routingVersion.versionStateCode
      })
    : fallback;
  if (!item?.itemNo) {
    return undefined;
  }
  const steps = withFallbackArray<ApiRoutingProcessStep>(payload.steps ?? payload.processFlow, []);
  const recipeReferences = uniqueReferences(steps.map((step) => mapRecipeReference(step.recipeReference)).filter(Boolean) as RoutingContextReference[]);
  const packagingContexts = uniqueReferences(steps.map((step) => mapPackagingContext(step.packagingContext)).filter(Boolean) as RoutingContextReference[]);
  const resourceEligibility = uniqueReferences(steps.map((step) => mapResourceEligibility(step.resourceEligibility)).filter(Boolean) as RoutingContextReference[]);
  const standardPerformance = uniqueReferences(steps.map((step) => mapStandardPerformance(step.standardPerformance)).filter(Boolean) as RoutingContextReference[]);
  return {
    item,
    versions: withFallbackArray<ApiRoutingVersion>(payload.versions, payload.version ? [payload.version] : []).map(mapVersion),
    steps: steps.map(mapStep).sort((a, b) => a.stepNo - b.stepNo),
    recipeReferences: withFallbackArray<ApiRoutingContextReference>(payload.recipeReferences ?? payload.recipeRefs, []).map(mapReference).concat(recipeReferences),
    packagingContexts: withFallbackArray<ApiRoutingContextReference>(payload.packagingContexts ?? payload.packagingRefs, []).map(mapReference).concat(packagingContexts),
    resourceEligibility: withFallbackArray<ApiRoutingContextReference>(payload.resourceEligibility ?? payload.resourceEligibilityRefs, []).map(mapReference).concat(resourceEligibility),
    standardPerformance: withFallbackArray<ApiRoutingContextReference>(payload.standardPerformance ?? payload.standardPerformanceRefs, []).map(mapReference).concat(standardPerformance),
    lineage: mapSourceLineage(payload.sourceLineage ?? payload.lineage),
    warnings: withFallbackArray<ApiRoutingWarning>(payload.warnings, []).map(mapWarning)
  };
}

function mapRecipeReference(reference?: ApiRoutingProcessStep["recipeReference"]): RoutingContextReference | undefined {
  if (!reference?.established) {
    return undefined;
  }
  return {
    typeLabel: "Recipe reference",
    refNo: reference.recipeNo ?? "",
    refName: reference.recipeVersion ? `Recipe Version ${reference.recipeVersion}` : "已建立 Recipe 參照",
    statusLabel: "已建立",
    tone: "success"
  };
}

function mapPackagingContext(context?: ApiRoutingProcessStep["packagingContext"]): RoutingContextReference | undefined {
  if (!context?.established) {
    return undefined;
  }
  const unit = unitLabel(context.unit);
  return {
    typeLabel: "Packaging context",
    refNo: context.packagingBomNo ?? "",
    refName: `Level ${context.packagingLevel ?? 0} · ${formatInteger(context.quantity)} ${unit} · ${formatNumber(context.weight)} kg`,
    statusLabel: "參照中",
    tone: "neutral"
  };
}

function mapResourceEligibility(resource?: ApiRoutingProcessStep["resourceEligibility"]): RoutingContextReference | undefined {
  if (!resource) {
    return undefined;
  }
  return {
    typeLabel: "Resource eligibility",
    refNo: resource.sourceCode ?? "not_recorded",
    refName: resource.governed ? withFallbackArray<string>(resource.eligibleResourceRefs, []).join(" / ") || "已建立資源資格" : "尚未建立治理來源",
    statusLabel: resource.governed ? "受治理" : "待治理",
    tone: resource.governed ? "success" : "warning"
  };
}

function mapStandardPerformance(performance?: ApiRoutingProcessStep["standardPerformance"]): RoutingContextReference | undefined {
  if (!performance) {
    return undefined;
  }
  const unit = unitLabel(performance.unit);
  return {
    typeLabel: "Standard performance",
    refNo: performance.sourceCode ?? "not_recorded",
    refName: performance.governed ? `${formatNumber(performance.hourlyOutput)} ${unit} / hr · ${formatInteger(performance.laborCount)} 人` : "尚未建立標準表現",
    statusLabel: performance.governed ? "受治理" : "待治理",
    tone: performance.governed ? "success" : "warning"
  };
}

function uniqueReferences(references: RoutingContextReference[]) {
  const seen = new Set<string>();
  return references.filter((reference) => {
    const key = `${reference.typeLabel}-${reference.refNo}-${reference.refName}`;
    if (seen.has(key)) {
      return false;
    }
    seen.add(key);
    return true;
  });
}

function buildDashboardPath(query: RoutingDashboardQuery = {}) {
  const params = new URLSearchParams();
  if (query.keyword) {
    params.set("keyword", query.keyword);
  }
  if (query.start !== undefined) {
    params.set("start", String(query.start));
  }
  params.set("count", String(query.count ?? 50));
  return `/api/v2/routing/dashboard?${params.toString()}`;
}

export async function getRoutingDashboard(
  query: RoutingDashboardQuery = {},
  dataSourceMode: DataSourceMode = "api"
): Promise<RoutingDashboardResult> {
  if (dataSourceMode === "mock") {
    return { data: routingDashboardMock, source: "mock" };
  }

  try {
    const payload = await apiGet<ApiRoutingDashboardPayload>(buildDashboardPath(query));
    return { data: mapDashboardPayload(payload), source: "api" };
  } catch (error) {
    return {
      data: emptyRoutingDashboardData,
      source: "api",
      error: error instanceof Error ? error.message : "Routing / Process Flow API unavailable"
    };
  }
}

export async function getRoutingDetail(
  itemNo: string,
  routingVersion: number,
  fallback?: RoutingProductItem,
  dataSourceMode: DataSourceMode = "api"
): Promise<RoutingDetailResult> {
  if (dataSourceMode === "mock") {
    return {
      detail:
        routingDetailMock[itemNo] ??
        (fallback
          ? {
              item: fallback,
              versions: [],
              steps: [],
              recipeReferences: [],
              packagingContexts: [],
              resourceEligibility: [],
              standardPerformance: [],
              lineage: [],
              warnings: []
            }
          : undefined),
      source: "mock"
    };
  }

  try {
    const versionsPayload = await apiGet<{ versions?: ApiRoutingProductItem[] }>(
      `/api/v2/routing/products/${encodeURIComponent(itemNo)}/versions`
    );
    const selectedVersion =
      withFallbackArray<ApiRoutingProductItem>(versionsPayload.versions, []).find((item) => asNumber(item.routingVersion ?? item.version) === routingVersion) ??
      withFallbackArray<ApiRoutingProductItem>(versionsPayload.versions, [])[0];
    const routingVersionId = selectedVersion?.routingVersionId ?? fallback?.routingVersionId;
    if (!routingVersionId) {
      throw new Error("Routing Version ID unavailable");
    }
    const payload = await apiGet<ApiRoutingDetailPayload>(
      `/api/v2/routing/versions/${encodeURIComponent(routingVersionId)}/steps`
    );
    return {
      detail: mapDetailPayload(
        {
          ...payload,
          versions: versionsPayload.versions,
          routingVersion: payload.routingVersion ?? selectedVersion
        },
        fallback
      ),
      source: "api"
    };
  } catch (error) {
    return {
      detail: fallback
        ? {
            item: fallback,
            versions: [],
            steps: [],
            recipeReferences: [],
            packagingContexts: [],
            resourceEligibility: [],
            standardPerformance: [],
            lineage: [],
            warnings: []
          }
        : undefined,
      source: "api",
      error: error instanceof Error ? error.message : "Routing / Process Flow detail API unavailable"
    };
  }
}
