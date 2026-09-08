"use client";

import Link from "next/link";
import {
  AlertTriangle,
  CalendarClock,
  CheckCircle2,
  FileCheck2,
  GitBranch,
  Loader2,
  Scale,
  Search,
  ShieldCheck,
  Weight
} from "lucide-react";
import { useMemo, useState } from "react";
import { DataSourceStatusBadge } from "@/components/common/data-source-status-badge";
import { DataSourceToggle, type DataSourceMode } from "@/components/common/data-source-toggle";
import { SupportEmptyState } from "@/components/common/support-empty-state";
import { StatusBadge } from "@/components/ui/status-badge";
import { useLanguage } from "@/i18n/language-provider";
import { AppLayout } from "@/layouts/app-layout";
import { useManufacturingDefinitionOverview } from "@/hooks/use-manufacturing-definition";
import type {
  ManufacturingAuthority,
  ManufacturingDefinitionData,
  ManufacturingDefinitionQuery,
  ManufacturingDomainReference,
  ManufacturingEffectivityRow,
  ManufacturingLineage,
  ManufacturingResolutionStatus,
  ManufacturingVersionReference,
  ManufacturingWarning
} from "@/types/manufacturing-definition";

type Scenario = "product" | "wip";

const scenarioDefaults: Record<Scenario, ManufacturingDefinitionQuery> = {
  product: { itemNo: "PRD-SD-001", itemCategory: 5 },
  wip: { itemNo: "INP-SD-001", itemCategory: 4 }
};

function formatNumber(value: number | undefined, language: string, digits = 2) {
  return new Intl.NumberFormat(language, {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits
  }).format(value ?? 0);
}

function toneForResolution(value: ManufacturingResolutionStatus) {
  if (value === "RESOLVED_SINGLE_CANDIDATE") return "success" as const;
  if (value === "CONFLICT") return "danger" as const;
  if (value === "UNAVAILABLE") return "danger" as const;
  if (value === "RESOLVED_WITH_WARNINGS" || value === "MULTIPLE_CANDIDATES" || value === "PARTIAL_CANDIDATE") return "warning" as const;
  return "neutral" as const;
}

function definitionStatusLabel(value: ManufacturingDefinitionData["definitionStatus"], language: string) {
  if (language === "en") return value === "candidate" ? "Candidate" : value === "partial" ? "Partial" : "Unavailable";
  if (language === "ja") return value === "candidate" ? "候補" : value === "partial" ? "一部候補" : "利用不可";
  if (language === "vi") return value === "candidate" ? "Ứng viên" : value === "partial" ? "Ứng viên một phần" : "Không khả dụng";
  return value === "candidate" ? "候選" : value === "partial" ? "部分候選" : "目前不可用";
}

function flagLabel(value: boolean | null, language: string) {
  if (value === null) return language === "zh-TW" ? "待確認" : language === "ja" ? "確認待ち" : language === "vi" ? "Chờ xác nhận" : "Review";
  if (language === "zh-TW") return value ? "是" : "否";
  if (language === "ja") return value ? "はい" : "いいえ";
  if (language === "vi") return value ? "Có" : "Không";
  return value ? "Yes" : "No";
}

function SummaryMetric({ label, value, hint }: { label: string; value: string; hint?: string }) {
  return (
    <div className="rounded-lg border border-border bg-slate-50 p-4">
      <p className="text-xs font-medium text-textSecondary">{label}</p>
      <p className="mt-2 text-xl font-semibold text-textPrimary">{value}</p>
      {hint ? <p className="mt-1 text-xs text-textSecondary">{hint}</p> : null}
    </div>
  );
}

