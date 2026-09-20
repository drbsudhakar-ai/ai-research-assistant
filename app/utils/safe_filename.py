"""Sanitize uploaded filenames before writing to disk."""

from __future__ import annotations

from pathlib import Path

__all__ = [
    "resolve_upload_path",
    "safe_upload_filename",
]


def safe_upload_filename(
    name: str | None,
    *,
    default: str = "upload.pdf",
) -> str:
    """Return a basename-only filename, rejecting empty or traversal names."""

    candidate = Path(str(name or "")).name.strip()
    if not candidate or candidate in {".", ".."}:
        return default
    return candidate


def resolve_upload_path(upload_dir: Path, filename: str) -> Path:
    """Resolve ``filename`` under ``upload_dir`` or raise ValueError."""

    directory = upload_dir.expanduser().resolve()
    directory.mkdir(parents=True, exist_ok=True)
    target = (directory / safe_upload_filename(filename)).resolve()
    try:
        target.relative_to(directory)
    except ValueError as exc:
        raise ValueError("Invalid upload filename.") from exc
    return target
