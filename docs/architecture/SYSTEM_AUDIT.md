# System Audit Baseline (T005)

Inspection of the **actual repository** after T001–T004. This is not a
redesign proposal.

## Live architecture

```text
streamlit_app.py
        ↓
sidebar (app.ui.components.sidebar) + ThemeManager
        ↓
app.core.navigation.render_page
        ↓
app.ui.pages.analyze (module, not app/ui/pages/analyze/)
        ↓
ServiceContainer
        ↓
AnalysisService.analyze(AnalysisRequest) -> AnalysisResult
        ↓
ResearchAnalysisPipelineFactory / PipelineRunner
        ↓
ValidatePdf → PreparePaper → AnalyzePaper → SaveHistory
        ↓
PaperAnalyzer → LLMService → OllamaService → LLMResponse
        ↓
HistoryService → HistoryRepository → SQLite
        ↓
ReportDocument → Markdown/HTML download
```

Pages routed live: Dashboard, Analyze, History, Settings, About.
There is no live Home or Report navigation item.

## Classification (selected)

| Path | Classification |
| --- | --- |
| `app.services.*` live stack | LIVE |
| `app.ui.pages.analyze` module | LIVE |
| `app.reports` Markdown/HTML | LIVE |
| `ServiceFactory` / bootstrap analysis_container | COMPATIBILITY |
| `app.core.analysis.*` | UNUSED / DEFERRED (T011) |
| `app.controllers.*` | UNUSED / DEFERRED |
| `app.ui.pages.analyze_v5_draft/` package | EXPERIMENTAL / DEFERRED; deliberately excluded from live routing |
| `app.document.*` | LEGACY / UNUSED duplicate of PreparedPaper |
| `app.config.model_config` / `export_config` / `pipeline_config` | LEGACY |
| Settings UI `os.getenv` | LEGACY / T016 |
| Analyze UI extract + pipeline extract | DUPLICATE / T014 |
| `app.ui.home` | UNUSED (not in PAGE_ROUTES) |
| `app.ui.pages.report` | UNUSED (not in PAGE_ROUTES) |

## T005 remediations

- Removed live debug `print`s from `PaperAnalyzer` and `PipelineRunner`.
- Upload filenames are basename-only and resolved under `ApplicationConfig.paths.uploads_dir`.
- Analyze worker no longer writes `st.session_state` from the background thread.
- Invalid/corrupt PDF upload errors are shown instead of crashing the page.
- Renamed the unfinished Version 5 Analyze package so it cannot shadow the
  canonical `app.ui.pages.analyze` module during Python import resolution.

## Deferred

- T011/T012 job registry and `CANCEL_REQUESTED` vs `CANCELLED` UI.
- T014 single extract/prepare path.
- T016 SettingsManager merge / Settings `os.getenv`.
- PDF/DOCX export (not implemented).
- Do not delete `app.document` or alternate stacks without a dedicated task.
