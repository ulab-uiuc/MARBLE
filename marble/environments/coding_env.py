import os
from typing import Any, Dict

from marble.environments.base_env import BaseEnvironment


class CodingEnvironment(BaseEnvironment):
    def __init__(self, config: Dict[str, Any], name: str = "CodingEnv"):
        """
        Initialize the CodingEnvironment.

        Args:
            name (str): The name of the environment.
            config (Dict[str, Any]): Configuration for the environment.
        """
        super().__init__(name, config)
        self.workspace_path = config.get("workspace_path", "/home/zhe36/MARBLE/marble/workspace")
        os.makedirs(self.workspace_path, exist_ok=True)
        
        # Register actions
        self._register_actions()

    def _register_actions(self) -> None:
        """Register all available actions for the coding environment."""
        
        # Action for writing code to file
        write_code_description = {
            "type": "function",
            "function": {
                "name": "write_code",
                "description": "Writes code to a file in the workspace.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Name of the file to write code to",
                        },
                        "code": {
                            "type": "string",
                            "description": "The code content to write",
                        }
                    },
                    "required": ["filename", "code"],
                }
            }
        }
        self.register_action("write_code", self._write_code_handler, write_code_description)

        # Action for reading code from file
        read_code_description = {
            "type": "function",
            "function": {
                "name": "read_code",
                "description": "Reads code from a file in the workspace.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Name of the file to read",
                        }
                    },
                    "required": ["filename"],
                }
            }
        }
        self.register_action("read_code", self._read_code_handler, read_code_description)

        # Action for running tests
        run_test_description = {
            "type": "function",
            "function": {
                "name": "run_test",
                "description": "Runs test cases on the code.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "test_code": {
                            "type": "string",
                            "description": "The test code to execute",
                        }
                    },
                    "required": ["test_code"],
                }
            }
        }
        self.register_action("run_test", self._run_test_handler, run_test_description)

    def _write_code_handler(self, filename: str, code: str) -> Dict[str, Any]:
        """
        Handles writing code to a file.

        Args:
            filename (str): Name of the file to write to.
            code (str): Code content to write.

        Returns:
            Dict[str, Any]: Result of the operation.
        """
        try:
            file_path = os.path.join(self.workspace_path, filename)
            with open(file_path, 'w') as f:
                f.write(code)
            return {
                "success": True,
                "message": f"Code written to {filename}",
                "file_path": file_path
            }
        except Exception as e:
            return {
                "success": False,
                "error-msg": str(e)
            }

    def _read_code_handler(self, filename: str) -> Dict[str, Any]:
        """
        Handles reading code from a file.

        Args:
            filename (str): Name of the file to read from.

        Returns:
            Dict[str, Any]: Result of the operation including the code content.
        """
        try:
            file_path = os.path.join(self.workspace_path, filename)
            with open(file_path, 'r') as f:
                content = f.read()
            return {
                "success": True,
                "content": content,
                "file_path": file_path
            }
        except Exception as e:
            return {
                "success": False,
                "error-msg": str(e)
            }

    def _run_test_handler(self, test_code: str) -> Dict[str, Any]:
        """
        Handles running test cases.

        Args:
            test_code (str): Test code to execute.

        Returns:
            Dict[str, Any]: Result of the test execution.
        """
        try:
            test_file = os.path.join(self.workspace_path, "_temp_test.py")
            with open(test_file, 'w') as f:
                f.write(test_code)
            
            # Execute test in a controlled environment
            import subprocess
            result = subprocess.run(['python', test_file], 
                                 capture_output=True, 
                                 text=True)
            
            os.remove(test_file)  # Clean up
            
            return {
                "success": True,
                "output": result.stdout,
                "errors": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "error-msg": str(e)
            }

    def get_state(self) -> Dict[str, Any]:
        """
        Get the current environment state.

        Returns:
            Dict[str, Any]: The current environment state.
        """
        files = os.listdir(self.workspace_path)
        return {
            "workspace_path": self.workspace_path,
            "files": files
        }