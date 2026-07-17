import { productionDashboardMock } from "@/mock/production";
import { productionEnumLabel, productionRiskTone, productionStatusTone } from "@/i18n/production-enums";
import { defaultLanguage } from "@/i18n/dictionary";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type {
  ProductionAlert,
  ProductionDashboardData,
  ProductionDataSource,
  ProductionDaySchedule,
  ProductionLineSchedule,
  ProductionMaterial,
  ProductionRelatedDocument,
  ProductionSummaryItem,
  ProductionWorkflowStep,
  WorkOrder
} from "@/types/production";

type ApiProductionRange = {
  period?: string;
  startTimestamp?: number;
  endTimestamp?: number;
};

type ApiProductionSummary = {
  scheduledWorkOrderCount?: number;
  todayRunningWorkOrderCount?: number;
  readinessRiskCount?: number;
  averageEfficiencyRate?: number;
  averageMaterialLossRate?: number;
  averageUnitLaborCost?: number;
};

type ApiProductionSlot = {
  workOrderNo?: string;
  productOrderNo?: string;
  productNo?: string;
  productName?: string;
  batchNumber?: string;
  plannedStartTimestamp?: number;
  plannedEndTimestamp?: number;
  plannedQuantity?: number;
  completedQuantity?: number;
  unit?: number;
  status?: string;
  materialStatus?: string;
  staffStatus?: string;
  deliveryRisk?: string;
};

type ApiProductionScheduleLine = {
  date?: number;
  productionLineNo?: string;
  productionLineName?: string;
  oneProcess?: number;
  secProcess?: number;
  baseCapacityMinutes?: number;
  downtimeMinutes?: number;
  dailyCapacityMinutes?: number;
  scheduledMinutes?: number;
  availableMinutes?: number;
  capacityStatus?: string;
  changeoverMinutes?: number;
  changeoverStatus?: string;
  utilizationRate?: number;
  bottleneckRank?: number;
  riskLevel?: number;
  slots?: ApiProductionSlot[];
};

type ApiTodayWorkOrder = ApiProductionSlot & {
  productionLineNo?: string;
  productionLineName?: string;
  oneProcess?: number;
  secProcess?: number;
  actualStartTimestamp?: number;
  actualEndTimestamp?: number;
  progressRate?: number;
  machineStatus?: string;
  qualityStatus?: string;
  ownerEmployeeNo?: string;
  ownerEmployeeName?: string;
};

type ApiReadinessSignal = {
  workOrderNo?: string;
  signalType?: string;
  status?: string;
  riskLevel?: number;
  ownerDepartment?: number;
  requiredQuantity?: number;
  availableQuantity?: number;
  gapQuantity?: number;
  requiredStaffCount?: number;
  assignedStaffCount?: number;
  comment?: string;
};

type ApiProductionMetric = {
  workOrderNo?: string;
  standardMinutes?: number;
  actualMinutes?: number;
  efficiencyRate?: number;
  standardInputQuantity?: number;
  actualInputQuantity?: number;
  outputQuantity?: number;
  reuseQuantity?: number;
  wasteQuantity?: number;
  materialLossQuantity?: number;
  materialLossRate?: number;
  laborHours?: number;
  laborCost?: number;
  unitLaborCost?: number;
  riskLevel?: number;
};

type ApiProductionAlert = {
  alertType?: string;
  workOrderNo?: string;
  productionLineNo?: string;
  riskLevel?: number;
  ownerDepartment?: number;
  comment?: string;
};

type ApiProductionDashboardPayload = {
  serverTimestamp?: number;
  timezone?: string;
  range?: ApiProductionRange;
  summary?: ApiProductionSummary;
  total?: number;
  start?: number;
  count?: number;
  scheduleByLine?: ApiProductionScheduleLine[];
  todayWorkOrders?: ApiTodayWorkOrder[];
  readinessSignals?: ApiReadinessSignal[];
  productionMetrics?: ApiProductionMetric[];
  alerts?: ApiProductionAlert[];
};

