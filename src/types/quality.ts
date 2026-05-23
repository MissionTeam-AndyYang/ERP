import type { StatusTone } from "@/types/dashboard";

export type QualityWorkspaceTab = "inspection" | "release-block" | "ncr" | "documents";

export type QualityStage = "待抽樣" | "檢驗中" | "待判定" | "已放行" | "隔離" | "退回";

export type QualityDecision = "放行" | "待判" | "隔離" | "返工" | "報廢";

export type QualitySummary = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type QualityWorkflowStep = {
  label: string;
  ref: string;
  status: "完成" | "進行中" | "待處理" | "阻擋";
  tone: StatusTone;
};

export type QualityDocument = {
  type: string;
  no: string;
  status: "完整" | "待補" | "缺失";
  owner: string;
  tone: StatusTone;
};

export type QualityInspection = {
  id: string;
  itemName: string;
  itemNo: string;
  batchNo: string;
  sourceType: "收貨" | "生產" | "出貨";
  sourceNo: string;
  workOrder: string | null;
  salesOrder: string | null;
  supplier: string | null;
  line: string | null;
  inspectionType: "首件" | "製程抽驗" | "成品" | "原料" | "出貨前";
  stage: QualityStage;
  decision: QualityDecision;
  tone: StatusTone;
  sampleCount: number;
  defectCount: number;
  defectRate: number;
  pendingTests: string[];
  issueReason: string;
  blocksInventory: boolean;
  blocksShipment: boolean;
  blocksProduction: boolean;
  owner: string;
  dueTime: string;
  documents: QualityDocument[];
  workflow: QualityWorkflowStep[];
};
