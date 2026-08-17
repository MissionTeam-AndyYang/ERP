import type { DataSourceMode } from "@/components/common/data-source-toggle";
import {
  batchDepartmentLabel,
  batchInventoryCategoryLabel,
  batchInventorySourceLabel,
  batchItemCategoryLabel,
  batchItemTypeLabel,
  batchPalletStatusLabel,
  batchQaStatusLabel,
  batchQualityHoldReasonLabel,
  batchQualityHoldStatusLabel,
  batchRefCategoryLabel,
  batchReservationStatusLabel,
  batchRiskLabel,
  batchRiskLevelLabel,
  batchRiskTone,
  batchStageLabel,
  batchTaskStatusLabel,
  batchTaskStatusTone,
  batchTaskTypeLabel,
  batchUnitLabel,
  normalizeBatchRiskLevel
} from "@/i18n/batch-enums";
import { batchDetailMock, batchDistributionMock, batchesDashboardMock } from "@/mock/batches";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type {
  BatchDashboardData,
  BatchDataSource,
  BatchDetail,
  BatchDistributionData,
  BatchDistributionRow,
  BatchInventoryRecord,
  BatchItemSummary,
  BatchKpiItem,
  BatchQualityHold,
  BatchRelatedDocument,
  BatchReservation,
  BatchStockByWarehouse,
  BatchSummary,
  BatchTask
} from "@/types/batches";

type ApiBatchSummary = Partial<BatchSummary>;

type ApiBatchDashboardItem = {
  itemNo?: string;
  itemName?: string;
  itemCategory?: number;
  itemSubCategory?: number;
  itemType?: number;
  totalBatchCount?: number;
  warehouseCount?: number;
  currentQuantity?: number;
  availableQuantity?: number;
  reservedQuantity?: number;
  qualityHoldQuantity?: number;
  earliestValidDate?: number;
  qaHoldBatchCount?: number;
  nearExpiryBatchCount?: number;
  riskLevelCode?: string;
  riskCode?: string;
  ownerDepartment?: number;
};

type ApiBatchDashboardPayload = {
  serverTimestamp?: number;
  summary?: ApiBatchSummary;
  items?: ApiBatchDashboardItem[];
  total?: number;
  start?: number;
  count?: number;
};

type ApiBatchRelatedDocument = {
  refCategory?: number;
  refNo?: string;
};

type ApiBatchDistributionRow = {
  batchNo?: string;
  warehouseNo?: string;
  warehouseName?: string;
  locationCode?: string;
  palletCount?: number;
  currentQuantity?: number;
  availableQuantity?: number;
  reservedQuantity?: number;
  qualityHoldQuantity?: number;
  unit?: number;
  validDate?: number;
  validDays?: number;
  qaStatusCode?: string;
  batchStageCode?: string;
  riskLevelCode?: string;
  riskCodes?: string[];
  refCategory?: number;
  refNo?: string;
  relatedDocuments?: ApiBatchRelatedDocument[];
};

type ApiBatchDistributionPayload = {
  item?: {
    itemNo?: string;
    itemName?: string;
    itemCategory?: number;
    itemSubCategory?: number;
    itemType?: number;
    unit?: number;
  };
  batches?: ApiBatchDistributionRow[];
  total?: number;
  start?: number;
  count?: number;
};

