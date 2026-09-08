import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { bomUnitLabel, bomVersionStateLabel, bomVersionStateTone } from "@/i18n/bom-enums";
import { defaultLanguage, type LanguageCode } from "@/i18n/dictionary";
import { manufacturingDefinitionMock } from "@/mock/manufacturing-definition";
import { apiGet, withFallbackArray } from "@/services/api-client";
import type { StatusTone } from "@/types/dashboard";
import type {
  ManufacturingAuthority,
  ManufacturingCapabilityBoundary,
  ManufacturingDefinitionData,
  ManufacturingDefinitionDataSource,
  ManufacturingDefinitionQuery,
  ManufacturingDefinitionSubject,
  ManufacturingDefinitionStatus,
  ManufacturingDomainReference,
  ManufacturingEffectivityRow,
  ManufacturingFreezeCompatibility,
  ManufacturingLineage,
  ManufacturingResolutionStatus,
  ManufacturingVersionReference,
  ManufacturingWarning
} from "@/types/manufacturing-definition";

type ApiSubject = {
  itemNo?: string;
  itemName?: string;
  itemCategory?: number;
  itemSubCategory?: number;
  productVersion?: number;
  unitWarehouse?: number;
  unitProduct?: number;
  comment?: string;
  sourceCode?: string;
  masterStatusCode?: string;
  subjectSourceCode?: string;
};

type ApiVersion = {
  bomNo?: string;
  bomVersion?: number;
  bomName?: string;
  recipeNo?: string;
  recipeVersion?: number;
  versionStateCode?: string;
  formulaStatusCode?: string;
  dateTimestamp?: number;
  routingVersionId?: string;
  routingVersion?: number;
  routingStatusCode?: string;
  specId?: string;
  productNo?: string;
  productVersion?: number;
  packagingBomNo?: string;
};

type ApiDomain = {
  subject?: ApiSubject;
  moduleReadiness?: ApiModuleReadiness[];
  sourceLineage?: Record<string, string | ApiLineage | undefined>;
  warnings?: ApiWarning[];
  productStructure?: { bomEvidence?: ApiVersion[] };
  versions?: ApiVersion[];
  recipeFormula?: { recipeVersions?: ApiRecipeVersion[] };
  version?: ApiVersion;
  routingProcess?: { routing?: ApiVersion };
  packagingSpecs?: ApiVersion[];
};

type ApiRecipeVersion = {
  recipe?: ApiVersion;
  version?: ApiVersion;
  formula?: ApiVersion;
  inputs?: Array<{ inputNo?: string; quantity?: number; unit?: number }>;
  output?: { outputNo?: string; quantity?: number; unit?: number };
  sourceLineage?: Record<string, string>;
};

type ApiModuleReadiness = {
  moduleCode?: string;
  statusCode?: string;
  sourceCode?: string;
  warningCodes?: string[];
};

type ApiWarning = {
  domain?: string;
  moduleCode?: string;
  warningCode?: string;
  code?: string;
  refNo?: string;
};

type ApiLineage = {
  domain?: string;
  sourceCode?: string;
  sourceRef?: string;
  sourceParticipant?: string;
  acceptedEvidenceClass?: string;
  acceptanceState?: string;
  authorityCaveat?: string;
};

type ApiAuthority = {
  domain?: string;
  valueType?: string;
  value?: number;
  unit?: number;
  sourceCode?: string;
  sourceRef?: string;
  authorityCaveat?: string;
};

type ApiEffectivity = {
  asOfDate?: number;
  domains?: ApiEffectivityRow[];
};

type ApiEffectivityRow = {
  domain?: string;
  effectiveFrom?: number | null;
  effectiveTo?: number | null;
  currentActive?: boolean | null;
  retiredInactive?: boolean | null;
  statusCode?: string;
  evidenceRef?: string;
  conflictState?: string;
};

type ApiFreezeCompatibility = Partial<{
  statusCode: string;
  resolutionStatus: ManufacturingResolutionStatus;
  previewOnly: boolean;
  freezeReady: boolean;
  approvalSupported: boolean;
  releaseSupported: boolean;
  freezeSupported: boolean;
  productionOrderFreezeImplemented: boolean;
  warningCount: number;
}>;

