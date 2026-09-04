import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { bomUnitLabel } from "@/i18n/bom-enums";
import { defaultLanguage } from "@/i18n/dictionary";
import { packagingMock } from "@/mock/packaging";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { StatusTone } from "@/types/dashboard";
import type {
  PackagingCapabilityBoundary,
  PackagingDataSource,
  PackagingLineage,
  PackagingModuleReadiness,
  PackagingOverviewData,
  PackagingQuery,
  PackagingSpec,
  PackagingSpecLine,
  PackagingStatusCode,
  PackagingSubject,
  PackagingSummary,
  PackagingWarning
} from "@/types/packaging";

type ApiPackagingPayload = {
  serverTimestamp?: number;
  timezone?: string;
  requestIdentity?: Partial<PackagingQuery>;
  subject?: ApiPackagingSubject;
  summary?: Partial<PackagingSummary>;
  packagingSpecs?: ApiPackagingSpec[];
  sourceLineage?: ApiSourceLineage;
  warnings?: ApiWarning[];
  moduleReadiness?: ApiModuleReadiness[];
  capabilityBoundary?: Partial<PackagingCapabilityBoundary>;
};

type ApiPackagingSubject = {
  itemNo?: string;
  itemName?: string;
  itemCategory?: number;
  itemCategoryLabel?: string;
  itemSubCategory?: number;
  productVersion?: number;
  unitShipping?: number;
  unitWarehouse?: number;
  unitProduct?: number;
  unitShippingLabel?: string;
  unitWarehouseLabel?: string;
  unitProductLabel?: string;
  comment?: string;
  sourceCode?: string;
};

type ApiPackagingSpec = {
  specId?: string;
  productNo?: string;
  productVersion?: number;
  wipNo?: string;
  packagingLevel?: number;
  packagingLevelLabel?: string;
  packagingBomNo?: string;
  packagingBomName?: string;
  count?: number;
  unit?: number;
  unitLabel?: string;
  weight?: number;
  masterUnit?: number;
  masterUnitLabel?: string;
  masterWeight?: number;
  linkedBomNo?: string;
  linkedBomVersion?: number;
  lineCount?: number;
  lines?: ApiPackagingSpecLine[];
  sourceCode?: string;
  masterSourceCode?: string;
  lineSourceCode?: string;
};

type ApiPackagingSpecLine = {
  parentBomNo?: string;
  parentBomName?: string;
  childCategory?: number;
  childCategoryLabel?: string;
  childNo?: string;
  childName?: string;
  childUnit?: number;
  childUnitLabel?: string;
  count?: number;
  childUnit2?: number;
  childUnit2Label?: string;
  weight?: number;
  length?: number;
  expectedLoss?: number;
  actualLoss?: number;
  processCount?: number;
  comment?: string;
};

type ApiSourceLineage = Record<string, string | undefined> | PackagingLineage[];

type ApiWarning = {
  moduleCode?: string;
  moduleLabel?: string;
  warningCode?: string;
  code?: string;
  message?: string;
  refNo?: string;
};

type ApiModuleReadiness = {
  moduleCode?: string;
  moduleLabel?: string;
  statusCode?: string;
  statusLabel?: string;
  sourceCode?: string;
  sourceLabel?: string;
  warningCodes?: string[];
};

export type PackagingResult = {
  data: PackagingOverviewData;
  source: PackagingDataSource;
  error?: string;
};

export const emptyPackagingOverviewData: PackagingOverviewData = {
  timezone: "Asia/Taipei",
  requestIdentity: { itemNo: "", itemCategory: 5 },
  subject: undefined,
  summary: {
    packagingSpecCount: 0,
    packagingBomCount: 0,
    packageLevelCount: 0,
    materialLineCount: 0,
    totalCount: 0,
    totalWeight: 0
  },
  packagingSpecs: [],
  sourceLineage: [],
  moduleReadiness: [],
  warnings: [],
  capabilityBoundary: {
    readOnly: true,
    packagingWriteSupported: false,
    packagingApprovalSupported: false,
    packagingReleaseSupported: false,
    sourceOfTruthTransitionSupported: false,
    cutoverSupported: false,
    goLiveSupported: false
  }
};

