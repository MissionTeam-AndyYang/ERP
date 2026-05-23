export const languages = [
  { code: "zh-TW", label: "繁中", nativeName: "繁體中文" },
  { code: "en", label: "EN", nativeName: "English" },
  { code: "ja", label: "日本語", nativeName: "日本語" },
  { code: "vi", label: "VI", nativeName: "Tiếng Việt" }
] as const;

export type LanguageCode = (typeof languages)[number]["code"];

export type TranslationKey =
  | "app.metaTitle"
  | "app.defaultTitle"
  | "app.site"
  | "app.searchPlaceholder"
  | "app.notifications"
  | "app.factoryManager"
  | "app.managerRole"
  | "language.label"
  | "nav.dashboard"
  | "nav.orders"
  | "nav.items"
  | "nav.batches"
  | "nav.bom"
  | "nav.production"
  | "nav.warehouse"
  | "nav.quality"
  | "nav.traceability"
  | "nav.logistics"
  | "nav.workforce"
  | "nav.purchasing"
  | "nav.finance"
  | "nav.ai"
  | "nav.settings"
  | "warehouse.layoutTitle";

type Dictionary = Record<TranslationKey, string>;

export const defaultLanguage: LanguageCode = "zh-TW";

export const dictionaries: Record<LanguageCode, Dictionary> = {
  "zh-TW": {
    "app.metaTitle": "ERP 2.0 智慧食品工廠平台",
    "app.defaultTitle": "智慧食品工廠 Dashboard",
    "app.site": "台中一廠",
    "app.searchPlaceholder": "搜尋工單、批號、品項",
    "app.notifications": "通知",
    "app.factoryManager": "王廠長",
    "app.managerRole": "Factory Manager",
    "language.label": "語言",
    "nav.dashboard": "Dashboard",
    "nav.orders": "訂單中心",
    "nav.items": "品項中心",
    "nav.batches": "批號中心",
    "nav.bom": "BOM 中心",
    "nav.production": "生產中心",
    "nav.warehouse": "倉庫中心",
    "nav.quality": "品保中心",
    "nav.traceability": "溯源中心",
    "nav.logistics": "物流派車",
    "nav.workforce": "人員中心",
    "nav.purchasing": "採購中心",
    "nav.finance": "財務中心",
    "nav.ai": "AI 中心",
    "nav.settings": "系統設定",
    "warehouse.layoutTitle": "倉庫管理 Warehouse Workspace"
  },
  en: {
    "app.metaTitle": "ERP 2.0 Smart Food Factory Platform",
    "app.defaultTitle": "Smart Food Factory Dashboard",
    "app.site": "Taichung Plant 1",
    "app.searchPlaceholder": "Search work orders, batches, items",
    "app.notifications": "Notifications",
    "app.factoryManager": "Plant Manager Wang",
    "app.managerRole": "Factory Manager",
    "language.label": "Language",
    "nav.dashboard": "Dashboard",
    "nav.orders": "Orders",
    "nav.items": "Items",
    "nav.batches": "Batches",
    "nav.bom": "BOM",
    "nav.production": "Production",
    "nav.warehouse": "Warehouse",
    "nav.quality": "Quality",
    "nav.traceability": "Traceability",
    "nav.logistics": "Logistics",
    "nav.workforce": "Workforce",
    "nav.purchasing": "Purchasing",
    "nav.finance": "Finance",
    "nav.ai": "AI",
    "nav.settings": "Settings",
    "warehouse.layoutTitle": "Warehouse Management Workspace"
  },
  ja: {
    "app.metaTitle": "ERP 2.0 スマート食品工場プラットフォーム",
    "app.defaultTitle": "スマート食品工場 Dashboard",
    "app.site": "台中第一工場",
    "app.searchPlaceholder": "作業指示、ロット、品目を検索",
    "app.notifications": "通知",
    "app.factoryManager": "王工場長",
    "app.managerRole": "Factory Manager",
    "language.label": "言語",
    "nav.dashboard": "Dashboard",
    "nav.orders": "受注",
    "nav.items": "品目",
    "nav.batches": "ロット",
    "nav.bom": "BOM",
    "nav.production": "生産",
    "nav.warehouse": "倉庫",
    "nav.quality": "品質",
    "nav.traceability": "トレーサビリティ",
    "nav.logistics": "物流",
    "nav.workforce": "人員",
    "nav.purchasing": "購買",
    "nav.finance": "財務",
    "nav.ai": "AI",
    "nav.settings": "設定",
    "warehouse.layoutTitle": "倉庫管理ワークスペース"
  },
  vi: {
    "app.metaTitle": "Nền tảng ERP 2.0 Nhà máy thực phẩm thông minh",
    "app.defaultTitle": "Dashboard Nhà máy thực phẩm thông minh",
    "app.site": "Nhà máy Đài Trung 1",
    "app.searchPlaceholder": "Tìm lệnh sản xuất, lô, mặt hàng",
    "app.notifications": "Thông báo",
    "app.factoryManager": "Quản lý Wang",
    "app.managerRole": "Factory Manager",
    "language.label": "Ngôn ngữ",
    "nav.dashboard": "Dashboard",
    "nav.orders": "Đơn hàng",
    "nav.items": "Mặt hàng",
    "nav.batches": "Lô",
    "nav.bom": "BOM",
    "nav.production": "Sản xuất",
    "nav.warehouse": "Kho",
    "nav.quality": "Chất lượng",
    "nav.traceability": "Truy xuất",
    "nav.logistics": "Vận chuyển",
    "nav.workforce": "Nhân sự",
    "nav.purchasing": "Mua hàng",
    "nav.finance": "Tài chính",
    "nav.ai": "AI",
    "nav.settings": "Cài đặt",
    "warehouse.layoutTitle": "Không gian quản lý kho"
  }
};
