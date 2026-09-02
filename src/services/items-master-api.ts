import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { warehouseEnumLabel } from "@/i18n/warehouse-enums";
import { itemAndTransactionMasterMock } from "@/mock/items-master";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { StatusTone } from "@/types/dashboard";
import type {
  CompanyMasterRow,
  ItemAndTransactionMasterData,
  ItemCategorySummary,
  ItemsMasterDataSource,
  MaintenanceSuggestionRow,
  MaterialItemMasterRow,
  PaymentSummary,
  TransactionItemMasterRow
} from "@/types/items-master";

type ApiItemSummary = {
  totalItemCount?: number;
  activeItemCount?: number;
  finishedGoodsCount?: number;
  maintenanceItemCount?: number;
};

type ApiItemCategorySummary = {
  itemCategory?: number;
  itemCount?: number;
  stockItemCount?: number;
  bomLinkedItemCount?: number;
  maintenanceItemCount?: number;
};

type ApiItemRow = {
  itemNo?: string;
  itemName?: string;
  itemCategory?: number;
  itemSubCategory?: number;
  unitWarehouse?: number;
  unitProduct?: number;
  masterStatusCode?: string;
  maintenanceRiskCode?: string;
  hasStock?: boolean;
  currentQuantity?: number;
  batchCount?: number;
  bomCount?: number;
};

type ApiMaintenanceSuggestion = {
  suggestionId?: string;
  itemNo?: string;
  suggestionTypeCode?: string;
  riskLevelCode?: string;
};

type ApiItemsDashboardPayload = {
  summary?: ApiItemSummary;
  categorySummary?: ApiItemCategorySummary[];
  items?: ApiItemRow[];
  maintenanceSuggestions?: ApiMaintenanceSuggestion[];
  total?: number;
  start?: number;
  count?: number;
};

type ApiPayment = {
  paymentTypeCode?: string;
  paymentDate?: number;
  paymentPeriod?: number;
  paymentSource?: number;
};

type ApiCompanyRow = {
  companyNo?: string;
  companyDisplayName?: string;
  companyName?: string;
  businessNo?: string;
  transItemCount?: number;
  contractCount?: number;
  contactName?: string;
  contactPhone?: string;
  receivablePayment?: ApiPayment;
  payablePayment?: ApiPayment;
  dataQualityCode?: string;
};

type ApiTransactionItemRow = {
  transItemNo?: string;
  transItemName?: string;
  transItemType?: string;
  transItemCategory?: number;
  transItemAttribute?: number;
  companyNo?: string;
  companyDisplayName?: string;
  itemNo?: string;
  itemName?: string;
  itemCategory?: number;
  contractNo?: string;
  contractCategory?: number;
  contractType?: number;
  tradeUnit?: number;
  tradePrice?: number;
  shippingPrice?: number;
  unitConversion?: number;
  dataQualityCode?: string;
};

type ApiTransItemsDashboardPayload = {
  summary?: {
    companyCount?: number;
    customerCount?: number;
    supplierCount?: number;
    transItemCount?: number;
    linkedItemCount?: number;
    contractLinkedTransItemCount?: number;
    companyDataQualityIssueCount?: number;
    transItemDataQualityIssueCount?: number;
  };
  companies?: ApiCompanyRow[];
  transactionItems?: ApiTransactionItemRow[];
  total?: number;
  start?: number;
  count?: number;
};

export type ItemAndTransactionMasterQuery = {
  keyword?: string;
  start?: number;
  count?: number;
};

export type ItemAndTransactionMasterResult = {
  data: ItemAndTransactionMasterData;
  source: ItemsMasterDataSource;
  error?: string;
};

