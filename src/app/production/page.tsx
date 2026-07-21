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
import { useEffect, useMemo, useState } from "react";
import { DataSourceToggle, type DataSourceMode } from "@/components/common/data-source-toggle";
import { StatusBadge } from "@/components/ui/status-badge";
import { useProductionDashboard } from "@/hooks/use-production-dashboard";
import { productionEnumLabel, productionRiskTone, productionStatusTone } from "@/i18n/production-enums";
import type { LanguageCode } from "@/i18n/dictionary";
import { useLanguage } from "@/i18n/language-provider";
import { AppLayout } from "@/layouts/app-layout";
import { getProductionWorkOrderDetail } from "@/services/production-api";
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

function safeNumber(value: number | undefined) {
  return value !== undefined && Number.isFinite(value) ? value : 0;
}

function formatNumber(value: number | undefined, fractionDigits = 0) {
  return new Intl.NumberFormat("zh-TW", {
    minimumFractionDigits: fractionDigits,
    maximumFractionDigits: fractionDigits
  }).format(safeNumber(value));
}

function formatMoney(value: number | undefined) {
  return `$${formatNumber(value)}`;
}

function formatPercent(value: number | undefined) {
  return `${formatNumber(value, 2)}%`;
}

function formatHours(value: number | undefined) {
  return `${formatNumber(value, 2)} hr`;
}

function safePercent(numerator: number | undefined, denominator: number | undefined) {
  const base = safeNumber(denominator);
  if (base <= 0) {
    return 0;
  }
  return (safeNumber(numerator) / base) * 100;
}

function progressWidth(value: number | undefined) {
  const percentage = Math.max(0, Math.min(100, safeNumber(value)));
  return `${percentage}%`;
}

