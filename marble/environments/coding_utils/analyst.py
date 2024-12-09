# coding_utils/analyst.py
import ast
from typing import Any, Dict, Optional

def create_file_handler(env, filename: str, content: str, subdir: Optional[str] = None) -> Dict[str, Any]:
    try:
        file_path = env._get_file_path(filename, subdir)
        with open(file_path, 'w') as f:
            f.write(content)
        return {
            "success": True,
            "message": f"File created successfully: {file_path}",
            "file_path": file_path
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def register_analyst_actions(env):
    env.register_action(
        "create_file",
        handler=lambda **kwargs: create_file_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "create_file",
                "description": "Creates a new file in the workspace with specified content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string", "description": "Name of the file to create"},
                        "content": {"type": "string", "description": "Content to write to the file"},
                        "subdir": {"type": "string", "description": "Optional subdirectory within workspace"}
                    },
                    "required": ["filename", "content"]
                }
            }
        }
    )