type ApiWorkOrderDetail = {
  workOrder?: {
    workOrderNo?: string;
    productOrderNo?: string;
    apsNo?: string;
    productNo?: string;
    productName?: string;
    outputItemNo?: string;
    outputItemName?: string;
    productionLineNo?: string;
    productionLineName?: string;
    oneProcess?: number;
    secProcess?: number;
    plannedStartTimestamp?: number;
    plannedEndTimestamp?: number;
    plannedQuantity?: number;
    unit?: number;
    plannedMinutes?: number;
    requiredStaffCount?: number;
    assignedStaffCount?: number;
    status?: string;
    comment?: string;
  };
  materials?: {
    itemNo?: string;
    itemName?: string;
    batchNumber?: string;
    requiredQuantity?: number;
    issuedQuantity?: number;
    returnedQuantity?: number;
    availableQuantity?: number;
    unit?: number;
    status?: string;
  }[];
  mesEvents?: {
    eventType?: string;
    refNo?: string;
    timestamp?: number;
    itemNo?: string;
    itemName?: string;
    batchNumber?: string;
    quantity?: number;
    unit?: number;
    employeeNo?: string;
    employeeName?: string;
    equipmentNo?: string;
    equipmentName?: string;
    comment?: string;
  }[];
  outputs?: {
    itemNo?: string;
    itemName?: string;
    batchNumber?: string;
    serialNo?: string;
    validDateTimestamp?: number;
    quantity?: number;
    unit?: number;
  }[];
  reuseAndWaste?: {
    itemNo?: string;
    itemName?: string;
    category?: number;
    batchNumber?: string;
    quantity?: number;
    unit?: number;
    comment?: string;
  }[];
  labor?: {
    employeeNo?: string;
    employeeName?: string;
    action?: number;
    startTimestamp?: number;
    endTimestamp?: number;
    hours?: number;
  }[];
  machines?: {
    equipmentNo?: string;
    equipmentName?: string;
    timestamp?: number;
    action?: number;
  }[];
  relatedDocuments?: {
    documentType?: string;
    documentNo?: string;
    status?: string;
    timestamp?: number;
  }[];
};

export type ProductionDashboardQuery = {
  period?: "7d" | "14d";
  start?: number;
  count?: number;
  date?: number;
  productionLineNo?: string;
  workOrderNo?: string;
  keyword?: string;
};

export type ProductionDashboardResult = {
  data: ProductionDashboardData;
  source: ProductionDataSource;
  error?: string;
};

export type ProductionWorkOrderDetailResult = {
  order?: WorkOrder;
  source: ProductionDataSource;
  error?: string;
};

const locale = defaultLanguage;

function formatNumber(value: number, maximumFractionDigits = 1) {
  return new Intl.NumberFormat(locale, { maximumFractionDigits }).format(value);
}

function timestampToDate(value?: number) {
  if (!value) {
    return "";
  }
  return new Date(value * 1000).toLocaleDateString(locale, { timeZone: "Asia/Taipei" });
}

function timestampToTime(value?: number) {
  if (!value) {
    return "";
  }
  return new Date(value * 1000).toLocaleTimeString(locale, {
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "Asia/Taipei"
  });
}

function timestampToDateTime(value?: number) {
  if (!value) {
    return "";
  }
  return new Date(value * 1000).toLocaleString(locale, {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "Asia/Taipei"
  });
}

function unitLabel(unit?: number) {
  return unit === undefined || unit === null ? "" : productionEnumLabel("unit", unit, locale);
}

function processLabel(oneProcess?: number) {
  return productionEnumLabel("process", oneProcess, locale);
}

function progressRate(completed = 0, planned = 0, provided?: number) {
  if (provided !== undefined && Number.isFinite(provided)) {
    return Math.max(0, Math.min(100, Math.round(provided)));
  }
  if (!planned) {
    return 0;
  }
  return Math.max(0, Math.min(100, Math.round((completed / planned) * 100)));
}

function mapSummary(payload: ApiProductionDashboardPayload): ProductionSummaryItem[] {
  const summary = payload.summary ?? {};
  return [
    {
      label: "一週預排工單",
      value: formatNumber(summary.scheduledWorkOrderCount ?? 0, 0),
      hint: `${payload.range?.period ?? "7d"} 排程範圍`,
      tone: "info"
    },
    {
      label: "今日 MES 進行中",
      value: formatNumber(summary.todayRunningWorkOrderCount ?? 0, 0),
      hint: "生產中或已有 MES 生產資料",
      tone: (summary.todayRunningWorkOrderCount ?? 0) > 0 ? "success" : "info"
    },
    {
      label: "備料/人員風險",
      value: formatNumber(summary.readinessRiskCount ?? 0, 0),
      hint: "非 ready readiness 工單去重",
      tone: (summary.readinessRiskCount ?? 0) > 0 ? "warning" : "success"
    },
    {
      label: "效率 / 損耗 / 人工",
      value: `${formatNumber(summary.averageEfficiencyRate ?? 0)}%`,
      hint: `損耗 ${formatNumber(summary.averageMaterialLossRate ?? 0)}% · 單品人工 $${formatNumber(
        summary.averageUnitLaborCost ?? 0
      )}`,
      tone: (summary.averageEfficiencyRate ?? 0) >= 90 ? "success" : "warning"
    }
  ];
}

