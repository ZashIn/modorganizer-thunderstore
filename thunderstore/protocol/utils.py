import os
from pathlib import Path


def abs_norm_path(path: str | Path) -> Path:
    """Normalized, absolute path without resolving symlinks."""
    return Path(os.path.abspath(path))
