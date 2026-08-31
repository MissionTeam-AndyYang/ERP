import type { StatusTone } from "@/types/dashboard";

export type TraceabilityWorkspaceTab = "search" | "chain" | "timeline";

export type TraceDirectionCode = "upstream" | "downstream" | "both" | "unknown";
export type TraceStatusCode = "complete" | "broken" | "unknown";
export type TraceRiskLevelCode = "normal" | "attention" | "high_risk" | "unknown";
export type TraceRiskCode = "normal" | "broken_chain" | "expired" | "quality_hold" | "unknown";
export type TracePartnerTypeCode = "supplier" | "customer" | "internal" | "unknown";
export type TraceStepTypeCode = "receipt" | "production" | "sale" | "unknown";
export type TraceStepStatusCode = "complete" | "pending" | "blocked" | "missing" | "unknown";

export type TraceSummary = {
  traceableBatchCount: number;
  completeTraceRate: number;
  brokenTraceCount: number;
  highRiskTraceCount: number;
};

export type TraceKpiItem = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type TraceRecord = {
  traceId: string;
  traceDirectionCode: TraceDirectionCode;
  traceDirectionLabel: string;
  itemNo: string;
  itemName: string;
  itemCategory: number;
  itemCategoryLabel: string;
  itemSubCategory: number;
  itemType: number;
  batchNo: string;
  refCategory: number;
  refCategoryLabel: string;
  refNo: string;
  partnerTypeCode: TracePartnerTypeCode;
  partnerTypeLabel: string;
  partnerNo: string;
  partnerName: string;
  workOrderNo: string;
  warehouseNo: string;
  warehouseName: string;
  currentQuantity: number;
  unit: number;
  unitLabel: string;
  traceStatusCode: TraceStatusCode;
  traceStatusLabel: string;
  riskLevelCode: TraceRiskLevelCode;
  riskLevelLabel: string;
  riskCode: TraceRiskCode;
  riskLabel: string;
  latestEventTimestamp: number;
  latestEventDate: string;
  tone: StatusTone;
};

export type TraceStepItem = {
  itemNo: string;
  itemName: string;
  itemCategory: number;
  itemCategoryLabel: string;
  batchNo: string;
  quantity: number;
  unit: number;
  unitLabel: string;
};

export type TraceStep = {
  stepId: string;
  stepTypeCode: TraceStepTypeCode;
  stepTypeLabel: string;
  eventTimestamp: number;
  eventDate: string;
  refCategory: number;
  refCategoryLabel: string;
  refNo: string;
  statusCode: TraceStepStatusCode;
  statusLabel: string;
  riskLevelCode: TraceRiskLevelCode;
  riskLevelLabel: string;
  inputItems: TraceStepItem[];
  outputItems: TraceStepItem[];
  tone: StatusTone;
};

export type TraceBatchOverview = {
  batch: {
    batchNo: string;
    itemNo: string;
    itemName: string;
    itemCategory: number;
    itemCategoryLabel: string;
    itemSubCategory: number;
    itemType: number;
    unit: number;
    unitLabel: string;
    validDate: number;
    validDateLabel: string;
    validDays: number;
    refCategory: number;
    refCategoryLabel: string;
    refNo: string;
    traceDirectionCode: TraceDirectionCode;
    traceDirectionLabel: string;
    traceStatusCode: TraceStatusCode;
    traceStatusLabel: string;
    riskLevelCode: TraceRiskLevelCode;
    riskLevelLabel: string;
    riskCode: TraceRiskCode;
    riskLabel: string;
    tone: StatusTone;
  };
  traceSteps: TraceStep[];
};

export type TraceabilityDashboardData = {
  summary: TraceSummary;
  kpis: TraceKpiItem[];
  records: TraceRecord[];
  total: number;
  start: number;
  count: number;
};

export type TraceabilityDataSource = "api" | "mock";
