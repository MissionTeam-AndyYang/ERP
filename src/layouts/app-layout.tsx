import {
  Barcode,
  Bell,
  ClipboardList,
  DollarSign,
  Factory,
  FlaskConical,
  Home,
  IdCard,
  PackageSearch,
  Search,
  Settings,
  Shield,
  ShoppingCart,
  Sparkles,
  Truck,
  Warehouse
} from "lucide-react";
import { NavLink } from "@/components/common/nav-link";

const navItems = [
  { label: "Dashboard", icon: Home, href: "/" },
  { label: "訂單中心", icon: ClipboardList, href: "/orders" },
  { label: "品項中心", icon: PackageSearch, href: "/items" },
  { label: "批號中心", icon: Barcode, href: "/batches" },
  { label: "BOM 中心", icon: FlaskConical, href: "/bom" },
  { label: "生產中心", icon: Factory, href: "/production" },
  { label: "倉儲中心", icon: Warehouse, href: "/warehouse" },
  { label: "品保中心", icon: Shield, href: "/quality" },
  { label: "溯源中心", icon: Search, href: "/traceability" },
  { label: "物流派車", icon: Truck, href: "/logistics" },
  { label: "人員中心", icon: IdCard, href: "/workforce" },
  { label: "採購中心", icon: ShoppingCart, href: "/purchasing" },
  { label: "財務中心", icon: DollarSign, href: "/finance" },
  { label: "AI 中心", icon: Sparkles, href: "/ai" },
  { label: "系統設定", icon: Settings, href: "/settings" }
];

type AppLayoutProps = {
  children: React.ReactNode;
  activePath?: string;
  title?: string;
  site?: string;
};

export function AppLayout({
  children,
  activePath = "/",
  title = "智慧食品工廠 Dashboard",
  site = "台中一廠"
}: AppLayoutProps) {
  return (
    <div className="min-h-screen bg-appBg text-textPrimary">
      <aside className="fixed inset-y-0 left-0 hidden w-[280px] bg-primaryDark text-white lg:block">
        <div className="flex h-[72px] items-center border-b border-white/10 px-6">
          <div>
            <p className="text-lg font-bold">ERP 2.0</p>
            <p className="text-xs text-slate-300">Smart Food Factory</p>
          </div>
        </div>
        <nav className="space-y-1 px-4 py-5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = item.href === activePath;
            return (
              <NavLink
                href={item.href}
                key={item.label}
                className={`flex h-11 items-center gap-3 rounded-button px-3 text-sm font-medium transition ${
                  isActive
                    ? "bg-primary text-white"
                    : "text-slate-300 hover:bg-white/10 hover:text-white"
                }`}
              >
                <Icon className="h-4 w-4" aria-hidden="true" />
                {item.label}
              </NavLink>
            );
          })}
        </nav>
      </aside>

      <div className="lg:pl-[280px]">
        <header className="sticky top-0 z-10 flex h-[72px] items-center justify-between gap-3 border-b border-border bg-white/95 px-4 backdrop-blur md:px-6">
          <div className="min-w-0">
            <p className="text-xs font-medium text-textSecondary">{site}</p>
            <h1 className="truncate text-lg font-semibold text-textPrimary md:text-xl">
              {title}
            </h1>
          </div>
          <div className="flex items-center gap-3">
            <label className="hidden h-11 min-w-[280px] items-center gap-2 rounded-input border border-border bg-slate-50 px-3 md:flex">
              <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
              <input
                className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                placeholder="搜尋工單、批號、品項"
              />
            </label>
            <button className="grid h-11 w-11 place-items-center rounded-button border border-border bg-white text-textSecondary">
              <Bell className="h-5 w-5" aria-hidden="true" />
              <span className="sr-only">通知</span>
            </button>
            <div className="hidden text-right sm:block">
              <p className="text-sm font-semibold text-textPrimary">王廠長</p>
              <p className="text-xs text-textSecondary">Factory Manager</p>
            </div>
          </div>
        </header>
        <nav className="flex gap-2 overflow-x-auto border-b border-border bg-white px-4 py-3 lg:hidden">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = item.href === activePath;
            return (
              <NavLink
                href={item.href}
                key={item.label}
                className={`inline-flex h-10 shrink-0 items-center gap-2 rounded-button px-3 text-sm font-medium ${
                  isActive
                    ? "bg-primary text-white"
                    : "bg-slate-50 text-textSecondary"
                }`}
              >
                <Icon className="h-4 w-4" aria-hidden="true" />
                {item.label}
              </NavLink>
            );
          })}
        </nav>
        <main className="p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
}
