import { CalendarClock } from "lucide-react";
import { StatusBadge } from "@/components/ui/status-badge";
import type { ExpiryBatch } from "@/types/warehouse";

type ExpiryBatchTableProps = {
  batches: ExpiryBatch[];
};

export function ExpiryBatchTable({ batches }: ExpiryBatchTableProps) {
  return (
    <article className="rounded-card border border-border bg-white p-5 shadow-card">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-textSecondary">Batch & Expiry</p>
          <h2 className="text-xl font-semibold text-textPrimary">批號與效期追蹤</h2>
        </div>
        <div className="rounded-button bg-danger/10 p-3 text-danger">
          <CalendarClock className="h-5 w-5" aria-hidden="true" />
        </div>
      </div>

      <div className="mt-5 overflow-hidden rounded-card border border-border">
        <div className="grid grid-cols-[1.2fr_1fr_0.8fr_0.8fr] gap-3 bg-slate-50 px-4 py-3 text-xs font-semibold text-textSecondary">
          <span>批號 / 品項</span>
          <span>庫位</span>
          <span>效期</span>
          <span>狀態</span>
        </div>
        <div className="divide-y divide-border">
          {batches.map((batch) => (
            <div className="grid grid-cols-[1.2fr_1fr_0.8fr_0.8fr] gap-3 px-4 py-4 text-sm" key={batch.batchNo}>
              <div className="min-w-0">
                <p className="font-semibold text-textPrimary">{batch.batchNo}</p>
                <p className="mt-1 truncate text-textSecondary">
                  {batch.itemName} / {batch.quantity.toLocaleString()} {batch.unit}
                </p>
              </div>
              <div className="text-textSecondary">{batch.location}</div>
              <div>
                <p className="font-medium text-textPrimary">{batch.expiryDate}</p>
                <p className="mt-1 text-xs text-textSecondary">剩 {batch.daysLeft} 天</p>
              </div>
              <StatusBadge tone={batch.tone}>{batch.category}</StatusBadge>
            </div>
          ))}
        </div>
      </div>
    </article>
  );
}
