import { MapPinned, ThermometerSnowflake, Truck } from "lucide-react";
import { CompactListPanel } from "@/components/common/compact-list-panel";
import { DetailCard } from "@/components/common/detail-card";
import { ModuleHero } from "@/components/common/module-hero";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { ProcessBoard } from "@/components/common/process-board";
import { AppLayout } from "@/layouts/app-layout";

const kpis = [
  { label: "今日車趟", value: "18", hint: "6 趟配送中", tone: "info" as const },
  { label: "待派車", value: "5", hint: "含 2 筆急單", tone: "warning" as const },
  { label: "準時率", value: "96%", hint: "+2.1%", tone: "success" as const },
  { label: "溫層異常", value: "1", hint: "需追蹤", tone: "danger" as const }
];

const deliveryCards = [
  {
    eyebrow: "DLV-240512-008",
    title: "全聯中區 DC 冷凍配送",
    subtitle: "關聯訂單 SO-240512-018 / 出貨批號 SH-240512-08",
    status: "裝車中",
    tone: "info" as const,
    rows: [
      { label: "車輛", value: "KLA-2389 冷凍車" },
      { label: "司機", value: "陳志明" },
      { label: "溫層", value: "-18°C" }
    ]
  },
  {
    eyebrow: "DLV-240512-011",
    title: "CVS 北區新品試賣配送",
    subtitle: "關聯訂單 SO-240512-022 / 番茄牛肉燉飯",
    status: "待派車",
    tone: "warning" as const,
    rows: [
      { label: "車輛", value: "待安排" },
      { label: "路線", value: "北區 3 點" },
      { label: "到貨", value: "05/16 10:30" }
    ]
  }
];

const alerts = [
  {
    id: "LOG-AL-001",
    title: "DLV-240512-011 尚未派車",
    detail: "新品試賣訂單需冷藏配送，建議優先安排北區冷藏車。",
    meta: "關聯 SO-240512-022",
    status: "待調度",
    tone: "warning" as const
  },
  {
    id: "LOG-AL-002",
    title: "KLA-2389 回傳溫度短暫偏高",
    detail: "裝車門開啟期間溫度升至 -14°C，已回穩但需保留紀錄。",
    meta: "關聯 DLV-240512-008",
    status: "觀察",
    tone: "danger" as const
  }
];

const flow = [
  {
    title: "待派車",
    items: [{ id: "DLV-011", title: "CVS 北區配送", detail: "冷藏車待安排", tone: "warning" as const }]
  },
  {
    title: "裝車中",
    items: [{ id: "DLV-008", title: "全聯中區 DC", detail: "批號 SH-240512-08", tone: "info" as const }]
  },
  {
    title: "配送中",
    items: [{ id: "DLV-006", title: "餐飲通路", detail: "路線南區 5 點", tone: "success" as const }]
  },
  {
    title: "已簽收",
    items: [{ id: "DLV-004", title: "便利商店 DC", detail: "電子簽收完成", tone: "neutral" as const }]
  }
];

export default function LogisticsPage() {
  return (
    <AppLayout activePath="/logistics" title="物流派車中心 Logistics Module">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="Phase 1.6 Logistics"
          title="出貨、派車、溫層與簽收管理"
          description="串接訂單、批號、倉儲出庫與冷鏈配送，追蹤車趟、司機、車輛、路線、溫層與簽收狀態。"
          metrics={[
            { label: "車趟", value: "18", icon: Truck },
            { label: "溫層", value: "-18°C", icon: ThermometerSnowflake },
            { label: "路線", value: "7", icon: MapPinned }
          ]}
        />
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>
        <ProcessBoard eyebrow="Delivery Workflow" title="物流派車流程看板" columns={flow} />
        <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div className="grid gap-4">
            {deliveryCards.map((item) => <DetailCard {...item} key={item.eyebrow} />)}
          </div>
          <CompactListPanel eyebrow="Dispatch Alerts" title="派車與冷鏈提醒" items={alerts} />
        </section>
      </div>
    </AppLayout>
  );
}
