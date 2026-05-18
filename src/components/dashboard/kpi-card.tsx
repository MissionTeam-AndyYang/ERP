import type { KpiItem } from "@/types/dashboard";

const toneStyles: Record<KpiItem["tone"], string> = {
  success: "bg-success/10 text-success",
  warning: "bg-warning/10 text-warning",
  danger: "bg-danger/10 text-danger",
  info: "bg-info/10 text-info",
  neutral: "bg-slate-100 text-slate-600"
};

type KpiCardProps = {
  item: KpiItem;
};

export function KpiCard({ item }: KpiCardProps) {
  const Icon = item.icon;

  return (
    <article className="rounded-card border border-border bg-white p-5 shadow-card">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-textSecondary">{item.title}</p>
          <div className="mt-3 flex items-end gap-2">
            <strong className="text-4xl font-bold leading-none text-textPrimary">
              {item.value}
            </strong>
            <span className="pb-1 text-sm font-medium text-textSecondary">{item.unit}</span>
          </div>
        </div>
        <div className={`rounded-button p-3 ${toneStyles[item.tone]}`}>
          <Icon className="h-5 w-5" aria-hidden="true" />
        </div>
      </div>
      <p className="mt-4 text-sm text-textSecondary">{item.trend}</p>
    </article>
  );
}
