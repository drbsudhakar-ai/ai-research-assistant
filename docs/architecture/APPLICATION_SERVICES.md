# Application Services Baseline (T004)

This document describes the **live application-service boundary**.

## 1. Application-service responsibility

Canonical application service:

```text
app.services.analysis_service.AnalysisService
```

It coordinates the analysis use case:

```text
AnalysisRequest
      ↓
validate request (domain contract)
      ↓
create pipeline context (hidden from UI)
      ↓
run live ResearchAnalysisPipeline
      ↓
AnalysisResult
```

It does **not**:

- render Streamlit widgets;
- extract PDFs itself;
- call Ollama or other provider SDKs;
- execute SQL;
- format HTML/Markdown/PDF/DOCX reports.

## 2. ServiceContainer responsibility

Canonical composition root:

```text
app.services.service_container.ServiceContainer
```

```text
ApplicationConfig
      ↓
ServiceContainer
   ├── AnalysisService
   ├── HistoryService → HistoryRepository
   ├── LLMService → OllamaService
   ├── PaperAnalyzer
   ├── PDFExtractor / PaperPreprocessor
   └── ResearchAnalysisPipelineFactory
```

`ServiceContainer` constructs and injects dependencies. It does not run
analysis.

## 3. Dependency direction

```text
UI
 ↓
AnalysisService
 ↓
Pipeline (implementation)
 ↓
Domain contracts + infrastructure adapters
```

Infrastructure may depend on `app.models`. Domain models must not depend on
Streamlit, SQLite, Ollama, or UI components.

## 4. AnalysisRequest boundary

`AnalysisRequest` is the only public analysis input.

- framework-independent
- no `UploadedFile` / Streamlit session state
- identity: `source_path`, `filename`, `analysis_type`

The Analyze page adapts an uploaded file to a filesystem path, then builds
`AnalysisRequest`. That adapter stays in the UI.

## 5. AnalysisResult boundary

`AnalysisService.analyze()` returns `AnalysisResult`.

It does not return `AnalysisRecord`, `PipelineResult`, `LLMResponse`, or
provider SDK objects.

`result_from_pipeline()` is an internal mapping helper used to extract
`AnalysisResult` from the pipeline envelope. UI must not call the pipeline
directly.

## 6. Pipeline boundary

The live pipeline remains:

```text
ValidatePdfStep → PreparePaperStep → AnalyzePaperStep → SaveHistoryStep
```

composed by `ResearchAnalysisPipelineFactory` and executed by
`PipelineRunner`.

The UI must not depend on `PipelineContext`, pipeline keys, steps, or
`PipelineRunner`. Those stay inside `AnalysisService`.

## 7. History boundary

```text
AnalysisResult
      ↓
SaveHistoryStep
      ↓
HistoryService
      ↓
HistoryRepository
      ↓
SQLite
```

`AnalysisService` does not import `HistoryRepository` or `sqlite3`.
Persistence is coordinated through `HistoryService` injected into
`SaveHistoryStep` by `ServiceContainer`.

`AnalysisRecord` remains the history/persistence contract (T003).

## 8. Provider boundary

```text
AnalysisService
      ↓
PaperAnalyzer
      ↓
LLMService
      ↓
OllamaService
      ↓
LLMResponse → AnalysisResult
```

`AnalysisService` has no Ollama SDK imports.

## 9. UI boundary

Live Analyze UI: `app.ui.pages.analyze` via `app.core.navigation`.

T004 only required the page to call:

```text
ServiceContainer.analysis_service.analyze(AnalysisRequest) -> AnalysisResult
```

Duplicate UI extract/prepare for preview plus pipeline prepare remains
**T014**. Cancellation/job lifecycle remains **T011/T012**.

## 10. Compatibility modules

| Module | Classification | Behavior |
| --- | --- | --- |
| `app.services.service_factory.ServiceFactory` | COMPATIBILITY | Delegates to `ServiceContainer` |
| `app.bootstrap.analysis_container.build_analysis_service` | COMPATIBILITY | Delegates to `ServiceContainer` |
| `app.core.analysis.*` | UNUSED / DEFERRED | Alternate job stack; not live |
| `app.controllers.*` | UNUSED / DEFERRED | Not used by `streamlit_app.py` |
| `app.ui.pages.analyze/` package | UNUSED / DEFERRED | Alternate Analyze stack |

Do not merge those stacks in T004.

## 11. Deferred architecture issues

- T011/T012: job registry, `CANCEL_REQUESTED` vs `CANCELLED`
- T014: single prepare path; Analyze page use-case migration
- T016: Settings UI env reads / SettingsManager runtime merge
- Untracked controllers still calling `analyze(pdf_path=...)` are not live
