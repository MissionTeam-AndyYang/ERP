"use client";

import { Cell, Pie, PieChart, Tooltip } from "recharts";
import { ChartCard } from "@/components/charts/chart-card";
import type { AlertDistributionItem, StatusTone } from "@/types/dashboard";

const colors: Record<StatusTone, string> = {
  success: "#22C55E",
  warning: "#F59E0B",
  danger: "#EF4444",
  info: "#06B6D4",
  neutral: "#64748B"
};

type AlertDistributionChartProps = {
  data: AlertDistributionItem[];
};

export function AlertDistributionChart({ data }: AlertDistributionChartProps) {
  return (
    <ChartCard title="異常分類" subtitle="Alert Distribution">
      <div className="grid gap-3 sm:grid-cols-[180px_1fr]">
        <div className="h-[210px] min-w-0">
            <PieChart responsive style={{ height: "100%", width: "100%" }}>
              <Tooltip
                formatter={(value) => [`${value}%`, "占比"]}
                contentStyle={{
                  border: "1px solid #E2E8F0",
                  borderRadius: 12,
                  boxShadow: "0 8px 24px rgba(15, 23, 42, 0.12)"
                }}
              />
              <Pie data={data} dataKey="value" nameKey="name" innerRadius={54} outerRadius={82} paddingAngle={3}>
                {data.map((item) => (
                  <Cell fill={colors[item.tone]} key={item.name} />
                ))}
              </Pie>
            </PieChart>
        </div>
        <div className="flex flex-col justify-center gap-3">
          {data.map((item) => (
            <div className="flex items-center justify-between gap-4" key={item.name}>
              <div className="flex items-center gap-2">
                <span
                  className="h-2.5 w-2.5 rounded-full"
                  style={{ backgroundColor: colors[item.tone] }}
                />
                <span className="text-sm font-medium text-textPrimary">{item.name}</span>
              </div>
              <span className="text-sm text-textSecondary">{item.value}%</span>
            </div>
          ))}
        </div>
      </div>
    </ChartCard>
  );
}