export const emptyItemAndTransactionMasterData: ItemAndTransactionMasterData = {
  summary: {
    totalItemCount: 0,
    activeItemCount: 0,
    finishedGoodsCount: 0,
    maintenanceItemCount: 0,
    companyCount: 0,
    transItemCount: 0,
    linkedItemCount: 0,
    contractLinkedTransItemCount: 0,
    companyDataQualityIssueCount: 0,
    transItemDataQualityIssueCount: 0
  },
  categorySummary: [],
  items: [],
  maintenanceSuggestions: [],
  companies: [],
  transactionItems: [],
  totalItems: 0,
  totalTransactionItems: 0,
  start: 0,
  count: 0
};

const locale = "zh-TW";

function asNumber(value?: number) {
  return Number.isFinite(value) ? Number(value) : 0;
}

function formatPath(path: string, query: ItemAndTransactionMasterQuery = {}) {
  const params = new URLSearchParams();
  if (query.keyword) {
    params.set("keyword", query.keyword);
  }
  params.set("start", String(query.start ?? 0));
  params.set("count", String(query.count ?? 50));
  return `${path}?${params.toString()}`;
}

function statusTone(code?: string): StatusTone {
  if (code === "ready" || code === "normal") {
    return "success";
  }
  if (code === "high_risk") {
    return "danger";
  }
  if (code === "maintenance_needed" || code?.startsWith("missing")) {
    return "warning";
  }
  return "neutral";
}

function itemStatusLabel(code?: string) {
  if (code === "ready") {
    return "可使用";
  }
  if (code === "maintenance_needed") {
    return "待維護";
  }
  return "未確認";
}

function maintenanceRiskLabel(code?: string) {
  const labels: Record<string, string> = {
    normal: "資料完整",
    missing_unit: "缺少單位設定",
    missing_bom: "缺少 BOM 關聯",
    missing_stock_signal: "缺少庫存訊號",
    unknown: "未確認"
  };
  return labels[code ?? "unknown"] ?? "待確認";
}

function dataQualityLabel(code?: string) {
  const labels: Record<string, string> = {
    ready: "資料完整",
    missing_linked_item: "未關聯料品",
    missing_payment: "帳款條件待補",
    missing_contact: "聯絡資訊待補",
    unknown: "未確認"
  };
  return labels[code ?? "unknown"] ?? "待確認";
}

function suggestionLabel(code?: string) {
  return maintenanceRiskLabel(code);
}

function riskLevelLabel(code?: string) {
  if (code === "high_risk") {
    return "高風險";
  }
  if (code === "attention") {
    return "注意";
  }
  if (code === "normal") {
    return "正常";
  }
  return "未分級";
}

function paymentTypeLabel(code?: string) {
  if (code === "monthly") {
    return "月結";
  }
  if (code === "cash") {
    return "現結";
  }
  return "未設定";
}

function paymentSourceLabel(code?: number) {
  if (code === 1) {
    return "匯款";
  }
  if (code === 2) {
    return "支票";
  }
  return "現金";
}

function transItemTypeLabel(code?: string) {
  return code === "trans_items" ? "交易品項" : "交易品項";
}

function transItemCategoryLabel(code?: number) {
  if (code === 1) {
    return "採購品項";
  }
  if (code === 2) {
    return "訂購品項";
  }
  return "其他";
}

function contractCategoryLabel(code?: number) {
  if (code === 1) {
    return "採購合約";
  }
  if (code === 2) {
    return "訂購合約";
  }
  return "未關聯合約";
}

function unitLabel(code?: number) {
  return warehouseEnumLabel("unit", code, locale);
}

function itemCategoryLabel(code?: number) {
  return warehouseEnumLabel("itemCategory", code, locale);
}

function mapCategorySummary(item: ApiItemCategorySummary): ItemCategorySummary {
  return {
    itemCategory: asNumber(item.itemCategory),
    itemCategoryLabel: itemCategoryLabel(item.itemCategory),
    itemCount: asNumber(item.itemCount),
    stockItemCount: asNumber(item.stockItemCount),
    bomLinkedItemCount: asNumber(item.bomLinkedItemCount),
    maintenanceItemCount: asNumber(item.maintenanceItemCount)
  };
}

