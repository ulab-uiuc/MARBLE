import os
import json
import datetime
import re
from typing import Dict, Any
from marble.llms.model_prompting import model_prompting
from ruamel.yaml import YAML

def give_advice_and_revise_handler(env, task_description: str, model_name: str) -> Dict[str, Any]:
    """
    Reads solution.py content, provides improvement suggestions based on task description, and revises the code accordingly.
    
    Args:
        env: The environment instance.
        task_description (str): Task description (not used, will read from config).
        model_name (str): Name of the LLM model to use.

    Returns:
        Dict[str, Any]: Result of the operation containing advice and revised code.
    """
    try:
        full_path = os.path.join(env.workspace_dir, "solution.py")
        
        if not os.path.exists(full_path):
            return {
                "success": False,
                "error-msg": "Please use create_solution first to generate the solution file"
            }
            
        with open(full_path, 'r') as file:
            existing_code = file.read()
            
        if not existing_code.strip() or "forgot to include the task description" in existing_code:
            return {
                "success": False,
                "error-msg": "Solution file is empty or contains invalid code. Please use create_solution first to generate valid code"
            }


        config_path = "/opt/dlami/nvme/zhe/MARBLE/marble/configs/coding_config/coding_config.yaml"
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

        # Step 1: Generate single most important suggestion
        system_prompt_advice = (
            "You are a Python code reviewer. Review the code based on the task description and requirements, "
            "and provide ONE most critical suggestion.\n"
            "Focus priority: 1) Missing functionality 2) Existing issues 3) Code optimization\n"
            "Format your response as:\n"
            "LOCATION: [describe the specific part of code that needs change]\n"
            "ISSUE: [briefly describe the problem]\n"
            "SUGGESTION: [briefly describe how to fix it]\n\n"
            f"Task Description:\n{full_task_description}\n\n"
            f"Implementation Requirements:\n{requirements}\n\n"
            "Code to Review:\n"
            f"{existing_code}\n"
        )

        user_prompt_advice = "Provide ONE most critical suggestion in the specified format."

        response_advice = model_prompting(
            model_name,
            messages=[
                {"role": "system", "content": system_prompt_advice},
                {"role": "user", "content": user_prompt_advice}
            ],
            return_num=1,
            max_token_num=4096,
            temperature=0.0
        )[0]

        # Step 2: Generate modification strategy
        system_prompt_strategy = (
            "You are a Python developer. Based on the suggestion, provide specific modification strategy.\n"
            "Your response MUST be a valid JSON object with the following structure:\n"
            "{\n"
            '  "strategies": [\n'
            '    {\n'
            '      "action": "[add/delete/replace]",\n'
            '      "target": {\n'
            '        "code": "exact code to modify",\n'
            '        "before_context": "3-5 lines before target",\n'
            '        "after_context": "3-5 lines after target"\n'
            '      },\n'
            '      "new_code": "code to be added/replaced (empty if delete)"\n'
            '    }\n'
            '  ]\n'
            '}\n'
            'Do not include any additional text before or after the JSON object.\n\n'
            f"Task Description:\n{full_task_description}\n"
            "\nExisting Code:\n"
            f"{existing_code}\n"
            "\nSuggestion:\n"
            f"{response_advice.content}\n"
        )

        user_prompt_strategy = "Provide specific modification strategies in the specified JSON format."

        response_strategy = model_prompting(
            model_name,
            messages=[
                {"role": "system", "content": system_prompt_strategy},
                {"role": "user", "content": user_prompt_strategy}
            ],
            return_num=1,
            max_token_num=4096,
            temperature=0.0
        )[0]


        try:
            content = response_strategy.content.strip()
            if not content:
                return {
                    "success": False,
                    "error-msg": "Empty response from model"
                }
            

            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_content = content[json_start:json_end]
                strategy = json.loads(json_content)
            else:
                return {
                    "success": False,
                    "error-msg": "No valid JSON found in model response"
                }
            
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error-msg": f"Invalid JSON format: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error-msg": f"Error processing model response: {str(e)}"
            }

        # Step 3: Apply modifications
        modified_code = existing_code
        for mod in strategy['strategies']:
            target_code = mod['target']['code']
            before_ctx = mod['target']['before_context']
            after_ctx = mod['target']['after_context']
            
            # Find the location using context
            pattern = f"{re.escape(before_ctx)}(.*?){re.escape(after_ctx)}"
            match = re.search(pattern, modified_code, re.DOTALL)
            
            if match:
                if mod['action'] == 'add':
                    # Insert after the matched context
                    insert_pos = match.end()
                    modified_code = modified_code[:insert_pos] + "\n" + mod['new_code'] + modified_code[insert_pos:]
                elif mod['action'] == 'delete':
                    # Delete the matched content
                    modified_code = modified_code[:match.start(1)] + modified_code[match.end(1):]
                elif mod['action'] == 'replace':
                    # Replace the matched content
                    modified_code = modified_code[:match.start(1)] + mod['new_code'] + modified_code[match.end(1):]

        # Save modifications
        with open(full_path, 'w') as file:
            file.write(modified_code)

        # Save suggestion and strategy
        advice_data = {
            "task_description": full_task_description,
            "file_path": "solution.py",
            "timestamp": str(datetime.datetime.now()),
            "suggestion": response_advice.content,
            "strategy": strategy
        }

        existing_advices = []
        advice_path = os.path.join(env.workspace_dir, "advices.json")
        if os.path.exists(advice_path):
            try:
                with open(advice_path, 'r') as f:
                    existing_advices = json.load(f)
            except json.JSONDecodeError:
                pass
        existing_advices.append(advice_data)
        with open(advice_path, 'w') as f:
            json.dump(existing_advices, f, indent=2, ensure_ascii=False)

        return {
            "success": True,
            "message": f"Code review and revision completed. Suggestions saved to {advice_path} and solution revised at {full_path}",
            "original_code": existing_code,
            "suggestion": response_advice.content,
            "strategy": strategy
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
                "description": "Review existing solution.py file, provide improvement suggestions, and revise the code accordingly",
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
                            "default": "meta-llama/Llama-3.1-70B-Instruct"
                        }
                    },
                    "required": ["task_description", "model_name"],
                    "additionalProperties": False
                }
            }
        }
    )
