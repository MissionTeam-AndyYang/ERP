import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { FM02_C2_CUSTOMER_SCOPE_SENTINEL, fm02C2ItemReferenceMock } from "@/mock/fm02-c2";
import type {
  C2ConversionDraft,
  C2CustomerQualificationDraft,
  C2ItemReferenceData,
  C2ValidationError
} from "@/types/fm02-c2";

export const FM02_C2_UI_SCOPE_DECISION =
  "Product/Frontend acceptance of the C2 UI/API integration scope is not recorded; only mock display, form, and contract-error states are safe. Live C2 API wiring and persistence remain blocked.";

export type C2ReferenceResult = {
  data?: C2ItemReferenceData;
  source: "mock" | "blocked";
  error?: string;
};

export async function getItemC2Reference(itemId: string, dataSourceMode: DataSourceMode): Promise<C2ReferenceResult> {
  if (dataSourceMode !== "mock") {
    return {
      source: "blocked",
      error: "C2 API 尚未接入目前的主資料 runtime；依契約不呼叫 live API。"
    };
  }

  const data = fm02C2ItemReferenceMock[itemId];
  return data
    ? { data, source: "mock" }
    : { source: "mock", error: "示範資料中找不到此品項的 C2 參考資料。" };
}

export function validateC2ConversionDraft(
  draft: C2ConversionDraft,
  itemUomIds: string[]
): C2ValidationError[] {
  const errors: C2ValidationError[] = [];
  if (!draft.fromItemUomId) errors.push({ field: "fromItemUomId", message: "必須選擇來源 Item UOM。" });
  if (!draft.toItemUomId) errors.push({ field: "toItemUomId", message: "必須選擇目的 Item UOM。" });
  if (draft.fromItemUomId && draft.fromItemUomId === draft.toItemUomId) {
    errors.push({ field: "toItemUomId", message: "轉換端點必須不同。" });
  }
  if (draft.fromItemUomId && !itemUomIds.includes(draft.fromItemUomId)) {
    errors.push({ field: "fromItemUomId", message: "來源 UOM 必須屬於此 Item。" });
  }
  if (draft.toItemUomId && !itemUomIds.includes(draft.toItemUomId)) {
    errors.push({ field: "toItemUomId", message: "目的 UOM 必須屬於此 Item。" });
  }
  if (!draft.effectiveFrom) errors.push({ field: "effectiveFrom", message: "必須填寫生效時間。" });
  if (!draft.sourceReference.trim()) errors.push({ field: "sourceReference", message: "必須填寫來源參照。" });
  const conversionFactor = Number(draft.conversionFactor);
  if (draft.conversionType === "FIXED" && (!draft.conversionFactor || !Number.isFinite(conversionFactor) || conversionFactor <= 0)) {
    errors.push({ field: "conversionFactor", message: "FIXED 轉換必須填寫正數 conversion factor。" });
  }
  if (draft.conversionType === "CATCH_WEIGHT" && draft.conversionFactor) {
    errors.push({ field: "conversionFactor", message: "CATCH_WEIGHT 不接受固定 conversion factor。" });
  }
  return errors;
}

export function validateC2CustomerQualificationDraft(
  draft: C2CustomerQualificationDraft
): C2ValidationError[] {
  const errors: C2ValidationError[] = [];
  if (!draft.customerRef.trim()) errors.push({ field: "customerRef", message: "必須填寫 customer reference。" });
  if (!draft.supplyMethod.trim()) errors.push({ field: "supplyMethod", message: "必須填寫供應方式。" });
  if (!draft.effectiveFrom) errors.push({ field: "effectiveFrom", message: "必須填寫生效時間。" });
  if (!draft.sourceReference.trim()) errors.push({ field: "sourceReference", message: "必須填寫來源參照。" });
  if (draft.approvalScope === "SPECIFIC_SUPPLIER" && !draft.supplierQualificationId.trim()) {
    errors.push({ field: "supplierQualificationId", message: "指定供應商範圍必須填寫 Item-scoped supplier qualification。" });
  }
  if (draft.supplierQualificationId.trim() === FM02_C2_CUSTOMER_SCOPE_SENTINEL) {
    errors.push({ field: "supplierQualificationId", message: "保留 scope sentinel 不可作為實際 qualification。" });
  }
  if (draft.approvalScope === "ANY_GENERAL_QUALIFIED_SUPPLIER" && draft.supplierQualificationId.trim()) {
    errors.push({ field: "supplierQualificationId", message: "一般合格供應商範圍的 supplier qualification 必須留白。" });
  }
  return errors;
}