function VersionTable({ rows }: { rows: ManufacturingVersionReference[] }) {
  if (!rows.length) {
    return <SupportEmptyState title="沒有版本候選" description="後端未回傳可供查閱的 BOM、Recipe、Routing 或 Packaging 候選。" />;
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-border">
      <table className="min-w-[760px] w-full border-collapse text-sm">
        <thead className="bg-slate-50 text-left text-xs font-semibold text-textSecondary">
          <tr>
            <th className="px-4 py-3">領域</th>
            <th className="px-4 py-3">參照</th>
            <th className="px-4 py-3">版本</th>
            <th className="px-4 py-3">狀態</th>
            <th className="px-4 py-3">適用日期</th>
            <th className="px-4 py-3">說明</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border">
          {rows.map((row, index) => (
            <tr key={`${row.domainCode}-${row.referenceNo}-${row.versionLabel}-${index}`}>
              <td className="px-4 py-3 font-medium text-textPrimary">{row.domainLabel}</td>
              <td className="px-4 py-3 text-textSecondary">{row.referenceNo || "未提供"}</td>
              <td className="px-4 py-3 text-textPrimary">{row.versionLabel}</td>
              <td className="px-4 py-3"><StatusBadge tone={row.tone}>{row.statusLabel}</StatusBadge></td>
              <td className="px-4 py-3 text-textSecondary">{row.dateLabel}</td>
              <td className="px-4 py-3 text-textSecondary">{row.detailLabel}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function DomainReferenceGrid({ rows }: { rows: ManufacturingDomainReference[] }) {
  if (!rows.length) {
    return <SupportEmptyState title="沒有跨模組參照" description="API 回傳 domainReferences 為空；畫面不自行推測模組狀態。" />;
  }

  return (
    <div className="grid gap-3 md:grid-cols-2">
      {rows.map((row) => (
        <div className="rounded-lg border border-border bg-white p-4" key={row.domainCode}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="font-semibold text-textPrimary">{row.domainLabel}</p>
              <p className="mt-1 text-xs text-textSecondary">{row.sourceLabel || "未提供來源"}</p>
            </div>
            <StatusBadge tone={row.tone}>{row.statusLabel}</StatusBadge>
          </div>
          <p className="mt-3 text-sm text-textSecondary">{row.detailLabel}</p>
          {row.warningCodes.length ? (
            <p className="mt-2 text-xs text-warning">{row.warningCodes.join(" / ")}</p>
          ) : (
            <p className="mt-2 text-xs text-success">沒有模組警示</p>
          )}
        </div>
      ))}
    </div>
  );
}

function AuthorityTable({ title, icon: Icon, rows, language }: { title: string; icon: typeof Scale; rows: ManufacturingAuthority[]; language: string }) {
  return (
    <section className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Icon className="h-5 w-5 text-primary" aria-hidden="true" />
          <h2 className="text-lg font-semibold text-textPrimary">{title}</h2>
        </div>
        <StatusBadge tone="info">{rows.length} 筆</StatusBadge>
      </div>
      {!rows.length ? (
        <SupportEmptyState title="沒有依據資料" description="後端回傳空陣列；畫面如實呈現，不以其他模組資料代填。" />
      ) : (
        <div className="overflow-x-auto rounded-lg border border-border">
          <table className="min-w-[760px] w-full border-collapse text-sm">
            <thead className="bg-slate-50 text-left text-xs font-semibold text-textSecondary">
              <tr>
                <th className="px-4 py-3">領域 / 數值類型</th>
                <th className="px-4 py-3 text-right">數值</th>
                <th className="px-4 py-3">來源</th>
                <th className="px-4 py-3">參照</th>
                <th className="px-4 py-3">適用說明</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {rows.map((row, index) => (
                <tr key={`${row.domainCode}-${row.valueTypeCode}-${row.sourceRef}-${index}`}>
                  <td className="px-4 py-3">
                    <p className="font-medium text-textPrimary">{row.domainLabel}</p>
                    <p className="mt-1 text-xs text-textSecondary">{row.valueTypeLabel}</p>
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatNumber(row.value, language)} {row.unitLabel || ""}</td>
                  <td className="px-4 py-3"><StatusBadge tone={row.tone}>{row.sourceLabel}</StatusBadge></td>
                  <td className="px-4 py-3 text-textSecondary">{row.sourceRef || "未提供"}</td>
                  <td className="max-w-[300px] px-4 py-3 text-xs leading-5 text-textSecondary">{row.authorityCaveat || "未提供"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function EffectivityTable({ rows, asOfDateLabel, language }: { rows: ManufacturingEffectivityRow[]; asOfDateLabel: string; language: string }) {
  return (
    <section className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <CalendarClock className="h-5 w-5 text-primary" aria-hidden="true" />
          <div>
            <h2 className="text-lg font-semibold text-textPrimary">效期與適用狀態</h2>
            <p className="mt-1 text-xs text-textSecondary">查詢基準日：{asOfDateLabel}</p>
          </div>
        </div>
        <StatusBadge tone={rows.some((row) => row.tone === "danger") ? "danger" : "info"}>{rows.length} 筆</StatusBadge>
      </div>
      {!rows.length ? (
        <SupportEmptyState title="沒有效期資料" description="後端未回傳各領域效期列；畫面不推測目前適用版本。" />
      ) : (
        <div className="overflow-x-auto rounded-lg border border-border">
          <table className="min-w-[820px] w-full border-collapse text-sm">
            <thead className="bg-slate-50 text-left text-xs font-semibold text-textSecondary">
              <tr>
                <th className="px-4 py-3">領域</th>
                <th className="px-4 py-3">生效起訖</th>
                <th className="px-4 py-3">目前適用</th>
                <th className="px-4 py-3">版本狀態</th>
                <th className="px-4 py-3">證據參照</th>
                <th className="px-4 py-3">衝突</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {rows.map((row, index) => (
                <tr key={`${row.domainCode}-${row.evidenceRef}-${index}`}>
                  <td className="px-4 py-3 font-medium text-textPrimary">{row.domainLabel}</td>
                  <td className="px-4 py-3 text-textSecondary">{row.effectiveFromLabel} - {row.effectiveToLabel}</td>
                  <td className="px-4 py-3 text-textSecondary">{flagLabel(row.currentActive, language)}</td>
                  <td className="px-4 py-3"><StatusBadge tone={row.tone}>{row.statusLabel}</StatusBadge></td>
                  <td className="px-4 py-3 text-textSecondary">{row.evidenceRef || "未提供"}</td>
                  <td className="px-4 py-3 text-textSecondary">{row.conflictState === "UNKNOWN" ? "未判定" : row.conflictState}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function WarningPanel({ rows }: { rows: ManufacturingWarning[] }) {
  return (
    <section className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-warning" aria-hidden="true" />
          <h2 className="text-lg font-semibold text-textPrimary">來源與警示</h2>
        </div>
        <StatusBadge tone={rows.length ? "warning" : "success"}>{rows.length ? `${rows.length} 項` : "無警示"}</StatusBadge>
      </div>
      <div className="mt-4 space-y-2">
        {rows.length ? rows.map((row, index) => (
          <div className="rounded-md border border-warning/20 bg-warning/5 p-3" key={`${row.code}-${row.refNo}-${index}`}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-sm font-semibold text-textPrimary">{row.domainLabel}</p>
                <p className="mt-1 text-sm leading-6 text-textSecondary">{row.message}</p>
              </div>
              <StatusBadge tone={row.tone}>{row.code}</StatusBadge>
            </div>
            {row.refNo ? <p className="mt-2 text-xs text-textSecondary">參照：{row.refNo}</p> : null}
          </div>
        )) : <p className="rounded-md bg-success/10 px-3 py-2 text-sm text-success">目前沒有未解警示。</p>}
      </div>
    </section>
  );
}

function LineagePanel({ rows }: { rows: ManufacturingLineage[] }) {
  return (
    <section className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex items-center gap-2">
        <GitBranch className="h-5 w-5 text-primary" aria-hidden="true" />
        <div>
          <h2 className="text-lg font-semibold text-textPrimary">來源 lineage</h2>
          <p className="mt-1 text-xs text-textSecondary">來源存在不等於業務事實已完成確認。</p>
        </div>
      </div>
      <div className="mt-4 space-y-3">
        {rows.length ? rows.map((row, index) => (
          <div className="rounded-md bg-slate-50 p-3" key={`${row.domainCode}-${row.sourceCode}-${index}`}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-sm font-semibold text-textPrimary">{row.domainLabel}</p>
                <p className="mt-1 text-xs text-textSecondary">{row.sourceLabel} · {row.sourceRef || "未提供參照"}</p>
              </div>
              <StatusBadge tone={row.tone}>{row.acceptedEvidenceLabel}</StatusBadge>
            </div>
            <p className="mt-2 text-xs leading-5 text-textSecondary">{row.authorityCaveat || "未提供來源限制說明"}</p>
          </div>
        )) : <SupportEmptyState title="沒有來源 lineage" description="API 回傳來源清單為空；畫面不補入推測來源。" />}
      </div>
    </section>
  );
}

function FreezePanel({ data }: { data: ManufacturingDefinitionData }) {
  const boundary = data.capabilityBoundary;
  const supported = [
    ["核准", boundary.approvalSupported],
    ["發布", boundary.releaseSupported],
    ["凍結", boundary.freezeSupported],
    ["Source-of-Truth transition", boundary.sourceOfTruthTransitionSupported],
    ["Cutover", boundary.cutoverSupported],
    ["Go-Live", boundary.goLiveSupported]
  ];
  return (
    <section className="rounded-lg border border-success/20 bg-success/5 p-4 shadow-card">
      <div className="flex items-center gap-2 text-success">
        <ShieldCheck className="h-5 w-5" aria-hidden="true" />
        <h2 className="text-lg font-semibold">唯讀能力邊界</h2>
      </div>
      <p className="mt-3 text-sm leading-6 text-textSecondary">
        此頁只呈現候選定義與來源證據；候選不等於正式標準，freeze compatibility 也不代表已授權凍結。
      </p>
      <div className="mt-4 rounded-md border border-warning/20 bg-white p-3">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-sm font-semibold text-textPrimary">凍結相容性預覽</p>
            <p className="mt-1 text-xs text-textSecondary">{data.freezeCompatibility.statusLabel}</p>
          </div>
          <StatusBadge tone={data.freezeCompatibility.tone}>{data.freezeCompatibility.previewOnly ? "僅供預覽" : "待確認"}</StatusBadge>
        </div>
        <p className="mt-3 text-sm text-textSecondary">候選警示 {data.freezeCompatibility.warningCount} 項；目前不可執行核准、發布或凍結。</p>
      </div>
      <div className="mt-4 grid gap-2 sm:grid-cols-2">
        {supported.map(([label, enabled]) => (
          <div className="flex items-center justify-between rounded-md bg-white px-3 py-2 text-sm" key={String(label)}>
            <span className="text-textSecondary">{label}</span>
            <StatusBadge tone={enabled ? "success" : "neutral"}>{enabled ? "可用" : "未提供"}</StatusBadge>
          </div>
        ))}
      </div>
    </section>
  );
}

function RelatedNavigation({ query }: { query: ManufacturingDefinitionQuery }) {
  const item = encodeURIComponent(query.itemNo);
  return (
    <section className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex items-center gap-2">
        <FileCheck2 className="h-5 w-5 text-primary" aria-hidden="true" />
        <h2 className="text-lg font-semibold text-textPrimary">關聯唯讀畫面</h2>
      </div>
      <div className="mt-4 grid gap-2 sm:grid-cols-2">
        {[
          ["Product / WIP 360", `/product-360?itemNo=${item}`],
          ["BOM 中心", `/bom?itemNo=${item}`],
          ["Recipe / Formula", `/recipe?itemNo=${item}`],
          ["Routing / Process Flow", `/routing?itemNo=${item}`],
          ["包裝規格", `/packaging?itemNo=${item}`]
        ].map(([label, href]) => (
          <Link className="rounded-button border border-border px-3 py-2 text-sm font-medium text-primary hover:bg-primary/5" href={href} key={href}>
            {label}
          </Link>
        ))}
      </div>
    </section>
  );
}

export default function ManufacturingDefinitionPage() {
  const { language } = useLanguage();
  const [dataSourceMode, setDataSourceMode] = useState<DataSourceMode>("api");
  const [scenario, setScenario] = useState<Scenario>("product");
  const [itemNoInput, setItemNoInput] = useState(scenarioDefaults.product.itemNo);
  const query = useMemo<ManufacturingDefinitionQuery>(
    () => ({
      itemNo: itemNoInput.trim() || scenarioDefaults[scenario].itemNo,
      itemCategory: scenario === "wip" ? 4 : 5
    }),
    [itemNoInput, scenario]
  );
  const { data, error, isLoading, source } = useManufacturingDefinitionOverview(query, dataSourceMode, language);
  const subject = data.subject;

  function selectScenario(nextScenario: Scenario) {
    setScenario(nextScenario);
    setItemNoInput(scenarioDefaults[nextScenario].itemNo);
  }

  return (
    <AppLayout activePath="/manufacturing-definition" title="製造定義唯讀工作區">
      <div className="mx-auto max-w-[1500px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">唯讀</StatusBadge>
                <DataSourceStatusBadge source={source} isLoading={isLoading} hasError={Boolean(error)} />
                <StatusBadge tone="neutral">候選視角</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">製造定義</h2>
              <p className="mt-2 max-w-4xl text-sm leading-6 text-textSecondary">
                以單一 Product 或 Standalone WIP 主體彙整 BOM、Recipe、Routing 與 Packaging 的候選證據，協助辨識適用版本、來源與資料缺口；本頁不代表正式核准標準。
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
            製造定義資料載入中...
          </p>
        ) : null}

        {error ? (
          <p className="rounded-lg border border-danger/20 bg-danger/10 px-4 py-3 text-sm leading-6 text-danger">
            製造定義 API 資料取得失敗，畫面未改用示範資料。{error}
          </p>
        ) : null}

        {!isLoading && !error && !subject ? (
          <SupportEmptyState title="沒有製造定義主體資料" description="後端 API 回傳空主體；畫面如實呈現，不以 BOM、Recipe 或 mock 推測補齊。" />
        ) : null}

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="min-w-0 space-y-5">
            <section className="rounded-lg border border-border bg-white p-4 shadow-card">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p className="text-xs font-medium text-textSecondary">主體摘要</p>
                  <h2 className="mt-1 text-xl font-semibold text-textPrimary">
                    {subject?.itemNo || query.itemNo || "未選取"} · {subject?.itemName || "尚未取得主體資料"}
                  </h2>
                  <p className="mt-2 text-sm text-textSecondary">
                    {subject?.identityTypeLabel || (scenario === "wip" ? "Standalone WIP" : "Product")} · {subject?.itemCategoryLabel || "待確認"} · {subject?.sourceLabel || "未提供來源"}
                  </p>
                </div>
                <StatusBadge tone={subject ? toneForResolution(data.resolutionStatus) : error ? "danger" : "neutral"}>
                  {subject ? data.resolutionStatusLabel : "待載入"}
                </StatusBadge>
              </div>
              <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
                <SummaryMetric label="候選狀態" value={subject ? definitionStatusLabel(data.definitionStatus, language) : "未提供"} hint="前端依 API 狀態轉譯" />
                <SummaryMetric label="主體版本" value={subject?.versionLabel || "未提供"} hint={subject ? subject.itemCategoryLabel : "Product / WIP"} />
                <SummaryMetric label="倉庫單位" value={subject?.unitWarehouseLabel || "未提供"} hint="前端 enum 轉譯" />
                <SummaryMetric label="生產單位" value={subject?.unitProductLabel || "未提供"} hint={`查詢類別 ${query.itemCategory}`} />
              </div>
            </section>

            <section className="rounded-lg border border-border bg-white p-4 shadow-card">
              <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="h-5 w-5 text-primary" aria-hidden="true" />
                  <div>
                    <h2 className="text-lg font-semibold text-textPrimary">製造定義候選</h2>
                    <p className="mt-1 text-xs text-textSecondary">Candidate 不等於正式核准標準；保留各領域版本候選。</p>
                  </div>
                </div>
                <StatusBadge tone={toneForResolution(data.resolutionStatus)}>{data.candidateVersions.length} 個候選</StatusBadge>
              </div>
              <VersionTable rows={data.candidateVersions} />
            </section>

            <section className="rounded-lg border border-border bg-white p-4 shadow-card">
              <div className="mb-4 flex items-center gap-2">
                <GitBranch className="h-5 w-5 text-primary" aria-hidden="true" />
                <div>
                  <h2 className="text-lg font-semibold text-textPrimary">跨模組定義參照</h2>
                  <p className="mt-1 text-xs text-textSecondary">顯示 Backend composition 已整理的模組狀態，不在前端重組業務規則。</p>
                </div>
              </div>
              <DomainReferenceGrid rows={data.domainReferences} />
            </section>

            <AuthorityTable title="數量依據" icon={Scale} rows={data.quantityAuthorities} language={language} />
            <AuthorityTable title="重量依據" icon={Weight} rows={data.weightAuthorities} language={language} />
            <EffectivityTable rows={data.effectivity} asOfDateLabel={data.effectivityAsOfDateLabel} language={language} />
          </div>

          <aside className="space-y-5">
            <WarningPanel rows={data.warnings} />
            <LineagePanel rows={data.sourceLineage} />
            <FreezePanel data={data} />
            <RelatedNavigation query={query} />
          </aside>
        </section>
      </div>
    </AppLayout>
  );
}