function displayText(value: string | undefined) {
  return value && value.trim() ? value : "-";
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

function orderStageLabel(order: WorkOrder, language: LanguageCode) {
  return order.statusCode ? productionEnumLabel("status", order.statusCode, language) : order.stage;
}

function materialStatusLabel(order: WorkOrder, language: LanguageCode) {
  return order.materialStatusCode
    ? productionEnumLabel("materialStatus", order.materialStatusCode, language)
    : order.materialStatus;
}

function staffStatusLabel(order: WorkOrder, language: LanguageCode) {
  return order.staffStatusCode ? productionEnumLabel("staffStatus", order.staffStatusCode, language) : order.staffStatus;
}

function machineStatusLabel(order: WorkOrder, language: LanguageCode) {
  return order.machineStatusCode
    ? productionEnumLabel("machineStatus", order.machineStatusCode, language)
    : order.machineStatus;
}

function qualityStatusLabel(order: WorkOrder, language: LanguageCode) {
  return order.qualityStatusCode
    ? productionEnumLabel("qualityStatus", order.qualityStatusCode, language)
    : order.quality.status;
}

function deliveryRiskLabel(order: WorkOrder, language: LanguageCode) {
  return order.deliveryRiskCode
    ? productionEnumLabel("deliveryRisk", order.deliveryRiskCode, language)
    : order.deliveryRisk;
}

function normalizeSearch(value: string) {
  return value.trim().toLocaleLowerCase();
}

function includesSearch(value: string | number | boolean, search: string) {
  return String(value).toLocaleLowerCase().includes(search);
}

function orderMatchesSearch(order: WorkOrder | undefined, search: string) {
  if (!search) {
    return true;
  }
  if (!order) {
    return false;
  }

  return [
    order.id,
    order.product,
    order.batchNo,
    order.processType,
    order.line,
    order.stage,
    order.owner,
    order.eta,
    order.priority,
    order.sourceOrder,
    order.bomNo,
    order.customerDueDate,
    order.deliveryRisk,
    order.scheduleDate,
    order.startTime,
    order.endTime,
    order.materialStatus,
    order.staffStatus,
    order.machineStatus,
    order.quality.status,
    order.quality.result,
    order.qualityBlocksInventory,
    order.qualityBlocksShipment
  ].some((value) => includesSearch(value, search));
}

function getVisibleOrders(activeTab: ProductionWorkspaceTab, orders: WorkOrder[]) {
  if (activeTab === "mes") {
    return orders;
  }

  if (activeTab === "analytics") {
    return [...orders].sort((a, b) => safeNumber(a.efficiencyRate) - safeNumber(b.efficiencyRate));
  }

  return orders;
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="rounded-lg border border-dashed border-border bg-white px-4 py-8 text-center text-sm text-textSecondary">
      {message}
    </div>
  );
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

function WeekScheduleView({
  weekSchedule,
  searchQuery
}: {
  weekSchedule: ProductionDaySchedule[];
  searchQuery: string;
}) {
  const visibleSchedule = useMemo(
    () =>
      weekSchedule
        .map((day) => ({
          ...day,
          lines: day.lines
            .map((line) => ({
              ...line,
              slots: line.slots.filter((slot) => {
                if (!searchQuery) {
                  return true;
                }

                return [
                  day.date,
                  day.label,
                  line.line,
                  line.processType,
                  line.bottleneckRank,
                  slot.workOrderId,
                  slot.product,
                  slot.processType,
                  slot.startTime,
                  slot.endTime,
                  slot.materialStatus,
                  slot.staffStatus,
                  slot.stage
                ].some((value) => includesSearch(value, searchQuery));
              })
            }))
            .filter((line) => line.slots.length > 0)
        }))
        .filter((day) => day.lines.length > 0),
    [weekSchedule, searchQuery]
  );

  if (!visibleSchedule.length) {
    return <EmptyState message="目前查無符合條件的週排程。" />;
  }

  return (
    <div className="space-y-4">
      {visibleSchedule.map((day) => (
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
              const usedRatio = safePercent(line.usedHours, line.dailyCapacityHours);
              return (
                <div className="rounded-lg border border-border bg-slate-50 p-4" key={`${day.date}-${line.line}`}>
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="font-semibold text-textPrimary">
                        {line.line} · {line.processType}
                      </p>
                      <p className="mt-1 text-xs text-textSecondary">
                        已排 {formatHours(line.usedHours)} / 可用 {formatHours(line.availableHours)} / 換線 {formatHours(line.changeoverHours)}
                      </p>
                    </div>
                    <div className="flex flex-col items-end gap-1">
                      <StatusBadge tone={line.tone}>{formatPercent(usedRatio)}</StatusBadge>
                      <span className="text-xs text-textSecondary">瓶頸 #{line.bottleneckRank}</span>
                    </div>
                  </div>
                  <div className="mt-3 h-2 overflow-hidden rounded-full bg-white">
                    <div className="h-full rounded-full bg-primary" style={{ width: progressWidth(usedRatio) }} />
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

function AnalyticsView({
  orders,
  searchQuery,
  language
}: {
  orders: WorkOrder[];
  searchQuery: string;
  language: LanguageCode;
}) {
  const visibleOrders = orders.filter((order) => orderMatchesSearch(order, searchQuery));

  if (!visibleOrders.length) {
    return <EmptyState message="目前查無符合條件的效率、損耗或品質資料。" />;
  }

  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {visibleOrders.map((order) => (
        <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={order.id}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-sm font-semibold text-primary">{order.id}</p>
              <h3 className="mt-1 font-semibold text-textPrimary">{order.product}</h3>
              <p className="mt-1 text-xs text-textSecondary">{order.line}</p>
            </div>
            <StatusBadge tone={order.quality.tone}>{qualityStatusLabel(order, language)}</StatusBadge>
          </div>
          <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">產時效率</p>
              <p className="mt-1 font-semibold text-textPrimary">{formatPercent(order.efficiencyRate)}</p>
              <p className="mt-1 text-xs text-textSecondary">
                標準 {formatHours(order.standardHours)} / 實際 {formatHours(order.actualHours)}
              </p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">損耗率</p>
              <p className="mt-1 font-semibold text-textPrimary">{formatPercent(order.materialLossRate)}</p>
              <p className="mt-1 text-xs text-textSecondary">
                {formatNumber(order.actualMaterialQty, 2)} / {formatNumber(order.standardMaterialQty, 2)}
              </p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">單品人工費</p>
              <p className="mt-1 font-semibold text-textPrimary">{formatMoney(order.unitLaborCost)}</p>
              <p className="mt-1 text-xs text-textSecondary">{formatNumber(order.laborHours, 2)} 人時</p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">品質不良率</p>
              <p className="mt-1 font-semibold text-textPrimary">{formatPercent(order.quality.defectRate)}</p>
              <p className="mt-1 text-xs text-textSecondary">
                待判 {order.quality.pendingCount} · 樣本 {order.quality.sampleCount}
              </p>
            </div>
          </div>
          <div className="mt-3 flex flex-wrap gap-2">
            <StatusBadge tone={order.deliveryRiskCode ? productionRiskTone(order.deliveryRiskCode) : getRiskTone(order.deliveryRisk)}>
              交期 {deliveryRiskLabel(order, language)}
            </StatusBadge>
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
  searchQuery,
  language,
  onSelect
}: {
  activeTab: ProductionWorkspaceTab;
  orders: WorkOrder[];
  selectedId: string;
  searchQuery: string;
  language: LanguageCode;
  onSelect: (order: WorkOrder) => void;
}) {
  const rows = useMemo(
    () => getVisibleOrders(activeTab, orders).filter((order) => orderMatchesSearch(order, searchQuery)),
    [activeTab, orders, searchQuery]
  );

  if (!rows.length) {
    return <EmptyState message="目前查無符合條件的生產工單。" />;
  }

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
                    <p className="text-textPrimary">{displayText(order.scheduleDate)}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {displayText(order.line)} · {displayText(order.startTime)}-{displayText(order.endTime)}
                    </p>
                  </td>
                  <td className="px-4 py-3 text-textPrimary">{order.processType}</td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(order.completedQty, 2)} / {formatNumber(order.plannedQty, 2)} {order.unit}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="h-2 w-24 overflow-hidden rounded-full bg-slate-100">
                        <div className="h-full rounded-full bg-primary" style={{ width: progressWidth(order.progress) }} />
                      </div>
                      <span className="text-xs text-textSecondary">{formatPercent(order.progress)}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">料品 {materialStatusLabel(order, language)}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      人員 {order.assignedStaff}/{order.requiredStaff} · {staffStatusLabel(order, language)}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{machineStatusLabel(order, language)}</p>
                    <p className="mt-1 text-xs text-textSecondary">效率 {formatPercent(order.efficiencyRate)}</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={order.deliveryRiskCode ? productionRiskTone(order.deliveryRiskCode) : getRiskTone(order.deliveryRisk)}>
                      {deliveryRiskLabel(order, language)}
                    </StatusBadge>
                    <p className="mt-1 text-xs text-textSecondary">
                      交期 {displayText(order.customerDueDate)} · 換線 {formatNumber(order.changeoverMinutes)} 分
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={order.quality.tone}>{qualityStatusLabel(order, language)}</StatusBadge>
                    <p className="mt-1 text-xs text-textSecondary">不良 {formatPercent(order.quality.defectRate)}</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={order.statusCode ? productionStatusTone(order.statusCode) : order.tone}>
                      {orderStageLabel(order, language)}
                    </StatusBadge>
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

function DetailPanel({
  order,
  language,
  isLoading,
  error
}: {
  order: WorkOrder;
  language: LanguageCode;
  isLoading: boolean;
  error?: string;
}) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">目前工單</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{order.id}</h2>
          <p className="mt-1 text-sm text-textSecondary">{order.product}</p>
        </div>
        <StatusBadge tone={order.statusCode ? productionStatusTone(order.statusCode) : order.tone}>
          {isLoading ? "Loading" : orderStageLabel(order, language)}
        </StatusBadge>
      </div>

      {error ? (
        <p className="rounded-md border border-warning/20 bg-warning/10 px-3 py-2 text-xs leading-5 text-warning">
          Detail API 尚未可用，已保留清單資料。{error}
        </p>
      ) : null}

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">計畫產量</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(order.plannedQty, 2)} {order.unit}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">已完成</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(order.completedQty, 2)} {order.unit}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">料品/人員</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {materialStatusLabel(order, language)} / {staffStatusLabel(order, language)}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">品檢狀態</p>
          <p className="mt-1 font-semibold text-textPrimary">{qualityStatusLabel(order, language)}</p>
          <p className="mt-1 text-xs text-textSecondary">
            {order.qualityBlocksInventory ? "暫緩入庫" : "可入庫"} /{" "}
            {order.qualityBlocksShipment ? "暫緩出貨" : "可出貨"}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">損耗率</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatPercent(order.materialLossRate)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">單品人工費</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(order.unitLaborCost)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">交期風險</p>
          <p className="mt-1 font-semibold text-textPrimary">{deliveryRiskLabel(order, language)}</p>
          <p className="mt-1 text-xs text-textSecondary">交期 {displayText(order.customerDueDate)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">換線時間</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatNumber(order.changeoverMinutes)} 分</p>
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
              {formatNumber(item.issuedQty, 2)} / {formatNumber(item.requiredQty, 2)} {item.unit}
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
  selectedId,
  searchQuery,
  language,
  onSelectOrder
}: {
  activeTab: ProductionWorkspaceTab;
  data: ProductionDashboardData;
  selectedId: string;
  searchQuery: string;
  language: LanguageCode;
  onSelectOrder: (order: WorkOrder) => void;
}) {
  if (activeTab === "schedule") {
    return <WeekScheduleView weekSchedule={data.weekSchedule} searchQuery={searchQuery} />;
  }

  if (activeTab === "analytics") {
    return (
      <div className="space-y-4">
        <AnalyticsView orders={data.orders} searchQuery={searchQuery} language={language} />
        <ProductionTable
          activeTab={activeTab}
          orders={data.orders}
          selectedId={selectedId}
          searchQuery={searchQuery}
          language={language}
          onSelect={onSelectOrder}
        />
      </div>
    );
  }

  return (
    <ProductionTable
      activeTab={activeTab}
      orders={data.orders}
      selectedId={selectedId}
      searchQuery={searchQuery}
      language={language}
      onSelect={onSelectOrder}
    />
  );
}

export default function ProductionPage() {
  const { language } = useLanguage();
  const [dataSourceMode, setDataSourceMode] = useState<DataSourceMode>("api");
  const { data: productionData, error, isLoading, source } = useProductionDashboard(dataSourceMode);
  const [activeTab, setActiveTab] = useState<ProductionWorkspaceTab>("schedule");
  const [selectedOrderId, setSelectedOrderId] = useState<string>(productionData.orders[0]?.id ?? "");
  const [detailOrder, setDetailOrder] = useState<WorkOrder | undefined>();
  const [detailError, setDetailError] = useState<string | undefined>();
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const [searchValue, setSearchValue] = useState("");
  const searchQuery = normalizeSearch(searchValue);
  const selectedOrderCandidate =
    productionData.orders.find((order) => order.id === selectedOrderId) ?? productionData.orders[0];
  const selectedOrderBase =
    selectedOrderCandidate && searchQuery && !orderMatchesSearch(selectedOrderCandidate, searchQuery)
      ? productionData.orders.find((order) => orderMatchesSearch(order, searchQuery)) ?? selectedOrderCandidate
      : selectedOrderCandidate;
  const selectedOrder = selectedOrderBase && detailOrder?.id === selectedOrderBase.id ? detailOrder : selectedOrderBase;

  useEffect(() => {
    if (!selectedOrderBase?.id) {
      return;
    }

    let isMounted = true;

    getProductionWorkOrderDetail(selectedOrderBase.id, selectedOrderBase, dataSourceMode).then((result) => {
      if (!isMounted) {
        return;
      }
      setDetailOrder(result.order);
      setDetailError(result.error);
      setIsDetailLoading(false);
    });

    return () => {
      isMounted = false;
    };
  }, [dataSourceMode, selectedOrderBase]);

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
                <DataSourceToggle value={dataSourceMode} onChange={setDataSourceMode} />
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
                  aria-label="搜尋日期、產線、工單、品項或批號"
                  value={searchValue}
                  onChange={(event) => setSearchValue(event.target.value)}
                  placeholder="日期 / 產線 / 工單 / 品項 / 批號"
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
                onClick={() => setActiveTab("schedule")}
                title="切換到週排程與產能視圖。"
                type="button"
              >
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
          <div className="min-w-0 space-y-4">
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
              selectedId={selectedOrder?.id ?? ""}
              searchQuery={searchQuery}
              language={language}
              onSelectOrder={(order) => {
                setIsDetailLoading(true);
                setDetailError(undefined);
                setSelectedOrderId(order.id);
              }}
            />

            <div className="grid gap-3 lg:grid-cols-3">
              {productionData.alerts.map((item: ProductionAlert) => {
                const Icon = item.tone === "danger" ? AlertTriangle : item.tone === "info" ? ShieldCheck : BarChart3;
                const title = item.titleCode
                  ? productionEnumLabel("alertType", item.titleCode, language)
                  : item.title;
                const description = item.descriptionCode
                  ? productionEnumLabel("alertComment", item.descriptionCode, language)
                  : item.description;
                return (
                  <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.id}>
                    <div className="flex items-center gap-2">
                      <Icon className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                      <StatusBadge tone={item.tone}>{title}</StatusBadge>
                    </div>
                    <p className="mt-3 text-sm leading-6 text-textSecondary">
                      {description}
                      {(item.count ?? 0) > 1 ? `（共 ${formatNumber(item.count)} 筆）` : ""}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>

          {selectedOrder ? (
            <DetailPanel order={selectedOrder} language={language} isLoading={isDetailLoading} error={detailError} />
          ) : (
            <aside className="rounded-lg border border-dashed border-border bg-white p-4 text-sm text-textSecondary shadow-card">
              目前沒有可顯示的生產工單明細。
            </aside>
          )}
        </section>
      </div>
    </AppLayout>
  );
}
