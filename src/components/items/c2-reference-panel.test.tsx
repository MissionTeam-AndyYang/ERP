import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { C2ReferencePanel } from "@/components/items/c2-reference-panel";
import type { C2ItemReferenceData } from "@/types/fm02-c2";

const { mockGetItemC2Reference } = vi.hoisted(() => ({
  mockGetItemC2Reference: vi.fn()
}));

vi.mock("@/services/fm02-c2-api", async () => {
  const actual = await vi.importActual<typeof import("@/services/fm02-c2-api")>("@/services/fm02-c2-api");
  return { ...actual, getItemC2Reference: mockGetItemC2Reference };
});

const happyPathData: C2ItemReferenceData = {
  itemId: "RM-001",
  itemUoms: [
    { id: "RM-001-UOM-KG", code: "KG", label: "公斤", role: "STOCK" },
    { id: "RM-001-UOM-BOX", code: "BOX", label: "盒", role: "PRODUCTION" }
  ],
  conversionRules: [
    {
      id: "C2-CONV-RM-001-001",
      itemId: "RM-001",
      fromItemUomId: "RM-001-UOM-KG",
      toItemUomId: "RM-001-UOM-BOX",
      conversionType: "FIXED",
      conversionFactor: "2.5",
      lifecycleStatus: "ACTIVE",
      effectiveFrom: "2026-01-01T00:00:00",
      sourceReference: "frontend-test"
    }
  ],
  customerQualifications: [
    {
      id: "C2-CQ-RM-001-001",
      itemId: "RM-001",
      customerRef: "CUSTOMER-A",
      supplierQualificationScopeKey: "00000000-0000-0000-0000-000000000000",
      approvalScope: "ANY_GENERAL_QUALIFIED_SUPPLIER",
      supplyMethod: "PURCHASED",
      qualificationStatus: "ACTIVE",
      effectiveFrom: "2026-01-01T00:00:00",
      sourceReference: "frontend-test"
    }
  ],
  packageState: "NOT_AVAILABLE",
  legacyMappingState: "NOT_AVAILABLE"
};

const missingBomData: C2ItemReferenceData = {
  itemId: "FG-MISSING-BOM",
  itemUoms: [{ id: "FG-MISSING-BOM-UOM-BOX", code: "BOX", label: "盒", role: "STOCK" }],
  conversionRules: [],
  customerQualifications: [],
  packageState: "NOT_AVAILABLE",
  legacyMappingState: "NOT_AVAILABLE"
};

function renderPanel(itemId = "RM-001", dataSourceMode: "api" | "mock" = "mock") {
  render(<C2ReferencePanel itemId={itemId} dataSourceMode={dataSourceMode} />);
}

async function waitForData() {
  expect(await screen.findByText("CUSTOMER-A")).toBeInTheDocument();
}