function mapItem(item: ApiItemRow): MaterialItemMasterRow {
  const masterStatusCode = item.masterStatusCode ?? "unknown";
  const maintenanceRiskCode = item.maintenanceRiskCode ?? "unknown";
  return {
    id: item.itemNo ?? "item",
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    itemCategory: asNumber(item.itemCategory),
    itemCategoryLabel: itemCategoryLabel(item.itemCategory),
    itemSubCategory: asNumber(item.itemSubCategory),
    unitWarehouse: asNumber(item.unitWarehouse),
    unitWarehouseLabel: unitLabel(item.unitWarehouse),
    unitProduct: asNumber(item.unitProduct),
    unitProductLabel: unitLabel(item.unitProduct),
    masterStatusCode,
    masterStatusLabel: itemStatusLabel(masterStatusCode),
    maintenanceRiskCode,
    maintenanceRiskLabel: maintenanceRiskLabel(maintenanceRiskCode),
    hasStock: item.hasStock === true,
    currentQuantity: asNumber(item.currentQuantity),
    batchCount: asNumber(item.batchCount),
    bomCount: asNumber(item.bomCount),
    tone: statusTone(masterStatusCode === "ready" ? "ready" : maintenanceRiskCode)
  };
}

function mapSuggestion(item: ApiMaintenanceSuggestion): MaintenanceSuggestionRow {
  const suggestionTypeCode = item.suggestionTypeCode ?? "unknown";
  const riskLevelCode = item.riskLevelCode ?? "unknown";
  return {
    suggestionId: item.suggestionId ?? `${item.itemNo ?? "item"}-${suggestionTypeCode}`,
    itemNo: item.itemNo ?? "",
    suggestionTypeCode,
    suggestionTypeLabel: suggestionLabel(suggestionTypeCode),
    riskLevelCode,
    riskLevelLabel: riskLevelLabel(riskLevelCode),
    tone: statusTone(riskLevelCode)
  };
}

function mapPayment(item?: ApiPayment): PaymentSummary {
  const paymentTypeCode = item?.paymentTypeCode ?? "unknown";
  return {
    paymentTypeCode,
    paymentTypeLabel: paymentTypeLabel(paymentTypeCode),
    paymentDate: asNumber(item?.paymentDate),
    paymentPeriod: asNumber(item?.paymentPeriod),
    paymentSource: asNumber(item?.paymentSource),
    paymentSourceLabel: paymentSourceLabel(item?.paymentSource)
  };
}

function mapCompany(item: ApiCompanyRow): CompanyMasterRow {
  const dataQualityCode = item.dataQualityCode ?? "unknown";
  return {
    id: item.companyNo ?? "company",
    companyNo: item.companyNo ?? "",
    companyDisplayName: item.companyDisplayName ?? "",
    companyName: item.companyName ?? "",
    businessNo: item.businessNo ?? "",
    transItemCount: asNumber(item.transItemCount),
    contractCount: asNumber(item.contractCount),
    contactName: item.contactName ?? "",
    contactPhone: item.contactPhone ?? "",
    receivablePayment: mapPayment(item.receivablePayment),
    payablePayment: mapPayment(item.payablePayment),
    dataQualityCode,
    dataQualityLabel: dataQualityLabel(dataQualityCode),
    tone: statusTone(dataQualityCode)
  };
}

