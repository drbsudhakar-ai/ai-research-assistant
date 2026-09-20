"""
===============================================================================
File: app/ui/components/settings/provider_settings.py
Project: AI Research Assistant
Version: 2.0.0
Author: OpenAI
License: MIT

Production-ready Provider Settings Component

Part 1/8
- Imports
- Constants
- Enums
- Dataclasses
- Provider Registry
===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from app.ui.components.settings.api_settings import (
    get_provider_metadata,
    get_available_providers,
)

import streamlit as st

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

DEFAULT_TIMEOUT = 60
DEFAULT_RETRIES = 3

DEFAULT_OLLAMA_ENDPOINT = "http://localhost:11434"

SESSION_PROVIDER_STATE = "provider_settings_state"

# =============================================================================
# Provider Enums
# =============================================================================


class ProviderCategory(str, Enum):
    """
    Category of LLM provider.
    """

    LOCAL = "Local"
    CLOUD = "Cloud"


class ProviderType(str, Enum):
    """
    Supported LLM providers.
    """

    OLLAMA = "Ollama"

    OPENAI = "OpenAI"

    GEMINI = "Gemini"

    DEEPSEEK = "DeepSeek"

    AZURE_OPENAI = "Azure OpenAI"

    OPENROUTER = "OpenRouter"

    CUSTOM = "Custom"


class ConnectionStatus(str, Enum):
    """
    Current provider connection state.
    """

    UNKNOWN = "Unknown"

    TESTING = "Testing"

    CONNECTED = "Connected"

    DISCONNECTED = "Disconnected"

    ERROR = "Error"


# =============================================================================
# Provider Metadata
# =============================================================================


@dataclass(slots=True)
class ProviderMetadata:
    """
    Static metadata describing an LLM provider.

    This class contains only UI and descriptive information.
    Runtime configuration belongs to ProviderState.
    """

    provider: ProviderType

    category: ProviderCategory

    display_name: str

    description: str

    icon: str

    homepage: str | None = None

    default_endpoint: str | None = None

    requires_api_key: bool = True

    supports_streaming: bool = True

    supports_tools: bool = True

    supports_vision: bool = False

    supports_embeddings: bool = False

    supports_function_calling: bool = False


# =============================================================================
# Runtime Provider State
# =============================================================================


@dataclass(slots=True)
class ProviderState:
    """
    Mutable runtime state used by the Streamlit UI.
    """

    provider: ProviderType = ProviderType.OLLAMA

    endpoint: str = DEFAULT_OLLAMA_ENDPOINT

    api_key: str = ""

    selected_model: str = ""

    available_models: list[str] = field(default_factory=list)

    timeout: int = DEFAULT_TIMEOUT

    retries: int = DEFAULT_RETRIES

    enabled: bool = True

    is_default: bool = True

    configured: bool = False

    connection_status: ConnectionStatus = ConnectionStatus.UNKNOWN


# =============================================================================
# Provider Registry
# =============================================================================

PROVIDERS: dict[ProviderType, ProviderMetadata] = {
    ProviderType.OLLAMA: ProviderMetadata(
        provider=ProviderType.OLLAMA,
        category=ProviderCategory.LOCAL,
        display_name="Ollama",
        description=(
            "Run open-source LLMs locally for maximum privacy and "
            "zero API cost."
        ),
        icon="🦙",
        homepage="https://ollama.com",
        default_endpoint=DEFAULT_OLLAMA_ENDPOINT,
        requires_api_key=False,
        supports_streaming=True,
        supports_tools=True,
        supports_vision=True,
        supports_embeddings=True,
    ),
    ProviderType.OPENAI: ProviderMetadata(
        provider=ProviderType.OPENAI,
        category=ProviderCategory.CLOUD,
        display_name="OpenAI",
        description=(
            "Access GPT models using the OpenAI API."
        ),
        icon="🟢",
        homepage="https://platform.openai.com",
        requires_api_key=True,
        supports_streaming=True,
        supports_tools=True,
        supports_vision=True,
        supports_embeddings=True,
        supports_function_calling=True,
    ),
    ProviderType.GEMINI: ProviderMetadata(
        provider=ProviderType.GEMINI,
        category=ProviderCategory.CLOUD,
        display_name="Google Gemini",
        description=(
            "Google's Gemini family of multimodal language models."
        ),
        icon="🔷",
        homepage="https://ai.google.dev",
        requires_api_key=True,
        supports_streaming=True,
        supports_tools=True,
        supports_vision=True,
        supports_embeddings=True,
    ),
    ProviderType.DEEPSEEK: ProviderMetadata(
        provider=ProviderType.DEEPSEEK,
        category=ProviderCategory.CLOUD,
        display_name="DeepSeek",
        description=(
            "DeepSeek reasoning and coding models."
        ),
        icon="🧠",
        homepage="https://www.deepseek.com",
        requires_api_key=True,
        supports_streaming=True,
        supports_tools=True,
        supports_embeddings=True,
    ),
    ProviderType.AZURE_OPENAI: ProviderMetadata(
        provider=ProviderType.AZURE_OPENAI,
        category=ProviderCategory.CLOUD,
        display_name="Azure OpenAI",
        description=(
            "Azure-hosted OpenAI deployments."
        ),
        icon="☁️",
        homepage="https://azure.microsoft.com",
        requires_api_key=True,
        supports_streaming=True,
        supports_tools=True,
        supports_vision=True,
        supports_function_calling=True,
    ),
    ProviderType.OPENROUTER: ProviderMetadata(
        provider=ProviderType.OPENROUTER,
        category=ProviderCategory.CLOUD,
        display_name="OpenRouter",
        description=(
            "Unified gateway for multiple AI providers."
        ),
        icon="🛣️",
        homepage="https://openrouter.ai",
        requires_api_key=True,
        supports_streaming=True,
        supports_tools=True,
        supports_vision=True,
        supports_function_calling=True,
    ),
    ProviderType.CUSTOM: ProviderMetadata(
        provider=ProviderType.CUSTOM,
        category=ProviderCategory.CLOUD,
        display_name="Custom OpenAI Compatible",
        description=(
            "Any OpenAI-compatible endpoint."
        ),
        icon="⚙️",
        requires_api_key=False,
        supports_streaming=True,
        supports_tools=True,
        supports_function_calling=True,
    ),
}

# =============================================================================
# Callback Type Aliases
# =============================================================================

SaveCallback = Callable[[ProviderState], None]

ConnectionTestCallback = Callable[[ProviderState], bool]

RefreshModelsCallback = Callable[[ProviderState], list[str]]

# =============================================================================
# Provider Settings Component
# =============================================================================


class ProviderSettingsComponent:
    """
    Production-ready Provider Settings UI component.

    Responsibilities
    ----------------
    • Provider selection
    • API configuration
    • Model selection
    • Runtime options
    • Connection testing
    • Model refresh
    • Validation
    • Session-state management

    This component does NOT perform persistence itself.
    Configuration storage is delegated through callbacks.
    """

    def __init__(
        self,
        *,
        state: ProviderState | None = None,
        on_save: SaveCallback | None = None,
        on_test_connection: ConnectionTestCallback | None = None,
        on_refresh_models: RefreshModelsCallback | None = None,
    ) -> None:
        self.state = state or ProviderState()

        self._on_save = on_save

        self._on_test_connection = on_test_connection

        self._on_refresh_models = on_refresh_models

        logger.debug("ProviderSettingsComponent initialized.")

        # =========================================================================
    # Public API
    # =========================================================================

    def render(self) -> None:
        """
        Render the complete Provider Settings component.

        Rendering order
        ----------------
        1. Initialize session state
        2. Synchronize local state
        3. Render header
        4. Render provider summary
        5. Render provider selector
        6. Render provider configuration
        7. Render connection status
        8. Render actions
        """

        self._initialize_session_state()

        self._sync_state()

        self._render_header()

        st.divider()

        # self._render_provider_summary()

        # Temporary diagnostic import
        from app.ui.components.settings.api_settings import (
            get_provider_metadata,
        )

        metadata = get_provider_metadata(
            self.state.provider
        )



        st.divider()

        self._render_provider_selector()

        st.divider()

        self._render_provider_configuration()

        st.divider()

        self._render_connection_status()

        st.divider()

        self._render_actions()

    # =========================================================================
    # Session State
    # =========================================================================

    def _initialize_session_state(self) -> None:
        """
        Initialize Streamlit session state.

        Streamlit reruns the script after every widget interaction.
        Therefore the ProviderState object is persisted inside
        st.session_state.
        """

        if SESSION_PROVIDER_STATE not in st.session_state:

            st.session_state[SESSION_PROVIDER_STATE] = (
                self.state
            )

            logger.debug(
                "Created provider session state."
            )

    def _sync_state(self) -> None:
        """
        Synchronize component state with Streamlit session state.

        This guarantees that the component always works with the
        latest state object.
        """

        self.state = st.session_state[
            SESSION_PROVIDER_STATE
        ]

    def _update_session_state(self) -> None:
        """
        Persist current state back into Streamlit session storage.
        """

        st.session_state[
            SESSION_PROVIDER_STATE
        ] = self.state

    # =========================================================================
    # Header
    # =========================================================================

    def _render_header(self) -> None:
        """
        Render Provider Settings header.
        """

        render_html("""
            <div style="
                padding:18px;
                border-radius:12px;
                border:1px solid #dddddd;
                background-color:#fafafa;
                margin-bottom:10px;
            ">
                <h2 style="margin-bottom:0;">
                    🤖 Provider Settings
                </h2>

                <p style="margin-top:8px;margin-bottom:0;">
                    Configure local and cloud Large Language Model providers
                    used by the AI Research Assistant.
                </p>
            </div>
            """)

        metadata = PROVIDERS.get(
            self.state.provider
        )

        if metadata is None:
            return

        left, right = st.columns([4, 1])

        with left:

            st.caption(
                f"Current Provider: "
                f"{metadata.icon} {metadata.display_name}"
            )

        with right:

            if metadata.category == ProviderCategory.LOCAL:

                st.success("LOCAL")

            else:

                st.info("CLOUD")

        st.caption(
            "Tip: Develop locally using Ollama and switch to "
            "cloud providers only when needed."
        )

        self._update_session_state()

        # =========================================================================
    # Provider Summary
    # =========================================================================

    def _render_provider_summary(self) -> None:
        """
        Render a dashboard-style summary of the currently selected provider.
        """

        metadata = get_provider_metadata(
            self.state.provider
        )

        if metadata is None:
            st.warning("Provider metadata unavailable.")
            return

        st.subheader("Current Provider")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Provider",
                value=f"{metadata.icon} {metadata.display_name}",
            )

        with col2:
            st.metric(
                label="Category",
                value=metadata.category.value,
            )

        with col3:

            if self.state.enabled:
                status = "Enabled"
            else:
                status = "Disabled"

            st.metric(
                label="Status",
                value=status,
            )

        with col4:

            st.metric(
                label="Connection",
                value=self.state.connection_status.value,
            )

        badges: list[str] = []

        if metadata.supports_streaming:
            badges.append("⚡ Streaming")

        if metadata.supports_tools:
            badges.append("🛠 Tools")

        if metadata.supports_vision:
            badges.append("👁 Vision")

        if metadata.supports_embeddings:
            badges.append("📚 Embeddings")

        if metadata.supports_function_calling:
            badges.append("🔧 Function Calling")

        if badges:
            st.caption(" | ".join(badges))

        with st.expander(
            "Provider Information",
            expanded=False,
        ):

            st.markdown(
                f"**Description**\n\n{metadata.description}"
            )

            info = {
                "Display Name": metadata.display_name,
                "Provider": metadata.provider.value,
                "Category": metadata.category.value,
                "Default Endpoint": (
                    metadata.default_endpoint
                    or "Not Applicable"
                ),
                "Requires API Key": metadata.requires_api_key,
                "Supports Streaming": metadata.supports_streaming,
                "Supports Vision": metadata.supports_vision,
                "Supports Tools": metadata.supports_tools,
                "Supports Embeddings": metadata.supports_embeddings,
                "Supports Function Calling":
                    metadata.supports_function_calling,
            }

            st.json(info)

            if metadata.homepage:

                st.link_button(
                    label="Open Provider Website",
                    url=metadata.homepage,
                    use_container_width=True,
                )

    # =========================================================================
    # Provider Selection
    # =========================================================================

    def _render_provider_selector(self) -> None:
        """
        Render provider selection UI.
        """

        st.subheader("Select Provider")

        providers = get_available_providers()

        try:

            current_index = providers.index(
                self.state.provider
            )

        except ValueError:

            current_index = 0

        selected_provider = st.selectbox(
            label="Available Providers",
            options=providers,
            index=current_index,
            format_func=self._format_provider_name,
            help=(
                "Choose the LLM provider that will be used "
                "for research paper analysis."
            ),
        )

        if selected_provider != self.state.provider:

            logger.info(
                "Provider changed from %s to %s",
                self.state.provider.value,
                selected_provider.value,
            )

            self.state.provider = selected_provider

            self._apply_provider_defaults(
                selected_provider
            )

            self._update_session_state()

            st.rerun()

        # =========================================================================
    # Provider Helper Methods
    # =========================================================================

    def _format_provider_name(
        self,
        provider: ProviderType,
    ) -> str:
        """
        Format provider name for display in selection controls.

        Args:
            provider:
                Provider enumeration.

        Returns:
            User-friendly provider display name.
        """

        metadata = get_provider_metadata(provider)

        if metadata is None:
            return provider.value

        return f"{metadata.icon} {metadata.display_name}"

    def _apply_provider_defaults(
        self,
        provider: ProviderType,
    ) -> None:
        """
        Apply default configuration when the selected provider changes.

        Existing runtime settings such as timeout and retry count are
        preserved while provider-specific values are updated.

        Args:
            provider:
                Newly selected provider.
        """

        metadata = get_provider_metadata(provider)

        if metadata is None:
            logger.warning(
                "No metadata found for provider %s",
                provider.value,
            )
            return

        self.state.provider = provider

        if metadata.default_endpoint:
            self.state.endpoint = metadata.default_endpoint
        else:
            self.state.endpoint = ""

        self.state.api_key = ""

        self.state.selected_model = ""

        self.state.available_models.clear()

        self.state.connection_status = (
            ConnectionStatus.UNKNOWN
        )

        self.state.configured = False

        logger.info(
            "Applied defaults for provider %s",
            provider.value,
        )

    def _reset_provider_state(self) -> None:
        """
        Reset the current provider configuration to its defaults.

        This does not affect callbacks or the selected provider.
        """

        provider = self.state.provider

        timeout = self.state.timeout

        retries = self.state.retries

        enabled = self.state.enabled

        is_default = self.state.is_default

        self._apply_provider_defaults(provider)

        self.state.timeout = timeout

        self.state.retries = retries

        self.state.enabled = enabled

        self.state.is_default = is_default

        self._update_session_state()

        logger.info(
            "Provider state reset."
        )

    def _provider_status_color(self) -> str:
        """
        Return a color corresponding to the current connection status.

        Returns:
            CSS-compatible color string.
        """

        status = self.state.connection_status

        if status == ConnectionStatus.CONNECTED:
            return "green"

        if status == ConnectionStatus.TESTING:
            return "orange"

        if status == ConnectionStatus.DISCONNECTED:
            return "red"

        if status == ConnectionStatus.ERROR:
            return "darkred"

        return "gray"

    def _provider_status_icon(self) -> str:
        """
        Return an icon representing the current connection state.
        """

        mapping = {
            ConnectionStatus.UNKNOWN: "⚪",
            ConnectionStatus.TESTING: "🟡",
            ConnectionStatus.CONNECTED: "🟢",
            ConnectionStatus.DISCONNECTED: "🔴",
            ConnectionStatus.ERROR: "❌",
        }

        return mapping.get(
            self.state.connection_status,
            "⚪",
        )

    def _provider_requires_api_key(self) -> bool:
        """
        Determine whether the selected provider requires an API key.
        """

        metadata = get_provider_metadata(
            self.state.provider
        )

        if metadata is None:
            return False

        return metadata.requires_api_key

    def _provider_is_local(self) -> bool:
        """
        Check whether the selected provider is a local provider.
        """

        metadata = get_provider_metadata(
            self.state.provider
        )

        if metadata is None:
            return False

        return (
            metadata.category
            == ProviderCategory.LOCAL
        )

    def _provider_is_cloud(self) -> bool:
        """
        Check whether the selected provider is a cloud provider.
        """

        return not self._provider_is_local()

    def _mark_configured(self) -> None:
        """
        Mark the provider as configured.
        """

        self.state.configured = True

        self._update_session_state()

    def _mark_unconfigured(self) -> None:
        """
        Mark the provider as not configured.
        """

        self.state.configured = False

        self._update_session_state()


        # =========================================================================
    # Provider Configuration
    # =========================================================================

    def _render_provider_configuration(self) -> None:
        """
        Render the complete provider configuration panel.

        The configuration panel adapts automatically depending on the selected
        provider.

        Sections
        --------
        • Endpoint
        • Authentication
        • Model Selection
        • Runtime Options
        • Advanced Options
        """

        metadata = get_provider_metadata(
            self.state.provider
        )

        if metadata is None:
            st.error(
                "Unable to load provider configuration."
            )
            return

        st.subheader("Provider Configuration")

        self._render_endpoint_configuration(metadata)

        if metadata.requires_api_key:
            self._render_api_key_configuration()

        self._render_model_configuration()

        self._render_runtime_configuration()

        self._render_advanced_options()

    # =========================================================================
    # Endpoint Configuration
    # =========================================================================

    def _render_endpoint_configuration(
        self,
        metadata: ProviderMetadata,
    ) -> None:
        """
        Render endpoint configuration.

        Local providers use localhost endpoints while cloud providers
        generally require HTTPS API endpoints.
        """

        st.markdown("#### 🌐 Endpoint")

        help_text = (
            "Base URL of the provider endpoint."
        )

        self.state.endpoint = st.text_input(
            label="Endpoint URL",
            value=self.state.endpoint,
            help=help_text,
            placeholder=(
                metadata.default_endpoint
                if metadata.default_endpoint
                else "https://api.example.com/v1"
            ),
        )

        if (
            metadata.default_endpoint
            and st.button(
                "Restore Default Endpoint",
                key="restore_provider_endpoint",
                use_container_width=False,
            )
        ):
            self.state.endpoint = (
                metadata.default_endpoint
            )

            self._update_session_state()

            st.rerun()

        if metadata.category == ProviderCategory.LOCAL:

            st.info(
                """
