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
  BomProductStructureData,
  BomProductStructureNode,
  BomProductStructureWarning,
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

type ApiBomLinkedProductContent = NonNullable<
  NonNullable<ApiBomDetailPayload["linkedProducts"]>[number]["contents"]
>[number];

type ApiBomProductStructureWarning = {
  code?: string;
  warningCode?: string;
  message?: string;
  nodeId?: string;
  refNo?: string;
};

type ApiBomProductStructureNode = {
  id?: string;
  nodeId?: string;
  nodeNo?: string;
  no?: string;
  itemNo?: string;
  productNo?: string;
  nodeName?: string;
  name?: string;
  itemName?: string;
  productName?: string;
  nodeTypeCode?: string;
  nodeType?: string;
  itemType?: string | number;
  type?: string;
  level?: number;
  itemCategory?: number;
  itemSubCategory?: number;
  productVersion?: number;
  bomNo?: string;
  bomVersion?: number;
  quantity?: number;
  count?: number;
  relationshipQuantity?: number;
  weight?: number;
  relationshipWeight?: number;
  unit?: string | number;
  unitCode?: number;
  statusCode?: string;
  versionStateCode?: string;
  structureStatusCode?: string;
  statusLabel?: string;
  hasChildren?: boolean;
  warnings?: ApiBomProductStructureWarning[];
  children?: ApiBomProductStructureNode[];
};

type ApiBomProductStructureEvidence = {
  bomNo?: string;
  bomVersion?: number;
  bomName?: string;
  versionStateCode?: string;
  dateTimestamp?: number;
};

