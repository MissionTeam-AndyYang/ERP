import type { StatusTone } from "@/types/dashboard";

export type InventoryCategory = "原料" | "半成品" | "成品" | "包材";

export type WarehouseKpi = {
  label: string;
  value: string;
  hint: string;
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
