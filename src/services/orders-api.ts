import { ordersDashboardMock } from "@/mock/orders";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { StatusTone } from "@/types/dashboard";
import type {
  OrderDependency,
  OrderFulfillmentStep,
  OrderStatusSummary,
  OrderRiskLevel,
  OrdersDashboardData,
  OrdersDashboardPeriod,
  OrdersDashboardQuery,
  OrdersDataSource,
  OrdersFulfillmentData,
  SalesOrder
} from "@/types/orders";

type ApiOrdersRange = {
  period?: string;
  startTimestamp?: number;
  endTimestamp?: number;
};

type ApiOrdersSummary = {
  openOrderCount?: number;
  highRiskOrderCount?: number;
  commitmentRate?: number;
  estimatedMarginRiskCount?: number;
  paymentRiskCount?: number;
  totalOrderAmount?: number;
};

type ApiShipmentSummary = {
  shipmentCount?: number;
  shippedQuantity?: number;
  remainingQuantity?: number;
  firstShipTimestamp?: number;
  lastShipTimestamp?: number;
  shippingStatus?: string;
};

type ApiOrder = {
  orderNo?: string;
  customerNo?: string;
  customerName?: string;
  productNo?: string;
  productName?: string;
  quantity?: number;
  unit?: number;
  orderAmount?: number;
  estimatedCost?: number;
  estimatedMarginRate?: number;
  actualMarginRate?: number;
  dueTimestamp?: number;
  shipmentSummary?: ApiShipmentSummary;
  committedTimestamp?: number;
  stage?: string;
  deliveryRisk?: string;
  commitmentDecision?: string;
  productionFeasibility?: string;
  riskReason?: string;
  materialStatus?: string;
  productionStatus?: string;
  qualityStatus?: string;
  shippingStatus?: string;
  paymentStatus?: string;
  ownerDepartment?: number;
  priority?: string;
};

type ApiDeliveryRisk = {
  orderNo?: string;
  riskType?: string;
  riskLevel?: number;
  ownerDepartment?: number;
  dueTimestamp?: number;
  comment?: string;
};

type ApiMarginSignal = {
  orderNo?: string;
  estimatedMarginRate?: number;
  actualMarginRate?: number;
  marginRisk?: string;
  estimatedCost?: number;
  actualCost?: number;
};

type ApiPaymentSignal = {
  orderNo?: string;
  paymentStatus?: string;
  shippingOrderNo?: string;
  paymentNo?: string;
  paymentType?: string;
  paymentDueTimestamp?: number;
  receivedAmount?: number;
  remainingAmount?: number;
  paymentRisk?: string;
};

type ApiOrdersDashboardPayload = {
  serverTimestamp?: number;
  timezone?: string;
  range?: ApiOrdersRange;
  summary?: ApiOrdersSummary;
  total?: number;
  count?: number;
  start?: number;
  orders?: ApiOrder[];
  deliveryRisks?: ApiDeliveryRisk[];
  marginSignals?: ApiMarginSignal[];
  paymentSignals?: ApiPaymentSignal[];
};

type ApiFulfillmentStep = {
  stepCode?: string;
  refNo?: string;
  status?: string;
  ownerDepartment?: number;
  startTimestamp?: number;
  endTimestamp?: number;
  comment?: string;
};

type ApiFulfillmentDependency = {
  area?: string;
  status?: string;
  riskLevel?: number;
  ownerDepartment?: number;
  comment?: string;
};

type ApiOrdersFulfillmentPayload = {
  orderNo?: string;
  workflow?: ApiFulfillmentStep[];
  dependencies?: ApiFulfillmentDependency[];
};

export type OrdersDashboardResult = {
  data: OrdersDashboardData;
  source: OrdersDataSource;
  error?: string;
};

