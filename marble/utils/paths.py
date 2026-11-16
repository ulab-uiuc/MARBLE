"""
Filesystem locations used across MARBLE.

Everything here is derived from the location of the installed package, so the
engine can be launched from any working directory.
"""

import os

# .../MARBLE/marble
MARBLE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# .../MARBLE
REPO_ROOT: str = os.path.dirname(MARBLE_DIR)
# .../MARBLE/data (Minecraft blueprints and runtime state)
DATA_DIR: str = os.path.join(REPO_ROOT, "data")
# .../MARBLE/.cache (Minecraft judge heart-beat / load status)
CACHE_DIR: str = os.path.join(REPO_ROOT, ".cache")


def ensure_parent_dir(file_path: str) -> None:
    """Create the parent directory of ``file_path`` if it does not exist."""
    parent = os.path.dirname(os.path.abspath(file_path))
    os.makedirs(parent, exist_ok=True)
