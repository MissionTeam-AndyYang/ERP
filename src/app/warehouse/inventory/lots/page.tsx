"use client";

import {
  AlertTriangle,
  ArrowLeft,
  ClipboardList,
  Filter,
  Layers3,
  PackageCheck,
  PackageSearch,
  Search
} from "lucide-react";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { DataSourceToggle, type DataSourceMode } from "@/components/common/data-source-toggle";
import { StatusBadge } from "@/components/ui/status-badge";
import { AppLayout } from "@/layouts/app-layout";
import {
  getWarehouseInventoryLotDetail,
  getWarehouseInventoryLots,
  type WarehouseInventoryLotsQuery
} from "@/services/warehouse-api";
import type {
  WarehouseDataSource,
  WarehouseInventoryLot,
  WarehouseInventoryLotDetail,
  WarehouseInventoryLotListData
} from "@/types/warehouse";

const emptyLotList: WarehouseInventoryLotListData = {
  summary: {
    lotCount: 0,
    itemCount: 0,
    totalQuantity: 0,
    totalInventoryValue: 0,
    totalAvailableQuantity: 0,
    totalAvailableValue: 0,
    riskLotCount: 0,
    pendingTaskCount: 0
  },
  lots: [],
  total: 0,
  count: 0,
  start: 0
};

const availabilityOptions: Array<{ label: string; value: WarehouseInventoryLotsQuery["availability"] | "all" }> = [
  { label: "全部", value: "all" },
  { label: "可用", value: "available" },
  { label: "已預留", value: "reserved" },
  { label: "品檢保留", value: "quality_hold" },
  { label: "阻塞", value: "blocked" }
];

const sortOptions: Array<{ label: string; value: NonNullable<WarehouseInventoryLotsQuery["sort"]> }> = [
  { label: "庫存價值", value: "inventoryValue" },
  { label: "可用數量", value: "availableQuantity" },
  { label: "效期", value: "validDate" },
  { label: "庫存天數", value: "daysInStock" }
];

function formatNumber(value: number) {
  return new Intl.NumberFormat("zh-TW", { maximumFractionDigits: 2 }).format(value);
}

function formatMoney(value: number) {
  return `$${new Intl.NumberFormat("zh-TW", { maximumFractionDigits: 0 }).format(value)}`;
}

function SummaryCard({
  label,
  value,
  hint,
  tone
}: {
  label: string;
  value: string;
  hint: string;
  tone: "success" | "warning" | "danger" | "info";
}) {
  return (
    <div className="rounded-lg border border-border bg-white p-4 shadow-card">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-textSecondary">{label}</p>
          <p className="mt-2 text-2xl font-semibold text-textPrimary">{value}</p>
        </div>
        <StatusBadge tone={tone}>{label}</StatusBadge>
      </div>
      <p className="mt-3 text-xs leading-5 text-textSecondary">{hint}</p>
    </div>
  );
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="rounded-lg border border-dashed border-border bg-white px-4 py-8 text-center text-sm text-textSecondary">
      {message}
    </div>
  );
}

