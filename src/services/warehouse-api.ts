import { warehouseDashboardMock } from "@/mock/warehouse";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { StatusTone } from "@/types/dashboard";
import type {
  InventoryCategory,
  WarehouseAnalyticsBucket,
  WarehouseAnalyticsCategorySummary,
  WarehouseAnalyticsOverviewData,
  WarehouseAnalyticsOverdueTrendPoint,
  WarehouseAnalyticsPeriod,
  WarehouseAnalyticsRange,
  WarehouseAnalyticsRiskBreakdownData,
  WarehouseAnalyticsRiskBreakdownItem,
  WarehouseAnalyticsRiskSummary,
  WarehouseAnalyticsSpaceTrendPoint,
  WarehouseAnalyticsSpaceUtilizationData,
  WarehouseAnalyticsTaskDepartmentSummary,
  WarehouseAnalyticsTaskSlaData,
  WarehouseAnalyticsTaskSlaItem,
  WarehouseAnalyticsTopRiskLot,
  WarehouseAnalyticsValueTrendData,
  WarehouseAnalyticsValueTrendPoint,
  WarehouseAnalyticsWarehouseSummary,
  WarehouseCapacity,
  WarehouseCategorySummary,
  WarehouseDashboardData,
  WarehouseDataSource,
  WarehouseInventoryLot,
  WarehouseInventoryLotDetail,
  WarehouseInventoryLotListData,
  WarehouseInventoryLotSummary,
  WarehouseInventoryRecordLine,
  WarehouseKpi,
  WarehousePalletMovementLine,
  WarehouseQualityHoldLine,
  WarehouseRecord,
  WarehouseRelatedDocument,
  WarehouseReservationLine,
  WarehouseRisk,
  WarehouseSourceType,
  WarehouseTask,
  WarehouseTaskDetail,
  WarehouseTaskRelatedLot,
  WarehouseTaskSourceRef,
  WarehouseTaskTimelineEvent,
  WarehouseTaskWorkbenchData,
  WarehouseTaskWorkbenchItem,
  WarehouseTaskWorkbenchLane,
  WarehouseTaskWorkbenchSummary,
  WarehouseWorkflowTaskLine,
  WarehouseWorkflowStep
} from "@/types/warehouse";

type ApiWarehousePayload = {
  serverTimestamp?: number;
  range?: {
    date?: string;
    startTimestamp?: number;
    endTimestamp?: number;
  };
  summary?: {
    totalInventoryValue?: number;
    reservedInventoryValue?: number;
    availableInventoryValue?: number;
    qualityHoldInventoryValue?: number;
    totalPallets?: number;
    usedPallets?: number;
    reservedPallets?: number;
    availablePallets?: number;
    riskAlertCount?: number;
    pendingInboundCount?: number;
    pendingOutboundCount?: number;
  };
  inventoryValueByCategory?: ApiWarehouseCategory[];
  capacityByWarehouse?: ApiWarehouseCapacity[];
  riskAlerts?: ApiWarehouseRisk[];
  pendingTasks?: ApiWarehouseTask[];
  valueTrend?: ApiWarehouseValueTrend[];
  inventory?: ApiWarehouseInventory[];
};

type ApiWarehouseCategory = {
  itemCategory?: number;
  inventoryValue?: number;
  reservedValue?: number;
  availableValue?: number;
  qualityHoldValue?: number;
  quantity?: number;
  palletCount?: number;
  itemCount?: number;
  valueRatio?: number;
  trend7Days?: number;
};

type ApiWarehouseCapacity = {
  warehouseNo?: string;
  warehouseName?: string;
  warehouseType?: number;
  totalPallets?: number;
  usedPallets?: number;
  reservedPallets?: number;
  availablePallets?: number;
  utilizationRate?: number;
  riskLevel?: number;
};

type ApiWarehouseRisk = {
  alertId?: string;
  riskType?: string;
  riskLevel?: number;
  itemNo?: string;
  itemName?: string;
  itemCategory?: number;
  batchNo?: string;
  warehouseNo?: string;
  warehouseName?: string;
  quantity?: number;
  unit?: number;
  inventoryValue?: number;
  daysInStock?: number;
  validDate?: number;
  remainingShelfLifeRatio?: number;
  safetyStock?: number;
  messageCode?: string;
  messageParams?: {
    currentQuantity?: number;
    daysInStock?: number;
    validDate?: number;
    remainingShelfLifeRatio?: number;
    safetyStock?: number;
  };
  recommendedActionCode?: string;
};

type ApiWarehouseTask = {
  taskId?: string;
  taskType?: number;
  refCategory?: number;
  sourceNo?: string;
  sourceSubNo?: string;
  itemNo?: string;
  itemName?: string;
  itemCategory?: number;
  batchNo?: string;
  expectedQuantity?: number;
  processedQuantity?: number;
  remainingQuantity?: number;
  unit?: number;
  palletCount?: number;
  warehouseNo?: string;
  warehouseName?: string;
  dueTimestamp?: number;
  taskStatus?: number;
  ownerDepartment?: number;
  blockReason?: string;
};

type ApiWarehouseValueTrend = {
  date?: string;
  itemCategory?: number;
  inventoryValue?: number;
};

type ApiWarehouseInventory = {
  warehouseNo?: string;
  warehouseName?: string;
  itemCategory?: number;
  itemSubCategory?: number;
  itemType?: number;
  itemNo?: string;
  itemName?: string;
  batchNo?: string;
  unit?: number;
  currentQuantity?: number;
  reservedQuantity?: number;
  availableQuantity?: number;
  qualityHoldQuantity?: number;
  inventoryValue?: number;
  reservedValue?: number;
  availableValue?: number;
  qualityHoldValue?: number;
  firstInboundTimestamp?: number;
  validDays?: number;
  validDate?: number;
  sourceNo?: string;
  sourceRefCategory?: number;
};

type ApiWarehouseInventoryLotSummary = {
  lotCount?: number;
  itemCount?: number;
  totalQuantity?: number;
  totalInventoryValue?: number;
  totalAvailableQuantity?: number;
  totalAvailableValue?: number;
  riskLotCount?: number;
  pendingTaskCount?: number;
};

type ApiWarehouseInventoryLot = {
  lotKey?: string;
  warehouseNo?: string;
  warehouseName?: string;
  itemCategory?: number;
  itemNo?: string;
  itemName?: string;
  batchNo?: string;
  unit?: number;
  currentQuantity?: number;
  reservedQuantity?: number;
  qualityHoldQuantity?: number;
  availableQuantity?: number;
  unitCost?: number;
  inventoryValue?: number;
  reservedValue?: number;
  qualityHoldValue?: number;
  availableValue?: number;
  palletCount?: number;
  firstInboundTimestamp?: number;
  daysInStock?: number;
  validDays?: number;
  validDate?: number;
  remainingShelfLifeRatio?: number;
  safetyStock?: number;
  riskTypes?: string[];
  openTaskCount?: number;
  refNo?: string;
  refCategory?: number;
};

type ApiWarehouseInventoryLotListPayload = {
  total?: number;
  count?: number;
  start?: number;
  summary?: ApiWarehouseInventoryLotSummary;
  results?: ApiWarehouseInventoryLot[];
};

type ApiWarehouseInventoryRecordLine = {
  refCategory?: number;
  refNo?: string;
  refSubNo?: string;
  date?: number;
  category?: number;
  quantity?: number;
  amount?: number;
};

type ApiWarehouseReservationLine = {
  reservationNo?: string;
  refCategory?: number;
  refNo?: string;
  reservedQuantity?: number;
  reservedValue?: number;
  releaseTime?: number;
  status?: number;
};

type ApiWarehouseQualityHoldLine = {
  holdNo?: string;
  inspectionNo?: string;
  holdQuantity?: number;
  holdValue?: number;
  reason?: string;
  status?: number;
};

type ApiWarehousePalletMovementLine = {
  movementNo?: string;
  date?: number;
  palletGroupNo?: string;
  palletStatus?: number;
  palletCount?: number;
  refCategory?: number;
  refNo?: string;
};

type ApiWarehouseWorkflowTaskLine = {
  taskId?: string;
  taskType?: number;
  taskStatus?: number;
  ownerDepartment?: number;
  expectedQuantity?: number;
  processedQuantity?: number;
  remainingQuantity?: number;
  dueTimestamp?: number;
  blockReason?: string;
};

type ApiWarehouseInventoryLotDetailPayload = {
  lot?: ApiWarehouseInventoryLot;
  inventoryRecords?: ApiWarehouseInventoryRecordLine[];
  reservations?: ApiWarehouseReservationLine[];
  qualityHolds?: ApiWarehouseQualityHoldLine[];
  palletMovements?: ApiWarehousePalletMovementLine[];
  workflowTasks?: ApiWarehouseWorkflowTaskLine[];
};

type ApiWarehouseTaskWorkbenchSummary = {
  openTaskCount?: number;
  overdueTaskCount?: number;
  blockedTaskCount?: number;
  inboundTaskCount?: number;
  outboundTaskCount?: number;
  qualityTaskCount?: number;
  shipmentTaskCount?: number;
  inventoryShortageTaskCount?: number;
};

type ApiWarehouseTaskWorkbenchLane = {
  laneCode?: string;
  taskCount?: number;
  riskCount?: number;
};

type ApiWarehouseTaskWorkbenchItem = {
  taskId?: string;
  taskType?: number;
  taskStatus?: number;
  refCategory?: number;
  refNo?: string;
  refSubNo?: string;
  itemCategory?: number;
  itemNo?: string;
  itemName?: string;
  batchNo?: string;
  unit?: number;
  expectedQuantity?: number;
  processedQuantity?: number;
  remainingQuantity?: number;
  warehouseNo?: string;
  warehouseName?: string;
  dueTimestamp?: number;
  ownerDepartment?: number;
  riskLevel?: number;
  riskTypes?: string[];
  blockReasonCode?: string;
  blockReason?: string;
  availableQuantity?: number;
  reservedQuantity?: number;
  qualityHoldQuantity?: number;
  inventoryValue?: number;
  nextActionCode?: string;
};

type ApiWarehouseTaskWorkbenchPayload = {
  serverTimestamp?: number;
  timezone?: string;
  range?: {
    mode?: string;
    startTimestamp?: number;
    endTimestamp?: number;
  };
  summary?: ApiWarehouseTaskWorkbenchSummary;
  lanes?: ApiWarehouseTaskWorkbenchLane[];
  total?: number;
  count?: number;
  start?: number;
  results?: ApiWarehouseTaskWorkbenchItem[];
};

type ApiWarehouseTaskRelatedLot = {
  lotKey?: string;
  warehouseNo?: string;
  itemNo?: string;
  itemName?: string;
  batchNo?: string;
  currentQuantity?: number;
  availableQuantity?: number;
  qualityHoldQuantity?: number;
  validDate?: number;
  riskTypes?: string[];
};

type ApiWarehouseTaskSourceRef = {
  refCategory?: number;
  refNo?: string;
  refSubNo?: string;
  descriptionCode?: string;
};

type ApiWarehouseTaskTimelineEvent = {
  eventCode?: string;
  eventTimestamp?: number;
  department?: number;
  status?: number;
  comment?: string;
};

