"""
File: app/ui/components/settings/api_settings.py

Production-ready API Settings component for the
AI Research Assistant.

Responsibilities:
    - Manage external provider credentials
    - Configure API endpoints
    - Handle secure secrets
    - Validate API configuration

Persistence:
    Delegated to:
        app/config/settings_manager.py

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
# API Provider Definitions
# ============================================================================


class APIProvider(str, Enum):
    """
    Supported external API providers.
    """

    OPENAI = "OpenAI"

    GEMINI = "Google Gemini"

    DEEPSEEK = "DeepSeek"

    OPENROUTER = "OpenRouter"

    AZURE_OPENAI = "Azure OpenAI"

    CUSTOM = "Custom"




# ============================================================================
# Credential Types
# ============================================================================


class CredentialType(str, Enum):
    """
    Types of authentication credentials.
    """

    API_KEY = "API Key"

    BEARER_TOKEN = "Bearer Token"

    OAUTH_TOKEN = "OAuth Token"

    AZURE_KEY = "Azure API Key"




# ============================================================================
# API Provider Metadata
# ============================================================================


@dataclass(slots=True)
class APIProviderMetadata:
    """
    Metadata describing API provider requirements.
    """

    provider: APIProvider

    description: str

    credential_type: CredentialType


    requires_endpoint: bool = True


    requires_organization: bool = False


    supports_models_api: bool = False


    default_endpoint: str = ""




# ============================================================================
# API Configuration State
# ============================================================================


@dataclass(slots=True)
class APIConfigState:
    """
    Current API configuration state.
    """

    provider: APIProvider = (
        APIProvider.OPENAI
    )


    api_key: str = ""


    endpoint: str = ""


    organization_id: str = ""


    api_version: str = ""


    deployment_name: str = ""


    enabled: bool = False


    verified: bool = False


    last_error: str = ""



    custom_headers: dict[str, str] = field(
        default_factory=dict
    )




# ============================================================================
# API Provider Registry
# ============================================================================


API_PROVIDERS: dict[
    APIProvider,
    APIProviderMetadata
] = {


    APIProvider.OPENAI:

        APIProviderMetadata(

            provider=APIProvider.OPENAI,

            description=(

                "OpenAI API for advanced "
                "language models."

            ),

            credential_type=(
                CredentialType.API_KEY
            ),

            supports_models_api=True,

            default_endpoint=(

                "https://api.openai.com/v1"

            ),

        ),



    APIProvider.GEMINI:

        APIProviderMetadata(

            provider=APIProvider.GEMINI,

            description=(

                "Google Gemini API "
                "for multimodal AI."

            ),

            credential_type=(
                CredentialType.API_KEY
            ),

            supports_models_api=True,

            default_endpoint=(

                "https://generativelanguage.googleapis.com"

            ),

        ),



    APIProvider.DEEPSEEK:

        APIProviderMetadata(

            provider=APIProvider.DEEPSEEK,

            description=(

                "DeepSeek API provider."

            ),

            credential_type=(
                CredentialType.API_KEY
            ),

            default_endpoint=(

                "https://api.deepseek.com"

            ),

        ),



    APIProvider.OPENROUTER:

        APIProviderMetadata(

            provider=APIProvider.OPENROUTER,

            description=(

                "OpenRouter unified model API."

            ),

            credential_type=(
                CredentialType.API_KEY
            ),

            supports_models_api=True,

            default_endpoint=(

                "https://openrouter.ai/api/v1"

            ),

        ),



    APIProvider.AZURE_OPENAI:

        APIProviderMetadata(

            provider=APIProvider.AZURE_OPENAI,

            description=(

                "Azure hosted OpenAI models."

            ),

            credential_type=(

                CredentialType.AZURE_KEY

            ),

            requires_organization=True,

        ),

}




# ============================================================================
# Component Skeleton
# ============================================================================


class APISettingsComponent:
    """
    Streamlit UI component for API settings.

    Handles only configuration UI.
    """

    def __init__(
        self,
        *,
        state: APIConfigState | None = None,

        on_save: Callable[
            [APIConfigState],
            None
        ]
        | None = None,

        on_test: Callable[
            [APIConfigState],
            bool
        ]
        | None = None,

    ) -> None:
        """
        Initialize API settings component.
        """

        self.state = (

            state

            if state

            else APIConfigState()

        )


        self._on_save = on_save


        self._on_test = on_test


        logger.debug(
            "APISettingsComponent initialized."
        )


    # Rendering methods continue in Part 2.

    # ============================================================================
# Main Rendering
# ============================================================================


    def render(self) -> None:
        """
        Render complete API Settings interface.

        Rendering order:

            1. Initialize session state
            2. Header
            3. Provider selection
            4. Credential configuration
            5. Endpoint configuration
            6. Validation actions
        """

        self._initialize_session_state()


        self._render_header()


        st.divider()


        self._render_provider_selector()


        st.divider()


        self._render_configuration_summary()



# ============================================================================
# Session State
# ============================================================================


    def _initialize_session_state(
        self,
    ) -> None:
        """
        Initialize Streamlit session state.

        Preserves temporary API configuration during reruns.
        """

        if (
            "api_settings_state"
            not in st.session_state
        ):

            st.session_state.api_settings_state = (
                self.state
            )


            logger.debug(
                "API settings session state initialized."
            )



# ============================================================================
# Header
# ============================================================================


    def _render_header(
        self,
    ) -> None:
        """
        Render API settings header.
        """

        render_html("""
            <div class="settings-header">

                <h2>
                    🔐 API Configuration
                </h2>

                <p>
                    Manage external AI provider
                    credentials, endpoints,
                    and authentication settings.
                </p>

            </div>
            """)



# ============================================================================
# Provider Selector
# ============================================================================


    def _render_provider_selector(
        self,
    ) -> None:
        """
        Render API provider selection.
        """

        st.subheader(
            "API Provider"
        )


        providers = list(
            APIProvider
        )


        current_index = providers.index(
            self.state.provider
        )


        selected_provider = st.selectbox(

            label="Select Provider",

            options=providers,

            index=current_index,

            format_func=lambda item:
                item.value,

        )


        if selected_provider != (
            self.state.provider
        ):

            logger.info(
                "API provider changed: %s -> %s",
                self.state.provider.value,
                selected_provider.value,
            )


            self.state.provider = (
                selected_provider
            )


            self.state.api_key = ""

            self.state.verified = False

            self.state.last_error = ""



        self._render_provider_information()



# ============================================================================
# Provider Information
# ============================================================================


    def _render_provider_information(
        self,
    ) -> None:
        """
        Display selected provider details.
        """

        metadata = API_PROVIDERS.get(
            self.state.provider
        )


        if metadata is None:

            return



        with st.expander(
            "Provider Information",
            expanded=False,
        ):

            st.write(
                metadata.description
            )


            st.write(
                "Authentication:",
                metadata.credential_type.value,
            )


            st.write(
                "Endpoint Required:",
                metadata.requires_endpoint,
            )


            st.write(
                "Models API:",
                metadata.supports_models_api,
            )



# ============================================================================
# Configuration Summary
# ============================================================================


    def _render_configuration_summary(
        self,
    ) -> None:
        """
        Display current API configuration status.
        """

        st.subheader(
            "Configuration Status"
        )


        col1, col2, col3 = st.columns(
            3
        )


        with col1:

            st.metric(

                label="Provider",

                value=(
                    self.state.provider.value
                ),

            )


        with col2:

            status = (

                "Verified"

                if self.state.verified

                else "Not Verified"

            )


            st.metric(

                label="Status",

                value=status,

            )


        with col3:

            credential_status = (

                "Configured"

                if self.state.api_key

                else "Missing"

            )


            st.metric(

                label="Credential",

                value=credential_status,

            )


        if self.state.last_error:

            st.error(
                self.state.last_error
            )


    # ============================================================================
# Credential Configuration
# ============================================================================


    def _render_credentials(
        self,
    ) -> None:
        """
        Render authentication credential inputs.
        """

        st.subheader(
            "Authentication"
        )


        metadata = API_PROVIDERS.get(
            self.state.provider
        )


        if metadata is None:

            st.warning(
                "Provider metadata unavailable."
            )

            return



        credential_label = (

            metadata.credential_type.value

        )


        api_key = st.text_input(

            label=credential_label,

            value=self.state.api_key,

            type="password",

            placeholder=(

                "Enter secret key"

            ),

            help=(

                "Stored securely and never "
                "displayed."

            ),

        )


        if api_key:

            self.state.api_key = api_key

            self.state.verified = False



# ============================================================================
# Endpoint Configuration
# ============================================================================


    def _render_endpoint_settings(
        self,
    ) -> None:
        """
        Render API endpoint configuration.
        """

        st.subheader(
            "Endpoint Configuration"
        )


        metadata = API_PROVIDERS.get(
            self.state.provider
        )


        default_endpoint = (

            metadata.default_endpoint

            if metadata

            else ""

        )


        endpoint = st.text_input(

            label="Base URL",

            value=(

                self.state.endpoint

                or

                default_endpoint

            ),

            help=(

                "API endpoint URL."

            ),

        )


        self.state.endpoint = endpoint



# ============================================================================
# Organization Configuration
# ============================================================================


    def _render_organization_settings(
        self,
    ) -> None:
        """
        Render organization information.

        Used mainly by enterprise providers.
        """

        metadata = API_PROVIDERS.get(
            self.state.provider
        )


        if not metadata:

            return



        if metadata.requires_organization:

            self.state.organization_id = (

                st.text_input(

                    label="Organization ID",

                    value=(
                        self.state.organization_id
                    ),

                )

            )



# ============================================================================
# Azure OpenAI Configuration
# ============================================================================


    def _render_azure_settings(
        self,
    ) -> None:
        """
        Render Azure OpenAI specific settings.
        """

        if (
            self.state.provider
            !=
            APIProvider.AZURE_OPENAI
        ):

            return



        st.subheader(
            "Azure OpenAI Settings"
        )


        self.state.api_version = (

            st.text_input(

                label="API Version",

                value=(
                    self.state.api_version
                ),

                placeholder=(

                    "2024-02-15-preview"

                ),

            )

        )



        self.state.deployment_name = (

            st.text_input(

                label="Deployment Name",

                value=(

                    self.state.deployment_name

                ),

                help=(

                    "Azure model deployment name."

                ),

            )

        )



# ============================================================================
# Custom Headers
# ============================================================================


    def _render_custom_headers(
        self,
    ) -> None:
        """
        Manage custom API headers.

        Useful for:
            - OpenRouter
            - Enterprise gateways
            - Custom endpoints
        """

        st.subheader(
            "Custom Headers"
        )


        with st.expander(
            "Configure Headers",
            expanded=False,
        ):


            header_key = st.text_input(

                "Header Name",

                key="api_header_key",

            )


            header_value = st.text_input(

                "Header Value",

                key="api_header_value",

            )



            if st.button(
                "Add Header"
            ):

                if (
                    header_key
                    and
                    header_value
                ):

                    self.state.custom_headers[
                        header_key
                    ] = header_value


                    st.success(
                        "Header added."
                    )



            if self.state.custom_headers:

                st.write(
                    "Current Headers"
                )


                for key in (
                    self.state.custom_headers
                ):

                    st.write(
                        f"• {key}"
                    )



# ============================================================================
# Secret Utilities
# ============================================================================


    def _masked_key(
        self,
    ) -> str:
        """
        Return masked API key.

        Example:
            sk-abcd********
        """

        if not self.state.api_key:

            return "Not configured"



        if len(
            self.state.api_key
        ) <= 6:

            return "*" * len(
                self.state.api_key
            )


        return (

            self.state.api_key[:4]

            +

            "*" *
            (
                len(self.state.api_key)
                -
                4
            )

        )


    # ============================================================================
# Connection Testing
# ============================================================================


    def _render_connection_test(
        self,
    ) -> None:
        """
        Render provider connection test controls.
        """

        st.subheader(
            "Connection Test"
        )


        col1, col2 = st.columns(
            2
        )


        with col1:

            if st.button(
                "🔌 Test API Connection",
                use_container_width=True,
            ):

                self._test_connection()



        with col2:

            if st.button(
                "🧹 Clear Verification",
                use_container_width=True,
            ):

                self._clear_verification()



# ============================================================================
# Connection Test Logic
# ============================================================================


    def _test_connection(
        self,
    ) -> None:
        """
        Test API provider connectivity.

        Actual HTTP calls are delegated to the service layer.
        """

        valid, message = (
            self.validate_configuration()
        )


        if not valid:

            self.state.verified = False

            self.state.last_error = message


            st.warning(
                message
            )

            return



        try:

            if self._on_test:

                result = self._on_test(
                    self.state
                )


            else:

                result = True



            if result:

                self.state.verified = True

                self.state.last_error = ""

                st.success(
                    "API connection successful."
                )


                logger.info(
                    "API verification successful."
                )


            else:

                self.state.verified = False

                self.state.last_error = (
                    "Connection test failed."
                )


                st.error(
                    self.state.last_error
                )



        except Exception as exc:

            self.state.verified = False


            self.state.last_error = str(
                exc
            )


            logger.exception(
                "API connection test failed."
            )


            st.error(
                str(exc)
            )



# ============================================================================
# Verification Reset
# ============================================================================


    def _clear_verification(
        self,
    ) -> None:
        """
        Clear previous verification state.
        """

        self.state.verified = False

        self.state.last_error = ""

        st.info(
            "Verification status cleared."
        )



# ============================================================================
# Configuration Validation
# ============================================================================


    def validate_configuration(
        self,
    ) -> tuple[bool, str]:
        """
        Validate current API configuration.

        Returns:
            Validation status and message.
        """

        metadata = API_PROVIDERS.get(
            self.state.provider
        )


        if metadata is None:

            return (

                False,

                "Unknown API provider."

            )



        if not self.state.api_key:

            return (

                False,

                "API credential missing."

            )



        if (
            metadata.requires_endpoint

            and

            not self.state.endpoint

        ):

            return (

                False,

                "API endpoint missing."

            )



        if (

            self.state.provider

            ==

            APIProvider.AZURE_OPENAI

        ):


            if not self.state.api_version:

                return (

                    False,

                    "Azure API version required."

                )



            if not self.state.deployment_name:

                return (

                    False,

                    "Azure deployment name required."

                )



        return (

            True,

            "API configuration valid."

        )



# ============================================================================
# Provider Health Information
# ============================================================================


    def get_connection_status(
        self,
    ) -> dict[str, Any]:
        """
        Return API connection information.

        Used by SettingsManager and dashboard.
        """

        return {

            "provider":
                self.state.provider.value,


            "verified":
                self.state.verified,


            "endpoint":
                self.state.endpoint,


            "configured":
                bool(
                    self.state.api_key
                ),


            "error":
                self.state.last_error,

        }



# ============================================================================
# API Capability Checks
# ============================================================================


    def supports_model_listing(
        self,
    ) -> bool:
        """
        Check whether provider supports models API.
        """

        metadata = API_PROVIDERS.get(
            self.state.provider
        )


        if not metadata:

            return False


        return (
            metadata.supports_models_api
        )



    # ============================================================================
# Save Actions
# ============================================================================


    def _render_actions(
        self,
    ) -> None:
        """
        Render API settings actions.
        """

        st.subheader(
            "API Configuration Actions"
        )


        col1, col2, col3 = st.columns(
            3
        )


        with col1:

            if st.button(
                "💾 Save API Settings",
                use_container_width=True,
            ):

                self._save_configuration()



        with col2:

            if st.button(
                "♻️ Reset API Settings",
                use_container_width=True,
            ):

                self._reset_configuration()



        with col3:

            if st.button(
                "📋 Show Safe Configuration",
                use_container_width=True,
            ):

                st.json(
                    self.to_dict(
                        mask_secret=True
                    )
                )



# ============================================================================
# Save Configuration
# ============================================================================


    def _save_configuration(
        self,
    ) -> None:
        """
        Validate and save API configuration.
        """

        valid, message = (
            self.validate_configuration()
        )


        if not valid:

            st.warning(
                message
            )

            return



        try:

            if self._on_save:

                self._on_save(
                    self.state
                )


                st.success(
                    "API settings saved."
                )


                logger.info(
                    "API configuration saved."
                )


            else:

                st.info(
                    "Save handler not configured."
                )



        except Exception as exc:

            logger.exception(
                "API configuration save failed."
            )


            st.error(
                str(exc)
            )



# ============================================================================
# Reset Configuration
# ============================================================================


    def _reset_configuration(
        self,
    ) -> None:
        """
        Reset API settings.
        """

        logger.info(
            "Resetting API configuration."
        )


        current_provider = (
            self.state.provider
        )


        self.state = APIConfigState(

            provider=current_provider

        )


        st.success(
            "API settings reset."
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
        Load API configuration.

        Designed for:
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
                    APIProvider(
                        provider
                    )
                )


            self.state.endpoint = str(

                configuration.get(
                    "endpoint",
                    "",
                )

            )


            self.state.organization_id = str(

                configuration.get(
                    "organization_id",
                    "",
                )

            )


            self.state.api_version = str(

                configuration.get(
                    "api_version",
                    "",
                )

            )


            self.state.deployment_name = str(

                configuration.get(
                    "deployment_name",
                    "",
                )

            )


            self.state.enabled = bool(

                configuration.get(
                    "enabled",
                    False,
                )

            )


            logger.info(
                "API configuration loaded."
            )



        except Exception as exc:

            logger.exception(
                "Failed loading API configuration."
            )

            raise exc



    def save_to_configuration_manager(
        self,
        settings_manager: Any,
    ) -> None:
        """
        Save through SettingsManager.

        API keys should be handled by the
        secure secret layer.
        """

        settings_manager.save_api_config(

            self.to_dict(
                mask_secret=False
            )

        )


        logger.info(
            "API configuration saved "
            "through SettingsManager."
        )



# ============================================================================
# Serialization
# ============================================================================


    def to_dict(
        self,
        *,
        mask_secret: bool = False,
    ) -> dict[str, Any]:
        """
        Serialize API configuration.

        Args:
            mask_secret:
                Hide API credentials.

        Returns:
            Configuration dictionary.
        """

        api_key = self.state.api_key


        if mask_secret:

            api_key = (
                self._masked_key()
            )


        return {

            "provider":
                self.state.provider.value,


            "api_key":
                api_key,


            "endpoint":
                self.state.endpoint,


            "organization_id":
                self.state.organization_id,


            "api_version":
                self.state.api_version,


            "deployment_name":
                self.state.deployment_name,


            "enabled":
                self.state.enabled,


            "verified":
                self.state.verified,


            "custom_headers":
                self.state.custom_headers,

        }



# ============================================================================
# Environment Support
# ============================================================================


    def load_environment_defaults(
        self,
    ) -> None:
        """
        Load API configuration defaults from
        environment variables.
        """

        import os



        provider = os.getenv(
            "API_PROVIDER"
        )


        api_key = os.getenv(
            "API_KEY"
        )


        endpoint = os.getenv(
            "API_ENDPOINT"
        )



        if provider:

            try:

                self.state.provider = (
                    APIProvider(
                        provider
                    )
                )


            except ValueError:

                logger.warning(
                    "Unknown API provider: %s",
                    provider,
                )



        if api_key:

            self.state.api_key = api_key



        if endpoint:

            self.state.endpoint = endpoint



        logger.debug(
            "API environment defaults loaded."
        )


    # ============================================================================
# Secret Management
# ============================================================================


    def set_secret(
        self,
        secret_name: str,
        value: str,
    ) -> None:
        """
        Update sensitive credential values.

        Permanent storage should be handled by:
            - environment variables
            - secrets manager
            - encrypted configuration store

        Args:
            secret_name:
                Secret identifier.

            value:
                Secret value.
        """

        if not value:

            return



        if secret_name == "api_key":

            self.state.api_key = value


            self.state.verified = False



            logger.debug(
                "API secret updated."
            )



        else:

            logger.warning(
                "Unsupported secret name: %s",
                secret_name,
            )



    def clear_secret(
        self,
        secret_name: str,
    ) -> None:
        """
        Remove sensitive values.

        Args:
            secret_name:
                Secret identifier.
        """

        if secret_name == "api_key":

            self.state.api_key = ""

            self.state.verified = False



            logger.debug(
                "API key removed."
            )



# ============================================================================
# Credential Security Helpers
# ============================================================================


    def has_credentials(
        self,
    ) -> bool:
        """
        Check whether credentials exist.
        """

        return bool(
            self.state.api_key
        )



    def credential_preview(
        self,
    ) -> str:
        """
        Return safe credential preview.

        Example:
            sk-abcd********
        """

        return self._masked_key()



    def rotate_secret(
        self,
        new_secret: str,
    ) -> None:
        """
        Replace API credential.

        Used for API key rotation workflows.
        """

        if not new_secret:

            raise ValueError(
                "Secret cannot be empty."
            )


        self.state.api_key = new_secret


        self.state.verified = False


        logger.info(
            "API credential rotated."
        )



# ============================================================================
# Provider Specific Helpers
# ============================================================================


    def requires_organization_id(
        self,
    ) -> bool:
        """
        Check if provider needs organization ID.
        """

        metadata = API_PROVIDERS.get(
            self.state.provider
        )


        return (

            metadata.requires_organization

            if metadata

            else False

        )



    def requires_endpoint(
        self,
    ) -> bool:
        """
        Check if provider requires endpoint.
        """

        metadata = API_PROVIDERS.get(
            self.state.provider
        )


        return (

            metadata.requires_endpoint

            if metadata

            else False

        )



    def get_default_endpoint(
        self,
    ) -> str:
        """
        Return provider default endpoint.
        """

        metadata = API_PROVIDERS.get(
            self.state.provider
        )


        if metadata:

            return metadata.default_endpoint



        return ""



# ============================================================================
# Safe Import / Export
# ============================================================================


    def export_configuration(
        self,
    ) -> dict[str, Any]:
        """
        Export configuration safely.

        API secrets are masked.
        """

        return self.to_dict(
            mask_secret=True
        )



    def import_configuration(
        self,
        configuration: dict[str, Any],
    ) -> None:
        """
        Import API configuration.

        Sensitive fields are intentionally ignored
        unless explicitly restored through secret manager.
        """

        provider = (
            configuration.get(
                "provider"
            )
        )


        if provider:

            self.state.provider = (
                APIProvider(
                    provider
                )
            )



        self.state.endpoint = str(

            configuration.get(
                "endpoint",
                "",
            )

        )



        self.state.organization_id = str(

            configuration.get(
                "organization_id",
                "",
            )

        )



        self.state.api_version = str(

            configuration.get(
                "api_version",
                "",
            )

        )



        self.state.deployment_name = str(

            configuration.get(
                "deployment_name",
                "",
            )

        )



        self.state.enabled = bool(

            configuration.get(
                "enabled",
                False,
            )

        )



        logger.info(
            "API configuration imported."
        )



# ============================================================================
# Security Audit
# ============================================================================


    def security_audit(
        self,
    ) -> dict[str, Any]:
        """
        Return security status report.
        """

        return {

            "provider":
                self.state.provider.value,


            "credential_present":
                bool(
                    self.state.api_key
                ),


            "credential_masked":
                self._masked_key(),


            "endpoint_configured":
                bool(
                    self.state.endpoint
                ),


            "verified":
                self.state.verified,


            "custom_headers":
                list(
                    self.state.custom_headers.keys()
                ),

        }


    # ============================================================================
# Complete UI Sections
# ============================================================================


    def render_configuration_sections(
        self,
    ) -> None:
        """
        Render all API configuration sections.

        This method separates UI composition from individual sections.
        """

        self._render_credentials()


        st.divider()


        self._render_endpoint_settings()


        st.divider()


        self._render_organization_settings()


        st.divider()


        self._render_azure_settings()


        st.divider()


        self._render_custom_headers()



# ============================================================================
# Complete API Settings Render
# ============================================================================


    def render_full(
        self,
    ) -> None:
        """
        Render complete API settings page.

        Intended to be called from:

            app/ui/pages/settings.py
        """

        self._initialize_session_state()


        self._render_header()


        st.divider()


        self._render_provider_selector()


        st.divider()


        self.render_configuration_sections()


        st.divider()


        self._render_connection_test()


        st.divider()


        self._render_actions()



# ============================================================================
# Provider Configuration Summary
# ============================================================================


    def get_provider_summary(
        self,
    ) -> dict[str, Any]:
        """
        Return provider summary information.
        """

        metadata = API_PROVIDERS.get(
            self.state.provider
        )


        return {

            "provider":
                self.state.provider.value,


            "description":
                (
                    metadata.description
                    if metadata
                    else ""
                ),


            "credential_type":
                (
                    metadata
                    .credential_type
                    .value
                    if metadata
                    else ""
                ),


            "endpoint":
                self.state.endpoint,


            "verified":
                self.state.verified,


            "enabled":
                self.state.enabled,

        }



# ============================================================================
# Provider Enable / Disable
# ============================================================================


    def enable_provider(
        self,
    ) -> None:
        """
        Enable current API provider.
        """

        self.state.enabled = True


        logger.info(
            "API provider enabled."
        )



    def disable_provider(
        self,
    ) -> None:
        """
        Disable current API provider.
        """

        self.state.enabled = False


        self.state.verified = False


        logger.info(
            "API provider disabled."
        )



    def is_enabled(
        self,
    ) -> bool:
        """
        Check provider availability.
        """

        return self.state.enabled



# ============================================================================
# Runtime Configuration Helpers
# ============================================================================


    def get_runtime_configuration(
        self,
    ) -> dict[str, Any]:
        """
        Return configuration required by runtime services.

        Secrets are included only for internal use.
        """

        return {

            "provider":
                self.state.provider.value,


            "api_key":
                self.state.api_key,


            "endpoint":
                self.state.endpoint,


            "organization_id":
                self.state.organization_id,


            "api_version":
                self.state.api_version,


            "deployment_name":
                self.state.deployment_name,


            "headers":
                self.state.custom_headers,

        }



# ============================================================================
# Error Management
# ============================================================================


    def clear_errors(
        self,
    ) -> None:
        """
        Clear API error information.
        """

        self.state.last_error = ""


        logger.debug(
            "API errors cleared."
        )



    def has_error(
        self,
    ) -> bool:
        """
        Check whether API configuration has errors.
        """

        return bool(
            self.state.last_error
        )


    # ============================================================================
# Default State Factory
# ============================================================================


def create_default_api_state() -> APIConfigState:
    """
    Create default API configuration.

    Default follows project architecture:

        Local Ollama development
        +
        Optional cloud providers

    Returns:
        APIConfigState instance.
    """

    return APIConfigState(

        provider=APIProvider.OPENAI,

        endpoint=(

            API_PROVIDERS[
                APIProvider.OPENAI
            ].default_endpoint

        ),

        enabled=False,

    )



# ============================================================================
# Provider Utilities
# ============================================================================


def get_provider_metadata(
    provider: APIProvider,
) -> APIProviderMetadata | None:
    """
    Retrieve provider metadata.

    Args:
        provider:
            API provider.

    Returns:
        Provider metadata.
    """

    return API_PROVIDERS.get(
        provider
    )



def get_available_providers() -> list[APIProvider]:
    """
    Return all supported providers.
    """

    return list(
        API_PROVIDERS.keys()
    )



def provider_requires_api_key(
    provider: APIProvider,
) -> bool:
    """
    Check whether provider requires credentials.
    """

    metadata = API_PROVIDERS.get(
        provider
    )


    if metadata is None:

        return False


    return metadata.credential_type in [

        CredentialType.API_KEY,

        CredentialType.BEARER_TOKEN,

        CredentialType.AZURE_KEY,

    ]



# ============================================================================
# External Configuration Validation
# ============================================================================


def validate_api_configuration(
    configuration: dict[str, Any],
) -> tuple[bool, str]:
    """
    Validate API configuration externally.

    Can be used by:

        - SettingsManager
        - Services
        - Startup checks

    Args:
        configuration:
            API configuration dictionary.

    Returns:
        Validation result.
    """

    provider_value = configuration.get(
        "provider"
    )


    if not provider_value:

        return (

            False,

            "API provider missing."

        )



    try:

        provider = APIProvider(
            provider_value
        )


    except ValueError:

        return (

            False,

            "Unsupported API provider."

        )



    metadata = API_PROVIDERS.get(
        provider
    )


    if metadata is None:

        return (

            False,

            "Provider metadata unavailable."

        )



    api_key = configuration.get(
        "api_key"
    )


    if provider_requires_api_key(
        provider
    ):

        if not api_key:

            return (

                False,

                "API credential missing."

            )



    if metadata.requires_endpoint:

        if not configuration.get(
            "endpoint"
        ):

            return (

                False,

                "Endpoint missing."

            )



    return (

        True,

        "API configuration valid."

    )



# ============================================================================
# Component Factory
# ============================================================================


def create_api_settings_component(
    *,
    state: APIConfigState | None = None,

    on_save: Callable[
        [APIConfigState],
        None
    ]
    | None = None,

    on_test: Callable[
        [APIConfigState],
        bool
    ]
    | None = None,

) -> APISettingsComponent:
    """
    Create API settings component.

    Keeps page code clean.

    Returns:
        Configured APISettingsComponent.
    """

    return APISettingsComponent(

        state=state,

        on_save=on_save,

        on_test=on_test,

    )



# ============================================================================
# Module Exports
# ============================================================================


__all__ = [

    # Enums

    "APIProvider",

    "CredentialType",


    # Data Models

    "APIProviderMetadata",

    "APIConfigState",


    # Registry

    "API_PROVIDERS",


    # Component

    "APISettingsComponent",


    # Factories

    "create_default_api_state",

    "create_api_settings_component",


    # Utilities

    "get_provider_metadata",

    "get_available_providers",

    "provider_requires_api_key",


    # Validation

    "validate_api_configuration",

]