function mapTransactionItem(item: ApiTransactionItemRow): TransactionItemMasterRow {
  const dataQualityCode = item.dataQualityCode ?? "unknown";
  return {
    id: item.transItemNo ?? "trans-item",
    transItemNo: item.transItemNo ?? "",
    transItemName: item.transItemName ?? "",
    transItemType: item.transItemType ?? "trans_items",
    transItemTypeLabel: transItemTypeLabel(item.transItemType),
    transItemCategory: asNumber(item.transItemCategory),
    transItemCategoryLabel: transItemCategoryLabel(item.transItemCategory),
    transItemAttribute: asNumber(item.transItemAttribute),
    companyNo: item.companyNo ?? "",
    companyDisplayName: item.companyDisplayName ?? "",
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    itemCategory: asNumber(item.itemCategory),
    itemCategoryLabel: itemCategoryLabel(item.itemCategory),
    contractNo: item.contractNo ?? "",
    contractCategory: asNumber(item.contractCategory),
    contractCategoryLabel: contractCategoryLabel(item.contractCategory),
    contractType: asNumber(item.contractType),
    tradeUnit: asNumber(item.tradeUnit),
    tradeUnitLabel: unitLabel(item.tradeUnit),
    tradePrice: asNumber(item.tradePrice),
    shippingPrice: asNumber(item.shippingPrice),
    unitConversion: asNumber(item.unitConversion),
    dataQualityCode,
    dataQualityLabel: dataQualityLabel(dataQualityCode),
    tone: statusTone(dataQualityCode)
  };
}

function mapDashboardPayload(
  itemsPayload: ApiItemsDashboardPayload,
  transItemsPayload: ApiTransItemsDashboardPayload
): ItemAndTransactionMasterData {
  const itemSummary = itemsPayload.summary ?? {};
  const transSummary = transItemsPayload.summary ?? {};
  const items = withFallbackArray<ApiItemRow>(itemsPayload.items, []).map(mapItem);
  const transactionItems = withFallbackArray<ApiTransactionItemRow>(transItemsPayload.transactionItems, []).map(mapTransactionItem);

  return {
    summary: {
      totalItemCount: asNumber(itemSummary.totalItemCount),
      activeItemCount: asNumber(itemSummary.activeItemCount),
      finishedGoodsCount: asNumber(itemSummary.finishedGoodsCount),
      maintenanceItemCount: asNumber(itemSummary.maintenanceItemCount),
      companyCount: asNumber(transSummary.companyCount),
      transItemCount: asNumber(transSummary.transItemCount),
      linkedItemCount: asNumber(transSummary.linkedItemCount),
      contractLinkedTransItemCount: asNumber(transSummary.contractLinkedTransItemCount),
      companyDataQualityIssueCount: asNumber(transSummary.companyDataQualityIssueCount),
      transItemDataQualityIssueCount: asNumber(transSummary.transItemDataQualityIssueCount)
    },
    categorySummary: withFallbackArray<ApiItemCategorySummary>(itemsPayload.categorySummary, []).map(mapCategorySummary),
    items,
    maintenanceSuggestions: withFallbackArray<ApiMaintenanceSuggestion>(
      itemsPayload.maintenanceSuggestions,
      []
    ).map(mapSuggestion),
    companies: withFallbackArray<ApiCompanyRow>(transItemsPayload.companies, []).map(mapCompany),
    transactionItems,
    totalItems: itemsPayload.total ?? items.length,
    totalTransactionItems: transItemsPayload.total ?? transactionItems.length,
    start: transItemsPayload.start ?? itemsPayload.start ?? 0,
    count: transItemsPayload.count ?? itemsPayload.count ?? transactionItems.length
  };
}

export async function getItemAndTransactionMasterDashboard(
  query: ItemAndTransactionMasterQuery = {},
  dataSourceMode: DataSourceMode = "api"
): Promise<ItemAndTransactionMasterResult> {
  if (dataSourceMode === "mock") {
    return {
      data: itemAndTransactionMasterMock,
      source: "mock"
    };
  }

  try {
    const [itemsPayload, transItemsPayload] = await Promise.all([
      apiGet<ApiItemsDashboardPayload>(formatPath("/api/v2/items/dashboard", query)),
      apiGet<ApiTransItemsDashboardPayload>(formatPath("/api/v2/transitems/dashboard", query))
    ]);
    return {
      data: mapDashboardPayload(itemsPayload, transItemsPayload),
      source: "api"
    };
  } catch (error) {
    return {
      data: emptyItemAndTransactionMasterData,
      source: "api",
      error: error instanceof Error ? error.message : "品項與交易主資料 API 取得失敗"
    };
  }
}