type ApiWarehouseTaskDetailPayload = {
  task?: ApiWarehouseTaskWorkbenchItem;
  quantity?: ApiWarehouseTaskWorkbenchItem;
  relatedLots?: ApiWarehouseTaskRelatedLot[];
  sourceRefs?: ApiWarehouseTaskSourceRef[];
  timeline?: ApiWarehouseTaskTimelineEvent[];
};

type ApiWarehouseAnalyticsRange = {
  period?: string;
  bucket?: string;
  startTimestamp?: number;
  endTimestamp?: number;
};

type ApiWarehouseAnalyticsKpi = {
  totalInventoryValue?: number;
  valueChangeRate?: number;
  usedPallets?: number;
  spaceUtilizationRate?: number;
  riskLotCount?: number;
  openTaskCount?: number;
  overdueTaskRate?: number;
};

type ApiWarehouseAnalyticsValueTrendPoint = {
  bucketStart?: number;
  bucketLabel?: string;
  itemCategory?: number;
  inventoryValue?: number;
  availableValue?: number;
  reservedValue?: number;
  qualityHoldValue?: number;
};

type ApiWarehouseAnalyticsSpaceTrendPoint = {
  bucketStart?: number;
  warehouseNo?: string;
  warehouseName?: string;
  usedPallets?: number;
  reservedPallets?: number;
  availablePallets?: number;
  utilizationRate?: number;
};

type ApiWarehouseAnalyticsRiskBreakdownItem = {
  riskType?: string;
  riskLevel?: number;
  lotCount?: number;
  inventoryValue?: number;
  quantity?: number;
};

type ApiWarehouseAnalyticsTaskSlaItem = {
  taskType?: number;
  openTaskCount?: number;
  completedTaskCount?: number;
  overdueTaskCount?: number;
  blockedTaskCount?: number;
  onTimeRate?: number;
  averageLeadTimeHours?: number;
};

type ApiWarehouseAnalyticsOverviewPayload = {
  serverTimestamp?: number;
  timezone?: string;
  range?: ApiWarehouseAnalyticsRange;
  kpi?: ApiWarehouseAnalyticsKpi;
  valueTrend?: ApiWarehouseAnalyticsValueTrendPoint[];
  spaceTrend?: ApiWarehouseAnalyticsSpaceTrendPoint[];
  riskBreakdown?: ApiWarehouseAnalyticsRiskBreakdownItem[];
  taskSla?: ApiWarehouseAnalyticsTaskSlaItem[];
};

type ApiWarehouseAnalyticsCategorySummary = {
  itemCategory?: number;
  inventoryValue?: number;
  availableValue?: number;
  reservedValue?: number;
  qualityHoldValue?: number;
};

type ApiWarehouseAnalyticsWarehouseSummary = {
  warehouseNo?: string;
  warehouseName?: string;
  usedPallets?: number;
  reservedPallets?: number;
  availablePallets?: number;
  utilizationRate?: number;
};

type ApiWarehouseAnalyticsRiskSummary = {
  riskLotCount?: number;
  highRiskLotCount?: number;
  inventoryValue?: number;
  quantity?: number;
};

type ApiWarehouseAnalyticsTopRiskLot = {
  lotKey?: string;
  warehouseNo?: string;
  warehouseName?: string;
  itemNo?: string;
  itemName?: string;
  batchNo?: string;
  riskType?: string;
  riskLevel?: number;
  inventoryValue?: number;
  quantity?: number;
};

type ApiWarehouseAnalyticsTaskDepartmentSummary = {
  ownerDepartment?: number;
  openTaskCount?: number;
  overdueTaskCount?: number;
  blockedTaskCount?: number;
};

type ApiWarehouseAnalyticsOverdueTrendPoint = {
  bucketStart?: number;
  bucketLabel?: string;
  overdueTaskCount?: number;
  blockedTaskCount?: number;
};

type ApiWarehouseAnalyticsValueTrendPayload = {
  range?: ApiWarehouseAnalyticsRange;
  summaryByCategory?: ApiWarehouseAnalyticsCategorySummary[];
  valueTrend?: ApiWarehouseAnalyticsValueTrendPoint[];
};

type ApiWarehouseAnalyticsSpaceUtilizationPayload = {
  range?: ApiWarehouseAnalyticsRange;
  summaryByWarehouse?: ApiWarehouseAnalyticsWarehouseSummary[];
  spaceTrend?: ApiWarehouseAnalyticsSpaceTrendPoint[];
};

type ApiWarehouseAnalyticsRiskBreakdownPayload = {
  range?: ApiWarehouseAnalyticsRange;
  riskSummary?: ApiWarehouseAnalyticsRiskSummary;
  riskBreakdown?: ApiWarehouseAnalyticsRiskBreakdownItem[];
  topRiskLots?: ApiWarehouseAnalyticsTopRiskLot[];
};

type ApiWarehouseAnalyticsTaskSlaPayload = {
  range?: ApiWarehouseAnalyticsRange;
  summaryByTaskType?: ApiWarehouseAnalyticsTaskSlaItem[];
  summaryByDepartment?: ApiWarehouseAnalyticsTaskDepartmentSummary[];
  overdueTrend?: ApiWarehouseAnalyticsOverdueTrendPoint[];
};

export type WarehouseDashboardResult = {
  data: WarehouseDashboardData;
  source: WarehouseDataSource;
  error?: string;
};

export type WarehouseInventoryResult = {
  records: WarehouseRecord[];
  source: WarehouseDataSource;
  error?: string;
};

export type WarehouseTasksResult = {
  tasks: WarehouseTask[];
  source: WarehouseDataSource;
  error?: string;
};

export type WarehouseInventoryLotsQuery = {
  warehouseNo?: string;
  itemCategory?: number;
  itemNo?: string;
  batchNo?: string;
  riskType?: string;
  taskType?: number;
  availability?: "available" | "reserved" | "quality_hold" | "blocked";
  keyword?: string;
  sort?: "inventoryValue" | "availableQuantity" | "validDate" | "daysInStock";
  order?: "asc" | "desc";
  start?: number;
  count?: number;
};

export type WarehouseInventoryLotsResult = {
  data: WarehouseInventoryLotListData;
  source: WarehouseDataSource;
  error?: string;
};

export type WarehouseInventoryLotDetailResult = {
  detail?: WarehouseInventoryLotDetail;
  source: WarehouseDataSource;
  error?: string;
};

export type WarehouseTaskWorkbenchQuery = {
  dateRange?: "today" | "next_7_days" | "overdue" | "all_open";
  warehouseNo?: string;
  taskType?: number;
  status?: string | number;
  ownerDepartment?: number;
  riskOnly?: boolean;
  keyword?: string;
  sort?: "dueTimestamp" | "taskType" | "remainingQuantity" | "riskLevel";
  order?: "asc" | "desc";
  start?: number;
  count?: number;
};

export type WarehouseTaskWorkbenchResult = {
  data: WarehouseTaskWorkbenchData;
  source: WarehouseDataSource;
  error?: string;
};

export type WarehouseTaskDetailResult = {
  detail?: WarehouseTaskDetail;
  source: WarehouseDataSource;
  error?: string;
};

export type WarehouseAnalyticsQuery = {
  date?: number;
  period?: WarehouseAnalyticsPeriod;
  bucket?: WarehouseAnalyticsBucket;
  warehouseNo?: string;
  itemCategory?: number;
  taskType?: number;
};

export type WarehouseAnalyticsOverviewResult = {
  data: WarehouseAnalyticsOverviewData;
  source: WarehouseDataSource;
  error?: string;
};

export type WarehouseAnalyticsValueTrendResult = {
  data: WarehouseAnalyticsValueTrendData;
  source: WarehouseDataSource;
  error?: string;
};

export type WarehouseAnalyticsSpaceUtilizationResult = {
  data: WarehouseAnalyticsSpaceUtilizationData;
  source: WarehouseDataSource;
  error?: string;
};

export type WarehouseAnalyticsRiskBreakdownResult = {
  data: WarehouseAnalyticsRiskBreakdownData;
  source: WarehouseDataSource;
  error?: string;
};

export type WarehouseAnalyticsTaskSlaResult = {
  data: WarehouseAnalyticsTaskSlaData;
  source: WarehouseDataSource;
  error?: string;
};

const CATEGORY_LABELS: Record<number, InventoryCategory> = {
  1: "原料" as InventoryCategory,
  2: "物料" as InventoryCategory,
  3: "膠捲" as InventoryCategory,
  4: "在製品" as InventoryCategory,
  5: "製成品" as InventoryCategory
};

const SOURCE_REF_CATEGORY_LABELS: Record<number, WarehouseSourceType> = {
  0: "調整" as WarehouseSourceType,
  1: "採購" as WarehouseSourceType,
  2: "生產" as WarehouseSourceType,
  3: "銷退" as WarehouseSourceType
};

const UNIT_LABELS: Record<number, string> = {
  0: "其他",
  1: "公克",
  2: "公斤",
  3: "台斤",
  51: "公分",
  52: "公尺",
  101: "個",
  102: "條",
  103: "片",
  104: "張",
  105: "罐",
  106: "包",
  107: "捲",
  108: "桶",
  109: "盒",
  110: "組",
  111: "箱",
  112: "支",
  113: "式",
  114: "入",
  115: "袋",
  116: "顆",
  117: "瓶",
  201: "板",
  202: "件",
  203: "車",
  204: "次"
};

const RECOMMENDED_ACTION_LABELS: Record<string, string> = {
  "warehouse.action.prioritizeIssueOrProduction": "優先安排領料或生產使用",
  "warehouse.action.reviewSlowMovingStock": "檢討呆滯庫存處理",
  "warehouse.action.reviewSafetyStock": "檢查安全庫存與補貨設定",
  "warehouse.action.reviewExpiryRisk": "檢查效期風險並安排優先使用",
  "warehouse.action.reviewQualityHold": "確認品保 hold 狀態"
};

const RISK_TYPE_LABELS: Record<string, string> = {
  TURNOVER_OVER_30_DAYS: "迴轉超過一個月",
  SHELF_LIFE_LT_ONE_THIRD: "少於 1/3 效期",
  BELOW_SAFETY_STOCK: "低於安全水位"
};

const RESERVATION_REF_CATEGORY_LABELS: Record<number, string> = {
  0: "其他",
  1: "銷售 / 訂購",
  2: "生產 / 工單",
  3: "倉庫任務"
};

const PALLET_MOVEMENT_REF_CATEGORY_LABELS: Record<number, string> = {
  1: "入庫",
  2: "出庫",
  3: "移倉",
  4: "預留",
  5: "品檢保留",
  6: "釋放"
};

const TASK_STATUS_LABELS: Record<number, string> = {
  1: "待處理",
  2: "部分完成",
  3: "已完成",
  4: "阻塞",
  5: "取消"
};

const WORKFLOW_TASK_TYPE_LABELS: Record<number, string> = {
  1: "請購",
  2: "採購",
  3: "進貨",
  4: "入庫",
  5: "出庫",
  6: "移倉",
  7: "生產",
  8: "品檢",
  9: "出貨"
};

function formatNumber(value: number) {
  return new Intl.NumberFormat("zh-TW").format(Math.round(value));
}

function formatMoneyCompact(value: number) {
  if (Math.abs(value) >= 1000000) {
    return `$${(value / 1000000).toFixed(2)}M`;
  }
  return `$${formatNumber(value)}`;
}

function categoryLabel(value?: number): InventoryCategory {
  return CATEGORY_LABELS[value ?? 0] ?? ("原料" as InventoryCategory);
}

