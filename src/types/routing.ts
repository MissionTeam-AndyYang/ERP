import type { StatusTone } from "@/types/dashboard";

export type RoutingDataSource = "api" | "mock";

export type RoutingVersionStateCode = "effective" | "future" | "historical" | "warning" | "unknown";

export type RoutingSummary = {
  itemCount: number;
  routingVersionCount: number;
  effectiveRoutingCount: number;
  warningCount: number;
};

export type RoutingKpi = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type RoutingProductItem = {
  id: string;
  itemNo: string;
  itemName: string;
  itemTypeCode: "product" | "wip" | "unknown";
  itemTypeLabel: string;
  routingNo: string;
  routingVersionId: string;
  routingVersion: number;
  versionStateCode: RoutingVersionStateCode;
  versionStateLabel: string;
  tone: StatusTone;
  stepCount: number;
  warningCount: number;
  sourceLabel: string;
};

export type RoutingDashboardData = {
  summary: RoutingSummary;
  kpis: RoutingKpi[];
  items: RoutingProductItem[];
  total: number;
  start: number;
  count: number;
};

export type RoutingVersion = {
  version: number;
  versionStateCode: RoutingVersionStateCode;
  versionStateLabel: string;
  tone: StatusTone;
  effectiveDate: string;
  sourceLabel: string;
};

export type RoutingProcessStep = {
  stepNo: number;
  processNo: string;
  processLabel: string;
  stageLabel: string;
  groupLabel: string;
  standardQuantity: number;
  standardUnit: string;
  standardMinutes: number;
  standardRateLabel: string;
  resourceEligibilityLabel: string;
  sourceRef: string;
};

export type RoutingContextReference = {
  typeLabel: string;
  refNo: string;
  refName: string;
  statusLabel: string;
  tone: StatusTone;
};

export type RoutingLineage = {
  sourceTypeLabel: string;
  sourceRef: string;
  evidenceLabel: string;
  statusLabel: string;
};

export type RoutingWarning = {
  code: string;
  message: string;
  refNo: string;
};

export type RoutingDetail = {
  item: RoutingProductItem;
  versions: RoutingVersion[];
  steps: RoutingProcessStep[];
  recipeReferences: RoutingContextReference[];
  packagingContexts: RoutingContextReference[];
  resourceEligibility: RoutingContextReference[];
  standardPerformance: RoutingContextReference[];
  lineage: RoutingLineage[];
  warnings: RoutingWarning[];
};
