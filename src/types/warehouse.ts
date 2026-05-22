import type { StatusTone } from "@/types/dashboard";

export type InventoryCategory = "原料" | "半成品" | "成品" | "包材";

export type WarehouseKpi = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type WarehouseWorkspaceTab = "overview" | "batches" | "movements" | "storage";

export type WarehouseSourceType = "採購" | "生產" | "出貨" | "調整";

export type WarehouseRecord = {
  id: string;
  itemNo: string;
  itemName: string;
  category: InventoryCategory;
  warehouseNo: string;
  warehouseName: string;
  batchNo: string;
  sourceType: WarehouseSourceType;
  sourceNo: string;
  quantity: number;
  unit: string;
  amount: number;
  expiryDate: string;
  daysLeft: number;
  status: string;
  tone: StatusTone;
  storageDays: number;
  storageCharge: number;
  paymentStatus: string;
  workflow: WarehouseWorkflowStep[];
  relatedDocuments: WarehouseRelatedDocument[];
};

export type InventoryItem = {
  sku: string;
  name: string;
  category: InventoryCategory;
  warehouse: string;
  location: string;
  quantity: number;
  unit: string;
  safetyStock: number;
  status: string;
  tone: StatusTone;
};

export type ExpiryBatch = {
  batchNo: string;
  itemName: string;
  category: InventoryCategory;
  quantity: number;
  unit: string;
  expiryDate: string;
  daysLeft: number;
  location: string;
  tone: StatusTone;
};

export type WarehouseTask = {
  id: string;
  type: "入庫" | "出庫" | "移倉" | "盤點";
  itemName: string;
  batchNo: string;
  quantity: number;
  unit: string;
  owner: string;
  dueTime: string;
  status: string;
  tone: StatusTone;
};

export type WarehouseWorkflowStep = {
  label: string;
  ref: string;
  status: "完成" | "進行中" | "待處理";
  tone: StatusTone;
};

export type WarehouseRelatedDocument = {
  type: string;
  no: string;
  status: string;
  tone: StatusTone;
};

export type WarehouseException = {
  id: string;
  title: string;
  description: string;
  tone: StatusTone;
};