const locale = defaultLanguage;

function asNumber(value?: number) {
  return Number.isFinite(value) ? Number(value) : 0;
}

function unitLabel(value?: number, explicit?: string) {
  return explicit || bomUnitLabel(value, locale) || "";
}

function itemCategoryLabel(value?: number) {
  if (value === 5) {
    return "製成品";
  }
  if (value === 4) {
    return "在製品";
  }
  return "未分類";
}

function packagingLevelLabel(value?: number, explicit?: string) {
  if (explicit) {
    return explicit;
  }
  if (value === 1) {
    return "箱規";
  }
  if (value === 2) {
    return "組規";
  }
  if (value === 0) {
    return "其他";
  }
  return "未分類";
}

function sourceLabel(value?: string) {
  const labels: Record<string, string> = {
    product: "製成品主檔",
    inproduct: "在製品主檔",
    product_bom_spec: "product_bom_spec 包裝規格",
    bom2_number: "bom2_number 包材 BOM 主檔",
    bom2: "bom2 包材 BOM 明細",
    product_spec: "product_spec 下游產品關聯",
    not_recorded: "未建立"
  };
  return labels[value ?? ""] ?? value ?? "";
}

function statusCode(value?: string): PackagingStatusCode {
  if (value === "complete" || value === "partial" || value === "unavailable" || value === "error") {
    return value;
  }
  if (value === "ready" || value === "linked") {
    return "complete";
  }
  if (value === "missing" || value === "not_recorded") {
    return "unavailable";
  }
  return "partial";
}

function statusLabel(value?: string) {
  const normalized = statusCode(value);
  const labels: Record<PackagingStatusCode, string> = {
    complete: "完整",
    partial: "部分資料",
    unavailable: "目前不可用",
    error: "取得失敗"
  };
  return labels[normalized];
}

function statusTone(value?: string): StatusTone {
  const normalized = statusCode(value);
  if (normalized === "complete") {
    return "success";
  }
  if (normalized === "error") {
    return "danger";
  }
  if (normalized === "unavailable" || normalized === "partial") {
    return "warning";
  }
  return "neutral";
}

function sourceTone(value?: string): StatusTone {
  return value === "not_recorded" ? "warning" : "success";
}

function moduleLabel(value?: string) {
  return value === "packagingSpecification" ? "包裝規格" : value || "未知模組";
}

function warningMessage(code: string) {
  const messages: Record<string, string> = {
    missing_packaging_spec: "尚未建立包裝規格。",
    missing_packaging_bom_master: "包材 BOM 主檔尚未建立或未回填。",
    missing_packaging_bom_lines: "包材 BOM 明細尚未建立或未回填。",
    wip_packaging_context_from_downstream_product: "在製品包裝情境來自下游製成品關聯，需保留來源產品識別。",
    module_unavailable: "包裝規格模組資料取得失敗。"
  };
  return messages[code] ?? "包裝規格資料需確認。";
}

function mapSubject(subject: ApiPackagingSubject | undefined, query: PackagingQuery): PackagingSubject | undefined {
  if (!subject?.itemNo && !query.itemNo) {
    return undefined;
  }
  const itemCategory = subject?.itemCategory ?? query.itemCategory;
  const productVersion = asNumber(subject?.productVersion ?? query.productVersion);
  return {
    itemNo: subject?.itemNo ?? query.itemNo,
    itemName: subject?.itemName ?? "",
    itemCategory,
    itemCategoryLabel: subject?.itemCategoryLabel ?? itemCategoryLabel(itemCategory),
    itemSubCategory: asNumber(subject?.itemSubCategory),
    productVersion,
    versionLabel: productVersion ? `V${productVersion}` : "未指定",
    unitShippingLabel: subject?.unitShippingLabel ?? unitLabel(subject?.unitShipping),
    unitWarehouseLabel: subject?.unitWarehouseLabel ?? unitLabel(subject?.unitWarehouse),
    unitProductLabel: subject?.unitProductLabel ?? unitLabel(subject?.unitProduct),
    comment: subject?.comment ?? "",
    sourceLabel: sourceLabel(subject?.sourceCode),
    tone: subject?.itemNo ? "success" : "warning"
  };
}

