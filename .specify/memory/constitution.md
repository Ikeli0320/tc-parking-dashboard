<!--
Sync Impact Report:
Version: 0.1.0 (initial creation)
RATIFICATION_DATE: 2025-01-27
LAST_AMENDED_DATE: 2025-01-27

Principles:
- Minimal Scope Principle (new)
- Rapid Delivery Principle (new)
- Immediate Executability Principle (new)
- Documentation Simplicity Principle (new)

Added Sections:
- Project Nature Declaration
- Minimal Scope Principle
- Rapid Delivery Principle
- Immediate Executability Principle
- Documentation Simplicity Principle
- Governance

Templates requiring updates:
- ✅ updated: .specify/templates/plan-template.md (Constitution Check section updated)
- ⚠ pending: .specify/templates/spec-template.md (no constitution-specific content, aligned by design)
- ⚠ pending: .specify/templates/tasks-template.md (no constitution-specific content, aligned by design)
- ⚠ pending: .specify/templates/commands/*.md (to be reviewed if needed)

Follow-up TODOs:
- None
-->

# Project Constitution

**Project Name:** Crawl-ike (台中市停車場資料爬蟲)

**Constitution Version:** 0.1.0

**RATIFICATION_DATE:** 2025-01-27

**LAST_AMENDED_DATE:** 2025-01-27

## Project Nature Declaration

本專案為短期任務性質，目標是以最小可行範圍（Minimal Scope）快速完成指定目標，不進行架構性延展或長期維運設計。程式結構以可立即執行與易於交付為主，文件僅需簡要說明關鍵流程與使用方式，無需維持長期同步。重點在於效率與可交付成果，而非完整性或可擴充性。

## Principles

### Principle 1: Minimal Scope

**MUST** 僅實作完成指定目標所需的最少功能，不得進行架構性延展、抽象化設計或預留擴充介面。

**Rationale:** 專案性質為短期任務，過度設計會延遲交付時間並增加維護成本。所有開發決策必須以「是否為完成目標所必需」為唯一判斷標準。

### Principle 2: Rapid Delivery

**MUST** 優先選擇能最快達成目標的實作方式，即使該方式不符合長期最佳實踐。

**Rationale:** 效率與可交付成果優先於程式碼品質標準。在時間與品質的權衡中，必須選擇時間優先的方案。

### Principle 3: Immediate Executability

**MUST** 確保程式碼可立即執行並產生預期輸出，無需額外設定或複雜的部署流程。

**Rationale:** 易於交付是核心要求。程式必須能在標準環境中直接執行，輸出結果必須可直接使用。

### Principle 4: Documentation Simplicity

**MUST** 文件僅包含關鍵流程與使用方式，無需詳細的架構說明、API 文件或長期維護指南。

**Rationale:** 文件目的在於讓使用者能快速理解並使用程式，而非作為長期維護的參考。文件內容以「能讓使用者成功執行」為充分條件。

## Governance

### Amendment Procedure

本憲法可透過以下方式修訂：

1. 識別需要修改的原則或新增原則
2. 更新版本號（遵循語義化版本控制）
3. 更新 `LAST_AMENDED_DATE`
4. 在文件頂部同步影響報告中記錄變更

### Versioning Policy

版本號遵循語義化版本控制（Semantic Versioning）：

- **MAJOR:** 向後不相容的治理原則移除或重新定義
- **MINOR:** 新增原則或章節，或實質性擴展指引
- **PATCH:** 澄清、措辭修正、錯字修正、非語義性改進

### Compliance Review

本專案為短期任務性質，不進行定期合規審查。所有開發決策應在執行時參考本憲法原則，但無需建立正式的審查流程。

### Scope Boundaries

以下活動明確超出本專案範圍：

- 建立可擴充的架構設計
- 實作非目標功能
- 建立長期維護文件
- 進行效能優化（除非影響基本功能）
- 建立自動化測試套件（除非為交付要求）
- 建立 CI/CD 流程
- 進行程式碼重構以提升可維護性

## Compliance

所有參與本專案開發的人員必須遵循上述原則。在面臨決策時，應優先考慮：

1. 是否能最快達成目標？
2. 是否為完成目標所必需？
3. 是否能立即執行並產生預期輸出？
4. 文件是否足以讓使用者成功執行？

任何違反上述原則的開發活動都應被視為超出專案範圍。
