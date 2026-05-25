"use client";

import {
  AlertTriangle,
  BadgeCheck,
  FileCheck2,
  Filter,
  FlaskConical,
  Search,
  ShieldAlert,
  ShieldCheck
} from "lucide-react";
import { useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { useQualityDashboard } from "@/hooks/use-quality-dashboard";
import { AppLayout } from "@/layouts/app-layout";
import type {
  QualityDashboardData,
  QualityInspection,
  QualitySummary,
  QualityWorkspaceTab
} from "@/types/quality";

const tabs: { id: QualityWorkspaceTab; label: string }[] = [
  { id: "inspection", label: "檢驗批次" },
  { id: "release-block", label: "放行與阻擋" },
  { id: "ncr", label: "異常/NCR" },
  { id: "documents", label: "文件完整性" }
];

const tabDescriptions: Record<QualityWorkspaceTab, string> = {
  inspection: "查看今日原料、首件、製程、成品與出貨前檢驗批次。",
  "release-block": "集中檢視哪些批號可放行，哪些暫緩入庫、出貨或生產。",
  ncr: "追蹤異常原因、隔離、返工、報廢與責任單位。",
  documents: "追蹤 COA、溫度紀錄、微生物快篩、品檢與收貨文件完整性。"
};

function formatNumber(value: number) {
  return new Intl.NumberFormat("zh-TW").format(value);
}

function normalizeSearch(value: string) {
  return value.trim().toLocaleLowerCase();
}

function includesSearch(value: string | number | boolean | null, search: string) {
  if (value === null) {
    return false;
  }

  return String(value).toLocaleLowerCase().includes(search);
}

function inspectionMatchesSearch(item: QualityInspection, search: string) {
  if (!search) {
    return true;
  }

  return [
    item.id,
    item.itemName,
    item.itemNo,
    item.batchNo,
    item.sourceType,
    item.sourceNo,
    item.workOrder,
    item.salesOrder,
    item.supplier,
    item.line,
    item.inspectionType,
    item.stage,
    item.decision,
    item.issueReason,
    item.blocksInventory,
    item.blocksShipment,
    item.blocksProduction,
    item.owner,
    item.dueTime,
    ...item.pendingTests,
    ...item.documents.flatMap((doc) => [doc.type, doc.no, doc.status, doc.owner])
  ].some((value) => includesSearch(value, search));
}

function getVisibleInspections(activeTab: QualityWorkspaceTab, inspections: QualityInspection[]) {
  if (activeTab === "release-block") {
    return inspections.filter(
      (item) => item.blocksInventory || item.blocksShipment || item.blocksProduction || item.decision === "放行"
    );
  }

  if (activeTab === "ncr") {
    return inspections.filter((item) => item.decision === "隔離" || item.decision === "返工" || item.defectRate > 0);
  }

  if (activeTab === "documents") {
    return inspections.filter((item) => item.documents.some((doc) => doc.status !== "完整"));
  }

  return inspections;
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="rounded-lg border border-dashed border-border bg-white px-4 py-8 text-center text-sm text-textSecondary">
      {message}
    </div>
  );
}