Local Provider

• No internet connection required
• Models execute on your machine
• Lower operating cost
• Better privacy
                """
            )

        else:

            st.info(
                """
Cloud Provider

• Internet connection required
• API credentials required
• Latest commercial models
• Usage charges may apply
                """
            )

        if not self.state.endpoint:

            st.warning(
                "Endpoint URL has not been configured."
            )

        elif self.state.endpoint.startswith("http://"):

            if metadata.category == ProviderCategory.CLOUD:

                st.warning(
                    "Cloud providers should normally use HTTPS."
                )

        elif self.state.endpoint.startswith("https://"):

            st.success(
                "Secure HTTPS endpoint detected."
            )

        self._update_session_state()

        # =========================================================================
    # API Key Configuration
    # =========================================================================

    def _render_api_key_configuration(self) -> None:
        """
        Render API key configuration.

        Cloud providers typically require an authentication key.
        The key is stored only in the ProviderState. Persistent
        storage should be handled by the configuration layer.
        """

        st.markdown("#### 🔐 Authentication")

        show_key = st.checkbox(
            "Show API Key",
            value=False,
            key="provider_show_api_key",
        )

        self.state.api_key = st.text_input(
            label="API Key",
            value=self.state.api_key,
            type="default" if show_key else "password",
            placeholder="Enter provider API key",
            help=(
                "API keys are never displayed in plain text "
                "unless 'Show API Key' is enabled."
            ),
        )

        if self.state.api_key:

            st.success(
                "API key configured."
            )

        else:

            st.warning(
                "API key not configured."
            )

        self._update_session_state()

    # =========================================================================
    # Model Configuration
    # =========================================================================

    def _render_model_configuration(self) -> None:
        """
        Render model selection controls.

        Users may either:
        • Refresh models from the provider
        • Select an available model
        • Enter a model manually
        """

        st.markdown("#### 🧠 Model Configuration")

        refresh_col, info_col = st.columns([1, 3])

        with refresh_col:

            if st.button(
                "🔄 Refresh Models",
                key="provider_refresh_models",
                use_container_width=True,
            ):

                self._refresh_provider_models()

        with info_col:

            if self.state.available_models:

                st.success(
                    f"{len(self.state.available_models)} model(s) available."
                )

            else:

                st.info(
                    "No models loaded."
                )

        # -------------------------------------------------------------
        # Model Selection
        # -------------------------------------------------------------

        model_options = list(self.state.available_models)

        if self.state.selected_model:

            if self.state.selected_model not in model_options:

                model_options.insert(
                    0,
                    self.state.selected_model,
                )

        if model_options:

            try:

                current_index = model_options.index(
                    self.state.selected_model
                )

            except ValueError:

                current_index = 0

            selected = st.selectbox(
                "Available Models",
                options=model_options,
                index=current_index,
                help="Choose one of the available models.",
            )

            self.state.selected_model = selected

        st.markdown("##### Manual Model Entry")

        manual_model = st.text_input(
            label="Model Name",
            value=self.state.selected_model,
            placeholder=(
                "Examples: "
                "qwen3:4b, llama3.1:8b, "
                "gpt-4.1, gemini-2.5-pro"
            ),
            help=(
                "Manual entry overrides the selected model."
            ),
        )

        if manual_model.strip():

            self.state.selected_model = (
                manual_model.strip()
            )

        # -------------------------------------------------------------
        # Provider-specific recommendations
        # -------------------------------------------------------------

        if self.state.provider == ProviderType.OLLAMA:

            st.info(
                """
                Recommended Ollama Models

                • qwen3:4b
                • llama3.1:8b
                • mistral:7b
                • phi4
                • deepseek-r1
                """
            )

        elif self.state.provider == ProviderType.OPENAI:

            st.info(
                """
