"use client";

import { AlertTriangle, Factory, GitBranch, Loader2, Network, PackageCheck, Route, Search, Timer, Workflow } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { DataSourceStatusBadge } from "@/components/common/data-source-status-badge";
import { DataSourceToggle, type DataSourceMode } from "@/components/common/data-source-toggle";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { SupportEmptyState } from "@/components/common/support-empty-state";
import { StatusBadge } from "@/components/ui/status-badge";
import { useRoutingDashboard } from "@/hooks/use-routing-dashboard";
import { useLanguage } from "@/i18n/language-provider";
import { AppLayout } from "@/layouts/app-layout";
import { getRoutingDetail, type RoutingDashboardQuery } from "@/services/routing-api";
import type { RoutingContextReference, RoutingDetail, RoutingProductItem } from "@/types/routing";

function formatNumber(value: number | undefined, language: string, digits = 2) {
  return new Intl.NumberFormat(language, {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits
  }).format(value ?? 0);
}

function formatInteger(value: number | undefined, language: string) {
  return new Intl.NumberFormat(language, { maximumFractionDigits: 0 }).format(value ?? 0);
}

function normalizeSearch(value: string) {
  return value.trim().toLocaleLowerCase();
}

function itemMatchesSearch(item: RoutingProductItem, search: string) {
  if (!search) {
    return true;
  }
  return [item.itemNo, item.itemName, item.itemTypeLabel, item.routingNo, item.routingVersion, item.versionStateLabel, item.sourceLabel].some((value) =>
    String(value).toLocaleLowerCase().includes(search)
  );
}

