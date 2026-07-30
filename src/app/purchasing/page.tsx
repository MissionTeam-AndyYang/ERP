"use client";

import {
  AlertTriangle,
  CalendarDays,
  ChevronLeft,
  ChevronRight,
  FileText,
  PackageCheck,
  Search,
  ShoppingCart,
  Truck,
  Users
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { DataSourceToggle, type DataSourceMode } from "@/components/common/data-source-toggle";
import { StatusBadge } from "@/components/ui/status-badge";
import { usePurchasingDashboard } from "@/hooks/use-purchasing-dashboard";
import { useLanguage } from "@/i18n/language-provider";
import { AppLayout } from "@/layouts/app-layout";
import { getPurchaseOrderDetail, type PurchasingDashboardQuery } from "@/services/purchasing-api";
import type {
  PurchaseDeliveryRiskItem,
  PurchaseOrderDetail,
  PurchaseOrderItem,
  PurchaseReceiptItem,
  PurchaseSupplierItem,
  PurchasingDashboardData,
  PurchasingSummary,
  PurchasingWorkspaceTab
} from "@/types/purchasing";

const tabs: { id: PurchasingWorkspaceTab; label: string; icon: typeof ShoppingCart }[] = [
  { id: "purchase-orders", label: "採購單", icon: ShoppingCart },
  { id: "delivery-risk", label: "交期風險", icon: AlertTriangle },
  { id: "receiving", label: "到貨驗收入庫", icon: Truck },
  { id: "suppliers", label: "供應商追蹤", icon: Users }
];

const initialPageByTab: Record<PurchasingWorkspaceTab, number> = {
  "purchase-orders": 0,
  "delivery-risk": 0,
  receiving: 0,
  suppliers: 0
};

const pageSizeOptions = [25, 50, 100] as const;

const tabDescriptions: Record<PurchasingWorkspaceTab, string> = {
  "purchase-orders": "以採購單為主資料列，查詢採購日期、供應商、交易單位、單價、到貨規劃與請購關聯。",
  "delivery-risk": "聚焦逾期、今日到期、未收缺口與正式來源影響，讓採購追蹤有明確優先順序。",
  receiving: "以進貨單為主，呈現分批到貨、退回、實際數量、收貨狀態與倉庫入庫交接。",
  suppliers: "依供應商彙總採購單數、未收數量、逾期筆數與採購金額，快速掌握合作風險。"
};

function todayIsoDate() {
  return new Date().toISOString().slice(0, 10);
}

function firstDayOfMonthIsoDate() {
  const now = new Date();
  return new Date(now.getFullYear(), now.getMonth(), 1).toISOString().slice(0, 10);
}

function formatNumber(value: number | undefined, language: string, maximumFractionDigits = 2) {
  return new Intl.NumberFormat(language, {
    maximumFractionDigits,
    minimumFractionDigits: maximumFractionDigits
  }).format(value ?? 0);
}

function formatInteger(value: number | undefined, language: string) {
  return new Intl.NumberFormat(language, { maximumFractionDigits: 0 }).format(value ?? 0);
}

function formatMoney(value: number | undefined, language: string) {
  return `$${formatInteger(value, language)}`;
}

function totalByTab(data: PurchasingDashboardData, activeTab: PurchasingWorkspaceTab) {
  if (activeTab === "delivery-risk") {
    return data.total.deliveryRisks;
  }
  if (activeTab === "receiving") {
    return data.total.receipts;
  }
  if (activeTab === "suppliers") {
    return data.total.suppliers;
  }
  return data.total.purchaseOrders;
}

function rowCountByTab(data: PurchasingDashboardData, activeTab: PurchasingWorkspaceTab) {
  if (activeTab === "delivery-risk") {
    return data.deliveryRisks.length;
  }
  if (activeTab === "receiving") {
    return data.receipts.length;
  }
  if (activeTab === "suppliers") {
    return data.suppliers.length;
  }
  return data.purchaseOrders.length;
}

function normalizeSearch(value: string) {
  return value.trim().toLocaleLowerCase();
}

function includesSearch(value: string | number | undefined | null, search: string) {
  if (!search) {
    return true;
  }
  if (value === undefined || value === null) {
    return false;
  }
  return String(value).toLocaleLowerCase().includes(search);
}

function purchaseOrderMatchesSearch(item: PurchaseOrderItem, search: string) {
  return [
    item.purchaseOrderNo,
    item.purchaseDate,
    item.itemNo,
    item.itemName,
    item.supplierNo,
    item.supplierName,
    item.purchaseRequestNo,
    item.sourceOrderNo,
    item.linkedWorkOrderNo,
    item.warehouseStatus,
    item.riskLevel,
    item.riskTypeLabel
  ].some((value) => includesSearch(value, search));
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="rounded-lg border border-dashed border-border bg-white px-4 py-8 text-center text-sm text-textSecondary">
      {message}
    </div>
  );
}

