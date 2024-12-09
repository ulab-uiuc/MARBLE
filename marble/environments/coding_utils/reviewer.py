# coding_utils/reviewer.py
from typing import Any, Dict, Optional
from marble.llms.model_prompting import model_prompting

def review_code_handler(env, code: str, model_name: str, review_criteria: Optional[str] = None) -> Dict[str, Any]:
    try:
        task_description = env.config.get("task", {}).get("content", "")
        
        system_prompt = (
            "You are a strict code reviewer. Review the following code according to the task description and provide feedback.\n"
            "After your detailed review, your conclusion must be in this exact format:\n"
            "'The task description is: [repeat the full task description here]. Based on this task description, "
            "it looks good to me (LGTM)' OR 'it looks bad to me (LBTM)'.\n\n"
            f"Task Description:\n{task_description}\n"
            "\nRemember: Your final conclusion must restate the complete task description before giving LGTM/LBTM judgment."
        )
        
        if review_criteria:
            system_prompt += f"\nSpecific review criteria: {review_criteria}"

        user_prompt = f"Please review this code:\n```\n{code}\n```"

        response = model_prompting(
            model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            return_num=1,
            max_token_num=1024,
            temperature=0.0
        )[0]

        review_result = response.content
        is_lgtm = "LGTM" in review_result.upper()

        return {
            "success": True,
            "is_lgtm": is_lgtm,
            "review_feedback": review_result
        }
        
    except Exception as e:
        return {"success": False, "error-msg": str(e)}

def register_reviewer_actions(env):
    env.register_action(
        "review_code",
        handler=lambda **kwargs: review_code_handler(env, **kwargs),
        description={
            "type": "function",
            "function": {
                "name": "review_code",
                "description": "Review code and provide LGTM/LBTM feedback",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Code to be reviewed"},
                        "model_name": {
                            "type": "string", 
                            "description": "Name of the LLM model to use (e.g., 'gpt-3.5-turbo', 'gpt-4')"
                        },
                        "review_criteria": {
                            "type": "string", 
                            "description": "Specific criteria for code review (optional)"
                        }
                    },
                    "required": ["code", "model_name"],
                    "additionalProperties": False
                }
            }
        }
    )
