"use client";

import {
  Beaker,
  Calculator,
  FileText,
  Filter,
  GitBranch,
  Search,
  TrendingUp
} from "lucide-react";
import { useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { AppLayout } from "@/layouts/app-layout";
import { rdProjects, rdSummary } from "@/mock/rd";
import type { RdDecision, RdProject, RdWorkspaceTab } from "@/types/rd";

const tabs: { id: RdWorkspaceTab; label: string }[] = [
  { id: "projects", label: "開發案" },
  { id: "bom-versions", label: "BOM 版本" },
  { id: "costing", label: "成本試算" },
  { id: "quotation", label: "報價基礎" }
];

const tabDescriptions: Record<RdWorkspaceTab, string> = {
  projects: "追蹤客戶需求、樣品、試作、報價與量產移轉階段。",
  "bom-versions": "管理開發版、試作版、報價版與量產版 BOM，避免接單引用錯誤版本。",
  costing: "拆解原料、物料、包材、人工、製造費用、物流與耗損率的單品成本。",
  quotation: "以目標毛利、最低報價與建議報價支援 ODM 食品加工報價管理。"
};

function formatMoney(value: number) {
  return `$${new Intl.NumberFormat("zh-TW", { maximumFractionDigits: 1 }).format(value)}`;
}

function decisionTone(decision: RdDecision) {
  if (decision === "暫緩") return "danger";
  if (decision === "需調整") return "warning";
  return "success";
}

function getVisibleProjects(activeTab: RdWorkspaceTab) {
  if (activeTab === "bom-versions") {
    return [...rdProjects].sort((a, b) => a.bomStatus.localeCompare(b.bomStatus, "zh-TW"));
  }
  if (activeTab === "costing") {
    return [...rdProjects].sort((a, b) => b.totalUnitCost - a.totalUnitCost);
  }
  if (activeTab === "quotation") {
    return [...rdProjects].sort((a, b) => a.estimatedMarginRate - b.estimatedMarginRate);
  }
  return rdProjects;
}

function KpiStrip() {
  const icons = [Beaker, GitBranch, Calculator, TrendingUp];

  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {rdSummary.map((item, index) => {
        const Icon = icons[index] ?? Beaker;
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

function RdTable({
  activeTab,
  selectedId,
  onSelect
}: {
  activeTab: RdWorkspaceTab;
  selectedId: string;
  onSelect: (item: RdProject) => void;
}) {
  const rows = useMemo(() => getVisibleProjects(activeTab), [activeTab]);

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[1180px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">開發案 / 客戶</th>
              <th className="px-4 py-3">產品</th>
              <th className="px-4 py-3">BOM</th>
              <th className="px-4 py-3 text-right">單品成本</th>
              <th className="px-4 py-3">毛利</th>
              <th className="px-4 py-3">報價</th>
              <th className="px-4 py-3">階段</th>
              <th className="px-4 py-3">判定</th>
              <th className="px-4 py-3">負責</th>
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
                    <p className="font-semibold text-textPrimary">{item.id}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.customer} · {item.targetChannel}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="font-medium text-textPrimary">{item.productName}</p>
                    <p className="mt-1 text-xs text-textSecondary">上市 {item.targetLaunchDate}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{item.bomNo}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.bomVersion} · {item.bomStatus}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">{formatMoney(item.totalUnitCost)}</td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">目標 {item.targetMarginRate}%</p>
                    <p className="mt-1 text-xs text-textSecondary">預估 {item.estimatedMarginRate}%</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">建議 {formatMoney(item.suggestedQuote)}</p>
                    <p className="mt-1 text-xs text-textSecondary">最低 {formatMoney(item.minimumQuote)}</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={item.tone}>{item.stage}</StatusBadge>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={decisionTone(item.decision)}>{item.decision}</StatusBadge>
                    <p className="mt-1 line-clamp-2 text-xs text-textSecondary">{item.quoteRiskReason}</p>
                  </td>
                  <td className="px-4 py-3 text-textPrimary">{item.owner}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function CostingCards() {
  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {rdProjects.map((item) => (
        <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.id}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <StatusBadge tone={decisionTone(item.decision)}>{item.decision}</StatusBadge>
              <h3 className="mt-3 font-semibold text-textPrimary">{item.productName}</h3>
              <p className="mt-1 text-sm text-textSecondary">{item.bomVersion} · {item.bomStatus}</p>
            </div>
            <Calculator className="h-5 w-5 text-textSecondary" aria-hidden="true" />
          </div>
          <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">單品成本</p>
              <p className="mt-1 font-semibold text-textPrimary">{formatMoney(item.totalUnitCost)}</p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">預估毛利</p>
              <p className="mt-1 font-semibold text-textPrimary">{item.estimatedMarginRate}%</p>
            </div>
          </div>
          <p className="mt-3 text-xs leading-5 text-textSecondary">{item.quoteRiskReason}</p>
        </div>
      ))}
    </div>
  );
}

function DetailPanel({ item }: { item: RdProject }) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">目前開發案</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{item.productName}</h2>
          <p className="mt-1 text-sm text-textSecondary">{item.id} · {item.customer}</p>
        </div>
        <StatusBadge tone={decisionTone(item.decision)}>{item.decision}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">建議報價</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(item.suggestedQuote)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">最低報價</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(item.minimumQuote)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">單品成本</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(item.totalUnitCost)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">預估毛利</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.estimatedMarginRate}%</p>
        </div>
      </div>

      <div className="rounded-md bg-slate-50 p-3 text-sm">
        <p className="text-xs text-textSecondary">報價判斷</p>
        <p className="mt-1 leading-6 text-textPrimary">{item.quoteRiskReason}</p>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">成本明細</p>
        {item.costLines.map((line) => (
          <div className="rounded-md border border-border px-3 py-2" key={`${line.category}-${line.itemName}`}>
            <div className="flex items-center justify-between gap-3">
              <p className="font-medium text-textPrimary">{line.category} · {line.itemName}</p>
              <StatusBadge tone={line.tone}>{formatMoney(line.costAmount)}</StatusBadge>
            </div>
            <p className="mt-1 text-xs text-textSecondary">
              {line.version} · 用量 {line.usageQty} · 損耗 {line.lossRate}% · {line.note}
            </p>
          </div>
        ))}
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">研發流程</p>
        {item.workflow.map((step, index) => (
          <div className="flex gap-3" key={`${step.label}-${step.ref}`}>
            <div className="flex flex-col items-center">
              <span
                className={`grid h-6 w-6 place-items-center rounded-full text-xs font-bold ${
                  step.tone === "success"
                    ? "bg-success text-white"
                    : step.tone === "danger"
                      ? "bg-danger text-white"
                      : step.tone === "warning"
                        ? "bg-warning text-white"
                        : "bg-info text-white"
                }`}
              >
                {index + 1}
              </span>
              {index < item.workflow.length - 1 ? <span className="h-7 w-px bg-border" /> : null}
            </div>
            <div className="min-w-0 pb-2">
              <div className="flex flex-wrap items-center gap-2">
                <p className="font-medium text-textPrimary">{step.label}</p>
                <StatusBadge tone={step.tone}>{step.status}</StatusBadge>
              </div>
              <p className="mt-1 truncate text-xs text-textSecondary">{step.ref}</p>
            </div>
          </div>
        ))}
      </div>
    </aside>
  );
}

