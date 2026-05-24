"use client";

import { Filter, Globe2, KeyRound, Search, Settings, ShieldCheck } from "lucide-react";
import { useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { useSettingsDashboard } from "@/hooks/use-settings-dashboard";
import { AppLayout } from "@/layouts/app-layout";
import type {
  GovernanceRiskLevel,
  MasterDataItem,
  SettingsSummary,
  SettingsWorkspaceTab
} from "@/types/settings";

const tabs: { id: SettingsWorkspaceTab; label: string }[] = [
  { id: "master-data", label: "主檔治理" },
  { id: "permissions", label: "角色權限" },
  { id: "integrations", label: "系統串接" },
  { id: "localization", label: "語言/用詞" }
];

const tabDescriptions: Record<SettingsWorkspaceTab, string> = {
  "master-data": "檢視品項、BOM、客戶、供應商、倉位與產線等核心主檔完整性。",
  permissions: "追蹤角色權限、簽核範圍與高風險操作控制。",
  integrations: "管理資料庫、API、PDA、掃碼與外部系統串接基礎。",
  localization: "管理多國語言、現場用詞與跨語系顯示一致性。"
};

function riskTone(risk: GovernanceRiskLevel) {
  if (risk === "高風險") return "danger";
  if (risk === "注意") return "warning";
  return "success";
}

function getVisibleItems(activeTab: SettingsWorkspaceTab, items: MasterDataItem[]) {
  if (activeTab === "permissions") {
    return items.filter((item) => item.domain === "權限");
  }
  if (activeTab === "integrations") {
    return items.filter((item) => ["倉位", "產線"].includes(item.domain));
  }
  if (activeTab === "localization") {
    return items.filter((item) => item.domain === "語言");
  }
  return items;
}

function KpiStrip({ summary }: { summary: SettingsSummary[] }) {
  const icons = [Settings, ShieldCheck, KeyRound, Globe2];

  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {summary.map((item, index) => {
        const Icon = icons[index] ?? Settings;
        return (
          <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.label}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-sm font-medium text-textSecondary">{item.label}</p>
                <p className="mt-2 text-2xl font-semibold text-textPrimary">{item.value}</p>
              </div>
              <span className="grid h-10 w-10 place-items-center rounded-full bg-slate-100 text-textSecondary">
                <Icon className="h-5 w-5" aria-hidden="true" />
              </span>
            </div>
            <p className="mt-3 text-xs leading-5 text-textSecondary">{item.hint}</p>
          </div>
        );
      })}
    </section>
  );
}

function SettingsTable({
  activeTab,
  items,
  selectedId,
  onSelect
}: {
  activeTab: SettingsWorkspaceTab;
  items: MasterDataItem[];
  selectedId: string;
  onSelect: (item: MasterDataItem) => void;
}) {
  const rows = useMemo(() => getVisibleItems(activeTab, items), [activeTab, items]);

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[980px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">主檔</th>
              <th className="px-4 py-3">範圍</th>
              <th className="px-4 py-3">狀態</th>
              <th className="px-4 py-3">影響工作區</th>
              <th className="px-4 py-3">風險</th>
              <th className="px-4 py-3">負責</th>
              <th className="px-4 py-3">更新</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {rows.map((item) => {
              const isSelected = item.id === selectedId;
              return (
                <tr
                  className={`cursor-pointer transition ${isSelected ? "bg-info/10" : "hover:bg-slate-50"}`}
                  key={item.id}
                  onClick={() => onSelect(item)}
                >
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{item.name}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.id}</p>
                  </td>
                  <td className="px-4 py-3 text-textPrimary">{item.domain}</td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={item.tone}>{item.status}</StatusBadge>
                  </td>
                  <td className="px-4 py-3 text-textPrimary">{item.affectedWorkspaces.join(" / ")}</td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={riskTone(item.riskLevel)}>{item.riskLevel}</StatusBadge>
                    <p className="mt-1 line-clamp-2 text-xs text-textSecondary">{item.riskReason}</p>
                  </td>
                  <td className="px-4 py-3 text-textPrimary">{item.owner}</td>
                  <td className="px-4 py-3 text-textSecondary">{item.lastUpdated}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function DetailPanel({ item }: { item: MasterDataItem }) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">目前主檔</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{item.name}</h2>
          <p className="mt-1 text-sm text-textSecondary">{item.id}</p>
        </div>
        <StatusBadge tone={riskTone(item.riskLevel)}>{item.riskLevel}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">範圍</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.domain}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">狀態</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.status}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">負責</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.owner}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">更新</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.lastUpdated}</p>
        </div>
      </div>

      <div className="rounded-md bg-slate-50 p-3 text-sm">
        <p className="text-xs text-textSecondary">風險說明</p>
        <p className="mt-1 leading-6 text-textPrimary">{item.riskReason}</p>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">影響工作區</p>
        {item.affectedWorkspaces.map((workspace) => (
          <div className="rounded-md border border-border px-3 py-2" key={workspace}>
            <p className="font-medium text-textPrimary">{workspace}</p>
            <p className="mt-1 text-xs text-textSecondary">此主檔會影響該工作區的資料正確性與流程判斷。</p>
          </div>
        ))}
      </div>
    </aside>
  );
}

export default function SettingsPage() {
  const { data: settingsData, error, isLoading, source } = useSettingsDashboard();
  const [activeTab, setActiveTab] = useState<SettingsWorkspaceTab>("master-data");
  const [selectedItemId, setSelectedItemId] = useState<string>(settingsData.items[0].id);
  const selectedItem = settingsData.items.find((item) => item.id === selectedItemId) ?? settingsData.items[0];

  return (
    <AppLayout activePath="/settings" title="主檔設定 Master Data / Settings">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">EWDB 20260522</StatusBadge>
                <StatusBadge tone={source === "api" ? "success" : "warning"}>
                  {source === "api" ? "API data" : "Mock fallback"}
                </StatusBadge>
                {isLoading ? <StatusBadge tone="info">Loading API</StatusBadge> : null}
                <StatusBadge tone="neutral">主檔 / 權限 / 串接 / 語言</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">主檔治理與系統設定總覽</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                集中管理品項、BOM、客戶、供應商、倉位、產線、權限與多國語言基礎資料，
                確保各核心工作區的判斷規則與資料來源一致。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  placeholder="主檔 / 權限 / 工作區 / 負責人"
                />
              </label>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary">
                <Filter className="h-4 w-4" aria-hidden="true" />
                篩選
              </button>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white">
                <Settings className="h-4 w-4" aria-hidden="true" />
                設定
              </button>
            </div>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Settings API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}

        <KpiStrip summary={settingsData.summary} />

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="space-y-4">
            <div className="rounded-lg border border-border bg-white p-3 shadow-card">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">設定視圖</p>
                  <h3 className="mt-1 text-lg font-semibold text-textPrimary">
                    {tabs.find((tab) => tab.id === activeTab)?.label}
                  </h3>
                  <p className="mt-1 text-sm text-textSecondary">{tabDescriptions[activeTab]}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {tabs.map((tab) => (
                    <button
                      className={`h-9 rounded-button px-3 text-sm font-medium transition ${
                        activeTab === tab.id ? "bg-primary text-white" : "bg-slate-100 text-textSecondary hover:bg-slate-200"
                      }`}
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      type="button"
                    >
                      {tab.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <SettingsTable
              activeTab={activeTab}
              items={settingsData.items}
              selectedId={selectedItem.id}
              onSelect={(item) => setSelectedItemId(item.id)}
            />
          </div>

          <DetailPanel item={selectedItem} />
        </section>
      </div>
    </AppLayout>
  );
}
