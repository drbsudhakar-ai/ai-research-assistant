# T004 — Application Service & Use-Case Boundary

**Task ID:** T004  
**Status:** READY  
**Priority:** HIGH  
**Type:** Architecture / Refactoring / Backend  
**Depends On:** T001, T002, T003  
**Owner:** Cursor — Implementation Engineer  
**Reviewers:** Architectural Reviewer + Technology Acceptance Reviewer  

---

# 1. OBJECTIVE

Establish a clean application-service/use-case boundary between the UI,
domain contracts, infrastructure services, and pipeline execution.

T004 must make the application layer responsible for coordinating the
analysis use case while keeping:

- Streamlit concerns in the UI layer.
- Domain contracts in `app/models`.
- Provider-specific concerns in provider services.
- SQLite concerns in repositories.
- Report rendering in the report layer.
- Pipeline execution behind the application boundary.

The target direction is:

    UI
     ↓
    Application Service / Use Case
     ↓
    Pipeline
     ↓
    Domain + Infrastructure Services
     ↓
    AnalysisResult
     ↓
    History / Report / UI

T004 is a boundary-stabilization task.

It is NOT a complete Analyze-page redesign.

---

# 2. ARCHITECTURAL CONTEXT

T001 established the repository architecture baseline.

T002 established the application configuration boundary.

T003 established canonical domain contracts.

Current canonical result boundary:

    AnalysisRequest
          ↓
    AnalysisService
          ↓
    ResearchAnalysisPipeline
          ↓
    AnalysisResult
          ↓
    HistoryService / Report / UI

Canonical domain contracts include:

- `AnalysisRequest`
- `PreparedPaper`
- `PaperSections`
- `AnalysisResult`
- `AnalysisRecord`
- `LLMResponse`
- `AnalysisStatus`
- `ProgressEvent`
- `ProgressStage`

T003 established that:

    AnalysisResult = analysis outcome

    AnalysisRecord = history/persistence representation

T004 must preserve that separation.

---

# 3. PRIMARY GOALS

## G1 — Establish the application-service boundary

Identify the canonical application service responsible for coordinating
the analysis use case.

The live path must have one clear entry point.

Target:

    UI
     ↓
    AnalysisService
     ↓
    Pipeline

Avoid UI code directly coordinating multiple backend services.

---

## G2 — Stabilize AnalysisService

Review the existing `AnalysisService`.

Determine:

- constructor dependencies;
- configuration dependencies;
- pipeline dependency;
- progress dependency;
- history dependency;
- report dependency;
- error handling;
- return contracts.

The public analysis operation must use canonical domain contracts.

Preferred conceptual boundary:

    AnalysisRequest
          ↓
    AnalysisService.analyze(...)
          ↓
    AnalysisResult

Do not expose:

- Streamlit objects;
- UploadedFile;
- SQLite objects;
- Ollama SDK objects;
- pipeline implementation details.

---

## G3 — Stabilize ServiceContainer

Review `ServiceContainer`.

It must remain the composition root.

Responsibilities:

- construct application services;
- construct infrastructure services;
- inject dependencies;
- use `ApplicationConfig`;
- avoid business logic.

ServiceContainer must NOT perform analysis itself.

Target:

    ApplicationConfig
          ↓
    ServiceContainer
       ├── AnalysisService
       ├── HistoryService
       ├── LLMService
       ├── PDF services
       └── other infrastructure

---

## G4 — Stabilize dependency direction

Target dependency direction:

    UI
     ↓
    Application
     ↓
    Domain
     ↓
    Infrastructure adapters

Infrastructure may depend on domain contracts.

Domain models must not depend on:

- Streamlit;
- SQLite;
- Ollama;
- provider SDKs;
- UI components.

Application services may coordinate infrastructure services but must not
contain provider-specific implementation.

---

# 4. ANALYSIS USE CASE

Establish one canonical application-level analysis flow.

Conceptually:

    AnalysisRequest
          ↓
    validate request
          ↓
    prepare paper
          ↓
    execute analysis
          ↓
    obtain AnalysisResult
          ↓
    optionally persist history
          ↓
    return AnalysisResult

The exact implementation must follow the existing live pipeline and
contracts rather than introducing a parallel pipeline.

Do NOT create another analysis lifecycle.

---

# 5. PIPELINE BOUNDARY

