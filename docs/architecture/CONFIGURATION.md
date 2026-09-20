# Configuration Baseline (T002)

This document describes **configuration that is actually implemented**.

## Ownership

| Concern | Owner | Classification |
| --- | --- | --- |
| Runtime application/LLM/paths/db/logging/export | `ApplicationConfig` via `app.config.loader` | **CANONICAL** |
| Product identity (name, author, credit) | `BrandConfig` | **CANONICAL** (T001) |
| Layout/page constants | `app.config.app_config`, `ui_config` | **COMPATIBILITY** re-exports / UI copy |
| LLM default constants | `app.config.llm_config` | **COMPATIBILITY** re-export of ApplicationConfig defaults |
| Persisted Settings-UI API settings | `SettingsManager` + `app.settings.api` | **CANONICAL for user-editable API settings**; not auto-applied to runtime |
| Streamlit session keys | `session_config` | **RUNTIME-LOCAL** UI session defaults |
| Navigation items | `navigation_config` | **RUNTIME-LOCAL** UI |
| Upload/theme copy constants | `common_config` | **RUNTIME-LOCAL** UI |
| `app.config.model_config` / `export_config` / `pipeline_config` | unused by live `streamlit_app` / `ServiceContainer` | **LEGACY** (do not delete without review) |
| Settings page `os.getenv` reads | untracked settings UI | **LEGACY / T016** |

## Load path

```text
optional .env (does not override existing process env)
        ↓
environment variables
        ↓
explicit load_application_config(overrides=...)
        ↓
validated ApplicationConfig
        ↓
ServiceContainer / initialize_database / logging
```

Implemented precedence (highest wins):

1. explicit `overrides` argument to `load_application_config`
2. environment variables
3. safe application defaults

`SettingsManager` JSON is **not** merged automatically. Doing so would change
the current live analysis defaults. Wiring that merge belongs with T016.

## Environment variables

Prefix: `AI_RA_`

| Variable | Default | Notes |
| --- | --- | --- |
| `AI_RA_ENV` | `development` | `development` / `test` / `production` |
| `AI_RA_DEVELOPER_MODE` | `false` | Simulated LLM responses; does not change DB path by itself |
| `AI_RA_DEBUG` | `false` | Debug flag only; does not bypass validation |
| `AI_RA_LOG_LEVEL` | `INFO` | `DEBUG`/`INFO`/`WARNING`/`ERROR`/`CRITICAL` |
| `AI_RA_LOG_FILE` | unset | Optional file destination |
| `AI_RA_API_PROVIDER` | `ollama` | Runtime supports **ollama only** |
| `AI_RA_MODEL` | `qwen3:4b` | Name is not probed at load time |
| `AI_RA_OLLAMA_BASE_URL` | `http://localhost:11434` | Passed to `ollama.Client(host=...)` |
| `AI_RA_API_KEY` | empty | Stored; not required for Ollama; never logged |
| `AI_RA_TEMPERATURE` | `0.2` | Applied to Ollama chat options |
| `AI_RA_TOP_P` | `0.95` | Stored on config; not sent in the live Ollama options yet |
| `AI_RA_MAX_TOKENS` | unset | Stored; omitted from live Ollama options when unset |
| `AI_RA_TIMEOUT` | `120` | Client timeout seconds |
| `AI_RA_CONNECT_TIMEOUT` | `30` | Validated; stored |
| `AI_RA_MAX_RETRIES` | `3` | Ollama generate retries |
| `AI_RA_MAX_INPUT_CHARACTERS` | `10000` | Stored for callers that already used `llm_config` |
| `AI_RA_DATA_DIR` | `<repo>/data` | Also relocates default uploads/tmp/reports/logs/db unless those vars are set |
| `AI_RA_UPLOADS_DIR` | `<data>/uploads` | |
| `AI_RA_TEMP_DIR` | `<data>/tmp` | |
| `AI_RA_REPORTS_DIR` | `<data>/reports` | |
| `AI_RA_LOGS_DIR` | `<data>/logs` | |
| `AI_RA_CONFIG_DIR` | `<repo>/config` | SettingsManager JSON directory |
| `AI_RA_DATABASE_PATH` | `<data>/history.db` | SQLite only |
| `AI_RA_EXPORT_DEFAULT_FORMAT` | `markdown` | `markdown` or `html` |

Relative paths resolve against the repository root, not the process cwd.

Copy `.env.example` to `.env` for local overrides. `.env` is gitignored.

## Developer mode

`AI_RA_DEVELOPER_MODE=true` makes `OllamaService` return a deterministic
simulated response. It does **not**:

- skip configuration validation
- log or display secrets
- switch provider
- change the database path unless `AI_RA_DATABASE_PATH` / `AI_RA_DATA_DIR` is set

## Secrets

- Do not commit `.env` files that contain credentials.
- `ApplicationConfig.to_safe_dict()` masks `api_key`.
- `SettingsManager.export_settings(include_secrets=False)` and
  `safe_diagnostics()` strip API keys.
- Logging uses `to_safe_dict()` at DEBUG.

Configuration loading does **not** test whether Ollama is running.

## ServiceContainer

`ServiceContainer(config=None)` uses `get_application_config()` and constructs
`OllamaService` / `LLMService` / `PaperAnalyzer` from that object.

## Streamlit

`streamlit_app.initialize_application()` loads configuration, configures
logging, creates runtime directories, then initializes the database.
Pages must call `get_application_config()` rather than parsing env vars.

## Deferred

- Applying `SettingsManager` JSON onto runtime config (T016)
- Additional live LLM providers
- PDF/DOCX export generation (T017–T018)
- Sending `top_p` / `max_tokens` on the live Ollama chat request
