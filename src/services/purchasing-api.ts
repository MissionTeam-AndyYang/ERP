import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { defaultLanguage } from "@/i18n/dictionary";
import {
  purchasingEnumLabel,
  purchasingRiskLevelLabel,
  purchasingRiskTone,
  purchasingStatusTone,
  purchasingUnitLabel
} from "@/i18n/purchasing-enums";
import { purchasingDashboardMock } from "@/mock/purchasing";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type {
  PurchaseDeliveryRiskItem,
  PurchaseOrderDetail,
  PurchaseOrderItem,
  PurchaseReceiptDetail,
  PurchaseReceiptItem,
  PurchaseSupplierItem,
  PurchaseWorkflowStep,
  PurchasingDashboardData,
  PurchasingDataSource,
  PurchasingRange,
  PurchasingSummary
} from "@/types/purchasing";

type ApiRange = Partial<PurchasingRange>;

type ApiPurchaseOrderSummary = {
  openPurchaseOrderCount?: number;
  lateOrDueTodayCount?: number;
  purchaseAmount?: number;
  unlinkedPurchaseRequestCount?: number;
};

type ApiDeliveryRiskSummary = {
  highRiskCount?: number;
  noticeCount?: number;
  lateCount?: number;
  affectedWorkOrderCount?: number;
  averageLateDays?: number;
};

type ApiReceiptSummary = {
  receiptCount?: number;
  pendingPutawayCount?: number;
};

type ApiPurchaseOrderItem = {
  purchaseOrderNo?: string;
  purchaseDateTimestamp?: number;
  itemNo?: string;
  itemName?: string;
  unit?: number;
  supplierNo?: string;
  supplierName?: string;
  orderedCount?: number;
  receivedCount?: number;
  openCount?: number;
  unitPrice?: number;
  purchaseAmount?: number;
  expectedArrivalTimestamp?: number;
  purchaseRequestNo?: string;
  purchaseRequestLinkStatusCode?: string;
  sourceOrderNo?: string;
  linkedWorkOrderNo?: string;
  warehouseStatusCode?: string;
  riskLevel?: number;
  riskType?: string;
};

type ApiDeliveryRiskItem = ApiPurchaseOrderItem & {
  shortageCount?: number;
  shortageValue?: number;
  impactSourceType?: string;
  impactSourceNo?: string;
  followUpCode?: string;
};

type ApiReceiptItem = {
  no?: string;
  purchaseOrderNo?: string;
  dateTimestamp?: number;
  category?: number;
  itemNo?: string;
  itemName?: string;
  expectedCount?: number;
  checkedCount?: number;
  receivedCount?: number;
  receivingStatusCode?: string;
  warehouseStatusCode?: string;
  nextOwnerDepartment?: number;
};

type ApiSupplierItem = {
  supplierNo?: string;
  supplierName?: string;
  purchaseOrderCount?: number;
  openPurchaseOrderCount?: number;
  latePurchaseOrderCount?: number;
  purchaseAmount?: number;
  pendingReceiptCount?: number;
  riskLevel?: number;
};

type ApiPagedResponse<TItem, TSummary = unknown> = {
  serverTimestamp?: number;
  timezone?: string;
  range?: ApiRange;
  summary?: TSummary;
  items?: TItem[];
  total?: number;
  start?: number;
  count?: number;
};

type ApiPurchaseOrderDetail = {
  serverTimestamp?: number;
  timezone?: string;
  purchaseOrder?: ApiPurchaseOrderItem & { comment?: string };
  purchaseRequest?: {
    purchaseRequestNo?: string;
    sourceOrderNo?: string;
    itemNo?: string;
    requestedCount?: number;
  } | null;
  supplier?: {
    supplierNo?: string;
    supplierName?: string;
  } | null;
  receipts?: (ApiReceiptItem & { checkedCount?: number })[];
  source?: {
    sourceOrderNo?: string;
    linkedWorkOrderNo?: string;
  };
  inventory?: {
    currentCount?: number;
    reservedCount?: number;
    availableCount?: number;
  };
  workflow?: {
    taskId?: string;
    taskType?: number;
    refCategory?: number;
    refNo?: string;
    taskStatus?: number;
    ownerDepartment?: number;
  }[];
  relatedDocuments?: {
    quoteNo?: string;
    contractNo?: string;
  };
};

export type PurchasingDashboardQuery = {
  startDate: string;
  endDate: string;
  supplierNo?: string;
  riskLevel?: number;
  keyword?: string;
  start?: number;
  count?: number;
};