function mapMaterialStatus(status?: string) {
  return productionEnumLabel("materialStatus", status, locale);
}

function mapStaffStatus(status?: string) {
  return productionEnumLabel("staffStatus", status, locale);
}

function mapMachineStatus(status?: string) {
  return productionEnumLabel("machineStatus", status, locale);
}

function buildWorkflow(order: ApiTodayWorkOrder, metric?: ApiProductionMetric): ProductionWorkflowStep[] {
  const status = order.status ?? "unknown";
  return [
    {
      label: productionEnumLabel("workflowStep", "work_order", locale),
      ref: order.workOrderNo ?? "",
      status: "完成",
      tone: "success",
      stepCode: "work_order",
      statusCode: "completed"
    },
    {
      label: productionEnumLabel("workflowStep", "material", locale),
      ref: order.materialStatus ?? "",
      status: order.materialStatus === "ready" ? "完成" : "進行中",
      tone: productionStatusTone(order.materialStatus),
      stepCode: "material",
      statusCode: order.materialStatus
    },
    {
      label: productionEnumLabel("workflowStep", "production", locale),
      ref: `${formatNumber(metric?.outputQuantity ?? order.completedQuantity ?? 0)} ${unitLabel(order.unit)}`,
      status: status === "completed" || status === "pending_inventory" ? "完成" : status === "scheduled" ? "待處理" : "進行中",
      tone: productionStatusTone(status),
      stepCode: "production",
      statusCode: status
    },
    {
      label: productionEnumLabel("workflowStep", "quality", locale),
      ref: order.qualityStatus ?? "deferred",
      status: "待處理",
      tone: "info",
      stepCode: "quality",
      statusCode: order.qualityStatus ?? "deferred"
    },
    {
      label: productionEnumLabel("workflowStep", "inventory", locale),
      ref: status === "completed" ? "inventory confirmed" : "pending",
      status: status === "completed" ? "完成" : "待處理",
      tone: status === "completed" ? "success" : "warning",
      stepCode: "inventory",
      statusCode: status === "completed" ? "completed" : "pending_inventory"
    }
  ];
}

function mapMaterialsFromReadiness(signals: ApiReadinessSignal[], order: ApiTodayWorkOrder): ProductionMaterial[] {
  return signals
    .filter((signal) => signal.workOrderNo === order.workOrderNo && signal.signalType === "material")
    .map((signal, index) => ({
      itemNo: signal.signalType ?? `material-${index + 1}`,
      itemName: signal.comment ?? productionEnumLabel("readinessSignal", signal.signalType, locale),
      batchNo: "",
      requiredQty: signal.requiredQuantity ?? 0,
      issuedQty: signal.availableQuantity ?? 0,
      availableQty: signal.availableQuantity ?? 0,
      unit: "",
      status: mapMaterialStatus(signal.status),
      statusCode: signal.status,
      tone: productionStatusTone(signal.status, signal.riskLevel)
    }));
}

