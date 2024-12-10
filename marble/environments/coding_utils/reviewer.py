import os
import json
import datetime
from typing import Dict, Any, Optional
from marble.llms.model_prompting import model_prompting

def give_advice_handler(env, task_description: str, model_name: str, file_path: str = "solution.py") -> Dict[str, Any]:
    """
    Reads solution.py content and provides improvement suggestions based on task description.
    Saves suggestions to advices.json in the workspace directory.

    Args:
        env: The environment instance
        task_description (str): Task description
        model_name (str): Name of the LLM model to use
        file_path (str): File path, defaults to solution.py

    Returns:
        Dict[str, Any]: Result of the operation containing advice
    """
    try:
        full_path = os.path.join(env.workspace_dir, os.path.basename(file_path))
        advice_path = os.path.join(env.workspace_dir, "advices.json")
        
        if not os.path.exists(full_path):
            return {
                "success": False,
                "error-msg": f"File not found at {full_path}"
            }

        # Read existing code
        with open(full_path, 'r') as file:
            existing_code = file.read()

        system_prompt = (
            "You are a Python code reviewer. Review the existing code based on the task description.\n"
            "Provide clear, actionable suggestions for improvement without modifying the code.\n"
            "Focus on:\n"
            "1. Code quality and best practices\n"
            "2. Performance optimization opportunities\n"
            "3. Potential bugs or edge cases\n"
            "4. Documentation and readability\n"
            "Format your response as a structured list of suggestions.\n\n"
            f"Task Description:\n{task_description}\n"
            "\nCode to Review:\n"
            f"{existing_code}\n"
        )

        user_prompt = "Please provide a detailed code review with specific suggestions for improvement."

        response = model_prompting(
            model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            return_num=1,
            max_token_num=2048,
            temperature=0.0
        )[0]

        # Prepare advice data
        advice_data = {
            "task_description": task_description,
            "file_path": file_path,
            "timestamp": str(datetime.datetime.now()),
            "suggestions": response.content
        }

        # Load existing advices if file exists
        existing_advices = []
        if os.path.exists(advice_path):
            try:
                with open(advice_path, 'r') as f:
                    existing_advices = json.load(f)
            except json.JSONDecodeError:
                existing_advices = []

        # Append new advice
        if not isinstance(existing_advices, list):
            existing_advices = []
        existing_advices.append(advice_data)

        # Save updated advices
        with open(advice_path, 'w') as f:
            json.dump(existing_advices, f, indent=2, ensure_ascii=False)

        return {
            "success": True,
            "message": f"Code review completed and saved to {advice_path}",
            "code": existing_code,
            "suggestions": response.content
        }

    except Exception as e:
        return {"success": False, "error-msg": str(e)}

def register_reviewer_actions(env):
    """
    Register coding-related actions in the environment.
    """
    env.register_action(
        "give_advice",
        handler=lambda **kwargs: give_advice_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "give_advice",
                "description": "Review existing solution file and provide improvement suggestions without modifying the code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_description": {
                            "type": "string", 
                            "description": "Description of the task to review"
                        },
                        "model_name": {
                            "type": "string", 
                            "description": "Name of the LLM model to use (e.g., 'gpt-3.5-turbo', 'gpt-4')"
                        },
                        "file_path": {
                            "type": "string",
                            "description": "Path of the solution file to review (optional, defaults to 'solution.py')"
                        }
                    },
                    "required": ["task_description", "model_name"],
                    "additionalProperties": False
                }
            }
        }
    )