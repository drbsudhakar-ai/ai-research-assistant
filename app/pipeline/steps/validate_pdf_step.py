"""
===============================================================================
Project      : AI Research Assistant
Module       : Validate PDF Pipeline Step
File         : validate_pdf_step.py
Version      : 1.0.0

Description:
    Validates uploaded research paper PDF before analysis.

===============================================================================
"""

from __future__ import annotations

from pathlib import Path


from app.core.pipeline.base_pipeline_step import (
    BasePipelineStep,
)

from app.core.pipeline.pipeline_context import (
    PipelineContext,
)


__all__ = [
    "ValidatePdfStep",
]


class ValidatePdfStep(BasePipelineStep):
    """
    Pipeline step responsible for PDF validation.
    """


    VERSION = "1.0.0"


    MAX_FILE_SIZE_MB = 100


    # ------------------------------------------------------------------
    # Step metadata
    # ------------------------------------------------------------------

    @property
    def name(
        self,
    ) -> str:
        """
        Step name.
        """

        return "Validate PDF"



    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Validate uploaded PDF.

        Parameters
        ----------
        context:
            Shared pipeline execution context.

        Raises
        ------
        ValueError
            If PDF validation fails.
        """


        pdf_path = context.data.get(
            "pdf_path"
        )


        if not pdf_path:
            raise ValueError(
                "PDF path is missing"
            )


        path = Path(
            pdf_path
        )


        #
        # File existence
        #
        if not path.exists():

            raise FileNotFoundError(
                f"PDF file not found: {path}"
            )


        #
        # Extension validation
        #
        if path.suffix.lower() != ".pdf":

            raise ValueError(
                "Only PDF files are supported"
            )


        #
        # Size validation
        #
        file_size_mb = (
            path.stat().st_size
            /
            (1024 * 1024)
        )


        if file_size_mb > self.MAX_FILE_SIZE_MB:

            raise ValueError(
                (
                    "PDF size exceeds maximum limit "
                    f"({self.MAX_FILE_SIZE_MB} MB)"
                )
            )


        #
        # Store validation result
        #
        context.data["pdf_validation"] = {

            "valid": True,

            "filename": path.name,

            "path": str(path),

            "size_mb": round(
                file_size_mb,
                2,
            ),

        }


        #
        # Progress notification
        #
        self._report_progress(
            context,
            "PDF validation completed",
        )



    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _report_progress(
        self,
        context: PipelineContext,
        message: str,
    ) -> None:
        """
        Notify optional progress reporter.
        """

        reporter = getattr(
            context,
            "progress_reporter",
            None,
        )


        if reporter is None:
            return


        reporter.update(
            message=message,
        )