function unitLabel(value?: number) {
  return value === undefined || value === null ? "" : (UNIT_LABELS[value] ?? `單位 ${value}`);
}

function sourceRefCategoryLabel(value?: number): WarehouseSourceType {
  return value === undefined || value === null
    ? ("調整" as WarehouseSourceType)
    : (SOURCE_REF_CATEGORY_LABELS[value] ?? ("倉庫" as WarehouseSourceType));
}

function toneByRiskLevel(value?: number): StatusTone {
  if (value === 3) {
    return "danger";
  }
  if (value === 2) {
    return "warning";
  }
  if (value === 1) {
    return "success";
  }
  return "info";
}

function toneByUtilization(value?: number): StatusTone {
  if ((value ?? 0) >= 90) {
    return "danger";
  }
  if ((value ?? 0) >= 75) {
    return "warning";
  }
  return "success";
}

function riskTypeLabel(value?: string): WarehouseRisk["type"] {
  if (value === "SHELF_LIFE_LT_ONE_THIRD") {
    return "少於 1/3 效期";
  }
  if (value === "BELOW_SAFETY_STOCK") {
    return "低於安全水位";
  }
  return "迴轉超過一個月";
}

function taskTypeLabel(value?: number): WarehouseTask["type"] {
  if (value === 5 || value === 9) {
    return "出庫";
  }
  if (value === 6) {
    return "移倉";
  }
  if (value === 4 || value === 3) {
    return "入庫";
  }
  return "入庫";
}

function ownerDepartmentLabel(value?: number) {
  const labels: Record<number, string> = {
    1: "業務",
    2: "研發",
    3: "採購",
    4: "生管",
    5: "製造",
    6: "品保",
    7: "倉庫",
    8: "物流",
    9: "財務"
  };
  return labels[value ?? 0] ?? "待指派";
}

function timestampToDate(value?: number) {
  if (!value) {
    return "";
  }
  return new Date(value * 1000).toLocaleDateString("zh-TW", {
    timeZone: "Asia/Taipei"
  });
}

function timestampToTime(value?: number) {
  if (!value) {
    return "";
  }
  return new Date(value * 1000).toLocaleTimeString("zh-TW", {
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "Asia/Taipei"
  });
}

function timestampToDateTime(value?: number) {
  if (!value) {
    return "";
  }
  return new Date(value * 1000).toLocaleString("zh-TW", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "Asia/Taipei"
  });
}

function riskLabels(values?: string[]) {
  return withFallbackArray<string>(values, []).map((value) => RISK_TYPE_LABELS[value] ?? value);
}

function riskTone(values?: string[]): StatusTone {
  const risks = withFallbackArray<string>(values, []);
  if (risks.includes("SHELF_LIFE_LT_ONE_THIRD")) {
    return "danger";
  }
  if (risks.length) {
    return "warning";
  }
  return "success";
}

function riskLabel(values?: string[]) {
  const labels = riskLabels(values);
  return labels.length ? labels.join(" / ") : "正常";
}

function reservationRefCategoryLabel(value?: number) {
  return value === undefined || value === null ? "其他" : (RESERVATION_REF_CATEGORY_LABELS[value] ?? `來源 ${value}`);
}

function palletMovementRefCategoryLabel(value?: number) {
  return value === undefined || value === null
    ? "其他"
    : (PALLET_MOVEMENT_REF_CATEGORY_LABELS[value] ?? `來源 ${value}`);
}

function inventoryRecordCategoryLabel(value?: number): WarehouseInventoryRecordLine["categoryLabel"] {
  if (value === 1) {
    return "入庫";
  }
  if (value === 2) {
    return "出庫";
  }
  return "其他";
}

function taskStatusTone(value?: number): StatusTone {
  if (value === 4) {
    return "danger";
  }
  if (value === 2) {
    return "warning";
  }
  if (value === 3) {
    return "success";
  }
  return "info";
}

function buildKpis(payload: ApiWarehousePayload): WarehouseKpi[] {
  const summary = payload.summary ?? {};
  const totalPallets = summary.totalPallets ?? 0;
  const usedPallets = summary.usedPallets ?? 0;
  const utilization = totalPallets ? Math.round((usedPallets / totalPallets) * 100) : 0;
  const pendingCount = (summary.pendingInboundCount ?? 0) + (summary.pendingOutboundCount ?? 0);

  return [
    {
      label: "庫存總價值",
      value: formatMoneyCompact(summary.totalInventoryValue ?? 0),
      hint: `可用 ${formatMoneyCompact(summary.availableInventoryValue ?? 0)}，預留 ${formatMoneyCompact(summary.reservedInventoryValue ?? 0)}`,
      tone: "info"
    },
    {
      label: "倉位使用率",
      value: `${utilization}%`,
      hint: `已用 ${formatNumber(usedPallets)} 板，可用 ${formatNumber(summary.availablePallets ?? 0)} 板`,
      tone: toneByUtilization(utilization)
    },
    {
      label: "風險品項",
      value: formatNumber(summary.riskAlertCount ?? 0),
      hint: "迴轉、效期與安全水位警示",
      tone: (summary.riskAlertCount ?? 0) > 0 ? "danger" : "success"
    },
    {
      label: "今日待處理",
      value: formatNumber(pendingCount),
      hint: `入庫 ${formatNumber(summary.pendingInboundCount ?? 0)}，出庫 ${formatNumber(summary.pendingOutboundCount ?? 0)}`,
      tone: pendingCount > 0 ? "warning" : "success"
    }
  ];
}

function mapCategorySummaries(payload: ApiWarehousePayload): WarehouseCategorySummary[] {
  return withFallbackArray<ApiWarehouseCategory>(payload.inventoryValueByCategory, []).map((item) => ({
    category: categoryLabel(item.itemCategory),
    amount: item.inventoryValue ?? 0,
    amountRatio: item.valueRatio ?? 0,
    reservedAmount: item.reservedValue ?? 0,
    availableAmount: item.availableValue ?? 0,
    palletCount: item.palletCount ?? 0,
    itemCount: item.itemCount ?? 0,
    trend7Days: item.trend7Days ?? 0,
    tone: (item.trend7Days ?? 0) > 0 ? "warning" : "success"
  }));
}

function mapCapacities(payload: ApiWarehousePayload): WarehouseCapacity[] {
  return withFallbackArray<ApiWarehouseCapacity>(payload.capacityByWarehouse, []).map((item) => ({
    id: item.warehouseNo ?? "",
    warehouseName: item.warehouseName || item.warehouseNo || "未命名倉儲",
    warehouseType: item.warehouseType ? `類型 ${item.warehouseType}` : "未分類",
    totalPallets: item.totalPallets ?? 0,
    usedPallets: item.usedPallets ?? 0,
    reservedPallets: item.reservedPallets ?? 0,
    availablePallets: item.availablePallets ?? 0,
    tone: toneByRiskLevel(item.riskLevel) || toneByUtilization(item.utilizationRate)
  }));
}

function mapRisks(payload: ApiWarehousePayload): WarehouseRisk[] {
  return withFallbackArray<ApiWarehouseRisk>(payload.riskAlerts, [])
    .filter((item) => (item.quantity ?? 0) > 0 || item.riskType !== "BELOW_SAFETY_STOCK")
    .map((item) => ({
      id: item.alertId ?? `${item.riskType}-${item.warehouseNo}-${item.itemNo}-${item.batchNo}`,
      type: riskTypeLabel(item.riskType),
      itemName: item.itemName ?? "",
      category: categoryLabel(item.itemCategory),
      batchNo: item.batchNo ?? "",
      warehouseName: item.warehouseName ?? "",
      metric: buildRiskMetric(item),
      recommendation: actionLabel(item.recommendedActionCode),
      tone: toneByRiskLevel(item.riskLevel)
    }));
}

function buildRiskMetric(item: ApiWarehouseRisk) {
  if (item.riskType === "SHELF_LIFE_LT_ONE_THIRD") {
    return `剩餘效期比例 ${Math.round((item.remainingShelfLifeRatio ?? 0) * 100)}%`;
  }
  if (item.riskType === "BELOW_SAFETY_STOCK") {
    return `${formatNumber(item.quantity ?? 0)} / 安全水位 ${formatNumber(item.safetyStock ?? 0)}`;
  }
  return `庫齡 ${formatNumber(item.daysInStock ?? 0)} 天`;
}

function mapTasks(payload: ApiWarehousePayload): WarehouseTask[] {
  return withFallbackArray<ApiWarehouseTask>(payload.pendingTasks, []).map((item) => ({
    id: item.taskId ?? "",
    type: taskTypeLabel(item.taskType),
    itemName: item.itemName ?? "",
    batchNo: item.batchNo ?? "",
    quantity: item.remainingQuantity ?? item.expectedQuantity ?? 0,
    unit: unitLabel(item.unit),
    palletCount: item.palletCount ?? 0,
    owner: ownerDepartmentLabel(item.ownerDepartment),
    dueTime: timestampToTime(item.dueTimestamp),
    sourceNo: item.sourceNo ?? "",
    status: item.blockReason || `狀態 ${item.taskStatus ?? 0}`,
    tone: item.taskStatus === 4 ? "danger" : item.taskStatus === 2 ? "warning" : "info"
  }));
}

function actionLabel(value?: string) {
  if (!value) {
    return "請依風險類型安排後續處理。";
  }
  return RECOMMENDED_ACTION_LABELS[value] ?? value;
}

function mapRecords(payload: ApiWarehousePayload, risks: WarehouseRisk[], tasks: WarehouseTask[]): WarehouseRecord[] {
  const riskByBatch = new Map(risks.map((risk) => [risk.batchNo, risk]));
  const taskByBatch = new Map(tasks.map((task) => [task.batchNo, task]));

  return withFallbackArray<ApiWarehouseInventory>(payload.inventory, []).filter((item) => (item.currentQuantity ?? 0) > 0).map((item) => {
    const risk = riskByBatch.get(item.batchNo ?? "");
    const task = taskByBatch.get(item.batchNo ?? "");
    const sourceLabel = sourceRefCategoryLabel(item.sourceRefCategory);
    const workflow = buildWorkflow(item, task);
    return {
      id: `${item.warehouseNo ?? ""}-${item.itemNo ?? ""}-${item.batchNo ?? ""}`,
      itemNo: item.itemNo ?? "",
      itemName: item.itemName ?? "",
      category: categoryLabel(item.itemCategory),
      warehouseNo: item.warehouseNo ?? "",
      warehouseName: item.warehouseName ?? "",
      batchNo: item.batchNo ?? "",
      sourceLabel,
      sourceNo: item.sourceNo ?? "",
      quantity: item.currentQuantity ?? 0,
      reservedQuantity: item.reservedQuantity ?? 0,
      availableQuantity: item.availableQuantity ?? 0,
      unit: unitLabel(item.unit),
      amount: item.inventoryValue ?? 0,
      reservedAmount: item.reservedValue ?? 0,
      availableAmount: item.availableValue ?? 0,
      palletCount: (item as { palletCount?: number }).palletCount ?? 0,
      safetyStock: (item as { safetyStock?: number }).safetyStock ?? 0,
      expiryDate: timestampToDate(item.validDate),
      shelfLifeDays: item.validDays ?? 0,
      daysLeft: calculateDaysLeft(item.validDate),
      turnoverDays: (item as { daysInStock?: number }).daysInStock ?? 0,
      status: risk?.type ?? ((item.availableQuantity ?? 0) > 0 ? "可用" : "已預留"),
      tone: risk?.tone ?? ((item.availableQuantity ?? 0) > 0 ? "success" : "warning"),
      workflow,
      relatedDocuments: buildRelatedDocuments(item, risk, task)
    };
  });
}

