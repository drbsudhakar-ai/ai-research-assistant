# T002 — Configuration and Environment Baseline

**Status:** PLANNED  
**Phase:** Foundation and Existing-System Stabilization  
**Depends on:** T001 — Existing Implementation Audit, Controlled Refactor & Product Branding  
**Do not implement:** T003 or later tasks

---

## 1. Objective

Establish **one authoritative, typed, testable configuration and environment boundary** for the AI Research Assistant.

T002 must first inspect the existing configuration implementation and then consolidate it without unnecessarily rewriting working code.

The result must make configuration predictable for:

- application runtime;
- LLM provider;
- LLM model;
- generation parameters;
- database;
- filesystem paths;
- report/export behavior;
- developer/test mode;
- logging;
- environment-specific settings.

---

## 2. Required Reading

Before coding, read:

```text
PROJECT_CONTEXT.md
TASKS.md
CURSOR_INSTRUCTIONS.md
tasks/T002_CONFIGURATION_ENVIRONMENT_BASELINE.md
docs/architecture/CURRENT_ARCHITECTURE.md
```

Then inspect the actual repository.

The repository is authoritative.

---

## 3. Existing Configuration Discovery

Before modifying code, inspect and classify all current configuration sources, especially:

```text
app/config/
app/settings/
app/services/service_container.py
app/services/service_factory.py
streamlit_app.py
.env* / environment-variable usage
requirements.txt
pyproject.toml / setup configuration if present
```

Also inspect currently untracked/pre-existing configuration-related files such as, where present:

```text
app/config/export_config.py
app/config/model_config.py
app/config/pipeline_config.py
app/config/settings_manager.py
app/settings/
```

Do not assume these files are obsolete.

Classify each configuration mechanism as:

```text
CANONICAL
COMPATIBILITY
LEGACY / TO REMOVE
RUNTIME-LOCAL
```

Document important findings.

---

## 4. Target Architecture

Establish a clear boundary:

```text
Environment / config files
          ↓
Configuration loading
          ↓
Validated application configuration
          ↓
ServiceContainer / application services
          ↓
Infrastructure
```

UI code should consume configuration through approved application/configuration interfaces.

Do not allow individual UI pages to independently construct configuration objects.

Do not allow infrastructure services to read arbitrary environment variables throughout their implementation.

---

## 5. Configuration Domains

The final configuration model should clearly cover the applicable domains below.

### Application

Examples:

- application name;
- environment;
- debug/developer mode;
- timezone if required;
- version metadata where appropriate.

### LLM

Examples:

- provider;
- model;
- base URL/endpoint;
- request timeout;
- connection settings;
- generation parameters.

Supported providers must remain compatible with the existing project design.

Do not add new providers merely for T002.

### Generation

Where supported by the existing implementation:

- temperature;
- top-p;
- maximum output tokens;
- context limits;
- request timeout.

Use the project's existing terminology where possible.

### Database

Examples:

- database type;
- SQLite path;
- connection-related options;
- migration/schema location if applicable.

Do not change the database technology in T002.

Do not perform destructive migrations.

### Paths

Centralize approved paths for:

- data;
- uploads;
- temporary files;
- reports/exports;
- logs.

Avoid hard-coded machine-specific paths.

### Reports / Export

Only configuration already supported by the project should be consolidated.

Do not implement PDF/DOCX generation as part of T002.

### Logging

Where applicable:

- log level;
- log destination;
- development/production behavior.

Never place secrets in logs.

---

## 6. Environment Handling

Define a predictable precedence rule.

Unless the existing project has an explicitly documented alternative, prefer:

```text
explicit runtime/application configuration
        ↓
environment variables
        ↓
configuration file/defaults
        ↓
safe application defaults
```

Document the actual implemented precedence.

Do not silently change existing user-facing behavior without documenting it.

---

## 7. Secrets

Secrets must never be committed.

Examples:

```text
API keys
tokens
passwords
authorization headers
private credentials
```

Configuration objects may contain secret values at runtime, but:

- never log them;
- never print them;
- never expose them in UI diagnostics;
- never serialize them into reports;
- never commit `.env` files containing real credentials.

If the application has a settings UI, secret fields must remain appropriately protected.

---

## 8. Validation

Configuration should fail early and clearly when required values are invalid.

Validate applicable items such as:

- provider names;
- model names when validation is possible;
- URLs;
- numeric ranges;
- timeouts;
- filesystem paths;
- database paths;
- enum values.

Avoid over-validating values that legitimately depend on the external provider.

Example principle:

```text
configuration validation
        ≠
provider availability check
```

A provider connection test belongs to the appropriate service/settings workflow, not generic configuration loading.

---

## 9. Developer Mode

Preserve the existing developer/test mode behavior if present.

T002 must make its configuration explicit and predictable.

Developer mode must not accidentally:

- bypass security;
- expose secrets;
- modify production data;
- silently select a different provider;
- alter persisted history without clear configuration.

Do not remove developer mode.

---

## 10. ServiceContainer Integration

After consolidation, `ServiceContainer` must receive/use configuration through one authoritative mechanism.

Avoid patterns where values such as model, provider, and timeout are independently reconstructed from multiple configuration sources.

Prefer one validated configuration boundary.

The exact implementation should follow the existing architecture rather than introducing a new dependency-injection framework.

---

## 11. SettingsManager Integration

If `SettingsManager` exists, determine whether it is:

- the canonical persisted/user-settings layer;
- an adapter;
- a legacy mechanism;
- or a mixture of responsibilities.

