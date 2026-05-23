import type { StatusTone } from "@/types/dashboard";

export type WorkOrderStage = "待排程" | "待備料" | "生產中" | "品檢" | "包裝" | "完工";

export type ProductionWorkspaceTab = "schedule" | "mes" | "analytics" | "details";

export type ProductionMaterialStatus = "足夠" | "待領料" | "短缺";
export type ProductionStaffStatus = "足夠" | "需支援" | "不足";
export type ProductionQualityStatus = "未開始" | "首件通過" | "檢驗中" | "待判定" | "合格" | "異常";

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

export type QualitySnapshot = {
  status: ProductionQualityStatus;
  sampleCount: number;
  defectCount: number;
  defectRate: number;
  pendingCount: number;
  result: string;
  tone: StatusTone;
};

export type WorkOrder = {
  id: string;
  product: string;
  batchNo: string;
  processType: "調理" | "冷凍" | "包裝" | "殺菌" | "備料";
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
  customerDueDate: string;
  deliveryRisk: "正常" | "注意" | "高風險";
  scheduleDate: string;
  startTime: string;
  endTime: string;
  changeoverMinutes: number;
  materialStatus: ProductionMaterialStatus;
  staffStatus: ProductionStaffStatus;
  requiredStaff: number;
  assignedStaff: number;
  machineStatus: "正常" | "待機" | "異常";
  standardHours: number;
  actualHours: number;
  efficiencyRate: number;
  standardMaterialQty: number;
  actualMaterialQty: number;
  materialLossRate: number;
  laborHours: number;
  laborCost: number;
  unitLaborCost: number;
  quality: QualitySnapshot;
  qualityBlocksInventory: boolean;
  qualityBlocksShipment: boolean;
  materials: ProductionMaterial[];
  workflow: ProductionWorkflowStep[];
  relatedDocuments: ProductionRelatedDocument[];
};

export type ProductionScheduleSlot = {
  workOrderId: string;
  product: string;
  processType: WorkOrder["processType"];
  startTime: string;
  endTime: string;
  materialStatus: ProductionMaterialStatus;
  staffStatus: ProductionStaffStatus;
  stage: WorkOrderStage;
  tone: StatusTone;
};

export type ProductionLineSchedule = {
  line: string;
  processType: WorkOrder["processType"];
  dailyCapacityHours: number;
  usedHours: number;
  availableHours: number;
  changeoverHours: number;
  bottleneckRank: number;
  slots: ProductionScheduleSlot[];
  tone: StatusTone;
};

export type ProductionDaySchedule = {
  date: string;
  label: string;
  lines: ProductionLineSchedule[];
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
