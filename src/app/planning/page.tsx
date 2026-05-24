"use client";

import {
  AlertTriangle,
  CalendarRange,
  ClipboardCheck,
  Factory,
  Filter,
  PackageCheck,
  Search,
  ShoppingCart
} from "lucide-react";
import { useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { usePlanningDashboard } from "@/hooks/use-planning-dashboard";
import { AppLayout } from "@/layouts/app-layout";
import type {
  PlanningCase,
  PlanningDashboardData,
  PlanningDecision,
  PlanningSummary,
  PlanningWorkspaceTab
} from "@/types/planning";

const tabs: { id: PlanningWorkspaceTab; label: string }[] = [
  { id: "demand", label: "需求展開" },
  { id: "materials", label: "物料/請購" },
  { id: "capacity", label: "產能/人員" },
  { id: "work-orders", label: "工單建議" }
];

const tabDescriptions: Record<PlanningWorkspaceTab, string> = {
  demand: "承接 Orders 的接單承諾，將訂單需求展開成物料、產能、品保與出貨條件。",
  materials: "檢視 BOM 展開後的缺料、可用庫存、批號阻擋與請購建議。",
  capacity: "檢視各製程產線可用工時、人員需求、換線時間與產能衝突。",
  "work-orders": "彙整可建立或需調整的工單建議，作為下一步排程與現場執行基礎。"
};

function formatNumber(value: number) {
  return new Intl.NumberFormat("zh-TW").format(value);
}

function formatMoney(value: number) {
  return `$${new Intl.NumberFormat("zh-TW").format(value)}`;
}

function decisionTone(decision: PlanningDecision) {
  if (decision === "不可執行") {
    return "danger";
  }

  if (decision === "需協調") {
    return "warning";
  }

  return "success";
}

function getVisibleCases(activeTab: PlanningWorkspaceTab, cases: PlanningCase[]) {
  if (activeTab === "materials") {
    return cases.filter((item) => item.materials.some((material) => material.shortageQty > 0));
  }

  if (activeTab === "capacity") {
    return cases.filter((item) => item.capacity.some((capacity) => capacity.requiredHours > capacity.availableHours));
  }

  if (activeTab === "work-orders") {
    return cases.filter((item) => item.suggestedWorkOrderCount > 0 || item.workOrders.length > 0);
  }

  return cases;
}

function KpiStrip({ summary }: { summary: PlanningSummary[] }) {
  const icons = [CalendarRange, ShoppingCart, AlertTriangle, ClipboardCheck];

  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {summary.map((item, index) => {
        const Icon = icons[index] ?? CalendarRange;
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

function PlanningTable({
  activeTab,
  cases,
  selectedId,
  onSelect
}: {
  activeTab: PlanningWorkspaceTab;
  cases: PlanningCase[];
  selectedId: string;
  onSelect: (item: PlanningCase) => void;
}) {
  const rows = useMemo(() => getVisibleCases(activeTab, cases), [activeTab, cases]);

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[1180px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">計劃 / 訂單</th>
              <th className="px-4 py-3">產品</th>
              <th className="px-4 py-3 text-right">需求量</th>
              <th className="px-4 py-3">交期</th>
              <th className="px-4 py-3">計劃判定</th>
              <th className="px-4 py-3 text-right">缺料金額</th>
              <th className="px-4 py-3">產能</th>
              <th className="px-4 py-3">請購/工單</th>
              <th className="px-4 py-3">負責</th>
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
                    <p className="font-semibold text-textPrimary">{item.id}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.sourceOrder}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="font-medium text-textPrimary">{item.product}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.customer} · {item.itemNo}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(item.quantity)} {item.unit}
                  </td>
                  <td className="px-4 py-3">
                    <p className="font-medium text-textPrimary">{item.dueDate}</p>
                    <p className="mt-1 text-xs text-textSecondary">承諾 {item.promisedDate}</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={decisionTone(item.decision)}>{item.decision}</StatusBadge>
                    <p className="mt-1 line-clamp-2 text-xs text-textSecondary">{item.planningNote}</p>
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatMoney(item.materialShortageValue)}</td>
                  <td className="px-4 py-3">
                    <p className="font-medium text-textPrimary">
                      {item.requiredProductionHours} / {item.availableProductionHours} 小時
                    </p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {item.capacity.length} 條產線檢核
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">請購 {item.purchaseRequestCount} 張</p>
                    <p className="mt-1 text-xs text-textSecondary">工單 {item.suggestedWorkOrderCount} 張</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{item.owner}</p>
                    <p className="mt-1 text-xs text-textSecondary">優先 {item.priority}</p>
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

function MaterialCards({ cases }: { cases: PlanningCase[] }) {
  const shortageMaterials = cases.flatMap((item) =>
    item.materials
      .filter((material) => material.shortageQty > 0 || material.suggestedAction !== "直接備料")
      .map((material) => ({ ...material, planningId: item.id, sourceOrder: item.sourceOrder }))
  );

  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {shortageMaterials.map((item) => (
        <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={`${item.planningId}-${item.itemNo}`}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <StatusBadge tone={item.tone}>{item.suggestedAction}</StatusBadge>
              <h3 className="mt-3 font-semibold text-textPrimary">{item.itemName}</h3>
              <p className="mt-1 text-sm text-textSecondary">{item.itemNo} · {item.sourceOrder}</p>
            </div>
            <PackageCheck className="h-5 w-5 text-textSecondary" aria-hidden="true" />
          </div>
          <div className="mt-3 grid grid-cols-3 gap-2 text-sm">
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">需求</p>
              <p className="mt-1 font-semibold text-textPrimary">{formatNumber(item.requiredQty)}</p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">可用</p>
              <p className="mt-1 font-semibold text-textPrimary">{formatNumber(item.availableQty)}</p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">缺口</p>
              <p className="mt-1 font-semibold text-textPrimary">{formatNumber(item.shortageQty)}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

function CapacityCards({ cases }: { cases: PlanningCase[] }) {
  const capacityItems = cases.flatMap((item) =>
    item.capacity.map((capacity) => ({ ...capacity, planningId: item.id, sourceOrder: item.sourceOrder }))
  );

  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {capacityItems.map((item) => (
        <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={`${item.planningId}-${item.line}-${item.processType}`}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <StatusBadge tone={item.tone}>{item.status}</StatusBadge>
              <h3 className="mt-3 font-semibold text-textPrimary">{item.line}</h3>
              <p className="mt-1 text-sm text-textSecondary">{item.processType} · {item.sourceOrder}</p>
            </div>
            <Factory className="h-5 w-5 text-textSecondary" aria-hidden="true" />
          </div>
          <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">工時</p>
              <p className="mt-1 font-semibold text-textPrimary">
                {item.requiredHours} / {item.availableHours}
              </p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">人員</p>
              <p className="mt-1 font-semibold text-textPrimary">
                {item.staffRequired} / {item.staffAssigned}
              </p>
            </div>
          </div>
          <p className="mt-3 text-xs text-textSecondary">換線 {item.changeoverMinutes} 分鐘</p>
        </div>
      ))}
    </div>
  );
}

function DetailPanel({ item }: { item: PlanningCase }) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">目前計劃</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{item.id}</h2>
          <p className="mt-1 text-sm text-textSecondary">{item.product}</p>
        </div>
        <StatusBadge tone={decisionTone(item.decision)}>{item.decision}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">訂單交期</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.dueDate}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">承諾交期</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.promisedDate}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">缺料金額</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(item.materialShortageValue)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">建議工單</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.suggestedWorkOrderCount} 張</p>
        </div>
      </div>

      <div className="rounded-md bg-slate-50 p-3 text-sm">
        <p className="text-xs text-textSecondary">計劃說明</p>
        <p className="mt-1 leading-6 text-textPrimary">{item.planningNote}</p>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">計劃檢核</p>
        {item.checks.map((check) => (
          <div className="rounded-md border border-border px-3 py-2" key={`${check.area}-${check.status}`}>
            <div className="flex items-center justify-between gap-3">
              <p className="font-medium text-textPrimary">{check.area}</p>
              <StatusBadge tone={check.tone}>{check.status}</StatusBadge>
            </div>
            <p className="mt-1 text-xs text-textSecondary">{check.note}</p>
          </div>
        ))}
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">工單建議</p>
        {item.workOrders.map((workOrder) => (
          <div className="rounded-md border border-border px-3 py-2" key={workOrder.workOrderNo}>
            <div className="flex items-center justify-between gap-3">
              <p className="font-medium text-textPrimary">{workOrder.workOrderNo}</p>
              <StatusBadge tone={workOrder.tone}>{workOrder.status}</StatusBadge>
            </div>
            <p className="mt-1 text-xs text-textSecondary">
              {workOrder.line} · {workOrder.startTime}-{workOrder.endTime} · {formatNumber(workOrder.quantity)} {workOrder.unit}
            </p>
          </div>
        ))}
      </div>
    </aside>
  );
}

function MainContent({
  activeTab,
  data,
  selectedCase,
  onSelectCase
}: {
  activeTab: PlanningWorkspaceTab;
  data: PlanningDashboardData;
  selectedCase: PlanningCase;
  onSelectCase: (item: PlanningCase) => void;
}) {
  if (activeTab === "materials") {
    return (
      <div className="space-y-4">
        <MaterialCards cases={data.cases} />
        <PlanningTable activeTab={activeTab} cases={data.cases} selectedId={selectedCase.id} onSelect={onSelectCase} />
      </div>
    );
  }

  if (activeTab === "capacity") {
    return (
      <div className="space-y-4">
        <CapacityCards cases={data.cases} />
        <PlanningTable activeTab={activeTab} cases={data.cases} selectedId={selectedCase.id} onSelect={onSelectCase} />
      </div>
    );
  }

  return <PlanningTable activeTab={activeTab} cases={data.cases} selectedId={selectedCase.id} onSelect={onSelectCase} />;
}

export default function PlanningPage() {
  const { data: planningData, error, isLoading, source } = usePlanningDashboard();
  const [activeTab, setActiveTab] = useState<PlanningWorkspaceTab>("demand");
  const [selectedCaseId, setSelectedCaseId] = useState<string>(planningData.cases[0].id);
  const selectedCase = planningData.cases.find((item) => item.id === selectedCaseId) ?? planningData.cases[0];

  return (
    <AppLayout activePath="/planning" title="計劃中心 Planning / APS Workspace">
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
                <StatusBadge tone="neutral">ATP/CTP → MRP → 工單建議</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">訂單需求計劃與工單建議總覽</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                承接 Orders 的接單承諾，將已接單需求展開成物料缺口、請購建議、產能與人員檢核，
                再形成可建立或需調整的工單建議。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  placeholder="訂單 / 計劃 / 品項 / 產線"
                />
              </label>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary">
                <Filter className="h-4 w-4" aria-hidden="true" />
                篩選
              </button>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white">
                <CalendarRange className="h-4 w-4" aria-hidden="true" />
                排程
              </button>
            </div>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Planning API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}

        <KpiStrip summary={planningData.summary} />

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="min-w-0 space-y-4">
            <div className="rounded-lg border border-border bg-white p-3 shadow-card">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">計劃視圖</p>
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
              data={planningData}
              selectedCase={selectedCase}
              onSelectCase={(item) => setSelectedCaseId(item.id)}
            />
          </div>

          <DetailPanel item={selectedCase} />
        </section>
      </div>
    </AppLayout>
  );
}
