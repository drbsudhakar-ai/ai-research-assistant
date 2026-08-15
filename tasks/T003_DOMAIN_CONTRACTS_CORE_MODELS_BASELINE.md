# T003 — Domain Contracts & Core Models Baseline

**Status:** PLANNED  
**Phase:** Domain Foundation  
**Depends on:** T001 — Architecture Baseline; T002 — Configuration and Environment Baseline  
**Do not implement:** T004 or later tasks

---

## 1. Objective

Establish a **clear, canonical, typed domain-contract layer** for the AI Research Assistant.

T003 must inspect the existing models and contracts first, identify duplicate/conflicting representations, and establish one authoritative representation for the core analysis domain.

The goal is:

```text
Input
  ↓
Domain contracts
  ↓
Application services / pipeline
  ↓
Infrastructure
  ↓
Persistence / presentation
```

The domain models must not depend on Streamlit, Ollama, SQLite implementation details, report rendering, or other UI/infrastructure concerns.

---

## 2. Required Reading

Before coding, read:

```text
PROJECT_CONTEXT.md
TASKS.md
CURSOR_INSTRUCTIONS.md
tasks/T003_DOMAIN_CONTRACTS_CORE_MODELS_BASELINE.md
docs/architecture/CURRENT_ARCHITECTURE.md
docs/architecture/CONFIGURATION.md
```

Then inspect the actual repository.

The repository is authoritative.

---

## 3. Existing Model Discovery

Before modifying code, inspect all existing model/contract implementations, especially:

```text
app/models/
app/core/analysis/
app/core/pipeline/
app/core/progress/
app/services/
app/storage/
app/document/
app/prompts/
app/controllers/
```

Pay particular attention to existing or pre-existing files such as:

```text
app/models/paper_sections.py
app/models/prepared_paper.py
app/models/analysis_request.py
app/models/llm_response.py
```

Also inspect analysis status definitions, progress events, pipeline step contracts, history persistence models, report/export structures, PDF extraction/preparation result models, and any dataclasses/Pydantic models/Enums used across layers.

Do not assume untracked files are obsolete.

---

## 4. Classification Requirement

For every significant model/contract discovered, classify it as:

```text
CANONICAL
COMPATIBILITY
LEGACY / UNUSED
DUPLICATE / CONFLICTING
INFRASTRUCTURE-LOCAL
UI-LOCAL
```

Document important conflicts.

Do not delete a model merely because it appears unused.

---

## 5. Target Domain Boundary

The target dependency direction is:

