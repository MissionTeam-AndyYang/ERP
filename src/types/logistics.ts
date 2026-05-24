import type { StatusTone } from "@/types/dashboard";

export type LogisticsWorkspaceTab = "shipments" | "dispatch-risk" | "cold-chain" | "documents";

export type ShipmentStage = "待出庫" | "待派車" | "裝車中" | "配送中" | "已簽收" | "暫緩出貨";

export type DeliveryRiskLevel = "正常" | "注意" | "高風險";

export type LogisticsSummary = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type LogisticsDocument = {
  type: string;
  no: string;
  status: "完整" | "待補" | "缺失";
  owner: string;
  tone: StatusTone;
};

export type LogisticsWorkflowStep = {
  label: string;
  ref: string;
  status: "完成" | "進行中" | "待處理" | "阻擋";
  tone: StatusTone;
};

export type Shipment = {
  id: string;
  salesOrder: string;
  customer: string;
  channel: string;
  destination: string;
  route: string;
  product: string;
  batchNo: string;
  quantity: number;
  unit: string;
  requestedArrivalTime: string;
  plannedDepartureTime: string;
  stage: ShipmentStage;
  tone: StatusTone;
  deliveryRisk: DeliveryRiskLevel;
  riskReason: string;
  warehouseStatus: "已出庫" | "待揀貨" | "待覆核" | "阻擋";
  qualityReleaseStatus: "已放行" | "待判定" | "阻擋";
  vehicleNo: string | null;
  driver: string | null;
  temperatureRequirement: string;
  currentTemperature: string | null;
  temperatureStatus: "正常" | "注意" | "異常";
  documentsReady: boolean;
  proofOfDeliveryStatus: "未簽收" | "已簽收" | "異常回報";
  owner: string;
  documents: LogisticsDocument[];
  workflow: LogisticsWorkflowStep[];
};

export type LogisticsDashboardData = {
  summary: LogisticsSummary[];
  shipments: Shipment[];
};

export type LogisticsDataSource = "api" | "mock";
