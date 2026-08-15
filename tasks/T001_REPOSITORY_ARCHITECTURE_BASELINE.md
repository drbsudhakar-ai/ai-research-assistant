# T001 — Existing Implementation Audit, Refactor Baseline & Product Branding

**Priority:** P0  
**Type:** Audit + controlled refactor  
**Depends on:** `PROJECT_CONTEXT.md`  
**Next:** T002 only after T001 acceptance

## 1. Objective

Audit the **actual current repository**, identify architectural/implementation inconsistencies from previous development, perform only necessary controlled refactoring, and establish a clean baseline for subsequent tasks.

T001 also establishes the application's **visual identity, branding, credits, and document-branding foundation**.

This is NOT a full rewrite.

## 2. Read First

Cursor must read, in order:

1. `PROJECT_CONTEXT.md`
2. `TASKS.md`
3. `CURSOR_INSTRUCTIONS.md`
4. this task file

Then inspect the repository.

**Implement T001 only. Do not implement T002+.**

## 3. Phase A — Repository Discovery

Inspect at minimum:

```text
README.md
pyproject.toml / requirements.txt
streamlit_app.py
app/
tests/
configuration files
database/migrations
report/export modules
```

Identify the actual current implementations for:

- UI/pages/components
- application services
- domain models
- pipeline
- progress/job handling
- PDF extraction/preprocessing
- LLM providers
- configuration/settings
- database/repositories
- history
- reports/export
- tests

Create/update:

```text
docs/architecture/CURRENT_ARCHITECTURE.md
```

Keep it concise. Include:

- actual module map;
- execution flow;
- dependency direction;
- important interfaces;
- persistence flow;
- analysis flow;
- UI flow;
- known inconsistencies;
- technical debt;
- recommended corrections.

Document the repository as it actually exists. Do not document imaginary architecture.

## 4. Phase B — Verify Existing Contracts

Pay special attention to previously problematic areas.

### Pipeline

Verify:

- `Pipeline`
- `PipelineStep`
- `PipelineRunner`
- `PipelineBuilder`
- `ResearchAnalysisPipeline`
- factory/composition

There should be ONE canonical pipeline abstraction.

Do not retain competing `PipelineStage`/`PipelineStep` contracts without explicit justification.

### Progress

Verify:

- `ProgressManager`
- `ProgressRenderer`
- `ProgressEvent`
- progress state
- worker/job lifecycle
- Streamlit rerun behavior

Require:

- one canonical progress event contract;
- explicit state ownership;
- no duplicated progress loops;
- correct renderer lifecycle.

### Paper preparation

Verify consistency between:

- `PDFExtractor`
- `PaperPreprocessor`
- `PaperSectionExtractor`
- `PreparedPaper`
- `PaperSections`
- title/metadata extraction.

Find inconsistent method signatures and callers.

### Services

Verify:

- `ServiceContainer`
- `AnalysisService`
- provider services
- repository access

UI must not contain business orchestration or SQL.

### Settings

Verify one authoritative configuration path.

Avoid duplicated configuration state between:

```text
environment
session state
SettingsManager
provider instance
```

### Reports

Verify report generation is independent of Streamlit and consumes structured analysis/report data.

## 5. Phase C — Controlled Refactoring

Refactor only defects discovered in Phase A/B that are:

- clearly incorrect;
- causing current integration risk;
- violating an established boundary;
- creating duplicate contracts;
- preventing reliable future implementation.

### Do

- consolidate duplicate interfaces;
- fix broken imports;
- fix obvious contract mismatches;
- remove obsolete code only when proven redundant;
- improve dependency direction;
- preserve behavior where possible;
- add regression tests.

### Do NOT

- rewrite the application;
- replace frameworks;
- introduce major infrastructure;
- implement future tasks;
- redesign every screen;
- add authentication;
- add REST/FastAPI;
- add LangGraph/LangChain unless already part of the current approved architecture.

If a large redesign appears necessary:

**STOP and report it for architecture review.**

## 6. Phase D — Frontend Theme, Branding & Credits

T001 must establish a **centralized product branding/theme foundation**.

Do not scatter colors, fonts, logos, or product names across pages.

Create or consolidate a reusable presentation/theme mechanism providing centralized definitions for:

- application name;
- subtitle/tagline;
- logo/brand asset;
- primary/secondary visual identity;
- typography;
- page background/surface;
- cards;
- buttons;
- metrics;
- progress indicators;
- status indicators;
- spacing;
- common UI components.

Use a professional academic/research-oriented visual identity. Avoid excessive decorative UI.

Apply consistently to:

- Dashboard
- Analyze Paper
- History
- Settings
- About
- loading/error/empty states

### Branding

Default product name:

**AI Research Assistant**

Credit:

**Dr. B. Sudhakar**

Where an author/creator credit is appropriate:

**Developed by Dr. B. Sudhakar**

Do not invent institutional affiliations, awards, organizations, URLs, or claims. If official repository metadata already contains project information, use it consistently.

## 7. Branding Architecture

Create one source of truth for branding.

Conceptually:

```text
BrandConfig
    ├── application name
    ├── tagline
    ├── author/credit
    ├── logo
    ├── theme tokens
    └── document metadata
```

The exact location is determined after repository inspection.

Pages must consume shared branding configuration rather than hard-code product name, author, or theme values repeatedly.

