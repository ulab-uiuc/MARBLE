import os
from typing import Any, Dict
from marble.environments.base_env import BaseEnvironment


class CodingEnvironment(BaseEnvironment):
    def __init__(self, config: Dict[str, Any], name: str="CodingEnv"):
        super().__init__(name, config)
        self.workspace_path = config.get("workspace_path", "workspace")
        self._ensure_workspace_exists()
        
        analyze_task_description = {
            "type": "function",
            "function": {
                "name": "analyze_task",
                "description": "Analyzes the coding task and provides implementation suggestions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "The coding task to analyze",
                        },
                        "analysis": {
                            "type": "string",
                            "description": "The analysis and implementation suggestions in markdown format",
                        }
                    },
                    "required": ["task", "analysis"],
                    "additionalProperties": False
                }
            }
        }
        
        implement_code_description = {
            "type": "function",
            "function": {
                "name": "implement_code",
                "description": "Implements the code based on analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The pure implementation code",
                        },
                        "documentation": {
                            "type": "string",
                            "description": "The documentation in markdown format",
                        }
                    },
                    "required": ["code", "documentation"],
                    "additionalProperties": False
                }
            }
        }

        test_analysis_description = {
            "type": "function",
            "function": {
                "name": "update_analysis_with_test",
                "description": "Updates analysis with test cases strategy",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "test_analysis": {
                            "type": "string",
                            "description": "The test cases analysis in markdown format",
                        }
                    },
                    "required": ["test_analysis"],
                    "additionalProperties": False
                }
            }
        }
        
        implement_test_description = {
            "type": "function",
            "function": {
                "name": "implement_test",
                "description": "Implements test cases based on analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "test_code": {
                            "type": "string",
                            "description": "The test implementation code",
                        }
                    },
                    "required": ["test_code"],
                    "additionalProperties": False
                }
            }
        }
        
        self.register_action("analyze_task", self._analyze_task_handler, analyze_task_description)
        self.register_action("implement_code", self._implement_code_handler, implement_code_description)
        self.register_action("update_analysis_with_test", self._update_analysis_handler, test_analysis_description)
        self.register_action("implement_test", self._implement_test_handler, implement_test_description)

    def _analyze_task_handler(self, task: str, analysis: str) -> Dict[str, Any]:
        try:
            with open(os.path.join(self.workspace_path, "analysis.md"), "w") as f:
                f.write(analysis)
            
            self.state["task_analysis"] = analysis
            return {
                "success": True,
                "analysis": analysis
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _implement_code_handler(self, code: str, documentation: str) -> Dict[str, Any]:
        try:
            with open(os.path.join(self.workspace_path, "solution.py"), "w") as f:
                f.write(code)
            

            with open(os.path.join(self.workspace_path, "README.md"), "w") as f:
                f.write(documentation)
            
            self.state["implementation_code"] = code
            self.state["documentation"] = documentation
                
            return {
                "success": True,
                "message": "Code and documentation written successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _update_analysis_handler(self, test_analysis: str) -> Dict[str, Any]:
        try:
            with open(os.path.join(self.workspace_path, "analysis.md"), "r") as f:
                current_analysis = f.read()
            
            updated_analysis = current_analysis + "\n\n## Test Strategy\n" + test_analysis
            
            with open(os.path.join(self.workspace_path, "analysis.md"), "w") as f:
                f.write(updated_analysis)
            
            self.state["test_analysis"] = test_analysis
            return {
                "success": True,
                "analysis": updated_analysis
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _implement_test_handler(self, test_code: str) -> Dict[str, Any]:
        try:
            with open(os.path.join(self.workspace_path, "test_solution.py"), "w") as f:
                f.write(test_code)
            
            self.state["test_code"] = test_code
            return {
                "success": True,
                "message": "Test code written successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _ensure_workspace_exists(self) -> None:
        if not os.path.exists(self.workspace_path):
            os.makedirs(self.workspace_path)

    def get_state(self) -> Dict[str, Any]:
        return {
            "task_analysis": self.state.get("task_analysis", ""),
            "implementation_code": self.state.get("implementation_code", ""),
            "documentation": self.state.get("documentation", ""),
            "test_analysis": self.state.get("test_analysis", ""),
            "test_code": self.state.get("test_code", ""),
            "workspace_path": self.workspace_path
        }