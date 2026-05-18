import { MapPin, PackageOpen } from "lucide-react";
import { StatusBadge } from "@/components/ui/status-badge";
import type { InventoryItem } from "@/types/warehouse";

type InventoryCardProps = {
  item: InventoryItem;
};

export function InventoryCard({ item }: InventoryCardProps) {
  const stockRatio = Math.min(Math.round((item.quantity / item.safetyStock) * 100), 140);
  const barColor = item.quantity < item.safetyStock ? "bg-warning" : "bg-success";

  return (
    <article className="rounded-card border border-border bg-white p-5 shadow-card">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-sm font-semibold text-primary">{item.sku}</p>
          <h3 className="mt-1 truncate text-lg font-semibold text-textPrimary">{item.name}</h3>
          <p className="mt-1 text-xs text-textSecondary">{item.category} / {item.warehouse}</p>
        </div>
        <StatusBadge tone={item.tone}>{item.status}</StatusBadge>
      </div>

      <div className="mt-5 grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-button bg-slate-50 p-3">
          <div className="flex items-center gap-2 text-textSecondary">
            <PackageOpen className="h-4 w-4" aria-hidden="true" />
            <span>現有庫存</span>
          </div>
          <p className="mt-1 font-semibold text-textPrimary">
            {item.quantity.toLocaleString()} {item.unit}
          </p>
        </div>
        <div className="rounded-button bg-slate-50 p-3">
          <div className="flex items-center gap-2 text-textSecondary">
            <MapPin className="h-4 w-4" aria-hidden="true" />
            <span>庫位</span>
          </div>
          <p className="mt-1 font-semibold text-textPrimary">{item.location}</p>
        </div>
      </div>

      <div className="mt-5">
        <div className="mb-2 flex justify-between text-sm">
          <span className="font-medium text-textPrimary">安全庫存</span>
          <span className="text-textSecondary">
            {item.safetyStock.toLocaleString()} {item.unit}
          </span>
        </div>
        <div className="h-2 overflow-hidden rounded-full bg-slate-100">
          <div className={`h-full rounded-full ${barColor}`} style={{ width: `${Math.min(stockRatio, 100)}%` }} />
        </div>
      </div>
    </article>
  );
}
