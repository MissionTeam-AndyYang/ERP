"use client";

import {
  AlertTriangle,
  CircleDollarSign,
  FileText,
  Filter,
  ReceiptText,
  Search,
  TrendingDown
} from "lucide-react";
import { useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { useFinanceDashboard } from "@/hooks/use-finance-dashboard";
import { AppLayout } from "@/layouts/app-layout";
import type {
  FinanceDashboardData,
  FinanceOrderCase,
  FinanceRiskLevel,
  FinanceSummary,
  FinanceWorkspaceTab
} from "@/types/finance";

const tabs: { id: FinanceWorkspaceTab; label: string }[] = [
  { id: "margin", label: "毛利追蹤" },
  { id: "receivables", label: "應收/請款" },
  { id: "payables", label: "應付影響" },
  { id: "cost-variance", label: "成本差異" }
];

const tabDescriptions: Record<FinanceWorkspaceTab, string> = {
  margin: "追蹤訂單預估毛利、實際毛利與低毛利風險。",
  receivables: "以出貨與 POD 簽收狀態判斷是否可請款、是否逾期未收。",
  payables: "觀察採購、庫存、物流與生產成本對訂單毛利的影響。",
  "cost-variance": "比較預估成本與實際成本，追蹤原料、人工、製造與物流差異。"
};

function formatMoney(value: number) {
  return `$${new Intl.NumberFormat("zh-TW").format(value)}`;
}

function riskTone(risk: FinanceRiskLevel) {
  if (risk === "高風險") {
    return "danger";
  }

  if (risk === "注意") {
    return "warning";
  }

  return "success";
}

function getVisibleCases(activeTab: FinanceWorkspaceTab, cases: FinanceOrderCase[]) {
  if (activeTab === "receivables") {
    return cases.filter((item) => item.arStatus !== "已請款" || item.collectedAmount < item.orderAmount);
  }

  if (activeTab === "payables") {
    return [...cases].sort((a, b) => b.payableImpact - a.payableImpact);
  }

  if (activeTab === "cost-variance") {
    return cases.filter((item) => item.marginVarianceRate === null || item.marginVarianceRate < 0);
  }

  return [...cases].sort((a, b) => a.estimatedMarginRate - b.estimatedMarginRate);
}

function KpiStrip({ summary }: { summary: FinanceSummary[] }) {
  const icons = [CircleDollarSign, TrendingDown, ReceiptText, AlertTriangle];

  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {summary.map((item, index) => {
        const Icon = icons[index] ?? CircleDollarSign;
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

function FinanceTable({
  activeTab,
  cases,
  selectedId,
  onSelect
}: {
  activeTab: FinanceWorkspaceTab;
  cases: FinanceOrderCase[];
  selectedId: string;
  onSelect: (item: FinanceOrderCase) => void;
}) {
  const rows = useMemo(() => getVisibleCases(activeTab, cases), [activeTab, cases]);

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[1180px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">財務案件 / 訂單</th>
              <th className="px-4 py-3">客戶 / 產品</th>
              <th className="px-4 py-3 text-right">訂單金額</th>
              <th className="px-4 py-3">毛利</th>
              <th className="px-4 py-3 text-right">成本</th>
              <th className="px-4 py-3">請款/收款</th>
              <th className="px-4 py-3">POD</th>
              <th className="px-4 py-3">風險</th>
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
                    <p className="mt-1 text-xs text-textSecondary">{item.salesOrder}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="font-medium text-textPrimary">{item.customer}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.product}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">{formatMoney(item.orderAmount)}</td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">預估 {item.estimatedMarginRate}%</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      實際 {item.actualMarginRate === null ? "未結算" : `${item.actualMarginRate}%`}
                    </p>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <p className="text-textPrimary">{formatMoney(item.estimatedCost)}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      實際 {item.actualCost === null ? "未結算" : formatMoney(item.actualCost)}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{item.arStatus}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.paymentTerm} · {item.dueDate}</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={item.podStatus === "已簽收" ? "success" : "info"}>{item.podStatus}</StatusBadge>
                    <p className="mt-1 text-xs text-textSecondary">{item.shipmentNo ?? "尚未出貨"}</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={riskTone(item.riskLevel)}>{item.riskLevel}</StatusBadge>
                    <p className="mt-1 line-clamp-2 text-xs text-textSecondary">{item.riskReason}</p>
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

function MarginRiskCards({ cases }: { cases: FinanceOrderCase[] }) {
  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {cases
        .filter((item) => item.riskLevel !== "正常")
        .map((item) => (
          <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.id}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <StatusBadge tone={riskTone(item.riskLevel)}>{item.riskLevel}</StatusBadge>
                <h3 className="mt-3 font-semibold text-textPrimary">{item.salesOrder}</h3>
                <p className="mt-1 text-sm text-textSecondary">{item.product}</p>
              </div>
              <TrendingDown className="h-5 w-5 text-textSecondary" aria-hidden="true" />
            </div>
            <p className="mt-3 text-sm leading-6 text-textSecondary">{item.riskReason}</p>
            <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
              <div className="rounded-md bg-slate-50 p-3">
                <p className="text-xs text-textSecondary">預估毛利</p>
                <p className="mt-1 font-semibold text-textPrimary">{item.estimatedMarginRate}%</p>
              </div>
              <div className="rounded-md bg-slate-50 p-3">
                <p className="text-xs text-textSecondary">實際毛利</p>
                <p className="mt-1 font-semibold text-textPrimary">
                  {item.actualMarginRate === null ? "未結算" : `${item.actualMarginRate}%`}
                </p>
              </div>
            </div>
          </div>
        ))}
    </div>
  );
}

function DetailPanel({ item }: { item: FinanceOrderCase }) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">目前財務案件</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{item.id}</h2>
          <p className="mt-1 text-sm text-textSecondary">{item.customer}</p>
        </div>
        <StatusBadge tone={riskTone(item.riskLevel)}>{item.riskLevel}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">訂單金額</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(item.orderAmount)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">已收金額</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(item.collectedAmount)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">預估/實際成本</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(item.estimatedCost)}</p>
          <p className="mt-1 text-xs text-textSecondary">{item.actualCost === null ? "實際未結算" : formatMoney(item.actualCost)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">毛利差異</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {item.marginVarianceRate === null ? "未結算" : `${item.marginVarianceRate}%`}
          </p>
        </div>
      </div>

      <div className="rounded-md bg-slate-50 p-3 text-sm">
        <p className="text-xs text-textSecondary">風險說明</p>
        <p className="mt-1 leading-6 text-textPrimary">{item.riskReason}</p>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md border border-border p-3">
          <p className="text-xs text-textSecondary">採購/應付影響</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(item.payableImpact)}</p>
        </div>
        <div className="rounded-md border border-border p-3">
          <p className="text-xs text-textSecondary">庫存成本影響</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(item.inventoryCostImpact)}</p>
        </div>
        <div className="rounded-md border border-border p-3">
          <p className="text-xs text-textSecondary">生產成本影響</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(item.productionCostImpact)}</p>
        </div>
        <div className="rounded-md border border-border p-3">
          <p className="text-xs text-textSecondary">物流成本影響</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(item.logisticsCostImpact)}</p>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">文件</p>
        {item.documents.map((doc) => (
          <div className="rounded-md border border-border px-3 py-2" key={`${doc.type}-${doc.no}`}>
            <div className="flex items-center justify-between gap-3">
              <p className="font-medium text-textPrimary">{doc.type}</p>
              <StatusBadge tone={doc.tone}>{doc.status}</StatusBadge>
            </div>
            <p className="mt-1 text-xs text-textSecondary">{doc.no} · {doc.owner}</p>
          </div>
        ))}
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">財務流程</p>
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
  selectedCase,
  onSelectCase
}: {
  activeTab: FinanceWorkspaceTab;
  data: FinanceDashboardData;
  selectedCase: FinanceOrderCase;
  onSelectCase: (item: FinanceOrderCase) => void;
}) {
  if (activeTab === "margin" || activeTab === "cost-variance") {
    return (
      <div className="space-y-4">
        <MarginRiskCards cases={data.cases} />
        <FinanceTable activeTab={activeTab} cases={data.cases} selectedId={selectedCase.id} onSelect={onSelectCase} />
      </div>
    );
  }

  return <FinanceTable activeTab={activeTab} cases={data.cases} selectedId={selectedCase.id} onSelect={onSelectCase} />;
}

