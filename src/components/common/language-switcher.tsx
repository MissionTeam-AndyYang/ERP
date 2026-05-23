"use client";

import { Languages } from "lucide-react";
import { useLanguage } from "@/i18n/language-provider";
import type { LanguageCode } from "@/i18n/dictionary";

export function LanguageSwitcher() {
  const { language, languages, setLanguage, t } = useLanguage();

  return (
    <label className="inline-flex h-11 items-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary">
      <Languages className="h-4 w-4" aria-hidden="true" />
      <span className="sr-only">{t("language.label")}</span>
      <select
        aria-label={t("language.label")}
        className="bg-transparent text-sm font-medium outline-none"
        value={language}
        onChange={(event) => setLanguage(event.target.value as LanguageCode)}
      >
        {languages.map((item) => (
          <option key={item.code} value={item.code}>
            {item.label}
          </option>
        ))}
      </select>
    </label>
  );
}