function mapLotSummary(summary?: ApiWarehouseInventoryLotSummary): WarehouseInventoryLotSummary {
  return {
    lotCount: summary?.lotCount ?? 0,
    itemCount: summary?.itemCount ?? 0,
    totalQuantity: summary?.totalQuantity ?? 0,
    totalInventoryValue: summary?.totalInventoryValue ?? 0,
    totalAvailableQuantity: summary?.totalAvailableQuantity ?? 0,
    totalAvailableValue: summary?.totalAvailableValue ?? 0,
    riskLotCount: summary?.riskLotCount ?? 0,
    pendingTaskCount: summary?.pendingTaskCount ?? 0
  };
}

function mapLot(item: ApiWarehouseInventoryLot): WarehouseInventoryLot {
  const currentQuantity = item.currentQuantity ?? 0;
  const inventoryValue = item.inventoryValue ?? 0;
  return {
    lotKey: item.lotKey ?? `${item.warehouseNo ?? ""}|${item.itemNo ?? ""}|${item.batchNo ?? ""}`,
    warehouseNo: item.warehouseNo ?? "",
    warehouseName: item.warehouseName ?? "",
    category: categoryLabel(item.itemCategory),
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    batchNo: item.batchNo ?? "",
    unit: unitLabel(item.unit),
    currentQuantity,
    reservedQuantity: item.reservedQuantity ?? 0,
    qualityHoldQuantity: item.qualityHoldQuantity ?? 0,
    availableQuantity: item.availableQuantity ?? 0,
    unitCost: item.unitCost ?? (currentQuantity ? inventoryValue / currentQuantity : 0),
    inventoryValue,
    reservedValue: item.reservedValue ?? 0,
    qualityHoldValue: item.qualityHoldValue ?? 0,
    availableValue: item.availableValue ?? 0,
    palletCount: item.palletCount ?? 0,
    firstInboundDate: timestampToDate(item.firstInboundTimestamp),
    daysInStock: item.daysInStock ?? 0,
    validDays: item.validDays ?? 0,
    validDate: timestampToDate(item.validDate),
    remainingShelfLifeRatio: item.remainingShelfLifeRatio ?? 0,
    safetyStock: item.safetyStock ?? 0,
    riskTypes: riskLabels(item.riskTypes),
    riskLabel: riskLabel(item.riskTypes),
    riskTone: riskTone(item.riskTypes),
    openTaskCount: item.openTaskCount ?? 0,
    refNo: item.refNo ?? "",
    refCategoryLabel: sourceRefCategoryLabel(item.refCategory)
  };
}

function mapLotListPayload(payload: ApiWarehouseInventoryLotListPayload): WarehouseInventoryLotListData {
  const lots = withFallbackArray<ApiWarehouseInventoryLot>(payload.results, []).map(mapLot);
  return {
    summary: mapLotSummary(payload.summary),
    lots,
    total: payload.total ?? lots.length,
    count: payload.count ?? lots.length,
    start: payload.start ?? 0
  };
}

function mapInventoryRecordLine(item: ApiWarehouseInventoryRecordLine, index: number): WarehouseInventoryRecordLine {
  const categoryLabel = inventoryRecordCategoryLabel(item.category);
  return {
    id: `${item.refNo ?? "record"}-${item.date ?? index}-${index}`,
    refCategoryLabel: sourceRefCategoryLabel(item.refCategory),
    refNo: item.refNo ?? "",
    refSubNo: item.refSubNo ?? "",
    date: timestampToDateTime(item.date),
    categoryLabel,
    quantity: item.quantity ?? 0,
    amount: item.amount ?? 0,
    tone: categoryLabel === "出庫" ? "warning" : categoryLabel === "入庫" ? "success" : "info"
  };
}

function mapReservationLine(item: ApiWarehouseReservationLine, index: number): WarehouseReservationLine {
  return {
    id: item.reservationNo ?? `reservation-${index}`,
    reservationNo: item.reservationNo ?? "",
    refCategoryLabel: reservationRefCategoryLabel(item.refCategory),
    refNo: item.refNo ?? "",
    reservedQuantity: item.reservedQuantity ?? 0,
    reservedValue: item.reservedValue ?? 0,
    releaseDate: timestampToDateTime(item.releaseTime),
    status: item.status ? `狀態 ${item.status}` : "有效預留",
    tone: item.status === 3 ? "success" : "warning"
  };
}

function mapQualityHoldLine(item: ApiWarehouseQualityHoldLine, index: number): WarehouseQualityHoldLine {
  return {
    id: item.holdNo ?? `quality-hold-${index}`,
    holdNo: item.holdNo ?? "",
    inspectionNo: item.inspectionNo ?? "",
    holdQuantity: item.holdQuantity ?? 0,
    holdValue: item.holdValue ?? 0,
    reason: item.reason ?? "",
    status: item.status ? `狀態 ${item.status}` : "保留中",
    tone: item.status === 3 ? "success" : "warning"
  };
}

function mapPalletMovementLine(item: ApiWarehousePalletMovementLine, index: number): WarehousePalletMovementLine {
  return {
    id: item.movementNo ?? `pallet-${index}`,
    movementNo: item.movementNo ?? "",
    date: timestampToDateTime(item.date),
    palletGroupNo: item.palletGroupNo ?? "",
    palletStatus: item.palletStatus ? `狀態 ${item.palletStatus}` : "使用中",
    palletCount: item.palletCount ?? 0,
    refCategoryLabel: palletMovementRefCategoryLabel(item.refCategory),
    refNo: item.refNo ?? "",
    tone: item.refCategory === 6 ? "success" : "info"
  };
}

function mapWorkflowTaskLine(item: ApiWarehouseWorkflowTaskLine, index: number): WarehouseWorkflowTaskLine {
  return {
    id: item.taskId ?? `workflow-task-${index}`,
    taskId: item.taskId ?? "",
    taskTypeLabel: item.taskType ? (WORKFLOW_TASK_TYPE_LABELS[item.taskType] ?? `任務 ${item.taskType}`) : "任務",
    taskStatusLabel: item.taskStatus ? (TASK_STATUS_LABELS[item.taskStatus] ?? `狀態 ${item.taskStatus}`) : "待處理",
    ownerDepartmentLabel: ownerDepartmentLabel(item.ownerDepartment),
    expectedQuantity: item.expectedQuantity ?? 0,
    processedQuantity: item.processedQuantity ?? 0,
    remainingQuantity: item.remainingQuantity ?? 0,
    dueDate: timestampToDateTime(item.dueTimestamp),
    blockReason: item.blockReason ?? "",
    tone: taskStatusTone(item.taskStatus)
  };
}

function mapLotDetailPayload(payload: ApiWarehouseInventoryLotDetailPayload): WarehouseInventoryLotDetail | undefined {
  if (!payload.lot) {
    return undefined;
  }
  return {
    lot: mapLot(payload.lot),
    inventoryRecords: withFallbackArray<ApiWarehouseInventoryRecordLine>(payload.inventoryRecords, []).map(
      mapInventoryRecordLine
    ),
    reservations: withFallbackArray<ApiWarehouseReservationLine>(payload.reservations, []).map(mapReservationLine),
    qualityHolds: withFallbackArray<ApiWarehouseQualityHoldLine>(payload.qualityHolds, []).map(mapQualityHoldLine),
    palletMovements: withFallbackArray<ApiWarehousePalletMovementLine>(payload.palletMovements, []).map(
      mapPalletMovementLine
    ),
    workflowTasks: withFallbackArray<ApiWarehouseWorkflowTaskLine>(payload.workflowTasks, []).map(mapWorkflowTaskLine)
  };
}

function mockLotList(): WarehouseInventoryLotListData {
  const lots = warehouseDashboardMock.records.map((record) =>
    mapLot({
      lotKey: `${record.warehouseNo}|${record.itemNo}|${record.batchNo}`,
      warehouseNo: record.warehouseNo,
      warehouseName: record.warehouseName,
      itemCategory: 0,
      itemNo: record.itemNo,
      itemName: record.itemName,
      batchNo: record.batchNo,
      currentQuantity: record.quantity,
      reservedQuantity: record.reservedQuantity,
      availableQuantity: record.availableQuantity,
      inventoryValue: record.amount,
      reservedValue: record.reservedAmount,
      availableValue: record.availableAmount,
      palletCount: record.palletCount,
      daysInStock: record.turnoverDays,
      validDays: record.shelfLifeDays,
      safetyStock: record.safetyStock,
      riskTypes: record.tone === "danger" ? ["SHELF_LIFE_LT_ONE_THIRD"] : record.tone === "warning" ? ["TURNOVER_OVER_30_DAYS"] : [],
      openTaskCount: warehouseDashboardMock.tasks.filter((task) => task.batchNo === record.batchNo).length,
      refNo: record.sourceNo
    })
  );
  return {
    summary: {
      lotCount: lots.length,
      itemCount: new Set(lots.map((lot) => lot.itemNo)).size,
      totalQuantity: lots.reduce((sum, lot) => sum + lot.currentQuantity, 0),
      totalInventoryValue: lots.reduce((sum, lot) => sum + lot.inventoryValue, 0),
      totalAvailableQuantity: lots.reduce((sum, lot) => sum + lot.availableQuantity, 0),
      totalAvailableValue: lots.reduce((sum, lot) => sum + lot.availableValue, 0),
      riskLotCount: lots.filter((lot) => lot.riskTypes.length).length,
      pendingTaskCount: lots.reduce((sum, lot) => sum + lot.openTaskCount, 0)
    },
    lots,
    total: lots.length,
    count: lots.length,
    start: 0
  };
}

function mockLotDetail(lot?: WarehouseInventoryLot): WarehouseInventoryLotDetail | undefined {
  const selectedLot = lot ?? mockLotList().lots[0];
  if (!selectedLot) {
    return undefined;
  }
  return {
    lot: selectedLot,
    inventoryRecords: [
      {
        id: `${selectedLot.lotKey}-in`,
        refCategoryLabel: selectedLot.refCategoryLabel,
        refNo: selectedLot.refNo,
        refSubNo: "",
        date: selectedLot.firstInboundDate,
        categoryLabel: "入庫",
        quantity: selectedLot.currentQuantity + selectedLot.reservedQuantity,
        amount: selectedLot.inventoryValue,
        tone: "success"
      }
    ],
    reservations: selectedLot.reservedQuantity
      ? [
          {
            id: `${selectedLot.lotKey}-reservation`,
            reservationNo: "MOCK-RES",
            refCategoryLabel: "生產 / 工單",
            refNo: selectedLot.refNo,
            reservedQuantity: selectedLot.reservedQuantity,
            reservedValue: selectedLot.reservedValue,
            releaseDate: "",
            status: "有效預留",
            tone: "warning"
          }
        ]
      : [],
    qualityHolds: selectedLot.qualityHoldQuantity
      ? [
          {
            id: `${selectedLot.lotKey}-hold`,
            holdNo: "MOCK-QH",
            inspectionNo: "",
            holdQuantity: selectedLot.qualityHoldQuantity,
            holdValue: selectedLot.qualityHoldValue,
            reason: "待品保確認",
            status: "保留中",
            tone: "warning"
          }
        ]
      : [],
    palletMovements: [
      {
        id: `${selectedLot.lotKey}-pallet`,
        movementNo: "MOCK-PAL",
        date: selectedLot.firstInboundDate,
        palletGroupNo: selectedLot.warehouseNo,
        palletStatus: "使用中",
        palletCount: selectedLot.palletCount,
        refCategoryLabel: "入庫",
        refNo: selectedLot.refNo,
        tone: "info"
      }
    ],
    workflowTasks: warehouseDashboardMock.tasks
      .filter((task) => task.batchNo === selectedLot.batchNo)
      .map((task) => ({
        id: task.id,
        taskId: task.id,
        taskTypeLabel: task.type,
        taskStatusLabel: task.status,
        ownerDepartmentLabel: task.owner,
        expectedQuantity: task.quantity,
        processedQuantity: 0,
        remainingQuantity: task.quantity,
        dueDate: task.dueTime,
        blockReason: "",
        tone: task.tone
      }))
  };
}

