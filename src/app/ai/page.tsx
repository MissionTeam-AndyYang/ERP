"use client";

import { AlertTriangle, BrainCircuit, CheckCircle2, ClipboardList, Clock3 } from "lucide-react";
import { useMemo, useState } from "react";
import { ModuleHero } from "@/components/common/module-hero";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { SupportEmptyState } from "@/components/common/support-empty-state";
import { SupportSearchPanel } from "@/components/common/support-search-panel";
import { StatusBadge } from "@/components/ui/status-badge";
import { useSupportDashboard } from "@/hooks/use-support-dashboard";
import { AppLayout } from "@/layouts/app-layout";
import type { StatusTone } from "@/types/dashboard";
import { matchesSupportSearch, normalizeSupportSearch } from "@/utils/support-search";

type ProgressState = "normal" | "inProgress" | "attention" | "delayed";

type SourceRecord = {
  id: string;
  module: string;
  detail: string;
};

type TodayWorkItem = {
  workItemId: string;
  module: string;
  title: string;
  customerOrTarget: string;
  plannedTime: string;
  currentStatus: string;
  progressState: ProgressState;
  progressLabel: string;
  tone: StatusTone;
  delayMinutes: number;
  reasonSummary: string;
  impactSummary: string;
  ownerArea: string;
  sourceRecords: SourceRecord[];
};

const progressOrder: Record<ProgressState, number> = {
  delayed: 0,
  attention: 1,
  inProgress: 2,
  normal: 3
};

const kpis = [
  { label: "今日工作", value: "42", hint: "跨 8 模組", tone: "info" as const },
  { label: "進行中", value: "28", hint: "依序推進", tone: "success" as const },
  { label: "注意", value: "9", hint: "需追蹤", tone: "warning" as const },
  { label: "已落後", value: "5", hint: "需確認", tone: "danger" as const }
];