function mapOrder(
  item: ApiTodayWorkOrder,
  metrics: ApiProductionMetric[],
  readinessSignals: ApiReadinessSignal[]
): WorkOrder {
  const metric = metrics.find((candidate) => candidate.workOrderNo === item.workOrderNo);
  const status = item.status ?? "unknown";
  const materialStatus = item.materialStatus ?? "unknown";
  const staffStatus = item.staffStatus ?? "unknown";
  const qualityStatus = item.qualityStatus ?? "deferred";
  const deliveryRisk = item.deliveryRisk ?? "unknown";
  const plannedQty = item.plannedQuantity ?? 0;
  const completedQty = item.completedQuantity ?? metric?.outputQuantity ?? 0;
  const standardHours = (metric?.standardMinutes ?? 0) / 60;
  const actualHours = (metric?.actualMinutes ?? 0) / 60;
  const readiness = readinessSignals.filter((signal) => signal.workOrderNo === item.workOrderNo);
  const staffSignal = readiness.find((signal) => signal.signalType === "staff");
  const materials = mapMaterialsFromReadiness(readiness, item);

  return {
    id: item.workOrderNo ?? "",
    product: item.productName ?? "",
    batchNo: item.batchNumber ?? "",
    processType: processLabel(item.oneProcess),
    line: item.productionLineName || item.productionLineNo || "",
    stage: productionEnumLabel("status", status, locale),
    tone: productionStatusTone(status),
    progress: progressRate(completedQty, plannedQty, item.progressRate),
    plannedQty,
    completedQty,
    unit: unitLabel(item.unit),
    owner: item.ownerEmployeeName || item.ownerEmployeeNo || productionEnumLabel("department", staffSignal?.ownerDepartment, locale),
    eta: timestampToTime(item.plannedEndTimestamp),
    priority: deliveryRisk === "high_risk" ? "高" : "中",
    sourceOrder: item.productOrderNo ?? "",
    bomNo: "",
    customerDueDate: "",
    deliveryRisk: productionEnumLabel("deliveryRisk", deliveryRisk, locale),
    scheduleDate: timestampToDate(item.plannedStartTimestamp),
    startTime: timestampToTime(item.plannedStartTimestamp),
    endTime: timestampToTime(item.plannedEndTimestamp),
    changeoverMinutes: 0,
    materialStatus: mapMaterialStatus(materialStatus),
    staffStatus: mapStaffStatus(staffStatus),
    requiredStaff: staffSignal?.requiredStaffCount ?? 0,
    assignedStaff: staffSignal?.assignedStaffCount ?? 0,
    machineStatus: mapMachineStatus(item.machineStatus),
    standardHours,
    actualHours,
    efficiencyRate: metric?.efficiencyRate ?? 0,
    standardMaterialQty: metric?.standardInputQuantity ?? 0,
    actualMaterialQty: metric?.actualInputQuantity ?? 0,
    materialLossRate: metric?.materialLossRate ?? 0,
    laborHours: metric?.laborHours ?? 0,
    laborCost: metric?.laborCost ?? 0,
    unitLaborCost: metric?.unitLaborCost ?? 0,
    quality: {
      status: productionEnumLabel("qualityStatus", qualityStatus, locale),
      sampleCount: 0,
      defectCount: 0,
      defectRate: 0,
      pendingCount: 0,
      result: qualityStatus === "deferred" ? "品檢功能待下一版實作" : "",
      tone: "info",
      statusCode: qualityStatus
    },
    qualityBlocksInventory: status === "pending_inventory",
    qualityBlocksShipment: deliveryRisk === "high_risk",
    statusCode: status,
    materialStatusCode: materialStatus,
    staffStatusCode: staffStatus,
    machineStatusCode: item.machineStatus,
    qualityStatusCode: qualityStatus,
    deliveryRiskCode: deliveryRisk,
    unitCode: item.unit,
    productionLineNo: item.productionLineNo,
    productNo: item.productNo,
    ownerEmployeeNo: item.ownerEmployeeNo,
    actualStartTime: timestampToTime(item.actualStartTimestamp),
    actualEndTime: timestampToTime(item.actualEndTimestamp),
    materials,
    workflow: buildWorkflow(item, metric),
    relatedDocuments: [
      {
        type: productionEnumLabel("workflowStep", "order", locale),
        no: item.productOrderNo ?? "",
        status: productionEnumLabel("deliveryRisk", deliveryRisk, locale),
        tone: productionRiskTone(deliveryRisk),
        statusCode: deliveryRisk
      }
    ].filter((document) => document.no)
  };
}

function mapScheduleSlot(item: ApiProductionSlot) {
  const status = item.status ?? "unknown";
  return {
    workOrderId: item.workOrderNo ?? "",
    product: item.productName ?? "",
    processType: processLabel(undefined),
    startTime: timestampToTime(item.plannedStartTimestamp),
    endTime: timestampToTime(item.plannedEndTimestamp),
    materialStatus: mapMaterialStatus(item.materialStatus ?? "unknown"),
    staffStatus: mapStaffStatus(item.staffStatus ?? "unknown"),
    stage: productionEnumLabel("status", status, locale),
    tone: productionStatusTone(status)
  };
}