type ApiCapabilityBoundary = Partial<ManufacturingCapabilityBoundary>;

type ApiManufacturingDefinitionPayload = {
  serverTimestamp?: number;
  timezone?: string;
  requestIdentity?: Partial<ManufacturingDefinitionQuery>;
  subject?: ApiSubject;
  definitionCandidate?: {
    definitionId?: string;
    definitionStatus?: ManufacturingDefinitionStatus;
    bomVersion?: ApiVersion | null;
    recipeVersions?: ApiVersion[];
    routingVersion?: ApiVersion | null;
    packagingSpecVersion?: ApiVersion[];
  } | null;
  domainReferences?: Record<string, ApiDomain>;
  quantityAuthorities?: ApiAuthority[];
  weightAuthorities?: ApiAuthority[];
  effectivity?: ApiEffectivity;
  resolutionStatus?: string;
  warnings?: ApiWarning[];
  sourceLineage?: ApiLineage[];
  freezeCompatibility?: ApiFreezeCompatibility;
  capabilityBoundary?: ApiCapabilityBoundary;
};

export type ManufacturingDefinitionResult = {
  data: ManufacturingDefinitionData;
  source: ManufacturingDefinitionDataSource;
  error?: string;
};

export const emptyManufacturingDefinitionData: ManufacturingDefinitionData = {
  timezone: "Asia/Taipei",
  requestIdentity: { itemNo: "", itemCategory: 5 },
  definitionStatus: "unavailable",
  definitionId: "",
  candidateVersions: [],
  domainReferences: [],
  quantityAuthorities: [],
  weightAuthorities: [],
  effectivityAsOfDateLabel: "未提供",
  effectivity: [],
  resolutionStatus: "UNAVAILABLE",
  resolutionStatusLabel: "目前不可用",
  warnings: [],
  sourceLineage: [],
  freezeCompatibility: {
    statusCode: "UNAVAILABLE",
    statusLabel: "目前不可用",
    resolutionStatus: "UNAVAILABLE",
    previewOnly: true,
    freezeReady: false,
    approvalSupported: false,
    releaseSupported: false,
    freezeSupported: false,
    productionOrderFreezeImplemented: false,
    warningCount: 0,
    tone: "danger"
  },
  capabilityBoundary: {
    readOnly: true,
    manufacturingDefinitionWriteSupported: false,
    productWriteSupported: false,
    bomWriteSupported: false,
    recipeWriteSupported: false,
    routingWriteSupported: false,
    packagingWriteSupported: false,
    approvalSupported: false,
    releaseSupported: false,
    freezeSupported: false,
    sourceOfTruthTransitionSupported: false,
    cutoverSupported: false,
    goLiveSupported: false
  }
};

const locale = defaultLanguage;

function asNumber(value?: number | null) {
  return Number.isFinite(value) ? Number(value) : 0;
}

function formatTimestamp(value: number | null | undefined, language: LanguageCode = locale) {
  if (!value) {
    return "未提供";
  }
  return new Date(value * 1000).toLocaleDateString(language, { timeZone: "Asia/Taipei" });
}

function formatVersion(value?: number | null) {
  return value ? `V${value}` : "未指定";
}

function localized(language: LanguageCode, values: Record<LanguageCode, string>) {
  return values[language] ?? values[defaultLanguage];
}

function categoryLabel(value: number | undefined, language: LanguageCode) {
  if (value === 4) {
    return localized(language, { "zh-TW": "在製品", en: "In-process", ja: "仕掛品", vi: "Bán thành phẩm" });
  }
  if (value === 5) {
    return localized(language, { "zh-TW": "製成品", en: "Finished good", ja: "製品", vi: "Thành phẩm" });
  }
  return localized(language, { "zh-TW": "未分類", en: "Unclassified", ja: "未分類", vi: "Chưa phân loại" });
}