type ApiBatchDetailPayload = {
  batch?: {
    batchNo?: string;
    itemNo?: string;
    itemName?: string;
    itemCategory?: number;
    itemSubCategory?: number;
    itemType?: number;
    unit?: number;
    validDate?: number;
    validDays?: number;
    refCategory?: number;
    refNo?: string;
    creatorNo?: string;
    creationTime?: number;
  };
  stockByWarehouse?: ApiBatchDistributionRow[];
  inventoryRecords?: {
    recordTime?: number;
    refCategory?: number;
    refNo?: string;
    warehouseNo?: string;
    category?: number;
    source?: number;
    quantity?: number;
    unit?: number;
    amount?: number;
  }[];
  reservations?: {
    reservationNo?: string;
    refCategory?: number;
    refNo?: string;
    warehouseNo?: string;
    reservedQuantity?: number;
    status?: number;
    expiryTimestamp?: number;
  }[];
  qualityHolds?: {
    holdNo?: string;
    warehouseNo?: string;
    holdQuantity?: number;
    status?: number;
    reasonCode?: string;
    createdTimestamp?: number;
  }[];
  palletMovements?: {
    movementNo?: string;
    warehouseNo?: string;
    palletNo?: string;
    palletCount?: number;
    palletStatus?: number;
    movementTimestamp?: number;
  }[];
  tasks?: {
    taskId?: number;
    taskType?: number;
    taskStatus?: number;
    nextOwnerDepartment?: number;
    dueTimestamp?: number;
    refCategory?: number;
    refNo?: string;
  }[];
};

export type BatchDashboardQuery = {
  keyword?: string;
  itemCategory?: number;
  itemSubCategory?: number;
  itemType?: number;
  warehouseNo?: string;
  batchNo?: string;
  riskLevelCode?: string;
  qaStatusCode?: string;
  batchStageCode?: string;
  availabilityCode?: string;
  start?: number;
  count?: number;
};

export type BatchDashboardResult = {
  data: BatchDashboardData;
  source: BatchDataSource;
  error?: string;
};

export type BatchDistributionResult = {
  data: BatchDistributionData;
  source: BatchDataSource;
  error?: string;
};

export type BatchDetailResult = {
  detail?: BatchDetail;
  source: BatchDataSource;
  error?: string;
};

const locale = "zh-TW";

export const emptyBatchDashboardData: BatchDashboardData = {
  summary: {
    stockItemCount: 0,
    highRiskItemCount: 0,
    stockBatchCount: 0,
    qualityHoldQuantity: 0,
    nearExpiryBatchCount: 0
  },
  kpis: [
    { label: "批號管理品項", value: "0", hint: "目前沒有資料", tone: "info" },
    { label: "高風險品項", value: "0", hint: "目前沒有資料", tone: "success" },
    { label: "分倉批號", value: "0", hint: "目前沒有資料", tone: "info" },
    { label: "品檢保留量", value: "0", hint: "目前沒有資料", tone: "neutral" }
  ],
  items: [],
  total: 0,
  start: 0,
  count: 0
};

export const emptyBatchDistributionData: BatchDistributionData = {
  item: {
    itemNo: "",
    itemName: "",
    itemCategory: 0,
    itemCategoryLabel: batchItemCategoryLabel(0),
    itemSubCategory: 0,
    itemType: 0,
    itemTypeLabel: batchItemTypeLabel(0),
    unit: 0,
    unitLabel: batchUnitLabel(0)
  },
  batches: [],
  total: 0,
  start: 0,
  count: 0
};

function asNumber(value?: number) {
  return Number.isFinite(value) ? Number(value) : 0;
}

function formatInteger(value?: number) {
  return new Intl.NumberFormat(locale, { maximumFractionDigits: 0 }).format(value ?? 0);
}

function formatQuantity(value?: number) {
  return new Intl.NumberFormat(locale, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value ?? 0);
}

function timestampToDate(value?: number) {
  if (!value) {
    return "";
  }
  return new Date(value * 1000).toLocaleDateString(locale, { timeZone: "Asia/Taipei" });
}

function normalizeSummary(summary?: ApiBatchSummary): BatchSummary {
  return {
    stockItemCount: asNumber(summary?.stockItemCount),
    highRiskItemCount: asNumber(summary?.highRiskItemCount),
    stockBatchCount: asNumber(summary?.stockBatchCount),
    qualityHoldQuantity: asNumber(summary?.qualityHoldQuantity),
    nearExpiryBatchCount: asNumber(summary?.nearExpiryBatchCount)
  };
}

