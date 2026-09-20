# Domain Contracts Baseline (T003)

This document describes **contracts actually used by the live analysis path**,
plus classified leftovers.

## Dependency direction

```text
                 DOMAIN CONTRACTS (app.models)
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
   Application      Pipeline       Persistence
    Services         Steps          Adapters
        ↓              ↓              ↓
        └──────────────┼──────────────┘
                       ↓
                   UI / Reports
```

Domain modules must not import Streamlit, Ollama, SQLite, or report renderers.

## Canonical live contracts

| Concept | Contract | Kind |
| --- | --- | --- |
| Analysis request | `AnalysisRequest` | immutable value |
| Prepared paper | `PreparedPaper` | immutable value |
| Paper sections | `PaperSections` | immutable value |
| LLM output | `LLMResponse` | immutable value |
| Analysis outcome | `AnalysisResult` | immutable value |
| History snapshot | `AnalysisRecord` | mutable (`id` assigned after save) |
| Job status vocabulary | `AnalysisStatus` | enum |
| Progress event | `ProgressEvent` | immutable value |
| Progress stage | `ProgressStage` | enum |
| Report payload | `ReportDocument` | presentation contract in `app.reports` |

## Request vs prepared input vs result vs history

```text
AnalysisRequest     source path / filename / analysis type
        ↓
PreparedPaper       extracted text, pages, PaperSections
        ↓
LLMResponse         provider-neutral model output
        ↓
AnalysisResult      analysis text + provider/model/timing
        ↓
AnalysisRecord      history snapshot (paper identity + result)
        ↓
ReportDocument      renderer input (does not render)
```

The live `PaperAnalyzer.analyze()` returns `AnalysisResult`.
`SaveHistoryStep` / `HistoryService.save_result()` convert that into
`AnalysisRecord` at the persistence boundary.

## AnalysisStatus vs ProgressStage vs PipelineStatus

These are **different vocabularies**:

- `AnalysisStatus` — job/analysis lifecycle (`CANCEL_REQUESTED` ≠ `CANCELLED`)
- `ProgressStage` — workflow progress stages for UI-independent events
- `PipelineStatus` — pipeline runner envelope state

Do not collapse `CANCEL_REQUESTED` into `CANCELLED`. Completing cancel
lifecycle is T011/T012.

## PaperSections

- Missing body sections are empty strings.
- `section_count` is the counting API. `__len__` is a compatibility alias.
- `title` is identity, not a counted body section.

## Compatibility / legacy

| Module | Classification |
| --- | --- |
| `app.core.analysis.analysis_status.AnalysisStatus` | COMPATIBILITY re-export |
| `PipelineStep` / `AnalysisPipeline` / `ServiceFactory` | COMPATIBILITY (T001) |
| `PDFExtractionResult` | INFRASTRUCTURE-LOCAL |
| `PipelineResult` / `PipelineContext` | APPLICATION/PIPELINE envelope, not the analysis-result domain |
| `ProgressState` | RUNTIME-LOCAL mutable progress |
| `app.document.PaperDocument` / `PaperSection` | LEGACY / UNUSED by live path |
| Alternate `app.core.analysis` job stack | LEGACY / not live (`streamlit_app`) |

## Persistence / UI / provider boundaries

- `HistoryRepository` maps SQLite rows ↔ `AnalysisRecord`. Domain models contain no SQL.
- UI may map contracts into widgets; domain models do not import Streamlit.
- `OllamaService` translates SDK responses into `LLMResponse`.

## Deferred

- Duplicate Analyze UI extract/prepare (T014)
- Job registry and cancel completion (T011/T012)
- Unifying leftover Analyze UI session handling onto `AnalysisResult` helpers
- `app.document` adoption or removal
