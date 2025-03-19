# coding_env.py
import os
from typing import Any, Dict, Optional

from marble.environments.base_env import BaseEnvironment
from marble.environments.coding_utils import (  # register_tester_actions,; register_debugger_actions,; register_analyst_actions
    register_coder_actions,
    register_reviewer_actions,
)


class CodingEnvironment(BaseEnvironment):
    """Enhanced coding environment with comprehensive development tools."""

    def __init__(self, config: Dict[str, Any], name: str = "CodingEnv"):
        """
        Initialize the CodingEnvironment.

        Args:
            config (Dict[str, Any]): Configuration dictionary
            name (str): Name of the environment
        """
        super().__init__(name, config)
        self.config = config

        self.workspace_dir = config.get("workspace_dir", "workspace")
        os.makedirs(self.workspace_dir, exist_ok=True)

        self.register_standard_actions()

    def register_standard_actions(self) -> None:
        """Register all standard actions available in the coding environment."""
        # Register actions based on roles
        register_coder_actions(self)
        register_reviewer_actions(self)
        # register_tester_actions(self)
        # register_debugger_actions(self)
        # register_analyst_actions(self)

    def _get_file_path(self, filename: str, subdir: Optional[str] = None) -> str:
        """
        Constructs the full file path within the workspace.

        Args:
            filename (str): Name of the file
            subdir (Optional[str]): Optional subdirectory within workspace

        Returns:
            str: Full file path
        """
        if subdir:
            full_path = os.path.join(self.workspace_dir, subdir)
            os.makedirs(full_path, exist_ok=True)
            return os.path.join(full_path, filename)
        return os.path.join(self.workspace_dir, filename)
