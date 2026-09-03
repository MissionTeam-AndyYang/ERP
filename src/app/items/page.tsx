"use client";

import { AlertTriangle, Building2, Boxes, Eye, Link2, Loader2, PackageCheck, RefreshCw, Search, Tags } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { DataSourceStatusBadge } from "@/components/common/data-source-status-badge";
import { DataSourceToggle, type DataSourceMode } from "@/components/common/data-source-toggle";
import { ModuleHero } from "@/components/common/module-hero";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { SupportEmptyState } from "@/components/common/support-empty-state";
import { StatusBadge } from "@/components/ui/status-badge";
import { AppLayout } from "@/layouts/app-layout";
import {
  emptyItemAndTransactionMasterData,
  getCompanyMasterDetail,
  getItemAndTransactionMasterDashboard,
  getItemMasterDetail,
  getTransactionItemMasterDetail
} from "@/services/items-master-api";
import type {
  CompanyDetail,
  CompanyMasterRow,
  ContractSummaryRow,
  ItemAndTransactionMasterData,
  ItemMasterDetailData,
  ItemMasterDetailTarget,
  MaterialItemDetail,
  MaterialItemMasterRow,
  TransactionItemDetail,
  TransactionItemMasterRow
} from "@/types/items-master";

type MasterTab = "material" | "transaction" | "company";

const tabs: { id: MasterTab; label: string }[] = [
  { id: "material", label: "料品品項" },
  { id: "transaction", label: "交易品項" },
  { id: "company", label: "客戶／廠商" }
];

function formatInteger(value: number) {
  return new Intl.NumberFormat("zh-TW", { maximumFractionDigits: 0 }).format(value);
}

function formatNumber(value: number, fractionDigits = 2) {
  return new Intl.NumberFormat("zh-TW", {
    minimumFractionDigits: fractionDigits,
    maximumFractionDigits: fractionDigits
  }).format(value);
}

function formatPrice(value: number) {
  return new Intl.NumberFormat("zh-TW", {
    minimumFractionDigits: 4,
    maximumFractionDigits: 4
  }).format(value);
}

function RowLabel({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs text-textSecondary">{label}</p>
      <p className="mt-1 font-medium text-textPrimary">{value || "未提供"}</p>
    </div>
  );
}

function DetailButton({ onClick }: { onClick: () => void }) {
  return (
    <button
      className="inline-flex h-9 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-xs font-medium text-textSecondary transition hover:bg-slate-50"
      onClick={onClick}
      type="button"
    >
      <Eye className="h-4 w-4" />
      查看
    </button>
  );
}

function isMaterialDetail(data?: ItemMasterDetailData): data is MaterialItemDetail {
  return Boolean(data && "inventorySummary" in data);
}

function isCompanyDetail(data?: ItemMasterDetailData): data is CompanyDetail {
  return Boolean(data && "company" in data);
}

function isTransactionDetail(data?: ItemMasterDetailData): data is TransactionItemDetail {
  return Boolean(data && "transItem" in data);
}