```text
                 DOMAIN CONTRACTS
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

Core domain contracts must remain independent of:

```text
Streamlit
Ollama
SQLite
filesystem implementation
HTTP clients
report rendering
environment variables
session_state
```

Imports must follow the dependency direction.

---

# 6. Core Contracts

Establish or stabilize the following concepts **only where they are already supported by the existing application**.

Do not invent unnecessary abstractions.

### 6.1 Paper / Document Identity

Define the contract representing the analyzed document/paper.

Where applicable, distinguish:

```text
filename
source/path identity
document metadata
page count
content/extracted text
```

Do not put filesystem operations into the model.

Do not make the model responsible for reading PDFs.

### 6.2 Paper Sections

Stabilize the existing `PaperSections` representation.

It should provide a predictable representation for sections such as:

```text
title
abstract
introduction
related work
methodology
results
discussion
conclusion
references
```

Only retain fields supported by the existing implementation.

Important:

- section content may be absent;
- empty sections must be represented safely;
- consumers must not depend on dictionary-vs-dataclass ambiguity;
- section counting must use an explicit contract/API rather than assuming `len(PaperSections)` works.

Do not redesign section extraction logic in T003.

### 6.3 Prepared Paper

Stabilize `PreparedPaper`.

It represents prepared downstream analysis input and may contain supported metadata, extracted text, sections, page count, and content statistics.

It must not perform extraction and must not depend on Streamlit.

### 6.4 Analysis Request

Stabilize `AnalysisRequest` if present.

Clearly separate:

```text
request
vs
prepared input
vs
analysis result
```

The request model must not become a service/controller.

### 6.5 Analysis Result

Identify and stabilize the canonical analysis-result representation.

Downstream layers must consume it without depending on Streamlit session state, UI widgets, HTML fragments, or provider-specific response objects.

Do not redesign report formatting.

### 6.6 LLM Response

Review `LLMResponse`.

It must represent provider-neutral model output.

Do not make it depend on Ollama/OpenAI/LangChain SDK response classes. Provider adapters translate provider responses into the project contract.

### 6.7 Analysis Status

Stabilize the analysis status vocabulary.

Inspect states such as:

```text
PENDING
RUNNING
COMPLETED
FAILED
CANCEL_REQUESTED
CANCELLED
```

Do not implement cancellation lifecycle in T003.

Do not incorrectly collapse `CANCEL_REQUESTED` into `CANCELLED`.

### 6.8 Progress Contract

Review existing progress/event contracts.

Where supported, distinguish:

```text
stage
progress
message
status
timestamp / sequencing information
```

The contract must be provider- and UI-independent.

Do not redesign the progress UI.

### 6.9 History Contract

Separate the analysis/history application contract from:

```text
SQLite row / repository implementation
```

Do not put SQLite behavior into domain models.

Do not redesign the database schema or perform migrations.

### 6.10 Report / Export Contract

Inspect existing report/export data structures.

Preserve a common analysis-result contract where already supported.

Do not implement PDF/DOCX generation and do not make domain models responsible for rendering.

---

# 7. Type and Validation Rules

Use the project's existing model technology where practical.

Do not introduce a second validation framework without a clear need.

Contracts should:

- use explicit types;
- reject invalid structural values where appropriate;
- distinguish optional values from empty strings where meaningful;
- avoid mutable default values;
- avoid hidden side effects;
- have predictable serialization where required.

Use enums for controlled vocabularies where appropriate.

Do not duplicate the same enum in multiple modules.

---

# 8. Immutability and Mutation

Determine which contracts should be immutable/value-like and which legitimately represent mutable runtime state.

Prefer immutable/value-oriented models for:

```text
requests
responses
metadata
paper section snapshots
configuration-derived values
```

Runtime/session/job state may remain mutable where the current architecture requires it.

Do not force immutability onto deliberately mutable runtime objects.

Document important decisions.

---

# 9. Serialization

Where contracts cross boundaries, define predictable serialization for:

```text
domain ↔ persistence
domain ↔ API
domain ↔ report renderer
domain ↔ UI
```

Do not serialize:

```text
Streamlit objects
file handles
database connections
LLM client instances
locks/threads
```

---

# 10. Error Contracts

Inspect existing domain/application exceptions.

Where appropriate, distinguish:

```text
validation error
document/preparation error
analysis error
provider error
persistence error
configuration error
```

Do not redesign the entire exception hierarchy if the existing system is adequate.

---

# 11. Compatibility Strategy

Apply the established compatibility rule:

```text
canonical contract
       ↓
compatibility adapter / alias
```

Avoid multiple independent models representing the same concept.

For duplicate contracts:

1. identify the canonical contract;
2. update active consumers where safely possible;
3. retain compatibility aliases/adapters when necessary;
4. document remaining legacy modules;
5. do not mass-delete historical implementation.

---

# 12. Service and Pipeline Integration

Update only contracts required to make the live architecture consistent.

The live path established by T001 is approximately:

```text
Streamlit
   ↓
ServiceContainer
   ↓
AnalysisService
   ↓
ResearchAnalysisPipelineFactory
   ↓
PipelineRunner
   ↓
BasePipelineStep implementations
```

Ensure contracts passed between these layers are consistent.

Do not redesign the pipeline.

Do not solve duplicate extraction/preparation lifecycle; that remains a later task.

---

# 13. Persistence Boundary

Use the intended direction:

```text
Domain contract
      ↓
Repository interface / application boundary
      ↓
