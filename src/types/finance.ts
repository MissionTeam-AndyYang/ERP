import type { StatusTone } from "@/types/dashboard";

export type FinanceWorkspaceTab = "margin" | "receivables" | "payables" | "cost-variance";

export type FinanceRiskLevel = "正常" | "注意" | "高風險";

export type FinanceSummary = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type FinanceDocument = {
  type: string;
  no: string;
  status: "完整" | "待補" | "缺失";
  owner: string;
  tone: StatusTone;
};

export type FinanceWorkflowStep = {
  label: string;
  ref: string;
  status: "完成" | "進行中" | "待處理" | "阻擋";
  tone: StatusTone;
};

export type FinanceOrderCase = {
  id: string;
  salesOrder: string;
  shipmentNo: string | null;
  customer: string;
  product: string;
  orderAmount: number;
  estimatedCost: number;
  actualCost: number | null;
  estimatedMarginRate: number;
  actualMarginRate: number | null;
  marginVarianceRate: number | null;
  riskLevel: FinanceRiskLevel;
  riskReason: string;
  arStatus: "未請款" | "待請款" | "已請款" | "逾期";
  invoiceNo: string | null;
  paymentTerm: string;
  dueDate: string;
  collectedAmount: number;
  payableImpact: number;
  inventoryCostImpact: number;
  productionCostImpact: number;
  logisticsCostImpact: number;
  podStatus: "未簽收" | "已簽收" | "異常回報";
  owner: string;
  tone: StatusTone;
  documents: FinanceDocument[];
  workflow: FinanceWorkflowStep[];
};