function KpiStrip({ summary }: { summary: QualitySummary[] }) {
  const icons = [FlaskConical, BadgeCheck, ShieldAlert, FileCheck2];

  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {summary.map((item, index) => {
        const Icon = icons[index] ?? FlaskConical;
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

function QualityTable({
  activeTab,
  inspections,
  selectedId,
  searchQuery,
  onSelect
}: {
  activeTab: QualityWorkspaceTab;
  inspections: QualityInspection[];
  selectedId: string;
  searchQuery: string;
  onSelect: (inspection: QualityInspection) => void;
}) {
  const rows = useMemo(
    () => getVisibleInspections(activeTab, inspections).filter((item) => inspectionMatchesSearch(item, searchQuery)),
    [activeTab, inspections, searchQuery]
  );

  if (!rows.length) {
    return <EmptyState message="目前查無符合條件的品檢批次。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[1120px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">檢驗 / 批號</th>
              <th className="px-4 py-3">品項</th>
              <th className="px-4 py-3">來源</th>
              <th className="px-4 py-3">類型</th>
              <th className="px-4 py-3 text-right">抽樣/不良</th>
              <th className="px-4 py-3">阻擋</th>
              <th className="px-4 py-3">待判/文件</th>
              <th className="px-4 py-3">判定</th>
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
                    <p className="font-semibold text-textPrimary">{item.id}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.batchNo}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="font-medium text-textPrimary">{item.itemName}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.itemNo}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{item.sourceType}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.sourceNo}</p>
                  </td>
                  <td className="px-4 py-3 text-textPrimary">{item.inspectionType}</td>
                  <td className="px-4 py-3 text-right">
                    <p className="font-semibold text-textPrimary">
                      {formatNumber(item.sampleCount)} / {formatNumber(item.defectCount)}
                    </p>
                    <p className="mt-1 text-xs text-textSecondary">不良 {item.defectRate}%</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">
                      {item.blocksInventory ? "暫緩入庫" : "可入庫"}
                    </p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {item.blocksShipment ? "暫緩出貨" : "可出貨"} /{" "}
                      {item.blocksProduction ? "暫停生產" : "可生產"}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">
                      {item.pendingTests.length ? item.pendingTests.join("、") : "無"}
                    </p>
                    <p className="mt-1 text-xs text-textSecondary">{item.documents.length} 份文件</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={item.tone}>{item.decision}</StatusBadge>
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

function BlockCards({ inspections, searchQuery }: { inspections: QualityInspection[]; searchQuery: string }) {
  const visibleBlocks = inspections
    .filter((item) => item.blocksInventory || item.blocksShipment || item.blocksProduction)
    .filter((item) => inspectionMatchesSearch(item, searchQuery));

  if (!visibleBlocks.length) {
    return <EmptyState message="目前查無符合條件的放行或阻擋項目。" />;
  }

  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {visibleBlocks.map((item) => (
        <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.id}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <StatusBadge tone={item.tone}>{item.decision}</StatusBadge>
              <h3 className="mt-3 font-semibold text-textPrimary">{item.itemName}</h3>
              <p className="mt-1 text-sm text-textSecondary">{item.batchNo}</p>
            </div>
            <AlertTriangle className="h-5 w-5 text-textSecondary" aria-hidden="true" />
          </div>
          <p className="mt-3 text-sm leading-6 text-textSecondary">{item.issueReason}</p>
          <div className="mt-3 flex flex-wrap gap-2">
            <StatusBadge tone={item.blocksInventory ? "warning" : "success"}>
              {item.blocksInventory ? "暫緩入庫" : "可入庫"}
            </StatusBadge>
            <StatusBadge tone={item.blocksShipment ? "warning" : "success"}>
              {item.blocksShipment ? "暫緩出貨" : "可出貨"}
            </StatusBadge>
            <StatusBadge tone={item.blocksProduction ? "danger" : "success"}>
              {item.blocksProduction ? "暫停生產" : "可生產"}
            </StatusBadge>
          </div>
        </div>
      ))}
    </div>
  );
}

function DetailPanel({ item }: { item: QualityInspection }) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">目前品檢</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{item.id}</h2>
          <p className="mt-1 text-sm text-textSecondary">{item.itemName}</p>
          <p className="mt-1 text-xs text-textSecondary">{item.batchNo}</p>
        </div>
        <StatusBadge tone={item.tone}>{item.decision}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">抽樣/不良</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(item.sampleCount)} / {formatNumber(item.defectCount)}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">不良率</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.defectRate}%</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">負責</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.owner}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">期限</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.dueTime}</p>
        </div>
      </div>

      <div className="rounded-md bg-slate-50 p-3 text-sm">
        <p className="text-xs text-textSecondary">判定說明</p>
        <p className="mt-1 leading-6 text-textPrimary">{item.issueReason}</p>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">文件</p>
        {item.documents.map((doc) => (
          <div className="rounded-md border border-border px-3 py-2" key={`${doc.type}-${doc.no}`}>
            <div className="flex items-center justify-between gap-3">
              <p className="font-medium text-textPrimary">{doc.type}</p>
              <StatusBadge tone={doc.tone}>{doc.status}</StatusBadge>
            </div>
            <p className="mt-1 text-xs text-textSecondary">
              {doc.no} · {doc.owner}
            </p>
          </div>
        ))}
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">品質流程</p>
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
  searchQuery,
  onSelectItem
}: {
  activeTab: QualityWorkspaceTab;
  data: QualityDashboardData;
  selectedItem: QualityInspection;
  searchQuery: string;
  onSelectItem: (item: QualityInspection) => void;
}) {
  if (activeTab === "release-block") {
    return (
      <div className="space-y-4">
        <BlockCards inspections={data.inspections} searchQuery={searchQuery} />
        <QualityTable
          activeTab={activeTab}
          inspections={data.inspections}
          selectedId={selectedItem.id}
          searchQuery={searchQuery}
          onSelect={onSelectItem}
        />
      </div>
    );
  }

  return (
    <QualityTable
      activeTab={activeTab}
      inspections={data.inspections}
      selectedId={selectedItem.id}
      searchQuery={searchQuery}
      onSelect={onSelectItem}
    />
  );
}

