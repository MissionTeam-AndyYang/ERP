import type { LucideIcon } from "lucide-react";

export type StatusTone = "success" | "warning" | "danger" | "info" | "neutral";

export type KpiItem = {
  title: string;
  value: string;
  unit: string;
  trend: string;
  tone: StatusTone;
  icon: LucideIcon;
};

export type AlertItem = {
  title: string;
  detail: string;
  time: string;
  tone: StatusTone;
};

export type ProductionLine = {
  line: string;
  product: string;
  batchNo: string;
  status: string;
  tone: StatusTone;
  progress: number;
  yieldRate: string;
  eta: string;
};

export type ProductionTrendPoint = {
  time: string;
  planned: number;
  actual: number;
};

export type OeeTrendPoint = {
  time: string;
  oee: number;
  target: number;
};

export type QualityTrendPoint = {
  date: string;
  yieldRate: number;
  reworkRate: number;
};

export type AlertDistributionItem = {
  name: string;
  value: number;
  tone: StatusTone;
};

export type ManagerFocusItem = {
  label: string;
  value: string;
  detail: string;
  tone: StatusTone;
  icon: LucideIcon;
};

export type ManagerDecisionItem = {
  title: string;
  owner: string;
  due: string;
  impact: string;
  action: string;
  tone: StatusTone;
};

export type DepartmentBlocker = {
  department: string;
  title: string;
  detail: string;
  owner: string;
  relatedModule: string;
  href: string;
  tone: StatusTone;
};

export type TodayTask = {
  time: string;
  module: string;
  title: string;
  status: string;
  tone: StatusTone;
};

export type PreOrderPipelineItem = {
  stage: string;
  count: number;
  focus: string;
  owner: string;
  tone: StatusTone;
};

export type ManagerSnapshot = {
  fulfillmentRisk: string;
  deliveryCommitment: string;
  marginSignal: string;
  cashSignal: string;
};

export type ModuleShortcut = {
  label: string;
  href: string;
  icon: LucideIcon;
};

export type DashboardData = {
  managerSnapshot: ManagerSnapshot;
  managerFocusItems: ManagerFocusItem[];
  managerDecisionItems: ManagerDecisionItem[];
  departmentBlockers: DepartmentBlocker[];
  todayTasks: TodayTask[];
  preOrderPipeline: PreOrderPipelineItem[];
  productionLines: ProductionLine[];
  alertItems: AlertItem[];
  productionTrendData: ProductionTrendPoint[];
  oeeTrendData: OeeTrendPoint[];
  qualityTrendData: QualityTrendPoint[];
  alertDistributionData: AlertDistributionItem[];
  moduleShortcuts: ModuleShortcut[];
};

export type DashboardDataSource = "api" | "mock";