function LotTable({
  lots,
  onSelect,
  selectedKey
}: {
  lots: WarehouseInventoryLot[];
  onSelect: (lot: WarehouseInventoryLot) => void;
  selectedKey: string;
}) {
  if (!lots.length) {
    return <EmptyState message="目前沒有符合條件的庫存批號。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[1120px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">批號 / 品項</th>
              <th className="px-4 py-3">倉庫</th>
              <th className="px-4 py-3 text-right">現有 / 預留 / 可用</th>
              <th className="px-4 py-3 text-right">庫存價值</th>
              <th className="px-4 py-3 text-right">板數</th>
              <th className="px-4 py-3">來源</th>
              <th className="px-4 py-3">效期 / 庫齡</th>
              <th className="px-4 py-3">風險</th>
              <th className="px-4 py-3 text-right">任務</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {lots.map((lot) => {
              const isSelected = lot.lotKey === selectedKey;
              return (
                <tr
                  className={`cursor-pointer transition ${isSelected ? "bg-info/10" : "hover:bg-slate-50"}`}
                  key={lot.lotKey}
                  onClick={() => onSelect(lot)}
                >
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{lot.batchNo}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {lot.itemNo} · {lot.itemName} · {lot.category}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{lot.warehouseName || lot.warehouseNo}</p>
                    <p className="mt-1 text-xs text-textSecondary">{lot.warehouseNo}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(lot.currentQuantity)} / {formatNumber(lot.reservedQuantity)} /{" "}
                    {formatNumber(lot.availableQuantity)} {lot.unit}
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatMoney(lot.inventoryValue)}</td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatNumber(lot.palletCount)}</td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{lot.refCategoryLabel}</p>
                    <p className="mt-1 text-xs text-textSecondary">{lot.refNo || "無來源單號"}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{lot.validDate || "未提供效期"}</p>
                    <p className="mt-1 text-xs text-textSecondary">庫存 {formatNumber(lot.daysInStock)} 天</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={lot.riskTone}>{lot.riskLabel}</StatusBadge>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(lot.openTaskCount)}
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

function DetailPanel({
  detail,
  isLoading
}: {
  detail?: WarehouseInventoryLotDetail;
  isLoading: boolean;
}) {
  if (isLoading) {
    return <EmptyState message="正在載入批號追蹤資料。" />;
  }
  if (!detail) {
    return <EmptyState message="請選取左側批號以查看追蹤明細。" />;
  }

  const { lot } = detail;

  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">庫存批號追蹤</p>
          <h2 className="mt-1 truncate text-lg font-semibold text-textPrimary">{lot.batchNo}</h2>
          <p className="mt-1 text-sm text-textSecondary">{lot.itemName}</p>
        </div>
        <StatusBadge tone={lot.riskTone}>{lot.riskLabel}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">現有 / 可用</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(lot.currentQuantity)} / {formatNumber(lot.availableQuantity)} {lot.unit}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">庫存 / 可用價值</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(lot.inventoryValue)}</p>
          <p className="mt-1 text-xs text-textSecondary">{formatMoney(lot.availableValue)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">預留 / 品檢</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(lot.reservedQuantity)} / {formatNumber(lot.qualityHoldQuantity)} {lot.unit}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">板數 / 任務</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(lot.palletCount)} / {formatNumber(lot.openTaskCount)}
          </p>
        </div>
      </div>

      <section className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">庫存入出紀錄</p>
        {detail.inventoryRecords.length ? (
          detail.inventoryRecords.map((record) => (
            <div className="rounded-md border border-border px-3 py-2" key={record.id}>
              <div className="flex items-center justify-between gap-2">
                <StatusBadge tone={record.tone}>{record.categoryLabel}</StatusBadge>
                <p className="text-xs text-textSecondary">{record.date}</p>
              </div>
              <p className="mt-2 text-sm font-medium text-textPrimary">{record.refNo || record.refCategoryLabel}</p>
              <p className="mt-1 text-xs text-textSecondary">
                {formatNumber(record.quantity)} {lot.unit} · {formatMoney(record.amount)}
              </p>
            </div>
          ))
        ) : (
          <EmptyState message="尚無入出庫紀錄。" />
        )}
      </section>

      <section className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">預留與品檢</p>
        {[...detail.reservations, ...detail.qualityHolds].length ? (
          <>
            {detail.reservations.map((reservation) => (
              <div className="rounded-md border border-border px-3 py-2" key={reservation.id}>
                <div className="flex items-center justify-between gap-2">
                  <p className="text-sm font-medium text-textPrimary">{reservation.reservationNo || "預留"}</p>
                  <StatusBadge tone={reservation.tone}>{reservation.status}</StatusBadge>
                </div>
                <p className="mt-1 text-xs text-textSecondary">
                  {reservation.refCategoryLabel} · {reservation.refNo || "無來源單號"} ·{" "}
                  {formatNumber(reservation.reservedQuantity)} {lot.unit}
                </p>
              </div>
            ))}
            {detail.qualityHolds.map((hold) => (
              <div className="rounded-md border border-border px-3 py-2" key={hold.id}>
                <div className="flex items-center justify-between gap-2">
                  <p className="text-sm font-medium text-textPrimary">{hold.holdNo || "品檢保留"}</p>
                  <StatusBadge tone={hold.tone}>{hold.status}</StatusBadge>
                </div>
                <p className="mt-1 text-xs text-textSecondary">
                  {hold.reason || "待品保確認"} · {formatNumber(hold.holdQuantity)} {lot.unit}
                </p>
              </div>
            ))}
          </>
        ) : (
          <EmptyState message="尚無預留或品檢保留。" />
        )}
      </section>

      <section className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">板位與未完成任務</p>
        {detail.palletMovements.map((movement) => (
          <div className="rounded-md border border-border px-3 py-2" key={movement.id}>
            <div className="flex items-center justify-between gap-2">
              <p className="text-sm font-medium text-textPrimary">{movement.palletGroupNo || movement.movementNo}</p>
              <StatusBadge tone={movement.tone}>{movement.refCategoryLabel}</StatusBadge>
            </div>
            <p className="mt-1 text-xs text-textSecondary">
              {formatNumber(movement.palletCount)} 板 · {movement.refNo || "無來源單號"}
            </p>
          </div>
        ))}
        {detail.workflowTasks.map((task) => (
          <div className="rounded-md border border-border px-3 py-2" key={task.id}>
            <div className="flex items-center justify-between gap-2">
              <p className="text-sm font-medium text-textPrimary">{task.taskId || task.taskTypeLabel}</p>
              <StatusBadge tone={task.tone}>{task.taskStatusLabel}</StatusBadge>
            </div>
            <p className="mt-1 text-xs text-textSecondary">
              {task.taskTypeLabel} · {task.ownerDepartmentLabel} · 剩餘 {formatNumber(task.remainingQuantity)} {lot.unit}
            </p>
          </div>
        ))}
      </section>
    </aside>
  );
}

