import type { LanguageCode } from "@/i18n/dictionary";
import type { StatusTone } from "@/types/dashboard";
import type { RoutingVersionStateCode } from "@/types/routing";

const fallbackLanguage: LanguageCode = "zh-TW";

function pickLabel(labels: Partial<Record<LanguageCode, string>> | undefined, language: string, fallback: string) {
  const normalizedLanguage = language as LanguageCode;
  return labels?.[normalizedLanguage] ?? labels?.[fallbackLanguage] ?? fallback;
}

const versionStateLabels: Record<RoutingVersionStateCode, Partial<Record<LanguageCode, string>>> = {
  effective: { "zh-TW": "目前有效", en: "Effective", ja: "現在有効", vi: "Đang hiệu lực" },
  future: { "zh-TW": "未來生效", en: "Future", ja: "将来有効", vi: "Hiệu lực tương lai" },
  historical: { "zh-TW": "歷史版本", en: "Historical", ja: "履歴版", vi: "Phiên bản cũ" },
  warning: { "zh-TW": "待確認", en: "Needs review", ja: "確認待ち", vi: "Cần xác nhận" },
  unknown: { "zh-TW": "待確認", en: "Unknown", ja: "確認待ち", vi: "Chờ xác nhận" }
};

const mainProcessLabels: Record<number, Partial<Record<LanguageCode, string>>> = {
  0: { "zh-TW": "其他", en: "Other", ja: "その他", vi: "Khác" },
  1: { "zh-TW": "前備", en: "Preparation", ja: "前準備", vi: "Chuẩn bị" },
  2: { "zh-TW": "加工", en: "Processing", ja: "加工", vi: "Gia công" },
  3: { "zh-TW": "包裝", en: "Packaging", ja: "包装", vi: "Đóng gói" }
};

const subProcessLabels: Record<number, Partial<Record<LanguageCode, string>>> = {
  0: { "zh-TW": "其他", en: "Other", ja: "その他", vi: "Khác" },
  1: { "zh-TW": "調拌", en: "Mixing", ja: "混合", vi: "Trộn" },
  2: { "zh-TW": "塞料", en: "Filling prep", ja: "充填準備", vi: "Nạp liệu" },
  3: { "zh-TW": "烘烤", en: "Baking", ja: "焼成", vi: "Nướng" },
  4: { "zh-TW": "灌料", en: "Filling", ja: "充填", vi: "Chiết rót" }
};

const processingSubLabels: Record<number, Partial<Record<LanguageCode, string>>> = {
  0: subProcessLabels[0],
  1: { "zh-TW": "披覆", en: "Coating", ja: "コーティング", vi: "Phủ" },
  2: { "zh-TW": "封膜", en: "Sealing", ja: "シール", vi: "Ép màng" }
};

const packagingSubLabels: Record<number, Partial<Record<LanguageCode, string>>> = {
  0: subProcessLabels[0],
  1: { "zh-TW": "成組", en: "Kitting", ja: "セット組", vi: "Đóng bộ" },
  2: { "zh-TW": "入箱", en: "Cartoning", ja: "箱詰め", vi: "Đóng thùng" }
};

export function normalizeRoutingVersionStateCode(value?: string): RoutingVersionStateCode {
  if (value === "effective" || value === "future" || value === "historical" || value === "warning") {
    return value;
  }
  return "unknown";
}

export function routingVersionStateLabel(value?: string, language: string = fallbackLanguage) {
  const state = normalizeRoutingVersionStateCode(value);
  return pickLabel(versionStateLabels[state], language, state);
}

export function routingVersionStateTone(value?: string): StatusTone {
  const state = normalizeRoutingVersionStateCode(value);
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

export function routingMainProcessLabel(value?: number, language: string = fallbackLanguage) {
  return pickLabel(mainProcessLabels[value ?? 0], language, String(value ?? 0));
}

export function routingSubProcessLabel(oneProcess?: number, secProcess?: number, language: string = fallbackLanguage) {
  const labels = oneProcess === 2 ? processingSubLabels : oneProcess === 3 ? packagingSubLabels : subProcessLabels;
  return pickLabel(labels[secProcess ?? 0], language, String(secProcess ?? 0));
}