function kpisFromSummary(summary: BatchSummary): BatchKpiItem[] {
  return [
    { label: "批號管理品項", value: formatInteger(summary.stockItemCount), hint: "目前有庫存的批號品項", tone: "info" },
    { label: "高風險品項", value: formatInteger(summary.highRiskItemCount), hint: "需優先確認", tone: summary.highRiskItemCount ? "danger" : "success" },
    { label: "分倉批號", value: formatInteger(summary.stockBatchCount), hint: "跨倉庫或產製情境的批號列", tone: "info" },
    { label: "品檢保留量", value: formatQuantity(summary.qualityHoldQuantity), hint: `即期 ${formatInteger(summary.nearExpiryBatchCount)} 批`, tone: summary.qualityHoldQuantity ? "warning" : "neutral" }
  ];
}

function mapDashboardItem(item: ApiBatchDashboardItem): BatchItemSummary {
  const riskLevelCode = normalizeBatchRiskLevel(item.riskLevelCode);
  const riskCodes = item.riskCode ? [item.riskCode] : [];
  const unitLabel = "單位";

  return {
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    itemCategory: asNumber(item.itemCategory),
    itemCategoryLabel: batchItemCategoryLabel(item.itemCategory),
    itemSubCategory: asNumber(item.itemSubCategory),
    itemType: asNumber(item.itemType),
    itemTypeLabel: batchItemTypeLabel(item.itemType),
    totalBatchCount: asNumber(item.totalBatchCount),
    warehouseCount: asNumber(item.warehouseCount),
    currentQuantity: asNumber(item.currentQuantity),
    availableQuantity: asNumber(item.availableQuantity),
    reservedQuantity: asNumber(item.reservedQuantity),
    qualityHoldQuantity: asNumber(item.qualityHoldQuantity),
    earliestValidDate: timestampToDate(item.earliestValidDate),
    earliestValidTimestamp: asNumber(item.earliestValidDate),
    qaHoldBatchCount: asNumber(item.qaHoldBatchCount),
    nearExpiryBatchCount: asNumber(item.nearExpiryBatchCount),
    riskLevelCode,
    riskLevelLabel: batchRiskLevelLabel(riskLevelCode),
    riskCode: item.riskCode ?? "unknown",
    riskLabel: batchRiskLabel(item.riskCode),
    ownerDepartment: asNumber(item.ownerDepartment),
    ownerDepartmentLabel: batchDepartmentLabel(item.ownerDepartment),
    unitLabel,
    tone: batchRiskTone(riskLevelCode, riskCodes)
  };
}

function mapRelatedDocument(item: ApiBatchRelatedDocument): BatchRelatedDocument {
  return {
    refCategory: asNumber(item.refCategory),
    refCategoryLabel: batchRefCategoryLabel(item.refCategory),
    refNo: item.refNo ?? ""
  };
}

function mapDistributionRow(item: ApiBatchDistributionRow, index = 0): BatchDistributionRow {
  const riskLevelCode = normalizeBatchRiskLevel(item.riskLevelCode);
  const riskCodes = withFallbackArray<string>(item.riskCodes, []);
  const batchNo = item.batchNo ?? "";
  const warehouseNo = item.warehouseNo ?? "";
  const batchStageCode = item.batchStageCode ?? "unknown";

  return {
    rowKey: `${batchNo}|${warehouseNo}|${batchStageCode}|${index}`,
    batchNo,
    warehouseNo,
    warehouseName: item.warehouseName ?? "",
    locationCode: item.locationCode ?? "",
    palletCount: asNumber(item.palletCount),
    currentQuantity: asNumber(item.currentQuantity),
    availableQuantity: asNumber(item.availableQuantity),
    reservedQuantity: asNumber(item.reservedQuantity),
    qualityHoldQuantity: asNumber(item.qualityHoldQuantity),
    unit: asNumber(item.unit),
    unitLabel: batchUnitLabel(item.unit),
    validDate: timestampToDate(item.validDate),
    validTimestamp: asNumber(item.validDate),
    validDays: asNumber(item.validDays),
    qaStatusCode: item.qaStatusCode ?? "unknown",
    qaStatusLabel: batchQaStatusLabel(item.qaStatusCode),
    batchStageCode,
    batchStageLabel: batchStageLabel(batchStageCode),
    riskLevelCode,
    riskLevelLabel: batchRiskLevelLabel(riskLevelCode),
    riskCodes,
    riskLabels: riskCodes.length ? riskCodes.map(batchRiskLabel) : [batchRiskLabel(item.riskLevelCode)],
    refCategory: asNumber(item.refCategory),
    refCategoryLabel: batchRefCategoryLabel(item.refCategory),
    refNo: item.refNo ?? "",
    relatedDocuments: withFallbackArray<ApiBatchRelatedDocument>(item.relatedDocuments, []).map(mapRelatedDocument),
    tone: batchRiskTone(riskLevelCode, riskCodes)
  };
}

