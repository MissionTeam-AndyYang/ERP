import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { LanguageProvider } from "@/i18n/language-provider";
import type { Fm01Hierarchy } from "@/types/fm01-organization-location";
import type * as Fm01Api from "@/services/fm01-organization-location-api";

vi.mock("next/link", () => ({ default: ({ children, href, ...props }: { children: React.ReactNode; href: string }) => <a href={href} {...props}>{children}</a> }));
vi.mock("@/services/fm01-organization-location-api", async (importOriginal) => {
  const actual = await importOriginal<typeof Fm01Api>();
  return { ...actual, getFm01Hierarchy: vi.fn(), getFm01Record: vi.fn() };
});
vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams("resource=warehouses&id=5&operation=deactivate") }));

import OrganizationLocationCreatePage from "@/app/settings/organization-location/create/page";
import OrganizationLocationWorkflowPage from "@/app/settings/organization-location/workflow/page";
import { Fm01ApiError, getFm01Hierarchy, getFm01Record } from "@/services/fm01-organization-location-api";

const emptyHierarchy: Fm01Hierarchy = {
  "legal-entities": [],
  companies: [],
  sites: [],
  plants: [],
  warehouses: [],
  locations: []
};

const warehouse = {
  resource: "warehouses" as const,
  id: 5,
  ref: "WH-005",
  displayName: "倉庫一",
  relations: { site_id: 3, plant_id: 4 }
};

function renderPage(element: React.ReactElement) {
  return render(<LanguageProvider>{element}</LanguageProvider>);
}

describe("FM-01 page boundaries", () => {
  beforeEach(() => vi.resetAllMocks());

  it("shows create validation and never enables the submit mutation", async () => {
    vi.mocked(getFm01Hierarchy).mockResolvedValue(emptyHierarchy);
    renderPage(<OrganizationLocationCreatePage />);
    await waitFor(() => expect(vi.mocked(getFm01Hierarchy)).toHaveBeenCalledOnce());

    fireEvent.click(screen.getByRole("button", { name: "檢查欄位" }));
    expect(screen.getByRole("alert")).toHaveTextContent("請先修正以下欄位");
    expect(screen.getByRole("button", { name: "送出建立申請" })).toBeDisabled();
  });

  it("keeps parent selection unavailable when hierarchy loading fails", async () => {
    vi.mocked(getFm01Hierarchy).mockRejectedValue(new Fm01ApiError("NETWORK_UNAVAILABLE", undefined));
    renderPage(<OrganizationLocationCreatePage />);
    await waitFor(() => expect(screen.getByRole("alert")).toHaveTextContent("目前無法連線到後端"));

    fireEvent.change(screen.getByRole("combobox", { name: "資料類型" }), { target: { value: "warehouses" } });
    expect(document.getElementById("fm01-create-parent")).toBeDisabled();
    expect(screen.getByRole("button", { name: "送出建立申請" })).toBeDisabled();
  });

  it("renders workflow data and keeps all state-changing controls disabled", async () => {
    vi.mocked(getFm01Record).mockResolvedValue(warehouse);
    renderPage(<OrganizationLocationWorkflowPage />);
    await waitFor(() => expect(screen.getByRole("heading", { name: "倉庫一" })).toBeInTheDocument());

    expect(screen.getByRole("button", { name: "送交核准" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "核准" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "退回" })).toBeDisabled();
  });
});
