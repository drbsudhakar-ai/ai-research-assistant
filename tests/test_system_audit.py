"""Focused T005 tests for upload-path safety and live debug-print removal."""

from __future__ import annotations

from pathlib import Path

from app.utils.safe_filename import resolve_upload_path, safe_upload_filename


def test_safe_upload_filename_strips_directories() -> None:
    assert safe_upload_filename("../../etc/passwd") == "passwd"
    assert safe_upload_filename("paper.pdf") == "paper.pdf"
    assert safe_upload_filename("") == "upload.pdf"
    assert safe_upload_filename("..") == "upload.pdf"


def test_resolve_upload_path_stays_inside_upload_dir(tmp_path: Path) -> None:
    target = resolve_upload_path(tmp_path, "../escape.pdf")
    assert target.parent == tmp_path.resolve()
    assert target.name == "escape.pdf"


def test_paper_analyzer_has_no_debug_prints() -> None:
    source = Path("app/agents/paper_analyzer.py").read_text(encoding="utf-8")
    assert "print(" not in source


def test_pipeline_runner_has_no_debug_prints() -> None:
    source = Path("app/core/pipeline/pipeline_runner.py").read_text(encoding="utf-8")
    assert "print(" not in source


def test_analyze_worker_does_not_write_session_state() -> None:
    source = Path("app/ui/pages/analyze.py").read_text(encoding="utf-8")
    worker = source.split("def _analysis_worker")[1].split(
        "def _render_running_analysis"
    )[0]
    assert "st.session_state" not in worker
    assert "_analysis_queue.put" in worker
