# coding_utils/tester.py
import sys
import pytest
from typing import Any, Dict, Optional

def run_tests_handler(env, test_file: str, subdir: Optional[str] = None, 
                     verbosity: int = 2) -> Dict[str, Any]:
    try:
        test_path = env._get_file_path(test_file, subdir)
        
        # Add workspace to Python path
        sys.path.insert(0, env.workspace_dir)
        
        # Run pytest programmatically
        pytest_args = [
            test_path,
            f"--verbosity={verbosity}",
            "-p", "no:warnings",  # Disable warning capture
            "--tb=short"  # Short traceback
        ]
        
        test_output = pytest.main(pytest_args)
        
        # Remove workspace from Python path
        sys.path.pop(0)
        
        return {
            "success": test_output == pytest.ExitCode.OK,
            "exit_code": test_output,
            "test_file": test_path
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def register_tester_actions(env):
    env.register_action(
        "run_tests",
        handler=lambda **kwargs: run_tests_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "run_tests",
                "description": "Runs tests for the specified file or directory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "test_file": {"type": "string", "description": "Test file to run"},
                        "subdir": {"type": "string", "description": "Optional subdirectory within workspace"},
                        "verbosity": {"type": "integer", "description": "Test output verbosity level"}
                    },
                    "required": ["test_file"]
                }
            }
        }
    )
