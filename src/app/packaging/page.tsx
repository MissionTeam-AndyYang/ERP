"use client";

import Link from "next/link";
import {
  AlertTriangle,
  Boxes,
  FileText,
  GitBranch,
  Loader2,
  PackageCheck,
  PackageSearch,
  Route,
  Search,
  ShieldCheck
} from "lucide-react";
import { useMemo, useState } from "react";
import { DataSourceStatusBadge } from "@/components/common/data-source-status-badge";
import { DataSourceToggle, type DataSourceMode } from "@/components/common/data-source-toggle";
import { SupportEmptyState } from "@/components/common/support-empty-state";
import { StatusBadge } from "@/components/ui/status-badge";
import { usePackagingOverview } from "@/hooks/use-packaging-overview";
import { useLanguage } from "@/i18n/language-provider";
import { AppLayout } from "@/layouts/app-layout";
import type { PackagingOverviewData, PackagingQuery, PackagingSpec, PackagingSpecLine } from "@/types/packaging";

type Scenario = "product" | "wip";

const scenarioDefaults: Record<Scenario, PackagingQuery> = {
  product: { itemNo: "PRD-SD-001", itemCategory: 5, productVersion: 1 },
  wip: { itemNo: "INP-SD-001", itemCategory: 4 }
};

function formatNumber(value: number | undefined, language: string, digits = 2) {
  return new Intl.NumberFormat(language, {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits
  }).format(value ?? 0);
}

function formatInteger(value: number | undefined, language: string) {
  return new Intl.NumberFormat(language, { maximumFractionDigits: 0 }).format(value ?? 0);
}

function SummaryMetric({ label, value, hint }: { label: string; value: string; hint?: string }) {
  return (
    <div className="rounded-lg border border-border bg-slate-50 p-4">
      <p className="text-xs font-medium text-textSecondary">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-textPrimary">{value}</p>
      {hint ? <p className="mt-1 text-xs text-textSecondary">{hint}</p> : null}
    </div>
  );
}

function DomainNavigation({ itemNo }: { itemNo: string }) {
  const encoded = encodeURIComponent(itemNo);
  const links = [
    { label: "Product / WIP 360", href: `/product-360?itemNo=${encoded}`, icon: PackageSearch },
    { label: "BOM 中心", href: `/bom?productNo=${encoded}`, icon: GitBranch },
    { label: "Routing", href: `/routing?itemNo=${encoded}`, icon: Route },
    { label: "庫存批號", href: `/warehouse/inventory/lots?itemNo=${encoded}`, icon: Boxes }
  ];

  return (
    <div className="grid gap-2 sm:grid-cols-2 xl:grid-cols-4">
      {links.map((item) => {
        const Icon = item.icon;
        return (
          <Link
            className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary transition hover:border-primary/40 hover:text-primary"
            href={item.href}
            key={item.href}
          >
            <Icon className="h-4 w-4" aria-hidden="true" />
            {item.label}
          </Link>
        );
      })}
    </div>
  );
}

