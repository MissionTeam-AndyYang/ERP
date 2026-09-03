"use client";

import { AlertTriangle, FlaskConical, GitBranch, Loader2, Network, Route, Search } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { DataSourceStatusBadge } from "@/components/common/data-source-status-badge";
import { DataSourceToggle, type DataSourceMode } from "@/components/common/data-source-toggle";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { SupportEmptyState } from "@/components/common/support-empty-state";
import { StatusBadge } from "@/components/ui/status-badge";
import { useRecipeFormulaDashboard } from "@/hooks/use-recipe-formula-dashboard";
import { useLanguage } from "@/i18n/language-provider";
import { AppLayout } from "@/layouts/app-layout";
import { getRecipeFormulaComposition, type RecipeFormulaDashboardQuery } from "@/services/recipe-api";
import type { RecipeFormulaDetail, RecipeFormulaListItem } from "@/types/recipe";

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

function recipeMatchesSearch(item: RecipeFormulaListItem, search: string) {
  if (!search) {
    return true;
  }
  return [
    item.recipeNo,
    item.recipeName,
    item.productNo,
    item.productName,
    item.currentVersion,
    item.statusLabel,
    item.owner,
    item.sourceLabel
  ].some((value) => String(value).toLocaleLowerCase().includes(search));
}

