import "./globals.css";
import type { Metadata } from "next";
import { LanguageProvider } from "@/i18n/language-provider";

export const metadata: Metadata = {
  title: "ERP 2.0 智慧食品工廠平台",
  description: "Smart Food Factory ERP / MES Platform"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-TW">
      <body>
        <LanguageProvider>{children}</LanguageProvider>
      </body>
    </html>
  );
}