function PackagingSpecTable({ rows, language, selectedId, onSelect }: {
  rows: PackagingSpec[];
  language: string;
  selectedId: string;
  onSelect: (id: string) => void;
}) {
  if (!rows.length) {
    return <SupportEmptyState title="沒有包裝規格資料" description="後端 API 回傳空陣列；畫面如實呈現空狀態，未補入示範資料。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border">
      <div className="overflow-x-auto">
        <table className="min-w-[920px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold text-textSecondary">
            <tr>
              <th className="px-4 py-3">包裝階層</th>
              <th className="px-4 py-3">包材 BOM</th>
              <th className="px-4 py-3 text-right">規格份數</th>
              <th className="px-4 py-3 text-right">重量</th>
              <th className="px-4 py-3">來源</th>
              <th className="px-4 py-3">明細</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {rows.map((row) => (
              <tr className={selectedId === row.specId ? "bg-primary/5" : "bg-white"} key={row.specId}>
                <td className="px-4 py-3">
                  <div className="flex flex-wrap items-center gap-2">
                    <StatusBadge tone={row.tone}>{row.packagingLevelLabel}</StatusBadge>
                    <span className="text-xs text-textSecondary">Level {row.packagingLevel}</span>
                  </div>
                  {row.wipNo ? <p className="mt-1 text-xs text-warning">WIP context: {row.wipNo}</p> : null}
                </td>
                <td className="px-4 py-3">
                  <p className="font-semibold text-textPrimary">{row.packagingBomNo || "未提供 BOM No"}</p>
                  <p className="mt-1 text-xs text-textSecondary">{row.packagingBomName || "未提供名稱"}</p>
                </td>
                <td className="px-4 py-3 text-right text-textPrimary">
                  {formatInteger(row.count, language)} {row.unitLabel || "未提供單位"}
                </td>
                <td className="px-4 py-3 text-right text-textPrimary">
                  {formatNumber(row.weight, language)} {row.masterUnitLabel || row.unitLabel}
                  <p className="mt-1 text-xs text-textSecondary">主檔 {formatNumber(row.masterWeight, language)}</p>
                </td>
                <td className="px-4 py-3 text-textSecondary">
                  <p>{row.sourceLabel || "未提供"}</p>
                  <p className="mt-1 text-xs">主檔：{row.masterSourceLabel || "未提供"}</p>
                  <p className="mt-1 text-xs">明細：{row.lineSourceLabel || "未提供"}</p>
                </td>
                <td className="px-4 py-3">
                  <button
                    className="inline-flex h-9 items-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary transition hover:border-primary/40 hover:text-primary"
                    onClick={() => onSelect(row.specId)}
                    type="button"
                  >
                    <FileText className="h-4 w-4" aria-hidden="true" />
                    查看
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function PackagingLineTable({ rows, language }: { rows: PackagingSpecLine[]; language: string }) {
  if (!rows.length) {
    return <SupportEmptyState title="沒有包材 BOM 明細" description="後端 API 回傳 lines 為空；請依來源警示確認 BOM2 明細是否已建立。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border">
      <div className="overflow-x-auto">
        <table className="min-w-[860px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold text-textSecondary">
            <tr>
              <th className="px-4 py-3">包材品項</th>
              <th className="px-4 py-3">類別</th>
              <th className="px-4 py-3 text-right">數量</th>
              <th className="px-4 py-3 text-right">重量</th>
              <th className="px-4 py-3 text-right">損耗</th>
              <th className="px-4 py-3">備註</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {rows.map((row, index) => (
              <tr key={`${row.parentBomNo}-${row.childNo}-${index}`}>
                <td className="px-4 py-3">
                  <p className="font-semibold text-textPrimary">{row.childNo || "未提供品項"}</p>
                  <p className="mt-1 text-xs text-textSecondary">{row.childName || "未提供名稱"}</p>
                </td>
                <td className="px-4 py-3 text-textSecondary">{row.childCategoryLabel}</td>
                <td className="px-4 py-3 text-right text-textPrimary">
                  {formatInteger(row.count, language)} {row.childUnitLabel || "未提供單位"}
                  <p className="mt-1 text-xs text-textSecondary">處理 {formatNumber(row.processCount, language)}</p>
                </td>
                <td className="px-4 py-3 text-right text-textPrimary">
                  {formatNumber(row.weight, language)} {row.childUnit2Label || row.childUnitLabel}
                  {row.length ? <p className="mt-1 text-xs text-textSecondary">長度 {formatNumber(row.length, language)}</p> : null}
                </td>
                <td className="px-4 py-3 text-right text-textPrimary">
                  {formatNumber(row.expectedLoss, language)}% / {formatNumber(row.actualLoss, language)}%
                </td>
                <td className="px-4 py-3 text-textSecondary">{row.comment || "無"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function SourceWarningPanel({ data }: { data: PackagingOverviewData }) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-textPrimary">來源與警示</h2>
          <p className="mt-1 text-sm text-textSecondary">保留資料來源，不把包裝規格畫面當成新的權威資料。</p>
        </div>
        <StatusBadge tone={data.warnings.length ? "warning" : "success"}>
          {data.warnings.length ? `${data.warnings.length} 項` : "無警示"}
        </StatusBadge>
      </div>

      <div className="space-y-2">
        {data.moduleReadiness.length ? (
          data.moduleReadiness.map((item) => (
            <div className="rounded-md bg-slate-50 p-3 text-sm" key={`${item.moduleCode}-${item.statusCode}`}>
              <div className="flex items-start justify-between gap-2">
                <div>
                  <p className="font-semibold text-textPrimary">{item.moduleLabel}</p>
                  <p className="mt-1 text-xs text-textSecondary">{item.sourceLabel || "未提供來源"}</p>
                </div>
                <StatusBadge tone={item.tone}>{item.statusLabel}</StatusBadge>
              </div>
              {item.warningCodes.length ? <p className="mt-2 text-xs text-warning">{item.warningCodes.join(" / ")}</p> : null}
            </div>
          ))
        ) : (
          <SupportEmptyState title="沒有 readiness 資料" description="API 回傳 moduleReadiness 為空。" />
        )}
      </div>

      <div className="space-y-2">
        {data.sourceLineage.length ? (
          data.sourceLineage.map((item) => (
            <div className="rounded-md bg-slate-50 p-3 text-sm" key={`${item.sourceTypeLabel}-${item.sourceLabel}`}>
              <p className="font-medium text-textPrimary">{item.sourceTypeLabel}</p>
              <div className="mt-2 flex items-center justify-between gap-2">
                <span className="text-xs text-textSecondary">{item.sourceLabel || "未提供"}</span>
                <StatusBadge tone={item.tone}>{item.tone === "warning" ? "需確認" : "已提供"}</StatusBadge>
              </div>
            </div>
          ))
        ) : (
          <SupportEmptyState title="沒有 source lineage" description="API 回傳來源清單為空。" />
        )}
      </div>

      <div className="space-y-2">
        {data.warnings.length ? (
          data.warnings.map((warning, index) => (
            <p
              className={`rounded-md border px-3 py-2 text-sm leading-6 ${
                warning.tone === "danger" ? "border-danger/20 bg-danger/10 text-danger" : "border-warning/20 bg-warning/10 text-warning"
              }`}
              key={`${warning.code}-${warning.refNo}-${index}`}
            >
              {warning.moduleLabel} · {warning.message}
              {warning.refNo ? `（${warning.refNo}）` : ""}
            </p>
          ))
        ) : (
          <p className="rounded-md bg-success/10 px-3 py-2 text-sm text-success">目前沒有未解警示。</p>
        )}
      </div>

      <div className="rounded-lg border border-success/20 bg-success/5 p-4">
        <div className="flex items-center gap-2 text-success">
          <ShieldCheck className="h-4 w-4" aria-hidden="true" />
          <p className="text-sm font-semibold">唯讀邊界</p>
        </div>
        <ul className="mt-3 space-y-2 text-sm leading-6 text-textSecondary">
          <li>不新增或修改包裝規格、包材 BOM、Product / WIP。</li>
          <li>不核准、不發布、不切換權威資料來源。</li>
          <li>不執行 Cutover、Go-Live 或生產作業。</li>
        </ul>
      </div>
    </aside>
  );
}

export default function PackagingSpecificationPage() {
  const { language } = useLanguage();
  const [dataSourceMode, setDataSourceMode] = useState<DataSourceMode>("api");
  const [scenario, setScenario] = useState<Scenario>("product");
  const [itemNoInput, setItemNoInput] = useState(scenarioDefaults.product.itemNo);
  const [productVersionInput, setProductVersionInput] = useState("1");
  const query = useMemo<PackagingQuery>(() => {
    const version = Number(productVersionInput);
    return {
      itemNo: itemNoInput.trim() || scenarioDefaults[scenario].itemNo,
      itemCategory: scenario === "wip" ? 4 : 5,
      ...(scenario === "product" && Number.isFinite(version) && version > 0 ? { productVersion: version } : {})
    };
  }, [itemNoInput, productVersionInput, scenario]);
  const { data, error, isLoading, source } = usePackagingOverview(query, dataSourceMode);
  const selectedSpecId = data.packagingSpecs[0]?.specId ?? "";
  const [manualSelectedSpecId, setManualSelectedSpecId] = useState("");
  const activeSpec = data.packagingSpecs.find((item) => item.specId === (manualSelectedSpecId || selectedSpecId)) ?? data.packagingSpecs[0];

  function selectScenario(nextScenario: Scenario) {
    setScenario(nextScenario);
    setItemNoInput(scenarioDefaults[nextScenario].itemNo);
    setProductVersionInput(nextScenario === "product" ? String(scenarioDefaults.product.productVersion ?? 1) : "");
    setManualSelectedSpecId("");
  }

  return (
    <AppLayout activePath="/packaging" title="包裝規格唯讀檢視">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">Read-only</StatusBadge>
                <DataSourceStatusBadge source={source} isLoading={isLoading} hasError={Boolean(error)} />
                <StatusBadge tone="neutral">Packaging Specification</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">包裝規格唯讀檢視</h2>
              <p className="mt-2 max-w-4xl text-sm leading-6 text-textSecondary">
                以 Product 或 WIP identity 查詢包裝階層、包材 BOM、規格份數、重量、單位與來源警示。此頁只做檢視與導覽，包裝規格維護流程保留於後續正式權限與 mutation API 規劃。
              </p>
            </div>
            <div className="grid gap-2 md:grid-cols-[auto_minmax(220px,1fr)_120px_auto]">
              <div className="inline-flex h-10 rounded-button border border-border bg-white p-1">
                {(["product", "wip"] as const).map((item) => (
                  <button
                    className={`rounded-button px-3 text-sm font-medium transition ${scenario === item ? "bg-primary text-white" : "text-textSecondary hover:bg-slate-100"}`}
                    key={item}
                    onClick={() => selectScenario(item)}
                    type="button"
                  >
                    {item === "product" ? "Product" : "WIP"}
                  </button>
                ))}
              </div>
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  aria-label="查詢 Product 或 WIP"
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  onChange={(event) => {
                    setItemNoInput(event.target.value);
                    setManualSelectedSpecId("");
                  }}
                  placeholder="itemNo"
                  value={itemNoInput}
                />
              </label>
              <input
                aria-label="產品版本"
                className="h-10 rounded-input border border-border bg-slate-50 px-3 text-sm outline-none disabled:bg-slate-100 disabled:text-textSecondary"
                disabled={scenario === "wip"}
                onChange={(event) => {
                  setProductVersionInput(event.target.value);
                  setManualSelectedSpecId("");
                }}
                placeholder="版本"
                value={productVersionInput}
              />
              <DataSourceToggle value={dataSourceMode} onChange={setDataSourceMode} />
            </div>
          </div>
        </section>

        {isLoading ? (
          <p className="flex items-center gap-2 rounded-lg border border-info/20 bg-info/10 px-4 py-3 text-sm text-info">
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
            包裝規格資料載入中...
          </p>
        ) : null}

        {error ? (
          <p className="rounded-lg border border-danger/20 bg-danger/10 px-4 py-3 text-sm leading-6 text-danger">
            包裝規格 API 資料取得失敗，畫面未改用示範資料。{error}
          </p>
        ) : null}

        {!isLoading && !error && !data.subject ? (
          <SupportEmptyState title="沒有包裝規格主體資料" description="後端 API 回傳空資料；畫面如實呈現 true empty state。" />
        ) : null}

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="min-w-0 space-y-5">
            <section className="rounded-lg border border-border bg-white p-4 shadow-card">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p className="text-xs font-medium text-textSecondary">Packaging Subject</p>
                  <h2 className="mt-1 text-xl font-semibold text-textPrimary">
                    {data.subject?.itemNo || query.itemNo || "未選取"} · {data.subject?.itemName || "尚未取得主體資料"}
                  </h2>
                  <p className="mt-2 text-sm text-textSecondary">
                    {data.subject?.itemCategoryLabel || (scenario === "product" ? "製成品" : "在製品")} · {data.subject?.sourceLabel || "未提供來源"}
                    {data.subject?.comment ? ` · ${data.subject.comment}` : ""}
                  </p>
                </div>
                <StatusBadge tone={data.subject?.tone ?? (error ? "danger" : "neutral")}>{data.subject?.versionLabel || "待載入"}</StatusBadge>
              </div>
              <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
                <SummaryMetric label="包裝規格" value={`${formatInteger(data.summary.packagingSpecCount, language)} 筆`} hint={`${formatInteger(data.summary.packageLevelCount, language)} 個階層`} />
                <SummaryMetric label="包材 BOM" value={`${formatInteger(data.summary.packagingBomCount, language)} 組`} hint={`${formatInteger(data.summary.materialLineCount, language)} 筆包材明細`} />
                <SummaryMetric label="規格份數" value={formatInteger(data.summary.totalCount, language)} hint={data.subject?.unitShippingLabel || "依後端單位"} />
                <SummaryMetric label="包裝重量" value={formatNumber(data.summary.totalWeight, language)} hint={data.subject?.unitWarehouseLabel || "依規格單位"} />
              </div>
            </section>

            <section className="rounded-lg border border-border bg-white p-4 shadow-card">
              <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
                <div>
                  <h2 className="text-lg font-semibold text-textPrimary">包裝階層與規格</h2>
                  <p className="mt-1 text-sm text-textSecondary">依 `product_bom_spec.level` 呈現箱規、組規與其他階層；WIP 情境保留來源產品脈絡。</p>
                </div>
                <StatusBadge tone={data.packagingSpecs.length ? "success" : "warning"}>{data.packagingSpecs.length ? "已載入" : "無資料"}</StatusBadge>
              </div>
              <PackagingSpecTable
                rows={data.packagingSpecs}
                language={language}
                selectedId={manualSelectedSpecId || selectedSpecId}
                onSelect={setManualSelectedSpecId}
              />
            </section>

            <section className="rounded-lg border border-border bg-white p-4 shadow-card">
              <div className="mb-4 flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h2 className="text-lg font-semibold text-textPrimary">包材 BOM 明細</h2>
                  <p className="mt-1 text-sm text-textSecondary">
                    {activeSpec ? `${activeSpec.packagingLevelLabel} · ${activeSpec.packagingBomNo || "未提供 BOM No"} · ${activeSpec.packagingBomName || "未提供名稱"}` : "尚未選取包裝規格"}
                  </p>
                </div>
                <StatusBadge tone={activeSpec?.tone ?? "neutral"}>{activeSpec ? `${activeSpec.lineCount} 筆` : "待選取"}</StatusBadge>
              </div>
              <PackagingLineTable rows={activeSpec?.lines ?? []} language={language} />
            </section>

            <section className="rounded-lg border border-border bg-white p-4 shadow-card">
              <div className="mb-3 flex items-center gap-2">
                <PackageCheck className="h-4 w-4 text-primary" aria-hidden="true" />
                <h2 className="text-lg font-semibold text-textPrimary">關聯模組導覽</h2>
              </div>
              <DomainNavigation itemNo={data.subject?.itemNo || query.itemNo} />
            </section>
          </div>

          <SourceWarningPanel data={data} />
        </section>

        {data.warnings.length ? (
          <p className="flex items-start gap-2 rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm leading-6 text-warning">
            <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
            包裝規格存在需確認資料來源；請優先比對右側來源與警示，再回到 BOM 或 Product / WIP 360 追查。
          </p>
        ) : null}
      </div>
    </AppLayout>
  );
}