function mapScheduleLine(item: ApiProductionScheduleLine): ProductionLineSchedule {
  const dailyCapacityHours = (item.dailyCapacityMinutes ?? 0) / 60;
  const usedHours = (item.scheduledMinutes ?? 0) / 60;
  return {
    line: item.productionLineName || item.productionLineNo || "",
    processType: processLabel(item.oneProcess),
    dailyCapacityHours,
    usedHours,
    availableHours: (item.availableMinutes ?? 0) / 60,
    changeoverHours: (item.changeoverMinutes ?? 0) / 60,
    bottleneckRank: item.bottleneckRank ?? 0,
    slots: withFallbackArray<ApiProductionSlot>(item.slots, []).map(mapScheduleSlot),
    tone: productionStatusTone(item.capacityStatus, item.riskLevel)
  };
}

function mapSchedule(payload: ApiProductionDashboardPayload): ProductionDaySchedule[] {
  const grouped = new Map<string, ProductionDaySchedule>();
  withFallbackArray<ApiProductionScheduleLine>(payload.scheduleByLine, []).forEach((line) => {
    const date = timestampToDate(line.date) || "未提供日期";
    const current = grouped.get(date) ?? {
      date,
      label: date,
      lines: []
    };
    current.lines.push(mapScheduleLine(line));
    grouped.set(date, current);
  });
  return Array.from(grouped.values());
}

function mapAlerts(payload: ApiProductionDashboardPayload): ProductionAlert[] {
  return withFallbackArray<ApiProductionAlert>(payload.alerts, []).map((alert, index) => ({
    id: `${alert.alertType ?? "production-alert"}-${alert.workOrderNo ?? alert.productionLineNo ?? index}`,
    title: productionEnumLabel("alertType", alert.alertType, locale),
    description:
      alert.comment ||
      `${alert.workOrderNo ?? alert.productionLineNo ?? ""} · ${productionEnumLabel("department", alert.ownerDepartment, locale)}`,
    tone: productionStatusTone(alert.alertType, alert.riskLevel)
  }));
}

function mapDashboardPayload(payload: ApiProductionDashboardPayload): ProductionDashboardData {
  const metrics = withFallbackArray<ApiProductionMetric>(payload.productionMetrics, []);
  const readinessSignals = withFallbackArray<ApiReadinessSignal>(payload.readinessSignals, []);
  const orders = withFallbackArray<ApiTodayWorkOrder>(payload.todayWorkOrders, []).map((order) =>
    mapOrder(order, metrics, readinessSignals)
  );

  return {
    summary: mapSummary(payload),
    orders,
    weekSchedule: mapSchedule(payload),
    alerts: mapAlerts(payload)
  };
}

function mapDetailMaterials(payload: ApiWorkOrderDetail): ProductionMaterial[] {
  return withFallbackArray<NonNullable<ApiWorkOrderDetail["materials"]>[number]>(payload.materials, []).map(
    (item, index) => ({
      itemNo: item.itemNo ?? `material-${index + 1}`,
      itemName: item.itemName ?? "",
      batchNo: item.batchNumber ?? "",
      requiredQty: item.requiredQuantity ?? 0,
      issuedQty: item.issuedQuantity ?? 0,
      returnedQty: item.returnedQuantity ?? 0,
      availableQty: item.availableQuantity ?? 0,
      unit: unitLabel(item.unit),
      unitCode: item.unit,
      status: mapMaterialStatus(item.status),
      statusCode: item.status,
      tone: productionStatusTone(item.status)
    })
  );
}

function mapDetailWorkflow(payload: ApiWorkOrderDetail): ProductionWorkflowStep[] {
  const events = withFallbackArray<NonNullable<ApiWorkOrderDetail["mesEvents"]>[number]>(payload.mesEvents, []).map(
    (event, index) => ({
      label: productionEnumLabel("workflowStep", event.eventType, locale),
      ref: event.refNo || event.comment || `event-${index + 1}`,
      status: "進行中" as const,
      tone: "info" as const,
      stepCode: event.eventType,
      statusCode: event.eventType
    })
  );
  return events.length ? events : [];
}

function mapDetailDocuments(payload: ApiWorkOrderDetail): ProductionRelatedDocument[] {
  return withFallbackArray<NonNullable<ApiWorkOrderDetail["relatedDocuments"]>[number]>(
    payload.relatedDocuments,
    []
  ).map((item, index) => ({
    type: item.documentType ?? productionEnumLabel("workflowStep", "document", locale),
    no: item.documentNo ?? `document-${index + 1}`,
    status: item.status ?? "",
    statusCode: item.status,
    timestamp: timestampToDateTime(item.timestamp),
    tone: productionStatusTone(item.status)
  }));
}

