"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import { ChartCard } from "@/components/charts/chart-card";
import type { ProductionTrendPoint } from "@/types/dashboard";

type ProductionTrendChartProps = {
  data: ProductionTrendPoint[];
};

export function ProductionTrendChart({ data }: ProductionTrendChartProps) {
  return (
    <ChartCard title="生產趨勢" subtitle="Production Trend">
      <div className="h-[280px] min-w-0">
          <AreaChart
            data={data}
            margin={{ left: -10, right: 8, top: 8, bottom: 0 }}
            responsive
            style={{ height: "100%", width: "100%" }}
          >
            <defs>
              <linearGradient id="actualOutput" x1="0" x2="0" y1="0" y2="1">
                <stop offset="5%" stopColor="#2563EB" stopOpacity={0.26} />
                <stop offset="95%" stopColor="#2563EB" stopOpacity={0.02} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="#E2E8F0" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="time" tickLine={false} axisLine={false} tick={{ fill: "#64748B", fontSize: 12 }} />
            <YAxis tickLine={false} axisLine={false} tick={{ fill: "#64748B", fontSize: 12 }} />
            <Tooltip
              contentStyle={{
                border: "1px solid #E2E8F0",
                borderRadius: 12,
                boxShadow: "0 8px 24px rgba(15, 23, 42, 0.12)"
              }}
            />
            <Area
              type="monotone"
              dataKey="planned"
              name="計畫產量"
              stroke="#94A3B8"
              strokeDasharray="5 5"
              fill="transparent"
              strokeWidth={2}
            />
            <Area
              type="monotone"
              dataKey="actual"
              name="實際產量"
              stroke="#2563EB"
              fill="url(#actualOutput)"
              strokeWidth={3}
            />
          </AreaChart>
      </div>
    </ChartCard>
  );
}
