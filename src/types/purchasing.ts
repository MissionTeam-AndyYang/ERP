import type { StatusTone } from "@/types/dashboard";

export type PurchasingWorkspaceTab = "demand" | "delivery-risk" | "receiving" | "suppliers";

export type PurchaseStage = "請購" | "詢價" | "待核准" | "已下單" | "待到貨" | "驗收中" | "已入庫";

export type PurchaseRiskLevel = "正常" | "注意" | "高風險";

export type PurchasingSummary = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type PurchaseDependency = {
  area: "訂單" | "生產" | "庫存" | "品檢" | "入庫";
  status: string;
  note: string;
  tone: StatusTone;
};

export type PurchaseWorkflowStep = {
  label: string;
  ref: string;
  status: "完成" | "進行中" | "待處理" | "阻擋";
  tone: StatusTone;
};

export type PurchaseItem = {
  id: string;
  requestNo: string;
  purchaseOrderNo: string | null;
  itemNo: string;
  itemName: string;
  category: "原料" | "物料" | "膠捲" | "包材";
  supplier: string;
  quantity: number;
  unit: string;
  amount: number;
  requiredDate: string;
  expectedArrivalDate: string | null;
  stage: PurchaseStage;
  tone: StatusTone;
  riskLevel: PurchaseRiskLevel;
  riskReason: string;
  sourceOrder: string | null;
  linkedWorkOrder: string | null;
  currentStock: number;
  reservedStock: number;
  availableStock: number;
  safetyStock: number;
  leadTimeDays: number;
  delayDays: number;
  qualityDocumentStatus: "完整" | "待補" | "缺失";
  receivingStatus: string;
  warehouseStatus: string;
  owner: string;
  dependencies: PurchaseDependency[];
  workflow: PurchaseWorkflowStep[];
};
