"use client";

import {
  AlertTriangle,
  ArrowLeft,
  CalendarClock,
  ClipboardList,
  Filter,
  ListChecks,
  PackageSearch,
  Search,
  ShieldAlert,
  TimerReset
} from "lucide-react";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { DataSourceToggle, type DataSourceMode } from "@/components/common/data-source-toggle";
import { StatusBadge } from "@/components/ui/status-badge";
import { useLanguage } from "@/i18n/language-provider";
import {
  warehouseEnumLabel,
  warehouseLaneTone,
  warehouseRiskTone,
  warehouseTaskStatusTone
} from "@/i18n/warehouse-enums";
import { AppLayout } from "@/layouts/app-layout";
import {
  getWarehouseTaskDetail,
  getWarehouseTaskWorkbench,
  type WarehouseTaskWorkbenchQuery
} from "@/services/warehouse-api";
import type {
  WarehouseDataSource,
  WarehouseTaskDetail,
  WarehouseTaskWorkbenchData,
  WarehouseTaskWorkbenchItem,
  WarehouseTaskWorkbenchLane
} from "@/types/warehouse";

const emptyWorkbench: WarehouseTaskWorkbenchData = {
  serverDate: "",
  range: {
    mode: "today",
    startDate: "",
    endDate: ""
  },
  summary: {
    openTaskCount: 0,
    overdueTaskCount: 0,
    blockedTaskCount: 0,
    inboundTaskCount: 0,
    outboundTaskCount: 0,
    qualityTaskCount: 0,
    shipmentTaskCount: 0,
    inventoryShortageTaskCount: 0
  },
  lanes: [],
  tasks: [],
  total: 0,
  count: 0,
  start: 0
};

const dateRangeOptions: Array<{ label: string; value: NonNullable<WarehouseTaskWorkbenchQuery["dateRange"]> }> = [
  { label: "今日", value: "today" },
  { label: "近 7 日", value: "next_7_days" },
  { label: "逾期", value: "overdue" },
  { label: "全部未完成", value: "all_open" }
];

const taskTypeOptions: Array<{ label: string; value: number | "all" }> = [
  { label: "全部", value: "all" },
  { label: "進貨", value: 3 },
  { label: "入庫", value: 4 },
  { label: "出庫", value: 5 },
  { label: "移倉", value: 6 },
  { label: "品檢", value: 8 },
  { label: "出貨", value: 9 }
];

const sortOptions: Array<{ label: string; value: NonNullable<WarehouseTaskWorkbenchQuery["sort"]> }> = [
  { label: "到期時間", value: "dueTimestamp" },
  { label: "任務類型", value: "taskType" },
  { label: "剩餘數量", value: "remainingQuantity" },
  { label: "風險等級", value: "riskLevel" }
];

function formatNumber(value: number, language: string) {
  return new Intl.NumberFormat(language, { maximumFractionDigits: 2 }).format(value);
}

function formatMoney(value: number, language: string) {
  return `$${new Intl.NumberFormat(language, { maximumFractionDigits: 0 }).format(value)}`;
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="rounded-lg border border-dashed border-border bg-white px-4 py-8 text-center text-sm text-textSecondary">
      {message}
    </div>
  );
}

function SummaryCard({
  icon: Icon,
  label,
  value,
  hint,
  tone
}: {
  icon: typeof ClipboardList;
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
        <span className="grid h-10 w-10 place-items-center rounded-full bg-slate-100 text-textSecondary">
          <Icon className="h-5 w-5" aria-hidden="true" />
        </span>
      </div>
      <p className="mt-3 text-xs leading-5 text-textSecondary">{hint}</p>
      <div className="mt-3">
        <StatusBadge tone={tone}>{label}</StatusBadge>
      </div>
    </div>
  );
}

