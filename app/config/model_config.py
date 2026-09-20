# =============================================================================
# File: app/config/model_config.py
# Production Ready Model Configuration Layer
# Version: 1.0.0
# =============================================================================

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
    asdict,
)

from typing import (
    Any,
)


import logging


logger = logging.getLogger(
    __name__
)


# =============================================================================
# Model Configuration Dataclass
# =============================================================================


@dataclass
class ModelConfig:
    """
    Defines an AI model configuration.

    This layer describes model capabilities,
    independent of provider implementation.

    Examples:
        Ollama -> qwen3:4b
        OpenAI -> gpt-4.1
        Gemini -> gemini-2.5-pro
    """

    name: str

    provider: str

    context_window: int = 4096

    max_tokens: int = 2048

    temperature: float = 0.7

    supports_streaming: bool = False

    supports_vision: bool = False

    supports_tools: bool = False

    description: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Convert model configuration to dictionary.
        """

        return asdict(
            self
        )


    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "ModelConfig":
        """
        Create ModelConfig from dictionary.
        """

        return cls(
            **data
        )



    def validate(
        self,
    ) -> tuple[bool, str]:
        """
        Validate model configuration.
        """

        if not self.name:

            return (
                False,
                "Model name is required.",
            )


        if not self.provider:

            return (
                False,
                "Provider name is required.",
            )


        if self.context_window <= 0:

            return (
                False,
                "Context window must be positive.",
            )


        if self.max_tokens <= 0:

            return (
                False,
                "Max tokens must be positive.",
            )


        if not (
            0 <= self.temperature <= 2
        ):

            return (
                False,
                "Temperature must be between 0 and 2.",
            )


        return (
            True,
            "Model configuration valid.",
        )



# =============================================================================
# Model Registry
# =============================================================================


class ModelRegistry:
    """
    Central registry for available AI models.

    Provides:
        - model lookup
        - registration
        - provider filtering
        - runtime switching
    """


    def __init__(
        self,
    ) -> None:

        self._models: dict[
            str,
            ModelConfig
        ] = {}


        self._load_default_models()



    # -------------------------------------------------------------------------
    # Default Models
    # -------------------------------------------------------------------------

    def _load_default_models(
        self,
    ) -> None:
        """
        Register default supported models.
        """


        defaults = [

            ModelConfig(
                name="qwen3:4b",
                provider="ollama",
                context_window=8192,
                max_tokens=2048,
                temperature=0.7,
                description=(
                    "Local lightweight Qwen model."
                ),
            ),


            ModelConfig(
                name="llama3.1",
                provider="ollama",
                context_window=8192,
                max_tokens=4096,
                temperature=0.7,
                description=(
                    "Local Llama model."
                ),
            ),


            ModelConfig(
                name="gpt-4.1",
                provider="openai",
                context_window=128000,
                max_tokens=8192,
                supports_tools=True,
                supports_streaming=True,
                description=(
                    "OpenAI advanced reasoning model."
                ),
            ),


            ModelConfig(
                name="gemini-2.5-pro",
                provider="gemini",
                context_window=1000000,
                max_tokens=8192,
                supports_vision=True,
                supports_tools=True,
                description=(
                    "Google multimodal reasoning model."
                ),
            ),

        ]


        for model in defaults:

            self.register(
                model
            )



    # -------------------------------------------------------------------------
    # Registration
    # -------------------------------------------------------------------------

    def register(
        self,
        model: ModelConfig,
    ) -> None:
        """
        Register a model.
        """

        valid, message = (
            model.validate()
        )


        if not valid:

            raise ValueError(
                message
            )


        self._models[
            model.name
        ] = model


        logger.info(
            "Registered model: %s",
            model.name,
        )



    # -------------------------------------------------------------------------
    # Lookup
    # -------------------------------------------------------------------------

    def get(
        self,
        model_name: str,
    ) -> ModelConfig | None:
        """
        Retrieve model configuration.
        """

        return self._models.get(
            model_name
        )



    def exists(
        self,
        model_name: str,
    ) -> bool:
        """
        Check model availability.
        """

        return (
            model_name
            in self._models
        )



    # -------------------------------------------------------------------------
    # Filtering
    # -------------------------------------------------------------------------

    def get_by_provider(
        self,
        provider: str,
    ) -> list[ModelConfig]:
        """
        Return models belonging to provider.
        """

        return [

            model

            for model in self._models.values()

            if model.provider == provider

        ]



    def list_models(
        self,
    ) -> list[str]:
        """
        Return available model names.
        """

        return list(
            self._models.keys()
        )



    def export(
        self,
    ) -> dict[str, dict[str, Any]]:
        """
        Export registry.
        """

        return {

            name: model.to_dict()

            for name, model
            in self._models.items()

        }


# =============================================================================
# Global Registry Instance
# =============================================================================


MODEL_REGISTRY = ModelRegistry()



# =============================================================================
# Helper Functions
# =============================================================================


def get_model_config(
    model_name: str,
) -> ModelConfig | None:
    """
    Retrieve model configuration.
    """

    return MODEL_REGISTRY.get(
        model_name
    )



def list_available_models() -> list[str]:
    """
    List available models.
    """

    return MODEL_REGISTRY.list_models()



def register_model(
    model: ModelConfig,
) -> None:
    """
    Add custom model.
    """

    MODEL_REGISTRY.register(
        model
    )



__all__ = [

    "ModelConfig",

    "ModelRegistry",

    "MODEL_REGISTRY",

    "get_model_config",

    "list_available_models",

    "register_model",

]

# =============================================================================
# Advanced Model Profile Support
# =============================================================================


@dataclass
class ModelProfile:
    """
    High-level model profile.

    Used for intelligent model selection.

    Examples:
        research_analysis
        summarization
        quick_response
        coding
        vision_analysis
    """

    name: str

    description: str = ""

    preferred_providers: list[str] = field(
        default_factory=list
    )

    required_capabilities: list[str] = field(
        default_factory=list
    )

    preferred_models: list[str] = field(
        default_factory=list
    )

    max_cost_level: int = 1

    priority: str = "balanced"


    def matches(
        self,
        model: ModelConfig,
    ) -> bool:
        """
        Check whether model satisfies profile.
        """


        if (
            self.preferred_providers
            and
            model.provider
            not in self.preferred_providers
        ):

            return False



        capability_map = {

            "vision":
                model.supports_vision,

            "tools":
                model.supports_tools,

            "streaming":
                model.supports_streaming,

        }



        for capability in (
            self.required_capabilities
        ):

            if not capability_map.get(
                capability,
                False,
            ):

                return False



        if (
            self.preferred_models
            and
            model.name
            not in self.preferred_models
        ):

            return False



        return True



# =============================================================================
# Model Performance Metadata
# =============================================================================


@dataclass
class ModelPerformance:
    """
    Runtime performance information.

    Used for model selection decisions.
    """

    speed_score: float = 0.5

    reasoning_score: float = 0.5

    quality_score: float = 0.5

    memory_requirement_gb: float = 0.0


    def validate(
        self,
    ) -> bool:
        """
        Validate score ranges.
        """

        scores = (

            self.speed_score,

            self.reasoning_score,

            self.quality_score,

        )


        return all(

            0 <= score <= 1

            for score in scores

        )



# =============================================================================
# Model Cost Metadata
# =============================================================================


@dataclass
class ModelCost:
    """
    Cost classification.

    Level:
        0 -> Free/local
        1 -> Low
        2 -> Medium
        3 -> High
    """

    level: int = 0

    input_cost: float = 0.0

    output_cost: float = 0.0



    def is_allowed(
        self,
        maximum_level: int,
    ) -> bool:
        """
        Check cost policy.
        """

        return (
            self.level
            <= maximum_level
        )



# =============================================================================
# Model Intelligence Layer
# =============================================================================


class ModelSelector:
    """
    Intelligent model selection engine.

    Chooses models based on:

    - task profile
    - capabilities
    - cost limits
    - performance
    """


    def __init__(
        self,
        registry: ModelRegistry,
    ) -> None:

        self.registry = registry


        self.profiles = (
            self._create_default_profiles()
        )


        self.performance: dict[
            str,
            ModelPerformance
        ] = {}


        self.cost: dict[
            str,
            ModelCost
        ] = {}



    def _create_default_profiles(
        self,
    ) -> dict[str, ModelProfile]:

        return {

            "research_analysis":

                ModelProfile(

                    name="research_analysis",

                    description=(
                        "Deep paper analysis and "
                        "academic reasoning."
                    ),

                    required_capabilities=[],

                    priority="quality",

                    preferred_models=[

                        "qwen3:4b",

                        "gpt-4.1",

                        "gemini-2.5-pro",

                    ],

                ),



            "quick_summary":

                ModelProfile(

                    name="quick_summary",

                    description=(
                        "Fast summarization."
                    ),

                    priority="speed",

                    preferred_providers=[

                        "ollama",

                    ],

                ),



            "vision_analysis":

                ModelProfile(

                    name="vision_analysis",

                    description=(
                        "Figures, charts, images."
                    ),

                    required_capabilities=[

                        "vision",

                    ],

                    priority="quality",

                ),

        }



    def set_performance(
        self,
        model_name: str,
        performance: ModelPerformance,
    ) -> None:
        """
        Add performance metadata.
        """

        if not performance.validate():

            raise ValueError(
                "Invalid performance scores."
            )


        self.performance[
            model_name
        ] = performance



    def set_cost(
        self,
        model_name: str,
        cost: ModelCost,
    ) -> None:
        """
        Add cost metadata.
        """

        self.cost[
            model_name
        ] = cost



    def select(
        self,
        profile_name: str,
    ) -> ModelConfig | None:
        """
        Select best model for profile.
        """

        profile = (
            self.profiles.get(
                profile_name
            )
        )


        if profile is None:

            return None



        candidates = [

            model

            for model

            in self.registry._models.values()

            if profile.matches(model)

        ]



        if not candidates:

            return None



        if profile.priority == "speed":

            candidates.sort(

                key=lambda model:

                self.performance.get(

                    model.name,

                    ModelPerformance()

                ).speed_score,

                reverse=True,

            )


        elif profile.priority == "quality":

            candidates.sort(

                key=lambda model:

                self.performance.get(

                    model.name,

                    ModelPerformance()

                ).quality_score,

                reverse=True,

            )


        return candidates[0]

# =============================================================================
# Model Registry Persistence
# =============================================================================


class ModelConfigManager:
    """
    Persistence and integration manager for model configurations.

    Responsibilities:
        - Import/export model registry
        - Environment loading
        - Configuration manager sync
        - Runtime updates
    """


    def __init__(
        self,
        registry: ModelRegistry | None = None,
    ) -> None:

        self.registry = (
            registry
            or MODEL_REGISTRY
        )


    # -------------------------------------------------------------------------
    # Export Registry
    # -------------------------------------------------------------------------

    def export_registry(
        self,
    ) -> dict[str, Any]:
        """
        Export complete model registry.

        Returns
        -------
        dict[str, Any]
            Serializable model registry.
        """

        return {

            "models":
            self.registry.export()

        }



    # -------------------------------------------------------------------------
    # Import Registry
    # -------------------------------------------------------------------------

    def import_registry(
        self,
        data: dict[str, Any],
    ) -> int:
        """
        Import models into registry.

        Parameters
        ----------
        data:
            Registry dictionary.

        Returns
        -------
        int
            Number of models imported.
        """

        if not isinstance(
            data,
            dict,
        ):

            raise TypeError(
                "Registry data must be dictionary."
            )


        models = (
            data.get(
                "models",
                {},
            )
        )


        count = 0


        for name, config in (
            models.items()
        ):

            model = (
                ModelConfig.from_dict(
                    config
                )
            )


            self.registry.register(
                model
            )


            count += 1



        logger.info(
            "Imported %s models.",
            count,
        )


        return count



    # -------------------------------------------------------------------------
    # Environment Integration
    # -------------------------------------------------------------------------

    def load_from_environment(
        self,
        prefix: str = "AI_MODEL_",
    ) -> ModelConfig | None:
        """
        Load active model from environment.

        Supported variables:

            AI_MODEL_NAME
            AI_MODEL_PROVIDER
            AI_MODEL_CONTEXT
            AI_MODEL_MAX_TOKENS
            AI_MODEL_TEMPERATURE

        Returns
        -------
        ModelConfig | None
        """

        import os


        name = os.getenv(
            f"{prefix}NAME"
        )


        provider = os.getenv(
            f"{prefix}PROVIDER"
        )


        if not name or not provider:

            return None



        model = ModelConfig(

            name=name,

            provider=provider,

            context_window=int(

                os.getenv(

                    f"{prefix}CONTEXT",

                    "4096",

                )

            ),


            max_tokens=int(

                os.getenv(

                    f"{prefix}MAX_TOKENS",

                    "2048",

                )

            ),


            temperature=float(

                os.getenv(

                    f"{prefix}TEMPERATURE",

                    "0.7",

                )

            ),

        )


        self.registry.register(
            model
        )


        return model



    # -------------------------------------------------------------------------
    # Configuration Manager Sync
    # -------------------------------------------------------------------------

    def sync_with_configuration_manager(
        self,
        configuration_manager: Any,
    ) -> bool:
        """
        Synchronize model registry with external manager.

        Supported APIs:

            get_model_configuration()
            get_model_config()
            model_configuration attribute

        """

        if configuration_manager is None:

            return False


        try:

            data = None


            getter_methods = (

                "get_model_configuration",

                "get_model_config",

            )


            for method_name in getter_methods:

                method = getattr(

                    configuration_manager,

                    method_name,

                    None,

                )


                if callable(method):

                    data = method()

                    break



            if data is None:

                data = getattr(

                    configuration_manager,

                    "model_configuration",

                    None,

                )



            if data is None:

                return False



            self.import_registry(
                data
            )


            return True



        except Exception:

            logger.exception(

                "Model configuration sync failed."

            )

            return False



    # -------------------------------------------------------------------------
    # Save To Configuration Manager
    # -------------------------------------------------------------------------

    def save_to_configuration_manager(
        self,
        configuration_manager: Any,
    ) -> bool:
        """
        Save model registry externally.
        """

        if configuration_manager is None:

            return False



        data = (
            self.export_registry()
        )


        try:

            save_methods = (

                "save_model_configuration",

                "save_model_config",

            )


            for method_name in save_methods:

                method = getattr(

                    configuration_manager,

                    method_name,

                    None,

                )


                if callable(method):

                    method(
                        data
                    )

                    return True



            if hasattr(

                configuration_manager,

                "model_configuration",

            ):

                configuration_manager.model_configuration = (

                    data

                )

                return True



            return False



        except Exception:

            logger.exception(

                "Unable to save model configuration."

            )

            return False

# =============================================================================
# Hardware Profile
# =============================================================================


@dataclass
class HardwareProfile:
    """
    Describes available execution hardware.

    Used for intelligent model selection.

    Examples:
        Laptop development mode
        Cloud production mode
    """

    ram_gb: float = 8.0

    cpu_cores: int = 4

    has_gpu: bool = False

    gpu_memory_gb: float = 0.0



    def can_run(
        self,
        model: ModelConfig,
    ) -> bool:
        """
        Estimate whether hardware can run model.
        """

        required_memory = (
            model.metadata.get(
                "memory_requirement_gb",
                0,
            )
        )


        if required_memory:

            return (
                self.ram_gb
                >= required_memory
            )


        return True



# =============================================================================
# Runtime Model Policy
# =============================================================================


@dataclass
class ModelSelectionPolicy:
    """
    Defines runtime selection rules.
    """

    prefer_local: bool = True

    allow_cloud: bool = True

    maximum_cost_level: int = 1

    prioritize_quality: bool = True

    prioritize_speed: bool = False



# =============================================================================
# Hardware Aware Model Selector
# =============================================================================


class HardwareAwareModelSelector:
    """
    Selects models based on:

    - Hardware availability
    - Provider preference
    - Cost policy
    - Quality/speed requirement
    """


    def __init__(
        self,
        registry: ModelRegistry | None = None,
        hardware: HardwareProfile | None = None,
        policy: ModelSelectionPolicy | None = None,
    ) -> None:

        self.registry = (
            registry
            or MODEL_REGISTRY
        )


        self.hardware = (
            hardware
            or HardwareProfile()
        )


        self.policy = (
            policy
            or ModelSelectionPolicy()
        )



    # -------------------------------------------------------------------------
    # Candidate Filtering
    # -------------------------------------------------------------------------

    def get_candidates(
        self,
    ) -> list[ModelConfig]:
        """
        Return models matching hardware policy.
        """

        candidates = []


        for model in self.registry._models.values():

            if not self.hardware.can_run(
                model
            ):

                continue


            candidates.append(
                model
            )


        return candidates



    # -------------------------------------------------------------------------
    # Best Runtime Model
    # -------------------------------------------------------------------------

    def select_best(
        self,
        task: str = "research_analysis",
    ) -> ModelConfig | None:
        """
        Select optimal runtime model.

        Strategy:

        1. Local model preference
        2. Hardware compatibility
        3. Quality ranking
        4. Speed fallback
        """

        candidates = (
            self.get_candidates()
        )


        if not candidates:

            return None



        # -------------------------------------------------------------
        # Prefer local models
        # -------------------------------------------------------------

        if self.policy.prefer_local:

            local_models = [

                model

                for model in candidates

                if model.provider
                in (
                    "ollama",
                    "local",
                )

            ]


            if local_models:

                candidates = local_models



        # -------------------------------------------------------------
        # Quality ranking
        # -------------------------------------------------------------

        if self.policy.prioritize_quality:

            candidates.sort(

                key=lambda model:

                model.metadata.get(

                    "quality_score",

                    0.5,

                ),

                reverse=True,

            )


        # -------------------------------------------------------------
        # Speed ranking
        # -------------------------------------------------------------

        elif self.policy.prioritize_speed:

            candidates.sort(

                key=lambda model:

                model.metadata.get(

                    "speed_score",

                    0.5,

                ),

                reverse=True,

            )



        return candidates[0]



# =============================================================================
# Default Hardware Profiles
# =============================================================================


DEVELOPMENT_LAPTOP_PROFILE = HardwareProfile(

    ram_gb=12,

    cpu_cores=4,

    has_gpu=False,

)



CLOUD_PRODUCTION_PROFILE = HardwareProfile(

    ram_gb=64,

    cpu_cores=16,

    has_gpu=True,

    gpu_memory_gb=24,

)

# =============================================================================
# Model Fallback Configuration
# =============================================================================


@dataclass
class ModelFallbackRule:
    """
    Defines fallback behavior for a model.

    Example:

        qwen3:4b
            ↓
        llama3.1
            ↓
        gpt-4.1
    """

    primary_model: str

    fallback_models: list[str] = field(
        default_factory=list
    )

    retry_count: int = 2

    allow_provider_switch: bool = True



# =============================================================================
# Provider Availability State
# =============================================================================


@dataclass
class ProviderStatus:
    """
    Runtime provider availability.

    Used by failover engine.
    """

    provider: str

    available: bool = True

    response_time_ms: float = 0.0

    error_message: str = ""



# =============================================================================
# Model Failover Manager
# =============================================================================


class ModelFailoverManager:
    """
    Handles model and provider fallback.

    Responsibilities:

        - Maintain fallback chains
        - Check provider availability
        - Select backup models
        - Support runtime recovery

    """


    def __init__(
        self,
        registry: ModelRegistry | None = None,
    ) -> None:

        self.registry = (
            registry
            or MODEL_REGISTRY
        )


        self.rules: dict[
            str,
            ModelFallbackRule
        ] = {}


        self.providers: dict[
            str,
            ProviderStatus
        ] = {}


        self._load_default_rules()



    # -------------------------------------------------------------------------
    # Default Fallback Rules
    # -------------------------------------------------------------------------

    def _load_default_rules(
        self,
    ) -> None:
        """
        Register default fallback chains.
        """


        self.add_rule(

            ModelFallbackRule(

                primary_model="qwen3:4b",

                fallback_models=[

                    "llama3.1",

                    "gpt-4.1",

                    "gemini-2.5-pro",

                ],

            )

        )


        self.add_rule(

            ModelFallbackRule(

                primary_model="gpt-4.1",

                fallback_models=[

                    "gemini-2.5-pro",

                    "qwen3:4b",

                ],

            )

        )



    # -------------------------------------------------------------------------
    # Rule Management
    # -------------------------------------------------------------------------

    def add_rule(
        self,
        rule: ModelFallbackRule,
    ) -> None:
        """
        Add fallback rule.
        """

        self.rules[
            rule.primary_model
        ] = rule



    def get_fallback_models(
        self,
        model_name: str,
    ) -> list[str]:
        """
        Return fallback list.
        """

        rule = (
            self.rules.get(
                model_name
            )
        )


        if rule is None:

            return []


        return (
            rule.fallback_models
        )



    # -------------------------------------------------------------------------
    # Provider Tracking
    # -------------------------------------------------------------------------

    def update_provider_status(
        self,
        status: ProviderStatus,
    ) -> None:
        """
        Update provider availability.
        """

        self.providers[
            status.provider
        ] = status



    def is_provider_available(
        self,
        provider: str,
    ) -> bool:
        """
        Check provider status.
        """

        status = (
            self.providers.get(
                provider
            )
        )


        if status is None:

            return True


        return status.available



    # -------------------------------------------------------------------------
    # Model Recovery
    # -------------------------------------------------------------------------

    def find_available_model(
        self,
        failed_model: str,
    ) -> ModelConfig | None:
        """
        Find next available model.

        Algorithm:

        1. Check fallback chain
        2. Verify provider availability
        3. Return first match
        """


        candidates = [

            failed_model

        ] + self.get_fallback_models(
            failed_model
        )


        for model_name in candidates:

            model = (
                self.registry.get(
                    model_name
                )
            )


            if model is None:

                continue



            if self.is_provider_available(

                model.provider

            ):

                return model



        return None

# =============================================================================
# Model Usage Analytics
# =============================================================================


@dataclass
class ModelUsageRecord:
    """
    Stores runtime model usage information.
    """

    model_name: str

    total_requests: int = 0

    successful_requests: int = 0

    failed_requests: int = 0

    total_latency_ms: float = 0.0


    def record_success(
        self,
        latency_ms: float,
    ) -> None:
        """
        Record successful execution.
        """

        self.total_requests += 1

        self.successful_requests += 1

        self.total_latency_ms += latency_ms



    def record_failure(
        self,
    ) -> None:
        """
        Record failed execution.
        """

        self.total_requests += 1

        self.failed_requests += 1



    @property
    def success_rate(
        self,
    ) -> float:
        """
        Calculate success percentage.
        """

        if self.total_requests == 0:

            return 0.0


        return (
            self.successful_requests
            /
            self.total_requests
        )



    @property
    def average_latency(
        self,
    ) -> float:
        """
        Calculate average latency.
        """

        if self.successful_requests == 0:

            return 0.0


        return (
            self.total_latency_ms
            /
            self.successful_requests
        )



# =============================================================================
# Model Analytics Engine
# =============================================================================


class ModelAnalytics:
    """
    Tracks model execution behaviour.

    Used for adaptive model selection.

    """


    def __init__(
        self,
    ) -> None:

        self.records: dict[
            str,
            ModelUsageRecord
        ] = {}



    def _get_record(
        self,
        model_name: str,
    ) -> ModelUsageRecord:
        """
        Get or create model record.
        """

        if model_name not in self.records:

            self.records[
                model_name
            ] = ModelUsageRecord(
                model_name=model_name
            )


        return self.records[
            model_name
        ]



    def record_success(
        self,
        model_name: str,
        latency_ms: float,
    ) -> None:
        """
        Record successful model execution.
        """

        self._get_record(
            model_name
        ).record_success(
            latency_ms
        )



    def record_failure(
        self,
        model_name: str,
    ) -> None:
        """
        Record model failure.
        """

        self._get_record(
            model_name
        ).record_failure()



    def get_statistics(
        self,
        model_name: str,
    ) -> ModelUsageRecord | None:
        """
        Return model statistics.
        """

        return self.records.get(
            model_name
        )



    def export(
        self,
    ) -> dict[str, dict[str, Any]]:
        """
        Export analytics data.
        """

        return {

            name: {

                "requests":
                    record.total_requests,

                "success_rate":
                    record.success_rate,

                "average_latency":
                    record.average_latency,

            }

            for name, record
            in self.records.items()

        }



# =============================================================================
# Adaptive Model Ranking
# =============================================================================


class AdaptiveModelRanker:
    """
    Dynamically ranks models.

    Ranking factors:

        - Quality score
        - Success rate
        - Latency
        - Provider reliability

    """


    def __init__(
        self,
        analytics: ModelAnalytics,
    ) -> None:

        self.analytics = analytics



    def calculate_score(
        self,
        model: ModelConfig,
    ) -> float:
        """
        Calculate runtime model score.
        """


        usage = (
            self.analytics.get_statistics(
                model.name
            )
        )


        quality = model.metadata.get(

            "quality_score",

            0.5,

        )


        speed = model.metadata.get(

            "speed_score",

            0.5,

        )


        reliability = (

            usage.success_rate

            if usage

            else 0.5

        )


        latency_factor = 1.0


        if usage and usage.average_latency:

            latency_factor = (

                1
                /
                (
                    1
                    +
                    usage.average_latency
                    /
                    10000
                )

            )



        return (

            quality * 0.45

            +

            reliability * 0.30

            +

            speed * 0.15

            +

            latency_factor * 0.10

        )



    def rank(
        self,
        models: list[ModelConfig],
    ) -> list[ModelConfig]:
        """
        Return models sorted by adaptive score.
        """

        return sorted(

            models,

            key=self.calculate_score,

            reverse=True,

        )

# =============================================================================
# Model Analytics Persistence
# =============================================================================


class ModelAnalyticsManager:
    """
    Persistence manager for model analytics.

    Responsibilities:

        - Export analytics
        - Restore analytics
        - Generate health reports
        - Provide runtime metrics
    """


    def __init__(
        self,
        analytics: ModelAnalytics | None = None,
    ) -> None:

        self.analytics = (
            analytics
            or ModelAnalytics()
        )



    # -------------------------------------------------------------------------
    # Export Analytics
    # -------------------------------------------------------------------------

    def export(
        self,
    ) -> dict[str, Any]:
        """
        Export analytics data.
        """

        return (
            self.analytics.export()
        )



    # -------------------------------------------------------------------------
    # Import Analytics
    # -------------------------------------------------------------------------

    def import_data(
        self,
        data: dict[str, Any],
    ) -> None:
        """
        Restore analytics data.

        Parameters
        ----------
        data:
            Analytics dictionary.
        """

        if not isinstance(
            data,
            dict,
        ):

            raise TypeError(
                "Analytics data must be dictionary."
            )


        for model_name, values in (
            data.items()
        ):

            record = ModelUsageRecord(

                model_name=model_name,

                total_requests=(
                    values.get(
                        "requests",
                        0,
                    )
                ),

            )


            self.analytics.records[
                model_name
            ] = record



    # -------------------------------------------------------------------------
    # Health Report
    # -------------------------------------------------------------------------

    def generate_health_report(
        self,
    ) -> dict[str, Any]:
        """
        Generate model health report.
        """

        report = {}


        for name, record in (
            self.analytics.records.items()
        ):

            status = "healthy"


            if record.success_rate < 0.5:

                status = "unstable"


            if record.success_rate == 0:

                status = "failed"



            report[name] = {

                "status": status,

                "requests":
                    record.total_requests,

                "success_rate":
                    record.success_rate,

                "average_latency_ms":
                    record.average_latency,

            }


        return report



# =============================================================================
# LLMService Integration Helpers
# =============================================================================


class RuntimeModelContext:
    """
    Runtime context passed to LLM services.

    Keeps model selection information together.
    """


    def __init__(
        self,
        model: ModelConfig,
    ) -> None:

        self.model = model

        self.started_at = None

        self.metadata: dict[str, Any] = {}



    def start(
        self,
    ) -> None:
        """
        Mark execution start.
        """

        import time

        self.started_at = (
            time.time()
        )



    def finish(
        self,
    ) -> float:
        """
        Return execution duration.

        Returns
        -------
        float
            Duration milliseconds.
        """

        import time


        if self.started_at is None:

            return 0.0


        return (

            time.time()
            -
            self.started_at

        ) * 1000



# =============================================================================
# Runtime Model Manager
# =============================================================================


class RuntimeModelManager:
    """
    High-level runtime model controller.

    Connects:

        ModelRegistry
        ModelSelector
        Analytics
        Failover

    """


    def __init__(
        self,
        registry: ModelRegistry | None = None,
    ) -> None:

        self.registry = (
            registry
            or MODEL_REGISTRY
        )


        self.analytics = (
            ModelAnalytics()
        )


        self.selector = (
            AdaptiveModelRanker(
                self.analytics
            )
        )


        self.failover = (
            ModelFailoverManager(
                self.registry
            )
        )



    # -------------------------------------------------------------------------
    # Select Model
    # -------------------------------------------------------------------------

    def select_model(
        self,
        candidates: list[str],
    ) -> ModelConfig | None:
        """
        Select best runtime model.
        """

        models = [

            self.registry.get(
                name
            )

            for name in candidates

        ]


        models = [

            model

            for model in models

            if model is not None

        ]


        if not models:

            return None



        ranked = (
            self.selector.rank(
                models
            )
        )


        return ranked[0]



    # -------------------------------------------------------------------------
    # Record Execution
    # -------------------------------------------------------------------------

    def record_execution(
        self,
        model_name: str,
        success: bool,
        latency_ms: float = 0.0,
    ) -> None:
        """
        Record model execution result.
        """

        if success:

            self.analytics.record_success(

                model_name,

                latency_ms,

            )

        else:

            self.analytics.record_failure(

                model_name

            )

# =============================================================================
# Global Runtime Model Manager
# =============================================================================


RUNTIME_MODEL_MANAGER = RuntimeModelManager()



# =============================================================================
# Convenience Model APIs
# =============================================================================


def get_runtime_model(
    candidates: list[str],
) -> ModelConfig | None:
    """
    Select best runtime model from candidates.

    Parameters
    ----------
    candidates:
        Available model names.

    Returns
    -------
    ModelConfig | None
        Selected model.
    """

    return (
        RUNTIME_MODEL_MANAGER
        .select_model(
            candidates
        )
    )



def record_model_execution(
    model_name: str,
    success: bool,
    latency_ms: float = 0.0,
) -> None:
    """
    Record model execution result.

    Used by LLMService.
    """

    RUNTIME_MODEL_MANAGER.record_execution(

        model_name,

        success,

        latency_ms,

    )



def get_model_health_report(
) -> dict[str, Any]:
    """
    Return runtime model health.

    Returns
    -------
    dict[str, Any]
        Health information.
    """

    manager = ModelAnalyticsManager(

        RUNTIME_MODEL_MANAGER.analytics

    )


    return (
        manager.generate_health_report()
    )



# =============================================================================
# Model Capability Helpers
# =============================================================================


def model_supports_vision(
    model_name: str,
) -> bool:
    """
    Check vision capability.
    """

    model = (
        get_model_config(
            model_name
        )
    )


    if model is None:

        return False


    return (
        model.supports_vision
    )



def model_supports_tools(
    model_name: str,
) -> bool:
    """
    Check tool calling capability.
    """

    model = (
        get_model_config(
            model_name
        )
    )


    if model is None:

        return False


    return (
        model.supports_tools
    )



def get_models_for_provider(
    provider: str,
) -> list[ModelConfig]:
    """
    Return models for provider.
    """

    return (
        MODEL_REGISTRY
        .get_by_provider(
            provider
        )
    )



# =============================================================================
# Backward Compatibility Aliases
# =============================================================================


def get_available_models(
) -> list[str]:
    """
    Deprecated alias.

    Use:
        list_available_models()
    """

    logger.warning(

        "get_available_models() is deprecated. "

        "Use list_available_models()."

    )


    return (
        list_available_models()
    )



def get_model(
    model_name: str,
) -> ModelConfig | None:
    """
    Deprecated alias.

    Use:
        get_model_config()
    """

    logger.warning(

        "get_model() is deprecated. "

        "Use get_model_config()."

    )


    return (
        get_model_config(
            model_name
        )
    )



# =============================================================================
# Module Public API
# =============================================================================


__all__ = [

    # Core Models

    "ModelConfig",

    "ModelRegistry",

    "ModelProfile",

    "ModelPerformance",

    "ModelCost",


    # Registry

    "MODEL_REGISTRY",

    "get_model_config",

    "list_available_models",

    "register_model",


    # Selection

    "ModelSelector",

    "HardwareProfile",

    "HardwareAwareModelSelector",

    "ModelSelectionPolicy",


    # Failover

    "ModelFallbackRule",

    "ProviderStatus",

    "ModelFailoverManager",


    # Analytics

    "ModelUsageRecord",

    "ModelAnalytics",

    "AdaptiveModelRanker",

    "ModelAnalyticsManager",


    # Runtime

    "RuntimeModelContext",

    "RuntimeModelManager",

    "RUNTIME_MODEL_MANAGER",


    # Helpers

    "get_runtime_model",

    "record_model_execution",

    "get_model_health_report",

    "model_supports_vision",

    "model_supports_tools",

    "get_models_for_provider",


]

# =============================================================================
# Model Configuration Integrity Validation
# =============================================================================


def validate_model_registry(
) -> tuple[bool, list[str]]:
    """
    Validate complete model registry.

    Checks:
        - duplicate names
        - invalid configurations
        - missing providers
        - invalid metadata

    Returns
    -------
    tuple[bool, list[str]]
        Validation status and errors.
    """

    errors: list[str] = []


    models = (
        MODEL_REGISTRY._models
    )


    if not models:

        errors.append(
            "Model registry is empty."
        )


    for name, model in models.items():

        valid, message = (
            model.validate()
        )


        if not valid:

            errors.append(
                f"{name}: {message}"
            )


        if (
            model.provider
            is None
            or
            not model.provider
        ):

            errors.append(
                f"{name}: missing provider."
            )


    return (
        len(errors) == 0,
        errors,
    )



# =============================================================================
# Default Model Metadata Enhancement
# =============================================================================


def enrich_model_metadata(
) -> None:
    """
    Add default performance metadata.

    Used when explicit benchmark
    information is unavailable.
    """

    defaults = {

        "qwen3:4b": {

            "quality_score": 0.65,

            "speed_score": 0.85,

            "memory_requirement_gb": 6,

        },


        "llama3.1": {

            "quality_score": 0.75,

            "speed_score": 0.65,

            "memory_requirement_gb": 8,

        },


        "gpt-4.1": {

            "quality_score": 0.95,

            "speed_score": 0.75,

            "memory_requirement_gb": 0,

        },


        "gemini-2.5-pro": {

            "quality_score": 0.98,

            "speed_score": 0.80,

            "memory_requirement_gb": 0,

        },

    }



    for model_name, metadata in defaults.items():

        model = (
            MODEL_REGISTRY.get(
                model_name
            )
        )


        if model:

            model.metadata.update(
                metadata
            )



# Initialize metadata

enrich_model_metadata()



# =============================================================================
# Production Readiness Check
# =============================================================================


def run_model_system_check(
) -> dict[str, Any]:
    """
    Run complete model subsystem check.

    Returns
    -------
    dict[str, Any]
        Diagnostic report.
    """

    valid, errors = (
        validate_model_registry()
    )


    return {

        "status":
            (
                "READY"
                if valid
                else "ERROR"
            ),


        "registered_models":
            len(
                MODEL_REGISTRY.list_models()
            ),


        "models":
            MODEL_REGISTRY.list_models(),


        "errors":
            errors,


        "runtime_manager":
            isinstance(
                RUNTIME_MODEL_MANAGER,
                RuntimeModelManager,
            ),

    }



# =============================================================================
# Configuration Debug Export
# =============================================================================


def export_model_system_state(
) -> dict[str, Any]:
    """
    Export complete model subsystem state.

    Useful for:
        - debugging
        - support reports
        - diagnostics
    """

    return {

        "registry":

            MODEL_REGISTRY.export(),


        "health":

            get_model_health_report(),


        "system_check":

            run_model_system_check(),

    }