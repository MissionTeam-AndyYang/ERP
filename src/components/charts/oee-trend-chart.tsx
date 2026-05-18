"use client";

import {
  CartesianGrid,
  Line,
  LineChart,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import { ChartCard } from "@/components/charts/chart-card";
import type { OeeTrendPoint } from "@/types/dashboard";

type OeeTrendChartProps = {
  data: OeeTrendPoint[];
};

export function OeeTrendChart({ data }: OeeTrendChartProps) {
  return (
    <ChartCard title="OEE 趨勢" subtitle="Equipment Effectiveness">
      <div className="h-[260px] min-w-0">
          <LineChart
            data={data}
            margin={{ left: -18, right: 8, top: 8, bottom: 0 }}
            responsive
            style={{ height: "100%", width: "100%" }}
          >
            <CartesianGrid stroke="#E2E8F0" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="time" tickLine={false} axisLine={false} tick={{ fill: "#64748B", fontSize: 12 }} />
            <YAxis domain={[70, 95]} tickLine={false} axisLine={false} tick={{ fill: "#64748B", fontSize: 12 }} />
            <Tooltip
              formatter={(value) => [`${value}%`, ""]}
              contentStyle={{
                border: "1px solid #E2E8F0",
                borderRadius: 12,
                boxShadow: "0 8px 24px rgba(15, 23, 42, 0.12)"
              }}
            />
            <Line
              type="monotone"
              dataKey="target"
              name="目標"
              stroke="#94A3B8"
              strokeDasharray="5 5"
              strokeWidth={2}
              dot={false}
            />
            <Line
              type="monotone"
              dataKey="oee"
              name="OEE"
              stroke="#06B6D4"
              strokeWidth={3}
              dot={{ r: 3, strokeWidth: 2 }}
              activeDot={{ r: 5 }}
            />
          </LineChart>
      </div>
    </ChartCard>
  );
}
