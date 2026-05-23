import type { StatusTone } from "@/types/dashboard";

export type PlanningWorkspaceTab = "demand" | "materials" | "capacity" | "work-orders";

export type PlanningDecision = "可執行" | "需協調" | "不可執行";

export type PlanningSummary = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type PlanningCheck = {
  area: "訂單需求" | "BOM 展開" | "庫存/批號" | "採購請購" | "產能" | "人員" | "品保/出貨";
  status: string;
  note: string;
  tone: StatusTone;
};

export type MaterialRequirement = {
  itemNo: string;
  itemName: string;
  category: "原料" | "物料" | "包材" | "膠捲";
  requiredQty: number;
  availableQty: number;
  shortageQty: number;
  unit: string;
  requiredDate: string;
  suggestedAction: "直接備料" | "請購" | "調撥" | "品質放行後備料";
  tone: StatusTone;
};

export type CapacityRequirement = {
  processType: "備料" | "調理" | "冷凍" | "包裝" | "殺菌";
  line: string;
  requiredHours: number;
  availableHours: number;
  changeoverMinutes: number;
  staffRequired: number;
  staffAssigned: number;
  status: string;
  tone: StatusTone;
};

export type PlannedWorkOrder = {
  workOrderNo: string;
  line: string;
  startTime: string;
  endTime: string;
  quantity: number;
  unit: string;
  status: "建議建立" | "需調整" | "可排入";
  tone: StatusTone;
};

export type PlanningCase = {
  id: string;
  sourceOrder: string;
  customer: string;
  product: string;
  itemNo: string;
  quantity: number;
  unit: string;
  dueDate: string;
  promisedDate: string;
  decision: PlanningDecision;
  tone: StatusTone;
  priority: "高" | "中" | "低";
  owner: string;
  planningNote: string;
  materialShortageValue: number;
  requiredProductionHours: number;
  availableProductionHours: number;
  purchaseRequestCount: number;
  suggestedWorkOrderCount: number;
  checks: PlanningCheck[];
  materials: MaterialRequirement[];
  capacity: CapacityRequirement[];
  workOrders: PlannedWorkOrder[];
};

