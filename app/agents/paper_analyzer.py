"""
===============================================================================
Project      : AI Research Assistant
Module       : Research Agent
Agent Name   : Paper Analyzer
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Coordinates research paper analysis by combining the system prompt,
    paper analysis prompt, and the selected language model service.

Responsibilities:
    • Load prompts
    • Prepare the final prompt
    • Invoke the LLM service
    • Return the generated analysis

Last Updated:
    2026-06-28
===============================================================================
"""

from app.prompts.common.system_prompt import SYSTEM_PROMPT

from app.prompts.research.paper_analysis_prompt import (
    PAPER_ANALYSIS_PROMPT
)

from app.services.ollama_service import OllamaService


class PaperAnalyzer:
    """
    AI Agent responsible for research paper analysis.
    """

    def __init__(self):

        self.system_prompt = SYSTEM_PROMPT

        self.analysis_prompt = PAPER_ANALYSIS_PROMPT

        self.llm_service = OllamaService()

        self.agent_name = "Paper Analyzer"

        self.version = "1.0.0"

    def analyze(self, paper_text):
        """
        Analyze the given research paper.

        Parameters
        ----------
        paper_text : str
            Extracted text from the research paper.

        Returns
        -------
        str
            AI-generated analysis.
        """

        if not paper_text.strip():
            return "No paper text was provided."

        user_prompt = f"""
{self.analysis_prompt}

===============================================================================
RESEARCH PAPER
===============================================================================

{paper_text}
"""

        response = self.llm_service.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt
        )

        return response