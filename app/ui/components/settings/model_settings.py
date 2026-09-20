"""
File: app/ui/components/settings/model_settings.py

Production-ready Model Settings component for the AI Research Assistant.

This module manages LLM model-level configuration from the UI layer.

Responsibilities:
    - Model selection
    - Generation parameter configuration
    - Context management
    - Research analysis tuning
    - Embedding and vision model settings

Persistence and runtime execution are handled by:
    - app/config/model_config.py
    - app/config/settings_manager.py

Author:
    AI Research Assistant Project

License:
    MIT
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

import streamlit as st


logger = logging.getLogger(__name__)



# ============================================================================
# Model Capability Definitions
# ============================================================================


class ModelCapability(str, Enum):
    """
    Supported model capabilities.
    """

    CHAT = "Chat"

    REASONING = "Reasoning"

    VISION = "Vision"

    EMBEDDING = "Embedding"

    TOOL_USE = "Tool Use"

    LONG_CONTEXT = "Long Context"



class ModelProvider(str, Enum):
    """
    Model providers supported by the application.
    """

    OLLAMA = "Ollama"

    OPENAI = "OpenAI"

    GEMINI = "Gemini"

    DEEPSEEK = "DeepSeek"

    AZURE_OPENAI = "Azure OpenAI"

    OPENROUTER = "OpenRouter"

    CUSTOM = "Custom"



# ============================================================================
# Model Metadata
# ============================================================================


@dataclass(slots=True)
class ModelMetadata:
    """
    Describes model capabilities and information.
    """

    name: str

    provider: ModelProvider

    description: str

    capabilities: list[ModelCapability] = field(
        default_factory=list
    )

    context_window: int = 4096

    supports_streaming: bool = True

    recommended_for_research: bool = False



# ============================================================================
# Model Runtime State
# ============================================================================


@dataclass(slots=True)
class ModelState:
    """
    Current model configuration state.
    """

    provider: ModelProvider = (
        ModelProvider.OLLAMA
    )


    active_model: str = ""


    embedding_model: str = ""


    vision_model: str = ""


    available_models: list[str] = field(
        default_factory=list
    )


    temperature: float = 0.3


    top_p: float = 0.9


    top_k: int = 40


    max_tokens: int = 2048


    context_window: int = 8192


    frequency_penalty: float = 0.0


    presence_penalty: float = 0.0


    enable_streaming: bool = True


    enable_reasoning: bool = True


    reasoning_level: str = "Balanced"


    chunk_size: int = 1200


    chunk_overlap: int = 200


    citation_mode: bool = True



# ============================================================================
# Model Registry
# ============================================================================


MODEL_REGISTRY: dict[str, ModelMetadata] = {


    "qwen3:4b": ModelMetadata(

        name="qwen3:4b",

        provider=ModelProvider.OLLAMA,

        description=(
            "Lightweight local model suitable "
            "for development and experimentation."
        ),

        capabilities=[

            ModelCapability.CHAT,

            ModelCapability.REASONING,

        ],

        context_window=8192,

        recommended_for_research=True,
    ),



    "llama3.1": ModelMetadata(

        name="llama3.1",

        provider=ModelProvider.OLLAMA,

        description=(
            "General purpose open-source "
            "language model."
        ),

        capabilities=[

            ModelCapability.CHAT,

            ModelCapability.TOOL_USE,

        ],

        context_window=8192,

    ),



    "gpt-4.1": ModelMetadata(

        name="gpt-4.1",

        provider=ModelProvider.OPENAI,

        description=(
            "High quality cloud model "
            "for advanced research analysis."
        ),

        capabilities=[

            ModelCapability.CHAT,

            ModelCapability.REASONING,

            ModelCapability.LONG_CONTEXT,

        ],

        context_window=128000,

        recommended_for_research=True,

    ),



    "gemini-2.5-pro": ModelMetadata(

        name="gemini-2.5-pro",

        provider=ModelProvider.GEMINI,

        description=(
            "Multimodal research model."
        ),

        capabilities=[

            ModelCapability.CHAT,

            ModelCapability.VISION,

            ModelCapability.LONG_CONTEXT,

        ],

        context_window=1000000,

        recommended_for_research=True,

    ),

}



# ============================================================================
# Component
# ============================================================================


class ModelSettingsComponent:
    """
    Production Streamlit component for model settings.

    UI layer only.

    Configuration persistence and model execution are delegated to the
    configuration/service layers.
    """


    def __init__(
        self,
        *,
        state: ModelState | None = None,

        on_save: Callable[
            [ModelState],
            None
        ]
        | None = None,

        on_reset: Callable[
            [],
            None
        ]
        | None = None,

    ) -> None:
        """
        Initialize model settings component.
        """

        self.state = (
            state
            if state
            else ModelState()
        )


        self._on_save = on_save

        self._on_reset = on_reset


        logger.debug(
            "ModelSettingsComponent initialized."
        )



    # Rendering methods continue in Part 2.

    # ============================================================================
# Main Rendering
# ============================================================================


    def render(self) -> None:
        """
        Render complete Model Settings interface.

        Rendering order:

            1. Initialize state
            2. Header
            3. Current model summary
            4. Model selection
            5. Parameter configuration
            6. Research settings
            7. Actions
        """

        self._initialize_session_state()


        self._render_header()


        st.divider()


        self._render_model_summary()


        st.divider()


        self._render_model_selector()



# ============================================================================
# Session State
# ============================================================================


    def _initialize_session_state(
        self,
    ) -> None:
        """
        Initialize Streamlit session values.

        Streamlit reruns the application on every interaction.
        Session state preserves temporary UI configuration.
        """

        if (
            "model_settings_state"
            not in st.session_state
        ):

            st.session_state.model_settings_state = (
                self.state
            )


            logger.debug(
                "Initialized model settings session state."
            )



# ============================================================================
# Header
# ============================================================================


    def _render_header(
        self,
    ) -> None:
        """
        Render settings header.
        """

        render_html("""
            <div class="settings-header">

                <h2>
                    🧠 Model Configuration
                </h2>

                <p>
                    Configure language models,
                    generation parameters,
                    and research analysis behaviour.
                </p>

            </div>
            """)



# ============================================================================
# Model Summary
# ============================================================================


    def _render_model_summary(
        self,
    ) -> None:
        """
        Display current model information.
        """

        st.subheader(
            "Current Model"
        )


        col1, col2, col3 = st.columns(
            3
        )


        with col1:

            st.metric(
                label="Provider",

                value=(
                    self.state
                    .provider
                    .value
                ),
            )


        with col2:

            model_name = (
                self.state.active_model
                if self.state.active_model
                else "Not Selected"
            )


            st.metric(
                label="Model",

                value=model_name,
            )


        with col3:

            st.metric(
                label="Context Window",

                value=(
                    f"{self.state.context_window:,}"
                    " tokens"
                ),
            )


        self._render_model_capability_info()



# ============================================================================
# Capability Information
# ============================================================================


    def _render_model_capability_info(
        self,
    ) -> None:
        """
        Display selected model capabilities.
        """

        metadata = MODEL_REGISTRY.get(
            self.state.active_model
        )


        if metadata is None:

            st.info(
                "Select a model to view capabilities."
            )

            return


        with st.expander(
            "Model Capabilities",
            expanded=False,
        ):


            st.write(
                metadata.description
            )


            for capability in (
                metadata.capabilities
            ):

                st.write(
                    f"✅ {capability.value}"
                )


            st.write(
                (
                    "Context Window: "
                    f"{metadata.context_window:,}"
                    " tokens"
                )
            )


            if metadata.recommended_for_research:

                st.success(
                    "Recommended for research analysis."
                )

    # ============================================================================
# Model Selector
# ============================================================================


    def _render_model_selector(
        self,
    ) -> None:
        """
        Render model selection interface.
        """

        st.subheader(
            "Model Selection"
        )


        self._render_provider_selector()


        st.divider()


        self._render_available_model_selector()


        self._render_manual_model_input()



# ============================================================================
# Provider Selector
# ============================================================================


    def _render_provider_selector(
        self,
    ) -> None:
        """
        Render model provider selector.
        """

        providers = list(
            ModelProvider
        )


        current_index = providers.index(
            self.state.provider
        )


        selected_provider = st.selectbox(
            label="Model Provider",

            options=providers,

            index=current_index,

            format_func=lambda item:
                item.value,
        )


        if selected_provider != (
            self.state.provider
        ):

            logger.info(
                "Model provider changed: %s -> %s",
                self.state.provider.value,
                selected_provider.value,
            )


            self.state.provider = (
                selected_provider
            )


            self.state.active_model = ""

            self.state.available_models.clear()



# ============================================================================
# Available Model Selector
# ============================================================================


    def _render_available_model_selector(
        self,
    ) -> None:
        """
        Render available model dropdown.

        Models are filtered according to selected provider.
        """

        models = (
            self._get_provider_models()
        )


        if not models:

            st.info(
                "No registered models available "
                "for this provider."
            )

            return



        selected_model = st.selectbox(

            label="Available Models",

            options=models,

            index=(
                models.index(
                    self.state.active_model
                )
                if self.state.active_model
                in models
                else 0
            ),
        )



        if selected_model:

            if selected_model != (
                self.state.active_model
            ):

                self.state.active_model = (
                    selected_model
                )


                self._load_model_defaults(
                    selected_model
                )



# ============================================================================
# Manual Model Input
# ============================================================================


    def _render_manual_model_input(
        self,
    ) -> None:
        """
        Allow custom model names.

        Required for:
            - New Ollama models
            - Custom endpoints
            - Future providers
        """

        st.markdown(
            "#### Custom Model"
        )


        custom_model = st.text_input(

            label="Enter model name manually",

            value=self.state.active_model,

            placeholder=(
                "Example: qwen3:4b"
            ),

        )


        if custom_model:

            self.state.active_model = (
                custom_model
            )



# ============================================================================
# Model Registry Helpers
# ============================================================================


    def _get_provider_models(
        self,
    ) -> list[str]:
        """
        Return models for current provider.
        """

        return [

            name

            for name, metadata

            in MODEL_REGISTRY.items()

            if metadata.provider
            ==
            self.state.provider

        ]



    def _load_model_defaults(
        self,
        model_name: str,
    ) -> None:
        """
        Load recommended settings when model changes.
        """

        metadata = MODEL_REGISTRY.get(
            model_name
        )


        if metadata is None:

            return



        self.state.context_window = (
            metadata.context_window
        )


        if (
            ModelCapability.REASONING
            in metadata.capabilities
        ):

            self.state.enable_reasoning = True



        if metadata.recommended_for_research:

            self.state.reasoning_level = (
                "High"
            )


        logger.debug(
            "Loaded defaults for model %s",
            model_name,
        )



# ============================================================================
# Model Refresh Hook
# ============================================================================


    def refresh_models(
        self,
        models: list[str],
    ) -> None:
        """
        Update available models dynamically.

        Used by providers such as Ollama where models can change.
        """

        self.state.available_models = (
            models
        )


        logger.info(
            "Model list refreshed: %d models",
            len(models),
        )

    # ============================================================================
# Generation Settings
# ============================================================================


    def _render_generation_settings(
        self,
    ) -> None:
        """
        Render LLM generation parameters.

        These parameters control model response behaviour.
        """

        st.subheader(
            "Generation Parameters"
        )


        col1, col2 = st.columns(
            2
        )


        with col1:

            self.state.temperature = (
                st.slider(
                    label="Temperature",

                    min_value=0.0,

                    max_value=2.0,

                    value=self.state.temperature,

                    step=0.05,

                    help=(
                        "Controls randomness. "
                        "Lower values produce "
                        "more deterministic output."
                    ),
                )
            )



            self.state.top_p = (
                st.slider(
                    label="Top-P",

                    min_value=0.0,

                    max_value=1.0,

                    value=self.state.top_p,

                    step=0.05,

                    help=(
                        "Controls nucleus sampling."
                    ),
                )
            )



            self.state.top_k = (
                st.number_input(
                    label="Top-K",

                    min_value=0,

                    max_value=500,

                    value=self.state.top_k,

                    step=1,

                    help=(
                        "Limits candidate tokens."
                    ),
                )
            )



        with col2:

            self.state.max_tokens = (
                st.number_input(
                    label="Maximum Output Tokens",

                    min_value=128,

                    max_value=32768,

                    value=self.state.max_tokens,

                    step=128,

                    help=(
                        "Maximum generated response size."
                    ),
                )
            )



            self.state.frequency_penalty = (
                st.slider(
                    label="Frequency Penalty",

                    min_value=-2.0,

                    max_value=2.0,

                    value=self.state.frequency_penalty,

                    step=0.1,

                    help=(
                        "Reduces repeated phrases."
                    ),
                )
            )



            self.state.presence_penalty = (
                st.slider(
                    label="Presence Penalty",

                    min_value=-2.0,

                    max_value=2.0,

                    value=self.state.presence_penalty,

                    step=0.1,

                    help=(
                        "Encourages new topics."
                    ),
                )
            )



# ============================================================================
# Response Behaviour Settings
# ============================================================================


    def _render_response_settings(
        self,
    ) -> None:
        """
        Render response behaviour controls.
        """

        st.subheader(
            "Response Behaviour"
        )


        self.state.enable_streaming = (
            st.toggle(
                label="Enable Streaming Responses",

                value=self.state.enable_streaming,

                help=(
                    "Display generated output "
                    "incrementally."
                ),
            )
        )



        self.state.enable_reasoning = (
            st.toggle(
                label="Enable Reasoning Mode",

                value=self.state.enable_reasoning,

                help=(
                    "Enable deeper reasoning "
                    "for research analysis."
                ),
            )
        )



        reasoning_levels = [

            "Fast",

            "Balanced",

            "High",

            "Maximum",

        ]



        self.state.reasoning_level = (
            st.select_slider(
                label="Reasoning Level",

                options=reasoning_levels,

                value=self.state.reasoning_level,

            )
        )



# ============================================================================
# Generation Validation
# ============================================================================


    def _validate_generation_settings(
        self,
    ) -> tuple[bool, str]:
        """
        Validate generation parameters.

        Returns:
            Validation status and message.
        """

        if not (
            0.0
            <=
            self.state.temperature
            <=
            2.0
        ):

            return (

                False,

                "Temperature must be between 0 and 2."

            )



        if not (
            0.0
            <=
            self.state.top_p
            <=
            1.0
        ):

            return (

                False,

                "Top-P must be between 0 and 1."

            )



        if self.state.max_tokens <= 0:

            return (

                False,

                "Maximum tokens must be positive."

            )



        return (

            True,

            "Generation settings valid."

        )



# ============================================================================
# Recommended Presets
# ============================================================================


    def apply_research_preset(
        self,
    ) -> None:
        """
        Apply recommended settings for research paper analysis.

        Optimized for:
            - Accuracy
            - Structured reasoning
            - Long-form analysis
        """

        self.state.temperature = 0.2

        self.state.top_p = 0.9

        self.state.top_k = 40

        self.state.max_tokens = 4096

        self.state.enable_reasoning = True

        self.state.reasoning_level = (
            "High"
        )

        self.state.citation_mode = True



        logger.info(
            "Research analysis preset applied."
        )



    def apply_fast_preset(
        self,
    ) -> None:
        """
        Apply fast response preset.

        Useful for:
            - Quick summaries
            - UI testing
            - Development mode
        """

        self.state.temperature = 0.5

        self.state.top_p = 0.95

        self.state.top_k = 20

        self.state.max_tokens = 1024

        self.state.enable_reasoning = False

        self.state.reasoning_level = (
            "Fast"
        )



        logger.info(
            "Fast response preset applied."
        )

    # ============================================================================
# Context Configuration
# ============================================================================


    def _render_context_settings(
        self,
    ) -> None:
        """
        Render context window and long document settings.

        These settings control how large research papers are processed.
        """

        st.subheader(
            "Context & Document Processing"
        )


        self.state.context_window = (
            st.number_input(
                label="Context Window",

                min_value=1024,

                max_value=2000000,

                value=self.state.context_window,

                step=1024,

                help=(
                    "Maximum tokens available "
                    "for model context."
                ),
            )
        )


        col1, col2 = st.columns(
            2
        )


        with col1:

            self.state.chunk_size = (
                st.number_input(
                    label="Document Chunk Size",

                    min_value=200,

                    max_value=10000,

                    value=self.state.chunk_size,

                    step=100,

                    help=(
                        "Size of extracted text "
                        "chunks sent to the model."
                    ),
                )
            )


        with col2:

            self.state.chunk_overlap = (
                st.number_input(
                    label="Chunk Overlap",

                    min_value=0,

                    max_value=2000,

                    value=self.state.chunk_overlap,

                    step=50,

                    help=(
                        "Overlap between chunks "
                        "to preserve context."
                    ),
                )
            )


        if (
            self.state.chunk_overlap
            >=
            self.state.chunk_size
        ):

            st.warning(
                "Chunk overlap should be smaller "
                "than chunk size."
            )



# ============================================================================
# Research Analysis Settings
# ============================================================================


    def _render_research_settings(
        self,
    ) -> None:
        """
        Render research paper analysis controls.

        These settings are specific to the AI Research Assistant workflow.
        """

        st.subheader(
            "Research Analysis Settings"
        )


        analysis_modes = [

            "Quick Summary",

            "Standard Analysis",

            "Deep Research Analysis",

            "Publication Review",

        ]


        selected_mode = st.selectbox(
            label="Analysis Depth",

            options=analysis_modes,

            index=(
                analysis_modes.index(
                    "Deep Research Analysis"
                )
                if self.state.enable_reasoning
                else 0
            ),
        )


        st.session_state[
            "analysis_mode"
        ] = selected_mode



        self.state.citation_mode = (
            st.toggle(
                label="Enable Citation Extraction",

                value=self.state.citation_mode,

                help=(
                    "Extract references, "
                    "citations, and academic claims."
                ),
            )
        )



        enable_structure = st.toggle(
            label="Structured Research Report",

            value=True,

            help=(
                "Generate sections such as "
                "research gap, methodology, "
                "contributions and limitations."
            ),
        )


        st.session_state[
            "structured_report"
        ] = enable_structure



# ============================================================================
# Academic Quality Controls
# ============================================================================


    def _render_quality_settings(
        self,
    ) -> None:
        """
        Configure academic output quality.
        """

        st.subheader(
            "Research Quality Controls"
        )


        quality_level = st.select_slider(

            label="Analysis Quality Level",

            options=[

                "Basic",

                "Good",

                "Advanced",

                "Expert",

            ],

            value="Advanced",

        )


        st.session_state[
            "analysis_quality"
        ] = quality_level



        verification = st.toggle(

            label="Enable Claim Verification",

            value=True,

            help=(

                "Ask the model to distinguish "
                "facts, assumptions, and "
                "interpretations."

            ),
        )


        st.session_state[
            "claim_verification"
        ] = verification



        limitations = st.toggle(

            label="Highlight Limitations",

            value=True,

            help=(

                "Include weaknesses and "
                "future research directions."

            ),
        )


        st.session_state[
            "highlight_limitations"
        ] = limitations



# ============================================================================
# Context Validation
# ============================================================================


    def _validate_context_settings(
        self,
    ) -> tuple[bool, str]:
        """
        Validate context configuration.
        """

        if (
            self.state.chunk_size
            <= 0
        ):

            return (

                False,

                "Chunk size must be greater than zero."

            )


        if (
            self.state.chunk_overlap
            >=
            self.state.chunk_size
        ):

            return (

                False,

                "Chunk overlap must be smaller "
                "than chunk size."

            )


        if (
            self.state.context_window
            < 1024
        ):

            return (

                False,

                "Context window is too small."

            )


        return (

            True,

            "Context settings valid."

        )


    # ============================================================================
# Embedding Model Settings
# ============================================================================


    def _render_embedding_settings(
        self,
    ) -> None:
        """
        Render embedding model configuration.

        Embedding models are used for:
            - Semantic search
            - Paper retrieval
            - Knowledge indexing
            - RAG workflows
        """

        st.subheader(
            "Embedding Model Settings"
        )


        embedding_models = [

            "None",

            "nomic-embed-text",

            "mxbai-embed-large",

            "text-embedding-3-small",

            "text-embedding-3-large",

        ]


        selected_embedding = st.selectbox(

            label="Embedding Model",

            options=embedding_models,

            index=(

                embedding_models.index(
                    self.state.embedding_model
                )

                if self.state.embedding_model
                in embedding_models

                else 0

            ),

            help=(

                "Used for semantic search "
                "and document retrieval."

            ),

        )


        if selected_embedding != "None":

            self.state.embedding_model = (
                selected_embedding
            )

        else:

            self.state.embedding_model = ""



        enable_embeddings = st.toggle(

            label="Enable Semantic Retrieval",

            value=bool(
                self.state.embedding_model
            ),

        )


        if not enable_embeddings:

            self.state.embedding_model = ""



# ============================================================================
# Vision Model Settings
# ============================================================================


    def _render_vision_settings(
        self,
    ) -> None:
        """
        Render multimodal vision model settings.

        Used for:
            - Research paper figures
            - Tables
            - Charts
            - Mathematical diagrams
        """

        st.subheader(
            "Vision & Multimodal Settings"
        )


        vision_models = [

            "None",

            "llava",

            "llava-next",

            "gpt-4.1-vision",

            "gemini-2.5-pro",

        ]


        selected_vision = st.selectbox(

            label="Vision Model",

            options=vision_models,

            index=(

                vision_models.index(
                    self.state.vision_model
                )

                if self.state.vision_model
                in vision_models

                else 0

            ),

            help=(

                "Model used to understand "
                "images, diagrams and tables."

            ),

        )


        if selected_vision != "None":

            self.state.vision_model = (
                selected_vision
            )

        else:

            self.state.vision_model = ""



# ============================================================================
# Multimodal Analysis Controls
# ============================================================================


    def _render_multimodal_settings(
        self,
    ) -> None:
        """
        Configure multimodal research analysis.

        Enables future Research Paper Intelligence Engine features.
        """

        st.subheader(
            "Multimodal Research Analysis"
        )


        analyze_figures = st.toggle(

            label="Analyze Figures and Diagrams",

            value=True,

            help=(

                "Extract insights from "
                "figures, graphs and diagrams."

            ),

        )


        analyze_tables = st.toggle(

            label="Analyze Tables",

            value=True,

            help=(

                "Understand experimental "
                "tables and results."

            ),

        )


        analyze_equations = st.toggle(

            label="Analyze Mathematical Expressions",

            value=False,

            help=(

                "Support equation interpretation "
                "and mathematical explanations."

            ),

        )


        st.session_state[
            "analyze_figures"
        ] = analyze_figures


        st.session_state[
            "analyze_tables"
        ] = analyze_tables


        st.session_state[
            "analyze_equations"
        ] = analyze_equations



# ============================================================================
# Capability Detection
# ============================================================================


    def supports_capability(
        self,
        capability: ModelCapability,
    ) -> bool:
        """
        Check if selected model supports capability.

        Args:
            capability:
                Required model capability.

        Returns:
            True if supported.
        """

        metadata = MODEL_REGISTRY.get(

            self.state.active_model

        )


        if metadata is None:

            return False



        return (
            capability
            in
            metadata.capabilities
        )



    def has_vision_support(
        self,
    ) -> bool:
        """
        Check whether current model supports vision.
        """

        return self.supports_capability(
            ModelCapability.VISION
        )



    def has_long_context_support(
        self,
    ) -> bool:
        """
        Check long context support.
        """

        return self.supports_capability(
            ModelCapability.LONG_CONTEXT
        )



# ============================================================================
# Multimodal Validation
# ============================================================================


    def _validate_multimodal_settings(
        self,
    ) -> tuple[bool, str]:
        """
        Validate multimodal configuration.
        """

        if (
            st.session_state.get(
                "analyze_figures",
                False,
            )
            and not self.state.vision_model
        ):

            return (

                False,

                "Vision model required for "
                "figure analysis."

            )


        return (

            True,

            "Multimodal settings valid."

        )


    # ============================================================================
# Action Panel
# ============================================================================


    def _render_actions(
        self,
    ) -> None:
        """
        Render model settings action buttons.
        """

        st.subheader(
            "Model Settings Actions"
        )


        col1, col2, col3 = st.columns(
            3
        )


        with col1:

            if st.button(
                "💾 Save Model Settings",
                use_container_width=True,
            ):

                self._save_settings()



        with col2:

            if st.button(
                "♻️ Reset",
                use_container_width=True,
            ):

                self._reset_settings()



        with col3:

            if st.button(
                "🧪 Apply Research Preset",
                use_container_width=True,
            ):

                self.apply_research_preset()

                st.success(
                    "Research preset applied."
                )



# ============================================================================
# Save Workflow
# ============================================================================


    def _save_settings(
        self,
    ) -> None:
        """
        Validate and save model configuration.
        """

        validations = [

            self._validate_generation_settings(),

            self._validate_context_settings(),

            self._validate_multimodal_settings(),

        ]


        for valid, message in validations:

            if not valid:

                st.warning(
                    message
                )

                return



        logger.info(
            "Saving model configuration."
        )


        try:

            if self._on_save:

                self._on_save(
                    self.state
                )


                st.success(
                    "Model settings saved."
                )


            else:

                st.info(
                    "Save callback not configured."
                )



        except Exception as exc:

            logger.exception(
                "Failed saving model settings."
            )


            st.error(
                str(exc)
            )



# ============================================================================
# Reset Workflow
# ============================================================================


    def _reset_settings(
        self,
    ) -> None:
        """
        Reset model settings to defaults.
        """

        logger.info(
            "Resetting model settings."
        )


        self.state = ModelState()


        if self._on_reset:

            self._on_reset()



        st.success(
            "Model settings reset."
        )


        st.rerun()



# ============================================================================
# Settings Manager Integration
# ============================================================================


    def load_configuration(
        self,
        configuration: dict[str, Any],
    ) -> None:
        """
        Load model configuration.

        Designed for integration with:
            app/config/settings_manager.py
        """

        try:

            provider = (
                configuration.get(
                    "provider"
                )
            )


            if provider:

                self.state.provider = (
                    ModelProvider(
                        provider
                    )
                )



            self.state.active_model = str(

                configuration.get(
                    "active_model",
                    "",
                )

            )


            self.state.embedding_model = str(

                configuration.get(
                    "embedding_model",
                    "",
                )

            )


            self.state.vision_model = str(

                configuration.get(
                    "vision_model",
                    "",
                )

            )


            self.state.temperature = float(

                configuration.get(
                    "temperature",
                    0.3,
                )

            )


            self.state.top_p = float(

                configuration.get(
                    "top_p",
                    0.9,
                )

            )


            self.state.max_tokens = int(

                configuration.get(
                    "max_tokens",
                    2048,
                )

            )


            self.state.context_window = int(

                configuration.get(
                    "context_window",
                    8192,
                )

            )


            logger.info(
                "Model configuration loaded."
            )



        except Exception as exc:

            logger.exception(
                "Unable to load model configuration."
            )

            raise exc



    def save_to_configuration_manager(
        self,
        settings_manager: Any,
    ) -> None:
        """
        Save configuration using SettingsManager.
        """

        settings_manager.save_model_config(

            self.to_dict()

        )


        logger.info(
            "Model configuration saved "
            "through SettingsManager."
        )



# ============================================================================
# Serialization
# ============================================================================


    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Convert model state into serializable dictionary.
        """

        return {

            "provider":
                self.state.provider.value,


            "active_model":
                self.state.active_model,


            "embedding_model":
                self.state.embedding_model,


            "vision_model":
                self.state.vision_model,


            "temperature":
                self.state.temperature,


            "top_p":
                self.state.top_p,


            "top_k":
                self.state.top_k,


            "max_tokens":
                self.state.max_tokens,


            "context_window":
                self.state.context_window,


            "frequency_penalty":
                self.state.frequency_penalty,


            "presence_penalty":
                self.state.presence_penalty,


            "enable_streaming":
                self.state.enable_streaming,


            "enable_reasoning":
                self.state.enable_reasoning,


            "reasoning_level":
                self.state.reasoning_level,


            "chunk_size":
                self.state.chunk_size,


            "chunk_overlap":
                self.state.chunk_overlap,


            "citation_mode":
                self.state.citation_mode,

        }


    # ============================================================================
