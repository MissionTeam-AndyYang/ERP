"use client";

import {
  Barcode,
  Bell,
  CalendarRange,
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
import { LanguageSwitcher } from "@/components/common/language-switcher";
import { NavLink } from "@/components/common/nav-link";
import type { TranslationKey } from "@/i18n/dictionary";
import { useLanguage } from "@/i18n/language-provider";

const navItems: { labelKey: TranslationKey; icon: typeof Home; href: string }[] = [
  { labelKey: "nav.dashboard", icon: Home, href: "/" },
  { labelKey: "nav.orders", icon: ClipboardList, href: "/orders" },
  { labelKey: "nav.planning", icon: CalendarRange, href: "/planning" },
  { labelKey: "nav.items", icon: PackageSearch, href: "/items" },
  { labelKey: "nav.batches", icon: Barcode, href: "/batches" },
  { labelKey: "nav.bom", icon: FlaskConical, href: "/bom" },
  { labelKey: "nav.production", icon: Factory, href: "/production" },
  { labelKey: "nav.warehouse", icon: Warehouse, href: "/warehouse" },
  { labelKey: "nav.quality", icon: Shield, href: "/quality" },
  { labelKey: "nav.traceability", icon: Search, href: "/traceability" },
  { labelKey: "nav.logistics", icon: Truck, href: "/logistics" },
  { labelKey: "nav.workforce", icon: IdCard, href: "/workforce" },
  { labelKey: "nav.purchasing", icon: ShoppingCart, href: "/purchasing" },
  { labelKey: "nav.finance", icon: DollarSign, href: "/finance" },
  { labelKey: "nav.ai", icon: Sparkles, href: "/ai" },
  { labelKey: "nav.settings", icon: Settings, href: "/settings" }
];

type AppLayoutProps = {
  children: React.ReactNode;
  activePath?: string;
  title?: string;
  titleKey?: TranslationKey;
  site?: string;
  siteKey?: TranslationKey;
};

export function AppLayout({
  children,
  activePath = "/",
  title,
  titleKey = "app.defaultTitle",
  site,
  siteKey = "app.site"
}: AppLayoutProps) {
  const { t } = useLanguage();
  const resolvedTitle = title ?? t(titleKey);
  const resolvedSite = site ?? t(siteKey);

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
                key={item.href}
                className={`flex h-11 items-center gap-3 rounded-button px-3 text-sm font-medium transition ${
                  isActive
                    ? "bg-primary text-white"
                    : "text-slate-300 hover:bg-white/10 hover:text-white"
                }`}
              >
                <Icon className="h-4 w-4" aria-hidden="true" />
                {t(item.labelKey)}
              </NavLink>
            );
          })}
        </nav>
      </aside>

      <div className="lg:pl-[280px]">
        <header className="sticky top-0 z-10 flex h-[72px] items-center justify-between gap-3 border-b border-border bg-white/95 px-4 backdrop-blur md:px-6">
          <div className="min-w-0">
            <p className="text-xs font-medium text-textSecondary">{resolvedSite}</p>
            <h1 className="truncate text-lg font-semibold text-textPrimary md:text-xl">
              {resolvedTitle}
            </h1>
          </div>
          <div className="flex items-center gap-3">
            <label className="hidden h-11 min-w-[280px] items-center gap-2 rounded-input border border-border bg-slate-50 px-3 md:flex">
              <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
              <input
                className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                placeholder={t("app.searchPlaceholder")}
              />
            </label>
            <LanguageSwitcher />
            <button className="grid h-11 w-11 place-items-center rounded-button border border-border bg-white text-textSecondary">
              <Bell className="h-5 w-5" aria-hidden="true" />
              <span className="sr-only">{t("app.notifications")}</span>
            </button>
            <div className="hidden text-right sm:block">
              <p className="text-sm font-semibold text-textPrimary">{t("app.factoryManager")}</p>
              <p className="text-xs text-textSecondary">{t("app.managerRole")}</p>
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
                key={item.href}
                className={`inline-flex h-10 shrink-0 items-center gap-2 rounded-button px-3 text-sm font-medium ${
                  isActive
                    ? "bg-primary text-white"
                    : "bg-slate-50 text-textSecondary"
                }`}
              >
                <Icon className="h-4 w-4" aria-hidden="true" />
                {t(item.labelKey)}
              </NavLink>
            );
          })}
        </nav>
        <main className="p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
}