function mapTaskWorkbenchSummary(summary?: ApiWarehouseTaskWorkbenchSummary): WarehouseTaskWorkbenchSummary {
  return {
    openTaskCount: summary?.openTaskCount ?? 0,
    overdueTaskCount: summary?.overdueTaskCount ?? 0,
    blockedTaskCount: summary?.blockedTaskCount ?? 0,
    inboundTaskCount: summary?.inboundTaskCount ?? 0,
    outboundTaskCount: summary?.outboundTaskCount ?? 0,
    qualityTaskCount: summary?.qualityTaskCount ?? 0,
    shipmentTaskCount: summary?.shipmentTaskCount ?? 0,
    inventoryShortageTaskCount: summary?.inventoryShortageTaskCount ?? 0
  };
}

function mapTaskWorkbenchLane(item: ApiWarehouseTaskWorkbenchLane): WarehouseTaskWorkbenchLane {
  return {
    laneCode: item.laneCode ?? "inbound",
    taskCount: item.taskCount ?? 0,
    riskCount: item.riskCount ?? 0
  };
}

function mapTaskWorkbenchItem(item: ApiWarehouseTaskWorkbenchItem, index: number): WarehouseTaskWorkbenchItem {
  return {
    taskId: item.taskId ?? `warehouse-task-${index}`,
    taskType: item.taskType,
    taskStatus: item.taskStatus,
    refCategory: item.refCategory,
    refNo: item.refNo ?? "",
    refSubNo: item.refSubNo ?? "",
    itemCategory: item.itemCategory,
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    batchNo: item.batchNo ?? "",
    unit: item.unit,
    expectedQuantity: item.expectedQuantity ?? 0,
    processedQuantity: item.processedQuantity ?? 0,
    remainingQuantity: item.remainingQuantity ?? Math.max((item.expectedQuantity ?? 0) - (item.processedQuantity ?? 0), 0),
    warehouseNo: item.warehouseNo ?? "",
    warehouseName: item.warehouseName ?? "",
    dueDate: timestampToDateTime(item.dueTimestamp),
    ownerDepartment: item.ownerDepartment,
    riskLevel: item.riskLevel,
    riskTypes: withFallbackArray<string>(item.riskTypes, []),
    blockReasonCode: item.blockReasonCode ?? "",
    blockReason: item.blockReason ?? "",
    availableQuantity: item.availableQuantity ?? 0,
    reservedQuantity: item.reservedQuantity ?? 0,
    qualityHoldQuantity: item.qualityHoldQuantity ?? 0,
    inventoryValue: item.inventoryValue ?? 0,
    nextActionCode: item.nextActionCode ?? ""
  };
}

function mapTaskWorkbenchPayload(payload: ApiWarehouseTaskWorkbenchPayload): WarehouseTaskWorkbenchData {
  const tasks = withFallbackArray<ApiWarehouseTaskWorkbenchItem>(payload.results, []).map(mapTaskWorkbenchItem);
  return {
    serverDate: timestampToDateTime(payload.serverTimestamp),
    range: {
      mode: payload.range?.mode ?? "today",
      startDate: timestampToDateTime(payload.range?.startTimestamp),
      endDate: timestampToDateTime(payload.range?.endTimestamp)
    },
    summary: mapTaskWorkbenchSummary(payload.summary),
    lanes: withFallbackArray<ApiWarehouseTaskWorkbenchLane>(payload.lanes, []).map(mapTaskWorkbenchLane),
    tasks,
    total: payload.total ?? tasks.length,
    count: payload.count ?? tasks.length,
    start: payload.start ?? 0
  };
}

function mapTaskRelatedLot(item: ApiWarehouseTaskRelatedLot, index: number): WarehouseTaskRelatedLot {
  return {
    lotKey: item.lotKey ?? `${item.warehouseNo ?? ""}|${item.itemNo ?? ""}|${item.batchNo ?? index}`,
    warehouseNo: item.warehouseNo ?? "",
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    batchNo: item.batchNo ?? "",
    currentQuantity: item.currentQuantity ?? 0,
    availableQuantity: item.availableQuantity ?? 0,
    qualityHoldQuantity: item.qualityHoldQuantity ?? 0,
    validDate: timestampToDate(item.validDate),
    riskTypes: withFallbackArray<string>(item.riskTypes, [])
  };
}

function mapTaskSourceRef(item: ApiWarehouseTaskSourceRef, index: number): WarehouseTaskSourceRef {
  return {
    refCategory: item.refCategory,
    refNo: item.refNo ?? "",
    refSubNo: item.refSubNo ?? "",
    descriptionCode: item.descriptionCode ?? `warehouse.source.${index}`
  };
}

function mapTaskTimelineEvent(item: ApiWarehouseTaskTimelineEvent, index: number): WarehouseTaskTimelineEvent {
  return {
    id: `${item.eventCode ?? "event"}-${item.eventTimestamp ?? index}-${index}`,
    eventCode: item.eventCode ?? "workflow.task.created",
    eventDate: timestampToDateTime(item.eventTimestamp),
    department: item.department,
    status: item.status,
    comment: item.comment ?? ""
  };
}

function mapTaskDetailPayload(payload: ApiWarehouseTaskDetailPayload): WarehouseTaskDetail | undefined {
  if (!payload.task) {
    return undefined;
  }
  const task = mapTaskWorkbenchItem(payload.task, 0);
  const quantity = mapTaskWorkbenchItem(
    {
      ...payload.task,
      ...payload.quantity
    },
    0
  );
  return {
    task: {
      taskId: task.taskId,
      taskType: task.taskType,
      taskStatus: task.taskStatus,
      refCategory: task.refCategory,
      refNo: task.refNo,
      refSubNo: task.refSubNo,
      ownerDepartment: task.ownerDepartment,
      warehouseNo: task.warehouseNo,
      warehouseName: task.warehouseName,
      dueDate: task.dueDate,
      blockReasonCode: task.blockReasonCode,
      blockReason: task.blockReason,
      riskLevel: task.riskLevel,
      riskTypes: task.riskTypes,
      nextActionCode: task.nextActionCode
    },
    quantity: {
      itemCategory: quantity.itemCategory,
      itemNo: quantity.itemNo,
      itemName: quantity.itemName,
      batchNo: quantity.batchNo,
      unit: quantity.unit,
      expectedQuantity: quantity.expectedQuantity,
      processedQuantity: quantity.processedQuantity,
      remainingQuantity: quantity.remainingQuantity,
      availableQuantity: quantity.availableQuantity,
      reservedQuantity: quantity.reservedQuantity,
      qualityHoldQuantity: quantity.qualityHoldQuantity
    },
    relatedLots: withFallbackArray<ApiWarehouseTaskRelatedLot>(payload.relatedLots, []).map(mapTaskRelatedLot),
    sourceRefs: withFallbackArray<ApiWarehouseTaskSourceRef>(payload.sourceRefs, []).map(mapTaskSourceRef),
    timeline: withFallbackArray<ApiWarehouseTaskTimelineEvent>(payload.timeline, []).map(mapTaskTimelineEvent)
  };
}

function inferLaneCode(task: WarehouseTaskWorkbenchItem) {
  if (task.taskStatus === 4 || task.riskTypes.includes("BLOCKED")) {
    return "blocked";
  }
  if (task.taskType === 3 || task.taskType === 4) {
    return "inbound";
  }
  if (task.taskType === 8) {
    return "quality";
  }
  if (task.taskType === 9) {
    return "shipment";
  }
  return "outbound";
}

function mockTaskWorkbench(): WarehouseTaskWorkbenchData {
  const now = Math.floor(Date.now() / 1000);
  const tasks = warehouseDashboardMock.tasks.map((task, index) =>
    mapTaskWorkbenchItem(
      {
        taskId: task.id,
        taskType: task.type === "入庫" ? 4 : task.type === "移倉" ? 6 : 5,
        taskStatus: task.tone === "danger" ? 4 : task.tone === "warning" ? 2 : 1,
        refCategory: task.sourceNo.startsWith("WO") ? 2 : task.sourceNo.startsWith("SO") ? 3 : 1,
        refNo: task.sourceNo,
        refSubNo: "",
        itemCategory: 1,
        itemNo: task.itemName,
        itemName: task.itemName,
        batchNo: task.batchNo,
        unit: task.unit === "kg" ? 2 : 101,
        expectedQuantity: task.quantity,
        processedQuantity: task.tone === "warning" ? Math.round(task.quantity * 0.35) : 0,
        remainingQuantity: task.quantity,
        warehouseNo: "WH-MOCK",
        warehouseName: "Warehouse mock",
        dueTimestamp: now + index * 3600,
        ownerDepartment: 7,
        riskLevel: task.tone === "danger" ? 3 : task.tone === "warning" ? 2 : 1,
        riskTypes: task.tone === "danger" ? ["BLOCKED", "INVENTORY_SHORTAGE"] : task.tone === "warning" ? ["QUALITY_HOLD"] : [],
        blockReasonCode: task.tone === "danger" ? "inventoryShortage" : "",
        blockReason: task.tone === "danger" ? task.status : "",
        availableQuantity: task.tone === "danger" ? 0 : task.quantity * 1.5,
        reservedQuantity: task.tone === "warning" ? task.quantity * 0.25 : 0,
        qualityHoldQuantity: task.tone === "warning" ? task.quantity * 0.1 : 0,
        inventoryValue: task.quantity * 120,
        nextActionCode:
          task.tone === "danger"
            ? "warehouse.task.resolveBlocker"
            : task.type === "入庫"
              ? "warehouse.task.arrangeInbound"
              : task.type === "移倉"
                ? "warehouse.task.arrangeTransfer"
                : "warehouse.task.prepareOutbound"
      },
      index
    )
  );

  const lanes = ["inbound", "outbound", "quality", "shipment", "blocked"].map((laneCode) => {
    const laneTasks = tasks.filter((task) => inferLaneCode(task) === laneCode);
    return {
      laneCode,
      taskCount: laneTasks.length,
      riskCount: laneTasks.filter((task) => task.riskTypes.length > 0).length
    };
  });

  return {
    serverDate: timestampToDateTime(now),
    range: {
      mode: "today",
      startDate: timestampToDateTime(now),
      endDate: timestampToDateTime(now + 86400)
    },
    summary: {
      openTaskCount: tasks.length,
      overdueTaskCount: 0,
      blockedTaskCount: tasks.filter((task) => task.taskStatus === 4).length,
      inboundTaskCount: tasks.filter((task) => task.taskType === 3 || task.taskType === 4).length,
      outboundTaskCount: tasks.filter((task) => task.taskType === 5 || task.taskType === 6).length,
      qualityTaskCount: tasks.filter((task) => task.taskType === 8).length,
      shipmentTaskCount: tasks.filter((task) => task.taskType === 9).length,
      inventoryShortageTaskCount: tasks.filter((task) => task.riskTypes.includes("INVENTORY_SHORTAGE")).length
    },
    lanes,
    tasks,
    total: tasks.length,
    count: tasks.length,
    start: 0
  };
}

