import type { StatusTone } from "@/types/dashboard";

const toneStyles: Record<StatusTone, string> = {
  success: "bg-success/10 text-success",
  warning: "bg-warning/10 text-warning",
  danger: "bg-danger/10 text-danger",
  info: "bg-info/10 text-info",
  neutral: "bg-slate-100 text-slate-600"
};

type ModuleKpiCardProps = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export function ModuleKpiCard({ label, value, hint, tone }: ModuleKpiCardProps) {
  return (
    <article className="rounded-card border border-border bg-white p-5 shadow-card">
      <p className="text-sm font-medium text-textSecondary">{label}</p>
      <div className="mt-3 flex items-end justify-between gap-3">
        <strong className="text-3xl font-bold leading-none text-textPrimary">{value}</strong>
        <span className={`rounded-full px-2.5 py-1 text-xs font-medium ${toneStyles[tone]}`}>
          {hint}
        </span>
      </div>
    </article>
  );
}
