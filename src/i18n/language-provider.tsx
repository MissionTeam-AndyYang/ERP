"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import {
  defaultLanguage,
  dictionaries,
  languages,
  type LanguageCode,
  type TranslationKey
} from "@/i18n/dictionary";

type LanguageContextValue = {
  language: LanguageCode;
  languages: typeof languages;
  setLanguage: (language: LanguageCode) => void;
  t: (key: TranslationKey) => string;
};

const LanguageContext = createContext<LanguageContextValue | null>(null);
const storageKey = "erp-language";

function isLanguageCode(value: string | null): value is LanguageCode {
  return languages.some((language) => language.code === value);
}

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<LanguageCode>(() => {
    if (typeof window === "undefined") {
      return defaultLanguage;
    }

    const savedLanguage = window.localStorage.getItem(storageKey);
    return isLanguageCode(savedLanguage) ? savedLanguage : defaultLanguage;
  });

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  const setLanguage = useCallback((nextLanguage: LanguageCode) => {
    setLanguageState(nextLanguage);
    window.localStorage.setItem(storageKey, nextLanguage);
  }, []);

  const t = useCallback(
    (key: TranslationKey) => dictionaries[language][key] ?? dictionaries[defaultLanguage][key],
    [language]
  );

  const value = useMemo(
    () => ({
      language,
      languages,
      setLanguage,
      t
    }),
    [language, setLanguage, t]
  );

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useLanguage() {
  const context = useContext(LanguageContext);

  if (!context) {
    throw new Error("useLanguage must be used within LanguageProvider");
  }

  return context;
}