# Model Factory Helpers
# ============================================================================


def create_default_model_state() -> ModelState:
    """
    Create default model configuration.

    Default follows project development strategy:
    local Ollama model first, cloud providers later.

    Returns:
        Default ModelState instance.
    """

    return ModelState(

        provider=ModelProvider.OLLAMA,

        active_model="qwen3:4b",

        context_window=8192,

        temperature=0.2,

        top_p=0.9,

        top_k=40,

        max_tokens=4096,

        enable_reasoning=True,

        reasoning_level="Balanced",

        citation_mode=True,

    )



def get_model_metadata(
    model_name: str,
) -> ModelMetadata | None:
    """
    Retrieve metadata for a model.

    Args:
        model_name:
            Model identifier.

    Returns:
        ModelMetadata or None.
    """

    return MODEL_REGISTRY.get(
        model_name
    )



def get_models_by_provider(
    provider: ModelProvider,
) -> list[str]:
    """
    Return available models for provider.

    Args:
        provider:
            Model provider.

    Returns:
        List of model names.
    """

    return [

        name

        for name, metadata

        in MODEL_REGISTRY.items()

        if metadata.provider == provider

    ]



# ============================================================================
# Preset Utilities
# ============================================================================


def create_research_model_preset() -> dict[str, Any]:
    """
    Return recommended settings for research paper analysis.

    Optimized for:
        - Academic reasoning
        - Long papers
        - Structured reports
        - Citation extraction
    """

    return {

        "temperature": 0.2,

        "top_p": 0.9,

        "top_k": 40,

        "max_tokens": 4096,

        "enable_reasoning": True,

        "reasoning_level": "High",

        "citation_mode": True,

        "chunk_size": 1200,

        "chunk_overlap": 200,

    }



