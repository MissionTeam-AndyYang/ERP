import type { StatusTone } from "@/types/dashboard";

export type InventoryCategory = "原料" | "物料" | "膠捲" | "在製品" | "製成品";

export type WarehouseKpi = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type WarehouseWorkspaceTab = "value-space" | "risk" | "tasks" | "details";

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
  reservedQuantity: number;
  availableQuantity: number;
  unit: string;
  amount: number;
  reservedAmount: number;
  availableAmount: number;
  palletCount: number;
  safetyStock: number;
  expiryDate: string;
  shelfLifeDays: number;
  daysLeft: number;
  turnoverDays: number;
  status: string;
  tone: StatusTone;
  workflow: WarehouseWorkflowStep[];
  relatedDocuments: WarehouseRelatedDocument[];
};

export type WarehouseCategorySummary = {
  category: InventoryCategory;
  amount: number;
  amountRatio: number;
  reservedAmount: number;
  availableAmount: number;
  palletCount: number;
  itemCount: number;
  trend7Days: number;
  tone: StatusTone;
};

export type WarehouseCapacity = {
  id: string;
  warehouseName: string;
  warehouseType: string;
  totalPallets: number;
  usedPallets: number;
  reservedPallets: number;
  availablePallets: number;
  tone: StatusTone;
};

export type WarehouseRisk = {
  id: string;
  type: "迴轉超過一個月" | "少於 1/3 效期" | "低於安全水位";
  itemName: string;
  category: InventoryCategory;
  batchNo: string;
  warehouseName: string;
  metric: string;
  recommendation: string;
  tone: StatusTone;
};

export type WarehouseTask = {
  id: string;
  type: "入庫" | "出庫" | "移倉" | "盤點";
  itemName: string;
  batchNo: string;
  quantity: number;
  unit: string;
  palletCount: number;
  owner: string;
  dueTime: string;
  sourceNo: string;
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