function identityLabel(value: number | undefined, language: LanguageCode) {
  return value === 4
    ? localized(language, { "zh-TW": "Standalone WIP", en: "Standalone WIP", ja: "Standalone WIP", vi: "Standalone WIP" })
    : value === 5
      ? "Product"
      : localized(language, { "zh-TW": "未知主體", en: "Unknown subject", ja: "不明な主体", vi: "Chủ thể chưa xác định" });
}

function domainLabel(value: string | undefined, language: LanguageCode) {
  const labels: Record<string, Record<LanguageCode, string>> = {
    productWip: { "zh-TW": "Product / WIP", en: "Product / WIP", ja: "Product / WIP", vi: "Product / WIP" },
    bom: { "zh-TW": "BOM / 產品結構", en: "BOM / Product Structure", ja: "BOM / 製品構成", vi: "BOM / Cấu trúc sản phẩm" },
    recipe: { "zh-TW": "Recipe / Formula", en: "Recipe / Formula", ja: "Recipe / Formula", vi: "Recipe / Formula" },
    routing: { "zh-TW": "Routing / Process Flow", en: "Routing / Process Flow", ja: "Routing / Process Flow", vi: "Routing / Process Flow" },
    packaging: { "zh-TW": "Packaging Specification", en: "Packaging Specification", ja: "Packaging Specification", vi: "Packaging Specification" },
    subject: { "zh-TW": "主體", en: "Subject", ja: "主体", vi: "Chủ thể" }
  };
  return labels[value ?? ""] ? localized(language, labels[value ?? ""]) : value || localized(language, { "zh-TW": "未分類", en: "Unclassified", ja: "未分類", vi: "Chưa phân loại" });
}

function statusLabel(value: string | undefined, language: LanguageCode) {
  const labels: Record<string, Record<LanguageCode, string>> = {
    effective: { "zh-TW": "目前有效", en: "Effective", ja: "現在有効", vi: "Đang hiệu lực" },
    future: { "zh-TW": "未來生效", en: "Future", ja: "将来有効", vi: "Hiệu lực tương lai" },
    historical: { "zh-TW": "歷史版本", en: "Historical", ja: "履歴版", vi: "Phiên bản cũ" },
    test_support: { "zh-TW": "測試支援", en: "Test support", ja: "テスト支援", vi: "Hỗ trợ kiểm thử" },
    complete: { "zh-TW": "資料可用", en: "Available", ja: "利用可能", vi: "Có sẵn" },
    partial: { "zh-TW": "部分可用", en: "Partial", ja: "一部利用可能", vi: "Một phần" },
    unavailable: { "zh-TW": "目前不可用", en: "Unavailable", ja: "利用不可", vi: "Không khả dụng" },
    error: { "zh-TW": "資料錯誤", en: "Data error", ja: "データエラー", vi: "Lỗi dữ liệu" },
    unknown: { "zh-TW": "待確認", en: "Unknown", ja: "確認待ち", vi: "Chờ xác nhận" }
  };
  return labels[value ?? ""] ? localized(language, labels[value ?? ""]) : value || labels.unknown[language];
}

function resolutionStatusLabel(value: ManufacturingResolutionStatus, language: LanguageCode) {
  const labels: Record<ManufacturingResolutionStatus, Record<LanguageCode, string>> = {
    RESOLVED_SINGLE_CANDIDATE: { "zh-TW": "單一候選已整理", en: "Single candidate resolved", ja: "単一候補を整理済み", vi: "Đã xác định một ứng viên" },
    RESOLVED_WITH_WARNINGS: { "zh-TW": "已整理，仍有警示", en: "Resolved with warnings", ja: "警告付きで整理済み", vi: "Đã xác định kèm cảnh báo" },
    MULTIPLE_CANDIDATES: { "zh-TW": "存在多個候選", en: "Multiple candidates", ja: "複数候補", vi: "Nhiều ứng viên" },
    PARTIAL_CANDIDATE: { "zh-TW": "部分候選", en: "Partial candidate", ja: "部分候補", vi: "Ứng viên một phần" },
    UNAVAILABLE: { "zh-TW": "目前不可用", en: "Unavailable", ja: "利用不可", vi: "Không khả dụng" },
    CONFLICT: { "zh-TW": "效期或來源衝突", en: "Conflict", ja: "競合", vi: "Xung đột" }
  };
  return localized(language, labels[value]);
}

