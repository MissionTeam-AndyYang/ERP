"use client";

import { Barcode, CalendarClock, Network } from "lucide-react";
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

type BatchDistributionRow = {
  batchNo: string;
  batchType: string;
  warehouse: string;
  location: string;
  quantity: string;
  availableQuantity: string;
  reservedQuantity: string;
  quarantineQuantity: string;
  expiryDate: string;
  qaStatus: string;
  batchStage: string;
  relatedWork: string[];
  riskTags: string[];
  tone: StatusTone;
};

type BatchItemSummary = {
  itemId: string;
  itemName: string;
  itemType: string;
  totalBatchCount: number;
  warehouseCount: number;
  totalQuantity: string;
  availableQuantity: string;
  reservedQuantity: string;
  heldQuantity: string;
  earliestExpiryDate: string;
  qaHoldBatchCount: number;
  quarantineBatchCount: number;
  nearExpiryBatchCount: number;
  demandImpact: string;
  highestRisk: "normal" | "attention" | "highRisk";
  riskLabel: string;
  tone: StatusTone;
  ownerArea: string;
  batches: BatchDistributionRow[];
};

type BatchesDashboardData = {
  kpis: Array<{
    label: string;
    value: string;
    hint: string;
    tone: StatusTone;
  }>;
  itemSummaries: BatchItemSummary[];
};

const kpis = [
  { label: "批號管理品項", value: "86", hint: "啟用批號", tone: "info" as const },
  { label: "高風險品項", value: "3", hint: "QA/即期/隔離", tone: "danger" as const },
  { label: "分倉批號", value: "42", hint: "跨 5 倉", tone: "warning" as const },
  { label: "待確認量", value: "1,420 kg", hint: "Hold/隔離", tone: "neutral" as const }
];

