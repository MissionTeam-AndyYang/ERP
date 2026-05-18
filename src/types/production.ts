import type { StatusTone } from "@/types/dashboard";

export type WorkOrderStage = "待生產" | "生產中" | "品檢" | "包裝" | "完工";

export type WorkOrder = {
  id: string;
  product: string;
  batchNo: string;
  line: string;
  stage: WorkOrderStage;
  tone: StatusTone;
  progress: number;
  plannedQty: number;
  completedQty: number;
  owner: string;
  eta: string;
  priority: "高" | "中" | "低";
};

export type ProductionScheduleItem = {
  line: string;
  slots: {
    time: string;
    workOrderId: string;
    product: string;
    stage: WorkOrderStage;
    tone: StatusTone;
  }[];
};

export type ProductionSummaryItem = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};