export type PurchasingDashboardResult = {
  data: PurchasingDashboardData;
  source: PurchasingDataSource;
  error?: string;
};

export type PurchaseOrderDetailResult = {
  detail?: PurchaseOrderDetail;
  source: PurchasingDataSource;
  error?: string;
};

const locale = defaultLanguage;

export const emptyPurchasingDashboardData: PurchasingDashboardData = {
  range: { startDate: "", endDate: "" },
  summary: [
    { label: "未收採購單", value: "0", hint: "API 尚未提供資料", tone: "info" },
    { label: "交期風險", value: "0", hint: "API 尚未提供資料", tone: "info" },
    { label: "採購金額", value: "$0", hint: "API 尚未提供資料", tone: "info" },
    { label: "未連請購", value: "0", hint: "API 尚未提供資料", tone: "info" }
  ],
  purchaseOrders: [],
  deliveryRisks: [],
  receipts: [],
  suppliers: [],
  total: {
    purchaseOrders: 0,
    deliveryRisks: 0,
    receipts: 0,
    suppliers: 0
  }
};

function formatNumber(value?: number, maximumFractionDigits = 0) {
  return new Intl.NumberFormat(locale, { maximumFractionDigits }).format(value ?? 0);
}

function formatMoney(value?: number) {
  return `$${formatNumber(value, 0)}`;
}

function timestampToDate(value?: number) {
  if (!value) {
    return "";
  }
  return new Date(value * 1000).toLocaleDateString(locale, { timeZone: "Asia/Taipei" });
}

function asNumber(value?: number) {
  return Number.isFinite(value) ? Number(value) : 0;
}

function rangeFromResponses(...ranges: (ApiRange | undefined)[]): PurchasingRange {
  const range = ranges.find((item) => item?.startDate || item?.endDate);
  return {
    startDate: range?.startDate ?? "",
    endDate: range?.endDate ?? "",
    startTimestamp: range?.startTimestamp,
    endTimestamp: range?.endTimestamp
  };
}

function mapPurchaseOrderItem(item: ApiPurchaseOrderItem): PurchaseOrderItem {
  const riskLevel = item.riskLevel ?? 0;
  const warehouseStatusCode = item.warehouseStatusCode || "unknown";
  const purchaseRequestLinkStatusCode = item.purchaseRequestLinkStatusCode || "unlinked";
  const riskType = item.riskType || "unknown";
  const openCount = item.openCount ?? Math.max(asNumber(item.orderedCount) - asNumber(item.receivedCount), 0);

  return {
    id: item.purchaseOrderNo || `${item.itemNo ?? "PO"}-${item.expectedArrivalTimestamp ?? "unknown"}`,
    purchaseOrderNo: item.purchaseOrderNo ?? "",
    purchaseDate: timestampToDate(item.purchaseDateTimestamp),
    purchaseDateTimestamp: item.purchaseDateTimestamp,
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    unit: purchasingUnitLabel(item.unit, locale),
    unitCode: item.unit,
    supplierNo: item.supplierNo ?? "",
    supplierName: item.supplierName ?? "",
    orderedCount: asNumber(item.orderedCount),
    receivedCount: asNumber(item.receivedCount),
    openCount,
    unitPrice: asNumber(item.unitPrice),
    purchaseAmount: asNumber(item.purchaseAmount),
    expectedArrivalDate: timestampToDate(item.expectedArrivalTimestamp),
    expectedArrivalTimestamp: item.expectedArrivalTimestamp,
    purchaseRequestNo: item.purchaseRequestNo ?? "",
    purchaseRequestLinkStatusCode,
    purchaseRequestLinkStatus: purchasingEnumLabel("purchaseRequestLinkStatus", purchaseRequestLinkStatusCode, locale),
    sourceOrderNo: item.sourceOrderNo ?? "",
    linkedWorkOrderNo: item.linkedWorkOrderNo ?? "",
    warehouseStatusCode,
    warehouseStatus: purchasingEnumLabel("warehouseStatus", warehouseStatusCode, locale),
    riskLevelCode: riskLevel,
    riskLevel: purchasingRiskLevelLabel(riskLevel, locale),
    riskType,
    riskTypeLabel: purchasingEnumLabel("riskType", riskType, locale),
    tone: purchasingRiskTone(riskLevel)
  };
}