const itemSummaries: BatchItemSummary[] = [
  {
    itemId: "FG-CURRY-101",
    itemName: "咖哩雞肉調理包",
    itemType: "成品",
    totalBatchCount: 4,
    warehouseCount: 3,
    totalQuantity: "18,240 盒",
    availableQuantity: "9,600 盒",
    reservedQuantity: "5,760 盒",
    heldQuantity: "2,880 盒",
    earliestExpiryDate: "2026-11-08",
    qaHoldBatchCount: 1,
    quarantineBatchCount: 0,
    nearExpiryBatchCount: 0,
    demandImpact: "今日出貨 SO-240526-018 受 QA 放行影響",
    highestRisk: "highRisk",
    riskLabel: "出貨受阻",
    tone: "danger",
    ownerArea: "品保",
    batches: [
      {
        batchNo: "B240512-A101",
        batchType: "finishedGoods",
        warehouse: "WH-FG-A",
        location: "A1-02-03",
        quantity: "9,600 盒",
        availableQuantity: "9,600 盒",
        reservedQuantity: "0 盒",
        quarantineQuantity: "0 盒",
        expiryDate: "2026-11-08",
        qaStatus: "已放行",
        batchStage: "可出貨",
        relatedWork: ["MO-240512-001", "QC-240512-018"],
        riskTags: ["正常可用"],
        tone: "success"
      },
      {
        batchNo: "B240513-A102",
        batchType: "finishedGoods",
        warehouse: "WH-QA-HOLD",
        location: "HOLD-01",
        quantity: "2,880 盒",
        availableQuantity: "0 盒",
        reservedQuantity: "2,880 盒",
        quarantineQuantity: "0 盒",
        expiryDate: "2026-11-09",
        qaStatus: "QA Hold",
        batchStage: "成品待放行",
        relatedWork: ["MO-240513-003", "QC-240513-027", "SO-240526-018"],
        riskTags: ["QA Hold", "已分配未放行"],
        tone: "danger"
      },
      {
        batchNo: "B240516-A106",
        batchType: "finishedGoods",
        warehouse: "WH-FG-B",
        location: "B2-01-01",
        quantity: "3,840 盒",
        availableQuantity: "0 盒",
        reservedQuantity: "2,880 盒",
        quarantineQuantity: "0 盒",
        expiryDate: "2026-11-12",
        qaStatus: "已放行",
        batchStage: "已分配",
        relatedWork: ["SO-240526-012"],
        riskTags: ["已預留"],
        tone: "info"
      },
      {
        batchNo: "B240518-A109",
        batchType: "finishedGoods",
        warehouse: "WH-FG-C",
        location: "C1-04-02",
        quantity: "1,920 盒",
        availableQuantity: "0 盒",
        reservedQuantity: "0 盒",
        quarantineQuantity: "0 盒",
        expiryDate: "2026-11-14",
        qaStatus: "檢驗中",
        batchStage: "成品待放行",
        relatedWork: ["QC-240518-011"],
        riskTags: ["檢驗中"],
        tone: "warning"
      }
    ]
  },
  {
    itemId: "RM-CORN-001",
    itemName: "冷凍玉米粒",
    itemType: "原料",
    totalBatchCount: 3,
    warehouseCount: 2,
    totalQuantity: "1,260 kg",
    availableQuantity: "720 kg",
    reservedQuantity: "360 kg",
    heldQuantity: "180 kg",
    earliestExpiryDate: "2026-05-31",
    qaHoldBatchCount: 0,
    quarantineBatchCount: 1,
    nearExpiryBatchCount: 1,
    demandImpact: "B2 冷凍蔬菜工單今日領料需優先確認",
    highestRisk: "highRisk",
    riskLabel: "即期/隔離",
    tone: "danger",
    ownerArea: "倉庫",
    batches: [
      {
        batchNo: "RM240506-CORN",
        batchType: "rawMaterial",
        warehouse: "WH-FZ-A",
        location: "FZ-A03-02",
        quantity: "180 kg",
        availableQuantity: "0 kg",
        reservedQuantity: "0 kg",
        quarantineQuantity: "180 kg",
        expiryDate: "2026-05-31",
        qaStatus: "阻擋",
        batchStage: "已入庫",
        relatedWork: ["QC-240506-006"],
        riskTags: ["即期", "隔離"],
        tone: "danger"
      },
      {
        batchNo: "RM240509-CORN",
        batchType: "rawMaterial",
        warehouse: "WH-FZ-A",
        location: "FZ-A04-01",
        quantity: "720 kg",
        availableQuantity: "720 kg",
        reservedQuantity: "0 kg",
        quarantineQuantity: "0 kg",
        expiryDate: "2026-06-08",
        qaStatus: "已放行",
        batchStage: "可領料",
        relatedWork: ["MO-240526-004"],
        riskTags: ["建議優先使用"],
        tone: "warning"
      },
      {
        batchNo: "RM240514-CORN",
        batchType: "rawMaterial",
        warehouse: "WH-FZ-B",
        location: "FZ-B01-04",
        quantity: "360 kg",
        availableQuantity: "0 kg",
        reservedQuantity: "360 kg",
        quarantineQuantity: "0 kg",
        expiryDate: "2026-06-21",
        qaStatus: "已放行",
        batchStage: "已預留",
        relatedWork: ["MO-240526-009"],
        riskTags: ["已預留"],
        tone: "info"
      }
    ]
  },
  {
    itemId: "PK-BAG-010",
    itemName: "耐熱殺菌袋 180g",
    itemType: "包材",
    totalBatchCount: 5,
    warehouseCount: 2,
    totalQuantity: "42,000 pcs",
    availableQuantity: "33,000 pcs",
    reservedQuantity: "9,000 pcs",
    heldQuantity: "0 pcs",
    earliestExpiryDate: "2027-02-12",
    qaHoldBatchCount: 0,
    quarantineBatchCount: 0,
    nearExpiryBatchCount: 0,
    demandImpact: "明日兩張調理包工單共需 12,000 pcs",
    highestRisk: "attention",
    riskLabel: "庫存需追蹤",
    tone: "warning",
    ownerArea: "生管",
    batches: [
      {
        batchNo: "PK240501-BAG",
        batchType: "packaging",
        warehouse: "WH-PK-A",
        location: "PK-A01-01",
        quantity: "18,000 pcs",
        availableQuantity: "18,000 pcs",
        reservedQuantity: "0 pcs",
        quarantineQuantity: "0 pcs",
        expiryDate: "2027-02-12",
        qaStatus: "已放行",
        batchStage: "可領料",
        relatedWork: ["PO-240430-011"],
        riskTags: ["正常可用"],
        tone: "success"
      },
      {
        batchNo: "PK240506-BAG",
        batchType: "packaging",
        warehouse: "WH-PK-A",
        location: "PK-A02-03",
        quantity: "15,000 pcs",
        availableQuantity: "15,000 pcs",
        reservedQuantity: "0 pcs",
        quarantineQuantity: "0 pcs",
        expiryDate: "2027-02-20",
        qaStatus: "已放行",
        batchStage: "可領料",
        relatedWork: ["PO-240505-004"],
        riskTags: ["正常可用"],
        tone: "success"
      },
      {
        batchNo: "PK240516-BAG",
        batchType: "packaging",
        warehouse: "WH-PK-B",
        location: "PK-B01-02",
        quantity: "9,000 pcs",
        availableQuantity: "0 pcs",
        reservedQuantity: "9,000 pcs",
        quarantineQuantity: "0 pcs",
        expiryDate: "2027-03-01",
        qaStatus: "待判定",
        batchStage: "待入庫確認",
        relatedWork: ["QC-240516-008", "MO-240527-002"],
        riskTags: ["待判定", "已預留"],
        tone: "warning"
      }
    ]
  }
];

