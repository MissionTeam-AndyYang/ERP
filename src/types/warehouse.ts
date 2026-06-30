import type { StatusTone } from "@/types/dashboard";

export type InventoryCategory = "原料" | "物料" | "膠捲" | "在製品" | "製成品";

export type WarehouseKpi = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type WarehouseWorkspaceTab = "value-space" | "risk" | "tasks" | "details";

export type WarehouseSourceType = "採購" | "生產" | "銷退" | "倉庫" | "調整";

export type WarehouseRecord = {
  id: string;
  itemNo: string;
  itemName: string;
  category: InventoryCategory;
  warehouseNo: string;
  warehouseName: string;
  batchNo: string;
  sourceLabel: WarehouseSourceType;
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

export type WarehouseDashboardData = {
  kpis: WarehouseKpi[];
  categorySummaries: WarehouseCategorySummary[];
  capacities: WarehouseCapacity[];
  records: WarehouseRecord[];
  risks: WarehouseRisk[];
  tasks: WarehouseTask[];
};

export type WarehouseDataSource = "api" | "mock";

export type WarehouseInventoryLotSummary = {
  lotCount: number;
  itemCount: number;
  totalQuantity: number;
  totalInventoryValue: number;
  totalAvailableQuantity: number;
  totalAvailableValue: number;
  riskLotCount: number;
  pendingTaskCount: number;
};

export type WarehouseInventoryLot = {
  lotKey: string;
  warehouseNo: string;
  warehouseName: string;
  category: InventoryCategory;
  itemNo: string;
  itemName: string;
  batchNo: string;
  unit: string;
  currentQuantity: number;
  reservedQuantity: number;
  qualityHoldQuantity: number;
  availableQuantity: number;
  unitCost: number;
  inventoryValue: number;
  reservedValue: number;
  qualityHoldValue: number;
  availableValue: number;
  palletCount: number;
  firstInboundDate: string;
  daysInStock: number;
  validDays: number;
  validDate: string;
  remainingShelfLifeRatio: number;
  safetyStock: number;
  riskTypes: string[];
  riskLabel: string;
  riskTone: StatusTone;
  openTaskCount: number;
  refNo: string;
  refCategoryLabel: WarehouseSourceType;
};

export type WarehouseInventoryLotListData = {
  summary: WarehouseInventoryLotSummary;
  lots: WarehouseInventoryLot[];
  total: number;
  count: number;
  start: number;
};

export type WarehouseInventoryRecordLine = {
  id: string;
  refCategoryLabel: WarehouseSourceType;
  refNo: string;
  refSubNo: string;
  date: string;
  categoryLabel: "入庫" | "出庫" | "其他";
  quantity: number;
  amount: number;
  tone: StatusTone;
};

export type WarehouseReservationLine = {
  id: string;
  reservationNo: string;
  refCategoryLabel: string;
  refNo: string;
  reservedQuantity: number;
  reservedValue: number;
  releaseDate: string;
  status: string;
  tone: StatusTone;
};

export type WarehouseQualityHoldLine = {
  id: string;
  holdNo: string;
  inspectionNo: string;
  holdQuantity: number;
  holdValue: number;
  reason: string;
  status: string;
  tone: StatusTone;
};

export type WarehousePalletMovementLine = {
  id: string;
  movementNo: string;
  date: string;
  palletGroupNo: string;
  palletStatus: string;
  palletCount: number;
  refCategoryLabel: string;
  refNo: string;
  tone: StatusTone;
};

export type WarehouseWorkflowTaskLine = {
  id: string;
  taskId: string;
  taskTypeLabel: string;
  taskStatusLabel: string;
  ownerDepartmentLabel: string;
  expectedQuantity: number;
  processedQuantity: number;
  remainingQuantity: number;
  dueDate: string;
  blockReason: string;
  tone: StatusTone;
};

export type WarehouseInventoryLotDetail = {
  lot: WarehouseInventoryLot;
  inventoryRecords: WarehouseInventoryRecordLine[];
  reservations: WarehouseReservationLine[];
  qualityHolds: WarehouseQualityHoldLine[];
  palletMovements: WarehousePalletMovementLine[];
  workflowTasks: WarehouseWorkflowTaskLine[];
};

export type WarehouseTaskWorkbenchRange = {
  mode: string;
  startDate: string;
  endDate: string;
};

export type WarehouseTaskWorkbenchSummary = {
  openTaskCount: number;
  overdueTaskCount: number;
  blockedTaskCount: number;
  inboundTaskCount: number;
  outboundTaskCount: number;
  qualityTaskCount: number;
  shipmentTaskCount: number;
  inventoryShortageTaskCount: number;
};

export type WarehouseTaskWorkbenchLane = {
  laneCode: string;
  taskCount: number;
  riskCount: number;
};

export type WarehouseTaskWorkbenchItem = {
  taskId: string;
  taskType?: number;
  taskStatus?: number;
  refCategory?: number;
  refNo: string;
  refSubNo: string;
  itemCategory?: number;
  itemNo: string;
  itemName: string;
  batchNo: string;
  unit?: number;
  expectedQuantity: number;
  processedQuantity: number;
  remainingQuantity: number;
  warehouseNo: string;
  warehouseName: string;
  dueDate: string;
  ownerDepartment?: number;
  riskLevel?: number;
  riskTypes: string[];
  blockReasonCode: string;
  blockReason: string;
  availableQuantity: number;
  reservedQuantity: number;
  qualityHoldQuantity: number;
  inventoryValue: number;
  nextActionCode: string;
};

export type WarehouseTaskWorkbenchData = {
  serverDate: string;
  range: WarehouseTaskWorkbenchRange;
  summary: WarehouseTaskWorkbenchSummary;
  lanes: WarehouseTaskWorkbenchLane[];
  tasks: WarehouseTaskWorkbenchItem[];
  total: number;
  count: number;
  start: number;
};

export type WarehouseTaskRelatedLot = {
  lotKey: string;
  warehouseNo: string;
  itemNo: string;
  itemName: string;
  batchNo: string;
  currentQuantity: number;
  availableQuantity: number;
  qualityHoldQuantity: number;
  validDate: string;
  riskTypes: string[];
};

export type WarehouseTaskSourceRef = {
  refCategory?: number;
  refNo: string;
  refSubNo: string;
  descriptionCode: string;
};

export type WarehouseTaskTimelineEvent = {
  id: string;
  eventCode: string;
  eventDate: string;
  department?: number;
  status?: number;
  comment: string;
};

export type WarehouseTaskDetail = {
  task: Pick<
    WarehouseTaskWorkbenchItem,
    | "taskId"
    | "taskType"
    | "taskStatus"
    | "refCategory"
    | "refNo"
    | "refSubNo"
    | "ownerDepartment"
    | "warehouseNo"
    | "warehouseName"
    | "dueDate"
    | "blockReasonCode"
    | "blockReason"
    | "riskLevel"
    | "riskTypes"
    | "nextActionCode"
  >;
  quantity: Pick<
    WarehouseTaskWorkbenchItem,
    | "itemCategory"
    | "itemNo"
    | "itemName"
    | "batchNo"
    | "unit"
    | "expectedQuantity"
    | "processedQuantity"
    | "remainingQuantity"
    | "availableQuantity"
    | "reservedQuantity"
    | "qualityHoldQuantity"
  >;
  relatedLots: WarehouseTaskRelatedLot[];
  sourceRefs: WarehouseTaskSourceRef[];
  timeline: WarehouseTaskTimelineEvent[];
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