function ProductWipSelector({
  items,
  selectedId,
  searchQuery,
  language,
  onSelect
}: {
  items: RoutingProductItem[];
  selectedId?: string;
  searchQuery: string;
  language: string;
  onSelect: (item: RoutingProductItem) => void;
}) {
  const rows = useMemo(() => items.filter((item) => itemMatchesSearch(item, searchQuery)), [items, searchQuery]);

  if (!rows.length) {
    return <SupportEmptyState title="沒有符合條件的 Product / WIP" description="請調整關鍵字，或確認 Routing / Process Flow API 是否已提供資料。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[860px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">Product / WIP</th>
              <th className="px-4 py-3">Routing</th>
              <th className="px-4 py-3 text-right">步驟</th>
              <th className="px-4 py-3 text-right">警示</th>
              <th className="px-4 py-3">來源</th>
              <th className="px-4 py-3">狀態</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {rows.map((item) => {
              const isSelected = item.id === selectedId;
              return (
                <tr className={`cursor-pointer transition ${isSelected ? "bg-info/10" : "hover:bg-slate-50"}`} key={item.id} onClick={() => onSelect(item)}>
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{item.itemNo || "未提供品項"}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {item.itemName || "未命名品項"} · {item.itemTypeLabel}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{item.routingNo || "未提供 Routing"}</p>
                    <p className="mt-1 text-xs text-textSecondary">V{formatInteger(item.routingVersion, language)}</p>
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatInteger(item.stepCount, language)}</td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatInteger(item.warningCount, language)}</td>
                  <td className="px-4 py-3 text-textSecondary">{item.sourceLabel}</td>
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

function OrderedProcessFlow({ detail, language }: { detail?: RoutingDetail; language: string }) {
  if (!detail?.steps.length) {
    return <SupportEmptyState title="沒有製程流程" description="此 Routing 版本尚未回傳 process flow 步驟。" />;
  }

  return (
    <section className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex items-center gap-2">
        <Workflow className="h-4 w-4 text-primary" aria-hidden="true" />
        <p className="text-sm font-semibold text-textPrimary">Ordered Process Flow</p>
      </div>
      <div className="mt-4 space-y-3">
        {detail.steps.map((step, index) => (
          <div className="grid gap-3 rounded-lg border border-border bg-slate-50 p-4 md:grid-cols-[80px_minmax(0,1fr)_220px]" key={`${step.stepNo}-${step.processNo}`}>
            <div>
              <p className="text-xs text-textSecondary">Step</p>
              <p className="mt-1 text-xl font-semibold text-textPrimary">{formatInteger(step.stepNo || index + 1, language)}</p>
            </div>
            <div className="min-w-0">
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">{step.stageLabel}</StatusBadge>
                <StatusBadge tone="neutral">{step.groupLabel}</StatusBadge>
              </div>
              <p className="mt-2 font-semibold text-textPrimary">{step.processNo || "未提供製程 no"}</p>
              <p className="mt-1 text-sm text-textSecondary">{step.processLabel || "未命名製程"} · {step.sourceRef || "未提供來源"}</p>
            </div>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="rounded-md bg-white p-3">
                <p className="text-xs text-textSecondary">標準產出</p>
                <p className="mt-1 font-semibold text-textPrimary">
                  {formatNumber(step.standardQuantity, language)} {step.standardUnit}
                </p>
              </div>
              <div className="rounded-md bg-white p-3">
                <p className="text-xs text-textSecondary">標準時間</p>
                <p className="mt-1 font-semibold text-textPrimary">{formatInteger(step.standardMinutes, language)} 分</p>
              </div>
              <div className="rounded-md bg-white p-3">
                <p className="text-xs text-textSecondary">效率基準</p>
                <p className="mt-1 font-semibold text-textPrimary">{step.standardRateLabel}</p>
              </div>
              <div className="rounded-md bg-white p-3">
                <p className="text-xs text-textSecondary">資源資格</p>
                <p className="mt-1 font-semibold text-textPrimary">{step.resourceEligibilityLabel}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function ReferenceCards({ title, icon: Icon, items }: { title: string; icon: typeof Route; items: RoutingContextReference[] }) {
  if (!items.length) {
    return <SupportEmptyState title={`沒有${title}`} description={`目前未回傳${title}；若此項為必要治理資訊，後端可用 warning code 表示。`} />;
  }

  return (
    <section className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex items-center gap-2">
        <Icon className="h-4 w-4 text-primary" aria-hidden="true" />
        <p className="text-sm font-semibold text-textPrimary">{title}</p>
      </div>
      <div className="mt-3 grid gap-3 md:grid-cols-2">
        {items.map((item) => (
          <div className="rounded-md bg-slate-50 p-3" key={`${item.typeLabel}-${item.refNo}`}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-xs text-textSecondary">{item.typeLabel}</p>
                <p className="mt-1 font-semibold text-textPrimary">{item.refNo || "未提供 no"}</p>
                <p className="mt-1 text-sm text-textSecondary">{item.refName || "未命名參照"}</p>
              </div>
              <StatusBadge tone={item.tone}>{item.statusLabel}</StatusBadge>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function LineageWarningPanel({ detail }: { detail?: RoutingDetail }) {
  return (
    <div className="grid gap-3 lg:grid-cols-2">
      <section className="rounded-lg border border-border bg-white p-4 shadow-card">
        <div className="flex items-center gap-2">
          <Network className="h-4 w-4 text-primary" aria-hidden="true" />
          <p className="text-sm font-semibold text-textPrimary">Source Lineage</p>
        </div>
        <div className="mt-3 space-y-2">
          {detail?.lineage.length ? (
            detail.lineage.map((lineage) => (
              <div className="rounded-md bg-slate-50 p-3 text-sm" key={`${lineage.sourceTypeLabel}-${lineage.sourceRef}`}>
                <p className="font-medium text-textPrimary">
                  {lineage.sourceTypeLabel} · {lineage.sourceRef || "未提供來源"}
                </p>
                <p className="mt-1 text-xs text-textSecondary">
                  {lineage.evidenceLabel} · {lineage.statusLabel}
                </p>
              </div>
            ))
          ) : (
            <SupportEmptyState title="沒有 source lineage" description="後端尚未回傳 Routing / Process Flow 來源依據。" />
          )}
        </div>
      </section>

      <section className="rounded-lg border border-border bg-white p-4 shadow-card">
        <div className="flex items-center gap-2">
          <AlertTriangle className="h-4 w-4 text-warning" aria-hidden="true" />
          <p className="text-sm font-semibold text-textPrimary">Controlled Warnings</p>
        </div>
        <div className="mt-3 space-y-2">
          {detail?.warnings.length ? (
            detail.warnings.map((warning, index) => (
              <p className="rounded-md border border-warning/20 bg-warning/10 px-3 py-2 text-sm leading-6 text-warning" key={`${warning.code}-${warning.refNo}-${index}`}>
                {warning.message}
                {warning.refNo ? `（${warning.refNo}）` : ""}
              </p>
            ))
          ) : (
            <p className="rounded-md bg-success/10 px-3 py-2 text-sm text-success">目前沒有未解警示。</p>
          )}
        </div>
      </section>
    </div>
  );
}

function DetailPanel({
  selectedItem,
  detail,
  isLoading,
  error,
  language,
  onVersionSelect
}: {
  selectedItem?: RoutingProductItem;
  detail?: RoutingDetail;
  isLoading: boolean;
  error?: string;
  language: string;
  onVersionSelect: (version: number) => void;
}) {
  if (!selectedItem) {
    return (
      <aside className="rounded-lg border border-border bg-white p-4 shadow-card">
        <SupportEmptyState title="尚未選取 Product / WIP" description="請從左側清單選擇一筆品項以查看 Routing Version。" />
      </aside>
    );
  }

  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium text-textSecondary">Routing Version</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{selectedItem.routingNo || "未提供 Routing"}</h2>
          <p className="mt-1 text-sm text-textSecondary">
            {selectedItem.itemNo} · V{formatInteger(selectedItem.routingVersion, language)}
          </p>
        </div>
        <StatusBadge tone={selectedItem.tone}>{selectedItem.versionStateLabel}</StatusBadge>
      </div>

      {isLoading ? (
        <p className="flex items-center gap-2 rounded-md bg-info/10 px-3 py-2 text-sm text-info">
          <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
          載入 Routing / Process Flow 明細中...
        </p>
      ) : null}
      {error ? (
        <p className="rounded-md border border-danger/20 bg-danger/10 px-3 py-2 text-sm leading-6 text-danger">
          Routing / Process Flow 明細取得失敗，畫面未改用示範資料。{error}
        </p>
      ) : null}

      {detail?.versions.length ? (
        <div className="space-y-2">
          <p className="text-sm font-semibold text-textPrimary">版本</p>
          <div className="flex flex-wrap gap-2">
            {detail.versions.map((version) => (
              <button
                className={`inline-flex h-9 items-center rounded-button px-3 text-sm font-medium transition ${
                  version.version === selectedItem.routingVersion ? "bg-primary text-white" : "bg-slate-100 text-textSecondary hover:bg-slate-200"
                }`}
                key={`${selectedItem.itemNo}-${version.version}`}
                onClick={() => onVersionSelect(version.version)}
                type="button"
              >
                V{formatInteger(version.version, language)} · {version.versionStateLabel}
              </button>
            ))}
          </div>
        </div>
      ) : null}

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">品項類型</p>
          <p className="mt-1 font-semibold text-textPrimary">{selectedItem.itemTypeLabel}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">流程步驟</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatInteger(detail?.steps.length ?? selectedItem.stepCount, language)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">Recipe 參照</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatInteger(detail?.recipeReferences.length ?? 0, language)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">警示</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatInteger(detail?.warnings.length ?? selectedItem.warningCount, language)}</p>
        </div>
      </div>
    </aside>
  );
}

export default function RoutingProcessFlowPage() {
  const { language } = useLanguage();
  const [dataSourceMode, setDataSourceMode] = useState<DataSourceMode>("api");
  const [searchValue, setSearchValue] = useState("");
  const [selectedItemNo, setSelectedItemNo] = useState<string>();
  const [selectedVersion, setSelectedVersion] = useState<number>();
  const [detailState, setDetailState] = useState<{
    itemNo?: string;
    version?: number;
    detail?: RoutingDetail;
    error?: string;
  }>({});
  const query = useMemo<RoutingDashboardQuery>(
    () => ({
      keyword: searchValue.trim() || undefined,
      count: 50
    }),
    [searchValue]
  );
  const { data, error, isLoading, source } = useRoutingDashboard(dataSourceMode, query);
  const searchQuery = normalizeSearch(searchValue);
  const selectedItem =
    data.items.find((item) => item.itemNo === selectedItemNo && item.routingVersion === selectedVersion) ??
    data.items.find((item) => item.itemNo === selectedItemNo) ??
    data.items[0];
  const selectedDetailVersion = selectedVersion ?? selectedItem?.routingVersion;

  function handleDataSourceModeChange(mode: DataSourceMode) {
    setDataSourceMode(mode);
    setSelectedItemNo(undefined);
    setSelectedVersion(undefined);
    setDetailState({});
  }

  useEffect(() => {
    if (source !== dataSourceMode) {
      return;
    }
    if (!selectedItem?.itemNo || selectedDetailVersion === undefined) {
      return;
    }

    let isMounted = true;
    getRoutingDetail(selectedItem.itemNo, selectedDetailVersion, selectedItem, dataSourceMode).then((result) => {
      if (!isMounted) {
        return;
      }
      setDetailState({
        itemNo: selectedItem.itemNo,
        version: selectedDetailVersion,
        detail: result.detail,
        error: result.error
      });
    });

    return () => {
      isMounted = false;
    };
  }, [selectedItem, selectedDetailVersion, dataSourceMode, source]);

  const activeDetail = detailState.itemNo === selectedItem?.itemNo && detailState.version === selectedDetailVersion ? detailState.detail : undefined;
  const activeDetailError = detailState.itemNo === selectedItem?.itemNo && detailState.version === selectedDetailVersion ? detailState.error : undefined;
  const isDetailLoading = Boolean(selectedItem?.itemNo && (detailState.itemNo !== selectedItem.itemNo || detailState.version !== selectedDetailVersion));

  return (
    <AppLayout activePath="/routing" title="Routing / Process Flow">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">Read-only</StatusBadge>
                <DataSourceStatusBadge source={source} isLoading={isLoading} hasError={Boolean(error)} />
                <StatusBadge tone="neutral">Product / WIP 製程路線</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">Routing / Process Flow</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                檢視 Product / WIP 適用的製程路線、步驟順序、Recipe 參照、Packaging context、資源資格與標準表現；本畫面僅供查閱，不執行生產或排程。
              </p>
            </div>
            <div className="grid gap-2 md:grid-cols-[minmax(220px,1fr)_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  aria-label="搜尋 Product、WIP 或 Routing"
                  value={searchValue}
                  onChange={(event) => setSearchValue(event.target.value)}
                  placeholder="Product / WIP / Routing"
                />
              </label>
              <DataSourceToggle value={dataSourceMode} onChange={handleDataSourceModeChange} />
            </div>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-danger/20 bg-danger/10 px-4 py-3 text-sm text-danger">
            Routing / Process Flow 資料取得失敗，畫面未改用示範資料。{error}
          </p>
        ) : null}

        <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {data.kpis.map((item) => (
            <ModuleKpiCard {...item} key={item.label} />
          ))}
        </section>

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="min-w-0 space-y-4">
            <ProductWipSelector
              items={data.items}
              selectedId={selectedItem?.id}
              searchQuery={searchQuery}
              language={language}
              onSelect={(item) => {
                setSelectedItemNo(item.itemNo);
                setSelectedVersion(item.routingVersion);
              }}
            />
            <OrderedProcessFlow detail={activeDetail} language={language} />
            <div className="grid gap-4 xl:grid-cols-2">
              <ReferenceCards title="Recipe References" icon={GitBranch} items={activeDetail?.recipeReferences ?? []} />
              <ReferenceCards title="Packaging Context" icon={PackageCheck} items={activeDetail?.packagingContexts ?? []} />
              <ReferenceCards title="Resource Eligibility" icon={Factory} items={activeDetail?.resourceEligibility ?? []} />
              <ReferenceCards title="Standard Performance" icon={Timer} items={activeDetail?.standardPerformance ?? []} />
            </div>
            <LineageWarningPanel detail={activeDetail} />
          </div>

          <DetailPanel
            selectedItem={selectedItem}
            detail={activeDetail}
            isLoading={isDetailLoading}
            error={activeDetailError}
            language={language}
            onVersionSelect={(version) => {
              setSelectedItemNo(selectedItem?.itemNo);
              setSelectedVersion(version);
            }}
          />
        </section>
      </div>
    </AppLayout>
  );
}