function mapDashboardPayload(payload: ApiBatchDashboardPayload): BatchDashboardData {
  const summary = normalizeSummary(payload.summary);
  const items = withFallbackArray<ApiBatchDashboardItem>(payload.items, []).map(mapDashboardItem);

  return {
    summary,
    kpis: kpisFromSummary(summary),
    items,
    total: payload.total ?? items.length,
    start: payload.start ?? 0,
    count: payload.count ?? items.length
  };
}

function mapDistributionPayload(payload: ApiBatchDistributionPayload): BatchDistributionData {
  const item = payload.item;
  const batches = withFallbackArray<ApiBatchDistributionRow>(payload.batches, []).map(mapDistributionRow);

  return {
    item: {
      itemNo: item?.itemNo ?? "",
      itemName: item?.itemName ?? "",
      itemCategory: asNumber(item?.itemCategory),
      itemCategoryLabel: batchItemCategoryLabel(item?.itemCategory),
      itemSubCategory: asNumber(item?.itemSubCategory),
      itemType: asNumber(item?.itemType),
      itemTypeLabel: batchItemTypeLabel(item?.itemType),
      unit: asNumber(item?.unit),
      unitLabel: batchUnitLabel(item?.unit)
    },
    batches,
    total: payload.total ?? batches.length,
    start: payload.start ?? 0,
    count: payload.count ?? batches.length
  };
}

function mapStockByWarehouse(item: ApiBatchDistributionRow, index: number): BatchStockByWarehouse {
  const row = mapDistributionRow(item, index);
  return {
    warehouseNo: row.warehouseNo,
    warehouseName: row.warehouseName,
    locationCode: row.locationCode,
    palletCount: row.palletCount,
    currentQuantity: row.currentQuantity,
    availableQuantity: row.availableQuantity,
    reservedQuantity: row.reservedQuantity,
    qualityHoldQuantity: row.qualityHoldQuantity,
    unit: row.unit,
    unitLabel: row.unitLabel,
    riskLevelCode: row.riskLevelCode,
    riskLevelLabel: row.riskLevelLabel,
    riskCodes: row.riskCodes,
    riskLabels: row.riskLabels,
    tone: row.tone
  };
}

function mapInventoryRecord(item: NonNullable<ApiBatchDetailPayload["inventoryRecords"]>[number]): BatchInventoryRecord {
  return {
    recordTime: timestampToDate(item.recordTime),
    refCategory: asNumber(item.refCategory),
    refCategoryLabel: batchRefCategoryLabel(item.refCategory),
    refNo: item.refNo ?? "",
    warehouseNo: item.warehouseNo ?? "",
    category: asNumber(item.category),
    categoryLabel: batchInventoryCategoryLabel(item.category),
    source: asNumber(item.source),
    sourceLabel: batchInventorySourceLabel(item.source),
    quantity: asNumber(item.quantity),
    unit: asNumber(item.unit),
    unitLabel: batchUnitLabel(item.unit),
    amount: asNumber(item.amount)
  };
}

function mapReservation(item: NonNullable<ApiBatchDetailPayload["reservations"]>[number]): BatchReservation {
  return {
    reservationNo: item.reservationNo ?? "",
    refCategory: asNumber(item.refCategory),
    refCategoryLabel: batchRefCategoryLabel(item.refCategory),
    refNo: item.refNo ?? "",
    warehouseNo: item.warehouseNo ?? "",
    reservedQuantity: asNumber(item.reservedQuantity),
    status: asNumber(item.status),
    statusLabel: batchReservationStatusLabel(item.status),
    expiryTimestamp: timestampToDate(item.expiryTimestamp)
  };
}

