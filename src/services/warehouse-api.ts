import { warehouseDashboardMock } from "@/mock/warehouse";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { StatusTone } from "@/types/dashboard";
import type {
  InventoryCategory,
  WarehouseCapacity,
  WarehouseCategorySummary,
  WarehouseDashboardData,
  WarehouseDataSource,
  WarehouseKpi,
  WarehouseRecord,
  WarehouseRelatedDocument,
  WarehouseRisk,
  WarehouseSourceType,
  WarehouseTask,
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

const CATEGORY_LABELS: Record<number, InventoryCategory> = {
  1: "原料" as InventoryCategory,
  2: "物料" as InventoryCategory,
  3: "膠捲" as InventoryCategory,
  4: "在製品" as InventoryCategory,
  5: "製成品" as InventoryCategory
};

const SOURCE_TYPE_LABELS: Record<string, WarehouseSourceType> = {
  PURCHASE: "採購" as WarehouseSourceType,
  WORK: "生產" as WarehouseSourceType,
  SALE: "出貨" as WarehouseSourceType,
  OTHER: "調整" as WarehouseSourceType
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
    const sourceType = SOURCE_TYPE_LABELS[(item as { sourceType?: string }).sourceType ?? ""] ?? ("調整" as WarehouseSourceType);
    const workflow = buildWorkflow(item, task);
    return {
      id: `${item.warehouseNo ?? ""}-${item.itemNo ?? ""}-${item.batchNo ?? ""}`,
      itemNo: item.itemNo ?? "",
      itemName: item.itemName ?? "",
      category: categoryLabel(item.itemCategory),
      warehouseNo: item.warehouseNo ?? "",
      warehouseName: item.warehouseName ?? "",
      batchNo: item.batchNo ?? "",
      sourceType,
      sourceNo: (item as { sourceNo?: string }).sourceNo ?? "",
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
