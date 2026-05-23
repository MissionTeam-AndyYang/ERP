import type { StatusTone } from "@/types/dashboard";

export type RdWorkspaceTab = "projects" | "bom-versions" | "costing" | "quotation";

export type RdStage = "需求確認" | "配方設計" | "試作" | "成本試算" | "報價中" | "量產移轉";

export type RdDecision = "可報價" | "需調整" | "暫緩";

export type RdSummary = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type BomCostLine = {
  category: "原料" | "物料" | "包材" | "膠捲" | "人工" | "製造費用" | "物流";
  itemName: string;
  version: string;
  unitCost: number;
  usageQty: number;
  lossRate: number;
  costAmount: number;
  note: string;
  tone: StatusTone;
};

export type RdWorkflowStep = {
  label: string;
  ref: string;
  status: "完成" | "進行中" | "待處理" | "阻擋";
  tone: StatusTone;
};

export type RdProject = {
  id: string;
  customer: string;
  productName: string;
  targetChannel: string;
  stage: RdStage;
  decision: RdDecision;
  tone: StatusTone;
  priority: "高" | "中" | "低";
  owner: string;
  targetLaunchDate: string;
  sampleDueDate: string;
  bomNo: string;
  bomVersion: string;
  bomStatus: "開發版" | "試作版" | "報價版" | "量產版";
  targetPrice: number;
  suggestedQuote: number;
  minimumQuote: number;
  targetMarginRate: number;
  estimatedMarginRate: number;
  totalUnitCost: number;
  materialCost: number;
  packagingCost: number;
  laborCost: number;
  overheadCost: number;
  logisticsCost: number;
  lossRate: number;
  quoteRiskReason: string;
  transferReadiness: string;
  costLines: BomCostLine[];
  workflow: RdWorkflowStep[];
};