function normalizeResolutionStatus(value?: string): ManufacturingResolutionStatus {
  if (
    value === "RESOLVED_SINGLE_CANDIDATE" ||
    value === "RESOLVED_WITH_WARNINGS" ||
    value === "MULTIPLE_CANDIDATES" ||
    value === "PARTIAL_CANDIDATE" ||
    value === "UNAVAILABLE" ||
    value === "CONFLICT"
  ) {
    return value;
  }
  return "UNAVAILABLE";
}

function toneForStatus(value?: string): StatusTone {
  if (value === "effective" || value === "complete" || value === "RESOLVED_SINGLE_CANDIDATE") {
    return "success";
  }
  if (value === "CONFLICT") {
    return "danger";
  }
  if (value === "unavailable" || value === "error" || value === "UNAVAILABLE") {
    return "danger";
  }
  if (value === "partial" || value === "test_support" || value === "future" || value === "warning" || value === "RESOLVED_WITH_WARNINGS" || value === "MULTIPLE_CANDIDATES" || value === "PARTIAL_CANDIDATE") {
    return "warning";
  }
  return "neutral";
}

function sourceLabel(value: string | undefined, language: LanguageCode) {
  const labels: Record<string, Record<LanguageCode, string>> = {
    product_structure: { "zh-TW": "產品結構資料", en: "Product structure", ja: "製品構成", vi: "Cấu trúc sản phẩm" },
    recipe_formula: { "zh-TW": "Recipe / Formula 資料", en: "Recipe / Formula", ja: "Recipe / Formula", vi: "Recipe / Formula" },
    routing_process_flow: { "zh-TW": "Routing / Process Flow 資料", en: "Routing / Process Flow", ja: "Routing / Process Flow", vi: "Routing / Process Flow" },
    packaging_specification: { "zh-TW": "包裝規格資料", en: "Packaging specification", ja: "包装仕様", vi: "Quy cách đóng gói" },
    not_recorded: { "zh-TW": "尚未記錄來源", en: "Source not recorded", ja: "ソース未記録", vi: "Chưa ghi nhận nguồn" },
    existing_backend_read_surface: { "zh-TW": "既有後端唯讀資料面", en: "Existing backend read surface", ja: "既存バックエンド参照面", vi: "Bề mặt đọc Backend hiện có" },
    test_support: { "zh-TW": "測試支援資料", en: "Test-support data", ja: "テスト支援データ", vi: "Dữ liệu hỗ trợ kiểm thử" }
  };
  return labels[value ?? ""] ? localized(language, labels[value ?? ""]) : value || localized(language, { "zh-TW": "未提供來源", en: "Source not provided", ja: "ソース未提供", vi: "Chưa cung cấp nguồn" });
}

function authorityValueTypeLabel(value: string | undefined, language: LanguageCode) {
  const labels: Record<string, Record<LanguageCode, string>> = {
    component_quantity: { "zh-TW": "元件數量", en: "Component quantity", ja: "構成数量", vi: "Số lượng thành phần" },
    input_quantity: { "zh-TW": "配方投入數量", en: "Input quantity", ja: "投入数量", vi: "Số lượng đầu vào" },
    output_quantity: { "zh-TW": "配方產出數量", en: "Output quantity", ja: "産出数量", vi: "Số lượng đầu ra" },
    packaging_component_quantity: { "zh-TW": "包裝元件數量", en: "Packaging component quantity", ja: "包装構成数量", vi: "Số lượng thành phần đóng gói" },
    component_weight: { "zh-TW": "元件重量", en: "Component weight", ja: "構成重量", vi: "Trọng lượng thành phần" },
    formula_weight: { "zh-TW": "配方重量", en: "Formula weight", ja: "配合重量", vi: "Trọng lượng công thức" },
    output_weight: { "zh-TW": "產出重量", en: "Output weight", ja: "産出重量", vi: "Trọng lượng đầu ra" },
    input_weight: { "zh-TW": "投入重量", en: "Input weight", ja: "投入重量", vi: "Trọng lượng đầu vào" },
    packaging_unit_weight: { "zh-TW": "包裝單位重量", en: "Packaging unit weight", ja: "包装単位重量", vi: "Trọng lượng đơn vị đóng gói" }
  };
  return labels[value ?? ""] ? localized(language, labels[value ?? ""]) : value || localized(language, { "zh-TW": "數值", en: "Value", ja: "値", vi: "Giá trị" });
}