function MainContent({
  activeTab,
  selectedProject,
  onSelectProject
}: {
  activeTab: RdWorkspaceTab;
  selectedProject: RdProject;
  onSelectProject: (item: RdProject) => void;
}) {
  if (activeTab === "costing" || activeTab === "quotation") {
    return (
      <div className="space-y-4">
        <CostingCards />
        <RdTable activeTab={activeTab} selectedId={selectedProject.id} onSelect={onSelectProject} />
      </div>
    );
  }

  return <RdTable activeTab={activeTab} selectedId={selectedProject.id} onSelect={onSelectProject} />;
}

export default function RdPage() {
  const [activeTab, setActiveTab] = useState<RdWorkspaceTab>("projects");
  const [selectedProject, setSelectedProject] = useState<RdProject>(rdProjects[0]);

  return (
    <AppLayout activePath="/rd" title="產品研發與成本試算 R&D / Costing">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">ODM Food Manufacturing</StatusBadge>
                <StatusBadge tone="neutral">研發 / BOM / 成本 / 報價</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">產品研發、BOM 版本與報價成本總覽</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                以客戶需求與試作開發為起點，管理配方/BOM 版本、單品成本、損耗率、目標毛利與建議報價，
                作為後續 Orders、Planning、Production 與 Finance 的源頭依據。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  placeholder="開發案 / 客戶 / 產品 / BOM"
                />
              </label>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary">
                <Filter className="h-4 w-4" aria-hidden="true" />
                篩選
              </button>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white">
                <FileText className="h-4 w-4" aria-hidden="true" />
                報價
              </button>
            </div>
          </div>
        </section>

        <KpiStrip />

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="space-y-4">
            <div className="rounded-lg border border-border bg-white p-3 shadow-card">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">研發視圖</p>
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

            <MainContent
              activeTab={activeTab}
              selectedProject={selectedProject}
              onSelectProject={setSelectedProject}
            />
          </div>

          <DetailPanel item={selectedProject} />
        </section>
      </div>
    </AppLayout>
  );
}