function mapDeliveryRiskItem(item: ApiDeliveryRiskItem): PurchaseDeliveryRiskItem {
  const base = mapPurchaseOrderItem({
    ...item,
    openCount: item.shortageCount ?? item.openCount
  });
  const impactSourceType = item.impactSourceType || "unknown";
  const followUpCode = item.followUpCode || "unknown";

  return {
    ...base,
    shortageCount: asNumber(item.shortageCount ?? base.openCount),
    shortageValue: asNumber(item.shortageValue),
    impactSourceType,
    impactSourceNo: item.impactSourceNo ?? "",
    impactSourceLabel: purchasingEnumLabel("impactSource", impactSourceType, locale),
    followUpCode,
    followUpLabel: purchasingEnumLabel("followUp", followUpCode, locale)
  };
}

function mapReceiptItem(item: ApiReceiptItem): PurchaseReceiptItem {
  const receivingStatusCode = item.receivingStatusCode || (item.category === 1 ? "returned" : "unknown");
  const warehouseStatusCode = item.warehouseStatusCode || "unknown";

  return {
    id: item.no || `${item.purchaseOrderNo ?? "GRN"}-${item.dateTimestamp ?? "unknown"}`,
    no: item.no ?? "",
    purchaseOrderNo: item.purchaseOrderNo ?? "",
    date: timestampToDate(item.dateTimestamp),
    dateTimestamp: item.dateTimestamp,
    category: item.category ?? 0,
    categoryLabel: purchasingEnumLabel("receiptCategory", item.category ?? 0, locale),
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    expectedCount: asNumber(item.expectedCount),
    checkedCount: asNumber(item.checkedCount),
    receivedCount: asNumber(item.receivedCount),
    receivingStatusCode,
    receivingStatus: purchasingEnumLabel("receivingStatus", receivingStatusCode, locale),
    warehouseStatusCode,
    warehouseStatus: purchasingEnumLabel("warehouseStatus", warehouseStatusCode, locale),
    nextOwnerDepartment: item.nextOwnerDepartment,
    nextOwnerDepartmentLabel: purchasingEnumLabel("department", item.nextOwnerDepartment ?? 0, locale)
  };
}

function mapSupplierItem(item: ApiSupplierItem): PurchaseSupplierItem {
  const riskLevel = item.riskLevel ?? 0;
  return {
    id: item.supplierNo || item.supplierName || "supplier",
    supplierNo: item.supplierNo ?? "",
    supplierName: item.supplierName ?? "",
    purchaseOrderCount: asNumber(item.purchaseOrderCount),
    openPurchaseOrderCount: asNumber(item.openPurchaseOrderCount),
    latePurchaseOrderCount: asNumber(item.latePurchaseOrderCount),
    purchaseAmount: asNumber(item.purchaseAmount),
    pendingReceiptCount: asNumber(item.pendingReceiptCount),
    riskLevelCode: riskLevel,
    riskLevel: purchasingRiskLevelLabel(riskLevel, locale),
    tone: purchasingRiskTone(riskLevel)
  };
}

function mapSummary(
  purchaseOrderSummary?: ApiPurchaseOrderSummary,
  deliveryRiskSummary?: ApiDeliveryRiskSummary,
  receiptSummary?: ApiReceiptSummary
): PurchasingSummary[] {
  return [
    {
      label: "未收採購單",
      value: formatNumber(purchaseOrderSummary?.openPurchaseOrderCount),
      hint: `到期或逾期 ${formatNumber(purchaseOrderSummary?.lateOrDueTodayCount)} 筆`,
      tone: purchaseOrderSummary?.lateOrDueTodayCount ? "warning" : "success"
    },
    {
      label: "交期風險",
      value: `${formatNumber(deliveryRiskSummary?.highRiskCount)} / ${formatNumber(deliveryRiskSummary?.noticeCount)}`,
      hint: `逾期 ${formatNumber(deliveryRiskSummary?.lateCount)} 筆，影響工單 ${formatNumber(
        deliveryRiskSummary?.affectedWorkOrderCount
      )} 筆`,
      tone: deliveryRiskSummary?.highRiskCount ? "danger" : deliveryRiskSummary?.noticeCount ? "warning" : "success"
    },
    {
      label: "採購金額",
      value: formatMoney(purchaseOrderSummary?.purchaseAmount),
      hint: `查詢期間進貨單 ${formatNumber(receiptSummary?.receiptCount)} 筆`,
      tone: "info"
    },
    {
      label: "未連請購",
      value: formatNumber(purchaseOrderSummary?.unlinkedPurchaseRequestCount),
      hint: `待入庫交接 ${formatNumber(receiptSummary?.pendingPutawayCount)} 筆`,
      tone: purchaseOrderSummary?.unlinkedPurchaseRequestCount ? "warning" : "success"
    }
  ];
}

