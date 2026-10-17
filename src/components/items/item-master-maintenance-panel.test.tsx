import { describe, expect, it } from "vitest";
import { validateItemMasterDraft } from "@/components/items/item-master-maintenance-panel";
import type { ItemMasterDraft } from "@/types/item-master-governance";

const validDraft: ItemMasterDraft = {
  displayName: "不鏽鋼板",
  primaryCategory: "MATERIAL",
  ownershipContext: "COMPANY_PURCHASED",
  baseUomCode: "KG",
  description: "",
  specificationSummary: "SUS304",
  specificationReference: "SPEC-001",
  specificationEffectiveFrom: "2026-10-17T00:00",
  specificationEffectiveTo: "",
  conversionFromUomCode: "KG",
  conversionToUomCode: "G",
  conversionMode: "FIXED",
  conversionFactor: "1000",
  conversionDecimalScale: "2",
  conversionRoundingMode: "HALF_UP",
  conversionEffectiveFrom: "2026-10-17T00:00",
  conversionEffectiveTo: ""
};

describe("validateItemMasterDraft", () => {
  it("rejects missing required master fields", () => {
    const errors = validateItemMasterDraft({ ...validDraft, displayName: "", primaryCategory: "", ownershipContext: "", baseUomCode: "公斤" });

    expect(errors.displayName).toBeDefined();
    expect(errors.primaryCategory).toBeDefined();
    expect(errors.ownershipContext).toBeDefined();
    expect(errors.baseUomCode).toBeDefined();
  });

  it("rejects changing a locked base UOM", () => {
    const errors = validateItemMasterDraft({ ...validDraft, baseUomCode: "EA" }, {
      isEdit: true,
      originalBaseUomCode: "KG",
      baseUomLocked: true
    });

    expect(errors.baseUomCode).toContain("鎖定");
  });

  it("rejects a non-positive fixed conversion factor", () => {
    const errors = validateItemMasterDraft({ ...validDraft, conversionFactor: "0" });

    expect(errors.conversionFactor).toContain("大於 0");
  });

  it("requires authorization before using catch-weight conversion", () => {
    const errors = validateItemMasterDraft({ ...validDraft, conversionMode: "CATCH_WEIGHT", conversionFactor: "" });

    expect(errors.conversionMode).toContain("授權");
    expect(validateItemMasterDraft({ ...validDraft, conversionMode: "CATCH_WEIGHT", conversionFactor: "" }, { catchWeightAuthorized: true })).toEqual({});
  });
});