describe("C2ReferencePanel", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockGetItemC2Reference.mockResolvedValue({ data: happyPathData, source: "mock" });
  });

  it("renders item-scoped UOM, conversion, and qualification data", async () => {
    renderPanel();

    await waitForData();

    expect(screen.getByText("公斤")).toBeInTheDocument();
    expect(screen.getByText("盒")).toBeInTheDocument();
    expect(screen.getByText("公斤 → 盒")).toBeInTheDocument();
    expect(screen.getAllByText("啟用")).toHaveLength(2);
    expect(mockGetItemC2Reference).toHaveBeenCalledWith("RM-001", "mock");
  });

  it("shows explicit empty states for an item without BOM-scoped C2 rows", async () => {
    mockGetItemC2Reference.mockResolvedValue({ data: missingBomData, source: "mock" });
    renderPanel("FG-MISSING-BOM");

    expect(await screen.findByText("沒有可解析的 Item-specific conversion rule；不使用全域換算 fallback。")).toBeInTheDocument();
    expect(screen.getByText("目前沒有 customer qualification 示範資料。")).toBeInTheDocument();
    expect(screen.queryByText("CUSTOMER-A")).not.toBeInTheDocument();
  });

  it("renders the API-blocked state without attempting a live request", async () => {
    mockGetItemC2Reference.mockResolvedValue({
      source: "blocked",
      error: "C2 API 尚未接入目前的主資料 runtime；依契約不呼叫 live API。"
    });
    renderPanel("RM-001", "api");

    expect(await screen.findByText(/C2 API 尚未接入/)).toBeInTheDocument();
    expect(screen.getByText("API blocked")).toBeInTheDocument();
    expect(screen.queryByText("Item UOM")).not.toBeInTheDocument();
    expect(mockGetItemC2Reference).toHaveBeenCalledWith("RM-001", "api");
  });

  it("validates a fixed conversion and accepts a positive factor", async () => {
    renderPanel();
    await waitForData();
    fireEvent.click(screen.getAllByRole("button", { name: "新增示範" })[0]);

    fireEvent.click(screen.getByRole("button", { name: "執行示範驗證" }));
    expect(screen.getByRole("alert")).toHaveTextContent("conversionFactor");

    fireEvent.change(screen.getByLabelText("Conversion factor（FIXED）"), { target: { value: "2.5" } });
    fireEvent.click(screen.getByRole("button", { name: "執行示範驗證" }));
    expect(screen.getByText(/示範驗證通過/)).toBeInTheDocument();
  });

  it("supports catch-weight conversion without a fixed factor", async () => {
    renderPanel();
    await waitForData();
    fireEvent.click(screen.getAllByRole("button", { name: "新增示範" })[0]);

    const factorInput = screen.getByLabelText("Conversion factor（FIXED）");
    fireEvent.change(screen.getByLabelText("轉換類型"), { target: { value: "CATCH_WEIGHT" } });

    expect(factorInput).toBeDisabled();
    expect(factorInput).toHaveValue("");
    fireEvent.click(screen.getByRole("button", { name: "執行示範驗證" }));
    expect(screen.getByText(/示範驗證通過/)).toBeInTheDocument();
  });

  it("validates qualification scope and keeps supplier scope item-scoped", async () => {
    renderPanel();
    await waitForData();
    fireEvent.click(screen.getAllByRole("button", { name: "新增示範" })[1]);

    fireEvent.click(screen.getByRole("button", { name: "執行示範驗證" }));
    expect(screen.getByRole("alert")).toHaveTextContent("customerRef");

    const scopeSelect = screen.getByLabelText("Approval scope");
    const supplierInput = screen.getByLabelText(/Supplier qualification/);
    fireEvent.change(scopeSelect, { target: { value: "SPECIFIC_SUPPLIER" } });
    expect(supplierInput).not.toBeDisabled();
    fireEvent.click(screen.getByRole("button", { name: "執行示範驗證" }));
    expect(screen.getByRole("alert")).toHaveTextContent("supplierQualificationId");

    fireEvent.change(screen.getByLabelText("Customer reference"), { target: { value: "CUSTOMER-B" } });
    fireEvent.change(supplierInput, { target: { value: "00000000-0000-0000-0000-000000000000" } });
    fireEvent.click(screen.getByRole("button", { name: "執行示範驗證" }));
    expect(screen.getByRole("alert")).toHaveTextContent("保留 scope sentinel");

    fireEvent.change(supplierInput, { target: { value: "SUP-001" } });
    fireEvent.click(screen.getByRole("button", { name: "執行示範驗證" }));
    expect(screen.getByText(/示範驗證通過/)).toBeInTheDocument();

    fireEvent.change(scopeSelect, { target: { value: "ANY_GENERAL_QUALIFIED_SUPPLIER" } });
    expect(supplierInput).toBeDisabled();
    fireEvent.click(screen.getByRole("button", { name: "執行示範驗證" }));
    expect(screen.getByText(/示範驗證通過/)).toBeInTheDocument();
  });
});