Do not automatically delete or replace it.

Separate, where necessary:

```text
application configuration
vs
user-editable settings
vs
runtime secrets
```

These concepts must not be conflated.

A user setting can override an application default, but the precedence must be explicit.

---

## 12. Streamlit Integration

Streamlit pages must not become configuration owners.

The UI may:

- display configuration;
- request configuration changes through approved mechanisms;
- run connection tests;
- display safe configuration status.

The UI must not:

- duplicate configuration parsing;
- independently read arbitrary environment variables;
- construct conflicting configuration models.

---

## 13. Compatibility

T001 established canonical architecture while retaining compatibility modules.

T002 must preserve compatibility where reasonably safe.

For any compatibility configuration module:

```text
canonical source
        ↓
compatibility adapter/re-export
```

Do not create multiple independent configuration sources.

If a compatibility layer cannot be safely maintained, document the issue instead of deleting it without approval.

---

## 14. Testing Requirements

Add or update focused tests for:

### Configuration loading

- defaults;
- environment overrides;
- precedence;
- invalid values;
- missing required values.

### Configuration models

- valid values;
- invalid values;
- enum handling;
- numeric boundaries.

### Integration

- `ServiceContainer` construction;
- provider/model configuration propagation;
- database/path configuration propagation where practical.

### Security

- secrets are not logged;
- secrets are not included in diagnostic output.

Run:

```powershell
python -m pytest tests -q
```

Run targeted quality checks on T002-authored files:

```powershell
ruff check <T002 modified Python files>
black --check <T002 modified Python files>
```

Do not attempt to fix unrelated repository-wide lint/format debt.

---

## 15. Documentation

Update configuration documentation where necessary.

At minimum, document:

- supported environment/configuration variables actually implemented;
- defaults;
- precedence;
- provider/model configuration;
- database path;
- developer mode;
- safe secret handling.

Do not document configuration that does not actually exist.

If a configuration decision belongs to T003 or a later task, mark it as deferred rather than implementing it prematurely.

---

## 16. Scope Boundaries

### T002 SHOULD

- inspect existing configuration;
- consolidate duplicate configuration;
- establish canonical configuration contracts;
- integrate configuration with `ServiceContainer`;
- clarify settings/configuration boundaries;
- validate configuration;
- add focused tests;
- document the configuration baseline.

### T002 MUST NOT

- redesign domain models;
- redesign the analysis pipeline;
- redesign the Analyze page;
- implement job lifecycle;
- implement cancellation architecture;
- implement Streamlit rerun recovery;
- introduce authentication;
- introduce FastAPI;
- introduce LangGraph/LangChain;
- replace SQLite;
- replace Ollama;
- add new LLM providers;
- implement PDF/DOCX report generation;
- perform unrelated UI redesign;
- clean the entire repository's existing lint debt.

---

## 17. Change Discipline

Prefer:

```text
discover
→ consolidate
→ test
→ document
```

Avoid:

```text
discover
→ replace everything
→ create new framework
→ migrate unrelated code
```

If the existing implementation already satisfies a requirement, preserve it.

If two implementations conflict, identify:

```text
CANONICAL
COMPATIBILITY
LEGACY
```

and make the smallest safe change.

---

## 18. Acceptance Criteria

T002 is ready for architectural review only when:

- [ ] all existing configuration sources were inspected;
- [ ] canonical configuration ownership is documented;
- [ ] duplicate configuration paths are consolidated or explicitly classified;
- [ ] configuration precedence is deterministic;
- [ ] environment handling is documented;
- [ ] secrets are protected;
- [ ] `ServiceContainer` uses the canonical configuration boundary;
- [ ] `SettingsManager` responsibilities are clear;
- [ ] Streamlit does not independently own configuration;
- [ ] developer mode remains explicit and safe;
- [ ] focused configuration tests pass;
- [ ] T002-authored Ruff checks pass;
- [ ] T002-authored Black checks pass;
- [ ] no unrelated architecture was introduced;
- [ ] no destructive database changes occurred;
- [ ] documentation reflects actual implementation;
- [ ] no Git commit or push has been performed.

---

## 19. Required Completion Report

Use the concise format from `CURSOR_INSTRUCTIONS.md`:

```text
T002 STATUS: READY FOR ARCHITECTURAL REVIEW

DISCOVERY
- Configuration sources:
- Canonical configuration:
- Compatibility/legacy configuration:
- Important inconsistencies:

CHANGES
- Files added:
- Files modified:
- Files removed:
- Key refactors:

CONFIGURATION
- Precedence:
- Environment variables:
- Secrets handling:
- ServiceContainer integration:
- SettingsManager integration:

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
T002 STATUS: BLOCKED

REASON
- <short explanation>

WHAT WAS VERIFIED
- <short item>

REQUIRED DECISION
- <decision needed>
```

---

## 20. Review Gate

When implementation and tests are complete:

**STOP.**

Do not:

- commit;
- push;
- start T003.

The project owner and architecture reviewer will determine:

```text
ACCEPTED
CHANGES_REQUIRED
REJECTED
```

Only after explicit acceptance may T002 be committed and pushed.

---

## 21. Core T002 Principle

The goal is not to create more configuration files.

The goal is:

```text
Many configuration sources
        ↓
One clear configuration boundary
        ↓
Validated configuration
        ↓
Consistent application behavior
```

T002 should leave the project easier to configure, test, maintain, and extend without creating another parallel configuration architecture.