The pipeline remains an implementation mechanism.

The application layer should not expose internal pipeline mechanics to the UI.

Avoid UI code depending directly on:

- `PipelineContext`;
- pipeline keys;
- pipeline steps;
- pipeline runner;
- pipeline-specific result extraction.

Preferred:

    UI
     ↓
    AnalysisService
     ↓
    Pipeline

The application service converts the pipeline outcome into the canonical
`AnalysisResult`.

---

# 6. REQUEST BOUNDARY

`AnalysisRequest` is the canonical application input.

It must remain:

- framework-independent;
- Streamlit-independent;
- provider-independent;
- persistence-independent.

The application service must not accept:

- `st.file_uploader` output;
- `UploadedFile`;
- Streamlit session state;
- UI widgets.

If an adapter is required, keep that adapter at the UI/application boundary.

---

# 7. RESULT BOUNDARY

`AnalysisResult` is the canonical application output.

The application service must return `AnalysisResult`.

Do NOT return:

- `AnalysisRecord`;
- raw LLM response;
- pipeline result;
- provider SDK object;
- Streamlit object.

History remains separate:

    AnalysisResult
          ↓
    HistoryService
          ↓
    AnalysisRecord
          ↓
    HistoryRepository

---

# 8. HISTORY BOUNDARY

T003 established:

    AnalysisRecord = history contract

T004 must preserve this.

The application service may coordinate history persistence where the
existing architecture requires it, but history storage must remain behind
`HistoryService`.

The application service must not directly use:

- SQLite;
- SQL;
- repository implementation details.

Target:

    AnalysisService
          ↓
    HistoryService
          ↓
    HistoryRepository
          ↓
    SQLite

Do not redesign the database schema in T004.

---

# 9. LLM PROVIDER BOUNDARY

The application layer must remain provider-neutral.

Target:

    AnalysisService
          ↓
    LLMService
          ↓
    OllamaService
          ↓
    Ollama/provider API

The application service must not contain:

- Ollama-specific code;
- provider SDK imports;
- provider-specific response parsing.

Provider conversion remains:

    Provider response
          ↓
    LLMResponse
          ↓
    AnalysisResult

---

# 10. PDF/PAPER PREPARATION BOUNDARY

Paper preparation must remain behind the existing service/pipeline
boundary.

The application service should coordinate preparation rather than
implement PDF extraction itself.

Avoid:

    AnalysisService
        ↓
    PyMuPDF directly

Prefer existing service abstractions:

    AnalysisService
        ↓
    Pipeline / preparation service
        ↓
    PDFExtractor / PaperPreprocessor

Do not solve the known Analyze-page duplicate extraction/preparation
problem completely in T004.

That is deferred to T014.

T004 may document the boundary and prevent new duplication.

---

# 11. ERROR BOUNDARY

Review existing exception handling.

Application services should provide meaningful application-level errors
without exposing infrastructure implementation details.

Avoid leaking:

- raw SQLite errors;
- provider SDK exceptions;
- low-level PDF exceptions;
- Streamlit exceptions.

Use existing project exception contracts where available.

Do not create a large new exception hierarchy unless required.

Prefer minimal, meaningful application exceptions.

---

# 12. DEPENDENCY INJECTION

Dependencies must be explicit.

Prefer:

    class AnalysisService:
        def __init__(
            self,
            pipeline=...,
            history_service=...,
            ...
        ):
            ...

Do not use hidden global service instances.

Do not instantiate infrastructure services inside business methods.

Bad:

    def analyze(...):
        ollama = OllamaService(...)
        repository = HistoryRepository(...)

Preferred:

    ServiceContainer
          ↓
    dependency construction
          ↓
    AnalysisService
          ↓
    injected dependencies

---

# 13. TESTABILITY

The application service must be testable without:

- Streamlit;
- real SQLite;
- Ollama;
- external APIs;
- real PDF files where unnecessary.

Use fakes/mocks/stubs only where appropriate.

Tests should verify:

1. valid `AnalysisRequest` reaches the analysis pipeline;
2. `AnalysisResult` is returned;
3. pipeline failures are handled correctly;
4. history is not directly accessed from the application service;
5. provider-specific objects do not leak;
6. configuration is supplied through `ApplicationConfig`;
7. dependencies can be injected;
8. no Streamlit dependency exists in the application service.

---

