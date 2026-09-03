import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { warehouseEnumLabel } from "@/i18n/warehouse-enums";
import { itemAndTransactionMasterMock } from "@/mock/items-master";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { StatusTone } from "@/types/dashboard";
import type {
  CompanyMasterRow,
  CompanyDetail,
  ContractSummaryRow,
  ItemBomUsageRow,
  ItemAndTransactionMasterData,
  ItemCategorySummary,
  ItemInventorySummary,
  ItemMasterDetailData,
  ItemMasterDetailTarget,
  ItemRecentBatchRow,
  ItemsMasterDataSource,
  LinkedMaterialItemRow,
  MaintenanceSuggestionRow,
  MaterialItemDetail,
  MaterialItemMasterRow,
  PaymentSummary,
  TransactionItemDetail,
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

type ApiItemInventorySummary = {
  hasStock?: boolean;
  currentQuantity?: number;
  availableQuantity?: number;
  reservedQuantity?: number;
  qualityHoldQuantity?: number;
  warehouseCount?: number;
  batchCount?: number;
};

type ApiItemBomUsageRow = {
  bomNo?: string;
  bomVersion?: number;
  quantity?: number;
  unit?: number;
  effectiveTimestamp?: number;
};

type ApiItemRecentBatchRow = {
  batchNo?: string;
  refCategory?: number;
  refNo?: string;
  currentQuantity?: number;
  unit?: number;
  validDate?: number;
  riskLevelCode?: string;
};

type ApiItemDetailPayload = {
  serverTimestamp?: number;
  item?: ApiItemRow & {
    creationTime?: number;
  };
  inventorySummary?: ApiItemInventorySummary;
  bomUsage?: ApiItemBomUsageRow[];
  recentBatches?: ApiItemRecentBatchRow[];
  maintenanceSuggestions?: ApiMaintenanceSuggestion[];
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

type ApiCompanyDetailRow = ApiCompanyRow & {
  address?: string;
  phone?: string;
  contactTitle?: string;
  contactEmail?: string;
};

type ApiCompanyTransactionItemRow = {
  transItemNo?: string;
  transItemName?: string;
  transItemType?: string;
  transItemCategory?: number;
  transItemAttribute?: number;
  itemNo?: string;
  itemName?: string;
  contractNo?: string;
  tradeUnit?: number;
  tradePrice?: number;
  dataQualityCode?: string;
};

type ApiContractRow = {
  contractNo?: string;
  contractDisplayName?: string;
  contractCategory?: number;
  contractType?: number;
  tradeUnit?: number;
  tradePrice?: number;
  shippingPrice?: number;
  unitConversion?: number;
  effectiveDate?: number;
  transItemNo?: string;
  transItemName?: string;
};

type ApiCompanyDetailPayload = {
  serverTimestamp?: number;
  company?: ApiCompanyDetailRow;
  transactionItems?: ApiCompanyTransactionItemRow[];
  contracts?: ApiContractRow[];
};

type ApiTransactionItemDetailPayload = {
  serverTimestamp?: number;
  transItem?: ApiTransactionItemRow & {
    comment?: string;
    creationTime?: number;
  };
  contracts?: ApiContractRow[];
  linkedItems?: {
    itemNo?: string;
    itemName?: string;
    itemCategory?: number;
    unitWarehouse?: number;
  }[];
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

export type ItemMasterDetailResult = {
  data?: ItemMasterDetailData;
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

function timestampToDate(value?: number) {
  const timestamp = asNumber(value);
  if (!timestamp) {
    return "";
  }
  return new Intl.DateTimeFormat(locale, {
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  }).format(new Date(timestamp * 1000));
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
    missing_payment_terms: "帳款條件待補",
    missing_contact: "聯絡資訊待補",
    missing_company: "未關聯公司",
    missing_contract_price: "合約價格待補",
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

function mapItemInventorySummary(item?: ApiItemInventorySummary): ItemInventorySummary {
  return {
    hasStock: item?.hasStock === true,
    currentQuantity: asNumber(item?.currentQuantity),
    availableQuantity: asNumber(item?.availableQuantity),
    reservedQuantity: asNumber(item?.reservedQuantity),
    qualityHoldQuantity: asNumber(item?.qualityHoldQuantity),
    warehouseCount: asNumber(item?.warehouseCount),
    batchCount: asNumber(item?.batchCount)
  };
}

function mapBomUsage(item: ApiItemBomUsageRow): ItemBomUsageRow {
  const unit = asNumber(item.unit);
  const bomVersion = asNumber(item.bomVersion);
  const quantity = asNumber(item.quantity);
  return {
    id: `${item.bomNo ?? "bom"}-${bomVersion}-${unit}-${quantity}`,
    bomNo: item.bomNo ?? "",
    bomVersion,
    quantity,
    unit,
    unitLabel: unitLabel(unit),
    effectiveDate: timestampToDate(item.effectiveTimestamp)
  };
}

function refCategoryLabel(code?: number) {
  return warehouseEnumLabel("refCategory", code, locale);
}

function mapRecentBatch(item: ApiItemRecentBatchRow): ItemRecentBatchRow {
  const riskLevelCode = item.riskLevelCode ?? "unknown";
  const unit = asNumber(item.unit);
  return {
    id: item.batchNo ?? "batch",
    batchNo: item.batchNo ?? "",
    refCategory: asNumber(item.refCategory),
    refCategoryLabel: refCategoryLabel(item.refCategory),
    refNo: item.refNo ?? "",
    currentQuantity: asNumber(item.currentQuantity),
    unit,
    unitLabel: unitLabel(unit),
    validDate: timestampToDate(item.validDate),
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

function mapCompanyTransactionItem(item: ApiCompanyTransactionItemRow, company?: CompanyMasterRow): TransactionItemMasterRow {
  const dataQualityCode = item.dataQualityCode ?? "unknown";
  const tradeUnit = asNumber(item.tradeUnit);
  return {
    id: item.transItemNo ?? "trans-item",
    transItemNo: item.transItemNo ?? "",
    transItemName: item.transItemName ?? "",
    transItemType: item.transItemType ?? "trans_items",
    transItemTypeLabel: transItemTypeLabel(item.transItemType),
    transItemCategory: asNumber(item.transItemCategory),
    transItemCategoryLabel: transItemCategoryLabel(item.transItemCategory),
    transItemAttribute: asNumber(item.transItemAttribute),
    companyNo: company?.companyNo ?? "",
    companyDisplayName: company?.companyDisplayName ?? "",
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    itemCategory: 0,
    itemCategoryLabel: itemCategoryLabel(0),
    contractNo: item.contractNo ?? "",
    contractCategory: 0,
    contractCategoryLabel: contractCategoryLabel(0),
    contractType: 0,
    tradeUnit,
    tradeUnitLabel: unitLabel(tradeUnit),
    tradePrice: asNumber(item.tradePrice),
    shippingPrice: 0,
    unitConversion: 0,
    dataQualityCode,
    dataQualityLabel: dataQualityLabel(dataQualityCode),
    tone: statusTone(dataQualityCode)
  };
}

function mapContract(item: ApiContractRow): ContractSummaryRow {
  const contractCategory = asNumber(item.contractCategory);
  const tradeUnit = item.tradeUnit === undefined ? undefined : asNumber(item.tradeUnit);
  return {
    id: item.contractNo ?? "contract",
    contractNo: item.contractNo ?? "",
    contractDisplayName: item.contractDisplayName ?? "",
    contractCategory,
    contractCategoryLabel: contractCategoryLabel(contractCategory),
    contractType: asNumber(item.contractType),
    tradeUnit,
    tradeUnitLabel: tradeUnit === undefined ? undefined : unitLabel(tradeUnit),
    tradePrice: item.tradePrice === undefined ? undefined : asNumber(item.tradePrice),
    shippingPrice: item.shippingPrice === undefined ? undefined : asNumber(item.shippingPrice),
    unitConversion: item.unitConversion === undefined ? undefined : asNumber(item.unitConversion),
    effectiveDate: timestampToDate(item.effectiveDate),
    transItemNo: item.transItemNo,
    transItemName: item.transItemName
  };
}

function mapLinkedItem(item: { itemNo?: string; itemName?: string; itemCategory?: number; unitWarehouse?: number }): LinkedMaterialItemRow {
  const itemCategory = asNumber(item.itemCategory);
  const unitWarehouse = asNumber(item.unitWarehouse);
  return {
    id: item.itemNo ?? "item",
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    itemCategory,
    itemCategoryLabel: itemCategoryLabel(itemCategory),
    unitWarehouse,
    unitWarehouseLabel: unitLabel(unitWarehouse)
  };
}

function mapItemDetailPayload(payload: ApiItemDetailPayload): MaterialItemDetail | undefined {
  if (!payload.item?.itemNo) {
    return undefined;
  }
  return {
    item: mapItem(payload.item),
    creationDate: timestampToDate(payload.item.creationTime),
    inventorySummary: mapItemInventorySummary(payload.inventorySummary),
    bomUsage: withFallbackArray<ApiItemBomUsageRow>(payload.bomUsage, []).map(mapBomUsage),
    recentBatches: withFallbackArray<ApiItemRecentBatchRow>(payload.recentBatches, []).map(mapRecentBatch),
    maintenanceSuggestions: withFallbackArray<ApiMaintenanceSuggestion>(payload.maintenanceSuggestions, []).map(mapSuggestion)
  };
}

function mapCompanyDetailPayload(payload: ApiCompanyDetailPayload): CompanyDetail | undefined {
  if (!payload.company?.companyNo) {
    return undefined;
  }
  const company = {
    ...mapCompany(payload.company),
    address: payload.company.address ?? "",
    phone: payload.company.phone ?? "",
    contactTitle: payload.company.contactTitle ?? "",
    contactEmail: payload.company.contactEmail ?? ""
  };
  return {
    company,
    transactionItems: withFallbackArray<ApiCompanyTransactionItemRow>(payload.transactionItems, []).map((item) =>
      mapCompanyTransactionItem(item, company)
    ),
    contracts: withFallbackArray<ApiContractRow>(payload.contracts, []).map(mapContract)
  };
}

function mapTransactionItemDetailPayload(payload: ApiTransactionItemDetailPayload): TransactionItemDetail | undefined {
  if (!payload.transItem?.transItemNo) {
    return undefined;
  }
  return {
    transItem: {
      ...mapTransactionItem(payload.transItem),
      comment: payload.transItem.comment ?? "",
      creationDate: timestampToDate(payload.transItem.creationTime)
    },
    contracts: withFallbackArray<ApiContractRow>(payload.contracts, []).map(mapContract),
    linkedItems: withFallbackArray<{ itemNo?: string; itemName?: string; itemCategory?: number; unitWarehouse?: number }>(
      payload.linkedItems,
      []
    ).map(mapLinkedItem)
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

function mockDetailResult(target: ItemMasterDetailTarget): ItemMasterDetailResult {
  if (target.type === "material") {
    const item = itemAndTransactionMasterMock.items.find((row) => row.itemNo === target.id);
    return {
      data: item
        ? {
            item,
            creationDate: "",
            inventorySummary: {
              hasStock: item.hasStock,
              currentQuantity: item.currentQuantity,
              availableQuantity: item.currentQuantity,
              reservedQuantity: 0,
              qualityHoldQuantity: 0,
              warehouseCount: item.hasStock ? 1 : 0,
              batchCount: item.batchCount
            },
            bomUsage: [],
            recentBatches: [],
            maintenanceSuggestions: itemAndTransactionMasterMock.maintenanceSuggestions.filter(
              (suggestion) => suggestion.itemNo === item.itemNo
            )
          }
        : undefined,
      source: "mock",
      error: item ? undefined : "示範資料中找不到此料品。"
    };
  }

  if (target.type === "company") {
    const company = itemAndTransactionMasterMock.companies.find((row) => row.companyNo === target.id);
    return {
      data: company
        ? {
            company: {
              ...company,
              address: "",
              phone: company.contactPhone,
              contactTitle: "",
              contactEmail: ""
            },
            transactionItems: itemAndTransactionMasterMock.transactionItems.filter(
              (item) => item.companyNo === company.companyNo
            ),
            contracts: []
          }
        : undefined,
      source: "mock",
      error: company ? undefined : "示範資料中找不到此客戶／廠商。"
    };
  }

  const transItem = itemAndTransactionMasterMock.transactionItems.find((row) => row.transItemNo === target.id);
  return {
    data: transItem
      ? {
          transItem: {
            ...transItem,
            comment: "",
            creationDate: ""
          },
          contracts: [],
          linkedItems: transItem.itemNo
            ? [
                {
                  id: transItem.itemNo,
                  itemNo: transItem.itemNo,
                  itemName: transItem.itemName,
                  itemCategory: transItem.itemCategory,
                  itemCategoryLabel: transItem.itemCategoryLabel,
                  unitWarehouse: transItem.tradeUnit,
                  unitWarehouseLabel: transItem.tradeUnitLabel
                }
              ]
            : []
        }
      : undefined,
    source: "mock",
    error: transItem ? undefined : "示範資料中找不到此交易品項。"
  };
}

export async function getItemMasterDetail(
  itemNo: string,
  dataSourceMode: DataSourceMode = "api"
): Promise<ItemMasterDetailResult> {
  if (dataSourceMode === "mock") {
    return mockDetailResult({ type: "material", id: itemNo });
  }
  try {
    const payload = await apiGet<ApiItemDetailPayload>(`/api/v2/items/${encodeURIComponent(itemNo)}/detail`);
    return {
      data: mapItemDetailPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      source: "api",
      error: error instanceof Error ? error.message : "料品明細 API 取得失敗"
    };
  }
}

export async function getCompanyMasterDetail(
  companyNo: string,
  dataSourceMode: DataSourceMode = "api"
): Promise<ItemMasterDetailResult> {
  if (dataSourceMode === "mock") {
    return mockDetailResult({ type: "company", id: companyNo });
  }
  try {
    const payload = await apiGet<ApiCompanyDetailPayload>(
      `/api/v2/transitems/companies/${encodeURIComponent(companyNo)}/detail`
    );
    return {
      data: mapCompanyDetailPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      source: "api",
      error: error instanceof Error ? error.message : "客戶／廠商明細 API 取得失敗"
    };
  }
}

export async function getTransactionItemMasterDetail(
  transItemNo: string,
  dataSourceMode: DataSourceMode = "api"
): Promise<ItemMasterDetailResult> {
  if (dataSourceMode === "mock") {
    return mockDetailResult({ type: "transaction", id: transItemNo });
  }
  try {
    const payload = await apiGet<ApiTransactionItemDetailPayload>(
      `/api/v2/transitems/transitems/${encodeURIComponent(transItemNo)}/detail`
    );
    return {
      data: mapTransactionItemDetailPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      source: "api",
      error: error instanceof Error ? error.message : "交易品項明細 API 取得失敗"
    };
  }
}
