"use client";

import {
  AlertTriangle,
  ArrowLeft,
  BarChart3,
  Boxes,
  Building2,
  ClipboardList,
  Gauge,
  PackageSearch,
  RefreshCw,
  TrendingUp
} from "lucide-react";
import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import type { LanguageCode } from "@/i18n/dictionary";
import { useLanguage } from "@/i18n/language-provider";
import { warehouseEnumLabel, warehouseRiskTone } from "@/i18n/warehouse-enums";
import { AppLayout } from "@/layouts/app-layout";
import {
  getWarehouseAnalyticsOverview,
  getWarehouseAnalyticsRiskBreakdown,
  getWarehouseAnalyticsSpaceUtilization,
  getWarehouseAnalyticsTaskSla,
  getWarehouseAnalyticsValueTrend,
  type WarehouseAnalyticsQuery
} from "@/services/warehouse-api";
import type { StatusTone } from "@/types/dashboard";
import type {
  WarehouseAnalyticsBucket,
  WarehouseAnalyticsOverviewData,
  WarehouseAnalyticsPeriod,
  WarehouseAnalyticsRiskBreakdownData,
  WarehouseAnalyticsRiskBreakdownItem,
  WarehouseAnalyticsSpaceUtilizationData,
  WarehouseAnalyticsTaskSlaData,
  WarehouseAnalyticsTaskSlaItem,
  WarehouseAnalyticsValueTrendData
} from "@/types/warehouse";

const periodOptions: Array<{ label: string; value: WarehouseAnalyticsPeriod }> = [
  { label: "近 7 日", value: "7d" },
  { label: "近 30 日", value: "30d" },
  { label: "近 90 日", value: "90d" }
];

const bucketOptions: Array<{ label: string; value: WarehouseAnalyticsBucket }> = [
  { label: "日", value: "day" },
  { label: "週", value: "week" },
  { label: "月", value: "month" }
];

const itemCategoryOptions: Array<{ label: string; value: number | "all" }> = [
  { label: "全部品項", value: "all" },
  { label: "原料", value: 1 },
  { label: "物料", value: 2 },
  { label: "膠捲", value: 3 },
  { label: "在製品", value: 4 },
  { label: "製成品", value: 5 }
];

const emptyOverview: WarehouseAnalyticsOverviewData = {
  serverDate: "",
  timezone: "Asia/Taipei",
  range: {
    period: "30d",
    bucket: "day",
    startDate: "",
    endDate: ""
  },
  kpi: {
    totalInventoryValue: 0,
    valueChangeRate: 0,
    usedPallets: 0,
    spaceUtilizationRate: 0,
    riskLotCount: 0,
    openTaskCount: 0,
    overdueTaskRate: 0
  },
  valueTrend: [],
  spaceTrend: [],
  riskBreakdown: [],
  taskSla: []
};

const emptyValueTrend: WarehouseAnalyticsValueTrendData = {
  range: emptyOverview.range,
  summaryByCategory: [],
  valueTrend: []
};

const emptySpaceUtilization: WarehouseAnalyticsSpaceUtilizationData = {
  range: emptyOverview.range,
  summaryByWarehouse: [],
  spaceTrend: []
};

const emptyRiskBreakdown: WarehouseAnalyticsRiskBreakdownData = {
  range: emptyOverview.range,
  riskSummary: {
    riskLotCount: 0,
    highRiskLotCount: 0,
    inventoryValue: 0,
    quantity: 0
  },
  riskBreakdown: [],
  topRiskLots: []
};

const emptyTaskSla: WarehouseAnalyticsTaskSlaData = {
  range: emptyOverview.range,
  summaryByTaskType: [],
  summaryByDepartment: [],
  overdueTrend: []
};

function formatNumber(value: number, language: string, maximumFractionDigits = 2) {
  return new Intl.NumberFormat(language, { maximumFractionDigits }).format(value);
}

function formatMoney(value: number, language: string) {
  return `$${new Intl.NumberFormat(language, { maximumFractionDigits: 0 }).format(value)}`;
}

function formatRate(value: number, language: string) {
  return `${formatNumber(value, language, 1)}%`;
}