function mapSummary(summary?: Partial<PackagingSummary>): PackagingSummary {
  return {
    packagingSpecCount: asNumber(summary?.packagingSpecCount),
    packagingBomCount: asNumber(summary?.packagingBomCount),
    packageLevelCount: asNumber(summary?.packageLevelCount),
    materialLineCount: asNumber(summary?.materialLineCount),
    totalCount: asNumber(summary?.totalCount),
    totalWeight: asNumber(summary?.totalWeight)
  };
}

function mapLine(line: ApiPackagingSpecLine): PackagingSpecLine {
  return {
    parentBomNo: line.parentBomNo ?? "",
    parentBomName: line.parentBomName ?? "",
    childCategory: asNumber(line.childCategory),
    childCategoryLabel: line.childCategoryLabel ?? itemCategoryLabel(line.childCategory),
    childNo: line.childNo ?? "",
    childName: line.childName ?? "",
    childUnitLabel: line.childUnitLabel ?? unitLabel(line.childUnit),
    count: asNumber(line.count),
    childUnit2Label: line.childUnit2Label ?? unitLabel(line.childUnit2),
    weight: asNumber(line.weight),
    length: asNumber(line.length),
    expectedLoss: asNumber(line.expectedLoss),
    actualLoss: asNumber(line.actualLoss),
    processCount: asNumber(line.processCount),
    comment: line.comment ?? ""
  };
}

function mapSpec(spec: ApiPackagingSpec, index: number): PackagingSpec {
  const source = spec.sourceCode ?? "";
  const masterSource = spec.masterSourceCode ?? "";
  const lineSource = spec.lineSourceCode ?? "";
  const hasMissingSource = masterSource === "not_recorded" || lineSource === "not_recorded";
  return {
    specId: spec.specId ?? `${spec.productNo ?? "product"}:${spec.productVersion ?? 0}:${spec.packagingBomNo ?? index}`,
    productNo: spec.productNo ?? "",
    productVersion: asNumber(spec.productVersion),
    wipNo: spec.wipNo ?? "",
    packagingLevel: asNumber(spec.packagingLevel),
    packagingLevelLabel: packagingLevelLabel(spec.packagingLevel, spec.packagingLevelLabel),
    packagingBomNo: spec.packagingBomNo ?? "",
    packagingBomName: spec.packagingBomName ?? "",
    count: asNumber(spec.count),
    unitLabel: spec.unitLabel ?? unitLabel(spec.unit),
    weight: asNumber(spec.weight),
    masterUnitLabel: spec.masterUnitLabel ?? unitLabel(spec.masterUnit),
    masterWeight: asNumber(spec.masterWeight),
    linkedBomNo: spec.linkedBomNo ?? "",
    linkedBomVersion: asNumber(spec.linkedBomVersion),
    lineCount: asNumber(spec.lineCount),
    lines: withFallbackArray<ApiPackagingSpecLine>(spec.lines, []).map(mapLine),
    sourceLabel: sourceLabel(source),
    masterSourceLabel: sourceLabel(masterSource),
    lineSourceLabel: sourceLabel(lineSource),
    tone: hasMissingSource ? "warning" : "success"
  };
}