type ApiBomProductStructurePayload = {
  serverTimestamp?: number;
  productNo?: string;
  productVersion?: number;
  rootProduct?: {
    productNo?: string;
    productName?: string;
    productVersion?: number;
    productCategory?: number;
    unitProduct?: number;
    structureStatusCode?: string;
  };
  bomEvidence?: ApiBomProductStructureEvidence[];
  children?: ApiBomProductStructureNode[];
  effectiveDate?: string;
  depth?: number;
  statusCode?: string;
  versionStateCode?: string;
  structureStatusCode?: string;
  statusLabel?: string;
  isPartial?: boolean;
  partial?: boolean;
  warnings?: ApiBomProductStructureWarning[];
  root?: ApiBomProductStructureNode;
  tree?: ApiBomProductStructureNode;
  structure?: ApiBomProductStructureNode;
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

export type BomProductStructureQuery = {
  productVersion?: number;
  depth?: number;
  effectiveDate?: string;
};

export type BomProductStructureResult = {
  data?: BomProductStructureData;
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

function asOptionalNumber(value?: number) {
  return Number.isFinite(value) ? Number(value) : undefined;
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

function normalizeWarning(warning: ApiBomProductStructureWarning): BomProductStructureWarning {
  const code = warning.code ?? warning.warningCode ?? "warning";
  const refText = warning.refNo ? `（${warning.refNo}）` : "";
  const labels: Record<string, string> = {
    depth_limited: "產品結構已達本次展開深度上限。",
    missing_bom_items: "BOM 直接明細尚未完整提供。",
    missing_item_master: "節點料品主檔資料缺漏。",
    missing_product_spec: "此產品版本尚未設定產品結構。",
    circular_reference: "產品結構存在循環參照，後端已停止展開。",
    unknown: "產品結構資料需確認。"
  };
  return {
    code,
    message: warning.message ?? `${labels[code] ?? labels.unknown}${refText}`
  };
}

function productStructureTypeLabel(value?: string | number) {
  const normalized = String(value ?? "").trim().toLocaleLowerCase();
  const labels: Record<string, string> = {
    product: "製成品",
    finished_product: "製成品",
    finishedproduct: "製成品",
    fg: "製成品",
    wip: "在製品",
    semi_finished: "半成品",
    semifinished: "半成品",
    inproduct: "在製品",
    material: "材料",
    raw_material: "原料",
    rawmaterial: "原料",
    raw: "原料",
    packaging: "包材",
    "1": "原料",
    "2": "物料",
    "3": "膠捲",
    "4": "在製品",
    "5": "製成品",
    "6": "貨品"
  };
  return labels[normalized] ?? "結構節點";
}

function productStructureStatusLabel(statusCode?: string, explicitLabel?: string) {
  if (explicitLabel) {
    return explicitLabel;
  }
  if (statusCode === "complete") {
    return "結構完整";
  }
  if (statusCode === "partial") {
    return "部分資料";
  }
  if (statusCode === "missing") {
    return "未設定結構";
  }
  const normalized = normalizeBomVersionStateCode(statusCode);
  return bomVersionStateLabel(normalized, locale);
}

function productStructureUnitLabel(unit?: string | number, unitCode?: number) {
  if (typeof unit === "string" && unit.trim()) {
    return unit;
  }
  return bomUnitLabel(unitCode ?? (typeof unit === "number" ? unit : undefined), locale);
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
    contents: withFallbackArray<ApiBomLinkedProductContent>(item.contents, []).map((content) => ({
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

function mapProductStructureNode(node: ApiBomProductStructureNode, indexPath = "0"): BomProductStructureNode {
  const children = withFallbackArray<ApiBomProductStructureNode>(node.children, []);
  const nodeNo = node.nodeNo ?? node.no ?? node.itemNo ?? node.productNo ?? "";
  const nodeTypeCode = String(node.nodeTypeCode ?? node.nodeType ?? node.itemCategory ?? node.itemType ?? node.type ?? "").trim();
  const statusCode = node.statusCode ?? node.structureStatusCode ?? node.versionStateCode ?? "unknown";

  return {
    id: node.id ?? node.nodeId ?? `${nodeNo || "node"}-${indexPath}`,
    nodeNo,
    nodeName: node.nodeName ?? node.name ?? node.itemName ?? node.productName ?? "",
    nodeTypeCode,
    nodeTypeLabel: productStructureTypeLabel(nodeTypeCode),
    productNo: node.productNo,
    productVersion: asOptionalNumber(node.productVersion),
    bomNo: node.bomNo,
    bomVersion: asOptionalNumber(node.bomVersion),
    quantity: asNumber(node.relationshipQuantity ?? node.quantity ?? node.count),
    weight: asNumber(node.relationshipWeight ?? node.weight),
    unit: productStructureUnitLabel(node.unit, node.unitCode),
    unitCode: asOptionalNumber(node.unitCode ?? (typeof node.unit === "number" ? node.unit : undefined)),
    statusCode,
    statusLabel: productStructureStatusLabel(statusCode, node.statusLabel),
    hasChildren: node.hasChildren ?? children.length > 0,
    warnings: withFallbackArray<ApiBomProductStructureWarning>(node.warnings, []).map(normalizeWarning),
    children: children.map((child, childIndex) => mapProductStructureNode(child, `${indexPath}-${childIndex}`))
  };
}

function mapProductStructurePayload(payload: ApiBomProductStructurePayload): BomProductStructureData {
  const rootProduct = payload.rootProduct;
  const children = withFallbackArray<ApiBomProductStructureNode>(payload.children, []);
  const bomEvidence = withFallbackArray<ApiBomProductStructureEvidence>(payload.bomEvidence, [])[0];
  const explicitRoot = payload.root ?? payload.tree ?? payload.structure;
  const root =
    explicitRoot ??
    (rootProduct
      ? {
          id: `product-${rootProduct.productNo ?? "root"}-${rootProduct.productVersion ?? 0}`,
          nodeNo: rootProduct.productNo,
          productNo: rootProduct.productNo,
          nodeName: rootProduct.productName,
          productVersion: rootProduct.productVersion,
          nodeTypeCode: "finished_product",
          unit: rootProduct.unitProduct,
          unitCode: rootProduct.unitProduct,
          bomNo: bomEvidence?.bomNo,
          bomVersion: bomEvidence?.bomVersion,
          structureStatusCode: rootProduct.structureStatusCode,
          hasChildren: children.length > 0,
          children
        }
      : undefined);
  const statusCode =
    payload.statusCode ??
    payload.structureStatusCode ??
    rootProduct?.structureStatusCode ??
    payload.versionStateCode ??
    root?.statusCode ??
    root?.versionStateCode ??
    "unknown";

  return {
    productNo: payload.productNo ?? rootProduct?.productNo ?? root?.productNo ?? root?.nodeNo ?? "",
    productVersion: asOptionalNumber(payload.productVersion ?? rootProduct?.productVersion ?? root?.productVersion),
    effectiveDate: payload.effectiveDate,
    depth: asNumber(payload.depth),
    statusCode,
    statusLabel: productStructureStatusLabel(statusCode, payload.statusLabel),
    isPartial: Boolean(payload.isPartial ?? payload.partial ?? statusCode === "partial"),
    warnings: withFallbackArray<ApiBomProductStructureWarning>(payload.warnings, []).map(normalizeWarning),
    root: root ? mapProductStructureNode(root) : undefined
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

function buildProductStructurePath(productNo: string, query: BomProductStructureQuery = {}) {
  const params = new URLSearchParams();
  if (query.productVersion !== undefined) {
    params.set("productVersion", String(query.productVersion));
  }
  if (query.depth !== undefined) {
    params.set("depth", String(query.depth));
  }
  if (query.effectiveDate) {
    params.set("effectiveDate", query.effectiveDate);
  }
  const suffix = params.toString() ? `?${params.toString()}` : "";
  return `/api/v2/bom/product-structure/${encodeURIComponent(productNo)}${suffix}`;
}

export async function getBomProductStructure(
  productNo: string,
  query: BomProductStructureQuery = {},
  dataSourceMode: DataSourceMode = "api"
): Promise<BomProductStructureResult> {
  if (dataSourceMode === "mock") {
    const { bomProductStructureMock } = await import("@/mock/bom");
    return {
      data: bomProductStructureMock[productNo],
      source: "mock"
    };
  }

  try {
    const payload = await apiGet<ApiBomProductStructurePayload>(buildProductStructurePath(productNo, query));
    return {
      data: mapProductStructurePayload(payload),
      source: "api"
    };
  } catch (error) {
    return {
      source: "api",
      error: error instanceof Error ? error.message : "Product Structure API unavailable"
    };
  }
}
