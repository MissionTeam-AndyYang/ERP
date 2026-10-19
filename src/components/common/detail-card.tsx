import { StatusBadge } from "@/components/ui/status-badge";
import type { StatusTone } from "@/types/dashboard";

type DetailCardProps = {
  eyebrow: string;
  title: string;
  subtitle: string;
  status: string;
  tone: StatusTone;
  rows: { label: string; value: string }[];
};

export function DetailCard({ eyebrow, title, subtitle, status, tone, rows }: DetailCardProps) {
  return (
    <article className="rounded-card border border-border bg-white p-5 shadow-card">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-sm font-semibold text-primary">{eyebrow}</p>
          <h3 className="mt-1 truncate text-lg font-semibold text-textPrimary">{title}</h3>
          <p className="mt-1 text-xs text-textSecondary">{subtitle}</p>
        </div>
        <StatusBadge tone={tone}>{status}</StatusBadge>
      </div>
      <div className="mt-5 grid gap-3 sm:grid-cols-3">
        {rows.map((row) => (
          <div className="rounded-button bg-slate-50 p-3 text-sm" key={row.label}>
            <p className="text-xs text-textSecondary">{row.label}</p>
            <p className="mt-1 font-semibold text-textPrimary">{row.value}</p>
          </div>
        ))}
      </div>
    </article>
  );
}
