import type { StatusTone } from "@/types/dashboard";

export type TraceabilityWorkspaceTab = "search" | "chain" | "recall" | "documents";

export type TraceDirection = "原料到成品" | "成品到原料";

export type TraceSummary = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type TraceNode = {
  id: string;
  label: string;
  ref: string;
  status: string;
  tone: StatusTone;
};

export type TraceDocument = {
  type: string;
  no: string;
  status: "完整" | "待補" | "缺失";
  owner: string;
  tone: StatusTone;
};

export type TraceRecord = {
  id: string;
  queryType: "批號" | "品項" | "訂單" | "工單";
  queryValue: string;
  direction: TraceDirection;
  itemName: string;
  batchNo: string;
  sourceType: "採購" | "生產" | "出貨";
  supplier: string | null;
  customer: string | null;
  sourceDocument: string;
  workOrder: string | null;
  salesOrder: string | null;
  quantity: number;
  unit: string;
  warehouseName: string;
  shipTo: string | null;
  traceStatus: "完整" | "待補文件" | "斷鏈";
  riskReason: string;
  impactedQty: number;
  impactedCustomers: number;
  nodes: TraceNode[];
  documents: TraceDocument[];
};