const batchesDashboardMock: BatchesDashboardData = {
  kpis,
  itemSummaries
};

function itemMatchesSearch(item: BatchItemSummary, query: string) {
  return matchesSupportSearch(
    [
      item.itemId,
      item.itemName,
      item.itemType,
      item.totalQuantity,
      item.availableQuantity,
      item.reservedQuantity,
      item.heldQuantity,
      item.earliestExpiryDate,
      item.demandImpact,
      item.riskLabel,
      item.ownerArea,
      ...item.batches.flatMap((batch) => [
        batch.batchNo,
        batch.batchType,
        batch.warehouse,
        batch.location,
        batch.quantity,
        batch.availableQuantity,
        batch.reservedQuantity,
        batch.quarantineQuantity,
        batch.expiryDate,
        batch.qaStatus,
        batch.batchStage,
        ...batch.relatedWork,
        ...batch.riskTags
      ])
    ],
    query
  );
}

function batchMatchesSearch(batch: BatchDistributionRow, query: string) {
  return matchesSupportSearch(
    [
      batch.batchNo,
      batch.batchType,
      batch.warehouse,
      batch.location,
      batch.quantity,
      batch.availableQuantity,
      batch.reservedQuantity,
      batch.quarantineQuantity,
      batch.expiryDate,
      batch.qaStatus,
      batch.batchStage,
      ...batch.relatedWork,
      ...batch.riskTags
    ],
    query
  );
}

function ItemSummaryRow({
  item,
  isSelected,
  onSelect
}: {
  item: BatchItemSummary;
  isSelected: boolean;
  onSelect: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onSelect}
      className={`w-full rounded-lg border px-4 py-4 text-left transition hover:border-primary/40 hover:bg-primary/5 ${
        isSelected ? "border-primary bg-primary/5 ring-1 ring-primary/20" : "border-border bg-white"
      }`}
    >
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-textSecondary">{item.itemId}</p>
          <h3 className="mt-1 text-lg font-semibold text-textPrimary">{item.itemName}</h3>
          <p className="mt-1 text-sm text-textSecondary">
            {item.itemType} / {item.totalBatchCount} 批 / {item.warehouseCount} 倉
          </p>
        </div>
        <StatusBadge tone={item.tone}>{item.riskLabel}</StatusBadge>
      </div>
      <div className="mt-4 grid gap-3 sm:grid-cols-4">
        <SummaryMetric label="總量" value={item.totalQuantity} />
        <SummaryMetric label="可用" value={item.availableQuantity} />
        <SummaryMetric label="預留" value={item.reservedQuantity} />
        <SummaryMetric label="Hold/隔離" value={item.heldQuantity} />
      </div>
      <div className="mt-4 flex flex-wrap gap-2 text-xs text-textSecondary">
        <span>最早效期 {item.earliestExpiryDate}</span>
        <span>QA Hold {item.qaHoldBatchCount}</span>
        <span>隔離 {item.quarantineBatchCount}</span>
        <span>即期 {item.nearExpiryBatchCount}</span>
      </div>
      <p className="mt-3 text-sm text-textPrimary">{item.demandImpact}</p>
    </button>
  );
}

function SummaryMetric({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs font-medium text-textSecondary">{label}</p>
      <p className="mt-1 text-sm font-semibold text-textPrimary">{value}</p>
    </div>
  );
}

