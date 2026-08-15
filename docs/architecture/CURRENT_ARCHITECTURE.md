# Current Architecture Baseline (T001)

This document describes the **actual repository** as inspected during T001.
It is not a target architecture.

## Supported Python version

Declared requirement in existing modules (`app/settings/api/enums.py`,
layout/theme docstrings): **Python 3.11+**.

`enum.StrEnum` is therefore in-contract. T001 does **not** polyfill StrEnum
for Python 3.10 and does **not** change the declared requirement.

A 3.10 interpreter cannot import `StrEnum` modules. That is an environment
mismatch, not a T001 defect.

## Module map

```text
streamlit_app.py                 Streamlit entry / page config
app/
  config/                        App constants, branding, settings manager
  core/
    pipeline/                    Canonical pipeline framework
    progress/                    Progress events, manager, Streamlit renderer
    analysis/                    Alternate job-lifecycle stack (not live path)
    navigation.py                Page routing
    session.py                   Session initialization
  pipeline/steps/                Concrete analysis steps
  services/                      Composition root + analysis/history/LLM
  agents/paper_analyzer.py       LLM analysis agent
  utils/                         PDF extract/preprocess/title
  models/                        PreparedPaper, PaperSections, AnalysisRecord
  storage/                       SQLite history
  ui/pages/                      Dashboard, Analyze, History, Settings, About
  ui/theme/                      CSS/design tokens/theme manager
  ui/components/                 Page components
  reports/                       Streamlit-independent report renderers (T001)
  settings/api/                  API settings models
```

No `tests/` directory existed before T001.

## Live execution flow

```text
streamlit_app.configure_page()
        ↓
initialize_database()
initialize_session()
ThemeManager.initialize() / inject()
        ↓
app.ui.components.sidebar.render_sidebar()
        ↓
app.core.navigation.render_page()
        ↓
Analyze page (canonical analysis UI)
        ↓
ServiceContainer
        ↓
AnalysisService.analyze()          (app.services.analysis_service)
        ↓
ResearchAnalysisPipelineFactory.create()
        ↓
PipelineRunner.run(PipelineContext)
        ↓
ValidatePdfStep → PreparePaperStep → AnalyzePaperStep → SaveHistoryStep
        ↓
HistoryService / SQLite (data/history.db)
```

## Dependency direction (intended vs actual)

Intended:

```text
UI → Application services → Domain/pipeline → Infrastructure
```

Actual live Analyze path largely follows this, with exceptions documented
under “Analyze extract/prepare duplication (T014)”.

## Canonical interfaces

### Pipeline step ABC (final contract)

There is **one** canonical step ABC:

```text
app.core.pipeline.base_pipeline_step.BasePipelineStep
```

`PipelineRunner` calls `run()`. Subclasses implement `execute()`.
`Pipeline` type-checks steps with `isinstance(..., BasePipelineStep)`.

`PipelineStep` is **not** a second ABC and **not** the final contract name.
It is a legacy compatibility alias:

```text
PipelineStep = BasePipelineStep
```

New code must subclass/import `BasePipelineStep`.

`PipelineStage` is a **stage-name enum**, not a step ABC.
Settings UI `PipelineStageType` is a settings toggle enum, not the runner
contract.

### Pipeline composition

Canonical types:

- `Pipeline` (ordered steps; does not execute)
- `PipelineBuilder` (assembles `BasePipelineStep` instances)
- `PipelineRunner`
- `PipelineContext`
- `PipelineResult`
- `ResearchAnalysisPipeline` (composed workflow; requires configured steps)
- `ResearchAnalysisPipelineFactory` (live composition of steps)

### Legacy compatibility modules (not alternate implementations)

| Module | Classification |
| --- | --- |
| `app.core.pipeline.pipeline_step.PipelineStep` | Alias of `BasePipelineStep` |
| `app.core.pipeline.analysis_pipeline.AnalysisPipeline` | Alias of `ResearchAnalysisPipeline` |
| `app.services.service_factory.ServiceFactory` | Delegates to `ServiceContainer` |
| `app.bootstrap.analysis_container.build_analysis_service` | Delegates to `ServiceContainer` |

These exist so old imports do not construct a second graph.

### Progress

Canonical contract:

- `ProgressReporter.update(message, percentage, stage, metadata)`
- `ProgressEvent.stage` (not `step`)
- `ProgressManager` implements `ProgressReporter` and owns `CancellationToken`
- `ProgressRenderer` is UI-only (`app.core.progress.progress_renderer`); not
  re-exported from `app.core.progress` so core imports stay Streamlit-free

State ownership today: in-memory `ProgressManager` plus Streamlit session keys
on the Analyze page. Worker threads and a module-level `queue.Queue` are used.
Rerun-safe job identity is T011–T012.

