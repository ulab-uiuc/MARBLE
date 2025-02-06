import os
import json
import datetime
import subprocess
from typing import Dict, Any
from marble.llms.model_prompting import model_prompting

def extract_python_code(content: str) -> str:
    """
    Extracts Python code from a string that may contain Markdown-style code blocks.

    Args:
        content (str): The input content containing Python code wrapped in Markdown.

    Returns:
        str: Extracted Python code, or the original content if no Markdown-style block is found.
    """
    start_marker = "```python"
    end_marker = "```"
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx + len(start_marker))
    
    if start_idx != -1 and end_idx != -1:
        return content[start_idx + len(start_marker):end_idx].strip()
    return content

def run_and_debug_solution_handler(env, model_name: str, file_path: str = "solution.py") -> Dict[str, Any]:
    """
    Runs the solution.py file, captures any errors, and uses model_prompting to suggest fixes if errors occur.
    Saves error information to error.json and modifies the file to fix the issues.

    Args:
        env: The environment instance
        model_name (str): Name of the LLM model to use
        file_path (str): File path, defaults to solution.py

    Returns:
        Dict[str, Any]: Result of the operation containing run status and suggestions if applicable
    """
    try:
        full_path = os.path.join(env.workspace_dir, os.path.basename(file_path))
        error_path = os.path.join(env.workspace_dir, "error.json")

        if not os.path.exists(full_path):
            return {
                "success": False,
                "error-msg": f"File not found at {full_path}"
            }

        # Extract code from solution.py
        with open(full_path, 'r') as file:
            code_content = file.read()

        # Ensure proper Python code is extracted
        python_code = extract_python_code(code_content)

        # Write extracted Python code back to solution.py
        with open(full_path, 'w') as file:
            file.write(python_code)

        try:
            result = subprocess.run(
                ["python3", full_path],
                capture_output=True,
                text=True,
                check=True
            )
            # If no error occurs
            return {
                "success": True,
                "message": "Code ran successfully without errors.",
                "output": result.stdout
            }

        except subprocess.CalledProcessError as e:
            # Capture error details
            error_data = {
                "file_path": file_path,
                "timestamp": str(datetime.datetime.now()),
                "error_msg": e.stderr,
                "code": python_code
            }

            # Save error details to error.json
            with open(error_path, 'w') as f:
                json.dump(error_data, f, indent=2, ensure_ascii=False)

            # Use model_prompting to generate suggestions to fix the error
            system_prompt_suggestions = (
                "You are a Python debugging assistant. Analyze the following Python code and its error message.\n"
                "Provide actionable suggestions to fix the issue.\n\n"
                f"Code:\n{python_code}\n"
                f"\nError Message:\n{e.stderr}\n"
            )

            user_prompt_suggestions = "Please suggest fixes for the above code based on the error message."

            suggestions_response = model_prompting(
                model_name,
                messages=[
                    {"role": "system", "content": system_prompt_suggestions},
                    {"role": "user", "content": user_prompt_suggestions}
                ],
                return_num=1,
                max_token_num=2048,
                temperature=0.0
            )[0]

            suggestions = suggestions_response.content

            # Use suggestions to modify the code
            system_prompt_fix = (
                "You are a Python developer. Based on the following suggestions, modify the provided code to fix the errors:\n\n"
                f"Suggestions:\n{suggestions}\n\n"
                f"Code:\n{python_code}\n"
            )

            user_prompt_fix = "Please provide the modified version of the code based on the suggestions above."

            fix_response = model_prompting(
                model_name,
                messages=[
                    {"role": "system", "content": system_prompt_fix},
                    {"role": "user", "content": user_prompt_fix}
                ],
                return_num=1,
                max_token_num=2048,
                temperature=0.0
            )[0]

            fixed_code = fix_response.content

            # Save fixed code back to the file
            with open(full_path, 'w') as file:
                file.write(fixed_code)

            return {
                "success": True,
                "message": "Code encountered an error but was successfully debugged and fixed.",
                "error": e.stderr,
                "suggestions": suggestions,
                "fixed_code": fixed_code
            }

    except Exception as ex:
        return {"success": False, "error-msg": str(ex)}

def register_debugger_actions(env):
    """
    Register debugging-related actions in the environment.
    """
    env.register_action(
        "run_and_debug_solution",
        handler=lambda **kwargs: run_and_debug_solution_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "run_and_debug_solution",
                "description": "Runs the solution file, captures errors, and provides suggestions to fix issues",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "model_name": {
                            "type": "string", 
                            "description": "Name of the LLM model to use (e.g., 'gpt-3.5-turbo', 'gpt-4')"
                        },
                        "file_path": {
                            "type": "string",
                            "description": "Path of the solution file to run and debug (optional, defaults to 'solution.py')"
                        }
                    },
                    "required": ["model_name"],
                    "additionalProperties": False
                }
            }
        }
    )