function KpiStrip({ summary }: { summary: PurchasingSummary[] }) {
  const icons = [ShoppingCart, AlertTriangle, FileText, PackageCheck];

  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {summary.map((item, index) => {
        const Icon = icons[index] ?? ShoppingCart;
        return (
          <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.label}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-sm font-medium text-textSecondary">{item.label}</p>
                <p className="mt-2 text-2xl font-semibold text-textPrimary">{item.value}</p>
              </div>
              <span className="grid h-10 w-10 place-items-center rounded-full bg-slate-100 text-textSecondary">
                <Icon className="h-5 w-5" aria-hidden="true" />
              </span>
            </div>
            <p className="mt-3 text-xs leading-5 text-textSecondary">{item.hint}</p>
          </div>
        );
      })}
    </section>
  );
}

function PurchaseOrderTable({
  rows,
  selectedId,
  searchQuery,
  language,
  onSelect
}: {
  rows: PurchaseOrderItem[];
  selectedId?: string;
  searchQuery: string;
  language: string;
  onSelect: (item: PurchaseOrderItem) => void;
}) {
  const visibleRows = useMemo(
    () => rows.filter((item) => purchaseOrderMatchesSearch(item, searchQuery)),
    [rows, searchQuery]
  );

  if (!visibleRows.length) {
    return <EmptyState message="目前查無符合條件的採購單。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[1320px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">採購單 / 料品</th>
              <th className="px-4 py-3">日期</th>
              <th className="px-4 py-3">供應商</th>
              <th className="px-4 py-3 text-right">訂購 / 已收</th>
              <th className="px-4 py-3">單位</th>
              <th className="px-4 py-3 text-right">單價</th>
              <th className="px-4 py-3 text-right">金額</th>
              <th className="px-4 py-3">到貨規劃</th>
              <th className="px-4 py-3">請購關聯</th>
              <th className="px-4 py-3">來源影響</th>
              <th className="px-4 py-3">入庫</th>
              <th className="px-4 py-3">風險</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {visibleRows.map((item) => {
              const isSelected = item.id === selectedId;
              return (
                <tr
                  className={`cursor-pointer transition ${isSelected ? "bg-info/10" : "hover:bg-slate-50"}`}
                  key={item.id}
                  onClick={() => onSelect(item)}
                >
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{item.purchaseOrderNo || "未提供採購單號"}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {item.itemNo} · {item.itemName}
                    </p>
                  </td>
                  <td className="px-4 py-3 text-textPrimary">{item.purchaseDate || "未提供"}</td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{item.supplierName || "未提供供應商"}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.supplierNo || "無供應商編號"}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(item.orderedCount, language)} / {formatNumber(item.receivedCount, language)}
                  </td>
                  <td className="px-4 py-3 text-textPrimary">{item.unit || "未提供"}</td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatNumber(item.unitPrice, language, 4)}</td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatMoney(item.purchaseAmount, language)}</td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{item.expectedArrivalDate || "未提供"}</p>
                    <p className="mt-1 text-xs text-textSecondary">未收 {formatNumber(item.openCount, language)}</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={item.purchaseRequestLinkStatusCode === "linked" ? "success" : "warning"}>
                      {item.purchaseRequestLinkStatus}
                    </StatusBadge>
                    <p className="mt-1 text-xs text-textSecondary">{item.purchaseRequestNo || "無請購單"}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{item.sourceOrderNo || "未連來源訂單"}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.linkedWorkOrderNo || "未連工單"}</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={item.warehouseStatusCode === "stocked" ? "success" : "warning"}>
                      {item.warehouseStatus}
                    </StatusBadge>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={item.tone}>{item.riskLevel}</StatusBadge>
                    <p className="mt-1 text-xs text-textSecondary">{item.riskTypeLabel}</p>
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

function DeliveryRiskTable({
  rows,
  searchQuery,
  language,
  onSelect
}: {
  rows: PurchaseDeliveryRiskItem[];
  searchQuery: string;
  language: string;
  onSelect: (item: PurchaseDeliveryRiskItem) => void;
}) {
  const visibleRows = rows.filter((item) => purchaseOrderMatchesSearch(item, searchQuery));

  if (!visibleRows.length) {
    return <EmptyState message="目前查無符合條件的交期風險採購單。" />;
  }

  return (
    <div className="grid gap-3 lg:grid-cols-2">
      {visibleRows.map((item) => (
        <button
          className="rounded-lg border border-border bg-white p-4 text-left shadow-card transition hover:border-primary/40 hover:bg-slate-50"
          key={item.id}
          onClick={() => onSelect(item)}
          type="button"
        >
          <div className="flex items-start justify-between gap-3">
            <div>
              <StatusBadge tone={item.tone}>{item.riskLevel}</StatusBadge>
              <h3 className="mt-3 font-semibold text-textPrimary">{item.itemName}</h3>
              <p className="mt-1 text-sm text-textSecondary">{item.purchaseOrderNo}</p>
            </div>
            <AlertTriangle className="h-5 w-5 text-textSecondary" aria-hidden="true" />
          </div>
          <div className="mt-4 grid gap-2 sm:grid-cols-2">
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">預計到貨</p>
              <p className="mt-1 font-semibold text-textPrimary">{item.expectedArrivalDate || "未提供"}</p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">未收缺口</p>
              <p className="mt-1 font-semibold text-textPrimary">
                {formatNumber(item.shortageCount, language)} {item.unit}
              </p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">影響來源</p>
              <p className="mt-1 font-semibold text-textPrimary">{item.impactSourceNo || item.impactSourceLabel}</p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">追蹤動作</p>
              <p className="mt-1 font-semibold text-textPrimary">{item.followUpLabel}</p>
            </div>
          </div>
        </button>
      ))}
    </div>
  );
}

function ReceiptTable({
  rows,
  searchQuery,
  language
}: {
  rows: PurchaseReceiptItem[];
  searchQuery: string;
  language: string;
}) {
  const visibleRows = rows.filter((item) =>
    [
      item.no,
      item.purchaseOrderNo,
      item.date,
      item.categoryLabel,
      item.itemNo,
      item.itemName,
      item.receivingStatus,
      item.warehouseStatus,
      item.nextOwnerDepartmentLabel
    ].some((value) => includesSearch(value, searchQuery))
  );

  if (!visibleRows.length) {
    return <EmptyState message="目前查無符合條件的進貨與入庫交接資料。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[980px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">進貨單</th>
              <th className="px-4 py-3">採購單</th>
              <th className="px-4 py-3">日期</th>
              <th className="px-4 py-3">類別 / 料品</th>
              <th className="px-4 py-3 text-right">排定 / 實際 / 累計</th>
              <th className="px-4 py-3">收貨</th>
              <th className="px-4 py-3">入庫交接</th>
              <th className="px-4 py-3">下一步</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {visibleRows.map((item) => (
              <tr className="hover:bg-slate-50" key={item.id}>
                <td className="px-4 py-3 font-semibold text-textPrimary">{item.no || "未提供"}</td>
                <td className="px-4 py-3 text-textPrimary">{item.purchaseOrderNo || "未連採購單"}</td>
                <td className="px-4 py-3 text-textPrimary">{item.date || "未提供"}</td>
                <td className="px-4 py-3">
                  <StatusBadge tone={item.category === 1 ? "danger" : "info"}>{item.categoryLabel}</StatusBadge>
                  <p className="mt-1 text-xs text-textSecondary">
                    {item.itemNo} · {item.itemName}
                  </p>
                </td>
                <td className="px-4 py-3 text-right text-textPrimary">
                  {formatNumber(item.expectedCount, language)} / {formatNumber(item.checkedCount, language)} /{" "}
                  {formatNumber(item.receivedCount, language)}
                </td>
                <td className="px-4 py-3">
                  <StatusBadge tone={item.receivingStatusCode === "received" ? "success" : "warning"}>
                    {item.receivingStatus}
                  </StatusBadge>
                </td>
                <td className="px-4 py-3">
                  <StatusBadge tone={item.warehouseStatusCode === "stocked" ? "success" : "warning"}>
                    {item.warehouseStatus}
                  </StatusBadge>
                </td>
                <td className="px-4 py-3 text-textPrimary">{item.nextOwnerDepartmentLabel}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function SupplierTable({
  rows,
  searchQuery,
  language
}: {
  rows: PurchaseSupplierItem[];
  searchQuery: string;
  language: string;
}) {
  const visibleRows = rows.filter((item) =>
    [item.supplierNo, item.supplierName, item.riskLevel].some((value) => includesSearch(value, searchQuery))
  );

  if (!visibleRows.length) {
    return <EmptyState message="目前查無符合條件的供應商彙總。" />;
  }

  return (
    <div className="grid gap-3 lg:grid-cols-2">
      {visibleRows.map((item) => (
        <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.id}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <h3 className="font-semibold text-textPrimary">{item.supplierName || "未提供供應商"}</h3>
              <p className="mt-1 text-sm text-textSecondary">{item.supplierNo || "無供應商編號"}</p>
            </div>
            <StatusBadge tone={item.tone}>{item.riskLevel}</StatusBadge>
          </div>
          <div className="mt-4 grid grid-cols-2 gap-2 text-sm">
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">採購單 / 未收</p>
              <p className="mt-1 font-semibold text-textPrimary">
                {formatInteger(item.purchaseOrderCount, language)} / {formatInteger(item.openPurchaseOrderCount, language)}
              </p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">逾期採購單</p>
              <p className="mt-1 font-semibold text-textPrimary">{formatInteger(item.latePurchaseOrderCount, language)}</p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">未收數量</p>
              <p className="mt-1 font-semibold text-textPrimary">{formatNumber(item.pendingReceiptCount, language)}</p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">採購金額</p>
              <p className="mt-1 font-semibold text-textPrimary">{formatMoney(item.purchaseAmount, language)}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

function MainContent({
  activeTab,
  data,
  selectedId,
  searchQuery,
  language,
  onSelectPurchaseOrder
}: {
  activeTab: PurchasingWorkspaceTab;
  data: PurchasingDashboardData;
  selectedId?: string;
  searchQuery: string;
  language: string;
  onSelectPurchaseOrder: (item: PurchaseOrderItem) => void;
}) {
  if (activeTab === "delivery-risk") {
    return (
      <DeliveryRiskTable
        rows={data.deliveryRisks}
        searchQuery={searchQuery}
        language={language}
        onSelect={onSelectPurchaseOrder}
      />
    );
  }

  if (activeTab === "receiving") {
    return <ReceiptTable rows={data.receipts} searchQuery={searchQuery} language={language} />;
  }

  if (activeTab === "suppliers") {
    return <SupplierTable rows={data.suppliers} searchQuery={searchQuery} language={language} />;
  }

  return (
    <PurchaseOrderTable
      rows={data.purchaseOrders}
      selectedId={selectedId}
      searchQuery={searchQuery}
      language={language}
      onSelect={onSelectPurchaseOrder}
    />
  );
}

function PaginationControls({
  activeTabLabel,
  currentPage,
  pageSize,
  total,
  rowCount,
  language,
  isLoading,
  onPageChange,
  onPageSizeChange
}: {
  activeTabLabel: string;
  currentPage: number;
  pageSize: number;
  total: number;
  rowCount: number;
  language: string;
  isLoading: boolean;
  onPageChange: (page: number) => void;
  onPageSizeChange: (pageSize: number) => void;
}) {
  const pageStart = total > 0 ? currentPage * pageSize + 1 : 0;
  const pageEnd = total > 0 ? Math.min(currentPage * pageSize + rowCount, total) : 0;
  const pageCount = Math.max(1, Math.ceil(total / pageSize));
  const canGoPrevious = currentPage > 0 && !isLoading;
  const canGoNext = currentPage + 1 < pageCount && !isLoading;

  return (
    <div className="flex flex-col gap-3 rounded-lg border border-border bg-white p-3 shadow-card md:flex-row md:items-center md:justify-between">
      <div className="text-sm text-textSecondary">
        <span className="font-medium text-textPrimary">{activeTabLabel}</span>
        <span className="ml-2">
          {formatInteger(pageStart, language)}-{formatInteger(pageEnd, language)} /{" "}
          {formatInteger(total, language)} 筆
        </span>
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <label className="flex h-9 items-center gap-2 rounded-input border border-border bg-slate-50 px-3 text-sm text-textSecondary">
          每頁
          <select
            className="bg-transparent font-medium text-textPrimary outline-none"
            aria-label="採購中心每頁筆數"
            value={pageSize}
            onChange={(event) => onPageSizeChange(Number(event.target.value))}
          >
            {pageSizeOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </label>
        <button
          className="inline-flex h-9 items-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
          disabled={!canGoPrevious}
          onClick={() => onPageChange(Math.max(currentPage - 1, 0))}
          type="button"
        >
          <ChevronLeft className="h-4 w-4" aria-hidden="true" />
          上一頁
        </button>
        <span className="min-w-[92px] text-center text-sm text-textSecondary">
          {formatInteger(currentPage + 1, language)} / {formatInteger(pageCount, language)}
        </span>
        <button
          className="inline-flex h-9 items-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
          disabled={!canGoNext}
          onClick={() => onPageChange(currentPage + 1)}
          type="button"
        >
          下一頁
          <ChevronRight className="h-4 w-4" aria-hidden="true" />
        </button>
      </div>
    </div>
  );
}

function DetailPanel({
  item,
  detail,
  detailError,
  isLoading,
  language
}: {
  item?: PurchaseOrderItem;
  detail?: PurchaseOrderDetail;
  detailError?: string;
  isLoading: boolean;
  language: string;
}) {
  if (!item) {
    return (
      <aside className="rounded-lg border border-border bg-white p-4 shadow-card">
        <EmptyState message="尚未選取採購單。" />
      </aside>
    );
  }

  const visibleDetail = detail;

  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">採購單追蹤</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{item.purchaseOrderNo || "未提供採購單號"}</h2>
          <p className="mt-1 text-sm text-textSecondary">{item.itemName}</p>
        </div>
        <StatusBadge tone={item.tone}>{item.riskLevel}</StatusBadge>
      </div>

      {isLoading ? <p className="rounded-md bg-info/10 px-3 py-2 text-sm text-info">載入採購單明細中...</p> : null}
      {detailError ? (
        <p className="rounded-md border border-warning/20 bg-warning/10 px-3 py-2 text-sm text-warning">
          採購單明細 API 暫時無法取得，右側保留清單摘要。{detailError}
        </p>
      ) : null}

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">採購日期</p>
          <p className="mt-1 font-semibold text-textPrimary">{visibleDetail?.purchaseDate || item.purchaseDate || "未提供"}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">預計到貨</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {visibleDetail?.expectedArrivalDate || item.expectedArrivalDate || "未提供"}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">數量</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(visibleDetail?.orderedCount ?? item.orderedCount, language)} {item.unit}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">單價 / 金額</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(visibleDetail?.unitPrice ?? item.unitPrice, language, 4)} /{" "}
            {formatMoney(visibleDetail?.purchaseAmount ?? item.purchaseAmount, language)}
          </p>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">正式關聯</p>
        <div className="rounded-md border border-border px-3 py-2 text-sm">
          <p className="text-textPrimary">請購單：{visibleDetail?.purchaseRequestNo || item.purchaseRequestNo || "未連請購"}</p>
          <p className="mt-1 text-textSecondary">來源訂單：{visibleDetail?.sourceOrderNo || item.sourceOrderNo || "未確認"}</p>
          <p className="mt-1 text-textSecondary">生產工單：{visibleDetail?.linkedWorkOrderNo || item.linkedWorkOrderNo || "未確認"}</p>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">庫存摘要</p>
        <div className="grid grid-cols-3 gap-2 text-sm">
          <div className="rounded-md bg-slate-50 p-3">
            <p className="text-xs text-textSecondary">現有</p>
            <p className="mt-1 font-semibold text-textPrimary">{formatNumber(visibleDetail?.inventory.currentCount, language)}</p>
          </div>
          <div className="rounded-md bg-slate-50 p-3">
            <p className="text-xs text-textSecondary">預留</p>
            <p className="mt-1 font-semibold text-textPrimary">{formatNumber(visibleDetail?.inventory.reservedCount, language)}</p>
          </div>
          <div className="rounded-md bg-slate-50 p-3">
            <p className="text-xs text-textSecondary">可用</p>
            <p className="mt-1 font-semibold text-textPrimary">{formatNumber(visibleDetail?.inventory.availableCount, language)}</p>
          </div>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">進貨紀錄</p>
        {visibleDetail?.receipts.length ? (
          visibleDetail.receipts.map((receipt) => (
            <div className="rounded-md border border-border px-3 py-2 text-sm" key={receipt.no}>
              <div className="flex items-center justify-between gap-3">
                <p className="font-medium text-textPrimary">{receipt.no}</p>
                <StatusBadge tone={receipt.warehouseStatus === "已入庫" ? "success" : "warning"}>
                  {receipt.warehouseStatus}
                </StatusBadge>
              </div>
              <p className="mt-1 text-xs text-textSecondary">
                {receipt.date} · {receipt.categoryLabel} · {formatNumber(receipt.checkedCount, language)} {item.unit}
              </p>
            </div>
          ))
        ) : (
          <EmptyState message="目前沒有正式進貨紀錄。" />
        )}
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">Workflow</p>
        {visibleDetail?.workflow.length ? (
          visibleDetail.workflow.map((step, index) => (
            <div className="flex gap-3" key={`${step.taskId}-${step.refNo}`}>
              <div className="flex flex-col items-center">
                <span
                  className={`grid h-6 w-6 place-items-center rounded-full text-xs font-bold ${
                    step.tone === "success"
                      ? "bg-success text-white"
                      : step.tone === "danger"
                        ? "bg-danger text-white"
                        : step.tone === "warning"
                          ? "bg-warning text-white"
                          : "bg-info text-white"
                  }`}
                >
                  {index + 1}
                </span>
                {visibleDetail && index < visibleDetail.workflow.length - 1 ? <span className="h-7 w-px bg-border" /> : null}
              </div>
              <div className="min-w-0 pb-2 text-sm">
                <div className="flex flex-wrap items-center gap-2">
                  <p className="font-medium text-textPrimary">{step.taskTypeLabel}</p>
                  <StatusBadge tone={step.tone}>{step.taskStatusLabel}</StatusBadge>
                </div>
                <p className="mt-1 truncate text-xs text-textSecondary">
                  {step.refNo || "無來源單號"} · {step.ownerDepartmentLabel}
                </p>
              </div>
            </div>
          ))
        ) : (
          <EmptyState message="目前沒有 workflow 任務紀錄。" />
        )}
      </div>
    </aside>
  );
}

export default function PurchasingPage() {
  const { language } = useLanguage();
  const [activeTab, setActiveTab] = useState<PurchasingWorkspaceTab>("purchase-orders");
  const [dataSourceMode, setDataSourceMode] = useState<DataSourceMode>("api");
  const [selectedPurchaseOrderNo, setSelectedPurchaseOrderNo] = useState<string>();
  const [searchValue, setSearchValue] = useState("");
  const [startDate, setStartDate] = useState(firstDayOfMonthIsoDate());
  const [endDate, setEndDate] = useState(todayIsoDate());
  const [pageSize, setPageSize] = useState<number>(50);
  const [pageByTab, setPageByTab] = useState<Record<PurchasingWorkspaceTab, number>>(initialPageByTab);
  const [detailState, setDetailState] = useState<{
    detail?: PurchaseOrderDetail;
    purchaseOrderNo?: string;
    error?: string;
  }>({});

  const searchQuery = normalizeSearch(searchValue);
  const activePage = pageByTab[activeTab] ?? 0;
  const query = useMemo<PurchasingDashboardQuery>(
    () => ({
      startDate,
      endDate,
      keyword: searchValue.trim() || undefined,
      start: activePage * pageSize,
      count: pageSize
    }),
    [activePage, endDate, pageSize, searchValue, startDate]
  );
  const { data: purchasingData, error, isLoading, source } = usePurchasingDashboard(dataSourceMode, query);

  const selectedPurchaseOrderCandidate =
    purchasingData.purchaseOrders.find((item) => item.purchaseOrderNo === selectedPurchaseOrderNo) ??
    purchasingData.deliveryRisks.find((item) => item.purchaseOrderNo === selectedPurchaseOrderNo);
  const selectedPurchaseOrder = selectedPurchaseOrderCandidate ?? purchasingData.purchaseOrders[0];
  const activeTotal = totalByTab(purchasingData, activeTab);
  const activeRowCount = rowCountByTab(purchasingData, activeTab);

  function resetPagination() {
    setPageByTab(initialPageByTab);
  }

  useEffect(() => {
    if (!selectedPurchaseOrder?.purchaseOrderNo) {
      return;
    }

    let isMounted = true;

    getPurchaseOrderDetail(selectedPurchaseOrder.purchaseOrderNo, selectedPurchaseOrder, dataSourceMode).then((result) => {
      if (!isMounted) {
        return;
      }
      setDetailState({
        detail: result.detail,
        purchaseOrderNo: selectedPurchaseOrder.purchaseOrderNo,
        error: result.error
      });
    });

    return () => {
      isMounted = false;
    };
  }, [selectedPurchaseOrder, dataSourceMode]);

  const activeTabLabel = tabs.find((tab) => tab.id === activeTab)?.label ?? "採購單";

  return (
    <AppLayout activePath="/purchasing" title="採購中心 Purchasing Workspace">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">PO-first V1</StatusBadge>
                <StatusBadge tone={source === "api" ? "success" : "warning"}>
                  {source === "api" ? "API data" : "Mock data"}
                </StatusBadge>
                {isLoading ? <StatusBadge tone="info">Loading API</StatusBadge> : null}
                <StatusBadge tone="neutral">採購單 / 交期 / 到貨 / 供應商</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">採購單主視角工作區</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                以採購單為主資料列，查詢任意歷史區間內的採購金額、交易單位、預計到貨、分批進貨、
                入庫交接、請購關聯與來源影響。API 錯誤會明確顯示，不自動改用 mock 資料。
              </p>
            </div>
            <div className="grid gap-2 md:grid-cols-[auto_auto_auto] xl:grid-cols-[auto_auto_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <CalendarDays className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-[132px] bg-transparent text-sm outline-none"
                  aria-label="採購查詢起始日期"
                  type="date"
                  value={startDate}
                  onChange={(event) => {
                    setStartDate(event.target.value);
                    resetPagination();
                  }}
                />
              </label>
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <CalendarDays className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-[132px] bg-transparent text-sm outline-none"
                  aria-label="採購查詢結束日期"
                  type="date"
                  value={endDate}
                  onChange={(event) => {
                    setEndDate(event.target.value);
                    resetPagination();
                  }}
                />
              </label>
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full min-w-[210px] bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  aria-label="搜尋採購單、進貨單、請購單、供應商或料品"
                  value={searchValue}
                  onChange={(event) => {
                    setSearchValue(event.target.value);
                    resetPagination();
                  }}
                  placeholder="採購單 / 進貨單 / 供應商 / 料品"
                />
              </label>
              <DataSourceToggle
                value={dataSourceMode}
                onChange={(mode) => {
                  setDataSourceMode(mode);
                  resetPagination();
                }}
              />
            </div>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-danger/20 bg-danger/10 px-4 py-3 text-sm text-danger">
            Purchasing API 發生錯誤，畫面未改用 mock 資料。可切換資料來源為 Mock 進行前端預覽。{error}
          </p>
        ) : null}

        <KpiStrip summary={purchasingData.summary} />

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="min-w-0 space-y-4">
            <div className="rounded-lg border border-border bg-white p-3 shadow-card">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">採購視圖</p>
                  <h3 className="mt-1 text-lg font-semibold text-textPrimary">{activeTabLabel}</h3>
                  <p className="mt-1 text-sm text-textSecondary">{tabDescriptions[activeTab]}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {tabs.map((tab) => {
                    const Icon = tab.icon;
                    return (
                      <button
                        className={`inline-flex h-9 items-center gap-2 rounded-button px-3 text-sm font-medium transition ${
                          activeTab === tab.id
                            ? "bg-primary text-white"
                            : "bg-slate-100 text-textSecondary hover:bg-slate-200"
                        }`}
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        type="button"
                      >
                        <Icon className="h-4 w-4" aria-hidden="true" />
                        {tab.label}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-2 text-xs text-textSecondary">
              <StatusBadge tone="neutral">
                採購單 {formatInteger(purchasingData.total.purchaseOrders, language)}
              </StatusBadge>
              <StatusBadge tone="neutral">
                交期風險 {formatInteger(purchasingData.total.deliveryRisks, language)}
              </StatusBadge>
              <StatusBadge tone="neutral">進貨單 {formatInteger(purchasingData.total.receipts, language)}</StatusBadge>
              <StatusBadge tone="neutral">供應商 {formatInteger(purchasingData.total.suppliers, language)}</StatusBadge>
              <span>
                查詢區間 {purchasingData.range.startDate || startDate} 至 {purchasingData.range.endDate || endDate}
              </span>
            </div>

            <PaginationControls
              activeTabLabel={activeTabLabel}
              currentPage={activePage}
              pageSize={pageSize}
              total={activeTotal}
              rowCount={activeRowCount}
              language={language}
              isLoading={isLoading}
              onPageChange={(page) =>
                setPageByTab((current) => ({
                  ...current,
                  [activeTab]: page
                }))
              }
              onPageSizeChange={(nextPageSize) => {
                setPageSize(nextPageSize);
                resetPagination();
              }}
            />

            <MainContent
              activeTab={activeTab}
              data={purchasingData}
              selectedId={selectedPurchaseOrder?.id}
              searchQuery={searchQuery}
              language={language}
              onSelectPurchaseOrder={(item) => {
                setSelectedPurchaseOrderNo(item.purchaseOrderNo);
                setActiveTab(item.riskLevelCode ? "delivery-risk" : activeTab);
              }}
            />
          </div>

          <DetailPanel
            item={selectedPurchaseOrder}
            detail={detailState.purchaseOrderNo === selectedPurchaseOrder?.purchaseOrderNo ? detailState.detail : undefined}
            detailError={detailState.purchaseOrderNo === selectedPurchaseOrder?.purchaseOrderNo ? detailState.error : undefined}
            isLoading={Boolean(
              selectedPurchaseOrder?.purchaseOrderNo &&
                detailState.purchaseOrderNo !== selectedPurchaseOrder.purchaseOrderNo
            )}
            language={language}
          />
        </section>
      </div>
    </AppLayout>
  );
}