function RecipeSelector({
  recipes,
  selectedId,
  searchQuery,
  language,
  onSelect
}: {
  recipes: RecipeFormulaListItem[];
  selectedId?: string;
  searchQuery: string;
  language: string;
  onSelect: (recipe: RecipeFormulaListItem) => void;
}) {
  const rows = useMemo(() => recipes.filter((item) => recipeMatchesSearch(item, searchQuery)), [recipes, searchQuery]);

  if (!rows.length) {
    return <SupportEmptyState title="沒有符合條件的 Recipe" description="請調整關鍵字，或確認後端是否提供 Recipe / Formula 資料。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[940px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">Recipe / 產品</th>
              <th className="px-4 py-3">目前版本</th>
              <th className="px-4 py-3 text-right">輸入項</th>
              <th className="px-4 py-3 text-right">警示</th>
              <th className="px-4 py-3">來源</th>
              <th className="px-4 py-3">狀態</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {rows.map((item) => {
              const isSelected = item.id === selectedId;
              return (
                <tr
                  className={`cursor-pointer transition ${isSelected ? "bg-info/10" : "hover:bg-slate-50"}`}
                  key={item.id}
                  onClick={() => onSelect(item)}
                >
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{item.recipeNo || "未提供 Recipe no"}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.recipeName || "未命名 Recipe"}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {item.productNo || "未提供產品"} · {item.productName || "未命名產品"}
                    </p>
                  </td>
                  <td className="px-4 py-3 font-semibold text-textPrimary">V{formatInteger(item.currentVersion, language)}</td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatInteger(item.inputCount, language)}</td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatInteger(item.warningCount, language)}</td>
                  <td className="px-4 py-3 text-textPrimary">
                    <p>{item.owner}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.sourceLabel}</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={item.tone}>{item.statusLabel}</StatusBadge>
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

function FormulaCompositionTable({ detail, language }: { detail?: RecipeFormulaDetail; language: string }) {
  if (!detail?.inputs.length) {
    return <SupportEmptyState title="沒有 Formula 輸入" description="此 Recipe 版本尚未回傳輸入項目。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="border-b border-border px-4 py-3">
        <p className="text-sm font-semibold text-textPrimary">Formula 組成</p>
        <p className="mt-1 text-xs text-textSecondary">輸入項重量、比例與個別損耗為 Recipe Version 的定義值，不由生產實績覆寫。</p>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-[980px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">項次 / 階段</th>
              <th className="px-4 py-3">投入品項</th>
              <th className="px-4 py-3 text-right">數量</th>
              <th className="px-4 py-3 text-right">重量</th>
              <th className="px-4 py-3 text-right">重量比例</th>
              <th className="px-4 py-3 text-right">個別損耗</th>
              <th className="px-4 py-3">來源</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {detail.inputs.map((input) => (
              <tr key={`${input.lineNo}-${input.itemNo}`}>
                <td className="px-4 py-3">
                  <p className="font-medium text-textPrimary">{input.lineNo || "未提供"}</p>
                  <p className="mt-1 text-xs text-textSecondary">{input.processStageLabel}</p>
                </td>
                <td className="px-4 py-3">
                  <p className="font-semibold text-textPrimary">{input.itemNo || "未提供料號"}</p>
                  <p className="mt-1 text-xs text-textSecondary">
                    {input.itemName || "未命名投入"} · {input.itemCategoryLabel}
                  </p>
                </td>
                <td className="px-4 py-3 text-right text-textPrimary">{formatNumber(input.quantity, language)}</td>
                <td className="px-4 py-3 text-right text-textPrimary">
                  {formatNumber(input.weight, language)} {input.unit}
                </td>
                <td className="px-4 py-3 text-right text-textPrimary">{formatNumber(input.weightRatio, language)}%</td>
                <td className="px-4 py-3 text-right text-textPrimary">{formatNumber(input.inputLossRate, language)}%</td>
                <td className="px-4 py-3 text-textSecondary">{input.sourceRef || "未提供"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function OutputPanel({ detail, language }: { detail?: RecipeFormulaDetail; language: string }) {
  const output = detail?.output;

  if (!output) {
    return <SupportEmptyState title="沒有定義產出" description="Recipe Version 必須有且僅有一個定義產出；目前後端未提供。" />;
  }

  return (
    <section className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium text-textSecondary">Defined Output</p>
          <h3 className="mt-1 text-lg font-semibold text-textPrimary">{output.itemNo || "未提供產出品項"}</h3>
          <p className="mt-1 text-sm text-textSecondary">{output.itemName || "未命名產出"} · {output.outputTypeLabel}</p>
        </div>
        <StatusBadge tone="success">唯一產出</StatusBadge>
      </div>
      <div className="mt-4 grid grid-cols-3 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">產出數量</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatNumber(output.quantity, language)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">產出重量</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(output.weight, language)} {output.unit}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">標準良率</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatNumber(output.yieldRate, language)}%</p>
        </div>
      </div>
    </section>
  );
}

function ReferencePanel({ detail }: { detail?: RecipeFormulaDetail }) {
  const references = [
    ...(detail?.productStructureReferences ?? []).map((item) => ({ ...item, icon: GitBranch })),
    ...(detail?.routingReferences ?? []).map((item) => ({ ...item, icon: Route }))
  ];

  if (!references.length) {
    return <SupportEmptyState title="沒有參照資料" description="目前沒有 Product Structure 或 Routing 參照。" />;
  }

  return (
    <div className="grid gap-3 md:grid-cols-2">
      {references.map((reference) => {
        const Icon = reference.icon;
        return (
          <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={`${reference.typeLabel}-${reference.refNo}`}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-xs font-medium text-textSecondary">{reference.typeLabel}</p>
                <p className="mt-1 font-semibold text-textPrimary">{reference.refNo || "未提供參照 no"}</p>
                <p className="mt-1 text-sm text-textSecondary">{reference.refName || "未命名參照"}</p>
              </div>
              <Icon className="h-5 w-5 text-textSecondary" aria-hidden="true" />
            </div>
            <StatusBadge tone="neutral">{reference.statusLabel}</StatusBadge>
          </div>
        );
      })}
    </div>
  );
}

function LineageWarningPanel({ detail }: { detail?: RecipeFormulaDetail }) {
  return (
    <div className="grid gap-3 lg:grid-cols-2">
      <section className="rounded-lg border border-border bg-white p-4 shadow-card">
        <div className="flex items-center gap-2">
          <Network className="h-4 w-4 text-primary" aria-hidden="true" />
          <p className="text-sm font-semibold text-textPrimary">來源 lineage</p>
        </div>
        <div className="mt-3 space-y-2">
          {detail?.lineage.length ? (
            detail.lineage.map((lineage) => (
              <div className="rounded-md bg-slate-50 p-3 text-sm" key={`${lineage.sourceTypeLabel}-${lineage.sourceRef}`}>
                <p className="font-medium text-textPrimary">{lineage.sourceTypeLabel} · {lineage.sourceRef || "未提供來源"}</p>
                <p className="mt-1 text-xs text-textSecondary">
                  {lineage.evidenceLabel} · {lineage.statusLabel}
                </p>
              </div>
            ))
          ) : (
            <SupportEmptyState title="沒有來源 lineage" description="後端尚未回傳 Recipe / Formula 來源依據。" />
          )}
        </div>
      </section>

      <section className="rounded-lg border border-border bg-white p-4 shadow-card">
        <div className="flex items-center gap-2">
          <AlertTriangle className="h-4 w-4 text-warning" aria-hidden="true" />
          <p className="text-sm font-semibold text-textPrimary">警示</p>
        </div>
        <div className="mt-3 space-y-2">
          {detail?.warnings.length ? (
            detail.warnings.map((warning) => (
              <p className="rounded-md border border-warning/20 bg-warning/10 px-3 py-2 text-sm leading-6 text-warning" key={`${warning.code}-${warning.refNo}`}>
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
  selectedRecipe,
  detail,
  isLoading,
  error,
  language,
  onVersionSelect
}: {
  selectedRecipe?: RecipeFormulaListItem;
  detail?: RecipeFormulaDetail;
  isLoading: boolean;
  error?: string;
  language: string;
  onVersionSelect: (version: number) => void;
}) {
  if (!selectedRecipe) {
    return (
      <aside className="rounded-lg border border-border bg-white p-4 shadow-card">
        <SupportEmptyState title="尚未選取 Recipe" description="請從左側清單選擇一筆 Recipe / Formula。" />
      </aside>
    );
  }

  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium text-textSecondary">Recipe Version</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{selectedRecipe.recipeNo}</h2>
          <p className="mt-1 text-sm text-textSecondary">
            {selectedRecipe.recipeName || "未命名 Recipe"} · V{formatInteger(selectedRecipe.currentVersion, language)}
          </p>
        </div>
        <StatusBadge tone={selectedRecipe.tone}>{selectedRecipe.statusLabel}</StatusBadge>
      </div>

      {isLoading ? (
        <p className="flex items-center gap-2 rounded-md bg-info/10 px-3 py-2 text-sm text-info">
          <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
          載入 Recipe / Formula 明細中...
        </p>
      ) : null}
      {error ? (
        <p className="rounded-md border border-danger/20 bg-danger/10 px-3 py-2 text-sm leading-6 text-danger">
          Recipe / Formula 明細取得失敗，畫面未改用示範資料。{error}
        </p>
      ) : null}

      {detail?.versions.length ? (
        <div className="space-y-2">
          <p className="text-sm font-semibold text-textPrimary">版本</p>
          <div className="flex flex-wrap gap-2">
            {detail.versions.map((version) => (
              <button
                className={`inline-flex h-9 items-center rounded-button px-3 text-sm font-medium transition ${
                  version.version === selectedRecipe.currentVersion ? "bg-primary text-white" : "bg-slate-100 text-textSecondary hover:bg-slate-200"
                }`}
                key={`${selectedRecipe.recipeNo}-${version.version}`}
                onClick={() => onVersionSelect(version.version)}
                type="button"
              >
                V{formatInteger(version.version, language)} · {version.statusLabel}
              </button>
            ))}
          </div>
        </div>
      ) : null}

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">產品</p>
          <p className="mt-1 font-semibold text-textPrimary">{selectedRecipe.productNo || "未提供"}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">輸入項</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatInteger(detail?.inputs.length ?? selectedRecipe.inputCount, language)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">警示</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatInteger(detail?.warnings.length ?? selectedRecipe.warningCount, language)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">定義產出</p>
          <p className="mt-1 font-semibold text-textPrimary">{detail?.output?.itemNo || "待載入"}</p>
        </div>
      </div>
    </aside>
  );
}

export default function RecipeFormulaPage() {
  const { language } = useLanguage();
  const [dataSourceMode, setDataSourceMode] = useState<DataSourceMode>("api");
  const [searchValue, setSearchValue] = useState("");
  const [selectedRecipeNo, setSelectedRecipeNo] = useState<string>();
  const [selectedVersion, setSelectedVersion] = useState<number>();
  const [detailState, setDetailState] = useState<{
    recipeNo?: string;
    version?: number;
    detail?: RecipeFormulaDetail;
    error?: string;
  }>({});
  const query = useMemo<RecipeFormulaDashboardQuery>(
    () => ({
      keyword: searchValue.trim() || undefined,
      count: 50
    }),
    [searchValue]
  );
  const { data, error, isLoading, source } = useRecipeFormulaDashboard(dataSourceMode, query);
  const searchQuery = normalizeSearch(searchValue);
  const selectedRecipe =
    data.recipes.find((item) => item.recipeNo === selectedRecipeNo && item.currentVersion === selectedVersion) ??
    data.recipes.find((item) => item.recipeNo === selectedRecipeNo) ??
    data.recipes[0];
  const selectedDetailVersion = selectedVersion ?? selectedRecipe?.currentVersion;

  useEffect(() => {
    if (!selectedRecipe?.recipeNo || selectedDetailVersion === undefined) {
      return;
    }

    let isMounted = true;
    getRecipeFormulaComposition(selectedRecipe.recipeNo, selectedDetailVersion, selectedRecipe, dataSourceMode).then((result) => {
      if (!isMounted) {
        return;
      }
      setDetailState({
        recipeNo: selectedRecipe.recipeNo,
        version: selectedDetailVersion,
        detail: result.detail,
        error: result.error
      });
    });

    return () => {
      isMounted = false;
    };
  }, [selectedRecipe, selectedDetailVersion, dataSourceMode]);

  const activeDetail =
    detailState.recipeNo === selectedRecipe?.recipeNo && detailState.version === selectedDetailVersion ? detailState.detail : undefined;
  const activeDetailError =
    detailState.recipeNo === selectedRecipe?.recipeNo && detailState.version === selectedDetailVersion ? detailState.error : undefined;
  const isDetailLoading = Boolean(
    selectedRecipe?.recipeNo && (detailState.recipeNo !== selectedRecipe.recipeNo || detailState.version !== selectedDetailVersion)
  );

  return (
    <AppLayout activePath="/recipe" title="Recipe / Formula">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">Read-only</StatusBadge>
                <DataSourceStatusBadge source={source} isLoading={isLoading} hasError={Boolean(error)} />
                <StatusBadge tone="neutral">Recipe Version / Formula 組成</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">Recipe / Formula</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                檢視受治理 Recipe 版本的投入、重量比例、個別損耗與唯一定義產出，並保留 Product Structure 與 Routing 的參照邊界。
              </p>
            </div>
            <div className="grid gap-2 md:grid-cols-[minmax(220px,1fr)_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  aria-label="搜尋 Recipe、產品或來源"
                  value={searchValue}
                  onChange={(event) => setSearchValue(event.target.value)}
                  placeholder="Recipe / 產品 / 來源"
                />
              </label>
              <DataSourceToggle value={dataSourceMode} onChange={setDataSourceMode} />
            </div>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-danger/20 bg-danger/10 px-4 py-3 text-sm text-danger">
            Recipe / Formula 資料取得失敗，畫面未改用示範資料。{error}
          </p>
        ) : null}

        <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {data.kpis.map((item) => (
            <ModuleKpiCard {...item} key={item.label} />
          ))}
        </section>

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="min-w-0 space-y-4">
            <RecipeSelector
              recipes={data.recipes}
              selectedId={selectedRecipe?.id}
              searchQuery={searchQuery}
              language={language}
              onSelect={(recipe) => {
                setSelectedRecipeNo(recipe.recipeNo);
                setSelectedVersion(recipe.currentVersion);
              }}
            />
            <FormulaCompositionTable detail={activeDetail} language={language} />
            <OutputPanel detail={activeDetail} language={language} />
            <LineageWarningPanel detail={activeDetail} />
            <ReferencePanel detail={activeDetail} />
          </div>

          <DetailPanel
            selectedRecipe={selectedRecipe}
            detail={activeDetail}
            isLoading={isDetailLoading}
            error={activeDetailError}
            language={language}
            onVersionSelect={(version) => {
              setSelectedRecipeNo(selectedRecipe?.recipeNo);
              setSelectedVersion(version);
            }}
          />
        </section>
      </div>
    </AppLayout>
  );
}
