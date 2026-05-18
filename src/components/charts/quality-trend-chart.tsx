"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import { ChartCard } from "@/components/charts/chart-card";
import type { QualityTrendPoint } from "@/types/dashboard";

type QualityTrendChartProps = {
  data: QualityTrendPoint[];
};

export function QualityTrendChart({ data }: QualityTrendChartProps) {
  return (
    <ChartCard title="良率趨勢" subtitle="Quality Yield">
      <div className="h-[260px] min-w-0">
          <BarChart
            data={data}
            margin={{ left: -18, right: 8, top: 8, bottom: 0 }}
            responsive
            style={{ height: "100%", width: "100%" }}
          >
            <CartesianGrid stroke="#E2E8F0" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="date" tickLine={false} axisLine={false} tick={{ fill: "#64748B", fontSize: 12 }} />
            <YAxis yAxisId="yield" domain={[96, 100]} tickLine={false} axisLine={false} tick={{ fill: "#64748B", fontSize: 12 }} />
            <YAxis yAxisId="rework" orientation="right" hide domain={[0, 3]} />
            <Tooltip
              formatter={(value, name) => [`${value}%`, name === "yieldRate" ? "良率" : "重工率"]}
              contentStyle={{
                border: "1px solid #E2E8F0",
                borderRadius: 12,
                boxShadow: "0 8px 24px rgba(15, 23, 42, 0.12)"
              }}
            />
            <Bar yAxisId="rework" dataKey="reworkRate" name="重工率" fill="#F59E0B" radius={[6, 6, 0, 0]} />
            <Line
              yAxisId="yield"
              type="monotone"
              dataKey="yieldRate"
              name="良率"
              stroke="#22C55E"
              strokeWidth={3}
              dot={{ r: 3, strokeWidth: 2 }}
            />
          </BarChart>
      </div>
    </ChartCard>
  );
}
