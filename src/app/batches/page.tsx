"use client";

import { Barcode, CalendarClock, Network } from "lucide-react";
import { useMemo, useState } from "react";
import { CompactListPanel } from "@/components/common/compact-list-panel";
import { DetailCard } from "@/components/common/detail-card";
import { ModuleHero } from "@/components/common/module-hero";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { ProcessBoard } from "@/components/common/process-board";
import { SupportEmptyState } from "@/components/common/support-empty-state";
import { SupportSearchPanel } from "@/components/common/support-search-panel";
import { StatusBadge } from "@/components/ui/status-badge";
import { useSupportDashboard } from "@/hooks/use-support-dashboard";
import { AppLayout } from "@/layouts/app-layout";
import { matchesSupportSearch, normalizeSupportSearch } from "@/utils/support-search";

const kpis = [
  { label: "批號總數", value: "1,284", hint: "近 90 天", tone: "info" as const },
  { label: "製程批號", value: "312", hint: "今日 18 筆", tone: "success" as const },
  { label: "即期批號", value: "9", hint: "7 日內", tone: "warning" as const },
  { label: "隔離批號", value: "2", hint: "QA 鎖定", tone: "danger" as const }
];

const batchCards = [
  {
    eyebrow: "B240512-A101",
    title: "咖哩雞肉調理包成品批號",
    subtitle: "品項 FG-CURRY-101 / 工單 MO-240512-001",
    status: "生產中",
    tone: "success" as const,
    rows: [
      { label: "數量", value: "6,912 / 9,600 盒" },
      { label: "效期", value: "2026-11-08" },
      { label: "QA", value: "檢驗中" }
    ]
  },
  {
    eyebrow: "RM240506-CORN",
    title: "冷凍玉米粒原料批號",
    subtitle: "供應商綠田食品 / 庫位 FZ-A03-02",
    status: "即期",
    tone: "danger" as const,
    rows: [
      { label: "庫存", value: "180 kg" },
      { label: "效期", value: "2026-05-17" },
      { label: "去向", value: "B2 待領料" }
    ]
  }
];

const batchTasks = [
  {
    id: "BAT-TASK-001",
    title: "RM240506-CORN 即期優先使用",
    detail: "建議優先配置到 B2 冷凍蔬菜工單，避免原料逾期。",
    meta: "剩餘 5 天 / 180 kg",
    status: "需處理",
    tone: "danger" as const
  },
  {
    id: "BAT-TASK-002",
    title: "B240512-A101 待 QA 放行",
    detail: "成品批號需完成金檢與重量檢驗後才可入庫。",
    meta: "關聯 QC-240512-018",
    status: "檢驗中",
    tone: "info" as const
  }
];

const lifecycle = [
  {
    title: "原料批號",
    items: [{ id: "RM240506-CORN", title: "冷凍玉米粒", detail: "入庫 / 即期", tone: "danger" as const }]
  },
  {
    title: "製程批號",
    items: [{ id: "WIP240512-A101", title: "咖哩醬基底", detail: "A1 調理", tone: "info" as const }]
  },
  {
    title: "成品批號",
    items: [{ id: "B240512-A101", title: "咖哩雞肉調理包", detail: "生產中", tone: "success" as const }]
  },
  {
    title: "出貨批號",
    items: [{ id: "SH-240512-08", title: "全聯中區 DC", detail: "待出貨", tone: "warning" as const }]
  }
];

const batchesDashboardMock = {
  kpis,
  batchCards,
  batchTasks,
  lifecycle
};

function batchCardMatchesSearch(item: (typeof batchCards)[number], query: string) {
  return matchesSupportSearch([
    item.eyebrow,
    item.title,
    item.subtitle,
    item.status,
    ...item.rows.flatMap((row) => [row.label, row.value])
  ], query);
}

function batchTaskMatchesSearch(item: (typeof batchTasks)[number], query: string) {
  return matchesSupportSearch([item.id, item.title, item.detail, item.meta, item.status], query);
}

function lifecycleItemMatchesSearch(item: (typeof lifecycle)[number]["items"][number], query: string) {
  return matchesSupportSearch([item.id, item.title, item.detail], query);
}

export default function BatchesPage() {
  const { data, error, isLoading, source } = useSupportDashboard(
    "/api/v1/batches/dashboard",
    batchesDashboardMock,
    "Batches API unavailable"
  );
  const [searchValue, setSearchValue] = useState("");
  const searchQuery = normalizeSupportSearch(searchValue);
  const filteredBatchCards = useMemo(
    () => data.batchCards.filter((item) => batchCardMatchesSearch(item, searchQuery)),
    [data.batchCards, searchQuery]
  );
  const filteredBatchTasks = useMemo(
    () => data.batchTasks.filter((item) => batchTaskMatchesSearch(item, searchQuery)),
    [data.batchTasks, searchQuery]
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
    <AppLayout activePath="/batches" title="批號中心 Batch Module">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="Phase 1.5 Batches"
          title="原料、製程、成品與出貨批號管理"
          description="把食品工廠最重要的批號生命週期獨立管理，串接效期、庫位、檢驗狀態、工單與出貨去向。"
          metrics={[
            { label: "批號", value: "1,284", icon: Barcode },
            { label: "即期", value: "9", icon: CalendarClock },
            { label: "鏈路", value: "99%", icon: Network }
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
            Batches API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}
        <SupportSearchPanel
          ariaLabel="搜尋批號、品項、工單、庫位或待辦"
          placeholder="批號 / 品項 / 工單 / 庫位 / 待辦"
          value={searchValue}
          onChange={setSearchValue}
        />
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {data.kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>
        {filteredLifecycle.length > 0 ? (
          <ProcessBoard eyebrow="Batch Lifecycle" title="批號生命週期" columns={filteredLifecycle} />
        ) : (
          <SupportEmptyState title="沒有符合條件的批號流程" description="請調整搜尋關鍵字，或確認批號生命週期資料是否已建立。" />
        )}
        <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div className="grid gap-4">
            {filteredBatchCards.length > 0 ? (
              filteredBatchCards.map((item) => <DetailCard {...item} key={item.eyebrow} />)
            ) : (
              <SupportEmptyState title="沒有符合條件的批號" description="請調整搜尋關鍵字，或切回更寬的批號範圍檢查。" />
            )}
          </div>
          {filteredBatchTasks.length > 0 ? (
            <CompactListPanel eyebrow="Batch Tasks" title="批號風險與待辦" items={filteredBatchTasks} />
          ) : (
            <SupportEmptyState title="沒有符合條件的批號待辦" description="目前搜尋條件下沒有需要優先處理的批號風險項目。" />
          )}
        </section>
      </div>
    </AppLayout>
  );
}
