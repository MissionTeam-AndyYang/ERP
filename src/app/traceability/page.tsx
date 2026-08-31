"use client";

import {
  AlertTriangle,
  ArrowDownUp,
  Boxes,
  ChevronLeft,
  ChevronRight,
  Filter,
  LoaderCircle,
  Network,
  Search
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { DataSourceStatusBadge } from "@/components/common/data-source-status-badge";
import { DataSourceToggle, type DataSourceMode } from "@/components/common/data-source-toggle";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { SupportEmptyState } from "@/components/common/support-empty-state";
import { StatusBadge } from "@/components/ui/status-badge";
import { useTraceabilityDashboard } from "@/hooks/use-traceability-dashboard";
import { AppLayout } from "@/layouts/app-layout";
import { getTraceabilityOverview, type TraceabilityDashboardQuery } from "@/services/traceability-api";
import type {
  TraceBatchOverview,
  TraceRecord,
  TraceStep,
  TraceStepItem,
  TraceabilityWorkspaceTab
} from "@/types/traceability";
import { matchesSupportSearch, normalizeSupportSearch } from "@/utils/support-search";

const pageSize = 50;

const tabs: { id: TraceabilityWorkspaceTab; label: string }[] = [
  { id: "search", label: "溯源查詢" },
  { id: "chain", label: "批號鏈路" },
  { id: "timeline", label: "時間軸" }
];

const tabDescriptions: Record<TraceabilityWorkspaceTab, string> = {
  search: "以批號、料號、來源單據或工單查詢追溯紀錄。",
  chain: "查看選取批號的投入與產出關係，直接對應後端 traceSteps。",
  timeline: "依事件時間檢視進貨、產製與銷貨流程。"
};

const itemCategoryOptions = [
  { value: "", label: "全部料品類別" },
  { value: "1", label: "原料" },
  { value: "4", label: "在製品" },
  { value: "5", label: "製成品" },
  { value: "2", label: "物料" },
  { value: "3", label: "膠捲" }
];

function formatNumber(value: number, fractionDigits = 0) {
  return new Intl.NumberFormat("zh-TW", {
    minimumFractionDigits: fractionDigits,
    maximumFractionDigits: fractionDigits
  }).format(Number.isFinite(value) ? value : 0);
}

function traceRecordMatchesSearch(record: TraceRecord, query: string) {
  if (!query) {
    return true;
  }

  return matchesSupportSearch(
    [
      record.traceId,
      record.batchNo,
      record.itemNo,
      record.itemName,
      record.itemCategoryLabel,
      record.traceDirectionLabel,
      record.refCategoryLabel,
      record.refNo,
      record.partnerTypeLabel,
      record.partnerNo,
      record.partnerName,
      record.workOrderNo,
      record.warehouseNo,
      record.warehouseName,
      record.traceStatusLabel,
      record.riskLevelLabel,
      record.riskLabel
    ],
    query
  );
}

function EmptyState({ title, description }: { title: string; description: string }) {
  return <SupportEmptyState title={title} description={description} />;
}

function LoadingState({ title, description }: { title: string; description: string }) {
  return (
    <div className="flex items-start gap-3 rounded-lg border border-info/20 bg-info/10 px-4 py-4 text-info">
      <LoaderCircle className="mt-0.5 h-5 w-5 animate-spin" aria-hidden="true" />
      <div>
        <p className="text-sm font-semibold">{title}</p>
        <p className="mt-1 text-sm leading-6 text-textSecondary">{description}</p>
      </div>
    </div>
  );
}

function HeaderMetric({ label, value, icon: Icon }: { label: string; value: string; icon: typeof Network }) {
  return (
    <div className="flex items-center gap-3 rounded-lg border border-border bg-slate-50 px-3 py-2">
      <Icon className="h-4 w-4 text-textSecondary" aria-hidden="true" />
      <div>
        <p className="text-xs text-textSecondary">{label}</p>
        <p className="text-sm font-semibold text-textPrimary">{value}</p>
      </div>
    </div>
  );
}

function TraceTable({
  records,
  selectedId,
  isLoading,
  onSelect
}: {
  records: TraceRecord[];
  selectedId: string;
  isLoading: boolean;
  onSelect: (record: TraceRecord) => void;
}) {
  if (isLoading) {
    return <LoadingState title="正在載入溯源清單" description="系統正在取得批號追溯摘要資料。" />;
  }

  if (!records.length) {
    return <EmptyState title="沒有符合條件的溯源資料" description="請調整搜尋、料品類別或分頁條件後再查詢。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[1120px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">批號 / 料品</th>
              <th className="px-4 py-3">方向</th>
              <th className="px-4 py-3">來源單據</th>
              <th className="px-4 py-3">工單</th>
              <th className="px-4 py-3">主要對象</th>
              <th className="px-4 py-3">倉庫</th>
              <th className="px-4 py-3 text-right">目前數量</th>
              <th className="px-4 py-3">狀態</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {records.map((record) => {
              const isSelected = record.traceId === selectedId;
              return (
                <tr
                  className={`cursor-pointer transition ${isSelected ? "bg-primary/5" : "hover:bg-slate-50"}`}
                  key={record.traceId}
                  onClick={() => onSelect(record)}
                >
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{record.batchNo || "未提供批號"}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {record.itemName || "未命名料品"} · {record.itemNo || "未提供料號"}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone="info">{record.traceDirectionLabel}</StatusBadge>
                    <p className="mt-2 text-xs text-textSecondary">{record.itemCategoryLabel}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="font-medium text-textPrimary">{record.refNo || "-"}</p>
                    <p className="mt-1 text-xs text-textSecondary">{record.refCategoryLabel}</p>
                  </td>
                  <td className="px-4 py-3 text-textPrimary">{record.workOrderNo || "-"}</td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{record.partnerName || record.partnerTypeLabel}</p>
                    <p className="mt-1 text-xs text-textSecondary">{record.partnerNo || record.partnerTypeLabel}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{record.warehouseName || "-"}</p>
                    <p className="mt-1 text-xs text-textSecondary">{record.warehouseNo || "-"}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(record.currentQuantity, 2)} {record.unitLabel}
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={record.tone}>{record.traceStatusLabel}</StatusBadge>
                    <p className="mt-2 text-xs text-textSecondary">{record.riskLabel}</p>
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

function TraceStepItems({ title, items }: { title: string; items: TraceStepItem[] }) {
  return (
    <div className="rounded-md border border-border bg-slate-50 p-3">
      <p className="text-xs font-semibold text-textSecondary">{title}</p>
      <div className="mt-2 space-y-2">
        {items.length ? (
          items.map((item, index) => (
            <div className="rounded-md bg-white px-3 py-2" key={`${item.batchNo}-${item.itemNo}-${index}`}>
              <p className="text-sm font-semibold text-textPrimary">{item.batchNo || "未提供批號"}</p>
              <p className="mt-1 text-xs text-textSecondary">
                {item.itemName || "未命名料品"} · {item.itemCategoryLabel}
              </p>
              <p className="mt-1 text-xs text-textSecondary">
                {formatNumber(item.quantity, 2)} {item.unitLabel}
              </p>
            </div>
          ))
        ) : (
          <p className="text-xs text-textSecondary">無資料</p>
        )}
      </div>
    </div>
  );
}

function TraceStepCard({ step, index }: { step: TraceStep; index: number }) {
  return (
    <article className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-primary text-sm font-bold text-white">
            {index + 1}
          </span>
          <div>
            <p className="text-sm font-medium text-textSecondary">{step.stepTypeLabel}</p>
            <h3 className="mt-1 text-lg font-semibold text-textPrimary">{step.refNo || step.stepId}</h3>
            <p className="mt-1 text-xs text-textSecondary">
              {step.eventDate || "未提供日期"} · {step.refCategoryLabel}
            </p>
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          <StatusBadge tone={step.tone}>{step.statusLabel}</StatusBadge>
          <StatusBadge tone={step.tone}>{step.riskLevelLabel}</StatusBadge>
        </div>
      </div>

      <div className="mt-4 grid gap-3 lg:grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)]">
        <TraceStepItems title="投入批號" items={step.inputItems} />
        <div className="hidden items-center justify-center text-textSecondary lg:flex">
          <ArrowDownUp className="h-5 w-5 rotate-90" aria-hidden="true" />
        </div>
        <TraceStepItems title="產出 / 銷貨批號" items={step.outputItems} />
      </div>
    </article>
  );
}

function ChainView({
  overview,
  isLoading,
  activeTab
}: {
  overview?: TraceBatchOverview;
  isLoading: boolean;
  activeTab: TraceabilityWorkspaceTab;
}) {
  if (isLoading) {
    return <LoadingState title="正在載入批號鏈路" description="系統正在取得單一批號的 traceSteps 追溯流程。" />;
  }

  if (!overview) {
    return <EmptyState title="尚未載入批號鏈路" description="請先從溯源清單選擇一個批號。" />;
  }

  const steps =
    activeTab === "timeline"
      ? [...overview.traceSteps].sort((a, b) => a.eventTimestamp - b.eventTimestamp)
      : overview.traceSteps;

  return (
    <div className="space-y-3">
      {steps.length ? (
        steps.map((step, index) => <TraceStepCard key={step.stepId} step={step} index={index} />)
      ) : (
        <EmptyState
          title="此批號尚無可展開流程"
          description="第一版只展開原料與製成品批號；若後端回傳空 traceSteps，畫面會如實顯示。"
        />
      )}
    </div>
  );
}

function DetailMetric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md bg-slate-50 p-3">
      <p className="text-xs text-textSecondary">{label}</p>
      <p className="mt-1 font-semibold text-textPrimary">{value || "-"}</p>
    </div>
  );
}

function DetailPanel({
  record,
  overview,
  isLoading
}: {
  record?: TraceRecord;
  overview?: TraceBatchOverview;
  isLoading: boolean;
}) {
  if (isLoading) {
    return <LoadingState title="正在載入溯源明細" description="系統正在取得批號資訊與追溯流程。" />;
  }

  if (!record && !overview) {
    return <EmptyState title="尚未選擇批號" description="請先從左側清單選擇一筆溯源資料。" />;
  }

  const batch = overview?.batch;
  const title = batch?.batchNo ?? record?.batchNo ?? "溯源明細";
  const itemName = batch?.itemName ?? record?.itemName ?? "";
  const tone = batch?.tone ?? record?.tone ?? "neutral";

  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">目前批號</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{title}</h2>
          <p className="mt-1 text-sm text-textSecondary">{itemName || "未命名料品"}</p>
        </div>
        <StatusBadge tone={tone}>{batch?.traceStatusLabel ?? record?.traceStatusLabel ?? "待確認"}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <DetailMetric label="追溯方向" value={batch?.traceDirectionLabel ?? record?.traceDirectionLabel ?? ""} />
        <DetailMetric label="主要風險" value={batch?.riskLabel ?? record?.riskLabel ?? ""} />
        <DetailMetric label="來源單據" value={`${batch?.refCategoryLabel ?? record?.refCategoryLabel ?? ""} ${batch?.refNo ?? record?.refNo ?? ""}`.trim()} />
        <DetailMetric label="有效日期" value={batch?.validDateLabel ?? ""} />
        <DetailMetric label="目前數量" value={`${formatNumber(record?.currentQuantity ?? 0, 2)} ${record?.unitLabel ?? batch?.unitLabel ?? ""}`.trim()} />
        <DetailMetric label="流程數" value={formatNumber(overview?.traceSteps.length ?? 0)} />
      </div>

      <section className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">最新流程</p>
        {overview?.traceSteps.length ? (
          overview.traceSteps.slice(0, 4).map((step) => (
            <div className="rounded-md border border-border px-3 py-2" key={step.stepId}>
              <div className="flex items-center justify-between gap-3">
                <p className="font-medium text-textPrimary">{step.stepTypeLabel}</p>
                <StatusBadge tone={step.tone}>{step.statusLabel}</StatusBadge>
              </div>
              <p className="mt-1 text-xs text-textSecondary">
                {step.eventDate || "未提供日期"} · {step.refNo || step.stepId}
              </p>
            </div>
          ))
        ) : (
          <p className="rounded-md border border-dashed border-border px-3 py-3 text-xs text-textSecondary">
            尚無 traceSteps 可顯示。
          </p>
        )}
      </section>
    </aside>
  );
}

export default function TraceabilityPage() {
  const [dataSourceMode, setDataSourceMode] = useState<DataSourceMode>("api");
  const [activeTab, setActiveTab] = useState<TraceabilityWorkspaceTab>("search");
  const [searchValue, setSearchValue] = useState("");
  const [itemCategory, setItemCategory] = useState("");
  const [page, setPage] = useState(0);
  const [selectedTraceId, setSelectedTraceId] = useState("");
  const [overviewState, setOverviewState] = useState<{
    batchNo: string;
    overview?: TraceBatchOverview;
    error?: string;
  }>({ batchNo: "" });
  const searchQuery = normalizeSupportSearch(searchValue);

  const dashboardQuery = useMemo<TraceabilityDashboardQuery>(
    () => ({
      keyword: searchValue.trim() || undefined,
      itemCategory: itemCategory ? Number(itemCategory) : undefined,
      start: page * pageSize,
      count: pageSize
    }),
    [itemCategory, page, searchValue]
  );

  const { data: traceabilityData, error, isLoading, source } = useTraceabilityDashboard(
    dataSourceMode,
    dashboardQuery
  );
  const visibleRecords = useMemo(
    () => traceabilityData.records.filter((record) => traceRecordMatchesSearch(record, searchQuery)),
    [traceabilityData.records, searchQuery]
  );
  const selectedRecord = visibleRecords.find((record) => record.traceId === selectedTraceId) ?? visibleRecords[0];
  const selectedBatchNo = selectedRecord?.batchNo ?? "";
  const overview = overviewState.batchNo === selectedBatchNo ? overviewState.overview : undefined;
  const overviewError = overviewState.batchNo === selectedBatchNo ? overviewState.error : undefined;
  const isOverviewLoading = Boolean(selectedBatchNo) && overviewState.batchNo !== selectedBatchNo;
  const canGoPrevious = page > 0;
  const canGoNext = traceabilityData.start + traceabilityData.count < traceabilityData.total;

  useEffect(() => {
    if (!selectedBatchNo) {
      return;
    }

    let isMounted = true;

    getTraceabilityOverview(selectedBatchNo, dataSourceMode).then((result) => {
      if (!isMounted) {
        return;
      }
      setOverviewState({
        batchNo: selectedBatchNo,
        overview: result.overview,
        error: result.error
      });
    });

    return () => {
      isMounted = false;
    };
  }, [dataSourceMode, selectedBatchNo]);

  return (
    <AppLayout activePath="/traceability" title="溯源中心">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">溯源中心</StatusBadge>
                <StatusBadge tone="neutral">批號 / 進貨 / 產製 / 銷貨</StatusBadge>
                <DataSourceStatusBadge source={source} isLoading={isLoading} hasError={Boolean(error)} />
                <DataSourceToggle
                  value={dataSourceMode}
                  onChange={(mode) => {
                    setDataSourceMode(mode);
                    setPage(0);
                    setSelectedTraceId("");
                    setOverviewState({ batchNo: "" });
                  }}
                />
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">批號追溯與投產流程</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                以批號為入口，檢視可確認的進貨、產製與銷貨流程；單批號明細由後端 traceSteps 直接提供投入物與產出物關係。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-3">
              <HeaderMetric icon={Network} label="批號" value={formatNumber(traceabilityData.summary.traceableBatchCount)} />
              <HeaderMetric icon={AlertTriangle} label="斷鏈" value={formatNumber(traceabilityData.summary.brokenTraceCount)} />
              <HeaderMetric icon={Boxes} label="高風險" value={formatNumber(traceabilityData.summary.highRiskTraceCount)} />
            </div>
          </div>
        </section>

        <section className="rounded-lg border border-border bg-white p-3 shadow-card">
          <div className="grid gap-3 xl:grid-cols-[minmax(260px,1fr)_auto_auto_auto_auto]">
            <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
              <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
              <input
                aria-label="搜尋批號、料號、來源單號或工單"
                className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                onChange={(event) => {
                  setPage(0);
                  setSearchValue(event.target.value);
                }}
                placeholder="批號 / 料號 / 來源單據 / 工單"
                value={searchValue}
              />
            </label>
            <select
              className="h-10 rounded-input border border-border bg-slate-50 px-3 text-sm text-textPrimary outline-none"
              onChange={(event) => {
                setPage(0);
                setItemCategory(event.target.value);
              }}
              value={itemCategory}
            >
              {itemCategoryOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <button
              className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary"
              type="button"
              onClick={() => setActiveTab("chain")}
            >
              <Filter className="h-4 w-4" aria-hidden="true" />
              查看鏈路
            </button>
            <button
              className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary disabled:opacity-50"
              disabled={!canGoPrevious}
              onClick={() => setPage((current) => Math.max(0, current - 1))}
              type="button"
            >
              <ChevronLeft className="h-4 w-4" aria-hidden="true" />
              上一頁
            </button>
            <button
              className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary disabled:opacity-50"
              disabled={!canGoNext}
              onClick={() => setPage((current) => current + 1)}
              type="button"
            >
              下一頁
              <ChevronRight className="h-4 w-4" aria-hidden="true" />
            </button>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-danger/20 bg-danger/10 px-4 py-3 text-sm text-danger">
            溯源中心資料取得失敗，畫面未改用預覽資料。可切換資料來源為 Mock 進行前端預覽。{error}
          </p>
        ) : null}
        {overviewError ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            批號追溯資料取得失敗，明細面板保留空狀態。{overviewError}
          </p>
        ) : null}

        <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {traceabilityData.kpis.map((item) => (
            <ModuleKpiCard {...item} key={item.label} />
          ))}
        </section>

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="min-w-0 space-y-4">
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

            {activeTab === "search" ? (
              <div className="space-y-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <StatusBadge tone="neutral">
                    {traceabilityData.total
                      ? `${formatNumber(traceabilityData.start + 1)} - ${formatNumber(traceabilityData.start + traceabilityData.count)} / ${formatNumber(traceabilityData.total)}`
                      : "0 / 0"}
                  </StatusBadge>
                </div>
                <TraceTable
                  records={visibleRecords}
                  selectedId={selectedRecord?.traceId ?? ""}
                  isLoading={isLoading}
                  onSelect={(record) => {
                    setSelectedTraceId(record.traceId);
                    setActiveTab("chain");
                  }}
                />
              </div>
            ) : (
              <ChainView overview={overview} isLoading={isOverviewLoading} activeTab={activeTab} />
            )}
          </div>

          <DetailPanel record={selectedRecord} overview={overview} isLoading={isOverviewLoading} />
        </section>
      </div>
    </AppLayout>
  );
}
