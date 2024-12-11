import os
import json
import datetime
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

def give_advice_and_revise_handler(env, task_description: str, model_name: str, file_path: str = "solution.py") -> Dict[str, Any]:
    """
    Reads solution.py content, provides improvement suggestions based on task description, and revises the code accordingly.
    Saves suggestions to advices.json in the workspace directory and updates the solution file.

    Args:
        env: The environment instance
        task_description (str): Task description
        model_name (str): Name of the LLM model to use
        file_path (str): File path, defaults to solution.py

    Returns:
        Dict[str, Any]: Result of the operation containing advice and revised code
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

        # Extract actual Python code if wrapped in Markdown
        python_code = extract_python_code(existing_code)

        # Step 1: Generate advice
        system_prompt_advice = (
            "You are a Python code reviewer. Check if the given code satisfies the task description provided below. "
            "If there are unmet requirements based on the task description, provide actionable suggestions in the format: "
            "'You should ... as the task description ...'.\n\n"
            f"Task Description:\n{task_description}\n"
            "\nCode to Review:\n"
            f"{python_code}\n"
        )

        user_prompt_advice = "Check if the code meets the task description and provide actionable suggestions in the specified format."

        response_advice = model_prompting(
            model_name,
            messages=[
                {"role": "system", "content": system_prompt_advice},
                {"role": "user", "content": user_prompt_advice}
            ],
            return_num=1,
            max_token_num=2048,
            temperature=0.0
        )[0]

        # Save advice to advices.json
        advice_data = {
            "task_description": task_description,
            "file_path": file_path,
            "timestamp": str(datetime.datetime.now()),
            "suggestions": response_advice.content
        }

        # Append new advice to advices.json
        existing_advices = []
        if os.path.exists(advice_path):
            try:
                with open(advice_path, 'r') as f:
                    existing_advices = json.load(f)
            except json.JSONDecodeError:
                pass
        existing_advices.append(advice_data)
        with open(advice_path, 'w') as f:
            json.dump(existing_advices, f, indent=2, ensure_ascii=False)

        # Use the latest advice for revision
        latest_suggestions = advice_data["suggestions"]

        # Step 2: Revise the code
        system_prompt_revise = (
            "You are a Python developer. Review and improve the existing code based on the task description.\n"
            "Your improvements should maintain code clarity and follow Python best practices.\n"
            "After your improvements, your conclusion must be in this exact format:\n"
            "'The task description is: [repeat the full task description here]. Based on this task description, "
            "I have improved the solution.'\n\n"
            f"Task Description:\n{task_description}\n"
            "\nExisting Code:\n"
            f"{python_code}\n"
            "\nPrevious Code Review Suggestions:\n"
            f"{latest_suggestions}\n"
            "\nPlease consider these suggestions while improving the code."
        )

        user_prompt_revise = "Please provide the improved version of this code, taking into account any previous suggestions if provided."

        response_revise = model_prompting(
            model_name,
            messages=[
                {"role": "system", "content": system_prompt_revise},
                {"role": "user", "content": user_prompt_revise}
            ],
            return_num=1,
            max_token_num=2048,
            temperature=0.0
        )[0]

        improved_code = response_revise.content

        # Save revised code
        with open(full_path, 'w') as file:
            file.write(improved_code)

        return {
            "success": True,
            "message": f"Code review and revision completed. Suggestions saved to {advice_path} and solution revised at {full_path}",
            "original_code": python_code,
            "suggestions": latest_suggestions,
            "improved_code": improved_code
        }

    except Exception as e:
        return {"success": False, "error-msg": str(e)}

def register_reviewer_actions(env):
    """
    Register coding-related actions in the environment.
    """
    env.register_action(
        "give_advice_and_revise",
        handler=lambda **kwargs: give_advice_and_revise_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "give_advice_and_revise",
                "description": "Review existing solution file, provide improvement suggestions, and revise the code accordingly",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_description": {
                            "type": "string", 
                            "description": "Description of the task to review and implement"
                        },
                        "model_name": {
                            "type": "string", 
                            "description": "Name of the LLM model to use (e.g., 'gpt-3.5-turbo', 'gpt-4')"
                        },
                        "file_path": {
                            "type": "string",
                            "description": "Path of the solution file to review and revise (optional, defaults to 'solution.py')"
                        }
                    },
                    "required": ["task_description", "model_name"],
                    "additionalProperties": False
                }
            }
        }
    )
