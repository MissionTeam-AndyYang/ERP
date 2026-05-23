# ERP Frontend I18N Design

日期：2026-05-23

## Goal

The ERP frontend should support switching languages from the web UI. The first implementation adds a lightweight i18n foundation without introducing a large external translation framework.

## Supported Languages

Initial language options:

- `zh-TW`: 繁體中文
- `en`: English
- `ja`: 日本語
- `vi`: Tiếng Việt

## Current Implementation

Files:

- `src/i18n/dictionary.ts`
- `src/i18n/language-provider.tsx`
- `src/components/common/language-switcher.tsx`
- `src/layouts/app-layout.tsx`
- `src/app/layout.tsx`

The language provider:

- Stores selected language in `localStorage`.
- Updates `document.documentElement.lang`.
- Provides `t(key)` for shared UI text.

The current language switcher is placed in the top app header.

## First Translation Scope

Translated now:

- App title fallback.
- Plant/site label.
- Global search placeholder.
- Notification accessible label.
- User display labels.
- Sidebar and mobile navigation labels.
- Warehouse app-layout title.

Not fully translated yet:

- Business data from mock/API, such as item names, batch status, and document names.
- Page-specific labels inside Warehouse and Production.
- Backend/API content.

These should be migrated gradually as page designs stabilize.

## Design Rules

1. Common shell text should always use dictionary keys.
2. Page-level static labels should move into dictionary keys after the page design is approved.
3. Business records from the database should not be translated in the UI unless the database/API provides translated fields or a clear mapping table.
4. Status labels may need controlled translation because they affect filters, chips, and workflow logic.
5. Language switching should not require route changes in the first version.

## Next Steps

1. After Warehouse layout is approved, move Warehouse static labels into dictionary keys.
2. After Production layout is approved, move Production static labels into dictionary keys.
3. Decide whether master data needs multilingual fields in the database.
4. Decide if URLs should later include locale prefixes such as `/zh-TW/warehouse`.