function LaneCard({
  lane,
  isActive,
  onSelect
}: {
  lane: WarehouseTaskWorkbenchLane;
  isActive: boolean;
  onSelect: (laneCode: string) => void;
}) {
  const { language } = useLanguage();
  return (
    <button
      className={`rounded-lg border p-4 text-left shadow-card transition ${
        isActive ? "border-primary bg-primary/5" : "border-border bg-white hover:bg-slate-50"
      }`}
      onClick={() => onSelect(lane.laneCode)}
      type="button"
    >
      <div className="flex items-center justify-between gap-3">
        <StatusBadge tone={warehouseLaneTone(lane.laneCode)}>
          {warehouseEnumLabel("laneCode", lane.laneCode, language)}
        </StatusBadge>
        <p className="text-xl font-semibold text-textPrimary">{lane.taskCount}</p>
      </div>
      <p className="mt-3 text-xs text-textSecondary">
        {lane.riskCount > 0 ? `${lane.riskCount} risk tasks` : "No risk tasks"}
      </p>
    </button>
  );
}

function taskMatchesLane(task: WarehouseTaskWorkbenchItem, laneCode: string) {
  if (laneCode === "all") {
    return true;
  }
  if (task.taskStatus === 4 || task.riskTypes.includes("BLOCKED")) {
    return laneCode === "blocked";
  }
  if (task.taskType === 3 || task.taskType === 4) {
    return laneCode === "inbound";
  }
  if (task.taskType === 8) {
    return laneCode === "quality";
  }
  if (task.taskType === 9) {
    return laneCode === "shipment";
  }
  return laneCode === "outbound";
}