function BatchDistributionRows({
  batches,
  selectedBatchNo,
  onSelect
}: {
  batches: BatchDistributionRow[];
  selectedBatchNo?: string;
  onSelect: (batchNo: string) => void;
}) {
  return (
    <div className="overflow-hidden rounded-lg border border-border">
      <div className="grid grid-cols-[1.05fr_1fr_0.8fr] gap-3 bg-slate-50 px-4 py-3 text-xs font-semibold text-textSecondary md:grid-cols-[1fr_0.9fr_0.9fr_0.8fr_0.8fr]">
        <span>批號</span>
        <span>倉庫/庫位</span>
        <span className="hidden md:block">數量</span>
        <span>QA/階段</span>
        <span className="hidden md:block">效期</span>
      </div>
      <div className="divide-y divide-border">
        {batches.map((batch) => (
          <button
            type="button"
            key={batch.batchNo}
            onClick={() => onSelect(batch.batchNo)}
            className={`grid w-full grid-cols-[1.05fr_1fr_0.8fr] gap-3 px-4 py-3 text-left text-sm transition hover:bg-primary/5 md:grid-cols-[1fr_0.9fr_0.9fr_0.8fr_0.8fr] ${
              selectedBatchNo === batch.batchNo ? "bg-primary/5" : "bg-white"
            }`}
          >
            <span>
              <span className="block font-semibold text-textPrimary">{batch.batchNo}</span>
              <span className="mt-1 block text-xs text-textSecondary">{batch.batchType}</span>
            </span>
            <span>
              <span className="block font-medium text-textPrimary">{batch.warehouse}</span>
              <span className="mt-1 block text-xs text-textSecondary">{batch.location}</span>
            </span>
            <span className="hidden md:block">
              <span className="block font-medium text-textPrimary">{batch.quantity}</span>
              <span className="mt-1 block text-xs text-textSecondary">可用 {batch.availableQuantity}</span>
            </span>
            <span>
              <StatusBadge tone={batch.tone}>{batch.qaStatus}</StatusBadge>
              <span className="mt-2 block text-xs text-textSecondary">{batch.batchStage}</span>
            </span>
            <span className="hidden text-textPrimary md:block">{batch.expiryDate}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

function SelectedBatchDetail({ item, batch }: { item: BatchItemSummary; batch?: BatchDistributionRow }) {
  if (!batch) {
    return <SupportEmptyState title="尚未選擇批號" description="請先選擇品項與批號，檢視目前營運狀態。" />;
  }

  return (
    <article className="rounded-card border border-border bg-white p-5 shadow-card">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-textSecondary">{item.itemId}</p>
          <h3 className="mt-1 text-xl font-semibold text-textPrimary">{batch.batchNo}</h3>
          <p className="mt-1 text-sm text-textSecondary">{item.itemName}</p>
        </div>
        <StatusBadge tone={batch.tone}>{batch.qaStatus}</StatusBadge>
      </div>
      <dl className="mt-5 grid gap-4 sm:grid-cols-2">
        <DetailMetric label="倉庫/庫位" value={`${batch.warehouse} / ${batch.location}`} />
        <DetailMetric label="批號階段" value={batch.batchStage} />
        <DetailMetric label="總量" value={batch.quantity} />
        <DetailMetric label="可用量" value={batch.availableQuantity} />
        <DetailMetric label="預留量" value={batch.reservedQuantity} />
        <DetailMetric label="隔離量" value={batch.quarantineQuantity} />
        <DetailMetric label="有效日期" value={batch.expiryDate} />
        <DetailMetric label="下一檢視單位" value={item.ownerArea} />
      </dl>
      <div className="mt-5">
        <p className="text-xs font-semibold uppercase tracking-wide text-textSecondary">風險標籤</p>
        <div className="mt-2 flex flex-wrap gap-2">
          {batch.riskTags.map((tag) => (
            <StatusBadge key={tag} tone={batch.tone}>
              {tag}
            </StatusBadge>
          ))}
        </div>
      </div>
      <div className="mt-5">
        <p className="text-xs font-semibold uppercase tracking-wide text-textSecondary">關聯工作</p>
        <div className="mt-2 flex flex-wrap gap-2">
          {batch.relatedWork.map((work) => (
            <span key={work} className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-700">
              {work}
            </span>
          ))}
        </div>
      </div>
      <p className="mt-5 rounded-lg bg-slate-50 px-3 py-3 text-sm text-textPrimary">{item.demandImpact}</p>
    </article>
  );
}

function DetailMetric({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-xs font-medium text-textSecondary">{label}</dt>
      <dd className="mt-1 text-sm font-semibold text-textPrimary">{value}</dd>
    </div>
  );
}

export default function BatchesPage() {
  const { data, error, isLoading, source } = useSupportDashboard(
    "/api/v1/batches/dashboard",
    batchesDashboardMock,
    "Batches API unavailable"
  );
  const [searchValue, setSearchValue] = useState("");
  const [selectedItemId, setSelectedItemId] = useState(itemSummaries[0]?.itemId ?? "");
  const [selectedBatchNo, setSelectedBatchNo] = useState(itemSummaries[0]?.batches[0]?.batchNo ?? "");
  const searchQuery = normalizeSupportSearch(searchValue);
  const filteredItems = useMemo(
    () => data.itemSummaries.filter((item) => itemMatchesSearch(item, searchQuery)),
    [data.itemSummaries, searchQuery]
  );
  const selectedItem = useMemo(
    () => filteredItems.find((item) => item.itemId === selectedItemId) ?? filteredItems[0],
    [filteredItems, selectedItemId]
  );
  const filteredBatches = useMemo(() => {
    if (!selectedItem) {
      return [];
    }

    return selectedItem.batches.filter((batch) => batchMatchesSearch(batch, searchQuery));
  }, [searchQuery, selectedItem]);
  const selectedBatch = useMemo(
    () => filteredBatches.find((batch) => batch.batchNo === selectedBatchNo) ?? filteredBatches[0],
    [filteredBatches, selectedBatchNo]
  );

  return (
    <AppLayout activePath="/batches" title="批號中心 Batch Module">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="Batches V1.1 Operations"
          title="品項批號分布與營運狀態"
          description="以品項為第一層彙總多批號、多倉庫與多庫位狀態，快速判斷可用量、預留量、QA Hold、隔離與即期風險。"
          metrics={[
            { label: "品項", value: "86", icon: Barcode },
            { label: "即期", value: "3", icon: CalendarClock },
            { label: "分布", value: "5 倉", icon: Network }
          ]}
        />
        <div className="flex flex-wrap gap-2">
          <StatusBadge tone={source === "api" ? "success" : "warning"}>
            {source === "api" ? "API data" : "Mock fallback"}
          </StatusBadge>
          {isLoading ? <StatusBadge tone="info">Loading API</StatusBadge> : null}
          <StatusBadge tone="neutral">Read-only</StatusBadge>
        </div>
        {error ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Batches API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}
        <SupportSearchPanel
          ariaLabel="搜尋品項、批號、倉庫、庫位、QA 狀態或關聯工作"
          placeholder="品項 / 批號 / 倉庫 / 庫位 / QA / 工單"
          value={searchValue}
          onChange={setSearchValue}
        />
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {data.kpis.map((item) => (
            <ModuleKpiCard {...item} key={item.label} />
          ))}
        </section>
        <section className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_560px]">
          <article className="rounded-card border border-border bg-white p-5 shadow-card">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="text-sm font-medium text-textSecondary">Item Batch Summary</p>
                <h2 className="mt-1 text-xl font-semibold text-textPrimary">品項批號總覽</h2>
              </div>
              <StatusBadge tone="info">{filteredItems.length} 項</StatusBadge>
            </div>
            <div className="mt-5 grid gap-3">
              {filteredItems.length > 0 ? (
                filteredItems.map((item) => (
                  <ItemSummaryRow
                    key={item.itemId}
                    item={item}
                    isSelected={selectedItem?.itemId === item.itemId}
                    onSelect={() => {
                      setSelectedItemId(item.itemId);
                      setSelectedBatchNo(item.batches[0]?.batchNo ?? "");
                    }}
                  />
                ))
              ) : (
                <SupportEmptyState
                  title="沒有符合條件的品項批號"
                  description="請調整搜尋關鍵字，或確認該品項是否已啟用批號管理。"
                />
              )}
            </div>
          </article>
          <div className="space-y-6">
            <article className="rounded-card border border-border bg-white p-5 shadow-card">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p className="text-sm font-medium text-textSecondary">Batch Distribution</p>
                  <h2 className="mt-1 text-xl font-semibold text-textPrimary">
                    {selectedItem ? selectedItem.itemName : "批號分布"}
                  </h2>
                </div>
                {selectedItem ? <StatusBadge tone={selectedItem.tone}>{selectedItem.ownerArea}</StatusBadge> : null}
              </div>
              <div className="mt-5">
                {selectedItem && filteredBatches.length > 0 ? (
                  <BatchDistributionRows
                    batches={filteredBatches}
                    selectedBatchNo={selectedBatch?.batchNo}
                    onSelect={setSelectedBatchNo}
                  />
                ) : (
                  <SupportEmptyState
                    title="沒有符合條件的批號分布"
                    description="請調整搜尋條件，或確認此品項是否已有倉庫與庫位資料。"
                  />
                )}
              </div>
            </article>
            {selectedItem ? (
              <SelectedBatchDetail item={selectedItem} batch={selectedBatch} />
            ) : (
              <SupportEmptyState title="尚未選擇品項" description="請先從左側選擇品項，檢視批號分布與營運明細。" />
            )}
          </div>
        </section>
      </div>
    </AppLayout>
  );
}