export default function FinancePage() {
  const { data: financeData, error, isLoading, source } = useFinanceDashboard();
  const [activeTab, setActiveTab] = useState<FinanceWorkspaceTab>("margin");
  const [selectedCaseId, setSelectedCaseId] = useState<string>(financeData.cases[0].id);
  const selectedCase = financeData.cases.find((item) => item.id === selectedCaseId) ?? financeData.cases[0];

  return (
    <AppLayout activePath="/finance" title="財務毛利 Finance Workspace">
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
                <StatusBadge tone="neutral">毛利 / 成本 / 請款 / 收款</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">訂單毛利與請款收款總覽</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                串接訂單、採購、生產、庫存與物流簽收，追蹤預估毛利、實際毛利、成本差異，
                並確認哪些出貨已具備請款與收款追蹤條件。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  placeholder="訂單 / 客戶 / 發票 / 出貨單"
                />
              </label>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary">
                <Filter className="h-4 w-4" aria-hidden="true" />
                篩選
              </button>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white">
                <FileText className="h-4 w-4" aria-hidden="true" />
                請款
              </button>
            </div>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Finance API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}

        <KpiStrip summary={financeData.summary} />

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="min-w-0 space-y-4">
            <div className="rounded-lg border border-border bg-white p-3 shadow-card">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">財務視圖</p>
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
              data={financeData}
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