## 8. Frontend Quality Baseline

Correct obvious presentation inconsistencies without performing a complete redesign.

All screens should have:

- consistent page title;
- consistent identity;
- consistent spacing;
- consistent buttons;
- consistent status presentation;
- consistent typography;
- useful empty states;
- useful error states;
- useful loading states;
- no accidental debug output;
- no raw exception dumps to normal users.

## 9. Downloadable Document Branding

All currently supported downloadable/generated documents must use the same product identity.

Cover, where applicable:

- Markdown
- HTML
- PDF
- DOCX
- research summary
- executive summary
- citation-ready report

Where the format permits, include:

- application name;
- report title;
- paper title;
- author/credit;
- generation date/time;
- professional header/footer;
- consistent typography;
- page numbering for paginated formats;
- report metadata.

Example:

```text
AI Research Assistant
Research Paper Analysis Report

Paper: <paper title>

Developed by Dr. B. Sudhakar
Generated: <date/time>
```

Never invent data.

Report generation must remain independent of Streamlit. Renderers should consume structured report data plus branding configuration.

Do not duplicate report templates inside UI pages.

## 10. Branding Assets

Inspect existing:

- logo;
- favicon;
- icons;
- author information;
- project metadata.

Reuse valid existing assets.

If an asset is missing, do not invent institutional branding. Use a minimal neutral placeholder only if necessary and document the missing asset.

## 11. Tests

Add/update tests for changed contracts.

At minimum:

### Architecture/integration

- canonical pipeline imports;
- service construction;
- application startup/import path;
- important dependency boundaries where practical.

### Domain/contracts

- corrected constructor signatures;
- serialization;
- `PaperSections` behavior if changed.

### Branding

- branding configuration loads;
- required product/author metadata exists;
- branding components can render;
- report metadata receives branding configuration.

### Reports

Test supported existing generators, including:

- Markdown;
- HTML;
- PDF/DOCX where already implemented.

Avoid expensive cosmetic UI tests unless an existing UI test mechanism is available.

## 12. Regression Validation

Run existing tests, then targeted tests.

At minimum attempt:

```text
pytest
ruff check .
black --check .
```

Run existing type checking if configured.

Do not hide existing failures.

Classify failures as:

```text
pre-existing
introduced by T001
fixed by T001
environment/dependency related
```

## 13. Acceptance Criteria

T001 is accepted only when:

- [ ] Repository inspected.
- [ ] Actual architecture documented.
- [ ] Actual execution flow documented.
- [ ] Duplicate/contradictory contracts identified.
- [ ] Critical inconsistencies fixed or explicitly reported.
- [ ] No uncontrolled rewrite occurred.
- [ ] Pipeline has one clear canonical contract.
- [ ] Progress has one clear contract.
- [ ] PDF/preparation contracts are consistent.
- [ ] Service boundaries are clear.
- [ ] Configuration ownership is clear.
- [ ] Frontend has centralized professional theme/branding.
- [ ] Major screens use shared branding.
- [ ] Author/credit is consistent.
- [ ] Existing downloadable reports use shared branding.
- [ ] Report branding is independent of Streamlit.
- [ ] Tests added/updated.
- [ ] Existing tests executed.
- [ ] Formatting/linting checked.
- [ ] No secrets/debug artifacts introduced.
- [ ] Git diff contains only T001 changes.

## 14. Required Cursor Completion Report

Keep the report concise. Use exactly:

```text
T001 STATUS: READY FOR ARCHITECTURAL REVIEW

DISCOVERY
- Architecture:
- Major components:
- Critical inconsistencies:

CHANGES
- Files added:
- Files modified:
- Files removed:
- Key refactors:

BRANDING
- Theme location:
- Branding source of truth:
- Screens updated:
- Report formats updated:

TESTS
- Tests run:
- Result:
- Known failures:

RISKS
- Remaining issues:
- Deferred architecture decisions:

GIT
- Commit: NOT CREATED
- Push: NOT PERFORMED
```

Do not provide a long narrative unless requested.

## 15. Stop Conditions

Stop and request review if:

1. A large rewrite appears necessary.
2. Existing public contracts must be broken.
3. Database schema changes are required beyond a clearly local correction.
4. A new major framework is required.
5. A new external service is required.
6. Authentication/authorization becomes necessary.
7. A major concurrency architecture change is required.
8. Existing data may be lost or destructively migrated.
9. The correct architectural choice is ambiguous.

## 16. Git Rule

Do NOT commit or push T001 until architectural/technology acceptance is explicitly granted.

Expected lifecycle:

```text
Inspect
  ↓
Implement
  ↓
Test
  ↓
Report
  ↓
Architecture Review
  ↓
Corrections
  ↓
Acceptance
  ↓
Commit
  ↓
Push
```

## 17. T001 Boundary

T001 establishes the foundation.

It does NOT implement:

- new analysis capabilities;
- new LLM providers;
- new database features;
- new REST APIs;
- new report formats;
- authentication;
- multi-user features;
- RAG;
- agents;
- advanced research intelligence.

## Final Instruction

**Inspect first. Refactor only where justified. Establish the shared branding foundation. Test everything changed. Report concisely. Stop for architectural acceptance.**

T001 must leave the repository more consistent and predictable than it was found, without turning the task into a rewrite.
