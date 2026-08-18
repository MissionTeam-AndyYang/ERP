import type { StatusTone } from "@/types/dashboard";

export type BatchDataSource = "api" | "mock";

export type BatchRiskLevelCode = "normal" | "attention" | "high_risk" | "unknown";

export type BatchSummary = {
  stockItemCount: number;
  highRiskItemCount: number;
  stockBatchCount: number;
  qualityHoldQuantity: number;
  nearExpiryBatchCount: number;
};

export type BatchKpiItem = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type BatchItemSummary = {
  itemNo: string;
  itemName: string;
  itemCategory: number;
  itemCategoryLabel: string;
  itemSubCategory: number;
  itemType: number;
  itemTypeLabel: string;
  unit: number;
  totalBatchCount: number;
  warehouseCount: number;
  currentQuantity: number;
  availableQuantity: number;
  reservedQuantity: number;
  qualityHoldQuantity: number;
  earliestValidDate: string;
  earliestValidTimestamp: number;
  qaHoldBatchCount: number;
  nearExpiryBatchCount: number;
  riskLevelCode: BatchRiskLevelCode;
  riskLevelLabel: string;
  riskCode: string;
  riskLabel: string;
  ownerDepartment: number;
  ownerDepartmentLabel: string;
  unitLabel: string;
  tone: StatusTone;
};

export type BatchDashboardData = {
  summary: BatchSummary;
  kpis: BatchKpiItem[];
  items: BatchItemSummary[];
  total: number;
  start: number;
  count: number;
};

export type BatchDistributionRow = {
  rowKey: string;
  batchNo: string;
  warehouseNo: string;
  warehouseName: string;
  locationCode: string;
  palletCount: number;
  currentQuantity: number;
  availableQuantity: number;
  reservedQuantity: number;
  qualityHoldQuantity: number;
  unit: number;
  unitLabel: string;
  validDate: string;
  validTimestamp: number;
  validDays: number;
  daysInStock: number;
  expiryStatusCode: string;
  expiryStatusLabel: string;
  qaStatusCode: string;
  qaStatusLabel: string;
  batchStageCode: string;
  batchStageLabel: string;
  riskLevelCode: BatchRiskLevelCode;
  riskLevelLabel: string;
  riskCodes: string[];
  riskLabels: string[];
  refCategory: number;
  refCategoryLabel: string;
  refNo: string;
  relatedDocuments: BatchRelatedDocument[];
  tone: StatusTone;
};

export type BatchDistributionData = {
  item: {
    itemNo: string;
    itemName: string;
    itemCategory: number;
    itemCategoryLabel: string;
    itemSubCategory: number;
    itemType: number;
    itemTypeLabel: string;
    unit: number;
    unitLabel: string;
  };
  batches: BatchDistributionRow[];
  total: number;
  start: number;
  count: number;
};

export type BatchRelatedDocument = {
  refCategory: number;
  refCategoryLabel: string;
  refNo: string;
};

export type BatchStockByWarehouse = {
  warehouseNo: string;
  warehouseName: string;
  locationCode: string;
  palletCount: number;
  currentQuantity: number;
  availableQuantity: number;
  reservedQuantity: number;
  qualityHoldQuantity: number;
  unit: number;
  unitLabel: string;
  riskLevelCode: BatchRiskLevelCode;
  riskLevelLabel: string;
  riskCodes: string[];
  riskLabels: string[];
  tone: StatusTone;
};

export type BatchInventoryRecord = {
  recordTime: string;
  refCategory: number;
  refCategoryLabel: string;
  refNo: string;
  warehouseNo: string;
  category: number;
  categoryLabel: string;
  source: number;
  sourceLabel: string;
  quantity: number;
  unit: number;
  unitLabel: string;
  amount: number;
};

export type BatchReservation = {
  reservationNo: string;
  refCategory: number;
  refCategoryLabel: string;
  refNo: string;
  warehouseNo: string;
  reservedQuantity: number;
  status: number;
  statusLabel: string;
  expiryTimestamp: string;
};

export type BatchQualityHold = {
  holdNo: string;
  warehouseNo: string;
  holdQuantity: number;
  status: number;
  statusLabel: string;
  reasonCode: string;
  reasonLabel: string;
  createdTimestamp: string;
};

export type BatchPalletMovement = {
  movementNo: string;
  warehouseNo: string;
  palletNo: string;
  palletCount: number;
  palletStatus: number;
  palletStatusLabel: string;
  movementTimestamp: string;
};

export type BatchTask = {
  taskId: number;
  taskType: number;
  taskTypeLabel: string;
  taskStatus: number;
  taskStatusLabel: string;
  nextOwnerDepartment: number;
  nextOwnerDepartmentLabel: string;
  dueTimestamp: string;
  refCategory: number;
  refCategoryLabel: string;
  refNo: string;
  tone: StatusTone;
};

export type BatchDetail = {
  batch: {
    batchNo: string;
    itemNo: string;
    itemName: string;
    itemCategory: number;
    itemCategoryLabel: string;
    itemSubCategory: number;
    itemType: number;
    itemTypeLabel: string;
    unit: number;
    unitLabel: string;
    validDate: string;
    validTimestamp: number;
    validDays: number;
    refCategory: number;
    refCategoryLabel: string;
    refNo: string;
    creatorNo: string;
    creationTime: string;
  };
  stockByWarehouse: BatchStockByWarehouse[];
  inventoryRecords: BatchInventoryRecord[];
  reservations: BatchReservation[];
  qualityHolds: BatchQualityHold[];
  palletMovements: BatchPalletMovement[];
  tasks: BatchTask[];
};
