"use client";

import {
  AlertTriangle,
  Boxes,
  FileSearch,
  Filter,
  Network,
  Search,
  ShieldCheck
} from "lucide-react";
import { useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { AppLayout } from "@/layouts/app-layout";
import { traceRecords, traceSummary } from "@/mock/traceability";
import type { TraceRecord, TraceabilityWorkspaceTab } from "@/types/traceability";

const tabs: { id: TraceabilityWorkspaceTab; label: string }[] = [
  { id: "search", label: "溯源查詢" },
  { id: "chain", label: "批號鏈路" },
  { id: "recall", label: "召回範圍" },
  { id: "documents", label: "文件完整性" }
];

const tabDescriptions: Record<TraceabilityWorkspaceTab, string> = {
  search: "以批號、品項、訂單或工單查詢來源與去向。",
  chain: "查看供應商、收貨、批號、製程、品檢、入庫、出貨與客戶鏈路。",
  recall: "模擬某批原料或成品可能影響的數量、客戶與出貨範圍。",
  documents: "集中追蹤 COA、溫度紀錄、品檢與出貨文件是否完整。"
};

function formatNumber(value: number) {
  return new Intl.NumberFormat("zh-TW").format(value);
}

function getVisibleRecords(activeTab: TraceabilityWorkspaceTab) {
  if (activeTab === "documents") {
    return traceRecords.filter((record) => record.documents.some((doc) => doc.status !== "完整"));
  }

  if (activeTab === "recall") {
    return [...traceRecords].sort((a, b) => b.impactedQty - a.impactedQty);
  }

  return traceRecords;
}

function KpiStrip() {
  const icons = [Network, ShieldCheck, FileSearch, AlertTriangle];

  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {traceSummary.map((item, index) => {
        const Icon = icons[index] ?? Network;
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

function TraceTable({
  activeTab,
  selectedId,
  onSelect
}: {
  activeTab: TraceabilityWorkspaceTab;
  selectedId: string;
  onSelect: (record: TraceRecord) => void;
}) {
  const rows = useMemo(() => getVisibleRecords(activeTab), [activeTab]);

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[1080px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">查詢 / 批號</th>
              <th className="px-4 py-3">品項</th>
              <th className="px-4 py-3">方向</th>
              <th className="px-4 py-3">來源</th>
              <th className="px-4 py-3">工單 / 訂單</th>
              <th className="px-4 py-3 text-right">數量</th>
              <th className="px-4 py-3">影響範圍</th>
              <th className="px-4 py-3">狀態</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {rows.map((record) => {
              const isSelected = record.id === selectedId;
              const tone =
                record.traceStatus === "完整"
                  ? "success"
                  : record.traceStatus === "斷鏈"
                    ? "danger"
                    : "warning";
              return (
                <tr
                  className={`cursor-pointer transition ${
                    isSelected ? "bg-info/10" : "hover:bg-slate-50"
                  }`}
                  key={record.id}
                  onClick={() => onSelect(record)}
                >
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{record.queryValue}</p>
                    <p className="mt-1 text-xs text-textSecondary">{record.queryType}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="font-medium text-textPrimary">{record.itemName}</p>
                    <p className="mt-1 text-xs text-textSecondary">{record.batchNo}</p>
                  </td>
                  <td className="px-4 py-3 text-textPrimary">{record.direction}</td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{record.sourceType}</p>
                    <p className="mt-1 text-xs text-textSecondary">{record.sourceDocument}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{record.workOrder ?? "-"}</p>
                    <p className="mt-1 text-xs text-textSecondary">{record.salesOrder ?? "-"}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(record.quantity)} {record.unit}
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{formatNumber(record.impactedQty)} {record.unit}</p>
                    <p className="mt-1 text-xs text-textSecondary">{record.impactedCustomers} 個客戶</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={tone}>{record.traceStatus}</StatusBadge>
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

function ChainView({ record }: { record: TraceRecord }) {
  return (
    <div className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-medium text-textSecondary">Trace Chain</p>
          <h3 className="text-lg font-semibold text-textPrimary">{record.batchNo}</h3>
        </div>
        <p className="text-sm text-textSecondary">{record.riskReason}</p>
      </div>
      <div className="mt-4 grid gap-3 lg:grid-cols-3 xl:grid-cols-6">
        {record.nodes.map((node, index) => (
          <div className="rounded-lg border border-border bg-slate-50 p-3" key={node.id}>
            <div className="flex items-center justify-between gap-2">
              <span className="grid h-6 w-6 place-items-center rounded-full bg-primary text-xs font-bold text-white">
                {index + 1}
              </span>
              <StatusBadge tone={node.tone}>{node.status}</StatusBadge>
            </div>
            <p className="mt-3 font-semibold text-textPrimary">{node.label}</p>
            <p className="mt-1 text-xs text-textSecondary">{node.ref}</p>
            <p className="mt-2 truncate text-xs text-textSecondary">{node.id}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function DetailPanel({ record }: { record: TraceRecord }) {
  const tone =
    record.traceStatus === "完整"
      ? "success"
      : record.traceStatus === "斷鏈"
        ? "danger"
        : "warning";

  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">目前溯源</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{record.batchNo}</h2>
          <p className="mt-1 text-sm text-textSecondary">{record.itemName}</p>
        </div>
        <StatusBadge tone={tone}>{record.traceStatus}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">方向</p>
          <p className="mt-1 font-semibold text-textPrimary">{record.direction}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">影響量</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(record.impactedQty)} {record.unit}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">供應商</p>
          <p className="mt-1 font-semibold text-textPrimary">{record.supplier ?? "-"}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">客戶</p>
          <p className="mt-1 font-semibold text-textPrimary">{record.customer ?? "-"}</p>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">文件完整性</p>
        {record.documents.map((doc) => (
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
    </aside>
  );
}

function MainContent({
  activeTab,
  selectedRecord,
  onSelectRecord
}: {
  activeTab: TraceabilityWorkspaceTab;
  selectedRecord: TraceRecord;
  onSelectRecord: (record: TraceRecord) => void;
}) {
  if (activeTab === "chain") {
    return (
      <div className="space-y-4">
        <ChainView record={selectedRecord} />
        <TraceTable activeTab={activeTab} selectedId={selectedRecord.id} onSelect={onSelectRecord} />
      </div>
    );
  }

  return <TraceTable activeTab={activeTab} selectedId={selectedRecord.id} onSelect={onSelectRecord} />;
}

export default function TraceabilityPage() {
  const [activeTab, setActiveTab] = useState<TraceabilityWorkspaceTab>("search");
  const [selectedRecord, setSelectedRecord] = useState<TraceRecord>(traceRecords[0]);

  return (
    <AppLayout activePath="/traceability" title="溯源中心 Traceability Workspace">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">EWDB 20260522</StatusBadge>
                <StatusBadge tone="neutral">批號 / 品項 / 訂單 / 工單</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">批號溯源與召回範圍</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                以批號為核心，串接供應商、收貨、庫存、生產、品檢、出貨與客戶，
                支援食品安全查核、文件補件與召回範圍模擬。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  placeholder="批號 / 品項 / 訂單 / 工單"
                />
              </label>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary">
                <Filter className="h-4 w-4" aria-hidden="true" />
                篩選
              </button>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white">
                <FileSearch className="h-4 w-4" aria-hidden="true" />
                查詢
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
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">溯源視圖</p>
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
              selectedRecord={selectedRecord}
              onSelectRecord={setSelectedRecord}
            />
          </div>

          <DetailPanel record={selectedRecord} />
        </section>
      </div>
    </AppLayout>
  );
}
