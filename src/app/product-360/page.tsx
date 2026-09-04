"use client";

import Link from "next/link";
import {
  AlertTriangle,
  Boxes,
  ClipboardList,
  Factory,
  GitBranch,
  Loader2,
  Network,
  PackageSearch,
  Route,
  Search,
  ShieldCheck,
  Tags
} from "lucide-react";
import { useMemo, useState } from "react";
import { DataSourceStatusBadge } from "@/components/common/data-source-status-badge";
import { DataSourceToggle, type DataSourceMode } from "@/components/common/data-source-toggle";
import { SupportEmptyState } from "@/components/common/support-empty-state";
import { StatusBadge } from "@/components/ui/status-badge";
import { useLanguage } from "@/i18n/language-provider";
import { AppLayout } from "@/layouts/app-layout";
import { useProductWip360Overview } from "@/hooks/use-product-wip-360";
import type {
  ProductWip360BatchHighlight,
  ProductWip360ModuleReadiness,
  ProductWip360OverviewData,
  ProductWip360Query,
  ProductWip360RoutingStep,
  ProductWip360StructureNode
} from "@/types/product-wip-360";

type Scenario = "product" | "wip";

const scenarioDefaults: Record<Scenario, ProductWip360Query> = {
  product: { itemNo: "PRD-SD-001", itemCategory: 5 },
  wip: { itemNo: "WIP-SD-BASE-001", itemCategory: 4 }
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

function formatMoney(value: number | undefined, language: string) {
  return new Intl.NumberFormat(language, {
    maximumFractionDigits: 0,
    style: "currency",
    currency: "TWD"
  }).format(value ?? 0);
}

function identityCategory(scenario: Scenario) {
  return scenario === "wip" ? 4 : 5;
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

function ModuleReadinessGrid({ modules }: { modules: ProductWip360ModuleReadiness[] }) {
  if (!modules.length) {
    return <SupportEmptyState title="沒有模組可用性資料" description="後端 API 回傳空陣列，畫面如實呈現空狀態。" />;
  }

  return (
    <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
      {modules.map((item) => (
        <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.moduleCode || item.moduleLabel}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-sm font-semibold text-textPrimary">{item.moduleLabel}</p>
              <p className="mt-1 text-xs text-textSecondary">{item.sourceLabel || "未提供來源"}</p>
            </div>
            <StatusBadge tone={item.tone}>{item.statusLabel}</StatusBadge>
          </div>
          <p className="mt-3 text-xs text-textSecondary">
            {item.warningCodes.length ? item.warningCodes.join(" / ") : "沒有警示"}
          </p>
        </div>
      ))}
    </div>
  );
}

function BatchTable({ rows, language }: { rows: ProductWip360BatchHighlight[]; language: string }) {
  if (!rows.length) {
    return <SupportEmptyState title="沒有批號重點資料" description="API 回傳批號清單為空；畫面未補入示範批號。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border">
      <div className="overflow-x-auto">
        <table className="min-w-[760px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold text-textSecondary">
            <tr>
              <th className="px-4 py-3">批號</th>
              <th className="px-4 py-3">倉庫</th>
              <th className="px-4 py-3 text-right">目前 / 可用</th>
              <th className="px-4 py-3">期限</th>
              <th className="px-4 py-3">來源</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {rows.map((item) => (
              <tr key={`${item.batchNo}-${item.warehouseNo}`}>
                <td className="px-4 py-3">
                  <p className="font-semibold text-textPrimary">{item.batchNo || "未提供批號"}</p>
                  <StatusBadge tone={item.tone}>{item.riskLevelLabel}</StatusBadge>
                </td>
                <td className="px-4 py-3">
                  <p className="font-medium text-textPrimary">{item.warehouseNo || "未提供倉庫"}</p>
                  <p className="mt-1 text-xs text-textSecondary">{item.warehouseName || "未提供名稱"}</p>
                </td>
                <td className="px-4 py-3 text-right text-textPrimary">
                  {formatNumber(item.currentQuantity, language)} / {formatNumber(item.availableQuantity, language)} {item.unitLabel}
                </td>
                <td className="px-4 py-3 text-textSecondary">{item.validDateLabel || "未提供"}</td>
                <td className="px-4 py-3 text-textSecondary">{item.sourceRefLabel || "未提供來源單據"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function StructureTree({ nodes, language }: { nodes: ProductWip360StructureNode[]; language: string }) {
  if (!nodes.length) {
    return <SupportEmptyState title="沒有產品結構節點" description="Product Structure / BOM 區塊目前無資料；不由前端推測補齊。" />;
  }

  return (
    <div className="space-y-2">
      {nodes.map((node) => (
        <div
          className="rounded-lg border border-border bg-slate-50 p-3"
          key={node.id}
          style={{ marginLeft: `${Math.min(node.level, 3) * 18}px` }}
        >
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div>
              <p className="font-semibold text-textPrimary">{node.itemNo || "未提供料號"}</p>
              <p className="mt-1 text-sm text-textSecondary">{node.itemName || "未命名節點"}</p>
            </div>
            <StatusBadge tone={node.tone}>{node.nodeTypeLabel}</StatusBadge>
          </div>
          <p className="mt-2 text-xs text-textSecondary">
            關係數量 {formatNumber(node.quantity, language)} {node.unitLabel || "未提供單位"}
          </p>
        </div>
      ))}
    </div>
  );
}

function RoutingSteps({ steps }: { steps: ProductWip360RoutingStep[] }) {
  if (!steps.length) {
    return <SupportEmptyState title="沒有 Routing 流程步驟" description="若此為 standalone WIP，目前後端可能尚未提供獨立 WIP Routing Version evidence；畫面不推測補齊。" />;
  }

  return (
    <div className="space-y-3">
      {steps.map((step) => (
        <div className="grid gap-3 rounded-lg border border-border bg-slate-50 p-4 md:grid-cols-[64px_minmax(0,1fr)_220px]" key={`${step.stepNo}-${step.processLabel}`}>
          <div>
            <p className="text-xs text-textSecondary">Step</p>
            <p className="mt-1 text-xl font-semibold text-textPrimary">{step.stepNo}</p>
          </div>
          <div className="min-w-0">
            <div className="flex flex-wrap gap-2">
              <StatusBadge tone="info">{step.stageLabel}</StatusBadge>
              <StatusBadge tone="neutral">{step.groupLabel}</StatusBadge>
            </div>
            <p className="mt-2 font-semibold text-textPrimary">{step.processLabel}</p>
            <p className="mt-1 text-sm text-textSecondary">Recipe: {step.recipeRefLabel}</p>
          </div>
          <div className="text-sm text-textSecondary">
            <p>資源：{step.resourceLabel}</p>
            <p className="mt-1">標準：{step.standardRateLabel}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

function DomainNavigation({ itemNo }: { itemNo: string }) {
  const encodedItemNo = encodeURIComponent(itemNo);
  const links = [
    { label: "品項主資料", href: `/items?itemNo=${encodedItemNo}`, icon: PackageSearch },
    { label: "庫存批號", href: `/warehouse/inventory/lots?itemNo=${encodedItemNo}`, icon: Boxes },
    { label: "批號中心", href: `/batches?keyword=${encodedItemNo}`, icon: Tags },
    { label: "BOM 中心", href: `/bom?productNo=${encodedItemNo}`, icon: GitBranch },
    { label: "Recipe / Formula", href: `/recipe?productNo=${encodedItemNo}`, icon: ClipboardList },
    { label: "Routing", href: `/routing?itemNo=${encodedItemNo}`, icon: Route },
    { label: "溯源中心", href: `/traceability?keyword=${encodedItemNo}`, icon: Network }
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

function SourceWarningPanel({ data }: { data: ProductWip360OverviewData }) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div>
        <div className="flex items-center justify-between gap-3">
          <h2 className="text-lg font-semibold text-textPrimary">來源與警示</h2>
          <StatusBadge tone={data.warnings.length ? "warning" : "success"}>
            {data.warnings.length ? `${data.warnings.length} 項` : "無警示"}
          </StatusBadge>
        </div>
        <p className="mt-2 text-sm leading-6 text-textSecondary">保留各模組來源，不把 overview 當作新的權威資料來源。</p>
      </div>

      <div className="space-y-2">
        {data.sourceLineage.length ? (
          data.sourceLineage.map((item) => (
            <div className="rounded-md bg-slate-50 p-3 text-sm" key={`${item.moduleLabel}-${item.sourceLabel}`}>
              <div className="flex items-start justify-between gap-2">
                <div>
                  <p className="font-medium text-textPrimary">{item.moduleLabel}</p>
                  <p className="mt-1 text-xs text-textSecondary">{item.sourceLabel || "未提供來源"}</p>
                </div>
                <StatusBadge tone={item.tone}>{item.statusLabel}</StatusBadge>
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
            <p className={`rounded-md border px-3 py-2 text-sm leading-6 ${warning.tone === "info" ? "border-info/20 bg-info/10 text-info" : "border-warning/20 bg-warning/10 text-warning"}`} key={`${warning.code}-${warning.refNo}-${index}`}>
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
          <p className="text-sm font-semibold">No-write controls</p>
        </div>
        <ul className="mt-3 space-y-2 text-sm leading-6 text-textSecondary">
          <li>不新增、修改或停用 Product / WIP / Item。</li>
          <li>不核准或發布 BOM、Recipe、Routing。</li>
          <li>不執行入出庫、排程、MES、派工或生產動作。</li>
          <li>不代表 Source-of-Truth transition、Cutover 或 Go-Live。</li>
        </ul>
      </div>
    </aside>
  );
}

export default function ProductWip360Page() {
  const { language } = useLanguage();
  const [dataSourceMode, setDataSourceMode] = useState<DataSourceMode>("api");
  const [scenario, setScenario] = useState<Scenario>("product");
  const [itemNoInput, setItemNoInput] = useState(scenarioDefaults.product.itemNo);
  const query = useMemo<ProductWip360Query>(
    () => ({
      itemNo: itemNoInput.trim() || scenarioDefaults[scenario].itemNo,
      itemCategory: identityCategory(scenario)
    }),
    [itemNoInput, scenario]
  );
  const { data, error, isLoading, source } = useProductWip360Overview(query, dataSourceMode);
  const subject = data.subject;

  function selectScenario(nextScenario: Scenario) {
    setScenario(nextScenario);
    setItemNoInput(scenarioDefaults[nextScenario].itemNo);
  }

  return (
    <AppLayout activePath="/product-360" title="Product / WIP 360 唯讀總覽">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">Read-only</StatusBadge>
                <DataSourceStatusBadge source={source} isLoading={isLoading} hasError={Boolean(error)} />
                <StatusBadge tone="neutral">Overview navigation only</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">Product / WIP 360</h2>
              <p className="mt-2 max-w-4xl text-sm leading-6 text-textSecondary">
                以單一 Product 或 standalone WIP identity 彙整主資料、庫存數量狀態、BOM、Recipe / Formula、Routing / Process Flow 與來源警示。此頁只提供唯讀總覽與 domain drill-down。
              </p>
            </div>
            <div className="grid gap-2 md:grid-cols-[auto_minmax(220px,1fr)_auto]">
              <div className="inline-flex h-10 rounded-button border border-border bg-white p-1">
                {(["product", "wip"] as const).map((item) => (
                  <button
                    className={`rounded-button px-3 text-sm font-medium transition ${scenario === item ? "bg-primary text-white" : "text-textSecondary hover:bg-slate-100"}`}
                    key={item}
                    onClick={() => selectScenario(item)}
                    type="button"
                  >
                    {item === "product" ? "Product" : "Standalone WIP"}
                  </button>
                ))}
              </div>
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  aria-label="查詢 Product 或 WIP"
                  value={itemNoInput}
                  onChange={(event) => setItemNoInput(event.target.value)}
                  placeholder="Product / WIP itemNo"
                />
              </label>
              <DataSourceToggle value={dataSourceMode} onChange={setDataSourceMode} />
            </div>
          </div>
        </section>

        {isLoading ? (
          <p className="flex items-center gap-2 rounded-lg border border-info/20 bg-info/10 px-4 py-3 text-sm text-info">
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
            Product / WIP 360 資料載入中...
          </p>
        ) : null}

        {error ? (
          <p className="rounded-lg border border-danger/20 bg-danger/10 px-4 py-3 text-sm leading-6 text-danger">
            Product / WIP 360 API 資料取得失敗，畫面未改用示範資料。{error}
          </p>
        ) : null}

        {!isLoading && !error && !subject ? (
          <SupportEmptyState title="沒有 Product / WIP 總覽資料" description="後端 API 回傳空資料；畫面如實呈現 true empty state，未使用 mock 補資料。" />
        ) : null}

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="min-w-0 space-y-5">
            <section className="rounded-lg border border-border bg-white p-4 shadow-card">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p className="text-xs font-medium text-textSecondary">Product / WIP Summary</p>
                  <h2 className="mt-1 text-xl font-semibold text-textPrimary">
                    {subject?.itemNo || query.itemNo || "未選取"} · {subject?.itemName || "尚未取得主體資料"}
                  </h2>
                  <p className="mt-2 text-sm text-textSecondary">
                    {subject?.identityTypeLabel || (scenario === "product" ? "Product" : "Standalone WIP")} · {subject?.itemCategoryLabel || "待確認"} · {subject?.sourceLabel || "未提供來源"}
                  </p>
                </div>
                <StatusBadge tone={subject?.tone ?? (error ? "danger" : "neutral")}>{subject?.masterStatusLabel || "待載入"}</StatusBadge>
              </div>
              <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
                <SummaryMetric label="版本" value={subject?.versionLabel || "未提供"} hint={`查詢類別 ${query.itemCategory}`} />
                <SummaryMetric label="庫存單位" value={subject?.unitWarehouseLabel || "未提供"} hint="前端 enum 轉換" />
                <SummaryMetric label="生產單位" value={subject?.unitProductLabel || "未提供"} hint="前端 enum 轉換" />
                <SummaryMetric label="交易品項" value={`${formatInteger(data.transactionItems.length, language)} 筆`} hint={scenario === "wip" && !data.transactionItems.length ? "Standalone WIP 可不適用" : "客戶／廠商參照"} />
              </div>
            </section>

            <ModuleReadinessGrid modules={data.moduleReadiness} />

            <section className="rounded-lg border border-border bg-white p-4 shadow-card">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <h2 className="text-lg font-semibold text-textPrimary">Inventory / Quantity-State</h2>
                  <p className="mt-1 text-sm text-textSecondary">庫存摘要只做查閱；完整庫存作業仍回到倉庫與批號頁面。</p>
                </div>
                <StatusBadge tone={data.inventoryOverview.hasStock ? "success" : "neutral"}>
                  {data.inventoryOverview.hasStock ? "有庫存" : "無庫存"}
                </StatusBadge>
              </div>
              <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
                <SummaryMetric label="目前庫存" value={`${formatNumber(data.inventoryOverview.currentQuantity, language)} ${subject?.unitWarehouseLabel || ""}`} />
                <SummaryMetric label="可用數量" value={`${formatNumber(data.inventoryOverview.availableQuantity, language)} ${subject?.unitWarehouseLabel || ""}`} />
                <SummaryMetric label="預留 / 品檢保留" value={`${formatNumber(data.inventoryOverview.reservedQuantity, language)} / ${formatNumber(data.inventoryOverview.qualityHoldQuantity, language)}`} />
                <SummaryMetric label="庫存價值" value={formatMoney(data.inventoryOverview.inventoryValue, language)} hint={`倉庫 ${formatInteger(data.inventoryOverview.warehouseCount, language)} / 批號 ${formatInteger(data.inventoryOverview.batchCount, language)}`} />
              </div>
              <div className="mt-4">
                <BatchTable rows={data.batchHighlights} language={language} />
              </div>
            </section>

            <section className="grid gap-4 xl:grid-cols-2">
              <div className="rounded-lg border border-border bg-white p-4 shadow-card">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h2 className="text-lg font-semibold text-textPrimary">Product Structure / BOM</h2>
                    <p className="mt-1 text-sm text-textSecondary">
                      {data.productStructure.bomNo || "未提供 BOM"} · {data.productStructure.bomVersionLabel || "版本待確認"}
                    </p>
                  </div>
                  <StatusBadge tone={data.productStructure.tone}>{data.productStructure.statusLabel}</StatusBadge>
                </div>
                <div className="mt-4">
                  <StructureTree nodes={data.productStructure.children} language={language} />
                </div>
              </div>

              <div className="rounded-lg border border-border bg-white p-4 shadow-card">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h2 className="text-lg font-semibold text-textPrimary">Recipe / Formula</h2>
                    <p className="mt-1 text-sm text-textSecondary">
                      {data.recipeFormula.recipeNo || "未提供 Recipe"} · {data.recipeFormula.recipeVersionLabel || "版本待確認"}
                    </p>
                  </div>
                  <StatusBadge tone={data.recipeFormula.tone}>{data.recipeFormula.statusLabel}</StatusBadge>
                </div>
                <div className="mt-4 grid grid-cols-2 gap-3">
                  <SummaryMetric label="定義產出" value={data.recipeFormula.outputItemNo || "未提供"} hint={`${formatNumber(data.recipeFormula.outputQuantity, language)} ${data.recipeFormula.outputUnitLabel}`} />
                  <SummaryMetric label="Formula 輸入" value={`${formatInteger(data.recipeFormula.inputs.length, language)} 項`} />
                </div>
                <div className="mt-4 space-y-2">
                  {data.recipeFormula.inputs.length ? (
                    data.recipeFormula.inputs.map((input) => (
                      <div className="rounded-md bg-slate-50 p-3 text-sm" key={input.itemNo}>
                        <p className="font-semibold text-textPrimary">{input.itemNo} · {input.itemName || "未命名投入"}</p>
                        <p className="mt-1 text-textSecondary">
                          {formatNumber(input.quantity, language)} {input.unitLabel} · {formatNumber(input.weightRatio, language)}% · loss {formatNumber(input.lossRate, language)}%
                        </p>
                      </div>
                    ))
                  ) : (
                    <SupportEmptyState title="沒有 Formula 輸入" description="API 回傳空陣列；畫面未以 BOM 或 mock 推測補齊。" />
                  )}
                </div>
              </div>
            </section>

            <section className="rounded-lg border border-border bg-white p-4 shadow-card">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h2 className="text-lg font-semibold text-textPrimary">Routing / Process Flow</h2>
                  <p className="mt-1 text-sm text-textSecondary">
                    {data.routingProcess.routingVersionId || "未提供 Routing Version"} · {data.routingProcess.sourceLabel || "未提供來源"}
                  </p>
                </div>
                <StatusBadge tone={data.routingProcess.tone}>{data.routingProcess.statusLabel}</StatusBadge>
              </div>
              {data.routingProcess.sourceLabel === "test_support" || data.routingProcess.warnings.includes("test_support_only") ? (
                <p className="mt-3 rounded-md border border-warning/20 bg-warning/10 px-3 py-2 text-sm leading-6 text-warning">
                  Routing 目前資料來自非正式 Shared DEV test-support read-only surface，僅能作為非生產驗證 evidence。
                </p>
              ) : null}
              <div className="mt-4">
                <RoutingSteps steps={data.routingProcess.steps} />
              </div>
            </section>

            <section className="rounded-lg border border-border bg-white p-4 shadow-card">
              <div className="mb-3 flex items-center gap-2">
                <Factory className="h-4 w-4 text-primary" aria-hidden="true" />
                <h2 className="text-lg font-semibold text-textPrimary">Domain Detail Navigation</h2>
              </div>
              <DomainNavigation itemNo={subject?.itemNo || query.itemNo} />
            </section>
          </div>

          <SourceWarningPanel data={data} />
        </section>
      </div>
    </AppLayout>
  );
}
