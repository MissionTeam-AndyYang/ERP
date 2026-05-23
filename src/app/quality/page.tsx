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
import { AppLayout } from "@/layouts/app-layout";
import { qualityInspections, qualitySummary } from "@/mock/quality";
import type { QualityInspection, QualityWorkspaceTab } from "@/types/quality";

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

function getVisibleInspections(activeTab: QualityWorkspaceTab) {
  if (activeTab === "release-block") {
    return qualityInspections.filter(
      (item) => item.blocksInventory || item.blocksShipment || item.blocksProduction || item.decision === "放行"
    );
  }

  if (activeTab === "ncr") {
    return qualityInspections.filter((item) => item.decision === "隔離" || item.decision === "返工" || item.defectRate > 0);
  }

  if (activeTab === "documents") {
    return qualityInspections.filter((item) => item.documents.some((doc) => doc.status !== "完整"));
  }

  return qualityInspections;
}

function KpiStrip() {
  const icons = [FlaskConical, BadgeCheck, ShieldAlert, FileCheck2];

  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {qualitySummary.map((item, index) => {
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
  selectedId,
  onSelect
}: {
  activeTab: QualityWorkspaceTab;
  selectedId: string;
  onSelect: (inspection: QualityInspection) => void;
}) {
  const rows = useMemo(() => getVisibleInspections(activeTab), [activeTab]);

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

function BlockCards() {
  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {qualityInspections
        .filter((item) => item.blocksInventory || item.blocksShipment || item.blocksProduction)
        .map((item) => (
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
  selectedItem,
  onSelectItem
}: {
  activeTab: QualityWorkspaceTab;
  selectedItem: QualityInspection;
  onSelectItem: (item: QualityInspection) => void;
}) {
  if (activeTab === "release-block") {
    return (
      <div className="space-y-4">
        <BlockCards />
        <QualityTable activeTab={activeTab} selectedId={selectedItem.id} onSelect={onSelectItem} />
      </div>
    );
  }

  return <QualityTable activeTab={activeTab} selectedId={selectedItem.id} onSelect={onSelectItem} />;
}

export default function QualityPage() {
  const [activeTab, setActiveTab] = useState<QualityWorkspaceTab>("inspection");
  const [selectedItem, setSelectedItem] = useState<QualityInspection>(qualityInspections[0]);

  return (
    <AppLayout activePath="/quality" title="品保中心 Quality Workspace">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">EWDB 20260522</StatusBadge>
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
                  placeholder="品檢單 / 批號 / 品項 / 工單"
                />
              </label>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary">
                <Filter className="h-4 w-4" aria-hidden="true" />
                篩選
              </button>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white">
                <ShieldCheck className="h-4 w-4" aria-hidden="true" />
                放行
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
              selectedItem={selectedItem}
              onSelectItem={setSelectedItem}
            />
          </div>

          <DetailPanel item={selectedItem} />
        </section>
      </div>
    </AppLayout>
  );
}
