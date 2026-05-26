"use client";

import { Beaker, FlaskConical, GitBranch, Search } from "lucide-react";
import { useMemo, useState } from "react";
import { CompactListPanel } from "@/components/common/compact-list-panel";
import { DetailCard } from "@/components/common/detail-card";
import { ModuleHero } from "@/components/common/module-hero";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { ProcessBoard } from "@/components/common/process-board";
import { StatusBadge } from "@/components/ui/status-badge";
import { useSupportDashboard } from "@/hooks/use-support-dashboard";
import { AppLayout } from "@/layouts/app-layout";

const kpis = [
  { label: "BOM 版本", value: "146", hint: "32 個量產", tone: "info" as const },
  { label: "研發中", value: "8", hint: "3 個試產", tone: "warning" as const },
  { label: "已核准", value: "118", hint: "可排產", tone: "success" as const },
  { label: "待變更", value: "5", hint: "需簽核", tone: "danger" as const }
];

const bomCards = [
  {
    eyebrow: "BOM-FG-CURRY-101 v3.2",
    title: "咖哩雞肉調理包標準配方",
    subtitle: "品項 FG-CURRY-101 / A1、A2 調理包產線",
    status: "量產核准",
    tone: "success" as const,
    rows: [
      { label: "主原料", value: "雞胸肉 42%" },
      { label: "關鍵參數", value: "殺菌 121°C / 18 分" },
      { label: "生效日", value: "2026-05-01" }
    ]
  },
  {
    eyebrow: "BOM-FG-RICE-003 v0.9",
    title: "番茄牛肉燉飯試產配方",
    subtitle: "品項 FG-RICE-003 / 新品試賣訂單",
    status: "試產中",
    tone: "warning" as const,
    rows: [
      { label: "主原料", value: "牛肉 28%" },
      { label: "關鍵參數", value: "充填 240g / 盒" },
      { label: "待確認", value: "營養標示" }
    ]
  }
];

const changeTasks = [
  {
    id: "BOM-CR-001",
    title: "耐熱殺菌袋替代包材評估",
    detail: "若替代包材導入，需確認殺菌參數與金檢設定是否調整。",
    meta: "關聯 PK-BAG-010 / RFQ-011",
    status: "待研發",
    tone: "warning" as const
  },
  {
    id: "BOM-CR-002",
    title: "咖哩醬基底減鈉版本",
    detail: "客戶要求鈉含量降低 8%，需建立 v3.3 試產版本。",
    meta: "關聯 FG-CURRY-101",
    status: "需求確認",
    tone: "info" as const
  }
];

const lifecycle = [
  {
    title: "研發",
    items: [{ id: "BOM-RD-012", title: "減鈉咖哩醬", detail: "配方調整中", tone: "info" as const }]
  },
  {
    title: "試產",
    items: [{ id: "BOM-RICE-003", title: "番茄牛肉燉飯", detail: "v0.9 試產", tone: "warning" as const }]
  },
  {
    title: "簽核",
    items: [{ id: "BOM-CR-001", title: "包材替代", detail: "待 QA/RD 確認", tone: "danger" as const }]
  },
  {
    title: "量產",
    items: [{ id: "BOM-CURRY-101", title: "咖哩雞肉調理包", detail: "v3.2 生效", tone: "success" as const }]
  }
];

const bomDashboardMock = {
  kpis,
  bomCards,
  changeTasks,
  lifecycle
};

function normalizeSearch(value: string) {
  return value.trim().toLowerCase();
}

function includesSearch(value: string | number | null | undefined, query: string) {
  return String(value ?? "").toLowerCase().includes(query);
}

function bomCardMatchesSearch(item: (typeof bomCards)[number], query: string) {
  if (!query) {
    return true;
  }

  return [
    item.eyebrow,
    item.title,
    item.subtitle,
    item.status,
    ...item.rows.flatMap((row) => [row.label, row.value])
  ].some((value) => includesSearch(value, query));
}

