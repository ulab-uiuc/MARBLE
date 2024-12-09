import os
from typing import Any, Dict, Optional
from marble.llms.model_prompting import model_prompting

def create_solution_handler(env, task_description: str, model_name: str, file_path: str = "solution.py") -> Dict[str, Any]:
    """
    Creates solution.py file and generates content based on task description.

    Args:
        env: The environment instance
        task_description (str): Task description
        model_name (str): Name of the LLM model to use
        file_path (str): File path, defaults to solution.py

    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        # Construct full path using workspace directory
        workspace_dir = env.workspace_dir  # This should be "marble/workspace"
        full_path = os.path.join(workspace_dir, file_path)
        
        # Create workspace directory if it doesn't exist
        os.makedirs(workspace_dir, exist_ok=True)

        system_prompt = (
            "You are a Python developer. Create a solution based on the following task description.\n"
            "Your code should be clean, well-documented, and follow Python best practices.\n"
            "After your implementation, your conclusion must be in this exact format:\n"
            "'The task description is: [repeat the full task description here]. Based on this task description, "
            "I have implemented the solution.'\n\n"
            f"Task Description:\n{task_description}\n"
        )

        user_prompt = "Please write the complete Python code for this task."

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

        # Extract the code from the response
        code_content = response.content

        # Create the file and write the content
        with open(full_path, 'w') as file:
            file.write(code_content)

        return {
            "success": True,
            "message": f"Solution file created at {full_path}",
            "code": code_content
        }

    except Exception as e:
        return {"success": False, "error-msg": str(e)}

def revise_solution_handler(env, task_description: str, model_name: str, file_path: str = "solution.py") -> Dict[str, Any]:
    """
    Reads solution.py content and improves/modifies it based on task description.

    Args:
        env: The environment instance
        task_description (str): Task description
        model_name (str): Name of the LLM model to use
        file_path (str): File path, defaults to solution.py

    Returns:
        Dict[str, Any]: Result of the operation
    """
    try:
        # Construct full path using workspace directory
        workspace_dir = env.workspace_dir  # This should be "marble/workspace"
        full_path = os.path.join(workspace_dir, file_path)
        
        # Create workspace directory if it doesn't exist
        os.makedirs(workspace_dir, exist_ok=True)

        # Create file if it doesn't exist
        if not os.path.exists(full_path):
            return create_solution_handler(env, task_description, model_name, file_path)

        # Read existing code
        with open(full_path, 'r') as file:
            existing_code = file.read()

        system_prompt = (
            "You are a Python developer. Review and improve the existing code based on the task description.\n"
            "Your improvements should maintain code clarity and follow Python best practices.\n"
            "After your improvements, your conclusion must be in this exact format:\n"
            "'The task description is: [repeat the full task description here]. Based on this task description, "
            "I have improved the solution.'\n\n"
            f"Task Description:\n{task_description}\n"
            "\nExisting Code:\n"
            f"{existing_code}\n"
        )

        user_prompt = "Please provide the improved version of this code."

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

        # Extract the improved code from the response
        improved_code = response.content

        # revise the file with improved code
        with open(full_path, 'w') as file:
            file.write(improved_code)

        return {
            "success": True,
            "message": f"Solution file revised at {full_path}",
            "original_code": existing_code,
            "improved_code": improved_code
        }

    except Exception as e:
        return {"success": False, "error-msg": str(e)}

def register_coder_actions(env):
    """
    Register coding-related actions in the environment.
    """
    env.register_action(
        "create_solution",
        handler=lambda **kwargs: create_solution_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "create_solution",
                "description": "Create a new solution file with initial code based on task description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_description": {
                            "type": "string", 
                            "description": "Description of the task to implement"
                        },
                        "model_name": {
                            "type": "string", 
                            "description": "Name of the LLM model to use (e.g., 'gpt-3.5-turbo', 'gpt-4')"
                        },
                        "file_path": {
                            "type": "string",
                            "description": "Path where the solution file should be created (optional, defaults to 'solution.py')"
                        }
                    },
                    "required": ["task_description", "model_name"],
                    "additionalProperties": False
                }
            }
        }
    )

    env.register_action(
        "revise_solution",
        handler=lambda **kwargs: revise_solution_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "revise_solution",
                "description": "revise existing solution file by improving/modifying code based on task description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_description": {
                            "type": "string", 
                            "description": "Description of the task to implement"
                        },
                        "model_name": {
                            "type": "string", 
                            "description": "Name of the LLM model to use (e.g., 'gpt-3.5-turbo', 'gpt-4')"
                        },
                        "file_path": {
                            "type": "string",
                            "description": "Path of the solution file to revise (optional, defaults to 'solution.py')"
                        }
                    },
                    "required": ["task_description", "model_name"],
                    "additionalProperties": False
                }
            }
        }
    )