"""Architecture import and composition baseline tests."""

from __future__ import annotations

from app.core.pipeline import (
    BasePipelineStep,
    Pipeline,
    PipelineBuilder,
    PipelineContext,
    PipelineResult,
    PipelineRunner,
    PipelineStage,
    PipelineStep,
    ResearchAnalysisPipeline,
)
from app.core.pipeline.analysis_pipeline import AnalysisPipeline
from app.core.pipeline.pipeline_context import PipelineContext as Context
from app.core.progress import (
    ProgressEvent,
    ProgressManager,
    ProgressStage,
)


class _DummyStep(BasePipelineStep):
    def __init__(self, name: str) -> None:
        self._name = name
        self.ran = False

    @property
    def name(self) -> str:
        return self._name

    def execute(self, context: Context) -> None:
        self.ran = True
        context.set("ran", self._name)


def test_pipeline_step_alias_is_not_a_second_abc() -> None:
    assert PipelineStep is BasePipelineStep
    assert issubclass(_DummyStep, BasePipelineStep)
    assert issubclass(_DummyStep, PipelineStep)


def test_analysis_pipeline_is_legacy_alias() -> None:
    assert AnalysisPipeline is ResearchAnalysisPipeline


def test_canonical_pipeline_exports_exist() -> None:
    assert Pipeline is not None
    assert PipelineBuilder is not None
    assert PipelineContext is not None
    assert PipelineResult is not None
    assert PipelineRunner is not None
    assert PipelineStage is not None


def test_pipeline_construction_requires_base_pipeline_step() -> None:
    step = _DummyStep("one")
    pipeline = PipelineBuilder().add_step(step).build()
    assert isinstance(pipeline, Pipeline)
    assert pipeline.step_count == 1
    assert isinstance(pipeline.steps[0], BasePipelineStep)

    try:
        Pipeline(steps=["not-a-step"])  # type: ignore[list-item]
    except TypeError:
        pass
    else:
        raise AssertionError("Pipeline must reject non-BasePipelineStep values")


def test_pipeline_runner_executes_canonical_steps() -> None:
    step = _DummyStep("one")
    result = PipelineRunner(Pipeline([step])).run(Context())
    assert result.success
    assert step.ran
    assert result.context.get("ran") == "one"


def test_progress_event_uses_stage_not_step() -> None:
    event = ProgressEvent(
        stage=ProgressStage.STARTING,
        message="starting",
        percentage=0,
    )
    assert event.stage is ProgressStage.STARTING
    assert not hasattr(event, "step")


def test_progress_manager_satisfies_reporter_protocol() -> None:
    manager = ProgressManager()
    assert callable(manager.update)
    manager.update(message="working", percentage=10, stage=ProgressStage.ANALYZING)
    state = manager.get_state()
    assert state.percentage == 10
    assert state.stage is ProgressStage.ANALYZING


def test_cancellation_token_request_is_not_worker_stopped() -> None:
    manager = ProgressManager()
    assert not manager.cancellation_token.is_cancelled()
    manager.cancel()
    assert manager.cancellation_token.is_cancelled()
    assert manager.is_cancelled()


def test_research_pipeline_requires_configured_steps() -> None:
    try:
        ResearchAnalysisPipeline()
    except TypeError as exc:
        assert "ResearchAnalysisPipelineFactory" in str(exc)
    else:
        raise AssertionError("expected TypeError")
