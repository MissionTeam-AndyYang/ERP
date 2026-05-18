import type { LucideIcon } from "lucide-react";
import { StatusBadge } from "@/components/ui/status-badge";

type HeroMetric = {
  label: string;
  value: string;
  icon: LucideIcon;
};

type ModuleHeroProps = {
  badge: string;
  title: string;
  description: string;
  metrics: HeroMetric[];
};

export function ModuleHero({ badge, title, description, metrics }: ModuleHeroProps) {
  return (
    <section className="flex flex-col justify-between gap-4 rounded-card bg-primaryDark p-6 text-white shadow-card md:flex-row md:items-center">
      <div>
        <StatusBadge tone="info">{badge}</StatusBadge>
        <h2 className="mt-4 text-2xl font-semibold md:text-3xl">{title}</h2>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">{description}</p>
      </div>
      <div className="grid grid-cols-3 gap-3 rounded-card bg-white/10 p-4 text-center">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <div key={metric.label}>
              <Icon className="mx-auto h-5 w-5 text-slate-300" aria-hidden="true" />
              <p className="mt-2 text-2xl font-bold">{metric.value}</p>
              <p className="text-xs text-slate-300">{metric.label}</p>
            </div>
          );
        })}
      </div>
    </section>
  );
}