# 14. LIVE-PATH DISCOVERY

Before modifying code, inspect the repository.

Determine the actual live path from:

    streamlit_app.py
        ↓
    navigation
        ↓
    Analyze page
        ↓
    ServiceContainer
        ↓
    AnalysisService
        ↓
    pipeline
        ↓
    analysis
        ↓
    history

Also inspect but DO NOT automatically activate:

- `app/controllers`;
- `app/core/analysis`;
- alternate analysis services;
- alternate worker/session managers;
- untracked experimental application stacks.

Classify them as:

- LIVE;
- COMPATIBILITY;
- LEGACY;
- UNUSED;
- DEFERRED.

Do not merge competing architectures during T004.

---

# 15. COMPATIBILITY MODULES

Existing compatibility modules may remain if they are required by the
current repository.

Examples include:

- `ServiceFactory`;
- bootstrap compatibility modules;
- legacy analysis services;
- legacy pipeline aliases.

Do not delete compatibility modules merely for cleanliness.

If a compatibility module delegates to the canonical implementation,
document that relationship.

Target:

    Legacy API
       ↓
    Compatibility adapter
       ↓
    Canonical application service

not:

    Legacy API
       ↓
    second implementation

---

# 16. UI BOUNDARY

T004 must inspect the Analyze page and identify backend orchestration
that belongs in the application layer.

However:

**DO NOT redesign the Analyze page in T004.**

Do not implement:

- new UI components;
- new progress UI;
- new layout;
- new navigation;
- new branding;
- new download UI.

Only make minimal changes required to ensure the UI calls the canonical
application boundary.

The full Analyze use-case migration belongs to T014.

---

# 17. PROGRESS BOUNDARY

Progress reporting must remain UI-independent.

The application/pipeline layer may emit:

    ProgressEvent

The UI may render it.

Do not import Streamlit into:

- `AnalysisService`;
- pipeline;
- domain models;
- infrastructure services.

Do not redesign cancellation.

Cancellation lifecycle belongs to T011/T012.

---

# 18. REPORT BOUNDARY

Reports must consume domain/application results.

Target:

    AnalysisResult
          ↓
    ReportDocument
          ↓
    Renderer/exporter

Do not place HTML/Markdown/PDF/DOCX formatting inside
`AnalysisService`.

Do not implement PDF/DOCX in T004.

---

# 19. CONFIGURATION BOUNDARY

T002 established:

    ApplicationConfig

T004 must consume the existing configuration boundary.

Do not:

- introduce another configuration object;
- read `.env` directly in AnalysisService;
- read environment variables directly in analysis code;
- introduce module-level provider configuration.

Target:

    ApplicationConfig
          ↓
    ServiceContainer
          ↓
    injected services

---

# 20. API READINESS

T004 does NOT implement REST/FastAPI endpoints.

However, the application boundary should be suitable for future API use.

Desired future architecture:

    Streamlit UI ─────┐
                      │
    REST API ─────────┼──→ AnalysisService
                      │
    CLI ──────────────┘

Therefore the application service must not require Streamlit.

---

# 21. NON-GOALS

Do NOT implement the following in T004:

- T011 job registry;
- T012 cancellation/rerun recovery;
- T014 Analyze-page redesign;
- authentication;
- REST API;
- database schema redesign;
- PDF export;
- DOCX export;
- new LLM providers;
- SettingsManager runtime merge;
- complete removal of legacy modules;
- complete UI refactoring;
- frontend redesign;
- new theme;
- new branding;
- broad repository cleanup;
- migration of every untracked experimental module.

If discovered, document and defer them.

---

# 22. REQUIRED DOCUMENTATION

Update or create:

    docs/architecture/APPLICATION_SERVICES.md

Document:

1. application-service responsibility;
2. ServiceContainer responsibility;
3. dependency direction;
4. AnalysisRequest boundary;
5. AnalysisResult boundary;
6. pipeline boundary;
7. history boundary;
8. provider boundary;
9. UI boundary;
10. compatibility modules;
11. deferred architecture issues.

Update:

    docs/architecture/CURRENT_ARCHITECTURE.md

only where required to reflect the accepted T004 architecture.

---

# 23. REQUIRED TESTS

Add focused tests for the application-service boundary.

Suggested:

    tests/test_analysis_service.py
    tests/test_service_container.py