def create_fast_analysis_preset() -> dict[str, Any]:
    """
    Return fast execution preset.

    Useful for:
        - UI testing
        - Development
        - Quick summaries
    """

    return {

        "temperature": 0.5,

        "top_p": 0.95,

        "top_k": 20,

        "max_tokens": 1024,

        "enable_reasoning": False,

        "reasoning_level": "Fast",

    }



# ============================================================================
# External Validation
# ============================================================================


def validate_model_configuration(
    configuration: dict[str, Any],
) -> tuple[bool, str]:
    """
    Validate model configuration externally.

    Can be used by services without creating UI component.

    Args:
        configuration:
            Model configuration dictionary.

    Returns:
        Validation status and message.
    """

    model = configuration.get(
        "active_model"
    )


    if not model:

        return (

            False,

            "Model is not selected."

        )



    temperature = float(

        configuration.get(
            "temperature",
            0.3,
        )

    )


    if not (
        0.0
        <= temperature
        <= 2.0
    ):

        return (

            False,

            "Temperature must be between 0 and 2."

        )



    max_tokens = int(

        configuration.get(
            "max_tokens",
            0,
        )

    )


    if max_tokens <= 0:

        return (

            False,

            "Invalid token limit."

        )



    return (

        True,

        "Model configuration valid."

    )



# ============================================================================
# Component Factory
# ============================================================================


def create_model_settings_component(
    *,
    state: ModelState | None = None,

    on_save: Callable[
        [ModelState],
        None
    ]
    | None = None,

    on_reset: Callable[
        [],
        None
    ]
    | None = None,

) -> ModelSettingsComponent:
    """
    Create ModelSettingsComponent instance.

    Keeps page-level code clean.

    Returns:
        Configured component.
    """

    return ModelSettingsComponent(

        state=state,

        on_save=on_save,

        on_reset=on_reset,

    )



# ============================================================================
# Module Exports
# ============================================================================


__all__ = [

    # Enums

    "ModelCapability",

    "ModelProvider",


    # Data Models

    "ModelMetadata",

    "ModelState",


    # Registry

    "MODEL_REGISTRY",


    # Component

    "ModelSettingsComponent",


    # Factories

    "create_default_model_state",

    "create_model_settings_component",


    # Metadata helpers

    "get_model_metadata",

    "get_models_by_provider",


    # Presets

    "create_research_model_preset",

    "create_fast_analysis_preset",


    # Validation

    "validate_model_configuration",

]