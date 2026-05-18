import { ClipboardList, ShoppingCart, Truck } from "lucide-react";
import { CompactListPanel } from "@/components/common/compact-list-panel";
import { DetailCard } from "@/components/common/detail-card";
import { ModuleHero } from "@/components/common/module-hero";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { ProcessBoard } from "@/components/common/process-board";
import { AppLayout } from "@/layouts/app-layout";

const kpis = [
  { label: "待採購需求", value: "18", hint: "5 筆急件", tone: "warning" as const },
  { label: "本月採購額", value: "8.4M", hint: "-3.1%", tone: "success" as const },
  { label: "待交貨 PO", value: "26", hint: "7 筆今日到貨", tone: "info" as const },
  { label: "供應商異常", value: "3", hint: "需追蹤", tone: "danger" as const }
];

const poCards = [
  {
    eyebrow: "PO-240512-031",
    title: "冷凍玉米粒補貨採購",
    subtitle: "供應商：綠田食品 / 關聯 B2 待料",
    status: "待核准",
    tone: "warning" as const,
    rows: [
      { label: "數量", value: "1,200 kg" },
      { label: "金額", value: "NT$ 86,400" },
      { label: "預計到貨", value: "05/13 09:30" }
    ]
  },
  {
    eyebrow: "PO-240512-029",
    title: "耐熱殺菌袋追加採購",
    subtitle: "供應商：台灣包材 / 包材安全庫存不足",
    status: "已下單",
    tone: "info" as const,
    rows: [
      { label: "數量", value: "20,000 只" },
      { label: "金額", value: "NT$ 132,000" },
      { label: "預計到貨", value: "05/15 14:00" }
    ]
  }
];

const supplierAlerts = [
  {
    id: "SUP-AL-004",
    title: "綠田食品 COA 文件延遲",
    detail: "影響 RM240506-CORN 溯源文件完整率，需採購追補。",
    meta: "關聯 PO-240512-031",
    status: "追蹤中",
    tone: "warning" as const
  },
  {
    id: "SUP-AL-005",
    title: "包材交期風險",
    detail: "耐熱殺菌袋交期可能延後 1 天，建議確認替代供應商。",
    meta: "關聯 PK-BAG-010",
    status: "需決策",
    tone: "danger" as const
  }
];

const purchasingFlow = [
  {
    title: "請購",
    items: [{ id: "PR-018", title: "玉米粒補貨", detail: "低於安全庫存", tone: "warning" as const }]
  },
  {
    title: "比價",
    items: [{ id: "RFQ-011", title: "包材替代商", detail: "2 家供應商回覆", tone: "info" as const }]
  },
  {
    title: "核准",
    items: [{ id: "PO-031", title: "冷凍玉米粒", detail: "等待主管核准", tone: "warning" as const }]
  },
  {
    title: "到貨",
    items: [{ id: "PO-027", title: "雞胸肉原料", detail: "今日 10:40 驗收", tone: "success" as const }]
  }
];

export default function PurchasingPage() {
  return (
    <AppLayout activePath="/purchasing" title="採購中心 Purchasing Module">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="Sprint 7 Purchasing"
          title="採購、補貨與供應商協作中心"
          description="串接安全庫存、請購、比價、採購單與到貨驗收，讓缺料風險可以提早轉成可追蹤採購任務。"
          metrics={[
            { label: "採購需求", value: "18", icon: ShoppingCart },
            { label: "待交貨", value: "26", icon: Truck },
            { label: "待核准", value: "7", icon: ClipboardList }
          ]}
        />
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>
        <ProcessBoard eyebrow="Purchasing Workflow" title="採購流程看板" columns={purchasingFlow} />
        <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div className="grid gap-4">
            {poCards.map((item) => <DetailCard {...item} key={item.eyebrow} />)}
          </div>
          <CompactListPanel eyebrow="Supplier Alerts" title="供應商與交期提醒" items={supplierAlerts} />
        </section>
      </div>
    </AppLayout>
  );
}
