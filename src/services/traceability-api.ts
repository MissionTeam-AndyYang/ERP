import type { DataSourceMode } from "@/components/common/data-source-toggle";
import {
  traceDirectionLabel,
  traceItemCategoryLabel,
  tracePartnerTypeLabel,
  traceRefCategoryLabel,
  traceRiskLabel,
  traceRiskLevelLabel,
  traceRiskTone,
  traceStatusLabel,
  traceStepStatusLabel,
  traceStepStatusTone,
  traceStepTypeLabel,
  traceUnitLabel
} from "@/i18n/traceability-enums";
import { traceabilityDashboardMock, traceabilityOverviewMock } from "@/mock/traceability";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type {
  TraceBatchOverview,
  TraceKpiItem,
  TraceRecord,
  TraceRiskLevelCode,
  TraceStep,
  TraceStepItem,
  TraceSummary,
  TraceabilityDashboardData,
  TraceabilityDataSource
} from "@/types/traceability";

type ApiTraceSummary = Partial<TraceSummary>;

type ApiTraceRecord = {
  traceId?: string;
  traceDirectionCode?: string;
  itemNo?: string;
  itemName?: string;
  itemCategory?: number;
  itemSubCategory?: number;
  itemType?: number;
  batchNo?: string;
  refCategory?: number;
  refNo?: string;
  partnerTypeCode?: string;
  partnerNo?: string;
  partnerName?: string;
  workOrderNo?: string;
  warehouseNo?: string;
  warehouseName?: string;
  currentQuantity?: number;
  unit?: number;
  traceStatusCode?: string;
  riskLevelCode?: string;
  riskCode?: string;
  latestEventTimestamp?: number;
};

type ApiTraceDashboardPayload = {
  serverTimestamp?: number;
  summary?: ApiTraceSummary;
  records?: ApiTraceRecord[];
  total?: number;
  start?: number;
  count?: number;
};

type ApiTraceStepItem = {
  itemNo?: string;
  itemName?: string;
  itemCategory?: number;
  batchNo?: string;
  quantity?: number;
  unit?: number;
};

type ApiTraceStep = {
  stepId?: string;
  stepTypeCode?: string;
  eventTimestamp?: number;
  refCategory?: number;
  refNo?: string;
  statusCode?: string;
  riskLevelCode?: string;
  inputItems?: ApiTraceStepItem[];
  outputItems?: ApiTraceStepItem[];
};

type ApiTraceOverviewPayload = {
  serverTimestamp?: number;
  batch?: {
    batchNo?: string;
    itemNo?: string;
    itemName?: string;
    itemCategory?: number;
    itemSubCategory?: number;
    itemType?: number;
    unit?: number;
    validDate?: number;
    validDays?: number;
    refCategory?: number;
    refNo?: string;
    traceDirectionCode?: string;
    traceStatusCode?: string;
    riskLevelCode?: string;
    riskCode?: string;
  };
  traceSteps?: ApiTraceStep[];
};

export type TraceabilityDashboardQuery = {
  keyword?: string;
  batchNo?: string;
  itemCategory?: number;
  itemNo?: string;
  startDate?: number;
  endDate?: number;
  start?: number;
  count?: number;
};

export type TraceabilityDashboardResult = {
  data: TraceabilityDashboardData;
  source: TraceabilityDataSource;
  error?: string;
};

export type TraceabilityOverviewResult = {
  overview?: TraceBatchOverview;
  source: TraceabilityDataSource;
  error?: string;
};

const locale = "zh-TW";

export const emptyTraceabilityDashboardData: TraceabilityDashboardData = {
  summary: {
    traceableBatchCount: 0,
    completeTraceRate: 0,
    brokenTraceCount: 0,
    highRiskTraceCount: 0
  },
  kpis: [
    { label: "可追溯批號", value: "0", hint: "目前沒有資料", tone: "info" },
    { label: "鏈路完整率", value: "0.00%", hint: "目前沒有資料", tone: "neutral" },
    { label: "斷鏈追溯", value: "0", hint: "目前沒有資料", tone: "success" },
    { label: "高風險追溯", value: "0", hint: "目前沒有資料", tone: "success" }
  ],
  records: [],
  total: 0,
  start: 0,
  count: 0
};