Recommended OpenAI Models

• gpt-4.1
• gpt-4.1-mini
• gpt-4o
                """
            )

        elif self.state.provider == ProviderType.GEMINI:

            st.info(
                """
Recommended Gemini Models

• gemini-2.5-pro
• gemini-2.5-flash
                """
            )

        elif self.state.provider == ProviderType.DEEPSEEK:

            st.info(
                """
Recommended DeepSeek Models

• deepseek-chat
• deepseek-reasoner
                """
            )

        elif self.state.provider == ProviderType.OPENROUTER:

            st.info(
                """
OpenRouter supports hundreds of models.

Choose any model ID available
through your OpenRouter account.
                """
            )

        elif self.state.provider == ProviderType.CUSTOM:

            st.info(
                """
Specify any model exposed by your
OpenAI-compatible endpoint.
                """
            )

        if not self.state.selected_model.strip():

            st.warning(
                "Please specify a model."
            )

        self._update_session_state()


        # =========================================================================
    # Runtime Configuration
    # =========================================================================

    def _render_runtime_configuration(self) -> None:
        """
        Render runtime execution options.

        These options control how requests are sent to the
        configured LLM provider.
        """

        st.markdown("#### ⚙ Runtime Configuration")

        left_col, right_col = st.columns(2)

        with left_col:

            self.state.timeout = st.number_input(
                label="Request Timeout (seconds)",
                min_value=5,
                max_value=600,
                value=self.state.timeout,
                step=5,
                help="Maximum time to wait for a provider response.",
            )

            self.state.retries = st.number_input(
                label="Retry Attempts",
                min_value=0,
                max_value=10,
                value=self.state.retries,
                step=1,
                help="Number of retry attempts before failing.",
            )

        with right_col:

            self.state.enabled = st.toggle(
                label="Enable Provider",
                value=self.state.enabled,
                help="Enable or disable this provider.",
            )

            self.state.is_default = st.toggle(
                label="Default Provider",
                value=self.state.is_default,
                help="Use this provider by default.",
            )

        st.markdown("##### Generation Parameters")

        temperature = st.slider(
            label="Temperature",
            min_value=0.0,
            max_value=2.0,
            value=float(
                st.session_state.get(
                    "provider_temperature",
                    0.2,
                )
            ),
            step=0.05,
            help="Lower values produce more deterministic responses.",
        )

        st.session_state["provider_temperature"] = (
            temperature
        )

        max_tokens = st.number_input(
            label="Maximum Tokens",
            min_value=128,
            max_value=32768,
            value=int(
                st.session_state.get(
                    "provider_max_tokens",
                    4096,
                )
            ),
            step=128,
        )

        st.session_state["provider_max_tokens"] = (
            max_tokens
        )

        streaming = st.toggle(
            label="Enable Streaming",
            value=bool(
                st.session_state.get(
                    "provider_streaming",
                    True,
                )
            ),
        )

        st.session_state["provider_streaming"] = (
            streaming
        )

        self._update_session_state()

    # =========================================================================
    # Advanced Provider Options
    # =========================================================================

    def _render_advanced_options(self) -> None:
        """
        Render advanced provider configuration.

        These settings are optional and primarily intended for
        development and troubleshooting.
        """

        with st.expander(
            "Advanced Options",
            expanded=False,
        ):

            debug_logging = st.toggle(
                "Enable Debug Logging",
                value=bool(
                    st.session_state.get(
                        "provider_debug_logging",
                        False,
                    )
                ),
            )

            st.session_state[
                "provider_debug_logging"
            ] = debug_logging

            verify_ssl = st.toggle(
                "Verify SSL Certificates",
                value=bool(
                    st.session_state.get(
                        "provider_verify_ssl",
                        True,
                    )
                ),
            )

            st.session_state[
                "provider_verify_ssl"
            ] = verify_ssl

            auto_refresh = st.toggle(
                "Refresh Models Automatically",
                value=bool(
                    st.session_state.get(
                        "provider_auto_refresh",
                        False,
                    )
                ),
            )

            st.session_state[
                "provider_auto_refresh"
            ] = auto_refresh

            keep_alive = st.number_input(
                "Connection Keep-Alive (seconds)",
                min_value=0,
                max_value=3600,
                value=int(
                    st.session_state.get(
                        "provider_keep_alive",
                        300,
                    )
                ),
                step=30,
            )

            st.session_state[
                "provider_keep_alive"
            ] = keep_alive

            st.markdown("---")

            st.caption(
                "These settings are optional and are mainly "
                "intended for advanced users."
            )

            validation, message = (
                validate_provider_configuration(
                    self.state
                )
            )

            if validation:

                self._mark_configured()

                st.success(message)

            else:

                self._mark_unconfigured()

                st.warning(message)

        self._update_session_state()


        # =========================================================================
    # Validation
    # =========================================================================

    def _validate_provider_state(
        self,
    ) -> tuple[bool, str]:
        """
        Validate the current provider configuration.

        Returns
        -------
        tuple[bool, str]
            Validation result and message.
        """

        metadata = get_provider_metadata(
            self.state.provider
        )

        if metadata is None:

            return (
                False,
                "Unsupported provider selected.",
            )

        endpoint = self.state.endpoint.strip()

        if not endpoint:

            return (
                False,
                "Provider endpoint is required.",
            )

        if (
            metadata.category
            == ProviderCategory.CLOUD
            and not endpoint.startswith("https://")
        ):

            return (
                False,
                "Cloud providers should use an HTTPS endpoint.",
            )

        if (
            metadata.category
            == ProviderCategory.LOCAL
            and not (
                endpoint.startswith("http://")
                or endpoint.startswith("https://")
            )
        ):

            return (
                False,
                "Invalid local provider endpoint.",
            )

        if (
            metadata.requires_api_key
            and not self.state.api_key.strip()
        ):

            return (
                False,
                "API key is required.",
            )

        if not self.state.selected_model.strip():

            return (
                False,
                "Please select or enter a model.",
            )

        if self.state.timeout <= 0:

            return (
                False,
                "Timeout must be greater than zero.",
            )

        if self.state.retries < 0:

            return (
                False,
                "Retry count cannot be negative.",
            )

        return (
            True,
            "Provider configuration is valid.",
        )

    # =========================================================================
    # Connection Status
    # =========================================================================

    def _render_connection_status(self) -> None:
        """
        Render the current provider connection status.
        """

        st.subheader("Connection Status")

        status = self.state.connection_status

        status_map = {

            ConnectionStatus.UNKNOWN: (
                "⚪",
                "Not Tested",
                st.info,
            ),

            ConnectionStatus.TESTING: (
                "🟡",
                "Testing...",
                st.warning,
            ),

            ConnectionStatus.CONNECTED: (
                "🟢",
                "Connected",
                st.success,
            ),

            ConnectionStatus.DISCONNECTED: (
                "🔴",
                "Disconnected",
                st.error,
            ),

            ConnectionStatus.ERROR: (
                "❌",
                "Connection Error",
                st.error,
            ),
        }

        icon, label, renderer = status_map.get(
            status,
            (
                "⚪",
                "Unknown",
                st.info,
            ),
        )

        renderer(
            f"{icon} {label}"
        )

        left, right = st.columns(2)

        with left:

            st.metric(
                "Selected Provider",
                self.state.provider.value,
            )

            st.metric(
                "Model",
                self.state.selected_model
                if self.state.selected_model
                else "Not Selected",
            )

        with right:

            st.metric(
                "Endpoint",
                (
                    self.state.endpoint
                    if self.state.endpoint
                    else "-"
                ),
            )

            st.metric(
                "Configured",
                (
                    "Yes"
                    if self.state.configured
                    else "No"
                ),
            )

        with st.expander(
            "Validation Details",
            expanded=False,
        ):

            valid, message = (
                self._validate_provider_state()
            )

            if valid:

                st.success(message)

            else:

                st.error(message)

            st.json(
                {
                    "provider":
                        self.state.provider.value,
                    "endpoint":
                        self.state.endpoint,
                    "model":
                        self.state.selected_model,
                    "configured":
                        self.state.configured,
                    "enabled":
                        self.state.enabled,
                    "default":
                        self.state.is_default,
                    "status":
                        self.state.connection_status.value,
                }
            )

        self._update_session_state()



        # =========================================================================
    # Connection Testing
    # =========================================================================

    def _test_provider_connection(self) -> None:
        """
        Test connectivity to the currently selected provider.

        The actual network communication is delegated to the callback
        supplied during component construction. This keeps the UI layer
        independent from provider implementations.

        Workflow
        --------
        1. Validate configuration
        2. Update UI status
        3. Execute callback
        4. Update connection state
        5. Display result
        """

        valid, message = self._validate_provider_state()

        if not valid:

            self.state.connection_status = (
                ConnectionStatus.ERROR
            )

            self._update_session_state()

            st.error(message)

            return

        logger.info(
            "Testing provider connection: %s",
            self.state.provider.value,
        )

        self.state.connection_status = (
            ConnectionStatus.TESTING
        )

        self._update_session_state()

        progress = st.progress(0)

        status_placeholder = st.empty()

        try:

            status_placeholder.info(
                "Testing provider connection..."
            )

            progress.progress(20)

            if self._on_test_connection is None:

                logger.warning(
                    "No connection callback configured."
                )

                progress.progress(100)

                self.state.connection_status = (
                    ConnectionStatus.UNKNOWN
                )

                self._update_session_state()

                status_placeholder.warning(
                    "Connection test callback is not configured."
                )

                return

            progress.progress(50)

            connected = bool(
                self._on_test_connection(
                    self.state
                )
            )

            progress.progress(90)

            if connected:

                self.state.connection_status = (
                    ConnectionStatus.CONNECTED
                )

                self.state.configured = True

                logger.info(
                    "Provider connection successful."
                )

                status_placeholder.success(
                    "Successfully connected to provider."
                )

            else:

                self.state.connection_status = (
                    ConnectionStatus.DISCONNECTED
                )

                self.state.configured = False

                logger.warning(
                    "Provider connection failed."
                )

                status_placeholder.error(
                    "Unable to connect to provider."
                )

            progress.progress(100)

        except Exception as exc:

            logger.exception(
                "Provider connection test failed."
            )

            self.state.connection_status = (
                ConnectionStatus.ERROR
            )

            self.state.configured = False

            status_placeholder.error(
                f"Connection failed: {exc}"
            )

        finally:

            self._update_session_state()

        # =========================================================================
    # Model Refresh
    # =========================================================================

    def _refresh_provider_models(self) -> None:
        """
        Refresh available models from the selected provider.

        The actual communication with the provider is delegated to the
        callback supplied when the component is created.
        """

        logger.info(
            "Refreshing models for provider '%s'.",
            self.state.provider.value,
        )

        valid, message = self._validate_provider_state()

        if not valid:

            self._show_provider_warning(message)

            return

        if self._on_refresh_models is None:

            logger.warning(
                "No refresh callback configured."
            )

            self._show_provider_warning(
                "Model refresh callback is not configured."
            )

            return

        progress = st.progress(0)

        status_placeholder = st.empty()

        try:

            self._set_connection_status(
                ConnectionStatus.TESTING
            )

            status_placeholder.info(
                "Retrieving available models..."
            )

            progress.progress(25)

            models = self._on_refresh_models(
                self.state
            )

            progress.progress(75)

            if models is None:

                models = []

            models = sorted(
                list(
                    {
                        model.strip()
                        for model in models
                        if model and model.strip()
                    }
                )
            )

            self.state.available_models = models

            if (
                models
                and not self.state.selected_model
            ):
                self.state.selected_model = models[0]

            self._set_connection_status(
                ConnectionStatus.CONNECTED
            )

            progress.progress(100)

            status_placeholder.success(
                f"Loaded {len(models)} model(s)."
            )

            logger.info(
                "%d model(s) loaded.",
                len(models),
            )

        except Exception as exc:

            logger.exception(
                "Unable to refresh provider models."
            )

            self._set_connection_status(
                ConnectionStatus.ERROR
            )

            status_placeholder.error(
                f"Model refresh failed: {exc}"
            )

        finally:

            self._update_session_state()

    # =========================================================================
    # Status Helper Methods
    # =========================================================================

    def _set_connection_status(
        self,
        status: ConnectionStatus,
    ) -> None:
        """
        Update provider connection status.

        Args
        ----
        status:
            New connection status.
        """

        self.state.connection_status = status

        self._update_session_state()

        logger.debug(
            "Connection status changed to '%s'.",
            status.value,
        )

    def _show_provider_success(
        self,
        message: str,
    ) -> None:
        """
        Display a success message.
        """

        logger.info(message)

        st.success(message)

    def _show_provider_warning(
        self,
        message: str,
    ) -> None:
        """
        Display a warning message.
        """

        logger.warning(message)

        st.warning(message)

    def _show_provider_error(
        self,
        message: str,
    ) -> None:
        """
        Display an error message.
        """

        logger.error(message)

        st.error(message)

    def _clear_loaded_models(self) -> None:
        """
        Clear all cached provider models.
        """

        self.state.available_models.clear()

        self.state.selected_model = ""

        self._update_session_state()

        logger.debug(
            "Cached provider models cleared."
        )

    def _mark_connection_failed(
        self,
        reason: str,
    ) -> None:
        """
        Mark the provider connection as failed.

        Args
        ----
        reason:
            Human-readable failure reason.
        """

        self.state.connection_status = (
            ConnectionStatus.ERROR
        )

        self.state.configured = False

        self._update_session_state()

        logger.error(
            "Provider connection failed: %s",
            reason,
        )

        st.error(reason)

    def _mark_connection_success(self) -> None:
        """
        Mark the provider as successfully connected.
        """

        self.state.connection_status = (
            ConnectionStatus.CONNECTED
        )

        self.state.configured = True

        self._update_session_state()

        logger.info(
            "Provider successfully connected."
        )

    def _provider_summary(self) -> dict[str, Any]:
        """
        Return a lightweight provider summary.

        Returns
        -------
        dict[str, Any]
            Provider information useful for diagnostics.
        """

        return {
            "provider": self.state.provider.value,
            "endpoint": self.state.endpoint,
            "model": self.state.selected_model,
            "enabled": self.state.enabled,
            "configured": self.state.configured,
            "status": self.state.connection_status.value,
            "available_models": len(
                self.state.available_models
            ),
        }

        # =========================================================================
    # Action Panel
    # =========================================================================

    def _render_actions(self) -> None:
        """
        Render provider action buttons.

        The action panel contains all user operations related to
        provider management.
        """

        st.subheader("Provider Actions")

        test_col, refresh_col, save_col = st.columns(3)

        # ---------------------------------------------------------------------
        # Test Connection
        # ---------------------------------------------------------------------

        with test_col:

            if st.button(
                "🔌 Test Connection",
                key="provider_test_connection",
                use_container_width=True,
                type="secondary",
            ):

                self._test_provider_connection()

        # ---------------------------------------------------------------------
        # Refresh Models
        # ---------------------------------------------------------------------

        with refresh_col:

            if st.button(
                "🔄 Refresh Models",
                key="provider_refresh_models_action",
                use_container_width=True,
                type="secondary",
            ):

                self._refresh_provider_models()

        # ---------------------------------------------------------------------
        # Save Settings
        # ---------------------------------------------------------------------

        with save_col:

            if st.button(
                "💾 Save Settings",
                key="provider_save_settings",
                use_container_width=True,
                type="primary",
            ):

                self._save_provider_settings()

        st.divider()

        reset_col, preview_col = st.columns(2)

        # ---------------------------------------------------------------------
        # Reset Provider
        # ---------------------------------------------------------------------

        with reset_col:

            if st.button(
                "♻ Reset Configuration",
                key="provider_reset_configuration",
                use_container_width=True,
            ):

                self._reset_provider_settings()

        # ---------------------------------------------------------------------
        # Configuration Preview
        # ---------------------------------------------------------------------

        with preview_col:

            if st.button(
                "📋 Configuration Preview",
                key="provider_configuration_preview",
                use_container_width=True,
            ):

                self._show_configuration_preview()

        st.divider()

        # ---------------------------------------------------------------------
        # Current Status Summary
        # ---------------------------------------------------------------------

        status_icon = self._provider_status_icon()

        provider_name = self.state.provider.value

        model_name = (
            self.state.selected_model
            if self.state.selected_model
            else "Not Selected"
        )

        st.caption(
            f"{status_icon} "
            f"Provider: **{provider_name}** "
            f"| Model: **{model_name}**"
        )

        if self.state.enabled:

            st.success(
                "Provider is enabled and ready."
            )

        else:

            st.warning(
                "Provider is currently disabled."
            )

        self._update_session_state()

        # =========================================================================
    # Save Provider Settings
    # =========================================================================

    def _save_provider_settings(self) -> None:
        """
        Save the current provider configuration.

        Validation is performed before invoking the save callback.
        Persistence is delegated to the application configuration layer.
        """

        valid, message = self._validate_provider_state()

        if not valid:

            self._show_provider_warning(message)

            return

        logger.info(
            "Saving provider configuration for '%s'.",
            self.state.provider.value,
        )

        try:

            self.state.configured = True

            self._update_session_state()

            if self._on_save is not None:

                self._on_save(self.state)

                logger.info(
                    "Provider configuration successfully saved."
                )

                self._show_provider_success(
                    "Provider settings saved successfully."
                )

            else:

                logger.warning(
                    "No save callback has been configured."
                )

                self._show_provider_warning(
                    "Settings were validated, but no save handler "
                    "is configured."
                )

        except Exception as exc:

            logger.exception(
                "Unable to save provider configuration."
            )

            self.state.configured = False

            self._update_session_state()

            self._show_provider_error(
                f"Failed to save settings: {exc}"
            )

    # =========================================================================
    # Reset Provider Settings
    # =========================================================================

    def _reset_provider_settings(self) -> None:
        """
        Reset the current provider configuration.

        The selected provider remains unchanged while all provider-specific
        configuration values are restored to their defaults.
        """

        logger.info(
            "Resetting provider configuration."
        )

        provider = self.state.provider

        metadata = get_provider_metadata(provider)

        try:

            endpoint = (
                metadata.default_endpoint
                if (
                    metadata
                    and metadata.default_endpoint
                )
                else ""
            )

            self.state.endpoint = endpoint

            self.state.api_key = ""

            self.state.selected_model = ""

            self.state.available_models.clear()

            self.state.connection_status = (
                ConnectionStatus.UNKNOWN
            )

            self.state.configured = False

            self.state.timeout = DEFAULT_TIMEOUT

            self.state.retries = DEFAULT_RETRIES

            self.state.enabled = True

            self.state.is_default = (
                provider == ProviderType.OLLAMA
            )

            # Reset advanced runtime options

            st.session_state[
                "provider_temperature"
            ] = 0.20

            st.session_state[
                "provider_max_tokens"
            ] = 4096

            st.session_state[
                "provider_streaming"
            ] = True

            st.session_state[
                "provider_debug_logging"
            ] = False

            st.session_state[
                "provider_verify_ssl"
            ] = True

            st.session_state[
                "provider_auto_refresh"
            ] = False

            st.session_state[
                "provider_keep_alive"
            ] = 300

            self._update_session_state()

            logger.info(
                "Provider configuration reset completed."
            )

            self._show_provider_success(
                "Provider configuration has been reset."
            )

            st.rerun()

        except Exception as exc:

            logger.exception(
                "Provider reset failed."
            )

            self._show_provider_error(
                f"Unable to reset provider: {exc}"
            )

        # =========================================================================
    # Configuration Preview
    # =========================================================================

    def _show_configuration_preview(self) -> None:
        """
        Display a safe preview of the current provider configuration.

        Sensitive information such as API keys is masked before
        being displayed.
        """

        st.subheader("Configuration Preview")

        configuration = self._serialize_state(
            mask_secrets=True
        )

        st.json(configuration)

    # =========================================================================
    # Serialization
    # =========================================================================

    def _serialize_state(
        self,
        *,
        mask_secrets: bool = False,
    ) -> dict[str, Any]:
        """
        Serialize the current ProviderState into a dictionary.

        Parameters
        ----------
        mask_secrets:
            If True, secret values such as API keys are masked.

        Returns
        -------
        dict[str, Any]
            Serializable provider configuration.
        """

        api_key = self.state.api_key

        if mask_secrets:

            api_key = mask_secret(api_key)

        configuration: dict[str, Any] = {

            # ---------------------------------------------------------
            # Provider
            # ---------------------------------------------------------

            "provider":
                self.state.provider.value,

            "enabled":
                self.state.enabled,

            "default":
                self.state.is_default,

            "configured":
                self.state.configured,

            # ---------------------------------------------------------
            # Endpoint
            # ---------------------------------------------------------

            "endpoint":
                self.state.endpoint,

            # ---------------------------------------------------------
            # Authentication
            # ---------------------------------------------------------

            "api_key":
                api_key,

            # ---------------------------------------------------------
            # Model
            # ---------------------------------------------------------

            "selected_model":
                self.state.selected_model,

            "available_models":
                list(
                    self.state.available_models
                ),

            # ---------------------------------------------------------
            # Runtime
            # ---------------------------------------------------------

            "timeout":
                self.state.timeout,

            "retries":
                self.state.retries,

            # ---------------------------------------------------------
            # Generation Parameters
            # ---------------------------------------------------------

            "temperature":
                st.session_state.get(
                    "provider_temperature",
                    0.20,
                ),

            "max_tokens":
                st.session_state.get(
                    "provider_max_tokens",
                    4096,
                ),

            "streaming":
                st.session_state.get(
                    "provider_streaming",
                    True,
                ),

            # ---------------------------------------------------------
            # Advanced
            # ---------------------------------------------------------

            "verify_ssl":
                st.session_state.get(
                    "provider_verify_ssl",
                    True,
                ),

            "debug_logging":
                st.session_state.get(
                    "provider_debug_logging",
                    False,
                ),

            "auto_refresh":
                st.session_state.get(
                    "provider_auto_refresh",
                    False,
                ),

            "keep_alive":
                st.session_state.get(
                    "provider_keep_alive",
                    300,
                ),

            # ---------------------------------------------------------
            # Status
            # ---------------------------------------------------------

            "connection_status":
                self.state.connection_status.value,
        }

        return configuration

    def get_configuration(
        self,
    ) -> dict[str, Any]:
        """
        Return the current provider configuration.

        This public method is intended for the Settings Manager,
        export routines, and external integrations.
        """

        return self._serialize_state(
            mask_secrets=False
        )

    def get_safe_configuration(
        self,
    ) -> dict[str, Any]:
        """
        Return a configuration dictionary with secrets masked.

        Useful for diagnostics, logging, and configuration previews.
        """

        return self._serialize_state(
            mask_secrets=True
        )

        # =========================================================================
    # Configuration Loading
    # =========================================================================

    def load_configuration(
        self,
        configuration: dict[str, Any] | None,
    ) -> None:
        """
        Load provider configuration into the component.

        Parameters
        ----------
        configuration:
            Dictionary produced by the Settings Manager,
            provider_config.py, or an exported configuration file.
        """

        if configuration is None:
            logger.debug(
                "No provider configuration supplied."
            )
            return

        if not isinstance(configuration, dict):
            logger.warning(
                "Invalid provider configuration type: %s",
                type(configuration).__name__,
            )
            return

        logger.info(
            "Loading provider configuration."
        )

        try:

            # ---------------------------------------------------------
            # Provider
            # ---------------------------------------------------------

            provider_name = configuration.get(
                "provider",
                ProviderType.OLLAMA.value,
            )

            try:

                self.state.provider = ProviderType(
                    provider_name
                )

            except ValueError:

                logger.warning(
                    "Unknown provider '%s'. Falling back to Ollama.",
                    provider_name,
                )

                self.state.provider = (
                    ProviderType.OLLAMA
                )

            # ---------------------------------------------------------
            # Endpoint
            # ---------------------------------------------------------

            self.state.endpoint = configuration.get(
                "endpoint",
                self.state.endpoint,
            )

            # ---------------------------------------------------------
            # Authentication
            # ---------------------------------------------------------

            self.state.api_key = configuration.get(
                "api_key",
                self.state.api_key,
            )

            # ---------------------------------------------------------
            # Model
            # ---------------------------------------------------------

            self.state.selected_model = configuration.get(
                "selected_model",
                self.state.selected_model,
            )

            self.state.available_models = list(
                configuration.get(
                    "available_models",
                    self.state.available_models,
                )
            )

            # ---------------------------------------------------------
            # Runtime
            # ---------------------------------------------------------

            self.state.timeout = int(
                configuration.get(
                    "timeout",
                    self.state.timeout,
                )
            )

            self.state.retries = int(
                configuration.get(
                    "retries",
                    self.state.retries,
                )
            )

            self.state.enabled = bool(
                configuration.get(
                    "enabled",
                    self.state.enabled,
                )
            )

            self.state.is_default = bool(
                configuration.get(
                    "default",
                    self.state.is_default,
                )
            )

            self.state.configured = bool(
                configuration.get(
                    "configured",
                    self.state.configured,
                )
            )

            # ---------------------------------------------------------
            # Connection Status
            # ---------------------------------------------------------

            status_name = configuration.get(
                "connection_status",
                ConnectionStatus.UNKNOWN.value,
            )

            try:

                self.state.connection_status = (
                    ConnectionStatus(
                        status_name
                    )
                )

            except ValueError:

                self.state.connection_status = (
                    ConnectionStatus.UNKNOWN
                )

            # ---------------------------------------------------------
            # Generation Parameters
            # ---------------------------------------------------------

            st.session_state[
                "provider_temperature"
            ] = float(
                configuration.get(
                    "temperature",
                    st.session_state.get(
                        "provider_temperature",
                        0.20,
                    ),
                )
            )

            st.session_state[
                "provider_max_tokens"
            ] = int(
                configuration.get(
                    "max_tokens",
                    st.session_state.get(
                        "provider_max_tokens",
                        4096,
                    ),
                )
            )

            st.session_state[
                "provider_streaming"
            ] = bool(
                configuration.get(
                    "streaming",
                    st.session_state.get(
                        "provider_streaming",
                        True,
                    ),
                )
            )

            # ---------------------------------------------------------
            # Advanced Options
            # ---------------------------------------------------------

            st.session_state[
                "provider_verify_ssl"
            ] = bool(
                configuration.get(
                    "verify_ssl",
                    st.session_state.get(
                        "provider_verify_ssl",
                        True,
                    ),
                )
            )

            st.session_state[
                "provider_debug_logging"
            ] = bool(
                configuration.get(
                    "debug_logging",
                    st.session_state.get(
                        "provider_debug_logging",
                        False,
                    ),
                )
            )

            st.session_state[
                "provider_auto_refresh"
            ] = bool(
                configuration.get(
                    "auto_refresh",
                    st.session_state.get(
                        "provider_auto_refresh",
                        False,
                    ),
                )
            )

            st.session_state[
                "provider_keep_alive"
            ] = int(
                configuration.get(
                    "keep_alive",
                    st.session_state.get(
                        "provider_keep_alive",
                        300,
                    ),
                )
            )

            self._update_session_state()

            valid, message = (
                self._validate_provider_state()
            )

            if valid:

                logger.info(
                    "Provider configuration loaded successfully."
                )

            else:

                logger.warning(
                    "Loaded configuration requires attention: %s",
                    message,
                )

        except Exception:

            logger.exception(
                "Failed to load provider configuration."
            )

            raise

    # =========================================================================
    # Configuration Validation Helper
    # =========================================================================

    def validate_loaded_configuration(
        self,
    ) -> tuple[bool, list[str]]:
        """
        Validate the currently loaded configuration.

        Returns
        -------
        tuple[bool, list[str]]
            Validation status and list of detected issues.
        """

        issues: list[str] = []

        valid, message = (
            self._validate_provider_state()
        )

        if not valid:
            issues.append(message)

        if self.state.timeout < 5:
            issues.append(
                "Timeout is unusually low."
            )

        if self.state.retries > 5:
            issues.append(
                "Retry count is unusually high."
            )

        if (
            self.state.available_models
            and self.state.selected_model
            not in self.state.available_models
        ):
            issues.append(
                "Selected model is not present in the available model list."
            )

        return (
            len(issues) == 0,
            issues,
        )

        # =========================================================================
    # Configuration Manager Integration
    # =========================================================================

    def sync_with_configuration_manager(
        self,
        configuration_manager: Any,
    ) -> bool:
        """
        Synchronize this component from an external configuration manager.

        The configuration manager may expose one of several common APIs.

        Supported APIs
        --------------
        • get_provider_configuration()
        • get_provider_config()
        • load_provider_configuration()
        • provider_configuration attribute
        • provider_config attribute

        Parameters
        ----------
        configuration_manager:
            Settings/configuration manager instance.

        Returns
        -------
        bool
            True if synchronization succeeded.
        """

        if configuration_manager is None:

            logger.warning(
                "Configuration manager is None."
            )

            return False

        logger.info(
            "Synchronizing provider settings from configuration manager."
        )

        try:

            configuration: dict[str, Any] | None = None

            if hasattr(
                configuration_manager,
                "get_provider_configuration",
            ):

                configuration = (
                    configuration_manager
                    .get_provider_configuration()
                )

            elif hasattr(
                configuration_manager,
                "get_provider_config",
            ):

                configuration = (
                    configuration_manager
                    .get_provider_config()
                )

            elif hasattr(
                configuration_manager,
                "load_provider_configuration",
            ):

                configuration = (
                    configuration_manager
                    .load_provider_configuration()
                )

            elif hasattr(
                configuration_manager,
                "provider_configuration",
            ):

                configuration = getattr(
                    configuration_manager,
                    "provider_configuration",
                )

            elif hasattr(
                configuration_manager,
                "provider_config",
            ):

                configuration = getattr(
                    configuration_manager,
                    "provider_config",
                )

            if configuration is None:

                logger.warning(
                    "No provider configuration available."
                )

                return False

            self.load_configuration(
                configuration
            )

            logger.info(
                "Provider configuration synchronized."
            )

            return True

        except Exception:

            logger.exception(
                "Unable to synchronize provider configuration."
            )

            return False

    # =========================================================================
    # Save To Configuration Manager
    # =========================================================================

    def save_to_configuration_manager(
        self,
        configuration_manager: Any,
    ) -> bool:
        """
        Save the current provider configuration to an external
        configuration manager.

        Supported APIs
        --------------
        • save_provider_configuration()
        • save_provider_config()
        • update_provider_configuration()
        • provider_configuration attribute
        • provider_config attribute

        Parameters
        ----------
        configuration_manager:
            Target configuration manager.

        Returns
        -------
        bool
            True if save completed successfully.
        """

        if configuration_manager is None:

            logger.warning(
                "Configuration manager is None."
            )

            return False

        valid, message = (
            self._validate_provider_state()
        )

        if not valid:

            logger.warning(message)

            return False

        configuration = self.get_configuration()

        logger.info(
            "Saving provider configuration to configuration manager."
        )

        try:

            if hasattr(
                configuration_manager,
                "save_provider_configuration",
            ):

                configuration_manager.save_provider_configuration(
                    configuration
                )

            elif hasattr(
                configuration_manager,
                "save_provider_config",
            ):

                configuration_manager.save_provider_config(
                    configuration
                )

            elif hasattr(
                configuration_manager,
                "update_provider_configuration",
            ):

                configuration_manager.update_provider_configuration(
                    configuration
                )

            elif hasattr(
                configuration_manager,
                "provider_configuration",
            ):

                configuration_manager.provider_configuration = (
                    configuration
                )

            elif hasattr(
                configuration_manager,
                "provider_config",
            ):

                configuration_manager.provider_config = (
                    configuration
                )

            else:

                logger.warning(
                    "Configuration manager does not expose a supported save API."
                )

                return False

            logger.info(
                "Provider configuration saved successfully."
            )

            return True

        except Exception:

            logger.exception(
                "Unable to save provider configuration."
            )

            return False

    # =========================================================================
# Configuration Manager Integration
# =========================================================================

def sync_with_configuration_manager(
    self,
    configuration_manager: Any,
) -> bool:
    """
    Synchronize provider settings from an external configuration manager.

    Supported APIs
    --------------
    - get_provider_configuration()
    - get_provider_config()
    - load_provider_configuration()
    - provider_configuration attribute
    - provider_config attribute

    Parameters
    ----------
    configuration_manager:
        External configuration manager instance.

    Returns
    -------
    bool
        True when synchronization succeeds.
    """

    if configuration_manager is None:

        logger.warning(
            "Configuration manager is None."
        )

        return False

    logger.info(
        "Synchronizing provider configuration."
    )

    try:

        configuration = None

        getter_methods = (
            "get_provider_configuration",
            "get_provider_config",
            "load_provider_configuration",
        )

        for method_name in getter_methods:

            method = getattr(
                configuration_manager,
                method_name,
                None,
            )

            if callable(method):

                configuration = method()

                break

        if configuration is None:

            for attribute_name in (
                "provider_configuration",
                "provider_config",
            ):

                if hasattr(
                    configuration_manager,
                    attribute_name,
                ):

                    configuration = getattr(
                        configuration_manager,
                        attribute_name,
                    )

                    break

        if configuration is None:

            logger.warning(
                "No provider configuration found."
            )

            return False

        if not isinstance(
            configuration,
            dict,
        ):

            configuration = vars(
                configuration
            )

        self.load_configuration(
            configuration
        )

        logger.info(
            "Provider configuration synchronized successfully."
        )

        return True

    except Exception:

        logger.exception(
            "Provider synchronization failed."
        )

        return False


# =========================================================================
# Save To Configuration Manager
# =========================================================================

def save_to_configuration_manager(
    self,
    configuration_manager: Any,
) -> bool:
    """
    Save provider settings into an external configuration manager.

    Supported APIs
    --------------
    - save_provider_configuration()
    - save_provider_config()
    - update_provider_configuration()
    - provider_configuration attribute
    - provider_config attribute

    Parameters
    ----------
    configuration_manager:
        External configuration manager instance.

    Returns
    -------
    bool
        True when save succeeds.
    """

    if configuration_manager is None:

        logger.warning(
            "Configuration manager is None."
        )

        return False


    valid, message = (
        self._validate_provider_state()
    )

    if not valid:

        logger.warning(
            message
        )

        return False


    configuration = (
        self.get_configuration()
    )


    logger.info(
        "Saving provider configuration."
    )


    try:

        save_methods = (
            "save_provider_configuration",
            "save_provider_config",
            "update_provider_configuration",
        )

        for method_name in save_methods:

            method = getattr(
                configuration_manager,
                method_name,
                None,
            )

            if callable(method):

                method(
                    configuration
                )

                logger.info(
                    "Provider configuration saved using %s.",
                    method_name,
                )

                return True


        if hasattr(
            configuration_manager,
            "provider_configuration",
        ):

            configuration_manager.provider_configuration = (
                configuration
            )

            return True


        if hasattr(
            configuration_manager,
            "provider_config",
        ):

            configuration_manager.provider_config = (
                configuration
            )

            return True


        logger.warning(
            "No supported configuration save API found."
        )

        return False


    except Exception:

        logger.exception(
            "Unable to save provider configuration."
        )

        return False

    # =========================================================================
# Environment Variable Integration
# =========================================================================

def load_from_environment(
    self,
    prefix: str = "AI_PROVIDER_",
) -> bool:
    """
    Load provider configuration from environment variables.

    Supported variables
    -------------------
    AI_PROVIDER_NAME
    AI_PROVIDER_MODEL
    AI_PROVIDER_BASE_URL
    AI_PROVIDER_API_KEY
    AI_PROVIDER_TIMEOUT
    AI_PROVIDER_TEMPERATURE
    AI_PROVIDER_MAX_TOKENS
    AI_PROVIDER_ENABLED

    Parameters
    ----------
    prefix:
        Environment variable prefix.

    Returns
    -------
    bool
        True if environment loading succeeds.
    """

    import os

    logger.info(
        "Loading provider configuration from environment."
    )

    try:

        environment_mapping = {
            "name": (
                f"{prefix}NAME"
            ),

            "model": (
                f"{prefix}MODEL"
            ),

            "base_url": (
                f"{prefix}BASE_URL"
            ),

            "api_key": (
                f"{prefix}API_KEY"
            ),

            "timeout": (
                f"{prefix}TIMEOUT"
            ),

            "temperature": (
                f"{prefix}TEMPERATURE"
            ),

            "max_tokens": (
                f"{prefix}MAX_TOKENS"
            ),

            "enabled": (
                f"{prefix}ENABLED"
            ),
        }


        configuration = {}


        for key, environment_key in (
            environment_mapping.items()
        ):

            value = os.getenv(
                environment_key
            )

            if value is not None:

                configuration[key] = value



        if not configuration:

            logger.info(
                "No provider environment variables found."
            )

            return False



        self.load_configuration(
            configuration
        )


        logger.info(
            "Provider configuration loaded from environment."
        )

        return True



    except Exception:

        logger.exception(
            "Unable to load provider configuration from environment."
        )

        return False



# =========================================================================
# Export Environment Configuration
# =========================================================================

def export_to_environment_dict(
    self,
    prefix: str = "AI_PROVIDER_",
) -> dict[str, str]:
    """
    Export provider configuration into environment-style mapping.

    Useful for:
    - Docker environments
    - CI/CD pipelines
    - Deployment scripts
    - Testing

    Parameters
    ----------
    prefix:
        Environment variable prefix.

    Returns
    -------
    dict[str, str]
        Environment variable dictionary.
    """

    configuration = (
        self.get_configuration()
    )


    environment = {}


    mapping = {
        "name": "NAME",
        "model": "MODEL",
        "base_url": "BASE_URL",
        "api_key": "API_KEY",
        "timeout": "TIMEOUT",
        "temperature": "TEMPERATURE",
        "max_tokens": "MAX_TOKENS",
        "enabled": "ENABLED",
    }


    for key, env_name in (
        mapping.items()
    ):

        value = configuration.get(
            key
        )


        if value is not None:

            environment[
                f"{prefix}{env_name}"
            ] = str(value)



    return environment


    # =========================================================================
# Provider Configuration Validation
# =========================================================================

def validate_configuration(
    self,
) -> tuple[bool, str]:
    """
    Validate complete provider configuration.

    Returns
    -------
    tuple[bool, str]
        Validation status and message.
    """

    try:

        configuration = (
            self.get_configuration()
        )


        required_fields = (
            "name",
            "model",
        )


        missing_fields = [
            field
            for field in required_fields
            if not configuration.get(field)
        ]


        if missing_fields:

            return (
                False,
                (
                    "Missing required provider fields: "
                    f"{', '.join(missing_fields)}"
                ),
            )


        if not isinstance(
            configuration.get("enabled"),
            bool,
        ):

            return (
                False,
                "Provider enabled flag must be boolean.",
            )


        timeout = configuration.get(
            "timeout"
        )


        if timeout is not None:

            try:

                timeout_value = float(
                    timeout
                )

                if timeout_value <= 0:

                    return (
                        False,
                        "Timeout must be greater than zero.",
                    )

            except ValueError:

                return (
                    False,
                    "Timeout must be numeric.",
                )


        temperature = configuration.get(
            "temperature"
        )


        if temperature is not None:

            try:

                temperature_value = float(
                    temperature
                )

                if not (
                    0.0
                    <= temperature_value
                    <= 2.0
                ):

                    return (
                        False,
                        (
                            "Temperature must be "
                            "between 0 and 2."
                        ),
                    )


            except ValueError:

                return (
                    False,
                    "Temperature must be numeric.",
                )


        return (
            True,
            "Provider configuration is valid.",
        )


    except Exception as exc:

        logger.exception(
            "Provider validation failed."
        )

        return (
            False,
            str(exc),
        )



# =========================================================================
# Configuration Serialization
# =========================================================================

def to_dict(
    self,
) -> dict[str, Any]:
    """
    Return provider configuration as dictionary.

    Returns
    -------
    dict[str, Any]
        Provider configuration.
    """

    return (
        self.get_configuration()
        .copy()
    )



def from_dict(
    self,
    configuration: dict[str, Any],
) -> None:
    """
    Load provider configuration from dictionary.

    Parameters
    ----------
    configuration:
        Provider configuration mapping.
    """

    if not isinstance(
        configuration,
        dict,
    ):

        raise TypeError(
            "Provider configuration must be a dictionary."
        )


    self.load_configuration(
        configuration
    )



# =========================================================================
# Configuration Reset
# =========================================================================

def reset_to_defaults(
    self,
) -> None:
    """
    Reset provider configuration to default values.
    """

    logger.info(
        "Resetting provider configuration to defaults."
    )


    self.__init__()



# =========================================================================
# Representation Helpers
# =========================================================================

def __repr__(
    self,
) -> str:
    """
    Developer friendly representation.
    """

    return (
        f"{self.__class__.__name__}("
        f"name={self.name!r}, "
        f"model={self.model!r}, "
        f"enabled={self.enabled!r}"
        ")"
    )



def __str__(
    self,
) -> str:
    """
    Human readable representation.
    """

    return (
        f"Provider: {self.name}\n"
        f"Model: {self.model}\n"
        f"Enabled: {self.enabled}"
    )

    # =========================================================================
# Security Helpers
# =========================================================================

def get_safe_configuration(
    self,
) -> dict[str, Any]:
    """
    Return provider configuration with sensitive values masked.

    Sensitive fields:
    - api_key
    - token
    - secret
    - password

    Returns
    -------
    dict[str, Any]
        Sanitized configuration.
    """

    configuration = (
        self.get_configuration()
        .copy()
    )


    sensitive_fields = (
        "api_key",
        "token",
        "secret",
        "password",
    )


    for field in sensitive_fields:

        if field in configuration:

            value = configuration[field]

            if value:

                configuration[field] = (
                    "********"
                )


    return configuration



# =========================================================================
# Configuration Update Helpers
# =========================================================================

def update_configuration(
    self,
    **kwargs: Any,
) -> bool:
    """
    Update provider configuration fields.

    Parameters
    ----------
    kwargs:
        Configuration fields.

    Returns
    -------
    bool
        True if update succeeds.
    """

    try:

        configuration = (
            self.get_configuration()
            .copy()
        )


        configuration.update(
            kwargs
        )


        self.load_configuration(
            configuration
        )


        valid, message = (
            self.validate_configuration()
        )


        if not valid:

            logger.warning(
                "Configuration update validation failed: %s",
                message,
            )

            return False


        return True


    except Exception:

        logger.exception(
            "Provider configuration update failed."
        )

        return False



# =========================================================================
# Clone Support
# =========================================================================

def clone(
    self,
) -> "ProviderSettings":
    """
    Create an independent copy of provider settings.

    Returns
    -------
    ProviderSettings
        New provider settings instance.
    """

    cloned = (
        self.__class__()
    )


    cloned.load_configuration(
        self.get_configuration()
        .copy()
    )


    return cloned



# =========================================================================
# Comparison Helpers
# =========================================================================

def __eq__(
    self,
    other: object,
) -> bool:
    """
    Compare two provider configurations.
    """

    if not isinstance(
        other,
        self.__class__,
    ):

        return False


    return (
        self.get_configuration()
        ==
        other.get_configuration()
    )



# =========================================================================
# Provider Switching
# =========================================================================

def switch_provider(
    self,
    provider_name: str,
    model: str | None = None,
) -> bool:
    """
    Switch active provider.

    Useful for runtime provider selection.

    Parameters
    ----------
    provider_name:
        Provider identifier.

    model:
        Optional model override.

    Returns
    -------
    bool
        True if switch succeeds.
    """

    if not provider_name:

        logger.warning(
            "Provider name cannot be empty."
        )

        return False


    try:

        self.name = (
            provider_name
        )


        if model:

            self.model = (
                model
            )


        logger.info(
            "Provider switched to %s.",
            provider_name,
        )


        return True


    except Exception:

        logger.exception(
            "Unable to switch provider."
        )

        return False



# =========================================================================
# Final State Export
# =========================================================================

def export_state(
    self,
) -> dict[str, Any]:
    """
    Export complete runtime state.

    Returns
    -------
    dict[str, Any]
        Provider state snapshot.
    """

    return {
        "configuration": (
            self.get_safe_configuration()
        ),

        "valid": (
            self.validate_configuration()[0]
        ),

        "provider": (
            self.name
        ),

        "model": (
            self.model
        ),
    }

    # =========================================================================
# Property Accessors
# =========================================================================

@property
def provider_name(
    self,
) -> str:
    """
    Return active provider name.
    """

    return self.name



@provider_name.setter
def provider_name(
    self,
    value: str,
) -> None:
    """
    Update provider name.
    """

    self.name = value



@property
def active_model(
    self,
) -> str:
    """
    Return active model name.
    """

    return self.model



@active_model.setter
def active_model(
    self,
    value: str,
) -> None:
    """
    Update active model.
    """

    self.model = value



@property
def is_active(
    self,
) -> bool:
    """
    Check whether provider is enabled.
    """

    return bool(
        self.enabled
    )



# =========================================================================
# Provider Status Helpers
# =========================================================================

def enable(
    self,
) -> None:
    """
    Enable provider.
    """

    self.enabled = True

    logger.info(
        "Provider enabled."
    )



def disable(
    self,
) -> None:
    """
    Disable provider.
    """

    self.enabled = False

    logger.info(
        "Provider disabled."
    )



def get_provider_summary(
    self,
) -> str:
    """
    Return human readable provider summary.
    """

    status = (
        "Enabled"
        if self.enabled
        else "Disabled"
    )


    return (
        f"{self.name} | "
        f"{self.model} | "
        f"{status}"
    )



# =========================================================================
# Backward Compatibility Helpers
# =========================================================================

def get_provider_config(
    self,
) -> dict[str, Any]:
    """
    Backward compatible alias.

    Deprecated:
        Use get_configuration()
    """

    logger.warning(
        "get_provider_config() is deprecated. "
        "Use get_configuration()."
    )

    return (
        self.get_configuration()
    )



def set_provider_config(
    self,
    configuration: dict[str, Any],
) -> None:
    """
    Backward compatible alias.

    Deprecated:
        Use load_configuration()
    """

    logger.warning(
        "set_provider_config() is deprecated. "
        "Use load_configuration()."
    )

    self.load_configuration(
        configuration
    )



# =========================================================================
# Lifecycle Validation
# =========================================================================

def is_configured(
    self,
) -> bool:
    """
    Check whether provider has minimum configuration.
    """

    valid, _ = (
        self.validate_configuration()
    )

    return valid



def ensure_ready(
    self,
) -> None:
    """
    Raise exception when provider is not ready.

    Raises
    ------
    RuntimeError
        If provider configuration is invalid.
    """

    valid, message = (
        self.validate_configuration()
    )


    if not valid:

        raise RuntimeError(
            message
        )



# =========================================================================
# Debug Information
# =========================================================================

def debug_info(
    self,
) -> dict[str, Any]:
    """
    Return debugging information.

    Sensitive fields are masked.
    """

    return {
        "provider": self.name,

        "model": self.model,

        "enabled": self.enabled,

        "configuration": (
            self.get_safe_configuration()
        ),
    }

    # =========================================================================
# Module Level Factory Helpers
# =========================================================================


def create_provider_settings(
    configuration: dict[str, Any] | None = None,
) -> "ProviderSettings":
    """
    Create a new ProviderSettings instance.

    Parameters
    ----------
    configuration:
        Optional initial configuration.

    Returns
    -------
    ProviderSettings
        Configured provider settings instance.
    """

    settings = (
        ProviderSettings()
    )


    if configuration:

        settings.load_configuration(
            configuration
        )


    return settings



# =========================================================================
# Default Provider Factory
# =========================================================================


def create_default_provider_settings(
) -> "ProviderSettings":
    """
    Create default local development provider.

    Default:
        Ollama + qwen3:4b

    Returns
    -------
    ProviderSettings
        Default provider configuration.
    """

    return ProviderSettings(
        name="ollama",
        model="qwen3:4b",
        base_url=(
            "http://localhost:11434"
        ),
        enabled=True,
    )



# =========================================================================
# Configuration Validation Wrapper
# =========================================================================


def validate_provider_configuration(
    configuration: dict[str, Any],
) -> tuple[bool, str]:
    """
    Validate external provider configuration.

    Parameters
    ----------
    configuration:
        Provider configuration dictionary.

    Returns
    -------
    tuple[bool, str]
        Validation result.
    """

    settings = (
        create_provider_settings(
            configuration
        )
    )


    return (
        settings.validate_configuration()
    )



# =========================================================================
# Configuration Import Helpers
# =========================================================================


def load_provider_settings(
    source: dict[str, Any] | None = None,
) -> ProviderSettings:
    """
    Load provider settings from external source.

    Parameters
    ----------
    source:
        Configuration dictionary.

    Returns
    -------
    ProviderSettings
        Provider configuration instance.
    """

    if source is None:

        return (
            create_default_provider_settings()
        )


    return (
        create_provider_settings(
            source
        )
    )



# =========================================================================
# Configuration Export Helpers
# =========================================================================


def export_provider_configuration(
    settings: ProviderSettings,
) -> dict[str, Any]:
    """
    Export provider configuration safely.

    Parameters
    ----------
    settings:
        ProviderSettings instance.

    Returns
    -------
    dict[str, Any]
        Safe configuration dictionary.
    """

    if not isinstance(
        settings,
        ProviderSettings,
    ):

        raise TypeError(
            "settings must be ProviderSettings instance."
        )


    return (
        settings.get_safe_configuration()
    )



# =========================================================================
# Module Information
# =========================================================================


__all__ = [

    "ProviderSettings",

    "create_provider_settings",

    "create_default_provider_settings",

    "validate_provider_configuration",

    "load_provider_settings",

    "export_provider_configuration",

]

# =============================================================================
# Backward Compatibility Wrapper
# =============================================================================

def render_provider_settings(
    state: ProviderState | None = None,
    *,
    on_save=None,
    on_test_connection=None,
    on_refresh_models=None,
) -> ProviderSettingsComponent:
    """
    Render the Provider Settings component.

    Returns
    -------
    ProviderSettingsComponent
        The rendered component instance.
    """

    component = ProviderSettingsComponent(
        state=state,
        on_save=on_save,
        on_test_connection=on_test_connection,
        on_refresh_models=on_refresh_models,
    )

    component.render()

    return component