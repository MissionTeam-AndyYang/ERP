"use client";

import {
  AlertTriangle,
  Boxes,
  CalendarClock,
  ClipboardList,
  Filter,
  PackageSearch,
  ReceiptText,
  Search
} from "lucide-react";
import { useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { AppLayout } from "@/layouts/app-layout";
import {
  warehouseExceptions,
  warehouseKpis,
  warehouseRecords
} from "@/mock/warehouse";
import type { WarehouseRecord, WarehouseWorkspaceTab } from "@/types/warehouse";

const tabs: { id: WarehouseWorkspaceTab; label: string }[] = [
  { id: "overview", label: "庫存總覽" },
  { id: "batches", label: "批號效期" },
  { id: "movements", label: "進出紀錄" },
  { id: "storage", label: "倉租帳款" }
];

const tabDescriptions: Record<WarehouseWorkspaceTab, string> = {
  overview: "以品項與倉庫檢視目前庫存、金額與狀態。",
  batches: "以批號、效期與來源單號檢視批次風險。",
  movements: "檢視入庫、出庫、移倉與來源 workflow 關係。",
  storage: "檢視存放天數、倉租金額與結算狀態。"
};

function formatNumber(value: number) {
  return new Intl.NumberFormat("zh-TW").format(value);
}

function getVisibleRows(activeTab: WarehouseWorkspaceTab) {
  if (activeTab === "batches") {
    return [...warehouseRecords].sort((a, b) => a.daysLeft - b.daysLeft);
  }

  if (activeTab === "storage") {
    return warehouseRecords.filter((record) => record.storageCharge > 0);
  }

  return warehouseRecords;
}

function WarehouseTable({
  activeTab,
  selectedId,
  onSelect
}: {
  activeTab: WarehouseWorkspaceTab;
  selectedId: string;
  onSelect: (record: WarehouseRecord) => void;
}) {
  const rows = useMemo(() => getVisibleRows(activeTab), [activeTab]);

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[960px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">品項</th>
              <th className="px-4 py-3">批號</th>
              <th className="px-4 py-3">倉庫</th>
              <th className="px-4 py-3">來源</th>
              <th className="px-4 py-3 text-right">數量</th>
              <th className="px-4 py-3 text-right">金額</th>
              <th className="px-4 py-3">效期 / 倉租</th>
              <th className="px-4 py-3">狀態</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {rows.map((record) => {
              const isSelected = record.id === selectedId;
              return (
                <tr
                  className={`cursor-pointer transition ${
                    isSelected ? "bg-info/10" : "hover:bg-slate-50"
                  }`}
                  key={record.id}
                  onClick={() => onSelect(record)}
                >
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{record.itemName}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {record.itemNo} · {record.category}
                    </p>
                  </td>
                  <td className="px-4 py-3 font-medium text-textPrimary">{record.batchNo}</td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{record.warehouseName}</p>
                    <p className="mt-1 text-xs text-textSecondary">{record.warehouseNo}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{record.sourceType}</p>
                    <p className="mt-1 text-xs text-textSecondary">{record.sourceNo}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(record.quantity)} {record.unit}
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">
                    ${formatNumber(record.amount)}
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{record.expiryDate}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {record.daysLeft} 天 · 倉租 ${formatNumber(record.storageCharge)}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={record.tone}>{record.status}</StatusBadge>
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

function DetailPanel({ record }: { record: WarehouseRecord }) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">
            目前批號
          </p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{record.batchNo}</h2>
          <p className="mt-1 text-sm text-textSecondary">{record.itemName}</p>
        </div>
        <StatusBadge tone={record.tone}>{record.status}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">目前數量</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(record.quantity)} {record.unit}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">庫存金額</p>
          <p className="mt-1 font-semibold text-textPrimary">${formatNumber(record.amount)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">效期</p>
          <p className="mt-1 font-semibold text-textPrimary">{record.daysLeft} 天</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">倉租狀態</p>
          <p className="mt-1 font-semibold text-textPrimary">{record.paymentStatus}</p>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">流程狀態</p>
        <div className="space-y-2">
          {record.workflow.map((step, index) => (
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
                {index < record.workflow.length - 1 ? (
                  <span className="h-8 w-px bg-border" />
                ) : null}
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
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">關聯單據</p>
        {record.relatedDocuments.map((doc) => (
          <div
            className="flex items-center justify-between gap-3 rounded-md border border-border px-3 py-2"
            key={`${doc.type}-${doc.no}`}
          >
            <div className="min-w-0">
              <p className="text-sm font-medium text-textPrimary">{doc.type}</p>
              <p className="truncate text-xs text-textSecondary">{doc.no}</p>
            </div>
            <StatusBadge tone={doc.tone}>{doc.status}</StatusBadge>
          </div>
        ))}
      </div>
    </aside>
  );
}

export default function WarehousePage() {
  const [activeTab, setActiveTab] = useState<WarehouseWorkspaceTab>("overview");
  const [selectedRecord, setSelectedRecord] = useState<WarehouseRecord>(warehouseRecords[0]);

  return (
    <AppLayout activePath="/warehouse" title="倉儲工作台 Warehouse Workspace">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">EWDB 20260522</StatusBadge>
                <StatusBadge tone="neutral">查詢 / 檢視 / 流程狀態</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">倉儲庫存與批號狀態</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                以批號、庫存紀錄、倉儲紀錄與倉租帳款為核心，讓管理者快速看見即期風險、低庫存、
                進出紀錄與採購/生產/出貨來源。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  placeholder="批號 / 品項 / 來源單號"
                />
              </label>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary">
                <Filter className="h-4 w-4" aria-hidden="true" />
                篩選
              </button>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white">
                <PackageSearch className="h-4 w-4" aria-hidden="true" />
                追溯
              </button>
            </div>
          </div>
        </section>

        <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {warehouseKpis.map((item) => {
            const Icon =
              item.tone === "danger"
                ? AlertTriangle
                : item.tone === "warning"
                  ? CalendarClock
                  : item.tone === "success"
                    ? ReceiptText
                    : Boxes;
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

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="space-y-4">
            <div className="rounded-lg border border-border bg-white p-3 shadow-card">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">
                    倉儲視圖
                  </p>
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

            <WarehouseTable
              activeTab={activeTab}
              selectedId={selectedRecord.id}
              onSelect={setSelectedRecord}
            />

            <div className="grid gap-3 lg:grid-cols-3">
              {warehouseExceptions.map((item) => (
                <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.id}>
                  <div className="flex items-center gap-2">
                    <ClipboardList className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                    <StatusBadge tone={item.tone}>{item.title}</StatusBadge>
                  </div>
                  <p className="mt-3 text-sm leading-6 text-textSecondary">{item.description}</p>
                </div>
              ))}
            </div>
          </div>

          <DetailPanel record={selectedRecord} />
        </section>
      </div>
    </AppLayout>
  );
}
