import type { StatusTone } from "@/types/dashboard";

export type OrderWorkspaceTab = "overview" | "commitment" | "delivery-risk" | "fulfillment" | "margin-payment";

export type OrderStage = "待確認" | "已接單" | "備料中" | "已排產" | "生產中" | "品檢中" | "待出貨" | "已出貨";

export type OrderRiskLevel = "正常" | "注意" | "高風險";

export type OrderStatusSummary = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type OrderFulfillmentStep = {
  label: string;
  ref: string;
  status: "完成" | "進行中" | "待處理" | "阻擋";
  tone: StatusTone;
};

export type OrderDependency = {
  area: "庫存" | "採購" | "生產" | "品檢" | "出貨" | "收款";
  status: string;
  note: string;
  tone: StatusTone;
};

export type OrderCommitmentCheck = {
  area: "ATP 庫存" | "物料缺口" | "產能" | "人員" | "品質/出貨";
  status: string;
  note: string;
  tone: StatusTone;
};

export type SalesOrder = {
  id: string;
  customer: string;
  channel: string;
  product: string;
  itemNo: string;
  quantity: number;
  unit: string;
  orderAmount: number;
  estimatedCost: number;
  estimatedMarginRate: number;
  actualMarginRate: number | null;
  dueDate: string;
  shipDate: string | null;
  stage: OrderStage;
  tone: StatusTone;
  deliveryRisk: OrderRiskLevel;
  productionFeasibility: "可生產" | "需協調" | "不可如期";
  riskReason: string;
  materialStatus: string;
  productionStatus: string;
  qualityStatus: string;
  shippingStatus: string;
  paymentStatus: string;
  owner: string;
  priority: "高" | "中" | "低";
  committedDate: string;
  commitmentDecision: "可承諾" | "需協調" | "不可承諾";
  commitmentChecks: OrderCommitmentCheck[];
  dependencies: OrderDependency[];
  workflow: OrderFulfillmentStep[];
};

export type OrdersDashboardData = {
  summary: OrderStatusSummary[];
  orders: SalesOrder[];
};

export type OrdersDataSource = "api" | "mock";
