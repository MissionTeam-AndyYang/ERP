import { StatusBadge } from "@/components/ui/status-badge";
import type { ProductionLine, StatusTone } from "@/types/dashboard";

const progressStyles: Record<StatusTone, string> = {
  success: "bg-success",
  warning: "bg-warning",
  danger: "bg-danger",
  info: "bg-info",
  neutral: "bg-slate-400"
};

type ProductionLineCardProps = {
  line: ProductionLine;
};

export function ProductionLineCard({ line }: ProductionLineCardProps) {
  return (
    <article className="rounded-card border border-border bg-white p-5 shadow-card">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-textSecondary">{line.line}</p>
          <h3 className="mt-1 text-lg font-semibold text-textPrimary">{line.product}</h3>
          <p className="mt-1 text-xs text-textSecondary">批號 {line.batchNo}</p>
        </div>
        <StatusBadge tone={line.tone}>{line.status}</StatusBadge>
      </div>

      <div className="mt-5">
        <div className="mb-2 flex justify-between text-sm">
          <span className="font-medium text-textPrimary">進度</span>
          <span className="text-textSecondary">{line.progress}%</span>
        </div>
        <div className="h-2 overflow-hidden rounded-full bg-slate-100">
          <div
            className={`h-full rounded-full ${progressStyles[line.tone]}`}
            style={{ width: `${line.progress}%` }}
          />
        </div>
      </div>

      <div className="mt-5 grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-button bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">良率</p>
          <p className="mt-1 font-semibold text-textPrimary">{line.yieldRate}</p>
        </div>
        <div className="rounded-button bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">預估狀態</p>
          <p className="mt-1 font-semibold text-textPrimary">{line.eta}</p>
        </div>
      </div>
    </article>
  );
}