Do not duplicate existing tests unnecessarily.

Minimum coverage:

### Test 1 — canonical request

    AnalysisRequest
        ↓
    AnalysisService
        ↓
    AnalysisResult

### Test 2 — dependency injection

Verify the service can be constructed with test doubles.

### Test 3 — pipeline failure

Verify predictable application-level failure behavior.

### Test 4 — history boundary

Verify history interaction occurs through `HistoryService`, not directly
through `HistoryRepository`.

### Test 5 — provider isolation

Verify `AnalysisService` does not expose provider-specific objects.

### Test 6 — configuration

Verify services receive configuration through `ApplicationConfig`.

### Test 7 — Streamlit isolation

Application-service modules must not import Streamlit.

### Test 8 — compatibility

If compatibility services remain, verify they delegate to the canonical
service rather than implementing a second analysis lifecycle.

---

# 24. QUALITY GATES

Run:

    py -3.12 -m pytest tests -q

Then targeted Ruff:

    ruff check <T004-authored Python files>

Then targeted Black:

    black --check <T004-authored Python files>

If repository-wide Ruff/Black failures are pre-existing, do not perform
unrelated cleanup.

Report them separately.

---

# 25. ACCEPTANCE CRITERIA

T004 is complete only when:

- [ ] one canonical AnalysisService is identified;
- [ ] AnalysisService returns AnalysisResult;
- [ ] AnalysisRequest remains framework-independent;
- [ ] ServiceContainer remains the composition root;
- [ ] dependencies are injected;
- [ ] pipeline mechanics are hidden from UI;
- [ ] HistoryRepository is not directly used by AnalysisService;
- [ ] provider-specific code remains behind LLM services;
- [ ] ApplicationConfig remains the configuration source;
- [ ] application layer contains no Streamlit dependency;
- [ ] application layer contains no SQLite implementation;
- [ ] application layer contains no Ollama SDK implementation;
- [ ] compatibility modules do not contain competing implementations;
- [ ] tests cover the application boundary;
- [ ] architecture documentation is updated;
- [ ] no T011/T012/T014 work is introduced;
- [ ] no unrelated files are reformatted or rewritten;
- [ ] targeted Ruff passes;
- [ ] targeted Black passes;
- [ ] tests pass or failures are clearly classified;
- [ ] no commit is created;
- [ ] no push is performed.

---

# 26. CHANGE CONTROL

Cursor must use the following sequence:

    DISCOVER
       ↓
    CLASSIFY
       ↓
    DESIGN MINIMAL CHANGE
       ↓
    IMPLEMENT
       ↓
    TEST
       ↓
    REVIEW SCOPE
       ↓
    STOP

Do not continue into the next task.

Do not automatically fix unrelated problems discovered during the task.

Every unrelated issue should be recorded under RISKS / DEFERRED.

---

# 27. GIT SAFETY

Before implementation:

    git status

Do not assume the working tree is clean.

The repository intentionally contains unrelated modified and untracked
files from previous development.

Do NOT:

- `git reset --hard`;
- `git clean`;
- `git restore .`;
- `git stash`;
- delete untracked work;
- overwrite unrelated changes.

Never use:

    git add .

or:

    git add -A

for this task.

At completion:

- do NOT commit;
- do NOT push.

The human/architectural reviewer will authorize the commit separately.

---

# 28. REQUIRED FINAL REPORT

Stop after implementation and return exactly this structure:

# T004 STATUS: READY FOR ARCHITECTURAL REVIEW

## DISCOVERY

- Live application-service path:
- ServiceContainer role:
- AnalysisService role:
- Pipeline boundary:
- History boundary:
- Provider boundary:
- Compatibility/legacy modules:
- Important inconsistencies:

## CHANGES

- Files added:
- Files modified:
- Files removed:
- Key refactors:

## APPLICATION BOUNDARY

- Canonical input:
- Canonical output:
- Dependency direction:
- History boundary:
- Provider boundary:
- Configuration boundary:
- UI boundary:

## TESTS

- Tests run:
- Result:
- Targeted Ruff:
- Targeted Black:
- Known/pre-existing failures:

## RISKS

- Remaining issues:
- Compatibility concerns:
- Deferred architecture decisions:

## GIT

- Commit: NOT CREATED
- Push: NOT PERFORMED
- Unrelated working-tree changes preserved: YES

STOP.