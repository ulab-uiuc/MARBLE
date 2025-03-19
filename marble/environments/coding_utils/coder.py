import os
import re
from typing import Any, Dict, Optional
from marble.llms.model_prompting import model_prompting
from ruamel.yaml import YAML

def create_solution_handler(env, task_description: str, model_name: str, file_path: str = "solution.py") -> Dict[str, Any]:
    """
    Creates solution.py file and generates content based on task description.
    
    The generated code will include inline comments explaining the file,
    and the final output will be enclosed in a Markdown code block with the language
    specified as python. Only the code within the code block (without the markdown markers)
    will be stored in the file.

    Args:
        env: The environment instance.
        task_description (str): Task description.
        model_name (str): Name of the LLM model to use.
        file_path (str): File path, defaults to solution.py.

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        file_path = "solution.py"
        full_path = os.path.join(env.workspace_dir, file_path)
        
        if os.path.exists(full_path):
            return {
                "success": False,
                "error-msg": f"Solution file already exists at {full_path}. Operation aborted."
            }
            
        config_path = "marble/configs/coding_config/coding_config.yaml"
        if not os.path.exists(config_path):
            return {
                "success": False,
                "error-msg": f"Config file not found at {config_path}"
            }
            
        yaml = YAML()
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.load(f)
        
        full_task_description = config['task']['content']
        
        requirements_start = "1. Implementation requirements:\n"
        requirements_end = "\n\n2. Project structure:"
        requirements = full_task_description[
            full_task_description.find(requirements_start) + len(requirements_start):
            full_task_description.find(requirements_end)
        ].strip()

        os.makedirs(env.workspace_dir, exist_ok=True)

        system_prompt = (
            "You are a Python developer. Create a solution based on the following task description.\n"
            "Your code should be clean, well-documented, and follow Python best practices.\n"
            "Include explanations of the code and its functionality as inline comments within the code.\n"
            "Your final output must be enclosed in a markdown code block with the language specified as python.\n"
            "Ensure that nothing besides the code is inside the markdown code block.\n"
            f"Task Description:\n{full_task_description}\n\n"
            f"Implementation Requirements:\n{requirements}\n"
        )

        user_prompt = "Please write the complete Python code for this task."

        response = model_prompting(
            model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            return_num=1,
            max_token_num=4096,
            temperature=0.0
        )[0]

        code_content = response.content

        code_block_match = re.search(r"```python(.*?)```", code_content, re.DOTALL)
        if code_block_match:
            code_content = code_block_match.group(1).strip()
        else:
            code_content = code_content.strip()


        with open(full_path, 'w') as file:
            file.write(code_content)

        return {
            "success": True,
            "message": f"Solution file created at {full_path}",
            "code": code_content
        }

    except Exception as e:
        return {"success": False, "error-msg": str(e)}

# 以下 revise_solution_handler 函数也可以做类似的修改以确保输出纯代码，
# 这里只是作为参考，现已注释掉：
#
# def revise_solution_handler(env, task_description: str, model_name: str, file_path: str = "solution.py") -> Dict[str, Any]:
#     """
#     Reads solution.py content and improves/modifies it based on task description.
#     If advices.json exists, incorporates the suggestions into the improvement process.
#
#     Args:
#         env: The environment instance.
#         task_description (str): Task description.
#         model_name (str): Name of the LLM model to use.
#         file_path (str): File path, defaults to solution.py.
#
#     Returns:
#         Dict[str, Any]: Result of the operation.
#     """
#     try:
#         full_path = os.path.join(env.workspace_dir, os.path.basename(file_path))
#         advice_path = os.path.join(env.workspace_dir, "advices.json")
#         
#         # Create workspace directory if it doesn't exist
#         os.makedirs(env.workspace_dir, exist_ok=True)
#
#         # Create file if it doesn't exist
#         if not os.path.exists(full_path):
#             return create_solution_handler(env, task_description, model_name, file_path)
#
#         # Read existing code
#         with open(full_path, 'r') as file:
#             existing_code = file.read()
#
#         # Try to load suggestions from advices.json if it exists
#         suggestions = ""
#         if os.path.exists(advice_path):
#             try:
#                 with open(advice_path, 'r') as f:
#                     advice_data = json.load(f)
#                     if isinstance(advice_data, list) and len(advice_data) > 0:
#                         suggestions = advice_data[0].get("suggestions", "")
#             except (json.JSONDecodeError, KeyError):
#                 suggestions = ""
#
#         # Construct system prompt with suggestions if available
#         system_prompt = (
#             "You are a Python developer. Review and improve the existing code based on the task description.\n"
#             "Your improvements should maintain code clarity and follow Python best practices.\n"
#             "Include explanations of your modifications as inline comments within the code.\n"
#             "Your final output must be enclosed in a markdown code block with the language specified as python.\n"
#             "Ensure that only the code is within the code block.\n"
#             "At the very end of your code, include the following exact conclusion as a comment:\n"
#             "# The task description is: [repeat the full task description here]. Based on this task description, I have improved the solution.\n\n"
#             f"Task Description:\n{task_description}\n"
#             "\nExisting Code:\n"
#             f"{existing_code}\n"
#         )
#
#         if suggestions:
#             system_prompt += (
#                 "\nPrevious Code Review Suggestions:\n"
#                 f"{suggestions}\n"
#                 "\nPlease consider these suggestions while improving the code.\n"
#             )
#
#         user_prompt = "Please provide the improved version of this code, taking into account any previous suggestions if provided."
#
#         response = model_prompting(
#             model_name,
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_prompt}
#             ],
#             return_num=1,
#             max_token_num=4096,
#             temperature=0.0
#         )[0]
#
#         improved_code = response.content
#
#         # 提取 ```python ... ``` 内的代码
#         code_block_match = re.search(r"```python(.*?)```", improved_code, re.DOTALL)
#         if code_block_match:
#             improved_code = code_block_match.group(1).strip()
#         else:
#             improved_code = improved_code.strip()
#
#         # 更新文件内容
#         with open(full_path, 'w') as file:
#             file.write(improved_code)
#
#         return {
#             "success": True,
#             "message": f"Solution file revised at {full_path}",
#             "original_code": existing_code,
#             "improved_code": improved_code,
#             "previous_suggestions": suggestions if suggestions else "No previous suggestions found"
#         }
#
#     except Exception as e:
#         return {"success": False, "error-msg": str(e)}

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
                "description": "Creates solution.py file and generates content based on task description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_description": {
                            "type": "string",
                            "description": "Description of the task (will be read from config file)"
                        },
                        "model_name": {
                            "type": "string",
                            "description": "Name of the LLM model to use",
                            "default": "gpt-3.5-turbo"
                        }
                    },
                    "required": ["task_description", "model_name"],
                    "additionalProperties": False
                }
            }
        }
    )

    # 如果需要，也可以类似地注册 revise_solution 动作（目前该函数为注释状态）
    # env.register_action(
    #     "revise_solution",
    #     handler=lambda **kwargs: revise_solution_handler(env, **kwargs),
    #     description={
    #         "type": "function",
    #         "function": {
    #             "name": "revise_solution",
    #             "description": "Revise existing solution file by improving/modifying code based on task description",
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {
    #                     "task_description": {
    #                         "type": "string", 
    #                         "description": "Description of the task to implement"
    #                     },
    #                     "model_name": {
    #                         "type": "string", 
    #                         "description": "Name of the LLM model to use"
    #                     },
    #                     "file_path": {
    #                         "type": "string",
    #                         "description": "Path of the solution file to revise (optional, defaults to 'solution.py')"
    #                     }
    #                 },
    #                 "required": ["task_description", "model_name"],
    #                 "additionalProperties": False
    #             }
    #         }
    #     }
    # )
