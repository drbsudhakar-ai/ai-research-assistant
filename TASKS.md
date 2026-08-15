# AI Research Assistant — Master Task Plan

**Project:** AI Research Assistant  
**Primary UI:** Streamlit  
**Initial LLM:** Ollama / qwen3:4b  
**Database:** SQLite  
**Engineering model:** Cursor implements; Dr. B. Sudhakar + ChatGPT review and accept.

---

## 1. Purpose

This file is the master implementation roadmap.

Cursor must work **one task at a time**.

For every task:

```text
Read context
→ Inspect repository
→ Implement approved scope
→ Test
→ Report
→ Architecture review
→ Corrections if required
→ Acceptance
→ Git commit
→ Git push
→ Next task
```

**Do not skip architectural acceptance.**

---

## 2. Source-of-Truth Documents

Read in this order:

1. `PROJECT_CONTEXT.md`
2. `TASKS.md`
3. `CURSOR_INSTRUCTIONS.md`
4. the assigned `tasks/TXXX_*.md`

The actual repository is authoritative for current code.

---

## 3. Task Status

Use:

- `PLANNED`
- `IN_PROGRESS`
- `READY_FOR_REVIEW`
- `CHANGES_REQUIRED`
- `ACCEPTED`
- `BLOCKED`

Only the reviewers may mark a task `ACCEPTED`.

---

# 4. Implementation Roadmap

## Phase 0 — Foundation and Existing-System Stabilization

### T001 — Existing Implementation Audit, Controlled Refactor & Product Branding
**Status:** ACCEPTED

Audit the existing implementation and establish a stable baseline.

Scope:

- repository/architecture inspection;
- current execution-flow verification;
- pipeline contract verification;
- progress/job lifecycle verification;
- PDF/preprocessing contract verification;
- service/container verification;
- settings/configuration verification;
- report architecture verification;
- controlled refactoring of confirmed inconsistencies;
- centralized frontend theme;
- product branding;
- Dr. B. Sudhakar credit;
- branded downloadable documents;
- regression tests;
- current architecture documentation.

**Important:** T001 is not a rewrite.

---

### T002 — Configuration and Environment Baseline
**Status:** PLANNED

Establish one authoritative configuration model for:

- application settings;
- LLM provider;
- model;
- generation parameters;
- paths;
- database;
- developer mode;
- logging;
- environment-specific configuration.

---

### T003 — Domain Models and Application Contracts
**Status:** PLANNED

Establish stable contracts for:

- paper;
- paper metadata;
- paper sections;
- prepared paper;
- analysis run;
- analysis result;
- job status;
- progress;
- errors;
- report metadata.

---

# Phase 1 — Persistence

### T004 — Database Schema and Migrations
**Status:** PLANNED

Design and implement reviewed SQLite schema and migration strategy.

Cover:

- papers;
- analysis runs;
- analysis results;
- reports;
- execution metadata;
- timestamps;
- status;
- indexes;
- constraints.

No destructive migration without explicit approval.

---

### T005 — Repository and Persistence Services
**Status:** PLANNED

Implement repository abstractions and SQLite implementations.

UI and domain code must not contain SQL.

---

# Phase 2 — Paper Ingestion

### T006 — PDF Validation and Extraction
**Status:** PLANNED

Stabilize:

- PDF validation;
- file safety;
- text extraction;
- metadata;
- page statistics;
- extraction errors;
- large-file handling.

---

### T007 — Paper Preparation and Section Intelligence
**Status:** PLANNED

Stabilize:

- preprocessing;
- title extraction;
- section extraction;
- `PaperSections`;
- `PreparedPaper`;
- section normalization;
- content limits.

---

# Phase 3 — LLM and Analysis

### T008 — LLM Provider Abstraction
**Status:** PLANNED

Establish a provider-neutral interface.

Initial provider:

- Ollama.

Architecture must allow future providers without coupling analysis logic to a specific SDK.

---

### T009 — Prompt and Analysis Contracts
**Status:** PLANNED

Establish:

- prompt construction;
- structured input;
- structured output;
- response validation;
- token/content controls;
- provider metadata.

---

### T010 — Research Analysis Pipeline
**Status:** PLANNED

Implement/stabilize:

```text
Validate
→ Prepare
→ Analyze
→ Persist
```

Pipeline steps must be independently testable.

---

# Phase 4 — Jobs, Progress and Reliability

### T011 — Analysis Job Lifecycle
**Status:** PLANNED

Establish:

- job identity;
- queued/running/completed/failed/cancelled states;
- worker ownership;
- cancellation semantics;
- failure handling;
- stale-job handling where required.

---