function warningMessage(code: string, language: LanguageCode) {
  const messages: Record<string, Record<LanguageCode, string>> = {
    module_unavailable: { "zh-TW": "模組目前不可用，畫面不自行補入候選資料。", en: "The module is unavailable; the page does not infer a candidate.", ja: "モジュールが利用できないため、画面では候補を推測しません。", vi: "Mô-đun không khả dụng; màn hình không tự suy đoán ứng viên." },
    multiple_bom_versions: { "zh-TW": "存在多個 BOM 版本，需由使用者確認適用版本。", en: "Multiple BOM versions require user confirmation.", ja: "複数のBOMバージョンがあり、適用版の確認が必要です。", vi: "Có nhiều phiên bản BOM, cần xác nhận phiên bản áp dụng." },
    multiple_recipe_versions: { "zh-TW": "存在多個 Recipe 版本，畫面保留全部候選。", en: "Multiple Recipe versions are preserved as candidates.", ja: "複数のRecipeバージョンを候補として保持します。", vi: "Các phiên bản Recipe được giữ lại dưới dạng ứng viên." },
    test_support_only: { "zh-TW": "此來源屬於測試支援，不代表正式產品資料來源。", en: "This is test-support evidence, not a formal product source.", ja: "これはテスト支援証拠であり、正式な製品ソースではありません。", vi: "Đây là bằng chứng hỗ trợ kiểm thử, không phải nguồn sản phẩm chính thức." },
    subject_unavailable: { "zh-TW": "查無指定 Product / WIP 主體。", en: "The requested Product / WIP subject was not found.", ja: "指定されたProduct / WIP主体が見つかりません。", vi: "Không tìm thấy Product / WIP được yêu cầu." }
  };
  return messages[code] ? localized(language, messages[code]) : code || localized(language, { "zh-TW": "需要確認資料警示。", en: "Data warning requires review.", ja: "データ警告を確認してください。", vi: "Cần xem xét cảnh báo dữ liệu." });
}

function mapSubject(value: ApiSubject | undefined, query: ManufacturingDefinitionQuery, language: LanguageCode): ManufacturingDefinitionSubject | undefined {
  if (!value?.itemNo) {
    return undefined;
  }
  const itemCategory = value.itemCategory ?? query.itemCategory;
  const statusCode = value.masterStatusCode ?? "unknown";
  return {
    itemNo: value.itemNo,
    itemName: value.itemName ?? "",
    itemCategory,
    itemCategoryLabel: categoryLabel(itemCategory, language),
    identityType: itemCategory === 4 ? "wip" : itemCategory === 5 ? "product" : "unknown",
    identityTypeLabel: identityLabel(itemCategory, language),
    versionLabel: itemCategory === 4 ? localized(language, { "zh-TW": "不適用", en: "Not applicable", ja: "該当なし", vi: "Không áp dụng" }) : formatVersion(value.productVersion),
    unitWarehouseLabel: bomUnitLabel(value.unitWarehouse, language),
    unitProductLabel: bomUnitLabel(value.unitProduct, language),
    masterStatusLabel: statusLabel(statusCode, language),
    sourceLabel: sourceLabel(value.sourceCode ?? value.subjectSourceCode, language),
    tone: toneForStatus(statusCode)
  };
}