function mapDashboardPayload(
  purchaseOrdersPayload: ApiPagedResponse<ApiPurchaseOrderItem, ApiPurchaseOrderSummary>,
  risksPayload: ApiPagedResponse<ApiDeliveryRiskItem, ApiDeliveryRiskSummary>,
  receiptsPayload: ApiPagedResponse<ApiReceiptItem, ApiReceiptSummary>,
  suppliersPayload: ApiPagedResponse<ApiSupplierItem>
): PurchasingDashboardData {
  return {
    range: rangeFromResponses(
      purchaseOrdersPayload.range,
      risksPayload.range,
      receiptsPayload.range,
      suppliersPayload.range
    ),
    summary: mapSummary(purchaseOrdersPayload.summary, risksPayload.summary, receiptsPayload.summary),
    purchaseOrders: withFallbackArray(purchaseOrdersPayload.items, []).map(mapPurchaseOrderItem),
    deliveryRisks: withFallbackArray(risksPayload.items, []).map(mapDeliveryRiskItem),
    receipts: withFallbackArray(receiptsPayload.items, []).map(mapReceiptItem),
    suppliers: withFallbackArray(suppliersPayload.items, []).map(mapSupplierItem),
    total: {
      purchaseOrders: purchaseOrdersPayload.total ?? purchaseOrdersPayload.items?.length ?? 0,
      deliveryRisks: risksPayload.total ?? risksPayload.items?.length ?? 0,
      receipts: receiptsPayload.total ?? receiptsPayload.items?.length ?? 0,
      suppliers: suppliersPayload.total ?? suppliersPayload.items?.length ?? 0
    }
  };
}

export function normalizePurchasingDashboardData(data: PurchasingDashboardData): PurchasingDashboardData {
  return data;
}

function buildQueryPath(path: string, query: PurchasingDashboardQuery) {
  const params = new URLSearchParams();
  params.set("startDate", query.startDate);
  params.set("endDate", query.endDate);
  if (query.supplierNo) {
    params.set("supplierNo", query.supplierNo);
  }
  if (query.riskLevel !== undefined) {
    params.set("riskLevel", String(query.riskLevel));
  }
  if (query.keyword) {
    params.set("keyword", query.keyword);
  }
  if (query.start !== undefined) {
    params.set("start", String(query.start));
  }
  params.set("count", String(query.count ?? 50));
  return `${path}?${params.toString()}`;
}

export async function getPurchasingDashboard(
  query: PurchasingDashboardQuery,
  dataSourceMode: DataSourceMode = "api"
): Promise<PurchasingDashboardResult> {
  if (dataSourceMode === "mock") {
    return {
      data: normalizePurchasingDashboardData(purchasingDashboardMock),
      source: "mock"
    };
  }

  try {
    const [purchaseOrdersPayload, risksPayload, receiptsPayload, suppliersPayload] = await Promise.all([
      apiGet<ApiPagedResponse<ApiPurchaseOrderItem, ApiPurchaseOrderSummary>>(
        buildQueryPath("/api/v2/purchasing/purchase-orders/dashboard", query)
      ),
      apiGet<ApiPagedResponse<ApiDeliveryRiskItem, ApiDeliveryRiskSummary>>(
        buildQueryPath("/api/v2/purchasing/purchase-orders/delivery-risk", query)
      ),
      apiGet<ApiPagedResponse<ApiReceiptItem, ApiReceiptSummary>>(
        buildQueryPath("/api/v2/purchasing/goods-receipts/dashboard", query)
      ),
      apiGet<ApiPagedResponse<ApiSupplierItem>>(buildQueryPath("/api/v2/purchasing/suppliers/dashboard", query))
    ]);

    return {
      data: mapDashboardPayload(purchaseOrdersPayload, risksPayload, receiptsPayload, suppliersPayload),
      source: "api"
    };
  } catch (error) {
    return {
      data: emptyPurchasingDashboardData,
      source: "api",
      error: error instanceof Error ? error.message : "Purchasing API unavailable"
    };
  }
}

function mapReceiptDetail(item: ApiReceiptItem): PurchaseReceiptDetail {
  const receipt = mapReceiptItem(item);
  return {
    no: receipt.no,
    date: receipt.date,
    categoryLabel: receipt.categoryLabel,
    expectedCount: receipt.expectedCount,
    checkedCount: receipt.checkedCount,
    receivedCount: receipt.receivedCount,
    receivingStatus: receipt.receivingStatus,
    warehouseStatus: receipt.warehouseStatus
  };
}