function kpiTone(value: number, dangerAt: number, warningAt: number): StatusTone {
  if (value >= dangerAt) {
    return "danger";
  }
  if (value >= warningAt) {
    return "warning";
  }
  return "success";
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="rounded-lg border border-dashed border-border bg-white px-4 py-8 text-center text-sm text-textSecondary">
      {message}
    </div>
  );
}

function SummaryCard({
  icon: Icon,
  label,
  value,
  hint,
  tone
}: {
  icon: typeof BarChart3;
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
}) {
  return (
    <div className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-textSecondary">{label}</p>
          <p className="mt-2 text-2xl font-semibold text-textPrimary">{value}</p>
        </div>
        <span className="grid h-10 w-10 place-items-center rounded-full bg-slate-100 text-textSecondary">
          <Icon className="h-5 w-5" aria-hidden="true" />
        </span>
      </div>
      <p className="mt-3 text-xs leading-5 text-textSecondary">{hint}</p>
      <div className="mt-3">
        <StatusBadge tone={tone}>{label}</StatusBadge>
      </div>
    </div>
  );
}

function ValueTrendPanel({
  data,
  language
}: {
  data: WarehouseAnalyticsValueTrendData;
  language: LanguageCode;
}) {
  const trend = data.valueTrend.length ? data.valueTrend : [];
  const maxValue = Math.max(...trend.map((item) => item.inventoryValue), 1);

  if (!trend.length) {
    return <EmptyState message="目前沒有庫存價值趨勢資料。" />;
  }

  return (
    <section className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-medium text-textSecondary">庫存價值趨勢</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">依品項類別檢視資金分布</h2>
        </div>
        <StatusBadge tone="info">{data.range.period} / {data.range.bucket}</StatusBadge>
      </div>

      <div className="mt-4 space-y-3">
        {trend.map((item, index) => {
          const ratio = Math.max((item.inventoryValue / maxValue) * 100, 3);
          return (
            <div className="grid gap-2 sm:grid-cols-[150px_minmax(0,1fr)_130px]" key={`${item.bucketLabel}-${index}`}>
              <div className="min-w-0">
                <p className="truncate text-sm font-semibold text-textPrimary">
                  {warehouseEnumLabel("itemCategory", item.itemCategory, language)}
                </p>
                <p className="text-xs text-textSecondary">{item.bucketLabel || item.bucketStart}</p>
              </div>
              <div className="flex min-w-0 items-center">
                <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100">
                  <div className="h-full rounded-full bg-primary" style={{ width: `${ratio}%` }} />
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm font-semibold text-textPrimary">{formatMoney(item.inventoryValue, language)}</p>
                <p className="text-xs text-textSecondary">可用 {formatMoney(item.availableValue, language)}</p>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

function SpaceUtilizationPanel({
  data,
  language
}: {
  data: WarehouseAnalyticsSpaceUtilizationData;
  language: string;
}) {
  const warehouses = data.summaryByWarehouse.length ? data.summaryByWarehouse : data.spaceTrend;

  if (!warehouses.length) {
    return <EmptyState message="目前沒有倉位使用資料。" />;
  }

  return (
    <section className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-medium text-textSecondary">倉位與板位</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">各倉可用容量與使用壓力</h2>
        </div>
        <StatusBadge tone="info">{data.range.period} / {data.range.bucket}</StatusBadge>
      </div>

      <div className="mt-4 grid gap-3 lg:grid-cols-2">
        {warehouses.map((item) => {
          const tone = kpiTone(item.utilizationRate, 90, 75);
          return (
            <div className="rounded-md border border-border p-3" key={`${item.warehouseNo}-${item.warehouseName}`}>
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="truncate font-semibold text-textPrimary">{item.warehouseName || item.warehouseNo}</p>
                  <p className="mt-1 text-xs text-textSecondary">{item.warehouseNo}</p>
                </div>
                <StatusBadge tone={tone}>{formatRate(item.utilizationRate, language)}</StatusBadge>
              </div>
              <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100">
                <div className="h-full rounded-full bg-primary" style={{ width: `${Math.min(item.utilizationRate, 100)}%` }} />
              </div>
              <div className="mt-3 grid grid-cols-3 gap-2 text-sm">
                <div>
                  <p className="text-xs text-textSecondary">已用</p>
                  <p className="font-semibold text-textPrimary">{formatNumber(item.usedPallets, language)} 板</p>
                </div>
                <div>
                  <p className="text-xs text-textSecondary">預留</p>
                  <p className="font-semibold text-textPrimary">{formatNumber(item.reservedPallets, language)} 板</p>
                </div>
                <div>
                  <p className="text-xs text-textSecondary">可用</p>
                  <p className="font-semibold text-textPrimary">{formatNumber(item.availablePallets, language)} 板</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

function buildRiskDrilldownHref(risk: WarehouseAnalyticsRiskBreakdownItem, query: WarehouseAnalyticsQuery) {
  const params = new URLSearchParams();
  params.set("riskType", risk.riskType);
  if (query.warehouseNo) {
    params.set("warehouse_no", query.warehouseNo);
  }
  if (query.itemCategory !== undefined) {
    params.set("itemCategory", String(query.itemCategory));
  }
  return `/warehouse/inventory/lots?${params.toString()}`;
}

function buildTaskDrilldownHref(task: WarehouseAnalyticsTaskSlaItem, query: WarehouseAnalyticsQuery) {
  const params = new URLSearchParams();
  params.set("dateRange", "overdue");
  if (task.taskType !== undefined) {
    params.set("taskType", String(task.taskType));
  }
  if (query.warehouseNo) {
    params.set("warehouse_no", query.warehouseNo);
  }
  return `/warehouse/task-workbench?${params.toString()}`;
}

function RiskPanel({
  data,
  query,
  language
}: {
  data: WarehouseAnalyticsRiskBreakdownData;
  query: WarehouseAnalyticsQuery;
  language: LanguageCode;
}) {
  if (!data.riskBreakdown.length) {
    return <EmptyState message="目前沒有庫存風險分布資料。" />;
  }

  return (
    <section className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-medium text-textSecondary">風險分布</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">高風險批號與資金暴露</h2>
        </div>
        <StatusBadge tone={data.riskSummary.highRiskLotCount ? "danger" : "success"}>
          高風險 {formatNumber(data.riskSummary.highRiskLotCount, language, 0)}
        </StatusBadge>
      </div>

      <div className="mt-4 overflow-x-auto">
        <table className="min-w-[760px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">風險類型</th>
              <th className="px-4 py-3 text-right">批號數</th>
              <th className="px-4 py-3 text-right">庫存價值</th>
              <th className="px-4 py-3 text-right">數量</th>
              <th className="px-4 py-3">導向</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {data.riskBreakdown.map((item) => {
              const tone = warehouseRiskTone(item.riskLevel, [item.riskType]);
              return (
                <tr key={item.riskType}>
                  <td className="px-4 py-3">
                    <StatusBadge tone={tone}>{warehouseEnumLabel("riskType", item.riskType, language)}</StatusBadge>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(item.lotCount, language, 0)}
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatMoney(item.inventoryValue, language)}</td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatNumber(item.quantity, language)}</td>
                  <td className="px-4 py-3">
                    <Link
                      className="inline-flex h-9 items-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white"
                      href={buildRiskDrilldownHref(item, query)}
                    >
                      <PackageSearch className="h-4 w-4" aria-hidden="true" />
                      批號清單
                    </Link>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function TaskSlaPanel({
  data,
  query,
  language
}: {
  data: WarehouseAnalyticsTaskSlaData;
  query: WarehouseAnalyticsQuery;
  language: LanguageCode;
}) {
  if (!data.summaryByTaskType.length) {
    return <EmptyState message="目前沒有任務 SLA 資料。" />;
  }

  return (
    <section className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-medium text-textSecondary">任務 SLA</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">逾期、阻塞與平均處理時間</h2>
        </div>
        <StatusBadge tone="info">{data.range.period} / {data.range.bucket}</StatusBadge>
      </div>

      <div className="mt-4 overflow-x-auto">
        <table className="min-w-[860px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">任務類型</th>
              <th className="px-4 py-3 text-right">開放</th>
              <th className="px-4 py-3 text-right">完成</th>
              <th className="px-4 py-3 text-right">逾期</th>
              <th className="px-4 py-3 text-right">阻塞</th>
              <th className="px-4 py-3 text-right">準時率</th>
              <th className="px-4 py-3">導向</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {data.summaryByTaskType.map((item, index) => {
              const tone = item.overdueTaskCount || item.blockedTaskCount ? "warning" : "success";
              return (
                <tr key={`${item.taskType ?? "task"}-${index}`}>
                  <td className="px-4 py-3">
                    <StatusBadge tone={tone}>{warehouseEnumLabel("taskType", item.taskType, language)}</StatusBadge>
                    <p className="mt-1 text-xs text-textSecondary">
                      平均 {formatNumber(item.averageLeadTimeHours, language, 1)} 小時
                    </p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(item.openTaskCount, language, 0)}
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">
                    {formatNumber(item.completedTaskCount, language, 0)}
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">
                    {formatNumber(item.overdueTaskCount, language, 0)}
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">
                    {formatNumber(item.blockedTaskCount, language, 0)}
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatRate(item.onTimeRate, language)}
                  </td>
                  <td className="px-4 py-3">
                    <Link
                      className="inline-flex h-9 items-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white"
                      href={buildTaskDrilldownHref(item, query)}
                    >
                      <ClipboardList className="h-4 w-4" aria-hidden="true" />
                      任務工作台
                    </Link>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default function WarehouseAnalyticsPage() {
  const { language } = useLanguage();
  const [period, setPeriod] = useState<WarehouseAnalyticsPeriod>("30d");
  const [bucket, setBucket] = useState<WarehouseAnalyticsBucket>("day");
  const [warehouseNo, setWarehouseNo] = useState("");
  const [itemCategory, setItemCategory] = useState<number | "all">("all");
  const [reloadKey, setReloadKey] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [overview, setOverview] = useState<WarehouseAnalyticsOverviewData>(emptyOverview);
  const [valueTrend, setValueTrend] = useState<WarehouseAnalyticsValueTrendData>(emptyValueTrend);
  const [spaceUtilization, setSpaceUtilization] =
    useState<WarehouseAnalyticsSpaceUtilizationData>(emptySpaceUtilization);
  const [riskBreakdown, setRiskBreakdown] = useState<WarehouseAnalyticsRiskBreakdownData>(emptyRiskBreakdown);
  const [taskSla, setTaskSla] = useState<WarehouseAnalyticsTaskSlaData>(emptyTaskSla);
  const [source, setSource] = useState<"api" | "mock">("mock");
  const [errors, setErrors] = useState<string[]>([]);

  const query = useMemo<WarehouseAnalyticsQuery>(
    () => ({
      period,
      bucket,
      warehouseNo: warehouseNo.trim() || undefined,
      itemCategory: itemCategory === "all" ? undefined : itemCategory
    }),
    [bucket, itemCategory, period, warehouseNo]
  );

  useEffect(() => {
    let isMounted = true;

    Promise.all([
      getWarehouseAnalyticsOverview(query),
      getWarehouseAnalyticsValueTrend(query),
      getWarehouseAnalyticsSpaceUtilization(query),
      getWarehouseAnalyticsRiskBreakdown(query),
      getWarehouseAnalyticsTaskSla(query)
    ]).then(([overviewResult, valueTrendResult, spaceResult, riskResult, taskResult]) => {
      if (!isMounted) {
        return;
      }

      const nextErrors = [
        overviewResult.error,
        valueTrendResult.error,
        spaceResult.error,
        riskResult.error,
        taskResult.error
      ].filter(Boolean) as string[];

      setOverview(overviewResult.data);
      setValueTrend(valueTrendResult.data);
      setSpaceUtilization(spaceResult.data);
      setRiskBreakdown(riskResult.data);
      setTaskSla(taskResult.data);
      setSource(
        [overviewResult, valueTrendResult, spaceResult, riskResult, taskResult].some((result) => result.source === "mock")
          ? "mock"
          : "api"
      );
      setErrors(nextErrors);
      setIsLoading(false);
    });

    return () => {
      isMounted = false;
    };
  }, [query, reloadKey]);

  const handleRefresh = useCallback(() => {
    setIsLoading(true);
    setReloadKey((value) => value + 1);
  }, []);

  const totalReservedValue = valueTrend.summaryByCategory.reduce((sum, item) => sum + item.reservedValue, 0);
  const totalAvailableValue = valueTrend.summaryByCategory.reduce((sum, item) => sum + item.availableValue, 0);

  return (
    <AppLayout activePath="/warehouse" title="倉庫分析工作區">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">WarehouseAnalyticsScreen</StatusBadge>
                <StatusBadge tone="neutral">Read-only analytics</StatusBadge>
                <StatusBadge tone={source === "api" ? "success" : "warning"}>
                  {source === "api" ? "API data" : "Mock fallback"}
                </StatusBadge>
                {isLoading ? <StatusBadge tone="info">Loading API</StatusBadge> : null}
              </div>
              <h1 className="mt-3 text-2xl font-semibold text-textPrimary">倉庫分析工作區</h1>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                彙整庫存價值、倉位使用、風險分布與任務 SLA，並保留到批號清單與任務工作台的操作導向。
              </p>
              <p className="mt-2 text-xs text-textSecondary">
                資料期間 {overview.range.startDate || "-"} 至 {overview.range.endDate || "-"} · 更新{" "}
                {overview.serverDate || "-"} · {overview.timezone}
              </p>
            </div>

            <div className="grid gap-2 sm:grid-cols-[auto_auto_auto_auto] xl:min-w-[680px]">
              <Link
                className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary"
                href="/warehouse"
              >
                <ArrowLeft className="h-4 w-4" aria-hidden="true" />
                倉庫中心
              </Link>
              <Link
                className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white"
                href="/warehouse/inventory/lots"
              >
                <PackageSearch className="h-4 w-4" aria-hidden="true" />
                批號清單
              </Link>
              <Link
                className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white"
                href="/warehouse/task-workbench"
              >
                <ClipboardList className="h-4 w-4" aria-hidden="true" />
                任務工作台
              </Link>
              <button
                className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary"
                onClick={handleRefresh}
                type="button"
              >
                <RefreshCw className="h-4 w-4" aria-hidden="true" />
                重新整理
              </button>
            </div>
          </div>
        </section>

        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="grid gap-3 xl:grid-cols-[1fr_180px_180px_160px]">
            <div>
              <p className="mb-2 text-xs font-medium text-textSecondary">期間</p>
              <div className="flex flex-wrap gap-2">
                {periodOptions.map((option) => (
                  <button
                    className={`h-9 rounded-button px-3 text-sm font-medium transition ${
                      period === option.value ? "bg-primary text-white" : "bg-slate-100 text-textSecondary"
                    }`}
                    key={option.value}
                    onClick={() => {
                      setIsLoading(true);
                      setPeriod(option.value);
                    }}
                    type="button"
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>

            <label>
              <span className="mb-2 block text-xs font-medium text-textSecondary">趨勢粒度</span>
              <select
                className="h-10 w-full rounded-input border border-border bg-white px-3 text-sm text-textPrimary outline-none"
                value={bucket}
                onChange={(event) => {
                  setIsLoading(true);
                  setBucket(event.target.value as WarehouseAnalyticsBucket);
                }}
              >
                {bucketOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>

            <label>
              <span className="mb-2 block text-xs font-medium text-textSecondary">品項類別</span>
              <select
                className="h-10 w-full rounded-input border border-border bg-white px-3 text-sm text-textPrimary outline-none"
                value={itemCategory}
                onChange={(event) => {
                  setIsLoading(true);
                  setItemCategory(event.target.value === "all" ? "all" : Number(event.target.value));
                }}
              >
                {itemCategoryOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>

            <label>
              <span className="mb-2 block text-xs font-medium text-textSecondary">倉庫代號</span>
              <input
                className="h-10 w-full rounded-input border border-border bg-white px-3 text-sm text-textPrimary outline-none placeholder:text-textSecondary"
                value={warehouseNo}
                onChange={(event) => {
                  setIsLoading(true);
                  setWarehouseNo(event.target.value);
                }}
                placeholder="全部"
              />
            </label>
          </div>
        </section>

        {errors.length ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Analytics API 部分資料暫時使用 mock fallback。{errors[0]}
          </p>
        ) : null}

        <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          <SummaryCard
            icon={BarChart3}
            label="庫存總價值"
            value={formatMoney(overview.kpi.totalInventoryValue, language)}
            hint={`可用 ${formatMoney(totalAvailableValue, language)} · 預留 ${formatMoney(totalReservedValue, language)}`}
            tone="info"
          />
          <SummaryCard
            icon={TrendingUp}
            label="價值變化"
            value={formatRate(overview.kpi.valueChangeRate, language)}
            hint={`相較 ${overview.range.period} 起點的庫存價值變化率`}
            tone={overview.kpi.valueChangeRate >= 0 ? "warning" : "success"}
          />
          <SummaryCard
            icon={Gauge}
            label="倉位使用"
            value={formatRate(overview.kpi.spaceUtilizationRate, language)}
            hint={`已用 ${formatNumber(overview.kpi.usedPallets, language)} 板`}
            tone={kpiTone(overview.kpi.spaceUtilizationRate, 90, 75)}
          />
          <SummaryCard
            icon={AlertTriangle}
            label="風險與逾期"
            value={`${formatNumber(overview.kpi.riskLotCount, language, 0)} / ${formatRate(
              overview.kpi.overdueTaskRate,
              language
            )}`}
            hint={`開放任務 ${formatNumber(overview.kpi.openTaskCount, language, 0)} 件`}
            tone={overview.kpi.riskLotCount || overview.kpi.overdueTaskRate ? "warning" : "success"}
          />
        </section>

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1.1fr)_minmax(420px,0.9fr)]">
          <ValueTrendPanel data={valueTrend.valueTrend.length ? valueTrend : { ...valueTrend, valueTrend: overview.valueTrend }} language={language} />
          <SpaceUtilizationPanel
            data={
              spaceUtilization.spaceTrend.length
                ? spaceUtilization
                : { ...spaceUtilization, spaceTrend: overview.spaceTrend }
            }
            language={language}
          />
        </section>

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
          <RiskPanel
            data={
              riskBreakdown.riskBreakdown.length
                ? riskBreakdown
                : { ...riskBreakdown, riskBreakdown: overview.riskBreakdown }
            }
            query={query}
            language={language}
          />
          <TaskSlaPanel
            data={taskSla.summaryByTaskType.length ? taskSla : { ...taskSla, summaryByTaskType: overview.taskSla }}
            query={query}
            language={language}
          />
        </section>

        <section className="grid gap-3 md:grid-cols-3">
          <div className="rounded-lg border border-border bg-white p-4 shadow-card">
            <div className="flex items-center gap-2 text-textSecondary">
              <Boxes className="h-4 w-4" aria-hidden="true" />
              <p className="text-sm font-medium">庫存分析 API</p>
            </div>
            <p className="mt-2 text-xs leading-5 text-textSecondary">
              overview 負責首屏 KPI；value-trend、space-utilization、risk-breakdown、task-sla 負責細節分析。
            </p>
          </div>
          <div className="rounded-lg border border-border bg-white p-4 shadow-card">
            <div className="flex items-center gap-2 text-textSecondary">
              <Building2 className="h-4 w-4" aria-hidden="true" />
              <p className="text-sm font-medium">前端保留篩選狀態</p>
            </div>
            <p className="mt-2 text-xs leading-5 text-textSecondary">
              Drill-down URL 由前端依 riskType、taskType、warehouse_no 與 itemCategory 組合，不依賴後端回傳路由字串。
            </p>
          </div>
          <div className="rounded-lg border border-border bg-white p-4 shadow-card">
            <div className="flex items-center gap-2 text-textSecondary">
              <ClipboardList className="h-4 w-4" aria-hidden="true" />
              <p className="text-sm font-medium">Read-only V1</p>
            </div>
            <p className="mt-2 text-xs leading-5 text-textSecondary">
              本畫面不送出 POST、PUT、DELETE；異動計畫與任務執行保留給後續版本。
            </p>
          </div>
        </section>
      </div>
    </AppLayout>
  );
}