### T012 — Progress and Streamlit Rerun Recovery
**Status:** PLANNED

Make progress reliable across Streamlit reruns.

Cover:

- progress persistence;
- stage;
- percentage;
- elapsed time;
- cancellation request;
- completion;
- failure;
- UI reattachment.

---

# Phase 5 — Frontend

### T013 — Application Shell and Shared UI Components
**Status:** PLANNED

Stabilize:

- navigation;
- theme;
- layout;
- shared components;
- alerts;
- status indicators;
- loading states;
- empty states;
- error states.

Branding established in T001 must remain centralized.

---

### T014 — Analyze Paper Experience
**Status:** PLANNED

Implement the complete workflow:

```text
Input
→ Upload
→ Validation
→ Preview
→ Paper Information
→ Preparation
→ Analyze
→ Progress
→ Result
→ Reports
```

Cover duplicate clicks, cancellation, failure, and rerun recovery.

---

### T015 — History Experience
**Status:** PLANNED

Implement:

- history list;
- filtering/search;
- analysis details;
- status;
- reopening results;
- report access;
- failed/cancelled runs.

---

### T016 — Settings Experience
**Status:** PLANNED

Implement/review:

- provider;
- connection;
- model;
- generation;
- advanced settings;
- validation;
- safe secret handling;
- test connection.

---

# Phase 6 — Reports

### T017 — Report Generation Architecture
**Status:** PLANNED

Establish structured report data and renderer abstraction.

Avoid UI-specific report generation.

---

### T018 — Branded Report Formats
**Status:** PLANNED

Support currently approved formats such as:

- Markdown;
- HTML;
- PDF;
- DOCX.

Use centralized branding and report metadata.

---

# Phase 7 — API and Extensibility

### T019 — Application API Boundary
**Status:** PLANNED

Formalize application use cases so future REST/API frontends can consume them.

Do not introduce FastAPI unless separately approved.

---

### T020 — Health, Diagnostics and Observability
**Status:** PLANNED

Implement appropriate:

- health checks;
- provider diagnostics;
- structured logging;
- error correlation;
- safe diagnostics.

Never expose secrets.

---

# Phase 8 — Quality

### T021 — Comprehensive Test Suite
**Status:** PLANNED

Expand:

- unit tests;
- integration tests;
- pipeline tests;
- persistence tests;
- provider tests;
- report tests;
- UI-critical workflow tests.

---

### T022 — Performance and Resource Optimization
**Status:** PLANNED

Address:

- large PDFs;
- prompt size;
- duplicate LLM calls;
- memory;
- CPU usage;
- long-running jobs;
- report generation.

Preserve correctness.

---

### T023 — Release Hardening and Documentation
**Status:** PLANNED

Complete:

- README;
- setup;
- configuration documentation;
- architecture documentation;
- troubleshooting;
- test instructions;
- release checklist;
- clean Git state.

---

# 5. Dependency Order

Primary sequence:

```text
T001
 ↓
T002
 ↓
T003
 ↓
T004
 ↓
T005
 ↓
T006
 ↓
T007
 ↓
T008
 ↓
T009
 ↓
T010
 ↓
T011
 ↓
T012
 ↓
T013
 ↓
T014
 ↓
T015
 ↓
T016
 ↓
T017
 ↓
T018
 ↓
T019
 ↓
T020
 ↓
T021
 ↓
T022
 ↓
T023
```

Parallel work may be approved only when dependencies are clearly satisfied.

---

# 6. Universal Acceptance Requirements

Every task must:

- stay within its defined scope;
- preserve approved architecture;
- include appropriate tests;
- avoid secrets;
- avoid destructive data changes;
- avoid unnecessary dependencies;
- document important decisions;
- pass applicable lint/format/test checks;
- report known failures honestly;
- leave unrelated code unchanged where possible.

A task is not complete merely because the application starts.

---

# 7. Git Policy

No task is committed or pushed before acceptance.

Preferred commit pattern:

```text
feat(T001): stabilize architecture and branding
feat(T002): establish configuration baseline
fix(T012): recover analysis progress after rerun
test(T021): expand analysis integration coverage
```

One logical task should normally map to one logical commit.

---

# 8. Review Gate

At the end of each task Cursor must stop at:

```text
READY_FOR_REVIEW
```

Reviewers decide:

```text
ACCEPTED
CHANGES_REQUIRED
REJECTED
```

Only `ACCEPTED` permits Git commit/push and progression to the next task.

---

# 9. Current Starting Point

The first task is:

**T001 — Existing Implementation Audit, Controlled Refactor & Product Branding**

Do not start T002 until T001 has been reviewed and accepted.
