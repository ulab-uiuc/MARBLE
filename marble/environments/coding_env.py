import os
from typing import Any, Dict
from marble.environments.base_env import BaseEnvironment


class CodingEnvironment(BaseEnvironment):
    def __init__(self, config: Dict[str, Any], name: str="CodingEnv"):
        super().__init__(name, config)
        self.workspace_path = config.get("workspace_path", "/home/zhe36/MARBLE/marble/workspace")
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
        
        self.register_action("analyze_task", self._analyze_task_handler, analyze_task_description)
        self.register_action("implement_code", self._implement_code_handler, implement_code_description)

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
            # Write pure code to solution.py
            with open(os.path.join(self.workspace_path, "solution.py"), "w") as f:
                f.write(code)
            
            # Write documentation to README.md
            with open(os.path.join(self.workspace_path, "README.md"), "w") as f:
                f.write(documentation)
                
            return {
                "success": True,
                "message": "Code and documentation written successfully"
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
            "workspace_path": self.workspace_path
        }