function mergeDetailPayload(payload: ApiWorkOrderDetail, fallback?: WorkOrder): WorkOrder | undefined {
  const workOrder = payload.workOrder;
  if (!workOrder && !fallback) {
    return undefined;
  }
  const status = workOrder?.status ?? fallback?.statusCode ?? "unknown";
  const plannedQty = workOrder?.plannedQuantity ?? fallback?.plannedQty ?? 0;
  const materials = mapDetailMaterials(payload);
  const workflow = mapDetailWorkflow(payload);
  const documents = mapDetailDocuments(payload);

  return {
    ...(fallback ?? productionDashboardMock.orders[0]),
    id: workOrder?.workOrderNo ?? fallback?.id ?? "",
    product: workOrder?.outputItemName || workOrder?.productName || fallback?.product || "",
    line: workOrder?.productionLineName || workOrder?.productionLineNo || fallback?.line || "",
    processType: processLabel(workOrder?.oneProcess) || fallback?.processType || "",
    stage: productionEnumLabel("status", status, locale),
    tone: productionStatusTone(status),
    plannedQty,
    unit: unitLabel(workOrder?.unit) || fallback?.unit || "",
    requiredStaff: workOrder?.requiredStaffCount ?? fallback?.requiredStaff ?? 0,
    assignedStaff: workOrder?.assignedStaffCount ?? fallback?.assignedStaff ?? 0,
    scheduleDate: timestampToDate(workOrder?.plannedStartTimestamp) || fallback?.scheduleDate || "",
    startTime: timestampToTime(workOrder?.plannedStartTimestamp) || fallback?.startTime || "",
    endTime: timestampToTime(workOrder?.plannedEndTimestamp) || fallback?.endTime || "",
    sourceOrder: workOrder?.productOrderNo ?? fallback?.sourceOrder ?? "",
    bomNo: workOrder?.apsNo ?? fallback?.bomNo ?? "",
    statusCode: status,
    unitCode: workOrder?.unit ?? fallback?.unitCode,
    productionLineNo: workOrder?.productionLineNo ?? fallback?.productionLineNo,
    productNo: workOrder?.productNo ?? fallback?.productNo,
    materials: materials.length ? materials : fallback?.materials ?? [],
    workflow: workflow.length ? workflow : fallback?.workflow ?? [],
    relatedDocuments: documents.length ? documents : fallback?.relatedDocuments ?? []
  };
}

function buildDashboardPath(query: ProductionDashboardQuery = {}) {
  const params = new URLSearchParams();
  params.set("period", query.period ?? "7d");
  params.set("start", String(query.start ?? 0));
  params.set("count", String(query.count ?? 50));
  if (query.date !== undefined) {
    params.set("date", String(query.date));
  }
  if (query.productionLineNo) {
    params.set("production_line_no", query.productionLineNo);
  }
  if (query.workOrderNo) {
    params.set("work_order_no", query.workOrderNo);
  }
  if (query.keyword) {
    params.set("keyword", query.keyword);
  }
  return `/api/v2/production/dashboard?${params.toString()}`;
}

export async function getProductionDashboard(
  query: ProductionDashboardQuery = {}
): Promise<ProductionDashboardResult> {
  try {
    const payload = await apiGet<ApiProductionDashboardPayload>(buildDashboardPath(query));
    const data = mapDashboardPayload(payload);
    return {
      data: {
        summary: data.summary.length ? data.summary : productionDashboardMock.summary,
        orders: data.orders.length ? data.orders : productionDashboardMock.orders,
        weekSchedule: data.weekSchedule.length ? data.weekSchedule : productionDashboardMock.weekSchedule,
        alerts: data.alerts.length ? data.alerts : productionDashboardMock.alerts
      },
      source: "api"
    };
  } catch (error) {
    return {
      data: productionDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Production API unavailable"
    };
  }
}

export async function getProductionWorkOrderDetail(
  workOrderNo: string,
  fallback?: WorkOrder
): Promise<ProductionWorkOrderDetailResult> {
  try {
    const payload = await apiGet<ApiWorkOrderDetail>(
      `/api/v2/production/work-orders/${encodeURIComponent(workOrderNo)}/detail`
    );
    return {
      order: mergeDetailPayload(payload, fallback),
      source: "api"
    };
  } catch (error) {
    return {
      order: fallback,
      source: "mock",
      error: error instanceof Error ? error.message : "Production work order detail API unavailable"
    };
  }
}
