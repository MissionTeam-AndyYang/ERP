"use client";

import { Boxes, PackageCheck, Tags } from "lucide-react";
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
  { label: "品項總數", value: "428", hint: "含原料包材", tone: "info" as const },
  { label: "成品", value: "86", hint: "32 項量產", tone: "success" as const },
  { label: "待維護", value: "11", hint: "規格缺漏", tone: "warning" as const },
  { label: "停用品項", value: "7", hint: "不可下單", tone: "neutral" as const }
];

const itemCards = [
  {
    eyebrow: "FG-CURRY-101",
    title: "咖哩雞肉調理包",
    subtitle: "成品 / 冷凍保存 / A1 調理包產線",
    status: "量產",
    tone: "success" as const,
    rows: [
      { label: "單位", value: "盒" },
      { label: "效期", value: "180 天" },
      { label: "BOM", value: "BOM-FG-CURRY-101" }
    ]
  },
  {
    eyebrow: "RM-CORN-001",
    title: "冷凍玉米粒",
    subtitle: "原料 / 冷凍保存 / 供應商綠田食品",
    status: "低庫存",
    tone: "warning" as const,
    rows: [
      { label: "單位", value: "kg" },
      { label: "保存", value: "-18°C" },
      { label: "安全庫存", value: "420 kg" }
    ]
  },
  {
    eyebrow: "PK-BAG-010",
    title: "耐熱殺菌袋",
    subtitle: "包材 / 常溫保存 / A1、A2 共用",
    status: "需採購",
    tone: "danger" as const,
    rows: [
      { label: "單位", value: "只" },
      { label: "規格", value: "180 x 260 mm" },
      { label: "安全庫存", value: "6,000 只" }
    ]
  }
];

const masterTasks = [
  {
    id: "ITEM-TASK-001",
    title: "番茄牛肉燉飯規格待補",
    detail: "需補齊過敏原、營養標示與適用產線。",
    meta: "關聯 BOM-FG-RICE-003",
    status: "待研發",
    tone: "warning" as const
  },
  {
    id: "ITEM-TASK-002",
    title: "包材替代品項需建立",
    detail: "因 PK-BAG-010 供應風險，需建立替代包材主資料。",
    meta: "關聯採購 RFQ-011",
    status: "需新增",
    tone: "info" as const
  }
];

const categories = [
  {
    title: "成品",
    items: [{ id: "FG-CURRY-101", title: "咖哩雞肉調理包", detail: "量產 / 冷凍", tone: "success" as const }]
  },
  {
    title: "半成品",
    items: [{ id: "WIP-SAUCE-008", title: "咖哩醬基底", detail: "需批號管理", tone: "info" as const }]
  },
  {
    title: "原料",
    items: [{ id: "RM-CORN-001", title: "冷凍玉米粒", detail: "低於安全庫存", tone: "warning" as const }]
  },
  {
    title: "包材",
    items: [{ id: "PK-BAG-010", title: "耐熱殺菌袋", detail: "需採購", tone: "danger" as const }]
  }
];

const itemsDashboardMock = {
  kpis,
  itemCards,
  masterTasks,
  categories
};

function itemCardMatchesSearch(item: (typeof itemCards)[number], query: string) {
  return matchesSupportSearch([
    item.eyebrow,
    item.title,
    item.subtitle,
    item.status,
    ...item.rows.flatMap((row) => [row.label, row.value])
  ], query);
}

function taskMatchesSearch(item: (typeof masterTasks)[number], query: string) {
  return matchesSupportSearch([item.id, item.title, item.detail, item.meta, item.status], query);
}

function categoryItemMatchesSearch(item: (typeof categories)[number]["items"][number], query: string) {
  return matchesSupportSearch([item.id, item.title, item.detail], query);
}

export default function ItemsPage() {
  const { data, error, isLoading, source } = useSupportDashboard(
    "/api/v1/items/dashboard",
    itemsDashboardMock,
    "Items API unavailable"
  );
  const [searchValue, setSearchValue] = useState("");
  const searchQuery = normalizeSupportSearch(searchValue);
  const filteredItemCards = useMemo(
    () => data.itemCards.filter((item) => itemCardMatchesSearch(item, searchQuery)),
    [data.itemCards, searchQuery]
  );
  const filteredMasterTasks = useMemo(
    () => data.masterTasks.filter((item) => taskMatchesSearch(item, searchQuery)),
    [data.masterTasks, searchQuery]
  );
  const filteredCategories = useMemo(
    () =>
      data.categories
        .map((category) => ({
          ...category,
          items: category.items.filter((item) => categoryItemMatchesSearch(item, searchQuery))
        }))
        .filter((category) => category.items.length > 0),
    [data.categories, searchQuery]
  );

  return (
    <AppLayout activePath="/items" title="品項中心 Item Master">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="Phase 1.5 Items"
          title="品項、物料與食品規格主資料"
          description="集中維護成品、半成品、原料與包材，包含 SKU、單位、保存條件、效期、規格與適用產線。"
          metrics={[
            { label: "品項", value: "428", icon: Tags },
            { label: "成品", value: "86", icon: PackageCheck },
            { label: "物料", value: "342", icon: Boxes }
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
            Items API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}
        <SupportSearchPanel
          ariaLabel="搜尋品項、物料、BOM 或待辦"
          placeholder="品項 / 物料 / BOM / 待辦"
          value={searchValue}
          onChange={setSearchValue}
        />
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {data.kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>
        {filteredCategories.length > 0 ? (
          <ProcessBoard eyebrow="Item Categories" title="品項分類看板" columns={filteredCategories} />
        ) : (
          <SupportEmptyState title="沒有符合條件的品項分類" description="請調整搜尋關鍵字，或確認主檔分類資料是否已建立。" />
        )}
        <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div className="grid gap-4">
            {filteredItemCards.length > 0 ? (
              filteredItemCards.map((item) => <DetailCard {...item} key={item.eyebrow} />)
            ) : (
              <SupportEmptyState title="沒有符合條件的品項" description="請調整搜尋關鍵字，或切回更寬的品項範圍檢查。" />
            )}
          </div>
          {filteredMasterTasks.length > 0 ? (
            <CompactListPanel eyebrow="Master Data Tasks" title="主資料待辦" items={filteredMasterTasks} />
          ) : (
            <SupportEmptyState title="沒有符合條件的主檔待辦" description="目前搜尋條件下沒有需要優先處理的主檔項目。" />
          )}
        </section>
      </div>
    </AppLayout>
  );
}