SQLite implementation
```

Do not allow domain models to import SQLite or contain SQL.

Do not redesign the history schema.

---

# 14. UI Boundary

UI components may transform domain contracts into presentation models.

Domain models must not import:

```python
streamlit
```

or depend on:

```text
st.session_state
st.button
st.progress
st.download_button
```

Do not redesign screens in T003.

---

# 15. Tests

Add focused tests covering:

### Construction
- valid construction;
- required fields;
- optional fields;
- default behavior.

### Validation
- invalid values;
- invalid enum/state values;
- boundary values;
- missing required values.

### Compatibility
- compatibility aliases/adapters resolve correctly;
- active consumers use canonical representation.

### Serialization
Where applicable:
- round-trip serialization;
- safe representation;
- provider-neutral representation.

### Integration
Where practical:
- pipeline step input/output;
- `AnalysisService`;
- `ServiceContainer`;
- history boundary.

Run:

```powershell
python -m pytest tests -q
```

Run targeted checks:

```powershell
ruff check <T003 modified Python files>
black --check <T003 modified Python files>
```

Do not fix unrelated repository-wide lint/format debt.

---

# 16. Documentation

Update:

```text
docs/architecture/CURRENT_ARCHITECTURE.md
```

where required.

Add a domain-contract document if existing architecture documentation does not adequately describe the contracts.

Document:

- canonical models;
- important enums;
- dependency direction;
- compatibility aliases;
- major deferred conflicts.

Do not document models as canonical unless they are actually used by the live path.

---

# 17. Scope Boundaries

## T003 SHOULD

- discover existing domain models;
- classify competing contracts;
- establish canonical models;
- remove ambiguity between request/result/state;
- stabilize types and validation;
- stabilize provider-neutral response contracts;
- establish persistence/UI boundaries;
- add focused tests;
- update architecture documentation.

## T003 MUST NOT

- redesign the analysis pipeline;
- redesign Analyze UI;
- implement cancellation;
- implement job registry;
- implement job recovery/rerun;
- implement authentication;
- introduce FastAPI;
- introduce LangGraph/LangChain;
- replace SQLite;
- replace Ollama;
- add providers;
- implement PDF/DOCX reports;
- redesign report rendering;
- redesign configuration;
- implement SettingsManager runtime merge;
- perform destructive DB migrations;
- clean unrelated repository-wide lint debt.

---

# 18. Acceptance Criteria

T003 is ready for architectural review only when:

- [ ] all significant domain models/contracts were inspected;
- [ ] each significant model is classified;
- [ ] canonical contracts are explicitly identified;
- [ ] duplicate/conflicting representations are reduced or documented;
- [ ] `PaperSections` has a predictable interface;
- [ ] `PreparedPaper` is a pure data contract;
- [ ] `AnalysisRequest` and analysis result are clearly separated;
- [ ] `LLMResponse` is provider-neutral;
- [ ] analysis status vocabulary is stable;
- [ ] `CANCEL_REQUESTED` and `CANCELLED` are not incorrectly conflated;
- [ ] progress contracts are UI-independent;
- [ ] history contracts are persistence-independent;
- [ ] report/export contracts do not render documents;
- [ ] domain models have no Streamlit dependency;
- [ ] domain models have no direct SQLite dependency;
- [ ] service/pipeline boundaries use canonical contracts;
- [ ] compatibility aliases/adapters are documented;
- [ ] focused tests pass;
- [ ] T003-authored Ruff checks pass;
- [ ] T003-authored Black checks pass;
- [ ] architecture documentation is updated;
- [ ] no unrelated architecture was introduced;
- [ ] no Git commit or push has been performed.

---

# 19. Required Completion Report

Return exactly:

```text
T003 STATUS: READY FOR ARCHITECTURAL REVIEW

DISCOVERY
- Models/contracts inspected:
- Canonical contracts:
- Compatibility/legacy contracts:
- Important conflicts:

CHANGES
- Files added:
- Files modified:
- Files removed:
- Key refactors:

DOMAIN CONTRACTS
- Paper/PreparedPaper:
- PaperSections:
- AnalysisRequest:
- AnalysisResult:
- LLMResponse:
- AnalysisStatus:
- Progress:
- History:
- Report/Export:

BOUNDARIES
- Pipeline:
- Persistence:
- UI:
- Provider:

TESTS
- Tests run:
- Result:
- Targeted Ruff:
- Targeted Black:

RISKS
- Remaining issues:
- Deferred architecture decisions:

GIT
- Commit: NOT CREATED
- Push: NOT PERFORMED
```

If blocked:

```text
T003 STATUS: BLOCKED

REASON
- <short explanation>

WHAT WAS VERIFIED
- <short item>

REQUIRED DECISION
- <decision needed>
```

---

# 20. Review Gate

When implementation and tests are complete:

**STOP.**

Do not:

- commit;
- push;
- start T004.

The project owner and architecture/technology reviewers will determine:

```text
ACCEPTED
CHANGES_REQUIRED
REJECTED
```

Only after explicit acceptance may T003 be committed and pushed.

---

# 21. Core T003 Principle

The goal is not to create many new models.

The goal is:

```text
Multiple competing representations
             ↓
Discover + classify
             ↓
Canonical domain contracts
             ↓
Stable boundaries
             ↓
Predictable application behavior
```

T003 should make later work on:

```text
job lifecycle
cancellation
Analyze use cases
history
API boundaries
reporting
```

safer because those tasks can depend on stable contracts rather than continually changing data structures.
