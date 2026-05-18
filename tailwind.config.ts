import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/layouts/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: "#2563EB",
        primaryDark: "#1E293B",
        success: "#22C55E",
        warning: "#F59E0B",
        danger: "#EF4444",
        info: "#06B6D4",
        appBg: "#F5F7FA",
        border: "#E2E8F0",
        textPrimary: "#0F172A",
        textSecondary: "#64748B"
      },
      borderRadius: {
        button: "12px",
        card: "16px",
        modal: "20px",
        input: "12px"
      },
      boxShadow: {
        card: "0 2px 8px rgba(15, 23, 42, 0.06)",
        hoverCard: "0 8px 24px rgba(15, 23, 42, 0.12)"
      }
    }
  },
  plugins: []
};

export default config;