function changeTaskMatchesSearch(item: (typeof changeTasks)[number], query: string) {
  if (!query) {
    return true;
  }

  return [item.id, item.title, item.detail, item.meta, item.status].some((value) => includesSearch(value, query));
}

function lifecycleItemMatchesSearch(item: (typeof lifecycle)[number]["items"][number], query: string) {
  if (!query) {
    return true;
  }

  return [item.id, item.title, item.detail].some((value) => includesSearch(value, query));
}

function EmptyState({ title, description }: { title: string; description: string }) {
  return (
    <div className="rounded-lg border border-dashed border-border bg-slate-50 px-4 py-10 text-center">
      <p className="font-semibold text-textPrimary">{title}</p>
      <p className="mt-2 text-sm text-textSecondary">{description}</p>
    </div>
  );
}

export default function BomPage() {
  const { data, error, isLoading, source } = useSupportDashboard(
    "/api/v1/bom/dashboard",
    bomDashboardMock,
    "BOM API unavailable"
  );
  const [searchValue, setSearchValue] = useState("");
  const searchQuery = normalizeSearch(searchValue);
  const filteredBomCards = useMemo(
    () => data.bomCards.filter((item) => bomCardMatchesSearch(item, searchQuery)),
    [data.bomCards, searchQuery]
  );
  const filteredChangeTasks = useMemo(
    () => data.changeTasks.filter((item) => changeTaskMatchesSearch(item, searchQuery)),
    [data.changeTasks, searchQuery]
  );
  const filteredLifecycle = useMemo(
    () =>
      data.lifecycle
        .map((stage) => ({
          ...stage,
          items: stage.items.filter((item) => lifecycleItemMatchesSearch(item, searchQuery))
        }))
        .filter((stage) => stage.items.length > 0),
    [data.lifecycle, searchQuery]
  );

  return (
    <AppLayout activePath="/bom" title="研發 BOM / 配方中心">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="Phase 1.5 R&D BOM"
          title="配方、BOM 版本與製程參數管理"
          description="管理食品配方、原料比例、包材、製程參數與版本簽核，讓訂單與工單可以引用正確量產 BOM。"
          metrics={[
            { label: "BOM", value: "146", icon: GitBranch },
            { label: "試產", value: "8", icon: Beaker },
            { label: "參數", value: "52", icon: FlaskConical }
          ]}
        />
        <div className="flex flex-wrap gap-2">
          <StatusBadge tone={source === "api" ? "success" : "warning"}>
            {source === "api" ? "API data" : "Mock fallback"}
          </StatusBadge>
          {isLoading ? <StatusBadge tone="info">Loading API</StatusBadge> : null}
        </div>
        {error ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            BOM API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <label className="flex h-10 max-w-xl items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
            <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
            <input
              aria-label="搜尋 BOM、品項、版本或參數"
              className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
              placeholder="BOM / 品項 / 版本 / 參數"
              value={searchValue}
              onChange={(event) => setSearchValue(event.target.value)}
            />
          </label>
        </section>
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {data.kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>
        {filteredLifecycle.length > 0 ? (
          <ProcessBoard eyebrow="BOM Lifecycle" title="研發 BOM 版本流程" columns={filteredLifecycle} />
        ) : (
          <EmptyState title="沒有符合條件的 BOM 流程" description="請調整搜尋關鍵字，或確認 BOM 版本資料是否已建立。" />
        )}
        <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div className="grid gap-4">
            {filteredBomCards.length > 0 ? (
              filteredBomCards.map((item) => <DetailCard {...item} key={item.eyebrow} />)
            ) : (
              <EmptyState title="沒有符合條件的 BOM" description="請調整搜尋關鍵字，或切回更寬的 BOM 範圍檢查。" />
            )}
          </div>
          {filteredChangeTasks.length > 0 ? (
            <CompactListPanel eyebrow="Change Requests" title="配方變更與簽核" items={filteredChangeTasks} />
          ) : (
            <EmptyState title="沒有符合條件的變更待辦" description="目前搜尋條件下沒有需要優先處理的 BOM 變更項目。" />
          )}
        </section>
      </div>
    </AppLayout>
  );
}
