"use client";

import {
  AlertTriangle,
  BarChart3,
  CalendarDays,
  ClipboardList,
  Factory,
  Filter,
  PackageCheck,
  Search,
  ShieldCheck,
  UsersRound
} from "lucide-react";
import { useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { useProductionDashboard } from "@/hooks/use-production-dashboard";
import { AppLayout } from "@/layouts/app-layout";
import type {
  ProductionAlert,
  ProductionDashboardData,
  ProductionDaySchedule,
  ProductionSummaryItem,
  ProductionWorkspaceTab,
  WorkOrder
} from "@/types/production";

const tabs: { id: ProductionWorkspaceTab; label: string }[] = [
  { id: "schedule", label: "週排程與產能" },
  { id: "mes", label: "MES 工單現況" },
  { id: "analytics", label: "效率損耗品質" },
  { id: "details", label: "生產明細" }
];

const tabDescriptions: Record<ProductionWorkspaceTab, string> = {
  schedule: "以日期與產線視角檢視一週預排工單、製程產能、備料與人員是否可行。",
  mes: "掌握今日工單的製程階段、完成率、機台、人員、物料與品檢狀態。",
  analytics: "比較產時效率、原物料損耗率、單品人工費率與品質結果。",
  details: "查看工單、批號、BOM、備料、品檢與入庫 workflow 明細。"
};

function formatNumber(value: number) {
  return new Intl.NumberFormat("zh-TW").format(value);
}

function formatMoney(value: number) {
  return `$${new Intl.NumberFormat("zh-TW").format(value)}`;
}

function getRiskTone(risk: WorkOrder["deliveryRisk"]) {
  if (risk === "高風險") {
    return "danger";
  }

  if (risk === "注意") {
    return "warning";
  }

  return "success";
}

function getVisibleOrders(activeTab: ProductionWorkspaceTab, orders: WorkOrder[]) {
  if (activeTab === "mes") {
    return orders.filter((order) => order.scheduleDate === "2026-05-23");
  }

  if (activeTab === "analytics") {
    return [...orders].sort((a, b) => a.efficiencyRate - b.efficiencyRate);
  }

  return orders;
}

function KpiStrip({ summary }: { summary: ProductionSummaryItem[] }) {
  const icons = [CalendarDays, Factory, UsersRound, ShieldCheck];

  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {summary.map((item, index) => {
        const Icon = icons[index] ?? ClipboardList;
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

function WeekScheduleView({ weekSchedule }: { weekSchedule: ProductionDaySchedule[] }) {
  return (
    <div className="space-y-4">
      {weekSchedule.map((day) => (
        <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={day.date}>
          <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="text-sm font-medium text-textSecondary">{day.date}</p>
              <h3 className="text-lg font-semibold text-textPrimary">{day.label}預排工單</h3>
            </div>
            <p className="text-sm text-textSecondary">
              從製程產線、物料、人員檢查是否可如期生產
            </p>
          </div>
          <div className="mt-4 grid gap-3 xl:grid-cols-3">
            {day.lines.map((line) => {
              const usedRatio = Math.round((line.usedHours / line.dailyCapacityHours) * 100);
              return (
                <div className="rounded-lg border border-border bg-slate-50 p-4" key={`${day.date}-${line.line}`}>
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="font-semibold text-textPrimary">
                        {line.line} · {line.processType}
                      </p>
                      <p className="mt-1 text-xs text-textSecondary">
                        已排 {line.usedHours} hr / 可用 {line.availableHours} hr / 換線 {line.changeoverHours} hr
                      </p>
                    </div>
                    <div className="flex flex-col items-end gap-1">
                      <StatusBadge tone={line.tone}>{usedRatio}%</StatusBadge>
                      <span className="text-xs text-textSecondary">瓶頸 #{line.bottleneckRank}</span>
                    </div>
                  </div>
                  <div className="mt-3 h-2 overflow-hidden rounded-full bg-white">
                    <div className="h-full rounded-full bg-primary" style={{ width: `${usedRatio}%` }} />
                  </div>
                  <div className="mt-3 space-y-2">
                    {line.slots.map((slot) => (
                      <div className="rounded-md bg-white p-3 shadow-card" key={slot.workOrderId}>
                        <div className="flex items-center justify-between gap-2">
                          <p className="text-sm font-semibold text-textPrimary">{slot.workOrderId}</p>
                          <StatusBadge tone={slot.tone}>{slot.stage}</StatusBadge>
                        </div>
                        <p className="mt-1 text-sm text-textSecondary">{slot.product}</p>
                        <p className="mt-2 text-xs text-textSecondary">
                          {slot.startTime} - {slot.endTime}
                        </p>
                        <div className="mt-2 flex flex-wrap gap-2">
                          <StatusBadge tone={slot.materialStatus === "足夠" ? "success" : slot.materialStatus === "短缺" ? "danger" : "warning"}>
                            料品 {slot.materialStatus}
                          </StatusBadge>
                          <StatusBadge tone={slot.staffStatus === "足夠" ? "success" : slot.staffStatus === "不足" ? "danger" : "warning"}>
                            人員 {slot.staffStatus}
                          </StatusBadge>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}

function AnalyticsView({ orders }: { orders: WorkOrder[] }) {
  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {orders.map((order) => (
        <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={order.id}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-sm font-semibold text-primary">{order.id}</p>
              <h3 className="mt-1 font-semibold text-textPrimary">{order.product}</h3>
              <p className="mt-1 text-xs text-textSecondary">{order.line}</p>
            </div>
            <StatusBadge tone={order.quality.tone}>{order.quality.status}</StatusBadge>
          </div>
          <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">產時效率</p>
              <p className="mt-1 font-semibold text-textPrimary">{order.efficiencyRate}%</p>
              <p className="mt-1 text-xs text-textSecondary">
                標準 {order.standardHours} hr / 實際 {order.actualHours} hr
              </p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">損耗率</p>
              <p className="mt-1 font-semibold text-textPrimary">{order.materialLossRate}%</p>
              <p className="mt-1 text-xs text-textSecondary">
                {formatNumber(order.actualMaterialQty)} / {formatNumber(order.standardMaterialQty)}
              </p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">單品人工費</p>
              <p className="mt-1 font-semibold text-textPrimary">{formatMoney(order.unitLaborCost)}</p>
              <p className="mt-1 text-xs text-textSecondary">{order.laborHours} 人時</p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">品質不良率</p>
              <p className="mt-1 font-semibold text-textPrimary">{order.quality.defectRate}%</p>
              <p className="mt-1 text-xs text-textSecondary">
                待判 {order.quality.pendingCount} · 樣本 {order.quality.sampleCount}
              </p>
            </div>
          </div>
          <div className="mt-3 flex flex-wrap gap-2">
            <StatusBadge tone={getRiskTone(order.deliveryRisk)}>交期 {order.deliveryRisk}</StatusBadge>
            <StatusBadge tone={order.qualityBlocksInventory ? "warning" : "success"}>
              {order.qualityBlocksInventory ? "暫緩入庫" : "可入庫"}
            </StatusBadge>
            <StatusBadge tone={order.qualityBlocksShipment ? "warning" : "success"}>
              {order.qualityBlocksShipment ? "暫緩出貨" : "可出貨"}
            </StatusBadge>
          </div>
          <p className="mt-3 text-sm leading-6 text-textSecondary">{order.quality.result}</p>
        </div>
      ))}
    </div>
  );
}

function ProductionTable({
  activeTab,
  orders,
  selectedId,
  onSelect
}: {
  activeTab: ProductionWorkspaceTab;
  orders: WorkOrder[];
  selectedId: string;
  onSelect: (order: WorkOrder) => void;
}) {
  const rows = useMemo(() => getVisibleOrders(activeTab, orders), [activeTab, orders]);

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[1120px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">工單 / 產品</th>
              <th className="px-4 py-3">日期 / 產線</th>
              <th className="px-4 py-3">製程</th>
              <th className="px-4 py-3 text-right">產量</th>
              <th className="px-4 py-3">進度</th>
              <th className="px-4 py-3">料品 / 人員</th>
              <th className="px-4 py-3">MES</th>
              <th className="px-4 py-3">交期 / 換線</th>
              <th className="px-4 py-3">品檢</th>
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
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{order.scheduleDate}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {order.line} · {order.startTime}-{order.endTime}
                    </p>
                  </td>
                  <td className="px-4 py-3 text-textPrimary">{order.processType}</td>
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
                    <p className="text-textPrimary">料品 {order.materialStatus}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      人員 {order.assignedStaff}/{order.requiredStaff} · {order.staffStatus}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{order.machineStatus}</p>
                    <p className="mt-1 text-xs text-textSecondary">效率 {order.efficiencyRate}%</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={getRiskTone(order.deliveryRisk)}>{order.deliveryRisk}</StatusBadge>
                    <p className="mt-1 text-xs text-textSecondary">
                      交期 {order.customerDueDate} · 換線 {order.changeoverMinutes} 分
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={order.quality.tone}>{order.quality.status}</StatusBadge>
                    <p className="mt-1 text-xs text-textSecondary">不良 {order.quality.defectRate}%</p>
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
          <p className="text-xs text-textSecondary">料品/人員</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {order.materialStatus} / {order.staffStatus}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">品檢狀態</p>
          <p className="mt-1 font-semibold text-textPrimary">{order.quality.status}</p>
          <p className="mt-1 text-xs text-textSecondary">
            {order.qualityBlocksInventory ? "暫緩入庫" : "可入庫"} /{" "}
            {order.qualityBlocksShipment ? "暫緩出貨" : "可出貨"}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">損耗率</p>
          <p className="mt-1 font-semibold text-textPrimary">{order.materialLossRate}%</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">單品人工費</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(order.unitLaborCost)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">交期風險</p>
          <p className="mt-1 font-semibold text-textPrimary">{order.deliveryRisk}</p>
          <p className="mt-1 text-xs text-textSecondary">交期 {order.customerDueDate}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">換線時間</p>
          <p className="mt-1 font-semibold text-textPrimary">{order.changeoverMinutes} 分</p>
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

function MainContent({
  activeTab,
  data,
  selectedOrder,
  onSelectOrder
}: {
  activeTab: ProductionWorkspaceTab;
  data: ProductionDashboardData;
  selectedOrder: WorkOrder;
  onSelectOrder: (order: WorkOrder) => void;
}) {
  if (activeTab === "schedule") {
    return <WeekScheduleView weekSchedule={data.weekSchedule} />;
  }

  if (activeTab === "analytics") {
    return (
      <div className="space-y-4">
        <AnalyticsView orders={data.orders} />
        <ProductionTable
          activeTab={activeTab}
          orders={data.orders}
          selectedId={selectedOrder.id}
          onSelect={onSelectOrder}
        />
      </div>
    );
  }

  return (
    <ProductionTable
      activeTab={activeTab}
      orders={data.orders}
      selectedId={selectedOrder.id}
      onSelect={onSelectOrder}
    />
  );
}

export default function ProductionPage() {
  const { data: productionData, error, isLoading, source } = useProductionDashboard();
  const [activeTab, setActiveTab] = useState<ProductionWorkspaceTab>("schedule");
  const [selectedOrderId, setSelectedOrderId] = useState<string>(productionData.orders[0].id);
  const selectedOrder =
    productionData.orders.find((order) => order.id === selectedOrderId) ?? productionData.orders[0];

  return (
    <AppLayout activePath="/production" title="生產管理 Production Workspace">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">EWDB 20260522</StatusBadge>
                <StatusBadge tone="neutral">排程 / MES / 效率 / 品質</StatusBadge>
                <StatusBadge tone={source === "api" ? "success" : "warning"}>
                  {source === "api" ? "API data" : "Mock fallback"}
                </StatusBadge>
                {isLoading ? <StatusBadge tone="info">Loading API</StatusBadge> : null}
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">生產計畫與現場品質總覽</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                以日期、產線與製程產能檢視一週預排工單，並拉近到今日 MES 狀態、
                備料/人員可行性、品檢結果、產時效率、原物料損耗與單品人工費率。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  placeholder="日期 / 產線 / 工單 / 品項 / 批號"
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

        {error ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Production API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}

        <KpiStrip summary={productionData.summary} />

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

            <MainContent
              activeTab={activeTab}
              data={productionData}
              selectedOrder={selectedOrder}
              onSelectOrder={(order) => setSelectedOrderId(order.id)}
            />

            <div className="grid gap-3 lg:grid-cols-3">
              {productionData.alerts.map((item: ProductionAlert) => {
                const Icon = item.tone === "danger" ? AlertTriangle : item.tone === "info" ? ShieldCheck : BarChart3;
                return (
                  <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.id}>
                    <div className="flex items-center gap-2">
                      <Icon className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                      <StatusBadge tone={item.tone}>{item.title}</StatusBadge>
                    </div>
                    <p className="mt-3 text-sm leading-6 text-textSecondary">{item.description}</p>
                  </div>
                );
              })}
            </div>
          </div>

          <DetailPanel order={selectedOrder} />
        </section>
      </div>
    </AppLayout>
  );
}