export default function WarehouseInventoryLotsPage() {
  const [dataSourceMode, setDataSourceMode] = useState<DataSourceMode>("api");
  const [data, setData] = useState<WarehouseInventoryLotListData>(emptyLotList);
  const [detail, setDetail] = useState<WarehouseInventoryLotDetail | undefined>();
  const [selectedLot, setSelectedLot] = useState<WarehouseInventoryLot | undefined>();
  const [source, setSource] = useState<WarehouseDataSource>("mock");
  const [error, setError] = useState<string | undefined>();
  const [detailError, setDetailError] = useState<string | undefined>();
  const [isLoading, setIsLoading] = useState(true);
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const [keyword, setKeyword] = useState("");
  const [availability, setAvailability] = useState<(typeof availabilityOptions)[number]["value"]>("all");
  const [sort, setSort] = useState<NonNullable<WarehouseInventoryLotsQuery["sort"]>>("inventoryValue");
  const [order, setOrder] = useState<NonNullable<WarehouseInventoryLotsQuery["order"]>>("desc");

  const query = useMemo<WarehouseInventoryLotsQuery>(
    () => ({
      keyword: keyword.trim() || undefined,
      availability: availability === "all" ? undefined : availability,
      sort,
      order,
      count: 50
    }),
    [availability, keyword, order, sort]
  );

  useEffect(() => {
    let isMounted = true;

    getWarehouseInventoryLots(query, dataSourceMode).then((result) => {
      if (!isMounted) {
        return;
      }
      setData(result.data);
      setSource(result.source);
      setError(result.error);
      setSelectedLot(result.data.lots[0]);
      if (!result.data.lots[0]) {
        setDetail(undefined);
        setIsDetailLoading(false);
      }
      setIsLoading(false);
    });

    return () => {
      isMounted = false;
    };
  }, [dataSourceMode, query]);

  useEffect(() => {
    if (!selectedLot) {
      return;
    }

    let isMounted = true;

    getWarehouseInventoryLotDetail(selectedLot, dataSourceMode).then((result) => {
      if (!isMounted) {
        return;
      }
      setDetail(result.detail);
      setDetailError(result.error);
      setIsDetailLoading(false);
    });

    return () => {
      isMounted = false;
    };
  }, [dataSourceMode, selectedLot]);

  function handleSelectLot(lot: WarehouseInventoryLot) {
    setSelectedLot(lot);
    setIsDetailLoading(true);
  }

  return (
    <AppLayout activePath="/warehouse" title="庫存批號明細清單">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">WarehouseInventoryLotListScreen</StatusBadge>
                <StatusBadge tone={source === "api" ? "success" : "warning"}>
                  {source === "api" ? "API data" : "Mock fallback"}
                </StatusBadge>
                {isLoading ? <StatusBadge tone="info">Loading API</StatusBadge> : null}
                <DataSourceToggle value={dataSourceMode} onChange={setDataSourceMode} />
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">庫存批號明細清單</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                以批號、倉庫、料品與可用狀態檢視庫存明細，並從右側追蹤面板確認入出庫紀錄、預留、品檢、板位與未完成任務。
              </p>
            </div>
            <Link
              className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary"
              href="/warehouse"
            >
              <ArrowLeft className="h-4 w-4" aria-hidden="true" />
              返回倉庫中心
            </Link>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Inventory lots API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}
        {detailError ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Inventory lot detail API 尚未可用，已使用 mock fallback。{detailError}
          </p>
        ) : null}

        <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          <SummaryCard
            hint={`${formatNumber(data.summary.itemCount)} 個品項，${formatNumber(data.total)} 筆符合條件`}
            label="批號列數"
            tone="info"
            value={formatNumber(data.summary.lotCount)}
          />
          <SummaryCard
            hint={`可用 ${formatMoney(data.summary.totalAvailableValue)}`}
            label="庫存價值"
            tone="success"
            value={formatMoney(data.summary.totalInventoryValue)}
          />
          <SummaryCard
            hint={`${formatNumber(data.summary.totalAvailableQuantity)} 可用數量`}
            label="目前數量"
            tone="info"
            value={formatNumber(data.summary.totalQuantity)}
          />
          <SummaryCard
            hint={`未完成任務 ${formatNumber(data.summary.pendingTaskCount)}`}
            label="風險批號"
            tone={data.summary.riskLotCount ? "warning" : "success"}
            value={formatNumber(data.summary.riskLotCount)}
          />
        </section>

        <section className="rounded-lg border border-border bg-white p-3 shadow-card">
          <div className="grid gap-3 xl:grid-cols-[minmax(260px,1fr)_auto_auto_auto]">
            <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
              <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
              <input
                aria-label="搜尋料號、品名、批號、來源單號或倉庫"
                className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                onChange={(event) => setKeyword(event.target.value)}
                placeholder="料號 / 品名 / 批號 / 來源 / 倉庫"
                value={keyword}
              />
            </label>

            <div className="flex flex-wrap gap-2">
              {availabilityOptions.map((option) => (
                <button
                  className={`h-10 rounded-button px-3 text-sm font-medium ${
                    availability === option.value
                      ? "bg-primary text-white"
                      : "bg-slate-100 text-textSecondary hover:bg-slate-200"
                  }`}
                  key={option.value}
                  onClick={() => setAvailability(option.value)}
                  type="button"
                >
                  {option.label}
                </button>
              ))}
            </div>

            <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
              <Filter className="h-4 w-4 text-textSecondary" aria-hidden="true" />
              <select
                className="bg-transparent text-sm outline-none"
                onChange={(event) => setSort(event.target.value as NonNullable<WarehouseInventoryLotsQuery["sort"]>)}
                value={sort}
              >
                {sortOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>

            <button
              className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary"
              onClick={() => setOrder((current) => (current === "desc" ? "asc" : "desc"))}
              type="button"
            >
              {order === "desc" ? "降冪" : "升冪"}
            </button>
          </div>
        </section>

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_420px]">
          <div className="min-w-0 space-y-3">
            <div className="grid gap-3 md:grid-cols-3">
              <div className="rounded-lg border border-border bg-white p-4 shadow-card">
                <PackageSearch className="h-5 w-5 text-textSecondary" aria-hidden="true" />
                <p className="mt-2 text-sm font-semibold text-textPrimary">清單篩選</p>
                <p className="mt-1 text-xs leading-5 text-textSecondary">依 API query 取得批號明細，不使用 dashboard 明細列。</p>
              </div>
              <div className="rounded-lg border border-border bg-white p-4 shadow-card">
                <Layers3 className="h-5 w-5 text-textSecondary" aria-hidden="true" />
                <p className="mt-2 text-sm font-semibold text-textPrimary">批號層級</p>
                <p className="mt-1 text-xs leading-5 text-textSecondary">以 warehouseNo、itemNo、batchNo 作為 detail API path。</p>
              </div>
              <div className="rounded-lg border border-border bg-white p-4 shadow-card">
                <ClipboardList className="h-5 w-5 text-textSecondary" aria-hidden="true" />
                <p className="mt-2 text-sm font-semibold text-textPrimary">追蹤資料</p>
                <p className="mt-1 text-xs leading-5 text-textSecondary">點選批號後載入入出庫、預留、品檢、板位與任務資料。</p>
              </div>
            </div>

            {isLoading ? (
              <EmptyState message="正在載入庫存批號清單。" />
            ) : (
              <LotTable lots={data.lots} onSelect={handleSelectLot} selectedKey={selectedLot?.lotKey ?? ""} />
            )}
          </div>

          <DetailPanel detail={detail} isLoading={isDetailLoading} />
        </section>
      </div>
    </AppLayout>
  );
}