function mapVersion(domainCode: string, value: ApiVersion, language: LanguageCode): ManufacturingVersionReference {
  const versionStateCode = value.versionStateCode ?? value.formulaStatusCode ?? value.routingStatusCode ?? "unknown";
  const referenceNo = value.bomNo ?? value.recipeNo ?? value.routingVersionId ?? value.specId ?? value.packagingBomNo ?? value.productNo ?? "";
  const version = value.bomVersion ?? value.recipeVersion ?? value.routingVersion ?? value.productVersion;
  return {
    domainCode,
    domainLabel: domainLabel(domainCode, language),
    referenceNo,
    versionLabel: formatVersion(version),
    statusCode: versionStateCode,
    statusLabel: statusLabel(versionStateCode, language),
    dateLabel: formatTimestamp(value.dateTimestamp, language),
    detailLabel: value.bomName ?? (domainCode === "packaging" ? value.packagingBomNo ?? "包裝規格候選" : domainLabel(domainCode, language)),
    tone: toneForStatus(versionStateCode)
  };
}

function mapDomainReferences(value: Record<string, ApiDomain> | undefined, language: LanguageCode): ManufacturingDomainReference[] {
  return Object.entries(value ?? {}).map(([domainCode, domain]) => {
    const modules = withFallbackArray<ApiModuleReadiness>(domain.moduleReadiness, []);
    const rawVersions = domain.versions?.length
      ? domain.versions
      : domainCode === "bom"
        ? domain.productStructure?.bomEvidence ?? []
        : domainCode === "recipe"
          ? (domain.recipeFormula?.recipeVersions ?? []).map((item) => ({ ...(item.version ?? {}), ...(item.recipe ?? {}) }))
          : domainCode === "routing"
            ? domain.version ? [domain.version] : domain.routingProcess?.routing ? [domain.routingProcess.routing] : []
            : domain.packagingSpecs ?? [];
    const versions = rawVersions.map((item) => mapVersion(domainCode, item, language));
    const statusCode = modules[0]?.statusCode ?? (versions.length ? "complete" : "unavailable");
    const warningCodes = withFallbackArray<ApiModuleReadiness>(domain.moduleReadiness, []).flatMap((item) => item.warningCodes ?? []);
    return {
      domainCode,
      domainLabel: domainLabel(domainCode, language),
      statusCode,
      statusLabel: statusLabel(statusCode, language),
      sourceLabel: sourceLabel(modules[0]?.sourceCode, language),
      warningCodes,
      versions,
      detailLabel: versions.length ? `${versions.length} ${localized(language, { "zh-TW": "個版本候選", en: versions.length === 1 ? "version candidate" : "version candidates", ja: "件のバージョン候補", vi: "ứng viên phiên bản" })}` : localized(language, { "zh-TW": "目前沒有版本候選", en: "No version candidate", ja: "バージョン候補なし", vi: "Không có ứng viên phiên bản" }),
      tone: toneForStatus(statusCode)
    };
  });
}

function mapAuthorities(values: ApiAuthority[] | undefined, language: LanguageCode): ManufacturingAuthority[] {
  return withFallbackArray<ApiAuthority>(values, []).map((item) => ({
    domainCode: item.domain ?? "",
    domainLabel: domainLabel(item.domain, language),
    valueTypeCode: item.valueType ?? "",
    valueTypeLabel: authorityValueTypeLabel(item.valueType, language),
    value: asNumber(item.value),
    unitLabel: bomUnitLabel(item.unit, language),
    sourceLabel: sourceLabel(item.sourceCode, language),
    sourceRef: item.sourceRef ?? "",
    authorityCaveat: item.authorityCaveat ?? "",
    tone: item.sourceCode === "not_recorded" ? "warning" : "info"
  }));
}

function mapEffectivity(value: ApiEffectivity | undefined, language: LanguageCode) {
  return {
    asOfDateLabel: formatTimestamp(value?.asOfDate, language),
    rows: withFallbackArray<ApiEffectivityRow>(value?.domains, []).map<ManufacturingEffectivityRow>((item) => ({
      domainCode: item.domain ?? "",
      domainLabel: domainLabel(item.domain, language),
      effectiveFromLabel: formatTimestamp(item.effectiveFrom, language),
      effectiveToLabel: formatTimestamp(item.effectiveTo, language),
      currentActive: item.currentActive ?? null,
      retiredInactive: item.retiredInactive ?? null,
      statusCode: item.statusCode ?? "unknown",
      statusLabel: statusLabel(item.statusCode, language),
      evidenceRef: item.evidenceRef ?? "",
      conflictState: item.conflictState ?? "UNKNOWN",
      tone: item.conflictState && item.conflictState !== "UNKNOWN" ? "danger" : toneForStatus(item.statusCode)
    }))
  };
}