function mockTaskDetail(taskId?: string): WarehouseTaskDetail | undefined {
  const workbench = mockTaskWorkbench();
  const task = workbench.tasks.find((item) => item.taskId === taskId) ?? workbench.tasks[0];
  if (!task) {
    return undefined;
  }
  return {
    task: {
      taskId: task.taskId,
      taskType: task.taskType,
      taskStatus: task.taskStatus,
      refCategory: task.refCategory,
      refNo: task.refNo,
      refSubNo: task.refSubNo,
      ownerDepartment: task.ownerDepartment,
      warehouseNo: task.warehouseNo,
      warehouseName: task.warehouseName,
      dueDate: task.dueDate,
      blockReasonCode: task.blockReasonCode,
      blockReason: task.blockReason,
      riskLevel: task.riskLevel,
      riskTypes: task.riskTypes,
      nextActionCode: task.nextActionCode
    },
    quantity: {
      itemCategory: task.itemCategory,
      itemNo: task.itemNo,
      itemName: task.itemName,
      batchNo: task.batchNo,
      unit: task.unit,
      expectedQuantity: task.expectedQuantity,
      processedQuantity: task.processedQuantity,
      remainingQuantity: task.remainingQuantity,
      availableQuantity: task.availableQuantity,
      reservedQuantity: task.reservedQuantity,
      qualityHoldQuantity: task.qualityHoldQuantity
    },
    relatedLots: [
      {
        lotKey: `${task.warehouseNo}|${task.itemNo}|${task.batchNo}`,
        warehouseNo: task.warehouseNo,
        itemNo: task.itemNo,
        itemName: task.itemName,
        batchNo: task.batchNo,
        currentQuantity: task.availableQuantity + task.reservedQuantity + task.qualityHoldQuantity,
        availableQuantity: task.availableQuantity,
        qualityHoldQuantity: task.qualityHoldQuantity,
        validDate: "",
        riskTypes: task.riskTypes
      }
    ],
    sourceRefs: [
      {
        refCategory: task.refCategory,
        refNo: task.refNo,
        refSubNo: task.refSubNo,
        descriptionCode: "warehouse.source.primary"
      }
    ],
    timeline: [
      {
        id: `${task.taskId}-created`,
        eventCode: "workflow.task.created",
        eventDate: task.dueDate,
        department: task.ownerDepartment,
        status: 1,
        comment: ""
      },
      {
        id: `${task.taskId}-assigned`,
        eventCode: task.taskStatus === 4 ? "workflow.task.blocked" : "workflow.task.assigned",
        eventDate: task.dueDate,
        department: task.ownerDepartment,
        status: task.taskStatus,
        comment: task.blockReason
      }
    ]
  };
}

function normalizeAnalyticsPeriod(value?: string): WarehouseAnalyticsPeriod {
  if (value === "7d" || value === "90d") {
    return value;
  }
  return "30d";
}

function normalizeAnalyticsBucket(value?: string): WarehouseAnalyticsBucket {
  if (value === "week" || value === "month") {
    return value;
  }
  return "day";
}

function mapAnalyticsRange(range?: ApiWarehouseAnalyticsRange): WarehouseAnalyticsRange {
  return {
    period: normalizeAnalyticsPeriod(range?.period),
    bucket: normalizeAnalyticsBucket(range?.bucket),
    startDate: timestampToDate(range?.startTimestamp),
    endDate: timestampToDate(range?.endTimestamp)
  };
}

function mapAnalyticsValueTrendPoint(
  item: ApiWarehouseAnalyticsValueTrendPoint
): WarehouseAnalyticsValueTrendPoint {
  return {
    bucketStart: timestampToDate(item.bucketStart),
    bucketLabel: item.bucketLabel ?? timestampToDate(item.bucketStart),
    itemCategory: item.itemCategory,
    inventoryValue: item.inventoryValue ?? 0,
    availableValue: item.availableValue ?? 0,
    reservedValue: item.reservedValue ?? 0,
    qualityHoldValue: item.qualityHoldValue ?? 0
  };
}

function mapAnalyticsSpaceTrendPoint(
  item: ApiWarehouseAnalyticsSpaceTrendPoint
): WarehouseAnalyticsSpaceTrendPoint {
  return {
    bucketStart: timestampToDate(item.bucketStart),
    warehouseNo: item.warehouseNo ?? "",
    warehouseName: item.warehouseName ?? "",
    usedPallets: item.usedPallets ?? 0,
    reservedPallets: item.reservedPallets ?? 0,
    availablePallets: item.availablePallets ?? 0,
    utilizationRate: item.utilizationRate ?? 0
  };
}

function mapAnalyticsRiskBreakdownItem(
  item: ApiWarehouseAnalyticsRiskBreakdownItem
): WarehouseAnalyticsRiskBreakdownItem {
  return {
    riskType: item.riskType ?? "UNKNOWN",
    riskLevel: item.riskLevel,
    lotCount: item.lotCount ?? 0,
    inventoryValue: item.inventoryValue ?? 0,
    quantity: item.quantity ?? 0
  };
}

function mapAnalyticsTaskSlaItem(item: ApiWarehouseAnalyticsTaskSlaItem): WarehouseAnalyticsTaskSlaItem {
  return {
    taskType: item.taskType,
    openTaskCount: item.openTaskCount ?? 0,
    completedTaskCount: item.completedTaskCount ?? 0,
    overdueTaskCount: item.overdueTaskCount ?? 0,
    blockedTaskCount: item.blockedTaskCount ?? 0,
    onTimeRate: item.onTimeRate ?? 0,
    averageLeadTimeHours: item.averageLeadTimeHours ?? 0
  };
}

function mapAnalyticsOverviewPayload(payload: ApiWarehouseAnalyticsOverviewPayload): WarehouseAnalyticsOverviewData {
  return {
    serverDate: timestampToDateTime(payload.serverTimestamp),
    timezone: payload.timezone ?? "Asia/Taipei",
    range: mapAnalyticsRange(payload.range),
    kpi: {
      totalInventoryValue: payload.kpi?.totalInventoryValue ?? 0,
      valueChangeRate: payload.kpi?.valueChangeRate ?? 0,
      usedPallets: payload.kpi?.usedPallets ?? 0,
      spaceUtilizationRate: payload.kpi?.spaceUtilizationRate ?? 0,
      riskLotCount: payload.kpi?.riskLotCount ?? 0,
      openTaskCount: payload.kpi?.openTaskCount ?? 0,
      overdueTaskRate: payload.kpi?.overdueTaskRate ?? 0
    },
    valueTrend: withFallbackArray<ApiWarehouseAnalyticsValueTrendPoint>(payload.valueTrend, []).map(
      mapAnalyticsValueTrendPoint
    ),
    spaceTrend: withFallbackArray<ApiWarehouseAnalyticsSpaceTrendPoint>(payload.spaceTrend, []).map(
      mapAnalyticsSpaceTrendPoint
    ),
    riskBreakdown: withFallbackArray<ApiWarehouseAnalyticsRiskBreakdownItem>(payload.riskBreakdown, []).map(
      mapAnalyticsRiskBreakdownItem
    ),
    taskSla: withFallbackArray<ApiWarehouseAnalyticsTaskSlaItem>(payload.taskSla, []).map(mapAnalyticsTaskSlaItem)
  };
}

function mapAnalyticsCategorySummary(
  item: ApiWarehouseAnalyticsCategorySummary
): WarehouseAnalyticsCategorySummary {
  return {
    itemCategory: item.itemCategory,
    inventoryValue: item.inventoryValue ?? 0,
    availableValue: item.availableValue ?? 0,
    reservedValue: item.reservedValue ?? 0,
    qualityHoldValue: item.qualityHoldValue ?? 0
  };
}

function mapAnalyticsWarehouseSummary(
  item: ApiWarehouseAnalyticsWarehouseSummary
): WarehouseAnalyticsWarehouseSummary {
  return {
    warehouseNo: item.warehouseNo ?? "",
    warehouseName: item.warehouseName ?? "",
    usedPallets: item.usedPallets ?? 0,
    reservedPallets: item.reservedPallets ?? 0,
    availablePallets: item.availablePallets ?? 0,
    utilizationRate: item.utilizationRate ?? 0
  };
}

function mapAnalyticsRiskSummary(summary?: ApiWarehouseAnalyticsRiskSummary): WarehouseAnalyticsRiskSummary {
  return {
    riskLotCount: summary?.riskLotCount ?? 0,
    highRiskLotCount: summary?.highRiskLotCount ?? 0,
    inventoryValue: summary?.inventoryValue ?? 0,
    quantity: summary?.quantity ?? 0
  };
}

function mapAnalyticsTopRiskLot(item: ApiWarehouseAnalyticsTopRiskLot, index: number): WarehouseAnalyticsTopRiskLot {
  return {
    lotKey: item.lotKey ?? `${item.warehouseNo ?? ""}|${item.itemNo ?? ""}|${item.batchNo ?? index}`,
    warehouseNo: item.warehouseNo ?? "",
    warehouseName: item.warehouseName ?? "",
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    batchNo: item.batchNo ?? "",
    riskType: item.riskType ?? "UNKNOWN",
    riskLevel: item.riskLevel,
    inventoryValue: item.inventoryValue ?? 0,
    quantity: item.quantity ?? 0
  };
}

function mapAnalyticsDepartmentSummary(
  item: ApiWarehouseAnalyticsTaskDepartmentSummary
): WarehouseAnalyticsTaskDepartmentSummary {
  return {
    ownerDepartment: item.ownerDepartment,
    openTaskCount: item.openTaskCount ?? 0,
    overdueTaskCount: item.overdueTaskCount ?? 0,
    blockedTaskCount: item.blockedTaskCount ?? 0
  };
}

function mapAnalyticsOverdueTrendPoint(
  item: ApiWarehouseAnalyticsOverdueTrendPoint
): WarehouseAnalyticsOverdueTrendPoint {
  return {
    bucketStart: timestampToDate(item.bucketStart),
    bucketLabel: item.bucketLabel ?? timestampToDate(item.bucketStart),
    overdueTaskCount: item.overdueTaskCount ?? 0,
    blockedTaskCount: item.blockedTaskCount ?? 0
  };
}

function mapAnalyticsValueTrendPayload(
  payload: ApiWarehouseAnalyticsValueTrendPayload
): WarehouseAnalyticsValueTrendData {
  return {
    range: mapAnalyticsRange(payload.range),
    summaryByCategory: withFallbackArray<ApiWarehouseAnalyticsCategorySummary>(
      payload.summaryByCategory,
      []
    ).map(mapAnalyticsCategorySummary),
    valueTrend: withFallbackArray<ApiWarehouseAnalyticsValueTrendPoint>(payload.valueTrend, []).map(
      mapAnalyticsValueTrendPoint
    )
  };
}