function mapSourceLineage(value?: ApiSourceLineage): PackagingLineage[] {
  if (Array.isArray(value)) {
    return value;
  }
  return Object.entries(value ?? {})
    .filter(([, source]) => Boolean(source))
    .map(([key, source]) => ({
      sourceTypeLabel: {
        subjectSourceCode: "主體來源",
        packagingSpecSourceCode: "包裝規格來源",
        packagingBomMasterSourceCode: "包材 BOM 主檔來源",
        packagingBomLineSourceCode: "包材 BOM 明細來源"
      }[key] ?? key,
      sourceLabel: sourceLabel(source),
      tone: sourceTone(source)
    }));
}

function mapWarning(warning: ApiWarning): PackagingWarning {
  const code = warning.warningCode ?? warning.code ?? "unknown";
  return {
    moduleLabel: warning.moduleLabel ?? moduleLabel(warning.moduleCode),
    code,
    message: warning.message ?? warningMessage(code),
    refNo: warning.refNo ?? "",
    tone: code === "module_unavailable" ? "danger" : "warning"
  };
}

function mapModuleReadiness(item: ApiModuleReadiness): PackagingModuleReadiness {
  const normalized = statusCode(item.statusCode);
  return {
    moduleCode: item.moduleCode ?? "",
    moduleLabel: item.moduleLabel ?? moduleLabel(item.moduleCode),
    statusCode: normalized,
    statusLabel: item.statusLabel ?? statusLabel(normalized),
    sourceLabel: item.sourceLabel ?? sourceLabel(item.sourceCode),
    warningCodes: withFallbackArray<string>(item.warningCodes, []),
    tone: statusTone(normalized)
  };
}

function mapPayload(payload: ApiPackagingPayload, query: PackagingQuery): PackagingOverviewData {
  const requestIdentity = {
    ...query,
    ...payload.requestIdentity,
    itemNo: payload.requestIdentity?.itemNo ?? query.itemNo,
    itemCategory: (payload.requestIdentity?.itemCategory ?? query.itemCategory) as 4 | 5
  };
  return {
    serverTimestamp: payload.serverTimestamp,
    timezone: payload.timezone ?? "Asia/Taipei",
    requestIdentity,
    subject: mapSubject(payload.subject, requestIdentity),
    summary: mapSummary(payload.summary),
    packagingSpecs: withFallbackArray<ApiPackagingSpec>(payload.packagingSpecs, []).map(mapSpec),
    sourceLineage: mapSourceLineage(payload.sourceLineage),
    warnings: withFallbackArray<ApiWarning>(payload.warnings, []).map(mapWarning),
    moduleReadiness: withFallbackArray<ApiModuleReadiness>(payload.moduleReadiness, []).map(mapModuleReadiness),
    capabilityBoundary: {
      ...emptyPackagingOverviewData.capabilityBoundary,
      ...(payload.capabilityBoundary ?? {})
    }
  };
}

function buildOverviewPath(query: PackagingQuery) {
  const params = new URLSearchParams();
  params.set("itemNo", query.itemNo);
  params.set("itemCategory", String(query.itemCategory));
  if (query.productVersion !== undefined) {
    params.set("productVersion", String(query.productVersion));
  }
  if (query.effectiveDate !== undefined) {
    params.set("effectiveDate", String(query.effectiveDate));
  }
  return `/api/v2/packaging-specification/overview?${params.toString()}`;
}

export async function getPackagingOverview(query: PackagingQuery, dataSourceMode: DataSourceMode = "api"): Promise<PackagingResult> {
  if (dataSourceMode === "mock") {
    return {
      data: packagingMock(query.itemCategory === 4 ? "wip" : "product"),
      source: "mock"
    };
  }

  try {
    const payload = await apiGet<ApiPackagingPayload>(buildOverviewPath(query));
    return {
      data: mapPayload(payload, query),
      source: "api"
    };
  } catch (error) {
    return {
      data: {
        ...emptyPackagingOverviewData,
        requestIdentity: query
      },
      source: "api",
      error: error instanceof Error ? error.message : "Packaging specification API unavailable"
    };
  }
}
