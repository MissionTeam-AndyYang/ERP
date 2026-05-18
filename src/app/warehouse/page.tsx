import { Boxes, ClipboardList, PackageSearch } from "lucide-react";
import { ExpiryBatchTable } from "@/components/warehouse/expiry-batch-table";
import { InventoryCard } from "@/components/warehouse/inventory-card";
import { WarehouseKpiCard } from "@/components/warehouse/warehouse-kpi-card";
import { WarehouseTaskList } from "@/components/warehouse/warehouse-task-list";
import { StatusBadge } from "@/components/ui/status-badge";
import { AppLayout } from "@/layouts/app-layout";
import {
  expiryBatches,
  inventoryItems,
  warehouseKpis,
  warehouseTasks
} from "@/mock/warehouse";

export default function WarehousePage() {
  return (
    <AppLayout activePath="/warehouse" title="倉儲中心 Warehouse Module">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <section className="flex flex-col justify-between gap-4 rounded-card bg-primaryDark p-6 text-white shadow-card md:flex-row md:items-center">
          <div>
            <StatusBadge tone="info">Sprint 4 Warehouse</StatusBadge>
            <h2 className="mt-4 text-2xl font-semibold md:text-3xl">庫存、批號與入出庫控制台</h2>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">
              以批號與效期為核心管理原料、成品、包材與庫位，協助倉管即時掌握安全庫存、即期品與今日入出庫任務。
            </p>
          </div>
          <div className="grid grid-cols-3 gap-3 rounded-card bg-white/10 p-4 text-center">
            <div>
              <Boxes className="mx-auto h-5 w-5 text-slate-300" aria-hidden="true" />
              <p className="mt-2 text-2xl font-bold">428</p>
              <p className="text-xs text-slate-300">庫存品項</p>
            </div>
            <div>
              <PackageSearch className="mx-auto h-5 w-5 text-slate-300" aria-hidden="true" />
              <p className="mt-2 text-2xl font-bold">9</p>
              <p className="text-xs text-slate-300">即期批號</p>
            </div>
            <div>
              <ClipboardList className="mx-auto h-5 w-5 text-slate-300" aria-hidden="true" />
              <p className="mt-2 text-2xl font-bold">23</p>
              <p className="text-xs text-slate-300">待處理任務</p>
            </div>
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {warehouseKpis.map((item) => (
            <WarehouseKpiCard item={item} key={item.label} />
          ))}
        </section>

        <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
          <div className="space-y-4">
            <div className="flex flex-col justify-between gap-3 md:flex-row md:items-center">
              <div>
                <p className="text-sm font-medium text-textSecondary">Inventory</p>
                <h2 className="text-xl font-semibold text-textPrimary">原料 / 成品庫存卡片</h2>
              </div>
              <div className="flex flex-wrap gap-2">
                <StatusBadge tone="success">庫存正常</StatusBadge>
                <StatusBadge tone="warning">低於安全庫存</StatusBadge>
                <StatusBadge tone="danger">需採購</StatusBadge>
              </div>
            </div>
            <div className="grid gap-4 lg:grid-cols-2">
              {inventoryItems.map((item) => (
                <InventoryCard item={item} key={item.sku} />
              ))}
            </div>
          </div>

          <WarehouseTaskList tasks={warehouseTasks} />
        </section>

        <ExpiryBatchTable batches={expiryBatches} />
      </div>
    </AppLayout>
  );
}
