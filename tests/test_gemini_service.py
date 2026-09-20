"""Tests for the Google Gemini provider adapter."""

from __future__ import annotations

import httpx

from app.services.gemini_service import GeminiService


def _service(handler: httpx.MockTransport) -> GeminiService:
    return GeminiService(
        api_key="test-key",
        model="gemini-test",
        retries=1,
        client=httpx.Client(transport=handler),
    )


def test_generate_maps_gemini_response_to_llm_contract() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["x-goog-api-key"] == "test-key"
        assert "test-key" not in str(request.url)
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {
                        "content": {
                            "parts": [{"text": "A sufficiently detailed analysis."}]
                        }
                    }
                ],
                "usageMetadata": {
                    "promptTokenCount": 10,
                    "candidatesTokenCount": 5,
                    "totalTokenCount": 15,
                },
            },
        )

    result = _service(httpx.MockTransport(handler)).generate(
        system_prompt="Analyze research accurately.",
        user_prompt="Analyze this paper.",
    )

    assert result.provider == "gemini"
    assert result.model == "gemini-test"
    assert result.total_tokens == 15
    assert "detailed analysis" in result.content


def test_is_available_checks_configured_model() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/models/gemini-test")
        return httpx.Response(
            200,
            json={
                "name": "models/gemini-test",
                "supportedGenerationMethods": ["generateContent"],
            },
        )

    assert _service(httpx.MockTransport(handler)).is_available() is True


def test_generate_reports_blocked_response_without_exposing_key() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"promptFeedback": {"blockReason": "SAFETY"}},
        )

    service = _service(httpx.MockTransport(handler))
    try:
        service.generate(system_prompt="system prompt", user_prompt="user prompt")
    except RuntimeError as exc:
        assert "test-key" not in str(exc)
        assert isinstance(exc.__cause__, ValueError)
    else:
        raise AssertionError("Expected blocked Gemini response to fail.")
