import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { defaultLanguage } from "@/i18n/dictionary";
import {
  bomItemTypeLabel,
  bomProductCategoryLabel,
  bomUnitLabel,
  bomVersionStateLabel,
  bomVersionStateTone,
  normalizeBomVersionStateCode
} from "@/i18n/bom-enums";
import { bomDashboardMock, bomDetailMock } from "@/mock/bom";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type {
  BomDashboardData,
  BomDashboardItem,
  BomDataSource,
  BomDetail,
  BomKpiItem,
  BomLinkedProduct,
  BomMaterialItem,
  BomSummary,
  BomVersionOption
} from "@/types/bom";

type ApiBomSummary = Partial<BomSummary>;

type ApiBomDashboardItem = {
  bomNo?: string;
  bomName?: string;
  version?: number;
  dateTimestamp?: number;
  unit?: number;
  weight?: number;
  versionStateCode?: string;
  itemCount?: number;
  linkedProductCount?: number;
};

type ApiBomDashboardPayload = {
  serverTimestamp?: number;
  summary?: ApiBomSummary;
  items?: ApiBomDashboardItem[];
  total?: number;
  start?: number;
  count?: number;
};

type ApiBomDetailPayload = {
  bom?: ApiBomDashboardItem & {
    comment?: string;
  };
  versions?: {
    version?: number;
    dateTimestamp?: number;
    versionStateCode?: string;
  }[];
  items?: {
    itemNo?: string;
    itemName?: string;
    unit?: number;
    weight?: number;
  }[];
  linkedProducts?: {
    productNo?: string;
    productName?: string;
    productVersion?: number;
    productCategory?: number;
    contents?: {
      itemType?: number;
      itemNo?: string;
      itemName?: string;
      count?: number;
      unit?: number;
      weight?: number;
    }[];
  }[];
};

export type BomDashboardQuery = {
  keyword?: string;
  bomNo?: string;
  versionStateCode?: string;
  start?: number;
  count?: number;
};

export type BomDashboardResult = {
  data: BomDashboardData;
  source: BomDataSource;
  error?: string;
};

export type BomDetailResult = {
  detail?: BomDetail;
  source: BomDataSource;
  error?: string;
};

const locale = defaultLanguage;