function MaterialItemsView({
  items,
  onSelect
}: {
  items: MaterialItemMasterRow[];
  onSelect: (target: ItemMasterDetailTarget) => void;
}) {
  if (!items.length) {
    return <SupportEmptyState title="沒有符合條件的料品品項" description="請調整搜尋條件，或確認料品主檔 API 是否已有資料。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white">
      <table className="w-full min-w-[920px] text-left text-sm">
        <thead className="bg-slate-50 text-xs font-semibold uppercase text-textSecondary">
          <tr>
            <th className="px-4 py-3">料號 / 名稱</th>
            <th className="px-4 py-3">類別</th>
            <th className="px-4 py-3">單位</th>
            <th className="px-4 py-3 text-right">庫存</th>
            <th className="px-4 py-3 text-right">批號</th>
            <th className="px-4 py-3 text-right">BOM</th>
            <th className="px-4 py-3">狀態</th>
            <th className="px-4 py-3 text-right">明細</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border">
          {items.map((item) => (
            <tr className="align-top" key={item.id}>
              <td className="px-4 py-3">
                <p className="font-semibold text-textPrimary">{item.itemNo}</p>
                <p className="mt-1 text-xs text-textSecondary">{item.itemName || "未命名料品"}</p>
              </td>
              <td className="px-4 py-3">{item.itemCategoryLabel}</td>
              <td className="px-4 py-3">
                <p>{item.unitWarehouseLabel}</p>
                <p className="mt-1 text-xs text-textSecondary">生產 {item.unitProductLabel}</p>
              </td>
              <td className="px-4 py-3 text-right">{formatNumber(item.currentQuantity)}</td>
              <td className="px-4 py-3 text-right">{formatInteger(item.batchCount)}</td>
              <td className="px-4 py-3 text-right">{formatInteger(item.bomCount)}</td>
              <td className="px-4 py-3">
                <StatusBadge tone={item.tone}>{item.masterStatusLabel}</StatusBadge>
                <p className="mt-2 text-xs text-textSecondary">{item.maintenanceRiskLabel}</p>
              </td>
              <td className="px-4 py-3 text-right">
                <DetailButton onClick={() => onSelect({ type: "material", id: item.itemNo })} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function TransactionItemsView({
  items,
  onSelect
}: {
  items: TransactionItemMasterRow[];
  onSelect: (target: ItemMasterDetailTarget) => void;
}) {
  if (!items.length) {
    return <SupportEmptyState title="沒有符合條件的交易品項" description="請調整搜尋條件，或確認交易品項 API 是否已有資料。" />;
  }

  return (
    <div className="grid gap-4 xl:grid-cols-2">
      {items.map((item) => (
        <article className="rounded-lg border border-border bg-white p-4 shadow-sm" key={item.id}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-xs font-medium text-textSecondary">{item.transItemNo}</p>
              <h3 className="mt-1 text-base font-semibold text-textPrimary">{item.transItemName || "未命名交易品項"}</h3>
              <p className="mt-1 text-sm text-textSecondary">
                {item.companyDisplayName || "未關聯公司"} · {item.itemNo || "未關聯料品"}
              </p>
            </div>
            <StatusBadge tone={item.tone}>{item.dataQualityLabel}</StatusBadge>
          </div>
          <div className="mt-3">
            <DetailButton onClick={() => onSelect({ type: "transaction", id: item.transItemNo })} />
          </div>
          <div className="mt-4 grid gap-3 sm:grid-cols-3">
            <RowLabel label="交易類別" value={item.transItemCategoryLabel} />
            <RowLabel label="合約" value={item.contractNo || item.contractCategoryLabel} />
            <RowLabel label="對應料品" value={item.itemName || item.itemCategoryLabel} />
          </div>
          <div className="mt-4 grid gap-3 rounded-md bg-slate-50 p-3 sm:grid-cols-3">
            <RowLabel label="交易單位" value={item.tradeUnitLabel} />
            <RowLabel label="單價" value={formatPrice(item.tradePrice)} />
            <RowLabel label="物流價" value={formatPrice(item.shippingPrice)} />
          </div>
        </article>
      ))}
    </div>
  );
}

function CompaniesView({
  companies,
  onSelect
}: {
  companies: CompanyMasterRow[];
  onSelect: (target: ItemMasterDetailTarget) => void;
}) {
  if (!companies.length) {
    return <SupportEmptyState title="沒有符合條件的客戶／廠商" description="請調整搜尋條件，或確認公司主檔摘要是否已有資料。" />;
  }

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      {companies.map((company) => (
        <article className="rounded-lg border border-border bg-white p-4 shadow-sm" key={company.id}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-xs font-medium text-textSecondary">{company.companyNo}</p>
              <h3 className="mt-1 text-base font-semibold text-textPrimary">
                {company.companyDisplayName || company.companyName || "未命名公司"}
              </h3>
              <p className="mt-1 text-sm text-textSecondary">{company.companyName || company.businessNo || "未提供公司資訊"}</p>
            </div>
            <StatusBadge tone={company.tone}>{company.dataQualityLabel}</StatusBadge>
          </div>
          <div className="mt-3">
            <DetailButton onClick={() => onSelect({ type: "company", id: company.companyNo })} />
          </div>
          <div className="mt-4 grid gap-3 sm:grid-cols-3">
            <RowLabel label="交易品項" value={`${formatInteger(company.transItemCount)} 筆`} />
            <RowLabel label="合約" value={`${formatInteger(company.contractCount)} 筆`} />
            <RowLabel label="聯絡人" value={company.contactName || company.contactPhone} />
          </div>
          <div className="mt-4 grid gap-3 rounded-md bg-slate-50 p-3 sm:grid-cols-2">
            <RowLabel
              label="收款條件"
              value={`${company.receivablePayment.paymentTypeLabel} / ${company.receivablePayment.paymentSourceLabel}`}
            />
            <RowLabel
              label="付款條件"
              value={`${company.payablePayment.paymentTypeLabel} / ${company.payablePayment.paymentSourceLabel}`}
            />
          </div>
        </article>
      ))}
    </div>
  );
}

function CategorySummary({ data }: { data: ItemAndTransactionMasterData }) {
  return (
    <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
      <section className="rounded-lg border border-border bg-white p-4">
        <div className="mb-4 flex items-center justify-between gap-3">
          <div>
            <p className="text-xs font-medium text-textSecondary">料品分類</p>
            <h3 className="mt-1 text-base font-semibold text-textPrimary">庫存與 BOM 訊號</h3>
          </div>
          <StatusBadge tone="neutral">{formatInteger(data.categorySummary.length)} 類</StatusBadge>
        </div>
        <div className="grid gap-3 md:grid-cols-2">
          {data.categorySummary.length ? (
            data.categorySummary.map((item) => (
              <div className="rounded-md border border-border p-3" key={item.itemCategory}>
                <div className="flex items-center justify-between gap-2">
                  <p className="font-medium text-textPrimary">{item.itemCategoryLabel}</p>
                  <StatusBadge tone={item.maintenanceItemCount ? "warning" : "success"}>
                    {item.maintenanceItemCount ? "待維護" : "正常"}
                  </StatusBadge>
                </div>
                <div className="mt-3 grid grid-cols-3 gap-2 text-sm">
                  <RowLabel label="品項" value={formatInteger(item.itemCount)} />
                  <RowLabel label="有庫存" value={formatInteger(item.stockItemCount)} />
                  <RowLabel label="BOM" value={formatInteger(item.bomLinkedItemCount)} />
                </div>
              </div>
            ))
          ) : (
            <SupportEmptyState title="沒有分類摘要" description="目前 API 未回傳料品分類摘要。" />
          )}
        </div>
      </section>
      <section className="rounded-lg border border-border bg-white p-4">
        <div className="mb-4 flex items-center gap-2">
          <AlertTriangle className="h-4 w-4 text-warning" />
          <h3 className="text-base font-semibold text-textPrimary">主檔維護建議</h3>
        </div>
        <div className="space-y-3">
          {data.maintenanceSuggestions.length ? (
            data.maintenanceSuggestions.map((item) => (
              <div className="rounded-md border border-border p-3" key={item.suggestionId}>
                <div className="flex items-center justify-between gap-2">
                  <p className="font-medium text-textPrimary">{item.itemNo}</p>
                  <StatusBadge tone={item.tone}>{item.riskLevelLabel}</StatusBadge>
                </div>
                <p className="mt-2 text-sm text-textSecondary">{item.suggestionTypeLabel}</p>
              </div>
            ))
          ) : (
            <SupportEmptyState title="沒有維護建議" description="目前查詢條件下沒有 read-only 主檔維護建議。" />
          )}
        </div>
      </section>
    </div>
  );
}

function ContractList({ contracts }: { contracts: ContractSummaryRow[] }) {
  if (!contracts.length) {
    return <SupportEmptyState title="沒有合約資料" description="目前 API 回傳合約清單為空。" />;
  }
  return (
    <div className="space-y-3">
      {contracts.map((contract) => (
        <div className="rounded-md border border-border p-3" key={contract.id}>
          <div className="flex items-start justify-between gap-2">
            <div>
              <p className="font-medium text-textPrimary">{contract.contractNo || "未提供合約號"}</p>
              <p className="mt-1 text-xs text-textSecondary">{contract.contractDisplayName || contract.transItemName || "未提供合約名稱"}</p>
            </div>
            <StatusBadge tone="neutral">{contract.contractCategoryLabel}</StatusBadge>
          </div>
          <div className="mt-3 grid gap-2 text-sm sm:grid-cols-2">
            <RowLabel label="交易品項" value={contract.transItemNo || "-"} />
            <RowLabel label="生效日" value={contract.effectiveDate || "-"} />
            {contract.tradeUnitLabel ? <RowLabel label="單位" value={contract.tradeUnitLabel} /> : null}
            {contract.tradePrice !== undefined ? <RowLabel label="單價" value={formatPrice(contract.tradePrice)} /> : null}
          </div>
        </div>
      ))}
    </div>
  );
}

function DetailPanel({
  target,
  data,
  isLoading,
  error
}: {
  target?: ItemMasterDetailTarget;
  data?: ItemMasterDetailData;
  isLoading: boolean;
  error?: string;
}) {
  return (
    <aside className="rounded-lg border border-border bg-white p-4">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs font-medium text-textSecondary">明細面板</p>
          <h3 className="mt-1 text-lg font-semibold text-textPrimary">
            {target?.type === "material" ? "料品明細" : null}
            {target?.type === "transaction" ? "交易品項明細" : null}
            {target?.type === "company" ? "客戶／廠商明細" : null}
            {!target ? "請選取資料" : null}
          </h3>
        </div>
        {isLoading ? <Loader2 className="h-5 w-5 animate-spin text-primary" /> : null}
      </div>

      <div className="mt-4">
        {!target ? (
          <SupportEmptyState title="尚未選取明細" description="請在左側列表點選查看，確認後端明細資料。" />
        ) : null}
        {error ? (
          <p className="rounded-md border border-danger/20 bg-danger/10 px-3 py-2 text-sm text-danger">
            明細資料取得失敗，畫面未改用示範資料。{error}
          </p>
        ) : null}
        {target && !isLoading && !error && !data ? (
          <SupportEmptyState title="沒有明細資料" description="API 回傳空資料，畫面依真實結果呈現。" />
        ) : null}

        {isMaterialDetail(data) ? (
          <div className="space-y-5">
            <div>
              <StatusBadge tone={data.item.tone}>{data.item.masterStatusLabel}</StatusBadge>
              <h4 className="mt-3 text-base font-semibold text-textPrimary">{data.item.itemName || data.item.itemNo}</h4>
              <p className="mt-1 text-sm text-textSecondary">{data.item.itemNo} · {data.item.itemCategoryLabel}</p>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              <RowLabel label="目前庫存" value={`${formatNumber(data.inventorySummary.currentQuantity)} ${data.item.unitWarehouseLabel}`} />
              <RowLabel label="可用數量" value={`${formatNumber(data.inventorySummary.availableQuantity)} ${data.item.unitWarehouseLabel}`} />
              <RowLabel label="預留數量" value={`${formatNumber(data.inventorySummary.reservedQuantity)} ${data.item.unitWarehouseLabel}`} />
              <RowLabel label="品檢保留" value={`${formatNumber(data.inventorySummary.qualityHoldQuantity)} ${data.item.unitWarehouseLabel}`} />
              <RowLabel label="倉庫數" value={formatInteger(data.inventorySummary.warehouseCount)} />
              <RowLabel label="批號數" value={formatInteger(data.inventorySummary.batchCount)} />
            </div>
            <section>
              <p className="mb-2 text-sm font-semibold text-textPrimary">BOM 使用</p>
              {data.bomUsage.length ? (
                <div className="space-y-2">
                  {data.bomUsage.map((bom) => (
                    <div className="rounded-md border border-border p-3" key={bom.id}>
                      <p className="font-medium text-textPrimary">{bom.bomNo}</p>
                      <p className="mt-1 text-xs text-textSecondary">
                        v{formatInteger(bom.bomVersion)} · {formatNumber(bom.quantity)} {bom.unitLabel} · {bom.effectiveDate || "未提供日期"}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <SupportEmptyState title="沒有 BOM 使用資料" description="目前 API 回傳 BOM 使用清單為空。" />
              )}
            </section>
            <section>
              <p className="mb-2 text-sm font-semibold text-textPrimary">近期批號</p>
              {data.recentBatches.length ? (
                <div className="space-y-2">
                  {data.recentBatches.map((batch) => (
                    <div className="rounded-md border border-border p-3" key={batch.id}>
                      <div className="flex items-center justify-between gap-2">
                        <p className="font-medium text-textPrimary">{batch.batchNo}</p>
                        <StatusBadge tone={batch.tone}>{batch.riskLevelLabel}</StatusBadge>
                      </div>
                      <p className="mt-1 text-xs text-textSecondary">
                        {formatNumber(batch.currentQuantity)} {batch.unitLabel} · {batch.refNo || batch.refCategoryLabel} · {batch.validDate || "未提供效期"}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <SupportEmptyState title="沒有近期批號" description="目前 API 回傳近期批號清單為空。" />
              )}
            </section>
          </div>
        ) : null}

        {isCompanyDetail(data) ? (
          <div className="space-y-5">
            <div>
              <StatusBadge tone={data.company.tone}>{data.company.dataQualityLabel}</StatusBadge>
              <h4 className="mt-3 text-base font-semibold text-textPrimary">
                {data.company.companyDisplayName || data.company.companyName || data.company.companyNo}
              </h4>
              <p className="mt-1 text-sm text-textSecondary">{data.company.companyNo} · {data.company.businessNo || "未提供統編"}</p>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              <RowLabel label="地址" value={data.company.address} />
              <RowLabel label="電話" value={data.company.phone || data.company.contactPhone} />
              <RowLabel label="聯絡人" value={data.company.contactName} />
              <RowLabel label="Email" value={data.company.contactEmail} />
              <RowLabel label="收款條件" value={`${data.company.receivablePayment.paymentTypeLabel} / ${data.company.receivablePayment.paymentSourceLabel}`} />
              <RowLabel label="付款條件" value={`${data.company.payablePayment.paymentTypeLabel} / ${data.company.payablePayment.paymentSourceLabel}`} />
            </div>
            <section>
              <p className="mb-2 text-sm font-semibold text-textPrimary">交易品項</p>
              {data.transactionItems.length ? (
                <div className="space-y-2">
                  {data.transactionItems.map((item) => (
                    <div className="rounded-md border border-border p-3" key={item.id}>
                      <p className="font-medium text-textPrimary">{item.transItemName || item.transItemNo}</p>
                      <p className="mt-1 text-xs text-textSecondary">
                        {item.transItemNo} · {item.itemNo || "未關聯料品"} · {item.tradeUnitLabel}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <SupportEmptyState title="沒有交易品項" description="目前 API 回傳交易品項清單為空。" />
              )}
            </section>
            <section>
              <p className="mb-2 text-sm font-semibold text-textPrimary">合約</p>
              <ContractList contracts={data.contracts} />
            </section>
          </div>
        ) : null}

        {isTransactionDetail(data) ? (
          <div className="space-y-5">
            <div>
              <StatusBadge tone={data.transItem.tone}>{data.transItem.dataQualityLabel}</StatusBadge>
              <h4 className="mt-3 text-base font-semibold text-textPrimary">
                {data.transItem.transItemName || data.transItem.transItemNo}
              </h4>
              <p className="mt-1 text-sm text-textSecondary">
                {data.transItem.transItemNo} · {data.transItem.companyDisplayName || "未關聯公司"}
              </p>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              <RowLabel label="交易類別" value={data.transItem.transItemCategoryLabel} />
              <RowLabel label="對應料品" value={data.transItem.itemName || data.transItem.itemNo} />
              <RowLabel label="建立日期" value={data.transItem.creationDate} />
              <RowLabel label="備註" value={data.transItem.comment} />
            </div>
            <section>
              <p className="mb-2 text-sm font-semibold text-textPrimary">關聯料品</p>
              {data.linkedItems.length ? (
                <div className="space-y-2">
                  {data.linkedItems.map((item) => (
                    <div className="rounded-md border border-border p-3" key={item.id}>
                      <p className="font-medium text-textPrimary">{item.itemName || item.itemNo}</p>
                      <p className="mt-1 text-xs text-textSecondary">
                        {item.itemNo} · {item.itemCategoryLabel} · {item.unitWarehouseLabel}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <SupportEmptyState title="沒有關聯料品" description="目前 API 回傳關聯料品清單為空。" />
              )}
            </section>
            <section>
              <p className="mb-2 text-sm font-semibold text-textPrimary">合約</p>
              <ContractList contracts={data.contracts} />
            </section>
          </div>
        ) : null}
      </div>
    </aside>
  );
}

export default function ItemsPage() {
  const [dataSourceMode, setDataSourceMode] = useState<DataSourceMode>("api");
  const [activeTab, setActiveTab] = useState<MasterTab>("material");
  const [searchValue, setSearchValue] = useState("");
  const [data, setData] = useState<ItemAndTransactionMasterData>(emptyItemAndTransactionMasterData);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | undefined>();
  const [refreshKey, setRefreshKey] = useState(0);
  const [detailTarget, setDetailTarget] = useState<ItemMasterDetailTarget | undefined>();
  const [detailData, setDetailData] = useState<ItemMasterDetailData | undefined>();
  const [isDetailLoading, setIsDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState<string | undefined>();

  const clearDetail = () => {
    setDetailTarget(undefined);
    setDetailData(undefined);
    setDetailError(undefined);
    setIsDetailLoading(false);
  };

  const selectDetail = (target: ItemMasterDetailTarget) => {
    setDetailTarget(target);
    setDetailData(undefined);
    setDetailError(undefined);
    setIsDetailLoading(true);
  };

  useEffect(() => {
    let cancelled = false;
    getItemAndTransactionMasterDashboard({ keyword: searchValue, count: 50 }, dataSourceMode).then((result) => {
      if (cancelled) {
        return;
      }
      setData(result.data);
      setError(result.error);
      setIsLoading(false);
    });
    return () => {
      cancelled = true;
    };
  }, [dataSourceMode, refreshKey, searchValue]);

  useEffect(() => {
    if (!detailTarget) {
      return;
    }

    let cancelled = false;
    const request =
      detailTarget.type === "material"
        ? getItemMasterDetail(detailTarget.id, dataSourceMode)
        : detailTarget.type === "company"
          ? getCompanyMasterDetail(detailTarget.id, dataSourceMode)
          : getTransactionItemMasterDetail(detailTarget.id, dataSourceMode);

    request.then((result) => {
      if (cancelled) {
        return;
      }
      setDetailData(result.data);
      setDetailError(result.error);
      setIsDetailLoading(false);
    });

    return () => {
      cancelled = true;
    };
  }, [dataSourceMode, detailTarget]);

  const kpis = useMemo(
    () => [
      { label: "料品總數", value: formatInteger(data.summary.totalItemCount), hint: `可使用 ${formatInteger(data.summary.activeItemCount)} 筆`, tone: "info" as const },
      { label: "交易品項", value: formatInteger(data.summary.transItemCount), hint: `已關聯料品 ${formatInteger(data.summary.linkedItemCount)} 筆`, tone: "success" as const },
      { label: "客戶／廠商", value: formatInteger(data.summary.companyCount), hint: `合約關聯 ${formatInteger(data.summary.contractLinkedTransItemCount)} 筆`, tone: "neutral" as const },
      { label: "待維護", value: formatInteger(data.summary.maintenanceItemCount + data.summary.companyDataQualityIssueCount + data.summary.transItemDataQualityIssueCount), hint: "料品、公司與交易品項資料缺口", tone: "warning" as const }
    ],
    [data.summary]
  );

  return (
    <AppLayout activePath="/items" title="品項中心">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="主資料中心"
          title="品項中心"
          description="同一入口檢視料品品項、交易品項與客戶／廠商主資料，保留清楚的資料邊界與後續 API integration 彈性。"
          metrics={[
            { label: "料品", value: formatInteger(data.summary.totalItemCount), icon: Tags },
            { label: "交易品項", value: formatInteger(data.summary.transItemCount), icon: Link2 },
            { label: "客戶／廠商", value: formatInteger(data.summary.companyCount), icon: Building2 }
          ]}
        />

        <div className="flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
          <div className="flex flex-wrap items-center gap-2">
            <DataSourceStatusBadge source={dataSourceMode} isLoading={isLoading} hasError={Boolean(error)} />
            <StatusBadge tone="neutral">Read-only</StatusBadge>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <label className="flex h-10 min-w-[260px] items-center gap-2 rounded-input border border-border bg-white px-3">
              <Search className="h-4 w-4 text-textSecondary" />
              <input
                aria-label="搜尋料品、交易品項或公司"
                className="min-w-0 flex-1 bg-transparent text-sm outline-none"
                onChange={(event) => {
                  setIsLoading(true);
                  setSearchValue(event.target.value);
                }}
                placeholder="料號 / 交易品項 / 公司 / 合約"
                value={searchValue}
              />
            </label>
            <button
              className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary"
              onClick={() => {
                setIsLoading(true);
                setRefreshKey((value) => value + 1);
              }}
              type="button"
            >
              <RefreshCw className="h-4 w-4" />
              重新整理
            </button>
            <DataSourceToggle
              value={dataSourceMode}
              onChange={(value) => {
                setIsLoading(true);
                clearDetail();
                setDataSourceMode(value);
              }}
            />
          </div>
        </div>

        {error ? (
          <p className="rounded-lg border border-danger/20 bg-danger/10 px-4 py-3 text-sm text-danger">
            品項中心資料取得失敗，畫面未改用示範資料。可切換資料來源為示範資料檢視畫面格式。{error}
          </p>
        ) : null}

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>

        <CategorySummary data={data} />

        <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_420px]">
          <section className="rounded-lg border border-border bg-white p-4">
            <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <p className="text-xs font-medium text-textSecondary">主資料視圖</p>
                <h3 className="mt-1 text-lg font-semibold text-textPrimary">
                  {tabs.find((tab) => tab.id === activeTab)?.label}
                </h3>
              </div>
              <div className="flex flex-wrap gap-2">
                {tabs.map((tab) => (
                  <button
                    className={`inline-flex h-10 items-center justify-center rounded-button px-3 text-sm font-medium transition ${
                      activeTab === tab.id ? "bg-primary text-white" : "border border-border bg-white text-textSecondary hover:bg-slate-50"
                    }`}
                    key={tab.id}
                    onClick={() => {
                      setActiveTab(tab.id);
                      clearDetail();
                    }}
                    type="button"
                  >
                    {tab.label}
                  </button>
                ))}
              </div>
            </div>

            <div className="mt-4">
              {isLoading ? (
                <div className="flex min-h-[180px] items-center justify-center rounded-md border border-dashed border-border text-sm text-textSecondary">
                  <Loader2 className="mr-2 h-4 w-4 animate-spin text-primary" />
                  資料載入中
                </div>
              ) : null}
              {!isLoading && activeTab === "material" ? (
                <MaterialItemsView items={data.items} onSelect={selectDetail} />
              ) : null}
              {!isLoading && activeTab === "transaction" ? (
                <TransactionItemsView items={data.transactionItems} onSelect={selectDetail} />
              ) : null}
              {!isLoading && activeTab === "company" ? (
                <CompaniesView companies={data.companies} onSelect={selectDetail} />
              ) : null}
            </div>
          </section>

          <DetailPanel target={detailTarget} data={detailData} isLoading={isDetailLoading} error={detailError} />
        </div>

        <section className="grid gap-4 md:grid-cols-3">
          <div className="rounded-lg border border-border bg-white p-4">
            <Boxes className="h-5 w-5 text-primary" />
            <h4 className="mt-3 font-semibold text-textPrimary">料品品項</h4>
            <p className="mt-2 text-sm leading-6 text-textSecondary">檢視料品是否具備庫存單位、BOM 關聯與庫存訊號。</p>
          </div>
          <div className="rounded-lg border border-border bg-white p-4">
            <PackageCheck className="h-5 w-5 text-success" />
            <h4 className="mt-3 font-semibold text-textPrimary">交易品項</h4>
            <p className="mt-2 text-sm leading-6 text-textSecondary">檢視交易品名、關聯公司、關聯料品、合約、單位與價格。</p>
          </div>
          <div className="rounded-lg border border-border bg-white p-4">
            <Building2 className="h-5 w-5 text-info" />
            <h4 className="mt-3 font-semibold text-textPrimary">客戶／廠商</h4>
            <p className="mt-2 text-sm leading-6 text-textSecondary">檢視公司主檔、聯絡資訊、收付款條件與資料完整度。</p>
          </div>
        </section>
      </div>
    </AppLayout>
  );
}