function mapAnalyticsSpaceUtilizationPayload(
  payload: ApiWarehouseAnalyticsSpaceUtilizationPayload
): WarehouseAnalyticsSpaceUtilizationData {
  return {
    range: mapAnalyticsRange(payload.range),
    summaryByWarehouse: withFallbackArray<ApiWarehouseAnalyticsWarehouseSummary>(
      payload.summaryByWarehouse,
      []
    ).map(mapAnalyticsWarehouseSummary),
    spaceTrend: withFallbackArray<ApiWarehouseAnalyticsSpaceTrendPoint>(payload.spaceTrend, []).map(
      mapAnalyticsSpaceTrendPoint
    )
  };
}

function mapAnalyticsRiskBreakdownPayload(
  payload: ApiWarehouseAnalyticsRiskBreakdownPayload
): WarehouseAnalyticsRiskBreakdownData {
  return {
    range: mapAnalyticsRange(payload.range),
    riskSummary: mapAnalyticsRiskSummary(payload.riskSummary),
    riskBreakdown: withFallbackArray<ApiWarehouseAnalyticsRiskBreakdownItem>(payload.riskBreakdown, []).map(
      mapAnalyticsRiskBreakdownItem
    ),
    topRiskLots: withFallbackArray<ApiWarehouseAnalyticsTopRiskLot>(payload.topRiskLots, []).map(
      mapAnalyticsTopRiskLot
    )
  };
}

function mapAnalyticsTaskSlaPayload(payload: ApiWarehouseAnalyticsTaskSlaPayload): WarehouseAnalyticsTaskSlaData {
  return {
    range: mapAnalyticsRange(payload.range),
    summaryByTaskType: withFallbackArray<ApiWarehouseAnalyticsTaskSlaItem>(payload.summaryByTaskType, []).map(
      mapAnalyticsTaskSlaItem
    ),
    summaryByDepartment: withFallbackArray<ApiWarehouseAnalyticsTaskDepartmentSummary>(
      payload.summaryByDepartment,
      []
    ).map(mapAnalyticsDepartmentSummary),
    overdueTrend: withFallbackArray<ApiWarehouseAnalyticsOverdueTrendPoint>(payload.overdueTrend, []).map(
      mapAnalyticsOverdueTrendPoint
    )
  };
}

function periodDays(period: WarehouseAnalyticsPeriod) {
  if (period === "7d") {
    return 7;
  }
  if (period === "90d") {
    return 90;
  }
  return 30;
}

function buildMockAnalyticsPayload(query: WarehouseAnalyticsQuery = {}): ApiWarehouseAnalyticsOverviewPayload {
  const period = query.period ?? "30d";
  const bucket = query.bucket ?? "day";
  const now = Math.floor(Date.now() / 1000);
  const start = now - periodDays(period) * 86400;
  const records = warehouseDashboardMock.records;
  const capacities = warehouseDashboardMock.capacities;
  const risks = warehouseDashboardMock.risks;
  const tasks = warehouseDashboardMock.tasks;
  const totalInventoryValue = records.reduce((sum, item) => sum + item.amount, 0);
  const usedPallets = capacities.reduce((sum, item) => sum + item.usedPallets, 0);
  const totalPallets = capacities.reduce((sum, item) => sum + item.totalPallets, 0);

  const valueTrend: ApiWarehouseAnalyticsValueTrendPoint[] = warehouseDashboardMock.categorySummaries.map(
    (item, index) => ({
      bucketStart: start + index * Math.max(Math.floor((now - start) / 5), 86400),
      bucketLabel: item.category,
      itemCategory: index + 1,
      inventoryValue: item.amount,
      availableValue: item.availableAmount,
      reservedValue: item.reservedAmount,
      qualityHoldValue: Math.round(item.amount * 0.03)
    })
  );

  return {
    serverTimestamp: now,
    timezone: "Asia/Taipei",
    range: {
      period,
      bucket,
      startTimestamp: start,
      endTimestamp: now
    },
    kpi: {
      totalInventoryValue,
      valueChangeRate: 4.8,
      usedPallets,
      spaceUtilizationRate: totalPallets ? (usedPallets / totalPallets) * 100 : 0,
      riskLotCount: risks.length,
      openTaskCount: tasks.length,
      overdueTaskRate: tasks.length ? (tasks.filter((task) => task.tone === "danger").length / tasks.length) * 100 : 0
    },
    valueTrend,
    spaceTrend: capacities.map((item, index) => ({
      bucketStart: start + index * 86400,
      bucketLabel: item.warehouseName,
      warehouseNo: item.id,
      warehouseName: item.warehouseName,
      usedPallets: item.usedPallets,
      reservedPallets: item.reservedPallets,
      availablePallets: item.availablePallets,
      utilizationRate: item.totalPallets ? ((item.usedPallets + item.reservedPallets) / item.totalPallets) * 100 : 0
    })),
    riskBreakdown: [
      {
        riskType: "TURNOVER_OVER_30_DAYS",
        riskLevel: 2,
        lotCount: risks.filter((risk) => risk.type === "迴轉超過一個月").length || 1,
        inventoryValue: Math.round(totalInventoryValue * 0.18),
        quantity: 620
      },
      {
        riskType: "SHELF_LIFE_LT_ONE_THIRD",
        riskLevel: 3,
        lotCount: risks.filter((risk) => risk.type === "少於 1/3 效期").length || 1,
        inventoryValue: Math.round(totalInventoryValue * 0.12),
        quantity: 310
      },
      {
        riskType: "BELOW_SAFETY_STOCK",
        riskLevel: 3,
        lotCount: risks.filter((risk) => risk.type === "低於安全水位").length || 1,
        inventoryValue: Math.round(totalInventoryValue * 0.08),
        quantity: 140
      }
    ],
    taskSla: [
      {
        taskType: 4,
        openTaskCount: tasks.filter((task) => task.type === "入庫").length || 2,
        completedTaskCount: 9,
        overdueTaskCount: 1,
        blockedTaskCount: 0,
        onTimeRate: 91.4,
        averageLeadTimeHours: 5.2
      },
      {
        taskType: 5,
        openTaskCount: tasks.filter((task) => task.type === "出庫").length || 3,
        completedTaskCount: 12,
        overdueTaskCount: 2,
        blockedTaskCount: 1,
        onTimeRate: 86.7,
        averageLeadTimeHours: 4.6
      },
      {
        taskType: 6,
        openTaskCount: tasks.filter((task) => task.type === "移倉").length || 1,
        completedTaskCount: 6,
        overdueTaskCount: 0,
        blockedTaskCount: 0,
        onTimeRate: 96.2,
        averageLeadTimeHours: 3.1
      }
    ]
  };
}

function mockAnalyticsOverview(query: WarehouseAnalyticsQuery = {}): WarehouseAnalyticsOverviewData {
  return mapAnalyticsOverviewPayload(buildMockAnalyticsPayload(query));
}

function mockAnalyticsValueTrend(query: WarehouseAnalyticsQuery = {}): WarehouseAnalyticsValueTrendData {
  const payload = buildMockAnalyticsPayload(query);
  return {
    range: mapAnalyticsRange(payload.range),
    summaryByCategory: payload.valueTrend?.map((item) => mapAnalyticsCategorySummary(item)) ?? [],
    valueTrend: payload.valueTrend?.map(mapAnalyticsValueTrendPoint) ?? []
  };
}

function mockAnalyticsSpaceUtilization(query: WarehouseAnalyticsQuery = {}): WarehouseAnalyticsSpaceUtilizationData {
  const payload = buildMockAnalyticsPayload(query);
  return {
    range: mapAnalyticsRange(payload.range),
    summaryByWarehouse: payload.spaceTrend?.map((item) => mapAnalyticsWarehouseSummary(item)) ?? [],
    spaceTrend: payload.spaceTrend?.map(mapAnalyticsSpaceTrendPoint) ?? []
  };
}

function mockAnalyticsRiskBreakdown(query: WarehouseAnalyticsQuery = {}): WarehouseAnalyticsRiskBreakdownData {
  const payload = buildMockAnalyticsPayload(query);
  const riskBreakdown = payload.riskBreakdown?.map(mapAnalyticsRiskBreakdownItem) ?? [];
  return {
    range: mapAnalyticsRange(payload.range),
    riskSummary: {
      riskLotCount: riskBreakdown.reduce((sum, item) => sum + item.lotCount, 0),
      highRiskLotCount: riskBreakdown.filter((item) => (item.riskLevel ?? 0) >= 3).length,
      inventoryValue: riskBreakdown.reduce((sum, item) => sum + item.inventoryValue, 0),
      quantity: riskBreakdown.reduce((sum, item) => sum + item.quantity, 0)
    },
    riskBreakdown,
    topRiskLots: warehouseDashboardMock.records.slice(0, 5).map((record, index) => ({
      lotKey: record.id,
      warehouseNo: record.warehouseNo,
      warehouseName: record.warehouseName,
      itemNo: record.itemNo,
      itemName: record.itemName,
      batchNo: record.batchNo,
      riskType: index % 2 === 0 ? "SHELF_LIFE_LT_ONE_THIRD" : "TURNOVER_OVER_30_DAYS",
      riskLevel: record.tone === "danger" ? 3 : 2,
      inventoryValue: record.amount,
      quantity: record.quantity
    }))
  };
}

function mockAnalyticsTaskSla(query: WarehouseAnalyticsQuery = {}): WarehouseAnalyticsTaskSlaData {
  const payload = buildMockAnalyticsPayload(query);
  return {
    range: mapAnalyticsRange(payload.range),
    summaryByTaskType: payload.taskSla?.map(mapAnalyticsTaskSlaItem) ?? [],
    summaryByDepartment: [
      {
        ownerDepartment: 7,
        openTaskCount: payload.kpi?.openTaskCount ?? 0,
        overdueTaskCount: 2,
        blockedTaskCount: 1
      }
    ],
    overdueTrend: [
      {
        bucketStart: payload.range?.startTimestamp,
        bucketLabel: "Start",
        overdueTaskCount: 1,
        blockedTaskCount: 0
      },
      {
        bucketStart: payload.range?.endTimestamp,
        bucketLabel: "Now",
        overdueTaskCount: 2,
        blockedTaskCount: 1
      }
    ].map(mapAnalyticsOverdueTrendPoint)
  };
}

function calculateDaysLeft(validDate?: number) {
  if (!validDate) {
    return 0;
  }
  return Math.max(Math.ceil((validDate * 1000 - Date.now()) / 86400000), 0);
}

function buildWorkflow(item: ApiWarehouseInventory, task?: WarehouseTask): WarehouseWorkflowStep[] {
  return [
    { label: "來源", ref: (item as { sourceNo?: string }).sourceNo ?? "", status: "完成", tone: "success" },
    { label: "批號", ref: item.batchNo ?? "", status: "完成", tone: "success" },
    {
      label: "庫存",
      ref: `${formatNumber(item.currentQuantity ?? 0)} ${unitLabel(item.unit)}`,
      status: "進行中",
      tone: "warning"
    },
    {
      label: "後續任務",
      ref: task?.id ?? "無待處理任務",
      status: task ? "待處理" : "完成",
      tone: task ? task.tone : "success"
    }
  ];
}

