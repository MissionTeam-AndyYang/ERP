"use client";

import {
  AlertTriangle,
  CalendarClock,
  ClipboardList,
  Factory,
  Filter,
  PackageCheck,
  Search,
  ShieldCheck
} from "lucide-react";
import { useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { AppLayout } from "@/layouts/app-layout";
import {
  productionAlerts,
  productionOrders,
  productionSchedule,
  productionSummary
} from "@/mock/production";
import type { ProductionWorkspaceTab, WorkOrder } from "@/types/production";

const tabs: { id: ProductionWorkspaceTab; label: string }[] = [
  { id: "orders", label: "工單總覽" },
  { id: "materials", label: "備料狀態" },
  { id: "quality", label: "品檢入庫" },
  { id: "capacity", label: "產線產能" }
];

const tabDescriptions: Record<ProductionWorkspaceTab, string> = {
  orders: "以工單、批號、產線與進度檢視今日生產狀態。",
  materials: "聚焦缺料、待領料與 BOM/庫存來源。",
  quality: "檢視品檢待判、完工入庫與批號流向。",
  capacity: "以產線利用率與排程時段檢視插單風險。"
};

function formatNumber(value: number) {
  return new Intl.NumberFormat("zh-TW").format(value);
}

function getVisibleOrders(activeTab: ProductionWorkspaceTab) {
  if (activeTab === "materials") {
    return productionOrders.filter((order) => order.materialStatus !== "足夠");
  }

  if (activeTab === "quality") {
    return productionOrders.filter((order) => order.stage === "品檢" || order.stage === "包裝");
  }

  if (activeTab === "capacity") {
    return [...productionOrders].sort((a, b) => b.progress - a.progress);
  }

  return productionOrders;
}

function ProductionTable({
  activeTab,
  selectedId,
  onSelect
}: {
  activeTab: ProductionWorkspaceTab;
  selectedId: string;
  onSelect: (order: WorkOrder) => void;
}) {
  const rows = useMemo(() => getVisibleOrders(activeTab), [activeTab]);

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[980px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">工單 / 產品</th>
              <th className="px-4 py-3">批號</th>
              <th className="px-4 py-3">產線</th>
              <th className="px-4 py-3">來源訂單</th>
              <th className="px-4 py-3 text-right">產量</th>
              <th className="px-4 py-3">進度</th>
              <th className="px-4 py-3">備料 / 品檢</th>
              <th className="px-4 py-3">狀態</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {rows.map((order) => {
              const isSelected = order.id === selectedId;
              return (
                <tr
                  className={`cursor-pointer transition ${
                    isSelected ? "bg-info/10" : "hover:bg-slate-50"
                  }`}
                  key={order.id}
                  onClick={() => onSelect(order)}
                >
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{order.product}</p>
                    <p className="mt-1 text-xs text-textSecondary">{order.id}</p>
                  </td>
                  <td className="px-4 py-3 font-medium text-textPrimary">{order.batchNo}</td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{order.line}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {order.startTime} - {order.endTime}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{order.sourceOrder}</p>
                    <p className="mt-1 text-xs text-textSecondary">{order.bomNo}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(order.completedQty)} / {formatNumber(order.plannedQty)} {order.unit}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="h-2 w-24 overflow-hidden rounded-full bg-slate-100">
                        <div className="h-full rounded-full bg-primary" style={{ width: `${order.progress}%` }} />
                      </div>
                      <span className="text-xs text-textSecondary">{order.progress}%</span>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{order.materialStatus}</p>
                    <p className="mt-1 text-xs text-textSecondary">{order.qualityStatus}</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={order.tone}>{order.stage}</StatusBadge>
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

function DetailPanel({ order }: { order: WorkOrder }) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">目前工單</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{order.id}</h2>
          <p className="mt-1 text-sm text-textSecondary">{order.product}</p>
        </div>
        <StatusBadge tone={order.tone}>{order.stage}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">計畫產量</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(order.plannedQty)} {order.unit}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">已完成</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(order.completedQty)} {order.unit}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">負責人</p>
          <p className="mt-1 font-semibold text-textPrimary">{order.owner}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">預計完成</p>
          <p className="mt-1 font-semibold text-textPrimary">{order.eta}</p>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">流程狀態</p>
        {order.workflow.map((step, index) => (
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
              {index < order.workflow.length - 1 ? <span className="h-7 w-px bg-border" /> : null}
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

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">備料明細</p>
        {order.materials.map((item) => (
          <div className="rounded-md border border-border px-3 py-2" key={`${item.itemNo}-${item.batchNo}`}>
            <div className="flex items-center justify-between gap-3">
              <div className="min-w-0">
                <p className="truncate text-sm font-medium text-textPrimary">{item.itemName}</p>
                <p className="truncate text-xs text-textSecondary">{item.batchNo}</p>
              </div>
              <StatusBadge tone={item.tone}>{item.status}</StatusBadge>
            </div>
            <p className="mt-2 text-xs text-textSecondary">
              {formatNumber(item.issuedQty)} / {formatNumber(item.requiredQty)} {item.unit}
            </p>
          </div>
        ))}
      </div>
    </aside>
  );
}

export default function ProductionPage() {
  const [activeTab, setActiveTab] = useState<ProductionWorkspaceTab>("orders");
  const [selectedOrder, setSelectedOrder] = useState<WorkOrder>(productionOrders[0]);

  return (
    <AppLayout activePath="/production" title="生產工作台 Production Workspace">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">EWDB 20260522</StatusBadge>
                <StatusBadge tone="neutral">工單 / 備料 / 品檢 / 產線</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">生產工單與流程狀態</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                以訂單、BOM、領料、生產、品檢與入庫為主線，讓管理者快速掌握今日工單進度、
                物料缺口與產線負載。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  placeholder="工單 / 批號 / 產品 / 訂單"
                />
              </label>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary">
                <Filter className="h-4 w-4" aria-hidden="true" />
                篩選
              </button>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white">
                <Factory className="h-4 w-4" aria-hidden="true" />
                排程
              </button>
            </div>
          </div>
        </section>

        <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {productionSummary.map((item) => {
            const Icon =
              item.tone === "danger"
                ? AlertTriangle
                : item.tone === "warning"
                  ? CalendarClock
                  : item.tone === "success"
                    ? ShieldCheck
                    : ClipboardList;
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
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">生產視圖</p>
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

            <ProductionTable
              activeTab={activeTab}
              selectedId={selectedOrder.id}
              onSelect={setSelectedOrder}
            />

            <div className="grid gap-3 lg:grid-cols-3">
              {productionAlerts.map((item) => (
                <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.id}>
                  <div className="flex items-center gap-2">
                    <PackageCheck className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                    <StatusBadge tone={item.tone}>{item.title}</StatusBadge>
                  </div>
                  <p className="mt-3 text-sm leading-6 text-textSecondary">{item.description}</p>
                </div>
              ))}
            </div>

            <div className="grid gap-3 lg:grid-cols-3">
              {productionSchedule.map((line) => (
                <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={line.line}>
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-xs text-textSecondary">產線</p>
                      <p className="mt-1 font-semibold text-textPrimary">{line.line}</p>
                    </div>
                    <StatusBadge tone={line.utilization >= 85 ? "warning" : "info"}>
                      {line.utilization}% 使用率
                    </StatusBadge>
                  </div>
                  <div className="mt-3 space-y-2">
                    {line.slots.map((slot) => (
                      <div className="rounded-md bg-slate-50 px-3 py-2" key={`${line.line}-${slot.time}`}>
                        <div className="flex items-center justify-between gap-2">
                          <p className="text-sm font-medium text-textPrimary">{slot.time}</p>
                          <StatusBadge tone={slot.tone}>{slot.stage}</StatusBadge>
                        </div>
                        <p className="mt-1 truncate text-xs text-textSecondary">
                          {slot.workOrderId} · {slot.product}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <DetailPanel order={selectedOrder} />
        </section>
      </div>
    </AppLayout>
  );
}