function asNumber(value?: number) {
  return Number.isFinite(value) ? Number(value) : 0;
}

function formatInteger(value?: number) {
  return new Intl.NumberFormat(locale, { maximumFractionDigits: 0 }).format(asNumber(value));
}

function formatRate(value?: number) {
  return `${new Intl.NumberFormat(locale, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(asNumber(value))}%`;
}

function timestampToDate(value?: number) {
  if (!value) {
    return "";
  }
  return new Date(value * 1000).toLocaleDateString(locale, { timeZone: "Asia/Taipei" });
}

function normalizeRiskLevel(value?: string): TraceRiskLevelCode {
  if (value === "normal" || value === "attention" || value === "high_risk") {
    return value;
  }
  return "unknown";
}

function normalizeSummary(summary?: ApiTraceSummary): TraceSummary {
  return {
    traceableBatchCount: asNumber(summary?.traceableBatchCount),
    completeTraceRate: asNumber(summary?.completeTraceRate),
    brokenTraceCount: asNumber(summary?.brokenTraceCount),
    highRiskTraceCount: asNumber(summary?.highRiskTraceCount)
  };
}

function kpisFromSummary(summary: TraceSummary): TraceKpiItem[] {
  return [
    {
      label: "可追溯批號",
      value: formatInteger(summary.traceableBatchCount),
      hint: "符合目前查詢條件的批號",
      tone: "info"
    },
    {
      label: "鏈路完整率",
      value: formatRate(summary.completeTraceRate),
      hint: "完整追溯批號比例",
      tone: summary.completeTraceRate >= 99 ? "success" : summary.completeTraceRate >= 95 ? "warning" : "danger"
    },
    {
      label: "斷鏈追溯",
      value: formatInteger(summary.brokenTraceCount),
      hint: "追到不可再追溯的批號",
      tone: summary.brokenTraceCount ? "danger" : "success"
    },
    {
      label: "高風險追溯",
      value: formatInteger(summary.highRiskTraceCount),
      hint: "斷鏈、過期或品檢保留",
      tone: summary.highRiskTraceCount ? "danger" : "success"
    }
  ];
}

function mapTraceRecord(record: ApiTraceRecord, index = 0): TraceRecord {
  const riskLevelCode = normalizeRiskLevel(record.riskLevelCode);
  const riskCode = record.riskCode ?? "unknown";
  const traceStatusCode = record.traceStatusCode === "complete" || record.traceStatusCode === "broken"
    ? record.traceStatusCode
    : "unknown";
  const traceDirectionCode =
    record.traceDirectionCode === "upstream" || record.traceDirectionCode === "downstream" || record.traceDirectionCode === "both"
      ? record.traceDirectionCode
      : "unknown";
  const partnerTypeCode =
    record.partnerTypeCode === "supplier" || record.partnerTypeCode === "customer" || record.partnerTypeCode === "internal"
      ? record.partnerTypeCode
      : "unknown";
  const traceId = record.traceId || record.batchNo || `${record.itemNo ?? "trace"}-${index}`;

  return {
    traceId,
    traceDirectionCode,
    traceDirectionLabel: traceDirectionLabel(traceDirectionCode, locale),
    itemNo: record.itemNo ?? "",
    itemName: record.itemName ?? "",
    itemCategory: asNumber(record.itemCategory),
    itemCategoryLabel: traceItemCategoryLabel(record.itemCategory, locale),
    itemSubCategory: asNumber(record.itemSubCategory),
    itemType: asNumber(record.itemType),
    batchNo: record.batchNo ?? "",
    refCategory: asNumber(record.refCategory),
    refCategoryLabel: traceRefCategoryLabel(record.refCategory, locale),
    refNo: record.refNo ?? "",
    partnerTypeCode,
    partnerTypeLabel: tracePartnerTypeLabel(partnerTypeCode, locale),
    partnerNo: record.partnerNo ?? "",
    partnerName: record.partnerName ?? "",
    workOrderNo: record.workOrderNo ?? "",
    warehouseNo: record.warehouseNo ?? "",
    warehouseName: record.warehouseName ?? "",
    currentQuantity: asNumber(record.currentQuantity),
    unit: asNumber(record.unit),
    unitLabel: traceUnitLabel(record.unit, locale),
    traceStatusCode,
    traceStatusLabel: traceStatusLabel(traceStatusCode, locale),
    riskLevelCode,
    riskLevelLabel: traceRiskLevelLabel(riskLevelCode, locale),
    riskCode: riskCode as TraceRecord["riskCode"],
    riskLabel: traceRiskLabel(riskCode, locale),
    latestEventTimestamp: asNumber(record.latestEventTimestamp),
    latestEventDate: timestampToDate(record.latestEventTimestamp),
    tone: traceRiskTone(riskLevelCode, riskCode)
  };
}

