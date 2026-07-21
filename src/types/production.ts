import type { StatusTone } from "@/types/dashboard";

export type WorkOrderStage = string;

export type ProductionWorkspaceTab = "schedule" | "mes" | "analytics" | "details";

export type ProductionMaterialStatus = string;
export type ProductionStaffStatus = string;
export type ProductionQualityStatus = string;

export type ProductionMaterial = {
  itemNo: string;
  itemName: string;
  batchNo: string;
  requiredQty: number;
  issuedQty: number;
  unit: string;
  status: ProductionMaterialStatus;
  tone: StatusTone;
  statusCode?: string;
  unitCode?: number;
  availableQty?: number;
  returnedQty?: number;
};

export type ProductionWorkflowStep = {
  label: string;
  ref: string;
  status: "完成" | "進行中" | "待處理";
  tone: StatusTone;
  statusCode?: string;
  stepCode?: string;
};

export type ProductionRelatedDocument = {
  type: string;
  no: string;
  status: string;
  tone: StatusTone;
  statusCode?: string;
  timestamp?: string;
};

export type QualitySnapshot = {
  status: ProductionQualityStatus;
  sampleCount: number;
  defectCount: number;
  defectRate: number;
  pendingCount: number;
  result: string;
  tone: StatusTone;
  statusCode?: string;
};

export type WorkOrder = {
  id: string;
  product: string;
  batchNo: string;
  processType: string;
  line: string;
  stage: WorkOrderStage;
  tone: StatusTone;
  progress: number;
  plannedQty: number;
  completedQty: number;
  unit: string;
  owner: string;
  eta: string;
  priority: string;
  sourceOrder: string;
  bomNo: string;
  customerDueDate: string;
  deliveryRisk: string;
  scheduleDate: string;
  startTime: string;
  endTime: string;
  changeoverMinutes: number;
  materialStatus: ProductionMaterialStatus;
  staffStatus: ProductionStaffStatus;
  requiredStaff: number;
  assignedStaff: number;
  machineStatus: string;
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
  statusCode?: string;
  materialStatusCode?: string;
  staffStatusCode?: string;
  machineStatusCode?: string;
  qualityStatusCode?: string;
  deliveryRiskCode?: string;
  unitCode?: number;
  productionLineNo?: string;
  productNo?: string;
  ownerEmployeeNo?: string;
  actualStartTime?: string;
  actualEndTime?: string;
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
  titleCode?: string;
  descriptionCode?: string;
  count?: number;
};

export type ProductionDashboardData = {
  summary: ProductionSummaryItem[];
  orders: WorkOrder[];
  weekSchedule: ProductionDaySchedule[];
  alerts: ProductionAlert[];
};

export type ProductionDataSource = "api" | "mock";
