# FM01-I2D Shared Frontend Source Admission Manifest

Source: `codex/fm02-item-master-uom-integration-20261017-001` at `ed69b1a22202af7994cbaab60feee2855252565c`

Destination assessment: canonical FM-01 isolated target has no existing files at the listed destination paths. No admission or copy is executed by this manifest.

| SourcePath | SourceCommit | SourceBlob | DestinationPath | DestinationExistingBlob/Absent | Classification | DependencyCheck | AdmissionDecision |
|---|---|---|---|---|---|---|---|
| `package.json` | `ed69b1a` | `5af1ec7bb78a26d82335e5a5d40943f054ce39cc` | `package.json` | ABSENT | DEPENDENCY_REVIEW_REQUIRED | package dependency review | HOLD |
| `package-lock.json` | `ed69b1a` | `dd1e525b18a2ba46051b26ab1f9d8653f40ccddc` | `package-lock.json` | ABSENT | DEPENDENCY_REVIEW_REQUIRED | lockfile review | HOLD |
| `tsconfig.json` | `ed69b1a` | `9510a915d16e102c305a50ca78d5dda0c15635a1` | `tsconfig.json` | ABSENT | DEPENDENCY_REVIEW_REQUIRED | compiler/path review | HOLD |
| `src/app/layout.tsx` | `ed69b1a` | `7985ed9ff99d69318aea7595e41235fb3900ed2b` | `src/app/layout.tsx` | ABSENT | SHARED_APPROVED | shell-only review | ACCEPTED |
| `src/app/globals.css` | `ed69b1a` | `2047a81176aed910f6b31c45f814b83125b25b75` | `src/app/globals.css` | ABSENT | SHARED_APPROVED | global style review | ACCEPTED |
| `src/layouts/app-layout.tsx` | `ed69b1a` | `64e17d6d1ee9d718215408a3951c6847c549fc69` | `src/layouts/app-layout.tsx` | ABSENT | SHARED_APPROVED | shell-only review | ACCEPTED |
| `src/components/ui/status-badge.tsx` | `ed69b1a` | `b6ee296c94982cb422dff11b2b7960c643150fbf` | `src/components/ui/status-badge.tsx` | ABSENT | SHARED_APPROVED | shared UI review | ACCEPTED |
| `docs/design-system/ERP_2_0_Design_System_Specification.md` | `ed69b1a` | `3a27c79252cc8409816f1876808b9fd4a96fde24` | `docs/design-system/ERP_2_0_Design_System_Specification.md` | ABSENT | SHARED_APPROVED | design-system reference | ACCEPTED |
| `src/components/common/compact-list-panel.tsx` | `ed69b1a` | `dcf9c77107e0c241b238422af8452ce478693865` | same | ABSENT | SHARED_APPROVED | shared component review | ACCEPTED |
| `src/components/common/data-source-status-badge.tsx` | `ed69b1a` | `ad02de6ae939c71dd46f3a9ae442368f6ef278cf` | same | ABSENT | SHARED_APPROVED | shared component review | ACCEPTED |
| `src/components/common/data-source-toggle.tsx` | `ed69b1a` | `28f0c224f21563e492642501eefff2b7c8ece46a` | same | ABSENT | SHARED_APPROVED | shared component review | ACCEPTED |
| `src/components/common/detail-card.tsx` | `ed69b1a` | `90459e59b74ea44d95aaf262c2a0094b787e482f` | same | ABSENT | SHARED_APPROVED | shared component review | ACCEPTED |
| `src/components/common/language-switcher.tsx` | `ed69b1a` | `39fb88d65ba9b517f9fb1ca3470fa61e5258fd0c` | same | ABSENT | SHARED_APPROVED | shared component review | ACCEPTED |
| `src/components/common/module-hero.tsx` | `ed69b1a` | `809db4d5a61e768e1e5c235c5a03b92854b115c0` | same | ABSENT | SHARED_APPROVED | shared component review | ACCEPTED |
| `src/components/common/module-kpi-card.tsx` | `ed69b1a` | `0a4bb2b0b625b14074a4cd6044f351875f91b513` | same | ABSENT | SHARED_APPROVED | shared component review | ACCEPTED |
| `src/components/common/nav-link.tsx` | `ed69b1a` | `a22c5e758333932369ee03845a43d2033885d7f6` | same | ABSENT | SHARED_APPROVED | shared component review | ACCEPTED |
| `src/components/common/process-board.tsx` | `ed69b1a` | `70c45c493e8efdae4b89faf7492ecf0eb914767e` | same | ABSENT | SHARED_APPROVED | shared component review | ACCEPTED |
| `src/components/common/support-empty-state.tsx` | `ed69b1a` | `2ac42a7c338a1c1135a60384216320809ae740cf` | same | ABSENT | SHARED_APPROVED | shared component review | ACCEPTED |
| `src/components/common/support-search-panel.tsx` | `ed69b1a` | `12255dc26e02865130f1d836da4c774df28cc733` | same | ABSENT | SHARED_APPROVED | shared component review | ACCEPTED |

Excluded: Item Master pages/components, FM-02 business behavior, backend/API source, database/migration source, tests, secrets and private environment files.

## CIO-Authorized Three-File Dependency Extension

Source admission commit: `3c1bf00ec33cefa4ded053213906109eaceff863`
Source commit: `ed69b1a22202af7994cbaab60feee2855252565c`
Extension scope: exactly three shared dependency files; no wildcard or FM-02-specific source.

| SourceCommit | SourcePath | SourceBlob | DestinationPath | DestinationBlob | Classification | DependencyRationale | AdmissionDecision |
|---|---|---|---|---|---|---|---|
| `ed69b1a22202af7994cbaab60feee2855252565c` | `src/i18n/dictionary.ts` | `bfc7d48fb6154a8b460161edb6b2ddd4b47d3d3a` | `src/i18n/dictionary.ts` | `bfc7d48fb6154a8b460161edb6b2ddd4b47d3d3a` | SHARED_APPROVED | AppLayout requires translation keys and locale types; LanguageSwitcher consumes supported language labels. | ACCEPTED |
| `ed69b1a22202af7994cbaab60feee2855252565c` | `src/i18n/language-provider.tsx` | `be8fa518a608c1d0d56daba13cc5456fb9060e4b` | `src/i18n/language-provider.tsx` | `be8fa518a608c1d0d56daba13cc5456fb9060e4b` | SHARED_APPROVED | Root layout, AppLayout and LanguageSwitcher require the shared language context/provider. | ACCEPTED |
| `ed69b1a22202af7994cbaab60feee2855252565c` | `src/types/dashboard.ts` | `a4de742878e864e3d82536cb0c91d931c4a0e74a` | `src/types/dashboard.ts` | `a4de742878e864e3d82536cb0c91d931c4a0e74a` | SHARED_APPROVED | StatusBadge and admitted shared components import the shared StatusTone type. | ACCEPTED |