function buildRelatedDocuments(
  item: ApiWarehouseInventory,
  risk?: WarehouseRisk,
  task?: WarehouseTask
): WarehouseRelatedDocument[] {
  const docs: WarehouseRelatedDocument[] = [
    {
      type: "來源單據",
      no: (item as { sourceNo?: string }).sourceNo ?? "",
      status: "已關聯",
      tone: "success"
    }
  ];
  if (risk) {
    docs.push({ type: "庫存警示", no: risk.id, status: "需處理", tone: risk.tone });
  }
  if (task) {
    docs.push({ type: "待處理任務", no: task.id, status: task.status, tone: task.tone });
  }
  return docs;
}

function normalizeWarehouseDashboard(payload: ApiWarehousePayload): WarehouseDashboardData {
  const risks = mapRisks(payload);
  return {
    kpis: buildKpis(payload),
    categorySummaries: mapCategorySummaries(payload),
    capacities: mapCapacities(payload),
    records: [],
    risks,
    tasks: []
  };
}

export async function getWarehouseDashboard(): Promise<WarehouseDashboardResult> {
  try {
    const payload = await apiGet<ApiWarehousePayload>(
      "/api/v2/warehouse/dashboard?trendDays=7"
    );
    const data = normalizeWarehouseDashboard(payload);
    return {
      data: {
        kpis: data.kpis.length ? data.kpis : warehouseDashboardMock.kpis,
        categorySummaries: data.categorySummaries.length
          ? data.categorySummaries
          : warehouseDashboardMock.categorySummaries,
        capacities: data.capacities.length ? data.capacities : warehouseDashboardMock.capacities,
        records: data.records,
        risks: data.risks,
        tasks: data.tasks
      },
      source: "api"
    };
  } catch (error) {
    return {
      data: warehouseDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Warehouse API unavailable"
    };
  }
}

export async function getWarehouseInventory(): Promise<WarehouseInventoryResult> {
  try {
    const payload = await apiGet<ApiWarehousePayload & { results?: ApiWarehouseInventory[] }>(
      "/api/v2/warehouse/inventory?count=100"
    );
    const inventoryPayload: ApiWarehousePayload = {
      ...payload,
      inventory: payload.results ?? payload.inventory ?? []
    };
    return {
      records: mapRecords(inventoryPayload, [], []),
      source: "api"
    };
  } catch (error) {
    return {
      records: warehouseDashboardMock.records,
      source: "mock",
      error: error instanceof Error ? error.message : "Warehouse inventory API unavailable"
    };
  }
}

export async function getWarehouseTasks(): Promise<WarehouseTasksResult> {
  try {
    const payload = await apiGet<ApiWarehousePayload & { results?: ApiWarehouseTask[] }>(
      "/api/v2/warehouse/tasks?count=100"
    );
    return {
      tasks: mapTasks({
        pendingTasks: payload.results ?? payload.pendingTasks ?? []
      }),
      source: "api"
    };
  } catch (error) {
    return {
      tasks: warehouseDashboardMock.tasks,
      source: "mock",
      error: error instanceof Error ? error.message : "Warehouse tasks API unavailable"
    };
  }
}

function buildTaskWorkbenchPath(query: WarehouseTaskWorkbenchQuery = {}) {
  const params = new URLSearchParams();
  if (query.dateRange) {
    params.set("dateRange", query.dateRange);
  }
  if (query.warehouseNo) {
    params.set("warehouse_no", query.warehouseNo);
  }
  if (query.taskType !== undefined) {
    params.set("taskType", String(query.taskType));
  }
  if (query.status !== undefined) {
    params.set("status", String(query.status));
  }
  if (query.ownerDepartment !== undefined) {
    params.set("ownerDepartment", String(query.ownerDepartment));
  }
  if (query.riskOnly !== undefined) {
    params.set("riskOnly", String(query.riskOnly));
  }
  if (query.keyword) {
    params.set("keyword", query.keyword);
  }
  if (query.sort) {
    params.set("sort", query.sort);
  }
  if (query.order) {
    params.set("order", query.order);
  }
  params.set("start", String(query.start ?? 0));
  params.set("count", String(query.count ?? 50));

  return `/api/v2/warehouse/task-workbench?${params.toString()}`;
}

export async function getWarehouseTaskWorkbench(
  query: WarehouseTaskWorkbenchQuery = {}
): Promise<WarehouseTaskWorkbenchResult> {
  try {
    const payload = await apiGet<ApiWarehouseTaskWorkbenchPayload>(buildTaskWorkbenchPath(query));
    return {
      data: mapTaskWorkbenchPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: mockTaskWorkbench(),
      source: "mock",
      error: error instanceof Error ? error.message : "Warehouse task workbench API unavailable"
    };
  }
}

export async function getWarehouseTaskDetail(taskId: string): Promise<WarehouseTaskDetailResult> {
  try {
    const payload = await apiGet<ApiWarehouseTaskDetailPayload>(
      `/api/v2/warehouse/task-workbench/tasks/${encodeURIComponent(taskId)}`
    );
    return {
      detail: mapTaskDetailPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      detail: mockTaskDetail(taskId),
      source: "mock",
      error: error instanceof Error ? error.message : "Warehouse task detail API unavailable"
    };
  }
}

function buildWarehouseAnalyticsPath(endpoint: string, query: WarehouseAnalyticsQuery = {}) {
  const params = new URLSearchParams();
  if (query.date !== undefined) {
    params.set("date", String(query.date));
  }
  if (query.period) {
    params.set("period", query.period);
  }
  if (query.bucket) {
    params.set("bucket", query.bucket);
  }
  if (query.warehouseNo) {
    params.set("warehouse_no", query.warehouseNo);
  }
  if (query.itemCategory !== undefined) {
    params.set("itemCategory", String(query.itemCategory));
  }
  if (query.taskType !== undefined) {
    params.set("taskType", String(query.taskType));
  }

  const queryString = params.toString();
  return `/api/v2/warehouse/analytics/${endpoint}${queryString ? `?${queryString}` : ""}`;
}

export async function getWarehouseAnalyticsOverview(
  query: WarehouseAnalyticsQuery = {}
): Promise<WarehouseAnalyticsOverviewResult> {
  try {
    const payload = await apiGet<ApiWarehouseAnalyticsOverviewPayload>(
      buildWarehouseAnalyticsPath("overview", query)
    );
    return {
      data: mapAnalyticsOverviewPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: mockAnalyticsOverview(query),
      source: "mock",
      error: error instanceof Error ? error.message : "Warehouse analytics overview API unavailable"
    };
  }
}

export async function getWarehouseAnalyticsValueTrend(
  query: WarehouseAnalyticsQuery = {}
): Promise<WarehouseAnalyticsValueTrendResult> {
  try {
    const payload = await apiGet<ApiWarehouseAnalyticsValueTrendPayload>(
      buildWarehouseAnalyticsPath("value-trend", query)
    );
    return {
      data: mapAnalyticsValueTrendPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: mockAnalyticsValueTrend(query),
      source: "mock",
      error: error instanceof Error ? error.message : "Warehouse analytics value trend API unavailable"
    };
  }
}

export async function getWarehouseAnalyticsSpaceUtilization(
  query: WarehouseAnalyticsQuery = {}
): Promise<WarehouseAnalyticsSpaceUtilizationResult> {
  try {
    const payload = await apiGet<ApiWarehouseAnalyticsSpaceUtilizationPayload>(
      buildWarehouseAnalyticsPath("space-utilization", query)
    );
    return {
      data: mapAnalyticsSpaceUtilizationPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: mockAnalyticsSpaceUtilization(query),
      source: "mock",
      error: error instanceof Error ? error.message : "Warehouse analytics space utilization API unavailable"
    };
  }
}

export async function getWarehouseAnalyticsRiskBreakdown(
  query: WarehouseAnalyticsQuery = {}
): Promise<WarehouseAnalyticsRiskBreakdownResult> {
  try {
    const payload = await apiGet<ApiWarehouseAnalyticsRiskBreakdownPayload>(
      buildWarehouseAnalyticsPath("risk-breakdown", query)
    );
    return {
      data: mapAnalyticsRiskBreakdownPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: mockAnalyticsRiskBreakdown(query),
      source: "mock",
      error: error instanceof Error ? error.message : "Warehouse analytics risk breakdown API unavailable"
    };
  }
}

export async function getWarehouseAnalyticsTaskSla(
  query: WarehouseAnalyticsQuery = {}
): Promise<WarehouseAnalyticsTaskSlaResult> {
  try {
    const payload = await apiGet<ApiWarehouseAnalyticsTaskSlaPayload>(
      buildWarehouseAnalyticsPath("task-sla", query)
    );
    return {
      data: mapAnalyticsTaskSlaPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: mockAnalyticsTaskSla(query),
      source: "mock",
      error: error instanceof Error ? error.message : "Warehouse analytics task SLA API unavailable"
    };
  }
}

function buildLotListPath(query: WarehouseInventoryLotsQuery = {}) {
  const params = new URLSearchParams();
  if (query.warehouseNo) {
    params.set("warehouse_no", query.warehouseNo);
  }
  if (query.itemCategory !== undefined) {
    params.set("itemCategory", String(query.itemCategory));
  }
  if (query.itemNo) {
    params.set("item_no", query.itemNo);
  }
  if (query.batchNo) {
    params.set("batchNo", query.batchNo);
  }
  if (query.riskType) {
    params.set("riskType", query.riskType);
  }
  if (query.taskType !== undefined) {
    params.set("taskType", String(query.taskType));
  }
  if (query.availability) {
    params.set("availability", query.availability);
  }
  if (query.keyword) {
    params.set("keyword", query.keyword);
  }
  if (query.sort) {
    params.set("sort", query.sort);
  }
  if (query.order) {
    params.set("order", query.order);
  }
  params.set("start", String(query.start ?? 0));
  params.set("count", String(query.count ?? 50));

  return `/api/v2/warehouse/inventory/lots?${params.toString()}`;
}

export async function getWarehouseInventoryLots(
  query: WarehouseInventoryLotsQuery = {}
): Promise<WarehouseInventoryLotsResult> {
  try {
    const payload = await apiGet<ApiWarehouseInventoryLotListPayload>(buildLotListPath(query));
    return {
      data: mapLotListPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: mockLotList(),
      source: "mock",
      error: error instanceof Error ? error.message : "Warehouse inventory lots API unavailable"
    };
  }
}

export async function getWarehouseInventoryLotDetail(
  lot: Pick<WarehouseInventoryLot, "warehouseNo" | "itemNo" | "batchNo">
): Promise<WarehouseInventoryLotDetailResult> {
  const path = `/api/v2/warehouse/inventory/lots/wh/${encodeURIComponent(lot.warehouseNo)}/item/${encodeURIComponent(
    lot.itemNo
  )}/batch/${encodeURIComponent(lot.batchNo)}`;

  try {
    const payload = await apiGet<ApiWarehouseInventoryLotDetailPayload>(path);
    return {
      detail: mapLotDetailPayload(payload),
      source: "api"
    };
  } catch (error) {
    const fallbackLot = mockLotList().lots.find(
      (item) => item.warehouseNo === lot.warehouseNo && item.itemNo === lot.itemNo && item.batchNo === lot.batchNo
    );
    return {
      detail: mockLotDetail(fallbackLot),
      source: "mock",
      error: error instanceof Error ? error.message : "Warehouse inventory lot detail API unavailable"
    };
  }
}
