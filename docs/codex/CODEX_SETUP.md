# Codex Setup Guide

## 官方安裝方式

Codex CLI 支援 macOS、Windows、Linux。

### npm 安裝

```bash
npm install -g @openai/codex
```

### Homebrew 安裝

```bash
brew install codex
```

### 執行並登入

```bash
codex
```

啟動後依照畫面登入 ChatGPT 帳號或使用 OpenAI API key。

## Windows 建議

Windows 可使用 Codex App，或使用 WSL 執行 Codex CLI。

## 本專案建議用法

進入專案資料夾：

```bash
cd erp-2.0-project
codex
```

建議第一次給 Codex 的任務：

```txt
請依 docs/design-system/ERP_2_0_Design_System_Specification.md 建立 Dashboard Layout、KPI Card、Status Badge、Alert Card、Sidebar、Top Navbar 的第一版 React Components。
```