function mapTraceStepItem(item: ApiTraceStepItem): TraceStepItem {
  return {
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    itemCategory: asNumber(item.itemCategory),
    itemCategoryLabel: traceItemCategoryLabel(item.itemCategory, locale),
    batchNo: item.batchNo ?? "",
    quantity: asNumber(item.quantity),
    unit: asNumber(item.unit),
    unitLabel: traceUnitLabel(item.unit, locale)
  };
}

function mapTraceStep(step: ApiTraceStep, index = 0): TraceStep {
  const stepTypeCode =
    step.stepTypeCode === "receipt" || step.stepTypeCode === "production" || step.stepTypeCode === "sale"
      ? step.stepTypeCode
      : "unknown";
  const statusCode =
    step.statusCode === "complete" ||
    step.statusCode === "pending" ||
    step.statusCode === "blocked" ||
    step.statusCode === "missing"
      ? step.statusCode
      : "unknown";
  const riskLevelCode = normalizeRiskLevel(step.riskLevelCode);

  return {
    stepId: step.stepId || `${stepTypeCode}-${step.refNo ?? index}`,
    stepTypeCode,
    stepTypeLabel: traceStepTypeLabel(stepTypeCode, locale),
    eventTimestamp: asNumber(step.eventTimestamp),
    eventDate: timestampToDate(step.eventTimestamp),
    refCategory: asNumber(step.refCategory),
    refCategoryLabel: traceRefCategoryLabel(step.refCategory, locale),
    refNo: step.refNo ?? "",
    statusCode,
    statusLabel: traceStepStatusLabel(statusCode, locale),
    riskLevelCode,
    riskLevelLabel: traceRiskLevelLabel(riskLevelCode, locale),
    inputItems: withFallbackArray<ApiTraceStepItem>(step.inputItems, []).map(mapTraceStepItem),
    outputItems: withFallbackArray<ApiTraceStepItem>(step.outputItems, []).map(mapTraceStepItem),
    tone: traceStepStatusTone(statusCode, riskLevelCode)
  };
}

