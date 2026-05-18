import { CalendarDays, IdCard, UsersRound } from "lucide-react";
import { CompactListPanel } from "@/components/common/compact-list-panel";
import { DetailCard } from "@/components/common/detail-card";
import { ModuleHero } from "@/components/common/module-hero";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { ProcessBoard } from "@/components/common/process-board";
import { AppLayout } from "@/layouts/app-layout";

const kpis = [
  { label: "今日出勤", value: "86", hint: "92% 到勤", tone: "success" as const },
  { label: "產線人力", value: "42", hint: "A1 滿編", tone: "info" as const },
  { label: "待補班", value: "3", hint: "晚班缺口", tone: "warning" as const },
  { label: "證照到期", value: "2", hint: "需複訓", tone: "danger" as const }
];

const staffCards = [
  {
    eyebrow: "EMP-0008",
    title: "林組長",
    subtitle: "生產部 / A1 調理包產線 / 日班",
    status: "當班",
    tone: "success" as const,
    rows: [
      { label: "負責", value: "MO-240512-001" },
      { label: "技能", value: "調理 / 殺菌 / 報工" },
      { label: "班別", value: "08:00-17:00" }
    ]
  },
  {
    eyebrow: "EMP-0021",
    title: "吳品保",
    subtitle: "品保部 / 首件檢驗 / 日班",
    status: "檢驗中",
    tone: "info" as const,
    rows: [
      { label: "負責", value: "QC-240512-018" },
      { label: "技能", value: "金檢 / 微生物快篩" },
      { label: "班別", value: "08:30-17:30" }
    ]
  },
  {
    eyebrow: "DRV-0012",
    title: "陳志明",
    subtitle: "物流部 / 冷凍車司機 / 中區路線",
    status: "裝車中",
    tone: "warning" as const,
    rows: [
      { label: "車趟", value: "DLV-240512-008" },
      { label: "證照", value: "職業大貨車 / 冷鏈" },
      { label: "班別", value: "09:00-18:00" }
    ]
  }
];

const alerts = [
  {
    id: "HR-AL-001",
    title: "晚班 B2 產線缺 1 名操作員",
    detail: "若 B2 延後開線，晚班需補具冷凍蔬菜產線經驗人員。",
    meta: "關聯 MO-240512-002",
    status: "待排班",
    tone: "warning" as const
  },
  {
    id: "HR-AL-002",
    title: "冷鏈配送證照即將到期",
    detail: "2 名司機冷鏈訓練證照 30 天內到期，需安排複訓。",
    meta: "關聯 Logistics",
    status: "需複訓",
    tone: "danger" as const
  }
];

const roster = [
  {
    title: "生產",
    items: [{ id: "A1-DAY", title: "A1 日班", detail: "12/12 到勤", tone: "success" as const }]
  },
  {
    title: "倉儲",
    items: [{ id: "WH-DAY", title: "冷凍庫日班", detail: "8/9 到勤", tone: "warning" as const }]
  },
  {
    title: "品保",
    items: [{ id: "QA-DAY", title: "首件檢驗", detail: "5/5 到勤", tone: "info" as const }]
  },
  {
    title: "物流",
    items: [{ id: "LOG-DAY", title: "中區配送", detail: "3 車趟進行中", tone: "success" as const }]
  }
];

export default function WorkforcePage() {
  return (
    <AppLayout activePath="/workforce" title="人員員工中心 Workforce Module">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="Phase 1.6 Workforce"
          title="人員、班表、角色與責任配置"
          description="管理今日出勤、班表、部門角色、產線配置、工單負責人、品保檢驗員、倉管與司機，讓營運責任可追蹤。"
          metrics={[
            { label: "出勤", value: "86", icon: UsersRound },
            { label: "班表", value: "12", icon: CalendarDays },
            { label: "角色", value: "8", icon: IdCard }
          ]}
        />
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>
        <ProcessBoard eyebrow="Roster Board" title="今日人員配置看板" columns={roster} />
        <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div className="grid gap-4">
            {staffCards.map((item) => <DetailCard {...item} key={item.eyebrow} />)}
          </div>
          <CompactListPanel eyebrow="Workforce Alerts" title="人力與證照提醒" items={alerts} />
        </section>
      </div>
    </AppLayout>
  );
}
