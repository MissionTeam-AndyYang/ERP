import { Boxes, FileSearch, Network } from "lucide-react";
import { CompactListPanel } from "@/components/common/compact-list-panel";
import { DetailCard } from "@/components/common/detail-card";
import { ModuleHero } from "@/components/common/module-hero";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { ProcessBoard } from "@/components/common/process-board";
import { AppLayout } from "@/layouts/app-layout";

const kpis = [
  { label: "可追溯批號", value: "1,284", hint: "近 90 天", tone: "info" as const },
  { label: "完整鏈路率", value: "99.2%", hint: "+0.4%", tone: "success" as const },
  { label: "待補資料", value: "7", hint: "含 2 筆供應商", tone: "warning" as const },
  { label: "召回模擬", value: "3", hint: "本月演練", tone: "neutral" as const }
];

const traceCards = [
  {
    eyebrow: "TRACE-B240512-A101",
    title: "咖哩雞肉調理包批號鏈路",
    subtitle: "成品批號 B240512-A101 / 出貨批次 SH-240512-08",
    status: "鏈路完整",
    tone: "success" as const,
    rows: [
      { label: "原料", value: "雞胸肉 RM240512-CHK" },
      { label: "製程", value: "A1 調理 / 金檢通過" },
      { label: "出貨", value: "全聯中區 DC" }
    ]
  },
  {
    eyebrow: "TRACE-RM240506-CORN",
    title: "冷凍玉米粒原料去向",
    subtitle: "供應商：綠田食品 / 入庫 WH-IN-240506-011",
    status: "需補文件",
    tone: "warning" as const,
    rows: [
      { label: "使用批號", value: "B240512-B207" },
      { label: "庫位", value: "FZ-A03-02" },
      { label: "缺漏", value: "COA 電子檔" }
    ]
  }
];

const recallTasks = [
  {
    id: "RC-240512-001",
    title: "玉米粒供應商文件追補",
    detail: "補齊 RM240506-CORN 的 COA 與運輸溫度紀錄。",
    meta: "負責：採購 / 品保，期限 15:00",
    status: "追蹤中",
    tone: "warning" as const
  },
  {
    id: "RC-240512-002",
    title: "B240512-A101 召回範圍模擬",
    detail: "依成品批號回推原料、產線、客戶與出貨單。",
    meta: "預估影響 2,400 盒",
    status: "已完成",
    tone: "success" as const
  }
];

const chain = [
  {
    title: "供應商",
    items: [{ id: "SUP-022", title: "綠田食品", detail: "原料 COA / 運輸溫度", tone: "info" as const }]
  },
  {
    title: "入庫",
    items: [{ id: "WH-IN-011", title: "冷凍玉米粒", detail: "FZ-A03-02 / 180 kg", tone: "warning" as const }]
  },
  {
    title: "製程",
    items: [{ id: "MO-002", title: "綜合冷凍蔬菜", detail: "B2 產線 / 待料", tone: "warning" as const }]
  },
  {
    title: "出貨",
    items: [{ id: "SH-008", title: "中區 DC", detail: "待建立成品出貨", tone: "neutral" as const }]
  }
];

export default function TraceabilityPage() {
  return (
    <AppLayout activePath="/traceability" title="溯源中心 Traceability Module">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="Sprint 6 Traceability"
          title="食品批號與供應鏈追溯中心"
          description="將供應商、入庫、製程、品保與出貨串成可查詢鏈路，支援食品安全稽核與召回模擬。"
          metrics={[
            { label: "批號鏈路", value: "1,284", icon: Network },
            { label: "追溯查詢", value: "46", icon: FileSearch },
            { label: "關聯庫位", value: "32", icon: Boxes }
          ]}
        />
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>
        <ProcessBoard eyebrow="Trace Chain" title="批號追溯鏈路" columns={chain} />
        <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div className="grid gap-4">
            {traceCards.map((item) => <DetailCard {...item} key={item.eyebrow} />)}
          </div>
          <CompactListPanel eyebrow="Recall Tasks" title="召回 / 文件追蹤" items={recallTasks} />
        </section>
      </div>
    </AppLayout>
  );
}