const todayWorkItems: TodayWorkItem[] = [
  {
    workItemId: "MO-240512-001",
    module: "Production",
    title: "B2 冷凍蔬菜工單開線",
    customerOrTarget: "B2 產線 / 16:20",
    plannedTime: "16:20",
    currentStatus: "待補料",
    progressState: "delayed",
    progressLabel: "已落後",
    tone: "danger",
    delayMinutes: 45,
    reasonSummary: "RM240506-CORN 可用量低於今日投料需求。",
    impactSummary: "影響 B2 開線與後續冷凍蔬菜包裝入庫。",
    ownerArea: "倉庫 / 生管",
    sourceRecords: [
      { id: "RM240506-CORN", module: "Warehouse", detail: "可用庫存 180 kg" },
      { id: "PO-240508-014", module: "Purchasing", detail: "供應商預計 17:30 到貨" },
      { id: "APS-B2-1610", module: "Planning", detail: "原排程 16:20 開線" }
    ]
  },
  {
    workItemId: "QC-240512-018",
    module: "Quality",
    title: "A1 成品批號 QA 放行",
    customerOrTarget: "B240512-A101 / 全聯中區 DC",
    plannedTime: "15:30",
    currentStatus: "檢驗中",
    progressState: "delayed",
    progressLabel: "已落後",
    tone: "danger",
    delayMinutes: 30,
    reasonSummary: "金檢重檢率高於今日門檻，QA 尚未放行。",
    impactSummary: "影響 18:00 出貨備貨與物流冷鏈文件。",
    ownerArea: "品保 / 物流",
    sourceRecords: [
      { id: "B240512-A101", module: "Batches", detail: "成品批號待 QA 放行" },
      { id: "NCR-240512-004", module: "Quality", detail: "金檢重檢率異常" },
      { id: "SH-240512-08", module: "Logistics", detail: "18:00 出車排程" }
    ]
  },
  {
    workItemId: "PO-240511-022",
    module: "Purchasing",
    title: "耐熱殺菌袋到貨確認",
    customerOrTarget: "PK-BAG-010 / A1、A2 共用",
    plannedTime: "14:00",
    currentStatus: "待收貨",
    progressState: "attention",
    progressLabel: "注意",
    tone: "warning",
    delayMinutes: 0,
    reasonSummary: "供應商到貨時間接近今日包材安全庫存下限。",
    impactSummary: "若 16:00 前未完成收貨，明日 A2 工單需重排。",
    ownerArea: "採購 / 倉庫",
    sourceRecords: [
      { id: "PK-BAG-010", module: "Items", detail: "安全庫存 6,000 只" },
      { id: "PO-240511-022", module: "Purchasing", detail: "今日到貨待確認" }
    ]
  },
  {
    workItemId: "SO-240512-009",
    module: "Orders",
    title: "急單交期可行性確認",
    customerOrTarget: "便利通路新品試賣",
    plannedTime: "17:00",
    currentStatus: "評估中",
    progressState: "attention",
    progressLabel: "注意",
    tone: "warning",
    delayMinutes: 0,
    reasonSummary: "產能可用，但 BOM v0.9 營養標示仍待確認。",
    impactSummary: "影響業務今日是否回覆客戶承諾交期。",
    ownerArea: "業務 / 研發 / 生管",
    sourceRecords: [
      { id: "BOM-FG-RICE-003", module: "BOM", detail: "試產版本 v0.9" },
      { id: "RD-240510-006", module: "R&D", detail: "營養標示待補" }
    ]
  },
  {
    workItemId: "WH-OUT-240512-031",
    module: "Warehouse",
    title: "全聯中區 DC 出貨揀貨",
    customerOrTarget: "常溫暫存區 / 17:20",
    plannedTime: "17:20",
    currentStatus: "進行中",
    progressState: "inProgress",
    progressLabel: "進行中",
    tone: "info",
    delayMinutes: 0,
    reasonSummary: "揀貨進度正常，等待 QA 放行批號併入出貨。",
    impactSummary: "若 QA 延遲解除，出貨備貨時間會被壓縮。",
    ownerArea: "倉庫",
    sourceRecords: [
      { id: "SH-240512-08", module: "Logistics", detail: "全聯中區 DC 出貨" },
      { id: "QC-240512-018", module: "Quality", detail: "QA 放行待完成" }
    ]
  },
  {
    workItemId: "DOC-240512-006",
    module: "Documents",
    title: "出口批次文件補齊",
    customerOrTarget: "海外客戶 / 冷凍調理包",
    plannedTime: "18:00",
    currentStatus: "待確認",
    progressState: "delayed",
    progressLabel: "已落後",
    tone: "danger",
    delayMinutes: 25,
    reasonSummary: "COA 與溫度紀錄尚未完成主管確認。",
    impactSummary: "影響晚間物流文件封存與出貨審核。",
    ownerArea: "品保 / 業務",
    sourceRecords: [
      { id: "COA-240512-011", module: "Quality", detail: "COA 待確認" },
      { id: "SH-EXP-240512-02", module: "Logistics", detail: "出口文件封存" }
    ]
  }
];

const aiDashboardMock = {
  kpis,
  todayWorkItems
};

function workItemMatchesSearch(item: TodayWorkItem, query: string) {
  return matchesSupportSearch(
    [
      item.workItemId,
      item.module,
      item.title,
      item.customerOrTarget,
      item.plannedTime,
      item.currentStatus,
      item.progressLabel,
      item.reasonSummary,
      item.impactSummary,
      item.ownerArea,
      ...item.sourceRecords.flatMap((record) => [record.id, record.module, record.detail])
    ],
    query
  );
}

function sortWorkItems(items: TodayWorkItem[]) {
  return [...items].sort((a, b) => {
    const stateDiff = progressOrder[a.progressState] - progressOrder[b.progressState];

    if (stateDiff !== 0) {
      return stateDiff;
    }

    return b.delayMinutes - a.delayMinutes;
  });
}