export const emptyBomDashboardData: BomDashboardData = {
  summary: {
    bomCount: 0,
    versionCount: 0,
    effectiveVersionCount: 0,
    futureVersionCount: 0,
    historicalVersionCount: 0
  },
  kpis: [
    { label: "BOM 數量", value: "0", hint: "API 尚未提供資料", tone: "info" },
    { label: "版本總數", value: "0", hint: "API 尚未提供資料", tone: "info" },
    { label: "目前有效", value: "0", hint: "API 尚未提供資料", tone: "info" },
    { label: "未來生效", value: "0", hint: "API 尚未提供資料", tone: "info" },
    { label: "歷史版本", value: "0", hint: "API 尚未提供資料", tone: "info" }
  ],
  items: [],
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

function timestampToDate(value?: number) {
  if (!value) {
    return "";
  }
  return new Date(value * 1000).toLocaleDateString(locale, { timeZone: "Asia/Taipei" });
}

function normalizeSummary(summary?: ApiBomSummary): BomSummary {
  return {
    bomCount: asNumber(summary?.bomCount),
    versionCount: asNumber(summary?.versionCount),
    effectiveVersionCount: asNumber(summary?.effectiveVersionCount),
    futureVersionCount: asNumber(summary?.futureVersionCount),
    historicalVersionCount: asNumber(summary?.historicalVersionCount)
  };
}

function kpisFromSummary(summary: BomSummary): BomKpiItem[] {
  return [
    { label: "BOM 數量", value: formatInteger(summary.bomCount), hint: "不重複商品配方", tone: "info" },
    { label: "版本總數", value: formatInteger(summary.versionCount), hint: "目前查詢條件下的版本筆數", tone: "info" },
    { label: "目前有效", value: formatInteger(summary.effectiveVersionCount), hint: "可供生產引用", tone: "success" },
    { label: "未來生效", value: formatInteger(summary.futureVersionCount), hint: "需留意切換日", tone: "warning" },
    { label: "歷史版本", value: formatInteger(summary.historicalVersionCount), hint: "保留追溯，不作預設版本", tone: "neutral" }
  ];
}

function mapDashboardItem(item: ApiBomDashboardItem): BomDashboardItem {
  const versionStateCode = normalizeBomVersionStateCode(item.versionStateCode);
  const bomNo = item.bomNo ?? "";
  const version = asNumber(item.version);

  return {
    id: `${bomNo || "BOM"}-v${version || 0}`,
    bomNo,
    bomName: item.bomName ?? "",
    version,
    date: timestampToDate(item.dateTimestamp),
    dateTimestamp: asNumber(item.dateTimestamp),
    unit: bomUnitLabel(item.unit, locale),
    unitCode: asNumber(item.unit),
    weight: asNumber(item.weight),
    versionStateCode,
    versionStateLabel: bomVersionStateLabel(versionStateCode, locale),
    tone: bomVersionStateTone(versionStateCode),
    itemCount: asNumber(item.itemCount),
    linkedProductCount: asNumber(item.linkedProductCount)
  };
}

function mapVersionOption(item: NonNullable<ApiBomDetailPayload["versions"]>[number]): BomVersionOption {
  const versionStateCode = normalizeBomVersionStateCode(item.versionStateCode);
  return {
    version: asNumber(item.version),
    date: timestampToDate(item.dateTimestamp),
    dateTimestamp: asNumber(item.dateTimestamp),
    versionStateCode,
    versionStateLabel: bomVersionStateLabel(versionStateCode, locale),
    tone: bomVersionStateTone(versionStateCode)
  };
}

function mapMaterialItem(item: NonNullable<ApiBomDetailPayload["items"]>[number]): BomMaterialItem {
  return {
    itemNo: item.itemNo ?? "",
    itemName: item.itemName ?? "",
    unit: bomUnitLabel(item.unit, locale),
    unitCode: asNumber(item.unit),
    weight: asNumber(item.weight)
  };
}

function mapLinkedProduct(item: NonNullable<ApiBomDetailPayload["linkedProducts"]>[number]): BomLinkedProduct {
  return {
    productNo: item.productNo ?? "",
    productName: item.productName ?? "",
    productVersion: asNumber(item.productVersion),
    productCategory: asNumber(item.productCategory),
    productCategoryLabel: bomProductCategoryLabel(item.productCategory, locale),
    contents: withFallbackArray(item.contents, []).map((content) => ({
      itemType: asNumber(content.itemType),
      itemTypeLabel: bomItemTypeLabel(content.itemType, locale),
      itemNo: content.itemNo ?? "",
      itemName: content.itemName ?? "",
      count: asNumber(content.count),
      unit: bomUnitLabel(content.unit, locale),
      unitCode: asNumber(content.unit),
      weight: asNumber(content.weight)
    }))
  };
}

function mapDashboardPayload(payload: ApiBomDashboardPayload): BomDashboardData {
  const summary = normalizeSummary(payload.summary);
  const items = withFallbackArray(payload.items, []).map(mapDashboardItem);

  return {
    summary,
    kpis: kpisFromSummary(summary),
    items,
    total: payload.total ?? items.length,
    start: payload.start ?? 0,
    count: payload.count ?? items.length
  };
}

function mapDetailPayload(payload: ApiBomDetailPayload, fallback?: BomDashboardItem): BomDetail | undefined {
  const bom = payload.bom ? mapDashboardItem(payload.bom) : fallback;
  if (!bom?.bomNo) {
    return undefined;
  }

  return {
    bom: {
      ...bom,
      comment: payload.bom?.comment ?? ""
    },
    versions: withFallbackArray(payload.versions, []).map(mapVersionOption),
    items: withFallbackArray(payload.items, []).map(mapMaterialItem),
    linkedProducts: withFallbackArray(payload.linkedProducts, []).map(mapLinkedProduct)
  };
}

function buildDashboardPath(query: BomDashboardQuery) {
  const params = new URLSearchParams();
  if (query.keyword) {
    params.set("keyword", query.keyword);
  }
  if (query.bomNo) {
    params.set("bomNo", query.bomNo);
  }
  if (query.versionStateCode) {
    params.set("versionStateCode", query.versionStateCode);
  }
  if (query.start !== undefined) {
    params.set("start", String(query.start));
  }
  params.set("count", String(query.count ?? 50));
  return `/api/v2/bom/dashboard?${params.toString()}`;
}

export async function getBomDashboard(
  query: BomDashboardQuery = {},
  dataSourceMode: DataSourceMode = "api"
): Promise<BomDashboardResult> {
  if (dataSourceMode === "mock") {
    return {
      data: bomDashboardMock,
      source: "mock"
    };
  }

  try {
    const payload = await apiGet<ApiBomDashboardPayload>(buildDashboardPath(query));
    return {
      data: mapDashboardPayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      data: emptyBomDashboardData,
      source: "api",
      error: error instanceof Error ? error.message : "BOM Center API unavailable"
    };
  }
}

export async function getBomDetail(
  bomNo: string,
  version?: number,
  fallback?: BomDashboardItem,
  dataSourceMode: DataSourceMode = "api"
): Promise<BomDetailResult> {
  if (dataSourceMode === "mock") {
    return {
      detail: bomDetailMock[bomNo] ?? (fallback ? { bom: { ...fallback, comment: "" }, versions: [], items: [], linkedProducts: [] } : undefined),
      source: "mock"
    };
  }

  try {
    const params = new URLSearchParams();
    if (version !== undefined) {
      params.set("version", String(version));
    }
    const suffix = params.toString() ? `?${params.toString()}` : "";
    const payload = await apiGet<ApiBomDetailPayload>(`/api/v2/bom/${encodeURIComponent(bomNo)}/detail${suffix}`);
    return {
      detail: mapDetailPayload(payload, fallback),
      source: "api"
    };
  } catch (error) {
    return {
      detail: fallback ? { bom: { ...fallback, comment: "" }, versions: [], items: [], linkedProducts: [] } : undefined,
      source: "api",
      error: error instanceof Error ? error.message : "BOM Center detail API unavailable"
    };
  }
}