function mapOverviewPayload(payload: ApiTraceOverviewPayload): TraceBatchOverview | undefined {
  const batch = payload.batch;
  if (!batch?.batchNo) {
    return undefined;
  }

  const traceDirectionCode =
    batch.traceDirectionCode === "upstream" || batch.traceDirectionCode === "downstream" || batch.traceDirectionCode === "both"
      ? batch.traceDirectionCode
      : "unknown";
  const traceStatusCode =
    batch.traceStatusCode === "complete" || batch.traceStatusCode === "broken" ? batch.traceStatusCode : "unknown";
  const riskLevelCode = normalizeRiskLevel(batch.riskLevelCode);
  const riskCode = batch.riskCode ?? "unknown";

  return {
    batch: {
      batchNo: batch.batchNo,
      itemNo: batch.itemNo ?? "",
      itemName: batch.itemName ?? "",
      itemCategory: asNumber(batch.itemCategory),
      itemCategoryLabel: traceItemCategoryLabel(batch.itemCategory, locale),
      itemSubCategory: asNumber(batch.itemSubCategory),
      itemType: asNumber(batch.itemType),
      unit: asNumber(batch.unit),
      unitLabel: traceUnitLabel(batch.unit, locale),
      validDate: asNumber(batch.validDate),
      validDateLabel: timestampToDate(batch.validDate),
      validDays: asNumber(batch.validDays),
      refCategory: asNumber(batch.refCategory),
      refCategoryLabel: traceRefCategoryLabel(batch.refCategory, locale),
      refNo: batch.refNo ?? "",
      traceDirectionCode,
      traceDirectionLabel: traceDirectionLabel(traceDirectionCode, locale),
      traceStatusCode,
      traceStatusLabel: traceStatusLabel(traceStatusCode, locale),
      riskLevelCode,
      riskLevelLabel: traceRiskLevelLabel(riskLevelCode, locale),
      riskCode: riskCode as TraceBatchOverview["batch"]["riskCode"],
      riskLabel: traceRiskLabel(riskCode, locale),
      tone: traceRiskTone(riskLevelCode, riskCode)
    },
    traceSteps: withFallbackArray<ApiTraceStep>(payload.traceSteps, []).map(mapTraceStep)
  };
}

function mapDashboardPayload(payload: ApiTraceDashboardPayload): TraceabilityDashboardData {
  const summary = normalizeSummary(payload.summary);
  const records = withFallbackArray<ApiTraceRecord>(payload.records, []).map(mapTraceRecord);

  return {
    summary,
    kpis: kpisFromSummary(summary),
    records,
    total: payload.total ?? records.length,
    start: payload.start ?? 0,
    count: payload.count ?? records.length
  };
}

function buildDashboardPath(query: TraceabilityDashboardQuery = {}) {
  const params = new URLSearchParams();
  Object.entries(query).forEach(([key, value]) => {
    if (value !== undefined && value !== "") {
      params.set(key, String(value));
    }
  });
  params.set("start", String(query.start ?? 0));
  params.set("count", String(query.count ?? 50));
  return `/api/v2/trace/dashboard?${params.toString()}`;
}

export async function getTraceabilityDashboard(
  query: TraceabilityDashboardQuery = {},
  dataSourceMode: DataSourceMode = "api"
): Promise<TraceabilityDashboardResult> {
  if (dataSourceMode === "mock") {
    return {
      data: traceabilityDashboardMock,
      source: "mock"
    };
  }

  try {
    const payload = await apiGet<ApiTraceDashboardPayload>(buildDashboardPath(query));
    return {
      data: mapDashboardPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: emptyTraceabilityDashboardData,
      source: "api",
      error: error instanceof Error ? error.message : "溯源中心資料取得失敗"
    };
  }
}

export async function getTraceabilityOverview(
  batchNo: string,
  dataSourceMode: DataSourceMode = "api"
): Promise<TraceabilityOverviewResult> {
  if (!batchNo) {
    return {
      source: dataSourceMode === "mock" ? "mock" : "api"
    };
  }

  if (dataSourceMode === "mock") {
    return {
      overview: traceabilityOverviewMock[batchNo],
      source: "mock"
    };
  }

  try {
    const payload = await apiGet<ApiTraceOverviewPayload>(`/api/v2/trace/batches/${encodeURIComponent(batchNo)}/overview`);
    return {
      overview: mapOverviewPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      source: "api",
      error: error instanceof Error ? error.message : "批號追溯資料取得失敗"
    };
  }
}