function mapQualityHold(item: NonNullable<ApiBatchDetailPayload["qualityHolds"]>[number]): BatchQualityHold {
  return {
    holdNo: item.holdNo ?? "",
    warehouseNo: item.warehouseNo ?? "",
    holdQuantity: asNumber(item.holdQuantity),
    status: asNumber(item.status),
    statusLabel: batchQualityHoldStatusLabel(item.status),
    reasonCode: item.reasonCode ?? "unknown",
    reasonLabel: batchQualityHoldReasonLabel(item.reasonCode),
    createdTimestamp: timestampToDate(item.createdTimestamp)
  };
}

function mapPalletMovement(item: NonNullable<ApiBatchDetailPayload["palletMovements"]>[number]) {
  return {
    movementNo: item.movementNo ?? "",
    warehouseNo: item.warehouseNo ?? "",
    palletNo: item.palletNo ?? "",
    palletCount: asNumber(item.palletCount),
    palletStatus: asNumber(item.palletStatus),
    palletStatusLabel: batchPalletStatusLabel(item.palletStatus),
    movementTimestamp: timestampToDate(item.movementTimestamp)
  };
}

function mapTask(item: NonNullable<ApiBatchDetailPayload["tasks"]>[number]): BatchTask {
  const taskStatus = asNumber(item.taskStatus);
  return {
    taskId: asNumber(item.taskId),
    taskType: asNumber(item.taskType),
    taskTypeLabel: batchTaskTypeLabel(item.taskType),
    taskStatus,
    taskStatusLabel: batchTaskStatusLabel(item.taskStatus),
    nextOwnerDepartment: asNumber(item.nextOwnerDepartment),
    nextOwnerDepartmentLabel: batchDepartmentLabel(item.nextOwnerDepartment),
    dueTimestamp: timestampToDate(item.dueTimestamp),
    refCategory: asNumber(item.refCategory),
    refCategoryLabel: batchRefCategoryLabel(item.refCategory),
    refNo: item.refNo ?? "",
    tone: batchTaskStatusTone(taskStatus)
  };
}

function mapDetailPayload(payload: ApiBatchDetailPayload): BatchDetail | undefined {
  const batch = payload.batch;
  if (!batch?.batchNo) {
    return undefined;
  }

  return {
    batch: {
      batchNo: batch.batchNo,
      itemNo: batch.itemNo ?? "",
      itemName: batch.itemName ?? "",
      itemCategory: asNumber(batch.itemCategory),
      itemCategoryLabel: batchItemCategoryLabel(batch.itemCategory),
      itemSubCategory: asNumber(batch.itemSubCategory),
      itemType: asNumber(batch.itemType),
      itemTypeLabel: batchItemTypeLabel(batch.itemType),
      unit: asNumber(batch.unit),
      unitLabel: batchUnitLabel(batch.unit),
      validDate: timestampToDate(batch.validDate),
      validTimestamp: asNumber(batch.validDate),
      validDays: asNumber(batch.validDays),
      refCategory: asNumber(batch.refCategory),
      refCategoryLabel: batchRefCategoryLabel(batch.refCategory),
      refNo: batch.refNo ?? "",
      creatorNo: batch.creatorNo ?? "",
      creationTime: timestampToDate(batch.creationTime)
    },
    stockByWarehouse: withFallbackArray<ApiBatchDistributionRow>(payload.stockByWarehouse, []).map(mapStockByWarehouse),
    inventoryRecords: withFallbackArray<NonNullable<ApiBatchDetailPayload["inventoryRecords"]>[number]>(
      payload.inventoryRecords,
      []
    ).map(mapInventoryRecord),
    reservations: withFallbackArray<NonNullable<ApiBatchDetailPayload["reservations"]>[number]>(
      payload.reservations,
      []
    ).map(mapReservation),
    qualityHolds: withFallbackArray<NonNullable<ApiBatchDetailPayload["qualityHolds"]>[number]>(
      payload.qualityHolds,
      []
    ).map(mapQualityHold),
    palletMovements: withFallbackArray<NonNullable<ApiBatchDetailPayload["palletMovements"]>[number]>(
      payload.palletMovements,
      []
    ).map(mapPalletMovement),
    tasks: withFallbackArray<NonNullable<ApiBatchDetailPayload["tasks"]>[number]>(payload.tasks, []).map(mapTask)
  };
}