function WorkItemRow({
  item,
  isSelected,
  onSelect
}: {
  item: TodayWorkItem;
  isSelected: boolean;
  onSelect: () => void;
}) {
  return (
    <button
      aria-pressed={isSelected}
      className={`w-full rounded-lg border p-4 text-left transition ${
        isSelected ? "border-primary bg-primary/5 shadow-card" : "border-border bg-white hover:border-primary/40"
      }`}
      onClick={onSelect}
      type="button"
    >
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <p className="text-sm font-semibold text-primary">{item.workItemId}</p>
            <StatusBadge tone={item.tone}>{item.progressLabel}</StatusBadge>
          </div>
          <h3 className="mt-2 text-base font-semibold text-textPrimary">{item.title}</h3>
          <p className="mt-1 text-sm text-textSecondary">{item.customerOrTarget}</p>
        </div>
        <div className="text-right text-sm">
          <p className="font-semibold text-textPrimary">{item.plannedTime}</p>
          <p className="mt-1 text-textSecondary">{item.module}</p>
        </div>
      </div>
      <div className="mt-4 grid gap-3 text-sm md:grid-cols-3">
        <div>
          <p className="text-xs text-textSecondary">目前狀態</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.currentStatus}</p>
        </div>
        <div>
          <p className="text-xs text-textSecondary">負責單位</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.ownerArea}</p>
        </div>
        <div>
          <p className="text-xs text-textSecondary">時間差</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {item.delayMinutes > 0 ? `落後 ${item.delayMinutes} 分` : "未落後"}
          </p>
        </div>
      </div>
    </button>
  );
}

function DelayedFocus({ items, onSelect }: { items: TodayWorkItem[]; onSelect: (id: string) => void }) {
  if (items.length === 0) {
    return <SupportEmptyState title="目前沒有已落後項目" description="今日工作尚未出現需要優先處理的落後項目。" />;
  }

  return (
    <section className="grid gap-4 lg:grid-cols-3">
      {items.map((item) => (
        <button
          className="rounded-card border border-danger/20 bg-white p-5 text-left shadow-card transition hover:border-danger/50"
          key={item.workItemId}
          onClick={() => onSelect(item.workItemId)}
          type="button"
        >
          <div className="flex items-center justify-between gap-3">
            <p className="text-sm font-semibold text-primary">{item.workItemId}</p>
            <StatusBadge tone="danger">落後 {item.delayMinutes} 分</StatusBadge>
          </div>
          <h3 className="mt-3 text-base font-semibold text-textPrimary">{item.title}</h3>
          <p className="mt-2 text-sm leading-6 text-textSecondary">{item.reasonSummary}</p>
          <p className="mt-3 text-xs font-semibold text-danger">{item.impactSummary}</p>
        </button>
      ))}
    </section>
  );
}

function SelectedWorkDetail({ item }: { item: TodayWorkItem }) {
  return (
    <aside className="rounded-card border border-border bg-white p-5 shadow-card">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-primary">{item.workItemId}</p>
          <h2 className="mt-1 text-xl font-semibold text-textPrimary">{item.title}</h2>
          <p className="mt-1 text-sm text-textSecondary">{item.customerOrTarget}</p>
        </div>
        <StatusBadge tone={item.tone}>{item.progressLabel}</StatusBadge>
      </div>
      <div className="mt-5 grid gap-3 sm:grid-cols-2">
        {[
          { label: "模組", value: item.module },
          { label: "預計時間", value: item.plannedTime },
          { label: "目前狀態", value: item.currentStatus },
          { label: "負責單位", value: item.ownerArea }
        ].map((row) => (
          <div className="rounded-button bg-slate-50 p-3 text-sm" key={row.label}>
            <p className="text-xs text-textSecondary">{row.label}</p>
            <p className="mt-1 font-semibold text-textPrimary">{row.value}</p>
          </div>
        ))}
      </div>
      <div className="mt-5 space-y-4">
        <div>
          <p className="text-xs font-semibold text-textSecondary">原因摘要</p>
          <p className="mt-2 text-sm leading-6 text-textPrimary">{item.reasonSummary}</p>
        </div>
        <div>
          <p className="text-xs font-semibold text-textSecondary">影響範圍</p>
          <p className="mt-2 text-sm leading-6 text-textPrimary">{item.impactSummary}</p>
        </div>
      </div>
      <div className="mt-6">
        <p className="text-sm font-semibold text-textPrimary">來源紀錄</p>
        <div className="mt-3 space-y-3">
          {item.sourceRecords.map((record) => (
            <div className="rounded-lg border border-border p-3" key={`${record.module}-${record.id}`}>
              <div className="flex items-center justify-between gap-3">
                <p className="text-sm font-semibold text-primary">{record.id}</p>
                <span className="text-xs text-textSecondary">{record.module}</span>
              </div>
              <p className="mt-1 text-sm text-textSecondary">{record.detail}</p>
            </div>
          ))}
        </div>
      </div>
    </aside>
  );
}

