import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { EditDrawer } from "@/components/fm01/organization-location/edit-drawer";
import { DetailPanel } from "@/components/fm01/organization-location/detail-panel";
import { HierarchyTree, buildFm01Hierarchy } from "@/components/fm01/organization-location/hierarchy-tree";
import { Fm01ApiError } from "@/services/fm01-organization-location-api";
import { LanguageProvider } from "@/i18n/language-provider";
import type { Fm01Hierarchy, Fm01Record } from "@/types/fm01-organization-location";

function record(resource: Fm01Record["resource"], id: number, displayName: string, relations: Fm01Record["relations"] = {}): Fm01Record {
  return { resource, id, ref: `${resource}-${id}`, displayName, relations };
}

function renderWithLanguage(element: React.ReactElement) {
  return render(<LanguageProvider>{element}</LanguageProvider>);
}

const hierarchy: Fm01Hierarchy = {
  "legal-entities": [record("legal-entities", 1, "法人一")],
  companies: [record("companies", 2, "公司一", { legal_entity_id: 1 })],
  sites: [record("sites", 3, "廠區一", { company_id: 2 })],
  plants: [record("plants", 4, "廠別一", { site_id: 3 })],
  warehouses: [record("warehouses", 5, "倉庫一", { site_id: 3, plant_id: 4 })],
  locations: [record("locations", 6, "庫位一", { warehouse_id: 5, parent_location_id: null })]
};

describe("FM-01 organization/location components", () => {
  it("builds and renders the hierarchy, then emits the selected record", () => {
    const onSelect = vi.fn();
    const nodes = buildFm01Hierarchy(hierarchy);

    renderWithLanguage(
      <HierarchyTree
        nodes={nodes}
        query=""
        expanded={new Set(["legal-entities:1", "companies:2", "sites:3"])}
        onToggle={vi.fn()}
        onSelect={onSelect}
      />
    );

    expect(screen.getByText("公司一")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /倉庫一倉庫/ }));
    expect(onSelect).toHaveBeenCalledWith(expect.objectContaining({ id: 5, resource: "warehouses" }));
  });

  it("renders an empty hierarchy without inventing rows", () => {
    const { container } = renderWithLanguage(
      <HierarchyTree nodes={[]} query="" expanded={new Set()} onToggle={vi.fn()} onSelect={vi.fn()} />
    );

    expect(container).toBeEmptyDOMElement();
  });

  it("covers detail loading, error, empty and successful states", () => {
    const onRetry = vi.fn();
    const onEdit = vi.fn();
    const { rerender } = renderWithLanguage(
      <DetailPanel record={null} isLoading error={undefined} onRetry={onRetry} onEdit={onEdit} />
    );
    expect(document.querySelector("section[aria-busy='true']")).toBeInTheDocument();

    const error = new Fm01ApiError("NETWORK_UNAVAILABLE", undefined);
    rerender(<LanguageProvider><DetailPanel record={null} isLoading={false} error={error} onRetry={onRetry} onEdit={onEdit} /></LanguageProvider>);
    expect(screen.getByRole("alert")).toHaveTextContent("目前無法連線到後端");
    fireEvent.click(screen.getByRole("button", { name: "重試" }));
    expect(onRetry).toHaveBeenCalledOnce();

    rerender(<LanguageProvider><DetailPanel record={null} isLoading={false} onRetry={onRetry} onEdit={onEdit} /></LanguageProvider>);
    expect(screen.getByText("選取一筆資料以查看詳細資訊。")).toBeInTheDocument();

    rerender(<LanguageProvider><DetailPanel record={hierarchy.warehouses[0]} hierarchy={hierarchy} isLoading={false} onRetry={onRetry} onEdit={onEdit} /></LanguageProvider>);
    expect(screen.getByRole("heading", { name: "倉庫一" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "編輯名稱" }));
    expect(onEdit).toHaveBeenCalledOnce();
  });

  it("keeps edit submission fail-closed and validates the local draft", () => {
    const onClose = vi.fn();
    renderWithLanguage(<EditDrawer record={hierarchy.warehouses[0]} hierarchy={hierarchy} onClose={onClose} />);

    const input = screen.getByRole("textbox", { name: /顯示名稱/ });
    expect(screen.getByRole("button", { name: "送出變更" })).toBeDisabled();
    fireEvent.change(input, { target: { value: "   " } });
    fireEvent.click(screen.getByRole("button", { name: "檢查欄位" }));

    expect(screen.getByRole("alert")).toHaveTextContent("顯示名稱不可空白。");
    expect(screen.getByRole("button", { name: "送出變更" })).toBeDisabled();
  });
});
