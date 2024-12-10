import os
import json
from typing import Dict, Any
from marble.llms.model_prompting import model_prompting

def extract_code_content(code_path: str) -> str:
    """从文件中提取代码内容"""
    try:
        with open(code_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content.strip()
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return ""

def create_review_prompt(code: str, task_description: str = "") -> str:
    """创建review的system prompt"""
    system_prompt = (
        "You are a strict code reviewer. Review the following code according to the task description and provide feedback.\n"
        "After your detailed review, your conclusion must be in this exact format:\n"
        "'The task description is: [repeat the full task description here]. Based on this task description, "
        "it looks good to me (LGTM)' OR 'it looks bad to me (LBTM)'.\n\n"
        f"Task Description:\n{task_description}\n"
        "\nCode to review:\n"
        f"{code}\n"
        "\nRemember: Your final conclusion must restate the complete task description before giving LGTM/LBTM judgment."
    )
    return system_prompt

def get_model_review(system_prompt: str, model_name: str = "gpt-3.5-turbo") -> Dict[str, Any]:
    """获取模型的代码审查结果"""
    try:
        response = model_prompting(
            model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Please review the code."}
            ],
            return_num=1,
            max_token_num=2048,
            temperature=0.0
        )[0]
        
        return {
            "success": True,
            "review_result": response.content,
            "model_name": model_name
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "model_name": model_name
        }

def save_result(result: Dict[str, Any], output_path: str):
    """保存结果到JSON文件"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {output_path}")
    except Exception as e:
        print(f"Error saving results: {str(e)}")

def main():
    # 文件路径
    solution_path = "/home/zhe36/MARBLE/marble/workspace/solution.py"
    extraction_path = "/home/zhe36/MARBLE/marble/workspace/extraction.py"
    result_path = "/home/zhe36/MARBLE/marble/workspace/result.json"
    
    # 提取代码
    code = extract_code_content(solution_path)
    
    # 创建system prompt
    task_description = "Build a basic ping pong game with simple AI opponent"
    prompt = create_review_prompt(code, task_description)
    
    # 保存prompt到extraction.py（用于检查）
    try:
        with open(extraction_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"Prompt saved to {extraction_path}")
    except Exception as e:
        print(f"Error saving prompt: {str(e)}")
        return

    # 获取模型review结果
    result = get_model_review(prompt)
    
    # 保存结果到result.json
    save_result(result, result_path)

if __name__ == "__main__":
    main()