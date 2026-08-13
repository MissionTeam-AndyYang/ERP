import type { LanguageCode } from "@/i18n/dictionary";
import type { StatusTone } from "@/types/dashboard";
import type { BomVersionStateCode } from "@/types/bom";

const fallbackLanguage: LanguageCode = "zh-TW";

const unitLabels: Record<number, Partial<Record<LanguageCode, string>>> = {
  0: { "zh-TW": "其他", en: "Other", ja: "その他", vi: "Khác" },
  1: { "zh-TW": "公克", en: "g", ja: "g", vi: "g" },
  2: { "zh-TW": "公斤", en: "kg", ja: "kg", vi: "kg" },
  3: { "zh-TW": "台斤", en: "catty", ja: "台斤", vi: "cân Đài Loan" },
  51: { "zh-TW": "公分", en: "cm", ja: "cm", vi: "cm" },
  52: { "zh-TW": "公尺", en: "m", ja: "m", vi: "m" },
  101: { "zh-TW": "個", en: "pcs", ja: "個", vi: "cái" },
  102: { "zh-TW": "條", en: "strip", ja: "本", vi: "thanh" },
  103: { "zh-TW": "片", en: "sheet", ja: "枚", vi: "miếng" },
  104: { "zh-TW": "張", en: "sheet", ja: "枚", vi: "tờ" },
  105: { "zh-TW": "罐", en: "can", ja: "缶", vi: "lon" },
  106: { "zh-TW": "包", en: "pack", ja: "包", vi: "gói" },
  107: { "zh-TW": "捲", en: "roll", ja: "巻", vi: "cuộn" },
  108: { "zh-TW": "桶", en: "pail", ja: "桶", vi: "thùng" },
  109: { "zh-TW": "盒", en: "box", ja: "箱", vi: "hộp" },
  110: { "zh-TW": "組", en: "set", ja: "組", vi: "bộ" },
  111: { "zh-TW": "箱", en: "carton", ja: "箱", vi: "thùng" },
  112: { "zh-TW": "支", en: "piece", ja: "本", vi: "cây" },
  113: { "zh-TW": "式", en: "set", ja: "式", vi: "bộ" },
  114: { "zh-TW": "入", en: "unit", ja: "入り", vi: "đơn vị" },
  115: { "zh-TW": "袋", en: "bag", ja: "袋", vi: "túi" },
  116: { "zh-TW": "顆", en: "piece", ja: "粒", vi: "viên" },
  117: { "zh-TW": "瓶", en: "bottle", ja: "瓶", vi: "chai" },
  201: { "zh-TW": "板", en: "pallet", ja: "パレット", vi: "pallet" },
  202: { "zh-TW": "件", en: "case", ja: "件", vi: "kiện" },
  203: { "zh-TW": "車", en: "truck", ja: "車", vi: "xe" },
  204: { "zh-TW": "次", en: "time", ja: "回", vi: "lần" }
};

const versionStateLabels: Record<BomVersionStateCode, Partial<Record<LanguageCode, string>>> = {
  effective: { "zh-TW": "目前有效", en: "Effective", ja: "現在有効", vi: "Đang hiệu lực" },
  future: { "zh-TW": "未來生效", en: "Future", ja: "将来有効", vi: "Hiệu lực tương lai" },
  historical: { "zh-TW": "歷史版本", en: "Historical", ja: "履歴版", vi: "Phiên bản cũ" },
  unknown: { "zh-TW": "待確認", en: "Unknown", ja: "確認待ち", vi: "Chờ xác nhận" }
};

const levelLabels: Record<number, Partial<Record<LanguageCode, string>>> = {
  0: { "zh-TW": "未指定", en: "Unspecified", ja: "未指定", vi: "Chưa chỉ định" },
  1: { "zh-TW": "組規", en: "Set spec", ja: "組仕様", vi: "Quy cách bộ" },
  2: { "zh-TW": "箱規", en: "Carton spec", ja: "箱仕様", vi: "Quy cách thùng" }
};

const itemTypeLabels: Record<number, Partial<Record<LanguageCode, string>>> = {
  0: { "zh-TW": "未指定", en: "Unspecified", ja: "未指定", vi: "Chưa chỉ định" },
  1: { "zh-TW": "在製品", en: "In-process", ja: "仕掛品", vi: "Bán thành phẩm" },
  2: { "zh-TW": "製成品", en: "Finished good", ja: "製品", vi: "Thành phẩm" }
};

const productCategoryLabels: Record<number, Partial<Record<LanguageCode, string>>> = {
  0: { "zh-TW": "其他", en: "Other", ja: "その他", vi: "Khác" },
  1: { "zh-TW": "散裝品", en: "Bulk product", ja: "バルク品", vi: "Thành phẩm rời" },
  2: { "zh-TW": "組裝品", en: "Assembled product", ja: "組立品", vi: "Thành phẩm lắp ráp" }
};

function pickLabel(labels: Partial<Record<LanguageCode, string>> | undefined, language: string, fallback: string) {
  const normalizedLanguage = language as LanguageCode;
  return labels?.[normalizedLanguage] ?? labels?.[fallbackLanguage] ?? fallback;
}

export function bomUnitLabel(value?: number, language: string = fallbackLanguage) {
  if (value === undefined || value === null) {
    return "";
  }
  return pickLabel(unitLabels[value], language, String(value));
}

export function bomVersionStateLabel(value?: string, language: string = fallbackLanguage) {
  const state = normalizeBomVersionStateCode(value);
  return pickLabel(versionStateLabels[state], language, state);
}

export function bomVersionStateTone(value?: string): StatusTone {
  const state = normalizeBomVersionStateCode(value);
  if (state === "effective") {
    return "success";
  }
  if (state === "future") {
    return "info";
  }
  if (state === "historical") {
    return "neutral";
  }
  return "warning";
}

export function bomLevelLabel(value?: number, language: string = fallbackLanguage) {
  if (value === undefined || value === null) {
    return pickLabel(levelLabels[0], language, "0");
  }
  return pickLabel(levelLabels[value], language, String(value));
}

export function bomItemTypeLabel(value?: number, language: string = fallbackLanguage) {
  if (value === undefined || value === null) {
    return pickLabel(itemTypeLabels[0], language, "0");
  }
  return pickLabel(itemTypeLabels[value], language, String(value));
}

export function bomProductCategoryLabel(value?: number, language: string = fallbackLanguage) {
  if (value === undefined || value === null) {
    return pickLabel(productCategoryLabels[0], language, "0");
  }
  return pickLabel(productCategoryLabels[value], language, String(value));
}

export function normalizeBomVersionStateCode(value?: string): BomVersionStateCode {
  if (value === "effective" || value === "future" || value === "historical" || value === "unknown") {
    return value;
  }
  return "unknown";
}
