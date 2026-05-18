import { KeyRound, Settings, ShieldCheck } from "lucide-react";
import { CompactListPanel } from "@/components/common/compact-list-panel";
import { DetailCard } from "@/components/common/detail-card";
import { ModuleHero } from "@/components/common/module-hero";
import { ModuleKpiCard } from "@/components/common/module-kpi-card";
import { ProcessBoard } from "@/components/common/process-board";
import { AppLayout } from "@/layouts/app-layout";

const kpis = [
  { label: "使用者", value: "42", hint: "8 個角色", tone: "info" as const },
  { label: "啟用模組", value: "9", hint: "ERP 核心", tone: "success" as const },
  { label: "待審核權限", value: "3", hint: "本週異動", tone: "warning" as const },
  { label: "資料串接", value: "6", hint: "2 個待設定", tone: "neutral" as const }
];

const settingCards = [
  {
    eyebrow: "ROLE-FM",
    title: "廠長 Factory Manager",
    subtitle: "Dashboard / Production / Warehouse / Finance / AI",
    status: "完整權限",
    tone: "success" as const,
    rows: [
      { label: "成員", value: "3 人" },
      { label: "審核權", value: "採購 / 財務 / 異常" },
      { label: "資料範圍", value: "台中一廠" }
    ]
  },
  {
    eyebrow: "ROLE-QA",
    title: "品保 Quality Assurance",
    subtitle: "Quality / Traceability / Dashboard",
    status: "待確認",
    tone: "warning" as const,
    rows: [
      { label: "成員", value: "7 人" },
      { label: "審核權", value: "QA 放行 / NCR" },
      { label: "限制", value: "不可看財務" }
    ]
  }
];

const settingTasks = [
  {
    id: "SYS-SET-001",
    title: "MariaDB API 串接設定",
    detail: "建立後端 API base URL、認證方式與資料同步頻率。",
    meta: "狀態：待 Backend Sprint",
    status: "待設定",
    tone: "warning" as const
  },
  {
    id: "SYS-SET-002",
    title: "PDA / 掃碼設備設定",
    detail: "設定倉儲入出庫與現場報工使用的掃碼欄位規則。",
    meta: "適用 Warehouse / Production",
    status: "規劃中",
    tone: "info" as const
  }
];

const flow = [
  {
    title: "角色",
    items: [{ id: "ROLE-008", title: "倉管", detail: "出入庫與盤點權限", tone: "info" as const }]
  },
  {
    title: "模組",
    items: [{ id: "MOD-009", title: "AI 中心", detail: "洞察與摘要啟用", tone: "success" as const }]
  },
  {
    title: "資料",
    items: [{ id: "API-002", title: "MariaDB", detail: "待後端連線", tone: "warning" as const }]
  },
  {
    title: "稽核",
    items: [{ id: "AUD-011", title: "權限異動", detail: "保留 180 天紀錄", tone: "neutral" as const }]
  }
];

export default function SettingsPage() {
  return (
    <AppLayout activePath="/settings" title="系統設定 System Settings">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <ModuleHero
          badge="Sprint 10 Settings"
          title="系統設定、角色權限與整體導覽"
          description="集中管理角色、模組、資料串接、掃碼規則與稽核紀錄，讓 ERP Prototype 具備完整產品導覽閉環。"
          metrics={[
            { label: "角色", value: "8", icon: ShieldCheck },
            { label: "權限", value: "42", icon: KeyRound },
            { label: "設定", value: "6", icon: Settings }
          ]}
        />
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {kpis.map((item) => <ModuleKpiCard {...item} key={item.label} />)}
        </section>
        <ProcessBoard eyebrow="System Governance" title="系統治理看板" columns={flow} />
        <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div className="grid gap-4">
            {settingCards.map((item) => <DetailCard {...item} key={item.eyebrow} />)}
          </div>
          <CompactListPanel eyebrow="Setup Tasks" title="待設定項目" items={settingTasks} />
        </section>
      </div>
    </AppLayout>
  );
}
