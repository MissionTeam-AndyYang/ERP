import { AlertCircle } from "lucide-react";
import type { AlertItem } from "@/types/dashboard";

const toneStyles: Record<AlertItem["tone"], string> = {
  success: "border-success/20 bg-success/5 text-success",
  warning: "border-warning/20 bg-warning/5 text-warning",
  danger: "border-danger/20 bg-danger/5 text-danger",
  info: "border-info/20 bg-info/5 text-info",
  neutral: "border-slate-200 bg-slate-50 text-slate-600"
};

type AlertCardProps = {
  item: AlertItem;
};

export function AlertCard({ item }: AlertCardProps) {
  return (
    <article className="flex gap-3 rounded-card border border-border bg-white p-4">
      <div className={`h-fit rounded-button border p-2 ${toneStyles[item.tone]}`}>
        <AlertCircle className="h-4 w-4" aria-hidden="true" />
      </div>
      <div className="min-w-0 flex-1">
        <div className="flex items-start justify-between gap-3">
          <h3 className="text-sm font-semibold text-textPrimary">{item.title}</h3>
          <span className="shrink-0 text-xs text-textSecondary">{item.time}</span>
        </div>
        <p className="mt-1 text-sm leading-6 text-textSecondary">{item.detail}</p>
      </div>
    </article>
  );
}