function mapWorkflowStep(item: NonNullable<ApiPurchaseOrderDetail["workflow"]>[number]): PurchaseWorkflowStep {
  const taskStatus = item.taskStatus ?? 1;
  return {
    taskId: item.taskId ?? "",
    taskTypeLabel: purchasingEnumLabel("taskType", item.taskType ?? 0, locale),
    refNo: item.refNo ?? "",
    taskStatusLabel: purchasingEnumLabel("taskStatus", taskStatus, locale),
    ownerDepartmentLabel: purchasingEnumLabel("department", item.ownerDepartment ?? 0, locale),
    tone: purchasingStatusTone(taskStatus)
  };
}

function mapPurchaseOrderDetail(payload: ApiPurchaseOrderDetail): PurchaseOrderDetail | undefined {
  if (!payload.purchaseOrder?.purchaseOrderNo) {
    return undefined;
  }

  const purchaseOrder = mapPurchaseOrderItem(payload.purchaseOrder);

  return {
    purchaseOrderNo: purchaseOrder.purchaseOrderNo,
    purchaseDate: purchaseOrder.purchaseDate,
    itemNo: purchaseOrder.itemNo,
    itemName: purchaseOrder.itemName,
    unit: purchaseOrder.unit,
    supplierName: payload.supplier?.supplierName ?? purchaseOrder.supplierName,
    orderedCount: purchaseOrder.orderedCount,
    unitPrice: purchaseOrder.unitPrice,
    purchaseAmount: purchaseOrder.purchaseAmount,
    expectedArrivalDate: purchaseOrder.expectedArrivalDate,
    comment: payload.purchaseOrder.comment ?? "",
    purchaseRequestNo: payload.purchaseRequest?.purchaseRequestNo ?? purchaseOrder.purchaseRequestNo,
    sourceOrderNo: payload.source?.sourceOrderNo ?? payload.purchaseRequest?.sourceOrderNo ?? purchaseOrder.sourceOrderNo,
    linkedWorkOrderNo: payload.source?.linkedWorkOrderNo ?? purchaseOrder.linkedWorkOrderNo,
    inventory: {
      currentCount: asNumber(payload.inventory?.currentCount),
      reservedCount: asNumber(payload.inventory?.reservedCount),
      availableCount: asNumber(payload.inventory?.availableCount)
    },
    receipts: withFallbackArray(payload.receipts, []).map(mapReceiptDetail),
    workflow: withFallbackArray(payload.workflow, []).map(mapWorkflowStep),
    relatedDocuments: {
      quoteNo: payload.relatedDocuments?.quoteNo ?? "",
      contractNo: payload.relatedDocuments?.contractNo ?? ""
    }
  };
}

export async function getPurchaseOrderDetail(
  purchaseOrderNo: string,
  fallback?: PurchaseOrderItem,
  dataSourceMode: DataSourceMode = "api"
): Promise<PurchaseOrderDetailResult> {
  if (dataSourceMode === "mock") {
    return {
      detail: purchasingDashboardMock.details[purchaseOrderNo],
      source: "mock"
    };
  }

  try {
    const payload = await apiGet<ApiPurchaseOrderDetail>(
      `/api/v2/purchasing/purchase-orders/${encodeURIComponent(purchaseOrderNo)}/detail`
    );
    return {
      detail: mapPurchaseOrderDetail(payload),
      source: "api"
    };
  } catch (error) {
    return {
      detail: fallback
        ? {
            purchaseOrderNo: fallback.purchaseOrderNo,
            purchaseDate: fallback.purchaseDate,
            itemNo: fallback.itemNo,
            itemName: fallback.itemName,
            unit: fallback.unit,
            supplierName: fallback.supplierName,
            orderedCount: fallback.orderedCount,
            unitPrice: fallback.unitPrice,
            purchaseAmount: fallback.purchaseAmount,
            expectedArrivalDate: fallback.expectedArrivalDate,
            comment: "",
            purchaseRequestNo: fallback.purchaseRequestNo,
            sourceOrderNo: fallback.sourceOrderNo,
            linkedWorkOrderNo: fallback.linkedWorkOrderNo,
            inventory: { currentCount: 0, reservedCount: 0, availableCount: 0 },
            receipts: [],
            workflow: [],
            relatedDocuments: { quoteNo: "", contractNo: "" }
          }
        : undefined,
      source: "api",
      error: error instanceof Error ? error.message : "Purchasing purchase order detail API unavailable"
    };
  }
}
