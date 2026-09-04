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
    warningCount?: number;
  };
  items?: ApiRoutingProductItem[];
  products?: ApiRoutingProductItem[];
  results?: ApiRoutingProductItem[];
  total?: number;
  start?: number;
  count?: number;
};

type ApiRoutingProductItem = {
  id?: string;
  itemNo?: string;
  itemName?: string;
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
  sourceLineage?: ApiRoutingLineage[];
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
  if (normalized === "product") {
    return "製成品";
  }
  if (normalized === "wip" || normalized === "inproduct") {
    return "在製品";
  }
  return "未分類";
}

function normalizedItemTypeCode(value?: string, itemNo?: string): RoutingProductItem["itemTypeCode"] {
  const normalized = String(value ?? "").toLocaleLowerCase();
  if (normalized === "product") {
    return "product";
  }
  if (normalized === "wip" || normalized === "inproduct") {
    return "wip";
  }
  if (String(itemNo ?? "").startsWith("WIP")) {
    return "wip";
  }
  return "unknown";
}

function normalizeSummary(summary?: ApiRoutingDashboardPayload["summary"]): RoutingSummary {
  return {
    itemCount: asNumber(summary?.itemCount ?? summary?.productCount ?? summary?.wipCount),
    routingVersionCount: asNumber(summary?.routingVersionCount ?? summary?.versionCount),
    effectiveRoutingCount: asNumber(summary?.effectiveRoutingCount),
    warningCount: asNumber(summary?.warningCount)
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
  return {
    id: item.id ?? `${itemNo || "item"}-${item.routingNo ?? item.productProcessNo ?? "routing"}-v${routingVersion}`,
    itemNo,
    itemName,
    itemTypeCode: normalizedItemTypeCode(item.itemTypeCode, itemNo),
    itemTypeLabel: normalizeItemType(item.itemTypeCode, item.itemTypeLabel),
    routingNo: item.routingNo ?? item.productProcessNo ?? "",
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
  const unit = unitLabel(step.unit, step.processUnit);
  const quantity = asNumber(step.standardQuantity ?? step.processCount);
  const minutes = asNumber(step.standardMinutes ?? step.processTime);
  return {
    stepNo: asNumber(step.stepNo ?? step.order),
    processNo: step.processNo ?? step.no ?? "",
    processLabel: step.processLabel ?? step.processName ?? routingSubProcessLabel(oneProcess, secProcess, locale),
    stageLabel: step.stageLabel ?? routingMainProcessLabel(oneProcess, locale),
    groupLabel: step.groupLabel ?? routingSubProcessLabel(oneProcess, secProcess, locale),
    standardQuantity: quantity,
    standardUnit: unit,
    standardMinutes: minutes,
    standardRateLabel: standardRateLabel(quantity, unit, minutes, step.hourlyOutput),
    resourceEligibilityLabel: step.resourceEligibilityLabel ?? (step.laborCount ? `${formatInteger(step.laborCount)} 人` : "待確認"),
    sourceRef: step.sourceRef ?? "process_flow"
  };
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

function mapWarning(warning: ApiRoutingWarning): RoutingWarning {
  const code = warning.code ?? warning.warningCode ?? "unknown";
  const messages: Record<string, string> = {
    missing_process_flow: "尚未建立製程流程步驟。",
    missing_recipe_reference: "尚未建立 Recipe 參照。",
    missing_packaging_context: "包裝 context 尚未建立。",
    missing_resource_eligibility: "資源資格尚未建立治理來源。",
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
  const items = withFallbackArray<ApiRoutingProductItem>(payload.items ?? payload.products ?? payload.results, []).map(mapProductItem);
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
  const item = payload.item || payload.routing ? mapProductItem({ ...(payload.item ?? payload.routing), routingVersion: payload.version?.routingVersion ?? payload.version?.version }) : fallback;
  if (!item?.itemNo) {
    return undefined;
  }
  return {
    item,
    versions: withFallbackArray<ApiRoutingVersion>(payload.versions, payload.version ? [payload.version] : []).map(mapVersion),
    steps: withFallbackArray<ApiRoutingProcessStep>(payload.steps ?? payload.processFlow, []).map(mapStep).sort((a, b) => a.stepNo - b.stepNo),
    recipeReferences: withFallbackArray<ApiRoutingContextReference>(payload.recipeReferences ?? payload.recipeRefs, []).map(mapReference),
    packagingContexts: withFallbackArray<ApiRoutingContextReference>(payload.packagingContexts ?? payload.packagingRefs, []).map(mapReference),
    resourceEligibility: withFallbackArray<ApiRoutingContextReference>(payload.resourceEligibility ?? payload.resourceEligibilityRefs, []).map(mapReference),
    standardPerformance: withFallbackArray<ApiRoutingContextReference>(payload.standardPerformance ?? payload.standardPerformanceRefs, []).map(mapReference),
    lineage: withFallbackArray<ApiRoutingLineage>(payload.sourceLineage ?? payload.lineage, []).map(mapLineage),
    warnings: withFallbackArray<ApiRoutingWarning>(payload.warnings, []).map(mapWarning)
  };
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
  return `/api/v2/routing-process-flow/dashboard?${params.toString()}`;
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
    const payload = await apiGet<ApiRoutingDetailPayload>(
      `/api/v2/routing-process-flow/items/${encodeURIComponent(itemNo)}/versions/${encodeURIComponent(String(routingVersion))}`
    );
    return { detail: mapDetailPayload(payload, fallback), source: "api" };
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