export type OrdersFulfillmentResult = {
  data?: OrdersFulfillmentData;
  source: OrdersDataSource;
  error?: string;
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

const DEPARTMENT_LABELS: Record<number, string> = {
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

const STAGE_LABELS: Record<string, SalesOrder["stage"]> = {
  accepted: "已接單",
  material_preparing: "備料中",
  scheduled: "已排產",
  in_production: "生產中",
  shipped: "已出貨",
  unknown: "待確認"
};

const RISK_LABELS: Record<string, OrderRiskLevel> = {
  normal: "正常",
  attention: "注意",
  high_risk: "高風險",
  unknown: "注意"
};

const PRODUCTION_FEASIBILITY_LABELS: Record<string, SalesOrder["productionFeasibility"]> = {
  deferred: "需協調",
  feasible: "可生產",
  coordination_required: "需協調",
  not_feasible: "不可如期",
  unknown: "需協調"
};

const COMMITMENT_LABELS: Record<string, SalesOrder["commitmentDecision"]> = {
  deferred: "需協調",
  feasible: "可承諾",
  coordination_required: "需協調",
  not_feasible: "不可承諾",
  unknown: "需協調"
};

const PRIORITY_LABELS: Record<string, SalesOrder["priority"]> = {
  high: "高",
  medium: "中",
  low: "低",
  unknown: "中"
};

const STATUS_LABELS: Record<string, string> = {
  done: "完成",
  in_progress: "進行中",
  pending: "待處理",
  blocked: "阻擋",
  unknown: "未知",
  not_started: "未開始",
  scheduled: "已排程",
  completed: "完成",
  ready: "可用",
  partial_shipped: "部分出貨",
  shipped: "已出貨",
  unpaid: "未收款",
  partial_paid: "部分收款",
  paid: "已收款",
  overdue: "逾期"
};

const RISK_REASON_LABELS: Record<string, string> = {
  overdue_due_date: "交期已逾期",
  payment_risk: "收款風險",
  due_date_approaching: "交期接近",
  empty: "無明顯風險",
  unknown: "未判定"
};

const STEP_LABELS: Record<string, string> = {
  order_received: "接單",
  commitment_check: "承諾檢查",
  material_request: "請購需求",
  purchase_readiness: "採購準備",
  warehouse_readiness: "倉庫準備",
  production: "生產",
  quality_check: "品檢",
  shipping: "出貨",
  payment: "收款"
};

const DEPENDENCY_LABELS: Record<string, OrderDependency["area"]> = {
  inventory: "庫存",
  purchasing: "採購",
  production: "生產",
  quality: "品檢",
  shipping: "出貨",
  payment: "收款"
};

function formatNumber(value: number) {
  return new Intl.NumberFormat("zh-TW", { maximumFractionDigits: 1 }).format(value);
}

function formatMoneyCompact(value: number) {
  if (Math.abs(value) >= 1000000) {
    return `$${(value / 1000000).toFixed(2)}M`;
  }
  return `$${new Intl.NumberFormat("zh-TW", { maximumFractionDigits: 0 }).format(value)}`;
}

function timestampToDate(value?: number) {
  if (!value) {
    return "";
  }
  return new Date(value * 1000).toLocaleDateString("zh-TW", {
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

function normalizePeriod(value?: string): OrdersDashboardPeriod {
  if (value === "7d" || value === "90d") {
    return value;
  }
  return "30d";
}

function statusTone(status?: string, riskLevel?: number): StatusTone {
  if (status === "blocked" || status === "overdue" || (riskLevel ?? 0) >= 3) {
    return "danger";
  }
  if (status === "pending" || status === "in_progress" || status === "partial_paid" || (riskLevel ?? 0) >= 2) {
    return "warning";
  }
  if (status === "done" || status === "ready" || status === "paid" || status === "completed") {
    return "success";
  }
  return "info";
}

function deliveryRiskTone(value?: string): StatusTone {
  if (value === "high_risk") {
    return "danger";
  }
  if (value === "attention") {
    return "warning";
  }
  return "success";
}

function buildSummary(payload: ApiOrdersDashboardPayload): OrderStatusSummary[] {
  const summary = payload.summary ?? {};
  return [
    {
      label: "未完成出貨訂單",
      value: formatNumber(summary.openOrderCount ?? 0),
      hint: `訂單總額 ${formatMoneyCompact(summary.totalOrderAmount ?? 0)}`,
      tone: (summary.openOrderCount ?? 0) > 0 ? "info" : "success"
    },
    {
      label: "交期高風險",
      value: formatNumber(summary.highRiskOrderCount ?? 0),
      hint: "逾期、交期急迫或付款風險",
      tone: (summary.highRiskOrderCount ?? 0) > 0 ? "danger" : "success"
    },
    {
      label: "承諾檢查",
      value: `${formatNumber(summary.commitmentRate ?? 0)}%`,
      hint: "第一版 ATP/CTP 延至下一版",
      tone: "warning"
    },
    {
      label: "毛利 / 收款風險",
      value: `${formatNumber(summary.estimatedMarginRiskCount ?? 0)} / ${formatNumber(
        summary.paymentRiskCount ?? 0
      )}`,
      hint: "成本缺漏與出貨後收款追蹤",
      tone: (summary.paymentRiskCount ?? 0) > 0 ? "warning" : "success"
    }
  ];
}

function mapWorkflowStep(item: ApiFulfillmentStep, index: number): OrderFulfillmentStep {
  const status = item.status ?? "unknown";
  return {
    label: STEP_LABELS[item.stepCode ?? ""] ?? "流程",
    ref: item.refNo ?? "",
    status: (STATUS_LABELS[status] ?? "未知") as OrderFulfillmentStep["status"],
    tone: statusTone(status),
    stepCode: item.stepCode,
    statusCode: status,
    ownerDepartment: item.ownerDepartment,
    startDate: timestampToDateTime(item.startTimestamp),
    endDate: timestampToDateTime(item.endTimestamp),
    comment: item.comment ?? `step-${index}`
  };
}

function mapDependency(item: ApiFulfillmentDependency): OrderDependency {
  const status = item.status ?? "unknown";
  return {
    area: DEPENDENCY_LABELS[item.area ?? ""] ?? "庫存",
    status: STATUS_LABELS[status] ?? "未知",
    note: item.comment ?? "",
    tone: statusTone(status, item.riskLevel),
    areaCode: item.area,
    statusCode: status,
    riskLevel: item.riskLevel,
    ownerDepartment: item.ownerDepartment
  };
}

function fallbackOrderWorkflow(order: ApiOrder): OrderFulfillmentStep[] {
  return [
    {
      label: "接單",
      ref: order.orderNo ?? "",
      status: "完成",
      tone: "success",
      stepCode: "order_received",
      statusCode: "done"
    },
    {
      label: "承諾檢查",
      ref: "ATP/CTP deferred",
      status: "待處理",
      tone: "info",
      stepCode: "commitment_check",
      statusCode: "unknown"
    },
    {
      label: "出貨",
      ref: `${formatNumber(order.shipmentSummary?.shippedQuantity ?? 0)} / ${formatNumber(order.quantity ?? 0)}`,
      status: (STATUS_LABELS[order.shippingStatus ?? "unknown"] ?? "待處理") as OrderFulfillmentStep["status"],
      tone: statusTone(order.shippingStatus),
      stepCode: "shipping",
      statusCode: order.shippingStatus
    },
    {
      label: "收款",
      ref: order.paymentStatus ?? "",
      status: (STATUS_LABELS[order.paymentStatus ?? "unknown"] ?? "待處理") as OrderFulfillmentStep["status"],
      tone: statusTone(order.paymentStatus),
      stepCode: "payment",
      statusCode: order.paymentStatus
    }
  ];
}

function fallbackDependencies(order: ApiOrder): OrderDependency[] {
  return [
    {
      area: "生產",
      status: STATUS_LABELS[order.productionStatus ?? "unknown"] ?? "未知",
      note: RISK_REASON_LABELS[order.riskReason ?? "unknown"] ?? order.riskReason ?? "",
      tone: statusTone(order.productionStatus),
      areaCode: "production",
      statusCode: order.productionStatus
    },
    {
      area: "出貨",
      status: STATUS_LABELS[order.shippingStatus ?? "unknown"] ?? "未知",
      note: `尚未出貨 ${formatNumber(order.shipmentSummary?.remainingQuantity ?? 0)} ${unitLabel(order.unit)}`,
      tone: statusTone(order.shippingStatus),
      areaCode: "shipping",
      statusCode: order.shippingStatus
    },
    {
      area: "收款",
      status: STATUS_LABELS[order.paymentStatus ?? "unknown"] ?? "未知",
      note: "出貨後依付款條件追蹤帳款",
      tone: statusTone(order.paymentStatus),
      areaCode: "payment",
      statusCode: order.paymentStatus
    }
  ];
}

function unitLabel(value?: number) {
  return value === undefined || value === null ? "" : UNIT_LABELS[value] ?? `單位 ${value}`;
}

function mapOrder(item: ApiOrder): SalesOrder {
  const stageCode = item.stage ?? "unknown";
  const deliveryRiskCode = item.deliveryRisk ?? "unknown";
  const commitmentDecisionCode = item.commitmentDecision ?? "deferred";
  const productionFeasibilityCode = item.productionFeasibility ?? "deferred";
  const priorityCode = item.priority ?? "medium";
  const riskReasonCode = item.riskReason ?? "unknown";
  const shippingStatusCode = item.shippingStatus ?? item.shipmentSummary?.shippingStatus ?? "unknown";

  return {
    id: item.orderNo ?? "",
    customerNo: item.customerNo,
    customer: item.customerName ?? "",
    channel: "",
    product: item.productName ?? "",
    itemNo: item.productNo ?? "",
    quantity: item.quantity ?? 0,
    unit: unitLabel(item.unit),
    orderAmount: item.orderAmount ?? 0,
    estimatedCost: item.estimatedCost ?? 0,
    estimatedMarginRate: item.estimatedMarginRate ?? 0,
    actualMarginRate: item.actualMarginRate ?? null,
    dueDate: timestampToDate(item.dueTimestamp),
    shipDate: timestampToDate(item.shipmentSummary?.lastShipTimestamp) || null,
    stage: STAGE_LABELS[stageCode] ?? "待確認",
    stageCode,
    tone: deliveryRiskTone(deliveryRiskCode),
    deliveryRisk: RISK_LABELS[deliveryRiskCode] ?? "注意",
    deliveryRiskCode,
    productionFeasibility: PRODUCTION_FEASIBILITY_LABELS[productionFeasibilityCode] ?? "需協調",
    productionFeasibilityCode,
    riskReason: RISK_REASON_LABELS[riskReasonCode] ?? riskReasonCode,
    riskReasonCode,
    materialStatus: STATUS_LABELS[item.materialStatus ?? "unknown"] ?? "未知",
    materialStatusCode: item.materialStatus,
    productionStatus: STATUS_LABELS[item.productionStatus ?? "unknown"] ?? "未知",
    productionStatusCode: item.productionStatus,
    qualityStatus: STATUS_LABELS[item.qualityStatus ?? "unknown"] ?? "未知",
    qualityStatusCode: item.qualityStatus,
    shippingStatus: STATUS_LABELS[shippingStatusCode] ?? "未知",
    shippingStatusCode,
    paymentStatus: STATUS_LABELS[item.paymentStatus ?? "unknown"] ?? "未知",
    paymentStatusCode: item.paymentStatus,
    owner: item.ownerDepartment ? DEPARTMENT_LABELS[item.ownerDepartment] ?? `部門 ${item.ownerDepartment}` : "待指派",
    ownerDepartment: item.ownerDepartment,
    priority: PRIORITY_LABELS[priorityCode] ?? "中",
    priorityCode,
    committedDate: timestampToDate(item.committedTimestamp) || "待下一版",
    commitmentDecision: COMMITMENT_LABELS[commitmentDecisionCode] ?? "需協調",
    commitmentDecisionCode,
    shipmentCount: item.shipmentSummary?.shipmentCount ?? 0,
    shippedQuantity: item.shipmentSummary?.shippedQuantity ?? 0,
    remainingQuantity: item.shipmentSummary?.remainingQuantity ?? 0,
    commitmentChecks: [],
    dependencies: fallbackDependencies(item),
    workflow: fallbackOrderWorkflow(item)
  };
}

function mapOrdersDashboardPayload(payload: ApiOrdersDashboardPayload): OrdersDashboardData {
  const orders = withFallbackArray<ApiOrder>(payload.orders, []).map(mapOrder);
  return {
    summary: buildSummary(payload),
    orders,
    total: payload.total ?? orders.length,
    count: payload.count ?? orders.length,
    start: payload.start ?? 0,
    serverDate: timestampToDateTime(payload.serverTimestamp),
    range: {
      period: normalizePeriod(payload.range?.period),
      startDate: timestampToDate(payload.range?.startTimestamp),
      endDate: timestampToDate(payload.range?.endTimestamp)
    }
  };
}

function mapFulfillmentPayload(payload: ApiOrdersFulfillmentPayload): OrdersFulfillmentData {
  return {
    orderNo: payload.orderNo ?? "",
    workflow: withFallbackArray<ApiFulfillmentStep>(payload.workflow, []).map(mapWorkflowStep),
    dependencies: withFallbackArray<ApiFulfillmentDependency>(payload.dependencies, []).map(mapDependency)
  };
}

function buildDashboardPath(query: OrdersDashboardQuery = {}) {
  const params = new URLSearchParams();
  params.set("period", query.period ?? "30d");
  params.set("start", String(query.start ?? 0));
  params.set("count", String(query.count ?? 50));
  if (query.date !== undefined) {
    params.set("date", String(query.date));
  }
  if (query.customerNo) {
    params.set("customer_no", query.customerNo);
  }
  if (query.orderNo) {
    params.set("order_no", query.orderNo);
  }
  if (query.commitmentDecision) {
    params.set("commitmentDecision", query.commitmentDecision);
  }
  if (query.deliveryRisk) {
    params.set("deliveryRisk", query.deliveryRisk);
  }
  if (query.stage) {
    params.set("stage", query.stage);
  }
  if (query.keyword) {
    params.set("keyword", query.keyword);
  }
  return `/api/v2/orders/dashboard?${params.toString()}`;
}

export async function getOrdersDashboard(query: OrdersDashboardQuery = {}): Promise<OrdersDashboardResult> {
  try {
    const payload = await apiGet<ApiOrdersDashboardPayload>(buildDashboardPath(query));
    const data = mapOrdersDashboardPayload(payload);
    return {
      data: {
        ...data,
        summary: data.summary.length ? data.summary : ordersDashboardMock.summary,
        orders: data.orders.length ? data.orders : ordersDashboardMock.orders
      },
      source: "api"
    };
  } catch (error) {
    return {
      data: ordersDashboardMock,
      source: "mock",
      error: error instanceof Error ? error.message : "Orders API unavailable"
    };
  }
}

export async function getOrdersFulfillment(orderNo: string): Promise<OrdersFulfillmentResult> {
  try {
    const payload = await apiGet<ApiOrdersFulfillmentPayload>(
      `/api/v2/orders/${encodeURIComponent(orderNo)}/fulfillment`
    );
    return {
      data: mapFulfillmentPayload(payload),
      source: "api"
    };
  } catch (error) {
    const fallback = ordersDashboardMock.orders.find((order) => order.id === orderNo);
    return {
      data: fallback
        ? {
            orderNo,
            workflow: fallback.workflow,
            dependencies: fallback.dependencies
          }
        : undefined,
      source: "mock",
      error: error instanceof Error ? error.message : "Orders fulfillment API unavailable"
    };
  }
}
