"use client";

import {
  ChevronLeft,
  ChevronRight,
  GitBranch,
  Layers3,
  PackageCheck,
  Search
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { DataSourceToggle, type DataSourceMode } from "@/components/common/data-source-toggle";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { SupportEmptyState } from "@/components/common/support-empty-state";
import { StatusBadge } from "@/components/ui/status-badge";
import { useBomDashboard } from "@/hooks/use-bom-dashboard";
import { useLanguage } from "@/i18n/language-provider";
import { AppLayout } from "@/layouts/app-layout";
import { getBomDetail, type BomDashboardQuery } from "@/services/bom-api";
import type { BomDashboardData, BomDashboardItem, BomDetail, BomVersionStateCode } from "@/types/bom";

const versionStateFilters: { value: "" | BomVersionStateCode; label: string }[] = [
  { value: "", label: "全部版本狀態" },
  { value: "effective", label: "目前有效" },
  { value: "future", label: "未來生效" },
  { value: "historical", label: "歷史版本" },
  { value: "unknown", label: "待確認" }
];

const pageSizeOptions = [25, 50, 100] as const;

function formatInteger(value: number | undefined, language: string) {
  return new Intl.NumberFormat(language, { maximumFractionDigits: 0 }).format(value ?? 0);
}

function formatNumber(value: number | undefined, language: string, maximumFractionDigits = 2) {
  return new Intl.NumberFormat(language, {
    maximumFractionDigits,
    minimumFractionDigits: maximumFractionDigits
  }).format(value ?? 0);
}

function normalizeSearch(value: string) {
  return value.trim().toLocaleLowerCase();
}

function itemMatchesSearch(item: BomDashboardItem, search: string) {
  if (!search) {
    return true;
  }
  return [
    item.bomNo,
    item.bomName,
    item.version,
    item.date,
    item.unit,
    item.versionStateLabel,
    item.versionStateCode
  ].some((value) => String(value).toLocaleLowerCase().includes(search));
}

function EmptyList({ title, description }: { title: string; description: string }) {
  return <SupportEmptyState title={title} description={description} />;
}

function VersionStateBoard({ data, language }: { data: BomDashboardData; language: string }) {
  const columns = [
    {
      code: "effective",
      label: "目前有效",
      count: data.summary.effectiveVersionCount,
      tone: "success" as const
    },
    {
      code: "future",
      label: "未來生效",
      count: data.summary.futureVersionCount,
      tone: "info" as const
    },
    {
      code: "historical",
      label: "歷史版本",
      count: data.summary.historicalVersionCount,
      tone: "neutral" as const
    },
    {
      code: "unknown",
      label: "待確認",
      count: Math.max(
        data.summary.versionCount -
          data.summary.effectiveVersionCount -
          data.summary.futureVersionCount -
          data.summary.historicalVersionCount,
        0
      ),
      tone: "warning" as const
    }
  ];

  return (
    <section className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">Version State</p>
          <h3 className="mt-1 text-lg font-semibold text-textPrimary">BOM 版本狀態</h3>
        </div>
        <StatusBadge tone="neutral">共 {formatInteger(data.summary.versionCount, language)} 個版本</StatusBadge>
      </div>
      <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        {columns.map((column) => (
          <div className="rounded-lg border border-border bg-slate-50 p-3" key={column.code}>
            <div className="flex items-center justify-between gap-3">
              <p className="font-medium text-textPrimary">{column.label}</p>
              <StatusBadge tone={column.tone}>{formatInteger(column.count, language)}</StatusBadge>
            </div>
            <p className="mt-2 text-xs leading-5 text-textSecondary">
              由後端 `versionStateCode` 回傳 code，前端轉換顯示文字；不代表核准簽核流程。
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}

function BomVersionTable({
  items,
  selectedId,
  searchQuery,
  language,
  onSelect
}: {
  items: BomDashboardItem[];
  selectedId?: string;
  searchQuery: string;
  language: string;
  onSelect: (item: BomDashboardItem) => void;
}) {
  const visibleItems = useMemo(() => items.filter((item) => itemMatchesSearch(item, searchQuery)), [items, searchQuery]);

  if (!visibleItems.length) {
    return <EmptyList title="沒有符合條件的 BOM 版本" description="請調整搜尋、版本狀態或確認 API 是否有回傳資料。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[980px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">BOM / 名稱</th>
              <th className="px-4 py-3 text-right">版本</th>
              <th className="px-4 py-3">生效日</th>
              <th className="px-4 py-3">單位</th>
              <th className="px-4 py-3 text-right">基準重量</th>
              <th className="px-4 py-3 text-right">明細</th>
              <th className="px-4 py-3 text-right">關聯產品</th>
              <th className="px-4 py-3">狀態</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {visibleItems.map((item) => {
              const isSelected = item.id === selectedId;
              return (
                <tr
                  className={`cursor-pointer transition ${isSelected ? "bg-info/10" : "hover:bg-slate-50"}`}
                  key={item.id}
                  onClick={() => onSelect(item)}
                >
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{item.bomNo || "未提供 BOM no"}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.bomName || "未命名商品配方"}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">V{formatInteger(item.version, language)}</td>
                  <td className="px-4 py-3 text-textPrimary">{item.date || "未提供"}</td>
                  <td className="px-4 py-3 text-textPrimary">{item.unit || "未提供"}</td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatNumber(item.weight, language)}</td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatInteger(item.itemCount, language)}</td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatInteger(item.linkedProductCount, language)}</td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={item.tone}>{item.versionStateLabel}</StatusBadge>
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

function PaginationControls({
  page,
  pageSize,
  total,
  rowCount,
  language,
  isLoading,
  onPageChange,
  onPageSizeChange
}: {
  page: number;
  pageSize: number;
  total: number;
  rowCount: number;
  language: string;
  isLoading: boolean;
  onPageChange: (page: number) => void;
  onPageSizeChange: (pageSize: number) => void;
}) {
  const pageStart = total > 0 ? page * pageSize + 1 : 0;
  const pageEnd = total > 0 ? Math.min(page * pageSize + rowCount, total) : 0;
  const pageCount = Math.max(1, Math.ceil(total / pageSize));
  const canGoPrevious = page > 0 && !isLoading;
  const canGoNext = page + 1 < pageCount && !isLoading;

  return (
    <div className="flex flex-col gap-3 rounded-lg border border-border bg-white p-3 shadow-card md:flex-row md:items-center md:justify-between">
      <div className="text-sm text-textSecondary">
        <span className="font-medium text-textPrimary">BOM 版本清單</span>
        <span className="ml-2">
          {formatInteger(pageStart, language)}-{formatInteger(pageEnd, language)} / {formatInteger(total, language)} 筆
        </span>
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <label className="flex h-9 items-center gap-2 rounded-input border border-border bg-slate-50 px-3 text-sm text-textSecondary">
          每頁
          <select
            className="bg-transparent font-medium text-textPrimary outline-none"
            aria-label="BOM 每頁筆數"
            value={pageSize}
            onChange={(event) => onPageSizeChange(Number(event.target.value))}
          >
            {pageSizeOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </label>
        <button
          className="inline-flex h-9 items-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
          disabled={!canGoPrevious}
          onClick={() => onPageChange(Math.max(page - 1, 0))}
          type="button"
        >
          <ChevronLeft className="h-4 w-4" aria-hidden="true" />
          上一頁
        </button>
        <span className="min-w-[92px] text-center text-sm text-textSecondary">
          {formatInteger(page + 1, language)} / {formatInteger(pageCount, language)}
        </span>
        <button
          className="inline-flex h-9 items-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
          disabled={!canGoNext}
          onClick={() => onPageChange(page + 1)}
          type="button"
        >
          下一頁
          <ChevronRight className="h-4 w-4" aria-hidden="true" />
        </button>
      </div>
    </div>
  );
}

function BomDetailPanel({
  item,
  detail,
  isLoading,
  error,
  language,
  onVersionSelect
}: {
  item?: BomDashboardItem;
  detail?: BomDetail;
  isLoading: boolean;
  error?: string;
  language: string;
  onVersionSelect: (version: number) => void;
}) {
  if (!item) {
    return (
      <aside className="rounded-lg border border-border bg-white p-4 shadow-card">
        <EmptyList title="尚未選取 BOM" description="請從左側 BOM 版本清單選取一筆資料。" />
      </aside>
    );
  }

  const bom = detail?.bom ?? item;

  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">BOM Detail</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{bom.bomNo}</h2>
          <p className="mt-1 text-sm text-textSecondary">
            {bom.bomName || "未命名商品配方"} · V{formatInteger(bom.version, language)}
          </p>
        </div>
        <StatusBadge tone={bom.tone}>{bom.versionStateLabel}</StatusBadge>
      </div>

      {isLoading ? <p className="rounded-md bg-info/10 px-3 py-2 text-sm text-info">載入 BOM 明細中...</p> : null}
      {error ? (
        <p className="rounded-md border border-warning/20 bg-warning/10 px-3 py-2 text-sm text-warning">
          BOM detail API 暫時無法取得，右側保留清單摘要。{error}
        </p>
      ) : null}

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">生效日</p>
          <p className="mt-1 font-semibold text-textPrimary">{bom.date || "未提供"}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">基準</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(bom.weight, language)} {bom.unit}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">明細筆數</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatInteger(bom.itemCount, language)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">關聯產品</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatInteger(bom.linkedProductCount, language)}</p>
        </div>
      </div>

      {detail?.versions.length ? (
        <div className="space-y-2">
          <p className="text-sm font-semibold text-textPrimary">版本切換</p>
          <div className="flex flex-wrap gap-2">
            {detail.versions.map((version) => (
              <button
                className={`inline-flex h-9 items-center gap-2 rounded-button px-3 text-sm font-medium transition ${
                  version.version === bom.version ? "bg-primary text-white" : "bg-slate-100 text-textSecondary hover:bg-slate-200"
                }`}
                key={`${bom.bomNo}-${version.version}`}
                onClick={() => onVersionSelect(version.version)}
                type="button"
              >
                V{formatInteger(version.version, language)}
              </button>
            ))}
          </div>
        </div>
      ) : null}

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">直接配方明細</p>
        {detail?.items.length ? (
          <div className="overflow-hidden rounded-md border border-border">
            <table className="w-full border-collapse text-sm">
              <thead className="bg-slate-50 text-left text-xs font-semibold text-textSecondary">
                <tr>
                  <th className="px-3 py-2">料品</th>
                  <th className="px-3 py-2 text-right">用量</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {detail.items.map((material) => (
                  <tr key={`${material.itemNo}-${material.weight}`}>
                    <td className="px-3 py-2">
                      <p className="font-medium text-textPrimary">{material.itemNo || "未提供料號"}</p>
                      <p className="mt-1 text-xs text-textSecondary">{material.itemName || "未命名原料"}</p>
                    </td>
                    <td className="px-3 py-2 text-right text-textPrimary">
                      {formatNumber(material.weight, language)} {material.unit}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <EmptyList title="沒有配方明細" description="API 目前沒有回傳此 BOM 版本的直接 bom_item 明細。" />
        )}
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">關聯產品版本</p>
        {detail?.linkedProducts.length ? (
          detail.linkedProducts.map((product) => (
            <div className="rounded-md border border-border px-3 py-2 text-sm" key={`${product.productNo}-${product.productVersion}-${product.itemNo}`}>
              <div className="flex items-center justify-between gap-3">
                <p className="font-medium text-textPrimary">
                  {product.productNo} / V{formatInteger(product.productVersion, language)}
                </p>
                <StatusBadge tone="info">{product.levelLabel}</StatusBadge>
              </div>
              <p className="mt-1 text-xs text-textSecondary">
                {product.itemTypeLabel} · {product.itemNo || "無品項 no"} · {formatInteger(product.count, language)} 份 ·{" "}
                {formatNumber(product.weight, language)} {product.unit}
              </p>
            </div>
          ))
        ) : (
          <EmptyList title="沒有關聯產品" description="目前沒有 `product_spec.bom_no` 關聯資料。" />
        )}
      </div>
    </aside>
  );
}

export default function BomPage() {
  const { language } = useLanguage();
  const [dataSourceMode, setDataSourceMode] = useState<DataSourceMode>("api");
  const [searchValue, setSearchValue] = useState("");
  const [versionStateCode, setVersionStateCode] = useState<"" | BomVersionStateCode>("");
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState<number>(50);
  const [selectedBomNo, setSelectedBomNo] = useState<string>();
  const [selectedVersion, setSelectedVersion] = useState<number>();
  const [detailState, setDetailState] = useState<{
    bomNo?: string;
    version?: number;
    detail?: BomDetail;
    error?: string;
  }>({});

  const searchQuery = normalizeSearch(searchValue);
  const query = useMemo<BomDashboardQuery>(
    () => ({
      keyword: searchValue.trim() || undefined,
      versionStateCode: versionStateCode || undefined,
      start: page * pageSize,
      count: pageSize
    }),
    [page, pageSize, searchValue, versionStateCode]
  );
  const { data, error, isLoading, source } = useBomDashboard(dataSourceMode, query);
  const selectedItem =
    data.items.find((item) => item.bomNo === selectedBomNo && item.version === selectedVersion) ??
    data.items.find((item) => item.bomNo === selectedBomNo) ??
    data.items[0];
  const selectedDetailVersion = selectedVersion ?? selectedItem?.version;

  function resetPagination() {
    setPage(0);
  }

  useEffect(() => {
    if (!selectedItem?.bomNo) {
      return;
    }

    let isMounted = true;

    getBomDetail(selectedItem.bomNo, selectedDetailVersion, selectedItem, dataSourceMode).then((result) => {
      if (!isMounted) {
        return;
      }
      setDetailState({
        bomNo: selectedItem.bomNo,
        version: selectedDetailVersion,
        detail: result.detail,
        error: result.error
      });
    });

    return () => {
      isMounted = false;
    };
  }, [selectedItem, selectedDetailVersion, dataSourceMode]);

  const activeDetail =
    detailState.bomNo === selectedItem?.bomNo && detailState.version === selectedDetailVersion ? detailState.detail : undefined;
  const activeDetailError =
    detailState.bomNo === selectedItem?.bomNo && detailState.version === selectedDetailVersion ? detailState.error : undefined;
  const isDetailLoading = Boolean(
    selectedItem?.bomNo && (detailState.bomNo !== selectedItem.bomNo || detailState.version !== selectedDetailVersion)
  );

  return (
    <AppLayout activePath="/bom" title="BOM 中心">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">BOM Center V1</StatusBadge>
                <StatusBadge tone={source === "api" ? "success" : "warning"}>
                  {source === "api" ? "API data" : "Mock data"}
                </StatusBadge>
                {isLoading ? <StatusBadge tone="info">Loading API</StatusBadge> : null}
                <StatusBadge tone="neutral">read-only / direct bom_item</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">BOM 中心</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                集中檢視商品配方版本、有效日期、直接配方明細與產品版本關聯。本頁不呈現成本試算、報價、合約或 BOM 寫入操作。
              </p>
            </div>
            <div className="grid gap-2 md:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  aria-label="搜尋 BOM、名稱或料品"
                  value={searchValue}
                  onChange={(event) => {
                    setSearchValue(event.target.value);
                    resetPagination();
                  }}
                  placeholder="BOM / 名稱 / 料品"
                />
              </label>
              <select
                className="h-10 rounded-input border border-border bg-white px-3 text-sm font-medium text-textSecondary outline-none"
                aria-label="BOM 版本狀態"
                value={versionStateCode}
                onChange={(event) => {
                  setVersionStateCode(event.target.value as "" | BomVersionStateCode);
                  resetPagination();
                }}
              >
                {versionStateFilters.map((filter) => (
                  <option key={filter.value || "all"} value={filter.value}>
                    {filter.label}
                  </option>
                ))}
              </select>
              <DataSourceToggle
                value={dataSourceMode}
                onChange={(mode) => {
                  setDataSourceMode(mode);
                  resetPagination();
                }}
              />
            </div>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-danger/20 bg-danger/10 px-4 py-3 text-sm text-danger">
            BOM Center API 發生錯誤，畫面未改用 mock 資料。可切換資料來源為 Mock 進行前端預覽。{error}
          </p>
        ) : null}

        <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-5">
          {data.kpis.map((item) => (
            <ModuleKpiCard {...item} key={item.label} />
          ))}
        </section>

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="min-w-0 space-y-4">
            <VersionStateBoard data={data} language={language} />

            <div className="flex flex-wrap items-center gap-2 text-xs text-textSecondary">
              <StatusBadge tone="neutral">BOM {formatInteger(data.summary.bomCount, language)}</StatusBadge>
              <StatusBadge tone="neutral">版本 {formatInteger(data.summary.versionCount, language)}</StatusBadge>
              <span>目前頁面回傳 {formatInteger(data.count, language)} 筆</span>
            </div>

            <PaginationControls
              page={page}
              pageSize={pageSize}
              total={data.total}
              rowCount={data.items.length}
              language={language}
              isLoading={isLoading}
              onPageChange={setPage}
              onPageSizeChange={(nextPageSize) => {
                setPageSize(nextPageSize);
                resetPagination();
              }}
            />

            <BomVersionTable
              items={data.items}
              selectedId={selectedItem?.id}
              searchQuery={searchQuery}
              language={language}
              onSelect={(item) => {
                setSelectedBomNo(item.bomNo);
                setSelectedVersion(item.version);
              }}
            />
          </div>

          <BomDetailPanel
            item={selectedItem}
            detail={activeDetail}
            isLoading={isDetailLoading}
            error={activeDetailError}
            language={language}
            onVersionSelect={(version) => {
              setSelectedBomNo(selectedItem?.bomNo);
              setSelectedVersion(version);
            }}
          />
        </section>

        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="grid gap-3 md:grid-cols-3">
            <div className="flex gap-3">
              <GitBranch className="mt-1 h-5 w-5 text-textSecondary" aria-hidden="true" />
              <div>
                <p className="font-semibold text-textPrimary">版本視角</p>
                <p className="mt-1 text-sm text-textSecondary">同一 BOM no 的不同版本會各自列為一筆。</p>
              </div>
            </div>
            <div className="flex gap-3">
              <Layers3 className="mt-1 h-5 w-5 text-textSecondary" aria-hidden="true" />
              <div>
                <p className="font-semibold text-textPrimary">直接明細</p>
                <p className="mt-1 text-sm text-textSecondary">V1 僅呈現 `bom_item`，不遞迴展開 bom1 / bom2。</p>
              </div>
            </div>
            <div className="flex gap-3">
              <PackageCheck className="mt-1 h-5 w-5 text-textSecondary" aria-hidden="true" />
              <div>
                <p className="font-semibold text-textPrimary">產品關聯</p>
                <p className="mt-1 text-sm text-textSecondary">依 `product_spec.bom_no` 顯示關聯產品版本。</p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </AppLayout>
  );
}