function mapWarnings(values: ApiWarning[] | undefined, language: LanguageCode): ManufacturingWarning[] {
  return withFallbackArray<ApiWarning>(values, []).map((item) => {
    const code = item.warningCode ?? item.code ?? "unknown";
    const domainCode = item.domain ?? item.moduleCode ?? "subject";
    return {
      domainCode,
      domainLabel: domainLabel(domainCode, language),
      code,
      message: warningMessage(code, language),
      refNo: item.refNo ?? "",
      tone: code === "subject_unavailable" || code.includes("conflict") ? "danger" : "warning"
    };
  });
}

function mapLineage(values: ApiLineage[] | undefined, language: LanguageCode): ManufacturingLineage[] {
  return withFallbackArray<ApiLineage>(values, []).map((item) => {
    const acceptedEvidenceClass = item.acceptedEvidenceClass ?? "UNAVAILABLE";
    return {
      domainCode: item.domain ?? "subject",
      domainLabel: domainLabel(item.domain, language),
      sourceCode: item.sourceCode ?? "not_recorded",
      sourceLabel: sourceLabel(item.sourceCode, language),
      sourceRef: item.sourceRef ?? "",
      sourceParticipant: item.sourceParticipant ?? "",
      acceptedEvidenceClass,
      acceptedEvidenceLabel: acceptedEvidenceClass === "TEST_SUPPORT_ONLY"
        ? localized(language, { "zh-TW": "僅測試支援", en: "Test support only", ja: "テスト支援のみ", vi: "Chỉ hỗ trợ kiểm thử" })
        : acceptedEvidenceClass === "ACCEPTED_PRODUCT_EVIDENCE"
          ? localized(language, { "zh-TW": "可接受的產品證據", en: "Accepted product evidence", ja: "受入可能な製品証拠", vi: "Bằng chứng sản phẩm được chấp nhận" })
          : acceptedEvidenceClass === "PARTIAL"
            ? localized(language, { "zh-TW": "部分證據", en: "Partial evidence", ja: "部分証拠", vi: "Bằng chứng một phần" })
            : localized(language, { "zh-TW": "不可用", en: "Unavailable", ja: "利用不可", vi: "Không khả dụng" }),
      acceptanceState: item.acceptanceState ?? "",
      authorityCaveat: item.authorityCaveat ?? "",
      tone: acceptedEvidenceClass === "ACCEPTED_PRODUCT_EVIDENCE" ? "success" : acceptedEvidenceClass === "UNAVAILABLE" ? "danger" : "warning"
    };
  });
}

function mapFreeze(value: ApiFreezeCompatibility | undefined, resolutionStatus: ManufacturingResolutionStatus, language: LanguageCode): ManufacturingFreezeCompatibility {
  const statusCode = value?.statusCode ?? "UNAVAILABLE";
  return {
    statusCode,
    statusLabel: statusCode === "CANDIDATE_PREPARED_WITH_TARGETED_CONDITIONS"
      ? localized(language, { "zh-TW": "候選已整理，仍有條件", en: "Candidate prepared with conditions", ja: "条件付きで候補を整理済み", vi: "Ứng viên đã chuẩn bị với điều kiện" })
      : statusLabel(statusCode, language),
    resolutionStatus,
    previewOnly: value?.previewOnly ?? true,
    freezeReady: value?.freezeReady ?? false,
    approvalSupported: value?.approvalSupported ?? false,
    releaseSupported: value?.releaseSupported ?? false,
    freezeSupported: value?.freezeSupported ?? false,
    productionOrderFreezeImplemented: value?.productionOrderFreezeImplemented ?? false,
    warningCount: value?.warningCount ?? 0,
    tone: value?.freezeReady ? "success" : "warning"
  };
}