### Cancellation semantics (required; not implemented in T001)

Required distinction:

```text
CANCEL_REQUESTED  →  token/flag set; worker may still be running
CANCELLED         →  worker has actually stopped
```

`CancellationToken.cancel()` is a **request**. It must not be reported as
`CANCELLED` until the worker is no longer alive.

Current defect (deferred to T011/T012):
`app.controllers.analysis_controller` and `app.core.analysis.analysis_controller`
assign `AnalysisStatus.CANCELLED` immediately on cancel request. T001 does
not change that job architecture.

### Paper preparation

- `PDFExtractor.extract_text(file: BinaryIO) -> PDFExtractionResult`
- `PaperPreprocessor.prepare(extracted, filename) -> PreparedPaper`
- `PaperSectionExtractor.extract(title, text) -> PaperSections`
- `PreparedPaper.sections: PaperSections` with `section_count` and `__len__`

### Analyze extract/prepare duplication (deferred to T014)

T001 did **not** redesign the Analyze page and did **not** add a third
extract/prepare path.

Current (pre-existing) duplication:

```text
Analyze UI
  → PDFExtractor.extract_text (preview / paper info)
  → PaperPreprocessor.prepare
  → AnalysisService.analyze(pdf_path)
       → pipeline PreparePaperStep
            → PDFExtractor.extract_text again
            → PaperPreprocessor.prepare again
```

The UI extraction is for preview. The pipeline extraction is the analysis
contract. Unifying this into a single application use case is **T014**.

### Services

Live composition root: `app.services.service_container.ServiceContainer`.

Live analysis API: `app.services.analysis_service.AnalysisService(pipeline_factory=...)`.

A second stack exists under `app.core.analysis` and `app.controllers`.
It is **not** used by `streamlit_app.py`. Do not merge without review.

### Configuration

Canonical runtime configuration (T002):

```text
optional .env
        ↓
environment variables (AI_RA_*)
        ↓
validated ApplicationConfig (app.config.loader)
        ↓
ServiceContainer / SQLite path / logging
```

- Identity remains `BrandConfig`.
- `app.config.llm_config` and `app.config.app_config` are compatibility
  surfaces over the same defaults / live developer-mode flag.
- `SettingsManager` is the persisted Settings-UI API layer. It is **not**
  auto-merged into runtime `ApplicationConfig`.
- See `docs/architecture/CONFIGURATION.md`.

### Branding

Single source of truth: `app.config.branding.BrandConfig` via
`get_brand_config()`.

UI layout Header/Footer/Sidebar defaults and report renderers must read
`BrandConfig`. They must not define independent product-name/author literals.

### Persistence

`HistoryService` → `HistoryRepository` → SQLite `analysis_history`.

### Reports

Markdown and HTML via `app.reports` (Streamlit-independent).
PDF/DOCX generators are **not implemented**.

## Known inconsistencies / technical debt

1. Duplicate analysis lifecycle (`app.services` vs `app.core.analysis`).
2. Analyze page auto-refresh uses `time.sleep` + `st.rerun`.
3. Cancel request reported as `CANCELLED` before worker stop (T011/T012).
4. Analyze UI extract/prepare then pipeline extract/prepare (T014).
5. Settings placeholders vs existing settings components (T016).
6. Duplicate footer/sidebar/header modules; live sidebar is
   `app.ui.components.sidebar`.
7. `requirements.txt` still lists LangChain/LangGraph/Chroma; live analysis
   uses Ollama.
8. No logo/favicon assets.
9. Job identity is not persisted across Streamlit reruns.

## Recommended corrections (not T001)

- T003: stabilize domain contracts (`AnalysisRun`, job status).
- T011–T012: job registry, `CANCEL_REQUESTED` vs `CANCELLED`, rerun recovery.
- T014: Analyze page should call application use cases only (single prepare).
- T016: wire existing settings components.
- T017–T018: PDF/DOCX report renderers if required.

## T001 corrections applied

- Documented `BasePipelineStep` as the sole canonical ABC.
- Classified `PipelineStep` / `AnalysisPipeline` / `ServiceFactory` /
  bootstrap as compatibility only.
- `PipelineBuilder` types against `BasePipelineStep`.
- Streamlit removed from paper-preparation pipeline step.
- Debug prints removed from the live analysis/bootstrap path.
- `PaperSections.__len__` delegates to `section_count`.
- Central `BrandConfig`; layout defaults and reports consume it.
- Theme package exports tokens used by layout modules.
- Baseline tests added under `tests/`.
- Documented Analyze duplication (T014) and cancellation semantics (T011/T012).