function buildDashboardPath(query: BatchDashboardQuery) {
  const params = new URLSearchParams();
  Object.entries(query).forEach(([key, value]) => {
    if (value !== undefined && value !== "") {
      params.set(key, String(value));
    }
  });
  params.set("count", String(query.count ?? 50));
  return `/api/v2/batches/dashboard?${params.toString()}`;
}

function buildDistributionPath(itemNo: string, query: BatchDashboardQuery = {}) {
  const params = new URLSearchParams();
  if (query.keyword) {
    params.set("keyword", query.keyword);
  }
  if (query.warehouseNo) {
    params.set("warehouseNo", query.warehouseNo);
  }
  if (query.batchNo) {
    params.set("batchNo", query.batchNo);
  }
  if (query.riskLevelCode) {
    params.set("riskLevelCode", query.riskLevelCode);
  }
  if (query.qaStatusCode) {
    params.set("qaStatusCode", query.qaStatusCode);
  }
  if (query.batchStageCode) {
    params.set("batchStageCode", query.batchStageCode);
  }
  if (query.availabilityCode) {
    params.set("availabilityCode", query.availabilityCode);
  }
  params.set("start", String(query.start ?? 0));
  params.set("count", String(query.count ?? 50));
  return `/api/v2/batches/items/${encodeURIComponent(itemNo)}/distribution?${params.toString()}`;
}

export async function getBatchDashboard(
  query: BatchDashboardQuery = {},
  dataSourceMode: DataSourceMode = "api"
): Promise<BatchDashboardResult> {
  if (dataSourceMode === "mock") {
    return {
      data: batchesDashboardMock,
      source: "mock"
    };
  }

  try {
    const payload = await apiGet<ApiBatchDashboardPayload>(buildDashboardPath(query));
    return {
      data: mapDashboardPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: emptyBatchDashboardData,
      source: "api",
      error: error instanceof Error ? error.message : "批號中心資料取得失敗"
    };
  }
}

export async function getBatchDistribution(
  itemNo: string,
  query: BatchDashboardQuery = {},
  dataSourceMode: DataSourceMode = "api"
): Promise<BatchDistributionResult> {
  if (!itemNo) {
    return {
      data: emptyBatchDistributionData,
      source: dataSourceMode === "mock" ? "mock" : "api"
    };
  }

  if (dataSourceMode === "mock") {
    return {
      data: batchDistributionMock[itemNo] ?? { ...emptyBatchDistributionData, item: { ...emptyBatchDistributionData.item, itemNo } },
      source: "mock"
    };
  }

  try {
    const payload = await apiGet<ApiBatchDistributionPayload>(buildDistributionPath(itemNo, query));
    return {
      data: mapDistributionPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: { ...emptyBatchDistributionData, item: { ...emptyBatchDistributionData.item, itemNo } },
      source: "api",
      error: error instanceof Error ? error.message : "批號分布資料取得失敗"
    };
  }
}

export async function getBatchDetail(
  batchNo: string,
  dataSourceMode: DataSourceMode = "api"
): Promise<BatchDetailResult> {
  if (!batchNo) {
    return {
      source: dataSourceMode === "mock" ? "mock" : "api"
    };
  }

  if (dataSourceMode === "mock") {
    return {
      detail: batchDetailMock[batchNo],
      source: "mock"
    };
  }

  try {
    const payload = await apiGet<ApiBatchDetailPayload>(`/api/v2/batches/${encodeURIComponent(batchNo)}/detail`);
    return {
      detail: mapDetailPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      source: "api",
      error: error instanceof Error ? error.message : "批號追蹤明細取得失敗"
    };
  }
}
