"use client";

import {
  AlertTriangle,
  ClipboardList,
  FileCheck2,
  Filter,
  PackageCheck,
  Search,
  ShoppingCart,
  Truck
} from "lucide-react";
import { useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { usePurchasingDashboard } from "@/hooks/use-purchasing-dashboard";
import { AppLayout } from "@/layouts/app-layout";
import type {
  PurchaseItem,
  PurchaseRiskLevel,
  PurchasingDashboardData,
  PurchasingSummary,
  PurchasingWorkspaceTab
} from "@/types/purchasing";

const tabs: { id: PurchasingWorkspaceTab; label: string }[] = [
  { id: "demand", label: "採購需求" },
  { id: "delivery-risk", label: "交期風險" },
  { id: "receiving", label: "到貨驗收入庫" },
  { id: "suppliers", label: "供應商追蹤" }
];

const tabDescriptions: Record<PurchasingWorkspaceTab, string> = {
  demand: "從訂單、工單、安全水位與可用庫存檢視哪些料品需要採購。",
  "delivery-risk": "集中查看會影響交期或生產開線的採購風險。",
  receiving: "追蹤今日到貨、驗收、品檢文件與入庫狀態。",
  suppliers: "查看供應商交期、文件、延遲與替代供應商決策事項。"
};

function formatNumber(value: number) {
  return new Intl.NumberFormat("zh-TW").format(value);
}

function formatMoney(value: number) {
  return `$${new Intl.NumberFormat("zh-TW").format(value)}`;
}

function riskTone(risk: PurchaseRiskLevel) {
  if (risk === "高風險") {
    return "danger";
  }

  if (risk === "注意") {
    return "warning";
  }

  return "success";
}

function getVisibleItems(activeTab: PurchasingWorkspaceTab, items: PurchaseItem[]) {
  if (activeTab === "delivery-risk") {
    return items.filter((item) => item.riskLevel !== "正常");
  }

  if (activeTab === "receiving") {
    return items.filter((item) => item.stage === "驗收中" || item.receivingStatus !== "待到貨");
  }

  if (activeTab === "suppliers") {
    return [...items].sort((a, b) => b.delayDays - a.delayDays);
  }

  return items;
}

function KpiStrip({ summary }: { summary: PurchasingSummary[] }) {
  const icons = [ShoppingCart, AlertTriangle, Truck, FileCheck2];

  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {summary.map((item, index) => {
        const Icon = icons[index] ?? ShoppingCart;
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

function PurchasingTable({
  activeTab,
  items,
  selectedId,
  onSelect
}: {
  activeTab: PurchasingWorkspaceTab;
  items: PurchaseItem[];
  selectedId: string;
  onSelect: (item: PurchaseItem) => void;
}) {
  const rows = useMemo(() => getVisibleItems(activeTab, items), [activeTab, items]);

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[1160px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">料品 / 需求</th>
              <th className="px-4 py-3">供應商</th>
              <th className="px-4 py-3 text-right">數量</th>
              <th className="px-4 py-3 text-right">金額</th>
              <th className="px-4 py-3">庫存可用性</th>
              <th className="px-4 py-3">需求來源</th>
              <th className="px-4 py-3">到貨/驗收</th>
              <th className="px-4 py-3">風險</th>
              <th className="px-4 py-3">狀態</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {rows.map((item) => {
              const isSelected = item.id === selectedId;
              return (
                <tr
                  className={`cursor-pointer transition ${
                    isSelected ? "bg-info/10" : "hover:bg-slate-50"
                  }`}
                  key={item.id}
                  onClick={() => onSelect(item)}
                >
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{item.itemName}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {item.itemNo} · {item.requestNo}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{item.supplier}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.purchaseOrderNo ?? "尚未下單"}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(item.quantity)} {item.unit}
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatMoney(item.amount)}</td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">
                      現有 {formatNumber(item.currentStock)} / 可用 {formatNumber(item.availableStock)}
                    </p>
                    <p className="mt-1 text-xs text-textSecondary">安全水位 {formatNumber(item.safetyStock)}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{item.sourceOrder ?? "安全水位補貨"}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.linkedWorkOrder ?? "未連工單"}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{item.expectedArrivalDate ?? "待確認"}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {item.receivingStatus} · 文件 {item.qualityDocumentStatus}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={riskTone(item.riskLevel)}>{item.riskLevel}</StatusBadge>
                    <p className="mt-1 line-clamp-2 text-xs text-textSecondary">{item.riskReason}</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={item.tone}>{item.stage}</StatusBadge>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function RiskCards({ items }: { items: PurchaseItem[] }) {
  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {items
        .filter((item) => item.riskLevel !== "正常")
        .map((item) => (
          <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.id}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <StatusBadge tone={riskTone(item.riskLevel)}>{item.riskLevel}</StatusBadge>
                <h3 className="mt-3 font-semibold text-textPrimary">{item.itemName}</h3>
                <p className="mt-1 text-sm text-textSecondary">{item.requestNo}</p>
              </div>
              <AlertTriangle className="h-5 w-5 text-textSecondary" aria-hidden="true" />
            </div>
            <p className="mt-3 text-sm leading-6 text-textSecondary">{item.riskReason}</p>
            <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
              <div className="rounded-md bg-slate-50 p-3">
                <p className="text-xs text-textSecondary">需求日</p>
                <p className="mt-1 font-semibold text-textPrimary">{item.requiredDate}</p>
              </div>
              <div className="rounded-md bg-slate-50 p-3">
                <p className="text-xs text-textSecondary">預計到貨</p>
                <p className="mt-1 font-semibold text-textPrimary">{item.expectedArrivalDate ?? "待確認"}</p>
              </div>
            </div>
          </div>
        ))}
    </div>
  );
}

function DetailPanel({ item }: { item: PurchaseItem }) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">目前採購</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{item.requestNo}</h2>
          <p className="mt-1 text-sm text-textSecondary">{item.itemName}</p>
        </div>
        <StatusBadge tone={riskTone(item.riskLevel)}>{item.riskLevel}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">採購金額</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(item.amount)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">到貨</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.expectedArrivalDate ?? "待確認"}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">現有/預留/可用</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(item.currentStock)} / {formatNumber(item.reservedStock)} /{" "}
            {formatNumber(item.availableStock)}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">文件</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.qualityDocumentStatus}</p>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">履約影響</p>
        {item.dependencies.map((dependency) => (
          <div className="rounded-md border border-border px-3 py-2" key={`${dependency.area}-${dependency.status}`}>
            <div className="flex items-center justify-between gap-3">
              <p className="font-medium text-textPrimary">{dependency.area}</p>
              <StatusBadge tone={dependency.tone}>{dependency.status}</StatusBadge>
            </div>
            <p className="mt-1 text-xs text-textSecondary">{dependency.note}</p>
          </div>
        ))}
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">採購流程</p>
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
  data,
  selectedItem,
  onSelectItem
}: {
  activeTab: PurchasingWorkspaceTab;
  data: PurchasingDashboardData;
  selectedItem: PurchaseItem;
  onSelectItem: (item: PurchaseItem) => void;
}) {
  if (activeTab === "delivery-risk") {
    return (
      <div className="space-y-4">
        <RiskCards items={data.items} />
        <PurchasingTable activeTab={activeTab} items={data.items} selectedId={selectedItem.id} onSelect={onSelectItem} />
      </div>
    );
  }

  return <PurchasingTable activeTab={activeTab} items={data.items} selectedId={selectedItem.id} onSelect={onSelectItem} />;
}

export default function PurchasingPage() {
  const { data: purchasingData, error, isLoading, source } = usePurchasingDashboard();
  const [activeTab, setActiveTab] = useState<PurchasingWorkspaceTab>("demand");
  const [selectedItemId, setSelectedItemId] = useState<string>(purchasingData.items[0].id);
  const selectedItem = purchasingData.items.find((item) => item.id === selectedItemId) ?? purchasingData.items[0];

  return (
    <AppLayout activePath="/purchasing" title="採購備料 Purchasing Workspace">
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
                <StatusBadge tone="neutral">採購需求 / 交期 / 驗收 / 供應商</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">採購與備料風險總覽</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                以訂單履約與生產開線為核心，追蹤低庫存、缺料、採購交期、品檢文件、
                到貨驗收與入庫，讓採購任務能提前支援生產與出貨。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  placeholder="料品 / 請購 / 採購單 / 供應商"
                />
              </label>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary">
                <Filter className="h-4 w-4" aria-hidden="true" />
                篩選
              </button>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white">
                <PackageCheck className="h-4 w-4" aria-hidden="true" />
                備料
              </button>
            </div>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Purchasing API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}

        <KpiStrip summary={purchasingData.summary} />

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="min-w-0 space-y-4">
            <div className="rounded-lg border border-border bg-white p-3 shadow-card">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">採購視圖</p>
                  <h3 className="mt-1 text-lg font-semibold text-textPrimary">
                    {tabs.find((tab) => tab.id === activeTab)?.label}
                  </h3>
                  <p className="mt-1 text-sm text-textSecondary">{tabDescriptions[activeTab]}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {tabs.map((tab) => (
                    <button
                      className={`h-9 rounded-button px-3 text-sm font-medium transition ${
                        activeTab === tab.id
                          ? "bg-primary text-white"
                          : "bg-slate-100 text-textSecondary hover:bg-slate-200"
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
              data={purchasingData}
              selectedItem={selectedItem}
              onSelectItem={(item) => setSelectedItemId(item.id)}
            />
          </div>

          <DetailPanel item={selectedItem} />
        </section>
      </div>
    </AppLayout>
  );
}
