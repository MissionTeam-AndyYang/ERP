"use client";

import { Barcode, CalendarClock, ChevronLeft, ChevronRight, Database, Network, Search } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { DataSourceStatusBadge } from "@/components/common/data-source-status-badge";
import { DataSourceToggle, type DataSourceMode } from "@/components/common/data-source-toggle";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { SupportEmptyState } from "@/components/common/support-empty-state";
import { StatusBadge } from "@/components/ui/status-badge";
import { useBatchDashboard } from "@/hooks/use-batch-dashboard";
import { AppLayout } from "@/layouts/app-layout";
import { getBatchDetail, getBatchDistribution, type BatchDashboardQuery } from "@/services/batches-api";
import type { BatchDetail, BatchDistributionData, BatchDistributionRow, BatchItemSummary } from "@/types/batches";
import { matchesSupportSearch, normalizeSupportSearch } from "@/utils/support-search";

const pageSize = 50;

const itemCategoryOptions = [
  { value: "", label: "全部類別" },
  { value: "1", label: "原料" },
  { value: "2", label: "物料" },
  { value: "3", label: "膠捲" },
  { value: "4", label: "在製品" },
  { value: "5", label: "製成品" },
  { value: "6", label: "貨品" },
  { value: "0", label: "其他" }
];

const riskLevelOptions = [
  { value: "", label: "全部風險" },
  { value: "high_risk", label: "高風險" },
  { value: "attention", label: "注意" },
  { value: "normal", label: "正常" }
];

function formatNumber(value: number, fractionDigits = 0) {
  return new Intl.NumberFormat("zh-TW", {
    minimumFractionDigits: fractionDigits,
    maximumFractionDigits: fractionDigits
  }).format(Number.isFinite(value) ? value : 0);
}

function formatMoney(value: number) {
  return `$${formatNumber(value)}`;
}

function itemMatchesSearch(item: BatchItemSummary, query: string) {
  if (!query) {
    return true;
  }

  return matchesSupportSearch(
    [
      item.itemNo,
      item.itemName,
      item.itemCategoryLabel,
      item.itemTypeLabel,
      item.riskLevelLabel,
      item.riskLabel,
      item.ownerDepartmentLabel,
      item.earliestValidDate
    ],
    query
  );
}

function batchMatchesSearch(batch: BatchDistributionRow, query: string) {
  if (!query) {
    return true;
  }

  return matchesSupportSearch(
    [
      batch.batchNo,
      batch.warehouseNo,
      batch.warehouseName,
      batch.locationCode,
      batch.qaStatusLabel,
      batch.batchStageLabel,
      batch.refCategoryLabel,
      batch.refNo,
      ...batch.riskLabels,
      ...batch.relatedDocuments.map((document) => `${document.refCategoryLabel} ${document.refNo}`)
    ],
    query
  );
}

function EmptyState({ title, description }: { title: string; description: string }) {
  return <SupportEmptyState title={title} description={description} />;
}