function TaskTable({
  tasks,
  selectedTaskId,
  onSelect
}: {
  tasks: WarehouseTaskWorkbenchItem[];
  selectedTaskId: string;
  onSelect: (task: WarehouseTaskWorkbenchItem) => void;
}) {
  const { language } = useLanguage();

  if (!tasks.length) {
    return <EmptyState message="目前沒有符合條件的倉庫任務。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[1160px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">任務 / 狀態</th>
              <th className="px-4 py-3">品項 / 批號</th>
              <th className="px-4 py-3">來源</th>
              <th className="px-4 py-3">倉庫</th>
              <th className="px-4 py-3 text-right">預計 / 已處理 / 剩餘</th>
              <th className="px-4 py-3 text-right">可用 / 預留 / 品檢</th>
              <th className="px-4 py-3">到期 / 負責</th>
              <th className="px-4 py-3">風險</th>
              <th className="px-4 py-3">下一步</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {tasks.map((task) => {
              const isSelected = task.taskId === selectedTaskId;
              const riskTone = warehouseRiskTone(task.riskLevel, task.riskTypes);
              return (
                <tr
                  className={`cursor-pointer transition ${isSelected ? "bg-info/10" : "hover:bg-slate-50"}`}
                  key={task.taskId}
                  onClick={() => onSelect(task)}
                >
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{task.taskId}</p>
                    <div className="mt-2 flex flex-wrap gap-2">
                      <StatusBadge tone={riskTone}>{warehouseEnumLabel("taskType", task.taskType, language)}</StatusBadge>
                      <StatusBadge tone={warehouseTaskStatusTone(task.taskStatus)}>
                        {warehouseEnumLabel("taskStatus", task.taskStatus, language)}
                      </StatusBadge>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{task.itemName || task.itemNo}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {task.itemNo || "無料號"} · {task.batchNo || "未指定批號"}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{warehouseEnumLabel("refCategory", task.refCategory, language)}</p>
                    <p className="mt-1 text-xs text-textSecondary">{task.refNo || "無來源單號"}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{task.warehouseName || task.warehouseNo}</p>
                    <p className="mt-1 text-xs text-textSecondary">{task.warehouseNo}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(task.expectedQuantity, language)} / {formatNumber(task.processedQuantity, language)} /{" "}
                    {formatNumber(task.remainingQuantity, language)}{" "}
                    {warehouseEnumLabel("unit", task.unit, language)}
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">
                    {formatNumber(task.availableQuantity, language)} / {formatNumber(task.reservedQuantity, language)} /{" "}
                    {formatNumber(task.qualityHoldQuantity, language)}
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{task.dueDate || "未提供"}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {warehouseEnumLabel("department", task.ownerDepartment, language)}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={riskTone}>
                      {task.riskTypes.length
                        ? task.riskTypes.map((risk) => warehouseEnumLabel("riskType", risk, language)).join(" / ")
                        : warehouseEnumLabel("riskLevel", task.riskLevel, language)}
                    </StatusBadge>
                    {task.blockReason ? <p className="mt-2 text-xs text-danger">{task.blockReason}</p> : null}
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-sm font-medium text-textPrimary">
                      {warehouseEnumLabel("nextActionCode", task.nextActionCode, language)}
                    </p>
                    <p className="mt-1 text-xs text-textSecondary">{formatMoney(task.inventoryValue, language)}</p>
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

function DetailPanel({ detail, isLoading }: { detail?: WarehouseTaskDetail; isLoading: boolean }) {
  const { language } = useLanguage();

  if (isLoading) {
    return <EmptyState message="正在載入任務追蹤資料。" />;
  }
  if (!detail) {
    return <EmptyState message="請選取左側任務，以查看任務追蹤面板。" />;
  }

  const riskTone = warehouseRiskTone(detail.task.riskLevel, detail.task.riskTypes);

  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">WarehouseTaskDetailPanel</p>
          <h2 className="mt-1 truncate text-lg font-semibold text-textPrimary">{detail.task.taskId}</h2>
          <p className="mt-1 text-sm text-textSecondary">{detail.quantity.itemName || detail.quantity.itemNo}</p>
        </div>
        <StatusBadge tone={riskTone}>{warehouseEnumLabel("taskType", detail.task.taskType, language)}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">任務狀態</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {warehouseEnumLabel("taskStatus", detail.task.taskStatus, language)}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">下一步</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {warehouseEnumLabel("nextActionCode", detail.task.nextActionCode, language)}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">剩餘 / 可用</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(detail.quantity.remainingQuantity, language)} /{" "}
            {formatNumber(detail.quantity.availableQuantity, language)}{" "}
            {warehouseEnumLabel("unit", detail.quantity.unit, language)}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">預留 / 品檢</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(detail.quantity.reservedQuantity, language)} /{" "}
            {formatNumber(detail.quantity.qualityHoldQuantity, language)}
          </p>
        </div>
      </div>

      {detail.task.blockReason ? (
        <div className="rounded-md border border-danger/20 bg-danger/10 p-3 text-sm text-danger">
          {detail.task.blockReason}
        </div>
      ) : null}

      <section className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">主任務來源</p>
        {detail.sourceRefs.length ? (
          detail.sourceRefs.map((source) => (
            <div className="rounded-md border border-border px-3 py-2" key={`${source.refCategory}-${source.refNo}`}>
              <p className="text-sm font-medium text-textPrimary">
                {warehouseEnumLabel("refCategory", source.refCategory, language)}
              </p>
              <p className="mt-1 text-xs text-textSecondary">
                {source.refNo || "無來源單號"} {source.refSubNo ? `· ${source.refSubNo}` : ""}
              </p>
            </div>
          ))
        ) : (
          <EmptyState message="尚無來源單據資料。" />
        )}
      </section>

      <section className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">相關批號</p>
        {detail.relatedLots.length ? (
          detail.relatedLots.map((lot) => (
            <div className="rounded-md border border-border px-3 py-2" key={lot.lotKey}>
              <div className="flex items-center justify-between gap-2">
                <p className="text-sm font-medium text-textPrimary">{lot.batchNo || "未指定批號"}</p>
                <StatusBadge tone={warehouseRiskTone(undefined, lot.riskTypes)}>
                  {lot.riskTypes.length
                    ? lot.riskTypes.map((risk) => warehouseEnumLabel("riskType", risk, language)).join(" / ")
                    : "OK"}
                </StatusBadge>
              </div>
              <p className="mt-1 text-xs text-textSecondary">
                {lot.itemNo} · 可用 {formatNumber(lot.availableQuantity, language)} · 品檢{" "}
                {formatNumber(lot.qualityHoldQuantity, language)}
              </p>
            </div>
          ))
        ) : (
          <EmptyState message="尚無相關批號資料。" />
        )}
      </section>

      <section className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">任務時間線</p>
        {detail.timeline.length ? (
          detail.timeline.map((event, index) => (
            <div className="flex gap-3" key={event.id}>
              <div className="flex flex-col items-center">
                <span className="grid h-6 w-6 place-items-center rounded-full bg-primary text-xs font-bold text-white">
                  {index + 1}
                </span>
                {index < detail.timeline.length - 1 ? <span className="h-8 w-px bg-border" /> : null}
              </div>
              <div className="min-w-0 pb-3">
                <div className="flex flex-wrap items-center gap-2">
                  <p className="font-medium text-textPrimary">
                    {warehouseEnumLabel("eventCode", event.eventCode, language)}
                  </p>
                  <StatusBadge tone={warehouseTaskStatusTone(event.status)}>
                    {warehouseEnumLabel("taskStatus", event.status, language)}
                  </StatusBadge>
                </div>
                <p className="mt-1 text-xs text-textSecondary">
                  {event.eventDate || "未提供時間"} · {warehouseEnumLabel("department", event.department, language)}
                </p>
                {event.comment ? <p className="mt-1 text-xs text-textSecondary">{event.comment}</p> : null}
              </div>
            </div>
          ))
        ) : (
          <EmptyState message="尚無任務歷史事件，API 可先回傳空陣列。" />
        )}
      </section>
    </aside>
  );
}

export default function WarehouseTaskWorkbenchPage() {
  const { language } = useLanguage();
  const [dataSourceMode, setDataSourceMode] = useState<DataSourceMode>("api");
  const [data, setData] = useState<WarehouseTaskWorkbenchData>(emptyWorkbench);
  const [source, setSource] = useState<WarehouseDataSource>("mock");
  const [error, setError] = useState<string | undefined>();
  const [detail, setDetail] = useState<WarehouseTaskDetail | undefined>();
  const [detailError, setDetailError] = useState<string | undefined>();
  const [isLoading, setIsLoading] = useState(true);
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const [keyword, setKeyword] = useState("");
  const [dateRange, setDateRange] = useState<NonNullable<WarehouseTaskWorkbenchQuery["dateRange"]>>("today");
  const [taskType, setTaskType] = useState<number | "all">("all");
  const [laneCode, setLaneCode] = useState("all");
  const [riskOnly, setRiskOnly] = useState(false);
  const [sort, setSort] = useState<NonNullable<WarehouseTaskWorkbenchQuery["sort"]>>("dueTimestamp");
  const [order, setOrder] = useState<NonNullable<WarehouseTaskWorkbenchQuery["order"]>>("asc");
  const [selectedTaskId, setSelectedTaskId] = useState("");

  const query = useMemo<WarehouseTaskWorkbenchQuery>(
    () => ({
      dateRange,
      taskType: taskType === "all" ? undefined : taskType,
      riskOnly: riskOnly || undefined,
      keyword: keyword.trim() || undefined,
      sort,
      order,
      count: 50
    }),
    [dateRange, keyword, order, riskOnly, sort, taskType]
  );

  const visibleTasks = useMemo(
    () => data.tasks.filter((task) => taskMatchesLane(task, laneCode)),
    [data.tasks, laneCode]
  );

  const lanes = useMemo(() => {
    const apiLanes = data.lanes.length
      ? data.lanes
      : ["inbound", "outbound", "quality", "shipment", "blocked"].map((code) => ({
          laneCode: code,
          taskCount: data.tasks.filter((task) => taskMatchesLane(task, code)).length,
          riskCount: data.tasks.filter((task) => taskMatchesLane(task, code) && task.riskTypes.length > 0).length
        }));
    return [{ laneCode: "all", taskCount: data.tasks.length, riskCount: data.tasks.filter((task) => task.riskTypes.length).length }, ...apiLanes];
  }, [data.lanes, data.tasks]);

  useEffect(() => {
    let isMounted = true;

    getWarehouseTaskWorkbench(query, dataSourceMode).then((result) => {
      if (!isMounted) {
        return;
      }
      const firstTask = result.data.tasks[0];
      setData(result.data);
      setSource(result.source);
      setError(result.error);
      setSelectedTaskId(firstTask?.taskId ?? "");
      setDetail(undefined);
      setIsDetailLoading(Boolean(firstTask));
      setIsLoading(false);
    });

    return () => {
      isMounted = false;
    };
  }, [dataSourceMode, query]);

  useEffect(() => {
    if (!selectedTaskId) {
      return;
    }

    let isMounted = true;

    getWarehouseTaskDetail(selectedTaskId, dataSourceMode).then((result) => {
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
  }, [dataSourceMode, selectedTaskId]);

  function handleSelectTask(task: WarehouseTaskWorkbenchItem) {
    setIsDetailLoading(true);
    setSelectedTaskId(task.taskId);
  }

  return (
    <AppLayout activePath="/warehouse" title="倉庫任務工作台">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">WarehouseTaskWorkbenchScreen</StatusBadge>
                <StatusBadge tone={source === "api" ? "success" : "warning"}>
                  {source === "api" ? "API data" : "Mock fallback"}
                </StatusBadge>
                {isLoading ? <StatusBadge tone="info">Loading API</StatusBadge> : null}
                <DataSourceToggle value={dataSourceMode} onChange={setDataSourceMode} />
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">倉庫任務工作台</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                以今日、逾期與近期任務為核心，集中掌握入庫、出庫、移倉、品檢與出貨工作的處理狀態、阻塞原因與下一步負責部門。
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
            Task workbench API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}
        {detailError ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Task detail API 尚未可用，已使用 mock fallback。{detailError}
          </p>
        ) : null}

        <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          <SummaryCard
            hint={`${formatNumber(data.total, language)} tasks returned · ${data.range.mode}`}
            icon={ClipboardList}
            label="未完成任務"
            tone="info"
            value={formatNumber(data.summary.openTaskCount, language)}
          />
          <SummaryCard
            hint="已逾期且尚未完成的任務"
            icon={TimerReset}
            label="逾期任務"
            tone={data.summary.overdueTaskCount ? "danger" : "success"}
            value={formatNumber(data.summary.overdueTaskCount, language)}
          />
          <SummaryCard
            hint="需先處理阻塞原因"
            icon={ShieldAlert}
            label="阻塞任務"
            tone={data.summary.blockedTaskCount ? "danger" : "success"}
            value={formatNumber(data.summary.blockedTaskCount, language)}
          />
          <SummaryCard
            hint="出庫、移倉或出貨可能不足"
            icon={AlertTriangle}
            label="庫存不足"
            tone={data.summary.inventoryShortageTaskCount ? "warning" : "success"}
            value={formatNumber(data.summary.inventoryShortageTaskCount, language)}
          />
        </section>

        <section className="rounded-lg border border-border bg-white p-3 shadow-card">
          <div className="grid gap-3 xl:grid-cols-[minmax(260px,1fr)_auto_auto_auto_auto]">
            <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
              <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
              <input
                aria-label="搜尋任務、來源單號、料號、品名、批號或倉庫"
                className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                onChange={(event) => setKeyword(event.target.value)}
                placeholder="任務 / 來源 / 料號 / 品名 / 批號 / 倉庫"
                value={keyword}
              />
            </label>

            <div className="flex flex-wrap gap-2">
              {dateRangeOptions.map((option) => (
                <button
                  className={`h-10 rounded-button px-3 text-sm font-medium ${
                    dateRange === option.value
                      ? "bg-primary text-white"
                      : "bg-slate-100 text-textSecondary hover:bg-slate-200"
                  }`}
                  key={option.value}
                  onClick={() => setDateRange(option.value)}
                  type="button"
                >
                  {option.label}
                </button>
              ))}
            </div>

            <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
              <ListChecks className="h-4 w-4 text-textSecondary" aria-hidden="true" />
              <select
                className="bg-transparent text-sm outline-none"
                onChange={(event) => setTaskType(event.target.value === "all" ? "all" : Number(event.target.value))}
                value={taskType}
              >
                {taskTypeOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.value === "all" ? option.label : warehouseEnumLabel("taskType", option.value, language)}
                  </option>
                ))}
              </select>
            </label>

            <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
              <Filter className="h-4 w-4 text-textSecondary" aria-hidden="true" />
              <select
                className="bg-transparent text-sm outline-none"
                onChange={(event) => setSort(event.target.value as NonNullable<WarehouseTaskWorkbenchQuery["sort"]>)}
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
              className={`inline-flex h-10 items-center justify-center gap-2 rounded-button px-3 text-sm font-medium ${
                riskOnly ? "bg-danger text-white" : "border border-border bg-white text-textSecondary"
              }`}
              onClick={() => setRiskOnly((current) => !current)}
              type="button"
            >
              <AlertTriangle className="h-4 w-4" aria-hidden="true" />
              風險
            </button>

            <button
              className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary"
              onClick={() => setOrder((current) => (current === "asc" ? "desc" : "asc"))}
              type="button"
            >
              {order === "asc" ? "升冪" : "降冪"}
            </button>
          </div>
        </section>

        <section className="grid gap-3 md:grid-cols-3 xl:grid-cols-6">
          {lanes.map((lane) => (
            <LaneCard
              isActive={laneCode === lane.laneCode}
              key={lane.laneCode}
              lane={lane}
              onSelect={setLaneCode}
            />
          ))}
        </section>

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_420px]">
          <div className="min-w-0 space-y-3">
            <div className="rounded-lg border border-border bg-white p-4 shadow-card">
              <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">任務清單</p>
                  <h3 className="mt-1 text-lg font-semibold text-textPrimary">
                    {warehouseEnumLabel("laneCode", laneCode, language)}
                  </h3>
                </div>
                <div className="flex flex-wrap gap-2 text-xs text-textSecondary">
                  <span className="inline-flex items-center gap-1">
                    <CalendarClock className="h-4 w-4" aria-hidden="true" />
                    {data.range.startDate || "未提供"} - {data.range.endDate || "未提供"}
                  </span>
                  <span>{formatNumber(visibleTasks.length, language)} / {formatNumber(data.total, language)}</span>
                </div>
              </div>
            </div>

            {isLoading ? (
              <EmptyState message="正在載入倉庫任務工作台。" />
            ) : (
              <TaskTable tasks={visibleTasks} selectedTaskId={selectedTaskId} onSelect={handleSelectTask} />
            )}
          </div>

          <DetailPanel detail={detail} isLoading={isDetailLoading} />
        </section>

        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm font-semibold text-textPrimary">後續執行工作區</p>
              <p className="mt-1 text-xs leading-5 text-textSecondary">
                第一版工作台為 read-only；完成、放行、解除阻塞與數量異動延至下一版 Task Execution API。
              </p>
            </div>
            <Link
              className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary"
              href="/warehouse/inventory/lots"
            >
              <PackageSearch className="h-4 w-4" aria-hidden="true" />
              查看批號清單
            </Link>
          </div>
        </section>
      </div>
    </AppLayout>
  );
}