export default function QualityPage() {
  const { data: qualityData, error, isLoading, source } = useQualityDashboard();
  const [activeTab, setActiveTab] = useState<QualityWorkspaceTab>("inspection");
  const [selectedItemId, setSelectedItemId] = useState<string>(qualityData.inspections[0].id);
  const [searchValue, setSearchValue] = useState("");
  const searchQuery = normalizeSearch(searchValue);
  const selectedItemCandidate =
    qualityData.inspections.find((item) => item.id === selectedItemId) ?? qualityData.inspections[0];
  const selectedItem =
    searchQuery && !inspectionMatchesSearch(selectedItemCandidate, searchQuery)
      ? qualityData.inspections.find((item) => inspectionMatchesSearch(item, searchQuery)) ?? selectedItemCandidate
      : selectedItemCandidate;

  return (
    <AppLayout activePath="/quality" title="品保中心 Quality Workspace">
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
                <StatusBadge tone="neutral">檢驗 / 放行 / 阻擋 / 文件</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">品檢放行與品質阻擋總覽</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                以原料、首件、製程、成品與出貨前檢驗為核心，追蹤待判、異常、文件缺口，
                並明確標示是否阻擋生產、入庫或出貨。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  aria-label="搜尋品檢單、批號、品項或工單"
                  value={searchValue}
                  onChange={(event) => setSearchValue(event.target.value)}
                  placeholder="品檢單 / 批號 / 品項 / 工單"
                />
              </label>
              <button
                className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary"
                title="V1 先保留為進階篩選入口，待 API 條件欄位確認後啟用。"
                type="button"
              >
                <Filter className="h-4 w-4" aria-hidden="true" />
                篩選
              </button>
              <button
                className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white"
                onClick={() => setActiveTab("release-block")}
                title="切換到放行與阻擋視圖，檢視可入庫、可出貨與品質 hold 狀態。"
                type="button"
              >
                <ShieldCheck className="h-4 w-4" aria-hidden="true" />
                放行
              </button>
            </div>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Quality API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}

        <KpiStrip summary={qualityData.summary} />

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="min-w-0 space-y-4">
            <div className="rounded-lg border border-border bg-white p-3 shadow-card">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">品保視圖</p>
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
              data={qualityData}
              selectedItem={selectedItem}
              searchQuery={searchQuery}
              onSelectItem={(item) => setSelectedItemId(item.id)}
            />
          </div>

          <DetailPanel item={selectedItem} />
        </section>
      </div>
    </AppLayout>
  );
}