function HeaderMetric({ label, value, icon: Icon }: { label: string; value: string; icon: typeof Barcode }) {
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

function ItemSummaryRow({
  item,
  isSelected,
  onSelect
}: {
  item: BatchItemSummary;
  isSelected: boolean;
  onSelect: () => void;
}) {
  return (
    <button
      className={`w-full rounded-lg border px-4 py-4 text-left transition hover:border-primary/40 hover:bg-primary/5 ${
        isSelected ? "border-primary bg-primary/5 ring-1 ring-primary/20" : "border-border bg-white"
      }`}
      onClick={onSelect}
      type="button"
    >
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-textSecondary">{item.itemNo}</p>
          <h3 className="mt-1 text-lg font-semibold text-textPrimary">{item.itemName || "未命名品項"}</h3>
          <p className="mt-1 text-sm text-textSecondary">
            {item.itemCategoryLabel} / {item.totalBatchCount} 批 / {item.warehouseCount} 倉
          </p>
        </div>
        <StatusBadge tone={item.tone}>{item.riskLabel}</StatusBadge>
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-4">
        <SummaryMetric label="總量" value={`${formatNumber(item.currentQuantity, 2)} ${item.unitLabel}`} />
        <SummaryMetric label="可用" value={`${formatNumber(item.availableQuantity, 2)} ${item.unitLabel}`} />
        <SummaryMetric label="預留" value={`${formatNumber(item.reservedQuantity, 2)} ${item.unitLabel}`} />
        <SummaryMetric label="品檢保留" value={`${formatNumber(item.qualityHoldQuantity, 2)} ${item.unitLabel}`} />
      </div>

      <div className="mt-4 flex flex-wrap gap-2 text-xs text-textSecondary">
        <span>最早效期 {item.earliestValidDate || "未提供"}</span>
        <span>品檢保留批 {formatNumber(item.qaHoldBatchCount)}</span>
        <span>即期 {formatNumber(item.nearExpiryBatchCount)}</span>
        <span>下一步 {item.ownerDepartmentLabel}</span>
      </div>
    </button>
  );
}

function SummaryMetric({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs font-medium text-textSecondary">{label}</p>
      <p className="mt-1 text-sm font-semibold text-textPrimary">{value}</p>
    </div>
  );
}

function BatchDistributionRows({
  batches,
  selectedRowKey,
  onSelect
}: {
  batches: BatchDistributionRow[];
  selectedRowKey?: string;
  onSelect: (batch: BatchDistributionRow) => void;
}) {
  return (
    <div className="overflow-hidden rounded-lg border border-border">
      <div className="grid grid-cols-[1.05fr_1fr_0.8fr] gap-3 bg-slate-50 px-4 py-3 text-xs font-semibold text-textSecondary md:grid-cols-[1fr_0.9fr_0.9fr_0.8fr_0.8fr]">
        <span>批號</span>
        <span>倉庫 / 庫位</span>
        <span className="hidden md:block">數量</span>
        <span>品檢 / 階段</span>
        <span className="hidden md:block">效期</span>
      </div>
      <div className="divide-y divide-border">
        {batches.map((batch) => (
          <button
            className={`grid w-full grid-cols-[1.05fr_1fr_0.8fr] gap-3 px-4 py-3 text-left text-sm transition hover:bg-primary/5 md:grid-cols-[1fr_0.9fr_0.9fr_0.8fr_0.8fr] ${
              selectedRowKey === batch.rowKey ? "bg-primary/5" : "bg-white"
            }`}
            key={batch.rowKey}
            onClick={() => onSelect(batch)}
            type="button"
          >
            <span>
              <span className="block font-semibold text-textPrimary">{batch.batchNo || "未提供批號"}</span>
              <span className="mt-1 block text-xs text-textSecondary">{batch.refNo || "無來源單號"}</span>
            </span>
            <span>
              <span className="block font-medium text-textPrimary">{batch.warehouseName || batch.warehouseNo || "未提供倉庫"}</span>
              <span className="mt-1 block text-xs text-textSecondary">{batch.locationCode || "未提供庫位"}</span>
            </span>
            <span className="hidden md:block">
              <span className="block font-medium text-textPrimary">
                {formatNumber(batch.currentQuantity, 2)} {batch.unitLabel}
              </span>
              <span className="mt-1 block text-xs text-textSecondary">
                可用 {formatNumber(batch.availableQuantity, 2)} / 預留 {formatNumber(batch.reservedQuantity, 2)}
              </span>
            </span>
            <span>
              <StatusBadge tone={batch.tone}>{batch.qaStatusLabel}</StatusBadge>
              <span className="mt-2 block text-xs text-textSecondary">{batch.batchStageLabel}</span>
            </span>
            <span className="hidden text-textPrimary md:block">{batch.validDate || "未提供"}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

function DetailMetric({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-xs font-medium text-textSecondary">{label}</dt>
      <dd className="mt-1 text-sm font-semibold text-textPrimary">{value}</dd>
    </div>
  );
}

function BatchDetailPanel({
  detail,
  selectedBatch,
  isLoading
}: {
  detail?: BatchDetail;
  selectedBatch?: BatchDistributionRow;
  isLoading: boolean;
}) {
  if (isLoading) {
    return <EmptyState title="正在載入批號明細" description="系統正在取得批號庫存、來源、預留與任務資料。" />;
  }

  if (!selectedBatch && !detail) {
    return <EmptyState title="尚未選擇批號" description="請先選擇品項與批號，檢視目前營運狀態。" />;
  }

  const batch = detail?.batch;
  const title = batch?.batchNo ?? selectedBatch?.batchNo ?? "批號明細";
  const itemName = batch?.itemName ?? "";
  const stockRows = detail?.stockByWarehouse ?? [];
  const inventoryRows = detail?.inventoryRecords ?? [];
  const reservationRows = detail?.reservations ?? [];
  const qualityRows = detail?.qualityHolds ?? [];
  const taskRows = detail?.tasks ?? [];

  return (
    <article className="rounded-lg border border-border bg-white p-5 shadow-card">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-textSecondary">{batch?.itemNo ?? selectedBatch?.refNo ?? "批號追蹤"}</p>
          <h3 className="mt-1 text-xl font-semibold text-textPrimary">{title}</h3>
          <p className="mt-1 text-sm text-textSecondary">{itemName || selectedBatch?.warehouseName || "目前批號狀態"}</p>
        </div>
        <StatusBadge tone={selectedBatch?.tone ?? "neutral"}>{selectedBatch?.qaStatusLabel ?? "明細"}</StatusBadge>
      </div>

      <dl className="mt-5 grid gap-4 sm:grid-cols-2">
        <DetailMetric label="來源單據" value={`${batch?.refCategoryLabel ?? selectedBatch?.refCategoryLabel ?? "來源"} ${batch?.refNo ?? selectedBatch?.refNo ?? ""}`.trim()} />
        <DetailMetric label="有效日期" value={batch?.validDate || selectedBatch?.validDate || "未提供"} />
        <DetailMetric label="目前數量" value={`${formatNumber(selectedBatch?.currentQuantity ?? 0, 2)} ${selectedBatch?.unitLabel ?? batch?.unitLabel ?? ""}`} />
        <DetailMetric label="可用 / 預留 / 品檢保留" value={`${formatNumber(selectedBatch?.availableQuantity ?? 0, 2)} / ${formatNumber(selectedBatch?.reservedQuantity ?? 0, 2)} / ${formatNumber(selectedBatch?.qualityHoldQuantity ?? 0, 2)}`} />
      </dl>

      <section className="mt-5 space-y-2">
        <p className="text-sm font-semibold text-textPrimary">分倉庫存</p>
        {stockRows.length ? (
          stockRows.map((row) => (
            <div className="rounded-md border border-border px-3 py-2" key={`${row.warehouseNo}-${row.locationCode}`}>
              <div className="flex items-center justify-between gap-3">
                <p className="text-sm font-medium text-textPrimary">{row.warehouseName || row.warehouseNo}</p>
                <StatusBadge tone={row.tone}>{row.riskLevelLabel}</StatusBadge>
              </div>
              <p className="mt-1 text-xs text-textSecondary">
                {row.locationCode || "未提供庫位"} · 現有 {formatNumber(row.currentQuantity, 2)} {row.unitLabel} · 可用 {formatNumber(row.availableQuantity, 2)}
              </p>
            </div>
          ))
        ) : (
          <EmptyState title="沒有分倉庫存" description="目前此批號沒有可顯示的分倉庫存資料。" />
        )}
      </section>

      <section className="mt-5 space-y-2">
        <p className="text-sm font-semibold text-textPrimary">出入庫紀錄</p>
        {inventoryRows.length ? (
          inventoryRows.slice(0, 5).map((row) => (
            <div className="rounded-md border border-border px-3 py-2" key={`${row.recordTime}-${row.refNo}-${row.quantity}`}>
              <div className="flex items-center justify-between gap-3">
                <p className="text-sm font-medium text-textPrimary">{row.categoryLabel}</p>
                <span className="text-xs text-textSecondary">{row.recordTime || "未提供日期"}</span>
              </div>
              <p className="mt-1 text-xs text-textSecondary">
                {row.refCategoryLabel} {row.refNo || "無單號"} · {formatNumber(row.quantity, 2)} {row.unitLabel} · {formatMoney(row.amount)}
              </p>
            </div>
          ))
        ) : (
          <EmptyState title="沒有出入庫紀錄" description="目前沒有此批號的出入庫紀錄。" />
        )}
      </section>

      <section className="mt-5 grid gap-3 md:grid-cols-3">
        <DetailList
          title="預留"
          emptyText="目前沒有預留紀錄。"
          rows={reservationRows.map((row) => ({
            key: row.reservationNo || `${row.refNo}-${row.reservedQuantity}`,
            title: row.reservationNo || row.refNo || "預留紀錄",
            value: `${formatNumber(row.reservedQuantity, 2)} ${batch?.unitLabel ?? selectedBatch?.unitLabel ?? ""}`,
            meta: `${row.statusLabel} · ${row.expiryTimestamp || "未提供期限"}`
          }))}
        />
        <DetailList
          title="品檢保留"
          emptyText="目前沒有品檢保留。"
          rows={qualityRows.map((row) => ({
            key: row.holdNo || `${row.warehouseNo}-${row.holdQuantity}`,
            title: row.holdNo || row.reasonLabel,
            value: `${formatNumber(row.holdQuantity, 2)} ${batch?.unitLabel ?? selectedBatch?.unitLabel ?? ""}`,
            meta: `${row.statusLabel} · ${row.reasonLabel}`
          }))}
        />
        <DetailList
          title="未完成任務"
          emptyText="目前沒有未完成任務。"
          rows={taskRows.map((row) => ({
            key: String(row.taskId),
            title: row.taskTypeLabel,
            value: row.taskStatusLabel,
            meta: `${row.nextOwnerDepartmentLabel} · ${row.dueTimestamp || "未提供期限"}`
          }))}
        />
      </section>
    </article>
  );
}

function DetailList({
  title,
  emptyText,
  rows
}: {
  title: string;
  emptyText: string;
  rows: { key: string; title: string; value: string; meta: string }[];
}) {
  return (
    <div className="rounded-md border border-border p-3">
      <p className="text-sm font-semibold text-textPrimary">{title}</p>
      <div className="mt-2 space-y-2">
        {rows.length ? (
          rows.map((row) => (
            <div className="rounded-md bg-slate-50 px-3 py-2" key={row.key}>
              <p className="text-sm font-medium text-textPrimary">{row.title}</p>
              <p className="mt-1 text-xs text-textSecondary">{row.value}</p>
              <p className="mt-1 text-xs text-textSecondary">{row.meta}</p>
            </div>
          ))
        ) : (
          <p className="text-xs text-textSecondary">{emptyText}</p>
        )}
      </div>
    </div>
  );
}

export default function BatchesPage() {
  const [dataSourceMode, setDataSourceMode] = useState<DataSourceMode>("api");
  const [searchValue, setSearchValue] = useState("");
  const [itemCategory, setItemCategory] = useState("");
  const [riskLevelCode, setRiskLevelCode] = useState("");
  const [page, setPage] = useState(0);
  const [selectedItemNo, setSelectedItemNo] = useState("");
  const [selectedRowKey, setSelectedRowKey] = useState("");
  const [distribution, setDistribution] = useState<BatchDistributionData>();
  const [distributionError, setDistributionError] = useState<string>();
  const [isDistributionLoading, setIsDistributionLoading] = useState(true);
  const [detail, setDetail] = useState<BatchDetail>();
  const [detailError, setDetailError] = useState<string>();
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const searchQuery = normalizeSupportSearch(searchValue);

  const dashboardQuery = useMemo<BatchDashboardQuery>(
    () => ({
      keyword: searchValue.trim() || undefined,
      itemCategory: itemCategory === "" ? undefined : Number(itemCategory),
      riskLevelCode: riskLevelCode || undefined,
      start: page * pageSize,
      count: pageSize
    }),
    [itemCategory, page, riskLevelCode, searchValue]
  );

  const { data, error, isLoading, source } = useBatchDashboard(dataSourceMode, dashboardQuery);
  const visibleItems = useMemo(
    () => data.items.filter((item) => itemMatchesSearch(item, searchQuery)),
    [data.items, searchQuery]
  );
  const selectedItem =
    visibleItems.find((item) => item.itemNo === selectedItemNo) ?? visibleItems[0];
  const activeDistribution = distribution?.item.itemNo === selectedItem?.itemNo ? distribution : undefined;
  const visibleBatches = useMemo(
    () => (activeDistribution?.batches ?? []).filter((batch) => batchMatchesSearch(batch, searchQuery)),
    [activeDistribution?.batches, searchQuery]
  );
  const selectedBatch =
    visibleBatches.find((batch) => batch.rowKey === selectedRowKey) ?? visibleBatches[0];
  const activeDetail = selectedBatch?.batchNo && detail?.batch.batchNo === selectedBatch.batchNo ? detail : undefined;
  const canGoPrevious = page > 0;
  const canGoNext = data.start + data.count < data.total;
  const showDistributionLoading = Boolean(selectedItem?.itemNo) && isDistributionLoading;

  useEffect(() => {
    if (!selectedItem?.itemNo) {
      return;
    }

    let isMounted = true;

    getBatchDistribution(selectedItem.itemNo, dashboardQuery, dataSourceMode).then((result) => {
      if (!isMounted) {
        return;
      }
      setDistribution(result.data);
      setDistributionError(result.error);
      setSelectedRowKey(result.data.batches[0]?.rowKey ?? "");
      setIsDetailLoading(Boolean(result.data.batches[0]?.batchNo));
      setIsDistributionLoading(false);
    });

    return () => {
      isMounted = false;
    };
  }, [dashboardQuery, dataSourceMode, selectedItem?.itemNo]);

  useEffect(() => {
    if (!selectedBatch?.batchNo) {
      return;
    }

    let isMounted = true;

    getBatchDetail(selectedBatch.batchNo, dataSourceMode).then((result) => {
      if (!isMounted) {
        return;
      }
      setDetail(result.detail);
      setDetailError(result.error);
      setIsDetailLoading(false);
    });

    return () => {
      isMounted = false;
    };
  }, [dataSourceMode, selectedBatch?.batchNo]);

  return (
    <AppLayout activePath="/batches" title="批號中心">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">批號中心</StatusBadge>
                <StatusBadge tone="neutral">料品 / 批號 / 倉庫分布 / 品檢保留</StatusBadge>
                <DataSourceStatusBadge source={source} isLoading={isLoading} hasError={Boolean(error)} />
                <DataSourceToggle
                  value={dataSourceMode}
                  onChange={(value) => {
                    setDataSourceMode(value);
                    setIsDistributionLoading(true);
                    setIsDetailLoading(true);
                  }}
                />
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">品項批號分布與營運狀態</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                以料品為第一層彙總批號、倉庫分布、可用量、預留量、品檢保留與效期風險，協助快速確認批號目前可用性與下一步負責單位。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-3">
              <HeaderMetric icon={Barcode} label="品項" value={formatNumber(data.summary.stockItemCount)} />
              <HeaderMetric icon={CalendarClock} label="即期" value={formatNumber(data.summary.nearExpiryBatchCount)} />
              <HeaderMetric icon={Network} label="分布" value={formatNumber(data.summary.stockBatchCount)} />
            </div>
          </div>
        </section>

        <section className="rounded-lg border border-border bg-white p-3 shadow-card">
          <div className="grid gap-3 xl:grid-cols-[minmax(260px,1fr)_auto_auto_auto_auto]">
            <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
              <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
              <input
                aria-label="搜尋品項、批號、倉庫、庫位、來源單號或品檢狀態"
                className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                onChange={(event) => {
                  setPage(0);
                  setIsDistributionLoading(true);
                  setSearchValue(event.target.value);
                }}
                placeholder="品項 / 批號 / 倉庫 / 來源單號 / 品檢"
                value={searchValue}
              />
            </label>
            <select
              className="h-10 rounded-input border border-border bg-slate-50 px-3 text-sm text-textPrimary outline-none"
              onChange={(event) => {
                setPage(0);
                setIsDistributionLoading(true);
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
            <select
              className="h-10 rounded-input border border-border bg-slate-50 px-3 text-sm text-textPrimary outline-none"
              onChange={(event) => {
                setPage(0);
                setIsDistributionLoading(true);
                setRiskLevelCode(event.target.value);
              }}
              value={riskLevelCode}
            >
              {riskLevelOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <button
              className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary disabled:opacity-50"
              disabled={!canGoPrevious}
              onClick={() => {
                setIsDistributionLoading(true);
                setPage((current) => Math.max(0, current - 1));
              }}
              type="button"
            >
              <ChevronLeft className="h-4 w-4" aria-hidden="true" />
              上一頁
            </button>
            <button
              className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary disabled:opacity-50"
              disabled={!canGoNext}
              onClick={() => {
                setIsDistributionLoading(true);
                setPage((current) => current + 1);
              }}
              type="button"
            >
              下一頁
              <ChevronRight className="h-4 w-4" aria-hidden="true" />
            </button>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-danger/20 bg-danger/10 px-4 py-3 text-sm text-danger">
            批號中心資料取得失敗，畫面未改用預覽資料。可切換資料來源為 Mock 進行前端預覽。{error}
          </p>
        ) : null}
        {distributionError ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            批號分布資料取得失敗，右側分布區保留空狀態。{distributionError}
          </p>
        ) : null}
        {detailError ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            批號追蹤明細取得失敗，明細面板保留空狀態。{detailError}
          </p>
        ) : null}

        <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {data.kpis.map((item) => (
            <ModuleKpiCard {...item} key={item.label} />
          ))}
        </section>

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_minmax(520px,0.9fr)]">
          <article className="rounded-lg border border-border bg-white p-5 shadow-card">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="text-sm font-medium text-textSecondary">品項摘要</p>
                <h2 className="mt-1 text-xl font-semibold text-textPrimary">批號管理品項</h2>
              </div>
              <div className="flex flex-wrap gap-2">
                <StatusBadge tone="info">{formatNumber(visibleItems.length)} 項</StatusBadge>
                <StatusBadge tone="neutral">
                  {formatNumber(data.start + 1)} - {formatNumber(data.start + data.count)} / {formatNumber(data.total)}
                </StatusBadge>
              </div>
            </div>
            <div className="mt-5 grid gap-3">
              {isLoading ? (
                <EmptyState title="正在載入批號品項" description="系統正在取得批號中心摘要資料。" />
              ) : visibleItems.length ? (
                visibleItems.map((item) => (
                  <ItemSummaryRow
                    isSelected={selectedItem?.itemNo === item.itemNo}
                    item={item}
                    key={item.itemNo}
                    onSelect={() => {
                      setSelectedItemNo(item.itemNo);
                      setSelectedRowKey("");
                      setIsDistributionLoading(true);
                      setIsDetailLoading(true);
                    }}
                  />
                ))
              ) : (
                <EmptyState title="沒有符合條件的品項批號" description="請調整搜尋或篩選條件。" />
              )}
            </div>
          </article>

          <div className="space-y-5">
            <article className="rounded-lg border border-border bg-white p-5 shadow-card">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p className="text-sm font-medium text-textSecondary">批號分布</p>
                  <h2 className="mt-1 text-xl font-semibold text-textPrimary">
                    {selectedItem ? selectedItem.itemName || selectedItem.itemNo : "批號分布"}
                  </h2>
                </div>
                {selectedItem ? <StatusBadge tone={selectedItem.tone}>{selectedItem.ownerDepartmentLabel}</StatusBadge> : null}
              </div>
              <div className="mt-5">
                {showDistributionLoading ? (
                  <EmptyState title="正在載入批號分布" description="系統正在取得此品項的批號與倉庫分布。" />
                ) : visibleBatches.length ? (
                  <BatchDistributionRows
                    batches={visibleBatches}
                    selectedRowKey={selectedBatch?.rowKey}
                    onSelect={(batch) => {
                      setSelectedRowKey(batch.rowKey);
                      setIsDetailLoading(true);
                    }}
                  />
                ) : (
                  <EmptyState title="沒有符合條件的批號分布" description="目前此品項沒有可顯示的批號分布資料。" />
                )}
              </div>
            </article>

            <BatchDetailPanel detail={activeDetail} selectedBatch={selectedBatch} isLoading={isDetailLoading} />
          </div>
        </section>

        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex items-start gap-3 text-textSecondary">
            <Database className="mt-0.5 h-5 w-5" aria-hidden="true" />
            <p className="text-sm leading-6">
              此畫面目前以查看批號庫存、品檢保留、來源單據與未完成任務為主；新增、調整、放行與出入庫執行會由相對應作業流程處理。
            </p>
          </div>
        </section>
      </div>
    </AppLayout>
  );
}
