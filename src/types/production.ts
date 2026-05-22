import type { StatusTone } from "@/types/dashboard";

export type WorkOrderStage = "待排程" | "待備料" | "生產中" | "品檢" | "包裝" | "完工";

export type ProductionWorkspaceTab = "orders" | "materials" | "quality" | "capacity";

export type ProductionMaterialStatus = "足夠" | "待領料" | "短缺";

export type ProductionMaterial = {
  itemNo: string;
  itemName: string;
  batchNo: string;
  requiredQty: number;
  issuedQty: number;
  unit: string;
  status: ProductionMaterialStatus;
  tone: StatusTone;
};

export type ProductionWorkflowStep = {
  label: string;
  ref: string;
  status: "完成" | "進行中" | "待處理";
  tone: StatusTone;
};

export type ProductionRelatedDocument = {
  type: string;
  no: string;
  status: string;
  tone: StatusTone;
};

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
  unit: string;
  owner: string;
  eta: string;
  priority: "高" | "中" | "低";
  sourceOrder: string;
  bomNo: string;
  startTime: string;
  endTime: string;
  qualityStatus: string;
  materialStatus: ProductionMaterialStatus;
  materials: ProductionMaterial[];
  workflow: ProductionWorkflowStep[];
  relatedDocuments: ProductionRelatedDocument[];
};

export type ProductionScheduleItem = {
  line: string;
  utilization: number;
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

export type ProductionAlert = {
  id: string;
  title: string;
  description: string;
  tone: StatusTone;
};