function mapPayload(payload: ApiManufacturingDefinitionPayload, query: ManufacturingDefinitionQuery, language: LanguageCode): ManufacturingDefinitionData {
  const requestIdentity = {
    ...query,
    ...(payload.requestIdentity ?? {}),
    itemNo: payload.requestIdentity?.itemNo ?? query.itemNo,
    itemCategory: (payload.requestIdentity?.itemCategory ?? query.itemCategory) as 4 | 5
  };
  const resolutionStatus = normalizeResolutionStatus(payload.resolutionStatus);
  const candidate = payload.definitionCandidate;
  const candidateVersions = [
    ...(candidate?.bomVersion ? [mapVersion("bom", candidate.bomVersion, language)] : []),
    ...withFallbackArray<ApiVersion>(candidate?.recipeVersions, []).map((item) => mapVersion("recipe", item, language)),
    ...(candidate?.routingVersion ? [mapVersion("routing", candidate.routingVersion, language)] : []),
    ...withFallbackArray<ApiVersion>(candidate?.packagingSpecVersion, []).map((item) => mapVersion("packaging", item, language))
  ];
  const effectivity = mapEffectivity(payload.effectivity, language);
  const warnings = mapWarnings(payload.warnings, language);
  const definitionStatus = candidate?.definitionStatus ?? (resolutionStatus === "UNAVAILABLE" ? "unavailable" : resolutionStatus === "PARTIAL_CANDIDATE" || resolutionStatus === "CONFLICT" ? "partial" : "candidate");
  return {
    serverTimestamp: payload.serverTimestamp,
    timezone: payload.timezone ?? "Asia/Taipei",
    requestIdentity,
    subject: mapSubject(payload.subject, requestIdentity, language),
    definitionStatus,
    definitionId: candidate?.definitionId ?? "",
    candidateVersions,
    domainReferences: mapDomainReferences(payload.domainReferences, language),
    quantityAuthorities: mapAuthorities(payload.quantityAuthorities, language),
    weightAuthorities: mapAuthorities(payload.weightAuthorities, language),
    effectivityAsOfDateLabel: effectivity.asOfDateLabel,
    effectivity: effectivity.rows,
    resolutionStatus,
    resolutionStatusLabel: resolutionStatusLabel(resolutionStatus, language),
    warnings,
    sourceLineage: mapLineage(payload.sourceLineage, language),
    freezeCompatibility: mapFreeze(payload.freezeCompatibility, resolutionStatus, language),
    capabilityBoundary: {
      ...emptyManufacturingDefinitionData.capabilityBoundary,
      ...(payload.capabilityBoundary ?? {})
    }
  };
}

function buildOverviewPath(query: ManufacturingDefinitionQuery) {
  const params = new URLSearchParams();
  params.set("itemNo", query.itemNo);
  params.set("itemCategory", String(query.itemCategory));
  if (query.asOfDate !== undefined) params.set("asOfDate", String(query.asOfDate));
  if (query.bomVersion !== undefined) params.set("bomVersion", String(query.bomVersion));
  if (query.recipeVersion !== undefined) params.set("recipeVersion", String(query.recipeVersion));
  if (query.routingVersion !== undefined) params.set("routingVersion", String(query.routingVersion));
  if (query.packagingVersion !== undefined) params.set("packagingVersion", String(query.packagingVersion));
  return `/api/v2/manufacturing-definition/overview?${params.toString()}`;
}

export async function getManufacturingDefinitionOverview(
  query: ManufacturingDefinitionQuery,
  dataSourceMode: DataSourceMode = "api",
  language: LanguageCode = defaultLanguage
): Promise<ManufacturingDefinitionResult> {
  if (dataSourceMode === "mock") {
    return { data: manufacturingDefinitionMock(query), source: "mock" };
  }

  try {
    const payload = await apiGet<ApiManufacturingDefinitionPayload>(buildOverviewPath(query));
    return { data: mapPayload(payload, query, language), source: "api" };
  } catch (error) {
    return {
      data: { ...emptyManufacturingDefinitionData, requestIdentity: query },
      source: "api",
      error: error instanceof Error ? error.message : "Manufacturing definition API unavailable"
    };
  }
}