export default function AiPage() {
  const { data, error, isLoading, source } = useSupportDashboard(
    "/api/v1/ai/dashboard",
    aiDashboardMock,
    "AI API unavailable"
  );
  const [searchValue, setSearchValue] = useState("");
  const [selectedId, setSelectedId] = useState(data.todayWorkItems[0]?.workItemId ?? "");
  const searchQuery = normalizeSupportSearch(searchValue);
  const filteredWorkItems = useMemo(
    () => sortWorkItems(data.todayWorkItems.filter((item) => workItemMatchesSearch(item, searchQuery))),
    [data.todayWorkItems, searchQuery]
  );
  const delayedItems = useMemo(
    () => filteredWorkItems.filter((item) => item.progressState === "delayed"),
    [filteredWorkItems]
  );
  const selectedWorkItem =
    filteredWorkItems.find((item) => item.workItemId === selectedId) ?? filteredWorkItems[0] ?? data.todayWorkItems[0];

  return (
    <AppLayout activePath="/ai" title="AI 中心 AI Work Status">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="AI V1.1 Work Status"
          title="今日工作狀態與落後項目總覽"
          description="整合訂單、採購、倉庫、生產、品質、物流、文件與財務訊號，先讓今日工作進度與已落後項目清楚可見。"
          metrics={[
            { label: "工作", value: "42", icon: ClipboardList },
            { label: "注意", value: "9", icon: AlertTriangle },
            { label: "落後", value: "5", icon: Clock3 },
            { label: "AI", value: "V1.1", icon: BrainCircuit }
          ]}
        />
        <div className="flex flex-wrap gap-2">
          <StatusBadge tone={source === "api" ? "success" : "warning"}>
            {source === "api" ? "API data" : "Mock fallback"}
          </StatusBadge>
          <StatusBadge tone="info">Read-only visibility</StatusBadge>
          {isLoading ? <StatusBadge tone="info">Loading API</StatusBadge> : null}
        </div>
        {error ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            AI API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}
        <SupportSearchPanel
          ariaLabel="搜尋今日工作、模組、狀態、負責單位或來源紀錄"
          placeholder="工作 / 模組 / 狀態 / 負責單位 / 紀錄"
          value={searchValue}
          onChange={setSearchValue}
        />
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {data.kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>
        <DelayedFocus items={delayedItems} onSelect={setSelectedId} />
        <section className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_420px]">
          <article className="rounded-card border border-border bg-white p-5 shadow-card">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-sm font-medium text-textSecondary">Today Work Items</p>
                <h2 className="text-xl font-semibold text-textPrimary">今日工作項目</h2>
              </div>
              <div className="flex items-center gap-2 text-sm text-textSecondary">
                <CheckCircle2 className="h-4 w-4 text-success" aria-hidden="true" />
                <span>{filteredWorkItems.length} 筆</span>
              </div>
            </div>
            <div className="mt-5 space-y-3">
              {filteredWorkItems.length > 0 ? (
                filteredWorkItems.map((item) => (
                  <WorkItemRow
                    isSelected={selectedWorkItem?.workItemId === item.workItemId}
                    item={item}
                    key={item.workItemId}
                    onSelect={() => setSelectedId(item.workItemId)}
                  />
                ))
              ) : (
                <SupportEmptyState title="沒有符合條件的今日工作" description="請調整搜尋關鍵字，或切回更寬的工作範圍檢查。" />
              )}
            </div>
          </article>
          {selectedWorkItem ? (
            <SelectedWorkDetail item={selectedWorkItem} />
          ) : (
            <SupportEmptyState title="尚未選取工作項目" description="請從今日工作項目清單中選取一筆資料查看細節。" />
          )}
        </section>
      </div>
    </AppLayout>
  );
}
